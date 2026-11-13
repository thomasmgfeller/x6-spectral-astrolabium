# Wirkungsdynamik, Außenkragen und physikalische Paarung

Fachprüfung Geometriedynamik/Verklebung, 13. November 2026. Ausgangspunkt: PR290, Commit `f5ee44d7cb4dc1f924eee580f1eaf0cfcb4a5bc6`. Diese Prüfung ist interne KI-Arbeit, keine externe Begutachtung.

## Hauptbefund

**Für zwei N11-Kausalordnungen mit demselben festgelegten Außenkragen sind vollständige positive innere Staubsättel und eine nichtverschwindende Quellenabhängigkeit ihres Wirkungsunterschieds exakt nachvollzogen. Die innere stationäre Bewegung schließt sich nur mit den Beiträgen des gemeinsamen Zukunftskragens.** Das ist ein konkretes variationales Ergebnis auf endlichen Geometrien. Eine normalisierte physische Geometriedynamik folgt daraus weiterhin nicht.

Die Präfixkomposition der ursprünglichen Wirkung ist exakt und unabhängig von einer zulässigen natürlichen Beschriftung. Das ermöglicht eine gerichtete Berechnung bedingter Amplituden mit erhaltener Vergangenheit. Es liefert weder eine Regel, welche Ordnung entsteht, noch automatisch ein physisches Skalarprodukt oder einen unitären Zeitpropagator. Ein kovariantes Dekohärenzfunktional oder eine allgemeine Randamplitudentheorie bleibt als physikalische Zielstruktur ausdrücklich möglich.

## 1. Unveränderte Wirkung und neue, explizite Geometrien

Mit `b=(1,-9,16,-8)` für offene Intervallgrößen 0 bis 3 und `b=0` danach gilt

\[
S_C=\kappa\left(N-\sum_{y\prec x}b_{yx}\right)
-\frac12\sum_x r_x
-\frac\beta4\sum_{y\prec x}b_{yx}
\left[r_x(T_x-T_y)^2+(q_x-q_y)^2\right],
\qquad \beta=4/\sqrt6.
\]

Im N11-Vergleich sind `B={0,1,2,3,7,8,9,10}` und `I={4,5,6}`. Die erste Ordnung ist die vollständige Kette, die zweite entfernt allein `(4,5)` und `(5,6)` und behält sämtliche anderen Kettenrelationen, insbesondere `(4,6)`. Beide Relationenmengen sind transitiv abgeschlossen. Die induzierte Ordnung auf B ist identisch.

Wir setzen `T_j=Delta(u_j-5)`, `beta Delta²=2/19`, `u_B=j`, `r_B=rho`, `q=0` und `0<rho<1/2`. Die inneren Sättel sind:

| Ordnung | `(u4,u5,u6)` | `(r4,r5,r6)` | `F4` | Stationäre Wirkung bei κ=1 |
|---|---|---|---:|---|
| Kette | `(4,5,6)` | `(rho,rho,rho)` | 10 | `10−151rho/38` |
| Zwei entfernte Relationen | `(4,4,5)` | `(2rho,rho,rho)` | 18 | `18−105rho/38` |

Alle inneren Dichte-, Uhr- und Skalarableitungen verschwinden. Sämtliche inneren Dichten liegen strikt im positiven bisherigen Dichteträger. Der affine Außenkragen benötigt hingegen `|T|≤5Delta≈1,26945`; dies ist eine ausdrücklich neue Uhrunterstützung gegenüber `[-1,1]`. Der Kandidat ist daher kein nachträglich umgedeuteter Sechshistorienpilot. Eine physikalische Normierung des neuen Uhrmaßes wird hier nicht eingeführt.

Der exakt neu geprüfte Kontrast lautet

\[
S_{\rm Variante}^{\rm stat}-S_{\rm Kette}^{\rm stat}
=8+\frac{23}{19}\rho,
\qquad \frac{d}{d\rho}\Delta S^{\rm stat}=\frac{23}{19}.
\]

