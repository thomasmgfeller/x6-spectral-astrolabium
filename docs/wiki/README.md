# X6 Wiki — Deutsch und Englisch

Das Wiki erklärt die vorhandenen Werkzeuge, Begriffe und Evidenzgrenzen.
Es enthält acht inhaltlich entsprechende Kapitel je Sprache und eine
Sprachauswahl. Es ist Teil des versionierten Repositorys und des vorhandenen
GitHub-Pages-Portals, nicht ein getrennt gepflegtes GitHub-Wiki-Repository.

- [Deutsch](../../wiki/de/index.html)
- [English](../../wiki/en/index.html)

Aktualisierter Quellenstand: 19. Oktober 2026, Commit `5e164bdc0feaf529af34e019f43dfda949c47302`.
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

Vierter Nachtrag 19. Oktober 2026: gemeinsame Referenzrichtungen aus kausalen
Intervallzählungen auf 48 weiteren frischen Wolken. Metrik-RMS 4.840 → 3.709,
affine Drift 3.271 → 3.085 bei höchster Dichte. Gesamtentscheid COMMON_AXIS_HOLD;
weiter HOLD_PHASE3. Erste und zweite Momente werden getrennt ausgewiesen.

Fünfter Nachtrag 19. Oktober 2026: koordinatengestützte gemeinsame Momenten-
Machbarkeit auf 48 frischen Wolken. Bei höchster Dichte 16/16 Kappen mit
festen Zeitgewichten lösbar, minimale Gewichtssumme im Mittel 0.845×Basis.
Angepasste Momente sind Nebenbedingungen, keine unabhängige Validierung;
CAP_MOMENT_FEASIBILITY_SUPPORTED bei weiterhin HOLD_PHASE3.

Sechster Nachtrag 19. Oktober 2026: intrinsische Landmarkenkalibrierung auf
48 frischen Wolken vollständig nachgerechnet. 42 verfügbare Nachbarschaften
ohne zulässiges Landmarken-Triplett, sechs unverfügbar, 0/48 Übernahmen.
Rückfallbasis unverändert; Rauschschutz nicht erreicht. Koordinatengestützte
Feldverbesserung ist diagnostisch. INTRINSIC_MOMENT_HOLD und HOLD_PHASE3.
