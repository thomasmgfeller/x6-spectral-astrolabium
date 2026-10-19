# Eigenzeit: Referenz, Fehlergrenzen und sequenzielle Diagnose

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

[Eigenzeit-Labor öffnen →](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/proper-time.html)

## Quelle

Branch: main

Commit: 26432e3d4cde20adabb510f17d5639891f4ac642

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_proper_time_publication/README.md)

## Dokumentierte Aussage

Bedingte Eigenzeit-Referenz im bekannten flachen Modell: ursprüngliche 1+1-Qualifikation mit RMSE 0,031614; 49.152 neue Punktwolken prüfen d=2,3,4 und endliche Fehlergrenzen. Zeituniformes Nachbeproben mit expliziter Stoppregel und einmaliger Kettendiagnostik. Kein universeller Zeit-, Krümmungs- oder industrieller Leistungsnachweis; lokale Quellenfixierung vor den neuen Ziehungen, keine öffentliche Präregistrierung.

- [research/lorentz_proper_time/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_proper_time/RESULTS.md): Ursprünglich 6.912 Ordnungen: Hauptvergleich qualifiziert, größte exakt abgeglichene Zusatzkontrolle mit nur 63 statt 128 Paaren offen.
- [research/lorentz_proper_time_domain/results/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_proper_time_domain/results/RESULTS.md): CONDITIONAL_FLAT_MODEL_CHECK_PASSED; 24 Zellen, Binomialintervalle und Nullzählungsgrenze.
- [research/lorentz_proper_time_domain/results/verification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_proper_time_domain/results/verification.json): Interne Prüfung aller 49.152 Rohzählungen, Quellenbindung, Quantilinversion und zwölf voller Relationsgegenprüfungen.
- [research/lorentz_proper_time_sequential/results/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_proper_time_sequential/results/RESULTS.md): DECLARED_SEQUENTIAL_REFERENCE_CHECK_PASSED; getrennte Zählblock- und Geometriekontrollen, Budgetabbruch und Dichtestörung ausdrücklich ausgewiesen.
- [research/lorentz_proper_time_sequential/results/verification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_proper_time_sequential/results/verification.json): Interne skalare Stream-Replays, 2.048 Rang-p-Werte und geometrische Integration; keine externe Replikation.
- [research/lorentz_proper_time_sequential/EXECUTION_HISTORY.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_proper_time_sequential/EXECUTION_HISTORY.md): Erhaltener Erstlauf mit JSON-Serialisierungsfehler; einzige Typkonvertierung und identische Zählblöcke nach Wiederholung.
- [research/lorentz_proper_time_publication/planning.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/research/lorentz_proper_time_publication/planning.json): Analytische Feststichprobenbeispiele für unter 10% relativen Fehler bei tau/T=0,1 in 4D; getrennt von sequenziellen Budgetmedianen.

## Reproduzieren

Python 3.12 unter Linux/POSIX; NumPy 2.3.5 und SciPy 1.17.0. Reproduktion in temporären Verzeichnissen; nach Installation kein externer Dienst. Bekannte Dimension, Zeitskala und uniformes unabhängiges Beprobungsgesetz für die statistische Aussage erforderlich.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-proper-time
cd x6-lorentz-proper-time
git checkout --detach 26432e3d4cde20adabb510f17d5639891f4ac642
python3 -m pip install -r research/lorentz_proper_time_sequential/requirements.txt
OPENBLAS_NUM_THREADS=1 python3 -B research/lorentz_proper_time_publication/replay.py
python3 research/lorentz_proper_time_publication/planning.py
```

Erwartete Ausgabe: PASS_PUBLISHED_EVIDENCE_AND_REPLAY nach Prüfung beider neuen Archive, vollständiger Wiederholung, Rohdaten-/Ergebnisvergleich, Quellenfixierung und Reparaturhistorie. Der ursprüngliche 1+1-Versuch hat seinen separat dokumentierten Reproduktionsweg.

## Offene Prüfung

Externe Replikation des deklarierten Modells. Für eine Erweiterung zuerst eine bestimmte Geometrie-/Beprobungsklasse, unabhängige Maßstabskalibrierung und Modellfehlergrenze festlegen. Kettenwarnungen erlauben ohne bekannte Beprobung keine eindeutige Krümmungsdiagnose.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
