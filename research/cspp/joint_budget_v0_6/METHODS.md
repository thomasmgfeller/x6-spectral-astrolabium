# Gemeinsame Budgetplanung v0.6: Herleitung

28. Oktober 2026. Alle Zahlen verwenden die bisherige Einheit L0; insbesondere
sind Dichten Zahlen für rho*L0^4. Dezimalzahlen im Bericht sind gerundet.
Grundlage sind die unveränderten [Mittelwertnachweise v0.3](../certified_budget_v0_3/METHODS.md)
und [Varianzschranken v0.4](../variance_budget_v0_4/METHODS.md).

## 1. Feste Physik und veränderliche Gebiete

Die Quelle bleibt der kompakte Bump bei t=-1, Radius 1/2, Trägerwellenzahl 4.
Der Detektor liegt bei t=1, Zentrum (0,0,3/2), Radius 1/2. Die skalaren
Pilotwellenzahlen 0,2,4,8 bleiben unverändert. Für notwendige Operatortests
verwenden wir dieselbe Kalibrierfamilie

\[
\phi_{\omega,k}(t,\mathbf x)
=e^{-(t^2+r^2)/(2L^2)}e^{-i\omega t+ikx_3},\quad L=2,
\quad(\omega,k)\in\{(0,0),(1/4,0),(0,1/4),(1/4,1/4)\}.
\]

Es gilt Box phi(0)=omega^2-k^2-1/2. Insbesondere ist der reelle Gauß-Zeuge
phi=phi_00 am Prüfpunkt auf Box phi=-1/2 normiert. Das Feld wird bei Änderung
von rho, ell_k oder H nicht neu skaliert.

Wir unterscheiden zwei kausal konvexe Diamanten:

\[
D_H=I((-H,\mathbf0),(0,\mathbf0)),\quad V_D=\pi H^4/24,
\]
\[
\Omega_H=I((-H,\mathbf0),(4,\mathbf0)),\quad V_\Omega=\pi(H+4)^4/24.
\]

H ist die volle Dauer des vergangenen Diamanten, keine symmetrische Halbbreite.
Da Omega_H geschnitten mit J^-(0) genau D_H ist, hat der Operator am Ursprung
in beiden Sprinklings bei gleicher rho dieselbe Verteilung. Zusätzliche
Punkte in Omega_H sind dennoch Ressourcenverbrauch.

Der kausale Quellensupport erfüllt für -1<=t<=1 die Schranke r<=t+3/2.
Damit gelten t-r+H>=H-3/2 und 4-t-r>=5/2-2t. Für H>=2 sind beide
Nullkoordinatenabstände mindestens 1/2. Auch der feste Detektor liegt darin.
Dies ist eine geometrische Supportkontrolle; daraus folgt keine einheitliche
Fehlerschranke für Operatoren an sämtlichen Quell- oder Detektorpunkten.

## 2. Unveränderte Zulässigkeit und Dichteabhängigkeit

Mit q=ell_k^-4, epsilon=q/rho, a=4*sqrt(q/6) und
P(u)=1-9u+8u^2-4u^3/3 lautet der Mittelwert des unveränderten geglätteten
Schichtoperators

\[
\mu_H=a\left[-\phi(0)+q\int_{D_H}\phi(y)e^{-qV_y}P(qV_y)\,d^4y\right].
\]

Bei festem ell_k,H hängt dieser Mittelwert nicht von rho ab. Die
physikalische Zulässigkeit bleibt 0<epsilon<=1, also rho>=q. Folglich

\[
\mathbb EN\ge qV_D\quad\text{bzw.}\quad\mathbb EN\ge qV_\Omega.
\]

Insbesondere sind für ell_k=1/8 und D20 weiterhin
4096*pi*20^4/24=85.786.423,394... erwartete Punkte nötig, bevor ein Fehlerziel
überhaupt betrachtet wird. Keine Varianzverbesserung verändert diese Gleichung.
Die viel kleineren epsilon-Grenzen in Abschnitt 4 sind lediglich Regime für
bestimmte hinreichende Varianzbeweise.

