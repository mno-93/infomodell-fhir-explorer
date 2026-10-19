"""Terminologie des Informationsmodells: Tabellen nach Kopfzeilen, Wertelisten mit geprüftem Link, Abgleich mit der Profilbindung."""
import unittest

import hilfe  # noqa: F401
from mx import bauen
from mx.infomodell import terminologie
from mx.terminologie import staerke_trennen


class TerminologieTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = bauen.projekt_bauen('laborbefund')
        # „Freigabetyp“ gibt es zweimal (Composition, Provenance): über das Mapping eindeutig wählen
        cls.freigabetyp = next(n for n in cls.d['im'] if any(m['roh'] == 'CompositiondgLP.attester:legalAuthenticator.mode' for m in n['maps']))

    def test_tabelle_nach_kopfzeilen(self):
        tabelle = ('<table><tr><th>Konzept</th><th>Code</th><th>Display</th><th>CodeSystem</th><th>ValueSet</th></tr>'
                   '<tr><td>Rechtliche Verantwortung</td><td>legal</td><td>Legal</td><td>http://x</td><td>VS (required)</td></tr></table>')
        zeilen, wl, flach = terminologie('', tabelle, None)
        self.assertEqual(zeilen[0]['code'], 'legal')
        self.assertEqual(zeilen[0]['konzept'], 'Rechtliche Verantwortung')
        self.assertEqual(wl[0]['name'], 'VS')
        self.assertEqual(wl[0]['staerke'], 'required')
        self.assertEqual(flach, [{'code': 'legal', 'display': 'Legal', 'system': 'http://x'}])

    def test_staerke(self):
        self.assertEqual(staerke_trennen('LabStudyTypesEuVs (required)'), ('LabStudyTypesEuVs', 'required'))
        self.assertEqual(staerke_trennen('OhneStaerke'), ('OhneStaerke', ''))

    def test_freigabetyp_aus_der_liste(self):
        self.assertEqual(self.freigabetyp['terminologie'][0]['code'], 'legal')

    def test_werteliste_mit_link_auf_die_igseite(self):
        w = next(w for n in self.d['im'] for w in n['wertelisten'] if w['name'] == 'SpecimenTypeVS')
        self.assertEqual(w['seite'], 'https://gemspec.gematik.de/ig/fhir/terminology/1.1.0-ballot.2/ValueSet-specimen-type.html')

    def test_nicht_aufloesbare_werteliste_ohne_link(self):
        w = self.freigabetyp['wertelisten'][0]
        self.assertFalse(w['aufgeloest'])
        self.assertIsNone(w.get('seite'))

    def test_bindungsabgleich(self):
        ba = self.d['statistik']['bindungsabgleich']
        self.assertEqual(ba['abweichend'], [])
        self.assertIn('Freigabetyp', {x['im'] for x in ba['ungeklaert']})  # KBV-Werteliste nicht im Paketbestand
        self.assertEqual([x['vorschlag'] for x in ba['slice']], ['ObservationImageAttachmentdgLP.code.coding:snomed'])
        self.assertGreater(ba['zaehlung']['gleich'], 40)


if __name__ == '__main__':
    unittest.main()
