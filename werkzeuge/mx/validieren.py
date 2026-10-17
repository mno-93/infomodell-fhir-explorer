"""Beispieldateien mit dem HL7 FHIR Validator prüfen — je Projekt mit den Paketen aus `[validierung]`.

Java: $JAVA_HOME/bin/java oder `java` im Pfad. Validator: $VALIDATOR_JAR oder ~/.fhir/validator_cli.jar.
Ohne Terminologieserver (`-tx n/a`); Meldungen, die nur mit Server auswertbar sind, stehen begründet als Ausnahme
in der Projektkonfiguration. Ausnahmen ohne Treffer werden als Hinweis gemeldet.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from .grundlagen import AUSGABE
from .konfig import projekt_laden

DATEI_EXT = 'http://hl7.org/fhir/StructureDefinition/operationoutcome-file'


def _java():
    jh = os.environ.get('JAVA_HOME')
    return str(Path(jh) / 'bin' / 'java') if jh else 'java'


def _jar():
    return os.environ.get('VALIDATOR_JAR', str(Path('~/.fhir/validator_cli.jar').expanduser()))


def _meldungen(ergebnis):
    oos = [e['resource'] for e in ergebnis.get('entry', [])] if ergebnis.get('resourceType') == 'Bundle' else [ergebnis]
    for oo in oos:
        datei = next((x.get('valueString') for x in oo.get('extension', []) if x.get('url') == DATEI_EXT), '?')
        for i in oo.get('issue', []):
            if i.get('severity') in ('error', 'fatal'):
                text = (i.get('details') or {}).get('text') or i.get('diagnostics') or ''
                ort = ', '.join(i.get('expression', []) or i.get('location', []))
                yield Path(datei).name, f'{ort}: {text}'


def projekt(pid):
    k = projekt_laden(pid)
    v = k.get('validierung')
    dateien = [str(k['ordner'] / b['datei']) for b in k['beispiele'] if b.get('datei')]
    if not v or not dateien:
        print(f'{pid}: nichts zu validieren')
        return 0
    with tempfile.TemporaryDirectory() as tmp:
        aus = Path(tmp) / 'ergebnis.json'
        befehl = [_java(), '-jar', _jar(), *dateien, '-version', k.get('fhir', '4.0.1'), '-tx', 'n/a',
                  '-output', str(aus)]
        if v.get('erweiterungen'):
            befehl += ['-allow-example-urls', 'true']
            for e in v['erweiterungen']:
                befehl += ['-extension', e]
        for p in v['pakete']:
            befehl += ['-ig', p]
        print(f'{pid}: {len(dateien)} Dateien, Pakete {", ".join(v["pakete"])}', flush=True)
        r = subprocess.run(befehl, capture_output=True, text=True)
        if not aus.exists():
            print(r.stdout[-3000:], r.stderr[-3000:], sep='\n')
            return 1
        ergebnis = json.loads(aus.read_text(encoding='utf-8'))
    ausnahmen = v.get('ausnahmen', [])
    getroffen, fehler = set(), []
    for datei, text in _meldungen(ergebnis):
        a = next((i for i, a in enumerate(ausnahmen) if re.search(a['muster'], text)), None)
        if a is None:
            fehler.append(f'{datei} — {text}')
        else:
            getroffen.add(a)
    for i, a in enumerate(ausnahmen):
        if i not in getroffen:
            print(f'  Hinweis: Ausnahme ohne Treffer: {a["muster"]}')
    AUSGABE.mkdir(exist_ok=True)
    (AUSGABE / f'validierung-{pid}.txt').write_text('\n'.join(fehler) + '\n', encoding='utf-8')
    for f in fehler:
        print('  ' + f)
    print(f'{pid}: {len(fehler)} Fehler, {len(getroffen)} Ausnahme(n) genutzt')
    return 1 if fehler else 0


def alle(pids):
    return 1 if any([projekt(p) for p in pids]) else 0


if __name__ == '__main__':
    sys.exit(alle(sys.argv[1:]))
