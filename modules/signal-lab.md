# Signal Validation Lab

Registerstand: 2026-10-16. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

[Signal Lab öffnen →](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/signal-lab.html)

## Quelle

Branch: main

Commit: a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/SIGNAL_VALIDATION_LAB.md)

## Dokumentierte Aussage

Synthetische Signale werden gegen vier Verfahren verglichen; Roharrays und Qualitätsurteile bleiben im Replay erhalten.

- [docs/integration-v0.1/evidence/signal-run.log](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/integration-v0.1/evidence/signal-run.log): Erhaltenes Pulsbeispiel: X6-Phasenfilter FAIL ist ein fachliches Ergebnis, kein Laufabbruch.
- [docs/perspectives/edge-platform/evidence/independent-reference.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/perspectives/edge-platform/evidence/independent-reference.json): Gespeicherte NumPy/SciPy-Gegenprüfung.

## Reproduzieren

Python 3.12, Node >=22; setup --profile core. UI: app/signal-lab.html.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-signal-lab
cd x6-signal-lab
git checkout --detach a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f
python3 x6.py run signal --output runs/register-signal
python3 x6.py verify runs/register-signal
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Vor Leistungsclaims: starke Baselines, getrennte reale Testdaten, ereigniserhaltende Qualitätsgates und Ressourcenmessung.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
