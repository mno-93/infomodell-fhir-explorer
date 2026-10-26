# Neue Beispiele und neue Projekte

## Ein Beispiel ergänzen

1. Datei nach `projekte/<id>/beispiele/` legen — ein Bundle (`document`, `collection` …) oder eine einzelne Ressource. **Nur fiktive Daten.**
2. In `projekt.toml` einen Block anfügen:

   ```toml
   [[beispiele]]
   id = "kurzname"                      # eindeutig, erscheint im Link: …/<projekt>.html#kurzname
   titel = "Was es ist — Person, Datum"
   zweck = "Was dieses Beispiel zeigt, das die anderen nicht zeigen."
   herkunft = "Woher es stammt, mit Stand (Repository und Commit, Paket und Version)."
   datei = "beispiele/kurzname.json"
   ```

   Beispiele aus einem FHIR-Paket statt einer Datei: `paket = "<id>#<version>"` und `einstieg = "<Typ>/<id>"` — eingesammelt werden alle Ressourcen, die von der Einstiegsressource aus über Verweise erreichbar sind.
3. Prüfen und bauen:

   ```bash
   python3 -I werkzeuge/mx.py pruefen <projekt>
   python3 -I werkzeuge/mx.py validieren <projekt>
   python3 -I werkzeuge/mx.py bauen
   ```

4. Den neuen Prüfbericht `berichte/<projekt>.md` und das Validierungsergebnis `berichte/<projekt>.validierung.json` mit einchecken. Im Browser prüfen: Beispiel wählen, je einen Wert in Anwenderansicht, Dokument und Modell anklicken; unter „Abdeckung & Prüfung“ steht das Ergebnis des Validators.

Reihenfolge: erst `validieren`, dann `bauen` — der Bau liest das Validierungsergebnis. Ändert sich eine Beispieldatei nach der Validierung, melden Bericht und Oberfläche das Beispiel als veraltet und ein Test schlägt fehl, bis neu validiert ist.

## Ein Projekt anlegen

Vorlage: `projekte/patient-summary/projekt.toml` (ohne Informationsmodell) oder `projekte/laborbefund/projekt.toml` (mit gematik-Informationsmodell).

| Angabe | Inhalt |
|---|---|
| `id`, `titel`, `beschreibung` | `id` = Ordnername |
| `darstellung` | `laborbefund` oder `dokument` |
| `dokumente` | Auswahl aus `druck`, `pdf`, `erzaehltext` |
| `pakete` | alle Pakete mit StructureDefinitions, die Modell und Beispiele brauchen, mit fester Version; Reihenfolge = Vorrang; `hl7.fhir.r4.core#4.0.1` zuletzt |
| `terminologiepakete` | optional: Pakete nur zur Auflösung von Wertelisten (z. B. `de.gematik.terminology`, `hl7.terminology.r4`), feste Version |
| `[ig]` | `name`, `paket`, `status`, `url`, `kanonisch` (für Links auf Profilseiten) |
| `[standardprofile]` | Profil je Ressourcentyp für Ressourcen ohne `meta.profile` |
| `[informationsmodell]` | `art` und die Angaben des Adapters (siehe `docs/AUFBAU.md`); bei `aus-profilen` darf `einstieg` eine Liste sein |
| `[anforderungen]` | optional: `art = "gematik-requirements"`, `quelle` |
| `[[quellen]]` | gesicherte Quelldateien mit Herkunfts-URL |
| `[[beispiele]]` | siehe oben |
| `[validierung]` | Pakete für den HL7-Validator (lokale Pakete kommen automatisch mit `-ig <ordner>/package` dazu), `erweiterungen` (zugelassene Beispiel-Namensräume), `[[validierung.ausnahmen]]` mit `id`, `muster` (regulärer Ausdruck auf „Ort: Text“ einer Fehlermeldung) und `grund` |
| `[[strukturausnahmen]]` | optional: `element`, `grund` — nur für bekannte Profilfehler |

