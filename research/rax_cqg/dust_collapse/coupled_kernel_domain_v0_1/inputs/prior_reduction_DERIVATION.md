# Zustandsbeschränkung und Verklebung im endlichen AA-Kontrollmodell

**Version 0.1 · 11. November 2026 · Schritt 5.** Basis: Main `d4cac775a044177e9d66d517c11c941cb812f0a6`, PR #280–282. Alle Aussagen beziehen sich auf den erklärten Kandidaten. Keine physikalische CST-Übergangsmatrix, Wahrscheinlichkeit, Unitarität oder Singularitätsauflösung wird daraus abgeleitet. Alle acht physikalischen Gates bleiben HOLD.

## 1. Ergebnis und Reichweite

Die Vierzustandsbeschreibung ist bereits innerhalb eines expliziten, orthonormalen 15-dimensionalen Prüfbereichs nicht geschlossen. Für den normierten Eingang `0:00` beträgt die Norm der von vier auf 15 Zustände zusätzlich sichtbaren Ausgangskomponenten

$$r_{15\leftarrow4}=0.102348630703\pm10^{-12},\qquad
\frac{r_{15\leftarrow4}}{\|v_{15}\|_2}=0.367087702939\pm10^{-12}.$$

Die zweite Zahl ist eine relative Amplitudennorm im getesteten Raum, keine Wahrscheinlichkeit. Der bisherige Mischblock bleibt bei Erweiterung der Basis **exakt unverändert**; seine Berechnung war kein normierter Ersatz für die gesamte Ausgangswelle. Die numerischen Einschließungen überlappen den früheren Befund.

Zwei AA-Gebiete mit gemeinsamer Zweipunkt-Antichain liefern bei Verklebung ihrer lokalen Teilwirkungen selbst nach Korrektur der doppelten Schnittterme und des Quotientmaßes nicht dieselbe Wirkung wie die gemeinsame Rechnung. Für eine explizite Achtpunktordnung werden fünf fehlende Intervallterme und ein von null getrennter Unterschied im normiert projizierten Nullatombeitrag berechnet. Mit **derselben gemeinsamen Wirkung** stimmt hingegen die gestufte Gaußintegration exakt mit der direkten Integration überein.

Zusätzlich ist die entkoppelte Referenz aus Schritt 4 kein auf diesem Grundzustand definierter Operator in das ungegewichtete Rand-L²: In einer ausgehenden Feldrichtung bleibt eine ungedämpfte quadratische Phase. Damit existiert für diese Referenz keine endliche volle L²-Abschneidefehlergrenze durch beliebig viele endlich viele Hermite-Pakete. Diese Aussage wird nicht ungeprüft auf die gekoppelte Wirkung übertragen.

## 2. Unveränderter Versuch und korrekte Vergleichsfrage

Die 33 gelabelten AA-Historien, je zwei Randpunkte und ein innerer Punkt, werden mit `c_C=1/33`, `κ=1`, `μ=0` und voller Phase `exp(i F₄(C))` verwendet. Wirkungsparameter, Randmaße und Einheiten bleiben wie in Schritt 4. Es handelt sich um explizite endliche Kontrollentscheidungen, nicht um hergeleitete physikalische Historiengewichte. Die Spezifikation wurde nach der strukturellen Untersuchung und vor der primären numerischen Auswertung eingefroren; sie ist keine externe Präregistrierung.

Mit $t=T/\ell$, $r=w/\hbar$, $q=\Phi\ell/\sqrt\hbar$ gelten

$$d\lambda(t)=\tfrac12\mathbf1_{[-1,1]}dt,\qquad
d\nu(r)=\tfrac12\delta_0+\tfrac12\mathbf1_{(0,1)}dr,\qquad
d\mu_A=\tfrac12\prod_{j=1}^2d\lambda(t_j)d\nu(r_j)dq_j.$$

Die gesamte Ausstattung beider Punkte wird gemeinsam vertauscht. Alle verwendeten Zustände sind invariant. Ein Paket hat die Form $\Psi=\sqrt2\,d(r)\,h(q)\,\chi(t)$. Der gemeinsame Faktor $\sqrt2$ kompensiert genau den Quotientfaktor des Randmaßes.

Für festes $K,\psi,\varphi$ gilt unabhängig von der ergänzten Basis

