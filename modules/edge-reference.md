# Edge-Referenzadapter

Registerstand: 2026-10-16. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/experimental/edge_reference/README.md)

## Dokumentierte Aussage

Begrenzter lokaler Signalauftrag mit Export und rechnerischem Replay; main enthält den Adapter bereits.

- [docs/perspectives/edge-platform/evidence/local-validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/perspectives/edge-platform/evidence/local-validation.json): Lokale Softwareprüfung; keine Messung von Geräteeffizienz.

## Reproduzieren

Node >=22; keine npm-Laufzeitabhängigkeiten.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-edge-reference
cd x6-edge-reference
git checkout --detach a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f
node experimental/edge_reference/runner.cjs run experimental/edge_reference/examples/synthetic-signal.json runs/register-edge
node experimental/edge_reference/runner.cjs verify runs/register-edge
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Zweite unabhängige Anwendung, qualifizierter Geräteadapter und ARM64/x86-64-Vergleich nach Roadmap.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