`rho` bezeichnet hier die gemeinsame Randdichte, keine kalibrierte Masse. Der Kontrast beschreibt die Quellenabhängigkeit zweier stationärer Wirkungszweige; er ist keine Übergangswahrscheinlichkeit und keine kontinuierliche geometrische Bewegungsgleichung. Zur physikalischen Interferenz gehören zusätzlich dieselben zulässigen Randzustände, Maße, Paarung und geometrischen Ereignisse.

## 2. Exakte gerichtete Komposition ohne erfundene Transfermatrix

Sei `C_n` eine Folge kausaler Präfixe einer festgehaltenen Ordnung, bei der jeweils ein neues maximales Element x angefügt wird. Kein neues Element liegt zwischen zwei bereits vorhandenen Elementen; deshalb bleiben ihre Intervallkoeffizienten unverändert. Die Differenzwirkung ist exakt

\[
\Delta S_x=\kappa\left(1-\sum_{y\prec x}b_{yx}\right)
-\frac{r_x}{2}
-\frac\beta4\sum_{y\prec x}b_{yx}
\left[r_x(T_x-T_y)^2+(q_x-q_y)^2\right].
\]

Damit gilt `sum_x Delta S_x=S_C`. Alle Monome der Gravitation, des Staubs und des Skalarfelds wurden unabhängig über die vollständige Ordnung sowie über die Präfixinkremente verglichen. Die alternative zulässige natürliche Reihenfolge `0,1,2,3,5,4,6,7,8,9,10` für die zweite Ordnung liefert dieselbe Wirkung. Das natürliche Etikett ist keine zusätzlich postulierte physische Uhr.

Bei einer Kette benötigt ein Inkrement nur die letzten vier Vorgängerfelder, weil weiter zurückliegende offene Intervalle mindestens vier Elemente enthalten. Dieser Vierer-Speicher gilt nicht für allgemeine Kausalordnungen. Schon der N10-Fork benötigt an einem späteren Element fünf relevante Vorgänger.

Die Inkremente werden hier in drei disjunkte Schalen nach dem späteren Endpunkt aufgeteilt: Vergangenheit `0..3`, Inneres `4..6`, Zukunft `7..10`. Es gibt weder eine doppelte Vertexintegration noch eine überlappende Schnittfläche in dieser Aufteilung. Der Faktor zwei des früheren quotientierten AA-Zweipunktschnitts ist deshalb **nicht** übertragen worden. Für tatsächliche Integrale ist das gemeinsame Maß genau einmal zu deklarieren; ebenso wird jeder innere Abel-Regulator genau einmal eingefügt. Bei positivem Regulator und zulässigen Testpaketen kann die endliche Integration danach per Fubini gruppiert werden. Ein Grenzwert braucht seine eigene Verteilungsprüfung.

## 3. Die stationäre Uhrbewegung benötigt den Außenkragen

Würde man allein die innere Schale variieren, wäre sie am genannten Sattel nicht stationär. Die folgenden Ableitungen beziehen sich auf die dimensionslosen inneren u-Koordinaten:

| Ordnung | Uhrgradient der inneren Schale | Uhrgradient des Zukunftskragens |
|---|---|---|
| N11-Kette | `(−16,2,1)rho/19` | `(16,−2,−1)rho/19` |
| N11-Variante | `(3,1,1)rho/19` | `(−3,−1,−1)rho/19` |

Die Summe verschwindet jeweils exakt. Das liefert eine konkrete endliche Entsprechung des gesuchten Zwecks einer gemeinsamen Anschlussvariation: das stationäre Innere ist mit seiner äußeren Wirkung gekoppelt. Es beweist weder ein allgemeines Israel-/GHY-Gesetz noch einen Außenraum des Staubkollapses.

Zusätzlich wurde die stationäre Randantwort geprüft. Weil die inneren Ableitungen verschwinden, gilt entlang der gemeinsamen Randdichtevariation die Hüllensatzidentität

