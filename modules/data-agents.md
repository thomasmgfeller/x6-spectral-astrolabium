# Öffentliche Datenagenten: NOAA, Atlas, QuTech, NASA

Registerstand: 2026-10-16. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/SOURCE_AGENTS.md)

## Dokumentierte Aussage

Quellen-/Ablehnungsprüfungen und App-Checks auf öffentlichen Daten. Vier Datenjobs in zwei Workflows; kein Denoising-Nutzenbeleg.

- [docs/DATA_AGENT.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/DATA_AGENT.md): NOAA-Lauf, Inputs und Actions-Artefakte 30 Tage.
- [docs/SOURCE_AGENTS.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/SOURCE_AGENTS.md): Atlas/QuTech/NASA-Artefakte 14 Tage; Archivdaten explizit gekennzeichnet.
- [docs/AGENT_WINDOW_REPAIR_2026_10_13.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/AGENT_WINDOW_REPAIR_2026_10_13.md): Dokumentierte Fenster- und Schutzprüfungen.
- [docs/agent-archive/2026-10-15/ARCHIVE.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f/docs/agent-archive/2026-10-15/ARCHIVE.json): Drei ausgewählte Originalartefakte dauerhaft in Git: Mathematik/Lorentz, Graphatlas, NOAA; GitHub-Digests, innere Inventare und historische Quellhashes geprüft. Nicht alle Läufe archiviert.

## Reproduzieren

Lokale Tests: Abhängigkeiten aus agent/requirements.txt und agent/source-requirements.txt; siehe Dokumentation. Produktionsläufe nutzen geschützte GitHub-Workflows und deren Zeitfenster.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-data-agents
cd x6-data-agents
git checkout --detach a1f22f6c59f3c5259d12cfb6c0ca2e8b0886f33f
python3 -m unittest tests/python/test_data_agent.py tests/python/test_source_agents.py -v
```

Erwartete Ausgabe: Lokale Softwaretests; kein neuer Datenabruf. Tatsächliche geplante Läufe siehe datierte Workflow-Links im Register.

## Offene Prüfung

Nach diesem Archiv-Snapshot entstehende oder bislang nicht ausgewählte Belege separat vor Ablauf sichern; unabhängiger Datensatz-/Drift- und Qualitätsvergleich. Nach Frist STOPPED erwarten.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
