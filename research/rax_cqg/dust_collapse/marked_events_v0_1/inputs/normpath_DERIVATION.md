# CST-DUST: Normpfad und kohärenter Quotient v0.1

7. November 2026. Audit `CST-DUST-NORMPATH-QUOTIENT-001`.
Basis: Main `573084d007ae96d82eb6c241df6ae1d572523418`, nach PR 249.

## 1. Ergebnis und Reichweite

Der vorherige Gedächtnisvertrag wird weitergeführt: Die vollständige
Vergangenheit und alle alten Felder bleiben erhalten; die geerbten endlichen
Amplituden werden nicht lokal nachnormiert. Drei Fragen werden getrennt
beantwortet:

1. **Existenz:** Positive diagonale, feldunabhängige Normpfade existieren auf
   allen endlichen Stufen. Ihre vollständige Klassifikation ist
   h_m(P)=e(P)^2 μ_m(P), wobei μ ein konsistentes positives Zylindermaß auf
   natürlich gelabelten Wachstumshistorien ist. Beispiele können für jeden
   Endhorizont exakt zurückgezogen werden. Sie sind nicht eindeutig.
2. **Kohärente Endkontraktion:** Unter h_0=1 besitzt die unveränderte Summe
   über die Historien in dieser ganzen diagonalen Klasse keine gemeinsame
   endhorizontunabhängige Operatornormschranke. Das folgt aus einer allgemeinen
   Zählabschätzung, nicht aus dem begrenzten numerischen Scan.
3. **Labelquotient:** Für unmarkierte Geometrieamplituden ist der kohärente
   Quotient exakt mit der Fortsetzung verträglich. Positive diagonale
   Produkte machen seine Fortsetzung jedoch schon von zwei auf drei innere
   Elemente nicht auf dem ganzen Raum isometrisch. Nichtdiagonale Produkte
   können konstruiert werden, sind aber physikalisch nicht ausgewählt.

Damit ist die abstrakte Existenz einer Hilfsnorm geklärt. Eine physikalische
Randnorm, die markierte Ereignisalgebra und die Fortsetzung des ursprünglichen
Quantenmaßes bleiben offen. **Alle acht physikalischen Gates bleiben HOLD.**
Keine neue dynamische 4D-Simulation und kein Bounce- oder Regularitätsnachweis.

## 2. Präzise Normklasse

Sei Ω_m^nat die endliche Menge natürlich gelabelter innerer Ordnungen P mit
m Elementen. Die äußeren Anker und die Feldmaße bleiben wie im Vorgänger:
kompakte normierte Uhrmaße und dν(w)=½δ_0+½1_(0,1)dw. Das neueste innere
Element hat als Vergangenheit den Anfangsanker und ein beliebiges inneres
Ordnungsideal J. Der Endanker wird erst bei der Endkontraktion angefügt.

Mit e(P) als Zahl linearer Erweiterungen gilt weiterhin

