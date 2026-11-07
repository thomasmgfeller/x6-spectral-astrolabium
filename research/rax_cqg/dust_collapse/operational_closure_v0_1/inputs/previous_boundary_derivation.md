# CST-DUST: Kohärente Randauslese und Dekohärenz v0.1

Stand: 7. November 2026. Basis: Main nach PR 253, Commit
`36afc462dc5a9503616e9b016481e3b441b7c123`.
Sechs unveränderte Eingaben sind in `inputs/provenance.json` mit Git-Blob-SHA
und Originalpfad gepinnt. Die Aussagen sind konditional auf die nachstehenden
Referenzentscheidungen. **Alle acht physikalischen Gates bleiben HOLD.**

## 1. Was hinzukommt und was übernommen wird

Der Vorgänger konstruiert einen beschränkten, bei gemeinsamem Enduhrwert
isometrischen Transport vollständiger Historien. In seinem lokalen
Historienprodukt sind scharfe Records orthogonal; ihre Normwahrscheinlichkeiten
sind blind gegenüber reellen Wirkungsphasen. Hier werden zwei feste kohärente
Endauslesen hinzugefügt, ihre Rücktransporte bewiesen und die zugehörigen
Dekohärenzfunktionale untersucht. Dies ist die Wahl eines prüfbaren Instruments,
keine Herleitung einer physikalisch ausgezeichneten kosmologischen Randbedingung.

Wir behalten den ausgewählten monotonen Materieuhrsektor, die vollständige
Vergangenheit, das lokale Referenzprodukt und einen gemeinsamen Enduhrwert t*.
Mit s=(T+L)/(2L), L=2, ist das kontinuierliche Uhrmaß ds. Das Dichtemaß ist
ν(dw)=1/2 δ₀(dw)+1/2 1_(0,1)(w)dw, mit Gesamtmasse eins.
Ein Record Y=(P,s,w) hat n Elemente, strikt geordnete Uhren und eine hierzu
verträgliche partielle Ordnung P. Die Anfangsverankerung T_a=−2,w_a=0 ist Teil
der Wirkung, aber kein gezähltes neues Element. Ein neuer Endanker wird an
Zwischenschnitten nicht eingefügt. Die Raumzeitdimension dieser enumerierten
Ordnungen ist nicht auf vier beschränkt.

Die geerbte reelle Referenzwirkung lautet auf dem verankerten Record:

    Sg = |P_anchor| − Σ_(y≺x) B(k_yx),        B=(1,−9,16,−8),
    Sd = −(1/2)Σ_x w_x − (1/4)Σ_(y≺x) w_x B(k_yx)(T_x−T_y)².

B(k)=0 für k≥4. Die leere neue Geschichte hat Sg=1,Sd=0. Wir schreiben
θ(Y)=g[Sg(Y)−1]+μ Sd(Y). g und μ sind deklarierte dimensionslose
Diagnosekopplungen; keine physikalischen Werte werden ausgewählt.

Für q=|z|² und fα(n)=2^(−αn(n−1)/4), α≥1, hat der lokale offene Transport

    (U_ba ψ)(Y) = z^(n−m) fα(n)/fα(m)
                  × exp(i[θ(Y)−θ(Y_a)]) ψ(Y_a).

Die eindeutigen Präfixe Y_a, teleskopische Gewichte und Wirkungsdifferenzen
geben U_cb U_ba=U_ca. Die Zustandsumme Z(P,h) ist die lokale quadrierte
Fortsetzungsnorm; der Vorgänger beweist 1≤Z≤exp(qh). Bei einem endlichen
Regulator N gilt an jedem Schnitt dieselbe Gesamtzahlgrenze. Für den gemeinsamen
Enduhrwert ist

    K_ba = sqrt[Z(P_Y,t*−b)/Z(P_Ya,t*−a)] U_ba.

Diese K sind Isometrien und erfüllen K_cb K_ba=K_ca. Es sind keine behaupteten
surjektiven Unitaritäten. Alle nachfolgenden Rücktransporte benutzen denselben
Enduhrwert, dieselbe Zahlgewichtung und dieselbe Regulatorwahl.

## 2. Eine beschränkte feste Endauslese

