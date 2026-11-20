# CST-DUST: Staubstrom und Messgrößen v0.1

**Datum:** 6. November 2026. **Kennung:** CST-DUST-CURRENT-CAL-001.
**Elternvertrag:** CST-DUST-MC-001 v0.1, GitHub PR #239, Main-Commit
`0e47038f15d93edef486fbb68da5dad6bf017221`.

## Ergebnis und Status

Definiert wird ein konservativer, mit Materiemarken versehener Fluss auf einem
endlichen Kausalset. Kalibriert werden Schnittmasse, seitlicher Massenfluss,
räumliches Volumen und gemittelte Dichte an der festgelegten endlichen klassischen
Staubball-Referenz. Die Kalibrierung umfasst die Materieoberfläche und einen
Detektor, der in den Vakuumaußenraum reicht. Sie ist eine bedingte Referenzprüfung,
keine Ableitung eines physikalischen Staubstroms aus einer CST-Historiensumme.

Die Zähldichten 4λ₀ und 8λ₀ erfüllen das vorab festgelegte Referenzziel: mit
konservativ mindestens 98,1203 % beziehungsweise 99,9999723 % Wahrscheinlichkeit
liegen alle 315 Volumen- und Dichteintervalle einer Stufe vollständig innerhalb
von ±5 % ihrer jeweiligen Referenzwerte. Das setzt exakt bekannte Zähldichte,
Zeitfensterkorrektur und Detektorgeometrie voraus. Es wurden keine Zufallsstichproben
oder neuen dynamischen CST-Ensembles erzeugt. Die Wahrscheinlichkeiten sind
Gleitkommaauswertungen analytischer Poissonformeln, keine Intervallzertifikate.

## 1. Kontinuumsbezug und Einheiten

Für drucklosen, einströmigen Staub mit Signatur (−,+,+,+) gilt

\[
J^a=\rho u^a,\qquad u^au_a=-1,\qquad
T^{ab}=\rho u^au^b,\qquad \nabla_aJ^a=0.
\]

ρ ist die Ruhemassendichte. Eine raumartige Fläche Σ mit zukunftsgerichteter
Einheitsnormaler n misst \(Q_\Sigma=-\int_\Sigma J^an_a\,d\Sigma\).
Nur für n=u ist dies unmittelbar das Integral der Ruhemassendichte.
Unser Referenzschnitt erfüllt diese Bedingung im Inneren. Flüsse durch zeitartige
Detektorflächen erhalten eine positive Orientierung nach außen.

Bei c=1 sind die Einheiten: Zeit und Länge L; Masse M; J und ρ M/L³;
integrierter Fluss und Schnittmasse M; Flussrate M/L; V₃ L³; Ω₄ L⁴;
Sprinklingdichte λ L⁻⁴; Kalibrierfaktor A L; Kretschmannskalar K L⁻⁴.
G=1 bezeichnet geometrisierte Referenzeinheiten. Keine SI- oder Planckskalierung
wird hier gemessen. λ ist ausdrücklich nicht die Materiedichte ρ.

## 2. Diskreter markierter Strom

Sei C eine endliche kausale Ordnung, E eine deklarierte Menge vorwärtsgerichteter
Transportkanten mit x≺y. Zusätzlich zur Ordnung werden Materiemarken
\(f_{xy}\geq0\) in Masseneinheiten und deklarierte Quellen sₓ angegeben:

\[
d_x:=\sum_{y:(x,y)\in E}f_{xy}-\sum_{y:(y,x)\in E}f_{yx}=s_x.
\]

Im Bulk ist sₓ=0; an zeitlichen Ein- und Austrittsflächen liegen die entsprechenden
positiven und negativen Quellen. f ist eine integrierte transportierte Masse,
kein Gewicht, das blind jeder Kausalrelation zugeordnet wird. Die transitive
Ergänzung der Ordnung erzeugt keine weitere Materie. Ein DAG von
Ordnungs-Generatoren wird in `current.py` über seine erzeugte partielle Ordnung
verstanden. Die Transportkanten und ihre Marken bleiben gesondert.

Für jede Testfunktion φ und jede Ereignismenge W gilt durch Umordnen endlicher
Summen exakt:

\[
\sum_{(x,y)\in E} f_{xy}(\phi_y-\phi_x)=-\sum_x\phi_xd_x,
\qquad
\sum_{x\in W}d_x=\Phi_{\rm out}(W)-\Phi_{\rm in}(W).
\]

