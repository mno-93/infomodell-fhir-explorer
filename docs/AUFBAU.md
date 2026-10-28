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

Enthaltene Ressourcen (`contained`) bleiben Knoten der umgebenden Ressource (`Immunization/imm-1|contained[0].code.text`), werden aber nach denselben Regeln einem eigenen Profil zugeordnet — wie beim Validator. So zeigt z. B. das Impfstoffprodukt einer Impfung auf `ps-immunization-medication`, nicht auf `Immunization.contained`.

## Modell-Adapter

| `informationsmodell.art` | Quelle | Ergebnis |
|---|---|---|
| `gematik-baum` | JSON hinter der Baumansicht „Informationsmodell“ eines gematik-IG (Felder `fhirMappings`, `termAssocs`, `cardinality`, `otherProperties`) | Modell mit Mappings, Terminologie, Herkunft, eingebetteten Anforderungen; dazu die **ausmodellierte Sicht** (`referenzgruppe`, optional `ergaenzen_aus` für Profile, die das Modell nur als Ganzes nennt) |
| `mio-baum` | JSON hinter der Baumansicht „Informationsmodell“ eines MIO-IG (Felder `cardinality`, `codes`, `termAssocs`, `operationalisations`, `otherProperties`; kein `fhirMappings`) | Modell mit Kardinalität und Konformität (auch bedingt), Terminologie, Anforderungen (MUSS/SOLL/KANN), weiteren Angaben und dem **EHDS-Mapping** je Element (`ehds`); ausmodellierte Sicht über `referenzgruppe` (Referenzziele in beliebiger Tiefe). Optional `teilbaum` (nur ein Ast, z. B. ein Profil), `[[informationsmodell.mappings]]` (FHIR-Mappings aus einer Mappingtabelle des Projekts: `knoten`, `fhir` oder `ohne_ziel`) und `profil_ergaenzen` (Must-Support-Elemente eines gemappten Profils ohne Modellknoten als „aus Profil“) |
| `aus-profilen` | Einstiegsprofil (`einstieg`), meist die Composition; auch eine Liste von Profilen nebeneinander (z. B. ein Eintragsprofil und das Profil seiner enthaltenen Ressource) | Struktur aus Pflicht- und Must-Support-Elementen bis `tiefe`; Abschnitte und Eintrags-Slices immer, Zielprofile der Einträge ausmodelliert |

Knoten können zusätzlich `ehds` (Verweise auf das EHDS-Logikmodell, siehe unten) und `ohne_ziel` (Grund, warum ein Element bewusst kein FHIR-Ziel hat) tragen.

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

## EHDS-Mappingprüfung (mio-baum)

Ein MIO-Modell nennt je Element sein Gegenstück in den EHDS-Logikmodellen von Xt-EHR (`otherProperties`, Abschnitte „EHDS Logical Model“, „EHDS-Mapping“). `werkzeuge/mx/ehds.py` liest die Verweise und löst sie gegen die StructureDefinitions (`kind = logical`) der `logikmodellpakete` auf — wie die FHIR-Mappingprüfung gegen Profil-Snapshots.

| Ergebnis | Bedeutung |
|---|---|
| auflösbar | Modell und Element gibt es im Paket |
| nur Modell | nur das Modell genannt (passend für Elemente, die ein ganzes Modell abbilden) |
| Element fehlt im Modell · Modell nicht im Paketbestand | Verweis führt ins Leere |
| ausdrücklich ohne Gegenstück | „Element ist im EHDS Logical Model nicht vorhanden“ |
| Linkformat | versioniert (`…/models/1.0.0/en/…`) · ohne Version (`…/models/en/…`, jeweils aktueller Stand) · kanonische URL · Linkziel nur der Pfad · Klartext ohne Link · Link auf eine andere Seite |
| Modell eines anderen Bausteins | Modell weder das des nächsten übergeordneten Elements mit EHDS-Mapping noch dort als Typ genannt (z. B. Element unter „Allergie/Unverträglichkeit“ → `EHDSCondition.*`) |

