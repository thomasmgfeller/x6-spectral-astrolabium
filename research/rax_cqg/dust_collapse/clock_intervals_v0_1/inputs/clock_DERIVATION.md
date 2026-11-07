# CST-DUST: Relationale Uhr und Prüfung eines Evolutionskandidaten v0.1

Stand: 7. November 2026. Basis: Main `5e08cef8dcac5c7d1214dd2beff1b1533427e856`
nach PR 251, Repository `thomasmgfeller/x6-spectral-astrolabium`.
Prüfplan: `CST-DUST-RELATIONAL-CLOCK-001`.

## Ergebnis

Ein konkreter nächster Kandidat verbindet eine kausal geordnete Materieuhr,
eine explizite Präparation, ein lokales Konfigurationsprodukt und scharfe
Uhrereignisse. Seine zusätzliche Deutung als **geschlossene normerhaltende
Fortsetzung um genau ein Element** scheitert. Der Ausschluss gilt auf den
vollständigen erklärten Stufenräumen für alle beschränkten positiven
Kindprodukte und koerziven positiven Elternprodukte, einschließlich
nichtdiagonaler Produkte. Er gilt schon bei einer festen endlichen Stufe;
es ist kein unkontrolliertes N→∞-Argument.

Dabei ergeben sich drei nutzbare Resultate:

1. Im monotonen Uhrsektor ist die eindeutige chronologische Umnummerierung
   exakt möglich. Der frühere Faktor 1/e(P) darf danach nicht nochmals
   verwendet werden. Die korrekte chronologische Amplitude hat diesen
   Faktor nicht. Die vorherige **Auswahl des monotonen Sektors** verändert
   dagegen die Historienmenge und ist keine bloße Eichumbenennung.
2. Für das Referenzprodukt hat die Fortsetzung den exakten Normfaktor
   d(P)(L−T_m)/(2L), mit d(P)=Anzahl der Vergangenheitsideale. Nahe dem
   oberen Uhrregulator geht er gegen null. Deshalb existiert auf diesen
   ganzen Räumen kein äquivalenter beschränkter Normpfad, der diesen
   Ein-Geburts-Schritt isometrisch macht.
3. Eine positive Zweiausgangs-Ergänzung „Geburt / keine Geburt“ ist
   algebraisch möglich, besitzt aber einen freien Skalenfaktor. Sie ist
   weder eine hergeleitete Wartezeitregel noch eine aus CST gewonnene
   Evolution zwischen festen Materie-Uhrwerten.

Der konkrete Zusatzkandidat erhält **FAIL**. Die übergeordneten physikalischen
Gates MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING,
EXTENSION bleiben **HOLD**. Ein physikalischer Hilbertraum, eine globale Uhr
im Vakuumaußenraum, Junction-Dynamik, ein Bounce oder Singularitätsauflösung
sind nicht gewonnen. Frühere spezifische FAILs werden nicht aufgehoben.

## 1. Motivation und ausdrücklich gewählte Daten

Der geerbte Materiekandidat ist

\[
S_d=-\frac12\sum_xw_x(\Gamma_x[T]+1),\qquad
\Gamma_x[T]=\frac12\sum_{y\prec x}B_{xy}(T_x-T_y)^2,
\quad B_{xy}=A\,b(k(y,x)),\quad b=(1,-9,16,-8,0,\ldots). \tag{1}
\]

Im Code gilt A=ℏ=1. Die Gravitationswirkung bleibt der geerbte reelle
BDG-Ausdruck. w ist ein integriertes Dichtegewicht, keine kalibrierte
Ruhemasse. Der formal motivierende Kontinuumsausdruck ist der bereits
diskutierte wirbelfreie Staub mit zeitartigem Einheitsgradienten von T.
Eine Zukunftsorientierung motiviert ein entlang kausaler Relationen
wachsendes T vor Kaustiken. Kontinuumskonstruktionen mit Staubuhren
existieren [1,2]; sie liefern keinen Hamiltonoperator dieser CST-Amplitude.
Die BD-Operatorreferenz [3] rechtfertigt keinen ungeprüften Austausch von
Kontinuumsgrenze, Variation, Randbehandlung und Quantisierung.

