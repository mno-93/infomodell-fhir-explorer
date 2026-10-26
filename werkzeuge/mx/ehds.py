"""EHDS-Mappings eines Informationsmodells gegen die Xt-EHR-Logikmodelle prüfen (Paket `xtehr.eu.ehds.models`).

Ein MIO-Informationsmodell nennt je Element sein Gegenstück im EHDS-Logikmodell — als Link auf die Seite des Modells,
als kanonische URL des Modells, als Pfad im Linkziel oder nur als Text. Hier werden die Verweise gelesen, gegen die
StructureDefinitions der Logikmodelle (kind = logical, mit Snapshot) aufgelöst und gegen ihren Kontext geprüft.

Auflösung (status)
  aufloesbar          Modell und Element gibt es im Paket
  nur-modell          nur das Modell ist genannt, kein Element (passend für Knoten, die ein ganzes Modell abbilden)
  element-fehlt       das Modell gibt es, das Element nicht
  modell-fehlt        das Modell gibt es im Paket nicht
  ohne-entsprechung   ausdrücklich ohne Gegenstück („Element ist im EHDS Logical Model nicht vorhanden“)
Linkformat (format)
  versioniert         …/fhir/models/1.0.0/en/StructureDefinition-<Modell>-definitions.html#<Element>
  ohne-version        …/fhir/models/en/… — zeigt auf den jeweils aktuellen Stand, nicht auf 1.0.0
  kanonisch           kanonische URL des Modells (…/fhir/models/StructureDefinition/<Modell>), ohne Element
  ohne-url            das Linkziel ist nur der Pfad (`<a href="EHDSDeviceUse.device[x]">`)
  klartext            kein Link, nur Text
  fremder-link        Link auf eine andere Seite als das Logikmodell (z. B. ein FHIR-Profil)
Kontext
  Das Modell eines Verweises muss das des nächsten übergeordneten Elements mit EHDS-Mapping sein oder ein Modell, das
  dort als Typ des gemappten Elements steht; sonst „Modell eines anderen Bausteins“.
"""
import html
import re

from .grundlagen import text

XTEHR = 'xt-ehr.eu/fhir/models/'
XTEHR_KANONISCH = 'http://www.xt-ehr.eu/fhir/models/StructureDefinition/'
# Originalseiten (geprüft am 23.10.2026, HTTP 200): je Modell eine Seite, je Element ein Anker auf der Definitionsseite
SEITE = 'https://www.xt-ehr.eu/fhir/models/{version}/en/StructureDefinition-{modell}{teil}.html{anker}'
PFAD = re.compile(r'EHDS[A-Z][A-Za-z0-9]*(?:\.[A-Za-z][A-Za-z0-9]*(?:\[x\])?)*')
OHNE_ENTSPRECHUNG = re.compile(r'im EHDS Logical Model nicht vorhanden', re.I)
UNSICHTBAR = re.compile('[\u200b\u200c\u200d\u2060\ufeff]')  # unsichtbare Zeichen, z. B. in Klartext-Verweisen

STATUS = ('aufloesbar', 'nur-modell', 'element-fehlt', 'modell-fehlt', 'ohne-entsprechung')
FORMATE = ('versioniert', 'ohne-version', 'kanonisch', 'ohne-url', 'klartext', 'fremder-link')


def _pfad_teilen(pfad):
    return (pfad.split('.', 1)[0], pfad if '.' in pfad else None) if pfad else (None, None)


def verweise(inhalt):
    """Verweise eines Abschnitts „EHDS Logical Model“/„EHDS-Mapping“: [{roh, url, modell, element, format, …}]."""
    unsichtbar = bool(UNSICHTBAR.search(inhalt or ''))
    inhalt = UNSICHTBAR.sub('', inhalt or '')
    if OHNE_ENTSPRECHUNG.search(text(inhalt)):
        return [{'roh': text(inhalt), 'url': None, 'modell': None, 'element': None, 'format': None,
                 'status': 'ohne-entsprechung'}]
    aus = []
    for attr, linktext in re.findall(r'<a\b([^>]*)>(.*?)</a>', inhalt, re.S):
        href = re.search(r'href="([^"]*)"', attr)
        href = html.unescape(href.group(1)).strip() if href else ''
        linktext = text(linktext)
        v = {'roh': linktext, 'url': href or None}
        if XTEHR in href:
            m = re.search(r'StructureDefinition/(EHDS\w+)$', href)
            if m:
                v.update(modell=m.group(1), element=None, format='kanonisch')
            else:
                m = re.search(r'StructureDefinition-(EHDS\w+?)(?:-definitions)?\.html(?:#(.+))?$', href)
                modell, element = _pfad_teilen(m.group(2)) if m and m.group(2) else ((m.group(1), None) if m else (None, None))
                v.update(modell=modell, element=element,
                         format='versioniert' if re.search(r'/fhir/models/\d+\.\d+\.\d+/', href) else 'ohne-version')
        elif href and not re.match(r'^[a-z]+:', href):
            v.update(zip(('modell', 'element'), _pfad_teilen(href)), format='ohne-url')
        else:
            gefunden = PFAD.search(linktext)
            v.update(zip(('modell', 'element'), _pfad_teilen(gefunden.group(0) if gefunden else None)),
                     format='fremder-link' if href else 'klartext')
        aus.append(v)
    # Pfade im Text außerhalb von Links
    rest = text(re.sub(r'<a\b[^>]*>.*?</a>', ' ', inhalt, flags=re.S))
    for p in PFAD.findall(rest):
        aus.append(dict(zip(('modell', 'element'), _pfad_teilen(p)), roh=p, url=None, format='klartext'))
    for v in aus:
        if unsichtbar:
            v['unsichtbar'] = True
    return aus


