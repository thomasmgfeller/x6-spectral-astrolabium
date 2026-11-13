# Kanonischer Skalar-Randvertrag des N11-Paars

**Ergebnis: Ein konkreter positiver gemeinsamer Skalarvertrag existiert.** Die Wirkung liefert eine reguläre Vier-Paar-Karte für die Kette C0 und eine prä-/postkonstruierte Relation mit drei reduzierten Paaren für C1. Nach einem ausdrücklich zusätzlich gewählten gemeinsamen Riggingvertrag ergeben beide Historien verschiedene, exakt symplektische Karten auf sechs Dimensionen und exakt unitäre Operatoren auf demselben $L^2(\mathbb R^3)$. Für C0 lässt sich der benötigte riggingartige Sandwich direkt als Gaußintegral berechnen und mit einem exakten Faddeev–Popov-Normfaktor unitarisieren; für C1 liefert die Wirkung einen normalisierbaren Delta-Gaußkern auf dem Quotienten. Diese Konstruktion ist mehr als ein Existenzargument für irgendeine positive Paarung. Sie ist jedoch kein Beweis, dass das ursprüngliche kompakte Staubmaß diesen Randvertrag auswählt.

## 1. Wirkung, Orientierung und überprüfte Daten

Es gelten $P=(0,1,2,3)$, $I=(4,5,6)$, $F=(7,8,9,10)$, $\beta=4/\sqrt6>0$,

$$
S_\phi=\tfrac12q^THq,\qquad H=-\frac\beta2L,\qquad \bar H=H/\beta.
$$

Der Laplacian wird für jedes vergleichbare Paar mit den Intervallgewichten $b=(1,-9,16,-8)$ rekonstruiert. C0 ist die vollständige N11-Kette; C1 entfernt ausschließlich $4\prec5$ und $5\prec6$, behält $4\prec6$ bei. Die Randorientierung ist $p_P=-\partial_PS_\phi$, $p_F=+\partial_FS_\phi$. Wir schreiben $\pi=p/\beta$. Dann ist die physische Poissonmatrix $J/\beta$, also $[q_j,\pi_k]=i\delta_{jk}/\beta$, nicht $i\delta_{jk}$.

Der Standalone-Check `checks/canonical_scalar/check.py` rekonstruiert sämtliche Matrizen aus den Ordnungen. Seine `results.json` enthält vollständige rationale Matrizen, nicht nur gerundete Resultate. Die unabhängigen Prüfungen des Auditagenten stimmen überein.

## 2. Was die ursprüngliche Wirkung bereits entscheidet

Die Legendre-Matrix

$$
\bar A_c=\bar H_{(I,P),(I,F)}
$$

hat für C0 Determinante $-16384$, für C1 Rang sechs. Damit ist C0 eine eindeutige symplektische Karte $M_0:(q_P,\pi_P)\mapsto(q_F,\pi_F)$. Ihr oberer rechter Block hat Determinante $9/65536$. Der interne C0-Hessian hat Determinante $-9\beta^3/4$ und Signatur $+1$.

Für C1 sind die beiden primitiven linearen Randbedingungen

$$
A_-=-128q_0+241q_1+119q_2-232q_3-46\pi_0-32\pi_1-16\pi_2=0,
$$

$$
A_+=-232q_7+119q_8+241q_9-128q_{10}+16\pi_8+32\pi_9+46\pi_{10}=0.
$$

Diese folgen aus den linken Nullvektoren der vorwärts/rückwärts orientierten Randrelation. Stärker: Die Koeffizienten erfüllen exakte Zeilenidentitäten mit dem **vollen** $11\times11$-Hessian. Deshalb gilt distributionell $\widehat A_+K_1=0$ und $K_1\widehat A_-=0$, nicht lediglich am klassischen Sattel.

Der unintegrierte $q_5$-Nullmodus ist an den Rand gekoppelt. Der reguläre interne Block $(q_4,q_6)$ hat Determinante $-\beta^2/4$, Signatur null. Deshalb ist $K_1$ ein Delta-Gaußkern. Er ist kein unitärer Vier-Moden-Operator auf $L^2(\mathbb R^4,dq)$. Tatsächlich hat jede nichtverschwindende distributionelle Lösung von $A_+\psi=0$ konstante Betragsdichte entlang einer nichtkompakten Eichrichtung und daher keine endliche $L^2(\mathbb R^4)$-Norm.

