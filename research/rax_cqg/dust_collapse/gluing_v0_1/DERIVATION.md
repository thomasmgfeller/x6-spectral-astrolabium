# CST-DUST: exakte Verklebung, offene physikalische Naht

Version 0.1 · 6. November 2026 · CST-DUST-GLUING-001

## Ergebnis und Geltungsbereich

Für jede endliche strikte partielle Ordnung wird die BDG-Wirkung exakt in zwei
induzierte Teilordnungen und einen Kopplungsbeitrag zerlegt. Für ein ausdrücklich
angenommenes, markierungstreues Zählmaß wird die zugehörige Amplitudenkomposition
bewiesen. Eine endliche Variationsidentität und eine Strombilanz ergänzen die
Konstruktion. Dies sind strukturelle Resultate, keine Herleitung einer physikalischen
vierdimensionalen Einstein-Staub-Dynamik oder ihrer zeitartigen Anschlussbedingungen.

Die Literatur kennt bereits BDG-Biaktionen [1]. Hier werden insbesondere die
Unterscheidung zwischen isoliert induzierten und eingebetteten Teilordnungen,
Symmetriefaktoren, exakte Verklebungskerne und die Grenzen grober Zustandsdaten
ausgearbeitet. Ein neuer universeller CST-GHY-Term wird nicht beansprucht.

Der lokale Plan wurde vor der Rechnung fixiert; sein SHA-256 steht in plan.sha256.
Dies ist keine externe Präregistrierung und keine unabhängige physikalische
Vorhersageprüfung. Die Definitionen und kleinen Referenzbeispiele sind bekannt.
Alle hier getesteten Toleranzen sind exakt null; keine Fließkommaschwelle wurde
nachträglich angepasst. Es gibt keine neuen dynamischen CST-Ensembles.

## 1. Träger, Wirkung und Begriffe

Sei C eine endliche Menge mit irreflexiver transitiver Relation ≺. Für x≺y sei

\[
I_C(x,y)=\{z\in C:x\prec z\prec y\},\qquad k_C(x,y)=|I_C(x,y)|.
\]

N_k zählt Paare mit genau k **inneren** Elementen. In Quellen, die mit N_1 für
Links beginnen, entspricht dies N_(k+1). Die vierdimensionale BDG-Kombination ist

\[
F_4(C)=|C|-N_0+9N_1-16N_2+8N_3
      =|C|+\sum_{x\prec y}w(k_C(x,y)),
\]

mit w(0),...,w(3)=(-1,9,-16,8), sonst w=0. In der Konvention von [1]

\[
S_4/\hbar=\kappa F_4,\qquad
\kappa={4\over\sqrt6}(\ell/\ell_P)^2,
\qquad \ell_P^2=8\pi G\hbar\quad(c=1).
\]

Diese rationalisierte Plancklänge ist von sqrt(Gℏ) zu unterscheiden. Das Symbol
z bezeichnet zunächst eine formale von null verschiedene Variable; die Lesart
z=exp(iκ) ist eine zusätzliche Phasenparametrisierung. Es wird kein κ angepasst.

Die endliche Testklasse enthält alle Ordnungen mit 1 bis 5 Elementen, unabhängig
von ihrer Dimension oder Mannigfaltigkeitsnähe. Die Verwendung von F_4 macht
diese Klasse nicht zu einem physikalischen vierdimensionalen Ensemble.

Eine Partition C=A⊔B dient zunächst nur der Buchhaltung. Für einen Staubball
müssen Materiegebiet, Außenraum, ihre zeitartige Materialgrenze und ein äußerer
Rechenrand erst physikalisch identifiziert werden. Eine willkürliche Färbung
leistet das nicht; ein Übergang von der periodischen Modellzelle zum endlichen
Ball folgt ebenfalls nicht aus der Partition.

## 2. Satz: vollständige Wirkungsverklebung

A und B tragen die aus C induzierten Relationen. F(A) und F(B) werden **isoliert**
berechnet: Zwischenpunkte außerhalb des jeweiligen Blocks zählen dort nicht.
Definiere

