# Fensteranteile und Wiederholung des frühen Messbits

## Referenz und zwei verschiedene Aufgaben

Die Referenzordnung ist (0,1,2,3,4,5,6,11,12,13,14,7,8,9,10). Es gelten M=1, e=1/4, K=4−e, Δ⁴=3/722, D=KΔ und im Inneren Yⱼ=Y₃+Kuⱼ. Das ursprüngliche Uhrfenster W ist |u₅−1/4|≤R=1/64. Die anfänglichen zwei Pakete entsprechen n=0 und n=1 in der Darstellung u₅(n,t)=1/4+(n−1/2)d+t, d=1/(36DK²), |t|≤h=1/16384. Die Variable t ist kontinuierlich. Der endliche Index zählt disjunkte Teile dieses Kontinuums. Die Dichte x₁₁=w₁₁/D hat dieselben schmalen Fenster um 1/8±1/2048 wie im Vorversuch. Die frühe Phase θ=−0,00082061668758… rad ist durch z=u₄−1/8=t=0 und x₁₁=1/8 kalibriert. Die erste Messung soll diese zwei Dichtepräparationen unterscheiden. Die zweite soll erkennen, welches erste *Messergebnis* vorlag. Ihre Trefferquoten beantworten verschiedene Fragen.

Im Hilfsmodell gilt die gewöhnliche positive Norm der Uhrwellen. Die erste Messung auf der Geraden Qᵣ=(I+rS)/2, r=±1, verwendet als Impulsmultiplikator S=sign sin(dp−θ). Die ausserhalb W erzeugte Amplitude behandeln wir als ausgeschiedenen Zweig. Beim Transport wenden wir die ursprüngliche rechte Wirkung auf die neue Koordinate im Fenster an. Bereits vor dem Eingriff integrierte Staubdichten werden so belassen. Das offene Dichteband bei 11 hängt von u₆ und u₁₂ ab. Diese Vorgehensweise macht keine Annahme über eine Reflektion oder Rückkehr der Komponente ausserhalb W. Für P3 ist die Hilfsnorm als physische Wahrscheinlichkeit noch zu begründen.

## 1 · Exakte Aufteilung des Messzustands

Für jedes t liegen genau die Pakete n=−7,…,8 vollständig in W. Der Abstand des äussersten Pakets vom Rand beträgt nur 0,00000362976 in u₅. Das nächste Paket verbleibt mit Abstand 0,00194901 ausserhalb. Die Intervalle für d und beide Abstände folgen direkt aus Δ⁴. Sei V die isometrische Einbettung der beiden Eingangspakete und P der Projektor auf W. Bei ungerader Verschiebung k hat S den Koeffizienten 2i exp(ikθ)/(πk), bei gerader den Wert null. In W erreichen von jeder Eingangsspalte genau die acht Verschiebungen k=±1, ±3, ±5, ±7 ihren Zielort. Die zwei so verschobenen Spalten haben unterschiedliche Parität, also disjunkte Träger. Für B=P S V folgt

    B†B=c I,    c=(8/π²)(1+1/9+1/25+1/49),
    V†B=B†V=(2/π) A(θ).

A hat auf der Diagonale Nullen und unten links i exp(iθ), oben rechts dessen komplex Konjugiertes. Die beiden überlebenden Zweige sind Kᵣ=P Qᵣ V=(V+rB)/2. Damit ist die verlorene Hilfsnorm ℓ=(1−c)/2. Es gilt K₊†K₋=ℓI/2 und Σᵣ Kᵣ†Kᵣ=(1−ℓ)I. Die drei nichtüberlappenden Beiträge für jede normierte Anfangswelle und beide Ergebnisse zusammen sind

| Teil des Zustands | Anteil |
|---|---:|
| Zwei Anfangspakete | 70,26423673 % |
| Vierzehn weitere Pakete in W | 27,21565109 % |
| Ausserhalb W | 2,52011218 % |

Die Anteile beziehen sich auf die gesamte ursprüngliche Hilfsnorm, ohne Renormierung nach dem Ausschneiden. Der positive Überlappungsoperator zeigt auch, warum die Projektion auf W die perfekte Wiederholbarkeit des auf der ganzen Geraden projektiv geschriebenen Bits verlieren kann.

