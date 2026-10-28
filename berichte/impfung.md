# Prüfbericht — Impfung (Entwurf, EU-konform)

> Erzeugt von `python3 werkzeuge/mx.py bauen`. Nicht von Hand ändern; die CI prüft, dass der Bericht zum Stand passt.

> ![KI-gestützt erstellt](../web/ki-hinweis.svg) **Hinweis zur KI-Nutzung:** Dieser Modellexplorer – Programmcode, Projektkonfiguration und Texte – ist mit Unterstützung eines KI-Assistenten (Claude von Anthropic) entstanden. Die Darstellungen sind aus veröffentlichten Spezifikationen abgeleitet und keine Primärquelle; sie können Fehler enthalten. Maßgeblich sind die verlinkten Implementierungsleitfäden und FHIR-Pakete. Alle Beispieldaten sind fiktiv.

## Quellen

- Implementation Guide: Entwurf (nicht veröffentlicht) — Grundlagen: HL7 Europe Base 2.0.1, HL7 Europe Patient Summary 1.0.0-ballot (`example.impfung.entwurf#0.1.0`, Entwurf, nicht veröffentlicht)
- Darstellung des Modells: Informationsmodell — Teilbaum „Impfung“ aus dem Informationsmodell der ePA Patient Summary (CI-Build ePS-0.0.1). Das Modell selbst enthält keine FHIR-Mappings; die Zuordnung zu den Entwurfsprofilen ps-immunization und ps-immunization-medication steht als Mappingtabelle in dieser Projektkonfiguration. Elemente des Entwurfs ohne Knoten im Modell (z. B. identifier, primarySource, reportOrigin, recorded, Dosisnummer, PZN, Charge) zeigt die ausmodellierte Darstellung als „aus Profil“ — dort wäre das Modell nachzuziehen.
- Pakete: `example.impfung.entwurf#0.1.0`, `hl7.fhir.eu.eps#1.0.0-ballot`, `hl7.fhir.eu.base#2.0.1`, `hl7.fhir.uv.ips#2.0.1`, `hl7.fhir.eu.extensions.r4#1.3.1`, `hl7.fhir.uv.xver-r5.r4#0.1.0`, `hl7.fhir.uv.extensions.r4#5.3.0`, `de.gematik.epa#1.4.0-ballot.1`, `de.gematik.ti#1.5.0-ballot.2`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.r4.core#4.0.1`
- Lokales Paket (im Projekt, nicht veröffentlicht): `example.impfung.entwurf#0.1.0` aus `projekte/impfung/paket/`
- Logikmodelle für das EHDS-Mapping: `xtehr.eu.ehds.models#1.0.0`

## Mappingprüfung (Mappingtabelle des Projekts)

| Befund | Anzahl |
|---|---:|
| Elemente im Informationsmodell | 31 |
| davon mit FHIR-Mapping | 29 |
| FHIR-Mappings | 29 |
| exakt | 23 |
| gleichwertige Schreibweise (JSON-Name der Typwahl, Typ-Slice) — keine Korrektur nötig | 3 |
| Schreibvariante (gemischte Notation) — vereinheitlichen | 0 |
| über Extension-Definition oder Datentyp aufgelöst | 3 |
| **ohne Ziel** | **0** |
| **auf ein 0..0-Element** | **0** |
| Definition nicht im Paketbestand | 0 |
| in ein anderes Profil als das übergeordnete Element | 0 |

### Gleichwertige Schreibweisen (keine Korrektur nötig) (3)

| Element im Modell | Mapping | Befund |
|---|---|---|
| Impfdatum <br>*Impfung* | `PSImmunization.occurrenceDateTime` | JSON-Name `occurrenceDateTime` für die Typwahl `occurrence[x]` — gleichwertig |
| Referenz <br>*Notiz / Autor:in* | `PSImmunization.note.authorReference` | JSON-Name `authorReference` für die Typwahl `author[x]` — gleichwertig |
| Freitext <br>*Notiz / Autor:in* | `PSImmunization.note.authorString` | JSON-Name `authorString` für die Typwahl `author[x]` — gleichwertig |

## Wertelisten

1 Wertelisten im Modell, davon 1 im Paketbestand oder über eine Profilbindung aufgelöst, 1 mit Link auf die Originalseite.

### Werteliste im Modell gegen Bindung im Profil

Je Mapping eines Elements mit Werteliste: Bindung am Element, am zugehörigen CodeableConcept, am Wert einer gemappten Extension oder an einem Slice darunter.

