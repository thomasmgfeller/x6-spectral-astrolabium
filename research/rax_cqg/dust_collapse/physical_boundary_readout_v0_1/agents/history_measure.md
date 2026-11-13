# Historienmaß: stärkere Anforderungen und verbleibende Auswahl

## Befund

Positive Gewichte, Beschriftungskovarianz und exakte Präfixkomposition bestimmen das Historienmaß nicht eindeutig. Selbst wenn eine **normierte kausale klassische Wachstumsvorschrift** und klassische Bell-Kausalität hinzugefügt werden, bleibt eine explizite Parameterfamilie. Dies wird durch tatsächlich komponierbare Regeln gezeigt; es ist kein erneutes bloßes Freilassen zweier Endgewichte.

Für das feste N=11-Paar sind die Konsequenzen exakt berechenbar. Ein physisches Quantengravitationsmaß folgt daraus weiterhin nicht, weil die zusätzliche Wachstumsregel nicht aus der gemeinsamen CST-DUST-Wirkung abgeleitet ist.

## 1. Positive kovariante Maßfamilie mit exakter Komposition

Sei R(C) die Zahl sämtlicher strikter Ordnungsrelationen, nicht nur der Coverrelationen. Für jedes reelle λ definiere

\[
\mu_\lambda(C)=e^{-\lambda R(C)}.
\]

Dieses Gewicht ist strikt positiv und invariant unter Beschriftungswechseln. Bei natürlichem Wachstum entsteht ein neues Element x mit vollständig bekanntem Vergangenheitsbereich. Sein Faktor lautet

\[
w_\lambda(C\to C\cup\{x\})=e^{-\lambda|\operatorname{past}(x)|}.
\]

Jede Relation wird genau beim Hinzufügen ihres späteren Endpunkts gezählt. Daher gilt für jede natürliche Geburtsreihenfolge und jede Zerlegung in Präfixabschnitte

\[
\prod_xw_\lambda=e^{-\lambda\sum_x|\operatorname{past}(x)|}
=e^{-\lambda R(C)}.
\]

Damit sind Komposition und Reihenfolgenunabhängigkeit exakt. Dies ist zunächst eine **unnormierte Maßregel**, keine stochastische Übergangswahrscheinlichkeit. Eine nachträgliche lokale Normierung darf nicht ohne neue Prüfung als dieselbe kovariante Regel ausgegeben werden.

Im N=11-Paar hat C₀ insgesamt 55, C₁ insgesamt 53 Relationen. Somit

\[
\mu_\lambda(C_1)/\mu_\lambda(C_0)=e^{2\lambda}.
\]

λ ist ein zusätzlicher Maßparameter. Keine Änderung der Gravitation–Staub–Skalar-Wirkung wird vorgenommen; gerade diese Unabhängigkeit zeigt, dass jene Wirkung und die genannten strukturellen Anforderungen λ nicht festlegen.

## 2. Auch kausal normiertes Wachstum liefert keine Eindeutigkeit