Jede innere Kante trägt einmal +f und einmal −f bei. Das beweist die diskrete
Gaussidentität ohne Einbettung. Für eine Vergangenheitsmenge P gibt es keine
eingehenden Ordnungskanten; daher ist die Schnittmasse
\(Q(P)=\sum_{x\in P,y\notin P}f_{xy}=\sum_{x\in P}s_x\).
Für P₁⊂P₂ ohne Quellen in P₂\P₁ sind beide Schnittmassen gleich.

**Coarse graining:** Eine vollständige Blockpartition muss nach Quotientierung
azyklisch bleiben. Setze \(F_{AB}=\sum_{x\in A,y\in B}f_{xy}\) für A≠B und
\(S_A=\sum_{x\in A}s_x\). Innere Flüsse heben sich auf, also gilt dieselbe Bilanz
im Quotienten. Schnitte aus ganzen Blöcken haben exakt dieselbe Masse.
Diese Aussage gilt nicht für beliebige nicht kompatible Partitionen oder
angeschnittene Blöcke ohne zusätzliche Randinformation.

**Keine Eindeutigkeit aus der Ordnung:** Derselbe Graph kann mit f oder 2f
versehen werden. Selbst bei festgehaltener Gesamtmasse können Ströme auf zwei
Zweige anders aufgeteilt werden. Ordnung und Gesamtmasse bestimmen daher die
lokalen Materiemarken nicht. Die Kontrollen enthalten beide Gegenbeispiele.

**Erhaltung genügt nicht für Staub:** Zwei gleich starke Gegenströme mit
Geschwindigkeiten ±v haben verschwindenden räumlichen Gesamtstrom, aber
\(T^{xx}/\rho_{\rm rest,total}=v^2/(1-v^2)>0\).
Die Definition allein liefert weder Einströmigkeit noch Druckfreiheit,
Geodätenbewegung, Materiewirkung oder gravitative Rückwirkung. Diese Eigenschaften
muss der spätere gekoppelte Kandidat begründen.

## 3. Endliche Referenz statt periodischer Zelle

Unverändert aus REF-DUST-FB-01: G=1, R₀=10, M∈{0,25;1;4},

\[
T_s(M)=\frac23\sqrt{\frac{R_0^3}{2GM}},\quad
R_b(T)=R_0(1-T/T_s)^{2/3},\quad
H=-\frac{2}{3(T_s-T)},\quad \rho=\frac{3M}{4\pi R_b^3}.
\]

Das gemeinsame Fenster ist 0≤T≤T_end=½ min Tₛ=3,7267799625. Die fünf
Zeitpunkte liegen bei {0;¼;½;¾;1}T_end. Der flache homogene Staubinnenraum
wird an Schwarzschild mit derselben Masse M angeschlossen. Die Oberfläche ist
mitbewegend und trägt in dieser Referenz keine zusätzliche dünne Materieschicht.

Zur eindeutigen Volumendefinition wählen wir die marginal gebundene
Painlevé–Gullstrand-Fortsetzung der Oberflächeneigenzeit:

\[
ds^2=-dT^2+(dR-v\,dT)^2+R^2d\Omega^2,\qquad
v=\begin{cases}HR,&R\le R_b,\\-\sqrt{2GM/R},&R\ge R_b.\end{cases}
\]

Am Rand stimmen beide v überein. Die T-Schnitte sind beidseits räumlich flach,
die Vierervolumenform ist R² sinθ dT dR dθ dφ. Dies ist eine erklärte klassische
Geometriedictionary, keine aus einem Kausalset rekonstruierte Koordinate. Es
gibt keine periodische Identifikation. Der gesamte Vakuumaußenraum wird nicht
mit Punkten gefüllt; das Messgebiet umfasst nur die deklarierten endlichen
Detektorweltrohre. Eine äußere numerische Abschneidung und CST-Intervallbeiträge
über diese hinaus werden hier nicht dynamisch geprüft.

