# Reduziertes Referenzmodell

## 1. Explizite zusätzliche Struktur

Arbeitsraum ist Ω=(0,∞)×ℝ mit Koordinaten Q und φ. Q ist zunächst eine
reduzierte Geometriekoordinate, nicht bereits eine aus CST abgeleitete
Volumenobservable. Die Reihenfolge der Kanäle ist (0,+).

$$\mathcal H_S=L^2(\Omega,dQ\,d\varphi)\otimes\mathbb C^2,\qquad
\Psi=(\psi_0,\psi_+)^T.$$

Die Identifikation beider Strata mit derselben kontinuierlichen Basis ist
eine Modellannahme. Das geerbte Maß mit isoliertem Dichte-Nullatom und positivem
Kontinuum liefert diese Identifikation nicht automatisch. Der Atomzweig ist
kein Nullvektor und darf bei einer Quotientierung nicht entfernt werden.
Ein interner Zweikanalsektor wird direkt quantisiert; eine 2×2-Matrix ist
ohne zusätzliche Spin-Phasenraumstruktur kein skalarer klassischer Hamiltonian.

## 2. Zeitunabhängige Baseline

Mit positiven konstanten M_Q, m_φ und ℏ wird definiert:

$$H=-a\partial_Q^2-b\partial_\varphi^2+\mathcal V,
\quad a=\frac{\hbar^2}{2M_Q},\quad b=\frac{\hbar^2}{2m_\varphi},$$
$$\mathcal V=\begin{pmatrix}V_0&G\\G^*&V_+\end{pmatrix},\qquad
V_s=U_s(Q)+\tfrac12m_\varphi\omega_s^2(Q)\varphi^2.$$

Die spezielle lineare Baseline setzt G=g_1(Q)φ mit reellem g_1.
Komplexes G ist im allgemeineren Modell möglich. H_{+0}=H_{0+}† erzwingt
keinen reellen oberen Off-Diagonalblock. Eine konstante relative Kanalphase
kann eine konstante Kopplungsphase entfernen. Eine Q-abhängige Phase erzeugt
bei der Transformation der kinetischen Energie eine Verbindung und zusätzliche
Ableitungsterme; sie darf nicht durch Betragsbildung stillschweigend entfernt werden.

## 3. Eine hinreichende selbstadjungige Realisierung

Für einen konkreten hinreichenden Satz seien U_s reell, lokal beschränkt
und global nach unten beschränkt, ω_s messbar mit
0<ω_min≤ω_s≤ω_max<∞ und g_1 reell und beschränkt. Die Formdomäne ist

$$\mathcal Q=H_0^1(\Omega;\mathbb C^2)\cap
\{\Psi:\varphi\Psi\in L^2,\ \sum_s\int U_s^+|\psi_s|^2<\infty\}.$$

H_0^1 bezeichnet insbesondere die verschwindende Spur am geometrischen Rand
Q=0; in der Materierichtung liegt keine endliche Wand. Die positive
kinetische, geometrische und harmonische Form ist dicht definiert und
geschlossen. Für jedes ε>0 gilt punktweise

$$|g_1\varphi|\leq\varepsilon\varphi^2+
\frac{\|g_1\|_\infty^2}{4\varepsilon}.$$

Der Mischterm ist somit infinitesimal formbeschränkt relativ zur positiven
harmonischen Form. Der KLMN-Satz ergibt eine abgeschlossene, nach unten
beschränkte Form und ihren eindeutig zugeordneten selbstadjungigen Operator
(Quelle S1). Seine Operatordomäne wird durch den Formdarstellungssatz bestimmt;
eine bloß schematische H²-Domäne ersetzt diesen Schritt nicht. Für die späteren
punktweisen Bilanzen werden zusätzlich ausreichend glatte Koeffizienten und
Zustände mit den benötigten Ableitungen und integrierbaren Randspuren verlangt.

