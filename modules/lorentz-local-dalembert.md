# Lokaler d’Alembertian: intrinsischer Phase-1/2-Pilot

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 26432e3d4cde20adabb510f17d5639891f4ac642

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/README.md)

## Dokumentierte Aussage

Intrinsische längste Ketten und Kausalüberlappungs-Nachbarschaften, BK-Operator und Produktidentitäts-Metriktest in 2+1 Minkowski implementiert. Protokoll und Quellen vor Testdaten öffentlich fixiert. 48 getrennte Testwolken vollständig nachgerechnet. Bei höchster Dichte nur 3/16 verwendbare Nachbarschaften; relative Metrik-RMS-Fehler 3,110 mit glatten und 5,524 mit intrinsischen Feldern (Grenze 0,5). Softwarekontrollen bestehen, fachliche Abnahme scheitert. Keine 3+1-, Konvergenz- oder Krümmungsfreigabe. Nachtrag 19.10.2026: 48 frische gepaarte Testwolken prüfen die Eignungsfilterung vor der 64-Anker-Begrenzung. Bei höchster Dichte steigt Verfügbarkeit 2/16 → 16/16, wahrer Kappen-Recall 11,5% → 94,9%; Auswahlpräzision nur 68,3%. Metrik-RMS 7,326, mit exakter Abstandskappe 6,012, jeweils über 0,5. Alle neuen Wolken vollständig wiederholt; bessere Abdeckung ist keine Metrikfreigabe. Zweiter Nachtrag 19.10.2026: 48 weitere frische Wolken prüfen alle acht Kombinationen aus Zeitstützpunkt-, Schalen- und Richtungskontrolle. Bei höchster Dichte sinkt der Metrik-RMS von 7,387 auf 2,267; mit exakter Abstandskappe von 5,893 auf 1,002. Schalen- und Richtungsbeiträge dominieren die diagnostische Fehlerreduktion. Alle Eingriffe nutzen Simulationskoordinaten; beide Restfehler liegen über 0,5. Bei niedriger Dichte kann die Gesamtkontrolle verschlechtern. Vollständiger Replay aller neuen Wolken bestanden. Dritter Nachtrag 19.10.2026: Intrinsische inverse quadratische Schalengewichte aus kausalen Intervallzählungen auf weiteren 48 frischen Wolken getestet. Bei höchster Dichte Metrik-RMS 7,089 → 3,765 und normierte affine Drift 3,692 → 2,882, bei 16/16 verfügbaren Wolken. Alle drei vorab festgelegten Verbesserungsgrenzen bestanden. Richtige Lorentz-Signatur nur 8/16, Fehler über 0,5; keine flache oder Krümmungsqualifikation. Bekannte Dichte und 2+1 Minkowski bleiben Voraussetzungen. Vierter Nachtrag 19.10.2026: Gemeinsame Referenzrichtungen aus kausalen Intervallzählungen auf 48 weiteren frischen Wolken geprüft. Bei höchster Dichte Metrik-RMS 4.840 → 3.709, normierte affine Drift 3.271 → 3.085; 16/16 verfügbar, 14/16 richtige Signaturen. Vorab festgelegter Gesamtentscheid COMMON_AXIS_HOLD. Keine flache oder Krümmungsqualifikation; bekannte Dichte und 2+1 Minkowski bleiben Voraussetzungen.

