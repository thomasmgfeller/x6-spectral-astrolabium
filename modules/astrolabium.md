# Astrolabium und rationale Spektralreferenz

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

[Astrolabium öffnen →](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/)

## Quelle

Branch: main

Commit: aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/docs/SCIENTIFIC_SCOPE.md)

## Dokumentierte Aussage

Fünf rationale Referenzfälle prüfen strikte Untergrenzen für endliche gerundete Graph-Laplacians, einschliesslich ungültiger Schranken und getrennter Komponenten.

- [docs/integration-v0.1/evidence/spectral-run.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/docs/integration-v0.1/evidence/spectral-run.log): Erhaltene Referenzausführung; keine physische oder allgemeine Raumzeitaussage.
- [evidence/historical_python_results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb/evidence/historical_python_results.json): Historischer Python-Befund; datierter Prüfstand.

## Reproduzieren

Python 3.12; gemeinsames setup --profile core. Browser-App: app/index.html.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-astrolabium
cd x6-astrolabium
git checkout --detach aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb
python3 x6.py run spectral --output runs/register-spectral
python3 x6.py verify runs/register-spectral
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Externe Reproduktion der exakten Zertifikate und separat vollständige Browser-/Julia-Qualifikation.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