class Logikmodelle:
    def __init__(self, sds, paket=''):
        self.paket = paket
        self.modelle = {}
        for sd in sds.values():
            if sd.get('kind') == 'logical' and sd['url'].startswith(XTEHR_KANONISCH):
                self.modelle.setdefault(sd['name'], sd)
        self._ids = {}

    def ids(self, sd):
        if sd['url'] not in self._ids:
            self._ids[sd['url']] = {e['id']: e for e in sd['snapshot']['element']}
        return self._ids[sd['url']]

    def aufloesen(self, v):
        """Status, Link auf die Originalseite und die als Typ genannten Modelle eines Verweises ergänzen."""
        if v.get('status') == 'ohne-entsprechung':
            return v
        sd = self.modelle.get(v.get('modell'))
        if not sd:
            v['status'] = 'modell-fehlt'
            return v
        ziel = None
        if v.get('element'):
            ids = self.ids(sd)
            el = v['element']
            ziel = next((x for x in (el, el + '[x]', el[:-3] if el.endswith('[x]') else None) if x and x in ids), None)
            v['status'] = 'aufloesbar' if ziel else 'element-fehlt'
        else:
            v['status'] = 'nur-modell'
        version = sd.get('version', '')
        v['seite'] = SEITE.format(version=version, modell=sd['name'], teil='-definitions' if ziel else '',
                                  anker=f'#{ziel}' if ziel else '')
        e = self.ids(sd).get(ziel) if ziel else None
        v['typen'] = sorted({t['code'].rsplit('/', 1)[-1] for t in (e or {}).get('type', [])
                             if t.get('code', '').startswith(XTEHR_KANONISCH)})
        return v


def grund(v):
    """Befund eines Verweises in Worten (leer, wenn nichts zu bemerken ist)."""
    teile = []
    if v.get('status') == 'element-fehlt':
        teile.append(f'`{v["element"]}` gibt es im Modell `{v["modell"]}` nicht')
    elif v.get('status') == 'modell-fehlt':
        teile.append(f'Modell `{v.get("modell") or v["roh"]}` nicht im Paketbestand' if v.get('modell')
                     else f'kein Modell erkennbar in „{v["roh"]}“')
    fmt = v.get('format')
    if fmt == 'ohne-version':
        teile.append('Link ohne Version (`…/models/en/…`) — zeigt auf den jeweils aktuellen Stand')
    elif fmt == 'klartext':
        teile.append('nur als Text, ohne Link')
    elif fmt == 'ohne-url':
        teile.append(f'Linkziel ist nur der Pfad `{v.get("url")}`, keine URL')
    elif fmt == 'fremder-link':
        teile.append(f'Link führt auf `{v.get("url")}`, nicht auf das Logikmodell')
    if v.get('unsichtbar'):
        teile.append('enthält ein unsichtbares Zeichen (U+200B)')
    if v.get('kontext'):
        teile.append(v['kontext'])
    return '; '.join(teile)


def pruefen(knoten, logik):
    """Alle Verweise auflösen, Kontext prüfen. Liefert (statistik, befunde); die Verweise der Knoten werden ergänzt."""
    by = {n['id']: n for n in knoten}

    def pfad(n):
        teile = []
        while n:
            teile.insert(0, n['name'])
            n = by.get(n['p'])
        return ' / '.join(teile)

    for n in knoten:
        for v in n.get('ehds', []):
            logik.aufloesen(v)
    for n in knoten:
        eigene = [v for v in n.get('ehds', []) if v.get('modell')]
        if not eigene:
            continue
        o = by.get(n['p'])
        while o and not any(v.get('modell') for v in o.get('ehds', [])):
            o = by.get(o['p'])
        if not o:
            continue
        modelle = sorted({v['modell'] for v in o['ehds'] if v.get('modell')})
        erlaubt = set(modelle) | {t for v in o['ehds'] for t in v.get('typen', [])}
        for v in eigene:
            if v['modell'] not in erlaubt:
                v['kontext'] = (f'Modell eines anderen Bausteins: liegt unter „{o["name"]}“ ({", ".join(modelle)}), '
                                f'zeigt aber auf `{v["modell"]}`')
    alle = [(n, v) for n in knoten for v in n.get('ehds', [])]
    befunde = [{'id': n['id'], 'im': n['name'], 'pfad': pfad(n), 'roh': v['roh'], 'status': v['status'],
                'format': v.get('format'), 'kontext': bool(v.get('kontext')), 'grund': grund(v)}
               for n, v in alle if grund(v)]
    statistik = {
        'paket': logik.paket, 'modelle': len(logik.modelle),
        'knoten': sum(1 for n in knoten if n.get('ehds')), 'verweise': len(alle),
        'status': {s: sum(1 for _n, v in alle if v['status'] == s) for s in STATUS},
        'format': {f: sum(1 for _n, v in alle if v.get('format') == f) for f in FORMATE},
        'anderes_modell': sum(1 for _n, v in alle if v.get('kontext')),
        'unsichtbar': sum(1 for _n, v in alle if v.get('unsichtbar')),
    }
    return statistik, befunde
