# Äusserer Dichtezugriff vor der Pulswahl

## Fragestellung und Zugriff

Auf der totalen Ordnung vom Typ 2097151 lautet die Ereignisfolge 0, 1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 7, 8, 9, 10. Wir legen den Schnitt direkt hinter 11. Später wird ein Puls an der weitergereichten Kopie der Uhr 6 gewählt. Für eine Geschichte H betrachten wir die skalierte Dichte $x=x_{11}=w_{11}/D$. Die vorbereitete Dauer ist $D=(4-e)\Delta$ und $\Delta^4=3/722$. Es gelten die breiten Fenster bei markierter Dosis $M=1$. Die Aussage verlangt ein Gerät, dessen Messergebnis bereits vor der Pulswahl gespeichert werden könnte.

Die vier Quellen verändern ausschliesslich die Argumente der Wirkung am Eingangskragen um $h(\sigma U+\tau V)/\sqrt D$. Es gilt $h=1/8$, $U=(1,1,1,1)$, $V=(29,23,16,8)/64$ und $\sigma,\tau\in\{-1,1\}$. Andere Felder und Präparationsfenster bleiben beim Aufruf fest. Alle quellabhängigen Paare enden spätestens bei 11. Kein aktives Paar vom Eingang erreicht Ereignis 12. Die Gleichungen erhalten deshalb dieselben relativen Phasen, wenn wir die spätere Wirkung weglassen.

Wir räumen einem idealisierten Gerät eine kohärente Wahl der vier Stellungen ein. Auf einer festen Feinhistorie wirkt genau einmal die Diagonalmatrix mit Einträgen $\exp(iS_{\sigma\tau}(H))$. Eingangsregister, Hilfsregister und die gemeinsame Ausgangsmessung dürfen beliebig gewählt werden. Sie erhalten keine weiteren geschichtsabhängigen Daten. Bekannte gemeinsame Präparationsparameter dürfen verwendet werden. Ein auf allen ursprünglichen Geschichten gültiger Dichtezeiger muss für mindestens ein Ergebnis eine Wahrscheinlichkeit $f(x)$ mit nichtkonstantem $f$ erzeugen. Dieses schwache Kriterium lässt verrauschte Bits zu. Ein fehlerfreier Zahlenwert würde es ebenfalls erfüllen. Die Amplitudenmessungen an mehreren präparierten Ensembles in PR #361 unterliegen einem anderen Kriterium. Die kohärente Steuerung ist hier eine eingeräumte Zugriffsmöglichkeit des Rechenmodells.

## Zwei unabhängige Phasen bei unverändertem x

Wegen der quadratischen Uhrwirkung zerfällt jede der vier Phasen exakt in

$$
S_{\sigma\tau}=C+\sigma A+\tau B+\sigma\tau\chi,\qquad
\chi=\frac{h^2x}{19}.
$$

Der Mittelwert $C$ fällt aus jeder Messung dieses Registers heraus. In den übrigen Koeffizienten seien $dU=U_j-U_i$, $dV=V_j-V_i$, $g=Y_j-Y_i$ und $x_j=w_j/D$. Die ersten beiden lauten $A=-(h\sqrt D/19)\sum b_{ij}x_jg\,dU$ und $B=-(h\sqrt D/19)\sum b_{ij}x_jg\,dV$. Für den letzten gilt $\chi=-(h^2/19)\sum b_{ij}x_jdU dV$. Nur Ereignis 11 trägt dort bei. Die Nachrechnung verwendet einmal die Intervalle der Ordnung und einmal die unentwickelte Wirkung nach Kettenrang. Für jede Basisdichte wird das quadratische Polynom in $\sqrt D$ an drei rationalen Stützstellen und allen vier Stellungen geprüft.

Bei $e=1/4$ und mittleren inneren Uhren ergibt die Ableitung von $(A,B)/(h\sqrt D)$ nach $(x_4,x_5)$ die Matrix

$$
\begin{pmatrix}-5/76 & 17/304\\-53/608 & -47/608\end{pmatrix}.
$$

Ihre Determinante ist $1841/184832$. In beiden Zellen lässt der ursprüngliche Jitter voneinander unabhängige Variationen mit Halbbreite von einem Prozent der Zellmitte zu. Bereits Verschiebungen um $1/10000$ liegen im Inneren. Die Zielgrösse $x$ bleibt bei beiden Variationen fest. Die Determinante der skalierten Matrix ist ein Polynom in den Uhrdaten, auch nach Einsetzen der Präparationskoordinaten $e,u$. Der rationale Zeuge zeigt, dass es nicht identisch verschwindet. Die regulären Punkte liegen folglich dicht in beiden offenen Uhrfenstern.

