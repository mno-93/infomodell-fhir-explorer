"""Beispielinstanzen laden und jedem Knoten das Profilelement zuordnen (inkl. Slices) — wie ein Validator.

Knoten-Kennung (nid): '<Typ>/<id>|<JSON-Pfad>', z. B. 'Observation/obs-1|valueQuantity.value'.
Element: '<Profil-URL>#<kanonische Elementkennung>'.
"""
import base64
import re

from .aufloeser import Aufloeser
from .grundlagen import TECHNISCH, abdeckt, json_laden, kanon, text
from .pakete import ordner


# ---------------------------------------------------------------- Laden

def laden(konfig, beispiel):
    if beispiel.get('datei'):
        roh = json_laden(konfig['ordner'] / beispiel['datei'])
        if roh['resourceType'] == 'Bundle':
            ressourcen = [{'key': e['resource']['resourceType'] + '/' + e['resource']['id'],
                           'fullUrl': e.get('fullUrl') or e['resource']['resourceType'] + '/' + e['resource']['id'],
                           'res': e['resource']} for e in roh.get('entry', [])]
            bundle = {k: v for k, v in roh.items() if k != 'entry'}
        else:
            ressourcen = [{'key': roh['resourceType'] + '/' + roh['id'], 'fullUrl': roh['resourceType'] + '/' + roh['id'], 'res': roh}]
            bundle = None
        return ressourcen, bundle
    # Beispiele eines Pakets: Hülle der Verweise ab einer Einstiegsressource
    basis = ordner(beispiel['paket']) / 'package' / 'example'
    alle = {}
    for f in sorted(basis.glob('*.json')):
        if f.name.startswith('.'):
            continue
        r = json_laden(f)
        alle[r['resourceType'] + '/' + r['id']] = r
    offen, gesehen = [beispiel['einstieg']], []
    while offen:
        k = offen.pop(0)
        if k in gesehen or k not in alle:
            continue
        gesehen.append(k)
        offen.extend(_verweise(alle[k]))
    ressourcen = []
    for k in gesehen:
        r = {kk: vv for kk, vv in alle[k].items() if kk != 'text'}
        ressourcen.append({'key': k, 'fullUrl': k, 'res': r})
    return ressourcen, None


def _verweise(x):
    aus = []
    if isinstance(x, dict):
        for k, v in x.items():
            if k == 'reference' and isinstance(v, str):
                aus.append(v)
            else:
                aus.extend(_verweise(v))
    elif isinstance(x, list):
        for v in x:
            aus.extend(_verweise(v))
    return aus


# ---------------------------------------------------------------- Zuordnung

def _enthaelt(muster, wert):
    if isinstance(muster, dict):
        return isinstance(wert, dict) and all(k in wert and _enthaelt(v, wert[k]) for k, v in muster.items())
    if isinstance(muster, list):
        return isinstance(wert, list) and all(any(_enthaelt(m, w) for w in wert) for m in muster)
    return muster == wert


def _holen(obj, relpfad):
    werte = [obj]
    for teil in [t for t in relpfad.split('.') if t]:
        neu = []
        for w in werte:
            if isinstance(w, list):
                neu.extend(x[teil] for x in w if isinstance(x, dict) and teil in x)
            elif isinstance(w, dict) and teil in w:
                neu.append(w[teil])
        werte = neu
    return werte


