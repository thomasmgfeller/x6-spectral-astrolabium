# Gemeinsamer lokaler Einstieg

Registerstand: 2026-10-17. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 6ac1363b6d3e0bcef6f863320290e3826977952a

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6ac1363b6d3e0bcef6f863320290e3826977952a/docs/INTEGRATION.md)

## Dokumentierte Aussage

Installation, Signal/Spektral/RAX-Läufe sowie Export und Replay sind in main integriert. ACVM/C1 besitzen zusätzliche Unterbefehle.

- [docs/integration-v0.1/evidence/qualification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/6ac1363b6d3e0bcef6f863320290e3826977952a/docs/integration-v0.1/evidence/qualification.json): Historische Abnahme PASS_WITH_BROWSER, 23 Schritte; genaue damalige Revision im Bericht. Kein Nachweis für beliebige spätere Commits.

## Reproduzieren

Linux/POSIX x86-64, Python 3.12, Git, Node >=22; setup installiert gepinntes NumPy/SciPy. Browser für die Oberfläche.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-integration
cd x6-integration
git checkout --detach 6ac1363b6d3e0bcef6f863320290e3826977952a
python3 x6.py setup --profile research
python3 x6.py doctor --profile research
python3 x6.py serve
```

Erwartete Ausgabe: doctor: erfolgreich; serve meldet Loopback-URL und bleibt bis Strg+C aktiv.

## Offene Prüfung

Frischer Checkout der nächsten Implementierungsrevision: Installation, alle drei Adapter, ZIP-Replay, Negativkontrollen und Browser/CLI-Austausch bestehen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
