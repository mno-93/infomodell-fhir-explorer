"""Beispieldateien mit dem HL7 FHIR Validator prüfen — je Projekt mit den Paketen aus `[validierung]` und den
lokalen Paketen des Projekts (`-ig <ordner>`).

Java: $JAVA_HOME/bin/java oder `java` im Pfad. Validator: $VALIDATOR_JAR oder ~/.fhir/validator_cli.jar.
Ohne Terminologieserver (`-tx n/a`); Meldungen, die nur mit Server auswertbar sind, stehen begründet als Ausnahme
in der Projektkonfiguration. Ausnahmen ohne Treffer werden als Hinweis gemeldet. Exit-Code ≠ 0 bei Fehlern
(error, fatal), die keine begründete Ausnahme sind.

Ergebnis: `berichte/<projekt>.validierung.json` — eingecheckt und deterministisch: Meldungen sortiert, ohne
Zeitstempel und ohne absolute Pfade, Meldungstexte englisch (JVM-Sprache und Validator-Locale fest), damit
Windows, Linux und die CI dieselbe Datei schreiben. `bauen` liest die Datei (ohne Java) und zeigt das Ergebnis im
Prüfbericht und in der Oberfläche. Dazu für die CI-Ablage `ausgabe/validierung-<projekt>.txt` mit den offenen Fehlern.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from .grundlagen import AUSGABE, BERICHTE, WURZEL, json_laden, json_schreiben
from .konfig import projekt_laden
from .pakete import bezeichnung

EXT = 'http://hl7.org/fhir/StructureDefinition/'
DATEI_EXT = EXT + 'operationoutcome-file'
ZEILE_EXT = EXT + 'operationoutcome-issue-line'
KENNUNG_EXT = EXT + 'operationoutcome-message-id'
# Englische Meldungstexte unabhängig von der Spracheinstellung des Rechners
JVM_OPTIONEN = ['-Duser.language=en', '-Duser.country=US']
LOCALE = 'en-US'
RANG = {'fatal': 0, 'error': 1, 'warning': 2}
# Teile von Meldungen, die von der Netzantwort abhängen (z. B. Profil unter einer Beispiel-URL nachladen):
# vereinheitlichen, damit das Ergebnis nicht davon abhängt, was ein fremder Server gerade ausliefert
NETZABHAENGIG = [(re.compile(r'(could not be found), and fetching it resulted in the error .*$', re.S),
                  r'\g<1>; fetching it failed (response details omitted)')]


def _java():
    jh = os.environ.get('JAVA_HOME')
    return str(Path(jh) / 'bin' / 'java') if jh else 'java'


def _jar():
    return os.environ.get('VALIDATOR_JAR', str(Path('~/.fhir/validator_cli.jar').expanduser()))


def datei(pid):
    return BERICHTE / f'{pid}.validierung.json'


def datei_hash(pfad):
    """SHA-256 einer Beispieldatei — Beispiele sind mit `-text` eingecheckt, also auf jedem Rechner bytegleich."""
    return hashlib.sha256(Path(pfad).read_bytes()).hexdigest()


def ausnahme_kennung(a, i):
    return a.get('id') or f'ausnahme-{i + 1}'


def _version(ausgabe):
    m = re.search(r'FHIR Validation tool Version (\S+)', ausgabe)
    return m.group(1) if m else os.environ.get('VALIDATOR_VERSION', 'unbekannt')


def _bereinigen(text):
    """Absolute Pfade (Repository, Benutzerverzeichnis) in Meldungstexten durch relative ersetzen, `/` als Trenner;
    netzabhängige Einzelheiten vereinheitlichen."""
    for muster, ersatz in NETZABHAENGIG:
        text = muster.sub(ersatz, text)
    for basis, ersatz in ((WURZEL, ''), (Path.home(), '~/')):
        for form in sorted({str(basis), basis.as_posix()}):
            text = re.sub(re.escape(form) + r'[\\/]?([^\s\'"()\[\]]*)',
                          lambda m: ersatz + m.group(1).replace('\\', '/'), text, flags=re.I)
    return text


def _ext(x, url, feld):
    return next((e.get(feld) for e in x.get('extension', []) if e.get('url') == url), None)


def meldungen(ergebnis):
    """Meldungen aus der Ausgabe des Validators (OperationOutcome oder Bundle davon):
    [{datei, stufe, ort, zeile, text, kennung}] — `datei` wie auf der Kommandozeile übergeben."""
    oos = [e['resource'] for e in ergebnis.get('entry', [])] if ergebnis.get('resourceType') == 'Bundle' else [ergebnis]
    aus = []
    for oo in oos:
        d = _ext(oo, DATEI_EXT, 'valueString') or '?'
        for i in oo.get('issue', []):
            aus.append({
                'datei': d, 'stufe': i.get('severity', ''),
                'ort': _bereinigen(', '.join(i.get('expression', []) or i.get('location', []))),
                'zeile': _ext(i, ZEILE_EXT, 'valueInteger'),
                'text': _bereinigen((i.get('details') or {}).get('text') or i.get('diagnostics') or ''),
                'kennung': _ext(i, KENNUNG_EXT, 'valueString'),
            })
    return aus


def auswerten(k, roh, version):
    """Meldungen je Beispiel zählen, Ausnahmen zuordnen, sortieren → Inhalt von `berichte/<projekt>.validierung.json`."""
    v = k['validierung']
    ausnahmen = v.get('ausnahmen', [])
    nach_datei = {}
    for b in k['beispiele']:
        if b.get('datei'):
            nach_datei[(k['ordner'] / b['datei']).resolve().as_posix().lower()] = b
    treffer = [0] * len(ausnahmen)
    je = {b['id']: {'id': b['id'], 'datei': b['datei'], 'sha256': datei_hash(k['ordner'] / b['datei']),
                    'fehler': 0, 'ausnahmen': 0, 'warnungen': 0, 'hinweise': 0, 'meldungen': []}
          for b in k['beispiele'] if b.get('datei')}
    for m in roh:
        b = nach_datei.get(Path(m['datei']).resolve().as_posix().lower())
        if b is None:
            raise SystemExit(f'{k["id"]}: Meldung zu unbekannter Datei {m["datei"]}')
        e = je[b['id']]
        if m['stufe'] == 'information':
            e['hinweise'] += 1
            continue
        if m['stufe'] not in RANG:
            continue
        eintrag = {x: m[x] for x in ('stufe', 'ort', 'zeile', 'text', 'kennung') if m[x] is not None}
        if m['stufe'] == 'warning':
            e['warnungen'] += 1
        else:
            e['fehler'] += 1
            a = next((i for i, a in enumerate(ausnahmen) if re.search(a['muster'], f'{m["ort"]}: {m["text"]}')), None)
            if a is not None:
                treffer[a] += 1
                e['ausnahmen'] += 1
                eintrag['ausnahme'] = ausnahme_kennung(ausnahmen[a], a)
        e['meldungen'].append(eintrag)
    for e in je.values():
        e['meldungen'].sort(key=lambda x: (RANG[x['stufe']], x['ort'], x.get('zeile') or 0, x['text']))
    beispiele = [je[b['id']] for b in k['beispiele'] if b['id'] in je]
    summe = {f: sum(e[f] for e in beispiele) for f in ('fehler', 'ausnahmen', 'warnungen', 'hinweise')}
    summe['offen'] = summe['fehler'] - summe['ausnahmen']
    return {
        'projekt': k['id'], 'validator': version, 'fhir': k.get('fhir', '4.0.1'),
        'optionen': _optionen(v),
        'pakete': [f'{bezeichnung(o)} (lokal: {o.relative_to(k["ordner"]).as_posix()})' for o in k['lokale_ordner']]
                  + list(v['pakete']),
        'ausnahmen': [{'id': ausnahme_kennung(a, i), 'muster': a['muster'], 'grund': a['grund'], 'treffer': treffer[i]}
                      for i, a in enumerate(ausnahmen)],
        'summe': summe, 'beispiele': beispiele,
    }


def _optionen(v):
    o = ['-tx', 'n/a', '-locale', LOCALE]
    if v.get('erweiterungen'):
        o += ['-allow-example-urls', 'true']
        for e in v['erweiterungen']:
            o += ['-extension', e]
    return o


def projekt(pid):
    k = projekt_laden(pid)
    v = k.get('validierung')
    dateien = [str(k['ordner'] / b['datei']) for b in k['beispiele'] if b.get('datei')]
    if not v or not dateien:
        print(f'{pid}: nichts zu validieren')
        return 0
    with tempfile.TemporaryDirectory() as tmp:
        aus = Path(tmp) / 'ergebnis.json'
        befehl = [_java(), *JVM_OPTIONEN, '-jar', _jar(), *dateien, '-version', k.get('fhir', '4.0.1'),
                  *_optionen(v), '-output', str(aus)]
        for o in k['lokale_ordner']:
            befehl += ['-ig', str(o / 'package')]
        for p in v['pakete']:
            befehl += ['-ig', p]
        print(f'{pid}: {len(dateien)} Dateien, Pakete {", ".join(map(bezeichnung, k["lokale_ordner"] + v["pakete"]))}',
              flush=True)
        r = subprocess.run(befehl, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if not aus.exists():
            print(r.stdout[-3000:], r.stderr[-3000:], sep='\n')
            return 1
        ergebnis = json.loads(aus.read_text(encoding='utf-8'))
    daten = auswerten(k, meldungen(ergebnis), _version(r.stdout + r.stderr))
    json_schreiben(datei(pid), daten)
    for a in daten['ausnahmen']:
        if not a['treffer']:
            print(f'  Hinweis: Ausnahme ohne Treffer: {a["id"]} ({a["muster"]})')
    offen = [f'{b["datei"]} — {m["ort"]}: {m["text"]}' for b in daten['beispiele'] for m in b['meldungen']
             if m['stufe'] in ('fatal', 'error') and 'ausnahme' not in m]
    AUSGABE.mkdir(exist_ok=True)
    (AUSGABE / f'validierung-{pid}.txt').write_text('\n'.join(offen) + '\n', encoding='utf-8')
    for b in daten['beispiele']:
        print(f'  {b["id"]}: {b["fehler"]} Fehler ({b["ausnahmen"]} begründete Ausnahme), '
              f'{b["warnungen"]} Warnungen, {b["hinweise"]} Hinweise')
    for f in offen:
        print('  ' + f)
    s = daten['summe']
    genutzt = sum(1 for a in daten['ausnahmen'] if a['treffer'])
    print(f'{pid}: {s["offen"]} Fehler, {genutzt} Ausnahme(n) genutzt ({s["ausnahmen"]} Meldungen), {s["warnungen"]} Warnungen '
          f'— HL7 Validator {daten["validator"]}, {datei(pid).relative_to(WURZEL).as_posix()}')
    return 1 if offen else 0


def alle(pids):
    return 1 if any([projekt(p) for p in pids]) else 0


# ---------------------------------------------------------------- Ergebnis für den Bau (ohne Java)

def ergebnis_laden(k, pfad=None):
    """Validierungsergebnis eines Projekts für Bericht und Oberfläche, None ohne Datei.
    Je Beispiel: Zählung und Meldungen; `veraltet`, wenn die Beispieldatei seit der Validierung geändert wurde."""
    pfad = pfad or datei(k['id'])
    if not pfad.exists():
        return None
    d = json_laden(pfad)
    nach_id = {b['id']: b for b in d['beispiele']}
    beispiele = {}
    for bk in k['beispiele']:
        e = nach_id.get(bk['id'])
        if e is None:
            beispiele[bk['id']] = {'status': 'nicht validiert' if bk.get('datei') else 'Paketbeispiel'}
            continue
        veraltet = not bk.get('datei') or datei_hash(k['ordner'] / bk['datei']) != e['sha256']
        beispiele[bk['id']] = dict({x: y for x, y in e.items() if x != 'sha256'}, status='veraltet' if veraltet else 'aktuell')
    return {x: d[x] for x in ('validator', 'fhir', 'optionen', 'pakete', 'ausnahmen', 'summe')} | {'beispiele': beispiele}


if __name__ == '__main__':
    sys.exit(alle(sys.argv[1:]))
