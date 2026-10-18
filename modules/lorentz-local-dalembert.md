# Lokaler d’Alembertian: intrinsischer Phase-1/2-Pilot

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: e947dfbdd49890dcb119940548537d1db59272c2

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/README.md)

## Dokumentierte Aussage

Intrinsische längste Ketten und Kausalüberlappungs-Nachbarschaften, BK-Operator und Produktidentitäts-Metriktest in 2+1 Minkowski implementiert. Protokoll und Quellen vor Testdaten öffentlich fixiert. 48 getrennte Testwolken vollständig nachgerechnet. Bei höchster Dichte nur 3/16 verwendbare Nachbarschaften; relative Metrik-RMS-Fehler 3,110 mit glatten und 5,524 mit intrinsischen Feldern (Grenze 0,5). Softwarekontrollen bestehen, fachliche Abnahme scheitert. Keine 3+1-, Konvergenz- oder Krümmungsfreigabe.

- [research/lorentz_local_dalembert/PHASE12_RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/PHASE12_RESULTS.md): Befund, Verfügbarkeit, Auswahl- und Randfehler sowie Grenzen des HOLD.
- [research/lorentz_local_dalembert/phase12/PROTOCOL.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/PROTOCOL.md): Vor Entwicklungs- und Testdaten öffentlich fixierter Vertrag.
- [research/lorentz_local_dalembert/phase12/IMPLEMENTATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/IMPLEMENTATION.md): Nach Entwicklungsdaten, vor Testdaten fixierte Umsetzung und Auswertung.
- [research/lorentz_local_dalembert/phase12/results/execution.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/results/execution.json): Alle Seeds, Rohdatenhashes, Quellenfreeze und gemessene Kosten.
- [research/lorentz_local_dalembert/phase12/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/results/summary.json): Vollständige Kennzahlen, Unsicherheiten und Gates.
- [research/lorentz_local_dalembert/phase12/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/research/lorentz_local_dalembert/phase12/VERIFICATION.json): Vollständiger lokaler numerischer Replay; alle 48 Koordinatenhashes identisch.

## Reproduzieren

Python 3.12, NumPy 2.3.5, SciPy 1.17.0, C++17-Compiler g++ und vollständige Git-Historie. Quellenfreeze a4ff90306827f6df99048bd2fce61ef96a758f19 muss verfügbar sein.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-local-dalembert
cd x6-lorentz-local-dalembert
git checkout --detach e947dfbdd49890dcb119940548537d1db59272c2
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/phase12/verify.py
```

Erwartete Ausgabe: PASS_NUMERICAL_REPLAY für 48 Testwolken; fachlich HOLD_PHASE3. Koordinatenhashes werden getrennt berichtet. Der historische Vortest bleibt PASS_ASSEMBLY_ONLY.

## Offene Prüfung

Ankersuchabdeckung, Schalenpopulation und Randrobustheit zunächst auf Entwicklungsdaten verbessern. Neuer öffentlicher Vertrag und frische Testseeds für erneute flache Abnahme; keine Phase 3. Früherer BD-C2-NO_GO bleibt unverändert.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