| Detektor | Radialbereich auf dem T-Schnitt | Messgröße |
|---|---|---|
| whole | 0…R_b | gesamte Staubmasse und ganzes Innenvolumen |
| core | 0…0,5 R_b | zentrale mittlere Dichte |
| bulk | 0,5 R_b…0,8 R_b | mittlere Schalendichte |
| rim | 0,8 R_b…R_b | materialseitige Randregion |
| fixed_R4 | 0…4 | fester Arealradius, durchströmter Detektor |
| surface_material | R_b−0,5…R_b | maskierte Materialseite |
| surface_total | R_b−0,5…R_b+0,5 | Material und Vakuum, volle Detektordichte |

Das feste Randmaß w=0,5 bleibt bei Zählverfeinerung unverändert. Mitbewegende
Detektoren ändern ihre physikalische Größe im Verlauf des Kollapses; an einem
gegebenen T bleibt ihr physikalischer Bereich über alle Verfeinerungen gleich.
Die Ergebnisse sind keine punktweisen Dichteschätzer im Grenzfall w→0.

## 4. Masse und Fluss: deterministische Kalibrierung

Gleichgewichtete radiale Massenzellen werden durch
\(s_i=(i+1/2)/P,\ \chi_i=s_i^{1/3},\ m_i=M/P\) repräsentiert,
i=0,…,P−1, P∈{64,256,1024,4096}. Es handelt sich um radiale Quadraturpunkte,
nicht um eine erzeugte vierdimensionale CST-Sprinklung oder eine Angularauflösung.
Jeder Marker folgt der vorgegebenen klassischen Mitbewegung.

Für ein radiales Massenintervall ist die kumulative Mittelpunkt-Abweichung je
Endpunkt höchstens 1/(2P), folglich \(|\widehat Q-Q|\le M/P\).
Die ganze Kugel besitzt exakt Masse M. Für die Differenz zweier solcher
Messungen folgt konservativ ein Flussfehler höchstens 2M/P.

Für einen inneren Weltrohrradius R_D(T)=χ_D(T)R_b(T) ist
Q_D=Mχ_D³ und der nach außen gerichtete Fluss

\[
\dot\Phi_{\rm out}=4\pi R_D^2\rho\,[H R_D-\dot R_D]
=-3M\chi_D^2\dot\chi_D,\qquad
Q_D(T_2)-Q_D(T_1)+\Phi_{\rm out}=0.
\]

Kontrollen: χ_D=1 (kein Seitenfluss); R_D=4 (negativer Fluss, Einstrom);
χ_D=0,8−0,2T/T_end (positiver Fluss). Alle drei Detektorwände sind im
deklarierten Fenster zeitartig: die maximale Relativgeschwindigkeit beträgt
für R=4 höchstens 0,716 und für die schrumpfende χ-Fläche höchstens 0,537.
Die Flüsse werden zusätzlich unabhängig über die Kontinuumsrate integriert.

420 Massen- und 144 Flussfälle erfüllen ihre Schranken. Bei P=4096 beträgt
die größte beobachtete Massenabweichung 0,011868 % von M, die Flussabweichung
0,012516 % von M. Die garantierten Schranken sind 0,024414 % beziehungsweise
0,048828 % von M; sie beziehen sich auf die Gesamtmasse, nicht auf die eventuell
kleine Masse eines Detektors. Der diskrete Bilanzrest ist in diesen Fällen null.
Das ist ein Nachweis der konservativen Darstellung; die Bewegung wurde eingesetzt.

## 5. Vierervolumen, räumliches Volumen und Zeitfenster

N im vierdimensionalen Detektorweltrohr zählt bei vorgegebener Poisson-Sprinklung
\(N\sim\mathrm{Pois}(\lambda\Omega_4)\), mit

\[
\Omega_4=\int_{T_-}^{T_+}V_D(T)\,dT,\quad
A_D=\frac{\Omega_4}{V_D(T_c)},\quad
\widehat V_D(T_c)=\frac{N}{\lambda A_D}.
\]

N/λ schätzt ein Vierervolumen; es darf nicht als räumliches Volumen benutzt
werden. Bei genau bekanntem A ist der Volumenschätzer unverzerrt und
\(\mathrm{Var}(\widehat V)=V^2/\mu\), µ=λΩ₄. Ein Kehrwert davon ist jedoch
weder automatisch ein unverzerrter noch ein integrierbarer Dichteschätzer.

