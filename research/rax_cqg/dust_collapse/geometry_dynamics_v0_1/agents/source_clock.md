# Quelle und Uhr: reguläre stationäre Randwertfamilie aus derselben Wirkung

**Ergebnis.** Das positive Quellenhindernis des Sechshistorienpiloten lässt sich durch einen ausdrücklich neuen dicken Randkragen überwinden, ohne die Wirkungsform zu ändern. Ein Zehnerketten-Kontrollfall besitzt innerhalb der bisherigen Uhrbox `[-1,1]` positive Dichten, eine streng kausal monotone Uhr und einen regulären gemeinsamen stationären Punkt für alle sechs freien Staub-, Uhr- und Skalarvariablen. Das ist ein konkreter stationärer Feldzweig bei festgehaltener Ordnung. Eine physikalische Geometrieevolution folgt daraus nicht. Die aus der Wirkung abgeleitete Vorwärtsrekursion der Uhr enthält sogar einen exakt nachgewiesenen wachsenden Störmodus.

Reproduktion: `python checks/source_clock/check.py`. Acht Kontrollgruppen bestehen; es wurde keine Amplitudenquadratur ausgeführt. Exakte Koeffizienten, rationale Intervalle und Annahmen stehen in `checks/source_clock/results.json`.

## 1. Unveränderte Wirkung und Reichweite des alten Hindernisses

Ausgangspunkt ist genau die dimensionslose masselose Wirkung des veröffentlichten Piloten:

\[
S_C=F_4(C)-\frac12\sum_jr_j
-\frac{\beta}{4}\sum_{i\prec j}b_{ij}
\left[r_j(T_j-T_i)^2+(q_j-q_i)^2\right],\qquad
\beta=\frac4{\sqrt6}.
\]

Hier gilt `b_ij=(1,-9,16,-8)` für offene Intervallgrößen `0,1,2,3`, danach null. Für frei variierte positive innere Dichten folgt

\[
C_j=-2\partial_{r_j}S_C
=1+\frac\beta2\sum_{i\prec j}b_{ij}(T_j-T_i)^2=0.
\]

Die vollständige Uhrvariation, einschließlich aller zukünftigen aktiven Dichten, ist

\[
E_j=\partial_{T_j}S_C
=\sum_{j\prec k}J_{jk}-\sum_{i\prec j}J_{ij},\qquad
J_{ij}=\frac\beta2r_jb_{ij}(T_j-T_i).
\]

Im alten Piloten haben die beiden A-Punkte nur den einen Vorgänger P. Deshalb ist dort `C_A=1+beta(T_A-T_P)^2/2>=1`; keine Wahl gerichteter Uhrpakete kann diese frei-innere Stationaritätsbedingung lösen. Das betrifft weder festgehaltene Randdichten noch sämtliche off-shell Quantenrandzustände. Ein neuer Kragen muss negative Intervallkoeffizienten vor den freien Variablen bereitstellen. Einfach mehr Zukunft hinzuzufügen repariert die erste freie Linkschicht nicht.

Die ursprüngliche Wirkung ist unter `T -> -T` invariant, die einzelnen `J` sind ungerade. Der alte reflektionsgerade Uhrvertrag annulliert daher einzelne orientierte Strominsertionen. Eine gerichtete Randpräparation wählt einen der beiden spiegelbildlichen Zweige; die Wirkung allein wählt dessen Vorzeichen nicht. Ihre globale Shift-Invarianz ist außerdem keine Shift-Invarianz des festen Integrationswürfels. Es wird hier keine Quanten-Ward-Identität ohne Supportrandterme vorausgesetzt.

## 2. Analytischer Kettenzweig und abgeleitete Uhrrekursion

Für die natürliche Kette `0<...<N-1` bezeichne `b_k=(1,-9,16,-8)` die Koeffizienten zu Abstand `k=1,2,3,4`. Es gilt exakt

\[
\sum b_k=0,\qquad \sum kb_k=-1,\qquad \sum k^2b_k=-19.
\]

