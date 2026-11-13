# Variationaler Randvertrag für Staub und Uhr

13. November 2026. Anschluss an die N11-Familie aus PR292. Diese Prüfung verwendet ausschließlich die dortige Wirkung. Es wird keine zusätzliche kanonische Uhr, keine Hamiltonfunktion und kein neues Dichtemaß eingesetzt.

**Ergebnis:** Aus der stationären Wirkung folgt eine exakte klassische kanonische Randrelation. Der volle Anfangs-/Zukunftsvertrag ist jedoch kein eindeutig invertierbarer Evolutionsgraph: der verlangte 14×14-Jacobian hat Rang 10 bei C0 und Rang 9 bei C1. Vier Defekte sind strukturelle Anfangs-Dichteconstraints. Bei C1 bleibt selbst nach Festlegung sämtlicher zukünftiger Randdichten eine exakte einparametrige Familie verschiedener Zukunftsuhren mit identischen Anfangskonfigurationen und Anfangsimpulsen.

Eine mathematische lokale Reduktion der vier Anfangsconstraints ist möglich. Ihre physikalische Identifikation als Eichreduktion und ihre Quantisierung auf dem bisherigen Dichtemischmaß sind zusätzliche Aufgaben. Insbesondere kann dieses kompakte Maß keine unitäre Weyl-Gruppe vollständiger Dichtetranslationen tragen.

## 1. Konfiguration, Wirkung und Vorzeichen

Wir verwenden `P={0,1,2,3}`, `I={4,5,6}` und `F={7,8,9,10}`. C0 ist die vollständige Kette; C1 entfernt genau `(4,5)` und `(5,6)`. Für den Staub-/Uhrteil gilt

\[
S_d=-\frac12\sum_{j=0}^{10}r_j C_j(T),\qquad
C_j=1+\frac\beta2\sum_{i\prec j}b_{ij}(T_j-T_i)^2,
\]

mit `beta=4/sqrt(6)` und `b=(1,-9,16,-8,0,...)`. Für exakte rationale Rechnungen setzen wir

\[
T_j=\Delta(u_j-5),\qquad\beta\Delta^2=2/19.
\]

Dann ist `C_j=1+(1/19)sum b_ij(u_j-u_i)²`. Die Rangresultate sind invariant unter dieser nichtsingulären Skalierung. Die zugehörigen Uhrimpulse erfüllen `p_u=Delta p_T`.

Die Randkoordinaten sind jeweils `xi=(u,r)`. Die Vorzeichenkonvention lautet

\[
p_P=-\partial_P\bar S_d,\qquad p_F=+\partial_F\bar S_d,
\qquad d\bar S_d=p_F\,d\xi_F-p_P\,d\xi_P.
\]

Hier wird der Skalarsektor getrennt geprüft. Er koppelt in der erklärten Wirkung nicht direkt an r oder T. Sein Fehlen in der folgenden `(u,r)`-Rangrechnung entfernt deshalb keine entsprechenden Kreuzableitungen. Die Gravitation ist für eine festgehaltene Ordnung feldunabhängig.

## 2. Eine exakte kanonische Relation existiert lokal

Die beiden positiven Sättel haben gleiche Randkonfiguration `u_B=j`, `r_B=rho`, `0<rho<1/2` und

| Ordnung | `u_I` | `r_I` |
|---|---|---|
| C0 | `(4,5,6)` | `(rho,rho,rho)` |
| C1 | `(4,4,5)` | `(2rho,rho,rho)` |

Alle sechs inneren Ableitungen nach `(u_I,r_I)` verschwinden. Der vollständige innere 6×6-Hessian erfüllt bei beiden Sätteln exakt

\[
\det S_{II}=-19^{-6}\ne0.
\]