Die Zählung ist empfindlich gegenüber der Präparation von e. Alle 16 Pakete sind vollständig enthalten und die nächsten vollständig ausserhalb, wenn (R+h)/(17/2)<d(e)<(R−h)/(15/2) gilt, wobei d(e)=1/[36Δ(4−e)³]. Die beiden Grenzwerte in e liegen bei 0,100708148227… und 0,250291541946…. An den engen Grenzen berührt ein Endpunkt den Rand. Insbesondere liegt der obere Übergang nur 0,00029154 oberhalb der verwendeten Referenz. Die hier angegebenen 16-Paketquoten wurden nicht über die breiten äusseren Präparationen gemittelt.

## 2 · Gewöhnlicher Transportschritt und zweite Auslese

Das einzige von Uhr 5 abhängige Paar des neuen Wirkungsbeitrags bis einschliesslich Ereignis 12 ist 5→12 mit Gewicht 16. Bei gegebenem u₁₂ und x₁₂=w₁₂/D ist der armabhängige Faktor

    Uₙ(t)=exp[−i (16/38) D x₁₂ K² (u₁₂−u₅(n,t))²].

Die Integration über die nun vergessenen Variablen u₄ und x₁₁ verwendet für jedes n denselben restlichen rechten Faktor. Das Abschlussband f₁₁=(u₁₂−u₆)/2 bleibt gleich. Ein rechter Puls an Uhr 6 multipliziert beide Anfangskomponenten und alle ausgehenden Pakete mit demselben zusätzlichen Faktor bei vorgegebenen restlichen Variablen. Für eine beliebige linke Zweipaketwelle L sei H(t) deren kohärente Integration über die vergessenen Variablen mit diesem gemeinsamen Faktor. Für jedes der betrachteten, dort variablenunabhängigen Instrumente lautet der ausgeschnittene Ausgang exakt U(t) Kᵣ H(t). Die folgende spätere Auslese darf das vorhandene u₁₂ und x₁₂ benutzen und U herausrechnen. Diese Werte gehen nicht in die frühere Messung ein. 144 direkte Integrationsvergleiche mit separater Auswertung der Wirkung prüfen beide Instrumente, beide Ergebnisse, zwei Uhren an 12, zwei Dichten an 12, drei t-Werte und drei Pulswahlen.

Für die Aussage nach der Verklebung werden die beiden Ergebnisgewichte aus derselben H und derselben positiven Hilfsnorm gebildet. Die vorherige Zusammenfassung vergessener Daten muss keine normerhaltende physische Entwicklung sein. Alle folgenden Quotienten gelten auch für gemischte Eingänge und beliebige gemeinsame Gewichte der verbliebenen Variablen, sofern die Nenner positiv sind.

**Wiederholung derselben Impulsregel.** Nach Beschneidung auf W und Nullfortsetzung gilt Q₋ᵣ P Qᵣ V=−Q₋ᵣ(I−P)QᵣV. Die Eingangsunterstützung liegt in W. Daher ergibt die Summe beider Falschzuordnungen ℓ/2 pro Eingangsnorm. Unter den behaltenen Fällen beträgt die Fehlerquote ℓ/[2(1−ℓ)]=1,29263187 %.

**Beste binäre Auslese für jedes erste Ergebnis zusammen.** Setze J=B/√c. J und V sind Isometrien, V†J ist selbstadjungiert. Die Bildräume von V+J und V−J sind orthogonal. Die Projektoren auf diese Räume, auf dem orthogonalen Komplement beliebig vervollständigt, ergeben für jeden Eingang die unbedingte Fehlernorm (1−√c)²/4 und insgesamt die bedingte Fehlerquote 0,01671176 %. Für eine normierte reine Eingangswelle sind die beiden Kandidaten K₊ψ und K₋ψ. Ihre Normquadrate summieren zu 1−ℓ und ihre Überlappung beträgt ℓ/2. Die zwei Eigenwerte der Differenz ihrer unnormierten Rang-eins-Matrizen ergeben die maximale Spurwerterwartung der binären Entscheidung. Die zugehörige Spurnorm ist √[(1−ℓ)²−ℓ²]=√c. Somit erreicht das angegebene Gerät die Schranke für jede ψ mit derselben Einstellung. Es benutzt nur den verbliebenen Uhrzustand und hat keinen Zugriff auf ein separates klassisches Register. [Binäre Zustandsunterscheidung, J. Watrous, Kapitel 3, Satz 3.4](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf)

**Fehlerfreie Auslese mit einem dritten Ausgang.** Die akzeptierten Eingänge besitzen Aᵣ=Kᵣ†Kᵣ. Eine Isometrie auf der gemeinsamen Ausgangsspanne kann die beiden Kᵣψ wie folgt weitergeben

    Kᵣψ  ↦  |r⟩ √(Aᵣ−ℓ I/2) ψ + |?⟩ √(ℓ/2) ψ.

