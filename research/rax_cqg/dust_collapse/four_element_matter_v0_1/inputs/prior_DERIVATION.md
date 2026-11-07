# CST-DUST: vollständiger kontinuierlicher Drei-Element-Sektor v0.1

Stand: 7. November 2026. Ausgangspunkt ist Main nach PR 255,
Commit `9869528d008966a88052b65216da14eafce8db6f` im Repository
[thomasmgfeller/x6-spectral-astrolabium](https://github.com/thomasmgfeller/x6-spectral-astrolabium).
Acht Quelldateien sind mit Git-Blob-Identitäten in `inputs/provenance.json` gepinnt.

## 1. Aussage und festgehaltene Annahmen

Der vollständige Sektor mit drei neuen Elementen wird im bereits erklärten
Referenzmaß integriert. Die Dichtemarken werden analytisch, die verbleibenden
kontinuierlichen Uhren mit zertifizierter Gaußquadratur integriert. Ein Gitter
ersetzt weder das Maß noch die Theorie. Es werden keine neuen physikalischen
Kopplungen oder Endrandbedingungen ausgewählt.

Die acht Gates MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY,
TRAPPING und EXTENSION bleiben HOLD. Insbesondere bleibt die kohärente
Auslese vollständiger Historien eine zusätzliche Annahme; ein reiner
Elementzähler wäre weiterhin phasenblind. Diese Rechnung ist keine
vierdimensionale CST-Dynamik, keine Rückwirkungsherleitung und kein Bounce.

Festgehalten werden der Anfangsanker bei T=-2, w=0, die monotone Materieuhr
T=-2+4s mit 0<s<h und das normierte Dichtemaß

\[
 \nu(dw)=\tfrac12\delta_0(dw)+\tfrac12\mathbf1_{(0,1)}(w)dw.
\]

Es gilt h in {1/4,1/2}, alpha in {1,2}, mu in {0,1/4,1} und
g/pi in {0,1/18,1/9}. Die 36 Kombinationen sind diagnostische Referenzfälle.
Der Plan wurde nach analytischem Entwurf und vor der Implementierung und
neuen Integralwerten lokal eingefroren. Vorherige Abschätzungen der
Ableitungskosten waren bekannt; dies ist keine blinde Vorhersage oder externe
Präregistrierung.

## 2. Sieben natürliche Ordnungen und vollständige Wirkung

Ein Tupel p enthält für jedes neue Element die Bitmaske seiner Vorgänger.
Die Uhrreihenfolge ist fixiert. Deshalb werden sieben natürlich beschriftete
Ordnungen gezählt, nicht nur fünf unbeschriftete Isomorphieklassen. Die Uhr-
und Materiemarken gehören zu den Records; ein Austausch ohne die entsprechende
Maßtransformation wäre keine zulässige Gleichsetzung.

| p | G=S_g-1 |
|---|---:|
| (0,0,0) | 0 |
| (0,0,1) | 9 |
| (0,0,2) | 9 |
| (0,0,3) | -17 |
| (0,1,0) | 9 |
| (0,1,1) | 18 |
| (0,1,3) | 2 |

Der Anker gehört zur Wirkung, zählt aber nicht zu n. Mit
B=(1,-9,16,-8), B_k=0 für k>=4, und k_yj als offener Intervallkardinalität:

\[
 S_d=-\sum_{j=1}^{n}w_j a_j,\qquad
 a_j=\frac12+4h^2\sum_{y\prec j}B_{k_{yj}}(x_j-x_y)^2,
 \quad x_j=s_j/h,\quad x_{\rm anchor}=0.
\]

`geometry.py` erzeugt diese Polynome aus der vollständigen Ordnung.
3780 rationale Kontrollen vergleichen sie mit `intervals.action` und dessen
vollständiger Inkrementdarstellung. Sie prüfen 7 Ordnungen, 2 h-Werte,
10 streng geordnete Uhrtripel und 27 Dichtetripel. Die Endpunkte dienen
algebraischen Kontrollen; sie haben im kontinuierlichen Uhrmaß Maß null.

## 3. Exakte Dichteintegration und geordnete Uhrdomäne

Die charakteristische Funktion der Dichtemarke lautet

\[
 \chi(t)=\frac12+\frac12\frac{1-e^{-it}}{it},\qquad \chi(0)=1.
\]

Damit ist für eine einzelne Ordnung

\[
 A_p(\mu)=3!\int_{0<x_1<x_2<x_3<1}
           \prod_{j=1}^{3}\chi(\mu a_j(x))\,d^3x.
\]

Die Transformation x1=u1*u2*u3, x2=u2*u3, x3=u3 bildet den offenen
Einheitswürfel auf das geordnete Gebiet ab. Der normierte Jacobian ist
J(u)=6*u2*u3^2. Seine Integration ergibt eins. Jeder a_j ist in jeder
einzelnen Würfelkoordinate höchstens quadratisch.

Ein unabhängiger algebraischer Weg kontrolliert die Momente k=0,...,3:

\[
 3!\int_{x_1<x_2<x_3}x_1^{b_1}x_2^{b_2}x_3^{b_3}\,d^3x
 =\frac{6}{(b_1+1)(b_1+b_2+2)(b_1+b_2+b_3+3)}.
\]

Auf dem Würfel ist das entsprechende Integral
6/[(b1+1)(b2+2)(b3+3)]. Dichtemomente sind d0=1 und
dk=1/[2(k+1)] für k>=1. Beide Expansionswege stimmen in 56 Momenten exakt
überein. Zusätzlich wird die neue Quadratur für ein Element, Antikette und
Kette bei h=1/2, mu=1 gegen die gepinnten exakten Momentreihen bis Grad 48
geprüft. Die drei komplexen Differenzen liegen innerhalb der Summen beider
analytischer Fehlergrenzen. Dies ist ein Methodenvergleich innerhalb dieser
Arbeit, keine externe Replikation.

## 4. Ableitungsgrenzen ohne numerische Differentiation

Vor der Dichteintegration ist die Phase theta=mu*S_d reell. Für eine einzelne
Würfelkoordinate u_j gilt theta'''=0. Uniforme Grenzen
|theta'|<=D und |theta''|<=2A liefern

\[
 H_0=1,\quad H_1=D,\quad
 H_k=D H_{k-1}+2A(k-1)H_{k-2},\qquad
 |\partial_j^k e^{i\theta}|\le H_k.
\]

Das folgt durch Differentiation von f'=i*theta'*f. Die Integration gegen
das positive normierte Dichtemaß kann diese Grenze nicht vergrößern.

D und A werden rational aus Tensor-Bernstein-Koeffizienten auf
[0,1]^(2n) für die Uhr- und Dichtevariablen gewonnen. Für ein Polynom
P(x)=sum_a c_a*x^a mit Koordinatengraden d_i sind dessen Bernstein-
Koeffizienten

\[
 b_k=\sum_{a\le k}c_a\prod_i\frac{\binom{k_i}{a_i}}{\binom{d_i}{a_i}}.
\]

Die Bernstein-Basispolynome sind nichtnegativ und summieren sich zu eins.
Damit liegen P und seine Extremwerte zwischen min(b_k) und max(b_k).
Dies begrenzt theta' und theta''/2 auf der ganzen Domäne, nicht nur an
Stützstellen. Der Faktor |mu| wird anschließend eingesetzt.

Für die normierte n-Uhr-Würfeldichte J=n!*product_j u_j^j mit
nullbasierter Koordinatennummer p=j ist eine Grenze der m-ten Ableitung
des gesamten Integranden

\[
 B_{m,j}=n!\sum_{\ell=0}^{p}\binom{m}{\ell}
                  \frac{p!}{(p-\ell)!}H_{m-\ell}.
\]

Die übrigen Jacobianfaktoren sind höchstens eins. Diese etwas konservative
Grenze ist für alle verbleibenden Koordinaten gültig.

## 5. Gaußrest und vollständig eingeschlossene Arithmetik

Für q Punkte auf [0,1] ist die Gauß-Legendre-Fehlerkonstante

\[
 C_q=\frac{(q!)^4}{(2q+1)((2q)!)^3}.
\]

Die Standardformel für reelle Funktionen steht in NIST DLMF §3.5(v),
insbesondere (3.5.19) und (3.5.21). Für einen komplexen Integranden wird
kein gemeinsamer reeller Zwischenpunkt für Real- und Imaginärteil angenommen.
Stattdessen benutzt man den nichtnegativen Peano-Kern und dessen Gesamtmasse
C_q: |I(f)-Q(f)|<=C_q*sup|f^(2q)|. Die Positivität folgt auch aus der
Positivität des Gaußfehlers bei nichtnegativer 2q-ter Ableitung.

Positive Gaußgewichte summieren sich exakt zu eins. Teleskopieren des
Tensorproduktfehlers liefert deshalb

\[
 |A_p-Q_p|\le\sum_{j=1}^{n}C_{q_j}B_{2q_j,j}.
\]

Pro h,mu wird für jede Koordinate das kleinste gerade q aus 8,...,64 gewählt,
für das die schlimmste der sieben Geometrien höchstens 10^-10/6 beiträgt.
Diese Wahl verwendet ausschließlich Ableitungsgrenzen, keine beobachteten
Integralwerte. Die resultierenden Ordnungen sind:

| h | mu | (q1,q2,q3) | Punkte |
|---|---|---|---:|
| 1/4 | 1/4 | (8,8,10) | 640 |
| 1/4 | 1 | (12,12,14) | 2016 |
| 1/2 | 1/4 | (12,12,14) | 2016 |
| 1/2 | 1 | (20,22,30) | 13200 |

Bei mu=0 gilt A_p=1 exakt. Keine Quadratur ist dafür nötig.

Alle ausgewerteten Zahlen liegen in nach außen gerundeten Intervallen mit
Endpunkten auf dem Gitter 2^-160. Floating Point schlägt nur Startwerte der
Legendre-Nullstellen vor. Exakte rationale Vorzeichenwechsel, q disjunkte
Intervalle und der Polynomgrad q zertifizieren sämtliche Nullstellen. Die
Gewichte werden durch Intervallauswertung der Legendre-Ableitung eingeschlossen.
Zusätzlich enthalten die berechneten Monomialsummen ihre exakten Integrale
1/(k+1) für k=0,...,2q-1; alle Gewichte sind strikt positiv.

Pi wird über die Machin-Identität 16*atan(1/5)-4*atan(1/239) und
alternierende rationale Reihen eingeschlossen. Ein Intervall für das Argument
wird modulo pi/2 auf |x|<=1 reduziert. Kosinusgrad 32 und Sinusgrad 33 haben
Reste <=1/34! und <=1/35!. Für |t|<=1 wird chi direkt bis Grad 36 entwickelt;
der integrierte reelle Exponentialrest ist <=1/(2*38!). Sonst wird die
geschlossene Sinus-/Kosinusform mit einem von null getrennten Divisor verwendet.

Arithmetik- und Funktionsauswertungsfehler sind im resultierenden komplexen
Rechteck enthalten. Dessen Mittelpunkt dient als rationaler Amplitudenwert;
die Summe beider Halbbereiten ist eine sichere komplexe Radiusgrenze.
Der Gaußrest wird getrennt hinzuaddiert. Die größten beobachteten zertifizierten
Grenzen sind kleiner als 1.61e-37 für die Einzelgeometrie-Arithmetik und
6.50e-12 für die Einzelgeometrie-Quadratur. Das Ziel 1e-10 ist erfüllt.
Diese Aussagen verwenden ganzzahlige Arithmetik und analytische Beweise,
aber keinen unabhängigen formalen Beweisprüfer.

## 6. Kohärenter Zahlkanal und unbegrenzte Elementzahl

Die sieben Geometrien eines Zahlkanals werden kohärent summiert:

\[
 a_3(g,\mu)=\frac17\sum_p e^{igG_p}A_p(\mu),\qquad v_3=|a_3|^2.
\]

Hier sind die Gravitationsphasen im Allgemeinen nicht gaußrational; ihre
Intervallauswertung ist deshalb Teil des Zertifikats. Einzelgeometrie-
Quadraturfehler werden mit Gewicht 1/7 addiert; Rotation und Addition
erhalten eigene eingeschlossene Arithmetikfehler. Die normierte
Fixed-n-Auslese ist weiterhin unabhängig von alpha.

Mit V_n=E_n*h^n/n!, f_alpha(n)^2=2^(-alpha*n*(n-1)/2) und
c_n=f_alpha(n)^2*V_n gilt c3=7*h^3*2^(-3*alpha)/6. n<=2 wird unverändert
aus den gepinnten früheren Ergebnissen übernommen. Bei Amplitudenfehler epsilon
und |a|<=1 ist | |a|^2-|t|^2 |<=2*epsilon+epsilon^2.

Die bekannte Normierung reicht bis n=6:

\[
 Z_3=\sum_{n=0}^3c_n,\quad
 0\le Z_\infty-Z_6\le\delta_6=\frac{h^7}{7!}\frac1{1-h/8},\quad
 Z_{\max}=Z_6+\delta_6,\quad R_{\max}=Z_{\max}-Z_3.
\]

Die Normschranke folgt aus E_n<=2^(n(n-1)/2) und alpha>=1. R_max besteht
aus der exakten Normmasse n=4,...,6 und dem analytischen Rest n>6.
Die Feldphasen dieser Sektoren werden nicht ausgewertet.
Für S_L,U=sum_(n<=3)c_n*v_n,L,U gilt

\[
 \frac{S_L}{Z_{\max}}\le p_{\rm count,\infty}
 \le\frac{S_U+R_{\max}}{Z_{\max}}.
\]

Dies ist die Erfolgswahrscheinlichkeit des kohärenten Filters mit erhaltener
Zahl, nicht die Wahrscheinlichkeit einer bloßen Zahlmessung. Die obere Grenze
folgt aus S_U<=Z3 und der Monotonie von (S_U+R)/(Z3+R).
Alle 36 neuen Intervalle sind in den vorherigen Intervallen enthalten.

Für die kohärente Summe über sämtliche Zahlen wird die bekannte normierte
Amplitude durch 2*R_max/Z_max plus ihren Integrationsrest eingeschlossen.
Die Vakuumkomponente liefert zusätzlich (2/Z_max-1)^2 als Untergrenze,
weil Z_max<2. Das neue Intervall wird mit dem ebenfalls gültigen früheren
Intervall geschnitten; dieser Schnitt ist ausdrücklich dokumentiert.
Phasenfreie Fälle g=mu=0 ergeben exakt eins, auch bei unbegrenztem n.

## 7. Quantitativer Gewinn und Grenze

Die obere Wahrscheinlichkeit der noch nicht integrierten Phasensektoren
sinkt wie folgt (Dezimalzahlen hier nur zur Orientierung; JSON enthält
rationale Grenzen):

| h | alpha | vorher n>=3 | jetzt n>=4 | entfernte Schrankenmasse |
|---|---:|---:|---:|---:|
| 1/4 | 1 | 0.001856660114 | 0.00008150681631 | 95.61 % |
| 1/4 | 2 | 0.0002262681664 | 0.000001267648081 | 99.44 % |
| 1/2 | 1 | 0.01212947485 | 0.001047593961 | 91.36 % |
| 1/2 | 2 | 0.001473549829 | 0.00001736542217 | 98.82 % |

Beispiel h=1/2, alpha=1, g=0, mu=1: Das vollständig unbegrenzte
Zahlkanal-Erfolgsintervall liegt nach außen gerundet in
[0.932749749421; 0.933797343383], statt zuvor
[0.929417722608; 0.941547197461]. Die verbleibende Breite stammt praktisch
aus den Feldphasen ab n=4, nicht aus der neuen Quadratur.

Der Schritt schließt einen klar begrenzten quantitativen Engpass. Eine weitere
numerische Verfeinerung wäre der n=4-Sektor nach einem Kostenbudget.
Der physikalisch grundlegende offene Punkt bleibt die Auswahl des Dichtemaßes,
des kohärenten Historienzugriffs und der Randbedingung aus einer physikalischen
CST-Amplitude. Zusätzliche Dezimalstellen schließen diesen Punkt nicht.

## 8. Nachrechnung und Quellen

`python3 -O -B analyze.py` erzeugt sechs Ergebnisdateien.
`python3 -O -B replay.py` wiederholt die gesamte Rechnung in einem frischen
Verzeichnis und verlangt bytegleiche Ergebnisse. Der Replay übernimmt die
acht gepinnten Vorgängerquellen, keine berechneten neuen Ergebnisse oder Caches.
`python3 -B verify_package.py` prüft das SHA-256-Manifest.

Die Kontrollen für den fehlenden variablen Jacobianfaktor bei beibehaltenem
Faktor 6, den fehlenden Ordnungsfaktor 6 und eine fehlende natürliche Ordnung
schlagen an der Normierung an. Ein wichtiger Gegenfall: Lässt man den gesamten
Jacobian weg und integriert mit der uniformen Würfeldichte eins, bleibt die
Normierung eins. Dieser Fehler wird erst am Materiemoment sichtbar: Für die
Antikette bei h=1/2 wäre der erste Moment -107/216 statt -5/8. Die entsprechende
Negativkontrolle prüft ausdrücklich diesen normierungserhaltenden Fehler.
Eine nachträgliche Renormierung falscher Gewichte verändert das Modell.

Primärreferenz zur Gaußquadratur: [NIST Digital Library of Mathematical
Functions, §3.5(v), (3.5.19) und (3.5.21)](https://dlmf.nist.gov/3.5#v),
geprüft am 7. November 2026. Die spezielle Bernstein-/Ableitungsabschätzung,
CST-Anwendung und Fehlerfortpflanzung werden oben hergeleitet. Externe
Literatur wird verlinkt, nicht mitverteilt.
