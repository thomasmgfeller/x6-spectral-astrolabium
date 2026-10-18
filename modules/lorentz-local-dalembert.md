# Lokaler d’Alembertian: Koeffizientenvortest

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 49710201cdb2e2941404266b25e88051a659b08e

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/research/lorentz_local_dalembert/README.md)

## Dokumentierte Aussage

Quellenprüfung und algebraischer Vortest zum Boguñá–Krioukov-Operator: konstantes Feld, zeitliches und räumliches Quadrat. Keine implementierte intrinsische Nachbarschaftsrekonstruktion oder Konvergenzstudie. Der konstante Feldtest ist null; die BD-Krümmungsregel −2B(1) ist nicht übertragbar.

- [research/lorentz_local_dalembert/README.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/research/lorentz_local_dalembert/README.md): Primärquellen und getrennte geplante Abnahmefolge.
- [research/lorentz_local_dalembert/PREFLIGHT.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/research/lorentz_local_dalembert/PREFLIGHT.json): Begrenzter Vortest mit ausdrücklich fehlender intrinsischer Reproduktion.

## Reproduzieren

Python 3.12 und NumPy. Der vorhandene Test prüft nur die abschliessende Koeffizientenzusammensetzung.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-local-dalembert
cd x6-lorentz-local-dalembert
git checkout --detach 49710201cdb2e2941404266b25e88051a659b08e
python3 -B research/lorentz_local_dalembert/preflight.py
```

Erwartete Ausgabe: PASS_ASSEMBLY_ONLY, intrinsic_reproduction=false und curvature_estimator=false.

## Offene Prüfung

Intrinsische Zeit- und Raumabstände mit offengelegten Rand-/Ausfallregeln reproduzieren; danach ein vorab fixierter Minkowski-Test mit getrennten Daten. Gekrümmte Anwendungen benötigen eine eigene Zielherleitung.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
