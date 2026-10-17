"""Konsistenz über alle Projekte und Beispiele: Konfiguration, Zuordnung, Struktur, Determinismus, Berichte."""
import json
import unittest

import hilfe  # noqa: F401
from mx import bauen, berichte
from mx.grundlagen import BERICHTE
from mx.konfig import alle_projekte, projekt_laden


class ProjekteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.daten = {pid: bauen.projekt_bauen(pid) for pid in alle_projekte()}

    def test_konfiguration_und_dateien(self):
        for pid in alle_projekte():
            k = projekt_laden(pid)
            for b in k['beispiele']:
                if b.get('datei'):
                    self.assertTrue((k['ordner'] / b['datei']).exists(), f'{pid}: {b["datei"]} fehlt')

    def test_jede_ressource_hat_ein_profil(self):
        for pid, d in self.daten.items():
            for b in d['beispiele']:
                for r in b['ressourcen']:
                    self.assertIn(r['sd'], d['profile'], f'{pid}/{b["id"]}: {r["key"]}')

    def test_jeder_knoten_ist_zugeordnet(self):
        for pid, d in self.daten.items():
            for b in d['beispiele']:
                self.assertTrue(all('#' in el for el in b['elemente'].values()), f'{pid}/{b["id"]}')

    def test_keine_strukturbefunde_ausser_ausnahmen(self):
        for pid, d in self.daten.items():
            erlaubt = {a['element'] for a in projekt_laden(pid).get('strukturausnahmen', [])}
            for b in d['beispiele']:
                offen = [x['element'] for x in b['struktur'] if x['element'] not in erlaubt]
                self.assertEqual(offen, [], f'{pid}/{b["id"]}')

    def test_slice_der_bewertung_wird_erkannt(self):
        b = next(b for b in self.daten['laborbefund']['beispiele'] if b['id'] == 'hoffmann-2026-08-12')
        el = b['elemente']['Observation/obs-f81d4fae-0-0|interpretation[0].coding[0].code']
        self.assertTrue(el.endswith('#Observation.interpretation.coding:hl7Interpretation.code'), el)

    def test_bau_ist_deterministisch(self):
        for pid in alle_projekte():
            zweiter = bauen.projekt_bauen(pid)
            self.assertEqual(json.dumps(self.daten[pid], sort_keys=True), json.dumps(zweiter, sort_keys=True), pid)

    def test_berichte_sind_aktuell(self):
        for pid, d in self.daten.items():
            datei = BERICHTE / f'{pid}.md'
            self.assertTrue(datei.exists(), f'{datei} fehlt — `python3 werkzeuge/mx.py bauen`')
            self.assertEqual(datei.read_text(encoding='utf-8'), berichte.bericht(d),
                             f'{datei} passt nicht zum Stand — `python3 werkzeuge/mx.py bauen` und einchecken')


if __name__ == '__main__':
    unittest.main()
