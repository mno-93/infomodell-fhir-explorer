"""Modellexplorer — Kommandozeile.

  python3 werkzeuge/mx.py holen [--aktualisieren]   Pakete in die Caches holen (Projekte, Paketbestand des Validators),
                                                 Pakete und Quellen gegen die Sperrdatei prüfen
  python3 werkzeuge/mx.py bauen [projekt …]         Seiten nach ausgabe/, Prüfberichte nach berichte/
  python3 werkzeuge/mx.py pruefen [projekt …]       Konfiguration und Strukturbefunde prüfen (Exit-Code ≠ 0 bei Befund)
  python3 werkzeuge/mx.py validieren [projekt …]    Beispieldateien mit dem HL7 FHIR Validator prüfen (Java nötig),
                                                 Ergebnis nach berichte/<projekt>.validierung.json
  python3 werkzeuge/mx.py fsh <projekt>             lokales Paket des Projekts aus FSH neu erzeugen (SUSHI nötig)
  python3 werkzeuge/mx.py vertraulich               versionierte Dateien gegen .vertraulich-muster prüfen

Nur Python-Standardbibliothek (ab 3.11).
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mx import bauen, berichte, pakete  # noqa: E402
from mx.konfig import alle_projekte, projekt_laden  # noqa: E402


def holen(args):
    # lokale Pakete (`lokale_pakete`) liegen im Projektordner: nicht holen, nicht in die Sperrdatei
    sperre = pakete.sperre_laden()
    specs = sorted({p for pid in alle_projekte() for k in [projekt_laden(pid)]
                    for p in k['pakete'] + k.get('terminologiepakete', []) + k.get('logikmodellpakete', [])})
    for spec in specs:
        pakete.paket_sicherstellen(spec, sperre, aktualisieren=args.aktualisieren)
    from mx import validieren as v
    bestand = v.bestand_sicherstellen(sperre, aktualisieren=args.aktualisieren)
    # Sperrdatei: genau die benötigten Pakete (Projekte und Paketbestand des Validators)
    sperre['pakete'] = {s: sperre['pakete'][s] for s in set(specs) | set(bestand)}
    for pid in alle_projekte():
        k = projekt_laden(pid)
        for q in k.get('quellen', []):
            pakete.quelle_pruefen(k['ordner'] / q['datei'], q['url'], sperre, aktualisieren=args.aktualisieren)
    pakete.sperre_schreiben(sperre)
    print(f'{len(specs)} Pakete, Paketbestand des Validators ({len(bestand)} Pakete) und alle Quellen geprüft.')


def bauen_(args):
    alle = []
    for pid in args.projekte or alle_projekte():
        d = bauen.projekt_bauen(pid)
        bauen.seite_schreiben(d)
        berichte.schreiben(d)
        alle.append(d)
        s = d['statistik']
        print(f'{pid}: {len(d["beispiele"])} Beispiele, {s["mappings"]} Mappings '
              f'({s["mapping_status"]["fehler"] + s["mapping_status"]["verboten"]} fehlerhaft), '
              f'{sum(len(b["struktur"]) for b in d["beispiele"])} Strukturbefunde')
    if not args.projekte:
        bauen.index_schreiben(alle)


def pruefen(args):
    fehler = 0
    for pid in args.projekte or alle_projekte():
        k = projekt_laden(pid)
        d = bauen.projekt_bauen(pid)
        erlaubt = {a['element'] for a in k.get('strukturausnahmen', [])}
        for b in d['beispiele']:
            for x in b['struktur']:
                if x['element'] not in erlaubt:
                    print(f'{pid}/{b["id"]}: {x["element"]} — {x["grund"]}')
                    fehler += 1
        genutzt = {x['element'] for b in d['beispiele'] for x in b['struktur']}
        for a in sorted(erlaubt - genutzt):
            print(f'Hinweis {pid}: Strukturausnahme ohne Treffer: {a}')
    print('Strukturprüfung: ' + ('keine Befunde' if not fehler else f'{fehler} Befunde'))
    sys.exit(1 if fehler else 0)


def validieren(args):
    from mx import validieren as v
    sys.exit(v.alle(args.projekte or alle_projekte()))


def fsh(args):
    from mx import fsh as f
    sys.exit(f.bauen(args.projekt))


def vertraulich(_args):
    from mx import vertraulich as v
    sys.exit(v.pruefen())


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='befehl', required=True)
    h = sub.add_parser('holen')
    h.add_argument('--aktualisieren', action='store_true', help='Sperrdatei neu schreiben, Quellen neu laden')
    h.set_defaults(f=holen)
    for name, f in (('bauen', bauen_), ('pruefen', pruefen), ('validieren', validieren)):
        s = sub.add_parser(name)
        s.add_argument('projekte', nargs='*')
        s.set_defaults(f=f)
    sub.add_parser('vertraulich').set_defaults(f=vertraulich)
    s = sub.add_parser('fsh')
    s.add_argument('projekt')
    s.set_defaults(f=fsh)
    args = p.parse_args()
    args.f(args)


if __name__ == '__main__':
    main()