Links auf die Originalseiten nur nach dem geprüften Muster `https://www.xt-ehr.eu/fhir/models/<Version>/en/StructureDefinition-<Modell>[-definitions].html[#<Element>]`.

## FHIR-Validierung

`mx.py validieren` ruft den HL7 Validator je Projekt mit festen Optionen auf (`-tx n/a -locale en-US`, JVM mit `-Duser.language=en -Duser.country=US`) und schreibt `berichte/<projekt>.validierung.json` (`werkzeuge/mx/validieren.py`). Jede Meldung wird über ihre Datei dem Beispiel zugeordnet; Fehler werden gegen die begründeten Ausnahmen des Projekts geprüft. `bauen` bettet das Ergebnis ein: Prüfbericht, Dialog „Abdeckung & Prüfung“ (Ort als Sprung zum Wert, sofern er sich einem Knoten des Beispiels zuordnen lässt) und Übersichtsseite. Der Validator selbst läuft nur in `validieren`, nie im Bau — ohne Netz und nur mit dem gesperrten Paketbestand in `.validator/`, den `holen` füllt; so hängt das Ergebnis nicht davon ab, welche Paketfassungen der Paketserver gerade als neueste meldet.

### Anzeige für Anwender:innen: nichts geht verloren

Jeder inhaltliche Wert eines Beispiels steht in der Anwenderansicht, in einer Dokumentfassung (Druckfassung, PDF, Erzähltext) oder im **Auffangnetz** „Weitere Angaben aus der Instanz“ am Ende der Anwenderansicht (`weitereAngaben` in `web/explorer.html`). So bleibt die Ansicht für eine medizinische Sichtung vollständig, auch wenn ein Beispiel Elemente enthält, die keine Darstellung vorsieht.

- **Angezeigt** ist ein Wert, wenn ein Element der Ansicht ihn über `data-n` verknüpft — er selbst, ein Vorfahr oder ein Geschwister im selben Datentyp (die Anzeige von `code.text` deckt `code.coding`, die von `valueQuantity.value` deckt Einheit und System).
- **Mitgetragen** sind Angaben, die eine Zeile ausdrücklich, aber ohne eigene Anzeige vertritt; sie stehen in `data-implizit` (nur für die Prüfung, nicht für die Auswahl): Normalstatus wie `final`/`completed`, Kategorie, Zeitpunkte gleich Entnahme bzw. Befund, Methode im Namen, reine Markierungen. Weicht ein solcher Wert ab (vorläufig, anderer Zeitpunkt), zeigt die Ansicht ihn an.
- **Technisch** und nicht gezählt: Kennungen und Metadaten, Systeme, Versionen, URLs, Verweis-IDs, Erzähltext, UUID-Kennungen, Verweise mit Ziel im Beispiel (das Ziel wird selbst gezählt). Ein Verweis ohne Ziel mit `display` ist Inhalt.

`mx.py anzeige` führt die gebauten Seiten im Prüfmodus (`?abdeckung`) in einem Browser ohne Fenster aus und schreibt `berichte/<projekt>.anzeige.json`; der Prüfbericht zeigt das Ergebnis je Beispiel, die CI prüft, dass die Datei zum Stand passt. **Eine neue Darstellung** muss am Ende der Anwenderansicht `weitereAngabenHtml()` anhängen, Werte mit `F(…)` (Elementbezug) ausgeben, Mitgetragenes mit `data-implizit` kennzeichnen und ihre Dokumentfassungen in `DOKUMENT_HTML` eintragen.

## Grenzen

- Terminologie nur so weit, wie sie in Modell und Instanzen steht; kein Terminologieserver.
- Anforderungsbezüge über Pfade im Fließtext und Textabgleich mit PDF oder Erzähltext sind heuristisch.
- Anwenderansicht und Druckfassung sind **eine** mögliche Darstellung, nicht spezifiziert.
