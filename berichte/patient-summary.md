# Prüfbericht — Patient Summary (EU EPS)

> Erzeugt von `python3 werkzeuge/mx.py bauen`. Nicht von Hand ändern; die CI prüft, dass der Bericht zum Stand passt.

> ![KI-gestützt erstellt](../web/ki-hinweis.svg) **Hinweis zur KI-Nutzung:** Dieser Modellexplorer – Programmcode, Projektkonfiguration und Texte – ist mit Unterstützung eines KI-Assistenten (Claude von Anthropic) entstanden. Die Darstellungen sind aus veröffentlichten Spezifikationen abgeleitet und keine Primärquelle; sie können Fehler enthalten. Maßgeblich sind die verlinkten Implementierungsleitfäden und FHIR-Pakete. Alle Beispieldaten sind fiktiv.

## Quellen

- Implementation Guide: HL7 Europe Patient Summary (`hl7.fhir.eu.eps#1.0.0-ballot`, Ballot)
- Darstellung des Modells: Struktur aus den Profilen — Für die EU Patient Summary ist kein Informationsmodell mit FHIR-Mappings veröffentlicht; die Xt-EHR-Logikmodelle 1.0.0 enthalten keine Mappings auf FHIR. Die Struktur folgt deshalb den Profilen: Pflicht- und Must-Support-Elemente bis zur dritten Ebene.
- Pakete: `hl7.fhir.eu.eps#1.0.0-ballot`, `hl7.fhir.eu.base#2.0.1`, `hl7.fhir.uv.ips#2.0.1`, `hl7.fhir.eu.extensions.r4#1.3.1`, `hl7.fhir.uv.xver-r5.r4#0.1.0`, `hl7.fhir.uv.extensions.r4#5.3.0`, `de.gematik.epa.medication#1.3.5`, `de.gematik.epa#1.3.2`, `de.gematik.ti#1.5.0-ballot.2`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.r4.core#4.0.1`

## Beispiele

| Beispiel | Ressourcen | fachliche Werte | durch die abgeleitete Struktur gedeckt | Strukturbefunde |
|---|---:|---:|---:|---:|
| Patient Summary — Hoffmann | 54 | 556 | 208 | 0 |
| Patient Summary — Yildiz | 22 | 240 | 105 | 0 |

### Patient Summary — Hoffmann

- Zweck: Gefüllte Patient Summary: acht Abschnitte, Allergien, Diagnosen, Medikation aus der ePA, Laborwerte, Impfungen, Prozeduren, Implantat; je Abschnitt ein Erzähltext.
- Herkunft: Demo-PVS (github.com/mno-93/demo-pvs, Commit d0e9615), erzeugt aus dem Datenbestand der Demo; HL7-Validator 7.0.1 gegen hl7.fhir.eu.eps#1.0.0-ballot. Fiktive Daten.
- Datei: `beispiele/hoffmann.json`
- Profilzuordnung ohne `meta.profile`: 2× Basisressource, 13× Standardprofil des Projekts

### Patient Summary — Yildiz

- Zweck: Dünn besetzte Patient Summary: leere Abschnitte mit Erzähltext — zeigt, wie Leerstellen im Dokument erscheinen.
- Herkunft: Demo-PVS (github.com/mno-93/demo-pvs, Commit d0e9615). Fiktive Daten.
- Datei: `beispiele/yildiz.json`
- Profilzuordnung ohne `meta.profile`: 1× Basisressource, 6× Standardprofil des Projekts

## Anzeige für Anwender:innen

Stand: `berichte/patient-summary.anzeige.json`, geschrieben von `python3 -I werkzeuge/mx.py anzeige patient-summary`. Gezählt werden inhaltliche Werte der Beispiele, die weder die Anwenderansicht noch eine Dokumentfassung zeigt; auf der Seite stehen sie unter „Weitere Angaben aus der Instanz“. Technisch und nicht gezählt: Kennungen und Metadaten, Systeme, Versionen, URLs, Erzähltext, UUID-Kennungen, Verweise mit Ziel im Beispiel.

| Beispiel | nicht angezeigte Werte | in Elementen |
|---|---:|---:|
| Patient Summary — Hoffmann | 5 | 1 |
| Patient Summary — Yildiz | 2 | 1 |

**Verknüpfungen** zwischen Instanz, Profil und Informationsmodell (in allen Richtungen, über Profilgrenzen, mit Rückwegen und jedem Klick in der Anwenderansicht): alle tragen.

