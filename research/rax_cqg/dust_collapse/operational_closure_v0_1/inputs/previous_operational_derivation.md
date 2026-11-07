# CST-DUST: Messmodell und kontinuierliche Materiephase v0.1

Stand: 7. November 2026. Basis: Main nach PR 254,
`35a0d886c4a7ca1d639f09b2933ffeb6c255ad9e`.
Sechs Originalquellen sind in `inputs/provenance.json` mit Git-Blob-SHA gepinnt.
Dies ist eine konditionale Referenzkonstruktion. **Alle acht physikalischen
Gates bleiben HOLD.** Die Ergebnisse wählen weder eine kosmologische finale
Randbedingung noch einen physikalischen Detektor aus.

## 1. Die neue Aufgabe

Der Vorgänger konstruiert beschränkte kohärente Endeffekte und deren
konsistenten Rücktransport. Offen bleiben eine operationale Begründung der
Auslese sowie das kontinuierliche Integral bei nichtverschwindender Materiephase.
Hier werden drei konkret abgegrenzte Punkte bearbeitet:

1. Ein explizites Hilfssystem realisiert die Zahlkanäle mit kohärentem Filter.
   Es zeigt zugleich, welche zusätzliche Operation ein bloßer Elementzähler
   nicht leisten kann. Eine tatsächlich verfügbare Kopplung wird nicht behauptet.
2. Für die Zahlsektoren n=0,1,2 werden die kontinuierlichen Uhr- und
   Dichtemarken integriert. Exakte rationale Momente und eine analytische
   Taylor-Restschranke ersetzen ein unkontrolliertes Gitter.
3. Nicht integrierte Feldphasen bei n≥3 und der Normrest jenseits n=6
   erhalten getrennte Schranken. Daraus folgen konservative Intervalle
   auch ohne obere Elementzahlgrenze, bei festem endlichem Uhrhorizont.

## 2. Referenzraum und Wirkung

Wir behalten das lokale L²-Produkt vollständiger Historien, den ausgewählten
monotonen Uhrsektor, den gemeinsamen Enduhrwert und die zusätzliche Gewichtung

    fα(n)=2^(−α n(n−1)/4),       α∈{1,2},       z=1.

Die Uhr s∈(0,h) ist kontinuierlich; mit dem ursprünglichen Anfangsanker
T_a=−2 gilt T=−2+4s. Das Dichtemaß ist

    ν(dw)=1/2 δ₀(dw)+1/2 1_(0,1)(w)dw.

Der Anfangsanker hat w_a=0. Er zählt nicht zur neuen Elementzahl n.
Die Wirkungsphase ist θ=gG+μSd, mit G=Sg−1. Die geerbten Referenzwirkungen
auf der verankerten Ordnung lauten

    Sg = |P_anchor| − Σ_(y≺x) B(k_yx),    B=(1,−9,16,−8),
    Sd = −(1/2)Σ_x w_x −(1/4)Σ_(y≺x) w_x B(k_yx)(T_x−T_y)².

B(k)=0 für k≥4. Alle Kopplungen dieses Pakets sind dimensionslose,
deklarierte Diagnosewerte. Die enumerierten Ordnungen sind nicht auf eine
physikalische vierdimensionale CST-Population eingeschränkt.

Π_n ist der Projektor auf die endgültige Elementzahl. Sei b der normierte
phasenfrei entwickelte leere Anfangsrecord, b_n=Π_n b/||Π_n b||.
Die Volumina und Präparationsmassen sind

    V_n=E_n h^n/n!,       c_n=fα(n)² V_n,       Z=Σ_n c_n,
    p_n=c_n/Z,           b_n(Y)=1/sqrt(V_n)   im n-Sektor.

E_n zählt natürliche Ordnungen. Bei festem n und h ist der positive
Faktor fα(n) vollständig aus b_n herausgekürzt. **Das Zahlkanal-Instrument
ist bei festem h unabhängig von α; α verändert die Präparationsgewichte
zwischen Elementzahlen.** Die Rang-eins-Auslese über alle Zahlen des
Vorgängers besitzt diese Unabhängigkeit nicht. Eine Änderung von h verändert
auch den Endraum und dessen Randbezug; sie ist keine bloße Änderung eines
Zwischenschnitts bei festgehaltenem Endpunkt.

