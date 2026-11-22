# Herleitung der Rand- und Stationaritätstests

## 1. Modell, Einheiten und Variation

Für einen festgehaltenen Ordnungstyp seien Y = T/Δ und w die ursprünglichen Dichten. Im verwendeten Modell lautet die Staubphase

    S(Y,w) = −½ Σⱼ wⱼ − (1/38) Σᵢ≺ⱼ bᵢⱼ wⱼ (Yⱼ−Yᵢ)².

Auf der Gesamtordnung haben die vier letzten Vorgänger die Koeffizienten (1,−9,16,−8), vom nächstliegenden zum entferntesten. Die Dichte sitzt am späteren Ende der Beziehung. Geometrie und minimales Skalarfeld geben bei diesem Typ keine weiteren inneren Ableitungen in Y oder w. Auf einer offenen positiven Dichtezelle kann wⱼ bei festem Y unabhängig variiert werden. Für die Stationarität der reellen Phase sind dort sowohl die Dichte- als auch die Uhrgleichungen notwendig. Die vorbereiteten Jitterfenster lassen diese Variationen in ihrem Inneren zu. Das Gewicht eines eingeschränkten oszillatorischen Integrals wird durch die Stationarität im Inneren allein nicht festgelegt.

## 2. Erste und zweite innere Uhr

Für jeden der sieben inneren Knoten gilt wegen Σ b = 0

    0 = −38 ∂S/∂wⱼ = 19 + Σ bYᵢ² − 2Yⱼ Σ bYᵢ.

Die Eingangswerte sind (−5,−4,−3,−2+e), e = o/Δ. Die erste Gleichung liefert Y₄ = (e²−4e−2)/(2(1+e)). Einsetzen in die zweite Gleichung ergibt

    Y₅−Y₄ = (e⁴+36e³−44e²−96e−8) / (4(1+e)(17e²+18e−2)).

Nach Multiplikation mit den Nennern sind die beiden Ausgangsgleichungen Polynome vom Grad höchstens 12. Der Prüfer setzt die Kandidaten an 17 verschiedenen rationalen Werten ohne Polstellen exakt in die ursprünglichen vier Quadrate ein. So wird die Identität ohne ein symbolisches Algebra-Paket geprüft. Die Nenner sind in beiden physikalisch vorgegebenen Offsetintervallen von null getrennt. Mit Δ als eingeschlossener vierter Wurzel und 1024 rationalen Offsetzellen pro Fenster wird die Lücke mit ganzzahliger Intervallarithmetik nach aussen eingeschlossen. Bereits Y₅ < Y₄ widerspricht einer kausal vorwärts laufenden Staubuhr auf 4 ≺ 5. Die Formel liefert eine notwendige Konsequenz der positiven Dichtevariation, keine zeitliche Entwicklung aus Messdaten.

Zwei chronologische Kontrollen verwenden nur die Originalgleichungen. dichteschale.py setzt für die beiden ersten Uhren die präparierten Zeitboxen ein und prüft jede der 256 Zellen pro äusserem Fenster. monoton.py lässt stattdessen jede Uhr vom vorherigen Wert bis zur Zukunftsuhr Y₇=2 zu und halbiert nur noch unentschiedene Offsetzellen. Alle Zellen werden spätestens an der dritten inneren Uhr ausgeschlossen. Die analytische Lückenformel beweist die stärkere Aussage schon am zweiten Ereignis ohne Rückgriff auf die Zukunftsuhr.

## 3. Unabhängiger Test der Uhrgleichungen

Setze G = −19 grad_Y S. Dann gilt G = K(w)Y mit der symmetrischen gewichteten Laplacematrix der aktiven Paarterme. Auf einem Testvektor v im Inneren lautet das Residuum

    v·G = Σⱼ wⱼ Σᵢ bᵢⱼ(vⱼ−vᵢ)(Yⱼ−Yᵢ).

