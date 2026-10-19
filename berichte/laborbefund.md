# Prüfbericht — Laborbefund (dgLP)

> Erzeugt von `python3 werkzeuge/mx.py bauen`. Nicht von Hand ändern; die CI prüft, dass der Bericht zum Stand passt.

## Quellen

- Implementation Guide: ePA Laboratory Report Implementation Guide (`de.gematik.epa.laboratory#1.0.0-ballot.1`, öffentlicher Ballot, 15.09.2026)
- Darstellung des Modells: Informationsmodell
- Pakete: `de.gematik.epa.laboratory#1.0.0-ballot.1`, `de.gematik.ti#1.5.0-ballot.1`, `hl7.fhir.eu.laboratory#2.0.0`, `hl7.fhir.eu.base#2.0.0`, `hl7.fhir.eu.extensions.r4#1.3.0`, `hl7.fhir.uv.xver-r5.r4#0.1.0`, `hl7.fhir.uv.extensions.r4#5.3.0`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.r4.core#4.0.1`

## Mappingprüfung

| Befund | Anzahl |
|---|---:|
| Elemente im Informationsmodell | 463 |
| davon mit FHIR-Mapping | 393 |
| FHIR-Mappings | 450 |
| exakt | 396 |
| gleichwertige Schreibweise (JSON-Name der Typwahl, Typ-Slice) — keine Korrektur nötig | 21 |
| Schreibvariante (gemischte Notation) — vereinheitlichen | 23 |
| über Extension-Definition oder Datentyp aufgelöst | 0 |
| **ohne Ziel** | **8** |
| **auf ein 0..0-Element** | **2** |
| Definition nicht im Paketbestand | 0 |
| in ein anderes Profil als das übergeordnete Element | 3 |

### Fehlerhafte Mappings (10)

| Element im Modell | Mapping | Befund |
|---|---|---|
| Referenz Laborauftrag-Information <br>*Referenzierte Profile / Laborgesamtbefund* | `ServiceRequestdgLP.basedOn` | `ServiceRequest.basedOn` ist im Profil `service-request-dglp` auf 0..0 gesetzt |
| LOINC®-Code <br>*Labormedizinischer Bereich Code/Bezeichnung / Code-Auswahl* | `ObservationLaboratoryStudyGroupdgLP.category:studyType.coding:loinc` | Slice `coding:loinc` unter `Observation.category:studyType` nicht definiert |
| LOINC®-Code <br>*Labormedizinischer Bereich Code/Bezeichnung / Code-Auswahl* | `ObservationLaboratoryStudydgLP.category:studyType.coding:loinc` | Slice `coding:loinc` unter `Observation.category:studyType` nicht definiert |
| Einheit <br>*Ergebnisbereich mit Alternativeinheit / Obergrenze* | `ObservationLaboratoryStudydgLP.extension:alternativeResult.extension:value.value[x]:valueRange.high.ssystem` | `ssystem` gibt es unter `Quantity` nicht |
| Bezeichnung <br>*Identifikator Probe / ID-Typ Code/Bezeichnung* | `SpecimendgLP.identifier.type.text` | `Specimen.identifier.type.text` ist im Profil `specimen-dglp` auf 0..0 gesetzt |
| Referenz auf Probenbehälter <br>*Probe / Angaben zum Probenbehälter* | `SpecimendgLP.container.extension:SpecimenContainerDeviceR5.value[x]` | Slice `extension:SpecimenContainerDeviceR5` unter `Specimen.container` nicht definiert (vorhanden: device) |
| Code-Auswahl <br>*Untersuchungsbild-Anhang / Typ Untersuchungsbild - Code/Bezeichnung* | `ObservationImageAttachmentdgLP.coding` | `coding` gibt es unter `Observation` nicht |
| Dateiname <br>*Referenzierte Profile / Untersuchungsbild-Anhang* | `ObservationImageAttachmentdgLP.extension:value.value[x]:valueAttachment.title` | Slice `extension:value` unter `Observation` nicht definiert (vorhanden: accredited, bodyStructure, certifiedRefMaterialCodeable, certifiedRefMaterialIdentifer, labTestKit, supportingInfo, triggeredBy, value-r5) |
| Dateiformat <br>*Referenzierte Profile / Untersuchungsbild-Anhang* | `ObservationImageAttachmentdgLP.extension:value.value[x]:valueAttachment.contentType` | Slice `extension:value` unter `Observation` nicht definiert (vorhanden: accredited, bodyStructure, certifiedRefMaterialCodeable, certifiedRefMaterialIdentifer, labTestKit, supportingInfo, triggeredBy, value-r5) |
| Datei <br>*Referenzierte Profile / Untersuchungsbild-Anhang* | `ObservationImageAttachmentdgLP.extension:value.value[x]:valueAttachment.data` | Slice `extension:value` unter `Observation` nicht definiert (vorhanden: accredited, bodyStructure, certifiedRefMaterialCodeable, certifiedRefMaterialIdentifer, labTestKit, supportingInfo, triggeredBy, value-r5) |

### Mappings in ein anderes Profil (3)

