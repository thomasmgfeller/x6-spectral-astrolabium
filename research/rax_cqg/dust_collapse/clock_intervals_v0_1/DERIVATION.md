# CST-DUST: Feste Uhrintervalle und variable Elementzahl v0.1

7. November 2026. Basis: Main `3a26651cb1476b5e3b5d89c343e11487a012e432`
nach PR 252, `thomasmgfeller/x6-spectral-astrolabium`.
Prüfplan: `CST-DUST-CLOCK-INTERVAL-001`.

## Ergebnis und Aussagegrenze

Eine Fortsetzung zwischen festen Materieuhrwerten mit keiner, einer oder
mehreren Geburten lässt sich auf vollständigen vergangenen Historien exakt
zusammensetzen. Das behebt die Verwechslung von Geburtsnummer und Uhrzeit.
Es legt aber weder ein physikalisches Skalarprodukt noch die Gewichtung
unterschiedlicher Elementzahlen fest.

Die Prüfung liefert einen Ausschluss und eine bedingte Konstruktion:

1. Mit dem geerbten Betrag-eins-Koeffizienten, einem konstanten von null
   verschiedenen Geburtsfaktor und dem lokalen orthogonalen Historien-L2-
   Produkt divergiert die Norm auf jedem positiven Uhrintervall, sobald
   die Elementzahlgrenze entfernt wird. Eine elementare Zweischichtfamilie
   genügt als Beweis; keine KR-Asymptotik oder Kontinuumsnäherung ist nötig.
2. Explizite, ausschließlich von der Gesamtzahl abhängige Endpunktgewichte
   können diese Summe kontrollieren und die Komposition erhalten. Zwei
   Beispiele werden konstruiert. Sie sind zusätzliche Modellentscheidungen,
   keine aus der CST-Wirkung gewonnenen Kopplungen.
3. Ein **gemeinsamer Enduhrwert** und dessen verbleibende Zustandssumme
   liefern einen exakt normerhaltenden, kompatiblen Referenztransport.
   Eine getrennte Neunormierung jedes Einzelintervalls hätte diese
   Komposition nicht. Die Konstruktion ist eine Isometrie; Surjektivität,
   ein physikalischer Hamiltonoperator und eine Constraint-Reduktion
   werden nicht behauptet.
4. Die beiden gleich konsistenten Gewichte liefern nachweislich verschiedene
   Wahrscheinlichkeiten. Die mathematischen Bedingungen wählen deshalb
   die Physik noch nicht aus. Die diagonalen Historienwahrscheinlichkeiten
   dieser Referenz sind zudem blind gegenüber der reellen Wirkungsphase.

**Alle acht übergeordneten Gates MODEL, CURRENT, CORRESPONDENCE, BOUNCE,
REGULARITY, BOUNDARY, TRAPPING, EXTENSION bleiben HOLD.** Der unveränderte
unbegrenzte lokale-L2-Kandidat ist FAIL. Die vervollständigte Konstruktion
ist PASS nur als ausdrücklich bedingte mathematische Referenz. Dies ist
kein allgemeines No-go für CST, kein Nachweis physikalischer Explosion und
kein Bounce-Ergebnis. Frühere spezifische FAILs bleiben erhalten.

## 1. Festgelegter Raum, Maße und Uhr

Beibehalten werden der ausgewählte kausal monotone Uhrsektor, verschiedene
Uhrwerte, chronologische Beschriftung und die gesamte vergangene Ordnung
einschließlich aller T- und w-Marken. Das geerbte Maß lautet

\[
d\nu_T=dT/(2L)=ds,\quad s=(T+L)/(2L)\in[0,1],\qquad
d\nu_w=\tfrac12\delta_0+\tfrac12\mathbf1_{(0,1)}dw. \tag{1}
\]

In den folgenden Formeln sind a,b,c und der Enduhrwert t_* **normierte
Uhrwerte s**; h=b-a ist dimensionslos. Die endlichen Wirkungsprüfungen
speichern weiterhin die ursprünglichen rationalen T-Werte bei L=1.
Eine Rate pro s ist noch keine kalibrierte physikalische Rate.