$$\langle\varphi,K\psi\rangle_{\mathcal H}
=\langle\varphi,P_EKP_E\psi\rangle_{\mathcal H},\qquad
\psi,\varphi\in\operatorname{ran}P_E.$$

Soweit $K\psi$ nur als Funktional auf den Gaußpaketen vorliegt, ist dieselbe Aussage unmittelbar die unveränderte Paarung mit denselben Testfunktionen. Ein größerer Ausgaberaum ändert keine bereits festgehaltene Paarung. Ein beobachteter Unterschied durch Änderung der Breite oder Normierung wäre eine andere Präparation. Ein wirklicher Reduktionsfehler zeigt sich in **ausgelassenen Komponenten** oder in Zwischenprojektionen bei der Zusammensetzung.

## 3. Vier auf fünfzehn normierte Zustände

Die Maskenreihenfolge ist `00,10,01,11`; jede gelabelte Maske hat Masse $1/4$. Die Dichtevektoren ohne den gemeinsamen Randfaktor $\sqrt2$ sind

$$d_0=(2,0,0,0),\quad d_+=\frac2{\sqrt3}(0,1,1,1),$$
$$d_\Delta=\sqrt{\frac23}(0,1,1,-2),\quad
d_A=\sqrt2(0,1,-1,0).$$

Die drei symmetrischen Richtungen $0,+,\Delta$ sind orthonormal. $\Delta=d_M/\sqrt3-\sqrt{2/3}\,d_D$ löst die bisher zusammengefassten Einfach-/Doppelbelegungen auf. Es wird keine vierte disjunkte „+“-Maske erfunden. $d_A$ ist antisymmetrisch und darf nur zusammen mit einem ebenfalls antisymmetrischen anderen Faktor als invariant gezählt werden.

Mit $q_s=(q_1+q_2)/\sqrt2$, $q_a=(q_1-q_2)/\sqrt2$ und $h_{00}=\pi^{-1/2}e^{-(q_s^2+q_a^2)/2}$:

| Modus | Faktor vor $h_{00}$ | Vertauschung | Gesamtfeldparität |
|---|---|---|---|
| 00 | 1 | gerade | gerade |
| 10 | $\sqrt2q_s$ | gerade | ungerade |
| 20 | $(2q_s^2-1)/\sqrt2$ | gerade | gerade |
| 02 | $(2q_a^2-1)/\sqrt2$ | gerade | gerade |
| 01 | $\sqrt2q_a$ | ungerade | ungerade |
| 11 | $2q_sq_a$ | ungerade | gerade |

Die skalaren Indizes bezeichnen Hermite-Gaußpakete, keine hergeleiteten Teilchenzahlen oder Energien. Alle zwölf Kombinationen $(0,+,\Delta)\times(00,10,20,02)$ und die beiden Korrelationen $(A,01),(A,11)$ sind invariant und normiert. Sie bilden genau den 14-dimensionalen Raum der masken- und uhrkonstanten invarianten Skalarpolynome vom Gesamtgrad höchstens zwei vor dem Gaußgrundpaket: drei symmetrische Dichtemoden mal vier symmetrische Feldmoden, plus eine antisymmetrische Dichtemode mal zwei antisymmetrische Feldmoden.

Der fünfzehnte Zustand ist $\sqrt2d_+h_{00}\chi_2$, mit

$$\chi_2(t_1,t_2)=\sqrt{\frac52}\,[P_2(t_1)+P_2(t_2)],\qquad P_2(t)=\tfrac12(3t^2-1).$$

Wegen $\int P_2d\lambda=0$ und $\int P_2^2d\lambda=1/5$ ist dieser Uhrzustand normiert und orthogonal zu den anderen vierzehn. Die vollständige Gram-Matrix wird aus exakten Momenten gerechnet: **$G_{15}=I_{15}$, Rang 15**. Weitere Dichteprofile, Uhrmoden und höhere Feldanregungen bleiben außerhalb; 15 ist keine Vollständigkeitsbehauptung für den Rand-Hilbertraum.

## 4. Erweiterte Matrixspalte ohne neue Feldquadratur

Es wird die vollständige Spalte für den Eingang $\Psi_{0,00}$ im erklärten 15-dimensionalen Ausgaberaum berechnet. Es wird keine vollständige $15\times15$-Matrix behauptet.

