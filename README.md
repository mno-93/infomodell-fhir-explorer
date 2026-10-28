# Modellexplorer

Informationsmodell, FHIR-Profile, Beispielinstanzen, Anwenderansicht und Dokument — **auf Elementebene verknüpft**. Ein Klick auf ein Element in einer Darstellung zeigt in allen anderen, wo es vorkommt, und benennt, wo es fehlt.

```
Informationsmodell ──FHIR-Mapping──▶ Profilelement ──Zuordnung──▶ Instanzwert ──▶ Anwenderansicht
        │                                  │                          │          └▶ Dokument (Druck, PDF, Erzähltext)
        └── Anforderungen, Terminologie, Herkunft (LDT, Muster 10)    └── Verarbeitungsregeln
```

## Projekte

| Projekt | Grundlage | Informationsmodell | Beispiele |
|---|---|---|---|
| `laborbefund` | gematik `de.gematik.epa.laboratory` 1.0.0-ballot.1 | veröffentlicht, mit FHIR-Mappings; zusätzlich ausmodellierte Sicht | 3 aus dem Demo-PVS, 2 aus dem IG-Paket |
| `patient-summary` | HL7 Europe `hl7.fhir.eu.eps` 1.0.0-ballot | keins mit Mappings veröffentlicht — Struktur aus den Profilen abgeleitet | 2 aus dem Demo-PVS |
| `impfung` | Entwurf eines Impfeintrags nach EU Core (HL7 Europe Base 2.0.1) mit den EPS-Pflichtangaben; Profile als FSH im Projekt, nicht veröffentlicht | Teilbaum „Impfung“ des Modells der ePA Patient Summary; FHIR-Mappings aus einer Mappingtabelle des Projekts | 2 fiktive, für das Projekt erstellt (Erstdokumentation, Nachtrag aus dem Impfpass) |
| `epa-patient-summary` | MIO ePA Patient Summary, öffentlicher CI-Build ePS-0.0.1 (noch ohne FHIR-Profile) | veröffentlicht im CI-Build, ohne FHIR-Mappings, mit EHDS-Mapping auf die Xt-EHR-Logikmodelle 1.0.0 — geprüft wird dieses | keine (Begründung im Projekt) |

Die Prüfberichte je Projekt stehen in [`berichte/`](berichte/): Mappingprüfung (FHIR- bzw. EHDS-Mapping), Abdeckung, Strukturbefunde und das Ergebnis des HL7 Validators je Beispiel.

## Schnellstart

Python ab 3.12, sonst nichts. Für die Validierung zusätzlich Java (ab 17; die CI nutzt 21) und der HL7 FHIR Validator in der Version und mit der Prüfsumme aus `.github/workflows/ci.yml`; für den Bau genügt Python.

```bash
python3 -I werkzeuge/mx.py holen      # FHIR-Pakete aus der Registry nach .pakete/ und .validator/, Prüfung gegen sperrdatei.json
python3 -I werkzeuge/mx.py bauen      # ausgabe/index.html, ausgabe/<projekt>.html, berichte/<projekt>.md
python3 -I -m unittest discover -s tests
python3 -m http.server 8790 --directory ausgabe
```

Die Seiten sind eigenständig (Daten eingebettet, keine externen Abhängigkeiten) und lassen sich auch ohne Server öffnen. Der Link `…/laborbefund.html#yildiz-2026-07-02` öffnet ein bestimmtes Beispiel.

Weitere Befehle:

| Befehl | Wirkung |
|---|---|
| `mx.py pruefen` | belegte Elemente aller Beispiele gegen die Profile auflösen; Exit-Code ≠ 0 bei Befund |
| `mx.py validieren` | Beispieldateien mit dem HL7 FHIR Validator prüfen (Pakete und begründete Ausnahmen je Projekt; ohne Netz, nur mit dem gesperrten Paketbestand aus `holen`); Ergebnis nach `berichte/<projekt>.validierung.json` — einchecken |
| `mx.py fsh <projekt>` | lokales Paket eines Projekts aus FSH neu erzeugen (SUSHI nötig, siehe [`docs/NEUES_PROJEKT.md`](docs/NEUES_PROJEKT.md#lokale-pakete-profile-im-entwurf)) |
| `mx.py vertraulich` | versionierte Dateien gegen eingebaute und projektbezogene Muster prüfen |
| `mx.py holen --aktualisieren` | Sperrdatei neu schreiben, Quellen neu laden — nur bewusst, Änderung prüfen und einchecken. Neue Pakete und Quellen nimmt schon `holen` auf, ohne die vorhandenen neu zu laden |

## Bedienung

- **Vier Ansichten:** 1 Informationsmodell (oder abgeleitete Struktur) · 2 FHIR — Profil oder Instanz · 3 Anwenderansicht · 4 Dokument.
- **Verknüpfungsleiste** oben: Kette der Auswahl über alle Ansichten; fehlt ein Glied, wird es als Lücke markiert. Darunter Beschreibung, Codes, Herkunft und Anforderungen.
- **Zwei Markierungsstufen:** kräftig = genau dieser Wert, hell = dasselbe Element an anderer Stelle.
- **Informationsmodell referenziert oder ausmodelliert:** wie im IG oder mit jeder Referenz an ihrer Verwendungsstelle; Zyklen werden erkannt, Fundstellen mit ‹ › durchlaufen.
- **Terminologie:** Codes und Wertelisten des Modells als Tabelle mit Kopfzeilen; Wertelisten und Profilbindungen verlinkt auf ihre Originalseite, belegte Codes oben.
- **Legende:** Knopf im Kopf und Kurzlegende unter Modell und Profil erklären Zeichen und Farben — u. a. ● im Beispiel belegt, ↳ ausmodelliert, ↻ Zyklus, „aus Profil“ (nicht im Informationsmodell, aus dem FHIR-Profil ergänzt), S Must Support, IM Ziel eines Modell-Mappings. Esc schließt Fenster, dann Details, dann die Auswahl.
- **EHDS-Mapping:** Bei MIO-Modellen steht am Element sein Gegenstück im EHDS-Logikmodell (Xt-EHR) mit Link, Auflösung, Linkformat und Kontext; „E“ im Baum markiert Auffälligkeiten, ⊘ ein Element, das die Mappingtabelle bewusst ohne FHIR-Ziel lässt.
- **Abdeckung & Prüfung:** Mappingprüfung (FHIR- bzw. EHDS-Mapping), Werte ohne Modellelement, Strukturbefunde und FHIR-Validierung des gewählten Beispiels — Fehler und Warnungen des HL7 Validators mit Ort, Zeile und begründeter Ausnahme; ein Klick auf den Ort markiert den Wert in allen Ansichten. Die Übersichtsseite zeigt je Projekt die Kennzahl der Validierung.

## Direkt verlinken

Jede Ansicht hat eine eigene Adresse: Auswahl, Beispiel, Baumdarstellung und Reiter stehen im Fragment der URL und ändern sich mit jedem Klick. **Link kopieren** im Kopf legt die aktuelle Adresse in die Zwischenablage — zum Verschicken oder für Notizen.

| Teil | Bedeutung | Beispiel |
|---|---|---|
| `b` | Beispiel | `b=hoffmann-2026-08-12` |
| `im` | Element im Informationsmodell (Kennung aus dem IG, in den Details als „Kennung“ angezeigt) | `im=1627` |
| `k` | genau diese Fundstelle im ausmodellierten Baum (optional) | `k=a751d7dab` |
| `el` | Profilelement: Profil-id `/` Element-id | `el=observation-laboratory-study-dglp/Observation.value%5Bx%5D:valueQuantity.value` |
| `n` | Wert im Beispiel: Ressource `\|` JSON-Pfad (mehrfach möglich) | `n=Observation/obs-f81d4fae-0-0\|valueQuantity.value` |
| `v`, `f`, `d`, `info` | ausmodellierte Sicht, FHIR-Reiter Instanz, Dokumentansicht, Details aufgeklappt | `v=ausmodelliert&f=instanz&d=pdf&info=1` |

Beispiel: `laborbefund.html#b=hoffmann-2026-08-12&im=1627&info=1` öffnet den Befund, markiert „Wert“ in allen Ansichten und klappt die Details auf. Kennungen im Modell stammen aus dem IG; Fundstellen und die Elemente der aus Profilen abgeleiteten Struktur tragen Kennungen, die aus ihrem Pfad berechnet sind und bei einem Neubau gleich bleiben. Ein Verweis, der nicht mehr passt, wird im Kopf gemeldet. Die Kurzform `#<Beispiel>` gilt weiter.

## Reproduzierbar und konsistent

- **Sperrdatei** [`sperrdatei.json`](sperrdatei.json): je FHIR-Paket Herkunft und Inhalts-Hash über alle JSON-Dateien — ein frischer Download und ein vorhandener Cache sind gleich prüfbar. Die Pakete liegen in einem eigenen Cache `.pakete/`, nicht im gemeinsamen `~/.fhir/packages`, den andere Werkzeuge mit abweichenden Fassungen befüllen. Quellen von IG-Seiten liegen im Repository, ihre SHA-256 in der Sperrdatei.
- **Deterministischer Bau:** keine Zeitstempel, feste Reihenfolgen. Ein Test baut zweimal und vergleicht.
- **Berichte als Gegenprobe:** Die CI baut neu und bricht ab, wenn `berichte/` vom eingecheckten Stand abweicht.
- **Gleiche Regeln für alle Beispiele:** Profilzuordnung (inkl. Slices und enthaltener Ressourcen) und Strukturprüfung laufen über dieselben Funktionen; der HL7-Validator mit fester Version und Prüfsumme prüft jede Beispieldatei.
- **Validierungsergebnis im Projekt:** `mx.py validieren` schreibt `berichte/<projekt>.validierung.json` — sortiert, ohne Zeitstempel und absolute Pfade, Meldungstexte englisch (`-Duser.language=en -Duser.country=US`, `-locale en-US`), je Beispiel mit SHA-256 der Datei. `bauen` liest die Datei ohne Java; ein seit der Validierung geändertes Beispiel wird als veraltet gemeldet. Die CI validiert neu und bricht ab, wenn das Ergebnis vom eingecheckten Stand abweicht.

## Aufbau

```
projekte/<id>/projekt.toml     Projektkonfiguration: Pakete, Modellquelle, Darstellung, Beispiele, Validierung
projekte/<id>/quellen/         gesicherte Quellen (z. B. Informationsmodell und Verarbeitungsregeln eines IG)
projekte/<id>/beispiele/       Beispieldateien (Bundle oder Einzelressource)
projekte/<id>/fsh/, paket/     optional: Profile im Entwurf als FSH und das daraus erzeugte lokale Paket (eingecheckt)
werkzeuge/mx.py                Kommandozeile
werkzeuge/mx/                  Pakete, Pfadauflösung, Modell-Adapter, Zuordnung, Bau, Berichte, Validierung
web/explorer.html              eine Oberfläche für alle Projekte
berichte/                      erzeugte Prüfberichte und Validierungsergebnisse (eingecheckt)
tests/                         Tests
```

Neue Beispiele und Projekte: [`docs/NEUES_PROJEKT.md`](docs/NEUES_PROJEKT.md). Aufbau und Verknüpfungslogik: [`docs/AUFBAU.md`](docs/AUFBAU.md).

## Quellen und Daten

- Profile, Informationsmodell und Verarbeitungsregeln stammen aus veröffentlichten Implementation Guides (gematik, HL7 Europe) in den in `projekt.toml` genannten Versionen.
- Die Beispiele aus dem Demo-PVS (github.com/mno-93/demo-pvs) sind **fiktiv**; Personen, Einrichtungen und Nummern sind erfunden.
- Das Projekt `impfung` ist eine **Studie**: Entwurf eines Impfeintrags nach EU Core auf Grundlage veröffentlichter Pakete (HL7 Europe Base, EU Patient Summary, IPS, gematik-Ballot-Pakete), keine veröffentlichte Spezifikation. Seine Beispiele sind für dieses Projekt erstellt und fiktiv (Personen, PZN, Chargen, Handelsnamen).
- Kennzeichnung in Berichten und Doku: ⚠ = unbelegt · ▸ = Bewertung · ✦ = Vorschlag.
