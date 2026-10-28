"""Projektmuster der Vertraulichkeitsprüfung: aus der Umgebung (CI-Secret), leer gesetzt = Fehler."""
import os
import unittest
from unittest import mock

import hilfe  # noqa: F401
from mx import vertraulich


class ProjektmusterTest(unittest.TestCase):
    def test_muster_aus_der_umgebung(self):
        with mock.patch.dict(os.environ, {'VERTRAULICH_MUSTER': '# Kommentar\ngeheim\n\nintern(?!-frei)\n'}):
            muster = vertraulich._projektmuster()
        self.assertEqual([m.pattern for _a, m in muster], ['geheim', 'intern(?!-frei)'])
        self.assertTrue(muster[0][1].search('GEHEIM'))  # ohne Groß-/Kleinschreibung

    def test_leer_gesetzt_bricht_ab(self):
        for wert in ('', '  \n'):
            with self.subTest(wert=wert), mock.patch.dict(os.environ, {'VERTRAULICH_MUSTER': wert}):
                with self.assertRaises(SystemExit):
                    vertraulich._projektmuster()


if __name__ == '__main__':
    unittest.main()
