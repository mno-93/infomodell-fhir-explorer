# Prüfbericht — ePA Patient Summary (CI-Build ePS-0.0.1)

> Erzeugt von `python3 werkzeuge/mx.py bauen`. Nicht von Hand ändern; die CI prüft, dass der Bericht zum Stand passt.

> ![KI-gestützt erstellt](../web/ki-hinweis.svg) **Hinweis zur KI-Nutzung:** Dieser Modellexplorer – Programmcode, Projektkonfiguration und Texte – ist mit Unterstützung eines KI-Assistenten (Claude von Anthropic) entstanden. Die Darstellungen sind aus veröffentlichten Spezifikationen abgeleitet und keine Primärquelle; sie können Fehler enthalten. Maßgeblich sind die verlinkten Implementierungsleitfäden und FHIR-Pakete. Alle Beispieldaten sind fiktiv.

## Quellen

- Implementation Guide: MIO ePA Patient Summary (CI-Build) (`ePS-0.0.1 (kein Paket in der Registry)`, in Arbeit (CI-Build))
- Darstellung des Modells: Informationsmodell — Das Modell enthält keine FHIR-Mappings, aber je Element das EHDS-Mapping auf die Xt-EHR-Logikmodelle; geprüft wird deshalb dieses Mapping. Keine Beispiele: Die beiden Patient-Summary-Beispiele des Projekts patient-summary folgen den EPS- und gematik-Profilen, nicht diesem Modell. Ohne FHIR-Mappings bliebe die Kette Modell → Profil → Instanz leer; verbunden wären sie nur über einige allgemeine Codes (Hoffmann 11 von 74 Codes, Yildiz 5 von 41, z. B. Status und Diagnosesicherheit) — das wäre eine scheinbare, keine fachliche Verknüpfung.
- Pakete: `hl7.fhir.eu.base#2.0.1`, `hl7.fhir.uv.ips#2.0.1`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.r4.core#4.0.1`
- Logikmodelle für das EHDS-Mapping: `xtehr.eu.ehds.models#1.0.0`

## Mappingprüfung

481 Elemente im Informationsmodell. Das Modell enthält keine FHIR-Mappings; geprüft wird das EHDS-Mapping (unten).

## Wertelisten

45 Wertelisten im Modell, davon 26 im Paketbestand oder über eine Profilbindung aufgelöst, 26 mit Link auf die Originalseite.

Nicht auflösbar (weder im Paketbestand noch in einer Profilbindung):

- `BodystructureBodyLandmarkClockFacePosition`
- `ConditionDiagnosisSeverity`
- `Condition_Problem_DiagnosisCodes`
- `KBV_MIO_VS_AusloesendeSubstanzen`
- `KBV_MIO_VS_Manifestation`
- `KBV_VS_Base_Allergy_Substance_SNOMED_CT`
- `KBV_VS_Base_Device_SNOMED_CT`
- `KBV_VS_Base_Diagnosis_SNOMED_CT`
- `KBV_VS_Base_Localisation_Body_Structure_SNOMED_CT`
- `KBV_VS_Base_Procedure_Categories_SNOMED_CT`
- `KBV_VS_Base_Procedure_SNOMED_CT`
- `KBV_VS_Base_Route_of_Administration_SNOMED_CT`
- `KBV_VS_Base_Stage_Life`
- `KBV_VS_MIO_ListEmptyReasons_reduced`
- `KBV_VS_MIO_PS_Health_care_proxy_Type`
- `MehrfachkodierungsKennzeichen`
- `ProcedureNotPerformedReason_SNOMED_CT`
- `ProcedureOutcomeCodesSNOMEDCT`
- `http://snomed.info/sct`

## Ausmodellierte Darstellung

1982 Knoten · 240 Referenzen an der Verwendungsstelle aufgelöst · 1 Zyklen erkannt · 0 Knoten aus FHIR-Profilen ergänzt

## EHDS-Mappingprüfung

