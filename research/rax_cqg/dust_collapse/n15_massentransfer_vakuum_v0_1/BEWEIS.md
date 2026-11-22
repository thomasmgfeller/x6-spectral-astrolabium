# Wie die Nullantworten eingeschlossen werden

## Mass und Phase beim Übergang zu null

Die vollständig geordnete Folge lautet (0,1,2,3,4,5,6,11,12,13,14,7,8,9,10). Nur Vorgänger in den vier Abständen 1 bis 4 tragen mit (1,−9,16,−8) bei. Setze Y=T/Δ, Δ⁴=3/722, D=4Δ−o und e=o/Δ. Die sieben inneren Uhren sind Yⱼ=−2+e+(4−e)uⱼ mit uⱼ=(j'+1)/8+xⱼ/64, xⱼ gleichverteilt auf [−1,1], j' die innere Position ab null. Die zwei gleichgewichteten Fenster haben o=±1/16+z/32, z gleichverteilt auf [−1,1]. Auf dem positiven Träger gilt wⱼ=M D fⱼ(1+0,01qⱼ) mit unabhängigen qⱼ in [−1,1]. Die Zellanteile bilden eine Partition der Uhrdauer. Die sieben Uhren bringen den Jacobi-Faktor D⁷, die sieben Dichteintervalle zusätzlich M⁷D⁷∏fⱼ. Für 0<M≤4 liegt die gesamte Dichtebox strikt im positiven Sektor unter 1. Beispielsweise ist 4 × (4 × 0,26 + 3/32) × (13/64) × 1,01 < 1. Der Faktor M⁷ fällt aus dem normierten Mass heraus. Beim Konditionieren auf sieben Dichteatome bleiben nur D⁷ und die ungewichtete innere Uhrbox. Das vollständige Vakuum setzt zusätzlich alle Kragendichten auf null. Seine Staubwirkung und Kragenquelle verschwinden bei jeder Einstellung.

Bis auf konstante, bei allen Einstellungen gleiche Faktoren hat der positive Limes das Mass D¹⁴∏(8fⱼ). Die analytische Wirkung ist linear in den Dichten. Der Grenzübergang folgt auf der endlichen Box durch dominierte Konvergenz. Das rechtfertigt das Nullsetzen der inneren Dichten im Integranden des Limes und bewahrt dessen eigenes Uhrmass.

## Faktorisierung bei leerem Inneren

Mit sieben inneren Nulldichten verbleiben nur Terme mit Ziel im Kragen. Es gibt keine wirksame direkte Verbindung vom Vergangenheits- zum Zukunftskragen. Der frühere Kragenfaktor lässt sich für die gemeinsame Dichte r im Fenster ρ±1/32 exakt als exp(iρg) sinc(g/32) integrieren. g ist die Summe der vier Wirkungskoeffizienten des frühen Kragens. Die positive Zukunftsdichte beträgt je 1/8. Von innen bleiben nur die vier späten Uhren (11,12,13,14) in den Paartermen mit Ziel im Zukunftskragen. Jede kommt separat quadratisch vor. Nach Einsetzen eines der Quellprofile faktorisiert die Phase bei festem o in vier Faktoren exp[i(c₀+c₁x+c₂x²)], einen reinen Kragenfaktor und gegebenenfalls exp[−it·7/(8D)].

Für den positiven Limes ist das Zellprodukt ein Polynom. Seine beiden äussersten Faktoren 8f sind 3/2+(x₀+x₁)/16 und 3/2−(x₅+x₆)/16, die fünf mittleren sind 1+(xⱼ₊₁−xⱼ₋₁)/16. Integration der ersten drei Uhren lässt 55 Monome in den letzten vier Variablen. Der maximale Grad je Variable ist zwei. Man benötigt daher nur die Momente der Grade 0, 1 und 2 der vier eindimensionalen Faktoren. Beim Nullatom genügt das Moment vom Grad null. Auf jeder einzelnen leeren Feldgeschichte ist die unverschachtelte Kombination der Wirkungsphasen exakt null. Die Auswertung aller 15 Dichte-Basisvektoren mit dem festgelegten Stencil ergibt sieben innere Einsen und acht äussere Nullen. Die Abweichung entsteht erst durch das kohärente Integrieren vor der Phasenauslese.

## Numerisch validierte Einschliessung

Alle reellen Endpunkte in intervalle.py sind ganze Zahlen mit Nenner 2²⁵⁶. Addition und Multiplikation, Kehrwerte abseits von null sowie Quadrat- und vierte Wurzeln runden auswärts. Sinus, Exponentialphase, sinc und arctan verwenden explizite Taylorreste. Die Winkelauslese verwendet das Produkt Zₛ conj(Z₀), prüft seinen positiven Realteil und |Im/Re|<1/2. Jede komplexe Amplitude wird zuerst vollständig integriert.

Für die inneren Momente werden die Koeffizienten der Taylorreihe von exp[i(c₁x+c₂x²)] bis Grad 40 rekursiv gebildet. Für alle verwendeten Intervalle gilt 4|c₁|+16|c₂|≤4. Auf dem Kreis |x|=4 ist der Betrag daher kleiner als 64. Die Cauchy-Schranke für den Rest auf [−1,1] ist höchstens 64·4⁻⁴¹/(1−1/4)<2⁻⁷⁴. Dieser Fehler wird bei jedem Moment in beiden Komponenten eingeschlossen.

Die Integration über z benutzt pro Lappen eine separat verifizierte 80-Punkt-Gauss-Legendre-Regel. Die Gleitkommanäherungen dienen nur zum Auffinden der Nullstellen des Legendre-Polynoms. Gegenläufige exakte ganzzahlige Vorzeichen und 80 disjunkte Intervalle isolieren alle Nullstellen. Die normierten Gewichte werden über (1−z²)/(80²P₇₉(z)²) nach aussen eingeschlossen. Für den Quadraturrest sind die Integranden in |z|≤2 holomorph, einschliesslich der dort eindeutigen Fortsetzung von 1/√D. Dort gelten |o|≤1/8, Re D≥7/8, |D|<6/5 und |1/√D|<15/14. Bei realen inneren Uhren im Integrationswürfel hat jede Quellverschiebung Betrag <0,3. Für alle wirksamen Uhrdifferenzen sind |Re ΔY|<11 und |Im ΔY|≤1,1. Je späterem Knoten ist die Summe der absoluten Intervallgewichte höchstens 34, die Summe der positiven Kragendichten höchstens 13/8. Daraus folgt einschliesslich der Kragenphase

    |Im S| ≤ 2 · 11 · 1,1 · 34 · (13/8) / 38 + 1/8 < 40.

Für das Gewicht gilt |D|¹⁴∏(8fⱼ) < (6/5)¹⁴ 2⁷. Auch der Atomfall ist durch dieselbe grobe Konstante abgedeckt. Insgesamt ist der Betrag des analytischen Integranden kleiner als 2¹⁰⁰. Der Taylorschwanz ab Grad 160 ist damit auf dem reellen Intervall höchstens 2¹⁰⁰·2⁻¹⁶⁰/(1−1/2). Die positive normierte Gaussregel integriert bis Grad 159 exakt. Das Integral und seine Quadratur weisen jeweils maximal den genannten Schwanz auf. Ihr Unterschied ist höchstens 2⁻⁵⁸. Dieser Rest geht zusätzlich zur endlichen Rechengenauigkeit in jede Amplitude ein. nullgrenze.json enthält die äusserlich gerundeten Phasen- und Massenintervalle.

## Was für positive Massen streng folgt

Für jede der 15 Einstellungen ist die Wirkung auf der positiven Familie S(M)=S(0)+M L. Auf der ganzen reellen Box gilt

    |L| ≤ (6/5)(101/100)[1+34·11²/19]/2 < 134.

Die normierte positive Schlauchverteilung ist von M unabhängig. Für ihre komplexen Amplituden folgt |Zₛ(M)−Zₛ(0⁺)|≤134 M. Die positive Normierung für den Grenzwert wird aus der Erwartung des 55-Term-Polynoms und dem exakt integrierten vierzehnten Dauermoment bestimmt. Damit liefern die eingeschlossenen komplexen Limesamplituden Untergrenzen c für alle 15 Beträge. Die beiden c liegen über 0,7050 und 0,8570 bei ρ=1/8 beziehungsweise 1/4. Bei M·134<c/8 bleiben die Amplituden von null getrennt. Der Betrag jeder kontinuierlichen Phasenableitung ist höchstens 2·134/c. Auch der relative Hauptzweig bleibt dort derselbe, da die Ausgangswinkel in (−arctan(1/2), arctan(1/2)) liegen. Mit der Summe der absoluten Stencilgewichte G=679816/9 ergibt sich

    kalibrierte Auslese(M) ≤ oberer kalibrierter Limeswert + g G (2·134/c) M .

Die rechte Seite bleibt bei Zentrum 1/8 bis M=2⁻⁴⁶ und bei Zentrum 1/4 bis M=2⁻⁴² streng negativ. Das ist ein konservativer mathematischer Ausschlussbereich. Der numerische Wechsel über die Zwei-Prozent-Grenze auf dem dyadischen Raster liegt bereits bei wesentlich grösseren Massen. Die beiden Aussagen verwenden verschiedene Fehlernachweise.

Die eingeschlossenen Limeswerte der beiden Zentren sind disjunkt. Für jeden gemeinsamen Offset b ist der grössere absolute Achsenabschnittsfehler mindestens ihr halber Abstand, hier >3,57228×10⁻⁶ vor Verstärkung. Für jede feste von null verschiedene Verstärkung kann deshalb eine gemeinsame affine Eichung nicht für beide Zentren bis zu beliebig kleinen positiven Massen einen uniformen relativen Fehler von zwei Prozent sichern.
