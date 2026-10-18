# RAX-B1/M1: Benchmark und Methodenreview

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 49710201cdb2e2941404266b25e88051a659b08e

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/docs/research/rax/method-review-v0.1/README.md)

## Dokumentierte Aussage

67.584 Benchmarkläufe und Methoden-Gegenbeispiele werden nachgerechnet. Alle acht primären Überlegenheitsentscheidungen bleiben INCONCLUSIVE.

- [docs/research/rax/benchmark-v0.1/RAX_B1_Benchmarking_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/docs/research/rax/benchmark-v0.1/RAX_B1_Benchmarking_v0_1_Paket.zip): Eingefrorene B1-Daten und Referenzprüfer.
- [docs/research/rax/method-review-v0.1/RAX_M1_Methodenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/docs/research/rax/method-review-v0.1/RAX_M1_Methodenpruefung_v0_1_Paket.zip): Zwei nachgewiesene Validierungsfehler und Zusatzguards; ursprüngliche Daten bestehen Nachprüfung.

## Reproduzieren

setup --profile research; Python 3.12, NumPy/SciPy. Der Replay kann mehrere Minuten dauern.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-rax-b1-m1
cd x6-rax-b1-m1
git checkout --detach 49710201cdb2e2941404266b25e88051a659b08e
python3 x6.py run rax --output runs/register-rax
python3 x6.py verify runs/register-rax
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Historische Quellen bleiben unverändert. Neuer deklarativer RAX-G1-Runner mit 33 Angriffskontrollen im Modul rax-guarded; unabhängige personelle Wiederholung und allgemeine Isolation fremden Python-Codes bleiben offen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
