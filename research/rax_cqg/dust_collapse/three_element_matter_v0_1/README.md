# CST-DUST: kontinuierlicher Drei-Element-Sektor v0.1

Die kontinuierliche Materiephase ist für alle sieben natürlich beschrifteten
Drei-Element-Ordnungen im geerbten Referenzmaß integriert. 36 Kombinationen
aus Uhrhorizont, Zahlgewicht und Kopplungen besitzen rationale Fehlerzertifikate.
Die obere Schranke der noch nicht integrierten Phasensektoren sinkt um
91.36 bis 99.44 Prozent. Feldphasen ab n=4 bleiben offen.

**Alle acht physikalischen Gates bleiben HOLD.** Dies ist eine konditionale
Referenzrechnung, keine Auswahl eines physikalischen Detektors oder einer
Endrandbedingung und keine Herleitung von Rückwirkung, Bounce oder Junction Law.

## Inhalt

- `DERIVATION.md`: Modell, Beweise, Fehlerbudget und Interpretation.
- `plan.json`, `plan.sha256`: vor der neuen Integralrechnung eingefrorener Plan.
- `three_element_contract.json`: maschinenlesbare Aussagegrenzen.
- `inputs/`: acht byteidentische, auf Main nach PR 255 gepinnte Quellen.
- `geometry.py`: exakte Wirkungs- und Bernstein-Polynome.
- `intervals_fp.py`, `gauss.py`, `integrate.py`: nach außen gerundete Rechnung.
- `results/`: rationale Amplituden, Integrationszertifikate, Normreste und Replay.
- PDF: deutschsprachiger Ergebnisbericht.

## Nachrechnen

Python 3.12, ausschließlich Standardbibliothek für die wissenschaftliche Rechnung:

```sh
python3 -O -B analyze.py
python3 -O -B replay.py
python3 -B verify_package.py
```

Die Rechnung umfasst 3780 vollständige Wirkungs-/Inkrementkontrollen,
56 exakte niedrige Momente, drei Vergleiche gegen frühere Momentreihen,
Gaußnullstellen- und Gewichtszertifikate sowie 36 Intervall-Inklusionen.
Ein isolierter Replay reproduziert alle sechs Ergebnisdateien bytegleich.
Das ist Wiederholbarkeit derselben Implementierung, keine externe Replikation.

Die PDF-Erzeugung benötigt zusätzlich ReportLab und DejaVu Sans:

```sh
python3 -B build_report.py
python3 -B package.py
```

Der umfangreichste Integralfall nutzt 20×22×30 Punkte, mit Wiederverwendung
gleicher Dichtepolynome über die sieben Geometrien. Kein Zufallsensemble und
keine Cloud-Rechenleistung sind erforderlich. Architekturabhängige Laufzeiten
sind kein Bestandteil der Zertifikate.

## Anschluss

Nächster quantitativer Kandidat: n=4 mit vorherigem Kostenbudget. Der grundlegende
physikalische Schritt bleibt die Begründung von Dichtemaß, kohärentem Zugriff
und Endrandwahl aus einer vollständigen CST-Amplitude.

Apache-2.0; Quellen und Grenzen siehe `NOTICE` und `inputs/provenance.json`.
