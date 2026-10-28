"""Ein Projekt bauen: Profile, Informationsmodell, Anforderungen und alle Beispiele zu einem Datensatz
verknüpfen und als eigenständige HTML-Seite ausgeben. Die Ausgabe ist deterministisch (keine Zeitstempel)."""
import html
import json

from . import anforderungen, anzeige, beispiele, ehds, infomodell, validieren
from .grundlagen import AUSGABE, KI_HINWEIS, KI_LOGO, WURZEL
from .konfig import projekt_laden
from .pakete import bezeichnung, definitionen, projektpakete
from .profile import profil_aufbereiten
from .terminologie import Bindungsabgleich, Wertelisten

IM_TITEL = {'gematik-baum': 'Informationsmodell', 'mio-baum': 'Informationsmodell', 'aus-profilen': 'Struktur aus den Profilen'}


def projekt_bauen(pid):
    k = projekt_laden(pid)
    quellen = projektpakete(k)  # lokale Pakete zuerst
    sds = definitionen(quellen)
    wl = Wertelisten(quellen + k.get('terminologiepakete', []), sds)
    knoten, baum_aus = infomodell.laden(k, sds, wl)
    pruefung = infomodell.mappings_pruefen(knoten)
    # EHDS-Mappings (mio-baum) gegen die Logikmodelle der `logikmodellpakete`
    ehds_statistik, ehds_pruefung = None, []
    if k['informationsmodell']['art'] == 'mio-baum':
        logik = ehds.Logikmodelle(definitionen(k.get('logikmodellpakete', [])), ', '.join(k.get('logikmodellpakete', [])))
        ehds_statistik, ehds_pruefung = ehds.pruefen(knoten, logik)
    anf = anforderungen.laden(k, sds)

    genutzt = {m['sd'] for n in knoten for m in n['maps'] if m['sd']}
    for b in baum_aus or []:
        if 'y' in b:
            genutzt.add(b['y'][0])

    def profil_von(res):  # Profil enthaltener Ressourcen (contained)
        url, _wie = beispiele.profil_fuer(res, k, sds)
        return sds.get(url) if url else None

    validierung = validieren.ergebnis_laden(k)  # berichte/<projekt>.validierung.json, falls vorhanden
    liste = []
    for bk in k['beispiele']:
        ressourcen, bundle = beispiele.laden(k, bk)
        elemente, zuordnung = {}, {}
        for r in ressourcen:
            url, wie = beispiele.profil_fuer(r['res'], k, sds)
            if not url:
                raise SystemExit(f'{pid}/{bk["id"]}: {r["key"]} ohne bekanntes Profil')
            r['sd'], zuordnung[r['key']] = url, wie
            elemente.update(beispiele.zuordnen(r['res'], sds[url], r['key'], profil_von))
            for c in r['res'].get('contained', []):
                zuordnung[f'{r["key"]}#{c.get("id", "")}'] = beispiele.profil_fuer(c, k, sds)[1]
        genutzt.update(el.split('#', 1)[0] for el in elemente.values())
        werte = beispiele._wertindex(ressourcen)
        b = {
            'id': bk['id'], 'titel': bk['titel'], 'zweck': bk['zweck'], 'herkunft': bk['herkunft'],
            'quelle': bk.get('datei') or f'{bk["paket"]} · {bk["einstieg"]}',
            'bundle': bundle, 'ressourcen': ressourcen, 'elemente': elemente, 'profilzuordnung': zuordnung,
            'pdf': beispiele.pdf_text(ressourcen, werte) if 'pdf' in k.get('dokumente', []) else None,
            'texte': beispiele.erzaehltext(ressourcen, werte) if 'erzaehltext' in k.get('dokumente', []) else [],
        }
        b['abdeckung'] = beispiele.abdeckung(knoten, b)
        b['struktur'] = beispiele.struktur_pruefen(b, sds)
        b['validierung'] = validierung['beispiele'][bk['id']] if validierung else None
        liste.append(b)

    gemappt = {}
    for n in knoten:
        for m in n['maps']:
            if m['sd']:
                gemappt.setdefault(m['sd'], set()).add(m['k'])
    zusaetzlich = {}
    for b in baum_aus or []:
        if 'y' in b:
            zusaetzlich.setdefault(b['y'][0], set()).add(b['y'][1])
    ig = k.get('ig', {})
    profile = {}
    for u in sorted(genutzt):
        if u not in sds:
            continue
        seite = (ig['url'] + 'StructureDefinition-' + sds[u]['id'] + '.html') \
            if ig.get('kanonisch') and u.startswith(ig['kanonisch']) else None
        profile[u] = profil_aufbereiten(sds[u], gemappt.get(u, set()), seite, zusaetzlich.get(u, set()), wl)

    status = ('exakt', 'gleichwertig', 'schreibvariante', 'ueber-definition', 'verboten', 'fehler', 'unbekannt')
    statistik = {
        'im_knoten': len(knoten), 'im_mit_mapping': sum(1 for n in knoten if n['maps']),
        'mappings': sum(len(n['maps']) for n in knoten),
        'mapping_status': {s: sum(1 for n in knoten for m in n['maps'] if m['status'] == s) for s in status},
        'anderes_profil': sum(1 for p in pruefung if p['status'] == 'anderes-profil'),
        'anforderungen': len(anf), 'anforderungen_mit_pfad': sum(1 for a in anf if a['pfade']),
        'im_anforderungen': sum(len(n['anf']) for n in knoten),
        'ohne_ziel': sum(1 for n in knoten if n.get('ohne_ziel')),
        'ehds': ehds_statistik,
        'wertelisten': _wertelisten_statistik(knoten),
        'bindungsabgleich': _bindungsabgleich(knoten, sds),
        'baum_aus': {'knoten': len(baum_aus), 'zyklen': sum(1 for b in baum_aus if 'z' in b),
                     'aus_profil': sum(1 for b in baum_aus if 'y' in b),
                     'ausmodelliert': sum(1 for b in baum_aus if 'v' in b)} if baum_aus else None,
    }
    meta = {
        'projekt': pid, 'titel': k['titel'], 'beschreibung': k.get('beschreibung', ''),
        'darstellung': k['darstellung'], 'dokumente': k.get('dokumente', []),
        'im_art': k['informationsmodell']['art'], 'im_titel': IM_TITEL[k['informationsmodell']['art']],
        'im_hinweis': k['informationsmodell'].get('hinweis', ''), 'ig': ig,
        'pakete': [bezeichnung(q) for q in quellen], 'logikmodellpakete': k.get('logikmodellpakete', []),
        'lokale_pakete': [{'paket': bezeichnung(o), 'ordner': o.relative_to(WURZEL).as_posix()} for o in k['lokale_ordner']],
    }
    if validierung:
        validierung = {x: y for x, y in validierung.items() if x != 'beispiele'}
    return {'meta': meta, 'statistik': statistik, 'pruefung': pruefung, 'ehds_pruefung': ehds_pruefung, 'im': knoten,
            'baum_aus': baum_aus, 'profile': profile, 'anforderungen': anf, 'beispiele': liste, 'validierung': validierung,
            'anzeige': anzeige.ergebnis_laden(k)}