\[
\frac{dS_C^{\rm stat}}{d\rho}
=\sum_{b\in B}\frac{\partial S_C}{\partial r_b}\bigg|_{\rm stat}.
\]

Sie ergibt `−151/38` für die Kette und `−105/38` für die Variante. Die einzelnen Rand-Uhr- und Rand-Dichteableitungen stehen in `results_n11.json`. Ihre globale Uhrverschiebungsbilanz ist exakt null. Diese Ableitungen sind unnormierte kanonische Randantworten der erklärten Wirkung, noch keine gemessenen Ströme.

## 4. Der Skalarsektor verhindert eine unzulässige Abkürzung

Für die N11-Kette ist `H_II/beta` die Matrix

\[
\begin{pmatrix}0&1/2&-9/2\\1/2&0&1/2\\-9/2&1/2&0\end{pmatrix},
\]

also vom Rang drei. Bei der Variante lautet sie

\[
\begin{pmatrix}0&0&1/2\\0&0&0\\1/2&0&0\end{pmatrix}.
\]

Ihr innerer Nullmodus `e5` koppelt an die Randfelder; der gestapelte Block aus `H_II` und `H_BI` hat Rang drei. Damit ist die Variante ein distributioneller Fall, kein gewöhnlicher punktweiser innerer Gaußkern. Ein ad hoc Entfernen der Nullrichtung würde den Kern verändern. Es wird in dieser Prüfung keine neue Amplitude ausgewertet.

Die N10-Kette mit Innenmenge `{4,5}` und die Ein-Relations-Variante `C\{(4,5)}` dienen als Negativkontrolle. Dort hat die Variante den **vollständigen** Skalar-Nullvektor `e4−e5`. Die innere Kontrastrichtung `(q4−q5)/sqrt(2)` koppelt weder an innere noch an äußere Felder und trägt den Abel-Faktor `sqrt(2pi/epsilon)`. Der generische Randtest beseitigt ihn nicht. Diese N10-Variante kann mit dem unveränderten Lebesgue-Skalarmaß nicht als endliche Vergleichsamplitude verwendet werden. Die Ablehnung einer solchen Variante ist notwendig und keine Aufforderung, den Nullmodus ohne Maßbegründung zu dividieren.

## 5. Dichteintegration ist kein automatischer Constraint-Projektor

Die ursprüngliche Mischmaßintegration ergibt für einen festgehaltenen Dichtekoeffizienten C:

\[
D(C)=\frac12+\frac12\int_0^1e^{-irC/2}\,dr
=\frac12+\frac{i}{C}(e^{-iC/2}-1),\qquad D(0)=1.
\]

Daraus folgt die exakte Randidentität

\[
C D(C)=\frac C2+i(e^{-iC/2}-1).
\]

Der erste Term stammt vom Atom, der zweite von den Endpunkten des kontinuierlichen Dichteträgers. Beide dürfen nicht stillschweigend verworfen werden. Insbesondere gilt bei `C=2pi`:

\[
D=\tfrac12-\tfrac i\pi,\qquad D^2-D=-\tfrac14-\tfrac1{\pi^2}\ne0.
\]

Die erklärte Integration ist daher keine durch bloße Wiederholung idempotente Projektion auf `C=0`. Dies ist kein allgemeiner Ausschluss quantisierter Staubtheorien: eine alternative Zwangsquantisierung, Randpaarung oder kovariante Quantenmaßkonstruktion muss separat aus ihrem Vertrag begründet werden. Ebenso wird hier **nicht** behauptet, jedes physische Modell müsse einen externzeitlichen unitären Operator besitzen.

## 6. Konstruktiver nächster Vertrag

