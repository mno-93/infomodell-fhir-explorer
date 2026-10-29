"""Abdeckung der Anzeige (`mx.py anzeige`) — ohne Browser: Ergebnis auslesen, Datei je Projekt, Abschnitt im Prüfbericht."""
import html
import json
import unittest

import hilfe  # noqa: F401
from mx import anzeige, bauen, berichte
from mx.konfig import alle_projekte, projekt_laden


class AuslesenTest(unittest.TestCase):
    def test_letztes_ergebnis_zaehlt(self):
        daten = {'beispiele': {'b1': [{'element': 'Patient · telecom.value', 'anzahl': 1, 'werte': ['0511 <1>']}]},
                 'verknuepfung': {'b1': []}}
        dom = ('<script>…`<pre id="anzeige-ergebnis">${esc(JSON.stringify(ergebnis))}</pre>`…</script>'
               f'<pre id="anzeige-ergebnis">{html.escape(json.dumps(daten))}</pre>')
        self.assertEqual(anzeige.auslesen(dom), daten)

    def test_ohne_ergebnis(self):
        with self.assertRaises(ValueError):
            anzeige.auslesen('<html><body></body></html>')


class ErgebnisdateienTest(unittest.TestCase):
    def test_jedes_projekt_mit_beispielen_hat_eine_aktuelle_datei(self):
        """Eingecheckte Ergebnisse nennen genau die Beispiele des Projekts (neues Beispiel → `mx.py anzeige` laufen lassen)."""
        for pid in alle_projekte():
            k = projekt_laden(pid)
            if not k['beispiele']:
                continue
            with self.subTest(projekt=pid):
                e = anzeige.ergebnis_laden(k)
                self.assertIsNotNone(e, f'berichte/{pid}.anzeige.json fehlt')
                self.assertEqual(e['fehlt'], [])
                self.assertEqual(sorted(e['beispiele']), sorted(b['id'] for b in k['beispiele']))

    def test_alle_verknuepfungen_tragen(self):
        """Instanz ↔ Profil ↔ Informationsmodell in allen Richtungen, mit Rückwegen und Klicks (Prüfmodus der Seite)."""
        for pid in alle_projekte():
            k = projekt_laden(pid)
            if not k['beispiele']:
                continue
            e = anzeige.ergebnis_laden(k)
            self.assertIsNotNone(e, f'berichte/{pid}.anzeige.json fehlt')
            for bid in e['beispiele']:
                with self.subTest(projekt=pid, beispiel=bid):
                    self.assertIn(bid, e['verknuepfung'], 'Ergebnis ohne Verknüpfungsprüfung — `mx.py anzeige` laufen lassen')
                    self.assertEqual(e['verknuepfung'][bid], [])

    def test_abschnitt_im_pruefbericht(self):
        d = bauen.projekt_bauen('impfung')
        z = '\n'.join(berichte.anzeige(d))
        self.assertIn('## Anzeige für Anwender:innen', z)
        self.assertIn('berichte/impfung.anzeige.json', z)
        d['anzeige'] = None
        self.assertIn('Noch nicht geprüft', '\n'.join(berichte.anzeige(d)))


if __name__ == '__main__':
    unittest.main()