### Nicht angezeigt — Patient Summary — Hoffmann

| Element | Anzahl | Werte (Auswahl) |
|---|---:|---|
| `MedicationRequest · identifier.value` | 5 | emp-h-med-1 · emp-h-med-3 · emp-h-med-4 |

### Nicht angezeigt — Patient Summary — Yildiz

| Element | Anzahl | Werte (Auswahl) |
|---|---:|---|
| `MedicationRequest · identifier.value` | 2 | emp-y-1 · emp-k-mvazzci2-52 |

## FHIR-Validierung (HL7 Validator 7.0.1)

Stand: `berichte/patient-summary.validierung.json`, geschrieben von `python3 -I werkzeuge/mx.py validieren patient-summary`; FHIR 4.0.1, Optionen `-tx n/a -locale en-US -allow-example-urls true -extension https://example.org/` (ohne Terminologieserver).

- Pakete: `hl7.fhir.uv.extensions.r4#5.3.0`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.eu.base#2.0.1`, `hl7.fhir.uv.ips#2.0.1`, `de.gematik.ti#1.5.0-ballot.2`, `de.gematik.epa#1.3.2`, `de.gematik.epa.medication#1.3.5`, `de.gematik.terminology#1.1.0-ballot.2`, `hl7.fhir.eu.eps#1.0.0-ballot`
- Lädt der Validator selbst (im Paketbestand festgelegt, ohne Netz): `hl7.fhir.r4.core#4.0.1`, `hl7.fhir.xver-extensions#0.1.0`, `hl7.terminology.r4#6.2.0`, `hl7.fhir.uv.extensions.r4#5.2.0`, `hl7.terminology#7.5.0`, `hl7.fhir.uv.extensions#5.3.0`
- Abhängigkeiten mit Platzhalter, festgelegt: `ihe.formatcode.fhir#1.5.x` → `1.5.0`
- Ergebnis: **0 Fehler**, 4 als begründete Ausnahme, 162 Warnungen, 278 Hinweise

| Beispiel | Fehler | davon begründete Ausnahme | Warnungen | Hinweise | Stand |
|---|---:|---:|---:|---:|---|
| Patient Summary — Hoffmann | 2 | 2 | 119 | 203 | aktuell |
| Patient Summary — Yildiz | 2 | 2 | 43 | 75 | aktuell |

**Begründete Ausnahmen** (`[[validierung.ausnahmen]]` in `projekt.toml`):

- `provenance-versionsverweis` — 4 Treffer: Die Beispiele tragen Änderungseinträge früherer Fassungen (Provenance mit Versionsverweis) für die Herkunftszeile; im Dokument nicht auflösbar. Abbildung im Demo-PVS offen.

### Fehler und Warnungen — Patient Summary — Hoffmann

Gleiche Meldungen zusammengefasst; Ort als FHIRPath, Zeile in der Beispieldatei.

