# Begrenzter Mathematikagent: Lorentz n=3–5 und Propagator

Registerstand: 2026-10-17. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 389cb3f688dfbc9d90086bb55c1b5d199b7e9c58

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/docs/MATH_AGENT.md)

## Dokumentierte Aussage

Endliche Ordnungszählung und 1+1-Diamond-Spektralvergleich; Replikation/Kalibrierung, kein neuer Satz.

- [docs/LORENTZ_RESEARCH.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/docs/LORENTZ_RESEARCH.md): Definierte Referenzen, n=3/4/5-Zielzählungen und Grenzen.
- [agent/math-agent-config.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/agent/math-agent-config.json): Konfiguriertes exklusives Ende 2026-10-18T22:00:00Z; 90 Sekunden Rechenbudget.
- [docs/agent-archive/2026-10-15/ARCHIVE.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/389cb3f688dfbc9d90086bb55c1b5d199b7e9c58/docs/agent-archive/2026-10-15/ARCHIVE.json): Drei ausgewählte Originalartefakte dauerhaft in Git: Mathematik/Lorentz, Graphatlas, NOAA; GitHub-Digests, innere Inventare und historische Quellhashes geprüft. Nicht alle Läufe archiviert.

## Reproduzieren

Python 3.12, Node >=22 und gepinnte mathematische Abhängigkeiten.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-lorentz-agent
cd x6-lorentz-agent
git checkout --detach 389cb3f688dfbc9d90086bb55c1b5d199b7e9c58
python3 -m pip install -r agent/math-requirements.txt
python3 -m unittest tests/python/test_math_agent.py tests/python/test_lorentz_spectral.py -v
```

Erwartete Ausgabe: Exit 0 bei bestandenen Regressionen; startet keinen geplanten Forschungslauf.

## Offene Prüfung

Unabhängige Replikation; separat registrierte Grössen/Seeds/Ränge und Unsicherheit für Finite-Size-Studie. n=6-Restpaaranalyse in main: Modul lorentz-n6-residuals; vollständiger historischer Atlasgenerator weiter im Branch-Modul.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