Sei H_* die direkte lokale L²-Summe aller Endrecords. Bei z=1 und Uhrdauer h
ist der phasenfreie Endzustand aus dem leeren Anfangsrecord

    b(Y) = fα(n)/sqrt(Z),          ||b||=1,
    ψθ(Y) = exp(iθ(Y)) b(Y),      ||ψθ||=1,
    p₀(dY) = |b(Y)|² dμ(Y).

Hier umfasst dμ die Summe über Ordnungen und die geordneten Uhr-/Dichtemaße.
Auch bei unbegrenzter Elementzahl existiert b wegen der genannten Z-Schranke.
b wird festgehalten, während g und μ variiert werden. Eine nachträgliche
Anpassung von b an ψθ wäre ein anderes Instrument.

Das Rang-eins-Effektpaar lautet

    E_all=|b><b|,       E_fail=I−E_all,       0≤E_all≤I.

Der lineare Instrumentoperator ψ↦<b,ψ> hat als Komplement
sqrt(I−E_all)ψ. Weil E_all eine Projektion ist, genügt I−E_all als
Komplement-Krausoperator. Die tatsächliche Erfolgswahrscheinlichkeit ist

    p_all = |<b,ψθ>|² = |∫ exp(iθ(Y)) p₀(dY)|² ∈ [0,1].

Das Instrument ist zustandsunabhängig definiert. Nur eine ausdrücklich
bedingte Auswertung nach einem beobachteten Erfolg darf durch dessen
Wahrscheinlichkeit dividieren, und nur wenn sie positiv ist.

### Warum eine flache Endzeile nicht genügt

Die formale Zeile ℓ(ψ)=Σ_P∫ψ(P,s,w)dμ entspricht dem konstanten Vektor 1.
Seine Dualnorm auf der gesamten lokalen H_* ist

    ||1||² = Σ_n E_n h^n/n!.

E_n≥2^floor(n²/4) folgt aus frei wählbaren Relationen zwischen zwei Schichten.
Für jedes h>0 gehen diese positiven Summanden nicht gegen null. Somit ist ℓ
auf H_* unbeschränkt. Zahlgewichte im getesteten Eingabevektor machen eine
solche Zeile nicht zu einem beschränkten Effekt auf allen Zuständen. Bei
endlichem N kann sie normiert werden; das liefert keine unveränderte
unbeschränkte Grenzauslese. Dies ist ein Ausschluss dieses Kandidaten,
kein allgemeines No-go für CST oder für andere Skalarprodukte.

## 3. Rücktransport ohne nachträgliche Normierung

Für einen früheren Schnitt a setzen wir

    b_a=K_*a† b,        E_a=K_*a† E_all K_*a=|b_a><b_a|.

Da K_*a isometrisch ist, ist sein Adjungierter kontraktiv; ||b_a||≤1 und
0≤E_a≤I. Aus K_*a=K_*b K_ba folgt unmittelbar

    b_a=K_ba† b_b,      E_a=K_ba† E_b K_ba.

Komplement und Erfolg bleiben vollständig, denn K_*a† I K_*a=I.
Der zurücktransportierte Vektor ist im Allgemeinen nicht normiert. Auf dem
eindimensionalen leeren Anfangssektor ist ||b_0||²=p_all. Ihn auf Norm eins
zu setzen würde bei 0<p_all<1 dieselbe Anfangspräparation mit Erfolgswert eins
versehen. Das verändert das Instrument und zerstört die behauptete
Schnittübereinstimmung.

Wählt man stattdessen am Endschnitt b_θ=exp(iθ)b, erhält man <b_θ,ψθ>=1.
Diese kophasiert mitbewegte Randwahl entfernt jede hier beobachtete Interferenz.
Die Wahl eines festen Randbezugs ist daher eine wesentliche Zusatzannahme,
keine aus der Wirkung allein folgende Vorhersage.

## 4. Dekohärenzfunktional und seine begrenzte Wahrscheinlichkeitsdeutung

Für messbare Historienereignisse A ist P_A der lokale Multiplikationsprojektor.
Das Skalarprodukt ist im ersten Argument antilinear. Für ein beliebiges
festes 0≤E≤I definieren wir

    D_E(A,B)=<P_A ψ, E P_B ψ>.

Hermitizität ist direkt. Für jede endliche Ereignisfamilie und komplexe z_i gilt

    Σ_ij conjugate(z_i) D_E(A_i,A_j) z_j
        = ||sqrt(E) Σ_i z_i P_Ai ψ||² ≥ 0.