Dies ist ein bedingter Satz für diese Familie, keine Prüfung unbekannter
CST-Koeffizienten. Unbeschränktes g_1 oder veränderliche Massen verlangen
eine erneute Formanalyse. Dirichlet erzeugt eine reflektierende Wand;
dies ist keine hergeleitete Singularitätsauflösung. Der gewöhnliche
Halbgeradenimpuls -iℏ∂_Q ist dabei nicht selbstadjungig (S2).

## 4. Relationale Uhr und physikalisches Produkt

$$\mathcal H_{\rm kin}=L^2(\mathbb R,d\chi)\otimes\mathcal H_S,
\quad C=\overline{p_\chi\otimes I+I\otimes H},
\quad p_\chi=-i\hbar\partial_\chi.$$

Die selbstadjungige Summe ist über das gemeinsame Spektralmaß der Operatoren
auf getrennten Faktoren definiert. Für die idealisierte lineare Uhr gilt

$$C\Psi=0\iff i\hbar\partial_\chi\Psi=H\Psi,
\quad\Psi(\chi)=e^{-i(\chi-\chi_0)H/\hbar}\psi_0.$$

Das physikalische Skalarprodukt ist das Produkt der Anfangsdaten auf einem
Uhrschnitt und unabhängig vom Schnitt. Nichttriviale Lösungen sind über die
gesamte Uhrgerade nicht L²-normierbar; sie werden distributionell in einer
geeigneten Test-/Dualraumkonstruktion behandelt. Gruppenmittelung liefert
formal δ(C), keine beschränkte orthogonale Projektion im kinematischen L²-Raum.
Nach Quotientierung der Nullrichtungen und Vervollständigung gilt bedingt
H_phys≅H_S (S3). Die kanonische Monotonie der postulierten linearen Uhr ist
eingebaut und keine Herleitung einer physikalischen CST-Uhr.

Für eine reduzierte Observable A ist A(χ)=U(χ,χ_0)†AU(χ,χ_0) ihre Darstellung
auf den Anfangsdaten. Ein nackter Kanalprojektor kommutiert bei Mischung
nicht mit C. Eine skalare Matrixwirkung, eine Uhrparametrisierung und die
physikalische CST-Constraintalgebra sind verschiedene Aussagen.

## 5. Symmetrien und Reichweite

Bei geraden V_s in φ und ungeradem G gilt für P=σ_z R_φ (Spiegelung φ→-φ)
die Symmetrie [H,P]=0, sofern die Domäne invariant ist. Die P=±1-Räume sind
dynamisch invariant. Für einen Zustand in einem dieser Räume verschwindet
die reduzierte Stratumkohärenz trotz möglichem Transfer und Verschränkung.

Bei G=0 sind die Strata dynamisch entkoppelt. Superselektion würde zusätzlich
[Π_s,A]=0 für alle zulässigen Observablen verlangen (S4); sie folgt nicht
allein aus H_{0+}=0. Auch die Paritätszerlegung ist keine automatische
Superselektion. Globale Norm und bei zeitunabhängigem H die Energie bleiben
erhalten. Ihre Erhaltung allein besagt nichts über die numerische Genauigkeit.

## 6. Erwartungswerte und semiklassische Näherung

Mit gemeinsamem kinetischem Term und reellem G=g_1φ ist
h=(g_1φ,0,(V_0−V_+)/2). V_s enthalten hier ausdrücklich die vollständigen
diagonalen Potentiale, einschließlich der Materiefrequenzen. Für s=⟨σ⟩ gilt

$$\dot{\mathbf s}=\frac2\hbar\langle\mathbf h(\hat Q,\hat\varphi)
\times\boldsymbol\sigma\rangle.$$

Die Ersetzung durch (2/ℏ)h(⟨Q⟩,⟨φ⟩)×s ist eine zusätzliche
Korrelations- und Paketbreitennäherung. Reine Präzession erhält |s|;
Verschränkung kann dagegen |s|²=2 Tr(ρ_strat²)−1 ändern. Ein kontrollierter
semiklassischer Grenzfall benötigt einen kleinen Parameter, ein Zeitfenster
und Fehlerkontrolle. Die geometrische Ehrenfest-Bilanz enthält den Randimpuls
aus [BALANCES.md](BALANCES.md).
