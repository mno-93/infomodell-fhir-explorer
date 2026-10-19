"""Profile für die Anzeige aufbereiten: relevante Elemente mit Kardinalität, Must Support, Typ, Bindung."""
import re

from .grundlagen import kanon, wert_kurz

BOILERPLATE = re.compile(r'\.(id|meta|implicitRules|language|text|contained|modifierExtension)(\.|$)')


def element_aufbereiten(e, diff_ids, wl=None):
    typen = []
    for t in e.get('type', []):
        p = [x.split('/')[-1].split('|')[0] for x in t.get('profile', []) + t.get('targetProfile', [])]
        typen.append(t['code'] + ('(' + ', '.join(p) + ')' if p else ''))
    fest = None
    for k, v in e.items():
        if k.startswith('pattern') or k.startswith('fixed'):
            fest = k + ' = ' + wert_kurz(v)
    b = e.get('binding')
    return {
        'id': e['id'], 'k': kanon(e['id']), 'short': e.get('short', ''), 'def': (e.get('definition') or '')[:600],
        'card': f"{e.get('min', 0)}..{e.get('max', '*')}", 'ms': bool(e.get('mustSupport')), 'typ': ', '.join(typen),
        'bind': (b['strength'] + ' ' + b['valueSet'].split('/')[-1].split('|')[0]) if b and b.get('valueSet') else '',
        'bindung': dict(wl.zur_url(b['valueSet']) or {}, staerke=b['strength']) if wl and b and b.get('valueSet') else None,
        'fest': fest, 'diff': e['id'] in diff_ids,
    }


def profil_aufbereiten(sd, gemappt, ig_seite=None, zusaetzlich=(), wl=None):
    """gemappt: kanonische Kennungen, die das Informationsmodell nennt; zusaetzlich: Element-ids, die immer bleiben."""
    diff_ids = {e['id'] for e in sd.get('differential', {}).get('element', [])}
    elemente = []
    for e in sd['snapshot']['element']:
        eid = e['id']
        relevant = (eid in diff_ids or e.get('mustSupport') or kanon(eid) in gemappt or e.get('min', 0) > 0
                    or eid in zusaetzlich)
        if e.get('max') == '0' and eid not in diff_ids:
            continue
        if not relevant and (BOILERPLATE.search(eid) or eid.endswith('.extension')):
            continue
        if not relevant and eid.count('.') > 2:
            continue
        elemente.append(element_aufbereiten(e, diff_ids, wl))
    return {
        'url': sd['url'], 'id': sd['id'], 'name': sd['name'], 'titel': sd.get('title', sd['name']),
        'typ': sd['type'], 'basis': sd.get('baseDefinition', '').split('/')[-1], 'version': sd.get('version', ''),
        'elemente': elemente, 'seite': ig_seite or '',
    }
