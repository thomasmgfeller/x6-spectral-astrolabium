# Vollständiges relatives Gewicht unter festgelegtem Dirichlet-/Boxvertrag

**Ergebnis:** Die inneren Staubdichten und Uhren beider N=11-Ordnungen wurden unter einem gemeinsamen ausdrücklich bedingten Vertrag vollständig integriert. Das relative Gewicht verändert mit der Randdichte sowohl Betrag als auch Phase. Die zuvor berechnete stationäre Wirkungsdifferenz `8+(23/19)rho` darf nicht als Ersatz für dieses Integral und auch nicht als zusätzliche Phase verwendet werden.

Die Rechnung ist eine abgeschlossene endliche Hilfsrechnung: feste Dirichlet-Randdaten, drei innere Uhrvariablen, alle acht Atom-/Positivdichtestrata. Die innere Integration ist vollständig; eine physikalische Randpaarung oder ein ausgezeichnetes Historienmaß wird damit nicht hergeleitet.

## 1. Gemeinsamer, ausdrücklich neuer Integrationsvertrag

Die beiden Ordnungen sind die vollständige Kette `C0` auf elf Punkten und `C1=C0\{(4,5),(5,6)}`. Die vollständigen transitiven Relationen, nicht bloß Hassekanten, bestimmen die Intervallkoeffizienten. Der Punkt `4` bleibt vor `6`. Es gilt `F0=10`, `F1=18`, `I={4,5,6}` und `B={0,1,2,3,7,8,9,10}`.

Auf B werden festgehalten:

\[
T_j=(j-5)\Delta,\quad\Delta^2=\frac{\sqrt6}{38},\qquad r_j=\rho.
\]

Für die inneren Variablen wird genau derselbe normierte Vertrag benutzt:

\[
d\mu_T=\prod_{j\in I}\frac{dT_j}{3}\,\mathbf1_{[-3/2,3/2]}(T_j),\qquad
d\nu_j=\frac12\delta_0+\frac12\mathbf1_{(0,1)}(r_j)dr_j.
\]

**Es gibt keine zusätzlich eingefügte Theta-Beschränkung auf kausal monotone Uhren.** Solche Restriktionen würden das Integral verändern und sind nicht in den folgenden Ergebnissen enthalten. Die gerichteten klassischen Sättel aus dem vorherigen Paket sind zulässige einzelne innere Konfigurationen dieses größeren Integrals; weder ihre Dominanz noch die Vernachlässigbarkeit anderer Konfigurationen wird angenommen.

Die beiden Auditquellen sind `rho=1/8` und `rho=1/4`. Die Randwerte sind klassische Dirichletdaten, keine bereits normierten physikalischen Quantenrandzustände. Die äußeren Skalar-Gaußpakete und deren Abel-Paarung werden separat behandelt; die Wirkung enthält keine direkte Staub-Skalar-Kopplung.

## 2. Exakte Dichteintegration und Skalarfaktorisierung

Für jede Ordnung sei

\[
C_j(T)=1+\frac\beta2\sum_{i\prec j}b_{ij}(T_j-T_i)^2,
\quad\beta=\frac4{\sqrt6},\quad B_c(T)=\sum_{j\in B}C_j(T).
\]

Die einzelne innere Dichteintegration ergibt exakt die ganze Funktion

\[
\begin{aligned}
D(C)&=\frac12+\frac12\int_0^1e^{-irC/2}dr\\
&=\frac12+\frac{1-e^{-iC/2}}{iC},\qquad D(0)=1.
\end{aligned}
\]

Numerisch wird dieselbe Funktion stabil als
`D(C)=(1+exp(-iC/4)*sinc(C/(4*pi)))/2` ausgewertet, wobei NumPy `sinc(x)=sin(pi*x)/(pi*x)` verwendet.

Das vollständige Staub-/Uhrgewicht unter diesem Vertrag lautet

\[
\boxed{W_c(\rho)=e^{iF_c}\int_{[-3/2,3/2]^3}\frac{d^3T}{27}
e^{-i\rho B_c(T)/2}\prod_{j\in I}D(C_j(T)).}
\]

Alle äußeren Staubwirkungsterme einschließlich der Konstanten in `C_j` bleiben erhalten. Die acht Dichtestrata sind einzeln

