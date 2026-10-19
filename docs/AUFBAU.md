# Aufbau und Verknüpfungslogik

## Ein Schlüssel für alles

Jede Verknüpfung läuft über **Profil-URL + kanonische Elementkennung**, z. B.
`https://gematik.de/fhir/epa-laboratory/StructureDefinition/observation-laboratory-study-dglp#Observation.valueQuantity.value`.

- Typwahlen stehen als JSON-Name (`valueQuantity` statt `value[x]:valueQuantity`), damit Modell, Profil-Snapshot und Instanz dieselbe Schreibweise haben.
- Slices bleiben erhalten (`interpretation.coding:hl7Interpretation`).
- Ein Element **umfasst** ein anderes, wenn es gleich oder Vorfahr ist; `value[x]` umfasst `valueQuantity`, ein Element ohne Slice umfasst alle seine Slices.

## Die Kette

| Verbindung | Wie sie entsteht | Belastbarkeit |
|---|---|---|
| Modell → Profil | Mapping des Informationsmodells, über `aufloeser.py` gegen den Snapshot aufgelöst (Slices, Typwahl, Extension-Definitionen, Datentypen, `0..0`) | spezifiziert |
| Profil → Instanz | jeder Knoten der Instanz wird dem Profilelement zugeordnet; Slices über Muster und Festwerte, Extensions über ihre URL — wie ein Validator | abgeleitet, deterministisch |
| Instanz → Anwenderansicht, Druckfassung | die Darstellung trägt an jedem Wert den Instanzpfad, aus dem er stammt | konstruktiv |
| Instanz → PDF, Erzähltext | Textabgleich der Zeilen mit den Instanzwerten (Zahlen und Datumsangaben auch in deutscher Schreibweise) | heuristisch |
| Element → Anforderungen | Anforderungen im Modell direkt; Verarbeitungsregeln über die im Text genannten Pfade und das Profil des Abschnitts | teils heuristisch |
| Code → Modell | Code der Instanz gleich Code der Terminologiezuordnung im Modell | spezifiziert |

## Profilzuordnung der Ressourcen

1. `meta.profile`, sofern das Profil im Paketbestand liegt;
2. sonst das **Standardprofil** des Projekts für den Ressourcentyp (`[standardprofile]` in `projekt.toml`), z. B. die Zielprofile der Abschnitte einer Composition;
3. sonst die Basisressource.

Der Prüfbericht zählt je Beispiel, wie viele Ressourcen über 2. oder 3. zugeordnet wurden.

## Modell-Adapter

| `informationsmodell.art` | Quelle | Ergebnis |
|---|---|---|
| `gematik-baum` | JSON hinter der Baumansicht „Informationsmodell“ eines gematik-IG (Felder `fhirMappings`, `termAssocs`, `cardinality`, `otherProperties`) | Modell mit Mappings, Terminologie, Herkunft, eingebetteten Anforderungen; dazu die **ausmodellierte Sicht** (`referenzgruppe`, optional `ergaenzen_aus` für Profile, die das Modell nur als Ganzes nennt) |
| `aus-profilen` | Einstiegsprofil (`einstieg`), meist die Composition | Struktur aus Pflicht- und Must-Support-Elementen bis `tiefe`; Abschnitte und Eintrags-Slices immer, Zielprofile der Einträge ausmodelliert |

Ein weiterer Adapter — etwa für ein logisches Modell (`StructureDefinition` mit `kind = logical` und `mapping`) — liefert dasselbe Knotenformat (`werkzeuge/mx/infomodell.py`) und braucht keine Änderung an Oberfläche oder Berichten.

## Terminologie

Das Informationsmodell nennt je Element Codes und Wertelisten (Tabellen „termAssocs“ und „codes“ im IG-Export). Sie werden **nach ihren Kopfzeilen** gelesen (Konzept, Code, Display, Designations, Filter, CodeSystem, ValueSet) und im Explorer als Tabelle gezeigt; im Beispiel belegte Codes stehen oben und springen auf den Wert.

Wertelisten werden über Name, Kennung oder Titel in den Paketen des Projekts und in `terminologiepakete` gesucht (`werkzeuge/mx/terminologie.py`). Links nur nach geprüften Mustern:

| Paket | Originalseite |
|---|---|
| `hl7.fhir.r4.core` | `https://hl7.org/fhir/R4/valueset-<id>.html` |
| `hl7.terminology.r4#<v>` | `https://terminology.hl7.org/<v>/ValueSet-<id>.html` |
| `hl7.fhir.eu.<ig>#<v>` | `https://hl7.eu/fhir/<ig>/<v>/ValueSet-<id>.html` |
| `de.gematik.terminology#<v>` | `https://gemspec.gematik.de/ig/fhir/terminology/<v>/ValueSet-<id>.html` |

Liegt eine Werteliste nicht im Paketbestand, aber bindet ein Profil sie, wird ihre kanonische URL verlinkt — nur für Herausgeber, deren kanonische URLs auflösen (fhir.kbv.de, hl7.org, terminology.hl7.org). Sonst: „nicht im Paketbestand“, kein Link. Profilbindungen (`binding.valueSet`) werden genauso verlinkt.

**Abgleich:** Nennt das Modell für ein exakt gemapptes Element genau eine Werteliste, wird sie mit der Bindung des Profilelements verglichen; Abweichungen stehen im Prüfbericht und am Element.

## Darstellungen

| `darstellung` | Anwenderansicht |
|---|---|
| `laborbefund` | Befundeingang mit Kopf (Patient:in, Labor, Auftrag, Probe), Ergebnistabelle nach Laborbereich und Gruppe, Bewertung |
| `dokument` | allgemeine Ansicht einer Composition: Kopf, Abschnitte, je Eintrag Bezeichnung, Wert, Status, Datum; leere Abschnitte mit `emptyReason` |

| `dokumente` | Dokumentansicht |
|---|---|
| `druck` | A4-Druckfassung des Laborbefunds mit Freigabe, Dokument-ID und Version |
| `pdf` | Textebene des PDF aus `DiagnosticReport.presentedForm` |
| `erzaehltext` | Erzähltext der Abschnitte (`Composition.section.text`) |

## Grenzen

- Terminologie nur so weit, wie sie in Modell und Instanzen steht; kein Terminologieserver.
- Anforderungsbezüge über Pfade im Fließtext und Textabgleich mit PDF oder Erzähltext sind heuristisch.
- Anwenderansicht und Druckfassung sind **eine** mögliche Darstellung, nicht spezifiziert.