Die inneren normierten Uhrwerte haben Mittelposition k/8 und zulässige Abweichung bis 1/64. Die Verweilanteile fⱼ ergeben sich aus den Mittelpunkten benachbarter Zeiten und den beiden Enden des Einheitsintervalls. Für wⱼ = MD fⱼ(1+ηⱼ), |ηⱼ| ≤ 1/100, liefert die Änderung gegenüber der mittleren Dichte einen Betrag bis MD[1/64 + (fⱼ,mitte+1/64)/100]. Für den zentralen Dichteanteil wird die lineare Form in Y vor der Abschätzung der Uhrabweichung vollständig zusammengefasst. Für jeden Dichteabweichungsanteil wird die zugehörige lineare Form je Ziel separat nach aussen begrenzt. Je 16 Offsetzellen pro Fenster genügen für die sechs Kraftzertifikate in stationaer.json. Alle Rundungen verwenden ganze Zahlen mit Nenner 2²⁵⁶. Der Vergleich über beide frühen Dichtezentren ist hier derselbe, weil bei einer inneren Uhrvariation kein Ziel im Vergangenheitskragen beiträgt.

## 4. Identische vollständige Randwirkungsfunktionen

Schreibe Cⱼ = ∂S/∂wⱼ. Die Ziele 12 und 13 haben ausschliesslich innere aktive Vorgänger. Daher sind C₁₂ und C₁₃ unabhängig von sämtlichen Kragenuhren und -dichten. Halte Uhren und alle anderen Werte fest und variiere xⱼ = wⱼ/D als

    (δx₁₂,δx₁₃) = ±(1/512)(C₁₃,−C₁₂).

Der Phasenunterschied beider Varianten ist für beliebige gemeinsame äussere Felder exakt null. Das folgt aus der Linearität in w sowie C₁₂ C₁₃ − C₁₃ C₁₂ = 0. Dieser Nachweis gilt auch für finite Quellen, die ausschliesslich äussere Feldargumente der gleichen Wirkung verändern, und für identisch gewählte reine Kragenphasen. Ein unabhängiger Test vergleicht die absoluten Wirkungswerte auf einer quadratisch vollständigen Stichprobe von 45 äusseren Uhrvektoren. Hingegen ist −19 ∂ₐ∂ᵦS = 9w₁₃/D für die zwei inneren Verschiebungen mit Normierung 1/√D. Das einzige beide Uhren verbindende Paar hat Schichtgewicht −9. Die Identität wird über vier endliche Wirkungsdifferenzen nachgerechnet. Die gewöhnliche Summe Σwᵢ/D ändert sich genau um 2(C₁₃−C₁₂)/512.

Für den Punktzeugen wähle e=1/4 und uₖ=k/8, mit der einzigen Abweichung u₃=3/8+1/128 (drittes inneres Ereignis). Die zentralen Werte sind xⱼ=fⱼ, M=1. Alle verschobenen Werte liegen strikt im ±1-%-Band. Die Bezeichnungen „Minus“ und „Plus“ spezifizieren das Vorzeichen der Verschiebung.

Für ein Paket mit Ausdehnung in allen freien Variablen variiere e und alle sieben normierten inneren Uhrwerte in Intervallen mit Halbbreite 1/16384 um diesen Punkt. Die Basispakete verwenden auf diesem Gebiet xⱼ=fⱼ(1+qⱼ), |qⱼ|<1/500, etwa mit gleichförmiger Verteilung in den Paketkoordinaten. Die frühe Dichte kann über ihr ursprüngliches Fenster variieren. Für jede gekoppelte Stichprobe übersetze beide Dichtevarianten mit den bei ihren eigenen Uhrwerten bestimmten C₁₂ und C₁₃. Die auswärts gerundeten Schranken in gegenpaar.json sichern sowohl das Einhalten des ±1-%-Bandes als auch die Differenz der realisierten Summen im Intervall [0,00017502; 0,00019326]. Die Mischmarkerdifferenz liegt zwischen 0,01412 und 0,01421. Die Übersetzung ist bei festen Uhren eine injektive Verschiebung der zwei Dichtevariablen und bewahrt dort das Volumenelement. Schon vor dem Integrieren sind die äusseren komplexen Phasen auf jedem gepaarten Punkt identisch. Addiert man beiden normierten Paketmassen je zur Hälfte das gleiche volle Referenzmass, haben beide Mischungen vollen Träger, identische äussere Randamplituden und noch mindestens die Hälfte der nachgewiesenen positiven Marker- und Summendifferenz im gewöhnlichen Mittel. Hieraus folgt keine Aussage, dass gerade diese Mischungen durch die physikalische Dynamik ausgewählt werden.