Die Zeitfenster besitzen Vergangenheit/Zukunft-Multiplikatoren (1,1), (1,2),
(2,1) eines Basishalbfensters 0,1T_end. Sie werden an [0,T_end] abgeschnitten.
Es werden die tatsächlich verbleibenden Integrationsgrenzen benutzt.
Für mitbewegende Detektoren mit V∝(Tₛ−T)², d=Tₛ−T_c und tatsächlichen
Halbweiten h₋,h₊ lautet die exakte Mittelungskorrektur

\[
F=\frac{A}{\Delta T}=1-\frac{h_+-h_-}{d}
+\frac{h_+^2-h_+h_-+h_-^2}{3d^2}.
\]

Der naive Schätzer N/(λΔT) hat relativen Mittelwertfehler F−1. Im festen Plan
erreicht dessen Betrag 21,3333 %. Bei Randdetektoren fester physikalischer Breite
wird stattdessen deren tatsächliches Volumen integriert; die quadratische
Mitbewegungsformel darf nicht pauschal übertragen werden.

Alle benötigten Integrale sind analytisch:

\[
I_p=\int_l^h R_b^p\,dT=
\frac{R_0^p T_s}{1+2p/3}
\left[(1-l/T_s)^{1+2p/3}-(1-h/T_s)^{1+2p/3}\right].
\]

Für surface_material ist Ω₄=(4π/3)(3wI₂−3w²I₁+w³ΔT), für surface_total
Ω₄=(4π/3)(6wI₂+2w³ΔT). 315 unabhängige adaptive Quadraturen stimmen relativ
bis 5,33·10⁻¹⁵ mit diesen Formeln überein. Zusätzlich liegen 1575 Vergleiche
einer verfeinerten Mittelpunktquadratur vor. Zählverfeinerung und
Integrationsverfeinerung sind verschiedene Vorgänge.

## 6. Dichteintervalle, Bias und Kovarianz

Für α*=0,05/1260 liefert das zentrale Garwood-Intervall

\[
\mu_L=\tfrac12\chi^2_{2N,\alpha^*/2}\ (N>0),\quad \mu_L(0)=0,
\qquad\mu_U=\tfrac12\chi^2_{2N+2,1-\alpha^*/2}.
\]

Setze V_L,U=µ_L,U/(λA). Mit der deterministischen Massenschranke Q_L≤Q≤Q_U
folgt \(\rho\in[Q_L/V_U,Q_U/V_L]\). Bonferroni sichert über alle 1260
Zählintervalle mindestens 95 % gleichzeitige Überdeckung ohne Unabhängigkeitsannahme.
Diese Überdeckungswahrscheinlichkeit ist von der nachstehenden
Präzisions-/Erfolgswahrscheinlichkeit zu unterscheiden.

**Leere Zählung:** Für N=0 und positive mögliche Masse ist V_L=0 und die obere
Dichtegrenze unendlich: HOLD_ZERO_COUNT. Kein Pseudocount, kein Abschneiden des
Kehrwerts. Weil P(N=0)=exp(−µ)>0 für jedes endliche µ, besitzt ein als unendlich
fortgesetzter literal inverser Zählschätzer keine endlichen positiven Momente.
Ein reguläres klassisches Volumen kann dennoch vorliegen. Das ist eine Grenze
des Messadapters, kein Nachweis einer physikalischen Raumzeitsingularität.

**Randsignal:** Der volle Randdetektor misst

\[
\rho_{\rm total}/\rho_{\rm bulk}
=\frac{R_b^3-(R_b-w)^3}{(R_b+w)^3-(R_b-w)^3}.
\]

Das Verhältnis liegt zwischen 0,460398 und 0,475021. Diese Verdünnung durch
Vakuum ist Bestandteil der deklarierten Messgröße. Eine materialseitige Maske
liefert in der bekannten Referenz wieder die Bulk-Dichte. Ohne unabhängig
bestimmte Oberfläche ist diese Maskierung nicht kalibriert.

**Überlappung:** Für eine gemeinsame Poisson-Zählung gilt
Cov(N_A,N_B)=λ Vol₄(A∩B). Das folgt aus der Zerlegung in die disjunkten Mengen
A\B, B\A und A∩B. Zwölf 6×6-Kovarianzmatrizen für verschachtelte whole/core-
Detektoren und überlappende Zeitfenster werden geprüft. Für die deklarierte
Differenz zweier Fenster überschätzt eine fälschliche Unabhängigkeitsannahme
die Varianz um den Faktor 1,4945 bis 1,4998. Bei Summen kann die Richtung des
Fehlers anders sein. Die Formel allein beschreibt keine zusätzliche dynamische
Kovarianz von Materie-, Uhren- oder Geometriemarken.