\[
W_{c,s}=\frac{e^{iF_c}}8\int\frac{d^3T}{27}
e^{-i\rho B_c(T)/2}
\prod_{j:s_j=1}\int_0^1e^{-ir_jC_j(T)/2}dr_j,
\quad s\in\{0,1\}^3.
\]

Der Faktor `1/8` ist der Produktfaktor der drei ursprünglichen Atom-/Positivmaße; er kommt in jeder Stratumamplitude genau einmal vor. Die gespeicherte Summe aller Strata stimmt mit der direkt ausgewerteten Produktform bis auf Float64-Rundung überein.

Weil `S=F+Sd(T,r)+Sphi(q)` und die deklarierten Maße faktorisieren, ist für dieselben äußeren Skalarpakete

\[
A_c(\rho)=\omega_c\,G_c\,W_c(\rho),
\]

wobei `G_c` die vollständig gepaarte skalare Gaußamplitude und `omega_c` das zusätzlich deklarierte Historiengewicht ist. **W enthält bereits `exp(iF)` und die gesamte Staubwirkung.** Ein weiterer Faktor `exp(i S_on)` wäre eine Doppelzählung. Ein korrekter Zweigvergleich muss außerdem beide skalaren Faktoren mit ihrer Abel-Phase behalten.

Dominierte Differentiation auf dem kompakten inneren Bereich liefert exakt

\[
W_c'(\rho)=e^{iF_c}\int\frac{d^3T}{27}
\left(-\frac i2 B_c(T)\right)e^{-i\rho B_c(T)/2}\prod_ID(C_j).
\]

Wo `W0,W1` nicht verschwinden, gilt
`partial_rho log(W1/W0)=W1'/W1-W0'/W0`. Die stationäre Steigung `23/19` ersetzt diese Insertion nicht.

## 3. Ausgeführte Quadratur und Werte

Eine positive normierte Gauß-Legendre-Tensorquadratur wurde mit 64,96,128,160 Knoten pro Uhrdimension ausgeführt. Transformation `T=(3/2)x` erzeugt die normierten Gewichte `w/2` je Dimension. Alle acht Strata und beide Quellableitungen wurden jeweils ausgerechnet. Die Speicherung enthält nur die kompakten Summen; große Gitterarrays werden nicht archiviert.

Die Werte bei 160 Knoten pro Dimension sind:

| Quelle | W0: Kette | W1: zwei Relationen entfernt |
| --- | --- | --- |
| rho=1/8 | −0.5905773987344514 + 0.0601253101336243 i | 0.3335446055202790 − 0.8928326929746065 i |
| rho=1/4 | −0.3944227603004480 + 0.3236873552205812 i | 0.0259504407092110 − 0.9534705621904004 i |

| Quelle | W1/W0 | Betrag | partielle Ableitung log(W1/W0) |
| --- | --- | --- | --- |
| rho=1/8 | −0.711316922355095 + 1.439378723663173 i | 1.605547530957258 | 0.894388245208968 + 2.298401541807125 i |
| rho=1/4 | −1.224776668469493 + 1.412255827258362 i | 1.869370056797859 | 1.499473042358318 + 1.726611722842166 i |

Damit besitzt das **numerisch ausgewertete vollständige innere Gewicht** eine Betragsantwort und eine von `23/19` verschiedene Phasenantwort. Die reine stationäre Phasennäherung hätte `partial log ratio=i*23/19` und keine aus ihr folgende Betragsänderung. Die Quelle muss daher durch das vollständige Integral transportiert werden.

Die größte 128/160-Abweichung beträgt ungefähr `1.9e-15` für W und `1.2e-14` für W'. Diese Verfeinerungsdifferenzen sind Diagnostik, keine bewiesenen Gesamtfehlerschranken.

## 4. Analytische Quadraturrestschranke, getrennt von Rechenrundung

Für die ideale Gaußquadratur in exakter Arithmetik wird eine eigenständige analytische Restschranke bewiesen; sie wird nicht aus Knotenverdopplung abgeleitet.

Nehme eine einzelne komplexe Uhrvariable auf der Bernsteinellipse mit `R=7/4`, Halbachsen `a_R=(R+R^-1)/2`, `b_R=(R-R^-1)/2`; die übrigen Uhren sind reell. Mit `L=3/2`, `beta<5/3`, `rho<=1/4`, `r_I<=1` und `|T_B|<L` folgt aus der ursprünglichen quadratischen Staubwirkung