Wir wählen und prüfen jetzt folgenden zusätzlichen Kandidaten:

- Alle alten Ordnungs- und T,w-Daten bleiben erhalten; unabhängige kompakte
  Feldmaße werden vor der Sektorwahl beibehalten.
- Es werden nur vollständige Geschichten mit T_y<T_x für y≺x betrachtet.
  Alle inneren T-Werte sind paarweise verschieden. Bei kontinuierlichem
  Uhrmaß entfernt die zweite Bedingung nur eine Nullmenge.
- Die eindeutige Reihenfolge der T-Werte dient zur Hilfsbeschriftung.
  „Fortsetzung um eins“ fügt ein größeres T als alle bisher vorhandenen an.
- Als lokale Hilfsnorm dient zunächst das L²-Produkt dieser chronologischen
  Konfigurationen. Indikatoren aktueller Uhrbereiche und Staubmarkierungen
  sind darin selbstadjungierte Projektoren.
- Eine explizite positive Staubpräparation wird auf einer Ein-Element-Stufe
  gewählt. Es wird geprüft, ob die deklarierte Fortsetzung geschlossen
  normerhaltend ist und ob ein äquivalentes Produkt sie retten kann.

Diese Wahl ist physikalisch motiviert, aber nicht aus Constraints abgeleitet.
Insbesondere ist die Mikrozustandsbedingung strenger als eine Forderung an
einen semiklassischen Sattel: Quantenhistorien dürfen off shell sein.
Das im w=0-Sektor mitgeführte Hilfs-T wird durch seine Sortierung nicht zu
einer physikalischen Uhr des Vakuums. Ein Materie-Uhrschnitt nur im
Staubbereich wäre noch kein vollständiger Innen-/Außenraumschnitt.

Die unabhängigen Feldmaße sind

\[
d\nu_T=\frac{dT}{2L},\quad -L\le T\le L,\qquad
d\nu_w=\frac12\delta_0+\frac12\mathbf1_{(0,1)}(w)dw. \tag{2}
\]

In der Enumeration gilt L=1. Anfangs- und Endanker liegen bei T_a=−2,
T_f=2 mit w_a=w_f=0; sie sind extern fixiert und werden nicht mitgezählt.
Das gesonderte Stationaritätsbeispiel in Abschnitt 7 hat eigene ausdrücklich
angegebene Randwerte. S_outer=0 bleibt eine geerbte Modellannahme.

## 2. Ein durch T definierter Schnitt braucht einen Uhrsektor

Für eine vollständige markierte Ordnung setze

\[
J_\tau(C,T)=\{x:T_x\le\tau\}. \tag{3}
\]

Ist T kausal streng monoton, dann ist J_τ ein Ordnungsideal: Aus
y≺x und T_x≤τ folgt T_y<T_x≤τ. Die Konstruktion ist unter gemeinsamer
Umbenennung von Geometrie und Feldern invariant. Die maximalen Elemente
von J_τ bilden eine Antikette, müssen aber ohne weitere Annahmen weder
eine kontinuierliche Cauchyfläche noch eine ausreichend vollständige
Anfangsdatenfläche darstellen. Die unverändert benötigte nichtlokale
Vorgeschichte wird nicht durch diese Antikette ersetzt.

Im bisherigen freien Uhrmaß ist (3) dagegen nicht notwendig ein Ideal.
Schon für 1≺2 mit T_1=1/2, T_2=−1/2 enthält J_0 nur Element 2 und
verliert seinen Vorgänger. Die Sortierung der Labels allein korrigiert
das nicht: Die Kausalrelation würde in der sortierten Darstellung rückwärts
zeigen. Daher sind **kausale Monotonie auswählen** und **einen ausgewählten
Zustand nach Uhrwerten beschriften** zwei verschiedene Schritte.

## 3. Chronologische Beschriftung und korrektes Zählgewicht