Unter der zusätzlichen kanonischen CCR-/Lebesgue-Quantisierung lässt sich C0 dagegen bereits vor Reduktion normieren:

$$
U_0=N_0K_0^{\rm bare},\qquad
N_0=128\left(\frac\beta{2\pi}\right)^{7/2}.
$$

Dies folgt aus $K_0^{\dagger}K_0=(2\pi)^7/(16384\beta^7)\,I$. Die positive Normierung erhält die ursprüngliche Abel-/Fresnelphase. Die Paarungs- und CCR-Annahme ist ein Quantisierungspostulat; die dafür erforderliche Zahl ist anschließend festgelegt.

## 3. Ein enges Hindernis, das eine Projektion nicht ausschließt

Der auf den Eingang zurückgezogene Postconstraint $B=A_+\circ M_0$ hat die Koeffizientenzeile

$$
B=\left(\frac{971}{64},\frac{18823}{512},-\frac{109559}{512},\frac{10371}{64},\frac{19807}{256},\frac{309}{8},\frac{961}{32},\frac{53}{4}\right).
$$

Er ist nicht proportional zu $A_-$, und

$$
\kappa=A_-JB^T=-\frac{52625}{32},\qquad
\{A_-,B\}_{\rm phys}=-\frac{52625}{32\beta}.
$$

Zwei starke Quantenbedingungen $A_-\psi=B\psi=0$ haben deshalb nur die Null-Lösung, auch im temperierten Distributionsraum. Das schließt eine bloße Einschränkung von $U_0$ auf einen invarianten C1-Randnullraum aus. **Es schließt einen Rigging-Sandwich nicht aus.** Derselbe von null verschiedene Bracket macht $B=0$ zu einer eindeutigen Eichfixierung auf jeder $A_-$-Bahn.

## 4. Konstruktiver gemeinsamer Quotient

Wir wählen als gemeinsamen neuen Randvertrag die Quotienten von $A_-=0$ beziehungsweise $A_+=0$ nach ihren linearen Hamiltonflüssen. Praktische Darbouxsektionen sind

$$
q_0=0,\quad (x,\pi_x)=(q_1,q_2,q_3;\pi_1,\pi_2,\pi_3),
$$

$$
q_{10}=0,\quad (y,\pi_y)=(q_7,q_8,q_9;\pi_7,\pi_8,\pi_9).
$$

Die jeweiligen Constraints bestimmen den ausgelassenen Impuls. Für C0 verschiebt man den Eingang zunächst entlang des $A_-$-Flusses bis $B=0$, wendet $M_0$ an und verschiebt den Ausgang entlang des $A_+$-Flusses in die Ausgangssektion. Für C1 löst man die eigene Randrelation direkt in diesen Sektionen.

Das liefert zwei verschiedene rationale Matrizen $R_0,R_1$, beide mit $R_c^T J_6R_c=J_6$. Ihre Konfiguration-Impuls-Blöcke erfüllen

$$
\det(R_0)_{q\pi}=\frac{737}{35633440},\qquad
\operatorname{rank}(R_1)_{q\pi}=2.
$$

Der zweite Rang ist eine Konfigurationskaustik und kein Hindernis für eine unitäre Metaplektik. Beide $qq$-Blöcke sind invertierbar. Die exakt geprüfte Zerlegung

$$
R=\begin{pmatrix}I&0\\CA^{-1}&I\end{pmatrix}
\begin{pmatrix}A&0\\0&A^{-T}\end{pmatrix}
\begin{pmatrix}I&A^{-1}B\\0&I\end{pmatrix}
$$

hat symmetrische Scherblöcke und liefert Ortschirp, normierte lineare Koordinatentransformation und Impulschirp auf $L^2(\mathbb R^3)$.

Andere transversale Sektionen desselben Constraintquotienten ändern die Darstellung durch kanonische Koordinatenwechsel. Die substantielle Zusatzannahme ist die Wahl dieses gemeinsamen Quotienten **auch für C0**, bei dem diese Constraints nicht durch seine eigene Legendre-Relation erzwungen werden. Dabei wird ein kanonisches Paar entfernt. Das ist keine Behauptung, dass die originale Vier-Paar-Evolution diesen Unterraum erhält.

## 5. Exakter C0-Rigging-Sandwich und sein Normfaktor

Für jede Randseite schreiben wir $A=a\cdot q+b\cdot\pi$, $q=Ex+bt$, wobei $E$ die drei Sektionskoordinaten einbettet. Setze