\[
\log M_k\le\frac{15}{8}b_R(a_R+1)\sum_{\text{Kanten an }k}|b_{ij}|r_j^{\max}.
\]

Die drei gewichteten Kantensummen sind `(50,173/4,85/2)` für C0 und `(173/4,85/2,85/2)` für C1. Die positiven normierten Dichtemaße können diese Schranke nicht vergrößern. Sie gilt auch für die Stratumbeiträge mit ihrem expliziten Gewicht.

Chebyshev-Koeffizienten einer auf dieser Ellipse durch M beschränkten Funktion erfüllen `|a_m|<=2M R^-m`. Abschneiden bei Grad `2n-1`, die exakte Polynomgleichheit der n-Punkt-Gaußregel und Norm eins sowohl der Integration als auch der positiven normierten Quadratur ergeben

\[
|I-Q_n|\le\frac{4M R^{-2n}}{1-R^{-1}}.
\]

Die dreidimensionale Tensorregel wird durch Teleskopieren der drei Operatoren abgeschätzt. Alle verbleibenden Integrationen und positiven Quadraturen haben Norm eins. Daher

\[
|W-W^{\rm ideal}_{n^3}|\le
\sum_{k=1}^3\frac{4M_kR^{-2n}}{1-R^{-1}}.
\]

Für W' wird zusätzlich der komplexe Betrag der Polynominsertion `B_c/2` beschränkt. Bei n=160 ergeben sich folgende nach oben gerundete analytische Schranken:

| Größe | C0 | C1 |
| --- | --- | --- |
| absoluter W-Quadraturrest | 1.2 × 10⁻²⁵ | 1.6 × 10⁻³² |
| absoluter W'-Quadraturrest | 1.5 × 10⁻²² | 2.1 × 10⁻²⁹ |

Der Prüfer wertet die rationalen Exponenten und die abschließende Restformel mit mpmath-Intervallarithmetik aus. Der unabhängige Prüfer `checks/independent_audit/audit_quadrature.py` bestätigt die angegebenen Dezimalobergrenzen zusätzlich rein rational: Für die Exponentialfunktion verwendet er das Taylorpolynom bis Grad 512 und einen geometrischen Rest. Die analytischen Dezimalobergrenzen hängen damit nicht allein von einer Transzendentenauswertung in mpmath ab. **Diese Schranken enthalten nicht die Rundung der Float64-Knoten, Gewichte, Elementarfunktionen oder Summationen der numerischen Auswertung.** Die oben angegebenen komplexen Zahlen sind deshalb noch keine vollständig zertifizierten Zahlenintervalle. Die sehr kleinen analytischen Reste erlauben insbesondere nicht, alle ausgegebenen Stellen als mathematisch eingeschlossen auszugeben. Für einen folgenden strikten Intervallbericht wäre eine separate Rundungs- und Knotenprüfung erforderlich.

Unabhängig von der Numerik bleiben die groben rigorosen Schranken `|W_c|<=1` und `|W_c'|<=E_T|B_c|/2` gültig. Der unabhängige Audit rekonstruiert `B_c` separat als quadratisches Polynom, weist seine Positivität auf der Box nach und verschärft die Ableitungsschranke. Diese Aussagen verwenden keine Float64-Konvergenzannahme.

## 5. Aussagegrenze und reproduzierbare Dateien

`checks/full_weight/check.py` führt Dichteidentität, alle acht Strata, beide vollständigen Wirkungen, Quellableitungen und vier Quadraturordnungen aus. `results.json` enthält sämtliche komplexen Summen, die analytischen Restformeln und die getrennten empirischen Verfeinerungsdifferenzen. Typische lokale Gesamtlaufzeit liegt bei wenigen Sekunden; weder bezahlte externe Rechnungen noch frühere große Integrationen werden benötigt.

Das Ergebnis schließt die fehlende **innere** Staub-/Uhrintegration dieses neu deklarierten endlichen Vertrags. Es begründet noch kein physikalisches Gewicht zweier Universumsgeometrien, keine positive physische Randpaarung und keine vierdimensionale Geometriedynamik. Die Grenzen betreffen die Interpretation der vollständigen Hilfsrechnung; sie sind kein Grund, an ihrer Stelle erneut nur eine stationäre Phase einzusetzen.
