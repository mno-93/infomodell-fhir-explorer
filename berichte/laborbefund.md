# Prüfbericht — Laborbefund (dgLP)

> Erzeugt von `python3 werkzeuge/mx.py bauen`. Nicht von Hand ändern; die CI prüft, dass der Bericht zum Stand passt.

> ![KI-gestützt erstellt](../web/ki-hinweis.svg) **Hinweis zur KI-Nutzung:** Dieser Modellexplorer – Programmcode, Projektkonfiguration und Texte – ist mit Unterstützung eines KI-Assistenten (Claude von Anthropic) entstanden. Die Darstellungen sind aus veröffentlichten Spezifikationen abgeleitet und keine Primärquelle; sie können Fehler enthalten. Maßgeblich sind die verlinkten Implementierungsleitfäden und FHIR-Pakete. Alle Beispieldaten sind fiktiv.

## Quellen

- Implementation Guide: ePA Laboratory Report Implementation Guide (`de.gematik.epa.laboratory#1.0.0-ballot.1`, öffentlicher Ballot, 15.09.2026)
- Darstellung des Modells: Informationsmodell
- Pakete: `de.gematik.epa.laboratory#1.0.0-ballot.1`, `de.gematik.ti#1.5.0-ballot.2`, `hl7.fhir.eu.laboratory#2.0.0`, `hl7.fhir.eu.base#2.0.1`, `hl7.fhir.eu.extensions.r4#1.3.1`, `hl7.fhir.uv.xver-r5.r4#0.1.0`, `hl7.fhir.uv.extensions.r4#5.3.0`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.r4.core#4.0.1`

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
| Fallbeispiel 1 nach MIO Laborbefund — Hansen, 15.11.2021 | 43 | 1085 | 9 | 14 |

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

### Fallbeispiel 1 nach MIO Laborbefund — Hansen, 15.11.2021

- Zweck: Dokument nach den KBV-Profilen MIO Laborbefund 1.0.0-update zur inhaltlichen Sichtung: vier Untersuchungsgruppen (Klinische Chemie, Vitamine, Endokrinologie, Blutbild) mit 28 Werten, Auftrag, zwei Proben, Freigabe und Provenance. Validiert gegen das veröffentlichte Paket kbv.mio.laborbefund 1.0.0-update; es enthält keine Snapshots, deshalb ordnet die Darstellung über Standardprofil bzw. Basisressource zu.
- Herkunft: Fallbeispiel 1 zum MIO Laborbefund 1.0.0-update (KBV): Bundle-Bundle-ex1-1.json aus der SUSHI-Ausgabe, unverändert; zur Veröffentlichung freigegeben. Mit Claude erzeugt, fiktive Daten.
- Datei: `beispiele/mio-lab-ex1.json`
- Profilzuordnung ohne `meta.profile`: 38× Basisressource, 5× Standardprofil des Projekts

**Strukturbefunde** (Element im Profil nicht auflösbar):

- `Observation · Observation.extension.extension:value.url` — Slice `extension:value` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:value.valueQuantity.system` — Slice `extension:value` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:value.valueQuantity.value` — Slice `extension:value` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:value.valueQuantity.code` — Slice `extension:value` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:value.valueQuantity.unit` — Slice `extension:value` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:referenceRange.valueRange.low.system` — Slice `extension:referenceRange` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:referenceRange.valueRange.low.value` — Slice `extension:referenceRange` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:referenceRange.valueRange.low.code` — Slice `extension:referenceRange` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:referenceRange.valueRange.low.unit` — Slice `extension:referenceRange` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:referenceRange.valueRange.high.system` — Slice `extension:referenceRange` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:referenceRange.valueRange.high.value` — Slice `extension:referenceRange` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:referenceRange.valueRange.high.code` — Slice `extension:referenceRange` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:referenceRange.valueRange.high.unit` — Slice `extension:referenceRange` unter `Extension` nicht definiert
- `Observation · Observation.extension.extension:referenceRange.url` — Slice `extension:referenceRange` unter `Extension` nicht definiert

Werte ohne spezifisches Element im Informationsmodell (ohne url, reference, system, version, Erzähltext):

