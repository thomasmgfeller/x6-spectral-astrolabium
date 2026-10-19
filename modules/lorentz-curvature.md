# Krümmungsbenchmark: Empfindlichkeit und Dichteverwechslung

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 4a6fe9c383e56b5a26f286fba6aa6d8c9263308a

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_curvature/README.md)

## Dokumentierte Aussage

8.702 Ordnungen nach öffentlich fixiertem Prüfvertrag. Im primären de-Sitter-Fall N=128, h=1,25 warnt C2/C3/C4 in 118/512 Fällen, die längste Kette in 5/512; beide verfehlen das Empfindlichkeitsziel. 3.072 konforme Dichtezwillinge bestätigen dieselbe Ordnung trotz verschiedener Krümmung. Keine universelle Krümmungsidentifikation bei unbekannter Beprobungsdichte, keine physische Planck-Uhr und keine fortlaufende Testgarantie.

- [research/lorentz_curvature/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_curvature/RESULTS.md): Alle zwölf Zielzellen, vorab festgelegte Hauptentscheidung, Unsicherheit und exakte Dichteverwechslung.
- [research/lorentz_curvature/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_curvature/contract.json): Unveränderter Vertrag aus dem öffentlichen Quellenstand 31cfd8c vor dem ersten Ziellauf.
- [research/lorentz_curvature/results/verification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_curvature/results/verification.json): 8.702 volle Ordnungen, 26.106 unabhängige Kettenzählungen, 12.288 Ränge, 3.072 gekoppelte Zwillinge und 1.024 abgewiesene Relationsfehler.
- [research/lorentz_curvature/results/replay.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_curvature/results/replay.log): Vollständiger interner Replay aller Seeds, Relationsbytes, Koordinatenhashes und wissenschaftlichen Ausgaben; keine externe Replikation.
- [research/lorentz_curvature/PORTABILITY.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_curvature/PORTABILITY.md): Erster CI-Replay scheiterte am Koordinatenhash. Nachträgliche vollständige NumPy-Gegenprüfung: maximale Abweichung 2,22e-16, alle Relationen identisch. Originalquellen unverändert; zusätzlicher begrenzter Replay separat ausgewiesen.
- [research/lorentz_curvature/results/portable-replay.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/4a6fe9c383e56b5a26f286fba6aa6d8c9263308a/research/lorentz_curvature/results/portable-replay.log): Ergänzter vollständiger Replay mit 8.696 konkret geprüften Hashvarianten und sechs Originalhashes; unbekannte Varianten abgewiesen.

## Reproduzieren

Python 3.12 unter Linux/POSIX; NumPy 2.3.5, SciPy 1.17.0 und vollständige Git-Historie. Getrennte temporäre Reproduktion; pro Ziellauf 600 Sekunden und 2 GiB. N=64/128 ist fest, also bedingte Poisson-Beprobung.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-curvature
cd x6-lorentz-curvature
git checkout --detach 4a6fe9c383e56b5a26f286fba6aa6d8c9263308a
python3 -m pip install -r research/lorentz_curvature/requirements.txt
python3 -B research/lorentz_curvature/selftest.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_curvature/reproduce_portable.py
```

Erwartete Ausgabe: PASS_ARCHIVED_EVIDENCE und PASS_PORTABLE_CURVATURE_REPLAY. Nur Original- oder konkret gegengeprüfte Koordinatenhashes werden akzeptiert; unbekannte Varianten scheitern. Der ursprüngliche strenge Replay bleibt erhalten. Wissenschaftlich weiterhin PRIMARY_SENSITIVITY_NOT_ESTABLISHED für beide Methoden und NOT_IDENTIFIABLE_WITH_UNRESTRICTED_SAMPLING_DENSITY.

## Offene Prüfung

Externe Replikation. Ein Demonstrator muss Modellabweichungswarnungen und die Dichtezwillinge sichtbar trennen. Vor einer neuen Leistungsstudie unabhängiges Wissen über Beprobung/Volumen und eine identifizierbare geometrische Zielgröße festlegen; kein nachträgliches Retuning dieses Versuchs.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
