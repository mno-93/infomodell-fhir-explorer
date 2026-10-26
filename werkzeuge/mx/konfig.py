"""Projektkonfiguration `projekte/<id>/projekt.toml` lesen und prüfen."""
import tomllib

from .grundlagen import PROJEKTE

PFLICHT = ('id', 'titel', 'darstellung', 'pakete', 'informationsmodell', 'beispiele')
DARSTELLUNGEN = ('laborbefund', 'dokument')
DOKUMENTE = ('druck', 'pdf', 'erzaehltext')
IM_ARTEN = ('gematik-baum', 'aus-profilen')


class KonfigFehler(Exception):
    pass


def projekt_laden(pid, lokal_pruefen=True):
    """lokal_pruefen=False: lokale Pakete dürfen fehlen (beim Erzeugen mit `mx.py fsh`)."""
    pfad = PROJEKTE / pid / 'projekt.toml'
    with open(pfad, 'rb') as f:
        k = tomllib.load(f)
    fehlt = [p for p in PFLICHT if p not in k]
    if fehlt:
        raise KonfigFehler(f'{pfad}: fehlende Angaben {fehlt}')
    if k['id'] != pid:
        raise KonfigFehler(f'{pfad}: id "{k["id"]}" passt nicht zum Ordner "{pid}"')
    if k['darstellung'] not in DARSTELLUNGEN:
        raise KonfigFehler(f'{pfad}: darstellung muss eine von {DARSTELLUNGEN} sein')
    for d in k.get('dokumente', []):
        if d not in DOKUMENTE:
            raise KonfigFehler(f'{pfad}: unbekannte Dokumentansicht "{d}"')
    if k['informationsmodell'].get('art') not in IM_ARTEN:
        raise KonfigFehler(f'{pfad}: informationsmodell.art muss eine von {IM_ARTEN} sein')
    ids = [b['id'] for b in k['beispiele']]
    if len(ids) != len(set(ids)):
        raise KonfigFehler(f'{pfad}: Beispiel-ids sind nicht eindeutig')
    for b in k['beispiele']:
        for feld in ('id', 'titel', 'zweck', 'herkunft'):
            if not b.get(feld):
                raise KonfigFehler(f'{pfad}: Beispiel {b.get("id")} ohne "{feld}"')
        if not (b.get('datei') or b.get('einstieg')):
            raise KonfigFehler(f'{pfad}: Beispiel {b["id"]} braucht "datei" oder "einstieg"')
    k['ordner'] = PROJEKTE / pid
    # Lokale Pakete: Ordner im Projekt mit package/package.json und den Ressourcen eines FHIR-Pakets
    k['lokale_ordner'] = []
    for rel in k.get('lokale_pakete', []):
        ordner = k['ordner'] / rel
        if lokal_pruefen and not (ordner / 'package' / 'package.json').exists():
            raise KonfigFehler(f'{pfad}: lokales Paket "{rel}" ohne package/package.json')
        k['lokale_ordner'].append(ordner)
    ausnahmen = [a.get('id') for a in k.get('validierung', {}).get('ausnahmen', []) if a.get('id')]
    if len(ausnahmen) != len(set(ausnahmen)):
        raise KonfigFehler(f'{pfad}: Kennungen der Validierungsausnahmen sind nicht eindeutig')
    return k


def alle_projekte():
    return sorted(p.name for p in PROJEKTE.iterdir() if (p / 'projekt.toml').exists())