def _wertelisten_statistik(knoten):
    alle = {}
    for n in knoten:
        for w in n['wertelisten']:
            alle.setdefault(w['name'], w)
    return {'gesamt': len(alle), 'aufgeloest': sum(1 for w in alle.values() if w['aufgeloest']),
            'mit_link': sum(1 for w in alle.values() if w.get('seite')),
            'ohne': sorted(n for n, w in alle.items() if not w['aufgeloest'])}


def _bindungsabgleich(knoten, sds):
    """Werteliste im Modell gegen die Bindung im Profil — Regeln in `terminologie.Bindungsabgleich`."""
    from collections import Counter
    ba = Bindungsabgleich(sds)
    zaehlung, listen = Counter(), {'abweichend': [], 'ungeklärt': [], 'gleich, aber am Slice': []}
    for n in knoten:
        if not n['wertelisten']:
            continue
        for m in n['maps']:
            if not m['sd'] or '.' not in m['k'] or m['status'] in ('fehler', 'verboten', 'unbekannt'):
                continue
            art, info = ba.pruefe(m['sd'], m['k'], n['wertelisten'])
            zaehlung[art] += 1
            if art in listen:
                listen[art].append(dict(info, id=n['id'], im=n['name'], mapping=m['roh'],
                                        modell=', '.join(w['name'] for w in n['wertelisten']),
                                        vorschlag=(m['roh'] + ':' + info['slice']) if info.get('slice') else ''))
    return {'zaehlung': dict(sorted(zaehlung.items())), 'abweichend': listen['abweichend'],
            'ungeklaert': listen['ungeklärt'], 'slice': listen['gleich, aber am Slice']}


