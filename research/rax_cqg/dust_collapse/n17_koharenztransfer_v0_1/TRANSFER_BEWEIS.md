# Einschluss des eingefrorenen Primärkontrasts auf 42429

Sei s das Stromvorzeichen, x der Versatz der früheren Uhr und t die Enddichte. Für die zugelassenen Paketzentren lässt sich die Amplitude bei festem x bis auf gemeinsame Trägerphasen als G_s(t) a_s(x) exp[i t g(x)] schreiben. Der erste neue Knoten hat keine der variablen alten Zukunftsuhren als Vorgänger. Am letzten Knoten ist die Abhängigkeit von x additiv im Dichtephasenkoeffizienten und seine übrigen Beiträge stammen vom alten Zukunftskragen. Der Faktor G_s darf auf dieser Ordnung für beide Präparationen verschieden sein. Beim Zeitgemisch verschwinden die x-abhängigen Phasen aus dem Betragsquadrat, sodass die normierte Enddichte je Zentrum für alle festen x und das Gemisch dieselbe ist. Der gemeinsame endliche Skalarfaktor fällt in der normierten Wahrscheinlichkeit weg.

Im kohärenten Arm multipliziert der Uhrfaktor J_s(t) die Amplitude G_s(t). Schreibe die frühere Portdichte als m+v und ihre Steigung als d₀+a x+b x². Mit c₁=1/19 und c₂=−1/38 ist g(x)=c₁ x+c₂ x². Bis auf reine Trägerphasen gilt

    J_s(t) = E exp(iP)
    P = v d₀ + [(m+v)a + t c₁]x + [(m+v)b + t c₂]x².

Die unabhängigen x und v sind gleichförmig auf [−h,h]. Die Berechnung von ℓ_s(t) = d log |J_s(t)|²/dt übernimmt die rationalen Monommomente, den eingeschlossenen Taylorrest und die gleichmässige Schranke der zweiten logarithmischen Ableitung aus PR 349. Die drei Koeffizienten d₀,a,b stammen aus der neuen Ordnung und dem jeweiligen neuen Paket.

## Zentrumsdifferenz pro Präparation

Seien U(t)=|G_s(t)/G_s(m)|² und V(t)=|J_s(t)/J_s(m)|². Alle Integrale verwenden das normierte Mass auf dem ganzen Endfenster. + und − bezeichnen hier die obere bzw. untere Enddichtehälfte. Dann ist die Differenz zwischen den beiden Armwahrscheinlichkeiten exakt

    ∫₊∫₋ U(t) U(y) [V(t)−V(y)] dν(t)dν(y) / [(∫U dν)(∫UV dν)].

Die Integrale über zwei obere Halbräume heben sich beim Subtrahieren auf. Für t≥y gilt V(t)−V(y)=∫[y,t] ℓ_s(z)V(z) dz. Ohne Gewichte ist das Doppelintegral von (t−y) gleich h/4. Der Rechner schliesst den vorzeichenbehafteten Ableitungsbereich deshalb mit positiven Normgrenzen ein. Aus U∈[u₀,u₁], V∈[v₀,v₁] folgt als positiver Korrekturfaktor zwischen u₀²v₀/(u₁²v₁) und seinem Kehrwert.

Für jeden der beiden normierten Faktoren liefern der Phasenbogen und der Anker am Mittelpunkt eine scharfe relative Formschranke. Die zentrierte Gesamtamplitude hat dort Betrag mindestens c>0,99. Beide einzelnen bei m auftretenden Faktoren haben Betrag höchstens eins und deshalb mindestens c. Nach Entfernen des jeweils gemeinsamen linearen Trägers gilt |F(t)−F(m)|≤η. Für U ist η die Endhalbbreite mal maximale Steigungsänderung der drei früheren variablen Kragenuhren. Für V ist η=h sup|g(x)|, abgeschätzt über die Summe der Beträge. Das Betragsquadrat relativ zum Mittelpunkt liegt zwischen (1−η/c)² und (1+η/c)². Die Multiplikation vorzeichenbehafteter Intervalle im Code gilt auch bei negativen Steigungen.

## Von den Zentren zu den ganzen Paketen

Für festgehaltene äussere Grössen liegen 15 frühere unabhängige Uhren- und Dichteabweichungen symmetrisch in [−r,r]. Bei einem Uhrunterschied mit n schwankenden Enden ist sein mittleres Quadrat der *Abweichung* nr²/3. Eine Dichteabweichung hat Mittel null und ist von allen Uhren unabhängig. Für die Phasenabweichung δS vom Zentrum schliesst der Rechner deren Betrag durch B und den Betrag ihres Mittels durch b ein. Aus dem Taylorrest der komplexen Exponentialfunktion folgt der punktweise Amplitudenfehler e=b+B²/2. Der letzte Dichtephasenterm enthält keine der 15 schmalen Achsen. Daher ist nach Herausziehen seines gemeinsamen Trägers die Änderung dieses Fehlers zwischen m und t höchstens ηe.

Das Dividieren durch die jeweilige Mittelpunktamplitude gibt höchstens ηe(1+1/c)/(c−e) Fehler der relativen Amplitude. Nach Normierung im Endfenster begrenzt

    2ηe(1+1/c) / [(c−e)(1−η/c)]

den Fehler einer binären Wahrscheinlichkeit. Die kohärente Rechnung verwendet beide Beiträge zu η. Für festes x lässt sich dessen eigener Träger entfernen, wodurch nur der Beitrag der drei variablen Kragenuhren bleibt. Im Gemisch werden die festen x mit ihren tatsächlichen positiven Normen gewichtet. Weil alle Zentrumswahrscheinlichkeiten innerhalb desselben Zweigs übereinstimmen, gilt die gleichmässige Schranke auch nach dieser Gewichtung. Die vier Fehler für die beiden Vorzeichen und Arme werden addiert. Der Summenfehler vom Zentrums- zum Ganzpaketintervall liegt unter 6,559 × 10⁻²⁸.

Das vollständige rationale Intervall steht in [transfer.json](transfer.json). Beide unabhängig berechneten Zentrumswerte liegen innerhalb des gesonderten Zentrumsintervalls. Die analytische Rechnung behandelt den gewählten Dichteeffekt, die zwei markierten Pakete und die deklarierte Randpaarung.
