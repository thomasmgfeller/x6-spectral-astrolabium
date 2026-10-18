# Wolfram Fall 2: Polaritätsumkehr

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 49710201cdb2e2941404266b25e88051a659b08e

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/docs/signal-lab/wolfram-polarity-v0.1/README.md)

## Dokumentierte Aussage

Vier symbolische Identitäten und zwölf numerische Prüfungen; invertiertes Signal wird trotz gleicher PSD/Kohärenz zurückgewiesen.

- [docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/49710201cdb2e2941404266b25e88051a659b08e/docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

## Reproduzieren

Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-wolfram-polarity
cd x6-wolfram-polarity
git checkout --detach 49710201cdb2e2941404266b25e88051a659b08e
python3 -m zipfile -e docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip /tmp/x6-hub-wolfram-polarity
cd /tmp/x6-hub-wolfram-polarity/X6_Wolfram_Fall2_v0_1
python3 verify.py --rerun
```

Erwartete Ausgabe: PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

## Offene Prüfung

Externe Wiederholung; reale Signale benötigen einen eigenen Messvertrag.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