Der tragfähige Kandidat ist eine **gemeinsame Randamplitude mit gespeicherter bedingter Vergangenheit**, einer deklarierten geometrischen Ereignisalgebra und einer expliziten physikalischen Paarung. Ihr gerichtetes Auswertungsverfahren kann die gerade geprüften Präfixinkremente nutzen. Ein Logarithmus des bisherigen Kerns oder eine positive Norm `K†K` würde die fehlende Physik nicht herleiten.

Eine begrenzte algebraische Speicherverbesserung ist möglich: am früheren festen Zweipunktschnitt gruppiere linke Vergangenheitspunkte nach Fußabdruck `u≠0` und drei auf vier gekappten Intervallhistogrammen. Pro Typ genügen für die Kreuzwirkung `N, sum(T), sum(T²), sum(q), sum(q²)`. Denn der Kreuzkoeffizient zu einem rechten Punkt ist innerhalb eines solchen Typs konstant. Die Identität

`sum_a c[(T_b−T_a)²]=(c)[N T_b²−2T_b sum(T_a)+sum(T_a²)]`

liefert die volle quadratische Abhängigkeit; für q gilt dasselbe. Eine grobe Obergrenze sind `3·5³=375` Typen. Das ist eine analytische Suffizienzbehauptung für die **einmalige feste Schnittkopplung**, keine zusätzlich numerisch geprüfte Kompressionsimplementierung. Die gemeinsame Verteilung dieser kontinuierlichen Momente und ihre Korrelationen mit der lokalen Amplitude müssen erhalten bleiben. Mittelwertersatz, eine geschlossene Aktualisierung bei wanderndem Schnitt oder ein endlichdimensionaler physischer Zustandsraum sind damit nicht bewiesen.

## 7. Reproduktion und Reichweite

```sh
python -B checks/dynamics_sewing/check.py
python -B checks/dynamics_sewing/check_n11.py
```

Die ersten 66 exakten Prüfungen betreffen N10, die weiteren 75 N11 einschließlich alternativer natürlicher Beschriftung. SymPy genügt; keine Quadratur, kein bezahlter Lauf und kein äußerer Solver wird benötigt. Die Daten stehen in `checks/dynamics_sewing/results.json` und `results_n11.json`. Quellenhashes sind in `source_provenance.json` angegeben. Die neuen Ordnungen sind explizit neue Versuche; sie werden nicht als ursprüngliche AA33- oder Sechshistorienrechnungen ausgegeben.

**PASS:** endliche Wirkungsverklebung, positive innere stationäre Quellen, exakte Außenkragenbilanz, Quellenabhängigkeit zweier stationärer Geometriezweige, Skalar-Nullmodendiagnostik. **HOLD:** ausgezeichnetes Historienmaß, physische Randpaarung/Quantenmaß, physische Geometrieereignisse mit verifizierter Wahrscheinlichkeit, Masse-/Zeit-/Radiuskalibrierung und Verfeinerungsgrenze.

## Methodischer Literaturanschluss

- Robert Oeckl, *General boundary quantum field theory: Foundations and probability interpretation*, https://arxiv.org/abs/hep-th/0509122. Die verallgemeinerte Randamplitudenperspektive verhindert, dass ein externer Zeitpropagator fälschlich zur einzigen möglichen Zielstruktur erklärt wird. Die Literatur beweist keine physische Interpretation des vorliegenden CST-Kerns.
- Robert Oeckl, *Schrödinger-Feynman quantization and composition of observables in general boundary quantum field theory*, https://arxiv.org/abs/1201.1877. Der dortige Zusammenhang zwischen Observablenkomposition und Raumzeitverklebung ist methodischer Anschluss; die dort geprüften linearen/affinen Voraussetzungen werden nicht pauschal auf diese Historienfamilie übertragen.
- Fay Dowker, Steven Johnston und Sumati Surya, *On extending the Quantum Measure*, https://arxiv.org/abs/1007.2725. Endliche positive Dekohärenzdaten allein garantieren keine uneingeschränkte Fortsetzung auf sämtliche physikalischen Ereignisse.
