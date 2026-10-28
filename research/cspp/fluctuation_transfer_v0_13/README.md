# Prädiktiver Fluktuationstransfer v0.13

**Status:** überprüfbare gemeinsame Momentenrechnung und vollständige
Vorhersagen für zwei deklarierte Kontrollmodelle; zusätzliche rigorose
Momentenschranken für den ursprünglichen lokalen H1-Detektor.
**Die vollständigen Ensemble-Mittelwerte und -Kovarianzen des ursprünglichen
kompakten Detektors sind noch nicht numerisch ausgewertet. METHOD_HOLD und
G1 HOLD bleiben bestehen.**

Die Konstruktion verwendet keine aus den acht Archivwolken geschätzte
Kovarianz, kein angepasstes Dichtegesetz und keine neuen Zufallszahlen.
Das Ziel ist das gemeinsame Poisson-Ensemble derselben Wolke, nicht ein
zusätzliches Messrauschen und nicht eine quantenphysikalische Dekohärenz.
Die Ergebnisse und ihre genaue Reichweite stehen in [RESULTS.md](RESULTS.md).

## 1. Gemeinsamer Wahrscheinlichkeitsraum und Detektor

Es gilt weiterhin ein homogener Poisson-Prozess \(\eta\) auf
\(\Omega_4=\{(t,\mathbf x):|t|+|\mathbf x|<4\}\),
\(\rho=3/\pi\), \(\mathbb EN=512\), \(\epsilon=1/16\), \(m=1\).
Die deterministischen Funktionen \(f,g\) werden nicht verändert. Zufällig
sind ihre Abbildung auf die Wolke, die Intervallzählwerte, die retardierte
Inverse und gegebenenfalls die Detektorkoeffizienten.

Für eine vollständige Konfiguration ist der bisherige Detektor

\[
 A_r(\eta)=\int W_r(p)u_\eta(p)\,d^4p,
 \qquad W_r=\frac{1_{I_r\times D}}{|I_r||D|},
\]

mit \(D=B((0,0,3/2),1/2)\), \(I_1=[3/4,1]\),
\(I_2=[1,5/4]\). Die beiden Fenster benutzen dieselbe Konfiguration.
Definiere den Mittelwert, die Hermitesche Kovarianz und die Relationsmatrix
(auch Pseudokovarianz genannt):

\[
 \mu_r=\mathbb EA_r,\quad
 \Sigma_{rs}=\mathbb E[(A_r-\mu_r)\overline{(A_s-\mu_s)}],\quad
 \Pi_{rs}=\mathbb E[(A_r-\mu_r)(A_s-\mu_s)].
\]

Für komplexe Felder ist \(\Pi=0\) keine automatische Eigenschaft.
Beide Matrizen zusammen bestimmen die Kovarianz von Real- und Imaginärteilen.
In der Reihenfolge \((\Re A,\Im A)\) ist diese reelle Matrix

\[
 \frac12\begin{pmatrix}
 \Re(\Sigma+\Pi)&\Im(\Pi-\Sigma)\\
 \Im(\Pi+\Sigma)&\Re(\Sigma-\Pi)
 \end{pmatrix}.
\]

Bei existierenden zweiten Momenten gilt für den vollständigen Detektor

\[
 \Sigma_{rs}=\iint W_r(p)W_s(q)
       \operatorname{Cov}_*(u_\eta(p),u_\eta(q))\,d^4p\,d^4q.
\]

Es werden also verschiedene Orte **und** Zeiten gemeinsam integriert.
Ein Weißrauschansatz mit räumlicher oder zeitlicher Deltafunktion wird
nicht unterstellt. Auch raumartig getrennte Beobachtungen können eine
korrelierte gemeinsame Vergangenheit besitzen.

## 2. Gemeinsame kausale Intervalle: alle benötigten Momente

Für offene Intervalle \(J_e=I(y_e,x_e)\) setze \(N_e=\eta(J_e)\) und

\[
 w_\epsilon(n)=\sum_{k=0}^3c_k\binom nk\epsilon^k(1-\epsilon)^{n-k},
 \qquad c=(1,-9,16,-8).
\]

Zerlege die Vereinigung aller Intervalle in disjunkte Atome

\[
 B_S=\bigcap_{e\in S}J_e\setminus\bigcup_{e\notin S}J_e,
 \qquad \lambda_S=\rho|B_S|,\quad S\ne\varnothing.
\]

