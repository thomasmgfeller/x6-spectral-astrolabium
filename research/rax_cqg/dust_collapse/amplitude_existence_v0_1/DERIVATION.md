# Existenz der endlichen AA-Amplitude im Abel-Sinn

Version 0.1 · 11. November 2026 · Anschluss an PR #278, #279 und #280.

## 1. Präzise Aussage und Grenze

Für die **33 abgedeckten AA-Ordnungen mit einem inneren Element**, die volumen­gewichtete minimale Skalarwirkung aus Schritt 1 und die normierten Randzustände samt kompakten Staubmaßen aus Schritt 2 existieren sämtliche projizierten Matrixelemente im unten definierten Abel-Grenzwert. Dies gilt einschließlich der Dichteatome und beliebig kleiner positiver Dichten. Es gibt eine vom Abel-Regulator unabhängige integrierbare Majorante und eine explizite lineare Fehlerabschätzung.

Bewiesen wird ein Satz für diesen deklarierten endlichen Kandidaten. Die physikalische Historiengewichtung, das physikalische Skalarprodukt, die unendliche CST-Summe und die Entfernung der Staubboxen werden damit nicht hergeleitet. Alle acht physikalischen Gates bleiben **HOLD**. Die tatsächlich gewählten inneren Skalarblöcke sind gleichmäßig invertierbar; singuläre Blöcke werden zusätzlich durch einen allgemeinen Satz und Gegenbeispiele geprüft, nicht als Eigenschaften dieser 33 Blöcke ausgegeben.

## 2. Gemeinsamer Vertrag

Die gelabelten Mengen sind $L=\{0,1\}$, $I=\{2\}$ und $R=\{3,4\}$. Beide Ränder sind Zweierantichains. Die Kontrollfamilie $\mathcal C$ enthält die 33 transitiven Ordnungen, in denen das innere Element mindestens einen Vorgänger in $L$ und einen Nachfolger in $R$ hat und jeder äußere Punkt eine Relation zum gegenüberliegenden Rand besitzt. Die Labelkonvention ist fest; etwaige Symmetriefaktoren der Historien gehören in die noch zu spezifizierenden Koeffizienten $c_C$.

Fixiere $\ell,\hbar>0$, $\mu^2\geq0$ und positive endliche Paketbreiten $\sigma_s,\sigma_a$. Es gelten

$$v=\ell^4,\quad a=\frac4{\sqrt6\ell^2},\quad T_b=\ell,\quad W=\hbar,\quad F=\frac{\sqrt\hbar}{\ell},$$
$$t=T/T_b,\qquad r=w/W,\qquad q=\Phi/F.$$

Die Wirkungen bleiben unverändert:

$$S_d=-\frac12\sum_x w_x(1+\Gamma_x[T]),\qquad
\Gamma_x[T]=\frac12\sum_{y\prec x}B_{xy}(T_x-T_y)^2,$$
$$S_\Phi=\frac12\Phi^T H_C\Phi,\qquad
H_C=-\frac12D_{\rm inc}^T\operatorname{diag}(vB_{xy})D_{\rm inc}-\mu^2vI.$$

Hier ist $B_{xy}=a(1,-9,16,-8)$ für die entsprechenden Intervallschichten des deklarierten 4D-BD-Kandidaten. Die Skalarwirkung hängt **nicht direkt von $T,w$** ab; die direkte Staub-Skalar-Kopplung ist null. Insbesondere ist $w=0$ kein Abschalten des Skalarfeldes.

An jedem Punkt werden die Maße

$$d\lambda(t)=\tfrac12\mathbf1_{[-1,1]}dt,\qquad
d\nu(r)=\tfrac12\delta_0(dr)+\tfrac12\mathbf1_{(0,1)}dr$$

verwendet. Beide besitzen Masse eins. Das Randmaß ist