| Element im Modell | Mapping | Befund |
|---|---|---|
| Code Laboranalysegerät <br>*Laboranalysegerät / Kategorie* | `DeviceDefinitionLaboratoryAnalyzerdgLP.type.coding` | liegt unter „Laboranalysegerät“ (device-laboratory-analyzer-dglp), zeigt aber in `device-definition-laboratory-analyzer-dglp` |
| Hersteller <br>*Referenzierte Profile / Laboranalysegerät* | `DeviceDefinitionLaboratoryAnalyzerdgLP.manufacturer[x]:manufacturerString` | liegt unter „Laboranalysegerät“ (device-laboratory-analyzer-dglp), zeigt aber in `device-definition-laboratory-analyzer-dglp` |
| Referenz Laborauftrag-Information <br>*Referenzierte Profile / Laborgesamtbefund* | `ServiceRequestdgLP.basedOn` | liegt unter „Laborgesamtbefund“ (diagnostic-report-dglp), zeigt aber in `service-request-dglp` |

### Schreibvarianten (gemischte Notation) (23)

| Element im Modell | Mapping | Befund |
|---|---|---|
| Klinischer Bezugszeitpunkt <br>*Referenzierte Profile / Laboruntersuchung* | `ObservationLaboratoryStudydgLP.effective[x].effectiveDateTime` | `effective[x].effectiveDateTime` statt `effective[x]:effectiveDateTime` |
| Ergebniswert Quantität <br>*Messergebnis / Messergebnis quantitativ* | `ObservationLaboratoryStudydgLP.value[x].valueQuantity` | `value[x].valueQuantity` statt `value[x]:valueQuantity` |
| Wert <br>*Messergebnis quantitativ / Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueQuantity.value` | `value[x].valueQuantity` statt `value[x]:valueQuantity` |
| Komparator <br>*Messergebnis quantitativ / Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueQuantity.comparator` | `value[x].valueQuantity` statt `value[x]:valueQuantity` |
| Einheit <br>*Messergebnis quantitativ / Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueQuantity.system` | `value[x].valueQuantity` statt `value[x]:valueQuantity` |
| Einheit <br>*Messergebnis quantitativ / Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueQuantity.code` | `value[x].valueQuantity` statt `value[x]:valueQuantity` |
| Einheit <br>*Messergebnis quantitativ / Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueQuantity.unit` | `value[x].valueQuantity` statt `value[x]:valueQuantity` |
| Wert <br>*Ergebniswert Ratio / Zähler Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueRatio.numerator.value` | `value[x].valueRatio` statt `value[x]:valueRatio` |
| Einheit <br>*Ergebniswert Ratio / Zähler Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueRatio.numerator.system` | `value[x].valueRatio` statt `value[x]:valueRatio` |
| Einheit <br>*Ergebniswert Ratio / Zähler Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueRatio.numerator.code` | `value[x].valueRatio` statt `value[x]:valueRatio` |
| Einheit <br>*Ergebniswert Ratio / Zähler Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueRatio.numerator.unit` | `value[x].valueRatio` statt `value[x]:valueRatio` |
| Wert <br>*Ergebniswert Ratio / Nenner Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueRatio.denominator.value` | `value[x].valueRatio` statt `value[x]:valueRatio` |
| Einheit <br>*Ergebniswert Ratio / Nenner Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueRatio.denominator.system` | `value[x].valueRatio` statt `value[x]:valueRatio` |
| Einheit <br>*Ergebniswert Ratio / Nenner Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueRatio.denominator.code` | `value[x].valueRatio` statt `value[x]:valueRatio` |
| Einheit <br>*Ergebniswert Ratio / Nenner Ergebniswert Quantität* | `ObservationLaboratoryStudydgLP.value[x].valueRatio.denominator.unit` | `value[x].valueRatio` statt `value[x]:valueRatio` |
| Wert <br>*Ergebnisbereich / Obergrenze* | `ObservationLaboratoryStudydgLP.value[x].valueRange.high.value` | `value[x].valueRange` statt `value[x]:valueRange` |
| Einheit <br>*Ergebnisbereich / Obergrenze* | `ObservationLaboratoryStudydgLP.value[x].valueRange.high.system` | `value[x].valueRange` statt `value[x]:valueRange` |
| Einheit <br>*Ergebnisbereich / Obergrenze* | `ObservationLaboratoryStudydgLP.value[x].valueRange.high.code` | `value[x].valueRange` statt `value[x]:valueRange` |
| Einheit <br>*Ergebnisbereich / Obergrenze* | `ObservationLaboratoryStudydgLP.value[x].valueRange.high.unit` | `value[x].valueRange` statt `value[x]:valueRange` |
| Wert <br>*Ergebnisbereich / Untergrenze* | `ObservationLaboratoryStudydgLP.value[x].valueRange.low.value` | `value[x].valueRange` statt `value[x]:valueRange` |
| Einheit <br>*Ergebnisbereich / Untergrenze* | `ObservationLaboratoryStudydgLP.value[x].valueRange.low.system` | `value[x].valueRange` statt `value[x]:valueRange` |
| Einheit <br>*Ergebnisbereich / Untergrenze* | `ObservationLaboratoryStudydgLP.value[x].valueRange.low.code` | `value[x].valueRange` statt `value[x]:valueRange` |
| Einheit <br>*Ergebnisbereich / Untergrenze* | `ObservationLaboratoryStudydgLP.value[x].valueRange.low.unit` | `value[x].valueRange` statt `value[x]:valueRange` |