P bezeichnet eine natürliche innere Ordnung mit m Elementen. e(P) zählt
ihre linearen Erweiterungen. Die geerbte endlich erzeugte Amplitude enthält
1/e(P), weil die bisherigen Fortsetzungsfaktoren e(parent)/e(child)
teleskopieren. Sei

\[
D_P=\{T\in[-L,L]^m:T_y<T_x\ \mathrm{für}\ y\prec_Px\},\qquad
\Delta_m=\{-L<T_1<\cdots<T_m<L\}. \tag{4}
\]

Sei F(P,T,w) integrabel und invariant unter gemeinsamen Umbenennungen.
F darf die vollständige Wirkungsphase, Randphase, Präparation und ein
kovariantes Ereignis enthalten. Dann gilt die **exakte endliche Identität**

\[
\sum_{P\in\Omega_m^{nat}}\frac1{e(P)}
 \int_{D_P} F(P,T,w)d\nu_T^m d\nu_w^m
=\sum_{P\in\Omega_m^{nat}}
 \int_{\Delta_m}F(P,T,w)d\nu_T^m d\nu_w^m. \tag{5}
\]

**Beweis.** Außerhalb der Nullmenge gleicher Uhren bestimmt T eine eindeutige
lineare Erweiterung seiner Geometrie. Sortiere danach und permutiere alle
w-Marken mit. Jeder vollständig markierte chronologische Datensatz hat
genau e(P) natürliche Beschreibungen vor dieser Sortierung; seine
Geometrie hat in jeder Beschreibung dieselbe Erweiterungszahl e(P).
Die e(P) gleichen Beiträge mit Gewicht 1/e(P) addieren sich zu eins.
Gemeinsame Feldpermutationen bewahren das Produktmaß. Das gilt auch bei
Geometrie-Automorphismen: Die verschiedenen Uhrwerte entfernen jeden
nichttrivialen **vollständig markierten** Stabilisator. Alternativ zerlegt
man jeden geometrischen Uhrbereich D_P in seine e(P) gleich großen
Ordnungs-Kammern und gruppiert gleiche chronologische Darstellungen. ∎

Der richtige chronologische Repräsentant hat deshalb die erzeugte
Amplitudenfunktion exp(iS/ℏ) mit Koeffizient eins. Der frühere Faktor
1/e(P) darf nicht nach der Sortierung nochmals stehen bleiben. Seine
Entfernung in (5) ist eine exakt begründete Darstellungsänderung **innerhalb
des ausgewählten Sektors**, keine neue Anpassung der Wirkung.

Diese Identität betrifft vollständige feste-m-Summen und darin deklarierte
invariante Einfügungen. Sie ist **keine Behauptung**, dass die neue
chronologische Präfixfortsetzung durch unitäre Konjugation aus dem alten
V für jeden beliebigen natürlichen Präfixzustand hervorgeht. Der alte V
erlaubte eine spätere Geburt mit einem kleineren T als bisher vorhandene
unvergleichbare Elemente. Die chronologische Zerlegung gruppiert solche
Beschreibungen um. Eine Präparation am frühesten T ist eine andere
Definition als eine Präparation am ersten beliebig gewählten Geburtslabel.

### Die Sektorwahl selbst verändert die Amplitude

Unter dem normierten unabhängigen Uhrmaß ist

\[
\nu_T^m(D_P)=\frac{e(P)}{m!},\qquad
\nu_T^m(\Delta_m)=\frac1{m!}. \tag{6}
\]

Alle m! strikten Zeitordnungen haben gleiches Maß; genau e(P) sind kausal
zulässig. Schon bei zwei Elementen haben eine Kette und eine Antikette
verschiedene D_P-Massen. Im phasenfreien, über alle Felder integrierten
Beispiel lauten ihre ungelabelten Koeffizienten:

| Geometrietyp | Ohne Monotonieselektion | Nach Monotonieselektion |
|---|---:|---:|
| Zweierantikette | 1/2 | 1/2 |
| Zweierkette | 1 | 1/2 |