## 3. Vorzeichenbehaftete Randeinschließung

Für das reelle Gauß-Feld setze s=-t-r, v=-t+r, c=sqrt(pi*q/24), d=4L^2
und y=c*s*v. Nach Winkelintegration gilt

\[
d^4x=\frac\pi2(v-s)^2\,ds\,dv
=\frac{\pi}{2c}\frac{(v-y/(cv))^2}{v}\,dy\,dv.
\]

Der fehlende Randbeitrag delta_H=mu_infinity-mu_H entspricht v>=H,
0<=y<=cv^2. Mit C=4*sqrt(pi)*q ist er

\[
\delta_H=C\int_H^\infty\int_0^{cv^2}
e^{-y^2}P(y^2)e^{-v^2/d}
\left(v-\frac{2y}{cv}+\frac{y^2}{c^2v^3}\right)
e^{-y^2/(dc^2v^2)}\,dy\,dv.\tag{1}
\]

Wir erweitern zunächst y auf [0,infinity). Im erweiterten Integral wird
der letzte Exponentialfaktor bis Ordnung N=12 entwickelt. Für u>=0 gilt
die absolute Taylorrestschranke u^(N+1)/(N+1)!, unabhängig von seiner Größe.
Definiere die exakten signierten Momente

\[
M_j=\int_0^\infty y^je^{-y^2}P(y^2)dy
=-\frac{j(j-1)(j-2)}{12}\Gamma((j+1)/2).\tag{2}
\]

Die Identität folgt durch Einsetzen der vier Gamma-Momente und deren
Rekurrenz. M_0=M_1=M_2=0 erklärt, warum eine vorzeitige Betragsbildung
die Randrechnung so stark verschlechtert. Für absolute Majoranten dient

\[
U_j=\tfrac12\left[\Gamma((j+1)/2)+9\Gamma((j+3)/2)
+8\Gamma((j+5)/2)+\tfrac43\Gamma((j+7)/2)\right].
\]

Ferner ist mit x=H^2/d

\[
I_j=\int_H^\infty v^{1-2j}e^{-v^2/d}dv
=\tfrac12 d^{1-j}\Gamma(1-j,x).
\]

Die obere unvollständige Gammafunktion [1] wird aus G_0=e^-x,
G_1=E_1(x) und G_j=(x^(1-j)e^-x-G_(j-1))/(j-1) eingeschlossen.
Die endliche Summe ist

\[
S_N=C\sum_{n=0}^N\frac{(-1)^n}{n!(dc^2)^n}
\left[M_{2n}I_n-\frac2cM_{2n+1}I_{n+1}
+\frac1{c^2}M_{2n+2}I_{n+2}\right].\tag{3}
\]

Mit n=N+1 begrenzt

\[
R_N=\frac C{n!(dc^2)^n}
\left[U_{2n}I_n+\frac2cU_{2n+1}I_{n+1}
+\frac1{c^2}U_{2n+2}I_{n+2}\right]\tag{4}
\]

den Taylorrest. Zusätzlich muss der künstlich hinzugefügte Keil y>cv^2
entfernt werden. Setze Y=cH^2, T_j(Y)=integral_Y^infinity y^j exp(-y^2)dy
und U_j(Y)=T_j+9T_(j+2)+8T_(j+4)+(4/3)T_(j+6). Erweiterung dieses Keils
auf y>=Y,v>=H, Betragsbildung und exp[-y^2/(dc^2v^2)]<=1 liefern

\[
W=C\left[U_0(Y)I_0+\frac2cU_1(Y)I_1+\frac1{c^2}U_2(Y)I_2\right].\tag{5}
\]

Die T_j werden über die exakten erfc-/Exponentialrekurrenzen aus v0.4
ausgewertet. Somit gilt ohne unbegrenzte numerische Quadratur

\[
\boxed{\delta_H\in S_N+[-(R_N+W),R_N+W],\qquad
\mu_H=\mu_\infty-\delta_H.}\tag{6}
\]