- **error**: Can't find 'MedicationRequest/emp-h-med-4/_history/1' in the bundle (Bundle.entry[25].resource.target[0]). Note that there is a resource in the bundle with the same type and id, but it does not match because of the fullUrl based rules around matching relative references (must be 'https://example.org/demo-pvs/fhir/MedicationRequest/emp-h-med-4/_history/1', but found 'https://example.org/demo-pvs/fhir/MedicationRequest/emp-h-med-4') — begründete Ausnahme `provenance-versionsverweis`<br>`Bundle` (Zeile 1)
- **error**: Entry 'https://example.org/demo-pvs/fhir/Provenance/prov-mvazzcdz-8' isn't reachable by traversing links (forward or backward) from the Composition — begründete Ausnahme `provenance-versionsverweis`<br>`Bundle.entry[26]` (Zeile 1730)
- **warning** (11×): A definition for CodeSystem 'http://fhir.de/CodeSystem/bfarm/atc' version '2026' could not be found, so the code cannot be validated. No versions of this code system are known<br>`Bundle.entry[18].resource/*Medication/med-h-med-1*/.code.coding[0].system` (Zeile 1509), `Bundle.entry[19].resource/*Medication/med-h-med-3*/.code.coding[0].system` (Zeile 1535), `Bundle.entry[20].resource/*Medication/med-h-med-4*/.code.coding[0].system` (Zeile 1561) und 8 weitere
- **warning** (3×): A definition for CodeSystem 'http://fhir.de/CodeSystem/bfarm/ops' version '2026' could not be found, so the code cannot be validated. No versions of this code system are known<br>`Bundle.entry[49].resource/*Procedure/kh-proc-1-kh-e-2026-07-17*/.code.coding[0].system` (Zeile 3257), `Bundle.entry[50].resource/*Procedure/kh-proc-2-kh-e-2026-07-17*/.code.coding[0].system` (Zeile 3292), `Bundle.entry[51].resource/*Procedure/kh-proc-3-kh-e-2026-07-17*/.code.coding[0].system` (Zeile 3327)
- **warning** (6×): A definition for CodeSystem 'http://fhir.de/CodeSystem/ifa/pzn' could not be found, so the code cannot be validated<br>`Bundle.entry[34].resource/*Immunization/imm-mvazzchy-47*/.vaccineCode.coding[1].system` (Zeile 2373), `Bundle.entry[35].resource/*Immunization/imm-h-4*/.vaccineCode.coding[1].system` (Zeile 2437), `Bundle.entry[36].resource/*Immunization/imm-h-5*/.vaccineCode.coding[1].system` (Zeile 2508) und 3 weitere
- **warning** (5×): Constraint failed: DosageWarnungViererschemaInText: 'Hinweis: In Dosage.text wurde ein Viererschema (z. B. 1-1-1-1) erkannt. Bitte prüfen, ob dies strukturiert abgebildet werden kann.' (defined in http://ig.fhir.de/igs/medication/StructureDefinition/DosageDE)<br>`Bundle.entry[13].resource/*MedicationRequest/emp-h-med-1*/.dosageInstruction[0]` (Zeile 1210), `Bundle.entry[14].resource/*MedicationRequest/emp-h-med-3*/.dosageInstruction[0]` (Zeile 1280), `Bundle.entry[15].resource/*MedicationRequest/emp-h-med-4*/.dosageInstruction[0]` (Zeile 1350) und 2 weitere
- **warning** (48×): Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/DomainResource) (Best Practice Recommendation)<br>`Bundle.entry[0].resource/*Composition/ps-mvazzck5-66*/` (Zeile 18), `Bundle.entry[10].resource/*Provenance/prov-mvazzce0-13*/` (Zeile 1001), `Bundle.entry[11].resource/*Provenance/prov-mvazzce0-14*/` (Zeile 1050) und 45 weitere
- **warning**: Entry 15 matches the reference MedicationRequest/emp-h-med-4/_history/1 by type and id but its fullUrl https://example.org/demo-pvs/fhir/MedicationRequest/emp-h-med-4 does not match the full target URL https://example.org/demo-pvs/fhir/MedicationRequest/emp-h-med-4 by Bundle resolution rules<br>`Bundle.entry[25].resource/*Provenance/prov-mvazzcdz-8*/.target[0]`
- **warning** (2×): Profile reference 'https://example.org/demo-pvs/fhir/StructureDefinition/immunization-list-chronology-provenance' has not been checked because it could not be found; fetching it failed (response details omitted)<br>`Bundle.entry[45].resource/*Provenance/chron-mvazzce1-25*/.meta.profile[0]` (Zeile 3030), `Bundle.entry[47].resource/*Provenance/chron-mvazzchy-50*/.meta.profile[0]` (Zeile 3146)
- **warning** (3×): UCUM Codes that contain human readable annotations like {1.73_m2} can be misleading (e.g. they are ignored when comparing units). Best Practice is not to depend on annotations in the UCUM code, so this usage should be checked, and the Quantity.unit 'ml/min/1,73 m²' SHOULD contain the annotation (it does not)<br>`Bundle.entry[30].resource/*Observation/obs-f81d4fae-0-1-labor-2026-08-12*/.referenceRange[0].high` (Zeile 2103), `Bundle.entry[30].resource/*Observation/obs-f81d4fae-0-1-labor-2026-08-12*/.referenceRange[0].low` (Zeile 2097), `Bundle.entry[30].resource/*Observation/obs-f81d4fae-0-1-labor-2026-08-12*/.value.ofType(Quantity)` (Zeile 2078)
- **warning** (3×): Unable to validate code '%' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[32].resource/*Observation/obs-f81d4fae-2-0-labor-2026-08-12*/.referenceRange[0].high` (Zeile 2319), `Bundle.entry[32].resource/*Observation/obs-f81d4fae-2-0-labor-2026-08-12*/.referenceRange[0].low` (Zeile 2306), `Bundle.entry[32].resource/*Observation/obs-f81d4fae-2-0-labor-2026-08-12*/.value.ofType(Quantity)` (Zeile 2287)
- **warning** (3×): Unable to validate code 'mL/min/{1.73_m2}' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[30].resource/*Observation/obs-f81d4fae-0-1-labor-2026-08-12*/.referenceRange[0].high` (Zeile 2103), `Bundle.entry[30].resource/*Observation/obs-f81d4fae-0-1-labor-2026-08-12*/.referenceRange[0].low` (Zeile 2097), `Bundle.entry[30].resource/*Observation/obs-f81d4fae-0-1-labor-2026-08-12*/.value.ofType(Quantity)` (Zeile 2078)
- **warning** (3×): Unable to validate code 'mg/dL' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[29].resource/*Observation/obs-f81d4fae-0-0-labor-2026-08-12*/.referenceRange[0].high` (Zeile 2002), `Bundle.entry[29].resource/*Observation/obs-f81d4fae-0-0-labor-2026-08-12*/.referenceRange[0].low` (Zeile 1996), `Bundle.entry[29].resource/*Observation/obs-f81d4fae-0-0-labor-2026-08-12*/.value.ofType(Quantity)` (Zeile 1977)
- **warning** (3×): Unable to validate code 'mmol/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[31].resource/*Observation/obs-f81d4fae-1-0-labor-2026-08-12*/.referenceRange[0].high` (Zeile 2211), `Bundle.entry[31].resource/*Observation/obs-f81d4fae-1-0-labor-2026-08-12*/.referenceRange[0].low` (Zeile 2205), `Bundle.entry[31].resource/*Observation/obs-f81d4fae-1-0-labor-2026-08-12*/.value.ofType(Quantity)` (Zeile 2186)
- **warning** (2×): ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIAllergenNoDrug' not found<br>`Bundle.entry[3].resource.code` (Zeile 431), `Bundle.entry[4].resource.code` (Zeile 536)
- **warning** (15×): ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIIllnessandDisorder' not found<br>`Bundle.entry[13].resource.reasonCode[0]` (Zeile 1205), `Bundle.entry[14].resource.reasonCode[0]` (Zeile 1275), `Bundle.entry[15].resource.reasonCode[0]` (Zeile 1345) und 12 weitere
- **warning** (2×): ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIReactionAllergy' not found<br>`Bundle.entry[3].resource.reaction[0].manifestation[0]` (Zeile 465), `Bundle.entry[4].resource.reaction[0].manifestation[0]` (Zeile 565)
- **warning** (6×): ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIVaccine' not found<br>`Bundle.entry[34].resource/*Immunization/imm-mvazzchy-47*/.vaccineCode` (Zeile 2373), `Bundle.entry[35].resource/*Immunization/imm-h-4*/.vaccineCode` (Zeile 2437), `Bundle.entry[36].resource/*Immunization/imm-h-5*/.vaccineCode` (Zeile 2508) und 3 weitere
- **warning** (3×): ValueSet 'https://fhir.kbv.de/ValueSet/KBV_VS_SFHIR_ICD_DIAGNOSESICHERHEIT' not found<br>`Bundle.entry[7].resource/*Condition/cond-h-1*/.code.coding[0].extension[0].value.ofType(Coding)` (Zeile 752), `Bundle.entry[8].resource/*Condition/cond-h-2*/.code.coding[0].extension[0].value.ofType(Coding)` (Zeile 851), `Bundle.entry[9].resource/*Condition/cond-mvazzchy-43*/.code.coding[0].extension[0].value.ofType(Coding)` (Zeile 950)

