"""Prüfbericht je Projekt als Markdown — deterministisch, damit die CI Abweichungen per `git diff` erkennt."""
import re

from .grundlagen import BERICHTE

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
         '- Pakete: ' + ', '.join(f'`{p}`' for p in m['pakete']), '']
    if m['im_art'] == 'gematik-baum':
        z += ['## Mappingprüfung', '',
              '| Befund | Anzahl |', '|---|---:|',
              f'| Elemente im Informationsmodell | {s["im_knoten"]} |',
              f'| davon mit FHIR-Mapping | {s["im_mit_mapping"]} |',
              f'| FHIR-Mappings | {s["mappings"]} |',
              f'| exakt | {st["exakt"]} |', f'| Schreibvariante | {st["schreibvariante"]} |',
              f'| über Extension-Definition oder Datentyp aufgelöst | {st["ueber-definition"]} |',
              f'| **ohne Ziel** | **{st["fehler"]}** |', f'| **auf ein 0..0-Element** | **{st["verboten"]}** |',
              f'| Definition nicht im Paketbestand | {st["unbekannt"]} |',
              f'| in ein anderes Profil als das übergeordnete Element | {s["anderes_profil"]} |', '']
        for titel, stati in (('Fehlerhafte Mappings', ('fehler', 'verboten', 'unbekannt')),
                             ('Mappings in ein anderes Profil', ('anderes-profil',)),
                             ('Schreibvarianten', ('schreibvariante',))):
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
        abw = s.get('bindungsabgleich') or []
        if abw:
            z += [f'### Werteliste im Modell ≠ Bindung im Profil ({len(abw)})', '',
                  '| Element im Modell | Mapping | Werteliste im Modell | Bindung im Profil |', '|---|---|---|---|']
            z += [f'| {x["im"]} | `{x["mapping"]}` | `{x["modell"]}` | `{x["profil"]}` ({x["staerke_profil"]}) |' for x in abw]
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
    return '\n'.join(z).rstrip() + '\n'


def schreiben(d):
    BERICHTE.mkdir(exist_ok=True)
    (BERICHTE / f'{d["meta"]["projekt"]}.md').write_text(bericht(d), encoding='utf-8')