Arb schließt alle Rechenschritte und die beiden Reste ein. mu_infinity wird
durch die unveränderte Routine aus v0.3 eingeschlossen. (6) wird bei cH^2>=8
verwendet. Es ist eine Aussage über dieses feste Feld am Ursprung, keine
uniforme Operatornorm über eine Feldklasse.

Bei cH^2<8 wird mu_H direkt durch validierte Acb-Quadratur auf dem kompakten
Nullkoordinaten-Dreieck berechnet: v in [0,H], z=s/v in [0,1],
u=-t=v(1+z)/2 und r=v(1-z)/2. Das Maß ist
(pi/2)*v^3*(1-z)^2 dz dv. Für die modulierten Felder kommt
exp(i*omega*u)*sinc(k*r) hinzu. Die geschachtelte Quadratur liefert für
komplexe Argumentbereiche gültige vollständige innere Intervallhüllen;
ein Komponentenradius über 1e-12 führt zum Abbruch. Es gibt hier keinen
abgeschnittenen Integrationsrest.

Als unabhängige Randaudits wird (1) für drei Fälle auf dem Rechteck
y in [0,8], v in [H,32] eingeschlossen. Der Rest y>8 wird durch die
absoluten T_j-Momente kontrolliert, v>32 durch die frühere Gauß-Randhülle.
Alle drei unabhängigen Radien sind kleiner als 1e-18 und überlappen (6).
Ein absichtlich umgedrehtes Randvorzeichen scheitert an diesem Vergleich.

## 4. Varianzschranken bei verschiedenen ell_k und H

Die Pfadantwort und die Poisson-Chaos-/Poincare-Ungleichungen [2] aus v0.4
bleiben unverändert. Für den reellen Zeugen werden nur nachgewiesene positive
Beiträge der ersten Chaos-Norm benutzt:

\[
\operatorname{Var}F\ge K_L/\rho\quad(\rho\ge q).
\]

Die dortige Schale 3<=sqrt(qV_z)<=3.1 wird jetzt auf vorgegebene Intervalle
v_l<=v_z<=v_h, Breite 1/5, angewendet. Es muss v_h<H und
g=v_l-3.1/(cv_l)>0 gelten. In den Formeln von v0.4 werden 1.9,2.1 durch
v_l,v_h ersetzt. Die indirekte Antwort wird weiterhin über den gesamten
Vergangenheitskegel majorisiert. Diese obere Betragsgrenze gilt daher auch
bei abgeschnittenem D_H. Nur wenn der direkte Betrag nachweislich größer
als die indirekte Hülle ist, wird die ganze Schale für K_L benutzt.

Aus mehreren gültigen Schalen wird eine starke Untergrenze ausgewählt.
Die Auswahl ist kein Beweis eines optimalen K_L; jede ausgewählte Schranke
ist für sich gültig. Beim Vergleichspaar 37/256,11/4 ist die Schale
v in [2.5,2.7] gültig und K_L ungefähr 29055,2690164.

Die obere Varianzhülle aus v0.4 majorisiert alle nichtnegativen Integrale
über den gesamten Vergangenheitskegel, ist also für jedes D_H gültig.
Für sieben deklarierte epsilon_0-Regime wird jeweils

\[
\operatorname{Var}F\le K_U(\ell_k,\epsilon_0)/\rho,
\qquad\rho\ge q/\epsilon_0
\]

eingeschlossen. Wir wählen die kleinste nachgewiesen hinreichende ganzzahlige
Dichte unter diesen sieben Möglichkeiten. Beim Vergleichspaar wird
epsilon_0=2^-52 ausgewählt. Das ist ein Beweisregime für die konservative
Hülle, keine geänderte Zulässigkeitsdefinition. Die vollständige Integration
der gemeinsamen Intervallmomente einschließlich ihrer Vorzeichen bleibt offen.

## 5. Dichte eliminieren und notwendige von hinreichenden Budgets trennen