Der Hilfsraum am Schnitt a ist

\[
\mathcal H_a^{(N)}=\bigoplus_{m=0}^{N}\ \bigoplus_{P\in\Omega_m^{nat}}
L^2(0<s_1<\cdots<s_m\le a,\,d s^m d\nu_w^m). \tag{2}
\]

Für N=∞ ist dies die Hilbert-Direktsumme über endliche Historien. Die
leere Geschichte ist ein eindimensionaler Block. Ein Schnitt in einer
vollständigen chronologischen Geschichte Y ist ihr eindeutiges Präfix
Y_a mit s≤a. Die relative Zukunft enthält alle Idealerweiterungen und
Uhren in (a,b]. Wegen der eindeutigen Uhrsortierung tritt beim Zerlegen
des Produktmaßes kein weiterer Binomial- oder Permutationsfaktor auf.

Ein einzelner fixer Anfangsanker liegt wie im Vorgänger unter allen inneren
Elementen. An Zwischen-Uhrschnitten wird **kein neuer Endanker eingefügt**.
Die offene reelle Wirkung S enthält die geerbte Gravitation und Materie:

\[
S_g=n-\sum_{y\prec x} b(k(y,x)),\quad
S_d=-\tfrac12\sum_xw_x-\tfrac14\sum_{y\prec x}w_x b(k(y,x))(T_x-T_y)^2,
\quad b=(1,-9,16,-8,0,\ldots). \tag{3}
\]

Kopplungen und ℏ können wieder eingesetzt werden; alle Normargumente
benötigen nur eine reelle Wirkung. Im exakten Code werden S_g und S_d
getrennt mit rationalen Zahlen geprüft. Eine physikalische Endkontraktion,
die Außenraumvariation und eine globale materielle Vakuumuhr bleiben offen.
Weder Γ=-1 noch andere physikalische Constraints sind in (2) auferlegt.

## 2. Variable Geburtenzahl und exakte Komposition

Sei f(m)>0 eine zunächst frei gewählte Zahlgewichtung und z ein konstanter
komplexer Faktor pro Geburt. Der Fall f=1,z=1 setzt die chronologischen
Koeffizienten des Vorgängers ohne weitere Zahlgewichtung fort. Für eine
Endgeschichte Y am Schnitt b mit n Elementen und X=Y_a mit m Elementen:

\[
(U^{f,z,N}_{b,a}\psi)(Y)=
z^{n-m}\frac{f(n)}{f(m)}
\exp\{i[S(Y)-S(X)]/\hbar\}\,\psi(X),\qquad n\le N. \tag{4}
\]

Bei keiner Geburt ist der Koeffizient eins. Die Formel benutzt die
vollständige Vorgeschichte, nicht nur die letzte Antikette oder ein
isoliertes neues Intervall. Für a<b<c gilt exakt

\[
U^{f,z,N}_{c,b}U^{f,z,N}_{b,a}=U^{f,z,N}_{c,a},\quad U_{a,a}=I. \tag{5}
\]

**Beweis.** Y_b ist eindeutig. Geburtsexponenten addieren sich, f(|Y_b|)
kürzt sich und die beiden Wirkungsdifferenzen teleskopieren. Dies gilt
punktweise für alle Marken. Die gemeinsame Obergrenze betrifft die
**Gesamtzahl N**, also denselben Zustandsraum in allen Faktoren. ∎

Eine erneut pro Intervall erlaubte Zusatzgeburtszahl ist eine andere
Regel: Bei „höchstens eine Geburt“ kann ein zusammengesetztes Paar von
Intervallen zwei Geburten enthalten, das direkte Intervall dagegen nicht.
Ebenso darf kein zusätzlicher Faktor 1/k! in (4) eingefügt werden: Die
geordnete k-Uhrintegration enthält das Simplexvolumen h^k/k! bereits.
Ein nochmals eingefügtes 1/k! verletzt z^(j+k)=z^j z^k für j,k>0.