| Ergebnis | Anzahl |
|---|---:|
| gleich | 1 |

## Ausmodellierte Darstellung

297 Knoten · 0 Referenzen an der Verwendungsstelle aufgelöst · 0 Zyklen erkannt · 266 Knoten aus FHIR-Profilen ergänzt

## EHDS-Mappingprüfung

9 Verweise an 9 Elementen, aufgelöst gegen `xtehr.eu.ehds.models#1.0.0` (82 Logikmodelle).

| Auflösung | Anzahl |
|---|---:|
| auflösbar: Element im Logikmodell | 8 |
| nur Modell ohne Element | 1 |
| **Element fehlt im Modell** | 0 |
| **Modell nicht im Paketbestand** | 0 |
| ausdrücklich ohne Gegenstück („im EHDS Logical Model nicht vorhanden“) | 0 |

| Linkformat | Anzahl |
|---|---:|
| Link auf die Seite des Modells mit Version (`…/models/1.0.0/en/…`) | 0 |
| **uneinheitlich: Link ohne Version** (`…/models/en/…`, jeweils aktueller Stand) | 8 |
| kanonische URL des Modells (`http://www.xt-ehr.eu/fhir/models/StructureDefinition/…`) | 1 |
| **Linkziel nur der Pfad**, keine URL | 0 |
| **Klartext ohne Link** | 0 |
| **Link auf eine andere Seite** als das Logikmodell | 0 |

Kontext: **0** Verweise auf das Modell eines anderen Bausteins (Modell weder das des übergeordneten Elements noch dort als Typ genannt).

### Link ohne Version (8)

| Element im Modell | EHDS-Verweis |
|---|---|
| Status <br>*Impfung* | `EHDSImmunisation.header.status` |
| Zielerkrankung - Code/Bezeichnung <br>*Impfung* | `EHDSImmunisation.diseaseOrAgentTargeted` |
| Impfstoff - Code/Bezeichnung <br>*Impfung* | `EHDSImmunisation.vaccine` |
| Verabreichtes Produkt <br>*Impfung* | `EHDSImmunisation.administeredProduct` |
| Impfdatum <br>*Impfung* | `EHDSImmunisation.administrationTime` |
| Verantwortliche Einrichtung <br>*Impfung* | `EHDSImmunisation.administeringCentre` |
| Impfende Person/Einrichtung <br>*Impfung* | `EHDSImmunisation.administrator` |
| Notiz <br>*Impfung* | `EHDSImmunisation.note` |

## Beispiele

| Beispiel | Ressourcen | fachliche Werte | durch das Modell gedeckt | Strukturbefunde |
|---|---:|---:|---:|---:|
| Erstdokumentation — zwei Impfungen, Mustermann | 5 | 89 | 22 | 0 |
| Nachtrag aus einem Papier-Impfpass — Mustermann | 5 | 78 | 17 | 0 |

### Erstdokumentation — zwei Impfungen, Mustermann

- Zweck: Zwei Impfungen in der Praxis dokumentiert (primarySource = true): Influenza und Auffrischung Tetanus-Diphtherie-Pertussis-Polio, je mit SNOMED-Impfstoff (Vaccines – IPS), Zielerkrankungen (IPS Target Diseases), Dosisnummer, impfender Person (performer.function AP) und verabreichtem Produkt als enthaltene Medication nach ps-immunization-medication (PZN, Handelsname, Charge).
- Herkunft: Für dieses Projekt erstellt, Gerüst aus dem Beispiel patient-summary/yildiz. Fiktive Daten; PZN, Chargen und Handelsnamen sind erfunden.
- Datei: `beispiele/erstdokumentation.json`

Werte ohne spezifisches Element im Informationsmodell (ohne url, reference, system, version, Erzähltext):

