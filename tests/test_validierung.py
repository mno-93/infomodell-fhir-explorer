"""Ergebnis des HL7 Validators einlesen und darstellen — ohne Java: Zuordnung zu den Beispielen, Ausnahmen,
Sortierung, Pfade, Stand der Beispieldatei, Abschnitt im Prüfbericht, Kennzahl der Übersichtsseite."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import hilfe  # noqa: F401
from mx import bauen, berichte, validieren
from mx.grundlagen import WURZEL
from mx.konfig import projekt_laden

OO_DATEI = 'http://hl7.org/fhir/StructureDefinition/operationoutcome-file'
OO_ZEILE = 'http://hl7.org/fhir/StructureDefinition/operationoutcome-issue-line'


def issue(stufe, ort, text, zeile=None):
    i = {'severity': stufe, 'code': 'processing', 'details': {'text': text}, 'expression': [ort]}
    if zeile:
        i['extension'] = [{'url': OO_ZEILE, 'valueInteger': zeile}]
    return i


def ausgabe(dateien):
    """Ausgabe des Validators für mehrere Dateien: Bundle aus OperationOutcomes, je Datei eine Erweiterung."""
    return {'resourceType': 'Bundle', 'entry': [
        {'resource': {'resourceType': 'OperationOutcome', 'extension': [{'url': OO_DATEI, 'valueString': str(d)}],
                      'issue': issues}} for d, issues in dateien]}


class ValidierungEinlesenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = projekt_laden('patient-summary')
        cls.hoffmann = cls.k['ordner'] / 'beispiele' / 'hoffmann.json'
        cls.yildiz = cls.k['ordner'] / 'beispiele' / 'yildiz.json'
        roh = validieren.meldungen(ausgabe([
            (cls.yildiz, [issue('warning', 'Bundle.entry[1].resource/*Patient/p*/', 'zweite Warnung', 9),
                          issue('information', 'Bundle', 'nur gezählt')]),
            (cls.hoffmann, [issue('warning', 'Bundle.entry[2]', f'Datei {WURZEL / "projekte" / "x.json"} nicht lesbar', 20),
                            issue('error', 'Bundle.entry[3].resource/*Provenance/p1*/',
                                  "Entry 'https://example.org/Provenance/p1' isn't reachable by traversing links", 30),
                            issue('error', 'Bundle.entry[0]', 'echter Fehler', 5),
                            issue('warning', 'Bundle.entry[1]', 'erste Warnung', 10)]),
        ]))
        cls.daten = validieren.auswerten(cls.k, roh, '7.0.1')

    def beispiel(self, bid):
        return next(b for b in self.daten['beispiele'] if b['id'] == bid)

    def test_zuordnung_und_zaehlung(self):
        h, y = self.beispiel('hoffmann'), self.beispiel('yildiz')
        self.assertEqual((h['fehler'], h['ausnahmen'], h['warnungen'], h['hinweise']), (2, 1, 2, 0))
        self.assertEqual((y['fehler'], y['warnungen'], y['hinweise']), (0, 1, 1))
        self.assertEqual(self.daten['summe'], {'fehler': 2, 'ausnahmen': 1, 'warnungen': 3, 'hinweise': 1, 'offen': 1})
        self.assertEqual([b['id'] for b in self.daten['beispiele']], ['hoffmann', 'yildiz'])  # Reihenfolge wie projekt.toml

    def test_ausnahme_mit_kennung(self):
        h = self.beispiel('hoffmann')
        self.assertEqual([m.get('ausnahme') for m in h['meldungen'] if m['stufe'] == 'error'],
                         [None, 'provenance-versionsverweis'])
        self.assertEqual(self.daten['ausnahmen'][0]['treffer'], 1)

    def test_sortiert_ohne_hinweise(self):
        h = self.beispiel('hoffmann')
        self.assertEqual([(m['stufe'], m['ort']) for m in h['meldungen']],
                         [('error', 'Bundle.entry[0]'), ('error', 'Bundle.entry[3].resource/*Provenance/p1*/'),
                          ('warning', 'Bundle.entry[1]'), ('warning', 'Bundle.entry[2]')])
        self.assertEqual(h['meldungen'][0]['zeile'], 5)

    def test_ohne_absolute_pfade(self):
        text = json.dumps(self.daten, ensure_ascii=False)
        self.assertNotIn(str(WURZEL), text)
        self.assertNotIn(WURZEL.as_posix(), text)
        self.assertIn('Datei projekte/x.json nicht lesbar', text)
        self.assertEqual(self.beispiel('hoffmann')['datei'], 'beispiele/hoffmann.json')
        self.assertEqual(self.beispiel('hoffmann')['sha256'], validieren.datei_hash(self.hoffmann))

    def test_netzabhaengige_einzelheiten_vereinheitlicht(self):
        text = ("Profile reference 'https://example.org/p' has not been checked because it could not be found, and fetching "
                "it resulted in the error EFhirClientException: Unparseable HTML Source (line 1 column 549)")
        m = validieren.meldungen(ausgabe([(self.yildiz, [issue('warning', 'Bundle', text)])]))[0]
        self.assertEqual(m['text'], "Profile reference 'https://example.org/p' has not been checked because it could "
                                    "not be found; fetching it failed (response details omitted)")

    def test_unbekannte_datei_bricht_ab(self):
        roh = validieren.meldungen(ausgabe([(WURZEL / 'fremd.json', [issue('error', 'Bundle', 'x')])]))
        with self.assertRaises(SystemExit):
            validieren.auswerten(self.k, roh, '7.0.1')

    def test_einzelne_ressource_statt_bundle(self):
        oo = {'resourceType': 'OperationOutcome', 'extension': [{'url': OO_DATEI, 'valueString': str(self.yildiz)}],
              'issue': [issue('fatal', 'Bundle', 'kaputt')]}
        self.assertEqual([(m['stufe'], m['text']) for m in validieren.meldungen(oo)], [('fatal', 'kaputt')])

    def test_ergebnis_fuer_den_bau_und_veraltet(self):
        daten = copy.deepcopy(self.daten)
        daten['beispiele'][1]['sha256'] = '0' * 64  # yildiz seit der Validierung geändert
        with tempfile.TemporaryDirectory() as tmp:
            pfad = Path(tmp) / 'patient-summary.validierung.json'
            pfad.write_text(json.dumps(daten), encoding='utf-8')
            e = validieren.ergebnis_laden(self.k, pfad)
        self.assertEqual(e['validator'], '7.0.1')
        self.assertEqual(e['beispiele']['hoffmann']['status'], 'aktuell')
        self.assertEqual(e['beispiele']['yildiz']['status'], 'veraltet')
        self.assertNotIn('sha256', e['beispiele']['hoffmann'])

    def test_ohne_datei(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(validieren.ergebnis_laden(self.k, Path(tmp) / 'fehlt.json'))


class ValidierungDarstellenTest(unittest.TestCase):
    """Abschnitt im Prüfbericht und Kennzahl der Übersicht, mit und ohne Ergebnisdatei."""

    @classmethod
    def setUpClass(cls):
        cls.d = bauen.projekt_bauen('patient-summary')

    def test_bericht_ohne_ergebnis(self):
        d = dict(self.d, validierung=None)
        d['beispiele'] = [dict(b, validierung=None) for b in self.d['beispiele']]
        text = '\n'.join(berichte.validierung(d))
        self.assertIn('## FHIR-Validierung', text)
        self.assertIn('Noch nicht validiert', text)
        self.assertIn('noch nicht validiert', bauen.validierung_kurz(d))

    def test_bericht_mit_ergebnis(self):
        if not self.d['validierung']:
            self.skipTest('berichte/patient-summary.validierung.json fehlt')
        text = berichte.bericht(self.d)
        self.assertIn(f'## FHIR-Validierung (HL7 Validator {self.d["validierung"]["validator"]})', text)
        self.assertIn('| Beispiel | Fehler | davon begründete Ausnahme | Warnungen | Hinweise | Stand |', text)
        self.assertIn('HL7 Validator', bauen.validierung_kurz(self.d))
        for b in self.d['beispiele']:
            self.assertEqual(b['validierung']['status'], 'aktuell', f'{b["id"]}: neu validieren')

    def test_meldungen_gruppiert(self):
        ms = [{'stufe': 'warning', 'ort': 'b', 'text': 'W'}, {'stufe': 'error', 'ort': 'a', 'text': 'F'},
              {'stufe': 'warning', 'ort': 'a', 'text': 'W'}]
        g = berichte.meldungsgruppen(ms)
        self.assertEqual([(s, t, len(x)) for s, t, _a, x in g], [('error', 'F', 1), ('warning', 'W', 2)])

    def test_ergebnisdateien_passen_zu_den_beispielen(self):
        """Eingecheckte Validierungsergebnisse nennen genau die Beispieldateien des Projekts in deren Stand."""
        for pfad in sorted((WURZEL / 'berichte').glob('*.validierung.json')):
            pid = pfad.name.split('.')[0]
            k = projekt_laden(pid)
            e = validieren.ergebnis_laden(k)
            dateien = {b['id'] for b in k['beispiele'] if b.get('datei')}
            self.assertEqual({i for i, b in e['beispiele'].items() if b['status'] in ('aktuell', 'veraltet')}, dateien, pid)
            veraltet = [i for i, b in e['beispiele'].items() if b['status'] == 'veraltet']
            self.assertEqual(veraltet, [], f'{pid}: Beispiel geändert — `mx.py validieren {pid}`')


if __name__ == '__main__':
    unittest.main()