Innerhalb der engeren Klasse von Koeffizienten c_k, die nur von der
hinzugekommenen Zahl k abhängen, nicht vom Ausgangszustand oder Intervall,
erzwingt Komposition c_0=1 und c_(j+k)=c_j c_k, also c_k=z^k.
Das verbietet **keine** Größe-abhängige Gewichtung: Der Quotient f(n)/f(m)
ist gerade ein zulässiger Endpunkt-Kozyklus außerhalb dieser engeren
Klasse. Auch zeit- oder zustandsabhängige andere Regeln sind nicht durch
diese einfache Klassifikation ausgeschlossen.

### Weshalb die Vergangenheit benötigt wird

Für zwei innere Elemente in einer Kette, T=(0,1/2), w=(0,1/2), liefert
die volle Anfügung an die alte Ein-Element-Geschichte
`(ΔS_g,ΔS_d)=(9,27/4)`. Wird nur das neue Element mit einem isolierten
Anfangsanker behandelt, erhält man `(0,-33/32)`. Die über den Schnitt
reichenden Intervalle und Materiepaare fehlen. Die unabhängige Rechnung
über die geerbten Moment-Inkremente stimmt mit der vollständigen Wirkung
überein. Die Komposition (5) ist kein Markov-Ansatz auf einer verkleinerten
Antikettenzustandsmenge.

## 3. Die exakte Norm ist eine Erweiterungs-Zustandssumme

E_P(k) sei die Zahl chronologisch gelabelter k-Erweiterungen eines
gegebenen alten P. Es gilt

\[
E_P(0)=1,\qquad E_P(k+1)=\sum_{J\in\mathrm{Ideals}(P)}E_{P+J}(k). \tag{6}
\]

Da jede Endgeschichte genau ein altes Präfix besitzt, gibt es in der
lokalen Historiennorm keine kohärente Zusammenführung verschiedener
Präfixe am gleichen Y. Die Phase in (4) hebt sich auf. Setze q=|z|²:

\[
(U_{b,a})^\dagger U_{b,a}=Z_N(P,h)\quad\text{als Multiplikationsoperator},
\]
\[
Z_N(P,h)=\sum_{k=0}^{N-m} E_P(k)q^k
 \left[\frac{f(m+k)}{f(m)}\right]^2\frac{h^k}{k!},\quad m=|P|. \tag{7}
\]

Integration der neuen Dichtefelder ergibt eins, die Uhrintegration h^k/k!.
Das Ergebnis gilt auch bei nichtverschwindender Gravitations- und
Materiekopplung. Ist qh>0 und m<N, dann ist Z_N>1: Schon der Keine-Geburt-
Ausgang trägt Norm eins, und neue orthogonale Ausgänge kommen hinzu.
Für f=1, N=3, h=1/4, z=1 sind die Normfaktoren eines alten
Zweierantikettenblocks **2** und eines Zweierkettenblocks **7/4**. Eine
einzige skalare Gesamtnormierung macht nicht beide zu Isometrien.

Die unabhängige Enumeration aller oberen Relationsdreiecke mit
Transitivitätsprüfung ergibt |Ω_n^nat| für n=0,...,6:
`1, 1, 2, 7, 40, 357, 4824`. Sie stimmt mit der sukzessiven
Idealerzeugung überein. E_P(k) wird zusätzlich durch Präfixfilterung
dieser unabhängig erzeugten Endordnungen geprüft.

## 4. Ohne Zahlgewicht divergiert die lokale Historiennorm

**Satz.** Für f=1, jedes qh>0 und jedes endliche alte P ist
Z_∞(P,h)=∞. Damit liefert (4) auf der lokalen Direktsumme keinen
L2-Zustand aus einem von null verschiedenen Eingangsvektor.

**Beweis.** Füge alle k neuen Elemente oberhalb des gesamten alten P an.
Teile die neuen chronologischen Labels in a=floor(k/2) untere und
b=ceil(k/2) obere Elemente. Innerhalb jeder Schicht gibt es keine
Relationen; jede der a·b unteren-zu-oberen Relationen darf unabhängig
vorhanden oder abwesend sein. Diese 2^(ab) Ordnungen sind transitiv,
verschieden und alle durch Idealerweiterungen erreichbar. Daher

\[
E_P(k)\ge2^{\lfloor k^2/4\rfloor}. \tag{8}
\]