## 3. Was ein Elementzähler messen kann

Der reine Zahlzähler hat Effekte Π_n. Mit D_θ als Multiplikation mit exp(iθ)
kommutieren diese Projektoren und allgemein alle lokalen diagonalen
Recordeffekte F(Y):

    <D_θ b,F D_θ b>=<b,F b>.

Ein solches Instrument ist blind gegenüber der Wirkungsphase. Dies gilt
unabhängig davon, ob die Diagonalwerte scharf oder unscharf sind. In einem
Zwei-Geometrien-Sektor haben die normierten Zustände (1,1)/sqrt(2) und
(1,−1)/sqrt(2) beide Zahlwahrscheinlichkeit eins. Der kohärente Filter auf
(1,1)/sqrt(2) hat dagegen Erfolg eins beziehungsweise null.

Ein detektierter Zahlwert allein implementiert daher nicht die kohärenten
Zahlkanäle. Zusätzlich ist ein Zugriff auf Superpositionen verschiedener
Geometrie-, Uhr- und Dichtehistorien innerhalb desselben n erforderlich.
Ob ein solcher Zugriff in einer physikalischen CST-Theorie verfügbar ist,
bleibt offen. Die Konstruktion behandelt ihn ausdrücklich als Modellannahme.

## 4. Explizites Hilfssystem statt stillschweigender Postselektion

Setze für jeden n-Sektor

    E_n=|b_n><b_n|,       F_n=Π_n−E_n.

Alle E_n und F_n sind orthogonale Projektoren und ihre starke Summe ist I.
Die Ergebnisse sind (n,Erfolg) und (n,Ausfall). Die Krausoperatoren werden
in dieser konkreten Realisierung ebenfalls als E_n beziehungsweise F_n
gewählt. Ein anderer Zustandsupdate mit denselben Effekten wäre ein anderes
Instrument; die Effekte allein bestimmen den Update nicht.

Nummeriere die nichtverschwindenden Projektoren als P_j. Ein Hilfssystem
mit Basis |k>, k∈Z, besitzt unitäre Verschiebungen S_j|k>=|k+j>.
Die kontrollierte Kopplung ist

    U=Σ_j P_j ⊗ S_j.

Dies ist ein direkter orthogonaler Summenoperator. Für jeden Vektor ist die
Normsumme der Komponenten endlich; die starke Summe existiert und

    U†U=UU†=Σ_j P_j⊗I=I.

Bei Hilfspräparation |0> und anschließender Zeigerauslese liefert
<j|U|0>=P_j die gewünschten Krausoperatoren. Für endlich viele Ausgänge
genügen zyklische Verschiebungen in einem endlichdimensionalen Hilfssystem.
Die dabei erhaltenen CP-Operationen sind linear, vollständig und können
beliebige Eingaben einschließlich dunkler Zustände behandeln.

Diese übliche Art einer unitären Messrealisierung ist in [1,2] erläutert.
Hier ist die konkrete Wahl der Projektoren vollständig angegeben und
die Unitarität direkt bewiesen. Die Existenz dieser abstrakten Kopplung
ist **keine** Herleitung eines physikalischen Wechselwirkungs-Hamiltonoperators,
einer kosmologischen Randamplitude oder eines verfügbaren Laborgeräts.

Die endliche Kontrolle verwendet vier Recordbasisvektoren mit Zahlsektoren
der Dimensionen 1,1,2. E_0 und E_1 sind die ersten beiden Basisprojektoren;
im letzten Block sind E_2=1/2[[1,1],[1,1]] und
F_2=1/2[[1,−1],[−1,1]]. Vier Zeigerzustände ergeben eine exakte rationale
16×16-unitäre Matrix. Geprüft werden beide Unitaritätsrichtungen,
16 Projektorprodukte, alle vier Krausoperatoren und Vollständigkeit.
Dieser Kontrollraum ist keine Quadratur eines kontinuierlichen Zahlsektors.

