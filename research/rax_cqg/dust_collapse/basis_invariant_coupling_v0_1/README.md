# CST-DUST: Basisunabhängiger Kopplungsbefund v0.1

12. November 2026. Vollständiger 6×6-Differenzblock für festgelegte Test- und Eingangsbereiche mit der gewichteten V-Norm; zusätzlich vollständiger 4×2-Atom→Positiv-Block.

Der Kontrollpunkt umfasst alle ursprünglichen 33 AA-Historien, Gewicht 1/33, volle Gravitationsphasen, die bisherige auf Wirkungsebene festgelegte Entkopplung und alle inneren Dichtemasken. Zustände: drei symmetrische Dichtepakete (Atom, Positiv, Kontrast) mal zwei gerade Feldpakete (Grundzustand und radiale Anregung), konstante Uhrpakete.

| V-normierte Größe | Gesamter 6×6-Block | Atom→Positiv, 4×2 |
|---|---:|---:|
| größte Singularzahl von K1−K0 | 0.032602301976 | 0.012323446639 |
| zusammenhängender Historienanteil | 0.007251598185 | 0.003652388389 |
| Änderung der mittleren Skalarantwort | 0.030294483160 | 0.010489512041 |

Jede angezeigte Zahl hat eine **deterministische absolute Einschließung ±10^-12**, einschließlich Tabellenrundung. Die Blöcke addieren sich exakt; ihre Normen sind nicht additiv. Ergebnisse sind keine Wahrscheinlichkeiten oder Prozentwerte.

Die exakte Feld-Gram-Matrix in V lautet [[65,196],[196,913]]. Bloßes Normieren einzelner Basisvektoren würde den Überlapp 196 übersehen. Alle Matrizen und Fehler werden mit der vollständigen Gram-Matrix transformiert.

Auch die vorher konstruierten strikt positiven Gewichte, die den alten Grundpaketeintrag exakt auslöschen, lassen den Gesamtblock von null getrennt: größte Singularzahl etwa 0.008446681427; im Atom→Positiv-Bereich 0.001702265450. Diese Gewichte werden aus ihrer früheren Definition neu eingeschlossen und nicht am neuen Block optimiert.

## Aussage und Grenzen

Zertifiziert ist die Norm der eingeschränkten Antwort `R_F(K1-K0)|_E : E -> Fprime`, wobei E und F die deklarierten Unterräume von V sind. Sie ist die maximal erreichbare absolute Testantwort bei V-Einheitsnorm beider Zustände. Das ist basisunabhängig, aber abhängig von den gewählten Räumen, ihrer Norm, der Wirkung und den Historiengewichten.

Der Differenzblock hat exakt Rang zwei und vier Nullrichtungen auf der Eingangsseite. Es gibt daher empfindliche Zustände und zugleich unempfindliche Zustände. Es wird keine positive Untergrenze für jeden Eingang, keine volle V-Operatornorm, keine kompakte Reduktion aller Antworten und keine physikalische CST-Evolution behauptet. Kein neuer 1089-Historienlauf.

## Reproduktion

Python 3.12, python-flint 0.9.0, NumPy, SciPy und SymPy; genaue ausgeführte Versionen in environment.json. Keine Netzwerkdienste im Rechenlauf.

```sh
python -m pip install -r requirements.txt
python -B verify.py
```

`verify.py` prüft alle Hashes, führt die 40-Knoten-/192-Bit-Rechnung in einer temporären Kopie neu aus, verlangt bytegleiche numerische Dateien und führt 13 Kontrollgruppen aus. `python -B compute.py` regeneriert die lokalen Ergebnisse bewusst. `python -B tests.py` prüft die vorhandenen Ergebnisse. PDF-Neubau: `python -B build_pdf.py` mit TeX Live.

## Dateien

- `contract.json` und Hash: vor der neuen Blockauswertung festgelegte Bedingungen; kein externer Zeitstempel.
- `compute.py`: analytische Gaußmomente, volle Historiensumme, V-Normierung und Singularwertzertifikate.
- `tests.py`: unabhängige direkte fünfdimensionale Quadratur, Schur-Eigenphasen, exakte Gram-Momente, Basiswechsel und Auslöschungskontrollen.
- `results/uniform.json`: alle fünf vollständigen 6×6-Blöcke vor und nach V-Normierung, 4×2-Teilblöcke, Fehler und zwei unabhängige Singularwertzertifikate.
- `results/cancellation_control.json`: dieselben Blöcke für die vorher definierten Auslöschungsgewichte.
- `results/quadrature.json`: alle zehn Orbitbeiträge, inklusive aller 33 Historienlabels und analytischer Fehlergrenzen.
- `DERIVATION.tex`, PDF: vollständige mathematische Herleitung und expliziter normierter Differenzblock.

Quellbasis: Main d7acdb6a2558bbec0b6c2c208742debc55479e75 und aktuelles Prüfpaket Mischungsqualifikation v0.1; siehe provenance.json. Apache-2.0.
