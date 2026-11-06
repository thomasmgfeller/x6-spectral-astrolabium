# CST-DUST: Zustandsraum und Constraints v0.1

**Ergebnis:** Ein positiver, unter Umbenennungen reduzierter Hilfshistorienraum
ist konkret definiert und geprüft. Physikalische dynamische Constraints und
eine daraus abgeleitete CST-Evolution bleiben offen. Für den vorherigen rohen
Zweistellen-Kern scheitert unter der deklarierten Randraumidentifikation jede
gemeinsame positive Skalarproduktmatrix, auch mit beliebiger konstanter
Normierung. Die naive direkte Staub-Eulerbedingung besitzt in der gewählten
gewöhnlichen L²-Darstellung keine nichttrivialen Zustände auf nichtleeren
Staubstrata. Distributionelle Konstruktionen bleiben möglich.

## Inhalte

- `DERIVATION.md`: vollständige Definitionen, Beweise, Grenzen und Primärquellen.
- `plan.json`, `plan.sha256`: lokaler Plan vor der Rechnung; strukturelle
  Hindernisse vor der Zertifizierung erwartet, keine blinde Vorhersage.
- `quantum_structure.py`: rationale komplexe Intervall- und Matrixarithmetik.
- `analyze.py`: markierte Gruppenkontrolle, Metric-Zertifikat, Referenzkonstruktion
  und zwei getrennte P1-Datensätze.
- `results/`: 13 Ergebnisdateien; keine neuen physikalischen 4D-Daten.
- `inputs/`: unveränderte Quellen aus dem publizierten Variationspaket sowie
  geerbter Model-Contract und Herkunftshashes.
- `REPLAY.json`: isolierter Neulauf mit Vergleich aller Ergebnisdateien.
- `build_report.py`, `figures/`: Berichtsbau und erläuternde Abbildung.
- `CST_DUST_Zustandsraum_Constraints_v0_1.pdf`: Ergebnisbericht.
- `MANIFEST.sha256`: vollständige Dateiintegrität ohne Selbstreferenz.

## Wiederholung

Aus diesem Verzeichnis, Python 3.10 oder neuer:

```bash
python3 -O -B analyze.py
```

Die Berechnung verwendet ausschließlich die Standardbibliothek. Referenzlauf:
Python 3.12.14. Prüfungen benutzen explizite Ausnahmen und bleiben unter `-O`
aktiv. Keine Zufallszahlen, externen Daten oder kostenpflichtigen Läufe.
Bei anderer Python-Version ändern sich nur das Versionsfeld des Laufmanifests
und die davon abhängigen Datensatzhashes; wissenschaftliche Resultate bleiben
zu vergleichen. Der Neulauf überschreibt die Ergebnisdateien.

```bash
python3 -B build_report.py
sha256sum -c MANIFEST.sha256
```

Der Berichtsbau benötigt ReportLab, Matplotlib und DejaVu Sans. Ein optionales
erstes Argument legt den PDF-Zielpfad fest, sonst wird nach `../output/pdf/`
geschrieben. PDF-Erstellungsmetadaten gehören nicht zum Zahlen-Replay.

## Aussagegrenzen

3 671 markierte Zustände, 85 035 Gruppenwirkungen, 234 Orbits und 4 817
Wirkungsinvarianzprüfungen betreffen eine endliche Hilfsfamilie. Der Quotient
entfernt Labels; er erzeugt keine gravitativen Zwangsbedingungen und keinen
geschlossenen physikalischen Randzustandsraum. Die positive relationale
Zweizustandsreferenz ist vollständig lösbar, ihr Hamiltonian jedoch kein
abgeleitetes CST-Gesetz.

`CST-DUST-QS1-RELABEL`: alle acht physikalischen Entscheidungen HOLD.
`CST-DUST-V1-RAW-K-COMMON-M`: MODEL=FAIL nur unter der deklarierten gemeinsamen
M-Interpretation; sieben weitere Entscheidungen HOLD. Der frühe I₂-Test wird
nicht nachträglich geändert. Kovariante Historien- und andere wohldefinierte
Constraint-Ansätze bleiben ausdrücklich offen.

Lizenz: Apache-2.0; Herkunft in `NOTICE` und `inputs/provenance.json`.
