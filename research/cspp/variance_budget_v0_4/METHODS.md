# Varianzbudget v0.4: Herleitung und Gültigkeitsbereich

27. Oktober 2026. Neue deterministische Rechnung zum Gauß-Zeugen aus PR #135.
Diese Fassung ist ein eigenständiges Prüfpaket; sie verändert weder den
historischen Versuch noch dessen Gates. Alle Dezimalwerte im Text sind gerundet.

## 1. Festgehaltenes Modell

Wir verwenden den festen Auswertungspunkt 0, einen homogenen Poisson-Prozess
η mit Intensität ρ auf dem kausal konvexen 4D-Minkowski-Diamanten
D_H=I((-H,0),0) und offene Intervalle I_y=I(y,0).
V_y=Vol(I_y), N_y=η(I_y), q=ell_k^(-4)=ερ und a=4 sqrt(q/6).
Das Feld ist deterministisch und wird bei Einfügen eines Punktes nicht verändert.
Für die numerische Untergrenze gilt exakt

\[
\phi(t,\mathbf r)=\exp[-(t^2+r^2)/(2L^2)],\quad L=2,
\qquad \Box\phi(0)=-\tfrac12.
\]

Koordinaten sind Zahlen in der bisherigen Einheit L0. Physikalisch hat ρ die
Einheit L0^-4 und F die Einheit L0^-2. Die angegebenen numerischen Koeffizienten
beziehen sich auf rho_tilde=ρ L0^4 und F_tilde=L0^2 F; die Schreibweise unten
setzt L0=1. Eine dimensionslose Dichteliste ohne diese Festlegung wird nicht benutzt.

Mit c=(1,-9,16,-8,0,...) und w_ε(n)=E[c_K], K~Bin(n,ε), bleibt

\[
F(\eta)=a[-\phi(0)+\epsilon\sum_{y\in\eta}\phi(y)w_\epsilon(N_y)]
\]

unverändert. Es gilt 0<ε≤1, also ρ≥q. Die Varianz ist E|F-EF|².
Endliches Gebiet und beschränktes Feld sichern die benötigte
Quadratintegrierbarkeit und endlichen Differenzmomente.

## 2. Add-one-Antwort, obere und untere Schranke

Für z∈D_H ist die **pfadweise** Antwort

\[
D_zF=a\epsilon\left[\phi(z)w_\epsilon(N_z)
 +\sum_{y\in\eta:\,y\prec z}\phi(y)\Delta w_\epsilon(N_y)\right].
\]

Der zweite Term aktualisiert alle betroffenen Intervalle derselben Wolke.
Er darf nicht durch unabhängiges Schichtrauschen ersetzt werden.
Die Poisson-Poincaré-Schranke und der erste Term der Chaos-Isometrie [1] geben

\[
\rho\int|\mathbb E D_zF|^2 dz
\ \le\ \operatorname{Var}F
\ \le\ \rho\int\mathbb E|D_zF|^2 dz.
\tag{1}
\]

Setze

\[
P(u)=1-9u+8u^2-\tfrac43u^3,\qquad
Q(u)=P'(u)-P(u)=-10+25u-12u^2+\tfrac43u^3,
\]
\[
M_0(u)=e^{-u}P(u),\quad M_1(u)=e^{-u}Q(u).
\]

Poisson-Ausdünnung und die Campbell-Mecke-Formel ergeben

\[
\mathbb E D_zF=\frac{aq}{\rho}h(z),\qquad
h(z)=\phi(z)M_0(qV_z)
 +q\int_{y\prec z}\phi(y)M_1(qV_y)dy.
\tag{2}
\]

Damit ist

\[
\boxed{\operatorname{Var}F\ge\frac{a^2q^2}{\rho}
                 \int_{D_H}|h(z)|^2dz.}
\tag{3}
\]

Die rechte Integralkonstante hängt bei festem q,H,L nicht von ρ ab.
Eine positive Einschränkung dieses Integrals beweist tatsächlich vorhandene
Streuung; eine große Obergrenze allein kann dies nicht. Für komplexe Felder
folgt (1) durch Anwendung auf Real- und Imaginärteil. Die unten ausgewertete
Untergrenze benutzt aber ausschließlich das reale Gauß-Feld.

## 3. Exakte gemeinsame Intervallmomente