Für x=qh und k=2r ist ein unterer Summand B_(2r)=2^(r²)x^(2r)/(2r)!.
Sein exaktes Zweierschrittverhältnis lautet

\[
\frac{B_{2r+2}}{B_{2r}}=
\frac{2^{2r+1}x^2}{(2r+2)(2r+1)}\longrightarrow\infty. \tag{9}
\]

Die positiven Summanden gehen nicht einmal gegen null. Mit Tonelli gilt
die unendliche Norm auch für jedes nichtverschwindende Eingangs-L2-Paket:
Für fast jeden alten Datensatz mit |ψ|>0 ist seine Erweiterungsnorm
unendlich. ∎

Schon x=1/4 kann bei kleinen Elementzahlen harmlos aussehen; die
quadratische Zweischichtentropie setzt sich asymptotisch trotzdem durch.
Die endlichen Kontrollen illustrieren (8)-(9), ersetzen den Beweis aber
nicht. Ein konstanter, noch so kleiner von null verschiedener z-Faktor
beseitigt diese Divergenz nicht.

Für einen fixen alten Datensatz und eine feste Endzeit verschwindet im
normierten, aber ungedämpften N-Modell bei N→∞ die Wahrscheinlichkeit
jeder festen endlichen Geburtszahlmenge: Ihr endlicher Zähler bleibt
konstant, während Z_N wächst. Das ist kein Grenzwahrscheinlichkeitsmaß
auf der Vereinigung endlicher Records. Eine andere Grenzraumkonstruktion
wird damit weder geliefert noch allgemein ausgeschlossen.

**Geltungsbereich:** Die Quadratsumme behandelt vollständige Historien als
orthogonale Records. In einer oszillierenden skalaren Gesamtsumme können
andere Auslöschungen auftreten; (9) beweist nicht deren Fehlen. Andere
Skalarprodukte, Quantenmaße, Sektoren oder physikalische Constraints sind
nicht erfasst. Der Satz ist keine Behauptung über eine physikalische
Singularität oder die gesamte CST. Die konstruktive Zweischichtfamilie
ist keine Behauptung einer KR-Mehrheit.

## 5. Eine kontrollierte Zahlgewichtung erhält die Komposition

Als ausdrücklich neue Kandidaten wählen wir

\[
f_\alpha(n)=2^{-\alpha n(n-1)/4},\qquad \alpha=1\text{ oder }2. \tag{10}
\]

Bei festem Ausgangs-m und End-n ist dies ein gemeinsamer Skalar; die
relativen Geometrie- und Feldamplituden innerhalb dieser Größen bleiben
erhalten. Zwischen verschiedenen Größen ändern sich die Amplituden.
Es ist keine unitäre Eichumbenennung und keine aus (3) hergeleitete
Kopplung. Der Endpunktquotient in (4) erhält dennoch (5).

**Uniforme Schranke.** Jede neue Geburt j hat höchstens 2^(m+j) Ideale.
Daher gilt E_P(k)≤2^[mk+k(k-1)/2]. Für α≥1:

\[
E_P(k)\left[\frac{f_\alpha(m+k)}{f_\alpha(m)}\right]^2\le1,
\quad 1\le Z_\infty(P,h)\le e^{qh},\quad \|U^{f,z}_{b,a}\|^2\le e^{qh}. \tag{11}
\]

Dies ist uniform in der alten Größe und Geometrie. Die direkten Summen
definieren deshalb beschränkte Operatoren auch ohne Elementzahlgrenze.
Sie bleiben wegen Z>1 bei qh>0 zunächst nicht normerhaltend.
Für eine Abschneidung nach K Geburten ist der Rest für qh<K+2 beschränkt:

\[
0\le Z_\infty-Z_{m+K}\le
\frac{(qh)^{K+1}}{(K+1)!}\frac1{1-qh/(K+2)}. \tag{12}
\]

Der erste ausgelassene Exponentialreihenterm und eine geometrische
Majorante aller folgenden Quotienten beweisen (12). Bei q=1, h=1/2,
K=6 ist die Schranke **1/604800**. Sie umfasst alle noch nicht enumerierten
Geometrien und alle kontinuierlichen Marken im erklärten Referenzmaß.
Sie ist keine Unsicherheitsbilanz für eine physikalische Staubballsimulation.

