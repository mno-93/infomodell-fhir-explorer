"""MIO-Informationsmodell (mio-baum): Adapter, EHDS-Mappingprüfung gegen die Xt-EHR-Logikmodelle, Mappingtabelle eines
Projekts (Teilbaum Impfung → Entwurfsprofile) und ein Projekt ohne Beispiele."""
import unittest

import hilfe  # noqa: F401
from mx import bauen, berichte, ehds
from mx.konfig import projekt_laden
from mx.pakete import definitionen

XT = 'https://www.xt-ehr.eu/fhir/models/'


def verweis(html):
    return ehds.verweise(f'<div><p>{html}</p></div>')


class EhdsVerweiseTest(unittest.TestCase):
    """Lesen der Verweise — die Formate, wie sie im Modell vorkommen."""

    def test_versionierter_link(self):
        v, = verweis(f'<a href="{XT}1.0.0/en/StructureDefinition-EHDSAllergyIntolerance-definitions.html'
                     '#EHDSAllergyIntolerance.header.status"> EHDSAllergyIntolerance.header.status </a>')
        self.assertEqual((v['modell'], v['element'], v['format']),
                         ('EHDSAllergyIntolerance', 'EHDSAllergyIntolerance.header.status', 'versioniert'))

    def test_link_ohne_version(self):
        v, = verweis(f'<a href="{XT}en/StructureDefinition-EHDSImmunisation-definitions.html#EHDSImmunisation.vaccine">x</a>')
        self.assertEqual((v['element'], v['format']), ('EHDSImmunisation.vaccine', 'ohne-version'))

    def test_anker_auf_das_modell_ist_nur_modell(self):
        v, = verweis(f'<a href="{XT}en/StructureDefinition-EHDSCondition-definitions.html#EHDSCondition">EHDSCondition</a>')
        self.assertEqual((v['modell'], v['element']), ('EHDSCondition', None))

    def test_kanonische_url(self):
        v, = verweis('<a href="http://www.xt-ehr.eu/fhir/models/StructureDefinition/EHDSImmunisation">EHDSImmunisation</a>')
        self.assertEqual((v['modell'], v['element'], v['format']), ('EHDSImmunisation', None, 'kanonisch'))

    def test_linkziel_nur_pfad_und_klartext(self):
        a, = verweis('<a href="EHDSDeviceUse.device[x]">EHDSDeviceUse.deviceEHDSDevice</a>')
        self.assertEqual((a['element'], a['format']), ('EHDSDeviceUse.device[x]', 'ohne-url'))
        b, = verweis('EHDSAlert.code')
        self.assertEqual((b['element'], b['format']), ('EHDSAlert.code', 'klartext'))
        c, = verweis('<a rel="noopener">EHDSCarePlan</a>')
        self.assertEqual((c['modell'], c['format']), ('EHDSCarePlan', 'klartext'))

    def test_fremder_link_und_unsichtbares_zeichen(self):
        v, = verweis('<a href="https://build.fhir.org/ig/hl7-eu/eps/x.html#AllergyIntolerance.note.time">'
                     'EHDSAllergyIntolerance.note.time</a>')
        self.assertEqual((v['element'], v['format']), ('EHDSAllergyIntolerance.note.time', 'fremder-link'))
        w, = verweis('EHDSAllergyIntolerance.' + chr(0x200b) + 'certainty')
        self.assertEqual(w['element'], 'EHDSAllergyIntolerance.certainty')
        self.assertTrue(w['unsichtbar'])

    def test_mehrere_verweise_und_ohne_entsprechung(self):
        vs = verweis(f'<a href="{XT}en/StructureDefinition-EHDSCondition-definitions.html#EHDSCondition.onsetDate">a</a> und '
                     f'<a href="{XT}en/StructureDefinition-EHDSCondition-definitions.html#EHDSCondition.endDate">b</a>')
        self.assertEqual([v['element'] for v in vs], ['EHDSCondition.onsetDate', 'EHDSCondition.endDate'])
        o, = verweis('Element ist im EHDS Logical Model nicht vorhanden.')
        self.assertEqual(o['status'], 'ohne-entsprechung')


