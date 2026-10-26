"""Informationsmodell laden — zwei Adapter, ein gemeinsames Knotenformat.

Knoten: {id, p, name, typ, card, besch, rat, op, codes[], maps[{roh, sd, k, status, grund}], kurz, herkunft[], anf[]}

gematik-baum   JSON hinter der Baumansicht „Informationsmodell“ eines veröffentlichten gematik-IG mit
               FHIR-Mappings je Element; dazu die ausmodellierte Sicht.
aus-profilen   kein veröffentlichtes Informationsmodell mit Mappings: Struktur aus den Profilen ableiten
               (Composition → Abschnitte → Einträge → Must-Support-Elemente).
"""
import hashlib
import html
import re

from .aufloeser import Aufloeser
from .grundlagen import json_laden, kanon, text
from .terminologie import staerke_trennen


# ---------------------------------------------------------------- gematik-baum

def _tabelle(s):
    """HTML-Tabelle nach ihren Kopfzeilen auslesen: [{Kopf: Zelle}]. Ohne Kopfzeile: Code, Display, CodeSystem."""
    zeilen = re.findall(r'<tr>(.*?)</tr>', s or '', re.S)
    if not zeilen:
        return []
    kopf = [text(h) for h in re.findall(r'<th[^>]*>(.*?)</th>', zeilen[0], re.S)]
    if not kopf:
        kopf = ['Code', 'Display', 'CodeSystem']
    else:
        zeilen = zeilen[1:]
    aus = []
    for z in zeilen:
        zellen = [text(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', z, re.S)]
        if zellen:
            aus.append(dict(zip(kopf, zellen)))
    return aus


def terminologie(term_assocs, codes, wl):
    """Terminologie eines Modellelements: eigene Codes, Codes der Listeneinträge, gebundene Wertelisten.
    Liefert (zeilen, wertelisten, codes_flach)."""
    wertelisten, index = [], {}
    zeilen = []
    for quelle, tabelle in (('konzept', _tabelle(term_assocs)), ('liste', _tabelle(codes))):
        for r in tabelle:
            vs = None
            if r.get('ValueSet'):
                name, staerke = staerke_trennen(r['ValueSet'])
                if (name, staerke) not in index:
                    aufgeloest = wl.zum_namen(name) if wl else None
                    index[(name, staerke)] = len(wertelisten)
                    wertelisten.append(dict(aufgeloest or {}, name=name, staerke=staerke, aufgeloest=bool(aufgeloest)))
                vs = index[(name, staerke)]
            zeilen.append({'quelle': quelle, 'konzept': r.get('Konzept', ''), 'code': r.get('Code', ''),
                           'display': r.get('Display', ''), 'system': r.get('CodeSystem', ''),
                           'filter': r.get('Filter', ''), 'designations': r.get('Designations', ''), 'vs': vs})
    flach = [{'code': z['code'], 'display': z['display'], 'system': z['system']} for z in zeilen if z['code']]
    return zeilen, wertelisten, flach


def _weitere_angaben(s):
    """otherProperties: Short, LDT2/LDT3/Muster 10, Requirement-n."""
    kurz, herkunft, anforderungen = '', [], []
    teile = re.split(r'<p class="detailTitle">(.*?)</p>', s or '', flags=re.S)
    for i in range(1, len(teile) - 1, 2):
        titel = text(teile[i]).rstrip(':')
        inhalt = teile[i + 1]
        if titel == 'Short':
            kurz = text(inhalt)
        elif titel.startswith('Requirement'):
            felder = [text(p) for p in re.findall(r'<p>(.*?)</p>', inhalt, re.S)]
            d = dict(zip(felder[0::2], felder[1::2]))
            anforderungen.append({'titel': d.get('Titel', ''), 'kw': d.get('Schlüsselwort', ''),
                                  'akteur': d.get('Akteur', ''), 'text': d.get('Inhalt', '')})
        else:
            herkunft.append({'quelle': titel, 'text': text(inhalt)})
    return kurz, herkunft, anforderungen


def gematik_baum(konfig, sds, wl=None):
    aufl = Aufloeser(sds)
    nach_name = {}
    for d in sds.values():
        nach_name.setdefault(d['name'], d)
    roh = json_laden(konfig['ordner'] / konfig['informationsmodell']['quelle'])
    knoten = []
    for n in roh:
        d = n.get('data') or {}
        maps = []
        for _href, _t, ziel in re.findall(r'<a href="([^"]*)" title="([^"]*)">([^<]*)</a>', d.get('fhirMappings') or ''):
            ziel = html.unescape(ziel).strip()
            name, _, rest = ziel.partition('.')
            sd = nach_name.get(name)
            if not sd:
                maps.append({'roh': ziel, 'sd': None, 'k': None, 'status': 'unbekannt',
                             'grund': f'Profil `{name}` nicht im Paketbestand'})
                continue
            status, grund = aufl.pruefe(sd, rest)
            maps.append({'roh': ziel, 'sd': sd['url'], 'k': kanon(sd['type'] + ('.' + rest if rest else '')),
                         'status': status, 'grund': grund})
        kurz, herkunft, anforderungen = _weitere_angaben(d.get('otherProperties'))
        zeilen, wertelisten, flach = terminologie(d.get('termAssocs'), d.get('codes'), wl)
        knoten.append({
            'id': n['id'], 'p': None if n['parent'] == '#' else n['parent'], 'name': html.unescape(n['text']),
            'typ': d.get('datatype', ''), 'card': text(d.get('cardinality')), 'besch': text(d.get('description'))[:1500],
            'rat': text(d.get('rationale'))[:800], 'op': text(d.get('operationalisations'))[:800],
            'codes': flach, 'terminologie': zeilen, 'wertelisten': wertelisten,
            'maps': maps, 'kurz': kurz, 'herkunft': herkunft, 'anf': anforderungen,
        })
    return knoten


def _pfad(by, n):
    teile = []
    while n:
        teile.insert(0, n['name'])
        n = by.get(n['p'])
    return ' / '.join(teile)


def mappings_pruefen(knoten):
    """Alle nicht exakten Mappings, dazu Mappings in ein anderes Profil als das des Kontexts."""
    by = {n['id']: n for n in knoten}
    pruefung = []
    for n in knoten:
        for m in n['maps']:
            if m['status'] != 'exakt':
                pruefung.append({'id': n['id'], 'im': n['name'], 'pfad': _pfad(by, n), 'mapping': m['roh'],
                                 'status': m['status'], 'grund': m['grund']})
        v = by.get(n['p'])
        while v and not any(m['sd'] and '.' not in m['k'] for m in v['maps']):
            v = by.get(v['p'])
        if not v:
            continue
        kontext = {m['sd'] for m in v['maps'] if m['sd'] and '.' not in m['k']}
        for m in n['maps']:
            if m['sd'] and '.' in m['k'] and m['sd'] not in kontext and '/fhir/ti/' not in m['sd'] \
                    and not any(x['sd'] in kontext for x in n['maps'] if x is not m):
                pruefung.append({'id': n['id'], 'im': n['name'], 'pfad': _pfad(by, n), 'mapping': m['roh'],
                                 'status': 'anderes-profil',
                                 'grund': f'liegt unter „{v["name"]}“ ({", ".join(k.split("/")[-1] for k in sorted(kontext))}), '
                                          f'zeigt aber in `{m["sd"].split("/")[-1]}`'})
    return pruefung


def _must_support_knoten(sd_url, sds, p, neu, tiefe=3):
    """Must-Support-Elemente eines Profils als Unterbaum (für Profile, die das Modell nur als Ganzes nennt)."""
    gewaehlt = {}
    for e in sds[sd_url]['snapshot']['element']:
        eid = e['id']
        if '.' not in eid or e.get('max') == '0' or not e.get('mustSupport') or eid.count('.') > tiefe:
            continue
        if re.search(r'\.(id|url|meta|implicitRules|language|text|contained|modifierExtension|extension)(\.|$)', eid):
            continue
        eltern = eid.rsplit('.', 1)[0]
        while eltern not in gewaehlt and '.' in eltern:
            eltern = eltern.rsplit('.', 1)[0]
        gewaehlt[eid] = neu(gewaehlt.get(eltern, p), y=[sd_url, eid])


def ausmodellieren(knoten, sds, konfig):
    """Zweite Sicht: jede „(Referenz)“ wird durch das referenzierte Profil ersetzt; Zyklen werden erkannt.
    Profile unter `ergaenzen_aus` (z. B. TI Common), die das Modell nur als Ganzes nennt, werden aus dem
    FHIR-Profil ergänzt (Must Support bis zur dritten Ebene) und gekennzeichnet."""
    im = konfig['informationsmodell']
    by = {n['id']: n for n in knoten}
    kinder = {}
    for n in knoten:
        kinder.setdefault(n['p'], []).append(n['id'])
    wurzeln = kinder[None]
    referenziert = next((i for i in wurzeln if by[i]['name'] == im.get('referenzgruppe')), None)
    if referenziert is None:
        return None
    ziele = {}
    for c in kinder.get(referenziert, []):
        if kinder.get(c) and not by[c]['maps']:
            for cc in kinder[c]:
                ziele[by[cc]['name']] = cc
        else:
            ziele[by[c]['name']] = c
    baum, erreicht = [], set()
    ergaenzen = im.get('ergaenzen_aus')

    vergeben = set()

    def neu(p, **kw):
        # stabile Fundstellen-Kennung aus dem Pfad — bleibt gültig, solange sich der Weg dorthin nicht ändert
        teil = '|'.join(f'{k}={kw[k]}' for k in sorted(kw) if kw[k] is not None)
        u = 'a' + hashlib.sha1(f'{p}>{teil}'.encode()).hexdigest()[:8]
        n = 1
        while u in vergeben:  # gleiches Element zweimal unter demselben Knoten
            n += 1
            u = 'a' + hashlib.sha1(f'{p}>{teil}#{n}'.encode()).hexdigest()[:8]
        vergeben.add(u)
        baum.append(dict(u=u, p=p, **{k: v for k, v in kw.items() if v is not None}))
        return u

    def gehe(i, p, stapel):
        n = by[i]
        if n['name'].endswith(' (Referenz)'):
            z = ziele.get(n['name'][:-len(' (Referenz)')])
            if z is None:
                neu(p, s=i)
            elif z in stapel:
                neu(p, s=i, z=z)
            else:
                erreicht.add(z)
                unterbau(z, neu(p, s=z, v=i), stapel + [z])
            return
        unterbau(i, neu(p, s=i), stapel)

    def unterbau(i, u, stapel):
        if kinder.get(i):
            for c in kinder[i]:
                gehe(c, u, stapel)
            return
        wurzel = [m['sd'] for m in by[i]['maps'] if m['sd'] and '.' not in m['k']]
        if ergaenzen and wurzel and wurzel[0].startswith(ergaenzen) and wurzel[0] in sds:
            _must_support_knoten(wurzel[0], sds, u, neu)

    for w in wurzeln:
        if w != referenziert:
            erreicht.add(w)
            gehe(w, None, [w])
    rest = [z for z in ziele.values() if z not in erreicht]
    if rest:
        g = neu(None, n='Nicht vom Einstieg aus referenziert')
        for z in rest:
            gehe(z, g, [z])
    return baum


# ---------------------------------------------------------------- aus-profilen

AUSLASSEN = re.compile(r'\.(id|url|meta|implicitRules|language|text|contained|modifierExtension|extension)(\.|$)')


def aus_profilen(konfig, sds):
    """Struktur aus den Profilen ableiten: Einstiegsprofil(e), Abschnitte, Eintragsprofile, Must Support."""
    im = konfig['informationsmodell']
    tiefe = im.get('tiefe', 3)
    knoten = []
    vergeben = set()

    def neu(p, name, sd=None, eid=None, card='', besch=''):
        # stabile Kennung aus dem Pfad (übergeordneter Knoten, Profil, Element) — für dauerhafte Verweise per URL
        roh = f'{p}|{sd["id"] if sd else name}|{eid or ""}'
        i = 'p' + hashlib.sha1(roh.encode()).hexdigest()[:8]
        assert i not in vergeben, f'Kennung doppelt: {roh}'
        vergeben.add(i)
        maps = [{'roh': f'{sd["name"]}{eid[len(sd["type"]):] if eid else ""}', 'sd': sd['url'],
                 'k': kanon(eid or sd['type']), 'status': 'exakt', 'grund': ''}] if sd else []
        knoten.append({'id': i, 'p': p, 'name': name, 'typ': '', 'card': card, 'besch': besch, 'rat': '', 'op': '',
                       'codes': [], 'terminologie': [], 'wertelisten': [], 'maps': maps, 'kurz': '', 'herkunft': [], 'anf': []})
        return i

    def profil(url, p, stapel, name=None, card=''):
        sd = sds.get(url.split('|')[0])
        if not sd:
            return neu(p, (name or url.split('/')[-1]) + ' (Profil nicht im Paketbestand)', card=card)
        wurzel = neu(p, name or sd.get('title') or sd['name'], sd, None, card, sd.get('description', '')[:600])
        gewaehlt = {}
        for e in sd['snapshot']['element']:
            eid = e['id']
            if '.' not in eid or e.get('max') == '0' or AUSLASSEN.search(eid) or eid.count('.') > tiefe:
                continue
            # Abschnitte und ihre Eintrags-Slices tragen die Gliederung des Dokuments — immer aufnehmen
            gliederung = re.search(r'\.section:[^.]+(\.(title|code|emptyReason|entry(:[^.]+)?))?$', eid)
            if not (e.get('mustSupport') or e.get('min', 0) > 0 or gliederung):
                continue
            eltern = eid.rsplit('.', 1)[0]
            while eltern not in gewaehlt and '.' in eltern:
                eltern = eltern.rsplit('.', 1)[0]
            pk = gewaehlt.get(eltern, wurzel)
            card_e = f"{e.get('min', 0)}..{e.get('max', '*')}"
            titel = eid.split('.')[-1] + (f' — {e["short"]}' if e.get('short') else '')
            gewaehlt[eid] = neu(pk, titel, sd, eid, card_e, (e.get('definition') or '')[:600])
            # Einträge eines Abschnitts: Zielprofile ausmodellieren (ohne Zyklen)
            if re.search(r'\.section(:[^.]+)?\.entry(:[^.]+)?$', eid):
                for t in e.get('type', []):
                    for z in t.get('targetProfile', []):
                        z = z.split('|')[0]
                        if z not in stapel and z in sds and not z.startswith('http://hl7.org/fhir/StructureDefinition/'):
                            profil(z, gewaehlt[eid], stapel + [z])
        return wurzel

    # ein Einstieg oder mehrere nebeneinander (z. B. ein Profil und das Profil seiner enthaltenen Ressourcen)
    for einstieg in ([im['einstieg']] if isinstance(im['einstieg'], str) else im['einstieg']):
        profil(einstieg, None, [einstieg])
    return knoten


def laden(konfig, sds, wl=None):
    art = konfig['informationsmodell']['art']
    if art == 'gematik-baum':
        knoten = gematik_baum(konfig, sds, wl)
        return knoten, ausmodellieren(knoten, sds, konfig)
    return aus_profilen(konfig, sds), None
