# CST-DUST: Eichstruktur und Randkonsistenz v0.1 · Veröffentlichung

Die gemeinsame Label- und Uhrverschiebung ist im geprüften endlichen Ansatz
konsistent. Bei einer Referenzuhr ist das induzierte Maß der Zeitdifferenzen
korreliert. Unabhängige Vakuumuhrverschiebungen und getrenntes Zurücksetzen
gekoppelter Teilgebiete ohne relative Daten sind im Allgemeinen keine Symmetrien.

**Physikalische Eichquantisierung, gravitative Constraints, Junction-Gesetz,
Regularität und globaler Bounce bleiben offen. Eine gravitative Anomalie ist
nicht nachgewiesen.** Die frühere Zurückweisung der geprüften rohen
Evolutionsinterpretation bleibt unverändert wirksam.

[Bericht (PDF, sieben Seiten)](../reports/CST_DUST_Eichstruktur_Randkonsistenz_v0_1.pdf) ·
[Originales Prüfpaket (ZIP, 33 Mitglieder)](../packages/CST_DUST_Eichstruktur_Randkonsistenz_v0_1_Pruefpaket.zip) ·
[Beweise und genaue Geltungsbereiche](DERIVATION.md) ·
[Ergebnisse und Entscheidungen](results/verification.json)

## Ergebnisse

- 3 670 markierte Fälle und 85 034 gemeinsame Umbenennungen bestätigen die
  endliche Label-/Uhrverschiebungsalgebra.
- 49 992 geordnete Gebietsteilungen bestätigen die relative Randverschiebung;
  bei 30 820 ist die relative Richtung gekoppelt.
- Das exakte Pushforward-Maß der relativen Uhren besitzt 2 508 rationale
  Kontrollen. Bei zwei freien Uhren ist die Differenz dreiecksverteilt;
  E[r²]=2L²/3 statt L²/3 unter der nicht äquivalenten naiven Box.
- Von 7 249 Vakuumstellen der binären Algebra-Kontrollklasse haben 2 541 eine
  nichtverschwindende Kopplungsspalte. Der explizite Zeuge bei w=1/2 im offenen
  positiven Dichtestratum ändert seine Wirkung um 1/16.
- 24 zertifizierte Amplituden-/Ward-Kontrollen je Dichtewert w=1 und w=1/2
  sowie 66 unabhängige numerische Integrationen ergänzen die Beweise. Sie sind
  keine physikalischen Ensembles oder Wahrscheinlichkeitsaussagen.
- Sieben exakte Ergebnisdateien werden isoliert bytegleich reproduziert.

Der lokale Plan ist keine externe Präregistrierung oder blinde Vorhersage.
`supplement_01.json` dokumentiert die ergänzende Prüfung innerhalb des
Dichtestratums. Der Entwicklungshinweis zur ungeeigneten ersten Negativprobe
bleibt im Berichtspaket erhalten. Alle acht physikalischen Audit-Entscheidungen
sind HOLD; die drei abgegrenzten FAILs betreffen nur die benannten Abkürzungen.

## Reproduktion

Vom Repository-Stamm, Python 3.10+, nur Standardbibliothek:

```bash
python3 -O -B research/rax_cqg/dust_collapse/gauge_boundary_v0_1/publication_check.py
python3 -O -B research/rax_cqg/dust_collapse/gauge_boundary_v0_1/publication_check.py --replay
```

Die Prüfung verifiziert das Original-ZIP, alle 33 Mitglieder, die PDF-Kopie im
Berichtsordner, vollständige Hashes, den fixierten Plan, Vorgängereingaben und
die abgegrenzten Entscheidungen. Der Replay erzeugt die sieben exakten
Ergebnisdateien aus isolierten Quellen neu; alle Bytes und die Replay-Quittung
müssen übereinstimmen. Die archivierte zusätzliche SciPy-Quadratur ist kein
Intervallzertifikat und wird durch den Standardbibliothek-Replay nicht neu
ausgeführt. Sie ist separat mit `verify_quadrature.py` reproduzierbar.

`.github/workflows/cst-dust-gauge-boundary.yml` führt die Integritätsprüfung und
isolierte Nachrechnung bei passenden Pull Requests und Änderungen auf Main aus.
Ein Software-PASS hebt keine physikalische HOLD-Entscheidung auf.

## Präzisierung zur Herkunft der Eingaben

**PDF und ZIP werden unverändert veröffentlicht.** Der Bytevergleich bei der
Veröffentlichung zeigt: Die sieben geerbten Textdateien unter `inputs/` tragen
gegenüber ihren Quellen im angegebenen Main-Commit jeweils genau ein zusätzliches
abschließendes LF-Zeichen. Code, Definitionen und Dateninhalt sind sonst identisch.
Die Bezeichnung „unverändert“ im ursprünglichen Bericht ist insoweit als
inhaltliche Übernahme, nicht als Byteidentität dieser sieben Quellen zu lesen.

Die archivierten Kopien und ihre bereits ausgeführten Hashes werden nicht
nachträglich umgeschrieben. `publication_check.py` verlangt ausdrücklich die
Relation `Archivkopie = Repositoryquelle + ein LF` und akzeptiert keine weiteren
Unterschiede. Dieser Hinweis betrifft die Eingabeübernahme; die zugesicherte
Bytegleichheit von Originalartefakten und reproduzierten Ergebnissen bleibt
uneingeschränkt bestehen.

| Artefakt | SHA-256 |
|---|---|
| Original-ZIP | `80c948a0e53ca2c0f6a29e8e2354ad97b92dd1df786a0f0b3fbcc59fa0024606` |
| Bericht | `dcb47289b9ad298f2846aaa92553a79d927a6c2e7aa89af8c1680dd043658272` |
| Fixierter Plan | `f1075751c5a170bfb9d531a431c6e094214ab4bd2b2781f3eca32c09afa751c5` |

Basis: Main `374acc67cb0e6cc510ec3852fd9fe9ef2b5ed20a`, nach PR 246.
Nur diese Veröffentlichungsübersicht und `publication_check.py` ergänzen hier
den entpackten Originalinhalt. Keine neuen dynamischen 4D-Ensembles oder
Singularitätsauflösung.