Nach innerer Gaußintegration ist die Randquadratik $Q=I-iK$, $K=M_{BB}-M_{BI}M_{II}^{-1}M_{IB}$, mit $M=\beta H_0$, $\beta=4/\sqrt6$. Sei $V=Q^{-1}$ und $A_{00}$ die phasenrichtige Grundpaketprojektion aus Schritt 4. Im Randindex $(q_0,q_1,q_3,q_4)$ liefern die exakten Gaußmomente

$$A_{20}=\frac{A_{00}}{\sqrt2}(V_{22}+2V_{23}+V_{33}-1),$$
$$A_{02}=\frac{A_{00}}{\sqrt2}(V_{22}-2V_{23}+V_{33}-1),\qquad
A_{11}=A_{00}(V_{22}-V_{33}).$$

Die beiden linearen Projektionen $A_{10},A_{01}$ sind exakt null durch Gesamtfeldparität. Die Formeln folgen auch durch Ableiten von $\exp(J^TVJ/2)$; es wird kein numerisches Feldintegral hinzugenommen.

Alle inneren Fresnelphasen werden aus der exakten Signatur des rationalen Innenblocks bestimmt. Die Randdeterminanten werden als Produkt der Wurzeln einzelner komplexsymmetrischer Gaußpivots mit positiver Realteilkomponente ausgewertet. Eine unkontrollierte Hauptwurzel der gesamten Determinante wird nicht verwendet. Die Grundprojektionen überlappen alle früheren Einschließungen; ein unabhängiger Eigenphasenansatz kontrolliert die Vorzeichen.

## 5. Dichtemasken und Uhrprobe

Mit $E(k)=e^{-ik/2}\operatorname{sinc}(k/2)$, $E(0)=1$, und

$$\kappa_x=\tfrac12+\frac\beta4\sum_{y<x}c_{xy}(t_x-t_y)^2$$

werden alle Dichten analytisch integriert. Für $f=\int d\lambda(t_3)E(\kappa_3)$, $g=\int d\lambda(t_4)E(\kappa_4)$ und $f_2,g_2$ mit jeweils zusätzlichem Faktor $P_2$ in diesem Ausgangsintegral erhält man für die verbleibenden drei Uhrkoordinaten:

$$D_0=\frac1{16}\int d\lambda^3(1+E_2),\quad
D_+=\frac1{16\sqrt3}\int d\lambda^3(1+E_2)(f+g+fg),$$
$$D_\Delta=\frac{\sqrt{2/3}}{32}\int d\lambda^3(1+E_2)(f+g-2fg),$$
$$D_A=\frac{\sqrt2}{32}\int d\lambda^3(1+E_2)(f-g),$$
$$D_{\chi_2}=\frac{\sqrt{5/2}}{16\sqrt3}\int d\lambda^3(1+E_2)(f_2+g_2+f_2g+fg_2).$$

Der gemeinsame Faktor pro Ausgangsmaskenkoeffizient $d_s$ ist $(1/4)\cdot2\cdot2\cdot(1/32)=1/32$: zwei Randquotienten, die zwei $\sqrt2$-Paketfaktoren, das Eingangsdichtepaket und alle fünf Atom-/Positivgewichte. Die zwei inneren Dichtestrata sind in $1+E_2$ enthalten. Alle Uhren bleiben auch an Atomen erhalten.

Die Formeln kontrahieren dieselbe fünfdimensionale Tensorregel; sie approximieren nicht heimlich eine niedrigerdimensionale Integrationsaufgabe. Für $d_Ah_{11}$ ändern bei Randvertauschung sowohl der Dichtefaktor als auch der skalare Faktor das Vorzeichen. Ihr Produkt ist invariant; die zehn bisherigen Orbits bleiben korrekt gewichtet.

## 6. Zertifizierung und unabhängige Kontrolle

Die primäre Rechnung verwendet 48 Gauß-Legendre-Knoten je Achse und 192 Bit Arb/Acb-Arithmetik. Aus Schritt 4 wird die bewiesene 5D-Schranke übernommen:

$$e_C(n)\leq\frac{\sqrt3}{2}\frac{\rho^{-2n}}{1-\rho^{-1}}
\sum_{j=0}^4\exp\!\left[\frac\beta2b(a+1)W_j(C)\right],$$