# Logo im Seitenkopf, aufklappbar mit dem Hinweistext; Farben der Seite (helles und dunkles Schema)
KI_CSS = '''.ki-hinweis { position: relative; flex: none; }
.ki-hinweis summary { list-style: none; cursor: pointer; display: flex; border-radius: 11px; }
.ki-hinweis summary::-webkit-details-marker { display: none; }
.ki-hinweis summary:focus-visible { outline: 2px solid var(--akzent); outline-offset: 2px; }
.ki-hinweis p { position: absolute; right: 0; top: calc(100% + 6px); z-index: 60; width: min(380px, 85vw); margin: 0;
  padding: 10px 12px; background: var(--flaeche); color: var(--text); border: 1px solid var(--linie); border-radius: 8px;
  box-shadow: 0 6px 20px rgba(0,0,0,.18); font-size: 12.5px; line-height: 1.45; font-weight: 400; }
@media (max-width: 600px) { .ki-hinweis p { position: fixed; top: auto; left: 12px; right: 12px; width: auto; margin-top: 6px; } }'''


def ki_hinweis():
    """Logo „KI-gestützt erstellt“ (inline, die Seiten bleiben eigenständig) mit aufklappbarem Hinweis."""
    svg = KI_LOGO.read_text(encoding='utf-8').strip()
    return (f'<details class="ki-hinweis"><summary title="Hinweis zur KI-Nutzung">{svg}</summary>'
            f'<p><b>Hinweis zur KI-Nutzung.</b> {html.escape(KI_HINWEIS)}</p></details>')


