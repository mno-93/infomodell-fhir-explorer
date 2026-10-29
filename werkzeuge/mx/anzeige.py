"""Abdeckung der Anzeige: Werte der Beispiele, die weder Anwenderansicht noch Dokument zeigen.

Die Seite rechnet das selbst aus (Auffangnetz „Weitere Angaben aus der Instanz“ in `web/explorer.html`): Jeder inhaltliche
Wert eines Beispiels steht entweder in der Anwenderansicht bzw. einer Dokumentfassung (Elementbezug `data-n`, oder als
mitgetragene Angabe `data-implizit`) oder im Auffangnetz. Technisch sind nur Kennungen und Metadaten, Systeme, Versionen,
URLs, Erzähltext, UUID-Kennungen und Verweise, deren Ziel im Beispiel liegt.

Dazu die Verknüpfungsprüfung der Seite (`verknuepfungPruefen`): Jede Richtung Instanz ↔ Profil ↔ Informationsmodell muss
tragen — erwartet, wo ein Mapping bzw. Element den Wert abdeckt (auch über Profilgrenzen), dazu die Rückwege und jeder Klick
in der Anwenderansicht. Fehlt eine Verknüpfung, endet `anzeige` mit Exit-Code 1 (die CI schlägt fehl).

`mx.py anzeige` führt die gebaute Seite `ausgabe/<projekt>.html?abdeckung` in einem Browser ohne Fenster aus (Chrome,
Chromium oder Edge; über BROWSER_BIN wählbar) und schreibt `berichte/<projekt>.anzeige.json` — eingecheckt und
deterministisch, damit ein neues Beispiel oder eine geänderte Ansicht, die etwas verschluckt, im Diff auffällt. `bauen`
zeigt das Ergebnis im Prüfbericht; die CI prüft, dass die Datei zum Stand passt.
"""
import html
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .grundlagen import AUSGABE, BERICHTE, json_laden, json_schreiben
from .konfig import projekt_laden

KANDIDATEN = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome', 'msedge',
              r'C:\Program Files\Google\Chrome\Application\chrome.exe',
              r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
              r'C:\Program Files\Microsoft\Edge\Application\msedge.exe']
ERGEBNIS = re.compile(r'<pre id="anzeige-ergebnis">(.*?)</pre>', re.S)


def browser():
    if os.environ.get('BROWSER_BIN'):
        return os.environ['BROWSER_BIN']
    for k in KANDIDATEN:
        w = shutil.which(k) or (k if Path(k).is_file() else None)
        if w:
            return w
    raise SystemExit('Kein Browser gefunden (Chrome, Chromium oder Edge) — BROWSER_BIN setzen')


def datei(pid):
    return BERICHTE / f'{pid}.anzeige.json'


def auslesen(dom):
    """Ergebnis des Prüfmodus aus dem ausgegebenen DOM: {beispiele: {id: [{element, anzahl, werte}]},
    verknuepfung: {id: [{richtung, anzahl, beispiele}]}}. Das eingefügte Element steht
    am Ende der Seite; dieselbe Zeichenkette kommt vorher als Vorlage im Skript vor."""
    treffer = [html.unescape(t) for t in ERGEBNIS.findall(dom)]
    treffer = [t for t in treffer if t.lstrip().startswith('{')]
    if not treffer:
        raise ValueError('Die Seite hat kein Ergebnis des Prüfmodus geliefert')
    return json.loads(treffer[-1])


def projekt(pid):
    k = projekt_laden(pid)
    if not [b for b in k['beispiele']]:
        print(f'{pid}: keine Beispiele')
        return 0
    seite = AUSGABE / f'{pid}.html'
    if not seite.exists():
        raise SystemExit(f'{pid}: {seite} fehlt — zuerst `python3 -I werkzeuge/mx.py bauen`')
    with tempfile.TemporaryDirectory() as profil:
        r = subprocess.run([browser(), '--headless=new', '--disable-gpu', '--no-sandbox', '--no-first-run',
                            f'--user-data-dir={profil}', '--virtual-time-budget=30000', '--dump-dom',
                            seite.resolve().as_uri() + '?abdeckung'],
                           capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    try:
        e = auslesen(r.stdout)
    except ValueError as x:
        print(r.stderr[-2000:])
        raise SystemExit(f'{pid}: {x}')
    json_schreiben(datei(pid), {'projekt': pid, 'beispiele': e['beispiele'], 'verknuepfung': e['verknuepfung']})
    fehler = 0
    for bid, gruppen in e['beispiele'].items():
        n = sum(g['anzahl'] for g in gruppen)
        print(f'  {bid}: ' + (f'{n} Werte in {len(gruppen)} Elementen weder in Anwenderansicht noch Dokument' if n
                              else 'alle inhaltlichen Werte angezeigt'))
        for f in e['verknuepfung'].get(bid, []):
            fehler += f['anzahl']
            print(f'    Verknüpfung fehlt: {f["richtung"]} ({f["anzahl"]}×), z. B. {", ".join(f["beispiele"][:3])}')
    return 1 if fehler else 0


def alle(pids):
    ergebnis = 0
    for pid in pids:
        print(f'{pid}:')
        ergebnis |= projekt(pid)
    return ergebnis


def ergebnis_laden(k):
    """Ergebnis für den Prüfbericht, None ohne Datei; Beispiele, die nicht (mehr) im Projekt stehen, fallen weg."""
    p = datei(k['id'])
    if not p.exists():
        return None
    d = json_laden(p)
    ids = [b['id'] for b in k['beispiele']]
    return {'beispiele': {i: d['beispiele'][i] for i in ids if i in d['beispiele']},
            'verknuepfung': {i: d.get('verknuepfung', {}).get(i, []) for i in ids if i in d['beispiele']},
            'fehlt': [i for i in ids if i not in d['beispiele']]}