class EhdsPruefungTest(unittest.TestCase):
    """Auflösung gegen `xtehr.eu.ehds.models#1.0.0` und Ergebnis für das ganze Modell der ePA Patient Summary."""

    @classmethod
    def setUpClass(cls):
        cls.logik = ehds.Logikmodelle(definitionen(['xtehr.eu.ehds.models#1.0.0']), 'xtehr.eu.ehds.models#1.0.0')
        cls.d = bauen.projekt_bauen('epa-patient-summary')

    def aufloesen(self, html):
        return self.logik.aufloesen(verweis(html)[0])

    def test_aufloesung(self):
        a = self.aufloesen('EHDSImmunisation.vaccine')
        self.assertEqual(a['status'], 'aufloesbar')
        self.assertEqual(a['seite'], XT + '1.0.0/en/StructureDefinition-EHDSImmunisation-definitions.html#EHDSImmunisation.vaccine')
        self.assertEqual(self.aufloesen('EHDSImmunisation.administeredProduct')['typen'], ['EHDSMedication'])
        self.assertEqual(self.aufloesen('EHDSAllergyIntolerance.note.time')['status'], 'element-fehlt')
        self.assertEqual(self.aufloesen('EHDSCarePlan')['status'], 'nur-modell')
        self.assertEqual(self.aufloesen('EHDSGibtEsNicht.x')['status'], 'modell-fehlt')
        self.assertEqual(self.aufloesen('EHDSPatientSummary.header.author')['status'], 'aufloesbar')  # author[x]

    def test_statistik_des_modells(self):
        e = self.d['statistik']['ehds']
        self.assertEqual(self.d['statistik']['im_knoten'], 481)
        self.assertEqual(e['verweise'], sum(e['status'].values()))
        self.assertEqual(e['verweise'] - e['status']['ohne-entsprechung'], sum(e['format'].values()))
        self.assertGreater(e['status']['aufloesbar'], 80)
        self.assertGreater(e['format']['ohne-version'], 0)

    def test_allergie_mit_condition_ist_anderer_baustein(self):
        befunde = [b for b in self.d['ehds_pruefung'] if b['kontext']]
        self.assertTrue(befunde)
        for b in befunde:
            self.assertIn('Allergie/Unverträglichkeit', b['pfad'])
            self.assertTrue(b['roh'].startswith('EHDSCondition.'), b['roh'])
        # dieselben Elemente unter „Diagnose“ passen zum Kontext
        diagnose = [b for b in self.d['ehds_pruefung'] if '/ Diagnose /' in b['pfad']]
        self.assertFalse(any(b['kontext'] for b in diagnose))

    def test_adapter(self):
        by = {n['id']: n for n in self.d['im']}
        impfung = next(n for n in self.d['im'] if n['name'] == 'Impfung' and n['ehds'])
        self.assertEqual(impfung['card'], 'Daten eintragen oder übernehmen : 0..* (Optional)')
        self.assertEqual([v['modell'] for v in impfung['ehds']], ['EHDSImmunisation'])
        self.assertIn('EHDSImmunisation Mapping', [h['quelle'] for h in impfung['herkunft']])
        status = next(n for n in self.d['im'] if n['name'] == 'Status' and n['p'] == impfung['id'])
        self.assertEqual({z['code'] for z in status['terminologie']}, {'completed', 'not-done'})
        bedingt = [n for n in self.d['im'] if '0..0' in n['card']]
        self.assertTrue(bedingt and all(' · ' in n['card'] for n in bedingt))
        self.assertTrue(any(a['kw'] == 'MUSS' for n in self.d['im'] for a in n['anf']))
        self.assertTrue(all(n['p'] is None or n['p'] in by for n in self.d['im']))

    def test_ausmodelliert_mit_referenzen_in_untergruppen(self):
        b = self.d['baum_aus']
        self.assertTrue(b)
        name = {n['id']: n['name'] for n in self.d['im']}
        # „Schwangerschaftsstatus“ liegt in einer Untergruppe von „ePA ePS Profile (in Erarbeitung)“
        self.assertTrue(any(x.get('v') and name[x['s']] == 'Schwangerschaftsstatus' for x in b))

    def test_projekt_ohne_beispiele(self):
        self.assertEqual(self.d['beispiele'], [])
        text = berichte.bericht(self.d)
        self.assertIn('## EHDS-Mappingprüfung', text)
        self.assertIn('Keine Beispiele — nichts zu validieren.', text)
        self.assertIn('keine Beispiele', bauen.validierung_kurz(self.d))


