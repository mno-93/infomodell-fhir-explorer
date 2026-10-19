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

4. Den neuen Prüfbericht in `berichte/` mit einchecken. Im Browser prüfen: Beispiel wählen, je einen Wert in Anwenderansicht, Dokument und Modell anklicken.

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
| `[informationsmodell]` | `art` und die Angaben des Adapters (siehe `docs/AUFBAU.md`) |
| `[anforderungen]` | optional: `art = "gematik-requirements"`, `quelle` |
| `[[quellen]]` | gesicherte Quelldateien mit Herkunfts-URL |
| `[[beispiele]]` | siehe oben |
| `[validierung]` | Pakete für den HL7-Validator, `erweiterungen` (zugelassene Beispiel-Namensräume), `[[validierung.ausnahmen]]` mit `muster` und `grund` |
| `[[strukturausnahmen]]` | optional: `element`, `grund` — nur für bekannte Profilfehler |

Danach:

```bash
python3 -I werkzeuge/mx.py holen --aktualisieren   # neue Pakete und Quellen in die Sperrdatei
python3 -I werkzeuge/mx.py bauen
python3 -I -m unittest discover -s tests
```

`sperrdatei.json`, `berichte/<id>.md` und den Projektordner einchecken. Die Übersichtsseite nimmt das Projekt automatisch auf.

## Naheliegende nächste Projekte

| Projekt | Grundlage | Weg |
|---|---|---|
| Discharge Report | HL7 Europe Hospital Discharge Report (`hl7.fhir.eu.hdr` 1.0.0 in der Paketregistry) | `aus-profilen` mit der HDR-Composition als Einstieg, `darstellung = "dokument"`, `dokumente = ["erzaehltext"]`; Beispiele aus dem IG-Paket über `paket`/`einstieg` oder als Datei |
| Patient Summary der ePA | gematik-IG zur ePA-Patient-Summary, sobald als Paket in der Registry | wie `patient-summary`; ⚠ der Ballot liegt bisher nur als Download auf der IG-Seite vor, nicht in der Registry — dann über `[[quellen]]` oder einen eigenen Paket-Eintrag in der Sperrdatei mit URL |
| Weitere gematik-IGs mit Informationsmodell | IG mit `infomodell_js_treeview_*.json` | `gematik-baum` wie `laborbefund`; `referenzgruppe` auf den Namen der Gruppe „Referenzierte Profile“ des Modells setzen |
