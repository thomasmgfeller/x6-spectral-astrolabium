# Wolfram Fall 5: Kausalordnung

Registerstand: 2026-10-19. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 26432e3d4cde20adabb510f17d5639891f4ac642

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/docs/research/causal-order/wolfram-countercheck-v0.1/README.md)

## Dokumentierte Aussage

Sechzehn Wolfram-Assertions und exakte Python-Polynome bestätigen ein Drei-Ereignis-Gegenbeispiel gegen Vollständigkeit dieses Fingerprints.

- [docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/26432e3d4cde20adabb510f17d5639891f4ac642/docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

## Reproduzieren

Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-wolfram-causal
cd x6-wolfram-causal
git checkout --detach 26432e3d4cde20adabb510f17d5639891f4ac642
python3 -m zipfile -e docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip /tmp/x6-hub-wolfram-causal
cd /tmp/x6-hub-wolfram-causal/X6_Wolfram_Fall5_v0_1
python3 verify_release.py
```

Erwartete Ausgabe: PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

## Offene Prüfung

Zusätzliche Invarianten an registrierten Korpora prüfen; kein allgemeiner Rekonstruktionssatz.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
