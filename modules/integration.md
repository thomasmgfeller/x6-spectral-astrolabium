# Gemeinsamer lokaler Einstieg

Registerstand: 2026-10-17. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 389cb3f688dfbc9d90086bb55c1b5d199b7e9c58

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/docs/INTEGRATION.md)

## Dokumentierte Aussage

Installation, Signal/Spektral/RAX-Läufe sowie Export und Replay sind in main integriert. ACVM/C1 besitzen zusätzliche Unterbefehle.

- [docs/integration-v0.1/evidence/qualification.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/docs/integration-v0.1/evidence/qualification.json): Historische Abnahme PASS_WITH_BROWSER, 23 Schritte; genaue damalige Revision im Bericht. Kein Nachweis für beliebige spätere Commits.

## Reproduzieren

Linux/POSIX x86-64, Python 3.12, Git, Node >=22; setup installiert gepinntes NumPy/SciPy. Browser für die Oberfläche.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-integration
cd x6-integration
git checkout --detach 389cb3f688dfbc9d90086bb55c1b5d199b7e9c58
python3 x6.py setup --profile research
python3 x6.py doctor --profile research
python3 x6.py serve
```

Erwartete Ausgabe: doctor: erfolgreich; serve meldet Loopback-URL und bleibt bis Strg+C aktiv.

## Offene Prüfung

Frischer Checkout der nächsten Implementierungsrevision: Installation, alle drei Adapter, ZIP-Replay, Negativkontrollen und Browser/CLI-Austausch bestehen.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