Danach:

```bash
python3 -I werkzeuge/mx.py holen --aktualisieren   # neue Pakete und Quellen in die Sperrdatei
python3 -I werkzeuge/mx.py bauen
python3 -I -m unittest discover -s tests
```

`sperrdatei.json`, `berichte/<id>.md`, `berichte/<id>.validierung.json` und den Projektordner einchecken. Die Übersichtsseite nimmt das Projekt automatisch auf.

## FHIR-Validierung: Ergebnis im Projekt

```bash
python3 -I werkzeuge/mx.py validieren <projekt>   # Java und ~/.fhir/validator_cli.jar (oder $VALIDATOR_JAR)
```

- Aufruf je Projekt: alle Beispieldateien, `-version 4.0.1 -tx n/a -locale en-US`, `-ig` für die lokalen Pakete und die Pakete aus `[validierung]`; die JVM läuft mit `-Duser.language=en -Duser.country=US`, damit die Meldungstexte auf jedem Rechner englisch und gleich sind.
- Ergebnis `berichte/<projekt>.validierung.json`: Validator-Version (aus der Ausgabe des Validators), Optionen, Pakete, Ausnahmen mit Trefferzahl, Summe und je Beispiel (über die Datei dem `[[beispiele]]`-Eintrag zugeordnet) die Zahl der Fehler (error, fatal), davon begründete Ausnahmen, Warnungen und Hinweise (information), dazu die SHA-256 der Beispieldatei. Fehler und Warnungen stehen einzeln mit Stufe, Ort (FHIRPath, sonst Position), Zeile, Text und ggf. der Kennung der genutzten Ausnahme — sortiert, ohne Zeitstempel und ohne absolute Pfade; Einzelheiten, die von der Antwort eines fremden Servers abhängen (Nachladen eines Profils unter einer Beispiel-URL), werden vereinheitlicht.
- Exit-Code ≠ 0, wenn ein Fehler keine begründete Ausnahme ist; Ausnahmen ohne Treffer werden als Hinweis gemeldet. Ausnahmen nur für Grenzen der Prüfung (kein Terminologieserver, bekannte Werkzeug- oder Paketfehler) mit Begründung, nicht für Fehler der Beispiele oder Profile.
- `bauen` braucht kein Java: Es liest die Datei und zeigt das Ergebnis im Prüfbericht (Abschnitt „FHIR-Validierung (HL7 Validator x.y.z)“), unter „Abdeckung & Prüfung“ des gewählten Beispiels und als Kennzahl auf der Übersichtsseite; ohne Datei steht dort „noch nicht validiert“.
- Die CI validiert im Job `validieren` neu und prüft mit `git diff --exit-code`, dass `berichte/*.validierung.json` dem eingecheckten Stand entspricht.

## Naheliegende nächste Projekte

| Projekt | Grundlage | Weg |
|---|---|---|
| Discharge Report | HL7 Europe Hospital Discharge Report (`hl7.fhir.eu.hdr` 1.0.0 in der Paketregistry) | `aus-profilen` mit der HDR-Composition als Einstieg, `darstellung = "dokument"`, `dokumente = ["erzaehltext"]`; Beispiele aus dem IG-Paket über `paket`/`einstieg` oder als Datei |
| Patient Summary der ePA | gematik-IG zur ePA-Patient-Summary, sobald als Paket in der Registry | wie `patient-summary`; ⚠ der Ballot liegt bisher nur als Download auf der IG-Seite vor, nicht in der Registry — dann über `[[quellen]]` oder einen eigenen Paket-Eintrag in der Sperrdatei mit URL |
| Weitere gematik-IGs mit Informationsmodell | IG mit `infomodell_js_treeview_*.json` | `gematik-baum` wie `laborbefund`; `referenzgruppe` auf den Namen der Gruppe „Referenzierte Profile“ des Modells setzen |