\[
X(A,B;C)=\sum_{\substack{x\prec y\\x,y\text{ in verschiedenen Blöcken}}}
w(k_C(x,y)),
\]

\[
R(A,B;C)=\sum_{D\in\{A,B\}}\sum_{\substack{x\prec y\\x,y\in D}}
\big[w(k_C(x,y))-w(k_D(x,y))\big].
\]

Dann gilt ohne Einbettung oder Grenzübergang

\[
\boxed{F(C)=F(A)+F(B)+X(A,B;C)+R(A,B;C).}
\]

**Beweis.** Die Elementzahlen addieren sich. Jedes geordnete Paar liegt entweder
vollständig in A, vollständig in B oder hat Endpunkte in verschiedenen Blöcken.
Bei den ersten beiden Klassen korrigiert R die veränderte Zahl der Zwischenpunkte;
bei der dritten Klasse liefert X den bislang fehlenden Beitrag. Die Klassen sind
disjunkt und vollständig. Die Argumentation gilt für jedes Intervallgewicht w.

Sind beide Blöcke ordnungskonvex, enthält jedes Intervall mit beiden Endpunkten
im Block auch alle Zwischenpunkte dort; dann R=0. Ordnungskonvexität ist eine
hinreichende Bedingung, keine notwendige Bedingung für zufällige numerische
Auslöschung von R. Für allgemeine, insbesondere nichtkonvexe Schnitte ist R nötig.

**Eingebettete Konvention.** Definiert man dagegen

\[
\bar F_C(A)=|A|+\sum_{x,y\in A,\ x\prec y}w(k_C(x,y)),
\]

so gilt F(C)=F̄_C(A)+F̄_C(B)+X. In dieser Konvention darf R nicht nochmals addiert
werden. Die eingebetteten Beiträge kennen bereits die Umgebung; sie sind keine
autonomen Wirkungen isolierter Innenräume. Dies präzisiert die Biaktionssicht [1].

**Explizite Negativkontrolle.** Für die Dreierkette a≺b≺c und A={a,c}, B={b} gilt

\[
F(C)=10,\quad F(A)=F(B)=1,\quad X=-2,\quad R=10.
\]

Nur die grenzüberschreitenden Paare zu ergänzen ergäbe 0 statt 10. Der interne
Paarbeitrag (a,c) wechselt von −1 zu +9. Auch bei konvexen Blöcken genügt die
naive Summe nicht: Die Viererkette hat F=3, ihre beiden Zweierketten zusammen F=2.

**Assoziativität.** Schreibe Δ(A,B)=F(A∪B)−F(A)−F(B), stets mit der korrekten
induzierten Ordnung auf dem jeweiligen Vereinigungsgebiet. Für drei disjunkte
Blöcke gilt durch Teleskopieren

\[
\Delta(A,B)+\Delta(A\cup B,D)
=\Delta(B,D)+\Delta(A,B\cup D)
=F(C)-F(A)-F(B)-F(D).
\]

Der Zwischenzustand muss die volle induzierte Ordnung und die Markierungen
bewahren. Eine skalare Zusammenfassung als Volumen oder Wirkungswert wird dadurch
nicht als hinreichend bewiesen; Abschnitt 5 widerlegt eine solche Schließung.

## 3. Verschmierung und physikalische Verfeinerung

Die verschmierte BDG-Formel [1] lässt sich für 0<ε≤1 mit einem gemeinsamen
Vorfaktor schreiben als F_ε=√ε G_ε, wobei

\[
G_\epsilon(C)=|C|-\epsilon\sum_{x\prec y}f_4(k_C,\epsilon),
\]

\[
f_4(k,\epsilon)=\sum_{m=0}^{\min(3,k)}c_m {k\choose m}
\epsilon^m(1-\epsilon)^{k-m},\qquad(c_0,c_1,c_2,c_3)=(1,-9,16,-8).
\]

Der Beweis aus Abschnitt 2 gilt mit w_ε=−ε f_4 und unverändertem ε in allen
Teilen. Bei ε=1 entstehen genau die unverschmierten Gewichte. Exakte rationale
Kontrollen verwenden ε=1/2 und 1/4 für N≤4. Die Skalierung mit √ε ist in diesen
Kontrollen ausgeklammert; ihre Auslassung ist kein Vergleich verschiedener
physikalischer Kopplungen.