- `practitioner-eu-core#Practitioner.name.family` (1×)
- `practitioner-eu-core#Practitioner.name.given` (1×)
- `practitioner-eu-core#Practitioner.name.prefix` (1×)
- `practitioner-eu-core#Practitioner.name.use` (1×)
- `composition-eu-eps#Composition.date` (1×)
- `composition-eu-eps#Composition.identifier.value` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.title` (1×)
- `composition-eu-eps#Composition.section:sectionImmunizations.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionImmunizations.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionImmunizations.title` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.title` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.title` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.title` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.title` (1×)
- `composition-eu-eps#Composition.status` (1×)
- `composition-eu-eps#Composition.title` (1×)
- `composition-eu-eps#Composition.type.coding.code` (1×)
- `composition-eu-eps#Composition.type.coding.display` (1×)
- `patient-eu-eps#Patient.birthDate` (1×)
- `patient-eu-eps#Patient.gender` (1×)
- `patient-eu-eps#Patient.identifier.value` (1×)
- `patient-eu-eps#Patient.name.family` (1×)
- `patient-eu-eps#Patient.name.given` (1×)
- `patient-eu-eps#Patient.name.use` (1×)
- `ps-immunization#Immunization.identifier.value` (2×)
- `ps-immunization#Immunization.performer:administeringCentreOrHp.function.coding.code` (2×)
- `ps-immunization#Immunization.performer:administeringCentreOrHp.function.coding.display` (2×)
- `ps-immunization#Immunization.primarySource` (2×)
- `ps-immunization#Immunization.protocolApplied.doseNumberPositiveInt` (2×)
- `ps-immunization#Immunization.protocolApplied.series` (1×)
- `ps-immunization#Immunization.recorded` (2×)
- `ps-immunization-medication#Medication.batch.lotNumber` (2×)
- `ps-immunization-medication#Medication.code.coding:pzn.code` (2×)
- `ps-immunization-medication#Medication.code.coding:pzn.display` (2×)
- `ps-immunization-medication#Medication.code.text` (2×)
- `ps-immunization-medication#Medication.extension:isVaccine.valueBoolean` (2×)

### Nachtrag aus einem Papier-Impfpass — Mustermann

- Zweck: Zwei nachgetragene Impfungen (primarySource = false, reportOrigin record „Papier-Impfpass“): ein historischer Kombinationsimpfstoff nur als Text mit unbekannter Dosisnummer (doseNumberString mit data-absent-reason unknown) und eine Influenza-Impfung mit SNOMED-Code, das Produkt laut Etikett als enthaltene Medication ohne PZN.
- Herkunft: Für dieses Projekt erstellt, Gerüst aus dem Beispiel patient-summary/yildiz. Fiktive Daten.
- Datei: `beispiele/nachtrag-impfpass.json`

Werte ohne spezifisches Element im Informationsmodell (ohne url, reference, system, version, Erzähltext):

- `practitioner-eu-core#Practitioner.name.family` (1×)
- `practitioner-eu-core#Practitioner.name.given` (1×)
- `practitioner-eu-core#Practitioner.name.prefix` (1×)
- `practitioner-eu-core#Practitioner.name.use` (1×)
- `composition-eu-eps#Composition.date` (1×)
- `composition-eu-eps#Composition.identifier.value` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionAllergies.title` (1×)
- `composition-eu-eps#Composition.section:sectionImmunizations.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionImmunizations.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionImmunizations.title` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionMedicalDevices.title` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionMedications.title` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionProblems.title` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.code.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.code.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.emptyReason.coding.code` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.emptyReason.coding.display` (1×)
- `composition-eu-eps#Composition.section:sectionProceduresHx.title` (1×)
- `composition-eu-eps#Composition.status` (1×)
- `composition-eu-eps#Composition.title` (1×)
- `composition-eu-eps#Composition.type.coding.code` (1×)
- `composition-eu-eps#Composition.type.coding.display` (1×)
- `patient-eu-eps#Patient.birthDate` (1×)
- `patient-eu-eps#Patient.gender` (1×)
- `patient-eu-eps#Patient.identifier.value` (1×)
- `patient-eu-eps#Patient.name.family` (1×)
- `patient-eu-eps#Patient.name.given` (1×)
- `patient-eu-eps#Patient.name.use` (1×)
- `ps-immunization#Immunization.identifier.value` (2×)
- `ps-immunization#Immunization.primarySource` (2×)
- `ps-immunization#Immunization.protocolApplied.doseNumberPositiveInt` (1×)
- `ps-immunization#Immunization.protocolApplied.doseNumberString.extension.valueCode` (1×)
- `ps-immunization#Immunization.recorded` (2×)
- `ps-immunization#Immunization.reportOrigin.coding.code` (2×)
- `ps-immunization#Immunization.reportOrigin.coding.display` (2×)
- `ps-immunization#Immunization.reportOrigin.text` (2×)
- `ps-immunization-medication#Medication.batch.lotNumber` (1×)
- `ps-immunization-medication#Medication.code.text` (1×)
- `ps-immunization-medication#Medication.extension:isVaccine.valueBoolean` (1×)

## Anzeige für Anwender:innen

