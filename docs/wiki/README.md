# X6 Wiki — Deutsch und Englisch

Das Wiki erklärt die vorhandenen Werkzeuge, Begriffe und Evidenzgrenzen.
Es enthält acht inhaltlich entsprechende Kapitel je Sprache und eine
Sprachauswahl. Es ist Teil des versionierten Repositorys und des vorhandenen
GitHub-Pages-Portals, nicht ein getrennt gepflegtes GitHub-Wiki-Repository.

- [Deutsch](../../wiki/de/index.html)
- [English](../../wiki/en/index.html)

Quellenstand dieser Erstausgabe: 16. Oktober 2026, main nach PR #42,
Commit `08c64744caa584c940b45a8825d0b099ae0c92fb`.
Die Einführung ersetzt keine Originaldefinition, keinen Prüfvertrag und
keinen ausgeführten Evidenzbericht. Neuere Folgeläufe sind nicht allein
durch ihre Erwähnung als vollständig veröffentlicht zu verstehen.

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
