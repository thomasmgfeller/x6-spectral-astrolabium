# CSPP v0.3: mathematischer Umfang der Einschließungen

## 1. Modell und Bedeutung der Aussagen

Betrachtet wird der ideale geglättete 4D-BD-Operator in flacher Raumzeit,
mit einem **festen** Auswertungspunkt 0 und einem homogenen Poisson-Prozess
der Intensität ρ auf D_H=I((-H,0),(0,0)). Alle Größen verwenden dieselbe
Längeneinheit L0 wie v0.2. Es gelten q=ℓk⁻⁴=ερ, 0<ε≤1 und
a=4√(q/6). Die Aussagen betreffen exakte reelle Geometrie und Arithmetik
des mathematischen Modells. Sie enthalten noch keinen Fehlernachweis für
PRNG, Gleitkomma-Kausaltests oder eine endliche numerische Operatorauswertung.

Die hier eingeschlossenen Größen sind: ein nichtoszillierender Gauß-Zeuge,
eine allgemeine konservative Varianzobergrenze, die Normierung der bestehenden
kompakten Quelle und 34 ausgewählte Kontinuumsamplituden. Die E4-Felder,
Detektorintegration und Dirac-Qualifikation werden dadurch nicht ersetzt.

## 2. Eine korrelationsverträgliche Varianzobergrenze

Schreibe c=(1,−9,16,−8,0,0,…) und
wε(n)=E[c_K] für K~Binomial(n,ε). Das ist exakt die in v0.1 verwendete
geglättete Schichtgewichtung, einschließlich ε=1. Die Binomialkopplung ergibt

\[
|w_\epsilon(n)|\le16,\qquad
w_\epsilon(n+1)-w_\epsilon(n)
=\epsilon\,\mathbb E[c_{K+1}-c_K],\qquad
|\Delta w_\epsilon(n)|\le25\epsilon.
\]

Der Wert 25 ist tatsächlich erreichbar: ε=1, n=1.
Für ein deterministisches komplexes Feld |φ|≤1 sei

\[
F(C)=a\left[-\phi(0)+\epsilon\sum_{y\in C}\phi(y)
w_\epsilon(N(y,0))\right].
\]

Ein neuer Punkt z liefert sowohl seinen eigenen Summanden als auch eine
Zähländerung in **allen** Intervallen mit y≺z≺0. Daher gilt pfadweise

\[
|D_zF|\le a\epsilon(16+25\epsilon N_z^-),
\quad N_z^-=\#(C\cap I((-H,0),z)).
\]

Hier wird keine Unabhängigkeit überlappender Intervalle behauptet. Die
Poisson-Poincaré-Ungleichung [1], getrennt auf Real- und Imaginärteil angewandt,
liefert Var_C(F):=E|F−EF|²≤ρ∫E|D_zF|² dz. Da N_z^- eine Poisson-Zahl mit
Mittelwert ρV_z ist, gilt E(N_z^-)²=ρV_z+ρ²V_z².

Mit V=πH⁴/24 und kausal konvexem D_H erhält man exakt

\[
\int_{D_H}V_z^j\,dz
=V^{j+1}\frac{24}{(2j+1)(2j+2)(2j+3)(4j+4)}.
\]

Für j=0,1,2 sind die Faktoren 1,1/20,1/105. Zur Herleitung setzt man
V_z=πs²v²/24 und verwendet d⁴z=(π/2)(v−s)²dsdv auf 0<s<v<H.
Integration des Polynoms ergibt die angegebene rationale Formel. Somit

\[
\boxed{\operatorname{Var}_C F\le\frac{8q^3}{3\rho}
\left[256V+40qV^2+\frac{125q^2V^2}{4\rho}
+\frac{125q^2V^3}{21}\right].}
\]

Alle Voraussetzungen der Varianzabschätzung sind erfüllt: ein endliches
Gebiet, beschränktes Feld, |F|≤a(1+16εN) und endliche Poisson-Momente.
Insbesondere ist F quadratintegrierbar. Mit ρ≥q kann der eckige Ausdruck
durch 256V+(285/4)qV²+(125/21)q²V³ ersetzt werden. Das ergibt eine explizite
**hinreichende** Dichte für eine gewünschte Standardabweichung. Diese
Hüllschranke ist sehr locker; ihre Größe beweist keinen notwendigen Aufwand
und keine Unmöglichkeit genauerer Verfahren. Ihr 1/ρ-Verhalten gilt bei
**festem q und H**. Ein gemeinsamer Grenzübergang ℓk→0 oder H→∞ folgt nicht
ohne Kontrolle der stark wachsenden Konstanten.

## 3. Eingeschlossener Gauß-Erwartungswert