$$
f(x,t)=t\,a_E\cdot x+\tfrac12(a\cdot b)t^2.
$$

Die unitäre Koordinaten-/Chirptransformation ist

$$
(T\psi)(x,t)=\sqrt{46}\,e^{i\beta f(x,t)}\psi(Ex+bt).
$$

Sie macht $A$ zum Impuls $\Pi_t=-i\partial_t/\beta$. Wir fixieren die Fouriernormierung $\langle t|a\rangle=\sqrt{\beta/(2\pi)}e^{i\beta at}$. Der formal riggingartige Ausdruck wird nun als wohldefinierter oscillierender Kern zwischen den drei-dimensionalen Quotienten ausgewertet:

$$
S_0=\langle\Pi_{t,+}=0|T_+U_0T_-^{-1}|\Pi_{t,-}=0\rangle.
$$

Das ist kein Produkt gewöhnlicher beschränkter Projektoren im Vier-Moden-Hilbertraum. Sein zweidimensionales $t_-,t_+$-Gaußintegral hat den Hessian

$$
D=\frac19\begin{pmatrix}-7696&-4096\\-4096&-7696\end{pmatrix},
\quad\det D=\frac{4716800}{9},\quad\operatorname{sgn}D=-2.
$$

Der verbleibende Gaußkern erzeugt genau $R_0$. Alle Jacobis eingeschlossen ergibt sich

$$
S_0^\dagger S_0=\frac\beta{2\pi\,(52625/32)}I,
\qquad
V_0=\sqrt{\frac{2\pi\,52625}{32\beta}}\,S_0.
$$

Damit ist $V_0$ exakt unitär. Der positive Faktor ist die konkret berechnete transversale Rigging-/Faddeev–Popov-Normierung. Er ist nicht geraten. Der Schlüssel zum Check ist

$$
46^2\frac{\det(R_0)_{q\pi}}{\det(M_0)_{q\pi}\det D}=\frac{32}{52625}.
$$

Die ursprüngliche interne Fresnelphase $e^{i\pi/4}$ und die zusätzliche Zweivariablenphase $e^{-i\pi/2}$ ergeben den festgelegten reduzierten Kernelzweig $e^{-i\pi/4}$.

## 6. Exakter C1-Quotient und Delta-Normierung

Auf den Sektionen $q_0=q_{10}=0$ lautet der ursprüngliche Skalar-Kern

$$
K_1^{\rm bare}|_{\rm section}=\frac{8\pi^2}{\beta^2}\,\delta(\ell(x,y))e^{i\beta\Phi_1(x,y)},
$$

$$
\ell=8x_0-\tfrac92x_1+\tfrac12x_2+\tfrac12y_0-\tfrac92y_1+8y_2.
$$

Hier ist $\Phi_1=\tfrac12q_B^T[\bar H_{BB}-\bar H_{BR}\bar H_{RR}^{-1}\bar H_{RB}]q_B$, $R=(4,6)$, $q_B=(0,x,y,0)$. Nach derselben Randchirptransformation sind Phase und Deltaargument exakt unabhängig von beiden Eichkoordinaten. Deshalb muss man ihr Volumen **quotientieren**; ein erneutes unbereinigtes doppeltes Gruppenmitteln wäre divergent.

Direkte Kernelkomposition bestimmt die positive Normierung. Man eliminiert $y_2$ mit dem ersten Delta (Jacobi $8$) und Fourier-integriert $y_0,y_1$. Der verbleibende lineare Delta-Jacobi hat Betrag $2116$. Beide Kompositionsrichtungen geben deshalb

$$
V_1=\frac{92\sqrt2\,\beta}{2\pi}\,\delta(\ell)e^{i\beta\Phi_1},\qquad
V_1^\dagger V_1=V_1V_1^\dagger=I.
$$

Relativ zum oben ausdrücklich definierten **nackten Sektionskern** ist der positive Faktor

$$
N_1=\frac{23\sqrt2\,\beta^3}{4\pi^3}.
$$

Dieser Faktor sollte nicht ohne die gewählte Volumen-/Sektionskonvention mit dem unreduzierten Vier-Moden-Kernel verglichen werden. Der reguläre Zweivariablen-Fresnelblock hat Signatur null; der Nullmodus liefert $+2\pi\delta$. Positive Normierung erhält daher die Phase null. Zusammen mit Abschnitt 5 ist auch eine konkrete relative Phasenfortsetzung definiert. Die kanonischen Matrizen allein hätten diese Phasen nicht ausgewählt. Präzise handelt es sich um unitäre Implementierer linearer kanonischer Karten, also metaplektische Implementierer bis auf die ausdrücklich fixierte globale Phase. Eine zusätzliche strikte Metaplektik-Gruppen- oder Sewing-Liftkonvention müsste diese Phasen einheitlich behandeln; sie wird hier nicht stillschweigend behauptet.