Für eine spätere 4D-Familie ist ε=(ℓ/L_k)^4 mit Nichtlokalitätsskala L_k zu
berücksichtigen. ε zu wechseln oder N von 4 auf 5 zu erhöhen ist hier **keine
physikalisch abgeglichene Dichteverfeinerung**. Dafür müssten dieselbe materielle
Anfangssituation, Geometrie, physikalischen Skalen und Randbedingungen erhalten
werden. Eine solche Familie wird in diesem Paket nicht simuliert.

## 4. Zulässige Verklebungen, Maß und Amplituden

Für feste markierte induzierte Ordnungen A und B enthält G(A,B) genau jene
grenzüberschreitenden Relationen X, für die die Vereinigung der Relationen
irreflexiv und transitiv ist und beide vorgegebenen Einschränkungen erhält.
Blindes transitives Abschließen genügt nicht: Bei A={a,c} als Antikette und B={b}
erzwingt a≺b≺c nach Abschluss a≺c und verändert somit die vorgegebene Innenordnung.

### 4.1 Ausdrücklich bedingtes Maß

Als endliche Kontrollannahme werden beliebig gelabelte Ordnungen gleich gezählt
und durch n_A!n_B! dividiert. Isomorphismen erhalten alle Block- und Materiemarken.
Für eine invariante Funktion f liefert der Bahn-Stabilisator-Satz

\[
{1\over n_A!n_B!}\sum_{C\text{ gelabelt}}f(C)
=\sum_{[C]\text{ markiert}}{f(C)\over|\operatorname{Aut}_{A,B}(C)|}.
\]

**Beweis.** Die Gruppe S_(n_A)×S_(n_B) hat Ordnung n_A!n_B!. Jede Bahn enthält
deren Ordnung dividiert durch die Ordnung des markierungstreuen Stabilisators
viele gelabelte Vertreter. Auf einer Bahn ist f konstant; Division und Summation
ergeben die Formel. Bei weiteren fixierten Randlabels oder unterschiedlichen
Materiemarken ist die Gruppe entsprechend kleiner und neu zu bestimmen.

Diese Identität begründet den Symmetriefaktor **unter der genannten Annahme**.
Sie entscheidet weder ein fundamentalmaterielles Maß noch Zustandsgewichte,
relative Gewichte verschiedener N-Sektoren oder eine physikalische Normierung.
Beispiel: Die Viererantikette mit festen 2+2-Marken hat Aut-Ordnung 4, nicht 24.

### 4.2 Exakter Kern

Für je einen Vertreter der unmarkierten inneren Typen [A],[B] definiere

\[
K_{AB}(z)=\sum_{X\in G(A,B)}z^{\Delta F(C_X)},\qquad
\Delta F(C_X)=F(C_X)-F(A)-F(B).
\]

Dann ist im festen Größen- und Markierungssektor

\[
Z_{n_A,n_B}(z)=\sum_{[A],[B]}
{z^{F(A)+F(B)}\over |\operatorname{Aut}A||\operatorname{Aut}B|}K_{AB}(z).
\]

**Beweis.** Für jeden inneren Typ gibt es n_A!/|Aut A| und n_B!/|Aut B|
gelabelte Vertreter. Die entsprechenden Fasern G(A,B) werden durch Umbenennung
bijektiv aufeinander abgebildet. Aufteilung der vollständig gelabelten Summe
nach diesen Typen und Division durch n_A!n_B! ergeben die Formel. Äquivalent
wirkt Aut A×Aut B auf den Kreuzrelationen; deren Stabilisator ist Aut_(A,B)(C).
Das verhindert eine Doppelzählung des vollen markierten Kausalsets.

Für drei Blöcke folgen die entsprechende Maßkomposition und ihre Assoziativität
aus derselben endlichen Gesamtsumme. Es muss über vollständige zulässige
Zwischenordnungen summiert werden. Daraus folgt kein unitärer zeitlicher
Transferoperator durch eine zeitartige Materialfläche.

### 4.3 Vollständig ausgewerteter 2+2-Sektor

