# RAX-B1/M1: Benchmark und Methodenreview

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: c58cc26adb2b4a646e3940e417351040b5dc9ff0

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/docs/research/rax/method-review-v0.1/README.md)

## Dokumentierte Aussage

67.584 Benchmarkläufe und Methoden-Gegenbeispiele werden nachgerechnet. Alle acht primären Überlegenheitsentscheidungen bleiben INCONCLUSIVE.

- [docs/research/rax/benchmark-v0.1/RAX_B1_Benchmarking_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/docs/research/rax/benchmark-v0.1/RAX_B1_Benchmarking_v0_1_Paket.zip): Eingefrorene B1-Daten und Referenzprüfer.
- [docs/research/rax/method-review-v0.1/RAX_M1_Methodenpruefung_v0_1_Paket.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c58cc26adb2b4a646e3940e417351040b5dc9ff0/docs/research/rax/method-review-v0.1/RAX_M1_Methodenpruefung_v0_1_Paket.zip): Zwei nachgewiesene Validierungsfehler und Zusatzguards; ursprüngliche Daten bestehen Nachprüfung.

## Reproduzieren

setup --profile research; Python 3.12, NumPy/SciPy. Der Replay kann mehrere Minuten dauern.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-rax-b1-m1
cd x6-rax-b1-m1
git checkout --detach c58cc26adb2b4a646e3940e417351040b5dc9ff0
python3 x6.py run rax --output runs/register-rax
python3 x6.py verify runs/register-rax
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Historische Quellen bleiben unverändert. Neuer deklarativer RAX-G1-Runner mit 33 Angriffskontrollen im Modul rax-guarded; unabhängige personelle Wiederholung und allgemeine Isolation fremden Python-Codes bleiben offen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
