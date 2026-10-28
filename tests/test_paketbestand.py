"""Paketbestand des HL7 Validators — ohne Netz und ohne Java: Hülle der Abhängigkeiten, feste Versionen, Bereinigung
des Caches; je Projekt dieselben Paketversionen für Darstellung und Validierung."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

import hilfe  # noqa: F401
from mx import pakete, validieren
from mx.konfig import alle_projekte, projekt_laden


def paket(ordner, name, version, abhaengigkeiten=None):
    p = ordner / 'package'
    p.mkdir(parents=True)
    (p / 'package.json').write_text(json.dumps({'name': name, 'version': version,
                                                'dependencies': abhaengigkeiten or {}}), encoding='utf-8')


class HuelleTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.basis = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def neu(self, spec, abhaengigkeiten=None):
        name, _, version = spec.partition('#')
        paket(self.basis / spec, name, version, abhaengigkeiten)

    def test_abhaengigkeiten_ohne_kernpakete(self):
        self.neu('a#1.0.0', {'b': '2.0.0', 'hl7.fhir.r4.core': '4.0.1'})
        self.neu('b#2.0.0', {'c': '1.0.0-ballot.1', 'hl7.fhir.r5.core': '5.0.0'})
        self.neu('c#1.0.0-ballot.1', {'a': '1.0.0'})
        sperre = {'pakete': {}, 'quellen': {}}
        erwartet = ['a#1.0.0', 'b#2.0.0', 'c#1.0.0-ballot.1']
        self.assertEqual(pakete.huelle_sicherstellen(['a#1.0.0'], self.basis, sperre), erwartet)
        self.assertEqual(sorted(sperre['pakete']), erwartet)

    def test_lokales_paket_bringt_nur_abhaengigkeiten(self):
        lokal = self.basis / 'lokal'
        paket(lokal, 'example.lokal', '0.1.0', {'a': '1.0.0'})
        self.neu('a#1.0.0')
        self.assertEqual(pakete.huelle_sicherstellen([lokal], self.basis, {'pakete': {}, 'quellen': {}}), ['a#1.0.0'])

    def test_abhaengigkeit_ohne_feste_version_bricht_ab(self):
        for version in ('current', '5.x', 'dev'):
            with self.subTest(version=version):
                ordner = self.basis / f'a-{version}'
                paket(ordner, 'a', '1.0.0', {'b': version})
                with self.assertRaises(SystemExit):
                    pakete.abhaengigkeiten(ordner)

    def test_platzhalter_nur_mit_festlegung(self):
        ordner = self.basis / 'mhd'
        paket(ordner, 'ihe.iti.mhd', '4.2.5-comment', {'ihe.formatcode.fhir': '1.5.x'})
        self.assertEqual(pakete.abhaengigkeiten(ordner, {'ihe.formatcode.fhir#1.5.x': '1.5.0'}),
                         ['ihe.formatcode.fhir#1.5.0'])
        with self.assertRaises(SystemExit):
            pakete.abhaengigkeiten(ordner, {'ihe.formatcode.fhir#1.5.x': '1.6.0'})
        with self.assertRaises(SystemExit):
            pakete.abhaengigkeiten(ordner)

    def test_paket_wird_vollstaendig_entpackt_oder_gar_nicht(self):
        import tarfile
        puffer = io.BytesIO()
        with tarfile.open(fileobj=puffer, mode='w:gz') as tar:
            inhalt = json.dumps({'name': 'a', 'version': '1.0.0'}).encode()
            info = tarfile.TarInfo('package/package.json')
            info.size = len(inhalt)
            tar.addfile(info, io.BytesIO(inhalt))
        (self.basis / 'a#1.0.0' / 'package').mkdir(parents=True)  # Rest eines abgebrochenen Laufs, ohne package.json
        (self.basis / 'a#1.0.0.neu').mkdir()
        alt, pakete._holen = pakete._holen, lambda url: puffer.getvalue()
        try:
            with redirect_stderr(io.StringIO()):
                pakete.paket_sicherstellen('a#1.0.0', {'pakete': {}, 'quellen': {}}, basis=self.basis)
        finally:
            pakete._holen = alt
        self.assertEqual(sorted(o.name for o in self.basis.iterdir()), ['a#1.0.0'])
        self.assertTrue((self.basis / 'a#1.0.0' / 'package' / 'package.json').exists())

    def test_cache_bereinigen_laesst_nur_den_bestand(self):
        self.neu('a#1.0.0')
        self.neu('b#1.0.0')
        (self.basis / 'b#1.0.0.lock').write_text('', encoding='utf-8')
        (self.basis / 'packages.ini').write_text('[cache]\nversion = 4\n', encoding='utf-8')
        (self.basis / '0c96f224-0f53-4f31-98ab-a151b6b8f84c').mkdir()
        with redirect_stderr(io.StringIO()):
            pakete.cache_bereinigen(self.basis, {'a#1.0.0'})
        self.assertEqual(sorted(o.name for o in self.basis.iterdir()),
                         ['0c96f224-0f53-4f31-98ab-a151b6b8f84c', 'a#1.0.0', 'packages.ini'])


class ProjektpaketeTest(unittest.TestCase):
    def test_darstellung_und_validierung_mit_gleichen_versionen(self):
        for pid in alle_projekte():
            k = projekt_laden(pid)
            if not k.get('validierung'):
                continue
            darstellung = dict(p.split('#', 1) for p in k['pakete'])
            for p in k['validierung']['pakete']:
                name, version = p.split('#', 1)
                if name in darstellung:
                    with self.subTest(projekt=pid, paket=name):
                        self.assertEqual(darstellung[name], version)

    def test_versionslos_geladene_pakete_stehen_nur_im_werkzeug_fest(self):
        neueste = {s.split('#', 1)[0] for s in validieren.NEUESTE}
        self.assertEqual(len(neueste), len(validieren.NEUESTE))
        for pid in alle_projekte():
            for p in (projekt_laden(pid).get('validierung') or {}).get('pakete', []):
                self.assertNotIn(p.split('#', 1)[0], neueste, f'{pid}: {p}')

    def test_startpakete(self):
        start = validieren.startpakete(['impfung'])
        self.assertEqual(start[:len(validieren.KERNPAKETE) + len(validieren.NEUESTE)],
                         validieren.KERNPAKETE + validieren.NEUESTE)
        k = projekt_laden('impfung')
        self.assertTrue(set(k['validierung']['pakete']) <= set(start))
        self.assertIn(k['lokale_ordner'][0], start)


if __name__ == '__main__':
    unittest.main()