| Innere Typen A/B | Zulässige Kreuzordnungen | K(1) | K(−1) | K(i) |
|---|---:|---:|---:|---:|
| Antikette / Antikette | 35 | 35 | 3 | −13 |
| Antikette / Kette | 26 | 26 | 0 | 5−11i |
| Kette / Antikette | 26 | 26 | 0 | 5−11i |
| Kette / Kette | 20 | 20 | −4 | 2+8i |

Die Laurent-Polynome sind exakt

\[
K_{AA}=2z^{-4}+8z^{-3}+16z^{-2}+8z^{-1}+1,
\]
\[
K_{AK}=K_{KA}=z^{-19}+4z^{-2}+4z^{-1}+1+8z^7+6z^8+2z^{16},
\]
\[
K_{KK}=2z^{-18}+z^{-2}+2z^{-1}+1+6z+4z^8+4z^{17}.
\]

Die rekonstruierte Gesamtsumme stimmt koeffizientenweise mit der direkten
Enumeration aller 219 gelabelten Viererordnungen dividiert durch 4 überein:

\[
Z_{2,2}=3z^{-16}+\tfrac32+8z+9z^2+9z^3+\tfrac14 z^4
       +12z^{10}+6z^{11}+6z^{19}.
\]

Bei z=1 ist Z=219/4. Das Produkt isolierter Summen ohne Kopplung beträgt
z²+z³+z⁴/4, bei z=1 nur 9/4. Schon die unterschiedlichen Fasergrößen 35,26,20
zeigen, dass ein von A und B unabhängiger Faktor nicht alle bedingten Kerne ersetzt.

Die Werte sind Amplitudensummen, keine positiven Wahrscheinlichkeiten. K_AK(−1)=0
ist eine exakte Auslöschung an einer Kontrollphase. Ein effektiver Ausdruck
−iℏ log K kann daher komplex, mehrdeutig oder an Nullstellen undefiniert sein.
Dies allein beweist weder die Unterdrückung physikalischer Historien bei einem
gewählten κ noch die Existenz eines lokalen reellen Randpotentials.

## 5. Gegenbeispiel gegen den Zustand (N,F_4)

Betrachte V mit Relationen 0≺2,1≺2 und sein zeitliches Dual V* mit 0≺1,0≺2.
Beide haben N=3, F_4=1 und |Aut|=2. Ein neues maximales Element wird ergänzt;
seine Vergangenheit muss ein Ordnungsideal sein. Jede Ordnung hat fünf solche
Erweiterungen. Mit der **Gesamtänderung**, einschließlich des neuen Elements,
ΔF=F(C_neu)−F(C_alt), sind die Zukunftskerne

\[
L_V=z^{-1}+2+z+z^{18},\qquad
L_{V^*}=z^{-17}+1+z+2z^9.
\]

L_V(1)=L_V*(1)=5, aber L_V(i)=1 und L_V*(i)=1+2i. Eine reine
(N,F_4)-Zustandsbeschreibung kann diese beiden exakten konditionierten
Fortsetzungsamplituden nicht unterscheiden und ist daher für diese Komposition
nicht geschlossen. Auch gleiche Anzahlen zulässiger Fortsetzungen genügen nicht.

Die gemeinsame neue Einzelelement-Wirkung wäre bei der Definition aus Abschnitt 4
noch als Faktor z abzutrennen. Dieser gemeinsame Faktor ändert das Gegenbeispiel
nicht. V und V* werden nicht unter zeitumkehrenden Isomorphismen identifiziert:
Die Zukunftsrichtung ist Teil des Problems.

Dies ist eine zeitliche Strukturkontrolle, keine Simulation der zeitartigen
Stauboberfläche. Es widerlegt nicht jede denkbare grobe Volumentheorie; eine
solche Theorie benötigt jedoch zusätzliche Zustandsdaten oder eine begründete
Näherung einschließlich Gedächtnis- und Fehlerkontrolle.

## 6. Endliche Variationsidentität und Strombilanz

### 6.1 Variable ersetzen statt mikroskopisch ΔS=0 fordern