129 Verweise an 125 Elementen, aufgelöst gegen `xtehr.eu.ehds.models#1.0.0` (82 Logikmodelle).

| Auflösung | Anzahl |
|---|---:|
| auflösbar: Element im Logikmodell | 92 |
| nur Modell ohne Element | 31 |
| **Element fehlt im Modell** | 2 |
| **Modell nicht im Paketbestand** | 0 |
| ausdrücklich ohne Gegenstück („im EHDS Logical Model nicht vorhanden“) | 4 |

| Linkformat | Anzahl |
|---|---:|
| Link auf die Seite des Modells mit Version (`…/models/1.0.0/en/…`) | 38 |
| **uneinheitlich: Link ohne Version** (`…/models/en/…`, jeweils aktueller Stand) | 50 |
| kanonische URL des Modells (`http://www.xt-ehr.eu/fhir/models/StructureDefinition/…`) | 29 |
| **Linkziel nur der Pfad**, keine URL | 2 |
| **Klartext ohne Link** | 4 |
| **Link auf eine andere Seite** als das Logikmodell | 2 |

Kontext: **2** Verweise auf das Modell eines anderen Bausteins (Modell weder das des übergeordneten Elements noch dort als Typ genannt).

### Nicht auflösbar (2)

| Element im Modell | EHDS-Verweis | Befund |
|---|---|---|
| Zeitpunkt der Erstellung <br>*Allergie/Unverträglichkeit / Notiz* | `EHDSAllergyIntolerance.note.time` | `EHDSAllergyIntolerance.note.time` gibt es im Modell `EHDSAllergyIntolerance` nicht; Link führt auf `https://build.fhir.org/ig/hl7-eu/eps/StructureDefinition-allergyintolerance-obl-eu-eps-definitions.html#AllergyIntolerance.note.time`, nicht auf das Logikmodell |
| Text <br>*Allergie/Unverträglichkeit / Notiz* | `EHDSAllergyIntolerance.note.text` | `EHDSAllergyIntolerance.note.text` gibt es im Modell `EHDSAllergyIntolerance` nicht; Link führt auf `https://build.fhir.org/ig/hl7-eu/eps/StructureDefinition-allergyintolerance-obl-eu-eps-definitions.html#AllergyIntolerance.note.text`, nicht auf das Logikmodell |

### Modell eines anderen Bausteins (2)

| Element im Modell | EHDS-Verweis | Befund |
|---|---|---|
| Beteiligte Personen <br>*ePA ePS Profile (in Erarbeitung) / Allergie/Unverträglichkeit* | `EHDSCondition.header.author[x]` | Link ohne Version (`…/models/en/…`) — zeigt auf den jeweils aktuellen Stand; Modell eines anderen Bausteins: liegt unter „Allergie/Unverträglichkeit“ (EHDSAllergyIntolerance), zeigt aber auf `EHDSCondition` |
| Beteiligte Personen <br>*ePA ePS Profile (in Erarbeitung) / Allergie/Unverträglichkeit* | `EHDSCondition.specialistContact` | Link ohne Version (`…/models/en/…`) — zeigt auf den jeweils aktuellen Stand; Modell eines anderen Bausteins: liegt unter „Allergie/Unverträglichkeit“ (EHDSAllergyIntolerance), zeigt aber auf `EHDSCondition` |

### Klartext, Linkziel ohne URL, Link auf eine andere Seite (8)

