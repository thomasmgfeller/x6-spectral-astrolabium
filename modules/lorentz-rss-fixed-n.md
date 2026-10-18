# RSS bei fester Punktzahl: Formeln, Prüfung und Grenzen

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: e5840afa7c7865a48766d1a5366210508a7b1f05

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_rss_fixed_n/README.md)

## Dokumentierte Aussage

Exakte bedingte Kettenmomente und Kovarianzidentität; 24.576 unabhängige Wolken nach öffentlicher Quellenfixierung. Gemeinsames ±5%-Präzisionsziel nicht erreicht. Unabhängige C2-Quadratur stützt die korrigierte Vorhersage; die untersuchte allgemeine lineare Krümmungsinversion streut bei N=64/128 sehr stark. Keine Auflösung der Dichteverwechslung.

- [research/lorentz_rss_fixed_n/DERIVATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_rss_fixed_n/DERIVATION.md): Bedingte Mittelwerte, Volumenkorrektur, überlappende Teilmengen und Skalenannahmen.
- [research/lorentz_rss_fixed_n/RESULTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_rss_fixed_n/RESULTS.md): Alle Entscheidungen, Unsicherheit, Kovarianz und große Rekonstruktionsfehler.
- [research/lorentz_rss_fixed_n/contract.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_rss_fixed_n/contract.json): Unveränderter Vertrag aus dem öffentlichen Quellenstand 485d866 vor dem ersten Zielversuch.
- [research/lorentz_rss_fixed_n/results/summary.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_rss_fixed_n/results/summary.json): Maschinenlesbare Ergebnisse; gemeinsames Präzisionsziel nicht erfüllt.
- [research/lorentz_rss_fixed_n/VERIFICATION.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/research/lorentz_rss_fixed_n/VERIFICATION.json): Vollständiger interner Replay aller 24.576 Relationshashes und wissenschaftlichen Ausgaben.

## Reproduzieren

Python 3.12, Linux/POSIX, gepinnte NumPy-/SciPy-/Matplotlib-Versionen; vollständiger Git-Checkout. Pro Ziellauf 600 Sekunden und 2 GiB.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-rss-fixed-n
cd x6-lorentz-rss-fixed-n
git checkout --detach e5840afa7c7865a48766d1a5366210508a7b1f05
python3 -m pip install -r research/lorentz_rss_fixed_n/requirements.txt
python3 -B research/lorentz_rss_fixed_n/reproduce.py
```

Erwartete Ausgabe: PASS_FULL_RSS_FIXED_N_REPLAY; wissenschaftlich unverändert FORWARD_SLOPE_NOT_RESOLVED. Alle eingefrorenen Quellen bleiben identisch; eine dokumentierte Importhülle behebt den Namenskonflikt des ursprünglichen Prüfers.

## Offene Prüfung

Informationsbedarf vor größerem Budget bestimmen. De-Sitter-Modell mit bekannter Ricci-Beziehung und allgemeine Zweiparameter-Rekonstruktion getrennt prüfen; neue Geometriefamilien, Resttermkontrolle und kovarianzbewusste Unsicherheiten vorab festlegen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