Hier wird ausschließlich φ=exp[−(t²+r²)/(2L²)] mit L=2 betrachtet, also
ω=k=0. Am Ursprung ist □φ=−2/L²=−1/2. Aus dem Erwartungswert von v0.2 folgt
mit c0=√(πq/24), P(z)=1−9z+8z²−4z³/3:

\[
\mu_\infty=a\left[-1+12\int_0^\infty yP(y^2)e^{-y^2}
\left\{K_1\!\left(\frac{y}{2c_0L^2}\right)
-K_0\!\left(\frac{y}{2c_0L^2}\right)\right\}dy\right].
\]

Die Reduktion entsteht aus b=y/c0 und der Bessel-Integralidentität [2]:

\[
\int_{\sqrt b}^\infty\frac{(v-b/v)^2}{v}
e^{-(v^2+b^2/v^2)/(4L^2)}dv
=b[K_1(b/(2L^2))-K_0(b/(2L^2))].
\]

Mit w=v² wird das linke Integral zu einer Kombination von Integralen
über w∈[b,∞). Die Substitution w↦b²/w ergänzt diese auf (0,∞).
Die Standardidentität ∫₀∞w^(ν−1)e^(−βw−γ/w)dw
=2(γ/β)^(ν/2)Kν(2√βγ) ergibt das Resultat. Eine zweite direkte
Intervallintegration in v prüft sechs Fälle mit separat begrenztem Rest.

Der Kern wird zwischen δ=2⁻⁶⁴ und Y=8 durch FLINT integriert. Die analytische
Fortsetzbarkeit des K-Kerns wird nur auf Bällen mit positivem Realteil
zugelassen; ungeeignete Bälle liefern einen nichtendlichen Wert und erzwingen
Unterteilung. Die ausgelassenen Enden werden durch

\[
E_{<\delta}\le8\sqrt\pi qL^2\delta
(1+9\delta^2+8\delta^4+4\delta^6/3),
\]

\[
E_{>Y}\le8\sqrt\pi qL^2\int_Y^\infty e^{-y^2}
(1+9y^2+8y^4+4y^6/3)dy
\]

eingeschlossen. Der obere Rest wird aus erfc und der exakten Rekursion
T_j=Y^(2j−1)e^(−Y²)/2+(2j−1)T_(j−1)/2 berechnet.
Der endliche Rand hat weiterhin die analytische Schranke
E_H≤56πqL²exp[−H²/(4L²)], jetzt ebenfalls mit gerichteter Einschließung.
H wird als erster Wert der festgelegten Liste gewählt, für den E_H/|□φ|≤0,01
bewiesen ist. Das ist eine konservative Designentscheidung, kein minimales H.

Für das gemeinsame Budget wird **nur die echte stochastische Varianz**
quadratisch addiert:

\[
\mathbb E|F-\Box\phi|^2
=\operatorname{Var}F+|\mu_H-\Box\phi|^2,
\quad |\mu_H-\Box\phi|\le|\mu_\infty-\Box\phi|+E_H.
\]

Umgekehrt ist |μ∞−□φ|−E_H eine Untergrenze für den Betrag des endlichen Bias,
sofern positiv. Überschreitet diese relative Untergrenze 0,1, ist das
10%-RMS-Ziel für **diesen Zeugen, dieses ℓk und dieses H** bei jeder
zulässigen Dichte ausgeschlossen. Eine andere Randbehandlung, andere Felder
oder andere Operatoren werden davon nicht ausgeschlossen.

## 4. Abgesicherter Teil der kompakten Quellenreferenz

Die Quelle bleibt f=A exp[−1/h]exp(4iz), h=1−r²/a0²>0, a0=1/2,
sonst f=0; Anfangszeit −1 und Anfangsgeschwindigkeit null bleiben unverändert.
Zunächst wird I=4π∫₀^a0 r²exp(−2/h)dr eingeschlossen und A=I⁻¹ᐟ² berechnet.
Für den abgeschnittenen Bereich 0<h≤hc=1/64 gilt

\[
0\le I_{\rm tail}\le\frac{4\pi a_0^3}{3}e^{-2/h_c}.
\]

Die masselose Lösung K=∂τ(τMτf) wird an **allen 28 unveränderten Proben**
eingeschlossen. Im Winkelintegral wird nur h≥hc numerisch integriert.
Für den Rest folgt direkt vor der Azimutintegration, mit R=|x| und τ=|t+1|,

\[
|K_{\rm tail}|\le A e^{-1/h_c}
\left(1+4\tau+\frac{2\tau(\tau+R)}{a_0^2h_c^2}\right).
\]