- `Composition#Composition.attester.mode` (1×)
- `Composition#Composition.attester.time` (1×)
- `Composition#Composition.date` (1×)
- `Composition#Composition.extension.valueString` (1×)
- `Composition#Composition.identifier.value` (1×)
- `Composition#Composition.status` (1×)
- `Composition#Composition.subject.identifier.type.coding.code` (1×)
- `Composition#Composition.subject.identifier.type.coding.display` (1×)
- `Composition#Composition.subject.identifier.value` (1×)
- `Composition#Composition.title` (1×)
- `Composition#Composition.type.coding.code` (1×)
- `Composition#Composition.type.coding.display` (1×)
- `DiagnosticReport#DiagnosticReport.code.coding.code` (1×)
- `DiagnosticReport#DiagnosticReport.code.coding.display` (1×)
- `DiagnosticReport#DiagnosticReport.conclusion` (1×)
- `DiagnosticReport#DiagnosticReport.extension.valueDateTime` (1×)
- `DiagnosticReport#DiagnosticReport.identifier.type.coding.code` (1×)
- `DiagnosticReport#DiagnosticReport.identifier.type.coding.display` (1×)
- `DiagnosticReport#DiagnosticReport.identifier.value` (1×)
- `DiagnosticReport#DiagnosticReport.issued` (1×)
- `DiagnosticReport#DiagnosticReport.presentedForm.contentType` (1×)
- `DiagnosticReport#DiagnosticReport.presentedForm.creation` (1×)
- `DiagnosticReport#DiagnosticReport.presentedForm.data` (1×)
- `DiagnosticReport#DiagnosticReport.presentedForm.title` (1×)
- `DiagnosticReport#DiagnosticReport.result.extension.valuePositiveInt` (4×)
- `DiagnosticReport#DiagnosticReport.status` (1×)
- `DiagnosticReport#DiagnosticReport.subject.identifier.type.coding.code` (1×)
- `DiagnosticReport#DiagnosticReport.subject.identifier.type.coding.display` (1×)
- `DiagnosticReport#DiagnosticReport.subject.identifier.value` (1×)
- `Observation#Observation.category.coding.code` (73×)
- `Observation#Observation.category.coding.display` (73×)
- `Observation#Observation.category.extension.valueString` (73×)
- `Observation#Observation.category.text` (41×)
- `Observation#Observation.code.coding.code` (32×)
- `Observation#Observation.code.coding.display` (32×)
- `Observation#Observation.code.text` (28×)
- `Observation#Observation.effectiveDateTime` (28×)
- `Observation#Observation.effectiveDateTime.extension.valueCode` (4×)
- `Observation#Observation.extension.extension:referenceRange.valueRange.high.code` (1×)
- `Observation#Observation.extension.extension:referenceRange.valueRange.high.unit` (1×)
- `Observation#Observation.extension.extension:referenceRange.valueRange.high.value` (1×)
- `Observation#Observation.extension.extension:referenceRange.valueRange.low.code` (1×)
- `Observation#Observation.extension.extension:referenceRange.valueRange.low.unit` (1×)
- `Observation#Observation.extension.extension:referenceRange.valueRange.low.value` (1×)
- `Observation#Observation.extension.extension:value.valueQuantity.code` (1×)
- `Observation#Observation.extension.extension:value.valueQuantity.unit` (1×)
- `Observation#Observation.extension.extension:value.valueQuantity.value` (1×)
- `Observation#Observation.hasMember.extension.valuePositiveInt` (28×)
- `Observation#Observation.interpretation.coding.code` (28×)
- `Observation#Observation.interpretation.coding.display` (28×)
- `Observation#Observation.interpretation.text` (30×)
- `Observation#Observation.issued` (28×)
- `Observation#Observation.method.text` (2×)
- `Observation#Observation.referenceRange.high.code` (26×)
- `Observation#Observation.referenceRange.high.unit` (26×)
- `Observation#Observation.referenceRange.high.value` (26×)
- `Observation#Observation.referenceRange.low.code` (24×)
- `Observation#Observation.referenceRange.low.unit` (24×)
- `Observation#Observation.referenceRange.low.value` (24×)
- `Observation#Observation.referenceRange.text` (1×)
- `Observation#Observation.referenceRange.type.coding.code` (28×)
- `Observation#Observation.referenceRange.type.coding.display` (28×)
- `Observation#Observation.status` (32×)
- `Observation#Observation.subject.identifier.type.coding.code` (32×)
- `Observation#Observation.subject.identifier.type.coding.display` (32×)
- `Observation#Observation.subject.identifier.value` (32×)
- `Observation#Observation.valueQuantity.code` (28×)
- `Observation#Observation.valueQuantity.comparator` (1×)
- `Observation#Observation.valueQuantity.unit` (28×)
- `Observation#Observation.valueQuantity.value` (28×)
- `Provenance#Provenance.activity.coding.code` (1×)
- `Provenance#Provenance.activity.coding.display` (1×)
- `Provenance#Provenance.occurredDateTime` (1×)
- `Provenance#Provenance.recorded` (1×)
- `ServiceRequest#ServiceRequest.authoredOn` (1×)
- `ServiceRequest#ServiceRequest.code.coding.code` (1×)
- `ServiceRequest#ServiceRequest.code.coding.display` (1×)
- `ServiceRequest#ServiceRequest.identifier.type.coding.code` (1×)
- `ServiceRequest#ServiceRequest.identifier.type.coding.display` (1×)
- `ServiceRequest#ServiceRequest.identifier.value` (1×)
- `ServiceRequest#ServiceRequest.intent` (1×)
- `ServiceRequest#ServiceRequest.priority` (1×)
- `ServiceRequest#ServiceRequest.reasonCode.extension.valueString` (1×)
- `ServiceRequest#ServiceRequest.reasonCode.text` (1×)
- `ServiceRequest#ServiceRequest.status` (1×)
- `ServiceRequest#ServiceRequest.subject.identifier.type.coding.code` (1×)
- `ServiceRequest#ServiceRequest.subject.identifier.type.coding.display` (1×)
- `ServiceRequest#ServiceRequest.subject.identifier.value` (1×)
- `ServiceRequest#ServiceRequest.supportingInfo.display` (1×)
- `Specimen#Specimen.collection.collectedDateTime` (2×)
- `Specimen#Specimen.identifier.value` (2×)
- `Specimen#Specimen.receivedTime` (2×)
- `Specimen#Specimen.status` (2×)
- `Specimen#Specimen.subject.identifier.type.coding.code` (2×)
- `Specimen#Specimen.subject.identifier.type.coding.display` (2×)
- `Specimen#Specimen.subject.identifier.value` (2×)
- `Specimen#Specimen.type.coding.code` (2×)
- `Specimen#Specimen.type.coding.display` (2×)
- `Specimen#Specimen.type.text` (2×)
- `ti-organization#Organization.address.city` (1×)
- `ti-organization#Organization.address.country` (1×)
- `ti-organization#Organization.address.line` (1×)
- `ti-organization#Organization.address.line.extension:houseNumber.valueString` (1×)
- `ti-organization#Organization.address.line.extension:streetName.valueString` (1×)
- `ti-organization#Organization.address.postalCode` (1×)
- `ti-organization#Organization.address.type` (1×)
- `ti-organization#Organization.name` (1×)
- `ti-organization#Organization.telecom.value` (3×)
- `ti-patient#Patient.birthDate` (1×)
- `ti-patient#Patient.gender` (1×)
- `ti-patient#Patient.name:Name.family` (1×)
- `ti-patient#Patient.name:Name.family.extension.valueString` (1×)
- `ti-patient#Patient.name:Name.given` (1×)
- `ti-patient#Patient.name:Name.text` (1×)
- `ti-patient#Patient.name:Name.use` (1×)
- `ti-patient#Patient.telecom.value` (1×)
- `ti-practitioner#Practitioner.address.city` (1×)
- `ti-practitioner#Practitioner.address.country` (1×)
- `ti-practitioner#Practitioner.address.line` (1×)
- `ti-practitioner#Practitioner.address.line.extension.valueString` (2×)
- `ti-practitioner#Practitioner.address.postalCode` (1×)
- `ti-practitioner#Practitioner.address.type` (1×)
- `ti-practitioner#Practitioner.gender` (2×)
- `ti-practitioner#Practitioner.name.family` (2×)
- `ti-practitioner#Practitioner.name.family.extension:nachname.valueString` (2×)
- `ti-practitioner#Practitioner.name.given` (2×)
- `ti-practitioner#Practitioner.name.prefix` (2×)
- `ti-practitioner#Practitioner.name.prefix.extension:prefix-qualifier.valueCode` (2×)
- `ti-practitioner#Practitioner.name.text` (2×)
- `ti-practitioner#Practitioner.name.use` (2×)
- `ti-practitioner#Practitioner.qualification.code.coding.code` (2×)
- `ti-practitioner#Practitioner.qualification.code.coding.display` (2×)
- `ti-practitioner-role#PractitionerRole.code.coding.code` (1×)
- `ti-practitioner-role#PractitionerRole.code.coding.display` (1×)

## Anzeige für Anwender:innen

Stand: `berichte/laborbefund.anzeige.json`, geschrieben von `python3 -I werkzeuge/mx.py anzeige laborbefund`. Gezählt werden inhaltliche Werte der Beispiele, die weder die Anwenderansicht noch eine Dokumentfassung zeigt; auf der Seite stehen sie unter „Weitere Angaben aus der Instanz“. Technisch und nicht gezählt: Kennungen und Metadaten, Systeme, Versionen, URLs, Erzähltext, UUID-Kennungen, Verweise mit Ziel im Beispiel.

| Beispiel | nicht angezeigte Werte | in Elementen |
|---|---:|---:|
| Nierenfunktion und HbA1c — Hoffmann, 12.08.2026 | 0 | 0 |
| Vorbefund — Hoffmann, 18.03.2026 | 0 | 0 |
| Schilddrüse (TSH) — Yildiz, 02.07.2026 | 0 | 0 |
| IG-Beispiel mit Probe, Gerät und Anhang | 152 | 94 |
| IG-Beispiel, zweite Composition | 150 | 87 |
| Fallbeispiel 1 nach MIO Laborbefund — Hansen, 15.11.2021 | 22 | 17 |

**Verknüpfungen** zwischen Instanz, Profil und Informationsmodell (in allen Richtungen, über Profilgrenzen, mit Rückwegen und jedem Klick in der Anwenderansicht): alle tragen.

### Nicht angezeigt — IG-Beispiel mit Probe, Gerät und Anhang

