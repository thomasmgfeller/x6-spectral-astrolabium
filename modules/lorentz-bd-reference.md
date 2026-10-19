# Eigenzeit: geglättete BD-Referenz gegen C2

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_bd_reference/README.md)

## Dokumentierte Aussage

Geglätteter 4D-Benincasa–Dowker-Operator mit Poisson-Punktzahlen, bekannter physischer Dichte und externer Eigenzeit T=1. 384 Entwicklungs- und 6.144 getrennte Testwolken. Im Hauptfall ist das RMSE-Verhältnis BD/C2 33,34; die vorab lokal fixierten Nutzenkriterien scheitern. C2 nutzt die bekannte de-Sitter-Familie und Modellgrenzen. Nominale Student-Intervalle sind keine garantierten 95%-Intervalle; keine universelle Rangordnung oder allgemeine Krümmungsuhr.

- [research/lorentz_bd_reference/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_bd_reference/RESULTS.md): Ergebnisse aller zwölf Testzellen, Unsicherheiten, Kosten und Grenzen des NO_GO.
- [research/lorentz_bd_reference/METHODS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_bd_reference/METHODS.md): Operator, Poisson-Sprinkling, Kontinuumsquadratur und vorab lokal festgelegter Vergleich; keine öffentliche Vorregistrierung.
- [research/lorentz_bd_reference/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_bd_reference/contract.json): Unveränderter Prüfvertrag mit Budget, Seeds, Entwicklungsauswahl und Abbruchregeln.
- [research/lorentz_bd_reference/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_bd_reference/VERIFICATION.json): Archivierter vollständiger Nachbau und unabhängige Teilkontrollen.
- [research/lorentz_bd_reference/results/execution.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_bd_reference/results/execution.json): Ausführungsumgebung, ursprüngliche Quellenfixierung und gemessener Aufwand.
- [research/lorentz_bd_reference/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/research/lorentz_bd_reference/results/summary.json): Vollständige Kennzahlen und alle Entscheidungen.

## Reproduzieren

Python 3.12, NumPy 2.3.5, SciPy 1.17.0, C++17-Compiler g++ und vollständige Git-Historie. Der Quellencommit 2d2539123162ddc032b85ba51af56255ca36a906 muss erhalten bleiben. Der gepinnte Originalprüfer fordert bitgleiche Floats und setzt die Original-Rechenumgebung voraus. Die aktuelle README beschreibt zusätzlich den getrennten numerischen Plattformprüfer.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-bd-reference
cd x6-lorentz-bd-reference
git checkout --detach aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_bd_reference/verify.py --archive research/lorentz_bd_reference/results --replay
```

Erwartete Ausgabe: Originalumgebung: PASS_FULL_REPLAY für 6.528 Wolken und 102 zusätzliche unabhängige Relationsprüfungen. Für andere Rechner siehe aktuellen README-Einstieg: getrenntes PASS_PORTABLE_NUMERICAL_REPLAY mit offengelegter Gleitkommatoleranz. Fachlicher Entscheid bleibt NO_GO_VARIABLE_CURVATURE_IN_THIS_BUDGET.

## Offene Prüfung

Kein Ausbau auf variable Krümmung im geprüften Budget. Externe Replikation bleibt offen. Ein anderer Glättungs-/Skalenplan benötigt einen neuen vorab fixierten Vertrag und frische Testdaten; der lokale d’Alembertian bleibt ein separater Reproduktionszweig.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
