# Edge-Referenzadapter

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 5e164bdc0feaf529af34e019f43dfda949c47302

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/5e164bdc0feaf529af34e019f43dfda949c47302/experimental/edge_reference/README.md)

## Dokumentierte Aussage

Begrenzter lokaler Signalauftrag mit Export und rechnerischem Replay; main enthält den Adapter bereits.

- [docs/perspectives/edge-platform/evidence/local-validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/5e164bdc0feaf529af34e019f43dfda949c47302/docs/perspectives/edge-platform/evidence/local-validation.json): Lokale Softwareprüfung; keine Messung von Geräteeffizienz.

## Reproduzieren

Node >=22; keine npm-Laufzeitabhängigkeiten.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-edge-reference
cd x6-edge-reference
git checkout --detach 5e164bdc0feaf529af34e019f43dfda949c47302
node experimental/edge_reference/runner.cjs run experimental/edge_reference/examples/synthetic-signal.json runs/register-edge
node experimental/edge_reference/runner.cjs verify runs/register-edge
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Zweite unabhängige Anwendung, qualifizierter Geräteadapter und ARM64/x86-64-Vergleich nach Roadmap.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