Halte die ersten und letzten vier Punkte einschließlich ihrer Dichten fest. Frei sind nur `j=4,...,N-5`, jeweils `r_j,T_j,q_j`. Mit

\[
T_j=\left(j-\frac{N-1}2\right)\Delta,\qquad
\Delta=\sqrt{\frac2{19\beta}},\qquad r_j=\rho\in(0,1),\qquad q_j=0
\]

gelten alle freien `C_j=E_j=partial_qj S=0`. Dichten werden einzeln variiert; die später gewählte Gleichheit `r_j=rho` ersetzt nicht diese Variationen. Die Skalarkonstante null löst die Skalarvariation. Die endliche Uhrdifferenz beträgt `Delta≈0.253890244769331`. Der gemeinsame Vollschnittstrom im Bulk ist

\[
J_{\rm cut}=-\frac{19}2\beta\rho\Delta,
\qquad Q:=-J_{\rm cut}>0.
\]

Zwischen den beiden Rändern gilt vollständige Schnittbilanz. Einzelne Kantenströme wechseln weiterhin ihr Vorzeichen; `Q>0` ist keine positive Teilchenflussdarstellung auf jeder Kante und keine kalibrierte Masse. Dichteskalierung verändert `Q`, lässt in dieser festen Kontrollordnung aber dieselben Uhren bestehen.

Diese affine Familie benötigt eine neue Uhrbox: für N=9 mindestens `±4Delta≈±1.01556`, für N=10 `±(9/2)Delta≈±1.14251`, für N=11 `±5Delta≈±1.26945`. Ein kleinerer Support wird nicht stillschweigend vorausgesetzt. Der nächste Abschnitt zeigt unabhängig davon einen regulären N=10-Punkt im ursprünglichen Würfel.

Weil die Summe der vier Koeffizienten null ist, ist jede `C_j` exakt affin in ihrer eigenen Uhrvariablen. Für einen nichtverschwindenden Nenner folgt unmittelbar aus der Wirkung

\[
T_j=
\frac{1+(\beta/2)\sum_{k=1}^4b_kT_{j-k}^2}
     {\beta\sum_{k=1}^4b_kT_{j-k}}.
\]

Am affinen Zweig ist der Nenner `beta Delta` und
`partial C_j/partial T_j=-beta Delta`. Die Constraint-Jacobimatrix nach den inneren Uhren ist untere Dreiecksmatrix mit nichtverschwindender Diagonale. Für endliche kleine Randperturbationen kann ein regulärer lokaler Randwertzweig fortgesetzt werden, solange Nenner, positive Dichten, kausale Uhrabstände und Supportbedingungen erhalten bleiben. Die volle Uhrgleichung erfordert dabei die passende, im Allgemeinen rückwärtige Dichtefortsetzung; bloßes Einsetzen der Uhrrekursion genügt nicht.

**Keine stabile Cauchy-Evolution.** Die linearisierte Uhrrekursion ist

\[
\delta T_j+\delta T_{j-1}-18\delta T_{j-2}
+48\delta T_{j-3}-32\delta T_{j-4}=0.
\]

Ihr charakteristisches Polynom faktorisiert zu

\[
p(\lambda)=(\lambda-1)(\lambda^3+2\lambda^2-16\lambda+32).
\]

`p(-6)>0` und `p(-5)<0` beweisen eine reelle Wurzel in `(-6,-5)`. Es gibt damit eine vorwärts wachsende, alternierende lineare Störung mit Faktor größer als fünf pro Schritt. Die Dichtegleichung am affinen Zweig lautet
`rho_j+rho_(j+1)-18rho_(j+2)+48rho_(j+3)-32rho_(j+4)=0` und hat das reziproke Polynom. Stationäre Randwertregularität ist also nicht gleich gut gestellter Anfangswertdynamik. Dieser Befund wird nicht durch eine Projektions- oder Glättungsregel nachträglich entfernt.

## 3. Regulärer Zehnerkettenpunkt im unveränderten Uhrsupport