### Gleichwertige Schreibweisen (keine Korrektur nötig) (21)

| Element im Modell | Mapping | Befund |
|---|---|---|
| Hersteller <br>*Referenzierte Profile / Außerkörperliche Quelle* | `DeviceDefinitionSpecimenSubjectdgLP.manufacturer[x]:manufacturerString` | Typ-Slice `manufacturer[x]:manufacturerString` im Profil nicht eigens ausgewiesen (Element `manufacturer[x]`) — Typangabe bleibt gültig |
| SNOMED CT®-Code <br>*Körperstruktur / Körperstelle Code/Bezeichnung* | `BodyStructuredgLP.extension:includedStructure.extension:structure.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Bezeichnung <br>*Körperstruktur / Körperstelle Code/Bezeichnung* | `BodyStructuredgLP.extension:includedStructure.extension:structure.valueCodeableConcept.text` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| SNOMED  CT®-Code <br>*Körperstruktur / Lateralität Code/Bezeichnung* | `BodyStructuredgLP.extension:includedStructure.extension:laterality.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Bezeichnung <br>*Körperstruktur / Lateralität Code/Bezeichnung* | `BodyStructuredgLP.extension:includedStructure.extension:laterality.valueCodeableConcept.text` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| SNOMED CT®-Code <br>*Körperstruktur / Lokalisation Code/Bezeichnung* | `BodyStructuredgLP.extension:includedStructure.extension:qualifier.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Bezeichnung <br>*Körperstruktur / Lokalisation Code/Bezeichnung* | `BodyStructuredgLP.extension:includedStructure.extension:qualifier.valueCodeableConcept.text` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Uhrzeigerposition Code/Bezeichnung <br>*Referenzierte Profile / Körperstruktur* | `BodyStructuredgLP.extension:includedStructure.extension:bodyLandmarkOrientation.extension:clockFacePosition.valueCodeableConcept` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| SNOMED CT®-Code <br>*Körperstruktur / Uhrzeigerposition Code/Bezeichnung* | `BodyStructuredgLP.extension:includedStructure.extension:bodyLandmarkOrientation.extension:clockFacePosition.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Bezeichnung <br>*Körperstruktur / Uhrzeigerposition Code/Bezeichnung* | `BodyStructuredgLP.extension:includedStructure.extension:bodyLandmarkOrientation.extension:clockFacePosition.valueCodeableConcept.text` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Hersteller <br>*Referenzierte Profile / Laboranalysegerät* | `DeviceDefinitionLaboratoryAnalyzerdgLP.manufacturer[x]:manufacturerString` | Typ-Slice `manufacturer[x]:manufacturerString` im Profil nicht eigens ausgewiesen (Element `manufacturer[x]`) — Typangabe bleibt gültig |
| Code-Auswahl <br>*Fachliches Gruppierungsmerkmal Auswahl / Test-Profil Code/Bezeichnung* | `ObservationLaboratoryStudyGroupdgLP.extension:testProfile.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Code Test-Profil <br>*Test-Profil Code/Bezeichnung / Code-Auswahl* | `ObservationLaboratoryStudyGroupdgLP.extension:testProfile.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Code aus anderem Codesystem <br>*Test-Profil Code/Bezeichnung / Code-Auswahl* | `ObservationLaboratoryStudyGroupdgLP.extension:testProfile.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Bezeichnung <br>*Fachliches Gruppierungsmerkmal Auswahl / Test-Profil Code/Bezeichnung* | `ObservationLaboratoryStudyGroupdgLP.extension:testProfile.valueCodeableConcept.text` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Code-Auswahl <br>*Fachliches Gruppierungsmerkmal Auswahl / Test-Profil Code/Bezeichnung* | `ObservationLaboratoryStudydgLP.extension:testProfile.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Code Test-Profil <br>*Test-Profil Code/Bezeichnung / Code-Auswahl* | `ObservationLaboratoryStudydgLP.extension:testProfile.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Code aus anderem Codesystem <br>*Test-Profil Code/Bezeichnung / Code-Auswahl* | `ObservationLaboratoryStudydgLP.extension:testProfile.valueCodeableConcept.coding` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Bezeichnung <br>*Fachliches Gruppierungsmerkmal Auswahl / Test-Profil Code/Bezeichnung* | `ObservationLaboratoryStudydgLP.extension:testProfile.valueCodeableConcept.text` | JSON-Name `valueCodeableConcept` für die Typwahl `value[x]` — gleichwertig |
| Medizinischer Freigabezeitpunkt <br>*Referenzierte Profile / Medizinische Freigabe* | `ProvenancedgLP.occurred[x]:occurredDateTime` | Typ-Slice `occurred[x]:occurredDateTime` im Profil nicht eigens ausgewiesen (Element `occurred[x]`) — Typangabe bleibt gültig |
| Hersteller <br>*Referenzierte Profile / Probenbehälter* | `DeviceDefinitionSpecimenContainerdgLP.manufacturer[x]:manufacturerString` | Typ-Slice `manufacturer[x]:manufacturerString` im Profil nicht eigens ausgewiesen (Element `manufacturer[x]`) — Typangabe bleibt gültig |

## Wertelisten

45 Wertelisten im Modell, davon 39 im Paketbestand oder über eine Profilbindung aufgelöst, 39 mit Link auf die Originalseite.

Nicht auflösbar (weder im Paketbestand noch in einer Profilbindung):

- `KBV_VS_MIO_LAB_Comparator_RefRangeHigh`
- `KBV_VS_MIO_LAB_Comparator_RefRangeLow`
- `KBV_VS_MIO_LAB_Composition_Attester_Mode`
- `KBV_VS_MIO_LAB_Provenance_Activity_Type`
- `MehrfachkodierungsKennzeichen`
- `ObservationStatusdgLPVS`

### Werteliste im Modell gegen Bindung im Profil

Je Mapping eines Elements mit Werteliste: Bindung am Element, am zugehörigen CodeableConcept, am Wert einer gemappten Extension oder an einem Slice darunter.

| Ergebnis | Anzahl |
|---|---:|
| gleich | 45 |
| gleich, aber am Slice | 1 |
| ohne Bindung | 4 |
| ungeklärt | 4 |

**Gleich, aber am Slice — Mapping präzisieren (1)**

| Element im Modell | Mapping | Werteliste im Modell | Vorschlag |
|---|---|---|---|
| SNOMED CT®-Code | `ObservationImageAttachmentdgLP.code.coding` | `DiagramTypeVS` | `ObservationImageAttachmentdgLP.code.coding:snomed` |

**Ungeklärt — Werteliste des Modells nicht im Paketbestand (4)**

| Element im Modell | Mapping | Werteliste im Modell | Bindung im Profil |
|---|---|---|---|
| Freigabetyp | `CompositiondgLP.attester:legalAuthenticator.mode` | `KBV_VS_MIO_LAB_Composition_Attester_Mode` | `http://hl7.org/fhir/ValueSet/composition-attestation-mode` (required, am Element) |
| Codierungskennzeichen | `ConditionDiagnosisdgLP.code.coding:ICD-10-GM.extension:Mehrfachcodierungs-Kennzeichen` | `MehrfachkodierungsKennzeichen` | `http://fhir.de/ValueSet/icd-10-gm-mehrfachcodierungs-kennzeichen` (required, am Wert der Extension) |
| Status Laboruntersuchung | `ObservationLaboratoryStudydgLP.status` | `ObservationStatusdgLPVS` | `https://gematik.de/fhir/terminology/ValueSet/observation-status` (required, am Element) |
| Freigabetyp | `ProvenancedgLP.activity` | `KBV_VS_MIO_LAB_Provenance_Activity_Type` | `http://hl7.org/fhir/ValueSet/provenance-activity-type` (extensible, am Element) |

