# Astrolabium und rationale Spektralreferenz

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

[Astrolabium öffnen →](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/)

## Quelle

Branch: main

Commit: ac519f5e4a83de0e570680fe4cfeb2da133db351

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/docs/SCIENTIFIC_SCOPE.md)

## Dokumentierte Aussage

Fünf rationale Referenzfälle prüfen strikte Untergrenzen für endliche gerundete Graph-Laplacians, einschliesslich ungültiger Schranken und getrennter Komponenten.

- [docs/integration-v0.1/evidence/spectral-run.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/docs/integration-v0.1/evidence/spectral-run.log): Erhaltene Referenzausführung; keine physische oder allgemeine Raumzeitaussage.
- [evidence/historical_python_results.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ac519f5e4a83de0e570680fe4cfeb2da133db351/evidence/historical_python_results.json): Historischer Python-Befund; datierter Prüfstand.

## Reproduzieren

Python 3.12; gemeinsames setup --profile core. Browser-App: app/index.html.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-astrolabium
cd x6-astrolabium
git checkout --detach ac519f5e4a83de0e570680fe4cfeb2da133db351
python3 x6.py run spectral --output runs/register-spectral
python3 x6.py verify runs/register-spectral
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Externe Reproduktion der exakten Zertifikate und separat vollständige Browser-/Julia-Qualifikation.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