**Kalibrierunsicherheit:** Bei deterministischen Grenzen λ∈[λ_L,λ_U] und
A∈[A_L,A_U] gilt V∈[µ_L/(λ_U A_U), µ_U/(λ_L A_L)]. Die Dichtegrenzen werden
entsprechend weitergegeben. `calibrated_intervals` implementiert dies. Eine
Zusatzkontrolle mit ±1 % auf λ und ±2 % auf A verbreitert beide Intervalle.
Das 5-%-Ziel wird für diese erweiterten Unsicherheiten hier nicht neu freigegeben.
Statistische Kalibriergrenzen benötigen ein zusätzlich zugeteiltes Fehlerbudget.

## 7. Vorab festgelegter Verfeinerungsplan

Der unveränderte Plan umfasst 3 Massen × 5 Zeiten × 3 Fenster × 7 Detektoren =
315 Fälle pro Stufe, vier Zähldichten, insgesamt 1260 Intervalle. λ₀ wird aus
dem deklarierten analytischen Design so gewählt, dass min µ=5000. Dies ergibt
λ₀=92,894688446 L⁻⁴. P=4096 bleibt für die Massenschranken fest.

Gesucht ist die Wahrscheinlichkeit, dass beide Intervalle vollständig in
[0,95;1,05] des jeweiligen wahren Wertes liegen. Dafür müssen die Garwoodgrenzen
innerhalb [L,U] liegen, wobei

\[
L=\mu\max(0{,}95,Q_U/(1{,}05Q)),\qquad
U=\mu\min(1{,}05,Q_L/(0{,}95Q)).
\]

Die zulässigen ganzzahligen Zählwerte werden aus den monotonen Intervallgrenzen
bestimmt, die Erfolgswahrscheinlichkeit aus Poisson-CDF und Survivalfunktion.
Für 315 Fälle liefert 1−ΣP(Fehlschlag), bei null abgeschnitten, eine untere
Schranke. Negative Kontrollrechnung: der unkorrektierte Adapter verlangt
Garwoodgrenzen in [L/F,U/F]. Auch er wird ohne Zufallsstichproben ausgewertet.

| λ/λ₀ | Kleinster Erwartungswert µ | Untere Schranke gemeinsamer Präzisionserfolg | Entscheidung |
|---:|---:|---:|---|
| 1 | 5 000 | 0 | HOLD: Plan nicht qualifiziert |
| 2 | 10 000 | 0 | HOLD: Plan nicht qualifiziert |
| 4 | 20 000 | 0,9812029663 | PASS nur für bedingte Referenz |
| 8 | 40 000 | 0,9999997228 | PASS nur für bedingte Referenz |

Eine untere Schranke von null behauptet keine Erfolgswahrscheinlichkeit von
exakt null. Die unkorrektierte Kontrollrechnung erreicht auf keiner Stufe eine
positive gemeinsame Untergrenze. Die vollständig geprüften Einzelfallwerte
stehen in den CSV-Dateien; die kleinste numerische Garwood-Überdeckung beträgt
0,99996032098, konsistent mit 1−α*.

Bei λ=4λ₀ hätte ein vollständiges zeitliches Innenweltrohr je Masse ungefähr
3,38 bis 5,11 Millionen Punkte, bei 8λ₀ etwa 6,77 bis 10,21 Millionen. Das sind
Ressourcenprognosen, keine ausgeführten Läufe; Paarrelationen, Außenraum und
dynamische Historien können erheblich teurer sein. Die Null-Zählwahrscheinlichkeit
wird in den Rohdaten als log P₀=−µ geführt, damit Unterlauf nicht als exakte
Null fehlinterpretiert wird.

## 8. Eigene Regularitätsentscheidung

Auf dem festen klassischen Fenster ist R_b≥6,29960525. Aus den eingesetzten
Metriken folgen ρ≤0,003819718635, K_in=60G²M²/R_b⁶≤0,01536 und
K_out=48G²M²/R⁶≤0,012288 für R≥R_b. Der Dichtesprung an der Oberfläche
führt hier zu einem endlichen Krümmungssprung, nicht zu einer zusätzlichen
Delta-Materieschicht. Vakuumdichte null bedeutet keine verschwindende Krümmung.
Diese Aussagen gelten für das gesamte deklarierte klassische Fenster, nicht
für T→Tₛ oder eine Fortsetzung durch den klassischen Kollapsendpunkt.