Damit ist D stark positiv. Additivität in jedem Slot folgt für disjunkte
Ereignisse aus P_(A∪B)=P_A+P_B. Die Diagonale μ_E(A)=D_E(A,A) erfüllt für
paarweise disjunkte A,B,C die Grad-zwei-Regel

    μ_E(A∪B∪C)=μ_E(A∪B)+μ_E(A∪C)+μ_E(B∪C)
                −μ_E(A)−μ_E(B)−μ_E(C).

Für den festen endlichen Uhrhorizont gilt auch die übliche Grenzkontinuität
unter disjunkten Vereinigungen, weil die Vektorsumme P_Aψ in L² konvergiert
und sqrt(E) beschränkt ist. Das löst kein Erweiterungsproblem auf einen
unendlichen Zeithorizont oder auf einen anderen CST-Historienraum.

Der Gesamtwert D_E(Ω,Ω)=p_E ist die Instrument-Erfolgswahrscheinlichkeit.
Bei p_E>0 kann man D_E/p_E normieren. Daraus wird im Allgemeinen kein
additives Maß über exklusive Historien. Bei einer Partition {A_i} bedeutet
exakte mittlere Dekohärenz D_E(A_i,A_j)=0 für i≠j; dann liefern die
normalisierten Diagonalen eine konsistente klassische Verteilung. Ohne diese
Bedingung oder einen zusätzlich angegebenen Messkontext ist die Bezeichnung
Historienwahrscheinlichkeit nicht gerechtfertigt.

Der unbeobachtete Ausleseausgang erfüllt hingegen exakt

    D_E(A,B)+D_(I−E)(A,B)=<P_Aψ,P_Bψ>.

Für disjunkte A,B verschwindet dies. Die ursprüngliche phasenblinde
Recordverteilung wird wiedergewonnen. Eine bewusste Zwischenmessung eines
Records verändert im Allgemeinen den Kontext und kann die Interferenz
vernichten; ihre bedingten Wahrscheinlichkeiten sind nicht stillschweigend
mit D_E(A,A)/D_E(Ω,Ω) gleichzusetzen.

### Derselbe vergangene Zylinder an verschiedenen Schnitten

Ein Ereignis A werde durch einen festen Schnitt r bestimmt. Für a≥r trägt
jedes Präfix am Schnitt a weiterhin dasselbe Ereignis A(Y_r). Dann gilt

    P_A^* K_*a = K_*a P_A^a,
    <P_A^a ψ_a,E_a P_B^a ψ_a>=D_E(A,B).

Dies beweist Schnittunabhängigkeit für diese feste Ereignisfrage.
Die Zahl am jeweils aktuellen Schnitt ist eine andere Frage; sie darf nicht
als dasselbe vergangene Ereignis ausgegeben werden. Eine erst am Endschnitt
definierte Zahlfrage wird bei früherer Auswertung vollständig zurückgezogen,
nicht durch die frühere momentane Elementzahl ersetzt.

## 5. Ein Ranghindernis und konkrete Negativkontrollen

Bei reinem Anfangszustand und einem Effekt von endlichem Rang r ist die
Atommatrix D_ij eine Gram-Matrix von Vektoren sqrt(E)P_iψ in einem
höchstens r-dimensionalen Raum. Daher rank(D)≤r. Exakte mittlere Dekohärenz
mit k strikt positiven Atomen ergibt eine Diagonalmatrix vom Rang k. Also
ist k≤r notwendig. Für den Rang-eins-Effekt E_all kann höchstens ein Atom
einer exakt mittel-dekohärenten Partition positiv sein. Die Aussage betrifft
diese Reinheit, diesen Rang und exakte mittlere Dekohärenz; sie schließt
gemischte Zustände, höhere Ränge oder andere Dekohärenzkriterien nicht aus.

In einem normierten Zwei-Geometrien-Unterraum seien die relative Wirkungsphase
π, ψ=(2,−1)/sqrt(5) und b=(1,1)/sqrt(2). Dann

    D_+ = (1/10) [[4,−2],[−2,1]],     D_+(Ω,Ω)=1/10,
    D_− = (1/10) [[4, 2],[ 2,1]],     D_−(Ω,Ω)=9/10.