def seite_schreiben(daten):
    vorlage = (WURZEL / 'web' / 'explorer.html').read_text(encoding='utf-8')
    vorlage = vorlage.replace('/*KI-HINWEIS*/', KI_CSS).replace('<!--KI-HINWEIS-->', ki_hinweis())
    daten = {x: y for x, y in daten.items() if x != 'anzeige'}   # Ergebnis des Prüfmodus gehört in den Bericht, nicht in die Seite
    eingebettet =json.dumps(daten, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    seite = vorlage.replace('/*DATEN*/null', eingebettet).replace('<title>Modellexplorer</title>',
                                                                  f'<title>{html.escape(daten["meta"]["titel"])} – Modellexplorer</title>')
    AUSGABE.mkdir(exist_ok=True)
    (AUSGABE / f'{daten["meta"]["projekt"]}.html').write_text(seite, encoding='utf-8')


def validierung_kurz(d):
    """Kennzahl der FHIR-Validierung für die Übersichtsseite (HTML)."""
    v = d.get('validierung')
    if not d['beispiele']:
        return 'FHIR-Validierung: keine Beispiele im Projekt'
    if not v:
        return 'FHIR-Validierung: <b class="warn">noch nicht validiert</b>'
    s = v['summe']
    validiert = [b for b in d['beispiele'] if (b.get('validierung') or {}).get('status') in ('aktuell', 'veraltet')]
    veraltet = sum(1 for b in validiert if b['validierung']['status'] == 'veraltet')
    paket = sum(1 for b in d['beispiele'] if (b.get('validierung') or {}).get('status') == 'Paketbeispiel')
    teile = [f'<b class="{"fehler" if s["offen"] else "gut"}">{s["offen"]} Fehler</b>'
             + (f' (dazu {s["ausnahmen"]} begründete Ausnahme{"n" if s["ausnahmen"] != 1 else ""})' if s['ausnahmen'] else ''),
             f'{s["warnungen"]} Warnungen',
             f'{len(validiert)} von {len(d["beispiele"]) - paket} Beispieldateien validiert'
             + (' (Beispiele aus FHIR-Paketen prüft deren IG-Build)' if paket else '')]
    if veraltet:
        teile.append(f'<b class="warn">{veraltet} seit der Validierung geändert</b>')
    return f'FHIR-Validierung (HL7 Validator {html.escape(v["validator"])}): ' + ' · '.join(teile)


def index_schreiben(alle):
    zeilen = []
    for d in alle:
        s, m = d['statistik'], d['meta']
        st = s['mapping_status']
        modell = (f'{s["im_knoten"]} Elemente, {s["mappings"]} FHIR-Mappings, davon {st["fehler"] + st["verboten"]} fehlerhaft'
                  if m['im_art'] == 'gematik-baum' else 'kein veröffentlichtes Informationsmodell mit Mappings — Struktur aus den Profilen')
        if m['im_art'] == 'mio-baum':
            e = s['ehds']
            modell = (f'{s["im_knoten"]} Elemente, '
                      + (f'{s["mappings"]} FHIR-Mappings aus der Mappingtabelle des Projekts, davon {st["fehler"] + st["verboten"]} fehlerhaft'
                         if s['mappings'] else 'keine FHIR-Mappings')
                      + f'; EHDS-Mapping: {e["verweise"]} Verweise, {e["status"]["aufloesbar"]} auf ein Element und {e["status"]["nur-modell"]} '
                      f'auf ein Modell aufgelöst, '
                      f'{e["status"]["element-fehlt"] + e["status"]["modell-fehlt"]} nicht auflösbar, {e["anderes_modell"]} auf das Modell eines anderen Bausteins')
        bsp = ''.join(f'<li>{html.escape(b["titel"])} <span class="leise">— {html.escape(b["zweck"])}</span></li>' for b in d['beispiele'])
        zeilen.append(f'''<section class="karte"><h2><a href="{m["projekt"]}.html">{html.escape(m["titel"])}</a></h2>
<p>{html.escape(m["beschreibung"])}</p>
<p class="leise">{html.escape(m["ig"].get("name", ""))} · <code>{html.escape(m["ig"].get("paket", ""))}</code> · {html.escape(modell)}</p>
<p class="kennzahl">{validierung_kurz(d)}</p>
<h3>{len(d["beispiele"])} Beispiele</h3><ul>{bsp}</ul></section>''')
    seite = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Modellexplorer</title><style>
:root {{ --bg:#f6f7f9; --flaeche:#fff; --linie:#d9dde3; --text:#1c2430; --leise:#5b6676; --akzent:#1f5fae; --gut:#1d7a46; --warn:#a15c00; --fehler:#b42318; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#12161c; --flaeche:#1a1f27; --linie:#313947; --text:#e3e8ef; --leise:#9aa5b4; --akzent:#7fb0f0; --gut:#5cc48a; --warn:#e3a64a; --fehler:#f07c70; }} }}
:root[data-theme="dark"] {{ --bg:#12161c; --flaeche:#1a1f27; --linie:#313947; --text:#e3e8ef; --leise:#9aa5b4; --akzent:#7fb0f0; --gut:#5cc48a; --warn:#e3a64a; --fehler:#f07c70; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }}
main {{ max-width:900px; margin:0 auto; padding:24px 16px; }} h1 {{ font-size:24px; margin:0 0 4px; }}
.karte {{ background:var(--flaeche); border:1px solid var(--linie); border-radius:10px; padding:14px 18px; margin:16px 0; }}
.karte h2 {{ margin:0 0 6px; font-size:18px; }} .karte h3 {{ font-size:14px; margin:10px 0 2px; }}
a {{ color:var(--akzent); }} .leise {{ color:var(--leise); font-size:13.5px; }} code {{ font-size:12.5px; }} ul {{ margin:4px 0; padding-left:20px; }}
.kennzahl {{ font-size:13.5px; margin:6px 0; }} .kennzahl b.gut {{ color:var(--gut); }} .kennzahl b.fehler {{ color:var(--fehler); }} .kennzahl b.warn {{ color:var(--warn); }}
.titelzeile {{ display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; }}
{KI_CSS}
</style></head><body><main><div class="titelzeile"><h1>Modellexplorer</h1>{ki_hinweis()}</div>
<p class="leise">Informationsmodell, FHIR-Profile, Beispielinstanzen, Anwenderansicht und Dokument — auf Elementebene verknüpft.</p>
{"".join(zeilen)}</main></body></html>'''
    AUSGABE.mkdir(exist_ok=True)
    (AUSGABE / 'index.html').write_text(seite, encoding='utf-8')