In einer festen gelabelten Faser G(A,B) wähle ein gerichtetes Kreuzpaar. T fügt
seine Relation hinzu oder entfernt sie genau dann, wenn das Ergebnis wieder in
der Faser liegt; sonst lässt T die Ordnung unverändert. Dann ist T eine Involution.
Für jede Funktion f und z≠0 gilt

\[
\sum_C z^{F(C)}\left[f(TC)z^{F(TC)-F(C)}-f(C)\right]=0.
\]

**Beweis.** Der erste Summand ist f(TC)z^(F(TC)). Die Bijektion C↦TC benennt die
endliche Summe nur um. Es entsteht genau die zweite Summe. Bei allgemeinen
Gewichten ersetzt w(TC)/w(C) den Phasenquotienten, soweit der Quotient definiert
ist. Die quotientfreie Summenform bleibt auch bei Nullgewichten sinnvoll.
Maß-, Materie- und Zustandsfaktoren dürfen dabei nicht weggelassen werden.

Getestet werden f=#Relationen und acht gerichtete Kreuzpaare in jeder der vier
2+2-Fasern: 32 exakte Polynomidentitäten mit 400 nichttrivialen Bewegungsinstanzen.
Die Summation erfolgt gelabelt, daher entsteht hier kein unberücksichtigter
Aut-Quotient. Auf Isomorphieklassen müsste ein entsprechender Move erst mit
korrekter Gewichtung definiert werden.

Die Identität ist eine notwendige Konsistenzkontrolle für die vollständige
gewichtete Summe, kein Selektionsprinzip für das physikalisch richtige Gewicht.
Sie begründet insbesondere nicht ΔS=0 für jede diskrete Mikrobewegung und noch
kein Israel-Gesetz. Die Abbildung solcher Moves auf makroskopische
Randdeformationen bleibt offen.

### 6.2 Bilanz auf demselben Gesamtkausalset

Sei j_ij ein gerichteter Strom auf ausgewählten kausalen Kanten. Setze
q_i=Σ_j j_ij−Σ_j j_ji. Für jede Teilmenge A gilt

\[
\sum_{i\in A}q_i=\sum_{i\in A,j\notin A}j_{ij}
                 -\sum_{i\notin A,j\in A}j_{ij}.
\]

**Beweis.** Interne Kanten erscheinen einmal mit Plus und einmal mit Minus;
nur grenzüberschreitende Kanten bleiben übrig. Die numerischen Kontrollen setzen
j=1 auf den Überdeckungsrelationen des **vollen** Kausalsets. Diese Testströme
haben im Allgemeinen Quellen q und sind keine Lösungen druckloser Staubbewegung.
Bei der Dreierkette ist q=(1,0,−1). Abschneiden der Kreuzkanten verliert die
zugehörige Bilanz gegenüber diesen ursprünglichen Quellen.

Eine mitbewegte Materie-Vakuum-Grenze muss zusätzlich den physikalisch passenden
verschwindenden Staubfluss erfüllen. Die Identität allein wählt weder diese
Grenze noch Vierergeschwindigkeit, Geodäten, Stress oder Rückwirkung. Restmassen-
bilanz ist nicht gleich einer allgemeinen Bilanz gravitativer Energie.

## 7. Was zum physikalischen Anschluss fehlt

GHY-Beiträge dienen dem wohldefinierten Variationsprinzip; Israel-Bedingungen
beschreiben den zulässigen Anschluss einschließlich möglicher Oberflächenspannung.
Die mathematischen Formen müssen auf dem Kausalset nicht vorausgesetzt werden.
Der physikalische Zweck verlangt jedoch eine konsistente gemeinsame Variation
bzw. Quantensumme einschließlich Materie, Außenraum und Randzustand.

Eine schematische physikalische Gewichtung wäre

\[
W(C,\phi)=\mu(C,\phi)\,\Psi_{\partial}(C,\phi)
\exp\{i[S_{\rm BDG}(C)+S_{\rm dust}(C,\phi)]/\hbar\}.
\]