Die Wurzeln existieren, weil c>2/π. Die vier Blöcke der Gram-Matrix bleiben bei dieser Abbildung gleich, einschliesslich der Kreuzblöcke ℓI/2. Daher definiert die Vorschrift ein einziges Gerät für jede Eingangsform. Bei einer eindeutigen Antwort ist das Bit richtig. Die beiden unentschiedenen Teilgewichte summieren sich zu ℓ pro ursprünglicher Eingangsnorm. Ein fehlerfreies Gerät muss die gesamte Überlappung in den unentschiedenen Ausgang leiten. Cauchy-Schwarz und das arithmetisch-geometrische Mittel verlangen dafür mindestens ℓ. Das Verfahren ist also optimal. Es meldet bei 97,41473627 % der im Fenster akzeptierten Norm ein Bit, entsprechend 94,95977563 % der ursprünglichen Norm vor dem Ausschneiden. 2,52011218 % scheiden durch das Fenster aus und weitere 2,52011218 % bleiben darin unentschieden.

## 3 · Vergleich mit einem von Anfang an fensterinternen Messoperator

Wir prüfen als zusätzliche Annahme einen symmetrischen Differenzenoperator. In H_W=L²(W) sei T_d die gewöhnliche Translation nach Nullfortsetzung, am Ausgang auf W beschränkt. Es wird kein Endpunkt mit dem gegenüberliegenden identifiziert. Setze H₀=i exp(iθ) T_d + [i exp(iθ)T_d]†. Auf den besetzten Restklassen t besteht seine Matrix aus 16 Plätzen mit Kopplung nur zwischen Nachbarn. Das jeweilige Vorzeichen seines Eigenwerts liefert ein projektives Bit. Auf allgemeinen unbesetzten Teilräumen kann ein Nulleigenwert etwa Plus zugeordnet werden. Auf den besetzten Restklassen kommt keiner vor.

Nach einer diagonalen Phasendrehung ergeben sich als Eigenwerte 2 cos(kπ/17), k=1,…,16, mit den normierten Sinusmoden der offenen Kette. Die beiden zentralen Plätze sind 8 und 9. Die Kompression des Vorzeichens auf die Eingangspakete hat die Sichtbarkeit

    η_W = (4/17) Σₖ₌₁⁸ sin(8kπ/17) sin(9kπ/17) = 0,57870302632114….

Das Nebendiagonalelement des Plus-Effekts hat Betrag η_W/2=0,28935151316057…. Eine direkte Diagonalisierung mit vier frühen Phasen 0, π/2, π, 3π/2 ergibt die Pluswahrscheinlichkeiten 0,50023745, 0,78935142, 0,49976255, 0,21064858. Die beiden Phasendifferenzen ergeben denselben Betrag. Der Vorversuch auf der Geraden lieferte 1/π. Mit exakt derselben Referenz und gleichen Vorwahrscheinlichkeiten für die zwei Dichtefenster skaliert der *Vorteil über ½* mit η_W/(2/π). Daraus folgen numerisch 50,00004648 % richtige Dichtezuordnungen. Eine separate Intervallschranke aus der Vorrechnung wird mit demselben exakten Faktor übertragen.

Die fensterinternen Spektralprojektoren Eᵣ erfüllen E₋ᵣEᵣ=0 auf allen besetzten Paketen. Im ursprünglichen Transportschritt gilt U Eᵣ H. Die zweite ideale Auslese U Eᵣ U† reproduziert das Ergebnis auf jedem überlebenden Zweig exakt. Das Gerät ist ein Vergleich für eine mögliche Randoperation. Es entsteht nicht allein dadurch, dass die Uhrwerte der Feinhistorie in der Wirkung stehen.

## 4 · Kann die bekannte Translationssymmetrie den Operator begründen?

Für eine starre, feldunabhängige Variation Yⱼ→Yⱼ+a vⱼ ändert sich der lineare Wirkungsanteil um −a Σᵢⱼ wⱼ bᵢⱼ(Yⱼ−Yᵢ)(vⱼ−vᵢ)/19. Soll er für alle Felder und Dichten identisch verschwinden, erzwingt der Koeffizient von wⱼYᵢ für jedes aktive Paar bᵢⱼ(vⱼ−vᵢ)=0. Die 50 Zeilen dieser Inzidenzmatrix haben Rang 14 auf 15 Uhrwerten. Der verbleibende konstante Profilvektor verschiebt alle Uhren gleich und lässt die relative Koordinate u₅ unverändert. Werden die Kragenuhren fixiert, hat die Einschränkung auf die sieben inneren Uhren vollen Rang sieben. Als lokaler Zeuge beträgt ∂c₁₁/∂u₅ bei den zentralen Uhren −2025/1216, bestätigt auch durch die symmetrische endliche Wirkungsdifferenz. Eine lokale Verschiebung von Uhr 5 ist somit keine starre Symmetrie dieser Wirkung. Diese Prüfung umfasst keine feldabhängigen Transformationen oder separaten Apparatekopplungen und fordert von einem realen Eingriff keine Symmetrie.