Stand: `berichte/impfung.anzeige.json`, geschrieben von `python3 -I werkzeuge/mx.py anzeige impfung`. Gezählt werden inhaltliche Werte der Beispiele, die weder die Anwenderansicht noch eine Dokumentfassung zeigt; auf der Seite stehen sie unter „Weitere Angaben aus der Instanz“. Technisch und nicht gezählt: Kennungen und Metadaten, Systeme, Versionen, URLs, Erzähltext, UUID-Kennungen, Verweise mit Ziel im Beispiel.

| Beispiel | nicht angezeigte Werte | in Elementen |
|---|---:|---:|
| Erstdokumentation — zwei Impfungen, Mustermann | 0 | 0 |
| Nachtrag aus einem Papier-Impfpass — Mustermann | 0 | 0 |

## FHIR-Validierung (HL7 Validator 7.0.1)

Stand: `berichte/impfung.validierung.json`, geschrieben von `python3 -I werkzeuge/mx.py validieren impfung`; FHIR 4.0.1, Optionen `-tx n/a -locale en-US` (ohne Terminologieserver).

- Pakete: `example.impfung.entwurf#0.1.0 (lokal: paket)`, `hl7.fhir.uv.extensions.r4#5.3.0`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.eu.base#2.0.1`, `hl7.fhir.uv.ips#2.0.1`, `de.gematik.ti#1.5.0-ballot.2`, `de.gematik.epa#1.4.0-ballot.1`, `de.gematik.terminology#1.1.0-ballot.2`, `hl7.fhir.eu.eps#1.0.0-ballot`
- Lädt der Validator selbst (im Paketbestand festgelegt, ohne Netz): `hl7.fhir.r4.core#4.0.1`, `hl7.fhir.xver-extensions#0.1.0`, `hl7.terminology.r4#6.2.0`, `hl7.fhir.uv.extensions.r4#5.2.0`, `hl7.terminology#7.5.0`, `hl7.fhir.uv.extensions#5.3.0`
- Abhängigkeiten mit Platzhalter, festgelegt: `ihe.formatcode.fhir#1.5.x` → `1.5.0`
- Ergebnis: **0 Fehler**, 13 als begründete Ausnahme, 21 Warnungen, 37 Hinweise

| Beispiel | Fehler | davon begründete Ausnahme | Warnungen | Hinweise | Stand |
|---|---:|---:|---:|---:|---|
| Erstdokumentation — zwei Impfungen, Mustermann | 8 | 8 | 13 | 23 | aktuell |
| Nachtrag aus einem Papier-Impfpass — Mustermann | 5 | 5 | 8 | 14 | aktuell |

**Begründete Ausnahmen** (`[[validierung.ausnahmen]]` in `projekt.toml`):

- `xver-datatype-kontext` — 6 Treffer: Werkzeuggrenze: Die Querversions-Extension administeredProduct (hl7.fhir.uv.xver-r5.r4 0.1.0) verlangt die Teil-Extension _datatype (1..1, Wert CodeableReference). Deren Kontext ist in hl7.fhir.uv.extensions.r4 5.2.0 und 5.3.0 als Element „Base“ angegeben, das es in R4 nicht gibt; der HL7 Validator 7.0.1 lehnt _datatype deshalb an jeder Stelle ab. Ohne _datatype fehlt ein Pflicht-Slice. Gegenprobe ohne administeredProduct: keine Fehler.
- `xver-datatype-folgefehler` — 7 Treffer: Folgefehler von xver-datatype-kontext: Der Abschnitt Impfungen der EPS-Composition prüft seine Einträge gegen immunization-eu-core; eine Impfung mit administeredProduct scheitert dort nur an _datatype, daraufhin passt die Composition nicht auf den Pflicht-Slice des Bundles. Die Impfungen selbst werden über meta.profile vollständig geprüft; ihre eigenen Meldungen bleiben sichtbar.

### Fehler und Warnungen — Erstdokumentation — zwei Impfungen, Mustermann

Gleiche Meldungen zusammengefasst; Ort als FHIRPath, Zeile in der Beispieldatei.

