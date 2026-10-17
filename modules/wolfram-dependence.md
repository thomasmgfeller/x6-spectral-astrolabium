# Wolfram Fall 4: Nullfehler und Abhängigkeit

Registerstand: 2026-10-17. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 96fdd71b6741adecf5481174a5d19b32b66bfe2d

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/96fdd71b6741adecf5481174a5d19b32b66bfe2d/docs/signal-lab/wolfram-zero-failures-v0.1/README.md)

## Dokumentierte Aussage

Zwölf Wolfram-Prüfungen und sieben Python-Vergleiche: unabhängige Versuche und Kopien eines Versuchs haben unterschiedliche Deckung.

- [docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/96fdd71b6741adecf5481174a5d19b32b66bfe2d/docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

## Reproduzieren

Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-wolfram-dependence
cd x6-wolfram-dependence
git checkout --detach 96fdd71b6741adecf5481174a5d19b32b66bfe2d
python3 -m zipfile -e docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip /tmp/x6-hub-wolfram-dependence
cd /tmp/x6-hub-wolfram-dependence/X6_Wolfram_Fall4_v0_1
python3 verify.py
```

Erwartete Ausgabe: PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

## Offene Prüfung

Unabhängigkeit konkreter Datensätze belegen; das konstruktive Gegenbeispiel ist kein Audit aller Projektdaten.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
