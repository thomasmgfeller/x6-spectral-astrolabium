# Industrielle Entrauschung: V1-Bewertungsadapter

Registerstand: 2026-10-18. MAIN / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: main

Commit: 78a150f27fdf52187d140f9fcf440ce29c89cb48

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/experiments/industrial-v1/README.md)

## Dokumentierte Aussage

Vier Schemata, Vorprüfung, Bewertung und synthetischer Kontrollgenerator; ursprüngliche Quellen unverändert aus f5116b9970a6b7dc788c18623a8386b4cde33ad4 nach main übernommen. Bestätigende AP1-Freigabe bleibt NOT_READY. Der getrennte, tatsächlich ausgeführte Datenpilot steht im Modul industrial-pilot.

- [experiments/industrial-v1/examples/draft_readiness.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/78a150f27fdf52187d140f9fcf440ce29c89cb48/experiments/industrial-v1/examples/draft_readiness.json): Offene Eingabe-/Mess-/Protokollfelder einzeln ausgewiesen.

## Reproduzieren

Python 3.12, gepinnte Anforderungen aus requirements; isolierte venv empfohlen.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-industrial-v1
cd x6-industrial-v1
git checkout --detach 78a150f27fdf52187d140f9fcf440ce29c89cb48
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experiments/industrial-v1/evaluate.py experiments/industrial-v1/V1_PROFILE_DRAFT.json --root experiments/industrial-v1 --output /tmp/register-v1-readiness.json
```

Erwartete Ausgabe: NOT_READY, Exit 3 ist beim veröffentlichten Entwurf erwartet.

## Offene Prüfung

Für eine benannte industrielle Zielpopulation Rechte, 4-Kanal-Aufnahme/Kalibrierung, unabhängige Labels, Maschinen-/Standortstruktur und genügend unabhängige Lager beschaffen. Fachlich begründete Poweralternativen, Kandidat, starke Baseline und Schwellen vor Zugriff auf Bestätigungsdaten fixieren; ursprüngliche Gates unverändert anwenden.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
