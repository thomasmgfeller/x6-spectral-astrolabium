# Welche Entropie die Daten bestimmen können

Die Routine linear_entropy in pruefen.py setzt einen reinen, von null verschiedenen Zustand auf ausdrücklich vorgegebenen orthonormalen Produktregistern voraus. Die Zeilen der Koeffizientenmatrix stehen für die innere Basis, die Spalten für die äussere. Sie akzeptiert Paare rationaler Real- und Imaginärteile und liefert einen exakten Bruch. Diese Eingaben sind Teil des mathematischen Kontrollversuchs. Die untersuchten N22-Gewichte werden dabei nicht zu Zustandsamplituden erklärt.

## Normierung und Teilsystem

Für einen abstrakten Vektor |ψ⟩ mit Koeffizienten q in einer Basis mit Gram-Matrix G ist N=q†Gq die quadrierte Norm. Die Koordinatenmatrix des reinen Dichteoperators ist q q†G/N. Das abstrakte Projektor-Symbol |ψ⟩⟨ψ|/N ist damit vereinbar. Wer dagegen q q†/N direkt als gewöhnliche Operatormatrix spurt, kann sogar eine von eins verschiedene Gesamtspur erhalten. Bei singulärem positiv semidefinitem G sind Nullrichtungen auszuteilen. Ein indefinites G liefert zunächst keine Wahrscheinlichkeitsnorm.

Gibt es einen physischen Produktraum H_A⊗H_B, mit Produktbasis und zugehörigen Gram-Matrizen G_A und G_B, so ist für die Koeffizienten C_ab des reinen Zustands K_A = C G_Bᵀ C† G_A die unnormierte gemischte Koordinatenmatrix auf A. Es gilt ρ_A = K_A/tr(K_A) und S_lin = 1−tr(K_A²)/tr(K_A)². Im orthonormalen Fall reduziert sich K_A auf C C†. Eine Teilmenge der Komponenten in einem direkten Summenraum zu wählen, liefert zunächst einen Projektor auf einen Sektor. Für die Reduktion auf ein Subsystem ist darüber hinaus ein operational definierter Tensorfaktor oder eine geeignete Algebra der messbaren Observablen erforderlich.

## Gleiche Gewichte, verschiedene Entropien

Im Zwei-Qubit-Kontrollregister sei Cθ = [[1,1],[1,exp(iθ)]]/2. Für jede Phase haben alle vier gemeinsamen Basiszustände dieselbe Messwahrscheinlichkeit 1/4. Die lineare Entropie des reduzierten Zustands ist exakt (1−cos θ)/4. θ=0 ergibt 0 und θ=π ergibt 1/2. Für θ=π/4 ist (2−√2)/8 irrational, trotz derselben exakten rationalen Diagonaldaten. Bei exakten rationalen komplexen Amplituden und kompatiblen rationalen Gram-Matrizen liefern gewöhnliche Summen, Produkte und Division durch die positive Norm einen rationalen Wert. Rationale Intervallgrenzen eines Feldzeugen garantieren dies für den gesuchten physikalischen Wert nicht.

Die gleiche Mischung von |00⟩ und |11⟩ hat dieselbe Dichtematrix wie die gleiche Mischung von (|00⟩+|11⟩)/√2 und (|00⟩−|11⟩)/√2. Die mittlere lineare Entropie der reinen Komponenten beträgt bei der ersten Zerlegung 0, bei der zweiten 1/2. Ein fester Ein-Kopien-Operator mit Erwartungswert gleich der linearen Entropie für alle reinen Gesamtzustände würde der identischen gemischten Dichtematrix zwei verschiedene Erwartungswerte zuordnen. Ein SWAP-Test mit zwei unabhängig präparierten identischen Kopien eröffnet eine mögliche operative Reinheitsablesung. Seine Beziehung zur Staubfläche würde eine separate Herleitung brauchen. Selbst wenn auf einer eingeschränkten Zustandsfamilie die Rényi-2-Entropie S₂=−ln tr(ρ_A²)=κA belegt wäre, ergäbe die Umrechnung S_lin=1−exp(−κA).

## Kriterium für eine geometrische Auflösung

Die Familie (|0⟩+exp(iθ)|1⟩)/√2 ⊗ |0⟩ hat zu jeder Phase lineare Entropie null. Ihre QFI bezüglich θ beträgt eins. Das folgt aus F_Q=4(⟨∂ψ|∂ψ⟩−|⟨ψ|∂ψ⟩|²) in normierten Zuständen. Ein von θ unabhängiges Bell-Paar hat dagegen F_Q=0 und lineare Entropie 1/2. Werden beim Radiusvergleich die präparierten Dichteoperatoren und das Messprotokoll identisch gehalten, liefert jede Messung dieselbe Wahrscheinlichkeitsverteilung. Für zwei verschiedene, unabhängig hergeleitete Zustände ist der Spurabstand ein Mass für ihre optimale Unterscheidbarkeit. Eingeschränkte experimentelle Observablen können weniger Information erschliessen. Für eine Radius-QFI wird eine differenzierbare, physisch definierte Zustandsfamilie benötigt.

Im eindimensionalen Produktvakuum |0⟩_A⊗|0⟩_B ist die Entropie null. Eine Liste verschwindender klassischer Felder stellt einen solchen normierten Zustand erst nach Festlegung des Quantenmodells dar. Die Zuordnung aller Gewichte zu den Komponenten eines Vektors ergäbe im Vakuum den unnormierbaren Nullvektor.

## Offline prüfen

    python3 -B pruefen.py

Der Lauf benötigt Python 3.10 oder neuer mit Standardbibliothek. Ergebnisse.json enthält die rationalen Kontrollwerte.

[Watrous, The Theory of Quantum Information](https://johnwatrous.com/wp-content/uploads/TQI.pdf) · [Braunstein und Caves, statistische Unterscheidbarkeit](https://doi.org/10.1103/PhysRevLett.72.3439) · [Ekert et al., direkte Reinheitsmessung](https://doi.org/10.1103/PhysRevLett.88.217901)
