# Was Schnittzahlen erhalten – und was beim Zusammenfassen verloren geht

Diese Aussagen betreffen endliche binäre Inzidenzmatrizen und ausdrücklich
beschriebene Zweischichtenordnungen. Die positive Aussage ist eine Anwendung
der klassischen Möbius-Inversion auf dem Teilmengenverband, kein neuer allgemeiner
Rekonstruktionssatz für Kausalmengen. Die Negativaussage folgt aus einer elementaren
Zählung. Die Beweise und ihre Voraussetzungen sind von den endlichen Prüfläufen
zu unterscheiden.

## 1. Zugeordnete Schnittzahlen rekonstruieren die Spalten

Sei B eine binäre m×u-Matrix mit angegebenen Zeilen- und Spaltenseiten.
Für jede Spalte j sei Nⱼ ihre Nachbarschaft in der beschrifteten Zeilenmenge L.
Es sei bekannt, dass |Nⱼ|≤d gilt. Leere Zeilen und Spalten sind erlaubt.
Die vollständige Eingabe des Rekonstruktionsverfahrens besteht aus m,u,d sowie
den **zugeordneten** Werten

$$
g(S)=\#\{j:S\subseteq N_j\}\quad (S\subseteq L,\ |S|\le d),
\qquad g(\varnothing)=u.
$$

Auch Nullwerte und die jeweilige Teilmenge S gehören zur Eingabe. Es reicht
nicht, für jede Teilmengengröße nur die Häufigkeiten der Zahlen g(S) anzugeben.

**Aussage.** Diese Daten bestimmen das vollständige Multiset der Spaltennachbarschaften.
Für jede Teilmenge T mit |T|≤d ist ihre Spaltenmultiplizität

$$
a(T)=\#\{j:N_j=T\}
=\sum_{\substack{S\supseteq T\\ |S|\le d}}
(-1)^{|S|-|T|}g(S).
$$

**Beweis.** Nach der Definition gilt

$$
g(S)=\sum_{\substack{U\supseteq S\\ |U|\le d}}a(U).
$$

Einsetzen in die behauptete Inversion und Vertauschen der endlichen Summen ergibt

$$
\sum_{U\supseteq T}a(U)
\sum_{T\subseteq S\subseteq U}(-1)^{|S|-|T|}
=\sum_{U\supseteq T}a(U)(1-1)^{|U\setminus T|}
=a(T).
$$

Die Gradschranke erlaubt, alle größeren Mengen auszuschließen. Für T=∅ werden
auch leere Spalten wiedergewonnen; dafür ist g(∅)=u erforderlich. Jede Teilmenge
T wird anschließend genau a(T)-mal als Spalte ausgegeben. Dies rekonstruiert B
bis auf eine Spaltenpermutation und erhält die Zeilenlabels. ∎

Der Produzent berechnet dieselbe Inversion durch absteigende Subtraktion:
Nach den größeren T werden deren bereits bekannte Multiplizitäten von ihren
echten Teilmengen abgezogen. Der getrennte Prüfer verwendet direkt die
alternierende Summe. Beide prüfen die gesamte rekonstruierte Matrix unter
einer expliziten Spaltenpermutation, nicht nur Zeilen- oder Spaltengrade.

### Genaue Isomorphieaussage und Grenze

Für zwei Matrizen mit derselben angegebenen Seitengröße genügt eine Zeilenbijektion
π, unter der alle zugeordneten g-Werte übereinstimmen. Die Inversion liefert dann
dieselben Spaltennachbarschaften samt Multiplizitäten, also eine passende
Spaltenbijektion. Umgekehrt erhält jede solche Inzidenzisomorphie sämtliche g-Werte.

Damit ist die Information vollständig, **die Suche nach π ist aber weiterhin
eine Zuordnungs- beziehungsweise Isomorphieaufgabe**. Ein direktes Vergleichen der
beschrifteten Zahlenlisten ist kein permutationsinvarianter Fingerabdruck.
Die Rekonstruktion aus bekannten Zeilenlabels löst nicht automatisch diese Suche.

Für positive Zweischichtenordnungen C=[[0,B],[0,0]] sind die beiden Seiten durch
ihre Vorgänger-/Nachfolgergrade intrinsisch erkennbar. Bei isolierten Elementen
muss eine Seitenzuordnung zusätzlich angegeben sein; sie wird durch diesen Satz
nicht erschlossen. Für höhere Ordnungen mit mittleren Schichten wird hier kein
entsprechender Satz behauptet.

### Speicherbedarf