| Element | Anzahl | Werte (Auswahl) |
|---|---:|---|
| `BodyStructure · extension.extension.extension.valueCodeableConcept.coding.code` | 1 | 260330005 |
| `BodyStructure · extension.extension.extension.valueCodeableConcept.coding.display` | 1 | 3 o'clock position |
| `BodyStructure · extension.extension.extension.valueCodeableConcept.text` | 1 | test |
| `BodyStructure · extension.extension.valueCodeableConcept.coding.code` | 3 | 90432007 · 7771000 · 46053002 |
| `BodyStructure · extension.extension.valueCodeableConcept.coding.display` | 3 | Structure of mucous membrane of nasopharynx · Left · Distal |
| `BodyStructure · extension.extension.valueCodeableConcept.text` | 3 | test |
| `BodyStructure · morphology.coding.code` | 1 | 75910000 |
| `BodyStructure · morphology.coding.display` | 1 | Congenital hypersegmentation |
| `BodyStructure · morphology.text` | 1 | test |
| `Condition · clinicalStatus.coding.code` | 1 | active |
| `Condition · clinicalStatus.coding.display` | 1 | Active |
| `Condition · verificationStatus.coding.code` | 1 | provisional |
| `Condition · verificationStatus.coding.display` | 1 | Provisional |
| `Device · deviceName.name` | 2 | Test-Name · Test Model |
| `Device · deviceName.type` | 2 | manufacturer-name · model-name |
| `Device · distinctIdentifier` | 3 | example |
| `Device · expirationDate` | 3 | 01.04.2026 16:55 · 15.11.2021 16:55 |
| `Device · identifier.type.coding.code` | 3 | UDI |
| `Device · identifier.type.coding.display` | 3 | Universal Device Identifier |
| `Device · identifier.value` | 3 | 123456 · 345675 |
| `Device · lotNumber` | 3 | 12345 |
| `Device · manufactureDate` | 3 | 01.04.2024 16:55 · 15.11.2021 16:55 |
| `Device · modelNumber` | 3 | 123456789 · 56789 |
| `Device · note.text` | 3 | test |
| `Device · serialNumber` | 3 | 9654537 · 987654 · 12345 |
| `Device · type.coding.code` | 3 | 8407004 · 434711009 · 30234008 |
| `Device · type.coding.display` | 3 | Bile collection bag · Specimen container · Medical laboratory analyzer |
| `Device · type.text` | 3 | Medizinisches Laboranalysegerät · Probenbehälter |
| `Device · udiCarrier.deviceIdentifier` | 3 | example |
| `Device · version.value` | 2 | v1 |
| `DeviceDefinition · manufacturerString` | 3 | Herstellende Einrichtung |
| `DeviceDefinition · type.coding.code` | 3 | 371882005 · 434711009 · 30234008 |
| `DeviceDefinition · type.coding.display` | 3 | Device used · Specimen container · Medical laboratory analyzer |
| `DocumentReference · category.coding.code` | 1 | ADM |
| `DocumentReference · category.coding.display` | 1 | Administratives Dokument |
| `DocumentReference · category.text` | 1 | test |
| `DocumentReference · content.attachment.contentType` | 1 | application/pdf |
| `DocumentReference · content.attachment.creation` | 1 | 06.05.2022 |
| `DocumentReference · content.attachment.data` | 1 | dGVzdA== |
| `DocumentReference · content.attachment.title` | 1 | Anhang |
| `DocumentReference · status` | 1 | current |
| `DocumentReference · type.coding.code` | 1 | PATI |
| `DocumentReference · type.coding.display` | 1 | Patienteninformationen |
| `DocumentReference · type.text` | 1 | test |
| `Observation · extension.valueBoolean` | 3 | ja |
| `Observation · extension.valueCodeableConcept.coding.code` | 1 | haemato |
| `Observation · extension.valueCodeableConcept.coding.display` | 1 | Hämatologie |
| `Observation · extension.valueCodeableConcept.text` | 1 | Hämatologie |
| `Observation · extension.valueDecimal` | 1 | 2 |
| `Observation · identifier.type.coding.code` | 2 | OBI · UDI |
| `Observation · identifier.type.coding.display` | 2 | Observation Instance Identifier · Universal Device Identifier |
| `Observation · identifier.value` | 2 | 123456 |
| `Organization · contact.address.city` | 1 | Berlin |
| `Organization · contact.address.country` | 1 | D |
| `Organization · contact.address.line` | 2 | Muster-Allee 42 · Neukölln |
| `Organization · contact.address.postalCode` | 1 | 9132 |
| `Organization · contact.address.type` | 1 | both |
| `Organization · contact.name.family` | 1 | Ehrlich |
| `Organization · contact.name.given` | 1 | Marianne |
| `Organization · contact.name.text` | 1 | Frau Marianne Ehrlich |
| `Organization · contact.name.use` | 1 | official |
| `Organization · contact.purpose.coding.code` | 1 | PATINF |
| `Organization · contact.purpose.coding.display` | 1 | Patient |
| `Organization · contact.telecom.value` | 1 | 0173777 |
| `Organization · identifier.type.coding.code` | 4 | XX · BSNR · KZVA |
| `Organization · identifier.value` | 4 | 123456789 · 9-2.58.00000040 |
| `Organization · telecom.value` | 1 | 0173555 |
| `Organization · type.coding.code` | 1 | 1.2.276.0.76.4.54 |
| `Organization · type.coding.display` | 1 | Öffentliche Apotheke |
| `Patient · name._family.extension.valueString` | 1 | Blohm |
| `Patient · name.family` | 1 | Blohm |
| `Patient · name.use` | 1 | maiden |
| `Practitioner · gender` | 1 | other |
| `Practitioner · identifier.type.coding.code` | 2 | LANR · PRN |
| `Practitioner · identifier.type.coding.display` | 2 | Lifelong physician number · Provider number |
| `Practitioner · identifier.value` | 2 | 123456789 · 1-1.58.00000056 |
| `Practitioner · qualification.code.coding.code` | 1 | 26369006 |
| `Practitioner · qualification.code.coding.display` | 1 | Public health nurse |
| `Practitioner · telecom.value` | 1 | 12123455 |
| `ServiceRequest · identifier.type.coding.code` | 1 | NI |
| `ServiceRequest · identifier.type.coding.display` | 1 | Nachforderungsidentifikation |
| `ServiceRequest · identifier.value` | 1 | 20211115-127 |
| `Specimen · collection.collectedDateTime` | 1 | 03.05.2023 |
| `Specimen · container.specimenQuantity.code` | 1 | ms |
| `Specimen · container.specimenQuantity.unit` | 1 | ms |
| `Specimen · container.specimenQuantity.value` | 1 | 20 |
| `Specimen · identifier.value` | 1 | Test Specimen identifier |
| `Specimen · receivedTime` | 1 | 15.11.2021 16:55 |
| `Specimen · status` | 1 | available |
| `Specimen · type.coding.code` | 1 | 119376003 |
| `Specimen · type.coding.display` | 1 | Tissue specimen |
| `Substance · code.coding.code` | 1 | 69519002 |
| `Substance · code.coding.display` | 1 | Edetic acid |
| `Substance · code.text` | 1 | test |

### Nicht angezeigt — IG-Beispiel, zweite Composition