Nehme die Kette mit zehn Punkten, freie Punkte `4,5`, festgehaltene Randpunkte `0,1,2,3,6,7,8,9`. Alle Dichten sind bei dem Zeugen gleich `rho`, beispielsweise `rho=1/2`; alle Skalarwerte sind null. Setze

\[
T=(-1,-a,-b,-1/4,-d,d,1/4,b,a,1).
\]

Die vollständigen inneren Uhrgleichungen verschwinden für

\[
a=\frac{25b+d+11/2}{24}.
\]

Die zwei Dichteconstraints ergeben die folgenden beiden Polynome mit `c=1/4`:

\[
\begin{aligned}
0={}&16a^2-32ad-9b^2+18bd+c^2-2cd+16d-8+\sqrt6/2,\\
0={}&-8a^2-16ad+16b^2+32bd-9c^2-18cd+3d^2+\sqrt6/2.
\end{aligned}
\]

Elimination über `Q(sqrt(6))` liefert die Quartik

\[
\begin{aligned}
P(d)={}&5053647104d^4-13057422592d^3\\
&+(1144853856+4297302272\sqrt6)d^2\\
&+(5112353968-3554678400\sqrt6)d\\
&-1495146359+728374800\sqrt6.
\end{aligned}
\]

Die im Prüfer ausgewählte Wurzel ist durch
`0.12321176887857 < d < 0.12321176887858` isoliert. Gegensätzliche exakt rational eingeschlossene Endpunktvorzeichen beweisen Existenz; ein vollständig von null getrenntes Ableitungsintervall beweist Eindeutigkeit in diesem Intervall. Die Elimination liefert `b` als kubisches Polynom in `d` über `Q(sqrt(6))`; der genaue Ausdruck ist im JSON enthalten. Damit folgt

| Größe | Nach außen einschließendes Dezimalintervall |
| --- | --- |
| a | [0.740258642988029, 0.740258642988158] |
| b | [0.485719826513365, 0.485719826513488] |
| d | [0.12321176887857, 0.12321176887858] |

Die exakten rationalen Intervalle sind maßgeblich. Die Ordnung `0<d<1/4<b<a<1` ist bewiesen. Alle zehn Uhrwerte liegen im bisherigen `[-1,1]` und sind streng kausal geordnet. Dies ist keine auf Dezimalwerte allein gestützte Stationaritätsbehauptung: Die Gleichungen werden im algebraischen Quotienten exakt reduziert.

Die Constraint-Jacobimatrix lautet

\[
A=\frac{\partial(C_4,C_5)}{\partial(T_4,T_5)}
=\beta\begin{pmatrix}h&0\\-2d&h\end{pmatrix},
\qquad h=\frac{23b+2d-49/4}{3}<0.
\]

Der zertifizierte Bereich ist ungefähr
`h in [-0.277340150811821,-0.277340150810874]`; daher `det A=beta² h²>0`. Der innere masslose Skalarblock ist

\[
H_\phi=\begin{pmatrix}0&\beta/2\\\beta/2&0\end{pmatrix},
\qquad\det H_\phi=-\beta^2/4\ne0.
\]

Der gemeinsame Staub-/Uhrblock in der Reihenfolge `(T,r)` hat die Form
`[[H_TT,-A^T/2],[-A/2,0]]`; seine Determinante ist `det(A)²/16`. Weil der Skalar bei null nicht mit den übrigen inneren Variablen gemischt ist, ist die volle sechsdimensionale innere Hesse-Determinante `-beta^6 h^4/64`, also ungleich null. Somit liegt ein echter regulärer stationärer Feldpunkt mit lokalen Fortsetzungsbedingungen vor. Dieser algebraische Beweis wird durch den Fachagenten für den physikalischen Sektor unabhängig ergänzt.

Die drei vollständigen Schnitte hinter Punkt 3,4,5 liefern denselben Wert

\[
\frac{J_{\rm cut}}{\beta\rho}=-\frac{b+d}{3}-\frac{25}{12}
\in[-2.286310531797353,-2.286310531797314].
\]

