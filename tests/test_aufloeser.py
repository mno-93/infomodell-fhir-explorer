"""Pfadauflösung gegen Profil-Snapshots — die Fälle aus der Mappingprüfung des Laborbefunds."""
import unittest

import hilfe  # noqa: F401
from mx.aufloeser import Aufloeser
from mx.konfig import projekt_laden
from mx.pakete import definitionen

LAB = 'https://gematik.de/fhir/epa-laboratory/StructureDefinition/'


class AufloeserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sds = definitionen(projekt_laden('laborbefund')['pakete'])
        cls.a = Aufloeser(cls.sds)

    def pruefe(self, profil, pfad):
        return self.a.pruefe(self.sds[LAB + profil], pfad)[0]

    def test_exakt(self):
        self.assertEqual(self.pruefe('observation-laboratory-study-dglp', 'interpretation.coding:hl7Interpretation'), 'exakt')

    def test_typwahl_mit_punkt_ist_schreibvariante(self):
        self.assertEqual(self.pruefe('observation-laboratory-study-dglp', 'value[x].valueQuantity.value'), 'schreibvariante')

    def test_verbotenes_element(self):
        self.assertEqual(self.pruefe('service-request-dglp', 'basedOn'), 'verboten')

    def test_tippfehler_im_datentyp(self):
        self.assertEqual(self.pruefe('observation-laboratory-study-dglp',
                                     'extension:alternativeResult.extension:value.value[x]:valueRange.high.ssystem'), 'fehler')

    def test_unbekannter_slice(self):
        self.assertEqual(self.pruefe('specimen-dglp', 'container.extension:SpecimenContainerDeviceR5.value[x]'), 'fehler')

    def test_richtiger_slice(self):
        self.assertIn(self.pruefe('specimen-dglp', 'container.extension:device.value[x]'), ('exakt', 'schreibvariante'))

    def test_primitiver_datentyp_mit_extension(self):
        self.assertNotEqual(self.pruefe('observation-laboratory-study-group-dglp', 'effectiveDateTime.extension'), 'fehler')


if __name__ == '__main__':
    unittest.main()