Die physikalische CST-Regularität bleibt HOLD: Operatoren und Domänen,
physikalisches Maß, uniforme Schranken, Tails und kontrollierter Grenzprozess
sind damit nicht geliefert. Weder ein kleiner Bilanzrest noch ein verbessertes
Dichteintervall noch ein Bounce kann diese Entscheidung ersetzen.

## Geltungsgrenzen

Alle acht physikalischen Gates des Elternvertrags bleiben am Prüfpunkt P2 HOLD.
`checkpoint_P2_record.json` wird mit dem unveränderten Eltern-Gate geprüft;
`record_valid=true` bestätigt die Vollständigkeit des Datensatzes, keinen
physikalischen Beweis. Die Referenzentscheidungen werden gesondert gespeichert.

Offen bleiben insbesondere: dynamische Erzeugung der Materiemarken aus demselben
gekoppelten Kern; Einströmigkeit und Druckfreiheit; intrinsische Uhren und
Detektoren; unabhängige Kalibrierung von A und λ; Coarse-Fibre-/Historiengewichte;
Krümmungsoperatoren; kausale Beziehungen und Wirkungsbeiträge über die
Materieoberfläche; dynamisches Anschlussgesetz und äußerer Gebietsfehler.
Der Randvergleich dieser Arbeit ersetzt keinen CST-Innen-/Rand-/Außenraumtest.

Die früheren geglätteten BD-Paarstromschätzer nutzen eine andere Definition und
klassisch eingesetzte Dichtemarken. Deren bisherige Entscheidungen bleiben
unverändert. Insbesondere werden ihre unzureichenden Einzelordnungs-Trefferquoten
nicht durch die hier verwendeten exakten Referenzkorrekturen repariert.

Der nächste freigabefähige Schritt ist ein deklarierter Adapter, der aus dem
gekoppelten Kandidaten f, Uhr, Oberflächenmaske und Exposition erzeugt, ohne die
gesuchten Referenzwerte einzusetzen. Erst danach folgt ein unabhängiger
Korrespondenztest mit vorab festgelegtem Gesamtfehlerbudget. Es gibt hier keine
neue Aussage über Horizonte, Schwarze Löcher oder Singularitätsauflösung.

## Quellen und Herkunft

1. Projektvertrag: [CST-DUST Model Contract v0.1](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/0e47038f15d93edef486fbb68da5dad6bf017221/research/rax_cqg/dust_collapse/model_contract_v0_1/PUBLICATION.md), zugehörige `contract.json` unverändert im Paket.
2. J. D. Brown, K. V. Kuchař, *Dust as a Standard of Space and Time in Canonical Quantum Gravity*, [arXiv:gr-qc/9409001](https://arxiv.org/abs/gr-qc/9409001). Kontinuumsreferenz für Staub, keine Ableitung unserer diskreten Transportmarken.
3. F. Garwood, *Fiducial Limits for the Poisson Distribution*, Biometrika 28 (1936), 437–442, [doi:10.1093/biomet/28.3-4.437](https://doi.org/10.1093/biomet/28.3-4.437). Grundlage der exakten Poissonintervalle.
4. K. Krishnamoorthy, Y. Xia, F. Xie, *A Simple Approximate Procedure for Constructing Binomial and Poisson Tolerance Intervals* (2011), [Autorenfassung](https://userweb.ucs.louisiana.edu/~kxk4695/2011-Xia-Xie-CS.pdf). Explizite Chi-Quadrat-Darstellung des Garwood-Konfidenzintervalls; wir verwenden keine approximativen Toleranzintervalle aus dieser Arbeit.
5. Frühere Projektstände: README und Design des Pakets `CST_Staubkollaps_Geglaetteter_Massestrom_Pruefpaket.zip` unter `research/rax_cqg/dust_collapse/packages/` im selben Repository; gelesene Auszüge unter `inputs/previous_smoothed_*`.

Graphidentitäten, Quadraturgrenzen, Expositionsformeln und Fehlerfortpflanzung
werden oben unmittelbar hergeleitet. Der Planhash belegt die unveränderte
lokale Planversion; er ist keine externe Präregistrierung oder unabhängige Begutachtung.