class Zuordnung:
    def __init__(self, sd):
        self.sd = sd
        self.el = {e['id']: e for e in sd['snapshot']['element']}

    def _slices(self, basis):
        return [e for i, e in self.el.items() if i.startswith(basis + ':') and '.' not in i[len(basis) + 1:]
                and ':' not in i[len(basis) + 1:]]

    def slice_fuer(self, basis, eintrag):
        for s in self._slices(basis):
            bedingungen = []
            for t in s.get('type', []):
                if t['code'] == 'Extension' and t.get('profile'):
                    bedingungen.append(('url', t['profile'][0].split('|')[0]))
            for k, v in s.items():
                if k.startswith('pattern') or k.startswith('fixed'):
                    bedingungen.append(('', v))
            for i, e in self.el.items():
                if i.startswith(s['id'] + '.') and ':' not in i[len(s['id']) + 1:]:
                    rel = i[len(s['id']) + 1:]
                    for k, v in e.items():
                        if k.startswith('pattern') or k.startswith('fixed'):
                            bedingungen.append((rel, v))
            if bedingungen and all(any(_enthaelt(v, g) for g in ([eintrag] if rel == '' else _holen(eintrag, rel)))
                                   for rel, v in bedingungen):
                return s['id'].rsplit(':', 1)[1]
        if isinstance(eintrag, dict) and isinstance(eintrag.get('url'), str) and '/' not in eintrag['url'] \
                and basis.endswith('extension'):
            return eintrag['url']  # Teil-Extension einer komplexen Extension
        return None

    def kind_id(self, roh, schluessel):
        if roh + '.' + schluessel in self.el or not re.search(r'[a-z][A-Z]', schluessel):
            return roh + '.' + schluessel
        for i in self.el:
            if i.startswith(roh + '.') and i.endswith('[x]') and '.' not in i[len(roh) + 1:]:
                basis = i[len(roh) + 1:-3]
                if schluessel.startswith(basis) and schluessel[len(basis):][:1].isupper():
                    return i + ':' + schluessel
        return roh + '.' + schluessel


def zuordnen(res, sd, key):
    """{nid: '<Profil-URL>#<kanonische Kennung>'} für alle Knoten der Ressource."""
    z = Zuordnung(sd)
    ergebnis = {}

    def gehe(wert, roh, k, jpfad):
        ergebnis[key + '|' + jpfad] = k
        if not isinstance(wert, dict):
            return
        for schl, w in wert.items():
            if schl == 'resourceType' or (roh == sd['type'] and schl in ('id', 'meta', 'text')):
                continue
            name = schl[1:] if schl.startswith('_') else schl
            kid = z.kind_id(roh, name)
            kk = k + '.' + name
            jp = (jpfad + '.' if jpfad else '') + schl
            if isinstance(w, list):
                ergebnis[key + '|' + jp] = kk
                for i, eintrag in enumerate(w):
                    s = z.slice_fuer(kid, eintrag) if isinstance(eintrag, dict) else None
                    gehe(eintrag, kid + (':' + s if s else ''), kk + (':' + s if s else ''), f'{jp}[{i}]')
            else:
                gehe(w, kid, kk, jp)

    gehe(res, sd['type'], sd['type'], '')
    return {nid: sd['url'] + '#' + kanon(k) for nid, k in ergebnis.items()}


def profil_fuer(res, konfig, sds):
    for url in res.get('meta', {}).get('profile', []):
        url = url.split('|')[0]
        if url in sds:
            return url, 'meta.profile'
    std = konfig.get('standardprofile', {}).get(res['resourceType'])
    if std and std in sds:
        return std, 'Standardprofil des Projekts'
    basis = 'http://hl7.org/fhir/StructureDefinition/' + res['resourceType']
    return (basis, 'Basisressource') if basis in sds else (None, 'kein Profil')


# ---------------------------------------------------------------- Textebenen (PDF, Erzähltext)

