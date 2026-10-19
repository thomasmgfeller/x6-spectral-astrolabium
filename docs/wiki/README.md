# X6 Wiki — Deutsch und Englisch

Das Wiki erklärt die vorhandenen Werkzeuge, Begriffe und Evidenzgrenzen.
Es enthält acht inhaltlich entsprechende Kapitel je Sprache und eine
Sprachauswahl. Es ist Teil des versionierten Repositorys und des vorhandenen
GitHub-Pages-Portals, nicht ein getrennt gepflegtes GitHub-Wiki-Repository.

- [Deutsch](../../wiki/de/index.html)
- [English](../../wiki/en/index.html)

Aktualisierter Quellenstand: 19. Oktober 2026, Commit `aa2c3dae7bb7afb564cdf4f08b0fe8f2c64c9bfb`.
Die Eigenzeit-Referenzen bleiben mit ihren jeweiligen Grenzen dokumentiert.
Neu erklärt sind der vollständige Krümmungsbenchmark, beide verfehlten
Empfindlichkeitskriterien und die exakte konforme Dichteverwechslung.
Der Krümmungsvertrag war vor dem ersten Ziellauf öffentlich fixiert; die
älteren Eigenzeit-Erweiterungen hatten nur eine lokale Quellenfixierung.
Die nachträglich dokumentierte Koordinaten-Portabilitätskorrektur ist sichtbar;
Originalquellen und wissenschaftliche Ergebnisse bleiben erhalten.
Interne Wiederholung und GitHub CI sind keine externe Replikation.
Die Einführung ersetzt keinen Originalbericht und keinen Prüfvertrag.

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

Nachtrag 18. Oktober 2026: bedingte RSS-Kettenmomente, 24.576 neue Wolken,
dokumentierter Status FORWARD_SLOPE_NOT_RESOLVED und große
Einzelordnungsfehler der explorativen Krümmungsinversion.

Nachtrag 19. Oktober 2026: gepaarter BK-Ankersuchvergleich auf 48 frischen
Wolken. Eignungsfilter vor Begrenzung verbessert Abdeckung, aber Metrikfehler
und Fehlselektionen bleiben sichtbar; HOLD_PHASE3. Bericht und Rohdaten
sind im Kapitel kausale Ordnungen in beiden Sprachen verlinkt.

Zweiter Nachtrag 19. Oktober 2026: BK-Momentendiagnose mit 48 weiteren frischen
Wolken und acht Kombinationen von Zeit-, Schalen- und Richtungskontrollen.
Metrik-RMS bei höchster Dichte 7,387 → 2,267; mit exakter Kappe 5,893 → 1,002.
Alle Eingriffe koordinatengestützt, Restfehler über 0,5; weiterhin HOLD_PHASE3.

Dritter Nachtrag 19. Oktober 2026: intrinsische Intervallgewichte auf 48 weiteren
frischen Wolken. Metrik-RMS 7,089 → 3,765 und affine Drift 3,692 → 2,882 bei
höchster Dichte; begrenzter Verbesserungsvergleich bestanden. Nur 8/16 richtige
Lorentz-Signaturen, weiter HOLD_PHASE3.