### Ignorierte Ergebnisse bedeuten nicht ungestörten Nachmesszustand

Die nichtselektive Zustandsabbildung ist

    Φ(ρ)=Σ_n (E_n ρ E_n + F_n ρ F_n).

Sie erhält die Elementzahlverteilung, weil die Krausoperatoren die
Zahlsektoren nicht mischen. Sie muss jedoch weder den Zustand noch die
Geometrie-Recordverteilung innerhalb eines Sektors erhalten.
Ein scharfer erster Geometrierecord (1,0) im Zwei-Geometrien-Block wird
nach ignoriertem Filterausgang zu 1/2 I, also zur Diagonale (1/2,1/2).

Die Identität des Vorgängers D_E(A,B)+D_(I−E)(A,B)=<P_Aψ,P_Bψ> betrifft
die Summe der Funktionale für vor der Endauslese definierte Historienfragen.
Sie besagt nicht, dass der nichtselektive Nachmesskanal die Identität ist.
Vorherige Historienereignisse, terminale Zahl-Ausgänge und spätere
Geometriemessungen müssen auseinandergehalten werden. Auch eine konkrete
Zeigerrealisierung garantiert keine Dekohärenz jeder früheren Ereignisalgebra.

Der bereits geprüfte Rücktransport E_a=K_*a† E K_*a bleibt für die Effekte
anwendbar, mit demselben Enduhrwert und ohne Renormierung. Ein zurückgezogener
Effekt legt wiederum nicht allein das vollständige frühere Messinstrument fest.

## 5. Kontinuierliche Dichtemarken analytisch integrieren

Für feste Uhren ist Sd linear in den Dichtemarken:

    Sd=−Σ_j w_j a_j(T).

Die charakteristische Dichtefunktion lautet

    χ(t)=∫ exp(−itw)ν(dw)=1/2 + (1/2)(1−exp(−it))/(it),
    χ(0)=1.

Die scheinbare Singularität bei t=0 ist hebbar. Für feste Uhren ist der
Materiephasenmittelwert daher das Produkt ∏_j χ(μ a_j). Das diskrete Atom
bei w=0 trägt wesentlich bei. Lässt man es weg, erhält man χ(0)=1/2;
ersetzt man das gesamte Maß durch eine normierte uniforme Verteilung,
ändert sich bereits <w> von 1/4 auf 1/2.

Für die tatsächlichen Zertifikate werden keine instabilen Quotienten oder
Gleitkommaquadraturen verwendet. Die exakten Dichtemomente sind

    d_0=1,       d_k=1/[2(k+1)] für k≥1.

Sie werden mit den exakt integrierten Uhrpolynomen kombiniert.

## 6. Die vollständigen kontinuierlichen Sektoren n≤2

Schreibe s=h x. Für ein Element ist 0<x<1 und

    a_1(x)=1/2+4h²x²,       Sd=−w_1 a_1,       G=0.

Für zwei Elemente ist 0<x_1<x_2<1. Die normierte Uhrdichte auf diesem
Dreieck ist 2. Es gibt eine Antikette und eine Kette, beide mit gleicher
bedingter Referenzmasse. Die Anfangsverankerung bleibt enthalten:

    a_1=1/2+4h²x_1²,
    a_2,anti=1/2+4h²x_2²,                           G_anti=0,
    a_2,chain=1/2+4h²x_1²−8h²x_1x_2−32h²x_2²,     G_chain=9,
    Sd=−w_1a_1−w_2a_2.

Die letzte Formel folgt auch aus
a_2,chain=1/2−36h²x_2²+4h²(x_2−x_1)².
Die Polynome stimmen an 390 rationalen Kontrollen einschließlich
Randwerten mit der geerbten vollständigen Wirkung überein. Randwerte
werden nur für die algebraische Kontrolle verwendet; die kontinuierliche
Integration besitzt weiterhin das offene geordnete Uhrgebiet.

Die benötigten Uhrintegrale sind elementar:

    ∫_0^1 x^a dx = 1/(a+1),
    2∫_(0<x_1<x_2<1) x_1^a x_2^b dx_1 dx_2
       = 2/[(a+1)(a+b+2)].

