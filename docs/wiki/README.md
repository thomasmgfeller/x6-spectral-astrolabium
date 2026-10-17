# X6 Wiki — Deutsch und Englisch

Das Wiki erklärt die vorhandenen Werkzeuge, Begriffe und Evidenzgrenzen.
Es enthält acht inhaltlich entsprechende Kapitel je Sprache und eine
Sprachauswahl. Es ist Teil des versionierten Repositorys und des vorhandenen
GitHub-Pages-Portals, nicht ein getrennt gepflegtes GitHub-Wiki-Repository.

- [Deutsch](../../wiki/de/index.html)
- [English](../../wiki/en/index.html)

Aktualisierter Quellenstand: 17. Oktober 2026, Commit `389cb3f688dfbc9d90086bb55c1b5d199b7e9c58`.
Die ursprüngliche Eigenzeit-Referenz aus PR #44 bleibt unverändert dokumentiert.
Ergänzt sind die d-dimensionalen Gültigkeitsbedingungen, endliche Fehlergrenzen,
sequenzielles Nachbeproben, bedingte Kettendiagnostik und die erhaltene
Ausführungshistorie. Die neuen Pakete wurden lokal vor ihren Zielziehungen
fixiert und erst nach Ausführung veröffentlicht; keine öffentliche
Präregistrierung oder externe Replikation wird behauptet. Die Einführung
ersetzt keine Originaldefinition, keinen Prüfvertrag und keinen Evidenzbericht.

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