Es wird keine Eindeutigkeit oder optimale Dämpfung behauptet. Insbesondere
können weitere Endpunktprofile ebenfalls konvergieren. Die Wahl (10)
zeigt nur, dass die kombinatorische Hürde durch eine transparente zusätzliche
Zahlregel kontrollierbar ist, ohne das Kompositionsgesetz zu verlieren.

## 6. Normerhaltender Transport braucht einen gemeinsamen Enduhrwert

Für denselben globalen N und dasselbe f,z gilt die exakte Identität

\[
Z_N(P,s+t)=\sum_{j=0}^{N-m} q^j\left[\frac{f(m+j)}{f(m)}\right]^2
\frac{s^j}{j!}\sum_{Q\supset_jP} Z_N(Q,t). \tag{13}
\]

Jede Endgeschichte zerfällt eindeutig am Uhrschnitt. Feldmaße faktorisieren;
die geordneten Zeitvolumina beider Teilintervalle liefern die binomische
Zerlegung des vollständigen Simplex. Die Endpunktgewichte kürzen sich.
Die positiven Summen erlauben dieselbe Identität für N=∞ mit (10),
kontrolliert durch (11)-(12).

Fixiere nun einen **gemeinsamen** Enduhrwert t_*≥b≥a. Definiere

\[
(K^{t_*}_{b,a}\psi)(Y)=
\sqrt{\frac{Z_N(P_Y,t_*-b)}{Z_N(P_X,t_*-a)}}
(U_{b,a}\psi)(Y),\qquad X=Y_a. \tag{14}
\]

Hier P_X und P_Y sind die Geometrien der vollständigen jeweiligen Präfixe.
Z≥1 verhindert Division durch null. Mit (13) folgt

\[
(K^{t_*}_{b,a})^\dagger K^{t_*}_{b,a}=I,\qquad
K^{t_*}_{c,b}K^{t_*}_{b,a}=K^{t_*}_{c,a}. \tag{15}
\]

Die erste Gleichung ist (13) nach Division durch Z_N(P_X,t_*-a).
In der zweiten kürzen sich die beiden mittleren Z-Wurzeln zusätzlich
zu (5). Der Schluss gilt für jedes Eingangs-L2-Paket, nicht nur für eine
Präparation. Am Endpunkt t_* ist der Z-Zähler eins, also
K_(t_*,a)=U_(t_*,a)/sqrt(Z_N(P_X,t_*-a)). Die zusätzliche Normierung
ist abhängig vom alten Zustand und gemeinsamen Endhorizont.

Eine unabhängige Neunormierung jedes Intervalls mit seinem **eigenen**
Endpunkt wäre dagegen falsch. Für f=1,z=1,N=2 und leeres P gilt
Z(P,h)=1+h+h². Für zwei Viertelintervalle:

\[
Z(P,1/4)^2=441/256\ne448/256=Z(P,1/2). \tag{16}
\]

Schon der Keine-Geburt-Pfad hätte unterschiedliche direkte und
zusammengesetzte Koeffizienten. Mit dem gemeinsamen t_*=1/2 erhält man
dagegen für keine Geburt bis zur Hälfte 3/4, anschließend bedingt 16/21;
das Produkt ist 4/7, genau die direkte Keine-Geburt-Wahrscheinlichkeit.

### Zugehörige Referenzraten und endliche Geburtenzahl

Die verbleibende Zustandssumme erfüllt die Rückwärtsgleichung

\[
\partial_h Z_N(P,h)=\sum_{J\in\mathrm{Ideals}(P)}
q\left[\frac{f(m+1)}{f(m)}\right]^2 Z_N(P+J,h),\quad Z_N(P,0)=1, \tag{17}
\]

wobei die Summe bei m=N null ist. Die bedingte Rate eines Ideals J
zur aktuellen Uhr s kann als