Für eine feste Zwei-Element-Geometrie ergeben sich die Momente

    M_k=<Sd^k>
       = (−1)^k Σ_(r=0)^k binom(k,r) d_r d_(k−r)
                         × <a_1^r a_2^(k−r)>_clock.

Für ein Element gilt entsprechend

    M_k=(−1)^k d_k Σ_(j=0)^k binom(k,j)(1/2)^(k−j)(4h²)^j/(2j+1).

Die Umsetzung multipliziert ganzzahlige Polynome nach gemeinsamer
Nennerfreistellung. Das vollständige Resultat bleibt rational. Ein zweiter
Rechenweg expandiert für k=0,1,2,3 die volle Vier-Variablen-Wirkung und
integriert die vier Atom-/Uniform-Kombinationen ausdrücklich. Er bestätigt
16 Zwei-Geometrien-Momente unabhängig von der Faktorisierungsroutine.

Ausgewählte exakte Kontrollen:

| h | Geometrie | <Sd> | <Sd²> |
|---|---|---|---|
| 1/4 | ein Element | −7/48 | 83/1440 |
| 1/4 | Antikette | −7/24 | 101/640 |
| 1/4 | Kette | 1/96 | 499/3840 |
| 1/2 | ein Element | −5/24 | 47/360 |
| 1/2 | Antikette | −5/12 | 167/480 |
| 1/2 | Kette | 19/24 | 129/40 |

## 7. Zertifizierter Integrationsfehler

Da die Phase reell ist, liefert die Taylor-Integralrestform für jedes reelle u

    |exp(iu)−Σ_(k=0)^K (iu)^k/k!| ≤ |u|^(K+1)/(K+1)!.

Es ist kein zusätzlicher Faktor exp(|u|) nötig. Die Schranke folgt aus
dem Betrag eins der Ableitungen von exp(iu) auf der reellen Integrationsstrecke.
Mit einer uniformen Schranke |Sd|≤M erhalten wir

    t_K=Σ_(k=0)^K (iμ)^k M_k/k!,
    |<exp(iμSd)>−t_K|≤ε=(|μ|M)^(K+1)/(K+1)!.

Aus 0≤w≤1, der geordneten Uhrdomäne und den obigen Polynomen folgen

    M_one=1/2+4h²,
    M_anti=1+8h²,
    M_chain=1/2+4h²+max(1/2,36h²−1/2).

Insbesondere ist M_chain=10 bei h=1/2. Mit K=48, h∈{1/4,1/2} und
μ∈{0,1/4,1} beträgt der größte Einzelamplitudenrest
10^49/49!≈1,6439747083·10^(−14), unter dem vorgegebenen Ziel 10^(−12).
Dies ist eine analytische Integrationsschranke, keine Differenz zweier Gitter.

Für den normierten Phasenmittelwert a gilt |a|≤1. Bei |a−t|≤ε folgt

    ||a|²−|t|²| ≤ 2ε+ε².

Der Sichtbarkeitswert v=|a|² wird deshalb durch
[max(0,|t|²−2ε−ε²), min(1,|t|²+2ε+ε²)] eingeschlossen.
Alle Zertifikate enthalten rationale Endpunkte; Dezimalzahlen im Bericht
dienen nur der Lesbarkeit und werden bei Intervallen nach außen gerundet.

Für n=2 lautet der vollständige Geometrie-/Feldmittelwert

    a_2(g,μ)=(a_anti(μ)+exp(i9g)a_chain(μ))/2.

Die geprüften g=0,π/18,π/9 geben die exakten Faktoren 1,i,−1. Für μ=0
werden die drei veröffentlichten Gravitationsfransen exakt wiedergewonnen.
Für h=1/2,g=π/9,μ=1 liegt dagegen

    v_2 ∈ [0,053484072766766, 0,053484072766800].

Die Materiephase hebt in diesem ausdrücklich gewählten Referenzfall den
vollständig destruktiven n=2-Ausgang bei μ=0 auf. Das ist keine allgemeine
Entstehung von Materie, keine gravitative Rückwirkung und kein Bounce.