- **error**: Slice 'Bundle.entry:composition': a matching slice is required, but not found (from http://hl7.eu/fhir/eps/StructureDefinition/bundle-eu-eps\|1.0.0-ballot). Note that other slices are allowed in addition to this required slice — begründete Ausnahme `xver-datatype-folgefehler`<br>`Bundle` (Zeile 1)
- **error**: Slice 'Bundle.entry:composition': a matching slice is required, but not found (from http://hl7.org/fhir/uv/ips/StructureDefinition/Bundle-uv-ips\|2.0.0). Note that other slices are allowed in addition to this required slice — begründete Ausnahme `xver-datatype-folgefehler`<br>`Bundle` (Zeile 1)
- **error**: The extension http://hl7.org/fhir/StructureDefinition/_datatype v5.2.0 is not allowed to be used at this point (this element is [Bundle.entry.resource/*Immunization/imm-erst-influenza*/.extension, Extension, Immunization.extension]; allowed for this version = e:Base) — begründete Ausnahme `xver-datatype-kontext`<br>`Bundle.entry[3].resource/*Immunization/imm-erst-influenza*/.extension[0]` (Zeile 313)
- **error**: The extension http://hl7.org/fhir/StructureDefinition/_datatype v5.2.0 is not allowed to be used at this point (this element is [Bundle.entry.resource/*Immunization/imm-erst-tdap-ipv*/.extension, Extension, Immunization.extension]; allowed for this version = e:Base) — begründete Ausnahme `xver-datatype-kontext`<br>`Bundle.entry[4].resource/*Immunization/imm-erst-tdap-ipv*/.extension[0]` (Zeile 431)
- **error**: The extension http://hl7.org/fhir/StructureDefinition/_datatype v5.3.0 is not allowed to be used at this point (this element is [Bundle.entry.resource/*Immunization/imm-erst-influenza*/.extension, Extension, Immunization.extension]; allowed for this version = e:Base) — begründete Ausnahme `xver-datatype-kontext`<br>`Bundle.entry[3].resource/*Immunization/imm-erst-influenza*/.extension[0]` (Zeile 313)
- **error**: The extension http://hl7.org/fhir/StructureDefinition/_datatype v5.3.0 is not allowed to be used at this point (this element is [Bundle.entry.resource/*Immunization/imm-erst-tdap-ipv*/.extension, Extension, Immunization.extension]; allowed for this version = e:Base) — begründete Ausnahme `xver-datatype-kontext`<br>`Bundle.entry[4].resource/*Immunization/imm-erst-tdap-ipv*/.extension[0]` (Zeile 431)
- **error**: Unable to find a profile match for Immunization/imm-erst-influenza among choices: http://hl7.eu/fhir/base/StructureDefinition/immunization-eu-core — begründete Ausnahme `xver-datatype-folgefehler`<br>`Bundle.entry[0].resource/*Composition/ps-erstdokumentation*/.section[3].entry[0]` (Zeile 146)
- **error**: Unable to find a profile match for Immunization/imm-erst-tdap-ipv among choices: http://hl7.eu/fhir/base/StructureDefinition/immunization-eu-core — begründete Ausnahme `xver-datatype-folgefehler`<br>`Bundle.entry[0].resource/*Composition/ps-erstdokumentation*/.section[3].entry[1]` (Zeile 149)
- **warning** (2×): A definition for CodeSystem 'http://fhir.de/CodeSystem/ifa/pzn' could not be found, so the code cannot be validated<br>`Bundle.entry[3].resource/*Immunization/imm-erst-influenza*/.contained[0]/*Medication/impfstoff-1*/.code.coding[0].system` (Zeile 297), `Bundle.entry[4].resource/*Immunization/imm-erst-tdap-ipv*/.contained[0]/*Medication/impfstoff-2*/.code.coding[0].system` (Zeile 415)
- **warning**: Found multiple matching profiles for #impfstoff-1 among choices: http://hl7.org/fhir/5.0/StructureDefinition/profile-Medication\|0.1.0, http://hl7.org/fhir/StructureDefinition/Medication\|4.0.1<br>`Bundle.entry[3].resource/*Immunization/imm-erst-influenza*/.extension[0].extension[1].value.ofType(Reference)` (Zeile 322)
- **warning**: Found multiple matching profiles for #impfstoff-2 among choices: http://hl7.org/fhir/5.0/StructureDefinition/profile-Medication\|0.1.0, http://hl7.org/fhir/StructureDefinition/Medication\|4.0.1<br>`Bundle.entry[4].resource/*Immunization/imm-erst-tdap-ipv*/.extension[0].extension[1].value.ofType(Reference)` (Zeile 440)
- **warning** (5×): ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIIllnessandDisorder' not found<br>`Bundle.entry[3].resource/*Immunization/imm-erst-influenza*/.protocolApplied[0].targetDisease[0]` (Zeile 371), `Bundle.entry[4].resource/*Immunization/imm-erst-tdap-ipv*/.protocolApplied[0].targetDisease[0]` (Zeile 490), `Bundle.entry[4].resource/*Immunization/imm-erst-tdap-ipv*/.protocolApplied[0].targetDisease[1]` (Zeile 499) und 2 weitere
- **warning** (4×): ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIVaccine' not found<br>`Bundle.entry[3].resource/*Immunization/imm-erst-influenza*/.vaccineCode` (Zeile 336), `Bundle.entry[3].resource/*Immunization/imm-erst-influenza*/.vaccineCode.coding[0]` (Zeile 338), `Bundle.entry[4].resource/*Immunization/imm-erst-tdap-ipv*/.vaccineCode` (Zeile 454) und 1 weitere

### Fehler und Warnungen — Nachtrag aus einem Papier-Impfpass — Mustermann

Gleiche Meldungen zusammengefasst; Ort als FHIRPath, Zeile in der Beispieldatei.

- **error**: Slice 'Bundle.entry:composition': a matching slice is required, but not found (from http://hl7.eu/fhir/eps/StructureDefinition/bundle-eu-eps\|1.0.0-ballot). Note that other slices are allowed in addition to this required slice — begründete Ausnahme `xver-datatype-folgefehler`<br>`Bundle` (Zeile 1)
- **error**: Slice 'Bundle.entry:composition': a matching slice is required, but not found (from http://hl7.org/fhir/uv/ips/StructureDefinition/Bundle-uv-ips\|2.0.0). Note that other slices are allowed in addition to this required slice — begründete Ausnahme `xver-datatype-folgefehler`<br>`Bundle` (Zeile 1)
- **error**: The extension http://hl7.org/fhir/StructureDefinition/_datatype v5.2.0 is not allowed to be used at this point (this element is [Bundle.entry.resource/*Immunization/imm-nachtrag-influenza*/.extension, Extension, Immunization.extension]; allowed for this version = e:Base) — begründete Ausnahme `xver-datatype-kontext`<br>`Bundle.entry[4].resource/*Immunization/imm-nachtrag-influenza*/.extension[0]` (Zeile 389)
- **error**: The extension http://hl7.org/fhir/StructureDefinition/_datatype v5.3.0 is not allowed to be used at this point (this element is [Bundle.entry.resource/*Immunization/imm-nachtrag-influenza*/.extension, Extension, Immunization.extension]; allowed for this version = e:Base) — begründete Ausnahme `xver-datatype-kontext`<br>`Bundle.entry[4].resource/*Immunization/imm-nachtrag-influenza*/.extension[0]` (Zeile 389)
- **error**: Unable to find a profile match for Immunization/imm-nachtrag-influenza among choices: http://hl7.eu/fhir/base/StructureDefinition/immunization-eu-core — begründete Ausnahme `xver-datatype-folgefehler`<br>`Bundle.entry[0].resource/*Composition/ps-nachtrag-impfpass*/.section[3].entry[1]` (Zeile 149)
- **warning**: Found multiple matching profiles for #impfstoff-1 among choices: http://hl7.org/fhir/5.0/StructureDefinition/profile-Medication\|0.1.0, http://hl7.org/fhir/StructureDefinition/Medication\|4.0.1<br>`Bundle.entry[4].resource/*Immunization/imm-nachtrag-influenza*/.extension[0].extension[1].value.ofType(Reference)` (Zeile 398)
- **warning** (4×): ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIIllnessandDisorder' not found<br>`Bundle.entry[3].resource/*Immunization/imm-nachtrag-dt-polio*/.protocolApplied[0].targetDisease[0]` (Zeile 311), `Bundle.entry[3].resource/*Immunization/imm-nachtrag-dt-polio*/.protocolApplied[0].targetDisease[1]` (Zeile 320), `Bundle.entry[3].resource/*Immunization/imm-nachtrag-dt-polio*/.protocolApplied[0].targetDisease[2]` (Zeile 329) und 1 weitere
- **warning** (3×): ValueSet 'http://terminology.ehdsi.eu/ValueSet/eHDSIVaccine' not found<br>`Bundle.entry[3].resource/*Immunization/imm-nachtrag-dt-polio*/.vaccineCode` (Zeile 289), `Bundle.entry[4].resource/*Immunization/imm-nachtrag-influenza*/.vaccineCode` (Zeile 412), `Bundle.entry[4].resource/*Immunization/imm-nachtrag-influenza*/.vaccineCode.coding[0]` (Zeile 414)