Für den Gauß-Zeugen sind d0=|Box phi|=1/2, tau=0.1*d0 und sigma=0.07*d0.
Ist b=|mu_H-Box phi|, dann exakt

\[
\mathbb E|F-\Box\phi|^2=b^2+\operatorname{Var}F.\tag{7}
\]

Bias und Randbeitrag werden im signierten mu_H verbunden; sie werden nicht
wie unabhängige Zufallsfehler quadratisch addiert. Aus einer eingeschlossenen
Untergrenze b_- und K_L folgt, sofern tau^2-b_-^2>0,

\[
\rho\ge\max\left(q,\frac{K_L}{\tau^2-b_-^2}\right)
\quad\text{(nur 10 % Gesamt-RMS)},
\]
\[
\rho\ge\max\left(q,\frac{K_L}{\tau^2-b_-^2},\frac{K_L}{\sigma^2}\right)
\quad\text{(zusätzlich 7 % Streuung)}.\tag{8}
\]

Für konservative notwendige Werte werden der untere Endpunkt von K_L und
der obere Endpunkt des positiven Nenners benutzt. Hinreichende Dichten
erfüllen rho>=q/epsilon_0, K_U/rho<=sigma^2 und zusätzlich
b_+^2+K_U/rho<=tau^2. Getrennt werden 5 % Nichtlokalitätsbias und
1 % Randbeitrag geprüft. Dies lässt 115 Rasterpaare für den Planvergleich übrig.

Ein Budget B für erwartete Punkte setzt rho<=B/V. Daher ist

\[
\frac{\sqrt{b_-^2+K_L/(B/V)}}{d_0}\tag{9}
\]

eine Untergrenze des relativen RMS bei der größten budgetierbaren Dichte
und damit bei jeder kleineren zulässigen Dichte. Ein Wert über 0.1 schließt
das ganze Dichteintervall aus. Dichte wird nicht durch ein grobes Raster ersetzt.
Falls q>B/V, ist das Intervall bereits leer.

Der einzige bei B=20.000 in D_H so nicht ausgeschlossene Fall,
ell_k=3/2,H=2, erhält zusätzlich die vier festen Modenprüfungen aus Abschnitt 1.
Die zeitliche Mode besitzt eine relative Bias-Untergrenze über 0.22413,
die gemischte über 0.10603. Dies schließt das Paar bei jeder Dichte aus.
Weil V_Omega>V_D, gilt jeder solche Budgetausschluss auch für Omega_H.

Die in der Ergebnisdatei angegebenen Minima beziehen sich ausschließlich auf
das deklarierte endliche Raster und die benutzten Schranken. Die Reihenfolge
der notwendigen und hinreichenden Planminima wird durch nicht überlappende
Ball-Vergleiche geprüft. Die Funktionen werden zwischen Rasterpunkten nicht
global optimiert. Höhere Budgets in der Sensitivitätstabelle können deshalb
als `unresolved` erscheinen; das bedeutet keine Freigabe.

## 6. Ressourcen und Überlauf

Die übernommenen Grenzen sind B=20.000 erwartete Punkte pro Wolke, 4 GiB,
21.600 s und als historische Ensemblegröße 16. Das Fehlerziel betrifft eine
einzelne Wolke. Varianzreduktion durch Mittelung unabhängiger Wolken ist ein
anderes Ziel und wird nicht stillschweigend eingesetzt.

`counts.cpp` hält gleichzeitig eine int32-N*N-Matrix und zwei Bitmatrizen
mit jeweils N*ceil(N/64) uint64-Einträgen. Somit ist der Speicher mindestens
17*N^2/4 Bytes. Für N~Poisson(nu) folgt die Erwartungsuntergrenze
17*(nu^2+nu)/4, während die erwartete Zahl ungeordneter Paare nu^2/2 ist.
Diese Zahlen sind keine Speicherobergrenzen und keine Laufzeitmessungen.