Für zwei Punkte y,v definiere O=Vol(I_y∩I_v), u=qV_y, b=qV_v und
γ=ρε²O=qεO. Zwei unabhängige ε-Ausdünnungen derselben Poisson-Punkte liefern
Poisson-Zahlen A,B,C mit Mitteln u-γ,b-γ,γ und K=A+C, J=B+C.
Für endliche Koeffizientenfolgen r,s ist deshalb exakt

\[
\mathcal J(r,s;u,b,\gamma)=e^{-u-b+\gamma}
\sum_{i,j}r_i s_j\sum_{k=0}^{\min(i,j)}
\frac{(u-\gamma)^{i-k}(b-\gamma)^{j-k}\gamma^k}
{(i-k)!(j-k)!k!}.
\tag{4}
\]

Die erzeugende Funktion lautet
exp[u(z-1)+b(w-1)+γ(z-1)(w-1)]. Insbesondere wäre γ=qO falsch:
die gemeinsame Auswahl hat Wahrscheinlichkeit ε², nicht ε.

Zusätzlich sind bei der doppelten Mecke-Formel **Endpunkte einzufügen**.
Mit s_y=1_{v∈I_y}, s_v=1_{y∈I_v} gilt für eine Einfügung
c_i^(1)=(1-ε)c_i+εc_(i+1), sonst c^(0)=c. Die beiden Verschiebungen
sind für verschiedene kausal geordnete Punkte nie gleichzeitig 1.
Das exakte zweite Moment des Summandenpaares ist
J(c^(s_y),c^(s_v);u,b,γ), nicht J(c,c;u,b,γ).

Somit erhält man die exakte Varianzformel

\[
\begin{aligned}
\operatorname{Var}F=a^2\epsilon^2\{&\rho\int|\phi(y)|^2H_c(qV_y;\epsilon)dy\\
&+\rho^2\iint\phi(y)\overline{\phi(v)}
 [\mathcal J(c^{(s_y)},c^{(s_v)};u,b,\gamma)-M_0(u)M_0(b)]dy\,dv\},
\end{aligned}\tag{5}
\]

wobei H_c(u;ε)=J(c,c;u,u,εu). Die Gesamtgröße ist reell;
bei komplexen Feldern kann der Realteil der Doppelintegration genommen werden.
Der Kern (4), einschließlich der Endpunktverschiebung, ist implementiert und
unabhängig geprüft. **Die vollständige räumliche Integration von (5) und eine
allgemeine Berechnung von O für beliebige 4D-Intervalle sind hier nicht erfolgt.**
Die folgenden numerischen Obergrenzen kontrollieren O durch eine bewiesene Hülle.
Wegen wechselnder Vorzeichen der Schichtgewichte wird keine FKG-Monotonie benutzt.

## 4. Obergrenze mit Feldabnahme und wirklichen Gewichtsmomenten

Für eine endliche Folge r gilt die nichtnegative Darstellung

\[
H_r(u;\epsilon)=e^{-(2-\epsilon)u}
\sum_{k\ge0}\frac{(\epsilon u)^k}{k!}
\left[\sum_{j\ge0}r_{j+k}\frac{((1-\epsilon)u)^j}{j!}\right]^2.
\tag{6}
\]

Alle Summen enden nach höchstens vier Gliedern. Mit
d=(-10,25,-24,8) und e=(25,-24,8) ist Δw_ε/ε das geglättete d.
Eine zusätzliche Einfügung hat L²-Norm höchstens
sqrt(H_d)+ε sqrt(H_e). Definiere auf D_H

\[
A=\int|\phi|^2H_c(qV_y;\epsilon)dy,\quad
B=\int|\phi|^2V_yH_d(qV_y;\epsilon)dy,
\]
\[
C=\int|\phi(y)|\sqrt{V_y}
       [\sqrt{H_d(qV_y;\epsilon)}+\epsilon\sqrt{H_e(qV_y;\epsilon)}]dy.
\]

Im Paarterm des zweiten Summanden aus D_zF bleibt zunächst der gemeinsame
Beitrag O_yv=∫1_{z∈I_y}1_{z∈I_v}dz. Cauchy-Schwarz liefert
O_yv≤sqrt(V_y V_v). Cauchy-Schwarz für die Gewichtsmomente und anschließend
die Dreiecksungleichung in L²(dz×P) ergeben

