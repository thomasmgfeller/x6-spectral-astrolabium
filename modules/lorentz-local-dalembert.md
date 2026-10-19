# Lokaler d’Alembertian: intrinsischer Phase-1/2-Pilot

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: c58cc26adb2b4a646e3940e417351040b5dc9ff0

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/README.md)

## Dokumentierte Aussage

Intrinsische längste Ketten und Kausalüberlappungs-Nachbarschaften, BK-Operator und Produktidentitäts-Metriktest in 2+1 Minkowski implementiert. Protokoll und Quellen vor Testdaten öffentlich fixiert. 48 getrennte Testwolken vollständig nachgerechnet. Bei höchster Dichte nur 3/16 verwendbare Nachbarschaften; relative Metrik-RMS-Fehler 3,110 mit glatten und 5,524 mit intrinsischen Feldern (Grenze 0,5). Softwarekontrollen bestehen, fachliche Abnahme scheitert. Keine 3+1-, Konvergenz- oder Krümmungsfreigabe. Nachtrag 19.10.2026: 48 frische gepaarte Testwolken prüfen die Eignungsfilterung vor der 64-Anker-Begrenzung. Bei höchster Dichte steigt Verfügbarkeit 2/16 → 16/16, wahrer Kappen-Recall 11,5% → 94,9%; Auswahlpräzision nur 68,3%. Metrik-RMS 7,326, mit exakter Abstandskappe 6,012, jeweils über 0,5. Alle neuen Wolken vollständig wiederholt; bessere Abdeckung ist keine Metrikfreigabe.

- [research/lorentz_local_dalembert/PHASE12_RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/PHASE12_RESULTS.md): Befund, Verfügbarkeit, Auswahl- und Randfehler sowie Grenzen des HOLD.
- [research/lorentz_local_dalembert/phase12/PROTOCOL.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/phase12/PROTOCOL.md): Vor Entwicklungs- und Testdaten öffentlich fixierter Vertrag.
- [research/lorentz_local_dalembert/phase12/IMPLEMENTATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/phase12/IMPLEMENTATION.md): Nach Entwicklungsdaten, vor Testdaten fixierte Umsetzung und Auswertung.
- [research/lorentz_local_dalembert/phase12/results/execution.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/phase12/results/execution.json): Alle Seeds, Rohdatenhashes, Quellenfreeze und gemessene Kosten.
- [research/lorentz_local_dalembert/phase12/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/phase12/results/summary.json): Vollständige Kennzahlen, Unsicherheiten und Gates.
- [research/lorentz_local_dalembert/phase12/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/phase12/VERIFICATION.json): Vollständiger lokaler numerischer Replay; alle 48 Koordinatenhashes identisch.
- [research/lorentz_local_dalembert/anchor_audit/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/RESULTS.md): Gepaarter Suchvergleich, Fehlselektionen, Metrikverschlechterung und nächste Momentendiagnose.
- [research/lorentz_local_dalembert/anchor_audit/PROTOCOL.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/PROTOCOL.md): Vor neuen Daten öffentlich fixierter isolierter Ankersuchvergleich.
- [research/lorentz_local_dalembert/anchor_audit/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/results/summary.json): 48 frische Wolken, Unsicherheit, gemeinsame Teilmenge und Abdeckungskriterien.
- [research/lorentz_local_dalembert/anchor_audit/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/research/lorentz_local_dalembert/anchor_audit/VERIFICATION.json): Vollständiger Replay der 48 neuen Testwolken; 48 lokale Koordinatenhashes identisch.

## Reproduzieren

Python 3.12, NumPy 2.3.5, SciPy 1.17.0, C++17-Compiler g++ und vollständige Git-Historie. Originalfreeze a4ff90306827f6df99048bd2fce61ef96a758f19 und Ankersuchfreeze 6f61cf0b525b9ce4e5fa81bf91be185014b7dfd7 müssen verfügbar sein.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-local-dalembert
cd x6-lorentz-local-dalembert
git checkout --detach c58cc26adb2b4a646e3940e417351040b5dc9ff0
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/phase12/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/anchor_audit/verify_audit.py
```

Erwartete Ausgabe: Zwei vollständige PASS_NUMERICAL_REPLAY-Prüfungen: 48 ursprüngliche und 48 frische Ankersuch-Testwolken. Neues Ergebnis ANCHOR_COVERAGE_IMPROVED, wissenschaftlich weiter HOLD_PHASE3. Koordinatenhashes werden getrennt berichtet.

## Offene Prüfung

Zeit- und Raummomente der Schablone getrennt diagnostizieren: Kettenskala, Schalenstreuung, Geodätenrichtung, Winkelbesetzung und Randbeiträge. Neue intrinsische Korrektur erst nach Entwicklung, öffentlichem Quellenfreeze und frischen Testseeds. HOLD_PHASE3 und BD-C2-NO_GO bleiben bestehen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