\[
\lambda_J(P,s)=q\left[\frac{f(m+1)}{f(m)}\right]^2
\frac{Z_N(P+J,t_*-s)}{Z_N(P,t_*-s)} \tag{18}
\]

gelesen werden. Ihre Summe ist ∂_h log Z_N(P,h) bei h=t_*-s.
Die Überlebenswahrscheinlichkeit ohne Geburt zwischen a und b ist
Z_N(P,t_*-b)/Z_N(P,t_*-a). Diese Warte- und Sprungfaktoren reproduzieren
(14); sie sind nicht nachträglich einzeln an die Resultate angepasst.

Für (10), N=∞ und einen festen maximalen normierten Horizont H gilt
Σ_J λ_J≤q e^(qH): Es gibt höchstens 2^m Ideale, während der quadrierte
Ein-Geburts-Faktor höchstens 2^(-m) ist, Z_Kind≤e^(qH) und Z_Eltern≥1.
Eine beschränkte Gesamtrate kann auf diesem endlichen Uhrintervall nicht
unendlich viele Geburten erzeugen. Damit ist die unbeschränkte
Elementzahlreferenz auf jedem festgelegten endlichen Horizont wohldefiniert.
Dies beweist keine Quantenmaß-Fortsetzung über unendliche Zeit oder eine
allgemeine Singularitätsauflösung.

Die Raten (18) sind eine Darstellung der **gewählten** Endhorizont-Norm.
Sie sind noch keine aus Constraints gewonnene Staubbewegung. Ein anderer
Enduhrwert ändert sie; ein Herausschieben des Endhorizonts oder eine
physikalische Randzustandsauswahl ist nicht geprüft. Die Abhängigkeit von
einer Randbedingung ist keine Aussage über physikalische Rückwärtskausalität.

## 7. Zwei konsistente Entscheidungen liefern verschiedene Vorhersagen

Für leeres P, z=1, Endintervall h=1/2 und global N=2 ergibt sich exakt:

| α | Z_N | P(0 Geburten) | P(1 Geburt) | P(2 Geburten) |
|---|---:|---:|---:|---:|
| 0, nur bei endlichem N | 7/4 | 4/7 | 2/7 | 1/7 |
| 1 | 13/8 | 8/13 | 4/13 | 1/13 |
| 2 | 25/16 | 16/25 | 8/25 | 1/25 |

Alle Reihen summieren auf eins und verwenden die gemeinsame-Horizont-
Komposition. Sie sind dennoch verschieden. Auch nach Entfernen der
Elementzahlgrenze bleibt der Unterschied zwischen α=1 und α=2 bestehen:
Die bis N=6 exakt berechneten Z-Werte und die Restschranke 1/604800
liefern disjunkte Intervalle für die Keine-Geburt-Wahrscheinlichkeit.
Die Intervalle stehen rational in `results/weight_alternatives.json`.
Damit ist die Nicht-Eindeutigkeit nicht nur ein Abschneideeffekt.

Diese Zahlen sind Referenzwahrscheinlichkeiten. Sie sind keine
gemessenen Ereignisraten, keine Dichtekalibrierung und keine
Bounce-Wahrscheinlichkeiten. q, α und t_* werden nicht durch (3) ausgewählt.

### Weshalb dies noch keine gravitative Quantendynamik auswählt

Auf dem vollständig gespeicherten Historienraum kann die Phase geschrieben
werden als U^S=D_b U^0 D_a^†, mit D_sψ=exp(iS/ℏ)ψ. Dasselbe gilt für K,
weil Z keine Wirkungsphase enthält. Für diagonale Historienereignisse
heben sich diese Phasen vollständig aus den Born-Gewichten heraus.
Gravitations- oder Materiephasen unterdrücken in dieser scharfen
Record-Auslese also keine unerwünschten Geometrien. Eine kohärente
Endkontraktion könnte Interferenz enthalten, wäre aber eine zusätzliche
Mess-/Randdefinition mit eigener Norm- und Schnittprüfung.