## Ausmodellierte Darstellung

3079 Knoten · 103 Referenzen an der Verwendungsstelle aufgelöst · 20 Zyklen erkannt · 1552 Knoten aus FHIR-Profilen ergänzt

## Beispiele

| Beispiel | Ressourcen | fachliche Werte | durch das Modell gedeckt | Strukturbefunde |
|---|---:|---:|---:|---:|
| Nierenfunktion und HbA1c — Hoffmann, 12.08.2026 | 16 | 181 | 142 | 0 |
| Vorbefund — Hoffmann, 18.03.2026 | 14 | 148 | 113 | 0 |
| Schilddrüse (TSH) — Yildiz, 02.07.2026 | 11 | 90 | 60 | 0 |
| IG-Beispiel mit Probe, Gerät und Anhang | 22 | 376 | 278 | 0 |
| IG-Beispiel, zweite Composition | 21 | 325 | 232 | 0 |

### Nierenfunktion und HbA1c — Hoffmann, 12.08.2026

- Zweck: Klinisch plausibler Befund: drei Laborbereiche, vier Werte mit Bewertung, ein- und beidseitige Referenzbereiche, eingebettetes PDF.
- Herkunft: Demo-PVS (github.com/mno-93/demo-pvs, Commit d0e9615), erzeugt mit laborbefundBauen; HL7-Validator 7.0.1 ohne Fehler bis auf die im Projekt genannten Ausnahmen. Fiktive Daten.
- Datei: `beispiele/hoffmann-2026-08-12.json`
- Profilzuordnung ohne `meta.profile`: 5× Standardprofil des Projekts

Werte ohne spezifisches Element im Informationsmodell (ohne url, reference, system, version, Erzähltext):