## Was eine Messung nach einem Aufruf enthalten kann

Für jedes Ergebnis ist die Wahrscheinlichkeit eine Summe von Termen $m_{kl}\exp(i(S_k-S_l))$. Die Konstanten enthalten den Eingangs- und Hilfszustand und den gewählten Messeffekt. Bei festem $x$ ist dies ein endliches trigonometrisches Polynom in $A,B$. Für ein dichteabhängiges Ergebnis müsste es auf der offenen Menge der beiden zulässigen Phasenvariationen konstant sein. Ein trigonometrisches Polynom mit dieser Eigenschaft ist überall konstant. Sein Mittel über beide Winkel liefert exakt diesen Wert. Die Mittelung ist ein Beweisschritt und setzt keine physikalisch gleichverteilten Phasen voraus.

Die Frequenz jedes Terms ist $(\sigma_k-\sigma_l,\tau_k-\tau_l)$. Nur $k=l$ liefert die Nullfrequenz. Dann fällt auch $\chi$ weg. Übrig bleibt $\sum_k m_{kk}$, unabhängig von $x$. Auf allen regulären Geschichten gilt dasselbe Argument. Stetigkeit der tatsächlich erzeugten Messwahrscheinlichkeit schliesst die Rand- und Ausnahmebelegungen im positiven Referenzfenster ein. Der Beweis erlaubt gewöhnliche Statistiken, die gleichzeitig auf $x$ und auf die anderen Dichten ansprechen.

## Wie gut sich zwei bekannte Geschichten unterscheiden lassen

Wir fixieren $e=1/4$, die Randdichte am Zentrum $1/4$, die Zukunftsdichten wie im Referenzpaket und alle Jitter auf null. Alle inneren Uhren stehen am Zentrum, bis auf $u_{12}=5/8\pm1/80$. Die Abweichungen liegen strikt innerhalb der Halbbreite $1/64$. Die beiden positiven Belegungen vervollständigen zulässige Präfixe. Der Rechenvergleich benutzt $u_{12}$ zur Konstruktion. Das Messgerät erhält diesen späteren Wert nicht. Nur die Verweilanteile der Zellen 11 und 13 ändern sich. Quellen erreichen davon allein Zelle 11. Es folgt $x_-=19/160$, $x_+=21/160$ und $\delta x=1/80$. Die beiden Fälle sind gleich wahrscheinlich angesetzt. Die gemeinsame Präparation und beide möglichen Belegungen sind bei der Optimierung bekannt.

Das einzige aktive Eingangspaar zu 11 ist $(3,11)$ mit $b=-8$. Für $g=Y_{11}-Y_3=15/8$, $z=\sqrt D$ und $t=h(\sigma+\tau/8)$ lauten die relativen Eigenphasen des Unterschieds beider Registerwirkungen bis auf einen gemeinsamen Summanden $(4/19)\delta x\,(gz-t)^2$. Wegen $gz>9/64$ liegen alle vier auf einem Kreisbogen der Länge

$$
L=\frac{16}{19}\,\delta x\,g z\,\frac9{64}
\quad\text{mit}\quad 0.002708188211\le L\le0.002708188212.
$$

Für jeden reinen Eingangs- und Hilfszustand ist der Ausgangsüberlapp eine konvexe Kombination der vier relativen Eigenwerte. Seine Projektion auf die Mittelsenkrechte der Bogensehne ist mindestens $\cos(L/2)$. Gleiche Gewichte auf den beiden äussersten Phasen erreichen diesen Wert. Für gleiche Vorwahrscheinlichkeiten liefert der positive Eigenraum der Differenz der beiden Ausgangsdichtematrizen die optimale Messung. Bei zwei reinen Zuständen ist deren Spurdistanz $\sqrt{1-|\langle\psi_-|\psi_+\rangle|^2}$. Gemischte Eingänge erlauben durch Reinigung keine Verbesserung. Dies ergibt das erreichbare Optimum

$$
P_{\rm opt}=\tfrac12[1+\sin(L/2)]\in[0.500677046845,\ 0.500677046846].
$$

Das Intervall verwendet nach aussen gerundete 256-Bit-Ganzzahlschranken. Der Wert bezieht sich auf dieses Paar und diese Quellenstärke. Er ist keine Erfolgsquote für beliebige Staubballpräparationen. [John Watrous, The Theory of Quantum Information, Kapitel 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.pdf)

## Ein bedingter Zeiger aus zwei Kopplungen

