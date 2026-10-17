# Prüfbericht — Patient Summary (EU EPS)

> Erzeugt von `python3 werkzeuge/mx.py bauen`. Nicht von Hand ändern; die CI prüft, dass der Bericht zum Stand passt.

## Quellen

- Implementation Guide: HL7 Europe Patient Summary (`hl7.fhir.eu.eps#1.0.0-ballot`, Ballot)
- Darstellung des Modells: Struktur aus den Profilen — Für die EU Patient Summary ist kein Informationsmodell mit FHIR-Mappings veröffentlicht; die Xt-EHR-Logikmodelle 1.0.0 enthalten keine Mappings auf FHIR. Die Struktur folgt deshalb den Profilen: Pflicht- und Must-Support-Elemente bis zur dritten Ebene.
- Pakete: `hl7.fhir.eu.eps#1.0.0-ballot`, `hl7.fhir.eu.base#2.0.0`, `hl7.fhir.uv.ips#2.0.0`, `hl7.fhir.eu.extensions.r4#1.3.0`, `hl7.fhir.uv.xver-r5.r4#0.1.0`, `hl7.fhir.uv.extensions.r4#5.3.0`, `de.gematik.epa.medication#1.3.5`, `de.gematik.epa#1.3.2`, `de.gematik.ti#1.3.1`, `de.basisprofil.r4#1.5.4`, `hl7.fhir.r4.core#4.0.1`

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