Beide Matrizen sind positiv semidefinit. Die erste normierte Atomdiagonale
ist aber 4. Das ist ein expliziter Gegenbeleg gegen ihre Deutung als
gewöhnliche bedingte Historienwahrscheinlichkeit. Bei nicht ausgelesenem
Ergebnis bleiben die Recordwahrscheinlichkeiten 4/5 und 1/5.
Für ψ=(1,−1)/sqrt(2) ist D_+=1/4[[1,−1],[−1,1]] mit Gesamtwert null:
keine Normalisierung ist erlaubt. Der überskalierte Effekt 2|b><b| liefert
auf ψ=b den Wert 2; sein Komplement besteht die Positivitätsprüfung nicht.

## 6. Elementzahlkanäle mit Interferenz innerhalb jeder Zahl

Π_n projiziert auf die endgültige Elementzahl n. Für p_n=||Π_n b||²>0 sei

    b_n=Π_n b/sqrt(p_n),       E_n=|b_n><b_n|,
    E_count=Σ_n E_n.

Die b_n sind orthonormal. Die starke Summe ist eine beschränkte orthogonale
Projektion, 0≤E_count≤I. Rψ=(<b_n,ψ>)_n ist eine Kontraktion nach ℓ²;
zusammen mit sqrt(I−E_count) bildet sie ein vollständiges Instrument.
Die getrennten n-Ausgänge sind normale Messausgänge. Bei Gruppierung aller
Erfolge ist D_count(Π_n,Π_m)=δ_nm |<b_n,ψ>|² exakt diagonal. Bedingt auf
Erfolg und bei positivem Gesamterfolg gilt deshalb

    Pr(n | Erfolg)=|<b_n,ψ>|² / Σ_m |<b_m,ψ>|².

Verschiedene Geometrien und Felder innerhalb desselben n interferieren weiter.
Da b=Σ_n sqrt(p_n)b_n im Bild von E_count liegt, gilt E_all≤E_count und
p_all≤p_count. Die Rücktransporte E_count,a=K_*a† E_count K_*a sind wieder
positive Kontraktionen und komponieren. Zurücktransportierte Kanäle sind
im Allgemeinen nicht mehr orthonormal; ihre Normierung darf nicht verändert
werden. Für andere, etwa frühere, Ereignispartitionen ist keine Dekohärenz
garantiert. In sämtlichen zwölf geprüften atomaren Kopplungsfällen ist die
vergangene Drei-Atom-Partition tatsächlich nicht mittel-dekohärent.

Die unendliche Projektion E_count muss nicht spurenklassig sein. Ein zulässiger
POVM-Effekt ist nicht automatisch eine normalisierte kosmologische finale
Dichtematrix. Die physikalische Auswahl dieses Instruments bleibt offen.

## 7. Kontinuierlicher Gravitationstest und exakte Interferenz

Hier wird μ=0 gesetzt. Dann hängt θ=gG(P), G=Sg−1, nur von der Ordnung ab;
Uhr und Dichte lassen sich exakt integrieren. Das ist keine Diskretisierung
der kontinuierlichen Materiephase. Für E_n Ordnungen und die Zahlgrenze N:

    c_n = E_n fα(n)² h^n/n!,        Z_N=Σ_(n≤N)c_n,
    W_n = fα(n)² h^n/n! Σ_(P:n) exp(igG(P)),
    A_N = Σ W_n/Z_N,
    p_all,N=|A_N|²,
    p_count,N=Σ |W_n|²/(c_n Z_N).

Unabhängige obere-Dreiecks-Enumeration mit Transitivitätsfilter ergibt für
n=0,...,6 die natürlichen Ordnungszahlen 1,1,2,7,40,357,4824.
Für g=kπ/2, k=0,1,2,3, sind die Phasen i^(kG) gaußsch rational.
Alle Resultate sind als exakte rationale Zahlen gespeichert.

Der einfache Test N=2,α=1,h=1/2,q=1 hat vor Auslese p_n=(8,4,1)/13.
Die beiden n=2-Geometrien besitzen G=0 (Antikette) und G=9 (Kette).
Ihre kohärente Erfolgsfraktion ist v(g)=(1+cos(9g))/2. Somit:

| g | v(g) | Gesamterfolg der Zahlkanäle | Pr(n=0,1,2 \| Erfolg) |
|---|---|---|---|
| 0 | 1 | 1 | (8,4,1)/13 |
| π/18 | 1/2 | 25/26 | (16,8,1)/25 |
| π/9 | 0 | 12/13 | (2/3,1/3,0) |

Der Ausfallkanal ergänzt die fehlende n=2-Masse. Ohne Selektion des
Ausleseergebnisses bleibt (8,4,1)/13 unverändert. Die Phasen wirken also in
diesem gewählten kohärenten Instrument, ohne daraus eine gravitative
Rückwirkung, Staubbewegung oder einen Bounce abzuleiten.

### Kontrollierter Rest über weitere Elementzahlen

Für α≥1 ist E_n fα(n)²≤1. Bei x=qh=1/2,N=6 erhält man

    R=Z_∞−Z_N ≤ δ = x^7/7! / (1−x/8) = 1/604800.

Setze t=δ/(Z_N+δ). Die tatsächliche normierte Restmasse r=R/(Z_N+R)
ist höchstens t. Da jede Phasenmittelamplitude Betrag ≤1 hat, gilt

    |A_∞−A_N|≤2t,         |p_all,∞−p_all,N|≤4t.

Für Zahlkanäle ist der neue Anteil eine Mischung von Sichtbarkeiten in [0,1]:

    (1−t)p_count,N ≤ p_count,∞ ≤ (1−t)p_count,N+t.

Die Grenzen sind in `tail_bounds.json` exakt rational abgelegt. Der Rest
kontrolliert zusätzliche Elementzahlen, keine Uhr-/Dichtequadratur.
Außerdem gilt für beide geprüften α: Z_N+δ<2. Der leere Record hat Phase null
und Gewicht 1/Z_∞. Für beliebige reelle g und μ, nicht nur die enumerierten
Werte, liefern Dreiecksungleichung und der leere Zahlkanal

    p_all,∞ ≥ [2/(Z_N+δ)−1]² > 0,
    p_count,∞ ≥ 1/(Z_N+δ) > 0.

Dies verhindert einen Nullnenner für diese kurze, vakuumdominierte
Referenzpräparation. Andere Präparationen können vollständig dunkel sein,
wie die Zwei-Geometrien-Kontrolle zeigt. Die Schranke ist kein universelles
Singularitäts- oder Nichtauslöschungsgesetz.

## 8. Vollständige Wirkungsphasen auf einem gesonderten atomaren Maß

Die algebraischen Kontrollen mit μ≠0 verwenden ausdrücklich ein anderes
Wahrscheinlichkeitsmaß: vier Uhratome T∈{−1,−1/2,0,1/2} mit Masse 1/4,
zwei Dichteatome w∈{0,1/2} mit Masse 1/2, strikt verschiedene geordnete
Uhren und höchstens vier Elemente. Dies ist keine zertifizierte Quadratur
des kontinuierlichen Maßes. Es gibt insgesamt

    Σ_(n=0)^4 E_n binom(4,n) 2^n = 921

Endrecords. Jeder trägt unnormiertes Gewicht fα(n)²(1/8)^n.
An allen Records stimmen vollständige Wirkung und unabhängige
Inkrementrechnung exakt überein. Die Diagnosephasen sind

    exp{iπ/2 [kg(Sg−1)+kd·32 Sd]},
    (kg,kd)=(0,0),(1,0),(0,1),(1,1),(2,1),(1,2).

32 Sd ist auf diesem Gitter ganzzahlig. Entsprechend g=kgπ/2,μ=16π kd
sind die Rechnungen exakt mit rationalen Real-/Imaginärteilen möglich.
Die zwei α ergeben zwölf Kontrollen, keine Parameteranpassung.

Für jeden Präfix x seien p_x seine terminale Referenzmarginale und
W_xn=Σ_(Y:Y_a=x,|Y|=n) p₀(Y) exp(iθ(Y)). Nach Übergang in die zur
p_x-gewichteten Basis äquivalente Darstellung ist der rückgezogene
Kanalvektor bis auf den Faktor 1/sqrt(p_n)

    B_n(x)=exp(iθ(x)) conjugate(W_xn)/p_x.