$$d\mu_A=\tfrac12\prod_{j\in A}d\lambda(t_j)d\nu(r_j)dq_j.$$

Der Faktor $1/2$ ist der Quotient durch die Randvertauschung. Die Randpakete sind $\Psi_{s,n}=\sqrt2\,d_s h_n$, mit konstantem Uhrpaket $\chi=1$ auf der Box. Die gelabelten Dichtepakete und ihre **L1-Normen** sind:

| $s$ | $d_s$ | $a_s=\int|d_s|\,d\nu^2$ |
|---|---|---|
| $0$ | $2\mathbf1_{00}$ | $1/2$ |
| $M$ | $\sqrt2(\mathbf1_{10}+\mathbf1_{01})$ | $1/\sqrt2$ |
| $D$ | $2\mathbf1_{11}$ | $1/2$ |
| $+$ | $2(\mathbf1_{10}+\mathbf1_{01}+\mathbf1_{11})/\sqrt3$ | $\sqrt3/2$ |

Die Belegung 1 bedeutet $0<r<1$, die Belegung 0 das Atom. $+$ umfasst **mindestens eine positive Dichte**, kohärent mit gleicher positiver Amplitude. Es gilt $d_+=\sqrt{2/3}d_M+d_D/\sqrt3$.

Mit $q_s=(q_1+q_2)/\sqrt2$, $q_a=(q_1-q_2)/\sqrt2$ lauten die skalaren Pakete

$$h_0=\frac{\exp[-(q_s^2/\sigma_s^2+q_a^2/\sigma_a^2)/2]}{\sqrt{\pi\sigma_s\sigma_a}},\qquad
h_1=\sqrt2\frac{q_s}{\sigma_s}h_0.$$

Sie haben L2-Norm eins und L1-Normen

$$L_0=2\sqrt{\pi\sigma_s\sigma_a},\qquad L_1=4\sqrt{\sigma_s\sigma_a}.$$

Die primäre Familie ist $(s,n)=(0,0),(0,1),(+,0),(+,1)$; ihre kinematische Gram-Matrix ist $I_4$. Die folgenden Schranken gelten auch für die aufgelösten Sektoren $M,D$ und durch endliche Linearkombinationen für deren Spann.

## 3. Definition der vollständigen regulierten Kandidatenamplitude

Seien $c_C$ beliebige **feste endliche komplexe** Historienkoeffizienten mit

$$C_\nu=\sum_{C\in\mathcal C}|c_C|<\infty.$$

Sie sind unabhängig vom Abel-Regulator und den Staubvariablen; endliche gemeinsame Vorfaktoren dürfen hier absorbiert werden. Ein divergierender Regulatorvorfaktor ist nicht Teil dieses Satzes. $S_g(C)$ ist reell und endlich. Für $\epsilon>0$ definieren wir

$$\begin{aligned}
\mathcal M_{s'n',sn}(\epsilon)
={}&\sum_C c_Ce^{iS_g(C)/\hbar}
\int d\mu_R\,d\mu_L\int d\lambda(t_2)d\nu(r_2)dq_2\,
e^{-\epsilon q_2^2/2}\\
&\hspace{12mm}\times\overline{\Psi_{s',n'}(R)}\Psi_{s,n}(L)
e^{i(S_d+S_\Phi)/\hbar}.
\end{aligned}$$

Bei $\epsilon>0$ ist das Gesamtintegral absolut integrierbar: alle Staubmaße sind endlich, die Randpakete sind L1 und der innere Skalar wird gaußgedämpft. Fubini ist deshalb zunächst zulässig. Wegen der tatsächlichen Wirkungsseparation gilt exakt