## 7. Was der neue Vertrag erlaubt und offenlässt

**PASS:** Derselbe positive Skalarraum $\mathcal H_3=L^2(\mathbb R^3,dx)$, zwei konkrete unitäre Operatoren $V_0,V_1$, nachvollziehbare Fourier-/Abelphasen und feste positive Normfaktoren. Das gemeinsame ausgehende Observable $q_7=y_0$ ist invariant unter dem C1-Postconstraint und als gewöhnlicher selbstadjungierter Multiplikationsoperator verfügbar. Normierte Eingangsgaußzustände liefern normierte Ausgangszustände und können mit einem vollständigen Pointerinstrument untersucht werden. Dagegen ist $q_{10}$ keine quotientinvariante Observable, denn $[q_{10},A_+]=i46/\beta$.

**Zusatzvertrag:** kanonische CCR und Liouville-Paarung; dieselben C1-Randconstraints als gemeinsamer Riggingvertrag für beide Historien; die angegebenen Fourier-/Quotienten- und Phasenregeln. Innerhalb dieses Vertrags sind die skalaren Normfaktoren berechnet und keine freien Fitgewichte.

**HOLD für die volle physikalische Geometriedynamik:** Das ursprüngliche kompakte Staubmaß leitet diesen Gruppenmittelungs-/Projektionsvertrag nicht her. Seine Fouriertransformierte ist ein gewöhnlicher Faktor und keine Constraint-Deltafunktion. Feste äußere Uhr-/Dichtewerte bleiben Dirichletdaten, keine normierten physikalischen Randpakete. Auswahl und Normierung der Ordnungsgewichte, die physische Uhr-/Staubpaarung und ein tatsächlicher Detektorvertrag werden durch die Skalarreduktion nicht bestimmt. Eine kohärente Gesamtkombination kann nach diesen zusätzlichen Festlegungen konsistent gebildet werden; ihre Interpretation ist dann die dieses expliziten Modells.

Es gibt somit weder einen allgemeinen Unmöglichkeitsbeweis noch bereits eine eindeutige Volltheorie. Der konkrete Fortschritt ist ein aus der **vorliegenden** Skalarwirkung berechneter gemeinsamer reduzierter Quantisierungsvertrag, einschließlich jener Normalisierungen und Phasen, die vorher lediglich als freie Paarungswahl behandelt wurden.

## 8. Konkrete normierte Ausgangsgaußzustände

Für die zusätzlich festgelegte Präparation $\psi_{\rm in}(x)=(\beta/\pi)^{3/4}e^{-\beta x^Tx/2}$ berechnet gaussian_outputs.py beide normierten Ausgänge $\psi_c(y)=N_ce^{-y^TP_cy/2}$. Die exakten komplexen Präzisionen erfüllen $P_c=-i\beta(C_c+iD_c)(A_c+iB_c)^{-1}$ für die oben geprüften reduzierten Karten. Die Vorfaktoren werden aus den phasentreuen Kernen integriert. Jede komplexe Gaußwurzel wird entlang $R-itS$, $0\le t\le1$, vom positiven Realteil $R$ aus analytisch fortgesetzt; eine freie Hauptwurzel des Enddeterminanten wird nicht eingesetzt. Die Ausgänge stimmen exakt mit den kanonischen Karten überein; ihre Normen werden mit 70 Dezimalstellen kontrolliert.

Im gewählten positiven Normierungs-/Abelvertrag lautet der Überlapp

$$
\langle\psi_0,\psi_1\rangle
=0.00311695032117691677294
+0.00752958276498214750712\,i,
$$

mit Betrag $0.00814923284238467972$. Vollständige $N_c,P_c$, exakte rationale Präzisionen und die Wurzelkonvention stehen in checks/canonical_scalar/gaussian_outputs.json. Dieser Überlapp gehört zur **neuen normierten Dreipaar-Präparation**, nicht zur früheren vollständigen Schwartz-Paarung des Dirichletkernels. Ein entsprechender Detektor kann jetzt auf tatsächliche normalisierte Zustände angewandt werden.
