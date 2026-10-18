# Lorentz: vollständige n=7-Prüfung und Widerlegung von H7

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 78a150f27fdf52187d140f9fcf440ce29c89cb48

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_n7_complete/README.md)

## Dokumentierte Aussage

Vollständige exakte Prüfung von F0+W_future+W_past bis n=7. Bei n=7 bleiben zwei nichtisomorphe Paare der Höhe drei; die Hypothese ist widerlegt. Zweiter Enumerator prüft alle 2^21 oberen Binärmatrizen, 96.428 natürliche Beschriftungen und 2.045 Klassen. Insgesamt 2.450 Repräsentanten und 7.350 exakte Polynome. D trennt n≤7, ersetzt aber nicht die skalare Hypothese. Keine physische Validierung oder externe Begutachtung.

- [research/lorentz_n7_complete/results/RESULTS.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_n7_complete/results/RESULTS.json): Vollständiges negatives Ergebnis, Quellbindung und alle Größenklassen.
- [research/lorentz_n7_complete/results/independent-results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_n7_complete/results/independent-results.json): Algorithmisch getrennte Enumeration, Isomorphiesuche, natürliche Multiplizitäten und exakte Determinanteninterpolation.
- [research/lorentz_n7_complete/COUNTEREXAMPLES.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_n7_complete/COUNTEREXAMPLES.md): Beide minimalen n=7-Paare mit Matrizen und Polynomen; elementarer Nichtisomorphiebeweis und isolierte Erweiterungen für alle n≥7.
- [research/lorentz_n7_complete/freeze.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/research/lorentz_n7_complete/freeze.json): Vor dem vollständigen Lauf veröffentlichte Quellhashes; prospektiver Arbeitsablauf, keine externe Präregistrierung.

## Reproduzieren

Python 3.12 unter Linux/POSIX, nur Standardbibliothek. Kein Netzwerk oder Wolfram-Zugang für die Rechnung.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-n7-complete
cd x6-lorentz-n7-complete
git checkout --detach 78a150f27fdf52187d140f9fcf440ce29c89cb48
python3 -O research/lorentz_n7_complete/run.py --verify research/lorentz_n7_complete/results
```

Erwartete Ausgabe: Exit 0, PASS_REPRODUCED_EXACT_COUNTERCHECK mit REFUTED_BY_COUNTEREXAMPLE. 2.045 n=7-Ordnungen, 2.043 primäre Signaturklassen, zwei vollständig gespeicherte Restpaare. 17 Kontrollgruppen einschließlich 16 Zurückweisungen.

## Offene Prüfung

Externe Replikation und strukturelle Analyse der beiden minimalen Kollisionsklassen. Eine neue begrenzte Aussage vor der nächsten Suche festlegen; der unveränderte skalare Ansatz ist bereits widerlegt.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