Es gibt keine gemeinsame Skalierung, die diese relative Änderung rückgängig
macht. Jede Geometrie separat auf bedingte Maßmasse eins zu normieren wäre
eine weitere Modelländerung, keine Reparatur einer bloßen Labelkonvention.
Die Zahlen sind Amplitudenkoeffizienten im phasenfreien Beispiel, keine
physikalischen Wahrscheinlichkeiten.

| m | Freie Summe Σ_P1/e(P) | Uhrsektor | Falsch zusätzlich beibehaltenes 1/e |
|---|---:|---:|---:|
| 2 | 3/2 | 1 | 3/4 |
| 3 | 19/6 | 7/6 | 19/36 |
| 4 | 73/8 | 5/3 | 73/192 |

## 4. Präparation, Produkt und feste Endauslese sind konkret definiert

Der ausgewählte Hilfsraum lautet

\[
\mathcal H_m^{chron}=\bigoplus_{P\in\Omega_m^{nat}}
L^2(\Delta_m\times[0,1]^m,d\nu_T^m d\nu_w^m). \tag{7}
\]

Da die Uhrwerte die Beschriftung eindeutig festlegen, sind P-Blöcke nun
verschiedene vollständig markierte Konfigurationen. Die gewöhnliche lokale
Norm ist zunächst M_m=I. Indikatoren einer Partition nach J_τ,
Staubmarkierungen oder Uhrfenstern bilden darin eine orthogonale
Projektorzerlegung. Das ist eine definierte Hilfs-Messvorschrift, noch keine
hergeleitete gravitative Dirac-Observable.

Für m=1, L=1 und ein Intervall I⊂(−1,1) wird ausdrücklich die normierte
positive Staubpräparation gewählt:

\[
\psi_I(T,w)=\sqrt{4/|I|}\,\mathbf1_I(T)\mathbf1_{w>0}. \tag{8}
\]

Die Norm ist eins, weil das Uhrintervall Maß |I|/2 und das positive
Dichtestratum Maß 1/2 besitzt. Geprüft werden I_−=[−1/2,0] und
I_+=[0,1/2]. Die Definition ist labelinvariant und unabhängig von einem
gewünschten Bounce. Sie unterstellt noch nicht Γ=−1 oder die Uhrgleichung.

Auch eine feste kohärente Endauslese ist wohldefiniert:

\[
\ell_m(\psi)=\sum_P\int_{\Delta_m}b_m(P,T,w)\psi_P(T,w)d\nu^m,
\quad |b_m|=1,\qquad
\|\ell_m\|_*^2=\frac{|\Omega_m^{nat}|}{m!}. \tag{9}
\]

Die Norm folgt aus dem Rieszvektor mit Betrag eins und der Maßmasse jedes
Blocks. Der Endeffekt E_ℓ=λℓ†ℓ ist bei festem m zulässig für
0≤λ≤m!/|Ω_m^nat|. Beispielsweise lauten die oberen Grenzen bei m=2,3,4
1, 6/7, 3/5. Die Randphase wird nicht zu einer Wahrscheinlichkeit erklärt;
sie muss mit dem tatsächlichen Randzustand spezifiziert werden. Eine feste
Auslese und positive Ereignisse lösen die folgende Fortsetzungsprüfung nicht.

## 5. Der chronologische Ein-Geburts-Schritt ist keine geschlossene Isometrie

Die durch (5) motivierte chronologische Faktorisierung trägt beim Anfügen
eines neuen maximalen Elements mit Ideal J die Phase der exakten
Wirkungsdifferenz, jedoch keinen zusätzlichen Erweiterungsfaktor:

\[
(A_m\psi)(P+(J),T_1,\ldots,T_m,t,w,u)
=e^{i\Delta S/\hbar}\psi(P,T,w),\qquad T_m<t<L. \tag{10}
\]

Alle alten Daten bleiben erhalten. Das größere t macht die globale Uhrordnung
automatisch konsistent, für jedes Vergangenheitsideal J von P. J wird
kausal mit dem Anfangsanker verbunden wie im Vorgänger. Der eindeutige
chronologische Elternzustand entsteht durch Entfernen des Elements mit
größtem T. Unterschiedliche Elternbeiträge werden in (10) deshalb nicht
an derselben Kindkonfiguration kohärent zusammengeführt.

