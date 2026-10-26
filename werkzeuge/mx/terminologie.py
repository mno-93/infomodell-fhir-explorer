"""Wertelisten (ValueSets) auflösen: Name oder kanonische URL → Paket, Version, Titel und Link auf die Originalseite.

Links entstehen nur aus geprüften Mustern (Stand 19.10.2026, jeweils HTTP 200 an Stichproben):
  hl7.fhir.r4.core          https://hl7.org/fhir/R4/valueset-<id>.html
  hl7.terminology.r4#<v>    https://terminology.hl7.org/<v>/ValueSet-<id>.html
  hl7.fhir.eu.<ig>#<v>      https://hl7.eu/fhir/<ig>/<v>/ValueSet-<id>.html   (aus package.json `url`)
  de.gematik.terminology#<v> https://gemspec.gematik.de/ig/fhir/terminology/<v>/ValueSet-<id>.html
Liegt eine Werteliste nicht im Paketbestand, wird ihre kanonische URL nur verlinkt, wenn ein Profil sie bindet
und der Herausgeber kanonische URLs auflöst (fhir.kbv.de, hl7.org, terminology.hl7.org). Sonst kein Link.
"""
import re
from pathlib import Path

from .grundlagen import json_laden, kanon
from .pakete import bezeichnung, ordner

KANONISCH_AUFLOESBAR = ('https://fhir.kbv.de/', 'http://hl7.org/fhir/', 'http://terminology.hl7.org/')


def _seite(spec, paket_url, vs_id):
    pid, _, version = spec.partition('#')
    if pid == 'hl7.fhir.r4.core':
        return f'https://hl7.org/fhir/R4/valueset-{vs_id}.html'
    if pid == 'hl7.terminology.r4':
        return f'https://terminology.hl7.org/{version}/ValueSet-{vs_id}.html'
    if pid.startswith('hl7.fhir.eu.') and paket_url:
        return paket_url.replace('http://', 'https://').rstrip('/') + f'/ValueSet-{vs_id}.html'
    if pid == 'de.gematik.terminology':
        return f'https://gemspec.gematik.de/ig/fhir/terminology/{version}/ValueSet-{vs_id}.html'
    return None


class Wertelisten:
    def __init__(self, specs, sds):
        self.nach_url, self.nach_name = {}, {}
        for quelle in specs:
            basis = ordner(quelle) / 'package'
            if not basis.exists():
                continue
            # lokale Pakete (Ordner im Projekt) sind nicht veröffentlicht: Bezeichnung ohne Pfad, keine Originalseite
            spec, lokal = bezeichnung(quelle), isinstance(quelle, Path)
            paket_url = None if lokal else json_laden(basis / 'package.json').get('url')
            for f in sorted(basis.glob('ValueSet-*.json')):
                try:
                    v = json_laden(f)
                except ValueError:
                    continue
                if v.get('resourceType') != 'ValueSet':
                    continue
                e = self.nach_url.get(v['url'])  # erste Fundstelle gewinnt, Namen aller Fundstellen zählen
                if e is None:
                    e = {'url': v['url'], 'id': v.get('id'), 'titel': v.get('title') or v.get('name') or v.get('id'),
                         'version': v.get('version', ''), 'paket': spec,
                         'seite': None if lokal else _seite(spec, paket_url, v.get('id'))}
                    self.nach_url[v['url']] = e
                for schluessel in (v.get('name'), v.get('id'), v.get('title')):
                    if schluessel:
                        self.nach_name.setdefault(schluessel, e)
        # in Profilen gebundene Wertelisten, die selbst nicht im Paketbestand liegen
        self.gebunden = {}
        for sd in sds.values():
            for el in sd['snapshot']['element']:
                vs = (el.get('binding') or {}).get('valueSet')
                if vs:
                    url = vs.split('|')[0]
                    self.gebunden.setdefault(url.rsplit('/', 1)[-1], url)

    def zur_url(self, url):
        url = (url or '').split('|')[0]
        if url in self.nach_url:
            return dict(self.nach_url[url])
        if url.startswith(KANONISCH_AUFLOESBAR):
            return {'url': url, 'titel': url.rsplit('/', 1)[-1], 'seite': url, 'paket': None, 'version': ''}
        return {'url': url, 'titel': url.rsplit('/', 1)[-1], 'seite': None, 'paket': None, 'version': ''} if url else None

    def zum_namen(self, name):
        if name in self.nach_name:
            return dict(self.nach_name[name])
        url = self.gebunden.get(name)
        if url:
            return self.zur_url(url)
        return None