- [research/lorentz_local_dalembert/PHASE12_RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/PHASE12_RESULTS.md): Befund, Verfügbarkeit, Auswahl- und Randfehler sowie Grenzen des HOLD.
- [research/lorentz_local_dalembert/phase12/PROTOCOL.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/phase12/PROTOCOL.md): Vor Entwicklungs- und Testdaten öffentlich fixierter Vertrag.
- [research/lorentz_local_dalembert/phase12/IMPLEMENTATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/phase12/IMPLEMENTATION.md): Nach Entwicklungsdaten, vor Testdaten fixierte Umsetzung und Auswertung.
- [research/lorentz_local_dalembert/phase12/results/execution.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/phase12/results/execution.json): Alle Seeds, Rohdatenhashes, Quellenfreeze und gemessene Kosten.
- [research/lorentz_local_dalembert/phase12/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/phase12/results/summary.json): Vollständige Kennzahlen, Unsicherheiten und Gates.
- [research/lorentz_local_dalembert/phase12/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/phase12/VERIFICATION.json): Vollständiger lokaler numerischer Replay; alle 48 Koordinatenhashes identisch.
- [research/lorentz_local_dalembert/anchor_audit/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/anchor_audit/RESULTS.md): Gepaarter Suchvergleich, Fehlselektionen, Metrikverschlechterung und nächste Momentendiagnose.
- [research/lorentz_local_dalembert/anchor_audit/PROTOCOL.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/anchor_audit/PROTOCOL.md): Vor neuen Daten öffentlich fixierter isolierter Ankersuchvergleich.
- [research/lorentz_local_dalembert/anchor_audit/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/anchor_audit/results/summary.json): 48 frische Wolken, Unsicherheit, gemeinsame Teilmenge und Abdeckungskriterien.
- [research/lorentz_local_dalembert/anchor_audit/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/anchor_audit/VERIFICATION.json): Vollständiger Replay der 48 neuen Testwolken; 48 lokale Koordinatenhashes identisch.
- [research/lorentz_local_dalembert/moment_audit/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/moment_audit/RESULTS.md): Alle acht Momentenkontrollen, signierte Fehlerbilanz, Unsicherheit und verbleibender Fehler.
- [research/lorentz_local_dalembert/moment_audit/PROTOCOL.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/moment_audit/PROTOCOL.md): Vor Entwicklung öffentlich fixierte Zeit-, Schalen- und Richtungskontrollen.
- [research/lorentz_local_dalembert/moment_audit/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/moment_audit/results/summary.json): 48 frische Wolken; vollständiger faktorieller Vergleich und vorab fixierter Diagnoseentscheid.
- [research/lorentz_local_dalembert/moment_audit/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/moment_audit/VERIFICATION.json): Vollständiger Replay: alle 48 neuen Wolken und Koordinatenhashes identisch.
- [research/lorentz_local_dalembert/volume_shell/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/volume_shell/RESULTS.md): Alle fünf Gewichtsarme, affine Drift, Feldantworten und Grenzen der intrinsischen Verbesserung.
- [research/lorentz_local_dalembert/volume_shell/PROTOCOL.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/volume_shell/PROTOCOL.md): Vor Entwicklung veröffentlichter Intervallgewichtsvergleich mit festem Driftkriterium.
- [research/lorentz_local_dalembert/volume_shell/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/volume_shell/results/summary.json): 48 frische Wolken, gepaarte Kennzahlen und drei primäre Entscheidungskriterien.
- [research/lorentz_local_dalembert/volume_shell/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/volume_shell/VERIFICATION.json): Vollständiger lokaler numerischer Replay; Bytehashgleichheit separat berichtet.
- [research/lorentz_local_dalembert/common_axis/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/RESULTS.md): Alle vier Referenzarme, erste/zweite Momente, Vergleich mit exakten Auswahlzeiten und Grenzen.
- [research/lorentz_local_dalembert/common_axis/PROTOCOL.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/PROTOCOL.md): Vor Entwicklung veröffentlichte gemeinsame Referenzregel und zwei feste Fehlergrenzen.
- [research/lorentz_local_dalembert/common_axis/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/results/summary.json): 48 frische Wolken mit gepaarten Kennzahlen und allen Entscheidungskriterien.
- [research/lorentz_local_dalembert/common_axis/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_local_dalembert/common_axis/VERIFICATION.json): Vollständiger lokaler numerischer Replay; Koordinaten-Bytehashgleichheit separat.

## Reproduzieren

Python 3.12, NumPy 2.3.5, SciPy 1.17.0, C++17-Compiler g++ und vollständige Git-Historie. Originalfreeze a4ff90306827f6df99048bd2fce61ef96a758f19 und Ankersuchfreeze 6f61cf0b525b9ce4e5fa81bf91be185014b7dfd7 müssen verfügbar sein. Momentenfreeze fe7dcd1dbf9c5844459fa138def6ef6fca7294ee wird zusätzlich benötigt. Intervallgewichtsfreeze 457ec4a3275d91117d9f771cf8f3bbe781a19eca wird zusätzlich benötigt. Referenzrichtungsfreeze 2afc821419fcefff6cd7da41928f3bb54b2f8976 wird zusätzlich benötigt.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-local-dalembert
cd x6-lorentz-local-dalembert
git checkout --detach 26432e3d4cde20adabb510f17d5639891f4ac642
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/phase12/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/anchor_audit/verify_audit.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/moment_audit/verify_moments.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/volume_shell/verify_volume.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/common_axis/verify_axis.py
```

Erwartete Ausgabe: Fünf vollständige PASS_NUMERICAL_REPLAY-Prüfungen mit je 48 Zielwolken: Originalpilot, Ankersuchaudit, Momentendiagnose, intrinsische Intervallgewichte und gemeinsame Referenzrichtungen. Neuer begrenzter Vergleich COMMON_AXIS_HOLD; wissenschaftlich weiterhin HOLD_PHASE3. Koordinaten-Bytehashes separat ausweisen; keine plattformübergreifende Bitidentität zugesichert.

## Offene Prüfung

Explizite gemeinsame Bedingungen für verschwindende erste Momente und korrekte zweite Momente untersuchen, einschliesslich Winkelbesetzung und Randbeiträgen. Die Referenzregel allein qualifiziert keinen Operator. Neue Kandidaten benötigen einen separaten öffentlichen Vertrag und frische Testdaten; keine nachträgliche Oracle-Auswahl. HOLD_PHASE3 und BD-C2 NO_GO bleiben bestehen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
