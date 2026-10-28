"""FHIR-Pakete und Quelldateien reproduzierbar beschaffen.

Pakete liegen in einem eigenen Cache `.pakete/<id>#<version>/package` im Repository (über FHIR_PAKETE änderbar) —
nicht im gemeinsamen `~/.fhir/packages`, weil andere Werkzeuge dort Pakete anders befüllen (ältere Fassungen,
Zusatzordner) und die Prüfung gegen die Sperrdatei sonst vom Rechner abhinge.
Die Sperrdatei hält je Paket einen Inhalts-Hash über alle JSON-Dateien des Pakets (ohne die Indexdateien,
die Werkzeuge nachträglich anlegen) — damit sind ein frischer Download und ein vorhandener Cache gleich prüfbar.
Quelldateien (von IG-Seiten) liegen im Repo; die Sperrdatei hält Herkunfts-URL und SHA-256.
Lokale Pakete (`lokale_pakete` in projekt.toml) liegen eingecheckt im Projektordner; `holen` und die Sperrdatei
überspringen sie, Modell, Auflösung und Validierung nutzen sie wie ein Paket aus dem Cache.
Der HL7 Validator bekommt einen eigenen Cache `.validator/.fhir/packages` (über FHIR_VALIDATOR_HOME änderbar) mit
seinem vollständigen Paketbestand samt Abhängigkeiten; dieselbe Sperrdatei prüft ihn (siehe `validieren.py`).
"""
import hashlib
import io
import os
import re
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

from .grundlagen import SPERRDATEI, WURZEL, json_laden, json_schreiben

REGISTRY = 'https://packages.fhir.org/'


def cache():
    return Path(os.environ['FHIR_PAKETE']).expanduser() if os.environ.get('FHIR_PAKETE') else WURZEL / '.pakete'


def validator_home():
    """Benutzerverzeichnis des HL7 Validators (`-Duser.home`): darin `.fhir/packages` und `.fhir/fhir-settings.json`."""
    return (Path(os.environ['FHIR_VALIDATOR_HOME']).expanduser() if os.environ.get('FHIR_VALIDATOR_HOME')
            else WURZEL / '.validator')


def validator_cache():
    return validator_home() / '.fhir' / 'packages'


def ordner(spec):
    """Ordner eines Pakets: `<id>#<version>` im Cache; ein lokales Paket (Path) ist selbst der Ordner."""
    return spec if isinstance(spec, Path) else cache() / spec


def projektpakete(konfig):
    """Pakete eines Projekts in der Reihenfolge des Vorrangs: lokale Pakete zuerst, dann `pakete`."""
    return [*konfig.get('lokale_ordner', []), *konfig['pakete']]


def bezeichnung(spec):
    """`<id>#<version>` — für lokale Pakete aus ihrer package.json, ohne Pfad (Berichte bleiben rechnerunabhängig)."""
    if isinstance(spec, Path):
        p = json_laden(spec / 'package' / 'package.json')
        return f'{p["name"]}#{p["version"]}'
    return spec


def inhalt_hash(wurzel):
    m = hashlib.sha256()
    basis = wurzel / 'package'
    for dp, dn, fn in os.walk(basis):
        dn.sort()
        for f in sorted(fn):
            if f.startswith('.') or not f.endswith('.json'):
                continue
            p = Path(dp) / f
            m.update(p.relative_to(wurzel).as_posix().encode() + b'\0' + p.read_bytes() + b'\0')
    return m.hexdigest()


def datei_hash(pfad):
    return hashlib.sha256(Path(pfad).read_bytes()).hexdigest()


def sperre_laden():
    return json_laden(SPERRDATEI) if SPERRDATEI.exists() else {'pakete': {}, 'quellen': {}}


def _holen(url):
    anfrage = urllib.request.Request(url, headers={'Accept': 'application/tar+gzip', 'User-Agent': 'modellexplorer'})
    with urllib.request.urlopen(anfrage, timeout=120) as r:
        return r.read()


def paket_sicherstellen(spec, sperre, aktualisieren=False, pruefen=True, basis=None):
    """Paket in den Cache (`basis`, sonst `.pakete`) holen, falls nötig, und gegen die Sperrdatei prüfen."""
    pid, _, version = spec.partition('#')
    ziel = basis / spec if basis else ordner(spec)
    url = sperre['pakete'].get(spec, {}).get('url') or f'{REGISTRY}{pid}/{version}'
    if not (ziel / 'package' / 'package.json').exists():
        print(f'  hole {spec}', file=sys.stderr)
        daten = _holen(url)
        # erst vollständig entpacken, dann umbenennen: ein abgebrochener Lauf hinterlässt kein halbes Paket
        neu = ziel.with_name(ziel.name + '.neu')
        for o in (neu, ziel):
            if o.exists():
                shutil.rmtree(o)
        neu.mkdir(parents=True)
        with tarfile.open(fileobj=io.BytesIO(daten), mode='r:gz') as tar:
            tar.extractall(neu, filter='data')
        neu.rename(ziel)
    if not pruefen:
        return
    ist = inhalt_hash(ziel)
    soll = sperre['pakete'].get(spec, {}).get('inhalt_sha256')
    if soll and ist != soll and not aktualisieren:
        raise SystemExit(f'Paket {spec}: Inhalt weicht von der Sperrdatei ab ({ist[:12]} statt {soll[:12]}). '
                         f'Cache-Ordner {ziel} löschen und neu holen.')
    if not soll or aktualisieren:
        sperre['pakete'][spec] = {'url': url, 'inhalt_sha256': ist}