| Element im Modell | EHDS-Verweis | Befund |
|---|---|---|
| Gewissheit - Code <br>*Gewissheit - Code/Bezeichnung / Code-Auswahl* | `EHDSAllergyIntolerance.certainty` | nur als Text, ohne Link; enthält ein unsichtbares Zeichen (U+200B) |
| Spezifische Substanz - Code/Bezeichnung <br>*Allergie/Unverträglichkeit / Reaktion* | `EHDSAllergyIntolerance.reaction.agentOrAllergen` | Linkziel ist nur der Pfad `EHDSAllergyIntolerance.reaction.agentOrAllergen`, keine URL |
| Zeitpunkt der Erstellung <br>*Allergie/Unverträglichkeit / Notiz* | `EHDSAllergyIntolerance.note.time` | `EHDSAllergyIntolerance.note.time` gibt es im Modell `EHDSAllergyIntolerance` nicht; Link führt auf `https://build.fhir.org/ig/hl7-eu/eps/StructureDefinition-allergyintolerance-obl-eu-eps-definitions.html#AllergyIntolerance.note.time`, nicht auf das Logikmodell |
| Text <br>*Allergie/Unverträglichkeit / Notiz* | `EHDSAllergyIntolerance.note.text` | `EHDSAllergyIntolerance.note.text` gibt es im Modell `EHDSAllergyIntolerance` nicht; Link führt auf `https://build.fhir.org/ig/hl7-eu/eps/StructureDefinition-allergyintolerance-obl-eu-eps-definitions.html#AllergyIntolerance.note.text`, nicht auf das Logikmodell |
| Referenz auf das Gerät <br>*ePA ePS Profile (in Erarbeitung) / Gerätenutzung* | `EHDSDeviceUse.deviceEHDSDevice` | Linkziel ist nur der Pfad `EHDSDeviceUse.device[x]`, keine URL |
| Warnung - Code/Bezeichnung <br>*ePA ePS Profile (in Erarbeitung) / Medizinische Warnung* | `EHDSAlert.code` | nur als Text, ohne Link |
| Referenz auf anderen Eintrag <br>*ePA ePS Profile (in Erarbeitung) / Medizinische Warnung* | `EHDSAlert.sourceReference` | nur als Text, ohne Link |
| Versorgungsplan-Eintrag <br>*Profile / ePA ePS Profile (Backlog)* | `EHDSCarePlan` | nur als Text, ohne Link |

### Link ohne Version (50)