Wenn dieselbe ungestörte Geschichte zweimal kohärent dieselben vier Quellenphasen aufprägen kann, lassen sich zwei Wege überlagern. Weg eins benutzt $(+,+),(-,-)$ und Weg zwei $(+,-),(-,+)$. Ihre Phasen sind $2C+2\chi$ und $2C-2\chi$. Die relative Phase $4\chi=x/304$ ist vor der Pulswahl definiert. Eine Messung in der Sinusquadratur des Hilfsregisters hätte die beiden Wahrscheinlichkeiten

$$
p_\pm(x)=\tfrac12[1\pm\sin(x/304)].
$$

Auf einem Hilfsraum mit diagonalem Dichteoperator bilden $K_\pm=(\exp(2i\chi)\pm i\exp(-2i\chi))/2$ bis auf die gemeinsame Phase zwei Messoperatoren. Es gilt $\sum K_\pm^\dagger K_\pm=1$. Beide sind diagonal in der beibehaltenen Dichte. Der Prüfer multipliziert die Laurentpolynome aus. Das vorher betrachtete Paar unterscheidet sich in $p_+$ nur um rund 0,00002056. Das entspricht rund 0,00206 Prozentpunkten. Ein einzelner solcher Registereintrag wäre entsprechend verrauscht.

Bei verschiedenen Geschichten in den zwei Kopplungen bleibt in dieser Weganordnung der Zusatz $2(B_1-B_2)$ neben $2(\chi_1+\chi_2)$ stehen. Eine zulässige Verschiebung von $x_4$ um $1/10000$ in der ersten Geschichte erzeugt den Zusatz $-53\sqrt D/24320000$, obwohl beide $x_{11}$ identisch sind. Gleiche relevante Phasen und gleiche Zieldichte würden genügen. Eine zweimalige zerstörungsfreie Kopplung an dieselbe Geschichte ist eine konkrete hinreichende Annahme. Ihre Realisierung im gekoppelten Randmodell und die Speicherung eines Bits vor dem Puls sind offen.

## Grenze für einen Klick ohne Fehlalarm

Bei festen Uhren und übrigen Dichten variiert $x$ in einem offenen ursprünglichen Jitterintervall. Alle vier Wirkungsphasen sind affin in $x$. Nach jeder festen, endlichen Zahl von Anwendungen derselben Phasenquelle ist die Amplitude jedes Abfragepfades eine Konstante mal einer Exponentialfunktion einer linearen Funktion von $x$. Deshalb ist die Wahrscheinlichkeit eines registrierten Ereignisses ein endliches Exponentialpolynom in $x$. Das gilt auch mit geschichtsunabhängigen Zwischenoperationen, Hilfsregistern und einem expliziten Erfolgsausgang für eine Selektion.

Ein solches Polynom, das an jeder Stelle des alten Intervalls null ist, verschwindet bei denselben sonstigen Daten auf der gesamten reellen Achse. Das schliesst bei allein bewegtem Fenster 11 einen Klick aus, der im ursprünglichen Band voller Unterstützung exakt unmöglich und erst ausserhalb möglich wäre. Die Aussage betrifft die reine Phasenquelle. Ein von aussen bereitgestellter scharfer Dichtemesser, zusätzliche dichteabhängige Amplituden oder eine statistische Entscheidung mit zugelassenem Fehlalarm haben andere Voraussetzungen.

Das alte Gesamtband ist $[693/6400,909/6400]$. An den zwei oben verwendeten Uhrbelegungen verschiebt der jeweilige Puls das gesamte Jitterintervall nach ausserhalb. Für den positiven Puls liegt seine Obergrenze um mehr als 0,0055954 unter der alten globalen Untergrenze. Beim negativen Puls liegt die Untergrenze um mehr als 0,0048163 über der alten globalen Obergrenze. Diese positiven Abstände bestehen in offenen Umgebungen fort. Der frühere Vergleich von Trägern ist damit substanziell. Für seine Deutung als sicheres einzelnes Messergebnis fehlt weiterhin die physikalische Kopplung an einen entsprechenden frühen Speicher.

## Konsequenz für den Staubball

Die vier bekannten Quellen sind eine Ensembleauslese. Als alleiniger Zugang können sie kein universelles einzelnes Dichtedatum vor dem Puls erzeugen. Eine physikalisch begründete Instrumentenkopplung mit früh auslesbarem Speicher oder ein eigenständiger Präparationsvertrag könnte zwischen den Fenstervorschriften entscheiden. Eine unabhängige positive Masseneichung bleibt ein eigener offener Punkt. Das mitgeführte P3-Register enthält 60 Einträge mit Status `NOT_RUN`. Der Versuch berechnet keine Kollaps- oder Bounce-Trajektorie. [Ausgangsdaten und Herleitung, PR #361](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/f6d78fd5ef60b120da406a92b65b847494fa9cdf/research/rax_cqg/dust_collapse/n15_dichteantwort_am_uhrpuls_v0_1)
