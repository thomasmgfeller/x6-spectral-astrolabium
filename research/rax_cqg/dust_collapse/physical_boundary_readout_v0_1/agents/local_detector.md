# Gemeinsamer lokaler Randdetektor und seine Normvoraussetzung

**Ergebnis:** Ein festes, ausschließlich an gemeinsame zukünftige Skalarfelder gekoppeltes Gauß-Pointerinstrument lässt sich vollständig herleiten. Es enthält keinen versteckten Ordnungsindex. Im ursprünglichen gemeinsamen viermodigen Randmaß bleibt ein exakt bestimmtes Normhindernis. Unter dem zusätzlich erklärten gemeinsamen dreimodigen Reduktionsvertrag entsteht dagegen ein vollständiges positives Instrument: Die tatsächlichen reduzierten N11-Karten liefern verschiedene, normalisierte q7-Pointerverteilungen. Eine explizite Kontroll-/Umweltdilation ergänzt die kohärente akzeptierte Karte um alle fehlenden Ausgänge.

Der reduzierte Zustandsraum, seine Rigging-Normierung, die gemeinsame Eingangspräparation und die Dilation sind zusätzliche physikalische Postulate. Sie werden nicht als automatische Folge der ursprünglichen Wirkung ausgegeben. Die Rechnungen verwenden exakte Matrix- und Gaußidentitäten; es wird keine neue große Integration benötigt.

## 1. Festgelegter Apparat und gemeinsame Lokalität

Die gemeinsame zukünftige Randfläche besitzt Skalarwerte q_F=(q7,q8,q9,q10). Auf dem zunächst nur **kinematisch deklarierten** Raum H_F=L²(R⁴,dq_F) sei

\[
Q_\ell=\ell^Tq_F,
\qquad H_D=L^2(\mathbb R,dy),
\qquad p_y=-i\partial_y.
\]

Der Pointer beginnt im normierten Zustand

\[
\phi_\sigma(y)=(2\pi\sigma^2)^{-1/4}
\exp[-y^2/(4\sigma^2)],\qquad \sigma>0.
\]

Die eingeführte Wechselwirkung ist

\[
U_g=\exp[-igQ_\ell\otimes p_y].
\]

Q_ℓ und p_y sind selbstadjungierte Multiplikations-/Translationsobservablen auf den üblichen Definitionsbereichen; ihre Tensorfaktoren kommutieren stark. Die spektrale Definition liefert einen unitären Operator auf dem Produkt-Hilbertraum. In Koordinaten wirkt er als Translation des Pointers:

\[
(U_g\psi\otimes\phi_\sigma)(q_F,y)
=\psi(q_F)\phi_\sigma(y-g\ell^Tq_F).
\]

Dieselbe ℓ, dieselbe Breite σ und dieselbe Kopplung g werden für beide Ordnungszweige verwendet. Als einfaches konkretes kinematisches Beispiel dienen ℓ=(0,0,0,1), Q=q10, und g=σ=1 in den erklärten dimensionslosen Skalar-/Pointerkoordinaten. Die unten diskutierte Alternative Q=q7 bewahrt einen zusätzlichen Ausgangsconstraint des zweiten Zweigs.

**Eingeführt, nicht aus Gravitation hergeleitet:** Apparat, Pointerzustand, g, σ, Ausleseachse ℓ und Bineinteilung sind Messaufbauentscheidungen. Die N11-Wirkung begründet nicht von selbst diese Wechselwirkung. Der Fortschritt besteht darin, für einen fest erklärten lokalen Aufbau seine vollständige Wirkung abzuleiten, anstatt einen beliebigen Geometrie-Gramfaktor einzusetzen.

## 2. Vollständiges Instrument und tatsächliche Records

Die Messung der Pointerposition liefert die Krausdichte

\[
M_y=\langle y|U_g|\phi_\sigma\rangle
=(2\pi\sigma^2)^{-1/4}
\exp[-(y-gQ_\ell)^2/(4\sigma^2)].
\]

