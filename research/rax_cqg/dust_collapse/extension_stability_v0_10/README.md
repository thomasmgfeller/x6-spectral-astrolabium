# CST-DUST · Wie viel Amplitudengewicht verträgt der N15-Test?

Etappe 1, v0.10, 19. November 2026. Ausgangspunkt ist das eingefrorene Modell aus [PR 314](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/314). Die Daten beziehen sich auf `main` bei `1ddcfcfb8db1572c17c087ddbb884d93f9bf285b`.

## Fragestellung und Entscheidung

Die zwei N11-Eltern beginnen mit je ½ Amplitudengewicht. Beide übertragen denselben Anteil λ auf ihre erreichbaren Nachkommen. Innerhalb ihrer jeweiligen Menge von 1 163 bzw. 1 211 Nachkommen darf jede Elternhistorie eine eigene beliebige nichtnegative Verteilung mit Summe eins wählen. Bei beiden Anfangsdichten gilt dieselbe Präparation. 5 % entsprechen insgesamt 0,05 des anfänglichen Amplitudengewichts. Die beobachteten Detektorwahrscheinlichkeiten entstehen erst nach der kohärenten Summation.

| Träger und Nachweisart | Abgesicherter Transferbereich auf (32,6) und (48,8) |
| --- | --- |
| 1 217 Zustände, deterministische Rechnung mit den übernommenen numerischen Fehlerradien | 0 bis 4,7074 % (v0.9 bis 4,6904 %) |
| 1 100 Zustände, deterministische Rechnung mit denselben Radien | 0 bis 5 % (v0.9 mit 1 098 Zuständen) |
| Alle 1 217 Zustände, simultane statistische Untergrenzen für die zusätzlich geprüften Uhrantworten | 0 bis 5 %, familienweite Irrtumswahrscheinlichkeit höchstens 10⁻¹² im unabhängigen Gleichverteilungsmodell |

Der Detektor erfasst drei akzeptierte Ausgänge und einen Misserfolg. Die normierte Niveauabweichung ist die Totalvariation der vier Gewichte, geteilt durch den Gesamterfolg des jeweiligen N11-Referenzzustands. Ihre Toleranz ist 10 %. Die relative Änderung des vierteiligen Dichtekontrasts darf 25 % betragen. Die Differenz der Gesamterfolge zwischen hoher und niedriger Dichte muss negativ bleiben. Aus v0.9 folgen bereits beide letzten Aussagen und die Schranken für die sechs echten Teilmengen der akzeptierten Ausgänge sowie für einen Anstieg des Gesamterfolgs. Offen war allein ein zu starker Rückgang des Gesamterfolgs. Alle Angaben setzen die in v0.9 gespeicherten Gram-Spalten, den Detektor, die Uhrenkonvention und die zugehörigen Fehlerradien voraus.

| Anfangsdichte | Gesamterfolg in % der Referenz, statistische Untergrenze auf beiden Gittern (abgerundet) | Typ mit kleinster verbliebener Projektion |
| --- | ---: | --- |
| 1/8 | 90,001834298 % | N15_1011645 |
| 1/4 | 90,000454179 % | N15_46072 |

Die untere Schranke liegt im ungünstigsten Fall um 0,000454179 Prozentpunkte über der Schwelle. Sie deckt jede zulässige Mischung ab. Beide Typen, die den Zahlenwert begrenzen, waren bereits im deterministischen 1 098er-Träger enthalten. Die statistische Rechnung erweitert den Geltungsbereich der früheren Untergrenze. Die numerische Differenz zum unbekannten tatsächlichen Minimum kann deutlich grösser sein.

## Direkter Angriff auf die begrenzenden Uhrantworten

Für den ursprünglich limitierenden Typ **N15_356087** besitzt Uhr 13 fünf Vorgänger mit Koeffizienten (−8,16,−9,1,1). Die Uhren 12 und 13 lassen sich bedingt über zwei reelle Argumente summieren. Mit `x` als Uhrzeit und `e=x13`, `l=x12` gilt

```
U = −8 x4² + 16 x5² − 9 x6² + x11²
V = −8 x4  + 16 x5  − 9 x6  + x11
C13 = 1 + (β/2)(U − 2eV + e² + l² − 2le).
```

`target.py` summiert den bedingten Faktor auf einer Tabelle in U und V. `clock_lookup.c` verwendet je Richtung sechs Interpolationsknoten. Die Hilfsintegration über den gleichverteilten Anteil von H(C) = (1 + ∫₀¹ exp(−iuC/2)du)/2 benutzt 100 Gauss-Knoten. Zwei direkte kartesische Summen auf (4,3) und (5,4) prüfen das Ergebnis unabhängig. Die maximale komplexe Abweichung beträgt 1,01 × 10⁻¹³ (aufgerundet). Die beiden Referenzgitter unterscheiden sich um weniger als 9 × 10⁻¹⁰. Auf (48,8) erhält man bei Anfangsdichte 1/8 den Wert −0,004300720388 + 0,001260444678 i, bei 1/4 den Wert −0,003154749463 + 0,003152257152 i. Geben beide Eltern ihre vollen 5 % an diesen Typ, beträgt die relative Niveauabweichung rund 9,7284 %, die relative Kontraständerung rund 9,7294 %. Das Vorzeichen bleibt negativ.