Sei d(P)=|Ideals(P)|. Integration des neuen T und des normierten neuen
Dichtefelds ergibt **genau**

\[
A_m^\dagger A_m=r_m(P,T_m)I_{\mathrm{mult}},\qquad
r_m(P,T_m)=d(P)\frac{L-T_m}{2L}. \tag{11}
\]

Die Wirkungsphase hebt sich im Normquadrat auf, auch für die tatsächlich
geerbten nichtverschwindenden Kopplungen. (11) ist also kein phasenfreies
Näherungsargument. Unterschiedliche Geometrien können unterschiedliche
d(P) besitzen. Es gilt ||A_m||²=2^m: Eine m-Antikette hat alle 2^m
Teilmengen als Ideale; Uhrpakete mit T_m nahe −L nähern den Supremumswert.
Für jedes feste m ist A_m beschränkt und injektiv, aber für m≥1 nicht
nach unten beschränkt.

Die beiden normierten Präparationen (8) ergeben bei m=1 und L=1:

\[
\|A_1\psi_{I_-}\|^2=5/4,\qquad
\|A_1\psi_{I_+}\|^2=3/4. \tag{12}
\]

Keine gemeinsame skalare Normierung macht beide Werte eins. Ein neuer
Geburtsschritt ist nicht dasselbe wie ein vorgegebener Schritt in der
Materieuhr: Die verbleibende Uhrmaßmasse hängt von der Konfiguration ab.

### Allgemeiner Ausschluss äquivalenter beschränkter Produkte

**Satz.** Sei m≥1. Auf den vollständigen Räumen (7) existieren kein
koerzives Elternprodukt M_m≥aI mit a>0 und kein beschränktes positives
Kindprodukt 0≤M_{m+1}≤bI mit endlichem b, sodass
A_m†M_{m+1}A_m=M_m. Das gilt auch für nichtdiagonale und feldabhängige
Produkte und nach jeder festen von null verschiedenen skalaren
Multiplikation von A_m.

**Beweis.** Fixiere einen Geometrieblock P. Wähle normierte Wellenpakete,
deren letzte Uhr gleichmäßig in (L−ε,L) liegt. Bei m>1 können alle früheren
Uhren in einem festen, davon getrennten unteren geordneten Bereich liegen.
Die übrigen Marken können mit beliebiger normierter Feldfunktion versehen
werden. Nach (11) gilt exakt

\[
\|A_m\psi_\varepsilon\|^2=\frac{d(P)\varepsilon}{4L}\longrightarrow0.
\tag{13}
\]

Eine Isometrie in den behaupteten Produkten würde verlangen

\[
a\le\langle\psi_\varepsilon,M_m\psi_\varepsilon\rangle
=\langle A_m\psi_\varepsilon,M_{m+1}A_m\psi_\varepsilon\rangle
\le b\frac{d(P)\varepsilon}{4L}\longrightarrow0,
\]

ein Widerspruch. Jede feste Skalierung verändert nur b um einen festen
Faktor. ∎

Die fünf exakten m=1-Kontrollwerte für ε=1/2,1/4,1/8,1/16,1/32
lauten 1/4,1/8,1/16,1/32,1/64. Die allgemeine Aussage folgt aus dem
Grenzargument für beliebig kleine ε, nicht aus fünf Testpunkten.

Das widerspricht dem markierten Normsatz aus PR 251 nicht. Dort durfte das
neue Uhrfeld über sein ganzes unabhängiges Intervall laufen. Die private
Kegelabbildung hatte eine normierte Feldfaser und eine beschränkte
Linksinverse. Die neue Bedingung t>T_m macht die Fasermaßmasse beliebig
klein. Die Voraussetzung der früheren Konstruktion ist damit geändert.

### Reichweite und nicht ausgeschlossene Alternativen