mit $\rho=2$, $a=5/4$, $b=3/4$ und $W_j=\sum_{\text{inzident}}|c|\leq19$. Der Beweis nutzt analytische Chebyshevkoeffizienten, Exaktheit bis Grad $2n-1$, positive normierte Gewichte und Teleskopieren der fünf Achsen. Der Unterschied zweier Quadraturregeln dient nicht als Fehlerschranke.

Die Integrandmajoranten für $D_0,D_+,D_\Delta,D_A$ unterscheiden sich um die Faktoren $1/\sqrt3,1,2\sqrt2/3,\sqrt{2/3}$. Für die Uhrprobe kann auf der einen komplex fortgesetzten Achse und vier reellen Achsen einheitlich

$$|\chi_2|\leq C_\chi=\sqrt{\frac52}\frac{3(a^2+1)}2<7$$

verwendet werden. Denn $|z|\leq a$ auf der Ellipse und $|P_2(z)|\leq(3a^2+1)/2$; auf der jeweils anderen reellen Ausgangsachse gilt $|P_2|\leq1$. Bei komplexer Eingangsachse ist die noch kleinere reelle Schranke ausreichend.

Die Fehler einer Amplitude erfüllen $e_{s,n}\leq\sum_C|c_C||A_{C,n}|e_{C,s}$. Arb schließt alle Knoten, Gewichte, Phasen, Matrixinversen, Momente und Wurzeln ein. Die exportierten Dezimalintervalle enthalten Darstellungsrundung. Der größte primäre analytische Fehler einer Komponente der Testspalte beträgt weniger als $1.60\cdot10^{-17}$ im komplexen Betrag. Die auf zwölf Dezimalstellen berichteten Real-/Imaginärteile und Normen haben einschließlich Rundung Fehler höchstens $10^{-12}$.

Eine Kontrolle mit 56 Knoten und 224 Bit überlappt alle primären Intervalle; ihr maximaler analytischer Fehler liegt unter $2.44\cdot10^{-22}$. Eine unabhängige NumPy-Rechnung mit acht Knoten integriert alle 33 gelabelten Historien direkt in fünf Dimensionen, ohne Orbitreduktion oder Uhrkontraktion. Sie stimmt mit der kontrahierten Achterregel überein. Sie ist ein Strukturtest, kein Fehlerzertifikat für die primäre Rechnung.

## 7. Reduktionsfehler im geprüften Raum

Sei $v_{15}$ der Vektor der fünfzehn Paarungen mit dem normierten Eingang $\Psi_{0,00}$ und $P_4$ die Koordinatenprojektion auf `0:00,0:10,+:00,+:10`. Dann ist ohne Annahme einer vollständigen L²-Ausgangswelle exakt definiert:

$$r_{15\leftarrow4}=\|(I-P_4)v_{15}\|_2
=\left(\sum_{j\notin P_4}|M_{j,0:00}|^2\right)^{1/2}.$$

Numerisch eingeschlossen:

$$\|v_{15}\|_2=0.278812474196\pm10^{-12},\qquad
r_{15\leftarrow4}=0.102348630703\pm10^{-12}.$$

Neun ausgelassene Komponenten sind zertifiziert nicht null, zwei weitere ausgelassene Komponenten sind exakte Paritätsnullen. Die ungeraden Paritätsnullen sind eine Negativkontrolle und keine Rechtfertigung, auch die geraden Zusatzmoden zu verwerfen.

Falls für die gekoppelte Wirkung später $K\Psi_{0,00}\in\mathcal H_A$ bewiesen wird, liefert Bessels Ungleichung

$$\|(I-P_4)K\Psi_{0,00}\|\geq r_{15\leftarrow4}>0.10234.$$

Es ist eine **untere Schranke** für den gesamten ausgelassenen Anteil, keine obere Schranke. Die relative Zahl $0.367087702939$ bezieht sich ausschließlich auf $\|v_{15}\|$, nicht auf eine unbekannte volle Ausgangsnorm. Für diese Spalte ist eine Vierzustandsapproximation mit absolutem Fehler unter $0.10234$ daher schon mit den getesteten Paarungen ausgeschlossen. Andere Eingangsspalten und die Restmoden oberhalb dieses Prüfbereichs werden nicht behauptet.

