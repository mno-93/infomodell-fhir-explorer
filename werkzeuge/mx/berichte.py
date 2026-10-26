"""Prüfbericht je Projekt als Markdown — deterministisch, damit die CI Abweichungen per `git diff` erkennt."""
import re

from .grundlagen import BERICHTE
from .validieren import RANG

STATUS_TEXT = {'fehler': 'ohne Ziel', 'verboten': 'auf ein 0..0-Element', 'unbekannt': 'Definition fehlt',
               'anderes-profil': 'anderes Profil als das übergeordnete Element'}


def _code(s):
    return re.sub(r'`([^`]+)`', r'`\1`', s.replace('|', '\\|'))


def bericht(d):
    m, s = d['meta'], d['statistik']
    st = s['mapping_status']
    z = [f'# Prüfbericht — {m["titel"]}', '',
         '> Erzeugt von `python3 werkzeuge/mx.py bauen`. Nicht von Hand ändern; die CI prüft, dass der Bericht zum Stand passt.',
         '', '## Quellen', '',
         f'- Implementation Guide: {m["ig"].get("name", "—")} (`{m["ig"].get("paket", "—")}`, {m["ig"].get("status", "")})',
         f'- Darstellung des Modells: {m["im_titel"]}' + (f' — {m["im_hinweis"]}' if m['im_hinweis'] else ''),
         '- Pakete: ' + ', '.join(f'`{p}`' for p in m['pakete'])]
    for lp in m.get('lokale_pakete', []):
        z.append(f'- Lokales Paket (im Projekt, nicht veröffentlicht): `{lp["paket"]}` aus `{lp["ordner"]}/`')
    z.append('')
    if m['im_art'] == 'gematik-baum':
        z += ['## Mappingprüfung', '',
              '| Befund | Anzahl |', '|---|---:|',
              f'| Elemente im Informationsmodell | {s["im_knoten"]} |',
              f'| davon mit FHIR-Mapping | {s["im_mit_mapping"]} |',
              f'| FHIR-Mappings | {s["mappings"]} |',
              f'| exakt | {st["exakt"]} |',
              f'| gleichwertige Schreibweise (JSON-Name der Typwahl, Typ-Slice) — keine Korrektur nötig | {st["gleichwertig"]} |',
              f'| Schreibvariante (gemischte Notation) — vereinheitlichen | {st["schreibvariante"]} |',
              f'| über Extension-Definition oder Datentyp aufgelöst | {st["ueber-definition"]} |',
              f'| **ohne Ziel** | **{st["fehler"]}** |', f'| **auf ein 0..0-Element** | **{st["verboten"]}** |',
              f'| Definition nicht im Paketbestand | {st["unbekannt"]} |',
              f'| in ein anderes Profil als das übergeordnete Element | {s["anderes_profil"]} |', '']
        for titel, stati in (('Fehlerhafte Mappings', ('fehler', 'verboten', 'unbekannt')),
                             ('Mappings in ein anderes Profil', ('anderes-profil',)),
                             ('Schreibvarianten (gemischte Notation)', ('schreibvariante',)),
                             ('Gleichwertige Schreibweisen (keine Korrektur nötig)', ('gleichwertig',))):
            eintraege = [p for p in d['pruefung'] if p['status'] in stati]
            if not eintraege:
                continue
            z += [f'### {titel} ({len(eintraege)})', '', '| Element im Modell | Mapping | Befund |', '|---|---|---|']
            z += [f'| {p["im"]} <br>*{" / ".join(p["pfad"].split(" / ")[-3:-1])}* | `{p["mapping"]}` | {_code(p["grund"])} |'
                  for p in eintraege]
            z.append('')
        w = s.get('wertelisten') or {}
        if w.get('gesamt'):
            z += ['## Wertelisten', '', f'{w["gesamt"]} Wertelisten im Modell, davon {w["aufgeloest"]} im Paketbestand oder über eine '
                  f'Profilbindung aufgelöst, {w["mit_link"]} mit Link auf die Originalseite.', '']
            if w['ohne']:
                z += ['Nicht auflösbar (weder im Paketbestand noch in einer Profilbindung):', ''] + [f'- `{n}`' for n in w['ohne']] + ['']
        ba = s.get('bindungsabgleich') or {}
        if ba.get('zaehlung'):
            zl = ba['zaehlung']
            z += ['### Werteliste im Modell gegen Bindung im Profil', '',
                  'Je Mapping eines Elements mit Werteliste: Bindung am Element, am zugehörigen CodeableConcept, am Wert einer '
                  'gemappten Extension oder an einem Slice darunter.', '',
                  '| Ergebnis | Anzahl |', '|---|---:|'] + [f'| {k} | {v} |' for k, v in zl.items()] + ['']
            for titel, liste, spalte in (('Gleich, aber am Slice — Mapping präzisieren', ba.get('slice', []), 'vorschlag'),
                                         ('Abweichend', ba.get('abweichend', []), 'profil'),
                                         ('Ungeklärt — Werteliste des Modells nicht im Paketbestand', ba.get('ungeklaert', []), 'profil')):
                if liste:
                    z += [f'**{titel} ({len(liste)})**', '', '| Element im Modell | Mapping | Werteliste im Modell | ' +
                          ('Vorschlag' if spalte == 'vorschlag' else 'Bindung im Profil') + ' |', '|---|---|---|---|']
                    z += [f'| {x["im"]} | `{x["mapping"]}` | `{x["modell"]}` | `{x[spalte]}`' +
                          (f' ({x["staerke_profil"]}, {x["wo"]})' if spalte == 'profil' else '') + ' |' for x in liste]
                    z.append('')
        if s['baum_aus']:
            b = s['baum_aus']
            z += ['## Ausmodellierte Darstellung', '',
                  f'{b["knoten"]} Knoten · {b["ausmodelliert"]} Referenzen an der Verwendungsstelle aufgelöst · '
                  f'{b["zyklen"]} Zyklen erkannt · {b["aus_profil"]} Knoten aus FHIR-Profilen ergänzt', '']
    gedeckt = 'durch das Modell gedeckt' if m['im_art'] == 'gematik-baum' else 'durch die abgeleitete Struktur gedeckt'
    z += ['## Beispiele', '', f'| Beispiel | Ressourcen | fachliche Werte | {gedeckt} | Strukturbefunde |',
          '|---|---:|---:|---:|---:|']
    for b in d['beispiele']:
        a = b['abdeckung']
        z.append(f'| {b["titel"]} | {len(b["ressourcen"])} | {a["werte"]} | {a["gedeckt"]} | {len(b["struktur"])} |')
    z.append('')
    for b in d['beispiele']:
        z += [f'### {b["titel"]}', '', f'- Zweck: {b["zweck"]}', f'- Herkunft: {b["herkunft"]}', f'- Datei: `{b["quelle"]}`']
        ohne_profil = sorted({w for w in b['profilzuordnung'].values() if w != 'meta.profile'})
        if ohne_profil:
            z.append('- Profilzuordnung ohne `meta.profile`: ' + ', '.join(
                f'{sum(1 for v in b["profilzuordnung"].values() if v == w)}× {w}' for w in ohne_profil))
        if b['struktur']:
            z += ['', '**Strukturbefunde** (Element im Profil nicht auflösbar):', '']
            z += [f'- `{x["element"]}` — {_code(x["grund"])}' for x in b['struktur']]
        if b['abdeckung']['ohne_modell'] and d['meta']['im_art'] == 'gematik-baum':
            z += ['', 'Werte ohne spezifisches Element im Informationsmodell (ohne url, reference, system, version, Erzähltext):', '']
            z += [f'- `{el.split("/")[-1]}` ({n}×)' for el, n in b['abdeckung']['ohne_modell'].items()]
        z.append('')
    z += validierung(d)
    return '\n'.join(z).rstrip() + '\n'