Der Satz betrifft den ganzen erklärten Stufenraum mit festem Uhrregulator
und genau einer Geburt. Physikalisch begründete eingeschränkte Räume,
Uhrpakete mit garantiertem Abstand zum Regulatorende, unbeschränkte oder
nichtkoerzive Produkte, ein anderer Träger, eine andere Amplitude und eine
Evolution mit variabler Elementzahl sind nicht ausgeschlossen.
Der Regulatorendpunkt ist keine physikalische Singularität. Dies ist kein
No-go für CST, eine Staubuhr oder alle Quantendynamiken.

Die formale Normierung A_m r_m^{-1/2} würde auf dem natürlichen dichten
Definitionsbereich zu einer Isometrie fortgesetzt werden können, weil
r_m>0 fast überall und (11) gilt. Sie verändert jedoch die Amplituden
konfigurationsabhängig. Das ist ein anderer linearer Operator, nicht die
unveränderte Faktorisierung von (5). Eine solche Wahl braucht eine eigene
physikalische Begründung; sie wird hier nicht als reparierte CST-Dynamik
übernommen.

## 6. Eine algebraische Zweiausgangs-Ergänzung zeigt die fehlende Auswahl

Wähle 0≤α≤2^{-m}. Dann ist

\[
K_{Geburt}=\sqrt\alpha\,A_m,\quad
E_{Geburt}=\alpha r_m,\qquad
K_{keine}=\sqrt{I-\alpha r_m},\quad
E_{keine}=I-\alpha r_m,\quad
E_{Geburt}+E_{keine}=I. \tag{14}
\]

Beide Krausabbildungen zusammen definieren ein normiertes Instrument mit
Ausgängen in H_{m+1} beziehungsweise H_m (oder in deren markierter direkter
Summe). Die positive Quadratwurzel ist durch den beschränkten
Multiplikationsoperator wohldefiniert. Vollständigkeit folgt aus (11),
nicht aus einer nachträglichen Normierung jedes getesteten Zustands.

Bei m=1 unterscheiden sich zwei gleichermaßen zulässige Entscheidungen:

| α | P(Geburt bei I_−) | P(Geburt bei I_+) |
|---|---:|---:|
| 1/4 | 5/16 | 3/16 |
| 1/2 | 5/8 | 3/8 |

Die komplementären Wahrscheinlichkeiten ergänzen jeweils auf eins. Die
Wahl α=1 verletzt dagegen die Effektgrenze: Bei T_1=−1/2 wäre
E_Geburt=3/2 und E_keine=−1/2. Das ist eine Negativkontrolle, kein
physikalisch gültiges Instrument.

(14) ist ein **Hilfsinstrument**, keine hergeleitete Wartezeit- oder
Poisson-Regel. Es führt einen zusätzlichen Ausgang und eine freie
relative Gewichtung zwischen verschiedenen Elementzahlen ein. Wiederholte
„keine Geburt“-Ausgänge bewegen noch keine physikalische Uhr. Ein
vorgegebenes Δτ, die zugehörige Präparations-/Randstruktur und die
Komposition zwischen festen τ-Werten fehlen. Die vorhandene feste-m-Summe
bestimmt α nicht. Deshalb wird keiner der beiden Werte als physikalisch
ausgewählt ausgegeben.

Ein vollständiges hypothetisches Experiment könnte anschließend den
Endeffekt aus (9) innerhalb des Geburtsausgangs auslesen. Dessen Erfolg
ist dann eine zusätzliche Postselektion. Das ändert nichts an der offenen
Begründung des gesamten Instruments und rechtfertigt keine neue
Bounce-Wahrscheinlichkeit.

## 7. Uhrstationarität ist nicht durch Präfixstationarität erledigt

Die geerbte Wirkung hat auf einem offenen positiven Dichtestratum
∂S/∂w_x=−(Γ_x+1)/2. Ihre Uhrvariation enthält den Strom

\[
j_{y\to x}=\frac12 w_xB_{xy}(T_x-T_y),\qquad
q_z=\partial S/\partial T_z=\sum_{z\to x}j-\sum_{y\to z}j. \tag{15}
\]

