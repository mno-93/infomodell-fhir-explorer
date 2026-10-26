"""Lokale Pakete (`lokale_pakete` in projekt.toml): geladen für Modell und Auflösung, von `holen` und Sperrdatei
übersprungen; enthaltene Ressourcen werden gegen ihr eigenes Profil zugeordnet."""
import unittest

import hilfe  # noqa: F401
from mx import bauen, fsh, pakete
from mx.grundlagen import json_laden
from mx.konfig import alle_projekte, projekt_laden

ENTWURF = 'https://example.org/fhir/impfung-entwurf/StructureDefinition/'


class LokalePaketeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k = projekt_laden('impfung')
        cls.d = bauen.projekt_bauen('impfung')

    def test_lokales_paket_wird_geladen(self):
        self.assertEqual([o.name for o in self.k['lokale_ordner']], ['paket'])
        quellen = pakete.projektpakete(self.k)
        self.assertEqual(quellen[0], self.k['ordner'] / 'paket')  # Vorrang vor den Paketen aus dem Cache
        sds = pakete.definitionen(quellen)
        for pid in ('ps-immunization', 'ps-immunization-medication'):
            self.assertIn(ENTWURF + pid, sds)
            self.assertEqual(sds[ENTWURF + pid]['version'], '0.1.0')
        self.assertEqual(pakete.bezeichnung(quellen[0]), 'example.impfung.entwurf#0.1.0')
        self.assertEqual(self.d['meta']['pakete'][0], 'example.impfung.entwurf#0.1.0')
        self.assertEqual(self.d['meta']['lokale_pakete'], [{'paket': 'example.impfung.entwurf#0.1.0', 'ordner': 'projekte/impfung/paket'}])

    def test_holen_und_sperrdatei_ueberspringen_lokale_pakete(self):
        specs = {p for pid in alle_projekte() for k in [projekt_laden(pid)] for p in k['pakete'] + k.get('terminologiepakete', [])}
        self.assertFalse(any(s.startswith('example.impfung.entwurf') for s in specs))
        self.assertFalse(any(s.startswith('example.impfung.entwurf') for s in pakete.sperre_laden()['pakete']))

    def test_paket_passt_zur_sushi_konfiguration(self):
        cfg = fsh.sushi_config((self.k['ordner'] / 'sushi-config.yaml').read_text(encoding='utf-8'))
        self.assertEqual(cfg['dependencies']['de.gematik.epa'], '1.4.0-ballot.1')
        self.assertEqual(json_laden(self.k['ordner'] / 'paket' / 'package' / 'package.json'), fsh.paket_json(cfg))

    def test_profile_haben_snapshot_und_auflage(self):
        sd = pakete.definitionen([self.k['ordner'] / 'paket'])[ENTWURF + 'ps-immunization']
        self.assertEqual(sd['baseDefinition'], 'http://hl7.eu/fhir/base/StructureDefinition/immunization-eu-core')
        self.assertIn('http://hl7.eu/fhir/eps/StructureDefinition/immunization-obl-eu-eps',
                      [e.get('valueCanonical') for e in sd.get('extension', [])])

    def test_enthaltene_ressource_mit_eigenem_profil(self):
        b = next(b for b in self.d['beispiele'] if b['id'] == 'erstdokumentation')
        el = b['elemente']['Immunization/imm-erst-influenza|contained[0].batch.lotNumber']
        self.assertEqual(el, ENTWURF + 'ps-immunization-medication#Medication.batch.lotNumber')
        self.assertEqual(b['profilzuordnung']['Immunization/imm-erst-influenza#impfstoff-1'], 'meta.profile')
        self.assertIn(ENTWURF + 'ps-immunization-medication', self.d['profile'])
        self.assertEqual(b['struktur'], [])

    def test_struktur_mit_zwei_einstiegen(self):
        wurzeln = [n for n in self.d['im'] if n['p'] is None]
        self.assertEqual([n['maps'][0]['sd'] for n in wurzeln], [ENTWURF + 'ps-immunization', ENTWURF + 'ps-immunization-medication'])

    def test_dosis_unbekannt_wird_zugeordnet(self):
        b = next(b for b in self.d['beispiele'] if b['id'] == 'nachtrag-impfpass')
        el = b['elemente']['Immunization/imm-nachtrag-dt-polio|protocolApplied[0]._doseNumberString.extension[0].valueCode']
        self.assertTrue(el.endswith('#Immunization.protocolApplied.doseNumberString.extension.valueCode'), el)


if __name__ == '__main__':
    unittest.main()
