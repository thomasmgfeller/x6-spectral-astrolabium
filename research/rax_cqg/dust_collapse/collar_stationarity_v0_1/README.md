# CST-DUST: Vergangenheitskragen, Stationarität und Randzustände v0.1

Ein rationaler Kragen aus vier festen Kettenvorgängern erfüllt für ein letztes freies Element die Staub-Normierung und Uhrgleichung gleichzeitig. Die Lösung ist eine flache Familie und benötigt nichtverschwindende Randreaktionen. Ein expliziter normierter Randzustand endlicher Breite hat trotz verschwindender Mittelwerte positive Constraint-Residuen. Die Grenze verschwindender Randbreite und die Grenze starker Materiephase vertauschen nicht.

**Alle acht physikalischen Gates bleiben HOLD.** Kein physikalisch ausgewählter Randzustand, keine hergeleitete Constraintquantisierung, keine vollständige Geometrievariation und kein Bounce. Kein kostenpflichtiger Rechenlauf, kein n=5-Produktionslauf.

Basis: Main nach [PR 265](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/265), Commit `2b422800dcc0bd79643e1c946069acf8875a5291`. Datum: 8. November 2026 (Zürich).

## Lesen

* `CST_DUST_Vergangenheitskragen_Stationaritaet_Randzustaende_v0_1.pdf`: sechsseitiger Bericht.
* `DERIVATION.md`: Beweise, Domänen, Fehlerbudgets und genaue Grenzen.
* `collar_contract.json`: maschinenlesbare Annahmen und Anspruchsgrenzen.
* `provenance.json`, `plan.json`, `plan.sha256`, `manifest.json`: Quellenbindung und eingefrorener Kontrollplan.

## Nachrechnen

Python 3 mit Standardbibliothek genügt für alle wissenschaftlichen Kontrollen:

```sh
python3 -B verify_package.py
python3 -B replay.py
```

`analyze.py` erzeugt fünf Ergebnisdateien. `replay.py` vergleicht sie in einem isolierten temporären Verzeichnis bytegenau mit den mitgelieferten Daten. `package.py` erstellt das deterministische ZIP erneut. Nur die optionale PDF-Neuerstellung benötigt ReportLab und DejaVu-Schriften.

Kontrollen: 216 Kettenfälle, 2187 Randstörungen, drei normierte Pakete mit Momenten bis Grad vier, zwölf rigorose Amplitudenbudgets und neun zurückgewiesene Negativannahmen. Keine externe Replikation. Der Plan wurde nach analytischem Kandidatenentwurf vor diesen Kontrollen eingefroren; keine externe Präregistrierung.

Der nächste physikalische Schritt ist eine begründete Randpräparation mit Maß/Skalarprodukt und Randwirkung beziehungsweise gemeinsamer Randvariation, welche die ausgewiesenen Randreaktionen trägt. Ein größerer Rechenlauf ersetzt diese Modellentscheidung nicht.
