"""Ein Projekt bauen: Profile, Informationsmodell, Anforderungen und alle Beispiele zu einem Datensatz
verknüpfen und als eigenständige HTML-Seite ausgeben. Die Ausgabe ist deterministisch (keine Zeitstempel)."""
import html
import json

from . import anforderungen, beispiele, infomodell
from .grundlagen import AUSGABE, WURZEL
from .konfig import projekt_laden
from .pakete import definitionen
from .profile import profil_aufbereiten
from .terminologie import Bindungsabgleich, Wertelisten

IM_TITEL = {'gematik-baum': 'Informationsmodell', 'aus-profilen': 'Struktur aus den Profilen'}


def projekt_bauen(pid):
    k = projekt_laden(pid)
    sds = definitionen(k['pakete'])
    wl = Wertelisten(k['pakete'] + k.get('terminologiepakete', []), sds)
    knoten, baum_aus = infomodell.laden(k, sds, wl)
    pruefung = infomodell.mappings_pruefen(knoten)
    anf = anforderungen.laden(k, sds)

    genutzt = {m['sd'] for n in knoten for m in n['maps'] if m['sd']}
    for b in baum_aus or []:
        if 'y' in b:
            genutzt.add(b['y'][0])

    liste = []
    for bk in k['beispiele']:
        ressourcen, bundle = beispiele.laden(k, bk)
        elemente, zuordnung = {}, {}
        for r in ressourcen:
            url, wie = beispiele.profil_fuer(r['res'], k, sds)
            if not url:
                raise SystemExit(f'{pid}/{bk["id"]}: {r["key"]} ohne bekanntes Profil')
            r['sd'], zuordnung[r['key']] = url, wie
            genutzt.add(url)
            elemente.update(beispiele.zuordnen(r['res'], sds[url], r['key']))
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
        'im_hinweis': k['informationsmodell'].get('hinweis', ''), 'ig': ig, 'pakete': k['pakete'],
    }
    return {'meta': meta, 'statistik': statistik, 'pruefung': pruefung, 'im': knoten, 'baum_aus': baum_aus,
            'profile': profile, 'anforderungen': anf, 'beispiele': liste}


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


def seite_schreiben(daten):
    vorlage = (WURZEL / 'web' / 'explorer.html').read_text(encoding='utf-8')
    eingebettet = json.dumps(daten, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    seite = vorlage.replace('/*DATEN*/null', eingebettet).replace('<title>Modellexplorer</title>',
                                                                  f'<title>{html.escape(daten["meta"]["titel"])} – Modellexplorer</title>')
    AUSGABE.mkdir(exist_ok=True)
    (AUSGABE / f'{daten["meta"]["projekt"]}.html').write_text(seite, encoding='utf-8')


def index_schreiben(alle):
    zeilen = []
    for d in alle:
        s, m = d['statistik'], d['meta']
        st = s['mapping_status']
        modell = (f'{s["im_knoten"]} Elemente, {s["mappings"]} FHIR-Mappings, davon {st["fehler"] + st["verboten"]} fehlerhaft'
                  if m['im_art'] == 'gematik-baum' else 'kein veröffentlichtes Informationsmodell mit Mappings — Struktur aus den Profilen')
        bsp = ''.join(f'<li>{html.escape(b["titel"])} <span class="leise">— {html.escape(b["zweck"])}</span></li>' for b in d['beispiele'])
        zeilen.append(f'''<section class="karte"><h2><a href="{m["projekt"]}.html">{html.escape(m["titel"])}</a></h2>
<p>{html.escape(m["beschreibung"])}</p>
<p class="leise">{html.escape(m["ig"].get("name", ""))} · <code>{html.escape(m["ig"].get("paket", ""))}</code> · {html.escape(modell)}</p>
<h3>{len(d["beispiele"])} Beispiele</h3><ul>{bsp}</ul></section>''')
    seite = f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Modellexplorer</title><style>
:root {{ --bg:#f6f7f9; --flaeche:#fff; --linie:#d9dde3; --text:#1c2430; --leise:#5b6676; --akzent:#1f5fae; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#12161c; --flaeche:#1a1f27; --linie:#313947; --text:#e3e8ef; --leise:#9aa5b4; --akzent:#7fb0f0; }} }}
:root[data-theme="dark"] {{ --bg:#12161c; --flaeche:#1a1f27; --linie:#313947; --text:#e3e8ef; --leise:#9aa5b4; --akzent:#7fb0f0; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }}
main {{ max-width:900px; margin:0 auto; padding:24px 16px; }} h1 {{ font-size:24px; margin:0 0 4px; }}
.karte {{ background:var(--flaeche); border:1px solid var(--linie); border-radius:10px; padding:14px 18px; margin:16px 0; }}
.karte h2 {{ margin:0 0 6px; font-size:18px; }} .karte h3 {{ font-size:14px; margin:10px 0 2px; }}
a {{ color:var(--akzent); }} .leise {{ color:var(--leise); font-size:13.5px; }} code {{ font-size:12.5px; }} ul {{ margin:4px 0; padding-left:20px; }}
</style></head><body><main><h1>Modellexplorer</h1>
<p class="leise">Informationsmodell, FHIR-Profile, Beispielinstanzen, Anwenderansicht und Dokument — auf Elementebene verknüpft.</p>
{"".join(zeilen)}</main></body></html>'''
    AUSGABE.mkdir(exist_ok=True)
    (AUSGABE / 'index.html').write_text(seite, encoding='utf-8')