Die kleinste Stützebenenreserve innerhalb der neuen *Stichprobenergebnisse* erreicht **N15_39485**. Für diesen nach der Stichprobe ausgewählten Typ summiert `near_witness.py` zunächst die Faktoren der Uhren 12, 13 und 14 über ihre jeweiligen Vorgänger. Auf (5,4) unterscheidet sich die direkte kartesische Kontrolle um weniger als 1,2 × 10⁻¹⁷. Die zusätzlichen deterministischen Rechnungen verwenden auf den Referenzgittern den v0.9-Prüfradius 10⁻⁷. Mit diesen beiden Uhrantworten enthält der Träger für 5 % jetzt 1 100 deterministisch abgedeckte Zustände. Die 117 übrigen Typen stehen in `certificate.json`.

Für **N15_356087** wurde das kontinuierliche Integral zusätzlich abgeschätzt. Nach Wiedereinführung der Dichtemarken hat der Integrand in jeder normierten Einzelachse die Form exp(i(Ax²+Bx+C)), bei reellen übrigen Koordinaten und Marken. `continuum_bound.py` begrenzt |A| und |B| durch rationale Intervallrechnung. Auf einer Bernsteinellipse mit Parameter r gilt für den komplexen Betrag die Schranke M = exp(|A|(r²−r⁻²)/4 + |B|(r−r⁻¹)/2). Abschneiden der Chebyshev-Reihe bei Grad 2n−1 und Positivität der normierten Integrationsgewichte begrenzen den eindimensionalen Gaussfehler durch 4 M r^(1−2n)/(r−1). Die achsenweise Teleskopsumme für die Ordnungen (96,68,48,48,24,56,48) und die Randordnung 10 ergibt nach Normierung weniger als 2 × 10⁻¹². Der getrennte Rest der sechsknotigen Interpolation ist kleiner als 1,4 × 10⁻⁸. Hierzu werden die sechsten Ableitungen aus dem Integral von H, das Knotenprodukt im zentralen Teilintervall und eine Schranke 7,7 für die Summe der Beträge der Kardinalpolynome verwendet. Die 100-Punkt-Hilfsquadratur trägt auf dem gepolsterten Tabellengebiet weniger als 53²⁰⁰/200! pro Faktor bei. Rationale Wurzelintervalle prüfen die verwendeten Gauss-Knoten und Gewichte. `continuum.json` enthält die berechneten Amplituden. Die analytischen Restschranken betreffen ideale Quadratur und Interpolation. Für die binäre Gleitkommarechnung gilt das numerische Fehlerbudget mit den ausgewiesenen Gegenrechnungen. Der Schritt zu einem kontinuierlichen Detektornachweis für alle 1 217 Zustände erfordert weitere Fehlerkontrolle für die geerbten Uhren und die Referenz.

## Simultane Aussage für alle Mischungen

`plan.json` legt die Zielmenge von 119 Typen, 65 536 Stichproben, beide Referenzgitter, das kontinuierliche Uhrintegral, beide Dichten, das Irrtumsbudget und die Komponentenradien fest. Eine vorgängige explorative Sobol-Rechnung diente der Wahl des Designs. Für die Bestätigung wurde ein frischer, lokal vom Betriebssystem erzeugter Bitstrom verwendet und unverändert archiviert. Die Auslegung als Zufallsstichprobe setzt unabhängige gleichverteilte 32-Bit-Wörter voraus. Die gemeinsame Verwendung derselben Zeilen für mehrere Uhren und Gitter ist bei dieser Fehlerrechnung zulässig. Der Plan ist mit Prüfsumme erhalten. Es gibt keine externe Zeitbeglaubigung.

Jede Zeile liefert sieben innere Uhrzeiten und eine Randuhrzeit. Real- und Imaginärteil des normierten Integranden liegen jeweils zwischen −1/√768 und +1/√768. Für M = 119 × 3 × 2 × 2 = 1 428 reelle Mittelwerte und ε = 0,0013 begrenzen die zweiseitige Hoeffding-Ungleichung und die Vereinigungsabschätzung die Wahrscheinlichkeit für mindestens eine Überschreitung durch

```
2 M exp(−65 536 × 768 × ε² / 2) < 9,67 × 10⁻¹⁶ < 10⁻¹².
```