Als stärkeres Gegenbeispiel verwenden wir die klassische transitive Perkolation. Rideout und Sorkin definieren sie durch unabhängige Vorläuferverbindungen mit Wahrscheinlichkeit p und anschließenden transitiven Abschluss. Ihre Übergangsformel (6) erfüllt interne Temporalität, diskrete allgemeine Kovarianz, Bell-Kausalität und die Markov-Normierung. Die Arbeit behandelt ausdrücklich eine klassische stochastische Vorstufe; sie liefert damit keine Quantengravitationsamplituden. Primärquelle: [Rideout–Sorkin, Phys. Rev. D 61, 024002](https://doi.org/10.1103/PhysRevD.61.024002), [Originalmanuskript](https://arxiv.org/pdf/gr-qc/9904062), §§2–4.2, insbesondere Gleichung (6) und PDF-Seiten 15–16.

Unsere direkte endliche Ableitung: Ist A ein vergangenheitsabgeschlossenes Teilset des n-elementigen Elternorders und m(A) die Zahl seiner maximalen Elemente, müssen alle diese Maximalpunkte beim Vorläuferziehen ausgewählt werden. Alle Punkte außerhalb A müssen ausgelassen werden. Die übrigen Auswahlen innerhalb A sind redundant und summieren sich zu eins. Somit

\[
P_p(A\mid C_n)=p^{m(A)}(1-p)^{n-|A|},\qquad0<p<1.
\]

Die Vorgängerziehungen partitionieren sich eindeutig nach ihrem transitiv abgeschlossenen A; daher summieren diese Übergänge für jeden Elternorder zu eins. Beim Entfernen von Zuschauerelementen außerhalb zweier Vorläufermengen fällt derselbe Potenzfaktor aus ihrem Wahrscheinlichkeitsverhältnis weg. Das gibt hier direkt die klassische Bell-Kausalität.

Für eine bestimmte natürlich beschriftete Endrelation ist das Produkt der Übergänge

\[
P_p(C)=p^{L(C)}(1-p)^{I(C)},
\]

wobei L die Zahl der Coverrelationen und I=\(\binom N2-R\) die Zahl unvergleichbarer Paare ist. Die Exponenten sind Ordnungsinvarianten. Alternativ: Jede Coverkante muss bereits im anfänglichen unabhängigen gerichteten Graphen vorhanden sein; jede unvergleichbare Kante muss fehlen; sämtliche redundanten Relationen können unabhängig vorhanden oder abwesend sein und summieren sich weg.

## 3. N=11: Zählkonventionen explizit auseinanderhalten

Der gemeinsame Rand ist B={0,1,2,3,7,8,9,10}; nur I={4,5,6} wird umbenannt. C₀ ist die Kette. C₁ entfernt (4,5),(5,6) und behält (4,6).

| Invariante | C₀ | C₁ |
|---|---:|---:|
| Strikte Relationen R | 55 | 53 |
| Coverrelationen L | 10 | 11 |
| Unvergleichbare Paare I | 0 | 2 |
| Lineare Erweiterungen e | 1 | 3 |
| Randfixierende Automorphismen | 1 | 1 |
| Alle verschiedenen inneren S₃-Beschriftungen | 6 | 6 |
| Davon natürlich beschriftet | 1 | 3 |

Die drei inneren natürlichen Reihenfolgen von C₁ sind (4,5,6), (4,6,5) und (5,4,6). Für eine feste natürlich beschriftete Repräsentation gilt deshalb

\[
\frac{P_p(C_1)}{P_p(C_0)}=p(1-p)^2.
\]

Vergisst man hingegen die Geburtsbeschriftung eines normierten Wachstumsprozesses, muss man die Wahrscheinlichkeiten aller verschiedenen natürlichen Endrelationen addieren. Ihre Zahl ist e(C)/|Aut(C)|; hier also 3 beziehungsweise 1. Der **unbeschriftete Wachstums-Pushforward** ergibt

\[
\frac{P_p([C_1])}{P_p([C_0])}=3p(1-p)^2.
\]

Dieser Faktor drei ist kein Automorphismenfaktor. Ein anderer Vertrag, der eine bereits invariante Endgewichtsfunktion über **alle** sechs inneren Beschriftungen summiert und durch |S₃|=6 teilt, ergibt jeweils Gewicht/|Aut_B| und hier keinen relativen Faktor drei. Das ist eine eigenständige Endzählkonvention. Der stochastische Geburtsprozess weist nichtnatürlichen Geburtsbeschriftungen keine solchen Wahrscheinlichkeiten zu. Man darf die beiden Konventionen nicht vermischen.

Bei Umnummerierung sind sämtliche inneren Materievariablen und Rollen mitzutransportieren. Das bloße Neuetikettieren einer Ordnung bei festgehaltenen labelabhängigen Feldern wäre ein anderer physikalischer Randversuch.

Zwei strikt positive, vollständig normierte Regeln liefern bereits unterschiedliche Werte:

| Wachstumsparameter p | Verhältnis fester Repräsentationen | Verhältnis unbeschrifteter Klassen |
|---|---:|---:|
| 1/2 | 1/8 | 3/8 |
| 3/4 | 3/64 | 9/64 |

Das belegt die Nicht-Eindeutigkeit unter den starken Anforderungen. Die Auswahl eines bestimmten p wäre eine weitere physikalische Annahme; sie wurde hier nicht aus einem gewünschten Interferenzergebnis angepasst.

## 4. Vollständig ausgeführte kleine Kontrollen

Der eigenständige Prüfer `checks/history_measure/check.py` enumeriert bei N=0,…,5 sämtliche vorwärtsgerichteten Graphen, bildet ihre transitiven Abschlüsse und prüft exakt:

- Die Vorbildanzahl je Abschluss und Kantenzahl ist \(\binom{R-L}{k-L}\). Damit ist die Perkolationsgewichtsformel unabhängig rekonstruiert.
- Die Gewichte sämtlicher natürlich beschrifteten N-Orders summieren sich symbolisch für jedes p zu eins.
- Bei Eltern mit höchstens vier Punkten stimmen alle Vorläufersummen mit eins überein; Zuschauerentfernung erhält sämtliche geprüften Übergangsverhältnisse.
- Jede natürliche lineare Erweiterung reproduziert dieselben Präfixexponenten (L,I,R).
- Die Umnummerierungsorbits bestätigen die Klassenmultiplizität e/|Aut|.
- Die N=11-Relationen, Coverrelationen, Automorphismen und drei natürlichen Erweiterungen sind direkt gezählt.

Die Inventare natürlich beschrifteter Posets sind (1,1,2,7,40,357); die unbeschrifteten Klassen sind (1,1,2,5,16,63). Insgesamt bestehen **6.390 Präfixprüfungen natürlicher Erweiterungen**, **51 exakte Normierungsprüfungen von Elternfamilien** und **3.645 klassische Bell-Verhältnisprüfungen**. Der Lauf benötigt weniger als eine Sekunde; keine Monte-Carlo-Rechnung oder große Historienenumeration wird verwendet.

## 5. Physikalische Entscheidung, die noch fehlt

Der Befund trennt zwei Fragen. Ein Historienprior kann strukturell kovariant, positiv, kausal komponierbar und klassisch normiert sein, ohne eindeutig ausgewählt zu werden. Ein Detektor-/Umweltvertrag kann wiederum Kohärenz oder Recordbildung bestimmen, ohne diesen Maßparameter festzulegen.

Insbesondere darf P_p nicht stillschweigend als kohärenter Amplitudenfaktor ω eingesetzt werden. Die Wahl ω=P_p, ω=√P_p oder eine andere Quantisierung sind verschiedene zusätzliche Konstruktionen. Auch eine zuvor normierte klassische Regel normiert nicht automatisch die anschließend mit exp(iS_CST-DUST) gebildete Quantensumme oder deren physische Paarung.

**Abgeschlossen:** reproduzierbarer Nachweis verbleibender Maßfreiheit auch unter deutlich stärkeren Anforderungen und korrekte N=11-Multiplizitäten. **Nicht abgeschlossen:** ausgezeichnetes physikalisches Quantenhistorienmaß aus derselben Wirkung, gemeinsamer physischer Skalarprodukt-/Constraintvertrag und daraus folgende eindeutige Geometriedynamik.