- `composition-dglp#Composition.extension:version.valueString` (1×)
- `composition-dglp#Composition.section.code.coding.code` (1×)
- `composition-dglp#Composition.section.code.coding.display` (1×)
- `composition-dglp#Composition.section.title` (1×)
- `composition-dglp#Composition.status` (1×)
- `composition-dglp#Composition.subject.identifier.value` (1×)
- `composition-dglp#Composition.title` (1×)
- `composition-dglp#Composition.type.coding.code` (2×)
- `composition-dglp#Composition.type.coding.display` (2×)
- `diagnostic-report-dglp#DiagnosticReport.subject.identifier.value` (1×)
- `observation-laboratory-study-dglp#Observation.subject.identifier.value` (4×)
- `observation-laboratory-study-group-dglp#Observation.effectiveDateTime.extension.valueCode` (3×)
- `observation-laboratory-study-group-dglp#Observation.status` (3×)
- `observation-laboratory-study-group-dglp#Observation.subject.identifier.value` (3×)
- `service-request-dglp#ServiceRequest.code.coding.code` (1×)
- `service-request-dglp#ServiceRequest.code.coding.display` (1×)
- `service-request-dglp#ServiceRequest.intent` (1×)
- `service-request-dglp#ServiceRequest.status` (1×)
- `service-request-dglp#ServiceRequest.subject.identifier.value` (1×)
- `specimen-dglp#Specimen.subject.identifier.value` (1×)
- `ti-organization#Organization.name` (2×)
- `ti-patient#Patient.birthDate` (1×)
- `ti-patient#Patient.name.family` (1×)
- `ti-patient#Patient.name.given` (1×)
- `ti-practitioner#Practitioner.name.text` (1×)
- `ti-practitioner-role#PractitionerRole.organization.display` (1×)
- `ti-practitioner-role#PractitionerRole.practitioner.display` (1×)

### Vorbefund — Hoffmann, 18.03.2026

- Zweck: Vorbefund derselben Patientin aus einem anderen Labor; Grundlage für Verlauf und Kumulativansicht.
- Herkunft: Demo-PVS (github.com/mno-93/demo-pvs, Commit d0e9615), erzeugt mit laborbefundBauen. Fiktive Daten.
- Datei: `beispiele/hoffmann-2026-03-18.json`
- Profilzuordnung ohne `meta.profile`: 5× Standardprofil des Projekts

Werte ohne spezifisches Element im Informationsmodell (ohne url, reference, system, version, Erzähltext):

- `composition-dglp#Composition.extension:version.valueString` (1×)
- `composition-dglp#Composition.section.code.coding.code` (1×)
- `composition-dglp#Composition.section.code.coding.display` (1×)
- `composition-dglp#Composition.section.title` (1×)
- `composition-dglp#Composition.status` (1×)
- `composition-dglp#Composition.subject.identifier.value` (1×)
- `composition-dglp#Composition.title` (1×)
- `composition-dglp#Composition.type.coding.code` (2×)
- `composition-dglp#Composition.type.coding.display` (2×)
- `diagnostic-report-dglp#DiagnosticReport.subject.identifier.value` (1×)
- `observation-laboratory-study-dglp#Observation.subject.identifier.value` (3×)
- `observation-laboratory-study-group-dglp#Observation.effectiveDateTime.extension.valueCode` (2×)
- `observation-laboratory-study-group-dglp#Observation.status` (2×)
- `observation-laboratory-study-group-dglp#Observation.subject.identifier.value` (2×)
- `service-request-dglp#ServiceRequest.code.coding.code` (1×)
- `service-request-dglp#ServiceRequest.code.coding.display` (1×)
- `service-request-dglp#ServiceRequest.intent` (1×)
- `service-request-dglp#ServiceRequest.status` (1×)
- `service-request-dglp#ServiceRequest.subject.identifier.value` (1×)
- `specimen-dglp#Specimen.subject.identifier.value` (1×)
- `ti-organization#Organization.name` (2×)
- `ti-patient#Patient.birthDate` (1×)
- `ti-patient#Patient.name.family` (1×)
- `ti-patient#Patient.name.given` (1×)
- `ti-practitioner#Practitioner.name.text` (1×)
- `ti-practitioner-role#PractitionerRole.organization.display` (1×)
- `ti-practitioner-role#PractitionerRole.practitioner.display` (1×)

### Schilddrüse (TSH) — Yildiz, 02.07.2026

- Zweck: Minimaler Befund: eine Gruppe, ein Wert im Referenzbereich.
- Herkunft: Demo-PVS (github.com/mno-93/demo-pvs, Commit d0e9615), erzeugt mit laborbefundBauen. Fiktive Daten.
- Datei: `beispiele/yildiz-2026-07-02.json`
- Profilzuordnung ohne `meta.profile`: 5× Standardprofil des Projekts

Werte ohne spezifisches Element im Informationsmodell (ohne url, reference, system, version, Erzähltext):

