# CST-DUST: Markierte Zustände, Ereignisse und Endauslese v0.1

Datum: 2026-11-07. Basis: Main `57aea796ac1f35c31ca3fabce45e0a27c518a5bf`
nach PR 250 in `thomasmgfeller/x6-spectral-astrolabium`.

## Ergebnis und Geltungsbereich

Der bisher nur für unmarkierte Geometrieamplituden konstruierte kohärente
Quotient wird hier **bei jeder festen endlichen Stufe auf die vollständigen
kontinuierlichen Uhr- und Staubfelder erweitert**. Die geerbte Fortsetzung
steigt auf diesen Quotienten ab. Eine beschränkte Linksinverse liefert
positive, koerzive Skalarprodukte und transportierbare Präparationsprojektoren.
Das ist ein mathematischer Existenzsatz für die erklärte regulierte
Darstellung, keine Auswahl des physikalischen CST-Hilbertraums.

Zwei zusätzliche Bedingungen werden explizit:

1. Eine labelinvariante Aussage über den aktuellen Zustand ist nicht allein
   dadurch ein zulässiger scharfer Messprojektor. Sie muss bezüglich des
   gewählten Skalarprodukts selbstadjungiert sein. Ein exaktes Gegenbeispiel
   liefert als naiven Erwartungswert **−1/149**.
2. Die kohärente Endsumme kann auf jeder festen Stufe als skalierte Auslese
   realisiert werden, doch ihre Normierung und ihre Kompatibilität mit
   zusätzlichen Fortsetzungsschritten sind eigene Bedingungen. Im erklärten
   phasenfreien Referenzfall unterscheiden sich die Rückzugsfaktoren
   **8/3 und 11/6**; eine gemeinsame Skalierung reicht dort nicht.

Die endlichen Kontrollen verwenden zusätzlich einen binären Feldmaß-Ersatz.
Dieser ist weder eine Staubballsimulation noch eine kontrollierte Quadratur
des kontinuierlichen Feldintegrals. Allgemeine Aussagen beruhen auf den
nachfolgenden Beweisen, nicht auf der Enumeration kleiner Ordnungen.
**MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben jeweils HOLD.** Frühere kandidatenspezifische FAILs werden
dadurch nicht aufgehoben. Keine Neuheitsbehauptung und keine formale
Beweisassistenten-Zertifizierung.

## 1. Beibehaltene Daten

P ist eine natürlich gelabelte innere Ordnung mit m Elementen. Der feste
Anfangsanker a liegt unter allen inneren Elementen; der Endanker f wird erst
bei der Endkontraktion hinzugefügt. e(P) zählt die linearen Erweiterungen der
**Geometrie**, nicht die Automorphismen eines markierten Zustands.
Die Fortsetzung um ein neues maximales Element mit Vergangenheitsideal J
behält alle alten Felder ξ bei:

\[
(V_m\psi)(P',\xi,u)=\frac{e(P)}{e(P')}
 e^{i[S(P',\xi,u)-S(P,\xi)]/\hbar}\psi(P,\xi). \tag{1}
\]

S ist die geerbte reelle regulierte Gravitations- plus Staubwirkung aus dem
Vorgängerpaket. Der bekannte lokale Inkrementausdruck ist eine exakte
Differenz dieser Gesamtwirkung; er ersetzt keine physikalische Variation.
Die kontrollierten äußeren Anker haben w=0. Ein äußerer Wirkungsbeitrag oder
ein Junction-Gesetz wird nicht neu hergeleitet. Die natürliche Labelreihenfolge
ist Hilfsbuchhaltung und wird nicht mit dem Materie-Uhrfeld T identifiziert.

Für jedes innere Element ist das normierte Produktmaß fest:

\[
d\nu(u)=\frac{dT}{2L}\Big[\tfrac12\delta_0(dw)
 +\tfrac12\mathbf1_{(0,1)}(w)dw\Big],\quad T\in[-L,L],\quad L>0. \tag{2}
\]

Es wird keine zusätzliche Monotoniebedingung auf T eingeführt. Genau dieses
Produktmaß, die volle Vergangenheit und das nicht eingeschränkte Ideal-
Wachstum sind Voraussetzungen der Konstruktion. Zusätzliche Constraints
können insbesondere die unten benutzten Kegel-Fortsetzungen entfernen.

## 2. Kontinuierlicher kohärenter Quotient

Wähle für jeden ungelabelten Geometrietyp U einen Vertreter. Schreibe
a_U=|Aut(U)|, e_U=e(U), X_U=([-L,L]×[0,1])^m mit Maß ν^m. Der Hilfsraum ist

\[
\mathcal G_m=\bigoplus_{[U]}L^2(X_U,\nu^m)^{Aut(U)}. \tag{3}
\]

Die Funktionen sind invariant unter gleichzeitiger Vertauschung der
Geometrieelemente und ihrer T,w-Werte. Das Referenzskalarprodukt ist die
gewöhnliche Summe der L²-Produkte. Es dient zunächst nur zur Definition
beschränkter Operatoren und ihrer Adjunkten †.

Für beliebige natürliche Komponenten ψ_P definiere

\[
(Q_m\psi)_U(x)=\frac1{a_U}
 \sum_{P\simeq U\;\mathrm{nat}}\sum_{\phi\in Iso(U,P)}
 \psi_P(\phi_*x). \tag{4}
\]

φ_*x transportiert die Feldwerte mit dem Isomorphismus. Es wird nicht
versucht, für kontinuierliche markierte Konfigurationen eine naive Division
durch einen punktweisen Stabilisator vorzunehmen. Stattdessen mittelt (4)
über die endliche Geometrie-Automorphismengruppe und summiert die
inequivalenten natürlichen Beschreibungen kohärent.

**Surjektivität.** Es gibt k_U=e_U/a_U natürliche Geometriebeschreibungen
von U. Verteile f_U/k_U auf jede solche Komponente unter einem beliebigen
Isomorphismus. Weil f_U invariant ist, ist die Wahl des Isomorphismus
irrelevant. Diese beschränkte Abbildung R_m erfüllt Q_m R_m=I.
Q_m ist beschränkt, da nur endlich viele maßtreue Feldpermutationen
summiert werden. Somit ist der lineare Quotient durch ker Q_m wohldefiniert.
Die kohärente Aggregation ist aber noch keine aus physikalischen Constraints
abgeleitete Gauge- oder Dirac-Reduktion.

**Erhaltene Endsumme.** Für jede invariant transportierte Endphase b gilt

\[
\sum_U\int b_U(x)(Q_m\psi)_U(x)d\nu^m(x)
=\sum_{P\;\mathrm{nat}}\int b_P(\xi)\psi_P(\xi)d\nu^m(\xi). \tag{5}
\]

Beweis: Jede Menge Iso(U,P) hat a_U Elemente, und jede Permutation bewahrt
das Produktmaß. Nach Integration heben sich die a_U gleichen Beiträge
gegen den Vorfaktor auf. Der geerbte Faktor 1/e(P) steckt bereits in ψ_P;
er wird nicht ein zweites Mal eingefügt.

## 3. Abstieg der vollständigen Fortsetzung

Für ein maximales z in U' sei U_z=U'\{z}. Das Feld x' ohne seine z-Komponente
wird auf den gewählten Vertreter von U_z transportiert. Definiere

\[
(B_mf)_{U'}(x')=
\sum_{z\in Max(U')}\frac{e_{U_z}a_{U_z}}{e_{U'}a_{U'}}
 e^{i\Delta S_z(x')/\hbar} f_{U_z}(x'_{\setminus z}). \tag{6}
\]

Der Ausdruck ist unabhängig von den gewählten Vertreter-Isomorphismen,
und Aut(U') permutiert die Summanden einschließlich der Felder.

**Satz: Q_{m+1}V_m=B_mQ_m.** Die Paare aus natürlicher Geometrie und
Isomorphismus in (4) entsprechen den linearen Erweiterungen des abstrakten
U'. Gruppiere diese nach dem Element z, das das letzte Label erhält.
Die Präfixe sind genau die linearen Erweiterungen von U_z. Ihre Summe ist
a_{U_z}(Q_mψ)_{U_z}. (1) liefert zusätzlich e_{U_z}/e_{U'}, und (4)
liefert 1/a_{U'}. Das ergibt (6), auch bei verschiedenen alten Feldwerten.
Insbesondere V_m ker Q_m ⊆ ker Q_{m+1}.

B_m ist beschränkt: Jeder Summand ist ein Pullback unter Weglassen einer
Produktmaß-Komponente mit Norm eins, gefolgt von einer Phase vom Betrag
eins und einem endlichen Koeffizienten. Endlich viele solche Summanden
und Geometrietypen ergeben eine endliche Operatornorm bei festem m.

### Eine beschränkte Linksinverse

Sei C(U) der Kegel über U: Ein neues eindeutiges größtes Element liegt über
allen alten. Dann e_C=e_U, a_C=a_U, und (6) hat dort nur einen Summanden
mit Koeffizient eins. Deshalb ist

\[
(L_mg)_U(x)=\int e^{-i\Delta S_C(x,u)/\hbar}
 g_{C(U)}(x,u)d\nu(u),\qquad L_mB_m=I. \tag{7}
\]

Die verschiedenen Eltern haben verschiedene private Kegelblöcke.
Cauchy-Schwarz und ν(K)=1 liefern ||L_m||≤1 im Referenzprodukt.
Das integrierte neue Feld wird allein zur algebraischen Rückabbildung
benutzt; die Vorwärtsdynamik (1) integriert keine alten Felder aus.

## 4. Positive Produkte auf dem vollständigen markierten Hilfsraum

Seien M_m und K_{m+1} beschränkte positive koerzive Operatoren auf den
Referenzräumen, M_m≥aI, K_{m+1}≥cI mit a,c>0. Mit R=I−B_mL_m setze

\[
M_{m+1}=L_m^\dagger M_mL_m+R^\dagger K_{m+1}R. \tag{8}
\]

Dann gelten

\[
B_m^\dagger M_{m+1}B_m=M_m,\quad
B_m^\dagger M_{m+1}=M_mL_m. \tag{9}
\]

Beweis: LB=I und RB=0 eliminieren alle übrigen Terme. Außerdem
x=B Lx+Rx. Damit

\[
\langle x,M_{m+1}x\rangle\ge
\min(a,c)(\|Lx\|^2+\|Rx\|^2)
\ge \frac{\min(a,c)}{1+\|B\|^2}\|x\|^2. \tag{10}
\]

Die obere Beschränktheit folgt aus
||M_{m+1}||≤||M_m||||L||²+||K||||I−BL||².
Somit ist (8) auch im unendlichdimensionalen Feld-L²-Raum ein gültiges
äquivalentes Hilbertprodukt, nicht nur eine endliche positive Matrix.
Beginnend mit M_0=1 kann es für jedes endliche m rekursiv konstruiert werden.
Es wird **keine von m unabhängige Koerzivitäts- oder Äquivalenzschranke** behauptet.

Die Wirkungsphasen dürfen bei nichtdiagonalem M nicht bloß weggelassen
werden. Mit U_m f=e^{iS_m/ℏ}f gelten B^S=U_{m+1}B^0U_m† und
L^S=U_mL^0U_{m+1}†. Eine Rechnung in der phasenfreien Darstellung ist
äquivalent, wenn zugleich M^S=U_mM^0U_m† und alle Auslesen entsprechend
transformiert werden. (6)-(10) enthalten die Phase bereits explizit.

Dies schließt die frühere formale Lücke `full_marked_field_quotient:
NOT_CONSTRUCTED` im Normvertrag des Vorgängers unter den hier festgehaltenen
Voraussetzungen. Es wählt weder K noch ein physikalisches Anfangsprodukt,
keine Constraints, keinen Vierdimensionalitätssektor und keine Materie-Uhr-
Evolution aus. Weitere Eichsymmetrien sind hier nicht untersucht.

## 5. Was sich als Präparationsnachweis transportieren lässt

Verwende das physikalisch noch nicht ausgewählte Hilfsprodukt
<x,y>_m=<x,M_my>_ref. Das zugehörige Adjunkt von B ist nach (9)

\[
B^\sharp=M_m^{-1}B^\dagger M_{m+1}=L. \tag{11}
\]

Π=BL ist daher der M_{m+1}-orthogonale Projektor auf Ran B, und R=I−Π
der orthogonale Komplementprojektor. Ist {E_a} eine vollständige
orthogonale Projektorzerlegung auf der Elternstufe, dann bilden

\[
F_a=B E_aL,\qquad F_{neu}=I−BL \tag{12}
\]

eine vollständige orthogonale Projektorzerlegung auf der Kindstufe.
Denn F_aF_b=B E_aE_bL=δ_ab F_a; ihre Summe mit F_neu ist I, und
M-Selbstadjungiertheit folgt aus B^sharp=L und E_a^sharp=E_a.
Für jeden nichtverschwindenden Elternzustand ψ gilt exakt

\[
\frac{\langle B\psi,F_a B\psi\rangle_{m+1}}{\|B\psi\|_{m+1}^2}
=\frac{\langle\psi,E_a\psi\rangle_m}{\|\psi\|_m^2},\qquad
p(F_{neu}\mid B\psi)=0. \tag{13}
\]

Das sind formal konsistente, transportierte **Präparationsrecords**. Sie
fragen nach einem festgelegten früheren Unterraum. Sie sind nicht identisch
mit der Frage, welche Geometrie oder Materiemenge der aktuelle Zustand
punktweise besitzt. Auch die Wahl einer Präparationsstufe m ist noch kein
relationaler Schnitt durch das Feld T. Die Standardanforderungen an
Messungen und Projektorzerlegungen sind in [1] beschrieben; ihre konkrete
CST-Deutung wird durch (12) nicht geliefert.

## 6. Labelinvariante Zustandsaussagen und Historiengewichte

Für eine messbare Aut-invariante Menge A in der aktuellen markierten
Konfiguration definiert E_A f=1_A f einen beschränkten idempotenten
Operator. Er ist im Referenz-L²-Produkt orthogonal. Im gewählten Produkt
M gilt das nur bei

\[
E_A^\dagger M=M E_A. \tag{14}
\]

Ein nichtdiagonales M kann verschiedene Geometrie- oder Feldbereiche
koppeln. Dann scheitert (14). Ein negativer Wert von <ψ,E_Aψ>_M/||ψ||²_M
ist eine falsche Messzuordnung, kein negativer physikalischer Messbefund.
Die Zulässigkeit wird hier auf dem gesamten erklärten Hilfsraum geprüft.
Ein später begründeter engerer physikalisch erreichbarer Raum ist gesondert
zu untersuchen.

### Exaktes Gegenbeispiel

Im binären Referenzmaß aus Abschnitt 8, bei m=2, M_1=2I und K=I,
haben die relevanten integrierten Orbitkoordinaten die Typen
A01 (Zweierantikette mit einem Staubmark) und C00 (Vakuum-Zweierkette).
Die entsprechenden Matrixelemente sind

\[
M_{A01,A01}=1,\quad M_{C00,C00}=19/2,\quad
M_{C00,A01}=−1/2. \tag{15}
\]

Wähle ψ=e_A01+4e_C00, und A=„mindestens ein innerer Staubmark ist
ungleich null“. Dann ||ψ||²_M=149 und <ψ,E_Aψ>_M=−1. Der vermeintliche
Bornwert ist −1/149. Diese Aussage ist auf markierten Isomorphietypen
definiert, also labelinvariant. Labelinvarianz allein reicht folglich
nicht. Für den gesamten Raum ist die Messzuordnung widerlegt; ψ wird
nicht als aus dem leeren Anfangszustand physikalisch erreichbarer Zustand
ausgegeben.

### Ein Gramfunktional bleibt möglich, ist aber kein PVM

Bei festem nichtverschwindendem ψ definiere stattdessen

\[
D(A,B)=\frac{\langle E_A\psi,E_B\psi\rangle_M}{\|\psi\|_M^2}.
\tag{16}
\]

Konvention: Das erste Argument des Skalarprodukts wird konjugiert.
D ist hermitesch, in beiden Ereignisargumenten additiv auf disjunkten
Vereinigungen, normalisiert durch D(Ω,Ω)=1 und stark positiv: Für jede
endliche Ereignisliste und komplexe c_i ist
Σ_ij c_i*D(A_i,A_j)c_j=||Σ_j c_j E_Ajψ||²_M/||ψ||²_M≥0.
μ(A)=D(A,A) erfüllt damit die Grad-2-Additivität.

Die drei Alternativen „0, 1, 2 Staubmarkierungen“ liefern im Gegenbeispiel

\[
D_{Atome}=\frac1{149}
\begin{pmatrix}152&-2&0\\-2&1&0\\0&0&0\end{pmatrix}. \tag{17}
\]

Die Summe aller Einträge ist eins, aber die Summe der Diagonalelemente
ist 153/149. Es liegt Interferenz vor; die Diagonalgewichte sind nicht
bereits eine normierte Verteilung exklusiver Messausgänge. Erst zusätzliche
Dekohärenzbedingungen oder ein explizites Messinstrument rechtfertigen eine
solche Wahrscheinlichkeitsdeutung. Starke Positivität einer endlichen
Ereignisalgebra beweist keine Fortsetzung des ursprünglichen Quantenmaßes
auf unendliche Historien [2].

## 7. Kohärente Endkontraktion als Auslese

Auf einer festen Stufe ist die aus (5) geerbte lineare Endkontraktion ℓ
im Referenzprodukt beschränkt: Es gibt endlich viele Geometrieblöcke,
normierte Feldmaße und eine Phase vom Betrag eins. Bei koerzivem M bleibt
sie beschränkt. Setze

\[
r_\ell=M^{-1}\ell^\dagger,\quad
d_\ell=\ell M^{-1}\ell^\dagger=\|\ell\|_{M,*}^2>0. \tag{18}
\]

Der Operator E_ℓ=λ M^{-1}ℓ†ℓ ist M-selbstadjungiert und positiv. Er ist
genau dann ein zulässiger Effekt, 0≤E_ℓ≤I, wenn

\[
0\le\lambda\le d_\ell^{-1}. \tag{19}
\]

Beweis: Der einzige nichtverschwindende Eigenwert ist λd_ℓ, mit
Eigenvektor r_ℓ. Für den Maximalwert λ=1/d_ℓ ist E_ℓ ein orthogonaler
Rang-eins-Projektor. Die skalare Krausabbildung K_ℓ=√λ ℓ erfüllt
K_ℓ^sharp K_ℓ=E_ℓ und kann durch √(I−E_ℓ) zu einem Instrument ergänzt
werden. Die Postselektionswahrscheinlichkeit ist
λ|ℓψ|²/||ψ||²_M. Eine bloße Amplitude ℓψ ist keine Wahrscheinlichkeit.
Eine Normierung, die nachträglich vom getesteten Zustand abhängt, ersetzt
kein festes lineares Messinstrument.

Im binären, phasenfreien Referenzfall mit K=I ergeben sich exakt:

| Stufe | d_ℓ für die Summenzeile ℓ=(1,…,1) | maximal λ |
|---|---:|---:|
| m=2 | 29/4 | 4/29 |
| m=3 | 757/12 | 12/757 |

Wird λ auf 2/d_ℓ gesetzt, liefert der Rieszvektor als Negativkontrolle
die unzulässige Wahrscheinlichkeit 2. Das ist keine physikalische Vorhersage.
Der frühere allgemeine Divergenzsatz für die vollständige normierte
geometriediagonale, feldunabhängige Klasse impliziert dort zusätzlich:
Ein festes positives λ kann nicht über alle m funktionieren, denn
d_ℓ→∞. Dieser Satz wird hier nicht auf sämtliche nichtdiagonalen Produkte
oder begründet eingeschränkte physikalische Räume ausgedehnt.

### Konsistenz beim Verschieben des Ausleseschnitts

Soll dieselbe lineare Auslese auf zwei Darstellungsstufen dieselbe Amplitude
liefern, ist ℓ_{m+1}B_m=ℓ_m erforderlich. Gleiche Rang-eins-Effekte erlauben
eine gemeinsame Phase; bei zusätzlicher skalarer Gewichtung wenigstens eine
gemeinsame komplexe Proportionalität. Aus der Isometrie allein folgt dies
nicht.

In der separat deklarierten **phasenfreien Referenz** (alle Wirkungsphasen
eins, Summenauslese) ist bei m=2→3 der Rückzug

\[
\ell_3B_2=(8/3,8/3,8/3,11/6,11/6,11/6,11/6),\quad
\ell_2=(1,1,1,1,1,1,1). \tag{20}
\]

Die ersten drei Koordinaten sind Antiketten, die übrigen Ketten. Keine
globale Skalierung macht diese Zeilen proportional. Das ist ein konkretes
Gegenbeispiel gegen die Folgerung „normerhaltende Fortsetzung genügt für
dieselbe Endauslese“. Es ist kein No-go für alle physikalischen Kopplungen,
Randzustände oder relationale Ausleseschnitte; im phasentragenden Modell
muss die tatsächliche Randphase mittransformiert und geprüft werden.

Formal kann man stattdessen ℓ_{m+1}^{tr}=ℓ_m L_m setzen. Dann gilt
ℓ_{m+1}^{tr}B_m=ℓ_m und ||ℓ_{m+1}^{tr}||=||ℓ_m||, weil L=B^sharp
eine Koisometrie ist. Im Referenzfall bleibt d_ℓ=29/4. Diese transportierte
Zeile wählt jedoch nur die privaten Kegelanteile aus (hier zusätzlich die
neue Markierung 0 mit Faktor 2); sie ist **nicht die ursprüngliche Endsumme
über alle Geometrien**. Ihre physikalische Bedeutung muss separat begründet
werden. Falls m verschiedene physikalische Zeiten oder Volumina meint,
muss nicht dieselbe Auslese verlangt werden; auch diese Interpretation ist
noch zu entscheiden.

## 8. Exakte endliche Kontrollen

Unabhängig vom analytischen kontinuierlichen Satz wird ν durch
zwei atomare Marken ersetzt: (T,w)=(-1,0) und (1,1/2), jeweils mit q=1/2.
Die Anker sind (T_a,w_a)=(-2,0), (T_f,w_f)=(2,0). Das erhält die
Vakuum-/Staub-Aufteilung als Teststruktur, ist aber **keine nachgewiesene
Approximation** von (2).

Die numerischen Koordinaten g_s sind integrierte Amplituden eines markierten
Orbits, nicht punktweise Werte der kontinuierlichen Funktion f_U. Für
eine Farbkonfiguration c auf U ist
g_[U,c]=(∏q(c_i)) a_U/a_[U,c] · f_U(c).
Dadurch lautet die unabhängige maximale-Löschungsformel in diesen
Koordinaten

\[
B_{s',s}=\sum_{z\in Max(s'),\;s'\setminus z\simeq s}
q(c_z)\frac{e_s a_s}{e_{s'}a_{s'}}. \tag{21}
\]

Hier zählen a_s die **markierten** Stabilisatoren. Die primäre Route
enumeriert dagegen für jeden natürlichen Elternvertreter alle Ideale und
neuen Marken mit Gewicht q(c)e(parent)/e(child), anschließend kanonisiert
sie. Beide Routen werden vollständig verglichen. Die Endkoeffizienten
sind ∏q/a_s. Werden die Marken summiert, bleibt die unmarkierte
phasenfreie Endsumme Σ_P1/e(P) erhalten.

Für die Matrixkonstruktion wird der private Kegel mit neuer Marke 0 gewählt.
Sein Vorwärtskoeffizient ist q_0=1/2, daher selektiert L die entsprechende
Zeile mit Faktor 2. Das ist ein gültiger diskreter Hilfs-L, nicht die
einzige diskrete Realisierung des kontinuierlichen Integrations-L aus (7).
M_1=diag(1/q_0,1/q_1)=2I normiert den erzeugten Vektor (1/2,1/2) auf eins.
K=I und K=2I werden jeweils bis m=3 untersucht. Die Matrizen sind nach
Entfernung der teleskopierenden Phase angegeben; die Wirkungsdifferenzen
werden zusätzlich exakt geprüft.

| Kontrolle | Umfang / Ergebnis |
|---|---|
| Natürliche markierte Zustände m=0,…,4 | 1, 2, 8, 56, 640; insgesamt 707 |
| Markierte Isomorphietypen | 1, 2, 7, 32, 192; insgesamt 234 |
| Vertreterspalten bis m=3 | 67 exakt gleich unter Relabeling |
| Unabhängige Matrixeinträge über Maximal-Löschung | 6.384 |
| Permutationen mit offener und geschlossener Wirkungsprüfung | 15.715 |
| Exakte Wirkungsinkremente | 706 |
| Positive M₂/M₃ für zwei Komplementgewichte | 4 Konstruktionen mit rationalen LDL-Zertifikaten |
| Transportierte PVMs | 4 vollständige Matrixprüfungen; Wahrscheinlichkeiten 1/2, 1/2 und Nullen |
| Endliche Ereignisalgebra | 8 Ereignisse; 216 Additivitäts- und 64 Grad-2-Prüfungen |
| Negative Messzuordnung | −1/149, erwartetes FAIL |
| Endauslese | zwei Rang-eins-Effektprüfungen, Überskalierung 2, Schnittdefekt (20) |
| Isolierter Replay | sechs Ergebnisdateien bytegleich |

Der Plan wurde vor Implementierung und endlicher Auswertung lokal gehasht.
Die analytischen Mechanismen waren bereits vorab überlegt; das ist keine
blinde Vorhersage oder externe Präregistrierung. Python benutzt für die
Kontrollen ausschließlich Standardbibliothek und rationale Arithmetik.
Die Phase wird über exakte rationale Wirkungsbestandteile geprüft, nicht
durch gerundete komplexe Exponentialwerte. Die wiederholte Rechnung in
einem frischen temporären Verzeichnis ist eine Reproduzierbarkeitskontrolle,
keine unabhängige wissenschaftliche Replikation.

## 9. Was nun wirklich noch fehlt

Die mathematische Existenz markierter Hilfsräume ist geklärt. Offen bleibt
eine **physikalisch begründete gemeinsame Auswahl** von erlaubten Zuständen,
Produkt, Präparation, relationalem Uhrschnitt und Ausleseinstrument. Dafür
soll der nächste Schritt einen einzigen konkreten Kandidaten festlegen:

1. Eine labelinvariante Präparationsklasse und einen durch T definierten
   Ausleseschnitt mit wohldefinierter Domäne angeben. Eine formale
   m-Stufe darf nicht stillschweigend als physikalische Zeit dienen.
2. Ein konkretes M und die zulässigen Effekte durch eine zusätzliche
   physikalische Bedingung begründen; reine Existenz oder Positivität
   kann die freie K-Wahl nicht bestimmen.
3. Die tatsächlich geerbte Randkontraktion einschließlich Phase an diesem
   Kandidaten prüfen: Beschränktheit, Instrumentnormierung und - falls
   es nur ein Darstellungswechsel ist - Schnittkompatibilität. Bei einem
   geänderten Funktional muss die geänderte physikalische Frage benannt werden.

Erst danach folgen Messwahrscheinlichkeiten und die bereits offenen
Korrespondenz-/Rückwirkungs-, Außenraum-, Regularitäts- und Bounce-Prüfungen.
Dieses Paket schließt keine dieser acht physikalischen Prüfungen ab.

## Quellen und Provenienz

Die neuen Formeln (4), (6)-(14), (18)-(21) sind explizite Ableitungen für
die geerbte Darstellung. Die folgenden Quellen liefern die allgemeinen
Begriffe; sie werden nicht als Beleg einer bereits gelösten CST-Physik verwendet.

[1] John Watrous, *The Theory of Quantum Information*, Cambridge University
Press (2018), Kapitel 2, Definition 2.34 und Abschnitt 2.3 über projektive
Messungen und Instrumente. Primärquelle:
https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf . Nur verlinkt, nicht im
Paket nachgedruckt. Messungen werden durch positive Effekte beschrieben,
deren Summe die Identität ist; Projektionsmessungen sind der spezielle
orthogonale Fall.

[2] Fay Dowker, Steven Johnston, Sumati Surya, *On extending the Quantum
Measure*, J. Phys. A 43, 505305 (2010),
https://arxiv.org/abs/1007.2725v1 . Die Fortsetzung eines stark positiven
Dekohärenzfunktionals ist eine zusätzliche Vektormaß-Frage; endliche
Hilbertraumdarstellungen allein erledigen sie nicht.

Alle sieben verwendeten Repositorydateien liegen bytegleich in `inputs/`.
`inputs/git_sources.json` pinnt Pfad, Commit und Git-Blob-SHA; `analyze.py`
prüft diese vor jeder Rechnung. Die Vorgängerableitungen enthalten die
weiteren Quellen für die regulierte Wirkung und den alten Normvertrag.
Der vorherige Vertrag bleibt als historische Quelle unverändert; die neue
abgegrenzte Bewertung steht in `event_contract.json`.