STATUS_VALIDIERUNG = {'veraltet': '⚠ Beispieldatei seit der Validierung geändert — neu validieren',
                      'nicht validiert': 'noch nicht validiert', 'Paketbeispiel': 'nicht validiert (Beispiel aus einem FHIR-Paket)'}


def meldungsgruppen(meldungen):
    """Gleiche Meldungen (Stufe, Text, Ausnahme) zusammenfassen: [(stufe, text, ausnahme, [Meldungen])],
    sortiert nach Stufe und Text — gemeinsam für Prüfbericht und Oberfläche."""
    gruppen = {}
    for m in meldungen:
        gruppen.setdefault((m['stufe'], m['text'], m.get('ausnahme') or ''), []).append(m)
    return [(s, t, a, ms) for (s, t, a), ms in sorted(gruppen.items(), key=lambda g: (RANG.get(g[0][0], 9), g[0][1], g[0][2]))]


def _ort(x):
    return (f'`{x["ort"]}`' if x.get('ort') else '—') + (f' (Zeile {x["zeile"]})' if x.get('zeile') else '')


def _gruppe(stufe, text, ausnahme, ms, zeigen=3):
    anzahl = f' ({len(ms)}×)' if len(ms) > 1 else ''
    orte = ', '.join(_ort(x) for x in ms[:zeigen]) + (f' und {len(ms) - zeigen} weitere' if len(ms) > zeigen else '')
    return (f'- **{stufe}**{anzahl}: {_code(text)}' + (f' — begründete Ausnahme `{ausnahme}`' if ausnahme else '')
            + f'<br>{orte}')


