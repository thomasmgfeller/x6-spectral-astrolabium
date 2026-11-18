# Kohärente Prüfung auf markierten Uhrpfaden mit N ≤ 2

Der Vergleich verwendet die orthogonale Historienpaarung aus [CST-DUST-CLOCK-INTERVAL-001](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/2770f280ddcab063b925813170dc87c58a8b3821/research/rax_cqg/dust_collapse/clock_intervals_v0_1/DERIVATION.md), Gleichungen (1), (2), (4), (7), (10) und die Normierung am gemeinsamen Enduhrwert. Die alte Zeitmassdichte ist ds und das normierte Dichtemass lautet (δ₀ + 1₍₀,₁₎dw)/2. Für die Zahlgewichtung α=1, z=1 hat jede der beiden möglichen Zweierelement-Ordnungen nach einem Einelementpräfix quadriertes Rohgewicht 1/2. Der Präfix ist Teil jeder vollständigen markierten Endgeschichte.

## Prüffrage

Bei s=a=1/4 sei genau ein altes inneres Ereignis mit Uhr x und Dichtemarke w vorhanden. Bei b=3/8 wird früh gefragt, ob 1/16 < x ≤ 3/16, w>0 und bis b keine zweite Geburt erfolgt ist. Diese Multiplikation mit einem Indikator E im Referenzprodukt ist für H=1/2, 3/4, 1 exakt dieselbe Auslese. Am späteren Ende wird E auf den vollen Präfixzylinder zurückgezogen. Nach b dürfen also beide zulässigen Zweierelementordnungen in allen Marken auftreten. Die Frage «keine zweite Geburt bis H» wäre ein anderer Detektor.

Die beiden **neu gewählten Testpräparationen** auf der alten Einelementfaser sind

- ψ = 1(0 < x ≤ 3/16) · 1(w > 0) / √(3/32).
- φ = [1(1/16 < x ≤ 1/8) + i·1(1/8 < x ≤ 1/4)] · 1(w > 0) / √(3/32).

Die Masse jeder Stützmenge ist 3/32. Beide Pakete haben Einheitsnorm. Ihr komplexer Überlapp ist (1+i)/3, denn die beiden gemeinsamen Uhrzellen haben gleiche Masse 1/32 und relative Phasen 1 und i. Die Pakete gehören zum archivierten Hilfsraum. Eine Präparation durch physikalische Constraints bleibt offen.

## Zwei Rechnungen und drei Modelle

Die direkte Rechnung zerlegt die alte Zeit in vier Zellen und summiert über die Dichte am Atom und die positive Dichtestratum-Masse. Die Geschichte kann mit einem Ereignis enden oder ihr zweites Ereignis vor bzw. nach b erhalten. Alle neuen Dichteintegrale sind exakt, weil ihr Mass normiert und der Indikator von der zweiten Dichte unabhängig ist. Die Wirkungsphase fällt für jeden festen Endpfad aus dem Produkt von Bra und Ket heraus. Die getrennte Rechnung verwendet die analytischen Gram-Integrale der Pakete am Schnitt b und führt den letzten Schritt bis H samt sämtlichen Zukunftskanälen aus.

Bei erhaltenem Einelementpräfix ist das quadrierte Gewicht am Ende h₁(H)/h₁(a), bei Geburt in ds trägt jeder der zwei Kanäle ds/[2 h₁(a)]. In der archivierten terminalen Referenz ist h₁(s)=1+H−s. In den zwei neu geprüften mathematischen Vergleichsfamilien ist h₁(s)=β−s mit β=5/4 oder 4/3. Die benutzten Zweielementfasern haben h₂=1. Diese Rechnung beginnt mit einem Einelementpräfix und testet daher keine Leerpräfixamplitude.

Sei q die Wahrscheinlichkeit, dass bis b keine zweite Geburt stattfindet. Der volle Präfixzylinder liefert q=[h₁(H)+(H−b)]/h₁(a)=h₁(b)/h₁(a). Das einzelne Matrixelement des identischen Effekts ist ⟨Kψ,E Kφ⟩=q(1+i)/3.

| Modell | q bei H=1/2 | q bei H=3/4 | q bei H=1 |
| --- | --- | --- | --- |
| Archivierte terminale Referenz | 9/10 | 11/12 | 13/14 |
| β = 5/4 | 7/8 | 7/8 | 7/8 |
| β = 4/3 | 23/26 | 23/26 | 23/26 |

Für die einzeln normierten ψ und φ ist die Erfolgswahrscheinlichkeit jeweils 2q/3. Aus den vier Quadratformen für ψ±φ sowie ψ±iφ ergibt sich mittels Polarisation der oben angegebene komplexe Kreuzterm. Die **normierten** Superpositionen haben für ψ+φ und ψ−iφ jeweils die Erfolgswahrscheinlichkeit 3q/4, für ψ−φ und ψ+iφ jeweils q/2. Das macht die kohärente Präparation am festen Record unterscheidbar. Das volle Überlappelement ohne E ist in allen Fällen (1+i)/3. Die beiden β-Kandidaten unterscheiden sich im Real- und Imaginärteil des E-Kreuzterms um exakt 1/312. Der Test zeigt, dass innerhalb dieser Referenzklasse Enduhrunabhängigkeit mit verschiedenen Vorhersagen verträglich ist.

## Reproduktion und Reichweite

```sh
python3 -B -O coherent_audit.py
```

Die Ausgabe entspricht `coherent_audit.json`. Die Referenzprüfung vergleicht 108 Quadratformpaare (drei Modelle, drei Endwerte, zwei Effekte und sechs Vektoren). Eine fehlerhafte Löschung der Präparationsphasen und eine versehentlich bis H verlängerte Keine-Geburt-Auslese werden in sämtlichen neun Modell-Endwert-Paaren erkannt. Es werden nur rationale Rechnungen der Python-Standardbibliothek verwendet.

Der Kreuzterm stammt aus der gemeinsamen Unterstützung zweier Präparationen auf echten markierten Einerelementpräfixen. Verschiedene alte Präfixe führen in der geerbten lokalen orthogonalen Historienpaarung zu disjunkten Zylindern; ein diagonaler Präfixeffekt macht ihre reelle Wirkungsphase unsichtbar. Für Interferenz verschiedener Geometrievergangenheiten und für gravitative Rückwirkung braucht es ein dafür begründetes physikalisches Dekohärenzfunktional und physikalische Auslesen. Weder das Uhrpaket noch die neu gewählte β-Familie bestimmt die N14-Freiheit t oder eine P3-Dynamik.