Zum statistischen Radius kommt pro Komponente eine Reserve von 10⁻⁶. Die diskrete Auswahl der Gitterknoten verwendet exakte ganzzahlige CDF-Schwellen. Der Fehler der endlichen Abbildung ist kleiner als 10⁻⁸ bei normierten Gittergewichten. Auf der kontinuierlichen Uhr beträgt der maximale Koordinatenfehler δ = 1,5/2³². Über höchstens 105 gerichtete Paare mit Koeffizientenbetrag höchstens 16 ändern sich die quadratischen Argumente insgesamt höchstens um 105 × 16 × (12δ + 4δ²). Für jeden beteiligten Markierungsfaktor genügt eine Lipschitz-Schranke von eins. Nach Normierung bleibt die Abweichung unter 3 × 10⁻⁷. Der Rest der Reserve deckt die numerische Auswertung. `audit_samples.py` berechnet sämtliche 714 komplexen Mittelwerte nochmals mit getrennten reellen Sinus-/Kosinus-Polynomen und geänderter Summationsfolge. Die grösste beobachtete Abweichung beträgt 4,12 × 10⁻¹⁷. Die Irrtumsschranke bezieht sich auf die Stichprobenintegration innerhalb des angegebenen numerischen Modells.

Für jede mit den geerbten Spalten verträgliche positive Vervollständigung des Detektoreffekts S folgt aus ⟨x−q,S(x−q)⟩ ≥ 0 eine affine untere Schranke 2 Re⟨q,Sx⟩−⟨q,Sq⟩. Die Testvektoren q stammen aus v0.9. Ist z der Skalarüberlapp eines Typs mit q und â seine geschätzte komplexe Uhrantwort, so gilt auf dem gemeinsamen Vertrauensereignis

```
Re(z a) ≥ Re(z â) − 0,001301 (|Re z| + |Im z|).
```

`transfer_proof.py` kombiniert diese Rechtecke mit den geerbten deterministischen Schranken, minimiert die linearen Projektionen getrennt über die erreichbaren Typen beider Eltern und prüft die beiden Transferendpunkte exakt rational auf den gespeicherten Daten. Affinität deckt jeden Zwischenwert ab. Daher ist weder ein Raster von Mischgewichten noch eine Wahrscheinlichkeitsverteilung über Präparationen erforderlich. Die 119 kontinuierlichen Stichprobenmittelwerte sind archiviert. In die beiden Detektorzertifikate gehen jeweils nur die Daten des betreffenden Referenzgitters ein.

## Gegenbeispiel und nächster Schritt

Bei λ = 5 % sucht `witness_search.py` im vorhandenen Pilot-Gramblock über die direkt ausgewerteten Uhren nach ungünstigen zulässigen Mischungen. Beide Eltern dürfen ihre Nachkommen unabhängig wählen. Für die höhere Dichte auf (48,8) findet die Suche rund 20,1682 % N14_734, 69,1688 % N14_760 und 10,6630 % N14_8191 im übertragenen Anteil jeder Elternhistorie. Der eingeschlossene Gesamterfolg dieser Mischung liegt bei 90,04046 % bis 90,04057 % der Referenz (nach aussen gerundet). Dies ist eine konkrete Obergrenze für das unbekannte Minimum, kein Optimalitätsbeweis.

Die feste Vergleichsmischung aus v0.9 verwendet dieselben drei Nachkommen im Verhältnis 21:70:9. Bei genau 5 % liegt ihr Gesamterfolg für Dichte 1/4 auf beiden Gittern über 90,0404 %. Bei λ = 5,0211 % liegt sogar ihre obere Schranke auf beiden Gittern unter 89,999897 %. Die Niveaugrenze wird damit tatsächlich verletzt. Ein exakter kritischer Transfer folgt daraus bislang nicht. Für die deterministische Absicherung ist `N15_338934` auf beiden Gittern und für beide Dichten der nächste Typ mit der ungünstigsten Stützebenenprojektion. Das gewonnene Ergebnis betrifft die Erweiterungsstabilität dieses Detektors im N15-Modell.

## Offline nachrechnen

Die Auswertung verwendet Python 3.12, NumPy, SciPy, SymPy, mpmath und einen C99-Compiler. Die Zahlen aus v0.9, der Versuchsplan und die Zufallswörter sind im Paket enthalten. Aus dem entpackten Ordner ausführen. Der erste Befehl prüft die Prüfsummen und rechnet das Zertifikat. Der zweite rekonstruiert zusätzlich alle neuen Rechnungen in einem temporären Ordner. Es werden keine Netzwerkzugriffe benötigt.

```sh
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=1 python3 -B verify.py
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=1 python3 -B verify.py --rebuild
```

- `input_v09.zip` — unverändertes Prüfpaket aus PR 314, SHA-256 `76a4d9f6137eb714e16f211894424214fe84d4dcc57b16a9de4643eb024d4f77`.
- `plan.json` — SHA-256 `1cf97b377c864f11ad3dac35acda4047b91a4e02a7fade2d5d640115681e097e`.
- `uniforms_u32le.bin` — 65 536 × 8 Wörter im Little-Endian-Format. SHA-256 `bc8c8c14e8fbc044c5554d233d4544d2b9607a92580b23b6fb5191a45d8f6c08`.
- `certificate.json` enthält auch die exakten rationalen Untergrenzen und die 117 deterministisch offenen Typen. `witness.json` enthält die realisierbaren Gewichte mit Nenner 10⁸ je Elternhistorie. `SHA256SUMS` erfasst alle verteilten Einzeldateien ausser dem Prüfsummenverzeichnis selbst.