## 8. Andere Randpakete sind andere Präparationen

Als separate Breitenkontrolle wird nur der ausgehende symmetrische Skalargrundzustand auf $\sigma_s=1/2$ beziehungsweise $2$ geändert; $\sigma_a=1$, Eingang, Maße und Wirkung bleiben fest. Die Zustände werden jeweils korrekt neu normiert. Für den Atom-zu-Positiv-Eintrag folgt

| $\sigma_s$ ausgehend | Realteil | Imaginärteil |
|---|---:|---:|
| $1/2$ | −0.136384336821 | +0.104998562756 |
| $1$ | −0.155730245646 | +0.132674294297 |
| $2$ | −0.139781291672 | +0.136032575725 |

Fehler je Tabellenkomponente höchstens $10^{-12}$. Die Abhängigkeit ist messbar im Kontrollmodell, aber sie ist **kein** Abschneidefehler bei unverändertem Zustand. Der Überlapp mit dem ursprünglichen Skalarpaket ist $\sqrt{2\sigma_s/(1+\sigma_s^2)}<1$ für beide geänderten Breiten. Die zusätzliche Präparationsunsicherheit muss bei einer späteren physikalischen Interpretation gesondert festgelegt werden.

## 9. Verklebungsgeometrie und exakt fehlende Terme

Verwendet wird die vollständige geschichtete Ordnung $(2,1,2,1,2)$:

- Anfangsrand $\{0,1\}$, linkes inneres Element 2;
- Schnitt-Antichain $\{3,4\}$;
- rechtes inneres Element 5, Endrand $\{6,7\}$.

Jeder Punkt einer früheren Schicht liegt vor jedem Punkt einer späteren Schicht. Links $L=\{0,1,2,3,4\}$ und rechts $R=\{3,4,5,6,7\}$ steht jeweils die bereits zugelassene AA-Historie mit Code 25500. Der globale Raum hat acht, nicht zehn verschiedene Elemente.

Es werden zuerst die gemeinsamen Schnittterme abgezogen: $S_{\rm sew}=S_L+S_R-S_S$. Für den Schnitt ist $F_4(S)=2$, $S_{d,S}/\hbar=-(r_3+r_4)/2$ und der masselose skalare Schnittblock null. Außerdem kompensiert ein Faktor 2 das Schnitt-Quotientmaß $d\mu_S=(1/2)d\mu_{S,\rm lab}$, damit dieselbe gelabelte Innenmaßkonvention wie in der gemeinsamen Rechnung verwendet wird. Der folgende Fehler ist also nicht bloß eine doppelte Punktzählung oder ein vergessener Normierungsfaktor.

Die im Teilwirkungsprodukt fehlenden Paare sind:

| Paar $(i,j)$ | Innere Intervallpunkte | $c_{ij}$ |
|---|---:|---:|
| (0,5) | 3 | −8 |
| (1,5) | 3 | −8 |
| (2,5) | 2 | +16 |
| (2,6) | 3 | −8 |
| (2,7) | 3 | −8 |

Die weiteren grenzüberschreitenden Paare haben vier innere Punkte und Koeffizient null in dieser Wirkung. Daher

$$F_4(C)=88,\quad F_4(L)+F_4(R)-F_4(S)=72,\quad\Delta F_4=16,$$

$$\frac{\Delta S_\phi}{\hbar}=-\frac\beta4\sum_{(i,j)\in X}c_{ij}(q_j-q_i)^2,\qquad
\frac{\Delta S_d}{\hbar}=-\frac\beta4\sum_{(i,j)\in X}c_{ij}r_j(t_j-t_i)^2.$$

Insbesondere $\partial_{q_0}\partial_{q_5}(\Delta S_\phi/\hbar)=-4\beta\ne0$. Eine Korrektur, die ausschließlich die momentanen Schnittvariablen der Punkte 3 und 4 kennt, kann diese Abhängigkeit nicht herstellen. Erforderlich sind Informationen über schnittübergreifende Intervalle und ihre Endpunktfelder beziehungsweise ein daraus abgeleitetes gemeinsames Einflussfunktional. Wird beides bereits getrennt ausintegriert, reicht die momentane Zweipunkt-Randkonfiguration im Allgemeinen nicht aus. Die Behauptung bezieht sich auf diese lokale Schnittbeschreibung, nicht auf ein Verbot jeder möglichen erweiterten Verklebung.