Der Satz über implizite Funktionen liefert daher lokal eine eindeutige glatte innere Lösung `xi_I(xi_P,xi_F)` bei **vollständig vorgegebenen beiden Rändern**. Einsetzen definiert die stationäre Randwirkung `Sbar_d`. Ihre erste Variation hat keine inneren Restterme. Die durch die obigen Impulse erzeugte Relation ist damit eine exakte Lagrangesche Relation zwischen den beiden kanonischen Randphasenräumen. Das ist ein tatsächlicher variationaler Randvertrag; die Formulierung benötigt noch keine Behauptung über ein positives Quanten-Skalarprodukt.

Eindeutigkeit des inneren Randwertproblems ist jedoch eine andere Frage als Eindeutigkeit der Zukunft aus Anfangsdaten.

## 3. Der verlangte 14×14-Test

Festgehalten werden die acht Anfangskoordinaten und ihre vorgegebenen kanonischen Impulse. Die 14 unbekannten Koordinaten sind `xi_I` und `xi_F`. Wir verwenden die Zeilen

`(dS/du_I, dS/dr_I, p_uP, p_rP)`

und die Spalten

`(u_I, r_I, u_F, r_F)`.

Somit ist

\[
J_C=\frac{\partial(\partial_I S_d,\,-\partial_P S_d)}
{\partial(\xi_I,\xi_F)}.
\]

Die vier letzten Zeilen sind identisch null, auch abseits des Sattels. Denn jeder Anfangsvertex hat nur Vorgänger im Anfangspräfix:

\[
p_{r_j}^P=C_j(u_P)/2,\qquad j\in P.
\]

Diese vier Gleichungen legen zulässige Anfangsimpulse fest. Sie bestimmen keine zusätzlichen Zukunftsfelder.

| Prüfung | C0 | C1 |
|---|---:|---:|
| Rang des vollen 14×14-Blocks bei `rho=1/4` | 10 | 9 |
| Derselbe Rang entlang der erklärten Sättel für `0<rho<1/2` | 10 | 9 |
| Rang des nach Innenelimination verbleibenden 4×8-Blocks | 4 | 3 |
| Rang nach zusätzlicher Fixierung aller vier `r_F` | 10 von 10 | 9 von 10 |

Sämtliche Matrixeinträge und Nullraumbasen stehen in `checks/variational_boundary/results.json`. Es sind exakte rationale beziehungsweise symbolisch rationale Resultate, keine numerischen Rangschätzungen.

Wenn sämtliche vier zukünftigen Randdichten **zusätzlich festgelegt** werden, verbleiben sechs innere Gleichungen und vier Anfangs-Uhrimpulsgleichungen für zehn Unbekannte. Bei C0 ist deren Determinante

\[
\det J_{C0}^{(r_F\,\mathrm{fest})}
=\frac{2^{27}\rho^4}{19^{10}}\ne0.
\]

Damit folgt für C0 eine lokale Zukunftsbestimmung unter diesen zusätzlichen Endranddaten und verträglichen Anfangs-Dichteimpulsen. Das ist keine aus Anfangsdaten allein hergeleitete Cauchy-Evolution; `r_F` ist eine zusätzliche Randwahl.

## 4. C1 besitzt eine exakte Zukunftsfamilie bei gleichen Anfangsdaten

Bei C1 bleiben sämtliche P- und I-Felder und alle Dichten unverändert. Wir ändern allein

\[
u_F(\alpha)=(7,8,9,10)+\alpha(0,8,16,23).
\]

**Für jedes im gewählten Träger zulässige alpha** verschwinden weiterhin alle sechs inneren Eulerreste, und alle acht Anfangsimpulse bleiben exakt gleich. Dies ist stärker als ein linearer Nullvektor am Sattel. Schon `alpha=1/1000` liefert eine zweite zulässige Konfiguration im gemeinsamen Uhrträger `[-3/2,3/2]`; die vorhandenen Ordnungsrelationen bleiben mit den gerichteten Uhren vereinbar.

