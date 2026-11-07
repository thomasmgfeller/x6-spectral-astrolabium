# CST-DUST: Feste Uhrintervalle und variable Elementzahl v0.1

Arbeitspaket vom 7. November 2026, auf Main nach PR 252 aufgebaut.

**Ergebnis:** Vollständige Historien lassen sich zwischen festen Materieuhrwerten
mit variabler Elementzahl exakt zusammensetzen. Die unveränderte unbegrenzte
lokale Historien-L2-Norm divergiert. Zwei explizite zusätzliche Zahlgewichte
machen die Summe kontrollierbar. Ein gemeinsam festgelegter Enduhrwert liefert
einen normerhaltenden und schnittkompatiblen Referenztransport. Die Wahl der
Gewichte, des Endwerts und des Produkts ist damit noch nicht physikalisch begründet.

Alle acht physikalischen Gates bleiben HOLD. Es wurde kein globaler Bounce,
keine physikalische Singularitätsauflösung und kein allgemeines CST-No-go bewiesen.

## Lesen

- `DERIVATION.md`: vollständige Definitionen, Beweise und Geltungsgrenzen.
- `interval_contract.json`: maschinenlesbarer Status und Annahmen.
- `CST_DUST_Uhrintervalle_Variable_Elementzahl_v0_1.pdf`: kompakter Bericht.
- `plan.json`, `plan.sha256`: lokal vor Implementierung eingefrorener Prüfplan.
- `inputs/provenance.json`: sechs bytegleiche Quellen mit Commit/Pfad/Git-SHA.
- `results/`: sechs exakte Ergebnisdateien und Replay-Nachweis.

## Nachrechnen

Python 3.10 oder neuer; Analyse und Replay benötigen nur die Standardbibliothek.
Aus diesem Verzeichnis:

```bash
python3 -O -B analyze.py
python3 -O -B replay.py
python3 -B verify_package.py
```

Die Analyse enumeriert natürliche Ordnungen bis n=6 unabhängig von der
Idealerzeugung. Sie prüft exakte Wirkungsinkremente, Uhrschnitt-Komposition,
Zustandssummen, Restschranken und die beiden verschiedenen Gewichtskandidaten.
Der Replay erzeugt die sechs Dateien aus den Eingaben in einem frischen
Verzeichnis und verlangt Bytegleichheit. Das ist Wiederholbarkeit, keine
unabhängige wissenschaftliche Replikation oder formale Beweiszertifizierung.

`build_report.py` benötigt zusätzlich ReportLab und DejaVu-Schriften.
`package.py` erzeugt nach der Berichtskontrolle ein deterministisches Archiv.
Beim Nachrechnen das ausgelieferte Originalarchiv als Referenz behalten;
Neuverpackung darf nicht als unverändertes Original bezeichnet werden.

## Präzise Grenzen

Die endlichen T-Gitter und binären Dichtemarken sind algebraische Kontrollen,
keine nachgewiesene Quadratur der kontinuierlichen Feldintegration. Die
kontinuierlichen Norm- und unendlichen Restaussagen werden analytisch bewiesen.
Die Ergebnisse bleiben an den gewählten monotonen Uhrsektor und das lokale
Historienprodukt gebunden. Die scharfen Historienwahrscheinlichkeiten sind
blind gegenüber der reellen Wirkungsphase. Eine physikalisch gewählte kohärente
Randkontraktion oder ein Dekohärenzfunktional bleibt eine gesonderte Aufgabe.

Kein Monte Carlo, keine neuen 4D-CST-Ensembles und keine bezahlten Läufe.
Quellen werden verlinkt, nicht als externe Volltexte weiterverteilt.
