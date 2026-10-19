# Experiment Fabric

Registerstand: 2026-10-19. BRANCH_ONLY / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: research/x6-experiment-fabric-v1

Commit: a34c59f2b0e2d30c73936363040669941aa8ce09

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a34c59f2b0e2d30c73936363040669941aa8ce09/experimental/experiment_fabric/README.md)

## Dokumentierte Aussage

Gemeinsamer EIG-Planer, lokale Simulationsworker und Replay; ein Kontrollfall, kein reales Gerätenetz oder Nutzenvergleich.

- [experimental/experiment_fabric/examples/control-run.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a34c59f2b0e2d30c73936363040669941aa8ce09/experimental/experiment_fabric/examples/control-run.json): Gespeicherter synthetischer Kontrolllauf.
- [experimental/experiment_fabric/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a34c59f2b0e2d30c73936363040669941aa8ce09/experimental/experiment_fabric/VALIDATION.md): Dokumentierte Referenz- und Browserprüfung, begrenzter Geltungsbereich.

## Reproduzieren

Node >=22, Python 3.12 und Anforderungen aus industrial-v1.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch research/x6-experiment-fabric-v1 https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-experiment-fabric
cd x6-experiment-fabric
git checkout --detach a34c59f2b0e2d30c73936363040669941aa8ce09
node experimental/experiment_fabric/run.mjs run /tmp/register-fabric
node experimental/experiment_fabric/run.mjs verify /tmp/register-fabric/run.json
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experimental/experiment_fabric/verify_reference.py /tmp/register-fabric/run.json
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Zwei echte Rechennodes mit persistenten Jobs, Wiederanlauf und Tests für doppelte/verspätete Zustellung; anschliessend gleich budgetierter Nutzenvergleich.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
