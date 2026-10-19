# Industrieller Datenvertrag: Paderborn-Machbarkeitspilot

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 6738f129ca31e56a88690a9d17941516ccefb321

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/experiments/industrial-pilot/README.md)

## Dokumentierte Aussage

Status: reproduzierbare Labor-Maschinenreferenz abgeschlossen (Bezeichnung präzisiert am 17.10.2026; Evidenz des Piloten vom 15.10.2026). Tatsächlich ausgeführte, reproduzierbare Sekundärauswertung realer Labormessungen: pro physischem Lager eine vor den Scores nach Metadaten gewählte Aufnahme; 16 Verwerfungen bleiben protokolliert. Drei feste klassische Referenzen. Hüllkurve: 4/4 beschädigte Evaluationslager erkannt, 1/2 gesunde mit Fehlalarm. Keine neue Filterleistung, 1-%-Fehlalarmgarantie oder industrielle Generalisierung.

- [experiments/industrial-pilot/evidence/pilot-report.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/experiments/industrial-pilot/evidence/pilot-report.json): Reproduzierbare Labor-Maschinenreferenz abgeschlossen: vollständige Scores, Schwellen und Entscheidungen für 20 festgelegte Laborlager; industrielle Bestätigung ausdrücklich offen.
- [experiments/industrial-pilot/evidence/replay-portability.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/experiments/industrial-pilot/evidence/replay-portability.json): Nach anfänglichem CI-Rundungsfehler: unveränderte eingefrorene Quellen und Ergebnisse, separater portabler Replay mit 13 Tests / 25 Negativkontrollen. Unstabile Evaluationsentscheidungen werden abgelehnt.
- [experiments/industrial-pilot/evidence/execution.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/experiments/industrial-pilot/evidence/execution.json): Historischer Erstlauf: Vertrag/Daten/Code öffentlich vor Scores fixiert; damals elf Pilottests, 23 Negativkontrollen und 25 unveränderte V1-Tests bestanden.
- [experiments/industrial-pilot/data/manifest.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/experiments/industrial-pilot/data/manifest.json): Originalarchiv-, MAT-, Signal- und NPZ-Hashes; Lager-IDs, Labels, Splits und sämtliche geprüften Wiederholungen.
- [experiments/industrial-pilot/data/LICENSE.txt](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/experiments/industrial-pilot/data/LICENSE.txt): Quellenzuordnung und CC-BY-NC-4.0-Bedingungen der Messdaten; kommerzielle Nutzung nicht freigegeben.
- [experiments/industrial-pilot/evidence/power-plan.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6738f129ca31e56a88690a9d17941516ccefb321/experiments/industrial-pilot/evidence/power-plan.json): 368-Sonderfall bestätigt; zusätzliche exakte bedingte Powerrechnung mit gepaarten Diskordanzen. Planungsannahmen sind keine Piloteffekt-Schätzungen oder freigegebene Industrie-Fallzahlen.

## Reproduzieren

Python 3.12, gepinnte NumPy/SciPy-Abhängigkeiten; nach Installation offline. Enthaltene fremde Messkanäle: CC BY-NC 4.0, ausschließlich nichtkommerzieller Pilot; eigener Code Apache-2.0. Keine absoluten Kalibrierbelege.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-industrial-pilot
cd x6-industrial-pilot
git checkout --detach 6738f129ca31e56a88690a9d17941516ccefb321
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experiments/industrial-pilot/replay.py
python3 experiments/industrial-pilot/test_pilot.py
```

Erwartete Ausgabe: REPLAY_PASS, Exit 0; 20 Lager, feste Splits 7/7/6, 13 Tests mit 25 Negativkontrollen. industrial_claim_supported=false und bestätigender V1-Vertrag NOT_READY.

## Offene Prüfung

Benannte industrielle Datenpartnerschaft/Zielpopulation, verwendbare Rechte, unabhängige Labels und ausreichende lager-/maschinenweise getrennte Daten. Vor bestätigendem Leistungsvergleich fachlich geprüften Vertrag samt Kandidat, Baseline, Schwellen, Power und unveränderten V1-Gates einfrieren; bei Clusterung vorab eigenes Design.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