$$\mathcal M_{s'n',sn}(\epsilon)=\sum_C c_Ce^{iS_g(C)/\hbar}
D_C^{s's}A_C^{n'n}(\epsilon),$$
$$D_C^{s's}=\frac12\int\prod_{x=0}^4d\lambda(t_x)d\nu(r_x)
\,d_{s'}(r_3,r_4)d_s(r_0,r_1)e^{iS_d/\hbar},$$
$$A_C^{n'n}(\epsilon)=\int_{\mathbb R^4}d^4b\,
\overline{h_{n'}(b_R)}h_n(b_L)\,e^{ib^TB_Cb/2}F_{C,\epsilon}(J_Cb).$$

Hier $b=(q_0,q_1,q_3,q_4)$; die Matrixblöcke werden im nächsten Abschnitt definiert. Der Vorfaktor $1/2$ in $D_C$ ist $(1/2)^2(\sqrt2)^2$, also zwei Randquotientmaße und zwei normierte Randpakete. Er darf nicht nochmals eingesetzt werden.

**Art des Grenzwerts:** $\mathcal M(0)$ bedeutet ausschließlich $\lim_{\epsilon\downarrow0}\mathcal M(\epsilon)$ mit diesem unnormalisierten Abel-Regulator. Das unregulierte Integral über alle fünf Skalarvariablen ist nicht absolut konvergent: sein Absolutbetrag dämpft $q_2$ nicht. Bewiesen wird die absolute Integrierbarkeit nach der analytischen inneren Abel-Integration. Eine beliebige Umordnung des unregulierten fünfdimensionalen Integrals folgt daraus nicht.

## 4. Gleichmäßige Lücke der tatsächlichen inneren Blöcke

Setze $\beta=4/\sqrt6$ und $m_*^2=(\mu\ell)^2$. Für die dimensionslose Matrix $M_C=F^2H_C/\hbar$ gilt in der Reihenfolge $(b,q_2)$

$$M_C=\begin{pmatrix}B_C&J_C^T\\J_C&-\alpha_C\end{pmatrix},\qquad
\alpha_C=\frac\beta2(p_C+q_C)+m_*^2.$$

$p_C,q_C\in\{1,2\}$ zählen die Vorgänger beziehungsweise Nachfolger des inneren Elements. Alle diese inzidenten Relationen sind Links; damit ist jeder nichtverschwindende Eintrag von $J_C$ gleich $\beta/2$. Die übrigen Randeinträge dürfen andere Vorzeichen haben; sie erscheinen in der reinen Phase $e^{ib^TB_Cb/2}$.

$$\alpha_C\geq\alpha_0:=\beta+m_*^2>0,\qquad
\|J_C\|^2=\frac{\beta^2}4(p_C+q_C),\qquad
\frac{\|J_C\|^2}{\alpha_C^2}\leq\frac1{p_C+q_C}\leq\frac12.$$

Die unabhängig aus den Relationen rekonstruierten 33 Matrizen stimmen mit dem eingefrorenen Vorgängerartefakt überein. Die Häufigkeiten von $(p,q)$ sind $(1,1):20$, $(1,2):6$, $(2,1):6$, $(2,2):1$. Diese Lücke hängt von keiner Staubdichte ab. Sie schließt daher auch alle Null­dichte-Atome ein.

Im dimensionalen Feldmaß ist $|H_{II}|\geq v(a+\mu^2)$. Dass die dimensionslose Lücke unter $T_b=\ell$, $F=\sqrt\hbar/\ell$ bestehen bleibt, ist **kein Kontinuumssatz für festgehaltene physikalische Zustände**: Uhrbox und Feldpakete ändern dabei ihre physikalischen Skalen.

## 5. Majorante und dominierter Regulatorgrenzwert

Für reelles $\eta=J_Cb$ ergibt die komplexe Gaußintegration

$$F_{C,\epsilon}(\eta)=\int_{\mathbb R}e^{-(\epsilon+i\alpha_C)x^2/2+i\eta x}dx
=\frac{\sqrt{2\pi}}{(\epsilon+i\alpha_C)^{1/2}}
\exp\!\left[-\frac{\eta^2}{2(\epsilon+i\alpha_C)}\right].$$

Die Wurzel wird aus der rechten Halbebene fortgesetzt; bei $\epsilon=0$ und $\eta=0$ ist die Phase $e^{-i\pi/4}$. Es folgt

$$|F_{C,\epsilon}(\eta)|=
\frac{\sqrt{2\pi}}{(\epsilon^2+\alpha_C^2)^{1/4}}
\exp\!\left[-\frac{\epsilon\eta^2}{2(\epsilon^2+\alpha_C^2)}\right]
\leq\sqrt{\frac{2\pi}{\alpha_0}}.$$

Nach innerer Integration ist damit eine regulatorunabhängige Majorante bezüglich $\prod_xd\lambda(t_x)d\nu(r_x)\,d^4b$

$$g=\frac12|d_{s'}d_s|\,|h_{n'}h_n|\sqrt{\frac{2\pi}{\alpha_0}},\qquad
\int g=\frac{a_{s'}a_s}2L_{n'}L_n\sqrt{\frac{2\pi}{\alpha_0}}<\infty.$$

Die Phasen der Staub- und Randwirkung haben Betrag eins. Punktweise konvergiert $F_{C,\epsilon}$ auch bei $r_x=0$. Der Satz von der dominierten Konvergenz erlaubt daher den Grenzwert durch **alle Staubintegrale, die äußeren Skalarintegrale und die endliche Historiensumme**. Insbesondere

$$\boxed{|\mathcal M_{s'n',sn}(\epsilon)|\leq
C_\nu\sqrt{\frac{2\pi}{\alpha_0}}\frac{a_{s'}a_s}2L_{n'}L_n,\qquad\epsilon\geq0.}$$

Für Einheitsbreiten und $\mu=0$ lautet die gesamte entryweise Schrankenmatrix in der primären Reihenfolge

$$|\mathcal M(\epsilon)|_{\rm entry}\leq C_\nu\sqrt{\frac{2\pi}{\beta}}\,ff^T,
\qquad f=(\sqrt{\pi/2},\sqrt2,\sqrt{3\pi/2},\sqrt6)^T.$$

Alle Einträge sind daher höchstens

$$6\sqrt{\frac{\pi\sqrt6}{2}}\,C_\nu\approx11.7692557818\,C_\nu.$$

Das sind Amplitudenschranken, keine Wahrscheinlichkeiten und keine berechneten physikalischen Matrixeinträge. Für größere nichtnegative Masse bleibt die masselose Schranke gültig.

## 6. Quantitative Entfernung des Abel-Regulators

Mit $z=\epsilon+i\alpha$ gilt

$$\partial_\epsilon F=F\left(-\frac1{2z}+\frac{\eta^2}{2z^2}\right),\qquad
|F_\epsilon-F_0|\leq\epsilon\sqrt{\frac{2\pi}{\alpha}}
\left(\frac1{2\alpha}+\frac{\eta^2}{2\alpha^2}\right).$$

Die bezüglich $|h_n|/L_n$ normierten absoluten Paketverteilungen haben Mittelwert null und Kovarianzen $\operatorname{diag}(\sigma_s^2,\sigma_a^2)$ für $n=0$ und $\operatorname{diag}(2\sigma_s^2,\sigma_a^2)$ für $n=1$ in symmetrischen/antisymmetrischen Koordinaten. Für zwei Randpakete ist deshalb $\Sigma\preceq\Lambda I$ mit $\Lambda=\max(2\sigma_s^2,\sigma_a^2)$. Mit Abschnitt 4 folgt $J\Sigma J^T/\alpha^2\leq\Lambda/2$.

Somit gilt mit $B_{s'n',sn}$ als rechter Seite der eingerahmten Majorantenschranke

$$|\mathcal M_{s'n',sn}(\epsilon)-\mathcal M_{s'n',sn}(0)|
\leq\epsilon B_{s'n',sn}\left(\frac1{2\alpha_0}+\frac\Lambda4\right).$$

Bei Einheitsbreiten ist für sämtliche primären Einträge die konservative masselose Schranke

$$|\mathcal M_{ij}(\epsilon)-\mathcal M_{ij}(0)|\leq9.4882118057\,\epsilon C_\nu.$$

Der Dezimalwert ist hier nach oben gerundet. Beispiel: $\epsilon=10^{-4}$ liefert einen absoluten Regulatorfehler kleiner als $9.489\cdot10^{-4}C_\nu$. Geometrie-, Trunkierungs- oder Physikfehler sind darin nicht enthalten.

## 7. Die Dichteintegrale lassen sich vollständig eliminieren

Definiere für feste Uhrdaten

$$\kappa_x(t)=\frac{W}{2\hbar}\left(1+\Gamma_x[T_bt]\right),\qquad
E(k)=\int_0^1e^{-ikr}dr=e^{-ik/2}\operatorname{sinc}(k/2),$$

mit $\operatorname{sinc}z=\sin z/z$, $\operatorname{sinc}0=1$. Es gilt $E(0)=1$ und $|E(k)|\leq1$ für reelles $k$. Der Ausdruck $(1-e^{-ik})/(ik)$ hat bei null eine **hebbare**, keine echte Singularität.

Atom und Positivachse tragen $1/2$ beziehungsweise $E(k)/2$ bei. Nach Multiplikation mit dem jeweiligen Randpaket ergeben sich

$$R_0(u,v)=\frac12,\quad R_M(u,v)=\frac{u+v}{2\sqrt2},\quad
R_D(u,v)=\frac{uv}{2},\quad R_+(u,v)=\frac{u+v+uv}{2\sqrt3}.$$

Hier werden $u=E(\kappa_i)$ und $v=E(\kappa_j)$ eingesetzt. Damit ist **exakt**

$$D_C^{s's}=\frac12\int d\lambda^5(t)\,
R_{s'}(E(\kappa_3),E(\kappa_4))R_s(E(\kappa_0),E(\kappa_1))
\frac{1+E(\kappa_2)}2.$$

Alle 32 Atom/Positivmasken der fünf Punkte sind darin berücksichtigt. Übrig bleibt ein glattes Integral auf einer kompakten Uhrbox. Bei der jetzigen gerichteten Staubwirkung kann $\kappa_x$ negativ oder null sein; die Formel bleibt regulär.

Ein singulärer **Staubuhr-Hessian** erzeugt auf dieser Box keine Determinantenpolstelle: etwa ist $\frac12\int_{-1}^1e^{iat^2/2}dt$ bei $a=0$ gleich eins und für alle reellen $a$ im Betrag höchstens eins. Eine unbeschränkte Fresnel-Determinantenformel darf nicht an seine Stelle gesetzt werden. Der Skalar-Hessian und der Staubuhr-Hessian sind hier unterschiedliche Operatoren.

## 8. Allgemeiner hinreichender Satz bei singulären Innenblöcken

Für mögliche spätere Modelle sei $\theta$ ein Staubparameter auf einem kompakten Träger einschließlich aller Grenzstrata und Atome. Sei $H(\theta)$ eine stetige reelle symmetrische Matrix mit Randblock, Rand-Innenkopplung $J(\theta)$ und Innenblock $A(\theta)$. Sei $\Omega>0$ die feste Gaußpräzision des Randpakets. Setze

$$Q_0(\theta)=\operatorname{diag}(\Omega,0)-iH(\theta),\qquad
Q_\epsilon=Q_0+\epsilon\operatorname{diag}(0,I).$$

Dann ist $Q_0(\theta)$ genau dann invertierbar, wenn

$$\ker A(\theta)\cap\ker J(\theta)^T=\{0\}.$$

Beweis: Aus $Q_0z=0$ folgt durch den Realteil von $z^*Q_0z$, dass die Randkomponente null ist. Für die Innenkomponente verbleiben $Az_I=0$ und $J^Tz_I=0$. Die Umkehrung ist unmittelbar. Das Argument gilt auch für komplexe Nullvektoren, da die reellen Matrizen ihre reellen und imaginären Teile getrennt annihilieren.

Gilt das Kriterium **an jedem Punkt des abgeschlossenen Trägers**, so gibt es durch Stetigkeit und Kompaktheit $\delta=\inf_\theta\sigma_{\min}(Q_0(\theta))>0$. Für $0\leq\epsilon\leq\delta/2$ gilt dann

$$\|Q_\epsilon^{-1}\|\leq2/\delta,\qquad
|\det Q_\epsilon|\geq(\delta/2)^d,$$

mit $d$ als Gesamtdimension. Die vollständig gaußintegrierte Grundpaketamplitude ist ein konstanter Faktor mal $\det(Q_\epsilon)^{-1/2}$ mit durch $\epsilon>0$ fixierter Fortsetzung. Endliche Hermiteanregungen erzeugen nur endlichgradige Wick-Polynome in $Q_\epsilon^{-1}$. Beide Faktoren sind gleichmäßig beschränkt. Bei endlichem Staubmaß und beschränkten Staubpaketen folgt erneut dominierte Konvergenz. Ein singuläres $A$ ist also zulässig, sofern die Randkopplung seine Nullrichtungen überall erfasst.

Wenn das Kriterium nur fast überall oder nur für strikt positive Dichten gilt, liefert es **keine** solche Schranke. Alternativ kann eine lokal integrierbare Singularität ausreichen. Bei transversaler Radialvariable mit Maß $r^{k-1+\gamma}dr$ und Amplitudenbetrag von Ordnung $r^{-p}$ gilt lokale absolute Integrierbarkeit genau für $p<k+\gamma$; Gleichheit ergibt eine logarithmische Divergenz, sofern der führende Betrag nicht verschwindet. Eine obere Schranke beweist die hinreichende Richtung; die notwendige Richtung setzt eine entsprechende untere Abschätzung voraus. Hermite-Polynome können zusätzliche Pole erzeugen. Atombeiträge sind separat auszuwerten und werden von einer a.e.-Aussage nicht erfasst.

## 9. Explizite Gegenproben

Die folgenden reduzierten Zweivariablenmodelle sind **nicht die Wirkung der 33 tatsächlichen AA-Historien**. Sie prüfen genau die mögliche Lücke des punktweisen Kriteriums. Verwende ein gaußgedämpftes Randfeld $y$ mit Präzision eins und ein inneres Feld $x$ mit Regulator $\epsilon$. Nach Division durch den gemeinsamen Gaußfaktor $2\pi$ ist die Amplitude $U_\epsilon=(\det Q_\epsilon)^{-1/2}$.

### 9.1 Singulärer Innenblock mit wirksamer Randkopplung

Für $A=0,J=1$ gilt $\det Q_\epsilon=1+\epsilon$ und $U_\epsilon\to1$. Die innere Singularität allein beweist keine Divergenz.

### 9.2 Stetig integrierbar, am Atom divergent

Für $A=r,J=0$ gilt $U_\epsilon(r)=(\epsilon-ir)^{-1/2}$. Auf $0<r<1$ ist $|U_\epsilon(r)|\leq r^{-1/2}$ und

$$\int_0^1U_\epsilon(r)dr=2i[\sqrt{\epsilon-i}-\sqrt\epsilon]
\longrightarrow2e^{i\pi/4}.$$

Die stetige Dichteintegration existiert. Am Atom $r=0$ ist dagegen $U_\epsilon(0)=\epsilon^{-1/2}$: mit Atomgewicht $1/2$ ist bereits dieser Beitrag divergent. Das Weglassen des Atoms würde das Modell ändern.

### 9.3 Punktweise gültiges Kriterium, logarithmische Gesamtdivergenz

Für $A=0,J=r$ gilt das Nullraumkriterium für jedes $r>0$, jedoch

$$U_\epsilon(r)=\frac1{\sqrt{\epsilon+r^2}},\qquad
\int_0^1U_\epsilon(r)dr=\operatorname{arsinh}(\epsilon^{-1/2})
=\log2-\tfrac12\log\epsilon+o(1).$$

Mit dem tatsächlich verwendeten Mischmaß $\nu$ wird daraus

$$\int U_\epsilon\,d\nu=
\frac1{2\sqrt\epsilon}+\frac12\operatorname{arsinh}(\epsilon^{-1/2}).$$

Die führende Divergenz ist nun $1/(2\sqrt\epsilon)$; zusätzlich bleibt die logarithmische Divergenz des kontinuierlichen Sektors. Alle Faktoren sind positiv, daher kann hier keine oszillatorische Auslöschung die Divergenz beseitigen.

### 9.4 Entfernung der Uhrbox mit Lebesguemaß

Wird allein das innere Uhrmaß durch unnormalisiertes $dT_2$ auf $[-L,L]$ ersetzt, dann ist im Sektor, in dem alle fünf Dichten am Atom sitzen, $S_d=0$. Für eine einzelne Historie mit nichtverschwindendem geradem skalarem Paketbeitrag enthält die Amplitude den Faktor $\int_{-L}^LdT_2=2L\to\infty$. Dieser Sektor hat positive Maßmasse und gehört zum $0\to0$-Eintrag. Das zeigt, weshalb die jetzige Existenz kein Entfernen der Uhrbox rechtfertigt. Eine stattdessen verwendete Normierung $dT_2/(2L)$ ändert das Maß und ist ein anderes Grenzwertproblem.

## 10. Reproduktion und Schlussfolgerung

`python verify.py` prüft 22 algebraische und numerische Kontrollen, die vollständige Datei-Hashliste, die fünf eingefrorenen Git-Blobs und einen bytegleichen Ergebnis-Replay. Die einzelnen Kontrollen umfassen die unabhängige Enumeration und Rekonstruktion aller 33 Hessians, Dichtemasken, L1-Normen und zweite Momente, Innenblocklücke, Abelphase, Majorante, Fehlerrate und die Gegenbeispiele. Numerische Stichproben begleiten die analytischen Beweise; sie ersetzen diese nicht.

Das neue mathematische Ergebnis ist **FINITE_AA_ABEL_EXISTENCE_WITH_COMPACT_DUST_SUPPORTS**. Die zuvor offene gemeinsame Staubintegration und Abel-Entfernung ist unter dem expliziten endlichen Vertrag abgeschlossen. Nicht abgeschlossen sind die Wahl physikalischer Historiengewichte, die Entfernung der Staubstützen, eine unendliche Historiensumme, Renormierung, ein Grenzwert bei festen physikalischen Randzuständen oder die Herleitung einer physikalischen Evolution. Insbesondere folgen keine Unitarität, kein Bounce und keine Singularitätsauflösung.

### Quellen und Herkunft

- Projektbasis: [Main 602e4d5f2ab713ed6825061577cba4f471cd51a5](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/602e4d5f2ab713ed6825061577cba4f471cd51a5). Pfade und Blobwerte: `provenance.json`.
- [PR #278: gerichteter Randvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/278), [PR #279: minimale gemeinsame Wirkung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/279), [PR #280: normierte Randzustände](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/280).
- NIST DLMF [§7.2](https://dlmf.nist.gov/7.2) und [§7.7](https://dlmf.nist.gov/7.7): Hintergrund zu Gauß-/Fehlerfunktionsintegralen. Die modellbezogenen Schranken und Gegenbeispiele werden oben eigenständig hergeleitet.
