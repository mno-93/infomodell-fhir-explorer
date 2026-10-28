"""Gemeinsame Hilfen: Pfade, Text aus HTML, kanonische Elementkennung, Abdeckung."""
import html
import json
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
PROJEKTE = WURZEL / 'projekte'
AUSGABE = WURZEL / 'ausgabe'
BERICHTE = WURZEL / 'berichte'
SPERRDATEI = WURZEL / 'sperrdatei.json'

# Hinweis zur KI-Nutzung: als Logo (web/ki-hinweis.svg) im Kopf jeder Seite und in jedem Prüfbericht
KI_LOGO = WURZEL / 'web' / 'ki-hinweis.svg'
KI_HINWEIS = ('Dieser Modellexplorer – Programmcode, Projektkonfiguration und Texte – ist mit Unterstützung eines '
              'KI-Assistenten (Claude von Anthropic) entstanden. Die Darstellungen sind aus veröffentlichten '
              'Spezifikationen abgeleitet und keine Primärquelle; sie können Fehler enthalten. Maßgeblich sind die '
              'verlinkten Implementierungsleitfäden und FHIR-Pakete. Alle Beispieldaten sind fiktiv.')

# technische Angaben ohne eigenes fachliches Gegenstück im Informationsmodell
TECHNISCH = re.compile(r'\.(url|reference|system|version)$|\.text\.(div|status)$')


def text(s):
    """HTML zu einfachem Text, Absätze als Zeilenumbruch."""
    if not s:
        return ''
    s = re.sub(r'<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>', '\n', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t\r\f\v]+', ' ', s)
    s = re.sub(r'\s*\n\s*', '\n', s)
    return s.strip()


def kanon(pfad):
    """Kanonische Elementkennung: Typwahl als JSON-Name (value[x]:valueQuantity -> valueQuantity)."""
    return re.sub(r'(\w+)\[x\][:.](\1[A-Z]\w*)', r'\2', pfad)


def abdeckt(a, b):
    """Kanonisches Element a umfasst Element b (gleich oder Vorfahr, Slices berücksichtigt)."""
    ta, tb = a.split('.'), b.split('.')
    if len(ta) > len(tb):
        return False
    for x, y in zip(ta, tb):
        nx, _, sx = x.partition(':')
        ny, _, sy = y.partition(':')
        if nx.endswith('[x]'):
            if not (ny.startswith(nx[:-3]) and ny[len(nx) - 3:][:1].isupper()):
                return False
        elif nx != ny:
            return False
        if sx and sy and sx != sy:
            return False
    return True


def wert_kurz(v):
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= 140 else s[:137] + '…'


def json_laden(pfad):
    with open(pfad, encoding='utf-8') as f:
        return json.load(f)


def json_schreiben(pfad, daten, kompakt=False):
    pfad.parent.mkdir(parents=True, exist_ok=True)
    with open(pfad, 'w', encoding='utf-8') as f:
        if kompakt:
            json.dump(daten, f, ensure_ascii=False, separators=(',', ':'))
        else:
            json.dump(daten, f, ensure_ascii=False, indent=1)
            f.write('\n')