## 5. Bedingte Verschiebung und robuste Unmöglichkeit

Bei unverändertem w verlangt die Erhaltung der sieben inneren Uhrkräfte Kᵢᵢ t + Kᵢₑ c = 0. Die Matrix wird einmal aus den Paarbeiträgen und einmal durch exakte Polarisation der ursprünglichen Wirkung erstellt. An allen sechs Referenzen hat Kᵢᵢ Rang 7. Für die gewählten Randspalten B und die zwei Zielspalten L ist der erreichbare Anteil des zweidimensionalen Ziels von Dimension 2 + Rang(B) − Rang([B,L]). Der Prüfer berechnet zusätzlich die Linksnullvektoren von B und deren Zwangsgleichungen an L. Erfolgreiche Steuervektoren werden in allen sieben Originalgleichungen eingesetzt.

Im offenen Dichteband sollen t und c von den verborgenen Dichten unabhängig sein. Leite die Uhrkraftgleichung einmal nach w₁₂ und einmal nach w₁₃ ab. Alle auftretenden Endpunkte sind innen. Am früheren Ereignis 11 der Kante 11→12 bleibt für Ziel t=a e₁₁+b e₁₃ die Bedingung a=0. Am früheren Ereignis 12 der Kante 12→13 bleibt −b=0. Die Randspalten beider Dichteableitungen sind null. Damit gilt der Ausschluss unabhängig von der gewählten Zahl äusserer Uhrsteller. Die Aussage behandelt additive Uhrverschiebungen bei unveränderter Dichte. Rückkopplung mit zusätzlicher Kenntnis der inneren Dichten oder eine neue Quellenkopplung wurde nicht als verfügbar vorausgesetzt.

## 6. Stationäre Kontrolle und ihre Empfindlichkeit

Auf der affinen Kontrollkette mit Einheitsabstand in Y gelten Σ bₖ k²=−19 und Σ bₖ k=−1. Damit lösen konstante Dichten 1/8 alle inneren Dichte- und Uhrgleichungen. Bei den gleichen Uhren und vier vorgegebenen Zukunftsdichten folgt rückwärts aus der j-ten Uhrgleichung

    wⱼ = −wⱼ₊₁ + 18wⱼ₊₂ − 48wⱼ₊₃ + 32wⱼ₊₄.

Die Indizes in der Rekursion bezeichnen die Position in der Gesamtordnung. Der Prüfer setzt jede der vier Basislösungen in die Originalkräfte ein. Jede Zeile r des Übergangs hat Summe 1. Bei positiven gemeinsamen Basiswerten w₀ und Störungen |δw_f|≤ε w₀ ist der kleinstmögliche Wert w₀(1−ε∑|r_f|). Das Minimum ist mit gegensinnigen Vorzeichen der Randstörung erreichbar. Die grösste absolute Zeilensumme ist 1 998 123 an der ersten inneren Stelle. Die Grenze ist ein Supremum, da am exakten Grenzwert eine Dichte null wird. Dieser Verstärkungsfaktor betrifft die stationäre Rückrechnung bei fixierten affinen Uhren und unabhängig störbaren Randdichten.
