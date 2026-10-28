"""Hinweis zur KI-Nutzung: Logo mit Text auf jeder Seite, in jedem Prüfbericht und in der README."""
import html
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import hilfe  # noqa: F401
from mx import bauen
from mx.grundlagen import BERICHTE, KI_HINWEIS, KI_LOGO, WURZEL
from mx.konfig import alle_projekte


class KiHinweisTest(unittest.TestCase):
    def test_logo_ist_svg_mit_titel(self):
        svg = KI_LOGO.read_text(encoding='utf-8')
        self.assertTrue(svg.startswith('<svg '))
        self.assertIn('<title>KI-gestützt erstellt</title>', svg)

    def test_jede_seite_zeigt_logo_und_hinweis(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(bauen, 'AUSGABE', Path(tmp)):
            d = bauen.projekt_bauen('epa-patient-summary')
            bauen.seite_schreiben(d)
            bauen.index_schreiben([d])
            for name in ('epa-patient-summary.html', 'index.html'):
                with self.subTest(seite=name):
                    seite = (Path(tmp) / name).read_text(encoding='utf-8')
                    self.assertIn('<details class="ki-hinweis">', seite)
                    self.assertIn('<title>KI-gestützt erstellt</title>', seite)
                    self.assertIn(html.escape(KI_HINWEIS), seite)
                    self.assertIn('.ki-hinweis p {', seite)
                    self.assertNotIn('KI-HINWEIS', seite)

    def test_berichte_und_readme(self):
        for pid in alle_projekte():
            with self.subTest(bericht=pid):
                self.assertIn(KI_HINWEIS, (BERICHTE / f'{pid}.md').read_text(encoding='utf-8'))
        self.assertIn(KI_HINWEIS, (WURZEL / 'README.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
