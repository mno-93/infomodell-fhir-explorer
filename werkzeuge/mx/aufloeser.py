"""Prüft Elementpfade aus dem Informationsmodell gegen Profil-Snapshots — wie ein Validator:
Slices, Typwahl, Extension-Definitionen und Datentypen werden aufgelöst.

Ergebnis je Pfad: (status, grund)
  exakt            Pfad ist eine Elementkennung des Profil-Snapshots
  schreibvariante  gemeint ist eindeutig ein Element, die Schreibweise mischt aber zwei Notationen
                   (`value[x].valueQuantity` statt `value[x]:valueQuantity`) — vereinheitlichen
  gleichwertig     gültige andere Schreibweise derselben Stelle, keine Korrektur nötig: JSON-Name der
                   Typwahl (`valueCodeableConcept` statt `value[x]`) oder Typ-Slice, den das Profil nicht
                   eigens ausweist (`manufacturer[x]:manufacturerString` — präziser als `manufacturer[x]`)
  ueber-definition gültig, aber erst über die Extension-Definition oder den Datentyp auflösbar
  verboten         Element existiert, ist im Profil aber auf 0..0 gesetzt
  fehler           Pfad führt auf kein Element
  unbekannt        benötigte Definition liegt nicht im Paketbestand
"""
import re


def segmente(pfad):
    return [s for s in re.split(r'\.(?![^\[]*\])', pfad) if s] if pfad else []


class Aufloeser:
    def __init__(self, sds):
        self.sds = sds
        self.datentyp = {d['type']: d for d in sds.values()
                         if d['url'] == 'http://hl7.org/fhir/StructureDefinition/' + d['type']}
        self._ids = {}

    def ids(self, sd):
        if sd['url'] not in self._ids:
            self._ids[sd['url']] = {e['id']: e for e in sd['snapshot']['element']}
        return self._ids[sd['url']]

    def pruefe(self, sd, pfad):
        """pfad ohne Ressourcentyp, z. B. 'value[x].valueQuantity.value'."""
        varianten, ueber = [], []
        segs = segmente(pfad)
        # value[x] + valueQuantity zu einem Segment zusammenführen
        norm, i = [], 0
        while i < len(segs):
            s = segs[i]
            if s.endswith('[x]') and i + 1 < len(segs) and segs[i + 1].startswith(s[:-3]) \
                    and segs[i + 1][len(s) - 3:][:1].isupper():
                norm.append(s + ':' + segs[i + 1])
                varianten.append(('mischung', f'`{s}.{segs[i + 1]}` statt `{s}:{segs[i + 1]}`'))
                i += 2
                continue
            norm.append(s)
            i += 1
        ergebnis = self._gehe(sd, sd['type'], norm, varianten, ueber)
        if ergebnis:
            return ergebnis
        if ueber:
            return 'ueber-definition', 'aufgelöst über ' + ', '.join(ueber) + ('; ' + '; '.join(t for _a, t in varianten) if varianten else '')
        if any(a == 'mischung' for a, _t in varianten):
            return 'schreibvariante', '; '.join(t for _a, t in varianten)
        if varianten:
            return 'gleichwertig', '; '.join(t for _a, t in varianten)
        return 'exakt', ''

    def _gehe(self, sd, cur, norm, varianten, ueber):
        for pos, seg in enumerate(norm):
            ids = self.ids(sd)
            name, _, sl = seg.partition(':')
            if cur + '.' + seg in ids:
                cur = cur + '.' + seg
                if ids[cur].get('max') == '0':
                    return 'verboten', f'`{cur}` ist im Profil `{sd["id"]}` auf 0..0 gesetzt'
                continue
            # Typwahl: valueQuantity oder value[x]:valueQuantity an value[x]
            basis = None
            for x in ids:
                rest = x[len(cur) + 1:]
                if x.startswith(cur + '.') and x.endswith('[x]') and '.' not in rest and ':' not in rest:
                    b = rest[:-3]
                    if (name.startswith(b) and name[len(b):][:1].isupper()) or (name == b + '[x]' and sl.startswith(b)):
                        basis = x
            if basis:
                gewaehlt = sl if name.endswith('[x]') else name
                typname = gewaehlt[len(basis.split('.')[-1]) - 3:]
                erlaubt = [t['code'] for t in ids[basis].get('type', [])]
                if not any(t.lower() == typname.lower() for t in erlaubt):
                    return 'fehler', f'Typ `{typname}` an `{basis}` nicht zugelassen ({", ".join(erlaubt)})'
                kurz = basis.split('.')[-1]
                if name.endswith('[x]'):
                    varianten.append(('typslice', f'Typ-Slice `{seg}` im Profil nicht eigens ausgewiesen (Element `{kurz}`) — Typangabe bleibt gültig'))
                else:
                    varianten.append(('json', f'JSON-Name `{name}` für die Typwahl `{kurz}` — gleichwertig'))
                if basis + ':' + gewaehlt in ids:
                    cur = basis + ':' + gewaehlt
                    continue
                cur = basis
                if not any(x.startswith(cur + '.') for x in ids):
                    dt = (self.datentyp.get(typname) or self.datentyp.get(typname[0].lower() + typname[1:])
                          or self.datentyp.get(typname[0].upper() + typname[1:]))
                    if dt and pos + 1 < len(norm):
                        ueber.append('Datentyp ' + dt['type'])
                        return self._gehe(dt, dt['type'], norm[pos + 1:], varianten, ueber)
                continue
            if sl and cur + '.' + name in ids:
                andere = sorted(x.split(':', 1)[1] for x in ids if x.startswith(cur + '.' + name + ':') and '.' not in x[len(cur + '.' + name) + 1:])
                return 'fehler', f'Slice `{seg}` unter `{cur}` nicht definiert' + (f' (vorhanden: {", ".join(andere)})' if andere else '')
            # Snapshot endet hier: Extension-Definition oder Datentyp heranziehen
            e = ids.get(cur)
            hat_kinder = any(x.startswith(cur + '.') and x[len(cur) + 1:].split('.')[0].split(':')[0] == name for x in ids)
            if e and not hat_kinder:
                typen = e.get('type', [])
                if len(typen) == 1 and typen[0]['code'] == 'Extension' and typen[0].get('profile'):
                    url = typen[0]['profile'][0].split('|')[0]
                    ext = self.sds.get(url)
                    if not ext:
                        return 'unbekannt', f'Extension-Definition `{url}` nicht im Paketbestand'
                    ueber.append('Extension ' + url.split('/')[-1])
                    return self._gehe(ext, 'Extension', norm[pos:], varianten, ueber)
                if len(typen) == 1 and typen[0]['code'] in self.datentyp:
                    dt = self.datentyp[typen[0]['code']]
                    ueber.append('Datentyp ' + dt['type'])
                    return self._gehe(dt, dt['type'], norm[pos:], varianten, ueber)
            return 'fehler', f'`{seg}` gibt es unter `{cur}` nicht'
        return None
