# Fensterprojektion im bedingten Randkern

## Quelle und Ausgangsfenster

Die unverschobenen relativen Uhrwerte sind uⱼ = j/8 + xⱼ/64 mit −1 ≤ xⱼ ≤ 1. Die Koordinate einer verschobenen inneren Uhr ist u′ⱼ = uⱼ + Δsⱼ/D³ᐟ² bei sⱼ ∈ {−1/8,0,1/8}. Die beiden anderen äusseren Uhrenprofile und die lineare Kragenquelle wirken wie in PR #356 auf die Phase. Das Bezugsintervall D wird vor sämtlichen Quellen gelesen. Für Ausgangshalbbreite r prüft Pₛ die beiden Ungleichungen |u′ⱼ−j/8| ≤ r. Die neue Rahmenbedingung ist eine Ja/Nein-Projektion. Es wird weder ein neuer Dichtejitter gezogen noch die Zeit nach dem Eingriff als neue Dauer eingesetzt.

Für das enge Fenster ist der zulässige Bereich bei positiver Verschiebung in der Variablen x das Intervall [−1,1−2v], mit v = 32Δh/D³ᐟ². Bei negativer Verschiebung wird es gespiegelt. Für v ≥ 1 ist das Integral null. Die Grenzen der beiden äusseren Uhrfenster schliessen genau die Fälle links v < 1 und rechts v > 1 ein. Für r = 7/128 ist r > 1/64 + max Δh/D³ᐟ². Damit gilt Pₛ = 1 auf dem ganzen Träger für jede Einstellung, unabhängig von Wirkungsphase, Masse und Dichtezentrum innerhalb der untersuchten Box. Eingangsgewichte und aktiver Eingriff müssen dabei dieselben sein. Im vollständig staubfreien Vakuum ist die Phase identisch null und in allen Einstellungen bleibt links ein positiver Anteil. Darum gibt es dort auch beim engen Filter eine definierte Nullphase.

## Geschlossene Integrale für die Durchlassanteile

Das atomare Uhrmass ist bei festem D gleichverteilt und trägt den Faktor D⁷. Für positive Masse ist das Eingangsgewicht proportional zu D¹⁴ ∏ⱼ(8fⱼ). Die Zellen haben die Grenzen 0, die sechs Mittelpunkte benachbarter u-Werte und 1. Deshalb sind die beiden äussersten Faktoren 3/2+(x₁+x₂)/16 und 3/2−(x₆+x₇)/16. Die fünf mittleren Faktoren lauten 1+(xⱼ₊₁−xⱼ₋₁)/16. Das gesamte Produkt ist ein Polynom. Die fünf nicht adressierten Uhren lassen sich durch ihre rationalen Gleichverteilungsmomente ausintegrieren. Es verbleibt ein Polynom in x₄ und x₆. Für einen nicht verschobenen Port ist das k-te Moment 0 bei ungeradem k und 1/(k+1) bei geradem k. Für einen positiv verschobenen Port im linken Fenster ist sein unnormiertes k-tes Moment

    ((1−2v)^(k+1) − (−1)^(k+1)) / (2(k+1)).

Bei negativer Verschiebung kommt der Faktor (−1)^k hinzu. Das Produkt der zwei Momente wird mit dem reduzierten Dichtepolynom kontrahiert. Aus jedem Glied cₖ vᵏ entsteht cₖ(32Δh)ᵏ D^(p−3k/2), mit p = 7 bzw. 14. Beide äusseren Offsets sind gleichförmig und die beiden Lappen gleich breit. Die Stammfunktion je Fenster ist D^(p+1−3k/2)/(p+1−3k/2). Bei Verwendung von D als Integrationsvariable ist die untere Grenze beim grösseren Offset. Alle auftretenden Nenner sind positiv. Durch Division durch das ungefilterte Gesamtmass entsteht der tabellierte Anteil. Der Prüfer verwendet auswärts gerundete ganzzahlige Intervalloperationen mit 256 Nachkommabits, einschliesslich vierter Wurzel, Quadratwurzeln und Division. Die Ausgabebrüche umschliessen den Anteil. Eine separate tensorielle Quadratur prüft die Ergebnisse auf beiden Fenstern und im Gesamtmass.