\[
\boxed{\operatorname{Var}F\le\frac{a^2q^2}{\rho}
 [\sqrt A+\sqrt{(q^2/\rho)B+q^2C^2}]^2.}
\tag{7}
\]

Die gemeinsame Geometrie wird also sicher berücksichtigt, jedoch noch nicht
scharf ausintegriert. Die letzten Cauchy-Schwarz-Schritte verlieren Vorzeichen
und mögliche Auslöschungen. Das ist eine bekannte Quelle der verbleibenden Lücke.

Für die Gauß-Hülle werden A,B,C durch Integrale über den ganzen Vergangenheitskegel
majorisiert. Setze c0=sqrt(πq/24), x=sqrt(qV_y)=c0 s v,
s=-t-r, v=-t+r, 0<s<v. Nach Winkelintegration ist

\[
d^4y=\frac{\pi}{2c_0}\frac{(v-x/(c_0v))^2}{v}\,dx\,dv.
\]

Für jedes nichtnegative f und p>0 folgt elementar

\[
\int\phi^p f(qV_y)dy
\le K_p\int_0^\infty f(x^2)dx,
\quad K_p=\frac{\sqrt{24\pi}L^2}{p\sqrt q}.
\tag{8}
\]

Dazu werden (v-s)²/v≤v, exp[-p s²/(4L²)]≤1 und die Erweiterung des
v-Integrals von [sqrt(x/c0),∞) auf [0,∞) verwendet. Das verbleibende Integral
∫v exp[-pv²/(4L²)]dv=2L²/p ist exakt. Es gibt keinen weggelassenen Feldrest.

Wir wählen ε0=2^-20 als Rechenregime, nicht als neue physikalische Annahme.
Für 0≤ε≤ε0 wird (6) nach Potenzen von x integriert, mit

\[
\int_0^\infty x^n e^{-\alpha x^2}dx
=\frac{\Gamma((n+1)/2)}{2\alpha^{(n+1)/2}}.
\]

Arb-Intervalle schließen das ganze ε-Intervall ein. A≤K_2∫H_c(x²;ε)dx,
B≤(K_2/q)∫x²H_d(x²;ε)dx. Für C verwenden wir

\[
R_r(x)=e^{-(1-\epsilon_0/2)x^2}
\sum_{k,j}\frac{\epsilon_0^{k/2}|r_{j+k}|x^{k+2j}}{\sqrt{k!}\,j!},
\quad\sqrt{H_r(x^2;\epsilon)}\le R_r(x),
\]
\[
C\le\frac{K_1}{\sqrt q}\int_0^\infty x[R_d(x)+\epsilon_0 R_e(x)]dx.
\]

Auch diese Integrale sind endliche Gamma-Summen. In (7) ist
q²/ρ≤qε0. Damit entsteht ein expliziter K_U mit Var F≤K_U/ρ für
ρ≥q/ε0. Für ell_k=1/8 ergibt sich K_U≈2.48779596419739×10^17.
Der Großteil dieses Wertes kommt aus der Hülle der gemeinsamen Intervallbeiträge;
er ist keine Schätzung des wirklichen Varianzkoeffizienten.

## 5. Ausgewertete positive Untergrenze ohne räumliche Quadratur

Wir beschränken (3) auf die Rotationsschale

\[
3\le x_z\le3.1,\qquad1.9\le v_z\le2.1.
\tag{9}
\]

Bei q=4096 liegt sie vollständig in D_20. Die Box wurde nach numerischer
Exploration gewählt. Der anschließende Nachweis ist deterministisch; eine
Vorregistrierung oder statistische Bestätigung wird nicht behauptet.

Schreibe s_z=x_z/(c0 v_z) und g=1.9-3.1/(1.9c0)>0.
Für y≺z sind v_y≥v_z, s_y≥s_z und x_y≥x_z notwendig.
Der Anteil der erlaubten Raumwinkel ist

\[
f_\Omega=\min\!\left(1,
\frac{(s_y-s_z)(v_y-v_z)}{(v_y-s_y)(v_z-s_z)}\right).
\]

Mit qπ/(2c0²)=12 und (v_y-s_y)/v_y≤1 erhält man für den Betrag des
indirekten Terms in h(z)

