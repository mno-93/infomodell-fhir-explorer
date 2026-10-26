# Prüfbericht — Impfung (Entwurf, EU-konform)

> Erzeugt von `python3 werkzeuge/mx.py bauen`. Nicht von Hand ändern; die CI prüft, dass der Bericht zum Stand passt.

## Quellen

- Implementation Guide: Entwurf (nicht veröffentlicht) — Grundlagen: HL7 Europe Base 2.0.1, HL7 Europe Patient Summary 1.0.0-ballot (`example.impfung.entwurf#0.1.0`, Entwurf, nicht veröffentlicht)
- Darstellung des Modells: Struktur aus den Profilen — Kein Informationsmodell mit FHIR-Mappings: Die Struktur folgt den Entwurfsprofilen (Pflicht- und Must-Support-Elemente bis zur dritten Ebene). Einstieg ist das Impfprofil selbst, nicht die EPS-Composition — deren Abschnitt Impfungen zielt auf immunization-eu-core und würde den Entwurf nicht zeigen. Das Impfstoffprodukt steht als zweiter Einstieg daneben, weil es nur über die Extension administeredProduct als enthaltene Ressource erreicht wird.
- Pakete: `example.impfung.entwurf#0.1.0`, `hl7.fhir.eu.eps#1.0.0-ballot`, `hl7.fhir.eu.base#2.0.1`, `hl7.fhir.uv.ips#2.0.1`, `hl7.fhir.eu.extensions.r4#1.3.1`, `hl7.fhir.uv.xver-r5.r4#0.1.0`, `hl7.fhir.uv.extensions.r4#5.3.0`, `de.gematik.epa#1.4.0-ballot.1`, `de.gematik.ti#1.5.0-ballot.2`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.r4.core#4.0.1`
- Lokales Paket (im Projekt, nicht veröffentlicht): `example.impfung.entwurf#0.1.0` aus `projekte/impfung/paket/`

## Beispiele

| Beispiel | Ressourcen | fachliche Werte | durch die abgeleitete Struktur gedeckt | Strukturbefunde |
|---|---:|---:|---:|---:|
| Erstdokumentation — zwei Impfungen, Mustermann | 5 | 89 | 45 | 0 |
| Nachtrag aus einem Papier-Impfpass — Mustermann | 5 | 78 | 34 | 0 |

### Erstdokumentation — zwei Impfungen, Mustermann

- Zweck: Zwei Impfungen in der Praxis dokumentiert (primarySource = true): Influenza und Auffrischung Tetanus-Diphtherie-Pertussis-Polio, je mit SNOMED-Impfstoff (Vaccines – IPS), Zielerkrankungen (IPS Target Diseases), Dosisnummer, impfender Person (performer.function AP) und verabreichtem Produkt als enthaltene Medication nach ps-immunization-medication (PZN, Handelsname, Charge).
- Herkunft: Für dieses Projekt erstellt, Gerüst aus dem Beispiel patient-summary/yildiz. Fiktive Daten; PZN, Chargen und Handelsnamen sind erfunden.
- Datei: `beispiele/erstdokumentation.json`

### Nachtrag aus einem Papier-Impfpass — Mustermann

- Zweck: Zwei nachgetragene Impfungen (primarySource = false, reportOrigin record „Papier-Impfpass“): ein historischer Kombinationsimpfstoff nur als Text mit unbekannter Dosisnummer (doseNumberString mit data-absent-reason unknown) und eine Influenza-Impfung mit SNOMED-Code, das Produkt laut Etikett als enthaltene Medication ohne PZN.
- Herkunft: Für dieses Projekt erstellt, Gerüst aus dem Beispiel patient-summary/yildiz. Fiktive Daten.
- Datei: `beispiele/nachtrag-impfpass.json`

## FHIR-Validierung (HL7 Validator 7.0.1)

Stand: `berichte/impfung.validierung.json`, geschrieben von `python3 -I werkzeuge/mx.py validieren impfung`; FHIR 4.0.1, Optionen `-tx n/a -locale en-US` (ohne Terminologieserver).

- Pakete: `example.impfung.entwurf#0.1.0 (lokal: paket)`, `hl7.fhir.uv.extensions.r4#5.3.0`, `de.basisprofil.r4#1.6.0`, `hl7.fhir.eu.base#2.0.1`, `hl7.fhir.uv.ips#2.0.1`, `de.gematik.ti#1.5.0-ballot.2`, `de.gematik.epa#1.4.0-ballot.1`, `de.gematik.terminology#1.1.0-ballot.2`, `hl7.fhir.eu.eps#1.0.0-ballot`
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
