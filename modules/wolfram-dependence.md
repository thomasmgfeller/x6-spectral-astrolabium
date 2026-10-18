# Wolfram Fall 4: Nullfehler und Abhängigkeit

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: e5840afa7c7865a48766d1a5366210508a7b1f05

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/docs/signal-lab/wolfram-zero-failures-v0.1/README.md)

## Dokumentierte Aussage

Zwölf Wolfram-Prüfungen und sieben Python-Vergleiche: unabhängige Versuche und Kopien eines Versuchs haben unterschiedliche Deckung.

- [docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e5840afa7c7865a48766d1a5366210508a7b1f05/docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

## Reproduzieren

Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-wolfram-dependence
cd x6-wolfram-dependence
git checkout --detach e5840afa7c7865a48766d1a5366210508a7b1f05
python3 -m zipfile -e docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip /tmp/x6-hub-wolfram-dependence
cd /tmp/x6-hub-wolfram-dependence/X6_Wolfram_Fall4_v0_1
python3 verify.py
```

Erwartete Ausgabe: PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

## Offene Prüfung

Unabhängigkeit konkreter Datensätze belegen; das konstruktive Gegenbeispiel ist kein Audit aller Projektdaten.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
