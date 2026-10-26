"""FHIR-Pakete und Quelldateien reproduzierbar beschaffen.

Pakete liegen in einem eigenen Cache `.pakete/<id>#<version>/package` im Repository (über FHIR_PAKETE änderbar) —
nicht im gemeinsamen `~/.fhir/packages`, weil andere Werkzeuge dort Pakete anders befüllen (ältere Fassungen,
Zusatzordner) und die Prüfung gegen die Sperrdatei sonst vom Rechner abhinge.
Die Sperrdatei hält je Paket einen Inhalts-Hash über alle JSON-Dateien des Pakets (ohne die Indexdateien,
die Werkzeuge nachträglich anlegen) — damit sind ein frischer Download und ein vorhandener Cache gleich prüfbar.
Quelldateien (von IG-Seiten) liegen im Repo; die Sperrdatei hält Herkunfts-URL und SHA-256.
Lokale Pakete (`lokale_pakete` in projekt.toml) liegen eingecheckt im Projektordner; `holen` und die Sperrdatei
überspringen sie, Modell, Auflösung und Validierung nutzen sie wie ein Paket aus dem Cache.
"""
import hashlib
import io
import os
import sys
import tarfile
import urllib.request
from pathlib import Path

from .grundlagen import SPERRDATEI, WURZEL, json_laden, json_schreiben

REGISTRY = 'https://packages.fhir.org/'


def cache():
    return Path(os.environ['FHIR_PAKETE']).expanduser() if os.environ.get('FHIR_PAKETE') else WURZEL / '.pakete'


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


def paket_sicherstellen(spec, sperre, aktualisieren=False, pruefen=True):
    """Paket in den Cache holen (falls nötig) und gegen die Sperrdatei prüfen."""
    pid, _, version = spec.partition('#')
    ziel = ordner(spec)
    url = sperre['pakete'].get(spec, {}).get('url') or f'{REGISTRY}{pid}/{version}'
    if not (ziel / 'package' / 'package.json').exists():
        print(f'  hole {spec}', file=sys.stderr)
        daten = _holen(url)
        ziel.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(daten), mode='r:gz') as tar:
            tar.extractall(ziel, filter='data')
    if not pruefen:
        return
    ist = inhalt_hash(ziel)
    soll = sperre['pakete'].get(spec, {}).get('inhalt_sha256')
    if soll and ist != soll and not aktualisieren:
        raise SystemExit(f'Paket {spec}: Inhalt weicht von der Sperrdatei ab ({ist[:12]} statt {soll[:12]}). '
                         f'Cache-Ordner {ziel} löschen und neu holen.')
    if not soll or aktualisieren:
        sperre['pakete'][spec] = {'url': url, 'inhalt_sha256': ist}


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
