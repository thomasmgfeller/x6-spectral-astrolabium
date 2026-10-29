# Eigenzeit / CSPP: Varianzbudget v0.4

**Ergebnis:** Für den unveränderten Gauß-Zeugen ist die bisherige hinreichende
Punktzahl um knapp 15 Größenordnungen reduziert. Zugleich weist eine neue
positive Varianzuntergrenze einen erheblichen notwendigen Aufwand nach.
Die exakte erforderliche Dichte ist noch nicht bestimmt. **G1 bleibt HOLD.**

Stand: 27. Oktober 2026. ell_k=0.125 L0, Feldbreite L=2 L0,
D_20, Poisson-Sampling, fester Auswertungspunkt. Alle Punktzahlen sind
**Erwartungswerte**, keine harten Schranken für realisierte Poisson-Zahlen.

| Aussage | Erwartete Punkte |
|---|---:|
| Bisheriges hinreichendes Budget für 7 % stochastischen RMS | 2.87 × 10^39 |
| Neue hinreichende Garantie für dieselben 7 % | 4.25 × 10^24 |
| Neue notwendige Mindestzahl für dieselben 7 % | 1.94 × 10^12 |
| Neue notwendige Mindestzahl für 10 % gesamten RMS | 1.13 × 10^12 |

Die 7 % beziehen sich auf den Betrag der lokalen Kontinuumsreferenz 0.5,
also auf eine absolute Standardabweichung von 0.035. Die letzte Tabellenzeile
verwendet stattdessen direkt das Gesamtziel samt bereits eingeschlossenem Bias.
Zwischen notwendiger und hinreichender Zahl wird keine Machbarkeit behauptet.

Die mathematische Verbesserung besteht aus vier Teilen:

1. Die tatsächliche Gauß-Abnahme wird integriert und die Schichtmomente werden
   durch endliche Gamma-Summen eingeschlossen.
2. Ein exakter Paar-Kovarianzkern behandelt die gemeinsame Poisson-Masse und
   die beim Einfügen von Endpunkten veränderten Intervallzahlen.
3. Eine positive Einschränkung der ersten Chaos-Norm liefert eine ausgewertete
   Untergrenze, ohne räumliche Quadratur und ohne neue Poisson-Wolken.
4. Bias, Randfehler und stochastische Varianz bleiben getrennt; die bestehenden
   E4-Gates und Quellenreferenzen werden nicht ersetzt.

Die vollständige räumliche Integration des Paar-Kovarianzkerns ist noch offen.
Die neue Obergrenze nutzt für den Überlappungsbeitrag eine sichere
Cauchy-Schwarz-Hülle. Sie ist deshalb weiterhin konservativ.

## Sieben Skalen, unveränderte stochastische Teilallokation

| ell_k/L0 | H/L0 | Neues hinreichendes E N | Garantierte obere Gesamt-RMS-Grenze |
|---:|---:|---:|---:|
| 0.125 | 20 | 4.25 × 10^24 | 8.045 % |
| 0.1875 | 20 | 3.28 × 10^22 | 10.118 % |
| 0.25 | 20 | 1.04 × 10^21 | 13.062 % |
| 0.5 | 16 | 1.04 × 10^17 | 27.776 % |
| 1 | 16 | 2.55 × 10^13 | 51.001 % |
| 1.5 | 16 | 1.97 × 10^11 | 62.947 % |
| 2 | 16 | 6.26 × 10^9 | 68.648 % |

Eine obere RMS-Grenze oberhalb des Ziels beweist allein keine Unmöglichkeit.
Für die letzten fünf Zeilen besteht allerdings bereits der separate
Bias-Ausschluss aus v0.3. Bei ell_k=0.1875 ist eine andere stochastische
Teilallokation nicht ausgeschlossen; die bisherige 5-%-Bias-Allokation wird
aber überschritten. Nur die erste Zeile erfüllt die beibehaltene Gesamtallokation.

## Reproduzieren

Python 3.12. Getestet mit python-flint 0.8.0, NumPy 2.3.5 und SciPy 1.17.0.

```bash
python -m pip install -r requirements.txt
python run.py
python audit.py
```

Der Audit bestand: 253 exakte Identitäten, 36 unabhängige Poisson-Summenvergleiche,
zwei Negativkontrollen, acht Momentprüfungen und kompletter 192-Bit-Replay.
Es handelt sich um interne mathematische/Software-Prüfungen, nicht um externes Peer-Review.

- [METHODS.md](METHODS.md): Herleitung, Beweis der Untergrenze, Einheiten und Grenzen.
- [variance.py](variance.py): Gewichtsmomente, exakter Paar-Kern, obere/untere Schranke.
- [results/BUDGET.json](results/BUDGET.json): 128-Bit-Ergebnisse und Herkunft der Baseline.
- [results/BUDGET_192bit.json](results/BUDGET_192bit.json): höherpräziser Replay.
- [results/AUDIT.json](results/AUDIT.json): ausgeführte Kontrollen.
- [baseline/](baseline/): unveränderte gelesene v0.3-Eingaben.

Der nächste rechnerische Engpass ist die große Lücke zwischen den Schranken.
Die bereits implementierten exakten gemeinsamen Momente ermöglichen eine
gezielte räumliche Auswertung, die Vorzeichen und Überlappungsvolumina erhält.
Die bewiesene Untergrenze zeigt jedoch bereits: Der alte 20.000-Punkte-Screen
kann den betrachteten Einzelwolken-Zeugen mit diesem unveränderten Operator,
dieser Skala und diesem Gebiet nicht qualifizieren. Daraus folgt keine
Unmöglichkeit anderer Schätzer oder Versuchsdesigns.