## Amplituden und Kontrollarme

Auf dem einzelnen Typ bezeichne μ das normierte, positive Eingangsreferenzmass, Sₛ die reelle Staubwirkung mit den vorgeschriebenen Quellen und Kragenbeiträgen. Gemeinsame, quellenunabhängige Skalarfaktoren werden wie im Vorgängerversuch ausgeklammert. Die Beiträge je Einstellung sind

    Zₛ = ∫ Pₛ exp(iSₛ) dμ,      Aₛ = ∫ Pₛ dμ,      |Zₛ| ≤ Aₛ.

Die Auslese verwendet die Gewichte aus quellen/auslese.py und die relativen Hauptwinkel arg(Zₛ conj Z₀). Für die 24 Hauptfälle liegen alle ausgewerteten Hauptwinkel betragsmässig unter einem Radiant. Der enge Filter hat bei positiven Massen typischerweise nur kleine Beträge in den Armen mit zwei inneren Verschiebungen. Der Vergleich mit dem ungefilterten Bezugsarm umfasst dann unterschiedliche Anteile des Randuhrfensters. In der gepaarten Gegenprobe ersetzt ∫Pₛ exp(iS₀)dμ die gemeinsame Referenz. Das Momentanverhältnis wird dabei vor der Winkelbildung aus den beiden komplexen Integralen bestimmt. Die Summe verwendet weiterhin 15 feste Koeffizienten. Da Pₛ von der jeweiligen Quellenwahl abhängt, ist diese Gegenprobe eine weitere Auslesevorschrift.

## Ein positives Hilfsmodell für die Sichtbarkeit

Wähle L²(μ), den normierten konstanten Zustand 1 als Eingangs- und Endzustand und ein zweistufiges Armregister. Multiplikation mit exp(iSₛ) ist unitär, Pₛ ein orthogonaler Projektor. Die beiden Ausgänge Pₛ und 1−Pₛ sind vollständig. Der erfolgreiche Pfad mit gemeinsamer Endprojektion hat Amplitude Zₛ. Das Realisieren der kontrollierten Multiplikation und dieser Endprojektion ist eine Annahme dieses Hilfsmodells. Bei gleichgewichteter Armpräparation liefert der Auslesebasiswechsel für Winkel θ die gemeinsamen Wahrscheinlichkeiten

    p±(θ) = |Z₀ ± exp(iθ) Zₛ|² / 4.

Die Summe (|Z₀|²+|Zₛ|²)/2 ist die Wahrscheinlichkeit der erfolgreichen gemeinsamen Projektion im Modell. Die Differenzen bei θ = 0 und −π/2 ergeben Real- und Imaginärteil von Zₛ conj Z₀. Für die Sichtbarkeit folgt V = (p_max−p_min)/(p_max+p_min) = 2|ZₛZ₀|/(|Z₀|²+|Zₛ|²). Eine getrennte orthogonale Markierung der beiden Arme multipliziert den Kreuzterm nach Ausspuren mit dem Skalarprodukt null. Die Erfolgswahrscheinlichkeit der gemeinsamen Endprojektion und der geometrische Durchlass Aₛ bezeichnen verschiedene Grössen.

In dieser Konstruktion können die zwei Stellen in kausaler Reihenfolge adressiert werden, wenn die Innenmarkierung, die Referenzskala und die Quellenkontrolle bereitstehen. Die gemeinsamen Phasen müssen bis zur Randprojektion erhalten bleiben. Der Beweis für den Fensterdurchlass gilt innerhalb des endlichen Ensembles. Eine physikalische Verwirklichung der kontrollierten Quellen, eine Herleitung der Paarung aus der gekoppelten Wirkung und eine unabhängige Massenreferenz sind weiterhin offen.
