# Wolfram Fall 5: Kausalordnung

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: e947dfbdd49890dcb119940548537d1db59272c2

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/research/causal-order/wolfram-countercheck-v0.1/README.md)

## Dokumentierte Aussage

Sechzehn Wolfram-Assertions und exakte Python-Polynome bestätigen ein Drei-Ereignis-Gegenbeispiel gegen Vollständigkeit dieses Fingerprints.

- [docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e947dfbdd49890dcb119940548537d1db59272c2/docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip): Gespeicherte Erstfehler und korrigierte Wolfram-Antworten, Freeze-Dateien und vollständiges Inventar.

## Reproduzieren

Python 3.12/Standardbibliothek; Fall 2 mit --rerun zusätzlich Node. Kein frischer Wolfram-Lauf.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-wolfram-causal
cd x6-wolfram-causal
git checkout --detach e947dfbdd49890dcb119940548537d1db59272c2
python3 -m zipfile -e docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip /tmp/x6-hub-wolfram-causal
cd /tmp/x6-hub-wolfram-causal/X6_Wolfram_Fall5_v0_1
python3 verify_release.py
```

Erwartete Ausgabe: PASS_WITH_SCOPE_LIMITS oder erfolgreicher paketabhängiger Prüfbericht; Exit 0. Wissenschaftliche Aussage bleibt auf den konstruierten Fall begrenzt.

## Offene Prüfung

Zusätzliche Invarianten an registrierten Korpora prüfen; kein allgemeiner Rekonstruktionssatz.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