\[
q\left|\int_{y\prec z}\phi(y)M_1(qV_y)dy\right|
\le\frac{12}{v_z-s_z}
\int_{x_z}^\infty e^{-x^2}|Q(x^2)|
 \int_{v_z}^\infty e^{-v^2/(4L^2)}
 (\sqrt x-\sqrt{x_z})^2\,dv\,dx.
\tag{10}
\]

Die zentrale geometrische Ungleichung ist

\[
(x/v-x_z/v_z)(v-v_z)
\le(\sqrt x-\sqrt{x_z})^2
\le\frac{(x-x_z)^2}{4x_z}.
\]

Die erste Hälfte folgt aus AM-GM. Außerhalb der erlaubten Winkel wird der
Integrationsbereich nur mit nichtnegativen Majoranten erweitert.
Da |Q(x²)|≤10+25x²+12x⁴+4x⁶/3, ist auf der ganzen Box (9)

\[
B_*:=\frac{12}{g}\frac{\sqrt\pi L\operatorname{erfc}(1.9/(2L))}{12}
\int_3^\infty(x-3)^2e^{-x^2}(10+25x^2+12x^4+4x^6/3)dx
\]

eine Obergrenze des indirekten Betrags. Das letzte Integral wird über
T_0=√π erfc(3)/2, T_1=exp(-9)/2 und
T_n=[3^(n-1)exp(-9)+(n-1)T_(n-2)]/2 exakt eingeschlossen.

Der direkte Term ist negativ. Weil -P(x²) für x≥3 monoton wächst und
-P(9)=404, hat sein Betrag auf der Box die Untergrenze

\[
D_*=404\exp[-3.1^2-(2.1^2+(3.1/(1.9c_0))^2)/(4L^2)].
\]

Die eingeschlossenen Werte sind D_*≈0.02055768518,
B_*≈0.003631363981. Folglich ist h(z)<0 und
|h(z)|≥D_*-B_*≈0.01692632120 auf der **gesamten** Box.
Ihre Vierervolumen-Untergrenze ist

\[
V_*=(0.1)(0.2)\frac{\pi}{2c_0}\frac{g^2}{2.1}
\approx0.002162538567.
\]

Damit folgt ohne Monte Carlo und ohne ungesicherte Quadratur

\[
\boxed{\operatorname{Var}F\ge\frac{K_L}{\rho},\qquad
K_L=a^2q^2V_*(D_*-B_*)^2\approx113537.046750108.}
\tag{11}
\]

Dies gilt für **jede** zulässige Dichte ρ≥4096. Die Box umfasst nur einen
kleinen Teil der nichtnegativen ersten Chaos-Norm: K_L ist kein nahezu
exakter Varianzkoeffizient. Ein Vergleich von (7) und (11) als gemeinsames
Sandwich setzt zusätzlich das Obergrenzenregime ρ≥4096·2^20 voraus.

## 6. Dichte- und RMS-Budgets

Für den bisherigen stochastischen Anteil von 7 % ist σ=0.07·|Box φ|=0.035.
(11) verlangt ρ≥9.2683303469×10^7. Mit Vol(D_20)=π20⁴/24 folgt

\[
\mathbb EN\ge1.9411545686\times10^{12}\quad\text{(notwendig)}.
\]

(7) garantiert diesen stochastischen Anteil bei
ρ=203085384832439981150 und E N≈4.2534103536×10^24 Punkten.
Das ist ein konstruktiv angegebenes hinreichendes Budget, kein Minimum.
Das frühere Budget E N≈2.8744689174×10^39 ist damit um den Faktor
6.758×10^14 reduziert. Der notwendige Wert und der hinreichende Wert
lassen weiterhin mehr als zwölf Größenordnungen offen.

Aus der unveränderten Bias-Einschließung b_rel≈0.03956397744 und der
Randgrenze δ_rel≈0.00008006188 folgt für **10 % gesamten RMS** bereits

\[
\rho\ge\frac{K_L}{0.05^2-[0.5(b_{rel}-\delta_{rel})]^2}
\approx5.3802522069\times10^7,
\quad \mathbb EN\ge1.1268373872\times10^{12}.
\]