| Element | Anzahl | Werte (Auswahl) |
|---|---:|---|
| `BodyStructure · extension.extension.extension.valueCodeableConcept.coding.code` | 1 | 260330005 |
| `BodyStructure · extension.extension.extension.valueCodeableConcept.coding.display` | 1 | 3 o'clock position |
| `BodyStructure · extension.extension.extension.valueCodeableConcept.text` | 1 | test |
| `BodyStructure · extension.extension.valueCodeableConcept.coding.code` | 3 | 90432007 · 7771000 · 46053002 |
| `BodyStructure · extension.extension.valueCodeableConcept.coding.display` | 3 | Structure of mucous membrane of nasopharynx · Left · Distal |
| `BodyStructure · extension.extension.valueCodeableConcept.text` | 3 | test |
| `BodyStructure · morphology.coding.code` | 1 | 75910000 |
| `BodyStructure · morphology.coding.display` | 1 | Congenital hypersegmentation |
| `BodyStructure · morphology.text` | 1 | test |
| `Device · deviceName.name` | 2 | Test-Name · Test Model |
| `Device · deviceName.type` | 2 | manufacturer-name · model-name |
| `Device · distinctIdentifier` | 3 | example |
| `Device · expirationDate` | 3 | 15.11.2021 16:55 · 01.04.2026 16:55 |
| `Device · identifier.type.coding.code` | 3 | UDI |
| `Device · identifier.type.coding.display` | 3 | Universal Device Identifier |
| `Device · identifier.value` | 3 | 345675 · 123456 |
| `Device · lotNumber` | 3 | 12345 |
| `Device · manufactureDate` | 3 | 15.11.2021 16:55 · 01.04.2024 16:55 |
| `Device · modelNumber` | 3 | 123456789 · 56789 |
| `Device · note.text` | 3 | test |
| `Device · serialNumber` | 3 | 12345 · 9654537 · 987654 |
| `Device · type.coding.code` | 3 | 30234008 · 8407004 · 434711009 |
| `Device · type.coding.display` | 3 | Medical laboratory analyzer · Bile collection bag · Specimen container |
| `Device · type.text` | 3 | Medizinisches Laboranalysegerät · Probenbehälter |
| `Device · udiCarrier.deviceIdentifier` | 3 | example |
| `Device · version.value` | 2 | v1 |
| `DeviceDefinition · manufacturerString` | 3 | Herstellende Einrichtung |
| `DeviceDefinition · type.coding.code` | 3 | 30234008 · 371882005 · 434711009 |
| `DeviceDefinition · type.coding.display` | 3 | Medical laboratory analyzer · Device used · Specimen container |
| `Observation · _effectiveDateTime.extension.valueCode` | 1 | not-permitted |
| `Observation · category.coding.code` | 2 | laboratory |
| `Observation · category.coding.display` | 2 | Laboratory |
| `Observation · code.coding.code` | 2 | laboruntersuchungsgruppe · 98981-4 |
| `Observation · code.coding.display` | 2 | Laboruntersuchungsgruppe · Urate [Mass/volume] in Blood |
| `Observation · effectiveDateTime` | 1 | 15.11.2021 11:30 |
| `Observation · extension.valueBoolean` | 3 | ja |
| `Observation · extension.valueCodeableConcept.coding.code` | 1 | haemato |
| `Observation · extension.valueCodeableConcept.coding.display` | 1 | Hämatologie |
| `Observation · extension.valueCodeableConcept.text` | 1 | Hämatologie |
| `Observation · extension.valueDecimal` | 1 | 2 |
| `Observation · identifier.type.coding.code` | 2 | OBI · UDI |
| `Observation · identifier.type.coding.display` | 2 | Observation Instance Identifier · Universal Device Identifier |
| `Observation · identifier.value` | 2 | 123456 |
| `Observation · issued` | 1 | 15.11.2021 11:30 |
| `Observation · status` | 2 | final |
| `Observation · valueQuantity.code` | 1 | mg/dL |
| `Observation · valueQuantity.unit` | 1 | mg/dL |
| `Observation · valueQuantity.value` | 1 | 6,5 |
| `Organization · contact.address.city` | 1 | Berlin |
| `Organization · contact.address.country` | 1 | D |
| `Organization · contact.address.line` | 2 | Muster-Allee 42 · Neukölln |
| `Organization · contact.address.postalCode` | 1 | 9132 |
| `Organization · contact.address.type` | 1 | both |
| `Organization · contact.name.family` | 1 | Ehrlich |
| `Organization · contact.name.given` | 1 | Marianne |
| `Organization · contact.name.text` | 1 | Frau Marianne Ehrlich |
| `Organization · contact.name.use` | 1 | official |
| `Organization · contact.purpose.coding.code` | 1 | PATINF |
| `Organization · contact.purpose.coding.display` | 1 | Patient |
| `Organization · contact.telecom.value` | 1 | 0173777 |
| `Organization · identifier.type.coding.code` | 4 | XX · BSNR · KZVA |
| `Organization · identifier.value` | 4 | 123456789 · 9-2.58.00000040 |
| `Organization · telecom.value` | 1 | 0173555 |
| `Organization · type.coding.code` | 1 | 1.2.276.0.76.4.54 |
| `Organization · type.coding.display` | 1 | Öffentliche Apotheke |
| `Patient · name._family.extension.valueString` | 1 | Blohm |
| `Patient · name.family` | 1 | Blohm |
| `Patient · name.use` | 1 | maiden |
| `Practitioner · gender` | 1 | other |
| `Practitioner · identifier.type.coding.code` | 2 | LANR · PRN |
| `Practitioner · identifier.type.coding.display` | 2 | Lifelong physician number · Provider number |
| `Practitioner · identifier.value` | 2 | 123456789 · 1-1.58.00000056 |
| `Practitioner · qualification.code.coding.code` | 1 | 26369006 |
| `Practitioner · qualification.code.coding.display` | 1 | Public health nurse |
| `Practitioner · telecom.value` | 1 | 12123455 |
| `Specimen · collection.collectedDateTime` | 1 | 03.05.2023 |
| `Specimen · container.specimenQuantity.code` | 1 | ms |
| `Specimen · container.specimenQuantity.unit` | 1 | ms |
| `Specimen · container.specimenQuantity.value` | 1 | 20 |
| `Specimen · identifier.value` | 1 | Test Specimen identifier |
| `Specimen · receivedTime` | 1 | 15.11.2021 16:55 |
| `Specimen · status` | 1 | available |
| `Specimen · type.coding.code` | 1 | 119376003 |
| `Specimen · type.coding.display` | 1 | Tissue specimen |
| `Substance · code.coding.code` | 1 | 69519002 |
| `Substance · code.coding.display` | 1 | Edetic acid |
| `Substance · code.text` | 1 | test |

### Nicht angezeigt — Fallbeispiel 1 nach MIO Laborbefund — Hansen, 15.11.2021

| Element | Anzahl | Werte (Auswahl) |
|---|---:|---|
| `Organization · identifier.type.coding.code` | 1 | BSNR |
| `Organization · identifier.type.coding.display` | 1 | Primary physician office number |
| `Organization · identifier.value` | 1 | 561234500 |
| `Organization · telecom.value` | 3 | 0511-1234567-0 · 0511-1234567-888 · kontakt@Hannover-MVZ-Musterlabor.de |
| `Patient · telecom.value` | 1 | 0511 5566778 |
| `Practitioner · gender` | 2 | male · female |
| `Practitioner · identifier.type.coding.code` | 1 | LANR |
| `Practitioner · identifier.type.coding.display` | 1 | Lifelong physician number |
| `Practitioner · identifier.value` | 1 | 987654321 |
| `Practitioner · qualification.code.coding.code` | 2 | 171001 · 141111 |
| `Practitioner · qualification.code.coding.display` | 2 | FA Laboratoriumsmedizin · FA Innere Medizin und Endokrinologie und Diabetologie |
| `PractitionerRole · code.coding.code` | 1 | AG |
| `PractitionerRole · code.coding.display` | 1 | Ärztliche Geschäftsführung |
| `Provenance · activity.coding.code` | 1 | VRF |
| `Provenance · activity.coding.display` | 1 | verifier |
| `Provenance · occurredDateTime` | 1 | 15.11.2021 16:55 |
| `Provenance · recorded` | 1 | 15.11.2021 16:55 |

## FHIR-Validierung (HL7 Validator 7.0.1)

Stand: `berichte/laborbefund.validierung.json`, geschrieben von `python3 -I werkzeuge/mx.py validieren laborbefund`; FHIR 4.0.1, Optionen `-tx n/a -locale en-US -allow-example-urls true -extension https://example.org/` (ohne Terminologieserver).

- Pakete: `hl7.fhir.uv.extensions.r4#5.3.0`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.eu.base#2.0.1`, `de.gematik.ti#1.5.0-ballot.2`, `de.gematik.epa.laboratory#1.0.0-ballot.1`, `de.gematik.terminology#1.1.0-ballot.2`, `kbv.mio.laborbefund#1.0.0-update`
- Lädt der Validator selbst (im Paketbestand festgelegt, ohne Netz): `hl7.fhir.r4.core#4.0.1`, `hl7.fhir.xver-extensions#0.1.0`, `hl7.terminology.r4#6.2.0`, `hl7.fhir.uv.extensions.r4#5.2.0`, `hl7.terminology#7.5.0`, `hl7.fhir.uv.extensions#5.3.0`
- Abhängigkeiten mit Platzhalter, festgelegt: `ihe.formatcode.fhir#1.5.x` → `1.5.0`
- Ergebnis: **0 Fehler**, 12 als begründete Ausnahme, 252 Warnungen, 63 Hinweise