Die vollständige Variation wurde schon im Vorgänger hergeleitet. Neu
prüfen wir einen konkreten Uhr-geordneten Anfügungsschritt:

- Altes Präfix a≺y: T_a=0, T_y=11/45, w_a=w_y=0.
  Die freie Hilfsuhr y ist stationär: q_y=0.
- Füge z oberhalb von y an: T_z=43/90, w_z=1/2. a und der neue
  Auslesewert T_z werden im Randwertvergleich gehalten; T_y bleibt frei.

Die Uhren sind streng geordnet. Wegen B_zy=1 und B_za=−9 gilt

\[
\Gamma_z=\frac12[(7/30)^2-9(43/90)^2]=-1,
\qquad \frac{\partial S}{\partial w_z}=0. \tag{16}
\]

Trotz erfüllter neuer innerer Dichtestationarität ändert sich die alte
Uhrgleichung zu

\[
q_y=\frac14(7/30)=7/120\ne0. \tag{17}
\]

Der vollständige Gradientenvektor ist (−43/40,7/120,61/60); seine Summe
ist null. Exakte zentrale Differenzen der vollständigen quadratischen
Wirkung bestätigen alle Komponenten. Die positive Dichtevariation wird
ebenfalls exakt gegen die vollständige lineare w-Wirkung geprüft.

Das Beispiel zeigt: Ein stationäres freies Präfix und die neue
Dichtenormierung allein machen die längere Geschichte nicht stationär.
Das alte Feld muss im vollständigen Randwertproblem erneut reagieren.
Ein aus der Wirkung erst noch herzuleitendes Anfangswert- oder
Constraint-System kann zusätzliche Daten wie konjugierte Impulse oder
Randzustände verlangen. Der Befund behauptet weder physikalische
Akausalität noch, dass q=0 bereits ein kanonischer Quantenconstraint sei.
Insbesondere bleibt der frühere Nachweis erhalten, dass naives Auferlegen
von Γ+1 als Multiplikationsconstraint im freien L²-Raum keine korrekte
physikalische Reduktion liefert.

## 8. Exakte Kontrollen und Reproduzierbarkeit

Für die endliche Identität (5) werden Uhrgitter mit 5 und 6 Werten in
[−1,1], paarweise verschiedene Uhren und binäre Dichtemarken w=0,1/2
mit Gewichten 1/2 verwendet. Diese endlichen Maße sind selbständige
Kontrollmaße; keine kontrollierte Approximation des kontinuierlichen
Pfadintegrals wird behauptet. Inkomparablen Uhrgleichständen wird hier
explizit ebenfalls Maß null zugewiesen, indem nur verschiedene Gitterwerte
zugelassen werden. Es erfolgt keine versteckte Nachnormierung.

Die primäre Route enumeriert alle natürlichen Ordnungen, alle verschiedenen
Gitter-Zuweisungen und alle Dichtemarken; sie behält die kausal geordneten
Fälle und summiert mit 1/e(P). Die unabhängige Route benutzt nur steigende
Uhrtupel und alle natürlichen Ordnungen mit Koeffizient eins. Die Gleichheit
wird für jeden vollständigen chronologischen markierten Datensatz geprüft,
nicht nur für eine einzelne Gesamtsumme. Offene und geschlossene
Wirkungen bleiben bei der gemeinsamen Sortierung exakt gleich.

| Prüfung | Umfang / Ergebnis |
|---|---|
| Markierte natürliche Darstellungen in beiden Kontrollgittern | 88.324 |
| Vollständige chronologische Kontrollrecords | 14.704 |
| Gemeinsame Umbenennung, offene und geschlossene Wirkung | 88.324 exakte Doppelprüfungen |
| Schwellen-J_τ als Ordnungsideal | 29.440 Prüfungen |
| Fehlerhaft verbliebener 1/e-Faktor | 14.020 abweichende Recordkoeffizienten erkannt |
| Wellenpaket-Normen | 350 exakte Werte auf 50 natürlichen Elternordnungen |
| Zweiausgangs-Effekte | 250 punktweise Kontrollen und vier Präparationspaare |
| Präfixstationarität | rationales Gegenbeispiel; drei Uhr- und eine Dichteableitung geprüft |
| Isolierter Replay | sechs Ergebnisdateien bytegleich |

