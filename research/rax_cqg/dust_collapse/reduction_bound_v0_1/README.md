# CST-DUST: Obere Reduktionsfehlergrenze v0.1

Für die ursprünglichen 33 Historien wird der **vollständige ausgelassene Modenrest** analytisch nach oben beschränkt. Die Testtopologie ist unverändert `V = L²_inv((1+|q|²)^4 dμ)`, die Antwortnorm `V′`. Die vier bisherigen Eingänge, alle kohärenten Überlagerungen und beim Einzelkern die größere Klasse `C_M = {f in V: ||f||_H ≤ 1, ||f||_V ≤ sqrt(261)}` sind abgedeckt. Rückwärts gerichtete Paarungen haben eigene Konstanten.

Die 1089 minimal verklebten Historien erhalten eine gesonderte Schranke für äußere Zustände in der H-Einheitskugel des ursprünglichen Vierzustandsraums. Dabei bleiben Schnittinzidenzen, Intervallprofile und frühere Felder des erweiterten Randvertrags erhalten. Eine Projektion bedingter, regulierter Schnittfunktionen ist nicht mit der Multiplikation zweier integrierter L²-Kerne gleichzusetzen.

## Ergebnis

| Zertifikat | Analytische obere Grenze | Hinreichende Basisgröße |
| --- | ---: | ---: |
| Einzelkern, gesamte Klasse C_M | < 0,009003549 in V′ | 3 384 672 308 841 108 222 |
| Gemeinsame Paarung, beide äußeren Zustände in E4 | < 0,000969398 vor numerischer Koeffizientenauswertung | 35 026 448 697 292 180 628 528 179 868 001 600 |

Diese konservativen Basisgrößen wurden **nicht** als Matrizen aufgebaut und sind **keine** Mindestgrößen. Beim dokumentierten Limit von 1 000 000 Moden lautet die praktische Entscheidung **HOLD**. Die Schranke beweist keine kompakte Reduktion mit Fehler 0,01. Sie liefert erstmals ein vollständiges Restbudget und eine klare Abbruchregel.

Exakte Nullkombinationen der vier Eingänge schließen eine gleichmäßige relative Fehlerdefinition aus. Die Fehler sind absolut. Die ursprüngliche Aussage, dass der Kern nicht alle normierten H-Zustände wieder nach H abbildet, bleibt bestehen.

## Reproduzieren

Python 3.12, SymPy 1.14.0, python-flint 0.9.0; NumPy 2.3.5 nur für unabhängige Tests. Keine Netzabfragen, Zugangsdaten oder bezahlten Dienste im Rechenlauf.

```bash
python -m pip install -r requirements.txt
python -B verify.py
python -B check_budget.py --field 24 --density 3 --clock 8
python -B check_budget.py --field 24 --density 3 --clock 8 --composition
```

`verify.py` prüft alle Datei-Hashes und eingefrorenen Git-Blobs, führt zehn Testgruppen aus und regeneriert die sechs Ergebnisdateien in einer temporären Kopie. Die Ergebnisse müssen bytegleich sein. Die vollständigen 1089 Gaußpaarungen werden berechnet; große Galerkinmatrizen werden nicht berechnet.

Die Einzeldateien können auch direkt erzeugt werden:

```bash
python -B certify.py
python -B basis.py --output results/basis_6_0_2.json
python -B tests.py
```

Für ein mathematisches Toleranzzertifikat ohne den kleinen Ressourcenrahmen:

```bash
python -B check_budget.py --field 151306 --density 124 --clock 192 \
  --mode-cap 4000000000000000000
```

Dieser Aufruf wertet nur die analytische Fehlerformel aus. Ein realer Koeffizientenrechner muss über `--numerical-error` seine zusätzlich zertifizierte Fehlergrenze angeben. Der Wert null bezeichnet die exakte mathematische Projektion, keinen experimentell fehlerfreien Rechner. Überschreitung des Modenlimits hat Vorrang vor `TOLERANCE_PASS`.

## Dateien und fachliche Grenze

- `DERIVATION.tex` und PDF: Definitionen, zwei Restabschätzungen, Herleitung und Grenzen.
- `bounds.py`: exakte Momente, gewichtete Restschranken und bedingte Schnittreste.
- `basis.py`: vollständige verschachtelte Modenlabels und exakte Einbettung der vier Eingänge; Startbasis 516 Moden, vorherige 15 Zustände enthalten.
- `certify.py`: 192-Bit-Arb-Einschließungen, alle 33/1089 Historien und Abelvergleich gegen den analytischen Grenzwert.
- `check_budget.py`: `EXTEND_BASIS`, `TOLERANCE_PASS` oder `HOLD_RESOURCE_CAP` anhand der vollständigen Grenze.
- `tests.py`: unabhängige kartesische Momente, gradgenaue kompakte Gaußkontrollen, eigene Gaußphasenrechnung, Einbettungen und Abbruchentscheidungen.
- `contract.json`, `provenance.json`: Geltungsbereich, exakter Quellstand und acht eingefrorene Inputs.
- `results/`: sechs reproduzierbare Ergebnisdateien.
- `SHA256SUMS.json`: Integrität aller übrigen Paketdateien.

Die Topologie bestimmt neue Test-/Antwortprojektoren: Antwortmoden sind die gewichteten Dualmoden, nicht die Testmoden selbst. Bereits enthaltene Testpaarungen werden erhalten. Beim Schnitt müssen gelabelte bedingte Moden beibehalten werden; eine vorzeitige Invarianzprojektion verliert Gedächtnisinformation.

Nicht umfasst sind beliebige CST-Historien, Schnittumgehungen, andere Kopplungen, unendliche Volumen-/Feldgrenzen außerhalb des deklarierten Vertrags oder ein globaler Operatornormsatz für die verklebte Amplitude auf ganz V. Das Paket beweist keine physikalische Evolution, kein Bounce-Gesetz und keine Singularitätsauflösung.

Die Standarddefinitionen der Hermite-/Legendrefunktionen stehen in [DLMF §18.3](https://dlmf.nist.gov/18.3) und [DLMF §18.8](https://dlmf.nist.gov/18.8). Die konkreten Restgrenzen werden im Paket hergeleitet. Ausgangsstand: `thomasmgfeller/x6-spectral-astrolabium`, Main `3b6a186749b313ea59f43292e43052451dc4941c`.

Lizenz: Apache-2.0. PDF optional mit `python -B build_pdf.py` und vollständigem TeX Live neu bauen.
