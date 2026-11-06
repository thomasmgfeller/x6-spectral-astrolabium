# CST-DUST: Korrespondenz vor der Singularität v0.1

**Physikalischer Test: HOLD_NOT_ELIGIBLE / NOT_RUN.**
Die vorher festgelegten Toleranzen, physikalischen Abgleichregeln und getrennten
Regularitätsentscheidungen sind ausführbar dokumentiert. Numerische klassische
Referenzkontrollen und eine konservative Ableitungs-Budgetdiagnose sind ausgeführt.
Keine neuen dynamischen CST-Ensembles, Zufallsstichproben oder bezahlten Läufe.

## Reproduzieren

Python 3.12, NumPy 2.3.5 und SciPy 1.17.0:

```sh
python3 -B run.py
```

Die eingeschlossene Euler-Referenz und die rationalen Sensitivitätsrechnungen
verwenden nur die Python-Standardbibliothek. NumPy/SciPy werden durch die
unveränderte, hier übernommene Expositionsbibliothek des Vorgängerpakets importiert.
`python3 -O -B run.py` bleibt funktionsfähig: Die Kontrollen verwenden explizite
Fehlerprüfungen, keine abschaltbaren Assertions.

Für die PDF und Figuren zusätzlich Matplotlib, ReportLab sowie DejaVu-Schriften:
`python3 build_report.py`. Ausgabe standardmäßig unter `../output/pdf/`.

## Inhalt

- `plan.json`, `plan.sha256`: vor neuen Rechnungen fixierter lokaler Prüfplan.
- `DERIVATION.md`: Definitionen, Beweise, Ergebnisse, Grenzen und Quellen.
- `intervals.py`: nach außen gerundete Decimal-Intervalle und rationale Kubikwurzeln.
- `acceptance.py`: Toleranz-, Unsicherheits-, Abgleich- und Zulassungsregeln.
- `run.py`: reproduziert 26 Kontrollen, 240 numerische Referenzvergleiche,
  60 Vergleiche der letzten numerischen Stufen, 90 rationale Sensitivitätsfälle
  und 60 getrennte P3-Bewertungsdatensätze.
- `results/`: sämtliche CSV-Werte, exakte rationale Hüllen und JSON-Entscheidungen.
- `inputs/`: unveränderte Herkunftsdaten des Modellvertrags und der Stromkalibrierung.
- `SHA256SUMS`: vollständige Inhaltsprüfsummen, ohne Selbsthash.

Die vier numerischen Schrittweiten sind keine vier physischen CST-Dichten.
`PASS_METADATA_ONLY` belegt keine physikalische Gleichwertigkeit. Große
hinreichende Rauschhüllen sind keine nachgewiesenen Mindestfehler.
