# CST-DUST · Hängt der N15-Randtest von der Geburtsbeschriftung ab?

**21. November 2026 · Ergebnis für Typ 375841, markierte Masse 1/4, Anfangsdichtezentrum 1/8**

**35 von 35 Geburtsreihenfolgen ergeben dieselben beiden komplexen Randzustände und dieselbe Dekohärenzmatrix nach Rücktransport.** Das gilt auf der gesamten Zukunftsbox für die zwei offenen Feinhistorienpakete aus PR #338. Das positive Paket behält sein positives Stromvorzeichen, das negative sein negatives. Damit bleibt auch das im Randtest gefundene Hindernis für die Vorzeichenauslese unter allen zulässigen Geburtsbeschriftungen dieses Typs erhalten.

[Ausgangsversuch auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/n15_future_boundary_v0_1)

## Was geprüft wurde

Die vier Ereignisse des Vergangenheitskragens und die vier des Zukunftskragens sind jeweils total geordnet. Dazwischen liegen zwei voneinander unabhängige Ketten aus drei und vier Ereignissen. Jede der 35 Möglichkeiten, die Ketten unter Erhaltung ihrer internen Reihenfolge zu verschachteln, erhält aufsteigende Geburtsnummern von 0 bis 14. Eine topologische Aufzählung und eine unabhängige Prüfung aller 7! inneren Permutationen ergeben dieselbe Menge. Die Rechnung hat 35 verschiedene beschriftete Darstellungen derselben dekorierten Ordnung erzeugt. In der Ensembleamplitude wird dieser Typ weiterhin einmal gezählt.

| Vergleich nach Rücktransport | Ergebnis |
|---|---|
| Intervallkoeffizienten, skalarer quadratischer Wirkungsanteil, geordnete Randrollen, Staubpfade und Präparation | Exakte Übereinstimmung in allen 35 Fällen. Die Gravitationswirkung hat jeweils den Wert 7. |
| Strom im Zentrum des positiven Pakets, in Einheiten von M | 1429581 / 190000000. Die rationale Einhüllung der ganzen Zelle liegt in (0,0074, 0,0077). |
| Strom im Zentrum des negativen Pakets, in Einheiten von M | −1004581 / 190000000. Die rationale Einhüllung der ganzen Zelle liegt in (−0,0054, −0,0051). |
| Komplexe Randamplituden | Exakter Transport beider Funktionen über die gesamte Zukunftsbox. Grösste numerische Abweichung an den ausgewerteten H3-Feldpunkten im Referenzlauf 3,33 × 10⁻¹² (aufgerundet). |
| Alle vier komplexen Einträge der Dekohärenzmatrix | Exakt derselbe positive Wert γ in jedem Eintrag. Grösste numerische Abweichung vor Spurnormierung in der gemeinsamen Recheneinheit 4,45 × 10⁻¹⁶ (aufgerundet). |
| Gewichte | Im bedingten Randtest ist das Einzeltypgewicht 1. In der separat geprüften N15-Basistabelle mit A:B = 1:1 beträgt sein Amplitudenkoeffizient 1/40000000. Alle 35 Kodierungen führen über die Isomorphieklasse zum selben Archiveintrag. |

Die Dezimalwerte hängen von der numerischen Umgebung ab. Die Differenz der **exakt transportierten** Wirkungskoeffizienten beträgt null. Die Tabellen der 35 Fälle stehen in [der CSV-Datei](resultate/35_beschriftungen.csv) und im ausführlichen [Laufprotokoll](resultate/ergebnis.json).

## Weshalb die Aussage ganze Pakete und die volle Matrix erfasst

Sei σ die Abbildung von den bisherigen Ereignisnamen auf eine Geburtsbeschriftung. Auf der neu erzeugten Relation zählt der Prüfer für jedes geordnete Paar die inneren Intervallereignisse neu. Für alle Paare ergibt sich b′(σi, σj) = b(i,j). Damit stimmen nach Rücktransport die Gravitationsphase, sämtliche Koeffizienten der Staubwirkung und die gesamte skalare Hesse-Matrix vor der Elimination überein. Die äusseren Skalar- und Eichrichtungen bleiben an ihren geordneten Kragenrollen. Die Permutation der inneren Integrationskoordinaten erhält das Produktmass, den symmetrischen Skalarregulator und seine Fresnelgrenze.

Alle maximalen inneren Pfade, ihre Uhrzentren und ihre Länge werden neu bestimmt. Die Verweildichten f entstehen aus den Mittelpunkten auf genau diesen Pfaden. Die geordnete Dreiermarkierung der Dichteverschiebung wird auf dieselben Ereignisse übertragen. Damit stimmen auch die uhrabhängige Verschiebung d, beide Gebiete x = f ∓ d + ξ, die Grenzen der positiven Dichten und die Stromfunktion p unter der Variablensubstitution überein. Die rationale Intervallrechnung für beide ganzen Zellen wurde je Beschriftung wiederholt. Die äussere Uhröffnung, die gemeinsame Eingangsdichte, die sieben Zukunftsvariablen und das flache Zukunftsmass werden in derselben Rollenreihenfolge ausgewertet.

