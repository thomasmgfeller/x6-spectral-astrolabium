# Eine Untergrenze für den gesamten N14-Träger

Betrachtet wird der kohärente Zweilobenversuch mit demselben Vergangenheitskragen, zwei Anfangshistorien mit Koeffizient 1/2 und den beiden Dichten L = 1/8 und H = 1/4. Die zulässigen Skalarzustände sind auf eins normiert. Die drei akzeptierten positiven Zeigereffekte summieren sich zur Identität auf dem Skalarraum. Die vierte Wahrscheinlichkeit ist eins minus die Gesamterfolgswahrscheinlichkeit. Für jede Dichte seien b und v die kohärenten Vektoren der Anfangspräparation und der gesamten Nachkommenmischung. Die verwendeten reellen, nichtnegativen Amplitudengewichte von v summieren sich zu eins und sind für beide Dichten gleich. Der zu prüfende Vektor ist (1−λ)b + λv. Alle Normen beziehen sich auf diesen gemeinsamen Skalarraum.

## Uhrenabschätzung

Für jede Geometrie hat die innere Uhramplitude Betrag höchstens eins. Jeder Dichtefaktor ist eine konvexe Mischung von Phasen, die übrigen Phasen haben Betrag eins, und die Uhrenintegration verwendet positive normierte Masse. Der Faktor vor jeder äusseren Uhrenlobe beträgt 1/√1536. Durch kohärente Addition der beiden Loben mit dem Faktor 1/√2 gilt für jeden Endtyp und jede zulässige Mischung die Schranke a = 1/√768. Gleiche Abschätzungen gelten für mathematisch exakte positive, symmetrische und normierte Gauss-Legendre-Gewichte.

Schreibe t = −2 STEP + x, β = 4/√6 und STEP² = 2/(19β). Der im Dichtewechsel auftretende Phasenkoeffizient der vier festen Vergangenheitsknoten ist P(x) = 151/19 + 31β STEP x + 4β x². Im Summanden der integrierten Dichte steht exp(−iρP(x)/2) sinc(P(x)/(64π)), mit der normierten sinc-Funktion. Die Multiplikation des ganzen H-Vektors mit exp(i·151/304) entfernt die konstante Phase zwischen den Dichten. Sie lässt sämtliche Wahrscheinlichkeiten invariant. Nun folgt aus |exp(iy)−1| ≤ |y| eine Schranke für den Unterschied der beiden Vektoren.

Die beiden gleichgewichteten Loben haben Mitten bei x = ±1/16 und Halbbreite 1/32. Weil 31 STEP > 4·3/32, besitzt P(x)−P(0) auf beiden Loben das Vorzeichen von x. Im Mittel des Absolutbetrags über gespiegelte Knoten hebt sich der quadratische Beitrag auf. Der Mittelwert von |x| beträgt genau 1/16. Nach Rephasierung gilt deshalb für jeden Zweig und jede zugelassene Mischung ‖v_H−v_L‖ ≤ η = a·31β STEP/256. Für b gilt dieselbe Abschätzung.

## Vom Vektor zu vier Ausgängen

Für eine selbstadjungierte Spurklasseänderung E der unnormierten Zustandsmatrix lauten die ersten drei Änderungen tr(FᵢE). Die vierte ist −tr(E). Mit ∑Fᵢ=I und Fᵢ≥0 ist die halbe Summe der absoluten Änderungen höchstens ‖E‖₁. Diese Rechnung gilt ebenso für die Änderung des vierteiligen Dichtekontrasts. Der Betrag der Änderung des Gesamterfolgs ist durch dieselbe Spurnorm beschränkt.

Sei u eine obere Schranke für beide Referenznormen ‖b‖ und D = a+u. Mit d=v−b gilt ‖d‖ ≤ D. Die Änderung der unnormierten Dichtematrix ist E = λ(bd*+db*)+λ²dd*, wobei * den adjungierten Vektor bezeichnet. Aus der Spurnorm eines Rang-eins-Operators folgt für den Totalvariationsabstand pro Dichte

    L(λ) = 2λuD + λ²D².

Da ‖d_H−d_L‖ ≤ 2η, liefert dieselbe Entwicklung für die halbe L¹-Änderung des Kontrasts die obere Schranke 2λη(D+2u)+4λ²ηD. Mit a ≤ 0,036085, u ≤ 0,01966 und η ≤ 0,001812 genügt dies bereits für λ ≤ 0,0048, wenn beide N11-Erfolge mindestens 0,000379 und der Betrag ihres Unterschieds mindestens 0,00000667 sind. Die ursprüngliche halbe L¹-Kontrastnorm R₀ ist mindestens dieser Unterschied.

## Schärfung mit der N11-Präparation

Sei η_b = ‖b_H−b_L‖ nach Rephasierung. Für die ursprünglichen zwei N11-Zweige wird der Betrag der Änderung der kohärenten Uhrenamplitude mit höchstens 0,000165 bzw. 0,000315 angesetzt. Die normierten Skalarzustände sind dichteunabhängig. Mit dem Gewicht 1/2 folgt η_b ≤ 0,00024. Der Prüfer belegt die beiden Werte auf den archivierten N11-Gittern durch eine rationale Taylorabschätzung für exp(i·151/304) bis Grad zwölf mit Rest höchstens (151/304)¹³/13!. Das Archiv liefert R₀ ≤ 0,00000669.

Entwickelt man die quadratische Auslese in b und v, trägt die Änderung des Referenzkontrasts mit dem Faktor −λ(2−λ) bei. Die Kreuzterme werden durch zweimal (η_b a + uη) und die reine Nachkommenantwort durch 2aη beschränkt. Damit genügt

    C(λ) = λ(2−λ)R₀ + 2λ(1−λ)(η_b a + uη) + 2λ²aη.

Alle oberen Schranken wachsen im hier betrachteten Intervall. Bei λ = 0,016 ergibt die aufwärts abgesicherte Parameterwahl L ≤ 0,000035865816 und C ≤ 0,000001640270. Zulässig sind pro Dichte mindestens 0,0000379 und für den Kontrast mindestens 0,0000016675. Die Änderung des vorzeichenbehafteten Gesamterfolgsunterschieds ist höchstens die halbe L¹-Änderung des vierteiligen Kontrasts, da seine vier Komponenten zusammen null ergeben. Sein ursprünglicher Betrag ist grösser als die Fehlerschranke. Damit sind alle drei Kriterien bis einschliesslich 1,6 % erfüllt.

Die Abschätzung verwendet keine Anzahl von Nachkommen. Sie erfasst den gesamten N14-Träger und jede endliche Erweiterung, die dieselben Norm-, Gewichts-, Uhren- und Auslesevoraussetzungen erfüllt. Die N11-Eingangsschranken sind an beiden publizierten Gittern mit rationaler Arithmetik geprüft. Für die exakten N11-Uhrintegrale gilt die Aussage unter diesen Eingangsschranken. Eine rigorose Quadraturfehlereinschliessung der Referenzintegrale sowie ein Grenzwert der Folge von Historienmassen bleiben offen. Die erhaltenen 1,6 % sind eine hinreichende Grenze. Eine erste Verletzung kann bei einem höheren Wert auftreten.