## 8. Zahlgewichte und drei getrennte Fehlerquellen

Für n≤2 sind c_0=1,c_1=h,c_2=fα(2)²h² und Z_2=c_0+c_1+c_2.
Die endliche Zahlkanal-Erfolgswahrscheinlichkeit ist

    p_count,2 = Σ_(n≤2)c_n v_n/Z_2.

Für die kohärente Allzahl-Auslese wird zunächst die Amplitude
A_2=Σ_(n≤2)c_n a_n/Z_2 gebildet und danach |A_2|² genommen.
Die beiden Auslesen sind nicht auszutauschen.

Eine unbegrenzte Norm wird getrennt ausgewertet. Der Vorgänger beweist
E_n fα(n)²≤1 für α≥1. Die Normsumme bis n=6 kann ohne Feldphasen exakt
enumeriert werden. Ihr Rest erfüllt

    0≤Z_∞−Z_6≤δ_6=h^7/7! / (1−h/8).

Definiere Z_max=Z_6+δ_6 und

    R_max=Z_max−Z_2,       r_max=R_max/Z_max.

R_max erfasst sämtliche noch nicht integrierten n≥3-Feldphasen über ihre
maximal mögliche positive Referenzmasse. Es ist nicht dasselbe wie δ_6.
Sei S_L=Σ_(n≤2)c_n v_n,L und S_U=Σ_(n≤2)c_n v_n,U. Weil jeder noch
unbekannte Zahlkanal eine Sichtbarkeit zwischen null und eins hat, gilt

    S_L/Z_max ≤ p_count,∞ ≤ (S_U+R_max)/Z_max.

Die obere Formel benutzt, dass (S_U+R)/(Z_2+R) in R wächst, solange
S_U≤Z_2. Für die Allzahl-Amplitude gilt
|A_∞−A_2|≤2r_max. Zusammen mit dem endlichen Taylorfehler liefert dies
ebenfalls ein konservatives Wahrscheinlichkeitsintervall. Weil Z_max<2,
kann zusätzlich die Vakuumschranke p_all,∞≥(2/Z_max−1)² verwendet werden.

Die Unsicherheitsbilanz trennt damit:

| Anteil | Behandelt durch |
|---|---|
| Kontinuierliche Uhr-/Dichteintegration bei n≤2 | Exakte Momente und Taylorrest |
| Nicht integrierte Feldphasen bei n=3,4,5,6 | Exakte Normmassen, Sichtbarkeit in [0,1] |
| Alle n>6 | Analytischer Normrest δ_6, ebenfalls Sichtbarkeit in [0,1] |

Für die bedingten akzeptierten Zahlwerte 0,1,2 folgen sichere Grenzen

    c_n v_n,L/(S_U+R_max) ≤ Pr(n|Erfolg) ≤ min(1,c_n v_n,U/S_L).

Die gesamte bedingte Restwahrscheinlichkeit n≥3 ist höchstens
min(1,R_max/S_L). Dies sind getrennte marginale Intervalle, keine Behauptung,
dass ihre jeweiligen Endpunkte gleichzeitig erreicht werden.

Bei g=μ=0 ist die gesamte Konstruktion exakt phasenfrei; der Erfolg ist
auch ohne Zahlgrenze eins. Dieser analytische Sonderfall ersetzt dort die
sonst konservative Sichtbarkeitshülle für höhere Zahlen.

## 9. Was der Scan tatsächlich zeigt

Es werden 36 Kombinationen aus α=1,2, h=1/4,1/2, g=0,π/18,π/9 und
μ=0,1/4,1 berechnet. Für g=0,μ=1 sind folgende konservativ nach außen
gerundeten unbegrenzten Zahlkanal-Erfolgsintervalle erhalten:

| h | α | p_count,∞ | Noch nicht integrierte normierte n≥3-Masse, obere Grenze |
|---|---|---|---|
| 1/4 | 1 | [0,988415098758, 0,990271758873] | 0,001856660114 |
| 1/4 | 2 | [0,991311616231, 0,991537884398] | 0,000226268167 |
| 1/2 | 1 | [0,929417722608, 0,941547197461] | 0,012129474853 |
| 1/2 | 2 | [0,954632454516, 0,956106004346] | 0,001473549829 |