## 10. Quantitativer Kernvergleich und positive Kontrolle

Für eine exakt integrierbare Kontrolle werden **alle acht Dichten auf ihr Nullatom eingeschränkt**. Das ist ein eigener nichtverschwindend gewichteter Dichtestratum-Beitrag, keine Entfernung aller Staubvariablen. Alle acht Uhren werden mit ihrem normierten Boxmaß integriert; ihre Phasen sind dort null. Beide äußeren Randzustände sind die normierten Atom-/Skalargrundpakete. Alle vier inneren Skalarvariablen werden im Abel-Sinn integriert. Der gemeinsame Maß- und Paketfaktor außerhalb der Skalarprojektion ist

$$\frac14\,(\sqrt2\,2)^2\,\left(\frac12\right)^8=\frac1{128}.$$

Die beiden rationalen Innenblöcke $H_{0,II}$ auf $(2,3,4,5)$ haben

| Wirkung | Determinante | Signatur |
|---|---:|---:|
| gemeinsame Achtpunktwirkung | −17170 | +2 |
| korrigierte Summe lokaler Teilwirkungen | +1190 | 0 |

Beide sind invertierbar. Alle Fresnelzweige sind somit ausdrücklich bestimmt. Für äußere Felder null beträgt schon das Verhältnis der bedingten inneren Kernelbeträge exakt $\sqrt{1190/17170}=\sqrt{7/101}\approx0.263262$; eine reine Gravitationsphasenänderung erklärt den Unterschied nicht.

Die vollständige normierte äußere Gaußprojektion des Nullatombeitrags ergibt:

| Rechnung | Realteil | Imaginärteil |
|---|---:|---:|
| gemeinsame Wirkung | −0.000076122522 | −0.000071394860 |
| lokale Teilwirkungen mit Schnittkorrekturen | +0.000327584152 | −0.000729801282 |
| Differenz | −0.000403706674 | +0.000658406421 |

Fehler je gerundetem Real-/Imaginärteil höchstens $10^{-12}$. Alle vier Datensätze einschließlich der gesonderten Differenz ohne Gravitationsphasen sind numerisch von null getrennt. Es handelt sich um einen Gegenbeleg für die dichteaufgelöste lokale Verklebungsbehauptung. Eine vollständige Summe über die 1089 Historienpaare und alle positiven Dichtestrata der Achtpunktgeometrie wurde nicht gerechnet; eine zufällige Kompensation in einer speziell gewählten Gesamtsumme wird nicht als ausgeschlossen behauptet.

**Positive Kontrolle:** Ausgehend von der ursprünglichen gemeinsamen Achtpunktwirkung führt die exakte Blockelimination zuerst von $(2,5)$ und dann $(3,4)$ zu demselben Schur-Komplement und derselben Determinante wie die gemeinsame Elimination aller vier inneren Variablen. Bei positivem gemeinsamem Regulator $\epsilon=1$ und $1/7$ stimmen zwei Eliminationsreihenfolgen sowie eine unabhängige, mit dem Gaußgewicht skalierte Eigenphasenrechnung überein. Der Regulator wird dabei jedem inneren Punkt genau einmal zugeordnet. Die Reihenfolge der Integration ist nicht die Ursache des gefundenen Unterschieds; die verwendeten Wirkungen unterscheiden sich.

## 11. Warum noch keine volle Reduktions- oder Evolutionsschranke folgt

Für echte Hilbertoperatoren mit geeigneten Definitionsbereichen gilt bei einem orthogonalen Schnittprojektor $P$, $Q=I-P$:

$$P K_2K_1P-PK_2PK_1P=PK_2QK_1P,$$

$$|\langle g,K_2QK_1 f\rangle|\leq
\|QK_2^\dagger g\|\,\|QK_1f\|.$$

Eine obere Verklebungsfehlergrenze erfordert **obere** Schranken für die beiden vollständigen ausgelassenen Anteile sowie korrekte Wirkungs- und Maßverklebung. Die hier nachgewiesenen endlichen Zusatzkomponenten liefern solche oberen Schranken nicht. Die beiden Fehlerquellen dürfen nicht vermischt werden: Mehr Zwischenzustände reparieren fehlende schnittübergreifende Wirkungsterme nicht.

