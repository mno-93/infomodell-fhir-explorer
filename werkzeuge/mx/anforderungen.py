"""Anforderungen aus einer gematik-IG-Seite (`<requirement>`-Elemente) mit den genannten Elementpfaden."""
import html
import re

from .grundlagen import kanon, text


def gematik_requirements(konfig, sds):
    quelle = konfig.get('anforderungen', {}).get('quelle')
    if not quelle:
        return []
    nach_name = {d['name']: d['url'] for d in sds.values()}
    roh = (konfig['ordner'] / quelle).read_text(encoding='utf-8')
    ergebnis, abschnitt, profil = [], '', None
    for m in re.finditer(r'<h([2-5])[^>]*>(.*?)</h\1>|<requirement (.*?)>(.*?)</requirement>', roh, re.S):
        if m.group(1):
            abschnitt = text(m.group(2))
            klammer = re.search(r'\(([A-Za-z]+)\)', abschnitt)
            profil = nach_name.get(klammer.group(1)) if klammer else (None if m.group(1) in '234' else profil)
            continue
        attr = dict(re.findall(r'(\w+)="([^"]*)"', m.group(3)))
        rumpf = re.sub(r'<meta[^>]*/>|<actor.*?</actor>', '', m.group(4), flags=re.S)
        pfade = set()
        for kandidat in re.findall(r'<i>(.*?)</i>', rumpf, re.S) + \
                re.findall(r'\b([A-Z][A-Za-z]+(?:\.[A-Za-z][\w\[\]:-]*)+)', text(rumpf)):
            kandidat = text(kandidat).strip()
            if re.fullmatch(r'[A-Z][A-Za-z]+(\.[A-Za-z][\w\[\]:-]*)+', kandidat):
                pfade.add(kanon(kandidat))
        ergebnis.append({
            'key': attr.get('key'), 'titel': html.unescape(attr.get('title', '')), 'conf': attr.get('conformance'),
            'akteure': re.findall(r'<actor name="([^"]*)"', m.group(4)), 'abschnitt': abschnitt, 'sd': profil,
            'text': text(rumpf), 'pfade': sorted(pfade),
        })
    return ergebnis


def laden(konfig, sds):
    art = konfig.get('anforderungen', {}).get('art')
    return gematik_requirements(konfig, sds) if art == 'gematik-requirements' else []