Ihre Zählwerte sind unabhängig Poisson-verteilt. Die Intervallzählwerte
selbst sind es im Allgemeinen nicht. Insbesondere
\(\operatorname{Cov}(N_e,N_f)=\rho|J_e\cap J_f|\).
Für Produkte der geglätteten Gewichte werden pro Faktor unabhängige
Hilfs-Ausdünnungsmarken auf **dieselben** Poisson-Punkte gesetzt. Dann ist

\[
 G(z_1,\ldots,z_p)=\exp\!\left\{
 \sum_{S\ne\varnothing}\lambda_S
 \left[\prod_{e\in S}(1-\epsilon+\epsilon z_e)-1\right]\right\}.
 \tag{1}
\]

Wiederholte Faktoren desselben Intervalls erhalten eigene Marken und eigene
Variablen; der gemeinsame Grundprozess bleibt erhalten. Für zwei Faktoren
ist der gemeinsame ausgedünnte Poisson-Mittelwert
\(\rho\epsilon^2|J_1\cap J_2|\), nicht
\(\rho\epsilon|J_1\cap J_2|\).

Sind durch eine Mecke-Einfügung bereits \(s_e\) feste Punkte im offenen
Intervall enthalten, wird die endliche Folge verschoben:

\[
 c^{[s_e]}=((1-\epsilon)\operatorname{Id}+\epsilon E)^{s_e}c,
 \qquad (Ec)_k=c_{k+1}.
\]

Daraus folgt die **exakte endliche** Momentenformel

\[
 \mathbb E\prod_{e=1}^p w_\epsilon(N_e+s_e)
 =\sum_{k_1,\ldots,k_p=0}^3
       \left(\prod_e c^{[s_e]}_{k_e}\right)
       [z_1^{k_1}\cdots z_p^{k_p}]G(z).
 \tag{2}
\]

Sie enthält gemeinsame Intervalle jeder Ordnung, mehrfach verwendete
Kanten und sämtliche Endpunkteinfügungen. Es wird keine Gauß-Schließung
benutzt. Paarweise Kovarianzen allein bestimmen die höheren Produkte einer
zufälligen Inversen nicht.

`kernel.py` extrahiert die Koeffizienten von (1) mit Arb. Schreibe
\(\log G=g_0+\sum_{S\ne\varnothing}g_Sz_S\), \(G=\sum_nF_nz^n\).
Für jedes \(j\) mit \(n_j>0\) gilt

\[
 F_0=e^{g_0},\qquad n_jF_n=\sum_{S\ni j,\,1_S\le n}g_SF_{n-1_S}.
\]

Dies benötigt keine abgeschnittene Poisson-Summe. Der Aufwand wächst mit
der Zahl der Faktoren, nicht mit der unbeschränkten möglichen Punktzahl.
Große Pfadfamilien bleiben dennoch rechnerisch aufwendig.

### Zwei-Punkt-Kovarianz des Operators

