# Feste Uhrintervalle und variable Elementzahl v0.1

Veröffentlichtes Arbeitspaket vom 7. November 2026. Ausgangspunkt ist
Main `3a26651cb1476b5e3b5d89c343e11487a012e432` nach PR 252.

## Ergebnis und Voraussetzungen

Keine, eine oder mehrere neue Elemente werden zwischen festen relationalen
Uhrwerten gemeinsam behandelt. Bei vollständiger vergangener Ordnung samt
allen Uhr- und Dichtemarken ist die Zusammensetzung exakt: Der Uhrschnitt
bestimmt das Zwischenpräfix eindeutig, die Wirkungsdifferenzen teleskopieren.
Ein endlicher Gesamtzahlregulator muss für alle Intervalle derselbe sein.

Die unveränderte orthogonale Historien-L2-Norm divergiert ohne Elementzahlgrenze
auf jedem positiven Uhrintervall bei nichtverschwindendem konstantem
Geburtsfaktor. Eine Zweischichtfamilie liefert bereits die untere Schranke
`E_P(k) >= 2^floor(k^2/4)`; die positiven Normsummanden gehen nicht gegen null.
Dieser **FAIL betrifft den erklärten lokalen Normkandidaten**, nicht alle
oszillierenden Amplitudensummen, anderen Produkte oder die CST insgesamt.

Zwei ausdrücklich zusätzliche Zahlgewichte
`f_alpha(n)=2^(-alpha*n*(n-1)/4)`, alpha=1 oder 2, erhalten über den Quotienten
`f(n)/f(m)` die Komposition und kontrollieren die unendliche Summe.
Die Schranke `Z_infinity(P,h) <= exp(|z|^2*h)` ist uniform in der alten Größe
und Geometrie. Ein gemeinsamer Enduhrwert und der Quotient der verbleibenden
Zustandssummen liefern einen normerhaltenden, schnittkompatiblen
Referenztransport. Die Einzelintervalle unabhängig zu normieren wäre dagegen
nicht kompatibel. Isometrie ist bewiesen; Surjektivität wird nicht behauptet.

Die beiden Zahlgewichte ergeben verschiedene Wahrscheinlichkeiten. Auch im
unbegrenzten Fall sind die zertifizierten Intervalle für keine Geburt
disjunkt. Gewichte, Enduhrwert und Skalarprodukt sind dadurch noch nicht
physikalisch ausgewählt. Diagonale Historienwahrscheinlichkeiten bleiben
blind gegenüber der reellen Wirkungsphase; eine kohärente Randkontraktion
oder ein Dekohärenzfunktional muss separat begründet und geprüft werden.

**MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben jeweils HOLD.** Kein physikalischer Hamiltonoperator,
keine globale Vakuumuhr, kein Junction-Gesetz und kein globaler Bounce sind
hergeleitet. Die bedingte Referenzkonstruktion hebt frühere spezifische
FAILs nicht auf und beweist keine allgemeine Singularitätsauflösung.

## Artefakte

- [Bericht (PDF)](../reports/CST_DUST_Uhrintervalle_Variable_Elementzahl_v0_1.pdf)
- [Originales Prüfpaket (ZIP)](../packages/CST_DUST_Uhrintervalle_Variable_Elementzahl_v0_1_Pruefpaket.zip)
- [Vollständige Herleitung und Geltungsgrenzen](DERIVATION.md)
- [Maschinenlesbarer Intervallvertrag](interval_contract.json)
- [Nachrechnung und Nutzung](README.md)
- [Ergebnisse und Status](results/verification.json)

## Verifikation

Die unabhängige Relationsenumeration ergibt 4.824 natürliche Ordnungen bei
n=6. Geprüft werden 10.853 markierte Wirkungsrecords, 32.559 Wirkungsprüfungen
an Uhrschnitten, 97.677 Zahlgewicht-Kozyklen, je 198 Zustandssummen- und
Rückwärtsgleichungsidentitäten, 108.441 gemeinsame-Horizont-Koeffizienten,
102 uniforme Gewichtsgrenzen und 24 Restkontrollen. Sechs Ergebnisdateien
werden in einem frischen Verzeichnis bytegleich reproduziert.

Vom Repository-Stamm aus, Python 3.10 oder neuer, nur Standardbibliothek:

```bash
python3 -O -B research/rax_cqg/dust_collapse/clock_intervals_v0_1/publication_check.py --replay
```

Der Publikationsprüfer kontrolliert das Originalarchiv, alle 30 Mitglieder,
29 Manifest-Prüfsummen, beide PDF-Kopien, den eingefrorenen Plan, sechs
bytegleiche Repositoryquellen sowie die Ergebnisgrenzen. Der Workflow
`cst-dust-clock-intervals.yml` führt Integritätsprüfung und isolierten Replay
auf Pull Requests und Main aus.

Die Gitter dienen algebraischen Kontrollen und sind keine zertifizierte
Quadratur der kontinuierlichen Feldintegration. Allgemeine und unendliche
Aussagen werden analytisch bewiesen; es wurde kein formaler Beweisassistent
eingesetzt. Wiederholbarkeit ist keine unabhängige wissenschaftliche Replikation.
Keine neuen physikalischen 4D-Ensembles und keine bezahlten Läufe.

| Objekt | SHA-256 |
|---|---|
| Original ZIP | `673007adcbb2e4fd3660a31a366e311f11b4225375b5e7c38695734bec5d5974` |
| PDF | `49439bc26b564babbdab6d80d03f4fb9ef1cf628bdf117c09653a42c91adbbba` |
| Plan | `6e9655943c1b715a4de23fbec110061c2e63748002e000f572dcdc38afdf3acc` |

Alle Originaldateien bleiben unverändert. Diese Publikationsnotiz, der
Repository-Prüfer, CI und Index-/Integritätsdateien werden separat ergänzt.

## Nächster physikalischer Test

Eine deklarierte kohärente Randkontraktion oder ein Dekohärenzfunktional
gegen Positivität, Norm und Uhrschnittkompatibilität prüfen. Die kontrollierten
Zustandssummen sind dafür Bausteine. Eine physikalische Theorie muss zusätzlich
die Zahlgewichte, den Randzustand und die Ereignisstruktur begründen und
gravitative Interferenz in der gewählten Auslese erklären.