Die bekannten klassischen sequentiellen CST-Wachstumsmodelle werden unter
weiteren Kovarianz- und Kausalitätsbedingungen untersucht [1]. Unsere
markierte chronologische Konstruktion behauptet weder die entsprechende
unmarkierte Geburtsordnungsunabhängigkeit noch Bell-Kausalität. Ein
Quantenmaß kann zudem über gewöhnliche additive Recordwahrscheinlichkeiten
hinausgehen [2]. Diese Literaturmotivationen ersetzen keine physikalische
Auswahl des hier benutzten lokalen Produkts oder einer Quantendynamik.

## 8. Kontrollen, Reproduzierbarkeit und nächster Schritt

Die endliche Wirkungsprüfung benutzt 6 verschiedene T-Gitterwerte und
binäre w-Marken 0,1/2. Sie prüft algebraische Identitäten, keine
kontrollierte Quadratur des kontinuierlichen Feldintegrals. Die Norm-
und Kompositionsformeln werden dagegen für das kontinuierliche Maß
analytisch bewiesen; ihre endlichen Koeffizienten sind exakt rational.

| Kontrolle | Umfang |
|---|---:|
| Unabhängige natürliche Ordnungen, maximal n=6 | 4.824 bei n=6 |
| Markierte vollständige Wirkungsrecords, n≤4 | 10.853 |
| Wirkungs-Komposition an drei Uhrschnittpaaren | 32.559 |
| Endpunkt-Zahlgewichte an denselben Records | 97.677 |
| Zustandssummen-Komposition / Rückwärtsgleichung | je 198 |
| Gemeinsame-Horizont-Koeffizienten | 108.441 |
| Uniforme gewichtete Erweiterungsschranken | 102 |
| Kontrollierte unendliche Reste | 24 |
| Isolierte Nachrechnung | sechs Ergebnisdateien bytegleich |

Python 3.10+, Standardbibliothek und `fractions.Fraction`. Kein Monte Carlo,
keine neuen 4D-CST-Ensembles und keine bezahlten Läufe. Allgemeine Beweise
sind nicht durch einen formalen Beweisassistenten zertifiziert. Der Plan
wurde lokal nach analytischer Überlegung und vor Implementierung gehasht;
er ist keine blinde Vorhersage oder externe Präregistrierung. Bytegleicher
Replay ist keine unabhängige wissenschaftliche Replikation.

**Der nächste physikalische Engpass ist nun konkret:** Eine Quantendefinition
muss die relativen Größen-/Geometriegewichte, den Randzustand und das
Ereignisprodukt gemeinsam begründen und tatsächliche gravitative Interferenz
zulassen oder ihre Auslesedeutung erklären. Nur eine weitere normierte
Referenz auszuwählen würde das nicht lösen. Als nächster gezielter Test
ist eine deklarierte kohärente Randkontraktion beziehungsweise ein
Dekohärenzfunktional gegen Positivität und Schnittkompatibilität zu prüfen;
die hier erreichten Z-Schranken und unveränderten Wirkungsphasen können
dafür als kontrollierte Bausteine dienen. Ein physikalischer Anspruch
erfordert anschließend die getrennten acht Gates.

## Primärquellen und Herkunft

[1] D. P. Rideout, R. D. Sorkin, *A Classical Sequential Growth Dynamics
for Causal Sets*, Phys. Rev. D 61, 024002 (2000),
https://arxiv.org/abs/gr-qc/9904062v3 . Klassisch stochastische Modelle aus
expliziten Kausalitäts-/Kovarianzbedingungen; kein Nachweis unserer
markierten Staubuhrkonstruktion.

[2] R. D. Sorkin, *Quantum Mechanics as Quantum Measure Theory*,
Mod. Phys. Lett. A 9 (1994), https://arxiv.org/abs/gr-qc/9401003v2 .
Einordnung verallgemeinerter Quantenmaße gegenüber additiven klassischen
Wahrscheinlichkeiten; keine Auswahl des hier verwendeten Produkts.

Die hier benötigten Zähl-, Norm-, Rest- und Kompositionsbeweise sind im
Text geführt. Es wird keine mathematische Neuheit beansprucht. Sechs
Repositorydateien sind bytegleich in `inputs/` enthalten, durch Commit,
Pfad und Git-Blob-SHA gepinnt und werden bei jedem Analyselauf geprüft.
