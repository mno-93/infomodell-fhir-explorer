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
| `lokale_pakete` | optional: Ordner im Projekt mit `package/package.json` und den Ressourcen eines FHIR-Pakets (StructureDefinitions mit Snapshot), z. B. `["paket"]`; Vorrang vor `pakete`; siehe unten |
| `[fsh]` | optional: `quelle` (Ordner mit `*.fsh`, Vorgabe `fsh`) und `paket` (Zielordner des lokalen Pakets) für `mx.py fsh <projekt>` |
| `terminologiepakete` | optional: Pakete nur zur Auflösung von Wertelisten (z. B. `de.gematik.terminology`, `hl7.terminology.r4`), feste Version |
| `[ig]` | `name`, `paket`, `status`, `url`, `kanonisch` (für Links auf Profilseiten) |
| `[standardprofile]` | Profil je Ressourcentyp für Ressourcen ohne `meta.profile` |
| `logikmodellpakete` | optional: Pakete mit Logikmodellen für die EHDS-Mappingprüfung eines `mio-baum`, z. B. `xtehr.eu.ehds.models#1.0.0` |
| `[informationsmodell]` | `art` und die Angaben des Adapters (siehe `docs/AUFBAU.md`); bei `aus-profilen` darf `einstieg` eine Liste sein; bei `mio-baum` `quelle`, `referenzgruppe`, optional `teilbaum`, `profil_ergaenzen` und `[[informationsmodell.mappings]]` |
| `[anforderungen]` | optional: `art = "gematik-requirements"`, `quelle` |
| `[[quellen]]` | gesicherte Quelldateien mit Herkunfts-URL |
| `[[beispiele]]` | siehe oben; `beispiele = []` für ein Projekt, das nur ein Modell zeigt (Begründung in `hinweis`) |
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
- Pakete: Der Validator läuft **ohne Netz** mit eigenem Benutzerverzeichnis `.validator/` (`-Duser.home`, `fhir-settings.json` mit `prohibitNetworkAccess`). `holen` füllt dessen Cache `.validator/.fhir/packages` mit dem vollständigen Paketbestand — die Pakete aus `[validierung]`, die Abhängigkeiten der lokalen Pakete, die Pakete, die der Validator selbst lädt, und alle Abhängigkeiten — prüft ihn gegen `sperrdatei.json` und entfernt fremde Ordner. Grund: Der Validator lädt `hl7.terminology` und `hl7.fhir.uv.extensions` ohne Version, also die jeweils neueste beim Paketserver; ohne Netz nimmt er die einzige Fassung im Cache. Diese Fassungen stehen fest in `werkzeuge/mx/validieren.py` (`NEUESTE`) und erscheinen im Ergebnis unter `validatorpakete`; ebenso Abhängigkeiten mit Platzhalter wie `1.5.x`, die der Validator sonst auch beim Paketserver auflöst (`PLATZHALTER`, im Ergebnis unter `platzhalter`). Ein neuer Platzhalter ohne Festlegung bricht `holen` mit Hinweis ab. Ein neues Paket in `[validierung]` heißt also: `holen`, dann `validieren`, und `sperrdatei.json` mit einchecken.
- Ergebnis `berichte/<projekt>.validierung.json`: Validator-Version (aus der Ausgabe des Validators), Optionen, Pakete, Ausnahmen mit Trefferzahl, Summe und je Beispiel (über die Datei dem `[[beispiele]]`-Eintrag zugeordnet) die Zahl der Fehler (error, fatal), davon begründete Ausnahmen, Warnungen und Hinweise (information), dazu die SHA-256 der Beispieldatei. Fehler und Warnungen stehen einzeln mit Stufe, Ort (FHIRPath, sonst Position), Zeile, Text und ggf. der Kennung der genutzten Ausnahme — sortiert, ohne Zeitstempel und ohne absolute Pfade; Einzelheiten, die von der Antwort eines fremden Servers abhängen (Nachladen eines Profils unter einer Beispiel-URL), werden vereinheitlicht.
- Exit-Code ≠ 0, wenn ein Fehler keine begründete Ausnahme ist; Ausnahmen ohne Treffer werden als Hinweis gemeldet. Ausnahmen nur für Grenzen der Prüfung (kein Terminologieserver, bekannte Werkzeug- oder Paketfehler) mit Begründung, nicht für Fehler der Beispiele oder Profile.
- `bauen` braucht kein Java: Es liest die Datei und zeigt das Ergebnis im Prüfbericht (Abschnitt „FHIR-Validierung (HL7 Validator x.y.z)“), unter „Abdeckung & Prüfung“ des gewählten Beispiels und als Kennzahl auf der Übersichtsseite; ohne Datei steht dort „noch nicht validiert“.
- Die CI validiert im Job `validieren` neu und prüft mit `git diff --exit-code`, dass `berichte/*.validierung.json` dem eingecheckten Stand entspricht.

## Lokale Pakete (Profile im Entwurf)

Profile, die (noch) in keinem veröffentlichten Paket liegen, kommen als lokales Paket ins Projekt — Beispiel `projekte/impfung/`:

```
projekte/impfung/sushi-config.yaml   Paket-Id, Version, Canonical, Abhängigkeiten (SUSHI-Format, FSHOnly)
projekte/impfung/fsh/*.fsh           Quelltext der Profile und Invarianten
projekte/impfung/paket/package/      erzeugt und eingecheckt: package.json, StructureDefinitions mit Snapshot
```

In `projekt.toml`: `lokale_pakete = ["paket"]` und `[fsh]` mit `quelle = "fsh"`, `paket = "paket"`. Das lokale Paket steht in Modell, Profilzuordnung, Auflösung und Validierung zur Verfügung (`-ig projekte/<id>/paket/package`); `holen` und die Sperrdatei überspringen es. Berichte nennen es mit `<id>#<version>` aus seiner `package.json`.

Neu erzeugen nach einer Änderung an `fsh/` oder `sushi-config.yaml` (SUSHI ≥ 3, `npm install -g fsh-sushi`; die Abhängigkeiten lädt SUSHI in `~/.fhir/packages`):

```bash
python3 -I werkzeuge/mx.py fsh impfung
python3 -I werkzeuge/mx.py validieren impfung
python3 -I werkzeuge/mx.py bauen
```

`mx.py fsh` kopiert `fsh/*.fsh` nach `input/fsh/` eines temporären Ordners (SUSHI erwartet diesen Aufbau), ruft `sushi build <tmp> --snapshot -o <tmp>/aus` auf, ersetzt die Ressourcen in `paket/package/` und schreibt `package.json` aus `sushi-config.yaml`. Von Hand dasselbe:

```bash
mkdir -p /tmp/impfung/input/fsh
cp projekte/impfung/fsh/*.fsh /tmp/impfung/input/fsh/ && cp projekte/impfung/sushi-config.yaml /tmp/impfung/
sushi build /tmp/impfung --snapshot -o /tmp/impfung/aus
cp /tmp/impfung/aus/fsh-generated/resources/*.json projekte/impfung/paket/package/
```

Die Snapshots braucht der Modellexplorer (Modell, Zuordnung, Strukturprüfung); ein Test prüft, dass `package.json` zur `sushi-config.yaml` passt.

## Informationsmodell eines MIO-IG (mio-baum)

Beispiel `projekte/epa-patient-summary/`: Das Modell kommt als gesicherte Quelle aus dem öffentlichen IG (`[[quellen]]` mit
Herkunfts-URL; `holen` lädt eine neue Quelle und nimmt ihre SHA-256 in die Sperrdatei auf), dazu `logikmodellpakete` für die
EHDS-Mappingprüfung:

```toml
logikmodellpakete = ["xtehr.eu.ehds.models#1.0.0"]

[informationsmodell]
art = "mio-baum"
quelle = "quellen/infomodell_js_treeview_<ig>.json"
referenzgruppe = "Profile"
```

Nur einen Ast des Modells zeigen und ihn über eine **Mappingtabelle** mit eigenen Profilen verbinden — Beispiel `projekte/impfung/`:

```toml
[informationsmodell]
art = "mio-baum"
quelle = "../epa-patient-summary/quellen/infomodell_js_treeview_epa-ps.json"
teilbaum = "Profile / ePA ePS Profile (in Erarbeitung) / Impfung"
profil_ergaenzen = true

[[informationsmodell.mappings]]
knoten = "Impfung / Impfstoff - Code/Bezeichnung / Code-Auswahl / SNOMED-CT-Code"
fhir = "PSImmunization.vaccineCode.coding:snomed"

[[informationsmodell.mappings]]
knoten = "Impfung / Verabreichtes Produkt / Datentyp"
ohne_ziel = "Hilfsknoten des Modells, kein eigenes Element."
```

`knoten` ist der Pfad im Teilbaum mit „ / “ zwischen den Namen (beim letzten Glied darf „ (Referenz)“ fehlen), `fhir` der
Profilname mit Elementpfad wie in den FHIR-Mappings eines gematik-Modells. Ein unbekannter Knoten bricht den Bau ab. Danach läuft
die Kette Modell → Profil → Instanz → Ansicht wie beim Laborbefund; `profil_ergaenzen` zeigt Must-Support-Elemente der gemappten
Profile, für die das Modell keinen Knoten hat, in der ausmodellierten Darstellung als „aus Profil“.

## Naheliegende nächste Projekte

| Projekt | Grundlage | Weg |
|---|---|---|
| Discharge Report | HL7 Europe Hospital Discharge Report (`hl7.fhir.eu.hdr` 1.0.0 in der Paketregistry) | `aus-profilen` mit der HDR-Composition als Einstieg, `darstellung = "dokument"`, `dokumente = ["erzaehltext"]`; Beispiele aus dem IG-Paket über `paket`/`einstieg` oder als Datei |
| Patient Summary der ePA | gematik-IG zur ePA-Patient-Summary, sobald als Paket in der Registry | wie `patient-summary`; ⚠ der Ballot liegt bisher nur als Download auf der IG-Seite vor, nicht in der Registry — dann über `[[quellen]]` oder einen eigenen Paket-Eintrag in der Sperrdatei mit URL |
| Weitere gematik-IGs mit Informationsmodell | IG mit `infomodell_js_treeview_*.json` | `gematik-baum` wie `laborbefund`; `referenzgruppe` auf den Namen der Gruppe „Referenzierte Profile“ des Modells setzen |