| Beispiel | Fehler | davon begründete Ausnahme | Warnungen | Hinweise | Stand |
|---|---:|---:|---:|---:|---|
| Nierenfunktion und HbA1c — Hoffmann, 12.08.2026 | 4 | 4 | 29 | 13 | aktuell |
| Vorbefund — Hoffmann, 18.03.2026 | 4 | 4 | 25 | 12 | aktuell |
| Schilddrüse (TSH) — Yildiz, 02.07.2026 | 4 | 4 | 16 | 11 | aktuell |
| IG-Beispiel mit Probe, Gerät und Anhang | – | – | – | – | nicht validiert (Beispiel aus einem FHIR-Paket) |
| IG-Beispiel, zweite Composition | – | – | – | – | nicht validiert (Beispiel aus einem FHIR-Paket) |
| Fallbeispiel 1 nach MIO Laborbefund — Hansen, 15.11.2021 | 0 | 0 | 182 | 27 | aktuell |

**Begründete Ausnahmen** (`[[validierung.ausnahmen]]` in `projekt.toml`):

- `dr-comp-identifier` — 3 Treffer: Profilkonflikt im Ballot: Bundle-eu-lab verlangt eine DiagnosticReport-Kennung gleich Composition.identifier; composition-dglp verbietet identifier.type, diagnostic-report-dglp verlangt ihn bei geschlossenem Slicing — mit keiner Instanz erfüllbar.
- `abschnitt-ohne-terminologieserver` — 9 Treffer: Ohne Terminologieserver nicht auswertbar: composition-dglp ordnet den Abschnitt über eine required-Bindung an lab-studyType-eu-lab (LOINC) zu; der Validator verneint die Zugehörigkeit ohne Server. Dazu Folgefehler am Verweis auf die Composition.

### Fehler und Warnungen — Nierenfunktion und HbA1c — Hoffmann, 12.08.2026

Gleiche Meldungen zusammengefasst; Ort als FHIRPath, Zeile in der Beispieldatei.

- **error**: Constraint failed: dr-comp-identifier: 'If one or more DiagnosticReport.identifiers are given, at least one of them SHALL be equal to the Composition.identifier' (defined in http://hl7.eu/fhir/laboratory/StructureDefinition/Bundle-eu-lab) — begründete Ausnahme `dr-comp-identifier`<br>`Bundle` (Zeile 1)
- **error**: Slice 'Composition.section:result': a matching slice is required, but not found (from https://gematik.de/fhir/epa-laboratory/StructureDefinition/composition-dglp\|1.0.0). Note that other slices are allowed in addition to this required slice — begründete Ausnahme `abschnitt-ohne-terminologieserver`<br>`Bundle.entry[0].resource/*Composition/comp-f81d4fae*/` (Zeile 18)
- **error**: Unable to find a profile match for Composition/comp-f81d4fae among choices: http://hl7.org/fhir/5.0/StructureDefinition/profile-Composition\|0.1.0, http://hl7.org/fhir/StructureDefinition/Composition\|4.0.1 — begründete Ausnahme `abschnitt-ohne-terminologieserver`<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-f81d4fae*/.extension[0].value.ofType(Reference)` (Zeile 138)
- **error**: Unable to find a profile match for Composition/comp-f81d4fae among choices: https://gematik.de/fhir/epa-laboratory/StructureDefinition/composition-dglp — begründete Ausnahme `abschnitt-ohne-terminologieserver`<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-f81d4fae*/.extension[0].value.ofType(Reference)` (Zeile 138)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.eu/fhir/laboratory/StructureDefinition/Specimen-eu-lab) (Best Practice Recommendation)<br>`Bundle.entry[8].resource/*Specimen/sp-f81d4fae*/` (Zeile 364)
- **warning** (5×): Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/DomainResource) (Best Practice Recommendation)<br>`Bundle.entry[0].resource/*Composition/comp-f81d4fae*/` (Zeile 18), `Bundle.entry[1].resource/*DiagnosticReport/dr-f81d4fae*/` (Zeile 127), `Bundle.entry[2].resource/*Patient/pat-A123456780*/` (Zeile 249) und 2 weitere
- **warning** (2×): Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/Observation) (Best Practice Recommendation)<br>`Bundle.entry[12].resource/*Observation/obs-f81d4fae-0-0*/` (Zeile 640), `Bundle.entry[14].resource/*Observation/obs-f81d4fae-1-0*/` (Zeile 837)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/Organization) (Best Practice Recommendation)<br>`Bundle.entry[4].resource/*Organization/org-f81d4fae*/` (Zeile 321)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/Practitioner) (Best Practice Recommendation)<br>`Bundle.entry[6].resource/*Practitioner/prac-f81d4fae*/` (Zeile 337)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/PractitionerRole) (Best Practice Recommendation)<br>`Bundle.entry[7].resource/*PractitionerRole/role-f81d4fae*/` (Zeile 349)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = http://terminology.hl7.org/CodeSystem/v2-0203#RI)<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-f81d4fae*/.identifier[1].type` (Zeile 159)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = https://gematik.de/fhir/terminology/CodeSystem/laboratory-identificator#AE)<br>`Bundle.entry[3].resource/*ServiceRequest/sr-f81d4fae*/.identifier[0].type` (Zeile 281)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = https://gematik.de/fhir/terminology/CodeSystem/laboratory-identificator#AL)<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-f81d4fae*/.identifier[0].type` (Zeile 145)
- **warning** (3×): UCUM Codes that contain human readable annotations like {1.73_m2} can be misleading (e.g. they are ignored when comparing units). Best Practice is not to depend on annotations in the UCUM code, so this usage should be checked, and the Quantity.unit 'ml/min/1,73 m²' SHOULD contain the annotation (it does not)<br>`Bundle.entry[13].resource/*Observation/obs-f81d4fae-0-1*/.referenceRange[0].high` (Zeile 805), `Bundle.entry[13].resource/*Observation/obs-f81d4fae-0-1*/.referenceRange[0].low` (Zeile 799), `Bundle.entry[13].resource/*Observation/obs-f81d4fae-0-1*/.value.ofType(Quantity)` (Zeile 780)
- **warning** (3×): Unable to validate code '%' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[15].resource/*Observation/obs-f81d4fae-2-0*/.referenceRange[0].high` (Zeile 1009), `Bundle.entry[15].resource/*Observation/obs-f81d4fae-2-0*/.referenceRange[0].low` (Zeile 996), `Bundle.entry[15].resource/*Observation/obs-f81d4fae-2-0*/.value.ofType(Quantity)` (Zeile 977)
- **warning** (3×): Unable to validate code 'mL/min/{1.73_m2}' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[13].resource/*Observation/obs-f81d4fae-0-1*/.referenceRange[0].high` (Zeile 805), `Bundle.entry[13].resource/*Observation/obs-f81d4fae-0-1*/.referenceRange[0].low` (Zeile 799), `Bundle.entry[13].resource/*Observation/obs-f81d4fae-0-1*/.value.ofType(Quantity)` (Zeile 780)
- **warning** (3×): Unable to validate code 'mg/dL' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[12].resource/*Observation/obs-f81d4fae-0-0*/.referenceRange[0].high` (Zeile 710), `Bundle.entry[12].resource/*Observation/obs-f81d4fae-0-0*/.referenceRange[0].low` (Zeile 704), `Bundle.entry[12].resource/*Observation/obs-f81d4fae-0-0*/.value.ofType(Quantity)` (Zeile 685)
- **warning** (3×): Unable to validate code 'mmol/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[14].resource/*Observation/obs-f81d4fae-1-0*/.referenceRange[0].high` (Zeile 907), `Bundle.entry[14].resource/*Observation/obs-f81d4fae-1-0*/.referenceRange[0].low` (Zeile 901), `Bundle.entry[14].resource/*Observation/obs-f81d4fae-1-0*/.value.ofType(Quantity)` (Zeile 882)