def validierung(d):
    """Abschnitt „FHIR-Validierung“ aus `berichte/<projekt>.validierung.json` (geschrieben von `mx.py validieren`)."""
    v, pid = d.get('validierung'), d['meta']['projekt']
    if not v:
        return ['## FHIR-Validierung', '',
                f'Noch nicht validiert — `python3 -I werkzeuge/mx.py validieren {pid}` schreibt `berichte/{pid}.validierung.json`.', '']
    s = v['summe']
    z = [f'## FHIR-Validierung (HL7 Validator {v["validator"]})', '',
         f'Stand: `berichte/{pid}.validierung.json`, geschrieben von `python3 -I werkzeuge/mx.py validieren {pid}`; '
         f'FHIR {v["fhir"]}, Optionen `{" ".join(v["optionen"])}` (ohne Terminologieserver).', '',
         '- Pakete: ' + ', '.join(f'`{p}`' for p in v['pakete']),
         f'- Ergebnis: **{s["offen"]} Fehler**, {s["ausnahmen"]} als begründete Ausnahme, {s["warnungen"]} Warnungen, '
         f'{s["hinweise"]} Hinweise', '',
         '| Beispiel | Fehler | davon begründete Ausnahme | Warnungen | Hinweise | Stand |', '|---|---:|---:|---:|---:|---|']
    for b in d['beispiele']:
        e = b.get('validierung') or {}
        if e.get('status') in ('aktuell', 'veraltet'):
            z.append(f'| {b["titel"]} | {e["fehler"]} | {e["ausnahmen"]} | {e["warnungen"]} | {e["hinweise"]} | '
                     f'{STATUS_VALIDIERUNG.get(e["status"], e["status"])} |')
        else:
            z.append(f'| {b["titel"]} | – | – | – | – | {STATUS_VALIDIERUNG.get(e.get("status"), "noch nicht validiert")} |')
    z.append('')
    if v['ausnahmen']:
        z += ['**Begründete Ausnahmen** (`[[validierung.ausnahmen]]` in `projekt.toml`):', '']
        z += [f'- `{a["id"]}` — {a["treffer"]} Treffer{" ⚠" if not a["treffer"] else ""}: {_code(a["grund"])}'
              for a in v['ausnahmen']]
        z.append('')
    for b in d['beispiele']:
        e = b.get('validierung') or {}
        if e.get('meldungen'):
            z += [f'### Fehler und Warnungen — {b["titel"]}', '',
                  'Gleiche Meldungen zusammengefasst; Ort als FHIRPath, Zeile in der Beispieldatei.', '']
            z += [_gruppe(*g) for g in meldungsgruppen(e['meldungen'])] + ['']
    return z


def schreiben(d):
    BERICHTE.mkdir(exist_ok=True)
    (BERICHTE / f'{d["meta"]["projekt"]}.md').write_text(bericht(d), encoding='utf-8')