- `composition-dglp#Composition.extension:version.valueString` (1×)
- `composition-dglp#Composition.section.code.coding.code` (1×)
- `composition-dglp#Composition.section.code.coding.display` (1×)
- `composition-dglp#Composition.section.title` (1×)
- `composition-dglp#Composition.status` (1×)
- `composition-dglp#Composition.subject.identifier.value` (1×)
- `composition-dglp#Composition.title` (1×)
- `composition-dglp#Composition.type.coding.code` (2×)
- `composition-dglp#Composition.type.coding.display` (2×)
- `diagnostic-report-dglp#DiagnosticReport.subject.identifier.value` (1×)
- `observation-laboratory-study-dglp#Observation.subject.identifier.value` (1×)
- `observation-laboratory-study-group-dglp#Observation.effectiveDateTime.extension.valueCode` (1×)
- `observation-laboratory-study-group-dglp#Observation.status` (1×)
- `observation-laboratory-study-group-dglp#Observation.subject.identifier.value` (1×)
- `service-request-dglp#ServiceRequest.code.coding.code` (1×)
- `service-request-dglp#ServiceRequest.code.coding.display` (1×)
- `service-request-dglp#ServiceRequest.intent` (1×)
- `service-request-dglp#ServiceRequest.status` (1×)
- `service-request-dglp#ServiceRequest.subject.identifier.value` (1×)
- `specimen-dglp#Specimen.subject.identifier.value` (1×)
- `ti-organization#Organization.name` (2×)
- `ti-patient#Patient.birthDate` (1×)
- `ti-patient#Patient.name.family` (1×)
- `ti-patient#Patient.name.given` (1×)
- `ti-practitioner#Practitioner.name.text` (1×)
- `ti-practitioner-role#PractitionerRole.organization.display` (1×)
- `ti-practitioner-role#PractitionerRole.practitioner.display` (1×)

### IG-Beispiel mit Probe, Gerät und Anhang

- Zweck: Beispielinstanzen des IG um Composition cdfb127b: belegt viele optionale Profile (Probe, Additiv, Behälter, Gerät, Diagnose, Bildanhang), Inhalte überwiegend Platzhalter.
- Herkunft: Paket de.gematik.epa.laboratory#1.0.0-ballot.1, Ordner example/ (kein Bundle im Paket; Hülle der Verweise ab der Composition).
- Datei: `de.gematik.epa.laboratory#1.0.0-ballot.1 · Composition/cdfb127b-df3c-493f-bc7e-e8be4a7bdc45`

Werte ohne spezifisches Element im Informationsmodell (ohne url, reference, system, version, Erzähltext):