## 5 · Gemeinsamer später Ausgang hinter 13

Hier wird nach der ersten Messung **keine zweite Messung** eingeschaltet. Fixiert sind u₁₂=5/8, u₁₃=3/4 und x₁₃=1/8. Die Dichte w₁₂, die Uhr 4, die Tagdichte sowie die Pakettoffsets werden wie im alten Ausgang integriert. Pro frühem Messergebnis tragen alle 16 zulässigen Pakete *kohärent* bei. Über die beiden aufgezeichneten frühen Messergebnisse werden Intensitäten addiert. Die zwei ursprünglichen Kragendichtezentren 1/8 und 1/4 geben einen gemeinsamen Faktor. In jedem Tag misst B=(I₋−I₊)/(I₋+I₊) die Balance zweier Präparationen mit relativer Phase −π/2 bzw. +π/2. Die Tabelle verwendet B_hoch−B_niedrig.

| Eingriff, pulsfreier Lauf | Später Kontrast (gerundet) | Verhältnis zum Nullarm |
|---|---:|---:|
| Ohne frühe Messung | −3,217325253940 × 10⁻⁶ | 1 |
| Impulsmessung auf der Geraden, nur akzeptierter Fensterzweig | −3,217325253873 × 10⁻⁶ | 0,999999999979411… |
| Spektralmessung im offenen endlichen Fenster | −1,836771914143 × 10⁻⁶ | 0,570900288024557… |

Der akzeptierte Vergleich stammt aus einem Eingriff mit Ausscheidung. Sein nahezu gleicher *normierter* Kontrast sagt nichts über Gleichheit der unnormierten absoluten Ausgangsintensität aus. Die Differenz zum Nullarm liegt hier in [6,6241333;6,6241351]×10⁻¹⁷. Reine Gleitkommaauswertung kann diese Differenz nicht sicher auflösen.

Für den Nachweis bildet endintervall.py die 64 Integrale aus zwei Eingangspaketen, 16 Ausgangspaketen und zwei Dichtetags einzeln. Die eingehenden früheren Dichteintegrale verwenden die ursprünglichen armabhängigen Zellbreiten. Der rechte Faktor benutzt die Messausgangsuhr. Eine 24-Punkt-Gaussregel auf jeder der beiden reellen Koordinaten z/(1/64) und t/h wird mit nach aussen gerundeter 256-Bit-Festkommaarithmetik ausgewertet. Für die komplexen Scheiben vom Radius vier ist die Summe der Schranken der imaginären Wirkungsbeiträge kleiner als eins (siehe exponent_bound). Die sinc-Faktoren lassen sich dabei als Mittel über reelle Dichtejitter darstellen. Die Volumenfaktoren haben Betrag unter eins. Für jede Variable ist der Betrag des fortgesetzten Integranden somit kleiner als drei. Cauchy-Schranke, Exaktheit bis Grad 47 und positive normierte Gewichte geben nach beiden Achsen höchstens 4·3·4⁻⁴⁸/(1−1/4) Fehler je Integral. Die Amplituden werden erst anschliessend mit den eingeschlossenen Operatoreinträgen kombiniert. schnitt.py kontrolliert die Endausgabe mit zwei Integrationsverfahren und mit beiden Pulsrichtungen an Uhr 6. Die angegebenen strikten Endintervalle gelten für den pulsfreien Fall.

## Physikalischer Stand

Die Hypothesen für den frühen Zugriff und die positive physikalische Randpaarung bleiben offen. Der Originalvertrag erlaubt die Berechnung des Transports zulässiger Uhrwerte und liefert die strikte Einschränkung für starre Symmetrien. Für die Entscheidung über einen physikalischen Eingriff ist weiterhin ein separat hergeleiteter früher Messeffekt mit einem nichtverschwindenden Matrixelement zwischen den Paketen nötig. Die unabhängige Kalibrierung des positiven Massensektors steht aus. Im übernommenen Register stehen 60 P3-Einträge auf NOT_RUN.