Hier werden |n_z|≤1 und die Monotonie von e^(−1/h)/h² für h≤1/2 verwendet.
Huygens-Nullfälle außerhalb des Kugelschalen-Supports werden exakt behandelt.
Die Besselprodukte sind als ganze Funktionen ausgewertet:
J0(√w)=0F1(1;−w/4) und √w J1(√w)=w 0F1(2;−w/4)/2.
Es gibt damit keinen künstlichen Wurzelzweig am Winkelendpunkt.

Für m=1,2 werden zusätzlich die **drei Zentrumsproben** eingeschlossen.
Dort ist Mrf=A exp(−1/h)sinc(4r), also nur ein Radialintegral nötig. In der
unveränderten KG-Cauchyformel von v0.2 wird

\[
\frac{J_2(m\sqrt{s^2})}{s^2}
=\frac{m^2}{8}\,{}_0F_1(3;-m^2s^2/4)
\]

verwendet. Aus |J2(z)|≤z²/8 für reelles z [3] folgt für den ausgelassenen
massiven Volumenbeitrag die Schranke m⁴τAa0³exp(−1/hc)/24.
Der negative Oberflächenterm −m²τ²Mτf/2 bleibt enthalten.
27 exakte KG-Ebenenwellen und sechs falsche-Vorzeichen-Kontrollen prüfen dies.

**Die massiven Werte außerhalb des Zentrums sind noch nicht eingeschlossen.**
Die zertifizierten lokalen Werte sind keine globale Lösungsnorm und keine
Detektor-Dichtematrix. Die Referenz bleibt insgesamt HOLD.

## 5. Maschinenrechnung, Replay und Gültigkeitsgrenzen

Verwendet werden python-flint 0.8.0 / FLINT 3.3.1 mit 128 Bit. Die
Integrationsbibliothek liefert einschließende Bälle, nicht bloß eine
Auflösungsdifferenz; ihr analytischer Callback-Vertrag wird beachtet [4].
Die expliziten Restschranken werden auf die resultierenden Bälle addiert.
Ein komplexer Absolutfehler wird konservativ durch einen Rechteckfehler
abgedeckt. Alle Entscheidungen verwenden Bälle. Dezimale Mittelpunktfelder
sind ausschließlich Anzeige; die gespeicherten Ball-Strings werden auf
Erhaltung der ursprünglichen Einschließung geprüft.

Ein kompletter Replay mit 160 Bit wiederholt alle sieben Budgetzeilen und
34 Amplituden. Überlappung verschiedener Einschließungen ist eine
Regressionsprüfung; die Begründung der Einschließung stammt aus der Formel,
den Restschranken und der Ballarithmetik. Für frei gewählte **Obergrenzen**
aus Intervallendpunkten ist Überlappung keine notwendige Bedingung. Die erste
Auditfassung verlangte dies fälschlich. [Amendment 01](amendment_01/RECORD.json)
bewahrt die Originalfassung und protokolliert die Korrektur allein dieser
Prüfregel; Produktion, Parameter, Schwellen und Ergebnisdateien blieben
byteidentisch. Der korrigierte Audit prüft die hinreichende Ungleichung und
unveränderte Entscheidungen. Ein unsicherer Vergleich bleibt HOLD.

Diese Implementierung ist ein reproduzierbarer, begrenzter numerischer
Nachweis unter den dokumentierten Formeln und FLINT-Annahmen; sie ist weder
externes Peer-Review noch eine formalisierte Verifikation der Bibliothek.

## Primärquellen

1. Last, Penrose: *Poisson process Fock space representation, chaos expansion
   and covariance inequalities*, [arXiv:0909.3205](https://arxiv.org/pdf/0909.3205),
   Gleichung (1.8). Übernommen wird die Poisson-Poincaré-Ungleichung; die
   BD-spezifische Hülle und ihre Konstanten werden oben hergeleitet.
2. NIST DLMF, [§10.32.10](https://dlmf.nist.gov/10.32#E10),
   Integralrepräsentation von Kν. Die Gauß-Reduktion ist die angegebene
   Anwendung mit positiven Parametern.
3. NIST DLMF, [§10.14.4](https://dlmf.nist.gov/10.14#E4),
   Bessel-Schranke, hier ν=2 und reelles Argument.
4. python-flint, [acb.integral](https://python-flint.readthedocs.io/en/latest/acb.html#flint.acb.integral),
   Ballarithmetik und analytischer Callback-Vertrag. Ausgeführt wird die
   festgehaltene Version 0.8.0; deren Laufzeit-Dokumentation wurde ebenfalls geprüft.
5. Für den BD-Erwartungswert und die KG-Cauchyformel gelten unverändert die
   [Primärquellen und Herleitungen aus v0.2](../scale_calibration_v0_2/METHODS.md).