def staerke_trennen(text):
    """'LabStudyTypesEuVs (required)' → ('LabStudyTypesEuVs', 'required')."""
    m = re.match(r'^(.*?)\s*\((required|extensible|preferred|example)\)\s*$', text or '')
    return (m.group(1), m.group(2)) if m else ((text or '').strip(), '')


class Bindungsabgleich:
    """Werteliste im Modell gegen die Bindung im Profil.

    Gesucht wird (1) ein Slice direkt unter dem gemappten Element, dessen Bindung eine Werteliste des Modells ist
    (dann ist das Mapping zu ungenau), (2) die Bindung am gemappten Element, (3) am zugehörigen CodeableConcept
    (Mapping auf `….coding` oder `….coding.code`), (4) am Wert einer gemappten Extension. Nicht über
    Extension-Grenzen hinweg. Ergebnis: gleich · gleich, aber am Slice · abweichend (beide Wertelisten bekannt,
    verschieden) · ungeklärt (Werteliste des Modells nicht im Paketbestand) · ohne Bindung.
    """

    def __init__(self, sds):
        self.sds = sds
        self._index = {}

    def _elemente(self, sd_url):
        if sd_url not in self._index:
            ids = {e['id']: e for e in self.sds[sd_url]['snapshot']['element']}
            els = {}
            for i, e in ids.items():
                els[kanon(i)] = e
                teile = i.split('.')
                for j, t in enumerate(teile):  # Typwahl mit genau einem Typ auch unter dem JSON-Namen
                    if t.endswith('[x]'):
                        typen = (ids.get('.'.join(teile[:j + 1])) or {}).get('type', [])
                        if len(typen) == 1:
                            c = typen[0]['code']
                            els.setdefault(kanon('.'.join(teile[:j] + [t[:-3] + c[0].upper() + c[1:]] + teile[j + 1:])), e)
            self._index[sd_url] = els
        return self._index[sd_url]

    def pruefe(self, sd_url, k, wertelisten):
        els = self._elemente(sd_url)
        urls = {w.get('url') for w in wertelisten if w.get('aufgeloest')}

        def vs_von(e):
            return ((e or {}).get('binding') or {}).get('valueSet', '').split('|')[0]
        for x, e in els.items():
            if x.startswith(k + ':') and '.' not in x[len(k) + 1:] and vs_von(e) in urls:
                return 'gleich, aber am Slice', {'slice': x.rsplit(':', 1)[1], 'profil': vs_von(e),
                                                 'staerke_profil': e['binding'].get('strength', ''), 'wo': 'am Slice'}
        kandidaten = [(k, 'am Element')]
        if re.search(r'\.coding(:[^.]+)?(\.code)?$', k):
            kandidaten.append((re.sub(r'\.coding(:[^.]+)?(\.code)?$', '', k), 'am CodeableConcept'))
        if re.search(r'\.extension:[^.]+$', k):
            kandidaten.append((k + '.value[x]', 'am Wert der Extension'))
        for x, wo in kandidaten:
            vs = vs_von(els.get(x))
            if vs:
                info = {'profil': vs, 'staerke_profil': els[x]['binding'].get('strength', ''), 'wo': wo}
                if vs in urls:
                    return 'gleich', info
                if all(w.get('aufgeloest') for w in wertelisten):
                    return 'abweichend', info
                return 'ungeklärt', info
        return 'ohne Bindung', {}