Für ein deterministisches Testfeld \(\phi\) und passive Beobachtungen
\(x,x'\), die nicht in die Wolke eingefügt werden, sei

\[
 F_x=a\left[-\phi(x)+\epsilon\sum_{y\in\eta\cap P_x}
                   \phi(y)w_\epsilon(N_{yx})\right],
 \quad P_x=\Omega_4\cap J^-(x),\quad a=4\sqrt{\epsilon\rho/6}.
\]

Mit \(M(u)=e^{-u}(1-9u+8u^2-4u^3/3)\),
\(u_{yx}=\epsilon\rho|I(y,x)|\) und dem gemeinsamen Gewichtsmoment
\(J_{s,t}(y,x;v,x')\) aus (2) liefert Mecke:

\[
\begin{aligned}
 \operatorname{Cov}_*(F_x,F_{x'})=a^2\epsilon^2\bigg\{&
 \rho\int_{P_x\cap P_{x'}}|\phi(y)|^2J_{0,0}(y,x;y,x')\,dy\\
 &+\rho^2\int_{P_x}\int_{P_{x'}}\phi(y)\overline{\phi(v)}
 \left[J_{s,t}(y,x;v,x')-M(u_{yx})M(u_{vx'})\right]dv\,dy\bigg\},
\end{aligned}\tag{3}
\]

wobei \(s=1_{v\in I(y,x)}\), \(t=1_{y\in I(v,x')}\).
Der erste Term ist der identische Summationspunkt beider Summen; er darf
nicht ausgelassen werden. Im zweiten Term werden die **unverschobenen**
Einzelmittel abgezogen, nicht die Palm-verschobenen Einzelmittel.
`mecke_connected_pair` hält diese Unterscheidung ausdrücklich fest.
Bei aktiven, selbst gesprinkelten Beobachtungspunkten sind auch deren
Palm-Einfügungen zu berücksichtigen. (3) gilt nicht unverändert, wenn das
Testfeld selbst von \(\eta\) abhängt.

### Geometrische Kontrolle

`geometry.py` schließt Überlappungsvolumina beliebiger strikt zeitartiger
4D-Intervalle durch rationale Boxentscheidungen ein. Unaufgelöste Randboxen
liefern das ganze Intervall zwischen null und ihrem Volumen. Die Breite
bleibt sichtbar; Mittelpunktproben erzeugen kein Zertifikat.

Für die Kontrollrechnung werden zwei vertikale Intervalle mit verschiedenem
Raumzentrum benutzt. Auf jedem Zeitschnitt sind ihre Querschnitte Kugeln.
Für Radien \(r_1,r_2\) und Abstand \(d\) lautet das partielle Linsenvolumen

\[
 V_{\rm lens}=\frac{\pi(r_1+r_2-d)^2
 [d^2+2d(r_1+r_2)-3(r_1-r_2)^2]}{12d}.
\]

Außerhalb ist es null, bei Einschluss das kleinere Kugelvolumen.
Die Radien sind abschnittsweise affin in der Zeit; sämtliche Umschaltpunkte
und Zeitintegrale werden exakt rational berechnet. Diese Spezialrechnung
hat keinen geometrischen Quadraturrest. Allgemeine Pfadatom-Volumina sind
mit diesen Spezialfällen nicht bereits vollständig ausgewertet.

## 3. Retardierter Transfer mit zufälliger Inverser und Anfangsdaten

Für eine gemeinsame feste Zustandsdarstellung schreibe

\[
 v=K_\eta v+b_\eta,\quad R_\eta=(I-K_\eta)^{-1},\quad
 A=Q_\eta R_\eta b_\eta.
 \tag{4}
\]

History-Knoten können als erste Zustände mit Nullzeilen von \(K\) aufgenommen
werden; \(b\) trägt dann die History. So werden Produkte zwischen
Anfangsdatenkopplung und History nicht vorschnell gemittelt.
Bei endlichen kausal sortierten Zuständen ist \(K\) strikt unterdreieckig:
\(R=I+K+\cdots+K^{n-1}\). Die Inverse existiert ohne Kleinheitsannahme.

Die exakten Momente sind

\[
 \mu=\mathbb E[QRb],\qquad
 \Sigma=\mathbb E[QRbb^*R^*Q^*]-\mu\mu^*,\qquad
 \Pi=\mathbb E[QRbb^TR^TQ^T]-\mu\mu^T.
\]

Im Allgemeinen sind weder \(\mathbb ER=(I-\mathbb EK)^{-1}\) noch
\(\mathbb E[Kh]=(\mathbb EK)(\mathbb Eh)\) zulässig.
Der fehlende Term im zweiten Ausdruck ist \(\mathbb E[\delta K\delta h]\);
bei komplexen Daten ist dies ein unkonjugiertes gemischtes Moment.
Die physikalischen \(f,g\) können dabei vollständig deterministisch bleiben:
\(h=H_\eta(f,g)\) hängt über den Adapter von der gemeinsamen Geometrie ab.

### Lineare Vorhersage und Mittelwertverschiebung

Setze \(K_0=\mathbb EK\), \(b_0=\mathbb Eb\), \(Q_0=\mathbb EQ\),
\(R_0=(I-K_0)^{-1}\), \(v_0=R_0b_0\), \(A_0=Q_0v_0\). Dann

\[
 v_1=R_0(\delta b+\delta K v_0),\quad
 v_{j+1}=R_0\delta K v_j,
\]
\[
 A_1=Q_0v_1+\delta Qv_0,\qquad
 A_j=Q_0v_j+\delta Qv_{j-1}\quad(j\ge2).
 \tag{5}
\]

Die Summe endet im endlichen Dreiecksproblem exakt. Insbesondere
\(\mathbb EA_1=0\), aber

\[
 \mu-A_0=\mathbb EA_2+\mathbb EA_3+\cdots
\]

kann ungleich null sein. Schon \(A_2\) enthält Operator-Anfangsdaten-,
Operator-Operator- und Detektor-Zustandskorrelationen. Für den linearisierten
Blockvektor \(z=(\delta b,\operatorname{vec}\delta K,
\operatorname{vec}\delta Q)\) ist \(A_1=Jz\). Nur bei Verwendung des
**gesamten** gemeinsamen Blocks gilt

\[
 \Sigma^{(1)}=J\operatorname{Cov}_*(z)J^*,\qquad
 \Pi^{(1)}=J\operatorname{Cov}_T(z)J^T.
\]

Das Weglassen der Anfangsdatenkreuzblöcke ist eine andere Vorhersage,
keine äquivalente Schreibweise.

### Belastbare Restfortpflanzung

Schreibe \(A=A^{\rm lin}+E\),
\(\delta_r\ge\|E_r\|_{L^2(\mathbb P)}\),
\(s_r^2=\operatorname{Var}_*(A_r^{\rm lin})\). Cauchy-Schwarz liefert

\[
 |\mu_r-\mu_r^{\rm lin}|\le\delta_r,
\]
\[
 |\Sigma_{rs}-\Sigma_{rs}^{\rm lin}|,
 |\Pi_{rs}-\Pi_{rs}^{\rm lin}|
 \le s_r\delta_s+s_s\delta_r+\delta_r\delta_s.
 \tag{6}
\]

Für die endliche Kontrolle werden die ausgelassenen Polynome exakt
berechnet und ihre \(L^2\)-Normen mit (2) eingeschlossen. Es wird kein
unbegründetes \(O(\delta K^2)\) als numerische Fehlergrenze verwendet.
Die gleiche Abschätzung überträgt zertifizierte Integrations- oder
Lösungsfehler auf Momente, sobald ihre Ensemble-\(L^2\)-Grenzen vorliegen.
Die acht einzelnen Fehlerintervalle von v0.12 sind hierfür allein kein
Ensemblezertifikat. Deterministische Referenzunsicherheit ist kein
zusätzlicher stochastischer Varianzterm.

## 4. Unterschiedlich große Wolken: vollständige Poisson-Funktionale

Matrizen verschieden großer Wolken werden nicht elementweise gemittelt.
Gemeinsame Zielgrößen sind stattdessen die festen Detektorfunktionale
\(A_r(\eta)\). Mit dem Einfügedifferenzoperator
\(D_zA(\eta)=A(\eta+\delta_z)-A(\eta)\) gilt bei Quadratintegrierbarkeit

\[
 \Sigma_{rs}=\sum_{n\ge1}\frac{\rho^n}{n!}
 \int T_{n,r}(z)\overline{T_{n,s}(z)}\,d^{4n}z,
 \quad T_{n,r}=\mathbb E D_{z_1}\cdots D_{z_n}A_r.
 \tag{7}
\]

Ohne Konjugation folgt die Relationsmatrix. Dies ist die Poisson-Chaos-
Identität von Last und Penrose [1], auf die gemeinsamen Detektorfunktionale
angewandt. Jede Einfügung aktualisiert sämtliche betroffenen Intervalle,
den Anfangsdatenadapter, die retardierte Lösung und den Detektor.
Nur ein lokales Operatorgewicht zu ändern wäre nicht \(D_zA\).

Die ersten \(M\) Terme liefern eine positive semidefinite Unterapproximation
von \(\Sigma\), keine komponentenweise Untergrenze ihrer Nebendiagonalen.
Sei \(v_{n,r}\) der \(n\)-te diagonale Beitrag und sei
\(S_r\ge\rho\int\mathbb E|D_zA_r|^2dz\). Dann ist der diagonale Rest durch

\[
 R_{M,r}\le\frac{S_r-\sum_{n=1}^M n v_{n,r}}{M+1}
\]

begrenzt, sofern die rechte Seite mit gültigen Einschließungen gebildet
wird. Der Betrag des gemischten Rests ist höchstens
\(\sqrt{R_{M,r}R_{M,s}}\). Das ist eine kontrollierbare Hierarchie;
die benötigten vollständigen Einfügeintegrale des ursprünglichen
Detektors werden in v0.13 nicht als bereits ausgewertet ausgegeben.

### Exakte Pfadvorhersage für den ursprünglichen lokalen H1-Adapter

Für eine Konfiguration ist \(u_\eta(p)\) die Summe aller kausalen Pfade
von genau einem History-Knoten über aktive Knoten zum passiven Punkt \(p\).
Eine Kante trägt \(\beta w_\epsilon(N)\),
\(\beta=a\epsilon/(a+1)\). Ein Pfad mit \(r\) Wolkenknoten trägt
\(r\) Kantengewichte und einen Anfangswert.

Bei deterministischer Historyfunktion \(h(y)\) liefert die multivariate
Mecke-Formel für einen einzelnen Pfad

\[
 \mathbb Eu_\eta(p)=\sum_{r\ge1}(\rho\beta)^r
 \int_{\substack{y_0\in H,\ y_1,\ldots,y_{r-1}\in U\\
                   y_0\prec\cdots\prec y_{r-1}\prec p}}
 h(y_0)\prod_{j=0}^{r-1}M(\epsilon\rho|I(y_j,y_{j+1})|)
 \,dy_0\cdots dy_{r-1},\quad y_r=p.
 \tag{8}
\]

Die aufeinanderfolgenden offenen Intervalle einer Kette sind disjunkt;
kein anderer eingefügter Kettenpunkt liegt in ihnen. Diese spezielle
Unabhängigkeit erklärt die Produktform von (8). Für den lokalen Adapter
ist hier also eine exakte gemittelte Volterra-Gleichung möglich. Das
rechtfertigt keine allgemeine Mittelung zufälliger Inversen oder der
nichtlokalen Projektionshistory.

Für \(\mathbb E[u(p)\overline{u(q)}]\) werden **Paare** solcher Pfade
summiert. Gleiche Wolkenknoten beider Pfade werden zuerst identifiziert;
für \(v\) verschiedene Knoten ist der Mecke-Faktor \(\rho^v\).
Alle Kantenintervalle, einschließlich wiederholter Kanten, gehen gemeinsam
in (1)-(2) ein. Jeder andere eingefügte Pfadknoten im offenen Intervall
erhöht dessen \(s_e\). Anschließend werden \(p,q\) mit den vollständigen
Fenstergewichten integriert und \(\mu\mu^*\) abgezogen. Das gibt eine
explizite Vorhersagehierarchie einschließlich gemeinsamer Pfadknoten,
Intervalle und zeitlicher Korrelationen.

Bei \(h=H_\eta(f,g)\) muss im Mecke-Integrand auch
\(H_{\eta+Z}(f,g)\) mit der eingefügten Konfiguration verwendet werden.
Der Anfangsdatenfaktor darf dann nicht aus dem Erwartungswert gezogen
werden. Alternativ gilt unmittelbar die Funktionalhierarchie (7), sobald
Totalität und Momentenexistenz des Adapters gesichert sind.

### Explizite Abschneidegrenzen für die ursprüngliche lokale Quelle

Für \(\epsilon=1/16\) beweist `transfer.py` die globale Grenze
\(|w(n)|<2\): die Werte \(0\le n<128\) werden eingeschlossen; danach
majorisiert das monoton fallende Produkt
\((15/16)^n[1+9n/15+8n^2/15^2+4n^3/(3\,15^3)]\) den Betrag.
Setze \(b=2\beta\), \(\Lambda=512\). Weil \(|h|\le1\) für die
ursprüngliche durch \(A/e\) normierte kompakte H1-Quelle,

\[
 |A_r(\eta)|\le\sum_{j=1}^N\binom Nj b^j=(1+b)^N-1.
\]

Alle Momente existieren somit. Für die nach Pfadlänge \(L\) abgeschnittene
Antwort und jedes \(\alpha>1\) gilt

\[
 \|A_r-A_r^{(L)}\|_2\le
 \alpha^{-L-1}\exp\{\tfrac\Lambda2[(1+\alpha b)^2-1]\}.
 \tag{9}
\]

Mit \(L=128\) ist die ausgewertete Grenze kleiner als \(1.75\,10^{-48}\).
Für das Abschneiden der gesamten Konfigurationen bei \(N\le M\) gilt

\[
 \|A_r1_{N>M}\|_2^2\le
 e^{\Lambda[(1+b)^2-1]}
 \mathbb P\{\operatorname{Pois}(\Lambda(1+b)^2)>M\}.
 \tag{10}
\]

Die Poisson-Oberseite wird per Chernoff begrenzt; bei \(M=1024\) folgt
\(\|A_r1_{N>M}\|_2<3.12\,10^{-28}\).
(6) überträgt beide Grenzen auf Mittelwert und Kovarianz. Die verbleibenden
hohen räumlichen Pfadintegrale müssen trotzdem berechnet werden. Kleine
Abschneidereste sind kein Nachweis kleiner Quadraturfehler dieser Integrale.
Eine solche Gesamtauswertung ist hier offen.

## 5. Bereits numerisch scharfe Vorhersage für die ursprüngliche Quelle

Der lokale H1-Adapter benutzt \(h=f\), weil \(g=0\). Seine nichtverschwindenden
Historywerte können nur aus
\(S=\{r<1/2,\,-4+r<t\le-1\}\) stammen. Exakt

\[
 |S|=4\pi\int_0^{1/2}r^2(3-r)\,dr=\frac{7\pi}{16},
 \qquad \rho|S|=\frac{21}{16}.
\]

Daher hat das Ereignis \(E=\{\eta(S)=0\}\) die Wahrscheinlichkeit
\(p_0=e^{-21/16}\). Auf diesem Ereignis ist die gesamte History null.
Die homogene retardierte Dynamik liefert gleichzeitig \(A_1=A_2=0\).
Das ist eine Ensemblevorhersage vor jedem neuen Sprinkling, kein Rückschluss
aus der beobachteten Anzahl leerer Archivwolken.

Für den Vektor der v0.12-Kontinuumsantworten \(c\) gilt in Loewner-Ordnung

\[
 \mathbb E[(A-c)(A-c)^*]
 =\Sigma+(\mu-c)(\mu-c)^*\succeq p_0cc^*.
 \tag{11}
\]

Cauchy-Schwarz auf \(E^c\) liefert außerdem

\[
 \Sigma\succeq\frac{p_0}{1-p_0}\mu\mu^*.
 \tag{12}
\]

Dies sind gemeinsame Matrixschranken. Sie beziehen die Korrelation der
beiden Fenster ein; einzelne Nebendiagonalen dürfen daraus nicht separat
geordnet werden. Die RMS-Gesamtfehler haben dadurch positive Untergrenzen.
Falls zusätzlich \(|\mu_r-c_r|\le\delta\) gefordert wird, folgt

\[
 \sqrt{\Sigma_{rr}}\ge
 \sqrt{\frac{p_0}{1-p_0}}\max(0,|c_r|-\delta).
 \tag{13}
\]

Die ursprüngliche nichtlokale Projektion kann Quellintegrale auch ohne
lokalen Quellknoten erhalten; (11)-(13) werden deshalb nicht auf sie
übertragen.

## 6. Vollständig ausgewertete Poisson-Transferkontrolle

Die Kontrolle ist ein endliches kausales Grundgerüst mit vier fest
vorgegebenen Zuständen. Die Poisson-Hintergrundpunkte verändern seine
Intervallgewichte, sind aber **keine zusätzlichen Lösungszustände**.
Dieses ausdrücklich andere Modell ist eine Methodenkontrolle und keine
Ersatzrechnung des ursprünglichen räumlichen Detektors.

Es sei \(y_1=(-2,0)\), \(y_2=(-2,1/2)\), \(x_1=(0,0)\),
\(x_2=(1,1/2)\) in der \((t,z)\)-Ebene; die anderen Raumkoordinaten sind
null. Setze \(A=I(y_1,x_1)\), \(B=I(y_2,x_2)\),
\(C=I(x_1,x_2)\), \(H=A\cap B\cap\{t\le-1\}\).
Es gilt \(C\subset B\), \(C\cap A=\varnothing\).

Die disjunkten Atommittel bei \(\rho=3/\pi\) sind exakt:

| Atom | Poisson-Mittelwert |
|---|---:|
| \(A\setminus B\) | \(19/32\) |
| \((A\cap B)\setminus H\) | \(225/256\) |
| \(H\) | \(135/256\) |
| \(B\setminus(A\cup C)\) | \(1107/128\) |
| \(C\) | \(9/128\) |

Mit \(X_A=w(N_A)\), \(X_B=w(N_B+1)\), \(X_C=w(N_C)\),
\(X_H=w(N_H)\), \(m_H=\mathbb EX_H\), \(\kappa=1/5\) gilt

\[
 h_1=(1+i/2)[1+\kappa(X_H-m_H)],\qquad
 h_2=(1-i/3)[1-\kappa(X_H-m_H)/2],
\]
\[
 u_1=\beta X_Ah_1,\qquad
 u_2=\beta X_Bh_2+\beta X_Cu_1.
 \tag{14}
\]

Der feste Knoten \(x_1\) liegt im offenen Intervall \(B\), daher ist dessen
Verschiebung **eins**. Die beiden Ausgangskanäle sind \(u_1,u_2\). Nur die drei in (14)
angegebenen Kanten sind Teil dieser Kontrolle; weitere kausal mögliche
Kopplungen sind hier definitionsgemäß null.
Die History hängt von einem gemeinsamen Bereich bei \(t\le-1\) ab;
ihre Korrelation mit den Operatorgewichten ist explizit.

Die Ausgabe ist ein Polynom bis Grad drei in den Gewichten. (2) berechnet
alle benötigten Produkte bis Grad sechs exakt. Die erste, zweite und
dritte Variationsordnung werden einzeln ausgewiesen; ihre Summe ergibt
die vollständige Antwort. Eine unabhängige direkte Summation über
9.655.800 Poisson-Zählzustände kontrolliert die Ergebnisse. Deren
abgeschnittene Wahrscheinlichkeit ist analytisch begrenzt; ihre
Gleitkommasummation ist eine Diagnose, kein zweites Intervallzertifikat.

Negativkontrollen entfernen getrennt die Überlappung, die Palm-Einfügung,
die Operatorzufälligkeit oder die Historyzufälligkeit. Zusätzlich wird die
rein lineare Vorhersage mit dem vollständigen Ergebnis verglichen.
Ein nachweislich von null verschiedenes drittes zentriertes Gewichtsmoment
zeigt, weshalb eine Gauß-Schließung hier nicht exakt ist.

## 7. Lösbarer Oszillator als zusätzliche Kontrolle

Für \(\xi=\pm1\) mit Wahrscheinlichkeit \(1/2\) sei

\[
 \ddot u+(1+\xi/4)u=0,\qquad u(0)=1+\xi/5,\quad\dot u(0)=\xi/10.
\]

Frequenz und Anfangsdaten benutzen dieselbe Zufallsvariable. Mit
\(\omega_\xi=\sqrt{1+\xi/4}\) ist
\(u_\xi=f_\xi\cos(\omega_\xi\tau)
 +g_\xi\sin(\omega_\xi\tau)/\omega_\xi\).
Die Mittelung über ein ganzes verschobenes Fenster \([a,b]\) ergibt

\[
 A_\xi=\frac{f_\xi[\sin(\omega_\xi b)-\sin(\omega_\xi a)]}
                   {\omega_\xi(b-a)}
 +\frac{g_\xi[\cos(\omega_\xi a)-\cos(\omega_\xi b)]}
                   {\omega_\xi^2(b-a)}.
\]

Benutzt werden genau \([7/4,2]\) und \([2,9/4]\). Somit
\(\mu=(A_++A_-)/2\) und
\(\Sigma_{rs}=(A_{r,+}-A_{r,-})(A_{s,+}-A_{s,-})/4\).
Der Oszillator ist reell, also \(\Pi=\Sigma\); die Kovarianz hat Rang eins.

Die erste Variationsfunktion ist

\[
 u_1(\tau)=\xi[\kappa\cos\tau+\gamma\sin\tau
                     -\sigma\tau\sin\tau/2],
 \quad\sigma=1/4,\ \kappa=1/5,\ \gamma=1/10.
\]

Die retardierte Volterra-Reihe mit \(|\sin(t-s)|\le t-s\) liefert bei
Fensterende \(T\) den uniformen Rest nach erster Ordnung

\[
 \delta(T)\le\cosh(\sqrt\sigma T)-1-\sigma T^2/2
 +\kappa[\cosh(\sqrt\sigma T)-1]
 +\gamma[\sinh(\sqrt\sigma T)/\sqrt\sigma-T].
\]

Die entsprechenden ersten Terme werden für die zweite Ordnung ebenfalls
abgezogen. `oscillator.py` prüft beide punktweisen Fensterreste und die
Mittelwert-/Kovarianzgrenzen (6). Die exakte Zweipunktverteilung, nicht eine
Stichprobenvarianz, liefert die Kontrollvorhersage.

## 8. Ensemblefähigkeit des nichtlokalen Adapters und offene Arbeit

Die räumliche P1-Projektion aus v0.11 ist auf den acht untersuchten Wolken
zertifiziert. Ein unbedingtes Poisson-Ensemble enthält jedoch auch Wolken
mit weniger als vier History-Knoten. Für die ursprüngliche Historyregion
ist \(\mathbb EN_H=81\), daher

\[
 \mathbb P(N_H<4)=e^{-81}\sum_{j=0}^3\frac{81^j}{j!}>0.
\]

Auf solchen Konfigurationen fehlt der verlangte dreidimensionale
Projektionsraum. Weitere Wolken können Quellüberdeckung oder numerische
Zertifikate verlieren. Zudem ist die integrierte nodale Verstärkung über
alle möglichen nahezu entarteten Geometrien noch nicht begrenzt.
Es wird weder Unendlichkeit dieser Momente behauptet noch ihre Endlichkeit
vorausgesetzt.

Vor einer numerischen unbedingten PU-Ensemblevorhersage braucht es deshalb
eine ausdrücklich definierte Abbildung auch für diese Fälle sowie ein
Momentenzertifikat. Eine bedingte Vorhersage bei erfolgreicher Geometrie
ist ein anderes Ensemble und muss mit Erfolgswahrscheinlichkeit und
Ausfallbehandlung berichtet werden. Ein Ausfall wird nicht zu einer
Nullantwort und nicht aus der Stichprobe gestrichen.

Offen bleiben außerdem die eingeschlossene räumliche Auswertung der
vollständigen Pfadpaarintegrale bzw. Einfügekern-Hierarchie für den
ursprünglichen Detektor und die gemeinsame Ensemblebilanz seiner numerischen
Integrationsfehler. v0.13 behauptet keine scharfen numerischen Werte für
\(\mu,\Sigma,\Pi\) dieses vollständigen Poisson-Detektors. Die Vorhersagen
(11)-(13) gelten bereits für die ursprüngliche lokale Quelle; (14) und der
Oszillator liefern vollständige überprüfbare Kontrollmomente.

## 9. Reproduktion und Quellen

```bash
cd research/cspp/fluctuation_transfer_v0_13
python -m pip install -r requirements.txt
python -B run.py --bits 128 --out results/PREDICTIONS_128.json
python -B run.py --bits 192 --out results/PREDICTIONS_192.json
OPENBLAS_NUM_THREADS=1 python -B audit.py
python -B verify.py
python -B report.py
```

27 analytische Tests, 105 Vergleiche eingeschlossener Vorhersagegrößen bei
128/192 Bit und die unabhängige deterministische Zählsumme bilden die
Prüfung. Geometrie, Parameter und Methodenquellen sind lokal gehasht.
Analytische Entwicklung und Vorprüfungen gingen dem Freeze voraus;
öffentliche Vorregistrierung, unabhängige Sprinkling-Bestätigung und
externe Begutachtung werden nicht behauptet.

1. G. Last, M. D. Penrose, *Poisson process Fock space representation,
   chaos expansion and covariance inequalities*, Theorem 1.1:
   https://arxiv.org/abs/0909.3205. Allgemeine Grundlage von (7).
2. G. Last, M. Penrose, *Lectures on the Poisson Process*, Kapitel 4, 18-20:
   https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf.
   Multivariate Mecke-Formel, Poisson-Chaos und Differenznormen.
3. D. M. T. Benincasa, F. Dowker, *The Scalar Curvature of a Causal Set*:
   https://arxiv.org/abs/1001.2725. Ursprung der verwendeten Schichtgewichte.
4. Projektdateien: `../variance_budget_v0_4/METHODS.md`,
   `../scalar_propagation_v0_7/METHODS.md`,
   `../detector_transfer_v0_9/METHODS.md`,
   `../nonlocal_initial_v0_11/README.md`,
   `../full_continuum_v0_12/README.md`.

Die gemeinsame Momentenextraktion, Pfad- und Restbilanz sowie die hier
angegebenen Kontrollmodelle sind in diesem Paket ausdrücklich hergeleitet;
die Quellen belegen keine bereits erfolgte Qualifikation des CSPP-Detektors.
