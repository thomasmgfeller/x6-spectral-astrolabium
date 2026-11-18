# Der bedingte skalare Randsektor

Die Einteilung in drei vergangene und drei zukünftige skalare Randkoordinaten, die Auswahl der Sektionen, ihr Lebesgue-Mass und der normierte Eingang mit Präzision βI stammen aus dem N11-Vertrag. β = 4/√6. Die Zweige 1790 und 5374 besitzen nach Integration der sechs inneren Felder und der zwei Randintegrationskoordinaten jeweils einen regulären Skalarwirkungsblock K. Delta-Constraints und freie Richtungen treten bei beiden Integrationen nicht auf. Diese Rangangabe betrifft die gegebene skalare Reduktion.

## Paarung und positive Form

Bei Eingang ψ(x)=N exp(−β xᵀΩx/2) hat der Ausgang dieselbe Form mit Präzisionsmatrix

    Ω′ = Kᵀ_xy (Ω−iK_xx)⁻¹ K_xy − iK_yy.

Die Normierung folgt aus der Gaußintegration und der einheitlich fortgesetzten Fresnelphase. Der Betrag des Vorfaktors im unintegrierten Skalartransportkern ist (β/2π)³ᐟ² |det K_xy|¹ᐟ². Da K_xy invertierbar ist, zerfällt der Transport in quadratische Phasenmultiplikationen, eine Fouriertransformation und eine invertierbare lineare Koordinatenskalierung. Mit diesem Betrag ist er im vorausgesetzten L²(R³, d³y) unitär. Die Wirkung liefert die Matrizen und Phasen nach Wahl des Vertrags. Die Normierung benutzt den gewählten skalaren Randmassstab.

Seien Φ₁ und Φ₂ die normierten Ausgänge zum gemeinsamen Eingang und Rᵢ = Re Ωᵢ. Für Gᵢⱼ = ⟨Φᵢ,Φⱼ⟩ ergibt die Integration

    |G₁₂|⁴ = 64 det(R₁) det(R₂) / |det(Ω̄₁+Ω₂)|².

Beide Ωᵢ sind komplex-rational nach Ausklammern von β. Alle führenden reellen Hauptminoren sind exakt positiv und der letzte Ausdruck liegt als exakter Bruch strikt zwischen null und eins. Die Eigenwerte sind 1±|G₁₂|. Der Rang des Gram-Produkts ist zwei und sein Nullraum trivial. Der Prüfer summiert unabhängig die drei geerbten q₇-Zeigereffekte zu G und vergleicht die Präzision und Phase jedes Zweiges mit einer gedämpften Abel-Integration. Multiplikation jedes Zustands mit exp(iF₄) ändert die relative Phase des Produkteintrags, während die Eigenwerte erhalten bleiben. Im vollständigen Uhrpaket ist die Gravitationsphase bereits enthalten.

## Wiederholung unter einer fest gewählten Identifikation

Für diesen Test werden die ausgehenden y-Koordinaten eines Zweiges mit den eingehenden x-Koordinaten des nächsten identifiziert. Das ist eine zusätzliche Zuordnung der beiden reduzierten skalaren Räume. Ein vollständiger gekoppelter Zwischenrand mitsamt Gravitation und Staub folgt daraus nicht. Auf dem deklarierten Raum ergeben alle vier Zweierfolgen eine andere Gaußform als die zwei ersten Ausgänge. Für jede Folge sind die drei Koeffizienten von y₁² komplex-rational und paarweise verschieden. Entlang der y₁-Achse geben die Exponentialfunktionen bei Ableitung nach y₁² eine invertierbare Vandermonde-Matrix. Wegen der Stetigkeit folgt auch lineare Unabhängigkeit in L². Auf die jeweilige normierte Folge entfällt ein quadrierter Normanteil von mindestens 99,30 % ausserhalb des Zweierspans. Dies prüft der Code mit der orthogonalen Projektion über G⁻¹.

Darüber hinaus besitzt die Wiederholung jedes Einzelzweigs unter derselben Identifikation eine unendliche linear unabhängige Folge von Ausgängen. Der Nachweis verwendet nur die reellen kanonischen Matrizen mit sechs Zeilen und Spalten.

1. Aus p = −K_xx x − K_xy y und p′ = K_yx x + K_yy y folgt die reelle symplektische Matrix S. Für Typ 1790 ist tr(S) = 537285185/75177984 > 6. Für Typ 5374 ist tr(S⁴) = 6878045225725788492995641872225/945503435163255681152834338816 > 6. Hätten alle Eigenwerte von S Betrag höchstens eins, wäre der Betrag beider ausgewiesenen Spuren höchstens sechs. Jede der zwei Matrizen hat somit einen Eigenwert mit Betrag grösser als eins.
2. Eine normierbare zentrierte Gaußform Ω legt die komplexe Ebene L = {(q,iΩq)} fest. Auf L ist das hermitesche Produkt z*Jz/(2i) positiv, denn es ergibt q*(Re Ω)q. L und ihre komplex Konjugierte spannen gemeinsam den komplexifizierten Phasenraum auf. Eine reelle symplektische Matrix, die L invariant lässt, wirkt auf L unitär und auf der konjugierten Ebene konjugiert-unitär. Alle ihre Eigenwerte haben dann Betrag eins. Wegen Schritt 1 kann keine positive Potenz des jeweiligen S eine solche L festlassen. Daher treten bei Wiederholung beliebig viele paarweise verschiedene Präzisionsmatrizen auf.
3. Aus jeder endlichen Teilmenge paarweise verschiedener symmetrischer Matrizen Ωᵢ erhält man entlang einer geeigneten reellen Geraden y=tv paarweise verschiedene Werte vᵀΩᵢv. Nur eine endliche Vereinigung echter quadratischer Nullstellenmengen ist bei der Wahl von v auszunehmen. Ein Vandermonde-Argument in t² gibt lineare Unabhängigkeit der Gaußfunktionen. Folglich kann kein unter dem jeweiligen wiederholten Skalartransport invarianter endlichdimensionaler Raum eine dieser Gaußformen enthalten.

Der Abschluss des linearen Spans der so erzeugten Folgen existiert im geerbten Hilfsraum. Die Auswahl eines physikalischen Raumprodukts, gravitative dynamische Constraints, eine fehlerkontrollierte Reduktion für eine vorgegebene Anzahl Schritte sowie die Identifikation physikalischer Kleberänder bleiben selbständige Fragen.