Das Zwischenstück von x nach z multipliziert in dieser Darstellung mit
exp(i[θ(z)−θ(x)]); sein Adjungierter verwendet die bedingten Gewichte p_z/p_x.
Damit wird K_ba† B_n,b=B_n,a ohne numerische Quadratwurzel nachgerechnet.
Für die Kanalkontraktion ist

    H_nm=Σ_x W_xn conjugate(W_xm)/p_x

die skalierte Kanal-Gram-Matrix. Positivität von diag(p_n)−H ist durch
Diagonalkongruenz äquivalent zu I−Gram(b_n,a)≥0. Sie wird durch exakte
Hermitesche Schur-Elimination geprüft; bei einem Nullpivot muss die
verbleibende Zeile null sein. Dieselbe Prüfung kontrolliert alle
Erfolgs-/Komplement-Atommatrixen.

Schnitte T=−3/2,−3/4,−1/4,1/4,3/4 ergeben 1,3,13,87,921 Präfixrecords.
Das feste vergangene Ereignis ist die Elementzahl 0,1,2 am Schnitt −1/4;
es wird an diesem und beiden späteren Schnitten verglichen.
Resultate: 6.240 exakte Kanal-Komponenten-Rücktransportgleichheiten,
72 Übereinstimmungen der vergangenen Funktionale, positive Kontraktionen,
vollständiges Erfolgs-/Komplementpaar, Hermitizität, starke Positivität,
Additivität, Grad-zwei-Regel und exakt diagonale terminale Zahlkanäle.
Die vergangene Partition dekohäriert dagegen in keinem der zwölf Fälle,
bei keiner der beiden Auslesen. Ein terminaler Zähler ist keine allgemeine
Dekohärenz aller Historienfragen.

## 9. Wiederholbarkeit, offene Physik und nächster Entscheidungspunkt

Der Plan wurde lokal nach dem analytischen Entwurf und vor der neuen
Enumeration eingefroren; keine blinde Vorhersage oder externe Präregistrierung.
`analyze.py` kontrolliert Plan-SHA und die sechs Quellen, erzeugt sechs
Ergebnisdateien. `replay.py` kopiert nur Quellcode, Plan und Eingaben in ein
frisches Verzeichnis und verlangt Bytegleichheit aller sechs Ergebnisse.
Dies ist Wiederholbarkeit derselben Implementierung, keine unabhängige
wissenschaftliche Replikation oder formale Beweiszertifizierung.
Analyse und Replay benötigen nur die Python-Standardbibliothek.

MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD. Insbesondere bleibt BOUNDARY HOLD: ein wohldefinierter
Referenzeffekt ersetzt weder eine abgeleitete finale Randbedingung noch das
physikalische Innen-/Außenraum-Junction law.

Der nächste wissenschaftliche Entscheidungspunkt ist die Auswahl eines
operational oder dynamisch begründeten Randinstruments und einer dazu passenden
Ereignisalgebra. Danach sind kontinuierliche Materiephasen mit kontrollierten
Integrationsfehlern und Robustheit gegen Zahlgewichte/Enduhrwert zu prüfen.
Eine interne Wahl kann als neue Modellannahme untersucht, aber nicht als aus
der vierdimensionalen CST-Summe hergeleitet etikettiert werden. Kein weiterer
formaler Normierungsschritt allein schließt die physikalischen Gates.

## 10. Primärquellen und Zuordnung

1. M. Gell-Mann, J. B. Hartle, *Time Symmetry and Asymmetry in Quantum Mechanics
   and Quantum Cosmology*, arXiv:gr-qc/9304023v2,
   https://arxiv.org/abs/gr-qc/9304023v2 . Kontext für Anfangs-/Endrandbedingungen
   und die Unterscheidung von Dekohärenzfunktionalen und Historienwahrscheinlichkeiten.
   Der hier verwendete Rangbeweis ist oben vollständig ausgeführt; die Quelle
   begründet keine physikalische Auswahl unserer b_n.
2. F. Dowker, S. Johnston, S. Surya, *On extending the Quantum Measure*,
   arXiv:1007.2725v1, https://arxiv.org/abs/1007.2725v1 . Kontext für
   Erweiterungsprobleme quantaler Maße. Unsere feste endliche Uhrdauer und
   beschränkten L²-Effekte sind keine Lösung eines unendlichen
   CST-Zeit-/Ereigniserweiterungsproblems.

Quellen am 7. November 2026 geprüft. Externe Volltexte werden nicht verteilt.