### Fehler und Warnungen — Vorbefund — Hoffmann, 18.03.2026

Gleiche Meldungen zusammengefasst; Ort als FHIRPath, Zeile in der Beispieldatei.

- **error**: Constraint failed: dr-comp-identifier: 'If one or more DiagnosticReport.identifiers are given, at least one of them SHALL be equal to the Composition.identifier' (defined in http://hl7.eu/fhir/laboratory/StructureDefinition/Bundle-eu-lab) — begründete Ausnahme `dr-comp-identifier`<br>`Bundle` (Zeile 1)
- **error**: Slice 'Composition.section:result': a matching slice is required, but not found (from https://gematik.de/fhir/epa-laboratory/StructureDefinition/composition-dglp\|1.0.0). Note that other slices are allowed in addition to this required slice — begründete Ausnahme `abschnitt-ohne-terminologieserver`<br>`Bundle.entry[0].resource/*Composition/comp-9a3e6c10*/` (Zeile 18)
- **error**: Unable to find a profile match for Composition/comp-9a3e6c10 among choices: http://hl7.org/fhir/5.0/StructureDefinition/profile-Composition\|0.1.0, http://hl7.org/fhir/StructureDefinition/Composition\|4.0.1 — begründete Ausnahme `abschnitt-ohne-terminologieserver`<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-9a3e6c10*/.extension[0].value.ofType(Reference)` (Zeile 135)
- **error**: Unable to find a profile match for Composition/comp-9a3e6c10 among choices: https://gematik.de/fhir/epa-laboratory/StructureDefinition/composition-dglp — begründete Ausnahme `abschnitt-ohne-terminologieserver`<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-9a3e6c10*/.extension[0].value.ofType(Reference)` (Zeile 135)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.eu/fhir/laboratory/StructureDefinition/Specimen-eu-lab) (Best Practice Recommendation)<br>`Bundle.entry[8].resource/*Specimen/sp-9a3e6c10*/` (Zeile 352)
- **warning** (5×): Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/DomainResource) (Best Practice Recommendation)<br>`Bundle.entry[0].resource/*Composition/comp-9a3e6c10*/` (Zeile 18), `Bundle.entry[1].resource/*DiagnosticReport/dr-9a3e6c10*/` (Zeile 124), `Bundle.entry[2].resource/*Patient/pat-A123456780*/` (Zeile 237) und 2 weitere
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/Observation) (Best Practice Recommendation)<br>`Bundle.entry[11].resource/*Observation/obs-9a3e6c10-0-0*/` (Zeile 556)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/Organization) (Best Practice Recommendation)<br>`Bundle.entry[4].resource/*Organization/org-9a3e6c10*/` (Zeile 309)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/Practitioner) (Best Practice Recommendation)<br>`Bundle.entry[6].resource/*Practitioner/prac-9a3e6c10*/` (Zeile 325)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/PractitionerRole) (Best Practice Recommendation)<br>`Bundle.entry[7].resource/*PractitionerRole/role-9a3e6c10*/` (Zeile 337)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = http://terminology.hl7.org/CodeSystem/v2-0203#RI)<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-9a3e6c10*/.identifier[1].type` (Zeile 156)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = https://gematik.de/fhir/terminology/CodeSystem/laboratory-identificator#AE)<br>`Bundle.entry[3].resource/*ServiceRequest/sr-9a3e6c10*/.identifier[0].type` (Zeile 269)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = https://gematik.de/fhir/terminology/CodeSystem/laboratory-identificator#AL)<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-9a3e6c10*/.identifier[0].type` (Zeile 142)
- **warning** (3×): UCUM Codes that contain human readable annotations like {1.73_m2} can be misleading (e.g. they are ignored when comparing units). Best Practice is not to depend on annotations in the UCUM code, so this usage should be checked, and the Quantity.unit 'ml/min/1,73 m²' SHOULD contain the annotation (it does not)<br>`Bundle.entry[12].resource/*Observation/obs-9a3e6c10-0-1*/.referenceRange[0].high` (Zeile 721), `Bundle.entry[12].resource/*Observation/obs-9a3e6c10-0-1*/.referenceRange[0].low` (Zeile 715), `Bundle.entry[12].resource/*Observation/obs-9a3e6c10-0-1*/.value.ofType(Quantity)` (Zeile 696)
- **warning** (3×): Unable to validate code '%' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[13].resource/*Observation/obs-9a3e6c10-1-0*/.referenceRange[0].high` (Zeile 830), `Bundle.entry[13].resource/*Observation/obs-9a3e6c10-1-0*/.referenceRange[0].low` (Zeile 817), `Bundle.entry[13].resource/*Observation/obs-9a3e6c10-1-0*/.value.ofType(Quantity)` (Zeile 798)
- **warning** (3×): Unable to validate code 'mL/min/{1.73_m2}' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[12].resource/*Observation/obs-9a3e6c10-0-1*/.referenceRange[0].high` (Zeile 721), `Bundle.entry[12].resource/*Observation/obs-9a3e6c10-0-1*/.referenceRange[0].low` (Zeile 715), `Bundle.entry[12].resource/*Observation/obs-9a3e6c10-0-1*/.value.ofType(Quantity)` (Zeile 696)
- **warning** (3×): Unable to validate code 'mg/dL' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[11].resource/*Observation/obs-9a3e6c10-0-0*/.referenceRange[0].high` (Zeile 626), `Bundle.entry[11].resource/*Observation/obs-9a3e6c10-0-0*/.referenceRange[0].low` (Zeile 620), `Bundle.entry[11].resource/*Observation/obs-9a3e6c10-0-0*/.value.ofType(Quantity)` (Zeile 601)

### Fehler und Warnungen — Schilddrüse (TSH) — Yildiz, 02.07.2026

Gleiche Meldungen zusammengefasst; Ort als FHIRPath, Zeile in der Beispieldatei.

- **error**: Constraint failed: dr-comp-identifier: 'If one or more DiagnosticReport.identifiers are given, at least one of them SHALL be equal to the Composition.identifier' (defined in http://hl7.eu/fhir/laboratory/StructureDefinition/Bundle-eu-lab) — begründete Ausnahme `dr-comp-identifier`<br>`Bundle` (Zeile 1)
- **error**: Slice 'Composition.section:result': a matching slice is required, but not found (from https://gematik.de/fhir/epa-laboratory/StructureDefinition/composition-dglp\|1.0.0). Note that other slices are allowed in addition to this required slice — begründete Ausnahme `abschnitt-ohne-terminologieserver`<br>`Bundle.entry[0].resource/*Composition/comp-3b1c9a52*/` (Zeile 18)
- **error**: Unable to find a profile match for Composition/comp-3b1c9a52 among choices: http://hl7.org/fhir/5.0/StructureDefinition/profile-Composition\|0.1.0, http://hl7.org/fhir/StructureDefinition/Composition\|4.0.1 — begründete Ausnahme `abschnitt-ohne-terminologieserver`<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-3b1c9a52*/.extension[0].value.ofType(Reference)` (Zeile 132)
- **error**: Unable to find a profile match for Composition/comp-3b1c9a52 among choices: https://gematik.de/fhir/epa-laboratory/StructureDefinition/composition-dglp — begründete Ausnahme `abschnitt-ohne-terminologieserver`<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-3b1c9a52*/.extension[0].value.ofType(Reference)` (Zeile 132)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.eu/fhir/laboratory/StructureDefinition/Specimen-eu-lab) (Best Practice Recommendation)<br>`Bundle.entry[8].resource/*Specimen/sp-3b1c9a52*/` (Zeile 339)
- **warning** (5×): Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/DomainResource) (Best Practice Recommendation)<br>`Bundle.entry[0].resource/*Composition/comp-3b1c9a52*/` (Zeile 18), `Bundle.entry[1].resource/*DiagnosticReport/dr-3b1c9a52*/` (Zeile 121), `Bundle.entry[2].resource/*Patient/pat-M555123402*/` (Zeile 224) und 2 weitere
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/Observation) (Best Practice Recommendation)<br>`Bundle.entry[10].resource/*Observation/obs-3b1c9a52-0-0*/` (Zeile 462)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/Organization) (Best Practice Recommendation)<br>`Bundle.entry[4].resource/*Organization/org-3b1c9a52*/` (Zeile 296)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/Practitioner) (Best Practice Recommendation)<br>`Bundle.entry[6].resource/*Practitioner/prac-3b1c9a52*/` (Zeile 312)
- **warning**: Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/PractitionerRole) (Best Practice Recommendation)<br>`Bundle.entry[7].resource/*PractitionerRole/role-3b1c9a52*/` (Zeile 324)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = http://terminology.hl7.org/CodeSystem/v2-0203#RI)<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-3b1c9a52*/.identifier[1].type` (Zeile 153)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = https://gematik.de/fhir/terminology/CodeSystem/laboratory-identificator#AE)<br>`Bundle.entry[3].resource/*ServiceRequest/sr-3b1c9a52*/.identifier[0].type` (Zeile 256)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = https://gematik.de/fhir/terminology/CodeSystem/laboratory-identificator#AL)<br>`Bundle.entry[1].resource/*DiagnosticReport/dr-3b1c9a52*/.identifier[0].type` (Zeile 139)
- **warning** (3×): Unable to validate code 'm[IU]/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[10].resource/*Observation/obs-3b1c9a52-0-0*/.referenceRange[0].high` (Zeile 532), `Bundle.entry[10].resource/*Observation/obs-3b1c9a52-0-0*/.referenceRange[0].low` (Zeile 526), `Bundle.entry[10].resource/*Observation/obs-3b1c9a52-0-0*/.value.ofType(Quantity)` (Zeile 507)