Der Erfolg ist in diesen Fällen nachweisbar kleiner als der phasenfreie
Wert eins, selbst wenn die nicht integrierten höheren Zahlkanäle ihre
maximal mögliche Sichtbarkeit hätten. Die beiden α-Intervalle sind bei
jedem der zwei h disjunkt. Das weist die Präparationsabhängigkeit nach;
es wählt keinen α-Wert physikalisch aus. Der Vergleich der h-Werte verändert
die festgelegte Enddauer und den Randbezug und prüft daher Modellabhängigkeit,
nicht die bereits bewiesene Zwischenschnittkompatibilität.

## 10. Reproduzierbarkeit und Negativkontrollen

Der Plan wurde lokal nach dem analytischen Entwurf und vor Implementierung
eingefroren. Dies ist keine externe Präregistrierung oder blinde Vorhersage.
`analyze.py` kontrolliert Plan-SHA und sechs gepinnte Quellen. Es erzeugt
sechs Ergebnisdateien. `replay.py` kopiert nur Quellen, Plan und Eingaben
in ein frisches Verzeichnis und fordert Bytegleichheit aller Ergebnisse.
Alle Analysen benötigen nur die Python-Standardbibliothek.

Negativkontrollen betreffen das ausgelassene Dichteatom, einen ersetzten
Dichteprior, den fehlenden Faktor zwei der geordneten Uhrnorm, die
Verwechslung von Zählen und kohärentem Filtern, die nichtlineare
Renormierung eines selektierten Erfolgs und die falsche Gleichsetzung
eines ignorierten Messausgangs mit einem ungestörten Nachmesszustand.

Die exakten Zahlen sind Implementierungsnachweise derselben Rechenroutine,
keine unabhängige wissenschaftliche Replikation und kein formaler
Beweisassistent. Es gibt keine neuen physikalischen 4D-Ensembles,
keine Hardwaresteuerung und keine bezahlten Läufe.

## 11. Status und nächste wissenschaftliche Grenze

Die Referenz-Auslese ist nun als vollständiges Hilfssystem-Messmodell
ausgeschrieben. Zugleich ist bewiesen, dass die benötigte kohärente
Filteroperation eine zusätzliche Annahme gegenüber einer reinen Zahlmessung
ist. Die kontinuierliche Materiephase ist für n≤2 kontrolliert integriert;
höhere Zahlsektoren sind nur über positive Normmassen eingeschlossen.

Der nächste quantitative Ausbau ist n≥3: Dort dominiert gegenwärtig die
fehlende Feldphasenintegration das Gesamtintervall, nicht der Taylorrest.
Der physikalische Entscheidungspunkt bleibt die Begründung, warum dieses
Instrument, dieser Dichteprior und diese Endrandwahl verfügbar oder dynamisch
ausgezeichnet sein sollten. Eine abstrakte Messdilatation beantwortet dies nicht.

MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD. Keine kosmologische finale Randbedingung, keine
physikalische vierdimensionale Quantendynamik, kein Junction law und kein
Bounce wurden aus der vollständigen CST-Amplitude hergeleitet.

## Primärquellen

[1] John Preskill, *Lecture Notes for Ph219/CS219: Quantum Information*,
Chapter 3: Foundations II, Measurement and Evolution, Fassung Oktober 2018,
https://www.preskill.caltech.edu/ph219/chap3_15.pdf . Kontext für Zeigerkopplung,
Krausoperatoren und verallgemeinerte Messungen; kein CST-Auswahlprinzip.

[2] Matteo G. A. Paris, *The modern tools of quantum mechanics (A tutorial on
quantum states, measurements, and operations)*, Eur. Phys. J. ST 203, 61 (2012),
https://arxiv.org/abs/1110.6815v2 . Kontext für unitäre Dilatation und
vollständig positive Operationen. Die konkrete Kopplung und die
Integrationsschranken werden hier explizit hergeleitet.

Quellen am 7. November 2026 geprüft. Externe Volltexte werden nicht verteilt.