μ, die diskreten Staubvariablen φ, ihre Wirkung, der Zustand Ψ_∂ und ein geeignetes
Dekohärenz- oder Wahrscheinlichkeitsverfahren sind hier nicht festgelegt. Nach
deren Festlegung muss über zulässige gemeinsame Historien und alle kompatiblen
Materie-/Grenzdaten summiert werden. Kreuzkopplungen der Materie gehören zusätzlich
zur hier berechneten gravitativen ΔF. Eine Mittelung des Außenraums benötigt eine
angegebene Zustands- und Beobachtungsregel; ein Produkt zweier unabhängiger
Amplituden ersetzt sie nicht.

### 7.1 Warum ein GHY-Mittelwertgrenzfall nicht genügt

Buck et al. [2] konstruieren raumartige CST-Randterme mit GHY-Grenzwert im Mittel.
Die dort untersuchte Klasse ist von einer zeitartigen Staub-Vakuum-Naht zu
unterscheiden. Dowker et al. [1] untersuchen Biaktionen und geben Evidenz für
eine mit ℓ^−1 divergierende mittlere Wirkung an zeitartigen Gebietsgrenzen in
den untersuchten Sprinkling-Situationen. Dies ist kein allgemeiner Beweis über
Materiegrenzen und liefert nicht unmittelbar ein CST-Staub-Anschlussgesetz.

Selbst gleichmäßige Konvergenz einer Wirkung genügt nicht für ihre erste Variation:

\[
S_n(q)=S(q)+{\sin(n^2q)\over n},\qquad
\sup_q|S_n-S|\le 1/n,
\]

\[
\left.\left({dS_n\over dq}-{dS\over dq}\right)\right|_{q=0}=n.
\]

Das ist ein analytisches Gegenbeispiel zur Schlussregel „Wirkungsgrenzwert ⇒
Variationsgrenzwert“, keine Aussage, dass CST selbst diesen Fehler besitzt.

### 7.2 Bedingte klassische Brücke

Erforderlich ist eine physikalisch abgeglichene Familie mit kontrollierter
effektiver Gesamtwirkung **und** kontrollierten ersten Variationen unter
denselben Materie- und Randdeformationen. Fluktuationen, seltene Ausreißer,
Nichtlokalität, Renormierung und Zustand dürfen diesen Übergang nicht vereiteln.

Falls diese Kontrolle einen lokalen Einstein-Grenzfall mit korrekt orientierten
GHY-Beiträgen und gegebenenfalls Schichtwirkung liefert, ergibt die stationäre
klassische Variation die bekannte Darmois-Israel-Naht [3]. Für eine zeitartige
Fläche, Signatur (−+++), K_ab=h_a^μ h_b^ν∇_μ n_ν, eine gemeinsame vom Inneren
zum Äußeren gerichtete Normale und [Q]=Q_+−Q_- lautet sie

\[
[h_{ab}]=0,\qquad [K_{ab}-Kh_{ab}]=-8\pi G\,S^{\Sigma}_{ab}.
\]

Ohne dünne Materieschicht verschwindet die rechte Seite. Dies ist eine
**bedingte Zielprüfung**, keine aus den endlichen Kontrollen abgeleitete Grenze.
In der Quantenzone darf die klassische Gleichung nicht vorausgesetzt werden,
um erst nachträglich ein gewünschtes Bounce-Innere anschlussfähig zu machen.

## 8. Verifikation und Entscheidungen

Die Enumeration erzeugt 1,3,19,219,4231 beliebig gelabelte Ordnungen für N=1,...,5,
zusammen 4473, mit 1,2,5,16,63 unmarkierten Isomorphietypen. Geprüft wurden:

| Prüfung | Anzahl | Entscheidung |
|---|---:|---|
| Vollständige Zweiblock-Wirkung | 130116 | alle Reste exakt null |
| Verschmierte rationale Wirkung | 6372 | alle Reste exakt null |
| Stromschnittbilanz | 130116 | alle Reste exakt null |
| Geordnete Dreiblock-Assoziativität, N≤4 | 7998 | alle Reste exakt null |
| Markierte Maßsektoren, N=2,...,5 | 10 | exakte Polynomgleichheit |
| Markierte Bahn-Stabilisator-Prüfungen | 1549 | alle exakt |
| 2+2-Kerne / endliche Variationsidentitäten | 4 / 32 | exakt |
| Struktur- und Negativkontrollen | 13 | erwartete Ergebnisse |
| Zusätzliche synthetische Gate-Negativkontrollen | 5 | unzulässige Hochstufung abgewehrt |