### Fehler und Warnungen — Fallbeispiel 1 nach MIO Laborbefund — Hansen, 15.11.2021

Gleiche Meldungen zusammengefasst; Ort als FHIRPath, Zeile in der Beispieldatei.

- **warning** (2×): A definition for CodeSystem 'urn:ietf:bcp:13' could not be found, so the code cannot be validated<br>`Bundle.entry[1].resource/*DiagnosticReport/DiagnosticReport-ex1-1*/.presentedForm[0].contentType` (Zeile 218), `Bundle.entry[1].resource/*DiagnosticReport/DiagnosticReport-ex1-1*/.presentedForm[0].contentType.system` (Zeile 218)
- **warning** (39×): Constraint failed: dom-6: 'A resource should have narrative for robust management' (defined in http://hl7.org/fhir/StructureDefinition/DomainResource) (Best Practice Recommendation)<br>`Bundle.entry[0].resource/*Composition/Composition-ex1-1*/` (Zeile 16), `Bundle.entry[10].resource/*Observation/Observation-ex1-gfr*/` (Zeile 1234), `Bundle.entry[11].resource/*Observation/Observation-ex1-harnstoff*/` (Zeile 1360) und 36 weitere
- **warning**: Found multiple matching profiles for Composition/Composition-ex1-1 among choices: http://hl7.org/fhir/5.0/StructureDefinition/profile-Composition\|0.1.0, http://hl7.org/fhir/StructureDefinition/Composition\|4.0.1<br>`Bundle.entry[1].resource/*DiagnosticReport/DiagnosticReport-ex1-1*/.extension[1].value.ofType(Reference)` (Zeile 114)
- **warning** (2×): No code provided, and a code should be provided from the value set 'Observation Interpretation Codes' (http://hl7.org/fhir/ValueSet/observation-interpretation\|4.0.1)<br>`Bundle.entry[16].resource/*Observation/Observation-ex1-group-vitamin*/.interpretation[0]` (Zeile 2080), `Bundle.entry[18].resource/*Observation/Observation-ex1-group-endokrin*/.interpretation[0]` (Zeile 2307)
- **warning**: None of the codings provided are in the value set 'Identifier Type DeBasis ValueSet' (http://fhir.de/ValueSet/identifier-type-de-basis\|1.5.4), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = http://terminology.hl7.org/CodeSystem/v2-0203#BSNR)<br>`Bundle.entry[38].resource/*Organization/Organization-ex1-1*/.identifier[0].type` (Zeile 4857)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = http://terminology.hl7.org/CodeSystem/v2-0203#BSNR)<br>`Bundle.entry[38].resource/*Organization/Organization-ex1-1*/.identifier[0].type` (Zeile 4857)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = http://terminology.hl7.org/CodeSystem/v2-0203#RI)<br>`Bundle.entry[1].resource/*DiagnosticReport/DiagnosticReport-ex1-1*/.identifier[0].type` (Zeile 121)
- **warning**: None of the codings provided are in the value set 'IdentifierType' (http://hl7.org/fhir/ValueSet/identifier-type\|4.0.1), and a coding should come from this value set unless it has no suitable code (note that the validator cannot judge what is suitable) (codes = https://fhir.kbv.de/CodeSystem/KBV_CS_MIO_LAB_Laboratory_Identificator#AE)<br>`Bundle.entry[37].resource/*ServiceRequest/ServiceRequest-ex1-1*/.identifier[0].type` (Zeile 4780)
- **warning** (28×): The code system 'http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation' version '4.0.0' for the versionless include in the ValueSet include is different to the one in the value ('4.0.1')<br>`Bundle.entry[10].resource/*Observation/Observation-ex1-gfr*/.interpretation[0].coding[0].version` (Zeile 1310), `Bundle.entry[11].resource/*Observation/Observation-ex1-harnstoff*/.interpretation[0].coding[0].version` (Zeile 1436), `Bundle.entry[12].resource/*Observation/Observation-ex1-natrium*/.interpretation[0].coding[0].version` (Zeile 1565) und 25 weitere
- **warning**: The code system 'http://terminology.hl7.org/CodeSystem/v3-ParticipationType' version '7.0.0' for the versionless include in the ValueSet include is different to the one in the value ('6.0.0')<br>`Bundle.entry[42].resource/*Provenance/Provenance-ex1-1*/.activity.coding[0].version` (Zeile 5200)
- **warning** (2×): UCUM Codes that contain human readable annotations like {1.73_m2} can be misleading (e.g. they are ignored when comparing units). Best Practice is not to depend on annotations in the UCUM code, so this usage should be checked, and the Quantity.unit 'ml/min/1,73m2' SHOULD contain the annotation (it does not)<br>`Bundle.entry[10].resource/*Observation/Observation-ex1-gfr*/.referenceRange[0].low` (Zeile 1336), `Bundle.entry[10].resource/*Observation/Observation-ex1-gfr*/.value.ofType(Quantity)` (Zeile 1344)
- **warning** (3×): Unable to validate code '%' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[30].resource/*Observation/Observation-ex1-haematokrit*/.referenceRange[0].high` (Zeile 4064), `Bundle.entry[30].resource/*Observation/Observation-ex1-haematokrit*/.referenceRange[0].low` (Zeile 4058), `Bundle.entry[30].resource/*Observation/Observation-ex1-haematokrit*/.value.ofType(Quantity)` (Zeile 4072)
- **warning** (3×): Unable to validate code '1' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[24].resource/*Observation/Observation-ex1-fai*/.referenceRange[0].high` (Zeile 3173), `Bundle.entry[24].resource/*Observation/Observation-ex1-fai*/.referenceRange[0].low` (Zeile 3167), `Bundle.entry[24].resource/*Observation/Observation-ex1-fai*/.value.ofType(Quantity)` (Zeile 3181)
- **warning** (3×): Unable to validate code '10*12/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[28].resource/*Observation/Observation-ex1-erythrozyten*/.referenceRange[0].high` (Zeile 3772), `Bundle.entry[28].resource/*Observation/Observation-ex1-erythrozyten*/.referenceRange[0].low` (Zeile 3766), `Bundle.entry[28].resource/*Observation/Observation-ex1-erythrozyten*/.value.ofType(Quantity)` (Zeile 3780)
- **warning** (6×): Unable to validate code '10*9/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[27].resource/*Observation/Observation-ex1-leukozyten*/.referenceRange[0].high` (Zeile 3626), `Bundle.entry[27].resource/*Observation/Observation-ex1-leukozyten*/.referenceRange[0].low` (Zeile 3620), `Bundle.entry[27].resource/*Observation/Observation-ex1-leukozyten*/.value.ofType(Quantity)` (Zeile 3634) und 3 weitere
- **warning** (13×): Unable to validate code '18719-5' in system 'http://loinc.org' because the validator is running without terminology services<br>`Bundle.entry[10].resource/*Observation/Observation-ex1-gfr*/.category[1].coding[0]` (Zeile 1267), `Bundle.entry[11].resource/*Observation/Observation-ex1-harnstoff*/.category[1].coding[0]` (Zeile 1393), `Bundle.entry[12].resource/*Observation/Observation-ex1-natrium*/.category[1].coding[0]` (Zeile 1522) und 10 weitere
- **warning** (9×): Unable to validate code '18723-7' in system 'http://loinc.org' because the validator is running without terminology services<br>`Bundle.entry[26].resource/*Observation/Observation-ex1-group-blutbild*/.category[1].coding[0]` (Zeile 3359), `Bundle.entry[27].resource/*Observation/Observation-ex1-leukozyten*/.category[1].coding[0]` (Zeile 3537), `Bundle.entry[28].resource/*Observation/Observation-ex1-erythrozyten*/.category[1].coding[0]` (Zeile 3683) und 6 weitere
- **warning** (9×): Unable to validate code 'U/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[5].resource/*Observation/Observation-ex1-alat*/.referenceRange[0].high` (Zeile 709), `Bundle.entry[5].resource/*Observation/Observation-ex1-alat*/.value.ofType(Quantity)` (Zeile 717), `Bundle.entry[6].resource/*Observation/Observation-ex1-asat*/.referenceRange[0].high` (Zeile 832) und 6 weitere
- **warning** (6×): Unable to validate code '[iU]/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[19].resource/*Observation/Observation-ex1-fsh*/.referenceRange[0].high` (Zeile 2494), `Bundle.entry[19].resource/*Observation/Observation-ex1-fsh*/.referenceRange[0].low` (Zeile 2488), `Bundle.entry[19].resource/*Observation/Observation-ex1-fsh*/.value.ofType(Quantity)` (Zeile 2502) und 3 weitere
- **warning** (3×): Unable to validate code 'fL' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[31].resource/*Observation/Observation-ex1-mcv*/.referenceRange[0].high` (Zeile 4210), `Bundle.entry[31].resource/*Observation/Observation-ex1-mcv*/.referenceRange[0].low` (Zeile 4204), `Bundle.entry[31].resource/*Observation/Observation-ex1-mcv*/.value.ofType(Quantity)` (Zeile 4218)
- **warning** (6×): Unable to validate code 'g/dL' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[29].resource/*Observation/Observation-ex1-haemoglobin*/.referenceRange[0].high` (Zeile 3918), `Bundle.entry[29].resource/*Observation/Observation-ex1-haemoglobin*/.referenceRange[0].low` (Zeile 3912), `Bundle.entry[29].resource/*Observation/Observation-ex1-haemoglobin*/.value.ofType(Quantity)` (Zeile 3926) und 3 weitere
- **warning** (2×): Unable to validate code 'mL/min/{1.73_m2}' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[10].resource/*Observation/Observation-ex1-gfr*/.referenceRange[0].low` (Zeile 1336), `Bundle.entry[10].resource/*Observation/Observation-ex1-gfr*/.value.ofType(Quantity)` (Zeile 1344)
- **warning** (3×): Unable to validate code 'm[iU]/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[22].resource/*Observation/Observation-ex1-prolaktin*/.referenceRange[0].high` (Zeile 2882), `Bundle.entry[22].resource/*Observation/Observation-ex1-prolaktin*/.referenceRange[0].low` (Zeile 2876), `Bundle.entry[22].resource/*Observation/Observation-ex1-prolaktin*/.value.ofType(Quantity)` (Zeile 2923)
- **warning** (8×): Unable to validate code 'mg/dL' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[11].resource/*Observation/Observation-ex1-harnstoff*/.referenceRange[0].high` (Zeile 1465), `Bundle.entry[11].resource/*Observation/Observation-ex1-harnstoff*/.referenceRange[0].low` (Zeile 1459), `Bundle.entry[11].resource/*Observation/Observation-ex1-harnstoff*/.value.ofType(Quantity)` (Zeile 1473) und 5 weitere
- **warning** (12×): Unable to validate code 'mmol/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[12].resource/*Observation/Observation-ex1-natrium*/.referenceRange[0].high` (Zeile 1594), `Bundle.entry[12].resource/*Observation/Observation-ex1-natrium*/.referenceRange[0].low` (Zeile 1588), `Bundle.entry[12].resource/*Observation/Observation-ex1-natrium*/.value.ofType(Quantity)` (Zeile 1602) und 9 weitere
- **warning** (3×): Unable to validate code 'ng/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[21].resource/*Observation/Observation-ex1-estradiol*/.referenceRange[0].high` (Zeile 2753), `Bundle.entry[21].resource/*Observation/Observation-ex1-estradiol*/.referenceRange[0].low` (Zeile 2747), `Bundle.entry[21].resource/*Observation/Observation-ex1-estradiol*/.value.ofType(Quantity)` (Zeile 2761)
- **warning** (3×): Unable to validate code 'ng/mL' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[22].resource/*Observation/Observation-ex1-prolaktin*/.extension[0].extension[0].value.ofType(Quantity)` (Zeile 2895), `Bundle.entry[22].resource/*Observation/Observation-ex1-prolaktin*/.extension[0].extension[1].value.ofType(Range).high` (Zeile 2910), `Bundle.entry[22].resource/*Observation/Observation-ex1-prolaktin*/.extension[0].extension[1].value.ofType(Range).low` (Zeile 2904)
- **warning** (5×): Unable to validate code 'nmol/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[17].resource/*Observation/Observation-ex1-vitamin-d*/.referenceRange[0].low` (Zeile 2207), `Bundle.entry[17].resource/*Observation/Observation-ex1-vitamin-d*/.value.ofType(Quantity)` (Zeile 2216), `Bundle.entry[25].resource/*Observation/Observation-ex1-shbg*/.referenceRange[0].high` (Zeile 3302) und 2 weitere
- **warning** (3×): Unable to validate code 'pg' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[32].resource/*Observation/Observation-ex1-mch*/.referenceRange[0].high` (Zeile 4356), `Bundle.entry[32].resource/*Observation/Observation-ex1-mch*/.referenceRange[0].low` (Zeile 4350), `Bundle.entry[32].resource/*Observation/Observation-ex1-mch*/.value.ofType(Quantity)` (Zeile 4364)
- **warning** (3×): Unable to validate code 'ug/L' in system 'http://unitsofmeasure.org' because the validator is running without terminology services<br>`Bundle.entry[23].resource/*Observation/Observation-ex1-testosteron*/.referenceRange[0].high` (Zeile 3044), `Bundle.entry[23].resource/*Observation/Observation-ex1-testosteron*/.referenceRange[0].low` (Zeile 3038), `Bundle.entry[23].resource/*Observation/Observation-ex1-testosteron*/.value.ofType(Quantity)` (Zeile 3052)