Hier gelten Quelle, gerichtete Uhr und Schnittbilanz gemeinsam aus derselben Wirkung. Es wird weder ein künstlicher Quellterm hinzugefügt noch ein negativer Koeffizient durch seinen Betrag ersetzt.

## 4. Was geändert wird und was offen bleibt

Unverändert bleiben Wirkungsform, beta, massloses Skalarfeld, positive Dichtespanne und für den algebraischen Zehnerpunkt auch der Uhrwürfel. Neu sind die Kontrollgeometrie Kette, die vierlagigen festen Randkragen, gerichtete klassische Randwerte und positive terminale Dichten. Die alten terminalen Dichteatome und konstanten Uhrpakete werden nicht als derselbe Zustand umgedeutet. Exakte Dirichletwerte sind klassische Randdaten, keine bereits normierten L²-Quantenrandzustände. Es wurde keine neue Quantenamplitude mit diesem Randvertrag berechnet.

Die untere Schichtenbarriere und der frühere singuläre `delta(z²)`-Kragen werden damit in einem neuen endlichen Kandidaten überwunden. Dagegen bleiben physikalische Paarung, Massen- und Eigenzeitskala, Lorentz-/Vierdimensionalitätsnachweis, Geometriegleichung, ausgewähltes Historienmaß und gemeinsamer Außenraum offen. Die Kette ist ausdrücklich kein 4D-Mannigfaltigkeitsnachweis. Bei festgehaltenem C fällt `F4(C)` aus den Feldableitungen heraus, weil es feldunabhängig ist. Ein solcher stationärer Feldpunkt beweist folglich noch keine gravitative Rückwirkung.

Die kompakte Dichteintegration erzeugt weiterhin keine Constraint-Deltafunktion. Die Regularität macht eine Coarea-Konstruktion mathematisch möglich, leitet aber weder deren physikalische Auswahl noch eine RAQ-Paarung aus dem bisherigen Maß ab. Der neue Zweig ist ein kontrollierter Eingang für die jetzt getrennt erforderlichen Ordnungsvariation und Randverklebung; die instabile Uhr-Vorwärtsrekursion darf dabei nicht als etablierter Evolutionssolver verwendet werden.

## 5. Literaturanschluss und Prüfprovenienz

Die benutzte Wirkungsform ist ein Projektkandidat, dessen Kausalset-Operator durch Benincasa und Dowker motiviert ist. Deren Kontinuumsaussage setzt geeignete vierdimensionale approximierende Kausalsets und langsam variierende Felder voraus; sie validiert diese eindimensionale Kontrollkette nicht: [The Scalar Curvature of a Causal Set](https://arxiv.org/abs/1001.2725), [Verlagsfassung](https://doi.org/10.1103/PhysRevLett.104.181301).

Brown und Kuchař zeigen im kanonischen Kontinuumsmodell, wie Staubreferenzfelder zur Auflösung des Hamiltonconstraints dienen können. Das ersetzt nicht den fehlenden Nachweis einer entsprechenden diskreten kanonischen Struktur hier: [Dust as a Standard of Space and Time in Canonical Quantum Gravity](https://arxiv.org/abs/gr-qc/9409001), [Verlagsfassung](https://doi.org/10.1103/PhysRevD.51.5600).

Die neue Rechnung ist eigene symbolische/rationale Ableitung aus `boundary_coherence_v0_1/sources/pilot.json`. Der ausführbare Prüfer prüft Schichtenmomente, affine Familien N=9..16, volle Schnittbilanzen, Rekursion und wachsenden Modus, einen einfacheren supporttreuen N=9-Zeugen samt seinem Skalar-Nullmodus, den regulären supporttreuen N=10-Zeugen, algebraische Wurzelexistenz und alle sechs direkten inneren Ableitungen der vollständigen Wirkung. Keine der Literaturquellen wird als Beleg dieser neuen endlichen Rechnungen ausgegeben.
