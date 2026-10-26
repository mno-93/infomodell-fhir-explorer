"""Lokales Paket eines Projekts aus FSH neu erzeugen — mit SUSHI (`npm install -g fsh-sushi`), nicht Teil des Baus.

Projektordner:  sushi-config.yaml   Paket-Id, Version, Canonical, Abhängigkeiten (SUSHI-Format)
                fsh/*.fsh           Quelltext
                <paket>/package/    Ergebnis, eingecheckt: package.json und StructureDefinitions mit Snapshot

SUSHI erwartet den Quelltext unter `input/fsh/`; deshalb wird in einem temporären Ordner gebaut
(`sushi build <tmp> --snapshot`). Die Snapshots braucht der Modellexplorer (Modell, Zuordnung, Strukturprüfung);
der HL7 Validator liest dasselbe Paket mit `-ig <paket>/package`. package.json entsteht aus sushi-config.yaml.
"""
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .grundlagen import json_laden, json_schreiben
from .konfig import projekt_laden


def sushi_config(text):
    """Die einfachen Angaben aus sushi-config.yaml: `schlüssel: wert` und eine Ebene darunter (dependencies)."""
    aus, block = {}, None
    for zeile in text.splitlines():
        if not zeile.strip() or zeile.lstrip().startswith('#'):
            continue
        m = re.match(r'^(\s*)([\w.-]+):\s*(.*?)\s*$', zeile)
        if not m:
            continue
        einzug, schluessel, wert = m.groups()
        wert = wert.strip('"\'')
        if not einzug:
            block = None
            if wert:
                aus[schluessel] = wert
            else:
                block = aus.setdefault(schluessel, {})
        elif block is not None and wert:
            block[schluessel] = wert
    return aus


def paket_json(cfg):
    return {
        'name': cfg['id'], 'version': cfg['version'], 'type': 'fhir.ig', 'canonical': cfg['canonical'],
        'title': cfg.get('title') or cfg.get('name', cfg['id']), 'description': cfg.get('description', ''),
        'fhirVersions': [cfg.get('fhirVersion', '4.0.1')], 'dependencies': dict(sorted(cfg.get('dependencies', {}).items())),
    }


def bauen(pid):
    k = projekt_laden(pid, lokal_pruefen=False)
    f = k.get('fsh')
    if not f:
        raise SystemExit(f'{pid}: kein Abschnitt [fsh] in projekt.toml')
    quelle, ziel = k['ordner'] / f.get('quelle', 'fsh'), k['ordner'] / f['paket'] / 'package'
    config = k['ordner'] / f.get('config', 'sushi-config.yaml')
    sushi = shutil.which('sushi')
    if not sushi:
        raise SystemExit('SUSHI nicht gefunden — `npm install -g fsh-sushi`')
    cfg = sushi_config(config.read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / 'input' / 'fsh').mkdir(parents=True)
        for q in sorted(quelle.glob('*.fsh')):
            shutil.copy(q, t / 'input' / 'fsh' / q.name)
        shutil.copy(config, t / 'sushi-config.yaml')
        r = subprocess.run([sushi, 'build', str(t), '--snapshot', '-o', str(t / 'aus')],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        print('\n'.join(z for z in r.stdout.splitlines() if re.match(r'^(error|warn)\b', z) or 'Errors' in z))
        if r.returncode:
            print(r.stdout[-4000:], r.stderr[-2000:], sep='\n')
            return 1
        neu = sorted((t / 'aus' / 'fsh-generated' / 'resources').glob('*.json'))
        if not neu:
            raise SystemExit(f'{pid}: SUSHI hat keine Ressourcen erzeugt')
        ziel.mkdir(parents=True, exist_ok=True)
        for alt in ziel.glob('*.json'):
            alt.unlink()
        for d in neu:
            json_schreiben(ziel / d.name, json_laden(d))
    json_schreiben(ziel / 'package.json', paket_json(cfg))
    print(f'{pid}: {len(neu)} Ressourcen nach {ziel.relative_to(k["ordner"]).as_posix()}/ geschrieben '
          f'({cfg["id"]}#{cfg["version"]})')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(bauen(sys.argv[1]))