class MappingtabelleTest(unittest.TestCase):
    """Projekt impfung: Teilbaum „Impfung“ des Modells, FHIR-Mappings aus der Projektkonfiguration."""

    @classmethod
    def setUpClass(cls):
        cls.k = projekt_laden('impfung')
        cls.d = bauen.projekt_bauen('impfung')
        cls.nach_name = {}
        for n in cls.d['im']:
            cls.nach_name.setdefault(n['name'], []).append(n)

    def test_teilbaum(self):
        wurzeln = [n for n in self.d['im'] if n['p'] is None]
        self.assertEqual([n['name'] for n in wurzeln], ['Impfung'])
        self.assertEqual(self.d['meta']['im_art'], 'mio-baum')

    def test_alle_mappings_aufgeloest(self):
        s = self.d['statistik']
        self.assertEqual(s['mappings'], len([e for e in self.k['informationsmodell']['mappings'] if e.get('fhir')]))
        self.assertEqual(s['mapping_status']['fehler'] + s['mapping_status']['verboten'] + s['mapping_status']['unbekannt'], 0)
        self.assertEqual(s['ohne_ziel'], 0)   # jedes Blatt des Teilbaums hat ein Ziel im Entwurf

    def test_teilelemente_zugeordnet(self):
        """Codes außerhalb von SNOMED CT, Datentyp und Referenz des Produkts, Autor:in der Notiz als Text oder Verweis."""
        ziele = lambda name, eltern: [m['k'] for n in self.nach_name[name] for m in n['maps']
                                      if self.d['im'][[x['id'] for x in self.d['im']].index(n['p'])]['name'] == eltern]
        self.assertEqual(sorted(ziele('Code aus einem Code-System', 'Code-Auswahl')),
                         ['Immunization.protocolApplied.targetDisease.coding', 'Immunization.vaccineCode.coding'])
        self.assertEqual(ziele('Datentyp', 'Verabreichtes Produkt'),
                         ['Immunization.extension:administeredProduct.extension:_datatype.value[x]'])
        self.assertEqual(ziele('Referenz', 'Verabreichtes Produkt'),
                         ['Immunization.extension:administeredProduct.extension:reference.value[x]'])
        self.assertEqual(ziele('Freitext', 'Autor:in'), ['Immunization.note.authorString'])
        self.assertEqual(ziele('Referenz', 'Autor:in'), ['Immunization.note.authorReference'])

    def test_kette_modell_profil_instanz(self):
        snomed = next(n for n in self.nach_name['SNOMED-CT-Code'] if any('vaccineCode' in m['k'] for m in n['maps']))
        m, = snomed['maps']
        self.assertTrue(m['sd'].endswith('/ps-immunization'))
        self.assertEqual(m['k'], 'Immunization.vaccineCode.coding:snomed')
        b = next(b for b in self.d['beispiele'] if b['id'] == 'erstdokumentation')
        el = b['elemente']['Immunization/imm-erst-influenza|vaccineCode.coding[0].code']
        self.assertEqual(el, m['sd'] + '#Immunization.vaccineCode.coding:snomed.code')
        produkt = self.nach_name['Arzneimittel (ePA Medication Service) (Referenz)'][0]
        self.assertTrue(produkt['maps'][0]['sd'].endswith('/ps-immunization-medication'))

    def test_entwurf_ohne_modellknoten_aus_profil(self):
        aus_profil = {x['y'][1] for x in self.d['baum_aus'] if 'y' in x}
        for eid in ('Immunization.identifier', 'Immunization.primarySource', 'Immunization.reportOrigin',
                    'Immunization.recorded', 'Immunization.protocolApplied.doseNumber[x]', 'Medication.batch.lotNumber',
                    'Medication.code.coding:pzn', 'Medication.manufacturer'):
            self.assertIn(eid, aus_profil)
        for eid in ('Immunization.status', 'Immunization.vaccineCode', 'Immunization.vaccineCode.coding:snomed'):
            self.assertNotIn(eid, aus_profil)  # im Modell gemappt

    def test_abdeckung_der_impfungen(self):
        b = next(b for b in self.d['beispiele'] if b['id'] == 'erstdokumentation')
        ohne = b['abdeckung']['ohne_modell']
        self.assertTrue(any(el.endswith('#Immunization.primarySource') for el in ohne))
        self.assertFalse(any(el.endswith('#Immunization.vaccineCode.text') for el in ohne))

    def test_ehds_im_teilbaum(self):
        e = self.d['statistik']['ehds']
        self.assertEqual(e['status']['element-fehlt'] + e['status']['modell-fehlt'], 0)
        self.assertEqual(e['anderes_modell'], 0)


if __name__ == '__main__':
    unittest.main()