| Element im Modell | EHDS-Verweis |
|---|---|
| Beteiligte Personen <br>*ePA ePS Profile (in Erarbeitung) / Allergie/Unverträglichkeit* | `EHDSCondition.header.author[x]` |
| Beteiligte Personen <br>*ePA ePS Profile (in Erarbeitung) / Allergie/Unverträglichkeit* | `EHDSCondition.specialistContact` |
| Geschätzter Entbindungstermin <br>*ePA ePS Profile (in Erarbeitung) / AMTS-rZI (weitere)* | `EHDSCurrentPregnancy.expectedDateOfDelivery` |
| Diagnose <br>*Profile / ePA ePS Profile (in Erarbeitung)* | `EHDSCondition` |
| Kategorie <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.category` |
| Codierung Code/Bezeichnung <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.problem` |
| Klinischer Status <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.header.status` |
| Klinisch relevanter Zeitraum <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.onsetDate` |
| Klinisch relevanter Zeitraum <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.endDate` |
| Diagnosesicherheit <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.diagnosisAssertionStatus` |
| Schweregrad - SNOMED CT®-Code <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.severity` |
| Körperstelle <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.bodySite` |
| Stadium <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.stage` |
| Dokumentationsdatum <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.header.date` |
| Beteiligte Personen <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.header.author[x]` |
| Beteiligte Personen <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.specialistContact` |
| Externe Referenzen <br>*ePA ePS Profile (in Erarbeitung) / Diagnose* | `EHDSCondition.externalResource` |
| Typ - Code/Bezeichnung <br>*ePA ePS Profile (in Erarbeitung) / Gerät* | `EHDSDevice.type` |
| Name des Gerätes <br>*ePA ePS Profile (in Erarbeitung) / Gerät* | `EHDSDevice.name` |
| UDI <br>*ePA ePS Profile (in Erarbeitung) / Gerät* | `EHDSDevice.udi` |
| Modellnummer <br>*Gerät / Produktnummern* | `EHDSDevice.modelNumber` |
| Seriennummer <br>*Gerät / Produktnummern* | `EHDSDevice.serialNumber` |
| Chargennummer <br>*Gerät / Produktnummern* | `EHDSDevice.lotNumber` |
| Hersteller <br>*ePA ePS Profile (in Erarbeitung) / Gerät* | `EHDSDevice.manufacturer` |
| Herstellungsdatum <br>*ePA ePS Profile (in Erarbeitung) / Gerät* | `EHDSDevice.manufactureDate` |
| Haltbarkeitsdatum <br>*ePA ePS Profile (in Erarbeitung) / Gerät* | `EHDSDevice.expiryDate` |
| Version <br>*ePA ePS Profile (in Erarbeitung) / Gerät* | `EHDSDevice.version` |
| Status <br>*ePA ePS Profile (in Erarbeitung) / Gerätenutzung* | `EHDSDeviceUse.header.status` |
| Nutzungszeitraum <br>*ePA ePS Profile (in Erarbeitung) / Gerätenutzung* | `EHDSDeviceUse.periodOfUse` |
| Körperstelle <br>*ePA ePS Profile (in Erarbeitung) / Gerätenutzung* | `EHDSDeviceUse.bodySite` |
| Grund der Nutzung <br>*ePA ePS Profile (in Erarbeitung) / Gerätenutzung* | `EHDSDeviceUse.reason[x]` |
| Status <br>*ePA ePS Profile (in Erarbeitung) / Impfung* | `EHDSImmunisation.header.status` |
| Zielerkrankung - Code/Bezeichnung <br>*ePA ePS Profile (in Erarbeitung) / Impfung* | `EHDSImmunisation.diseaseOrAgentTargeted` |
| Impfstoff - Code/Bezeichnung <br>*ePA ePS Profile (in Erarbeitung) / Impfung* | `EHDSImmunisation.vaccine` |
| Verabreichtes Produkt <br>*ePA ePS Profile (in Erarbeitung) / Impfung* | `EHDSImmunisation.administeredProduct` |
| Impfdatum <br>*ePA ePS Profile (in Erarbeitung) / Impfung* | `EHDSImmunisation.administrationTime` |
| Verantwortliche Einrichtung <br>*ePA ePS Profile (in Erarbeitung) / Impfung* | `EHDSImmunisation.administeringCentre` |
| Impfende Person/Einrichtung <br>*ePA ePS Profile (in Erarbeitung) / Impfung* | `EHDSImmunisation.administrator` |
| Notiz <br>*ePA ePS Profile (in Erarbeitung) / Impfung* | `EHDSImmunisation.note` |
| Status <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.header.status` |
| Prozedur - Code/Bezeichnung <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.code` |
| Durchführung: Zeitangabe-Auswahl <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.procedureDate[x]` |
| Dokumentationsdatum <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.header.date` |
| Durchführende Person/Einrichtung <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.performer` |
| Dokumentierende Person <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.header.author[x]` |
| Begründung <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.reason[x]` |
| Körperstelle <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.bodySite` |
| Outcome Code/Bezeichnung <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.outcome` |
| Komplikationen <br>*ePA ePS Profile (in Erarbeitung) / Prozedur* | `EHDSProcedure.complication` |
| Körperstelle <br>*Mehrfach verwendete Elemente* | `EHDSProcedure.bodySite` |

### Ausdrücklich ohne Gegenstück im EHDS-Modell (4)

- Typ *(ePA ePS Profile (in Erarbeitung) / Allergie/Unverträglichkeit)*
- Wirkstoffkategorie *(ePA ePS Profile (in Erarbeitung) / Allergie/Unverträglichkeit)*
- Zeitlicher Verlauf der Reaktion *(Allergie/Unverträglichkeit / Reaktion)*
- Expositionsweg - Code/Bezeichnung *(Allergie/Unverträglichkeit / Reaktion)*

## Beispiele

Keine Beispiele im Projekt — Begründung im Hinweis zum Modell (oben).

## FHIR-Validierung

Keine Beispiele — nichts zu validieren.