- `body-structure-dglp#BodyStructure.patient.identifier.type.coding.code` (1×)
- `body-structure-dglp#BodyStructure.patient.identifier.type.coding.display` (1×)
- `body-structure-dglp#BodyStructure.patient.identifier.value` (1×)
- `composition-dglp#Composition.extension:version.valueString` (1×)
- `composition-dglp#Composition.section.code.coding.code` (1×)
- `composition-dglp#Composition.section.code.coding.display` (1×)
- `composition-dglp#Composition.section.code.text` (1×)
- `composition-dglp#Composition.section.title` (1×)
- `composition-dglp#Composition.status` (1×)
- `composition-dglp#Composition.subject.identifier.type.coding.code` (1×)
- `composition-dglp#Composition.subject.identifier.type.coding.display` (1×)
- `composition-dglp#Composition.subject.identifier.value` (1×)
- `composition-dglp#Composition.title` (1×)
- `composition-dglp#Composition.type.coding.code` (2×)
- `composition-dglp#Composition.type.coding.display` (2×)
- `condition-diagnosis-dglp#Condition.subject.identifier.type.coding.code` (1×)
- `condition-diagnosis-dglp#Condition.subject.identifier.type.coding.display` (1×)
- `condition-diagnosis-dglp#Condition.subject.identifier.value` (1×)
- `device-specimen-subject-dglp#Device.patient.identifier.type.coding.code` (1×)
- `device-specimen-subject-dglp#Device.patient.identifier.type.coding.display` (1×)
- `device-specimen-subject-dglp#Device.patient.identifier.value` (1×)
- `diagnostic-report-dglp#DiagnosticReport.subject.identifier.type.coding.code` (1×)
- `diagnostic-report-dglp#DiagnosticReport.subject.identifier.type.coding.display` (1×)
- `diagnostic-report-dglp#DiagnosticReport.subject.identifier.value` (1×)
- `document-reference-dglp#DocumentReference.status` (1×)
- `document-reference-dglp#DocumentReference.subject.identifier.type.coding.code` (1×)
- `document-reference-dglp#DocumentReference.subject.identifier.type.coding.display` (1×)
- `document-reference-dglp#DocumentReference.subject.identifier.value` (1×)
- `observation-image-attachment-dglp#Observation.category:laboratory.coding.code` (1×)
- `observation-image-attachment-dglp#Observation.category:laboratory.coding.display` (1×)
- `observation-image-attachment-dglp#Observation.subject.identifier.type.coding.code` (1×)
- `observation-image-attachment-dglp#Observation.subject.identifier.type.coding.display` (1×)
- `observation-image-attachment-dglp#Observation.subject.identifier.value` (1×)
- `observation-laboratory-study-dglp#Observation.subject.identifier.type.coding.code` (1×)
- `observation-laboratory-study-dglp#Observation.subject.identifier.type.coding.display` (1×)
- `observation-laboratory-study-dglp#Observation.subject.identifier.value` (1×)
- `observation-laboratory-study-group-dglp#Observation.effectiveDateTime.extension.valueCode` (1×)
- `observation-laboratory-study-group-dglp#Observation.status` (1×)
- `observation-laboratory-study-group-dglp#Observation.subject.identifier.type.coding.code` (1×)
- `observation-laboratory-study-group-dglp#Observation.subject.identifier.type.coding.display` (1×)
- `observation-laboratory-study-group-dglp#Observation.subject.identifier.value` (1×)
- `service-request-dglp#ServiceRequest.code.coding.code` (1×)
- `service-request-dglp#ServiceRequest.code.coding.display` (1×)
- `service-request-dglp#ServiceRequest.intent` (1×)
- `service-request-dglp#ServiceRequest.status` (1×)
- `service-request-dglp#ServiceRequest.subject.identifier.type.coding.code` (1×)
- `service-request-dglp#ServiceRequest.subject.identifier.type.coding.display` (1×)
- `service-request-dglp#ServiceRequest.subject.identifier.value` (1×)
- `specimen-dglp#Specimen.subject.identifier.type.coding.code` (2×)
- `specimen-dglp#Specimen.subject.identifier.type.coding.display` (2×)
- `specimen-dglp#Specimen.subject.identifier.value` (2×)
- `ti-organization#Organization.address.city` (1×)
- `ti-organization#Organization.address.country` (1×)
- `ti-organization#Organization.address.line` (1×)
- `ti-organization#Organization.address.postalCode` (1×)
- `ti-organization#Organization.address.type` (1×)
- `ti-organization#Organization.contact.address.city` (1×)
- `ti-organization#Organization.contact.address.country` (1×)
- `ti-organization#Organization.contact.address.line` (2×)
- `ti-organization#Organization.contact.address.postalCode` (1×)
- `ti-organization#Organization.contact.address.type` (1×)
- `ti-organization#Organization.contact.name.family` (1×)
- `ti-organization#Organization.contact.name.given` (1×)
- `ti-organization#Organization.contact.name.text` (1×)
- `ti-organization#Organization.contact.name.use` (1×)
- `ti-organization#Organization.contact.purpose.coding.code` (1×)
- `ti-organization#Organization.contact.purpose.coding.display` (1×)
- `ti-organization#Organization.contact.telecom.value` (1×)
- `ti-organization#Organization.name` (1×)
- `ti-organization#Organization.telecom.value` (1×)
- `ti-organization#Organization.type.coding.code` (1×)
- `ti-organization#Organization.type.coding.display` (1×)
- `ti-patient#Patient.birthDate` (1×)
- `ti-patient#Patient.gender` (1×)
- `ti-patient#Patient.name:Geburtsname.family` (1×)
- `ti-patient#Patient.name:Geburtsname.family.extension.valueString` (1×)
- `ti-patient#Patient.name:Geburtsname.use` (1×)
- `ti-patient#Patient.name:Name.family` (1×)
- `ti-patient#Patient.name:Name.given` (1×)
- `ti-patient#Patient.name:Name.prefix` (1×)
- `ti-patient#Patient.name:Name.prefix.extension.valueCode` (1×)
- `ti-patient#Patient.name:Name.use` (1×)
- `ti-practitioner#Practitioner.gender` (1×)
- `ti-practitioner#Practitioner.name.family` (1×)
- `ti-practitioner#Practitioner.name.given` (1×)
- `ti-practitioner#Practitioner.name.prefix` (1×)
- `ti-practitioner#Practitioner.name.prefix.extension:prefix-qualifier.valueCode` (1×)
- `ti-practitioner#Practitioner.name.text` (1×)
- `ti-practitioner#Practitioner.name.use` (1×)
- `ti-practitioner#Practitioner.qualification.code.coding.code` (1×)
- `ti-practitioner#Practitioner.qualification.code.coding.display` (1×)
- `ti-practitioner#Practitioner.telecom.value` (1×)

### IG-Beispiel, zweite Composition

- Zweck: Zweite Composition des IG mit eigenem Laborgesamtbefund und Auftrag.
- Herkunft: Paket de.gematik.epa.laboratory#1.0.0-ballot.1, Ordner example/ (Hülle der Verweise ab der Composition).
- Datei: `de.gematik.epa.laboratory#1.0.0-ballot.1 · Composition/13c807c0-53e7-488e-84bb-023376563cf3`

Werte ohne spezifisches Element im Informationsmodell (ohne url, reference, system, version, Erzähltext):