Jedes M_y ist beschränkt. Die Wirkungsdichte lautet

\[
E_y=M_y^\dagger M_y
=(2\pi\sigma^2)^{-1/2}
\exp[-(y-gQ_\ell)^2/(2\sigma^2)],
\quad \int_\mathbb R E_y\,dy=I.
\]

Die letzte Identität gilt im schwachen Operatursinn und für die zugehörige monoton wachsende Familie endlicher Integrale auch stark. Für einen normierten Zustand ρ entsteht die normierte Recorddichte p(y)=Tr(E_yρ). Alle y werden mitgeführt; ein willkürlicher Akzeptanz-Gain ist für dieses ideale vollständige Instrument nicht erforderlich. Ein realer Detektorverlust müsste als zusätzliche Physik samt eigenen Outcomes modelliert werden.

Für einen messbaren Bin B=[l,u] ergibt sich

\[
E_B=\Phi((u-gQ_\ell)/\sigma)-\Phi((l-gQ_\ell)/\sigma),
\qquad
\mathcal I_B(\rho)=\int_l^u M_y\rho M_y^\dagger\,dy.
\]

Eine Partition der gesamten reellen Achse, beispielsweise die drei Records y<−a, |y|≤a und y>a mit fest gewähltem a>0, summiert zu I. Das vergröberte Instrument ist im Allgemeinen **nicht** die einzelne Lüders-Karte √E_B ρ √E_B; die nicht mehr aufgelöste Pointerposition bleibt als innere Ausleseinformation berücksichtigt.

Bei festem q_F ist M_y in beiden Historien genau dieselbe Funktion. Das bedeutet nicht, dass die Historien prinzipiell dieselben Pointerstatistiken besitzen: Verschiedene **normierte** geometrieabhängige Skalar-Ausgangszustände können unterschiedliche Verteilungen von Q_ℓ erzeugen und damit vom gleichen lokalen Apparat unterschieden werden.

## 3. Der Umweltüberlapp wird zum berechneten Kern

Wenn der Pointer ausgelesen, sein Wert jedoch nicht aufbewahrt wird, ergibt sich im q_F-Kern