def _zahl_de(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return (('%g' % v) if isinstance(v, float) else str(v)).replace('.', ',')


def _wertindex(ressourcen):
    werte = []

    def gehe(w, key, jp):
        if isinstance(w, dict):
            for k, v in w.items():
                if k not in ('system', 'version', 'url', 'reference', 'id', 'fullUrl', 'data', 'div', 'meta'):
                    gehe(v, key, (jp + '.' if jp else '') + k)
        elif isinstance(w, list):
            for i, v in enumerate(w):
                gehe(v, key, f'{jp}[{i}]')
        elif isinstance(w, str):
            if len(w) >= 3:
                werte.append((w, key + '|' + jp))
            m = re.match(r'^(\d{4})-(\d\d)-(\d\d)', w)
            if m:
                werte.append((f'{m.group(3)}.{m.group(2)}.{m.group(1)}', key + '|' + jp))
        else:
            s = _zahl_de(w)
            if s:
                werte.append((s, key + '|' + jp))
                if isinstance(w, float) or isinstance(w, int):
                    werte.append((str(w), key + '|' + jp))
    for r in ressourcen:
        gehe(r['res'], r['key'], '')
    return werte


def _bezuege(zeilen, werte):
    aus = []
    for zeile in zeilen:
        treffer = {nid for s, nid in werte if re.search(r'(?<![\w,.])' + re.escape(s) + r'(?![\w,])', zeile)}
        aus.append(sorted(treffer))
    return aus


def pdf_text(ressourcen, werte):
    for r in ressourcen:
        for i, p in enumerate(r['res'].get('presentedForm', []) or []):
            if p.get('contentType') == 'application/pdf' and p.get('data'):
                roh = base64.b64decode(p['data']).decode('latin-1')
                zeilen = []
                for s in re.findall(r'\(((?:\\.|[^\\)])*)\)\s*Tj', roh):
                    s = re.sub(r'\\([0-7]{3})', lambda m: chr(int(m.group(1), 8)), s)
                    zeilen.append(re.sub(r'\\(.)', r'\1', s))
                if not zeilen:
                    continue
                return {'quelle': f'{r["key"]}|presentedForm[{i}]', 'titel': p.get('title', ''), 'base64': p['data'],
                        'zeilen': zeilen, 'bezuege': _bezuege(zeilen, werte)}
    return None


def erzaehltext(ressourcen, werte):
    """Erzähltext der Composition je Abschnitt — die menschenlesbare Fassung des Dokuments."""
    abschnitte = []
    for r in ressourcen:
        if r['res']['resourceType'] != 'Composition':
            continue
        for i, s in enumerate(r['res'].get('section', [])):
            div = (s.get('text') or {}).get('div')
            if not div:
                continue
            zeilen = [z for z in text(re.sub(r'</t[dh]>', ' · ', div)).split('\n') if z.strip(' ·')]
            abschnitte.append({'titel': s.get('title') or '', 'quelle': f'{r["key"]}|section[{i}].text.div',
                               'zeilen': zeilen, 'bezuege': _bezuege(zeilen, werte)})
    return abschnitte


# ---------------------------------------------------------------- Abdeckung und Strukturprüfung

def _wert(ressourcen_nach_key, nid):
    key, jp = nid.split('|', 1)
    w = ressourcen_nach_key[key]
    for teil in re.findall(r'[^.\[\]]+|\[\d+\]', jp):
        w = w[int(teil[1:-1])] if teil.startswith('[') else w[teil]
    return w


def blaetter(beispiel):
    nach_key = {r['key']: r['res'] for r in beispiel['ressourcen']}
    return [(nid, el) for nid, el in beispiel['elemente'].items()
            if not isinstance(_wert(nach_key, nid), (dict, list))]


def abdeckung(knoten, beispiel):
    maps = [(m['sd'], m['k']) for n in knoten for m in n['maps'] if m['sd'] and '.' in m['k']]
    fach = [(nid, el) for nid, el in blaetter(beispiel) if not TECHNISCH.search(el)]
    ohne = {}
    for nid, el in fach:
        sd, k = el.split('#', 1)
        if not any(s == sd and abdeckt(mk, k) for s, mk in maps):
            ohne[el] = ohne.get(el, 0) + 1
    return {'werte': len(fach), 'gedeckt': len(fach) - sum(ohne.values()), 'ohne_modell': dict(sorted(ohne.items()))}


def struktur_pruefen(beispiel, sds):
    """Jedes belegte Element muss im Profil auflösbar sein. Liefert Liste von Befunden."""
    aufl = Aufloeser(sds)
    befunde, gesehen = [], set()
    for nid, el in blaetter(beispiel):
        sd_url, k = el.split('#', 1)
        if (sd_url, k) in gesehen:
            continue
        gesehen.add((sd_url, k))
        rest = k.split('.', 1)[1] if '.' in k else ''
        status, grund = aufl.pruefe(sds[sd_url], rest)
        if status in ('fehler', 'verboten', 'unbekannt'):
            befunde.append({'element': f'{sds[sd_url]["id"]} · {k}', 'status': status, 'grund': grund, 'beispiel': nid})
    return befunde
