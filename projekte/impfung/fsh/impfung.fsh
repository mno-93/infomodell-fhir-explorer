// Impfung (Entwurf, EU-konform) — Studie eines Impfeintrags nach HL7 Europe Base (EU Core),
// zugleich konform zu den Pflichtangaben der EU Patient Summary (EPS-Obligation-Profile).
// Nicht veröffentlicht; Paket wird mit `python3 -I werkzeuge/mx.py fsh impfung` nach paket/ erzeugt.

Alias: $ImmunizationEuCore = http://hl7.eu/fhir/base/StructureDefinition/immunization-eu-core
Alias: $ImmunizationOblEuEps = http://hl7.eu/fhir/eps/StructureDefinition/immunization-obl-eu-eps
Alias: $MedicationEuCore = http://hl7.eu/fhir/base/StructureDefinition/medication-eu-core
Alias: $MedicationOblEuEps = http://hl7.eu/fhir/eps/StructureDefinition/medication-obl-eu-eps
Alias: $EpaMedication = https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication
Alias: $imposeProfile = http://hl7.org/fhir/StructureDefinition/structuredefinition-imposeProfile
Alias: $sct = http://snomed.info/sct
Alias: $vaccines-uv-ips = http://hl7.org/fhir/uv/ips/ValueSet/vaccines-uv-ips
Alias: $target-diseases-uv-ips = http://hl7.org/fhir/uv/ips/ValueSet/target-diseases-uv-ips

Profile: PSImmunization
Parent: $ImmunizationEuCore
Id: ps-immunization
Title: "Impfung (Entwurf, EU-konform)"
Description: "Entwurf eines Impfeintrags auf Grundlage von ImmunizationEuCore (HL7 Europe Base), zugleich konform zu den EPS-Pflichtangaben (ImmunizationOblEuEps). Studie, nicht veröffentlicht."
* ^status = #draft
* ^extension[0].url = $imposeProfile
* ^extension[0].valueCanonical = $ImmunizationOblEuEps
* obeys ps-imm-1 and ps-imm-2
* identifier MS
* status MS
* statusReason MS
* vaccineCode MS
* vaccineCode.coding ^slicing.discriminator.type = #value
* vaccineCode.coding ^slicing.discriminator.path = "system"
* vaccineCode.coding ^slicing.rules = #open
* vaccineCode.coding contains snomed 0..1 MS
* vaccineCode.coding[snomed].system = $sct
* vaccineCode.coding[snomed].code 1..1
* vaccineCode.coding[snomed] from $vaccines-uv-ips (required)
* vaccineCode.coding[snomed] ^binding.extension[0].url = "http://hl7.org/fhir/tools/StructureDefinition/additional-binding"
* vaccineCode.coding[snomed] ^binding.extension[0].extension[0].url = "purpose"
* vaccineCode.coding[snomed] ^binding.extension[0].extension[0].valueCode = #preferred
* vaccineCode.coding[snomed] ^binding.extension[0].extension[1].url = "valueSet"
* vaccineCode.coding[snomed] ^binding.extension[0].extension[1].valueCanonical = "http://terminology.ehdsi.eu/ValueSet/eHDSIVaccine"
* vaccineCode.coding[snomed] ^binding.extension[0].extension[2].url = "documentation"
* vaccineCode.coding[snomed] ^binding.extension[0].extension[2].valueMarkdown = "Für den grenzüberschreitenden Austausch bevorzugt Codes aus eHDSI Vaccine verwenden."
// ext-ab-1: zusätzliche Bindungen sollen eine Kennung tragen (Validator-Warnung am Profil)
* vaccineCode.coding[snomed] ^binding.extension[0].extension[3].url = "key"
* vaccineCode.coding[snomed] ^binding.extension[0].extension[3].valueId = "ehdsi-vaccine"
* vaccineCode.coding[snomed] ^binding.description = "SNOMED-CT-Impfstoffprodukt (Vaccines - IPS, intensional); bevorzugt eHDSI Vaccine"
* vaccineCode.text MS
* extension[administeredProduct] MS
* extension[administeredProduct].extension[reference].valueReference only Reference(PSImmunizationMedication)
* patient MS
* occurrence[x] only dateTime
* occurrence[x] MS
* recorded MS
* primarySource MS
* reportOrigin MS
* extension[informationSource] MS
* performer[administeringCentreOrHp] MS
* protocolApplied MS
* protocolApplied.targetDisease MS
* protocolApplied.targetDisease from $target-diseases-uv-ips (extensible)
* protocolApplied.doseNumber[x] MS

Profile: PSImmunizationMedication
Parent: $EpaMedication
Id: ps-immunization-medication
Title: "Impfstoffprodukt (Entwurf, EU-konform)"
Description: "Entwurf: verabreichtes Impfstoffprodukt auf Grundlage des ePA-Medikationsprofils (epa-medication), zugleich konform zu MedicationEuCore und den EPS-Pflichtangaben (MedicationOblEuEps). Studie, nicht veröffentlicht."
* ^status = #draft
* ^extension[0].url = $imposeProfile
* ^extension[0].valueCanonical = $MedicationEuCore
* ^extension[1].url = $imposeProfile
* ^extension[1].valueCanonical = $MedicationOblEuEps
* code 1..1 MS
* code.text MS
* manufacturer MS
* batch MS
* batch.lotNumber MS

Invariant: ps-imm-1
Description: "Impfstoff: SNOMED-CT-Code, Freitext (z. B. historische Kombinationsimpfstoffe) oder data-absent-reason"
Expression: "vaccineCode.coding.where(system='http://snomed.info/sct').exists() or vaccineCode.text.exists() or vaccineCode.extension('http://hl7.org/fhir/StructureDefinition/data-absent-reason').exists()"
Severity: #error

Invariant: ps-imm-2
Description: "Nachgetragene Impfungen (primarySource = false) nennen ihre Quelle"
Expression: "primarySource = false implies (reportOrigin.exists() or extension('http://hl7.org/fhir/5.0/StructureDefinition/extension-Immunization.informationSource').exists())"
Severity: #error