- `body-structure-dglp#BodyStructure.patient.identifier.type.coding.code` (1×)
- `body-structure-dglp#BodyStructure.patient.identifier.type.coding.display` (1×)
- `body-structure-dglp#BodyStructure.patient.identifier.value` (1×)
- `composition-dglp#Composition.extension:version.valueString` (1×)
- `composition-dglp#Composition.section.code.coding.code` (1×)
- `composition-dglp#Composition.section.code.coding.display` (1×)
- `composition-dglp#Composition.section.title` (1×)
- `composition-dglp#Composition.status` (1×)
- `composition-dglp#Composition.subject.identifier.type.coding.code` (1×)
- `composition-dglp#Composition.subject.identifier.type.coding.display` (1×)
- `composition-dglp#Composition.subject.identifier.value` (1×)
- `composition-dglp#Composition.title` (1×)
- `composition-dglp#Composition.type.coding.code` (2×)
- `composition-dglp#Composition.type.coding.display` (2×)
- `device-specimen-subject-dglp#Device.patient.identifier.type.coding.code` (1×)
- `device-specimen-subject-dglp#Device.patient.identifier.type.coding.display` (1×)
- `device-specimen-subject-dglp#Device.patient.identifier.value` (1×)
- `diagnostic-report-dglp#DiagnosticReport.subject.identifier.type.coding.code` (1×)
- `diagnostic-report-dglp#DiagnosticReport.subject.identifier.type.coding.display` (1×)
- `diagnostic-report-dglp#DiagnosticReport.subject.identifier.value` (1×)
- `observation-laboratory-study-dglp#Observation.subject.identifier.type.coding.code` (2×)
- `observation-laboratory-study-dglp#Observation.subject.identifier.type.coding.display` (2×)
- `observation-laboratory-study-dglp#Observation.subject.identifier.value` (2×)
- `observation-laboratory-study-group-dglp#Observation.effectiveDateTime.extension.valueCode` (2×)
- `observation-laboratory-study-group-dglp#Observation.status` (2×)
- `observation-laboratory-study-group-dglp#Observation.subject.identifier.type.coding.code` (2×)
- `observation-laboratory-study-group-dglp#Observation.subject.identifier.type.coding.display` (2×)
- `observation-laboratory-study-group-dglp#Observation.subject.identifier.value` (2×)
- `service-request-dglp#ServiceRequest.code.coding.code` (1×)
- `service-request-dglp#ServiceRequest.code.coding.display` (1×)
- `service-request-dglp#ServiceRequest.intent` (1×)
- `service-request-dglp#ServiceRequest.status` (1×)
- `service-request-dglp#ServiceRequest.subject.identifier.type.coding.code` (1×)
- `service-request-dglp#ServiceRequest.subject.identifier.type.coding.display` (1×)
- `service-request-dglp#ServiceRequest.subject.identifier.value` (1×)
- `specimen-dglp#Specimen.subject.identifier.type.coding.code` (2×)
- `specimen-dglp#Specimen.subject.identifier.type.coding.display` (2×)
- `specimen-dglp#Specimen.subject.identifier.value` (2×)
- `ti-organization#Organization.address.city` (1×)
- `ti-organization#Organization.address.country` (1×)
- `ti-organization#Organization.address.line` (1×)
- `ti-organization#Organization.address.postalCode` (1×)
- `ti-organization#Organization.address.type` (1×)
- `ti-organization#Organization.contact.address.city` (1×)
- `ti-organization#Organization.contact.address.country` (1×)
- `ti-organization#Organization.contact.address.line` (2×)
- `ti-organization#Organization.contact.address.postalCode` (1×)
- `ti-organization#Organization.contact.address.type` (1×)
- `ti-organization#Organization.contact.name.family` (1×)
- `ti-organization#Organization.contact.name.given` (1×)
- `ti-organization#Organization.contact.name.text` (1×)
- `ti-organization#Organization.contact.name.use` (1×)
- `ti-organization#Organization.contact.purpose.coding.code` (1×)
- `ti-organization#Organization.contact.purpose.coding.display` (1×)
- `ti-organization#Organization.contact.telecom.value` (1×)
- `ti-organization#Organization.name` (1×)
- `ti-organization#Organization.telecom.value` (1×)
- `ti-organization#Organization.type.coding.code` (1×)
- `ti-organization#Organization.type.coding.display` (1×)
- `ti-patient#Patient.birthDate` (1×)
- `ti-patient#Patient.gender` (1×)
- `ti-patient#Patient.name:Geburtsname.family` (1×)
- `ti-patient#Patient.name:Geburtsname.family.extension.valueString` (1×)
- `ti-patient#Patient.name:Geburtsname.use` (1×)
- `ti-patient#Patient.name:Name.family` (1×)
- `ti-patient#Patient.name:Name.given` (1×)
- `ti-patient#Patient.name:Name.prefix` (1×)
- `ti-patient#Patient.name:Name.prefix.extension.valueCode` (1×)
- `ti-patient#Patient.name:Name.use` (1×)
- `ti-practitioner#Practitioner.gender` (1×)
- `ti-practitioner#Practitioner.name.family` (1×)
- `ti-practitioner#Practitioner.name.given` (1×)
- `ti-practitioner#Practitioner.name.prefix` (1×)
- `ti-practitioner#Practitioner.name.prefix.extension:prefix-qualifier.valueCode` (1×)
- `ti-practitioner#Practitioner.name.text` (1×)
- `ti-practitioner#Practitioner.name.use` (1×)
- `ti-practitioner#Practitioner.qualification.code.coding.code` (1×)
- `ti-practitioner#Practitioner.qualification.code.coding.display` (1×)
- `ti-practitioner#Practitioner.telecom.value` (1×)