Ohne Kopplung scheitert die Additivität in 122960 der 130116 Zerlegungen; ohne
R scheitert sie in 45888. Dies sind kombinatorische Häufigkeiten, keine unabhängigen
Stichproben und keine physikalischen Fehlerraten.

verify_independent.py erzeugt dieselbe Klasse über vorwärts gerichtete Graphen,
transitiven Abschluss und alle Permutationen. Mengenbasierte Intervallzählung
prüft unabhängig die 4473 Wirkungswerte und 130116 Kopplungskorrekturen. Dies ist
ein Implementierungsabgleich zum unveränderten Plan, kein neues physikalisches
Experiment und kein Ersatz für den allgemeinen Beweis.

Ein einzelner neuer P5-Datensatz des unveränderten Model Contract dokumentiert
den vorliegenden Teilumfang. Alle acht physikalischen Gates bleiben HOLD. Das
setzt frühere, anders abgegrenzte klassische Kontrollen nicht nachträglich zurück.
Die fünf separaten Gate-Tests verwenden ausdrücklich synthetische Nachweisfelder;
der Auditor prüft deren Kategorien, nicht die Gültigkeit zitierter Beweise.

| Aussage | Ergebnis |
|---|---|
| Exakte finite BDG-Wirkungsverklebung | PASS_EXACT_FINITE_IDENTITY |
| Komposition unter angegebenem Zählmaß | PASS_CONDITIONAL_COUNTING_MEASURE |
| Endliche Variationsidentität | PASS_EXACT_FINITE_IDENTITY |
| Physikalisches CST-Staub-Anschlussgesetz | HOLD_NOT_DERIVED |
| Globaler CST-Bounce | HOLD_NOT_RUN |
| Regularität von Dichte/Krümmung unter Verfeinerung | HOLD |
| Globale kausale Fortsetzbarkeit | HOLD |

**Nächster physikalischer Engpass:** Ein konkretes diskretes Staubmodell mit
begründetem Maß und Zustand muss mit der vollständigen Geometrie gekoppelt
werden. Danach ist zuerst im regulären klassischen Bereich die gemeinsame
Variation an einem endlichen Staubball gegen die bekannte Naht zu prüfen.
Toleranzen, Skalenabgleich und Abbruchregeln werden vor dieser neuen Rechnung
festgelegt. Erst anschließend sind Hochkrümmungsbereich, Regularität und globaler
Bounce zu entscheiden. Der jetzige Befund legt kein positives Bounce-Ergebnis fest.

## Quellen und Herkunft

[1] F. Dowker, R. Liu, D. Lloyd-Jones, *Timelike boundary and corner terms in the
causal set action*, arXiv:2501.00139v2 (25.04.2025), insbesondere Biaktion und
isoliertes/eingebettetes Regime; Anhang A, Gleichungen 78 und 83–84.
https://arxiv.org/html/2501.00139v2

[2] M. Buck, F. Dowker, I. Jubb, S. Surya, *Boundary Terms for Causal Sets*,
arXiv:1502.05388v2 (29.10.2015).
https://arxiv.org/abs/1502.05388v2

[3] P. Musgrave, K. Lake, *Junctions and thin shells in general relativity using
computer algebra I: The Darmois-Israel Formalism*, Class. Quantum Grav. 13
(1996), 1885–1900, arXiv:gr-qc/9510052v3.
https://arxiv.org/abs/gr-qc/9510052v3

Projektbasis: thomasmgfeller/x6-spectral-astrolabium, Main-Commit
bc8c154be60c483c8a5a8f085c1b3b0668d8afa1, nach PR 243.
Die unveränderten Eingaben und ihre Hashes stehen in inputs/provenance.json.
Die hier ausgearbeiteten algebraischen Folgerungen sind von den zitierten
Literaturresultaten und von den noch offenen physikalischen Behauptungen getrennt.