Dies ist ein separater notwendiger Test, der die 7-%-Teilallokation nicht
voraussetzt. Erwartungswertfehler und Varianz werden durch
E|F-Box φ|²=Var F+|EF-Box φ|² verbunden. Bias und Randfehler werden nicht
als unabhängige Zufallsfehler quadratisch addiert.

Die stochastische Obergrenze gilt für eine einzelne Poisson-Realisierung.
Für das Mittel aus R unabhängigen Realisierungen wird die Varianz durch R
geteilt; bei festem q,H wird dafür die entsprechende notwendige Schranke
an Rρ gestellt. Gleichzeitige Proben aus derselben Wolke sind nicht solche
unabhängigen Wiederholungen. Die Kosten pro Operatorauswertung und die
kausale Paararbeit werden durch diese Punktbudgets nicht modelliert.

## 7. Numerische Prüfung und offene Grenzen

Alle berichteten Budgetentscheidungen verwenden Arb mit 128 Bit und einen
vollständigen Replay bei 192 Bit. Es gibt keine numerische räumliche Quadratur
in den zertifizierenden Berechnungen. Die acht SciPy-Integrale im Audit sind
unabhängige Plausibilitätsprüfungen der Gamma-Summen und keine Fehlerzertifikate.

Der Audit enthält 253 exakte rationale Identitätsprüfungen einschließlich
der pfadweisen Intervallaktualisierung, 36 direkte Poisson-Summenvergleiche
für den gemeinsamen Kern sowie Negativkontrollen für ausgelassene Überlappung
und ausgelassene Endpunkteinfügung. Alle sieben oberen Budgets, die untere
Boxrechnung und die Gateentscheidungen werden wiederholt. Einzelheiten und
Laufzeitversionen stehen in den JSON-Dateien. Ein Replay testet die Software;
die mathematische Begründung sind die obigen Ungleichungen.

Die frühe 4D-Gaußquadratur der gesamten ersten Chaos-Norm zeigte noch sichtbare
Auflösungsabhängigkeit. Ihre Zahlen werden für keine notwendige Dichte, keine
Gateentscheidung und keine hier berichtete Schranke verwendet.

Offen bleiben: die scharfe räumliche Integration der gemeinsamen Intervalle,
eine umfassendere eingeschlossene Chaos-Untergrenze, die Übertragung auf andere
Felder/Quellen und gekrümmte Raumzeiten, Gleitkomma-Kausaltests und die numerische
Auswertung einer riesigen diskreten Summe. G1 bleibt HOLD, G2/G3 NOT_RUN.
Das Resultat ist weder eine Aussage über Dirac-/Flavor-Propagation noch ein
allgemeiner Unmöglichkeitssatz für andere Operatoren, Domänen oder Varianzreduktion.
Externe unabhängige Reproduktion und Peer-Review stehen aus.

## Primärquellen und Provenienz

1. G. Last, M. D. Penrose, *Poisson process Fock space representation, chaos
   expansion and covariance inequalities*, [arXiv:0909.3205](https://arxiv.org/pdf/0909.3205),
   Theorem 1.1 und Gleichung (1.8). Diese liefern die allgemeinen Werkzeuge in
   (1); die BD-Kerne, Hüllen und die Box-Untergrenze wurden hier hergeleitet.
2. D. M. T. Benincasa, F. Dowker, *The Scalar Curvature of a Causal Set*,
   [arXiv:1001.2725](https://arxiv.org/pdf/1001.2725). Herkunft der geglätteten
   4D-Schichtgewichte; Normierung und endlicher Modellumfang bleiben die des Projekts.
3. [Projekt-PR #135](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/135),
   Merge-Commit 3a200404a23d79bde852b29a49f56c809fb68af4.
   Der aktuelle BUDGET-Snapshot wurde über GitHub gelesen und gegen dessen
   Git-Blob-ID 5736cc122205a6bf694163dfc0a5792c138369f9 geprüft.
   Er enthält die übernommenen Bias- und Rand-Einschließungen, deren Beweis
   dieses Paket nicht erneut ausführt. Die lokalen Snapshot-SHA256 stehen in den Ergebnissen.
4. [python-flint, Arb-Dokumentation](https://python-flint.readthedocs.io/en/latest/arb.html).
   Ausgeführt: python-flint 0.8.0; keine Übernahme einer neueren Versionsgarantie.