Die Zukunftsimpulse ändern sich dagegen. Für die vier Uhrimpulse gilt

\[
\delta p_{u_F}=\frac{\alpha\rho}{19}(232,-119,-241,128),
\]

und für die vier Dichteimpulse

\[
\delta p_{r_F}=\frac1{19}
\left(0,\;16\alpha(2\alpha-1),\;-8\alpha(244\alpha+173),\;
13\alpha(76\alpha+91)\right).
\]

Auch die stationäre Wirkung ändert sich:

\[
\bar S_d(\alpha)-\bar S_d(0)
=-\frac{\alpha\rho}{19}(932\alpha+217).
\]

Die Identität `dSbar/dalpha=p_F·dxi_F/dalpha` wurde zusätzlich exakt geprüft. Die Familie ist keine globale Uhrverschiebung, da der gesamte Anfangsrand fest bleibt. Aus den Rangdaten allein folgt aber auch kein Beweis, dass diese Richtung physisch unterscheidbar oder eine Eichrichtung ist. Eine mögliche Identifikation würde einen gesonderten Symmetrie-, Rand- und Observablenvertrag benötigen. Die Wirkung kann sich bei zulässigen Randtransformationen um Randterme ändern; ihr Unterschied allein ist daher kein allgemeiner Gauge-Ausschluss.

Was bereits eindeutig folgt: **Die hier gegebenen Anfangsdaten bilden für C1 ohne weitere Identifikation oder Randbedingung keinen eindeutigen Zukunftsgraphen.** Die kovariante kanonische Relation bleibt gültig. Eine solche Mehrdeutigkeit ist kein Ausschluss aller physikalischen oder quantisierten Randamplitudenbeschreibungen.

## 5. Was sich klassisch an den Anfangsconstraints reduzieren lässt

Auf dem Anfangsphasenraum sind

\[
\chi_j=p_{r_j}-C_j(u_P)/2=0
\]

vier unabhängige, paarweise Poisson-kommutierende Constraints. Ihre lokalen charakteristischen Flüsse verschieben `r_j` und ändern zugleich die Uhrimpulse. Die invarianten Uhrimpulse lauten

\[
\pi_a=p_{u_a}-\frac12\sum_{j\in P}r_j\partial_{u_a}C_j.
\]

Es gilt exakt `{pi_a,chi_j}=0`, `{u_a,pi_b}=delta_ab`, `{pi_a,pi_b}=0`. Die eingeschränkte kanonische Einsform hat die Gestalt

\[
\theta_P\big|_\chi
=\sum_a\pi_a\,du_a+
d\left(\frac12\sum_jr_jC_j\right).
\]

Mit der Konvention `omega=−dtheta` entsteht auf dem lokalen mathematischen Quotienten `sum du_a wedge dpi_a`. Dies liefert vier kanonische Uhrpaare. Ein klassisches Liouville-Volumen ist damit definierbar.

Diese Rechnung identifiziert die Dichtekoordinaten nicht automatisch als physisch redundante Quellen. Im bisherigen Versuchsvertrag waren Randdichten kontrollierte Präparationsdaten. Die charakteristischen Flüsse verlassen außerdem bei genügend großer Verschiebung den kompakten Dichteträger. Ihre globale physikalische Bedeutung und die Zulässigkeit einer Quotientierung müssen deshalb gesondert begründet werden. Das lokale symplektische Resultat wählt weder ein positives physisches Quanten-Skalarprodukt noch eine normierte Quantenwahrscheinlichkeit aus.

## 6. Eine exakte Obstruktion gegen die naheliegende Quantisierung

Der ursprüngliche Dichte-Hilbertraum ist

\[
L^2(d\nu),\qquad d\nu=\tfrac12\delta_0+\tfrac12\mathbf 1_{(0,1)}dr.
\]