Für die entkoppelte Referenz aus Schritt 4 lässt sich sogar eine konkrete Definitionsbereichslücke nachweisen. Ihr Schur-Komplement erfüllt in der ausgehenden antisymmetrischen Richtung

$$K_{a_R,a_R}=\beta\frac{28}{11},\qquad
K_{a_R,q_0}=K_{a_R,q_1}=K_{a_R,s_R}=0.$$

Nach Integration des normierten Eingangs besitzt die Ausgangsantwort deshalb die Form

$$g(t_R,r_R,q_{s,R},q_{a,R})=G(t_R,r_R)F(q_{s,R})
\exp\!\left(i\frac\beta2\frac{28}{11}q_{a,R}^2\right).$$

Die Grundzustandsmatrixpaarung $M_0\ne0$ aus Schritt 4 beweist, dass der Vorfaktor nicht fast überall null ist. Sein Betrag hängt nicht von $q_{a,R}$ ab. Da diese Feldachse die ganze reelle Linie umfasst, ist $\int|g|^2d\mu_A=\infty$. Die Matrixpaarungen mit Gaußpaketen bleiben dennoch endlich. Für jedes endliche Hermite-Paketprojektat $P_Ng\in L^2$ muss auch $g-P_Ng\notin L^2$ gelten; andernfalls wäre ihre Summe in $L^2$.

Das ist kein Widerspruch zu den normierten **Randzuständen** oder zur **Existenz endlicher Paketmatrixelemente**. Es zeigt, dass diese beiden Eigenschaften allein keinen überall definierten oder beschränkten Evolutionsoperator liefern. Für die gekoppelte Hauptwirkung wurde die vollständige L²-Abbildung in diesem Arbeitsschritt weder bewiesen noch widerlegt. Eine spätere Wahl eines anderen physikalischen Skalarprodukts, eines geeigneten Raums von Testfunktionen oder einer begründeten Randlokalisierung wäre eine zusätzliche Modelldefinition und müsste neu geprüft werden.

## 12. Was nun konkret fehlt

Für die untersuchte Eingangsspalte fehlen im Vierzustandsraum mindestens die detektierten geraden Feldanregungen, die aufgelöste Dichterichtung $\Delta$, eine Dichte-/Feldkorrelation und ein nichtkonstantes Uhrpaket. Der 15er-Raum macht sie sichtbar, ist aber selbst nicht als geschlossen nachgewiesen.

Für die Verklebung fehlen die schnittübergreifenden Intervallgewichte mit zugehörigen Endpunktfeld- und Staubuhrkorrelationen. Im Achtpunktbeispiel sind die fünf betreffenden Paare vollständig benannt. Ein gemeinsames Einflussfunktional oder ein ausreichend informationshaltiger erweiterter Rand-/Gedächtniszustand muss diese Abhängigkeiten behalten, bevor die versteckten Variablen separat integriert werden.

Für eine globale obere Reduktionsfehlergrenze fehlen der zulässige Operatorbereich, die vollständigen Zustandsrestschranken und ein qualifiziertes physikalisches Skalarprodukt. Die entkoppelte Referenz belegt, dass ein solcher Nachweis nicht aus kleinen numerischen Integrationsfehlern folgt.

## Quellen und reproduzierbare Belege

- Projektbasis: [PR #280](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/280), [PR #281](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/281), [PR #282](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/282). Sieben eingefrorene Dateien samt Git-Blob- und SHA-256-Werten stehen in `provenance.json`.
- NIST DLMF §18.3 und §18.12: [Hermite-Orthogonalität](https://dlmf.nist.gov/18.3), [erzeugende Funktionen](https://dlmf.nist.gov/18.12). Die hier verwendeten endlich vielen Polynome und Gram-Momente werden zusätzlich symbolisch geprüft.
- Python-FLINT 0.9.0: [Acb-Matrizen](https://python-flint.readthedocs.io/en/latest/acb_mat.html). Die Quadraturfehlerschranke wird separat analytisch bewiesen; die Ballarithmetik ersetzt diesen Beweis nicht.
- `results/states.json`, `reduction.json`, `crosscheck_56.json`, `gluing.json`, `independent_5d_n8.json` enthalten vollständige Matrizen, Orbitbeiträge, Einschließungen und Kontrollen.
