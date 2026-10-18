# Eigenzeit v0.2: Gültigkeitsbereich und Informationsbedarf

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_proper_time_validity/README.md)

## Dokumentierte Aussage

1.176 festgelegte Modell-/Budget-/Intervallkombinationen direkt berechnet. Alle 714 Kombinationen innerhalb ihrer Modellklasse erreichen mindestens 95% Überdeckung; 192 erfüllen zusätzlich das Präzisionsziel, 522 bleiben zu unpräzise. 462 Kombinationen liegen ausserhalb der jeweils vorausgesetzten Klasse. Extern begrenzte Dichtefehler erlauben konservative flache Eigenzeitintervalle, können aber eine irreduzible Präzisionsgrenze erzeugen. Keine allgemeine Krümmungsqualifikation.

- [research/lorentz_proper_time_validity/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_proper_time_validity/RESULTS.md): Gültigkeitskarte, Budgettabelle, Fehlpräzision bei selektiv fehlenden Ereignissen und verbleibende Grenzen.
- [research/lorentz_proper_time_validity/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_proper_time_validity/DERIVATION.md): Exakte Binomialmodelle, bekannte de-Sitter-Familie und konservative Transformation für extern begrenzte Intensitätsverhältnisse.
- [research/lorentz_proper_time_validity/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_proper_time_validity/contract.json): Öffentlicher Quellenstand 67dc770 vor der ersten Zielgitter-Auswertung.
- [research/lorentz_proper_time_validity/ARCHIVE.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_proper_time_validity/ARCHIVE.json): Prüfsumme und Inventar aller unveränderten Originalausgaben im ZIP.
- [research/lorentz_proper_time_validity/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1/research/lorentz_proper_time_validity/VERIFICATION.json): Getrennte Integral-/CDF-Gegenprüfung aller 1.176 Zellen und vollständiger Replay.

## Reproduzieren

Python 3.12, Linux/POSIX, gepinnte NumPy-/SciPy-/Matplotlib-Versionen und vollständige Git-Historie. Numerischer Ziellauf: 600 Sekunden und 2 GiB. Drei BLAS/OpenMP-Threadvariablen vor Python auf 1 setzen.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-proper-time-validity
cd x6-lorentz-proper-time-validity
git checkout --detach e6a5bce4cafe44ddb929da3ae32d9afa4d64eca1
python3 -m pip install -r research/lorentz_proper_time_validity/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research/lorentz_proper_time_validity/reproduce.py
```

Erwartete Ausgabe: PASS_FULL_PROPER_TIME_VALIDITY_REPLAY. 1.176 deterministische Kombinationen; vollständige Reproduktion mit unveränderten Forschungsquellen. Keine neuen Punktwolken oder realen Messungen.

## Offene Prüfung

Externe Replikation und unabhängig begründete Dichte-/Erfassungsgrenzen für eine konkrete Datenquelle. Die getrennten Module lorentz-de-sitter-information und lorentz-de-sitter-c2 enthalten inzwischen Kovarianzplanung und konservative modellbedingte Krümmungsintervalle; präzise gekrümmte Uhr weiterhin offen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