Die Substitution hat absoluten Jacobi-Faktor eins. Alle übrigen mass- und uhrabhängigen Faktoren sind identisch. Deshalb gilt für jedes z der Zukunftsbox und beide Vorzeichen F′χ′±(σz) = Uσ Fχ±(z), wobei Uσ den Rand in die mitgeführte Basis überträgt. Durch Paarung beider Funktionen mit demselben Randmass folgt die Gleichheit aller vier **unnormierten** Matrixelemente. Auch der gemeinsame Faktor bleibt erhalten. Der Referenzversuch reproduziert zwei identische, von null verschiedene Paketbilder v. Somit ist D = γ [[1,1],[1,1]] mit γ = ‖v‖² > 0. Der Vektor χ₊ − χ₋ hat Randnorm null. Sein positiv selektierter Anteil hat Normquadrat γ. Diese Aussagen beziehen sich auf das Referenzskalarprodukt aus PR #338.

## Numerische Gegenrechnung

Die H3-Ausgangsgaußfunktion einschliesslich Fresnelphase wird je Darstellung mit der archivierten Skalarreduktion neu aufgebaut. Die Präzisionsmatrix der Ausgangsdarstellung wird zusätzlich mit den sechs archivierten exakten Einträgen verglichen. Für die Staubamplitude integriert der Prüfer die gemeinsame Eingangsdichte und die sieben Dichteabweichungen ξ analytisch. Für e und sieben innere Uhren werden 64 und 128 gescrambelte Sobol-Punkte benutzt, für das Zukunftsintegral 16 und 32 weitere Punkte. Die Vergleichsläufe transportieren dieselben physikalischen Stützstellen. Jeder Lauf berechnet die Amplituden beider Pakete aus seinen Eingaben. Die vier Matrixelemente entstehen durch Paarung in H3 und Mittelung am Zukunftsrand.

Für die Zahlenrechnung sind feste gemeinsame Koordinatenvolumina und der zentrale Wert von D_T¹⁴ ausgeklammert. Das uhrabhängige Verhältnis (D_T/D_T,0)¹⁴ bleibt im Integral. Die Matrix wird in dieser gemeinsamen Einheit vor Spurnormierung verglichen. Alle Beschriftungen verwenden dieselben Phasen- und Normkonventionen. Die komplexen Staubkoeffizienten werden an allen ausgewählten Zukunftspunkten verglichen, die vollständige Wellenfunktion zusätzlich an drei H3-Feldpunkten je Zukunftspunkt. Das numerische Kriterium lautet |a−b| ≤ 2 × 10⁻⁸ (1 + |b|). Die Übereinstimmung auf der gesamten Box folgt aus dem exakten Variablenwechsel. Das Paket bestimmt keinen absoluten physikalischen Wert für γ.

## Zwei absichtliche Fehler

- **Dichtemarkierung an der alten Geburtsstelle belassen.** Nach dem Tausch der Ereignisse 5 und 6 muss die Markierung des Ereignisses 5 auf Geburtsplatz 6 liegen. Belässt man sie auf Platz 5, lauten die zentralen Ströme 1754179/380000000 und −904179/380000000. Die Vorzeichen bleiben erhalten. Beide exakten Werte verletzen das Vergleichskriterium.
- **Vorzeichenselektoren vertauscht.** Die beiden zentralen Ströme wechseln den Ausgang. Die Kontrolle mit festgelegter Vorzeichenreihenfolge erkennt den Fehler. Die exakte Zweipaketmatrix bleibt bei diesem Tausch unverändert.

## Reichweite und Wiederholung

Für den Test wurde der Prüfvertrag vor dem ersten Lauf dieser neuen Rechnung lokal mit SHA-256 festgehalten. Die Modellierung und die beiden Referenzpakete waren bereits bekannt. Der Vertrag ist in [pruefvertrag.json](pruefvertrag.json) enthalten. Der Basisvergleich der Gewichte rekonstruiert die Isomorphieklasse aus jeder nativen Relation und sucht ihren Archivschlüssel in den beiden publizierten Endtyptabellen. Das dort festgelegte gleiche Elterngewicht ist berücksichtigt. PR #338 spezifiziert keine elementaren Übergangsgewichte für die einzelnen Geburten. Die Pfadunabhängigkeit eines künftigen dynamischen Wachstumsgesetzes bleibt daher offen. Ebenso offen bleiben die physikalische Paarung und die P3-Kalibrierung. Alle 60 physischen P3-Checkpoints stehen weiterhin auf NOT_RUN.

Mit Python, NumPy und SciPy lässt sich das entpackte Paket lokal ausführen. Getestet mit Python 3.12.14, NumPy 2.3.5 und SciPy 1.17.0. Ein Durchlauf benötigt auf dem verwendeten Rechner wenige Sekunden.

```sh
sha256sum -c SHA256SUMS
OPENBLAS_NUM_THREADS=1 python -B pruefen.py --output wiederholung
```

Der Prüfer wiederholt zuerst den archivierten Referenzversuch und prüft dessen Ergebnis bytegenau. Danach erzeugt er die 35 neuen Resultate und prüft den Vertrag, die Negativkontrollen und die numerischen Schranken. Alle Eingaben liegen bei. Die Herkunft der übernommenen Dateien und des Einzeltypauszugs ist in [quellen.json](quellen.json) dokumentiert.