Pro Richtung werden vollständig

$$
E(m,d)=\sum_{k=0}^{d}\binom{m}{k}
$$

zugeordnete Einträge gespeichert. Für festes d ist diese Anzahl polynomial in m;
für d=m sind es 2ᵐ Einträge. Im Dateiformat enthält jeder Eintrag zusätzlich zur
Schnittzahl eine Teilmengenmaske. Das ist kein allgemeiner Kompressionsvorteil
gegenüber den m·u binären Einträgen der ursprünglichen Inzidenzmatrix.

## 2. Histogramme aller Schnittordnungen reichen allgemein nicht

Für jedes m≥6 konstruieren wir zwei m×m-Matrizen. Bei B₁ wird in einer einzigen
zyklischen Indexliste der Länge m in jeder Zeile i eine Eins in Spalte i und
in der zyklisch nächsten Spalte gesetzt. Bei B₂ erfolgt dasselbe unabhängig
in zwei aufeinanderfolgenden Blöcken der Längen 3 und m−3. Alle übrigen Einträge
sind null. Jeder Block hat mindestens drei Zeilen und Spalten.

Die Ordnungen Cᵣ=[[0,Bᵣ],[0,0]] haben jeweils 2m Elemente. Alle unteren Elemente
haben zwei Nachfolger, alle oberen zwei Vorgänger.

**Aussage.** In beiden Richtungen stimmen die vollständigen Histogramme der
gemeinsamen Nachbarzahlen über alle k-Teilmengen für jedes k=1,…,m überein:

| k | Gemeinsame Nachbarn | Zahl der Teilmengen |
|---:|---:|---:|
| 1 | 2 | m |
| 2 | 1 | m |
| 2 | 0 | binomial(m,2)−m |
| 3,…,m | 0 | binomial(m,k) |

**Beweis der Gleichheit.** Für k=1 folgt die Aussage unmittelbar aus dem Grad zwei.
Jede obere Spalte bestimmt ein Paar unterer Nachbarn. Die m so erhaltenen Paare
sind verschieden, da jeder Zyklusblock mindestens Länge drei hat. Daher teilen
genau m untere Paare genau einen oberen Nachbarn; alle anderen teilen keinen.
Ein oberes Element besitzt nur zwei Vorgänger, also können drei oder mehr
untere Elemente keinen gemeinsamen Nachfolger haben. Für die andere Richtung
gilt dieselbe Zählung mit vertauschten Seiten. ∎

**Beweis der Nichtisomorphie.** Vergisst man die Pfeilrichtung, ist die erste
Relation ein zusammenhängender Zyklus auf 2m Knoten. Die zweite besitzt zwei
Zusammenhangskomponenten mit sechs und 2(m−3) Knoten. Jede gerichtete Isomorphie
müsste auch diese Komponentenzahl erhalten. Sie existiert deshalb nicht, auch
nicht nach Zeitumkehr. ∎

Damit gibt es für **jede gerade Elementzahl n≥12** ein solches nichtisomorphes
Paar mit gleichen Schnittgrößen-Histogrammen sämtlicher Ordnungen in beiden
Richtungen. Höhere Schnittordnungen beheben den Verlust der Teilmengenzuordnung
somit allgemein nicht. Die endlichen Kontrollen m=6,7,8,9 prüfen Implementierung
und Formel; der Beweis für alle m beruht auf der obigen Konstruktion.

Diese Familie widerlegt ausschließlich die vollständigen gepoolten Schnittprofile
als universellen Identifikator. Sie wird nicht als Gegenbeispiel für die Kombination
mit H7, Q1 oder R2 behauptet. Auch die Vollständigkeit der **zugeordneten** Daten
aus Abschnitt 1 bleibt davon unberührt.

## 3. Quellen und Einordnung

Die Inversion ist die klassische Möbius-Inversion auf dem Booleschen Verband,
mit μ(T,S)=(−1)^(|S|−|T|) für T⊆S. Siehe die Lehrdarstellungen von
[Alexander Hulpke, Combinatorics, Möbius inversion](https://www.math.colostate.edu/~hulpke/lectures/m501/notes.html)
und [Stefan Felsner, Diskrete Strukturen, Abschnitt 24.5](https://page.math.tu-berlin.de/~felsner/Lehre/DSI23/Skript-DSI_2021.pdf).
Hier wird sie auf die Multiplizitäten binärer Spaltennachbarschaften angewandt.
Es gibt keine Neuheits-, Minimalitäts-, Physik- oder Kontinuumsbehauptung.