\[
(V_m\psi)(P',\xi,u)
=r(P,P')e^{i\Delta S/\hbar}\psi(P,\xi),\qquad r(P,P')=e(P)/e(P').
\]

Die betrachteten Normen sind

\[
\|\psi\|_{h_m}^2=
\sum_{P\in\Omega_m^{nat}}h_m(P)\int|\psi(P,\xi)|^2d\nu_P(\xi),
\qquad h_m(P)>0,
\]

mit normierten Feldmaßen ν_P, feldunabhängigen Gewichten und h_0(∅)=1.
Die Isometrie für **alle** Zustände ist äquivalent zu

\[
h_m(P)=\sum_{P'\text{ Kind von }P}r(P,P')^2h_{m+1}(P'). \tag{1}
\]

Das Kind besitzt in der natürlichen Beschreibung einen eindeutigen Elternteil.
Deshalb treten hier keine Kreuzterme verschiedener Eltern auf. Alle früheren
Felder werden behalten; die Phase hat Betrag eins und das neue Feldmaß
Gesamtmasse eins. Ein allgemeines nichtdiagonales oder feldabhängiges Produkt
ist durch (1) nicht erfasst. Die endliche Hilfsbox wird nicht entfernt.

## 3. Klassifikation und explizite allstufige Familie

**Satz 1.** Die positiven Lösungen von (1) mit h_0=1 entsprechen bijektiv
konsistenten Zylinderwahrscheinlichkeiten μ_m(P)>0 durch

\[
\mu_m(P)=h_m(P)/e(P)^2. \tag{2}
\]

**Beweis.** Einsetzen in (1) und Teilen durch e(P)^2 ergibt
μ_m(P)=Σ_Kind μ_(m+1)(P'). Umgekehrt führt diese Summenregel sofort auf (1).
Wegen μ_0=1 ist auf jeder Stufe Σ_P μ_m(P)=1. Die endlichen Verzweigungsmengen
definieren ein konsistentes Wahrscheinlichkeitsmaß auf dem Raum unendlicher
natürlicher Wachstumspfade. Das ist ein klassisches positives Maß als
Hilfskonstruktion und noch kein quantales Maß der ursprünglichen Amplitude.

Eine explizite Familie benutzt die bekannte transitive Perkolation [1]. Für
0<p<1, q=1-p, Linkzahl L(P), Relationszahl R(P) und K_m=m(m-1)/2 setze

\[
\mu_m^{(p)}(P)=p^{L(P)}q^{K_m-R(P)},\qquad
h_m^{(p)}(P)=e(P)^2p^{L(P)}q^{K_m-R(P)}. \tag{3}
\]

Die Anfangs- und Endanker werden hier **nicht** zufällig perkoliert; die
Hilfsverteilung betrifft die inneren Ordnungen des bereits erklärten Trägers.

**Unabhängige Herleitung.** Belege jedes vorwärts gerichtete Paar i<j
unabhängig mit einer Kante mit Wahrscheinlichkeit p und bilde die transitive
Hülle. Um genau P zu erhalten, müssen alle Links von P vorhanden sein, alle
unvergleichbaren Paare fehlen; die übrigen transitiv implizierten Kanten sind
frei. Das ergibt (3). Beim nächsten Element müssen die Maxima von J ausgewählt
und alle Punkte außerhalb J ausgeschlossen sein. Die restlichen Punkte von J
sind frei. Daher ist die Übergangswahrscheinlichkeit

\[
\alpha_p(P,J)=p^{|\max J|}q^{m-|J|},\qquad \sum_{J\text{ Ideal}}\alpha_p(P,J)=1. \tag{4}
\]

Das beweist Konsistenz und strikte Positivität für alle m. e,L,R sind
Isomorphieinvarianten. Die Gewichte behandeln verschiedene natürliche
Beschreibungen desselben unmarkierten Typs gleich, identifizieren sie aber
noch nicht zu einem physikalischen Zustand. Die Familie ist bekannt; die
hier benutzte Umgewichtung h=e²μ ist eine Hilfsnorm für den geerbten Operator,
keine Herleitung der Perkolationswahrscheinlichkeit aus der BDG-Staubwirkung.

**Nicht-Eindeutigkeit und Horizont.** Für die Zweierkette C und Zweierantikette A
lauten h_2(C)=p und h_2(A)=4q. Daher:

| p | h_2(C)/h_2(A) |
|---|---:|
| 1/4 | 1/12 |
| 1/2 | 1/4 |
| 3/4 | 3/4 |

Keine einzige Gesamtnormierung macht diese verschiedenen relativen Normen
gleich. Wählt man bei einem beliebigen endlichen M das Endprodukt h_M^(p),
liefert sein Rückzug exakt h_m^(p), unabhängig von M≥m. Das ist eine
konstruktiv kompatible Endwahl; daraus folgt keine Attraktivität unter
anderen Endwahlen. Die früheren Kontrollen mit Endgewicht 1 und 1+R werden
bis M=6 fortgesetzt. Ihre unterschiedlichen Quotienten zeigen endliche
Endwahlabhängigkeit, beweisen aber weder Konvergenz noch Divergenz dieses
separaten Grenzprozesses.

## 4. Was der Hilbert-Grenzraum leistet

Sei S_m die vollständige Wirkung des vorhandenen Anfangsankers und der m
inneren Elemente, ohne abschließenden Endanker. Die Transformation

\[
(W_m\psi)(P,\xi)=e(P)e^{-iS_m(P,\xi)/\hbar}\psi(P,\xi)
\]

bildet H_m(h) isometrisch auf das L²-Produkt aus μ_m und ν_P ab. Sie erfüllt

\[
W_{m+1}V_mW_m^{-1}f=f\circ\pi_m,
\]

weil die Wirkungszuwächse teleskopieren. π_m vergisst das letzte innere Element
und dessen neue Felder. Die stufenweisen Einbettungen liefern einen abstrakten
Hilbert-Induktivgrenzraum beziehungsweise die Vervollständigung der
Zylinderfunktionen für das gewählte positive Maß.

Der aus dem Anfangszustand erzeugte Vektor ψ_m=e^(iS_m/ℏ)/e(P) wird dabei auf
die konstante Funktion 1 abgebildet. Für bloße orthogonale Prefix-Records
ergibt sein Gramfunktional μ(A∩B). Es ist in dieser Konstruktion klassisch
und enthält keine Interferenz disjunkter Records. Das entfernt keine Physik
durch ein Argument: Die Wirkungsphasen stehen weiterhin in der geerbten
Endkontraktion und müssten zusammen mit den Observablen transformiert werden.
Es zeigt, dass die Hilfsnorm allein die ursprüngliche kohärente Summe nicht
als physikalisches Quantenmaß qualifiziert.

Ein natürlich gelabelter Prefix ist nicht automatisch ein kovariantes
physikalisches Ereignis. Labelunabhängige Ereignisse müssen gesondert
bestimmt werden; klassische Stem-Ereignisse sind dafür Literaturhintergrund
[2]. Ebenso ersetzt die Existenz dieses Hilbert-Grenzraums keine Prüfung der
Fortsetzung des ursprünglichen quantalen Vektormaßes [3].

## 5. Allgemeines Hindernis für eine gleichmäßig beschränkte Endsumme

Die unveränderte kohärente Endkontraktion im betrachteten endlichen Sektor sei

\[
\ell_m(\psi)=\sum_{P\in\Omega_m^{nat}}
\int b_m(P,\xi)\psi(P,\xi)d\nu_P(\xi),\qquad |b_m|=1. \tag{5}
\]

b_m kann die Phase des gemeinsamen Endankers enthalten. Die Gewichte 1/e(P)
sind bereits in den fortgesetzten Amplituden enthalten und werden in (5)
nicht ein zweites Mal eingesetzt. Diese Aussage betrifft die originale
kohärente Summe mit normierten Feldmaßen, ohne zusätzliche Dämpfung oder
stufenabhängige Endnormierung.

**Satz 2.** Auf den vollständigen Räumen der Klasse aus Abschnitt 2 gilt

\[
\|\ell_m\|^2=\sum_P\frac1{h_m(P)}
=\sum_P\frac1{e(P)^2\mu_m(P)}, \tag{6}
\]

und für jeden dieser normalisierten positiven Normpfade

\[
\|\ell_m\|\geq\sum_P\frac1{e(P)}
\geq\frac{2^{\lfloor m/2\rfloor\lceil m/2\rceil}}{m!}
\xrightarrow[m\to\infty]{}\infty. \tag{7}
\]

**Beweis.** Der Riesz-Repräsentant von (5) hat in jedem Sektor den Betrag
1/h_m(P). Wegen ν_P(X_P)=1 folgt (6). Cauchy-Schwarz auf den beiden Folgen
1/(e(P)√μ(P)) und √μ(P), mit Σμ=1, liefert die erste Schranke in (7).
Für die zweite betrachte die natürliche Zweischichtfamilie: die ersten
⌊m/2⌋ Labels bilden die untere Antikette, die übrigen die obere. Jede Teilmenge
der möglichen unteren-zu-oberen Kanten ist bereits transitiv und bestimmt
eine andere natürliche Ordnung. Es gibt 2^(⌊m/2⌋⌈m/2⌉) solche Ordnungen,
und für jede gilt e(P)≤m!. Schließlich wächst der quadratische Exponent
schneller als log(m!)=O(m log m). Das beweist die Divergenz.

Die exakte vollständige kleine Summe Σ_P1/e(P) lautet für m=0,…,6

\[
1,\quad1,\quad3/2,\quad19/6,\quad73/8,\quad4231/120,\quad14447/80.
\]

Die einfache Zweischichtschranke ist bei kleinen m schwach, beweist aber die
Asymptotik. Beispielsweise liegt sie bei m=16 über 8,8·10^5 und bei m=32 über
4,4·10^41. Dies sind Schranken für die Norm einer Endabbildung, keine
physikalischen Energien, Ereigniswahrscheinlichkeiten oder Bounce-Prognosen.

**Genaue Grenze:** Ausgeschlossen ist eine auf dem ganzen Hilbert-Grenzraum
beschränkte gemeinsame Endfunktional-Realisierung, deren Einschränkungen alle
unveränderten ℓ_m sind. Dafür wäre eine einheitliche Normschranke notwendig;
zusätzlich wäre die hier nicht postulierte Kompatibilität ℓ_(m+1)V_m=ℓ_m
erforderlich. Nicht ausgeschlossen sind unbeschränkte/distributionelle
Endzustände, passend eingeschränkte physikalisch erreichbare Räume,
nichtdiagonale oder feldabhängige Produkte, andere Randdaten oder offen
deklarierte Änderungen des Modells. Dies ist kein allgemeines No-go für CST
oder für jedes unendliche Quantenmaß.

## 6. Kohärenter Quotient: expliziter unmarkierter Referenzsektor

Hier wird die volle markierte Feldtheorie **nicht** quotientiert. Betrachtet
werden unmarkierte innere Geometrieamplituden nach Entfernung der
teleskopierenden Wirkungsphase. Im reinen Geometriesektor ist dies eine
diagonale Phasentransformation; es entspricht bei verschwindender Phase
direkt dem Zähloperator. Das ist ein struktureller Referenztest.

Für einen unmarkierten Typ U sei k(U)=e(U)/|Aut(U)| die Anzahl seiner
inequivalenten natürlichen Beschreibungen. Definiere die kohärente Summe

\[
(Q_m\psi)(U)=\sum_{P\simeq U}\psi(P).
\]

Für einen einzelnen Vertreter P vom Typ U und einen Kindtyp U′ setze

\[
B_m(U',U)=N(U',U)\,\frac{e(U)}{e(U')}, \tag{8}
\]

wobei N(U′,U) die Zahl der Ordnungsideale von P zählt, deren Anfügung den
Typ U′ erzeugt. Isomorphismen bilden Ideale bijektiv aufeinander ab; N ist
daher unabhängig vom gewählten natürlichen Vertreter. Direktes Gruppieren
der Summen liefert Q_(m+1)V_m=B_mQ_m. Insbesondere ist ker Q unter V in den
entsprechenden nächsten Kern abgebildet. Das Quotientieren ist hier
algebraisch wohldefiniert. Aus dem leeren Anfangszustand entsteht weiter der
ursprüngliche Typkoeffizient k(U)/e(U)=1/|Aut(U)|.

Dies ist eine **kohärente** Amplitudensumme. Das bloße Addieren klassischer
Wahrscheinlichkeiten μ(P) über Typen ist ein anderer Vorgang.

## 7. Warum diagonale Quotientenprodukte nicht genügen

Für Eltern A=Zweierantikette und C=Zweierkette und die fünf Kindtypen lautet
die exakt enumerierte Matrix aus (8):

| Kindtyp mit drei Elementen | aus A | aus C |
|---|---:|---:|
| Antikette | 1/3 | 0 |
| Kette plus isoliertes Element | 4/3 | 1/3 |
| Zwei Minima, ein gemeinsames Maximum | 1 | 0 |
| Ein Minimum, zwei Maxima | 0 | 1/2 |
| Dreierkette | 0 | 1 |

Ein strikt positives diagonales Kindprodukt D_3 ergibt somit

\[
(B_2^\dagger D_3B_2)_{A,C}=\frac49d_{\text{Kette+isoliert}}>0. \tag{9}
\]

Ein diagonales Elternprodukt D_2 hat dort null. Daher kann
B_2†D_3B_2=D_2 nicht auf dem gesamten zweidimensionalen Elternraum gelten.
Die vorhandenen geometrischen Wirkungsphasen ändern (9) nur um einen
gemeinsamen nichtverschwindenden Phasenfaktor. Der Befund ist kein
gravitatives Anomalieargument und nicht als Satz für den hier nicht
ausgearbeiteten vollständigen markierten Feldquotienten ausgewiesen.

Für ein isomorphieinvariantes natürliches Diagonalprodukt h ist das durch
Minimierung über Qψ=A induzierte Quotientenprodukt ebenfalls diagonal:
D_m(U)=h_m(U)/k(U). Die Minimierung folgt aus Cauchy-Schwarz innerhalb jedes
Orbits. Der Widerspruch (9) trifft daher auch die Forderung, diesen
naheliegenden kohärenten Quotienten auf allen Zuständen isometrisch
fortzusetzen. Er widerspricht nicht der Isometrie auf den ursprünglichen
orthogonalen natürlichen Records: Dort werden die gemeinsam endenden
Beiträge noch nicht kohärent identifiziert.

## 8. Nichtdiagonale Produkte existieren, bleiben aber frei

**Satz 3 für den unmarkierten Referenzsektor.** B_m besitzt auf jeder Stufe
eine Linksinverse L_m. Wähle zu jedem Typ U sein Kind C(U), das durch
Anfügen eines über allen Elementen liegenden neuen Elements entsteht.
Dieses Kind hat ein eindeutiges größtes Element. Dessen Entfernung ergibt
eindeutig U; kein anderer Eltern-Typ trägt zu dieser Zeile bei. Außerdem
ist e(C(U))=e(U), und das volle Ideal ist genau einmal vorhanden. Also ist
die ausgewählte Zeile von B genau der entsprechende Einheitsvektor.
L_m selektiert diese Zeilen und erfüllt L_mB_m=I.

Für jedes positiv definite Elternprodukt M_m und jedes positiv definite
Komplementprodukt K_(m+1) liefert

\[
M_{m+1}=L_m^\dagger M_mL_m
+(I-B_mL_m)^\dagger K_{m+1}(I-B_mL_m) \tag{10}
\]

ein positiv definites Produkt mit B_m†M_(m+1)B_m=M_m. Die Isometrie folgt
unmittelbar aus LB=I. Hat ein Vektor unter (10) Norm null, sind Lx=0 und
(I-BL)x=0, also x=0; damit ist die Positivität bewiesen. Dies lässt sich
rekursiv auf allen endlichen Stufen ausführen und ergibt einen abstrakten
Hilbert-Induktivgrenzraum des unmarkierten Referenzsystems.

Die Wahl K=λI ist bereits frei. Zwei Familien λ=1 und λ=2 werden bis zu
16 unmarkierten Typen geprüft; positive rationale LDL-Pivots zertifizieren
die endlichen Matrizen. Eine zusätzliche explizite 5×5-Matrix bildet ein
Einheitsprodukt der zwei Eltern exakt zurück. Ihr vollständiger Inhalt
steht in `results/coherent_quotient.json`.

Die Konstruktion ist **kein unabhängig hergeleitetes physikalisches Produkt**.
Sie benutzt eine ausgewählte algebraische Linksinverse und freie
Komplementgewichte. Gleichmäßige Äquivalenz- oder Kontinuumsschranken werden
nicht bewiesen. Für ein nichtdiagonales M sind zudem die üblichen
Koordinatenprojektoren auf einzelne Geometrietypen im Allgemeinen nicht
M-selbstadjungiert: P_U†M=MP_U verlangt verschwindende Kreuzmatrixelemente
zwischen U und seinem Komplement. Man darf diese Projektoren deshalb nicht
ungeprüft als scharfe physikalische Messungen verwenden. Eine Ereignisalgebra
oder ein Dekohärenzfunktional benötigt eine eigene Definition.

## 9. Ausgeführte Kontrollen

| Kontrolle | Umfang |
|---|---:|
| Natürliche Ordnungen m=0,…,6 | 5.232 |
| Unabhängig enumerierte natürliche DAGs mit transitiver Hülle | 33.868 |
| Rationale Wahrscheinlichkeitsvergleiche, drei p-Werte | 15.696 |
| Positive Normwerte | 15.696 |
| Zylinder-/Übergangsrekursionen | 1.224 |
| Normrekursionen | 1.224 |
| Stufennormierungen | 21 |
| Exakte Rückzüge der kompatiblen Endprodukte | 17.118 |
| Nichtkompatible Endwahl-Kontrollen | 10 |
| Isomorphietypen einschließlich leerem Typ, m≤5 | 88 |
| Vertreterunabhängige Quotientenspalten | 51 |
| Erhaltene Endkoeffizienten 1/Aut | 87 |
| Linksinversen-Matrixeinträge | 287 |
| Rekursiv konstruierte positive Produkte | 8, plus eine 5×5-Kontrolle |

Die genaue Arithmetik benutzt ausschließlich rationale Zahlen. Die DAG-Route
erzeugt Kantenmengen unabhängig und verwendet Warshall-Hüllen; die primäre
Route erzeugt Ordnungen durch Ideale. Allgemeine Aussagen beruhen auf den
ausgeschriebenen Beweisen, nicht allein auf diesen endlich vielen Fällen.
Sie sind nicht durch einen formalen Beweisassistenten zertifiziert.

Fünf Ergebnisdateien werden in einem isolierten Verzeichnis allein aus den
Quellen erzeugt und byteweise verglichen. Der lokale Plan wurde vor der
Implementierung gehasht, die erwarteten Mechanismen waren bereits diskutiert.
Dies ist keine externe Präregistrierung und keine blinde Vorhersage.

## 10. Konsequenz für den nächsten wissenschaftlichen Schritt

Eine weitere Anpassung positiver Diagonalgewichte löst das gemeinsame
Problem nicht: Ihre Existenz ist konstruktiv geklärt, während (7) und (9)
die genau bezeichneten Kohärenzanforderungen begrenzen.

Der nächste Schritt muss **physikalische Zustände und Ereignisse samt
Endkontraktion gemeinsam festlegen**. Eine konkrete Route ist ein
nichtdiagonales Produkt auf vollständig markierten, kovarianten Zuständen
mit begründetem Ereignisfunktional. Eine andere wäre eine kontrollierte
distributionelle Endkontraktion auf einem begründeten physikalischen
Zustandsraum. Beide benötigen unabhängige Auswahlkriterien, Kontrollschranken
und anschließend die klassische Korrespondenz. Die hier freie Konstruktion
K=λI oder ein frei gewähltes p ersetzt das nicht.

MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben jeweils **HOLD**. Historische kandidatenspezifische FAILs
werden nicht aufgehoben.

## Literatur und Herkunft

1. D. P. Rideout, R. D. Sorkin, *A Classical Sequential Growth Dynamics for
   Causal Sets*, Phys. Rev. D 61, 024002 (2000),
   https://arxiv.org/html/gr-qc/9904062v3, insbesondere Abschnitt 4.2 zur
   Perkolation und Abschnitt 5 zur Unterscheidung natürlicher und kovarianter
   Ereignisse. Die bekannte Perkolationsfamilie wird als Hilfsbeispiel benutzt.
2. G. Brightwell, H. F. Dowker, R. S. Garcia, J. Henson, R. D. Sorkin,
   *“Observables” in causal set cosmology*, Phys. Rev. D 67, 084031 (2003),
   https://arxiv.org/abs/gr-qc/0210061v2. Kontext für kovariante klassische
   Ereignisse; das dortige Ergebnis wird nicht auf unsere Quantenamplitude
   übertragen.
3. F. Dowker, S. Johnston, S. Surya, *On extending the Quantum Measure*,
   J. Phys. A 43, 505305 (2010), https://arxiv.org/abs/1007.2725v1.
   Die Fortsetzung eines quantalen Vektormaßes ist eine eigene Aufgabe;
   unser Hilbert-Induktivgrenzraum beweist sie nicht.

Sechs Vorgängerdateien sind unverändert übernommen. Pfade und SHA-256 stehen
in `inputs/provenance.json`. Diese Notiz ist eine neue mathematische Prüfung
des erklärten Kandidaten, kein Anspruch auf einen publizierten physikalischen
Modellschluss oder auf Priorität für die verwendeten Standardkonstruktionen.