Multiplikation mit r ist ein beschränkter selbstadjungierter Operator mit Spektrum `[0,1]`; bei null liegt zusätzlich ein Atom-Eigenvektor vor. Angenommen, ein selbstadjungierter Generator implementierte eine volle unitäre Weyl-Gruppe mit

\[
U(s)\,\hat r\,U(s)^\dagger=\hat r+sI
\quad\text{für alle reellen }s.
\]

Unitäre Konjugation erhält das Spektrum. Rechts stünde aber `[s,1+s]`, das für jedes `s≠0` von `[0,1]` verschieden ist. Das ist ein unmittelbarer Widerspruch. Somit kann die formale klassische Dichtetranslationsreduktion auf diesem ursprünglichen Hilbertraum nicht ohne Weiteres als solche Weyl-/RAQ-Gruppenwirkung realisiert werden.

Die Aussage betrifft genau diesen Operator, dieses Maß und diese volle Translationsforderung. Sie behauptet nicht, dass jeder selbstadjungierte Differentialoperator auf einem Intervall unmöglich wäre; periodische oder andere Randbedingungen verwirklichen nicht dieselbe globale Relation `r→r+s`. Ebenso werden alternative Quantisierungen, andere physische Paarungen oder eine begründete Änderung des Trägers nicht ausgeschlossen.

Der endliche Uhrträger würde eine analoge volle Translationsforderung ebenfalls blockieren. Er ist hier ausdrücklich Teil der endlichen Hilfsvervollständigung, keine abgeleitete fundamentale Begrenzung physischer Zeit. Die atomaren Beiträge und Endpunktflüsse der Dichte-/Uhr-Wardidentitäten sind in der getrennten Quellen-/Uhrprüfung zu berücksichtigen; eine naive Projektion darf sie nicht löschen.

## 7. Die bekannten zwei Sättel sind keine identischen Cauchy-Anfangsdaten

Für die bisher verglichenen Sättel stimmen die Anfangskonfiguration und die vier Dichteimpulse überein. Die Uhrimpulse sind jedoch

\[
p_{u_P}^{C0}=\frac\rho{19}(1,2,-16,32),\qquad
p_{u_P}^{C1}=\frac\rho{19}(65,-94,-12,78).
\]

Ihre Differenz beträgt `rho(64,−96,4,46)/19`. Die frühere gemeinsame Konfigurationsrandpaarung bleibt damit gültig. Sie darf aber nicht als Vergleich zweier klassischer Geometrieentwicklungen aus identischen vollständigen kanonischen Anfangsdaten ausgegeben werden. In einer Quanten-Konfigurationsrandpaarung können verschiedene Impulszweige selbstverständlich beitragen; deren physische Interpretation braucht den noch offenen Paarungsvertrag.

## 8. Reproduktion und Ergebnisstatus

```sh
python -B checks/variational_boundary/check.py
```

SymPy genügt. Der Prüfer rekonstruiert die Wirkung, kontrolliert die beiden Sättel, strukturelle Nullzeilen, symbolische Ränge, die vollständigen Nullräume, den regulären inneren Hessian, den reduzierten gemischten Block, die exakte Zukunftsfamilie, ihre Randvariation und die Poisson-Algebra der vier Anfangsconstraints. Null neue Integrationen.

**Abgeleitet:** eine klassische kanonische Randrelation; vier explizite Anfangsconstraints und deren lokale mathematische Reduktion; ein bedingter lokaler Zukunftsgraph für C0 bei zusätzlich festem `r_F`; ein exaktes Nicht-Eindeutigkeitszeugnis für C1; eine präzise Obstruktion gegen die automatische Weyl-Quantisierung auf dem alten Dichtemaß.

**Nicht abgeleitet:** die physische Eichidentifikation der Reduktion, eine gemeinsame physische Randpaarung beider Ordnungen, ein aus Anfangsdaten allein ausgewählter Geometrieprozess, kalibrierte Masse/Zeit oder eine vierdimensionale Geometriedynamik.