\[
\rho(q_F,q'_F)\longmapsto
\exp\!\left[-\frac{g^2(\ell^Tq_F-\ell^Tq'_F)^2}{8\sigma^2}\right]
\rho(q_F,q'_F).
\]

Dieser Faktor ist der explizit berechnete Überlapp der beiden verschobenen Pointerzustände. Er hängt von **Feldkonfigurationen**, nicht von einem verborgenen Ordnungsklassenlabel ab. Ein beliebiger konstanter γ_c darf nach der Zustandsintegration nicht unabhängig gewählt werden. Bei Zweigen ψ0 und ψ1 ist der recordabhängige Kreuzterm beispielsweise

\[
D_{01}(y)=\int dq_F\,|M_y(q_F)|^2\psi_0(q_F)\psi_1(q_F)^*.
\]

Seine y-Abhängigkeit wird durch die Zustände und denselben Apparat bestimmt. Die Vollständigkeit impliziert ∫dy D01(y)=⟨ψ1|ψ0⟩. Eine vollständige gemeinsame Unitärkopplung verändert den globalen Zweigüberlapp nicht; sie verteilt Informationen auf System und Pointer.

Falls ein separat begründeter normierter Ausgang eine Gauß-Marginale Q_ℓ∼N(m,v) besitzt, folgt exakt

\[
y\sim N(gm,\sigma^2+g^2v).
\]

Die Gaußfaltung wurde algebraisch geprüft. Als ausschließlich mathematische Gegenkontrolle zeigen die normierten zentrierten Marginalen v=1/2 und v=1 bei g=σ=a=1 verschiedene Mittelbinwahrscheinlichkeiten erf(1/√3) und erf(1/2). Es sind **keine N11-Zahlen**. Dieser Test widerlegt lediglich die unzutreffende Behauptung, derselbe Randraum oder derselbe lokale Apparat müsse alle geometrieabhängigen Zustände ununterscheidbar machen.

## 4. Ein aus der N11-Wirkung abgeleitetes Hindernis

Für C1, die Kette mit ausschließlich entfernten Relationen (4,5) und (5,6), rekonstruiert der Audit die ursprüngliche Intervallmatrix L aus (1,−9,16,−8). Mit H=βH̄ und H̄=−L/2 gilt die **exakte Elfspaltenidentität**

\[
a_{\rm eingebettet}+b\,\bar H_{F,:}=0,
\qquad
a=(-232,119,241,-128),\quad b=(0,16,32,46).
\]

Daraus folgt bei π=p/β der Ausgangsconstraint

\[
A_+=-232q_7+119q_8+241q_9-128q_{10}
+16\pi_8+32\pi_9+46\pi_{10}.
\]

Die Differentialdarstellung A+=a·q_F−(i/β)b·∇_F annihiliert bereits exp(iS_φ) punktweise, ohne stationäre Approximation und ohne partielle Integration. Ein ausschließlich innerer Abel-Regulator verändert die Identität nicht. Sie bleibt daher unter den gegebenen inneren Fresnel-/Abel-Paarungen, beliebiger zulässiger Eingangspaarung und dem q-unabhängigen Staub-/Uhrfaktor erhalten.

Setze e=b/||b||, q_F=z+te, z⊥e. Die allgemeine Lösung entlang dieser Richtung hat die Form

\[
\psi(z+te)=
\exp\!\left[-\frac{i\beta}{\|b\|}
\left((a\cdot z)t+\frac{a\cdot e}{2}t^2\right)\right]\Phi(z).
\]

Der Betrag ist unabhängig von t. Eine nichtnullige solche Lösung kann nicht in L²(R⁴,dq_F) liegen. Präziser lässt sich der lineare Constraint durch eine unitäre Phasenmultiplikation auf die freie Ableitung längs t transformieren; deren Nullraum in L²(R) ist trivial. Auch distributionelle Lösungen liefern deshalb keinen nichtnulligen L²-Ausgang.

Die gewöhnliche viermodige Skalar-Hilbertnorm trägt den C1-Zweig somit nicht. Eine endliche Paarung mit einem zusätzlichen Gauß-Randtest behebt das nicht: Sie ist ein endliches Matrixelement einer Distribution, keine Norm eines inklusiven Ausgangszustands. Ein nichtnulliger C1-Beitrag kann auch nicht durch Addition eines L²-C0-Ausgangs zu einem L²-Zustand werden; sonst wäre bereits ihre Differenz, der C1-Beitrag, L².

## 5. Warum der vollständige lokale Detektor die Norm nicht repariert

Die positive Integraldichte erlaubt die Tonelli-Vertauschung:

\[
\int dy\,\|M_y\psi\|^2
=\int dq_F\,|\psi(q_F)|^2\int dy\,|M_y(q_F)|^2
=\|\psi\|^2.
\]

Diese Identität gilt auch mit dem Wert ∞. Eine vollständige POVM macht aus der divergenten Ausgangsnorm keine endliche Wahrscheinlichkeit.

Für Q=q10 ist der konkrete Mechanismus noch deutlicher. Hier ℓ·e=46/||b||≠0. Für eine normierte transversale Amplitude Φ und jedes einzelne y ist die formale bedingte Norm

\[
\|M_y\psi\|^2
=\frac{1}{|g\ell\cdot e|},
\]

unabhängig von y. Der Pointer lokalisiert zwar für jedes feste y die nichtkompakte t-Richtung, liefert über sämtliche y aber eine unnormierbare uniforme Dichte. Genau diese Gaußintegration wurde ausgeführt.

Für eine gegenüber dem Postconstraint invariante Wahl wie Q=q7 gilt dagegen ℓ·e=0. Das Pointergewicht hängt nicht von t ab, sodass bereits jeder nichtnullige Record die unendliche Orbitnorm beibehält. Ein vollständiger Detektor kann weder mit einer invarianten noch mit einer nichtinvarianten Auslese die fehlende physikalische Norm ersetzen.

## 6. Observable im reduzierten Kandidatenraum

Unter dem allein für C1 vorgeschlagenen reduzierten Constraintvertrag gilt

\[
[q_{10},A_+]=i46/\beta\ne0,\qquad [q_7,A_+]=0.
\]

q10 ist somit keine wohldefinierte Dirac-Observable dieses Kandidatenquotienten. q7 ist eine invariant bleibende Feldobservable. Die gemeinsame positive Paarung entsteht nicht aus der Pointerkopplung; Abschnitt 7 verwendet dafür ausdrücklich den gesondert konstruierten gemeinsamen Reduktionsvertrag. Das viermodige Hindernis wird dadurch nicht widerlegt: Die zusätzliche Projektion/Quotientierung ändert den Vertrag.

Die nichtinvariante Kopplung kann nicht stillschweigend als constraintneutral behandelt werden. Sie transportiert den Constraint zu

\[
U_g A_+U_g^\dagger
=A_++(g\,b\cdot\ell/\beta)p_y.
\]

Bei b·ℓ≠0 ist y allein danach nicht invariant. Die Kombination y−gQ_ℓ kommutiert mit dem transportierten Constraint und wird durch U_g† auf die ursprüngliche Pointerposition zurückgeführt. Ein physikalisch informativer relationaler Detektor müsste deshalb einen tatsächlichen Referenz-/Apparatusvertrag mitführen; die bloße kinematische Translation ersetzt ihn nicht. Diese Aussage ist kein Verbot beliebiger relationaler Messmodelle.

## 7. Tatsächliche reduzierte N11-Zustände und lokale Records

`checks/independent_audit/results.json`, Abschnitt `conditional_common_scalar_reduction`, enthält die unabhängig bestätigten rationalen symplektischen 6×6-Karten R0 und R1. Der Vertrag verwendet eingangs q0=0 mit Darbouxkoordinaten (q1,q2,q3,π1,π2,π3) und ausgangs q10=0 mit (q7,q8,q9,π7,π8,π9). C0 benötigt eine zusätzliche beidseitige Constraintprojektion mit Normierung; C1 benötigt den Quotienten seines eigenen Constraints. Die Karten besitzen im so erklärten H3=L²(R³) unitäre kanonische Implementierer Vc, metaplektisch bis auf eine globale Phase. Relative Phasen müssen durch den gemeinsamen Fourier-/Rigging-Vertrag festgelegt werden; sie folgen nicht aus Kovarianzen. Für Abschnitt 8 werden die positiv normierten ursprünglichen Abel-/Fresnelkerne verwendet. Dies behauptet noch keine hiervon unabhängig vorgeschriebene strikte Mp-Gruppen-/Sewing-Liftkonvention.

Als **neue gemeinsame normierte Präparation** wird gewählt

\[
\psi_{\rm in}(Q)=(\beta/\pi)^{3/4}e^{-\beta|Q|^2/2},
\quad \beta=4/\sqrt6,
\quad [Q_j,\Pi_k]=i\delta_{jk}/\beta,
\quad \Sigma_{\rm in}=I_6/(2\beta).
\]

Dies ist nicht das frühere Produkt eines ein- und ausgehenden Randtest-Gaußfaktors. Die normierten Ausgänge ψc=Vcψin haben Kovarianzen Σc=RcRcᵀ/(2β). q7 ist ihre erste ausgehende Positionskoordinate und kommutiert mit dem C1-Postconstraint. Derselbe lokale Pointer mit **festen** g=σ=1 misst sie in beiden Zweigen.

\[
v_0=\frac{402923015552527127\sqrt6}{48005370368000000},
\qquad
v_1=\frac{9990583\sqrt6}{17334272}.
\]

| Tatsächlicher reduzierter Zweig | Var(q7) | Var(y)=1+Var(q7) | P(\|y\|≤1) |
| --- | ---: | ---: | ---: |
| C0: Kette | 20.5592788090 | 21.5592788090 | 0.170520244385 |
| C1: zwei entfernte Relationen | 1.41175992755 | 2.41175992755 | 0.480373695920 |

Die letzte Spalte ist jeweils exakt erf(1/√(2(1+vc))); die Tabelle zeigt Dezimalauswertungen dieser exakten Ausdrücke. Anders als die synthetische Gegenkontrolle in Abschnitt 3 sind dies die tatsächlich berechneten Zweigstatistiken der **erklärten reduzierten N11-Präparation**. Es sind nicht bereits die bedingten Wahrscheinlichkeiten einer kohärenten Zweigsumme und auch keine Wahrscheinlichkeiten für C0 beziehungsweise C1.

Damit kann derselbe ausschließlich feldlokale Aufbau die beiden Ausgangsverteilungen statistisch unterscheiden. Beide Gaußgesetze besitzen vollen Träger: Der Pointer liest keine perfekte historische C-Projektion aus. Der Überlapp der gesamten reinen Skalarzustände folgt ohne Wahl einer relativen Phase aus

\[
|\langle\psi_0|\psi_1\rangle|^2
=\frac{8}{\sqrt{\det(G_0+G_1)}},
\quad G_c=R_cR_c^T,
\quad
\det(G_0+G_1)=
\frac{48302375511159976015329778787094473}{3328552589678608384000000}.
\]

Sein Betrag ist 0.00814923284238. Dies ist ein **aus den vollen reduzierten Zuständen berechneter** Überlapp, weder ein frei eingesetztes γ noch der klassische Überlapp allein der Pointer-Recordgesetze. Der klassische Bhattacharyya-Koeffizient der beiden Pointerdichten ist hier vielmehr ∫√(p0(y)p1(y))dy=0.775646160295. Das komplexe Argument des quantenmechanischen Zustandsüberlapps wird durch diese Rechnung nicht bestimmt. Ein q7-Pointer lässt weitere Skalarinformationen ungemessen; seine Recordüberlappung darf daher nicht mit diesem vollen Zustandsüberlapp gleichgesetzt werden.

## 8. Explizite inklusive Dilation der kohärenten Karte

Die ursprünglichen inneren Uhr-/Dichtevariablen tragen das normierte positive Produktmaß

\[
d\mu=\prod_{j\in I}\left[\frac{dT_j}{3}\mathbf1_{[-3/2,3/2]}(T_j)
\;\frac{\delta_0(dr_j)+\mathbf1_{(0,1)}(r_j)dr_j}{2}\right].
\]

Als zusätzlicher Quantenvertrag wird E=L²(μ) mit normiertem |e⟩=1 eingeführt. Die Multiplikation mit exp(iSc(T,r)) ist unitär, weil Sc reell ist. Sc enthält die innere Staub-/Uhrwirkung und die gesamte ordnungsabhängige Phase Fc genau einmal. Dann ist Wc=⟨e|exp(iSc)|e⟩ genau das bestehende volle innere Integral, insbesondere |Wc|≤1. **W enthält bereits exp(iFc); ein weiterer Gravitationsvorfaktor wäre eine Doppelzählung.**

Ein offen deklarierter zusätzlicher Ordnungs-Kontrollraum C² wird in

\[
|w\rangle=\sqrt{\omega_0}|0\rangle+\sqrt{\omega_1}|1\rangle,
\qquad \omega_c\ge0,\quad \omega_0+\omega_1=1
\]

präpariert. Die Gewichte sind hierbei die gewählte Kontrollpräparation, keine aus CST hergeleitete fundamentale Historienverteilung. Auf C²⊗E⊗H3 wirkt die ausdrücklich erklärte unitäre Karte

\[
\mathcal U=\sum_c|c\rangle\langle c|\otimes e^{iS_c}\otimes V_c.
\]

Die Projektion des Kontroll-/Umweltzustands zurück auf |w,e⟩ löscht seine Welche-Ordnung-Information kohärent und liefert

\[
K=\langle w,e|\mathcal U|w,e\rangle
=\omega_0W_0V_0+\omega_1W_1V_1,
\qquad
\|K\|\le\sum_c\omega_c|W_c|\le1.
\]

Die Projektion ist ein markierter Ausgang dieses neuen Experiments. Das orthogonale Komplement des Kontroll-/Umweltraums wird vollständig als Fehlereignis mitgeführt. Die zugehörige CP-Karte erhält man durch Projektion mit I−|w,e⟩⟨w,e| und vollständige Ancilla-Spur. Ihr Effekt ist

\[
E_{\rm fail}=I-K^\dagger K\ge0.
\]

Der konkrete lokale q7-Pointer liest anschließend den akzeptierten Skalarausgang aus. Seine Krausdichte ist Ky=MyK, und damit

\[
\int_{\mathbb R}K_y^\dagger K_y\,dy+E_{\rm fail}=I.
\]

Diese Identität beweist Positivität und inklusive Normierung auf dem gesamten erklärten H3, nicht nur für die ausgewählte Gaußpräparation. Insbesondere gilt für jeden normierten Eingang p_fail≥1−(Σωc|Wc|)². Die einzelne Karte √(I−K†K) wäre eine alternative Vervollständigung mit demselben Fehlereffekt; sie darf nicht ohne Weiteres mit dem konkreten Zustand nach dem Ancilla-Fehlereignis gleichgesetzt werden.

Der Pointer selbst enthält weiterhin nur q7 und keine verborgene C-Steuerung. Der vorgeschaltete Ordnungs-Kontrollraum ist dagegen eine **offene zusätzliche physikalische Annahme**, die in der ursprünglichen N11-Wirkung nicht bereits als Apparat vorliegt. Dasselbe gilt für die Hilbertrauminterpretation des kompakten inneren Maßes und die kohärente Rückprojektion. Diese Konstruktion beweist ein wohldefiniertes bedingtes Experiment, nicht die Eindeutigkeit oder Fundamentalität dieses Vertrags.

Für ψin und fest gewählte ω0=ω1=1/2 gilt mit z=⟨ψ0|ψ1⟩

\[
p_{\rm acc}=\frac{|W_0|^2+|W_1|^2}{4}
+\frac12\operatorname{Re}(W_0^*W_1z),
\quad
p(y,\mathrm{acc})=\|M_yK\psi_{\rm in}\|^2.
\]

Ohne die relative Phase vorwegzunehmen, liefern die berechneten |z| und die vorhandenen n160-Uhrgewichte folgende Schranken:

| Zukünftiger Dichte-Randwert ρF | p_acc für den erklärten Gaußeingang | p_fail für jeden normierten Eingang mindestens |
| --- | --- | ---: |
| 1/8 | [0.312894358667, 0.317505110498] | 0.401905426118 |
| 1/4 | [0.290547566654, 0.294513611401] | 0.464130876949 |

Die Operator- und Gaußformeln sind exakt; diese mit W ausgewerteten Dezimalschranken übernehmen die bisherige Float64-Quadratur ohne vollständiges Rundungsintervall.

### Kohärente q7-Statistik mit festgelegten Kernphasen

`checks/canonical_scalar/gaussian_outputs.json` stellt zusätzlich die beiden normierten Ausgänge

\[
\psi_c(Q)=N_c\exp[-Q^TP_cQ/2],\qquad \operatorname{Re}P_c>0
\]

mit festgelegten relativen Phasen bereit: Der positiv normierte C0-Kern trägt exp(−iπ/4), der C1-Delta-Kern einen positiven Vorfaktor ohne zusätzliche Phase. Die Gaußwurzeln werden analytisch vom positiven reellen Gaußintegral fortgesetzt. Eine frei gewählte Hauptwurzel von det(P) wäre hierfür nicht ausreichend. Der lokale Check rekonstruiert dieselbe Fortsetzung unabhängig mittels sukzessiver komplexer Schur-Gaußpivots und bestätigt die vom kanonischen Agenten verwendete Whitening-Fortsetzung.

Die daraus berechneten Größen sind

\[
z=\langle\psi_0|\psi_1\rangle
=0.00311695032117692+0.00752958276498215i,
\]
\[
T=P_0^*+P_1,
\qquad u=1+(T^{-1})_{11}
=1.15596228880049-0.00632240560461981i.
\]

Für g=σ=1 lautet die Kreuzdichte mit der Konvention ψ0*ψ1

\[
D_{01}(y)=\frac{z}{\sqrt{2\pi u}}e^{-y^2/(2u)},
\quad
\int y^2D_{01}(y)dy=zu,
\quad
\int_{-1}^{1}D_{01}(y)dy=z\,\mathrm{erf}(1/\sqrt{2u}).
\]

Hier Re(u)>1; die Quadratwurzel wird im rechten komplexen Halbraum fortgesetzt. Diese drei Formeln wurden zusätzlich durch direkte eindimensionale Gaußintegrale überprüft. D01 ist ein komplexer Interferenzterm, keine eigenständige Wahrscheinlichkeitsdichte.

Setze ac=ωcWc, Z=pacc und sc²=1+vc. Die kohärenten akzeptierten Records besitzen aufgrund ihrer geraden Parität exakt Mittelwert null und

\[
\operatorname{Var}(y\mid\mathrm{acc})=
\frac{|a_0|^2s_0^2+|a_1|^2s_1^2
+2\operatorname{Re}(a_0^*a_1zu)}{Z},
\]
\[
P(|y|\le1\mid\mathrm{acc})=
\frac{\sum_c|a_c|^2\mathrm{erf}(1/\sqrt{2s_c^2})
+2\operatorname{Re}[a_0^*a_1z\,\mathrm{erf}(1/\sqrt{2u})]}{Z}.
\]

| ρF | pacc | pfail | Var(y\|acc) | P(\|y\|≤1\|acc) |
| --- | ---: | ---: | ---: | ---: |
| 1/8 | 0.312899454311426 | 0.687100545688574 | 7.81211583081042 | 0.391902869242470 |
| 1/4 | 0.290649447480394 | 0.709350552519606 | 6.70761574882277 | 0.409907634672626 |

Das sind jetzt tatsächliche kohärente Records der gewählten vollständigen Dilation mit ω0=ω1=1/2; die Zweigüberlappung wird aus den normierten Ausgangswellenfunktionen berechnet. Der größte Unterschied zwischen den eingesetzten n128- und n160-Uhrgewichten beträgt für die berichteten Größen 1.60×10⁻¹⁴. Die Gaußrechnung verwendet 70 Dezimalstellen; die Endwerte erben weiterhin die nicht vollständig rundungszertifizierte Float64-Uhrquadratur. Für die beiden Anfangswerte ρP=1/8 und 1/4 stimmen sämtliche Records gemäß der nachfolgenden exakten Phasenidentität überein.

## 9. Quellenvariation und physikalische Reichweite

Die unabhängig rekonstruierte Uhrwirkung liefert bei festen affinen Randuhren für beide Ordnungen ΣP C=151/19 und daher exakt

\[
W_c(\rho_P,\rho_F)=e^{-i151\rho_P/38}\widetilde W_c(\rho_F),
\qquad
K(\rho_P,\rho_F)=e^{-i151\rho_P/38}\widetilde K(\rho_F).
\]

Alle akzeptierten Pointereffekte K†EyK sowie der Fehlereffekt I−K†K sind somit bei festem ρF **exakt unabhängig von ρP**. Diese Aussage schließt alle Recordbins und eine Konditionierung auf Akzeptanz ein, sofern die Akzeptanzwahrscheinlichkeit nicht null ist. Ein positiver, normalisierter Messvertrag erzeugt also nicht nachträglich die fehlende Rückwirkung einer ausschließlich anfänglichen Dichtevariation.

Die vorstehende Änderung mit ρF ist die Änderung eines zukünftigen Randfilters beziehungsweise einer zukünftigen Randbedingung. Sie ist keine nachgewiesene Dynamikantwort auf eine ausschließlich frühere Materiequelle. Vollständig normalisierte gemeinsame Randpakete für Uhr und Dichte und ihre Integration in denselben physikalischen Vertrag sind hier noch nicht konstruiert. Die neue Präparation betrifft den reduzierten Skalarsektor; die äußeren Uhr-/Dichtedaten bleiben Parameter.

## 10. Status und Reproduktion

`python -B checks/local_detector/check.py` besteht mit **49 Kontrollen**. Das Hauptskript rekonstruiert den ursprünglichen N11-Postconstraint unabhängig; `reduced_detector.py` prüft beide bereitgestellten rationalen Karten erneut auf Symplektizität und reine Gaußkovarianz, berechnet die tatsächlichen q7-Records, den phasenunabhängigen Zustandsüberlapp und die inklusiven Kontraktions-/Quellenidentitäten. `coherent_detector.py` verifiziert zusätzlich die phasentreuen Präzisionsmatrizen, Normen und Wurzelfortsetzung und berechnet die tatsächlichen kohärenten Pointerwerte mit direkten eindimensionalen Gegenkontrollen. Die JSON-Ausgabe dokumentiert die lokalen Quelldateien samt SHA-256; keine große Integration wird gestartet.

| Bestandteil | Status |
| --- | --- |
| Gemeinsamer feldlokaler Pointer, keine versteckte C-Steuerung | Expliziter neuer Apparatusvertrag |
| Krausdichte, vollständige POVM und Recordbins | Exakt abgeleitet aus diesem Vertrag |
| Konfigurationsabhängiger Umweltüberlapp | Exakt abgeleitet; kein frei wählbarer Klassenparameter |
| C1-Ausgangsconstraint und Normobstruktion | Exakt aus der ursprünglichen N11-Skalarwirkung abgeleitet |
| Normalisierte N11-Zweizustands-Pointerwahrscheinlichkeiten im gemeinsamen L²(R⁴) | Nicht definiert |
| Gemeinsamer reduzierter H3-Raum samt q7-Instrument | Unter ausdrücklich erklärtem Rigging-/Normierungsvertrag konstruiert |
| Tatsächliche verschiedene N11-Zweig-Recordgesetze | Exakt aus den reduzierten Karten und einer erklärten gemeinsamen Präparation berechnet |
| Kohärente inklusive Karte einschließlich Fehlschlag | Durch zusätzliche unitäre Kontroll-/Umweltdilation vollständig normiert |
| Kohärente q7-Records mit festgelegten Abel-/Fresnelphasen | Berechnet; relative Phase und Kreuzdichte aus den tatsächlichen reduzierten Gaußzuständen |
| Anfängliche Dichteantwort bei festen Uhren und künftigem Rand | Exakt null in diesem Vertrag |
| Vollständiger gravitationsabgeleiteter physikalischer Randvertrag | Weiterhin offen; die zusätzlichen Postulate werden nicht aus der Wirkung hergeleitet |

Die Trennung ist damit präzise: Der ursprüngliche viermodige Kern besitzt das Normhindernis; der zusätzlich deklarierte dreimodige Vertrag trägt ein konkretes positives Experiment. Der zweite Befund ist konstruktiv, ersetzt aber nicht die noch fehlende Herleitung dieses Vertrags und einer echten Anfangsquellenantwort.
