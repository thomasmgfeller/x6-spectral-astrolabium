# Edge-Referenzadapter

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/experimental/edge_reference/README.md)

## Dokumentierte Aussage

Begrenzter lokaler Signalauftrag mit Export und rechnerischem Replay; main enthält den Adapter bereits.

- [docs/perspectives/edge-platform/evidence/local-validation.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee/docs/perspectives/edge-platform/evidence/local-validation.json): Lokale Softwareprüfung; keine Messung von Geräteeffizienz.

## Reproduzieren

Node >=22; keine npm-Laufzeitabhängigkeiten.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-edge-reference
cd x6-edge-reference
git checkout --detach d6c9f3d9ddf975cdc6f0c2ce055c5becb1f7a2ee
node experimental/edge_reference/runner.cjs run experimental/edge_reference/examples/synthetic-signal.json runs/register-edge
node experimental/edge_reference/runner.cjs verify runs/register-edge
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Zweite unabhängige Anwendung, qualifizierter Geräteadapter und ARM64/x86-64-Vergleich nach Roadmap.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