Für einen tatsächlichen Punktdeckel C=20.000 setzen wir n=C+1. Chernoff folgt
direkt aus E exp(tN)=exp[nu*(exp(t)-1)] und t=log(n/nu)>0:

\[
P(N>C)\le e^{-\nu}(e\nu/n)^n.
\]

Für 16 Wolken ist die Summe dieser Schranken bei nu=19.462 höchstens
0.009820849, bei nu=19.463 aber größer als 0.01. 19.462 ist daher der größte
ganzzahlige Mittelwert, den diese konkrete 1-%-Ressourcenallokation bestätigt.
Es ist nicht der optimale Wert aus der exakten Poisson-Verteilung. Bei einer
Überschreitung wäre der Lauf als RESOURCE_HOLD zu erhalten, ohne Neuziehen.
Da schon der günstigere Erwartungsbudgettest scheitert, wurde kein Lauf gestartet.

## 7. Audit, Provenienz und Grenzen

Die Produktion berechnet alle 320 Paare bei 128 und 192 Bit. Der Audit prüft
31 rationale Momentidentitäten, 51 Gamma-Rekurrenzen gegen die unabhängige
unvollständige Gammafunktion, drei doppelte Randeinschließungen mit expliziten
Resten, eine höhere Taylorordnung und das Randvorzeichen. Vier gewöhnliche
96-Punkt-Gaußquadraturen in unabhängigen Zeit-/Radiuskoordinaten vergleichen
die Moden am Gegenbeispiel; sie sind Regressionen, keine Fehlerzertifikate.
Der alte v0.4-Untergrenzenwert wird wiedergefunden, eine außerhalb von D2
liegende Schale verworfen, feste Quell-/Detektorparameter und die D20-Zahl
werden gegen die ursprünglichen Dateien geprüft. Ungültige Skalen scheitern.

`FREEZE.json` bindet Protokoll, Programme und benutzte Vorgängerdateien nach
explorativer Vorrechnung und vor der gespeicherten Produktion. Das Paket ist
deterministische Entwicklungsplanung. `SHA256SUMS` erfasst zusätzlich sämtliche
Berichte und Ergebnisse. Der Verifier prüft auch unter Python -O und kann die
gesamte Rechnung in temporären Dateien wiederholen. Ein Präzisionsvergleich
ersetzt nicht die mathematischen Rest- und Varianzbeweise.

Die Entscheidung gilt für das deklarierte Raster, den bisherigen Operator,
die festgehaltene notwendige Feldfamilie und das übernommene Budget. Sie ist
kein globales No-go für alle kontinuierlichen ell_k,H oder andere Algorithmen.
Es gibt keine Freigabe für die übrigen Wellen, räumliche Lösungsnormen,
Dirac-/Flavor-Propagation oder die gesamte E4-Pipeline. Die v0.5-Referenz
bleibt unverändert; ihre offenen Detektorfehler werden hier nicht verbessert.

## Primärquellen

1. NIST DLMF, [Definitionen der unvollständigen Gammafunktionen, 8.2](https://dlmf.nist.gov/8.2),
   [Rekurrenzen, 8.8](https://dlmf.nist.gov/8.8) und
   [verallgemeinertes Exponentialintegral, 8.19](https://dlmf.nist.gov/8.19).
   Daraus stammen die Standardidentitäten; die Randeinschließung (1)–(6)
   ist die hier ausgeführte Anwendung auf den festen Schichtkern.
2. G. Last, M. D. Penrose, [Poisson process Fock space representation, chaos
   expansion and covariance inequalities](https://arxiv.org/abs/0909.3205),
   Theorem 1.1 und Gleichung (1.8). Die konkrete Box- und Varianzhülle wird
   aus dem projektinternen v0.4-Beweis übernommen.
3. [Projekt-PR #137](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/137),
   Basis-Commit `fd3c15edf5023daf1f1bcbfccc9f02f7cd125362`.
   Die Änderungen dieses Pakets ergänzen den bestehenden Stand; sie ändern
   weder historische Ergebnisse noch wissenschaftliche Gates.