### Fehler und Warnungen — Patient Summary — Yildiz

Gleiche Meldungen zusammengefasst; Ort als FHIRPath, Zeile in der Beispieldatei.

- **error**: Can't find 'MedicationRequest/emp-y-1/_history/1' in the bundle (Bundle.entry[13].resource.target[0]). Note that there is a resource in the bundle with the same type and id, but it does not match because of the fullUrl based rules around matching relative references (must be 'https://example.org/demo-pvs/fhir/MedicationRequest/emp-y-1/_history/1', but found 'https://example.org/demo-pvs/fhir/MedicationRequest/emp-y-1') — begründete Ausnahme `provenance-versionsverweis`<br>`Bundle` (Zeile 1)
- **error**: Entry 'https://example.org/demo-pvs/fhir/Provenance/prov-mvazzce1-30' isn't reachable by traversing links (forward or backward) from the Composition — begründete Ausnahme `provenance-versionsverweis`<br>`Bundle.entry[14]` (Zeile 980)
- **warning** (3×): A definition for CodeSystem 'http://fhir.de/CodeSystem/bfarm/atc' version '2026' could not be found, so the code cannot be validated. No versions of this code system are known<br>`Bundle.entry[11].resource/*Medication/med-y-1*/.code.coding[0].system` (Zeile 941), `Bundle.entry[12].resource/*Medication/med-k-mvazzci2-52*/.code.coding[0].system` (Zeile 967), `Bundle.entry[18].resource/*Immunization/imm-mvazzci3-62*/.vaccineCode.coding[0].system` (Zeile 1254)
- **warning**: A definition for CodeSystem 'http://fhir.de/CodeSystem/ifa/pzn' could not be found, so the code cannot be validated<br>`Bundle.entry[18].resource/*Immunization/imm-mvazzci3-62*/.vaccineCode.coding[1].system` (Zeile 1254)
- **warning** (2×): Constraint failed: DosageWarnungViererschemaInText: 'Hinweis: In Dosage.text wurde ein Viererschema (z. B. 1-1-1-1) erkannt. Bitte prüfen, ob dies strukturiert abgebildet werden kann.' (defined in http://ig.fhir.de/igs/medication/StructureDefinition/DosageDE)<br>`Bundle.entry[10].resource/*MedicationRequest/emp-k-mvazzci2-52*/.dosageInstruction[0]` (Zeile 922), `Bundle.entry[9].resource/*MedicationRequest/emp-y-1*/.dosageInstruction[0]` (Zeile 852)
- **warning** (22×): Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/DomainResource) (Best Practice Recommendation)<br>`Bundle.entry[0].resource/*Composition/ps-mvazzcl5-68*/` (Zeile 18), `Bundle.entry[10].resource/*MedicationRequest/emp-k-mvazzci2-52*/` (Zeile 860), `Bundle.entry[11].resource/*Medication/med-y-1*/` (Zeile 930) und 19 weitere
- **warning**: Entry 9 matches the reference MedicationRequest/emp-y-1/_history/1 by type and id but its fullUrl https://example.org/demo-pvs/fhir/MedicationRequest/emp-y-1 does not match the full target URL https://example.org/demo-pvs/fhir/MedicationRequest/emp-y-1 by Bundle resolution rules<br>`Bundle.entry[13].resource/*Provenance/prov-mvazzce1-30*/.target[0]`
- **warning**: Profile reference 'https://example.org/demo-pvs/fhir/StructureDefinition/immunization-list-chronology-provenance' has not been checked because it could not be found; fetching it failed (response details omitted)<br>`Bundle.entry[20].resource/*Provenance/chron-mvazzci3-65*/.meta.profile[0]` (Zeile 1357)
- **warning** (3×): Unable to validate code 'm[IU]/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[16].resource/*Observation/obs-3b1c9a52-0-0-labor-2026-07-02*/.referenceRange[0].high` (Zeile 1200), `Bundle.entry[16].resource/*Observation/obs-3b1c9a52-0-0-labor-2026-07-02*/.referenceRange[0].low` (Zeile 1194), `Bundle.entry[16].resource/*Observation/obs-3b1c9a52-0-0-labor-2026-07-02*/.value.ofType(Quantity)` (Zeile 1175)
- **warning** (6×): ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIIllnessandDisorder' not found<br>`Bundle.entry[10].resource.reasonCode[0]` (Zeile 917), `Bundle.entry[18].resource/*Immunization/imm-mvazzci3-62*/.protocolApplied[0].targetDisease[0]` (Zeile 1289), `Bundle.entry[3].resource.code` (Zeile 398) und 3 weitere
- **warning**: ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIVaccine' not found<br>`Bundle.entry[18].resource/*Immunization/imm-mvazzci3-62*/.vaccineCode` (Zeile 1254)
- **warning** (3×): ValueSet 'https://fhir.kbv.de/ValueSet/KBV_VS_SFHIR_ICD_DIAGNOSESICHERHEIT' not found<br>`Bundle.entry[3].resource/*Condition/cond-y-1*/.code.coding[0].extension[0].value.ofType(Coding)` (Zeile 408), `Bundle.entry[4].resource/*Condition/cond-y-2*/.code.coding[0].extension[0].value.ofType(Coding)` (Zeile 500), `Bundle.entry[5].resource/*Condition/cond-mvazzci3-58*/.code.coding[0].extension[0].value.ofType(Coding)` (Zeile 592)