Python 3.10+, Standardbibliothek, `fractions.Fraction`; kein Monte Carlo,
keine neue vierdimensionale dynamische CST-Stichprobe und keine bezahlten
Läufe. Die allgemeine Normobstruktion ist analytisch bewiesen; die endlichen
Werte illustrieren sie. Es wurde kein formaler Beweisassistent eingesetzt.

Der Plan wurde lokal vor Implementierung und endlicher Enumeration gehasht.
Die Mechanismen wurden analytisch vorab überlegt. Das ist keine blinde
Vorhersage oder externe Präregistrierung. Die isolierte Nachrechnung ist
keine unabhängige wissenschaftliche Replikation.

## 9. Konsequenz für den nächsten physikalischen Schritt

Der geprüfte Ansatz aus Uhrsektor, lokaler Präparation und scharfer
Konfigurationsauslese ist definiert. Sein Anspruch einer geschlossenen,
genau-eine-Geburt-Evolution mit äquivalenten beschränkten Produkten ist
verworfen. Die offenen Voraussetzungen dürfen nicht durch die freie Wahl
eines neuen M oder eine stille Umgewichtung verdeckt werden.

Als nächstes braucht das Programm eine **Evolution oder Historienzuordnung
zwischen festgelegten relationalen Uhrwerten mit variabler Elementzahl**.
Die Regeln für keine, eine oder mehrere neue Elemente sowie die gemeinsamen
Rand- und Materiedaten müssen aus einer begründeten Quantendefinition
stammen. Alternativ ist ein begründeter physikalischer Unterraum mit
anderer Auslesedeutung zu prüfen. Ein beliebiger Instrumentabschluss wie
(14) genügt nicht zur Auswahl.

Eine solche Regel muss die Wirkung und das Zählmaß reproduzieren oder ihre
Änderung ausdrücklich begründen, den Vakuumaußenraum behandeln, zulässige
Ereignisse liefern und die behauptete Komposition prüfen. Erst danach sind
die weiterhin getrennten Korrespondenz-, Rückwirkungs-, Anschluss-,
Regularitäts- und Bounce-Prüfungen physikalisch interpretierbar.

## Quellen

[1] J. D. Brown, K. V. Kuchař, *Dust as a Standard of Space and Time in
Canonical Quantum Gravity*, Phys. Rev. D 51, 5600 (1995),
https://arxiv.org/abs/gr-qc/9409001v1 . Kontinuumsreferenz einer
Staubzeitreduktion; kein CST-Hamiltonian.

[2] J. Świeżewski, *On the properties of the irrotational dust model*,
Class. Quantum Grav. 30, 237001 (2013),
https://arxiv.org/abs/1307.4687v2 . Die Zeit-Eichwahl ist Teil einer
konkreten kanonischen Konstruktion und kann nicht allein durch eine
Sortierung diskreter Daten ersetzt werden; letztere Abgrenzung ist unsere
Einordnung, keine Behauptung des Artikels über CST.

[3] D. M. T. Benincasa, F. Dowker, *The Scalar Curvature of a Causal Set*,
Phys. Rev. Lett. 104, 181301 (2010), korrigierte Fassung
https://arxiv.org/abs/1001.2725v4 . Referenz für den geerbten
retardierten Operatorkandidaten unter seinen Kontinuumsvoraussetzungen.

Die Quellen werden nur verlinkt. Sechs verwendete Repositorydateien liegen
bytegleich in `inputs/` und sind durch Commit, Pfad und Git-Blob-SHA
gepinnt. `analyze.py` prüft sie bei jedem Lauf. Die hier gezeigten
Zähl-, Norm- und Gegenbeispielrechnungen werden im Text abgeleitet; es
wird keine mathematische Neuheit beansprucht.
