# X6 Wiki — Deutsch und Englisch

Das Wiki erklärt die vorhandenen Werkzeuge, Begriffe und Evidenzgrenzen.
Es enthält acht inhaltlich entsprechende Kapitel je Sprache und eine
Sprachauswahl. Es ist Teil des versionierten Repositorys und des vorhandenen
GitHub-Pages-Portals, nicht ein getrennt gepflegtes GitHub-Wiki-Repository.

- [Deutsch](../../wiki/de/index.html)
- [English](../../wiki/en/index.html)

Aktualisierter Quellenstand: 16. Oktober 2026, Eigenzeit-Ergebnisse aus PR #44,
Commit `967c7662f005d887918cac9350e5bbaf76f653a9`.
Die Erstausgabe aus PR #43 erklärte den Stand nach dem Design in PR #42.
Diese Aktualisierung ergänzt den ausgeführten Lauf: 6.912 Ordnungen,
RMSE 0,031614 im Hauptvergleich und die unzureichende größte Zusatzkontrolle
(63 statt 128 Paare). Originaldaten, Quellenfixierung und Ergebnisgrenzen
werden nicht verändert. Die Einführung ersetzt keine Originaldefinition,
keinen Prüfvertrag und keinen ausgeführten Evidenzbericht.

## Pflege / maintenance

Edit `docs/wiki/content.json`, keeping German and English chapter IDs,
section IDs and scientific scope aligned. Link claims to their original
repository sources. Update the snapshot and source commit after reviewing
new evidence. Do not silently change a planned or inconclusive result to PASS.
Technical source documents may remain in their original language; the wiki
articles themselves are provided in both German and English.

```sh
python3 tools/build_hub.py --write
python3 tools/build_hub.py --check
python3 tools/check_hub.py
python3 tools/check_wiki.py
```

`tools/build_wiki.py` generates HTML and Markdown from the same paired
content, through the existing hub renderer. Reading, chapter navigation,
language switching and source links require no JavaScript. The shared
sitemap and llms.txt include the wiki; indexing by external services is not
guaranteed. Update the current navigation source inventory after regenerating;
historical evidence inventories and research-source freezes stay unchanged.

Browser checks cover article navigation, corresponding language switches,
mobile overflow and reading with JavaScript disabled. These are documentation
and interface checks, not a full accessibility audit or scientific validation.