# FHIR-Kernpakete: Der Validator lädt sie nicht als Abhängigkeit nach (den Kern seiner FHIR-Version lädt er selbst)
KERNPAKET = re.compile(r'hl7\.fhir\.r\d+b?\.core')
FESTE_VERSION = re.compile(r'\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?')


def abhaengigkeiten(paketordner, platzhalter=None):
    """Abhängigkeiten aus der package.json als `<id>#<version>`, ohne FHIR-Kernpakete. Versionen müssen fest sein:
    `current`, `dev` oder Platzhalter wie `1.5.x` löst der Validator sonst beim Paketserver auf. Ein Platzhalter gilt
    nur mit Festlegung in `platzhalter` (`{'<id>#1.5.x': '1.5.0'}`); ohne Netz nimmt der Validator dann die
    passende Fassung im Cache."""
    p = json_laden(paketordner / 'package' / 'package.json')
    aus = []
    for pid, version in sorted(p.get('dependencies', {}).items()):
        if KERNPAKET.fullmatch(pid):
            continue
        if not FESTE_VERSION.fullmatch(version):
            fest = (platzhalter or {}).get(f'{pid}#{version}')
            if not fest:
                raise SystemExit(f'{p["name"]}#{p["version"]}: Abhängigkeit {pid} ohne feste Version ({version}) — '
                                 f'Fassung festlegen (PLATZHALTER in werkzeuge/mx/validieren.py)')
            muster = re.escape(version).replace('x', r'\d+') + r'(-.+)?'
            if not (FESTE_VERSION.fullmatch(fest) and re.fullmatch(muster, fest)):
                raise SystemExit(f'Festlegung {pid}#{version} → {fest} passt nicht zum Platzhalter')
            version = fest
        aus.append(f'{pid}#{version}')
    return aus


def huelle_sicherstellen(start, basis, sperre, aktualisieren=False, platzhalter=None):
    """Pakete samt allen Abhängigkeiten in den Cache `basis` holen und gegen die Sperrdatei prüfen.
    `start`: `<id>#<version>` oder Ordner lokaler Pakete (nur deren Abhängigkeiten). Ergebnis: sortierte Paketliste."""
    offen, gesehen = list(start), set()
    while offen:
        spec = offen.pop()
        if spec in gesehen:
            continue
        gesehen.add(spec)
        if isinstance(spec, Path):
            offen += abhaengigkeiten(spec, platzhalter)
            continue
        paket_sicherstellen(spec, sperre, aktualisieren, basis=basis)
        offen += abhaengigkeiten(basis / spec, platzhalter)
    return sorted(s for s in gesehen if not isinstance(s, Path))


def cache_bereinigen(basis, bestand):
    """Paketordner in `basis` entfernen, die nicht zum Bestand gehören (samt Sperrdateien des Validators)."""
    for o in sorted(basis.iterdir()):
        name = o.name[:-5] if o.name.endswith('.lock') else o.name
        if '#' in name and name not in bestand:
            print(f'  entferne {o.name} aus {basis}', file=sys.stderr)
            shutil.rmtree(o) if o.is_dir() else o.unlink()


def quelle_pruefen(pfad, url, sperre, aktualisieren=False):
    """Quelldatei gegen die Sperrdatei prüfen. Fehlt sie noch (neue Quelle), wird sie geladen und aufgenommen —
    so nimmt `holen` neue Quellen auf, ohne die vorhandenen neu zu laden."""
    rel = Path(pfad).relative_to(WURZEL).as_posix()
    if aktualisieren or not Path(pfad).exists():
        Path(pfad).parent.mkdir(parents=True, exist_ok=True)
        print(f'  hole {url}', file=sys.stderr)
        Path(pfad).write_bytes(_holen(url))
    ist = datei_hash(pfad)
    soll = sperre['quellen'].get(rel, {}).get('sha256')
    if soll and ist != soll and not aktualisieren:
        raise SystemExit(f'Quelle {rel}: SHA-256 weicht von der Sperrdatei ab')
    sperre['quellen'][rel] = {'url': url, 'sha256': ist}


def sperre_schreiben(sperre):
    sperre['pakete'] = dict(sorted(sperre['pakete'].items()))
    sperre['quellen'] = dict(sorted(sperre['quellen'].items()))
    json_schreiben(SPERRDATEI, sperre)


def definitionen(specs):
    """Alle StructureDefinitions der Pakete, erste Fundstelle gewinnt (Reihenfolge der Konfiguration).
    `specs`: `<id>#<version>` aus dem Cache oder Ordner lokaler Pakete (siehe `projektpakete`)."""
    sds = {}
    for spec in specs:
        basis = ordner(spec) / 'package'
        if not basis.exists():
            if isinstance(spec, Path):
                raise SystemExit(f'Lokales Paket {spec} ohne Ordner package/')
            raise SystemExit(f'Paket {spec} fehlt im Cache — zuerst `python3 werkzeuge/mx.py holen`')
        for f in sorted(basis.glob('StructureDefinition-*.json')):
            try:
                d = json_laden(f)
            except ValueError:
                continue
            if 'snapshot' in d:
                sds.setdefault(d['url'], d)
    return sds
