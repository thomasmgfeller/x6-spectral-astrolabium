# Neutral Discovery

Registerstand: 2026-10-19. BRANCH_ONLY / SOFTWARE. Kein Live-Prüfsiegel.

## Quelle

Branch: research/x6-neutral-discovery-v1

Commit: 1a02c482d59a42d554337fb83e0f6d6e6d84b516

[Originaldokumentation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/1a02c482d59a42d554337fb83e0f6d6e6d84b516/experimental/neutral_discovery/README.md)

## Dokumentierte Aussage

Drei synthetische Kontrollen und Challenge-Gates in endlichem Modellraum; hohe vorherige Gewichtung verhindert keine Verwerfung.

- [experimental/neutral_discovery/VALIDATION.md](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/1a02c482d59a42d554337fb83e0f6d6e6d84b516/experimental/neutral_discovery/VALIDATION.md): 17 Python-Tests, neun Zweierbatches/36 Ausgangsbelegungen, vollständige endliche Testgrössenprüfung.
- [experimental/neutral_discovery/examples/control.json](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/1a02c482d59a42d554337fb83e0f6d6e6d84b516/experimental/neutral_discovery/examples/control.json): Deterministische publizierte Kontrollen.

## Reproduzieren

Python 3.12/jsonschema, Node >=22 für die JS-Gegenprüfung.

Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.

```sh
git clone --branch research/x6-neutral-discovery-v1 https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-neutral-discovery
cd x6-neutral-discovery
git checkout --detach 1a02c482d59a42d554337fb83e0f6d6e6d84b516
python3 -m pip install -r experiments/industrial-v1/requirements.txt
python3 experimental/neutral_discovery/discovery.py verify experimental/neutral_discovery/examples/control.json
python3 -m unittest discover -s experimental/neutral_discovery/tests -v
```

Erwartete Ausgabe: Exit 0; nur die unten genannte Softwareaussage.

## Offene Prüfung

Persistente Präregistrierung und kampagnenübergreifendes Fehlerbudget; unabhängige Bestätigung unter erweitertem Modellraum.

Evidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.
