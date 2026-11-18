# Kann der geerbte Detektor einen gemeinsamen Kern für eine physikalische Projektion liefern?

Auf den beiden N14-Historien A = 1790 und B = 5374 prüfen wir eine konkrete Zusatzannahme für Etappe 4. Ein einziger eindimensionaler Sektor im Raum der komplexen Historienkoeffizienten soll bei beiden Staubdichten die akzeptierten q7-Ausgänge reduzieren. Das bedeutet, dass ein Zustand im Sektor und ein Zustand im Komplement in jedem dieser Ausgänge einen verschwindenden Kreuzterm haben. Eine solche Zerlegung könnte einen Kandidaten für die Auswahl relativer Historienamplituden liefern. Die Forderung bezieht sich auf alle Koeffizienten im Zweierspan. Eine allgemeine CST-Constraint muss sie nicht erfüllen.

## Präparation und Auslese

Im Skalarausgang spannen die normierten Gaußzustände Φ_A und Φ_B einen Raum mit positiver Grammatrix G auf. Die drei komprimierten Fensterformen B_k summieren sich zu G. Wegen der Parität gilt B_links = B_rechts. Die verallgemeinerten Eigenwerte des mittleren Fensters relativ zu G betragen 0,1170152803 und 0,2403946623. Seine zwei Eigenlinien reduzieren damit alle drei Erfolgsfenster auf diesem Span. Das beschreibt die bedingte Auslese. Über die Zustandsänderung beim Messen trifft die Rechnung keine Aussage.

Eine Präparation zur Dichte ρ bildet den gemeinsamen Koeffizientenvektor c auf Σᵢ cᵢ aᵢ(ρ) Φᵢ ab. Die Uhrenamplituden aᵢ enthalten beide Lobes und die geerbte Gravitationsphase. Mit der Diagonalmatrix C_ρ aus diesen Amplituden sind die akzeptierten Formen E_ρk = C_ρ† B_k C_ρ und ihre Summe G_ρ = C_ρ† G C_ρ. Der Fehlschlag bleibt für jede deklarierte Präparation eins minus gesamte Erfolgswahrscheinlichkeit. Die Rechnung verwendet dafür keine lineare positive Form auf dem Koeffizientenraum.

## Warum die gemeinsame Projektion scheitert

Ein reduzierendes Idempotent P müsste P† E_ρk = E_ρk P für jedes akzeptierte Fenster erfüllen. Durch Summieren folgt P† G_ρ = G_ρ P. Damit müsste P mit L_ρ = G_ρ⁻¹ E_ρ,mitte für beide Dichten kommutieren. Diese notwendige Bedingung kommt ohne frei gewähltes gemeinsames Eingangs-Skalarprodukt aus. Am festen Skalarausgang ist L = G⁻¹ B_mitte. Auf den gemeinsamen Historienkoeffizienten gilt dagegen L_ρ = C_ρ⁻¹ L C_ρ. Die beiden Präparationen verändern das Verhältnis von B- zu A-Amplitude um den komplexen Faktor 1,0000156575 − 0,0016543019 i.

Auf dem Gitter 80/12 ergibt die Rechnung

    det([L₁/₈, L₁/₄]) ≈ 1,64688903 × 10⁻¹³ + 4,65338883 × 10⁻¹⁵ i.

Jeder Vektor auf einer gemeinsamen Eigenlinie würde vom Kommutator vernichtet. Die von null verschiedene Determinante schliesst eine solche Linie aus. Eine unabhängige Rangrechnung liefert für den gemeinsamen Kommutanten die komplexe Dimension eins. Es bleiben skalare Vielfache der Identität. Bei jeder einzelnen Dichte lassen sich die beiden Ausgangsprojektoren über C_ρ zurücktransportieren und reduzieren dann alle zugehörigen Erfolgsformen. Für eine einzige, von beiden Präparationen geteilte Rang-eins-Projektion scheitert bereits der Test der akzeptierten Ausgänge.

## Rechenkontrolle und Reichweite

`selection.py` prüft die vier archivierten Gitter von 32/6 bis 80/12 durch exakte rationale Arithmetik auf Real- und Imaginärteilen der gespeicherten Binary64-Werte. Es verwendet die hermiteschen Teile der Erfolgsformen. Auf jedem Gitter liegt der Realteil der Determinante strikt zwischen 1,64 × 10⁻¹³ und 1,66 × 10⁻¹³. Eine zweite Rechnung konstruiert den Kommutator aus G, dem mittleren Skalarfenster und den einzelnen Uhrenlobes. Intervallarithmetik erlaubt eine unabhängige Störung jeder reellen und imaginären Komponente um 10⁻¹² bei den Skalarformen und 2 × 10⁻¹⁰ bei den Lobes. Auf 80/12 bleibt der Realteil im Intervall [1,64625 × 10⁻¹³, 1,64753 × 10⁻¹³]. Diese Radien beschreiben einen Sensitivitätstest. Die Quadraturgenauigkeit selbst ist durch Verfeinerungen und gekreuzte Gitter empirisch kontrolliert.

Das Ergebnis schliesst diesen detektorverträglichen Auswahlmechanismus auf dem deklarierten Paar aus. Es bestimmt weder ein physikalisches Historienmass noch eine Constraint-Algebra oder einen physikalischen Zustandsraum der CST. Die Wirkungen anderer Präparationen, Detektoren und möglicher dynamischer Constraints bleiben offen.
