# CSPP v0.24 – Gate-Neubewertung nach der globalen Bilanz

**Schritt 3 ist abgeschlossen. METHOD und G1 bleiben HOLD.** Die vollständige
v0.23-Restbilanz qualifiziert weder die Genauigkeit noch ein frisches
Bestätigungsensemble. Der nächste Hauptweg ist ein ausdrücklich geänderter
skalarer Kandidat mit deterministischer Kontroll- und Stabilitätsprüfung.
Dieser neue Kandidat ist hier noch nicht gewählt oder ausgeführt.

## Ergebnisse

- Über 99,9999 % des aktuellen Restzertifikats entfallen auf die nahe
  Lichtkegelhülle. Die ausgewiesenen Grenzen sind keine beobachteten Fehler.
- Selbst bei hypothetisch entferntem unendlichem Zertifikat bleibt die
  unveränderte endliche Majorante beim etwa 477- bis 549-Fachen von 0,001.
  Dies ist eine Diagnose des Beweisinstruments, keine Fehleruntergrenze.
- Die uniforme aktive Hülle liefert unter dem idealen Poisson-Gesetz
  eine zusätzliche unbedingte L1-Kontrolle der vollen KG-History-Diagnose.
  Gemeinsame Momente, Kovarianz und statistische Zulassung folgen daraus nicht.
- Der übernommene Gauß-Zeuge aus v0.15 schließt für die unveränderte feste
  Zelle eine reine Gebietsreparatur weiterhin aus: relativer Bias > 0,417
  für jedes reelle H >= 4. Die gesamte Operatorfamilie wird nicht verworfen.
- Alle sechs v0.14-Methodenkriterien bleiben verbindlich. Beide alten
  Kandidaten bleiben für einen Bestätigungslauf nicht zugelassen.

Keine neuen Poissonwolken, Zufallsaufrufe, Seeds, Operatorparameter,
Alpha-Werte, Powerziele oder Stichprobenumfänge. Keine neue Bestätigungsstudie.

## Inhalt und Reproduktion

- `PROOF.md`: Herleitung, Geltungsbereich und Gegenbeispiele.
- `NEXT_WORK_PACKAGE.md`: vorbereiteter nächster Arbeitsauftrag.
- `PROTOCOL.json`, `STATUS.json`, `NEXT_STEPS.json`: maschinenlesbare Grenzen.
- `PROVENANCE.json`, `evidence/`: 34 gegen Main verifizierte Eingaben und Baum.
- `results/`: vier numerische Ergebnisdateien; `REPLAY.json`: Bytevergleich.
- `report/Gate_Neubewertung_Globale_Bilanz_v0_24.pdf`: deutscher Ergebnisbericht.
- `PACKAGE.json`, `SHA256SUMS`: Paketinventar und Hashes.

Getestet mit Python 3.12.14, python-flint 0.8.0.
Im entpackten Verzeichnis:

```sh
python3 -m pip install -r requirements.txt
python3 reproduce.py
```

Nur Prüfungen bestehender Resultate: `python3 reproduce.py --quick`.
Der volle Lauf reproduziert vier Dateien isoliert und verlangt Byteidentität;
er lässt die Originaldateien unverändert. Die früheren Gaußquadraturen werden
nicht erneut gerechnet, sondern ihre unveränderten Einschließungen neu zur
kontinuierlichen H-Abdeckung zusammengesetzt. Die fünf v0.23-Resultate werden
gegen deren Replay-Hashes kontrolliert, nicht als v0.24-Neurechnung ausgegeben.

Die Kontrollen decken 16 globale Zerlegungen, 258 übernommene H-Stützstellen,
zwölf unabhängige Poisson-PGF-Kontrollen, 60 rationale Gegenbeispielidentitäten
und zwei Kovarianz-Vorzeichenkontrollen ab. Ein wissenschaftliches Peer Review
und eine Beweisassistent-Verifikation wurden nicht durchgeführt.

Der Bericht lässt sich mit `python3 build_report.py` neu erstellen
(ReportLab 4.4.9 und DejaVu Sans erforderlich). `python3 package.py` erzeugt
das ZIP mit festen Archivzeitstempeln und überprüft seine Bytes.

## Herkunft und Veröffentlichung

Basis ist Main nach PR #155, Commit
`0edb8e02aa3dbf5a1b827d7c9aa82385e056e817` in
https://github.com/thomasmgfeller/x6-spectral-astrolabium .
Die projektspezifischen Ergebnisse und Primärquellen sind in `PROOF.md`
einzeln eingeordnet. Stand: 29. Oktober 2026.

Dieses v0.24-Paket ist fertiggestellt; GitHub-Publikation und Merge sind
in diesem Arbeitsschritt noch nicht ausgeführt.
