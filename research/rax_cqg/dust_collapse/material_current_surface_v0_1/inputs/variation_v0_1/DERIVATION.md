# CST-DUST: gemeinsamer Variationskandidat und Quantennormierung v0.1

Stand: 6. November 2026. Kandidat `CST-DUST-V1-RAW-K`; Plan `CST-DUST-VARIATION-001`.
Basis: Main nach PR 244, Commit `9fa170dfd604be3847004ea2bdbe8587ada5d068`.

**Ergebnis:** Eine regulierte gemeinsame Geometrie-Staub-Amplitude ist als Kandidat
definiert. Ihre endlichen Wirkungsvariationen und ein bedingter Außenfeld-Response
sind ausgerechnet. Die zusätzliche Interpretation ihres rohen Randkerns als
geschlossene Quantenevolution mit den unten festgelegten kinematischen
Skalarprodukten scheitert analytisch. Ein physikalisches CST-Junction-Gesetz,
eine gemeinsame Außenraumgeometrie und ein globaler Bounce sind damit nicht
hergeleitet. Diese Aussagen bleiben HOLD; das FAIL betrifft allein die ausdrücklich
angegebene Realisierung des Kandidaten.

## 1. Träger, Einheiten und Annahmen

Wir verwenden endliche strikte partielle Ordnungen C bei festem N. Anfangs- und
Endantichain sind markiert; jedes freie Element liegt kausal zwischen mindestens
einem Anfangs- und einem Endelement. Die extern vorgegebenen Ordnungs- und
Felddaten bleiben erhalten. Die implementierte Spezialklasse hat genau ein
Anfangselement 0, ein Endelement N−1 und 0 ≺ x ≺ N−1 für alle freien x.
Die breitere Enumeration aller gelabelten Ordnungen bis N=5 dient nur der
algebraischen Implementierungsprüfung. Sie ist kein vierdimensionales Ensemble.

C enthält gemeinsam Materieträger und Außenbereich. Eine interne Zerlegung A/B
ist eine Markierung derselben Geschichte und kein Ersatz durch zwei unabhängige
Summen. Bei nichtlokaler Kopplung gehören auch durch die interne Grenze laufende
Intervalle zur vollständigen Wirkung. Der äußere Rechenrand ist davon verschieden.

Bei c=1 hat T die Dimension Länge. B hat die Dimension Länge⁻². Mit
v₄=ℓ⁴ und einer Dichte ρ mit Dimension Wirkung/Länge⁴ setzen wir w=v₄ρ.
**w ist ein integriertes Dichtegewicht mit Dimension Wirkung, keine Ruhemasse.**
Eine räumliche Ruhemasse benötigt zusätzlich eine physikalisch definierte
Hypersurface und einen kalibrierten Strom. Im Code sind der B-Vorfaktor und ℏ
jeweils 1; physikalische Skalen werden damit nicht numerisch bestimmt.

Die Gravitationswirkung ist

\[
S_g/\hbar=\kappa F_4(C),\qquad
F_4=N-N_0+9N_1-16N_2+8N_3,
\quad\kappa={4\over\sqrt6}{\ell^2\over\ell_P^2},
\quad\ell_P^2=8\pi G\hbar.
\]

N_k zählt kausale Paare mit k strikt dazwischenliegenden Elementen. Λ=0 und
S_outer=0 werden für diesen Kandidaten ausdrücklich angenommen. Letzteres ist
**kein** hergeleiteter zeitartiger GHY-Term und keine qualifizierte Behandlung
eines physikalischen äußeren Randes. Die folgenden algebraischen Rechnungen
hängen von dieser offenen Grenzwertfrage nicht ab.

## 2. Eine konkrete Materiewirkung

Für y ≺ x sei k_C(y,x) die Intervallgröße. Der unverschmierte BD-Kandidat in 4D ist

\[
B_{xx}=-A,\quad B_{xy}=A b(k_C(y,x)),\quad
A={4\over\sqrt6\ell^2},\qquad b=(1,-9,16,-8,0,\ldots).
\]

Alle übrigen Einträge verschwinden. Definiere

\[
\Gamma_x[T]={1\over2}\{B(T^2)_x-2T_x(BT)_x+T_x^2(B1)_x\}
={1\over2}\sum_{y\prec x}B_{xy}(T_x-T_y)^2,
\]

\[
S_d[C,T,w]=-{1\over2}\sum_x w_x(\Gamma_x+1)
=-{1\over2}\sum_x w_x-{1\over4}\sum_{y\prec x}w_xB_{xy}(T_x-T_y)^2.
\]

Die zweite Darstellung folgt durch direktes Ausmultiplizieren, einschließlich
des diagonalen Terms. Der Term T²B1 ist wesentlich: Für B→□−R/2 hebt er den
Nullordnungsterm auf, sodass Γ formal zu g^{ab}∂_aT∂_bT wird. Ohne ihn bliebe
zusätzlich RT²/4. Auf jedem endlichen C ist Γ invariant unter T→T+c; die
unkorrigierte Formel besitzt diese Eigenschaft nicht.

Dies motiviert den irrotationalen Kontinuumskandidaten

\[
S_d^{\rm cont}=-{1\over2}\int d^4x\sqrt{-g}\,\rho
\left(g^{ab}\partial_aT\partial_bT+1\right),\quad(-+++).
\]

Seine **Kontinuums**variation gibt Normierung, Kontinuität und auf der
Normierungsfläche den Staub-Stresstensor:

\[
g^{ab}\partial_aT\partial_bT=-1,\qquad
\nabla_a(\rho\nabla^aT)=0,\qquad
T_{ab}=\rho\,\partial_aT\partial_bT=\rho u_a u_b,
\quad u_a=-\partial_aT.
\]

Bei gewählter Zukunftsorientierung ist u ein zeitartiges Einheitsfeld. Aus seiner
Gradientenform und Normierung folgt u^a∇_a u_b=0. Diese Rechnung betrifft nur
wirbelfreien Staub vor Mehrstrombildung beziehungsweise Kaustiken. Sie beweist
keine endliche CST-Geodätengleichung. Eine physikalische Brücke müsste B,
Produktidentität, erste Variationen, Materiegrößen und Randbeiträge gemeinsam
kontrollieren. Konvergenz einer gemittelten Wirkung reicht dafür nicht.
Unter Geometrievariation sind w und ρ zudem über das Volumenelement verbunden;
die Umparametrisierung muss in einem Kontinuumsvergleich berücksichtigt werden.

## 3. Regulierte gemeinsame Amplitude

Für externe Daten b_ext wird festgelegt:

\[
K_N(b_{\rm out},b_{\rm in})={1\over|G_{\rm fix}|}
\sum_{C\in\Omega_N^{\rm lab}(b_{\rm ext})}
\int \prod_{x\in F_T}{dT_x\over2T_{\max}}
\prod_{x\in F_w}d\nu(w_x)\,
\exp\!\left({i\over\hbar}[S_g(C)+S_d(C,T,w)]\right),
\]

\[
-T_{\max}\le T_x\le T_{\max},\qquad
d\nu(w)={1\over2}\delta_0(dw)
+{1\over2w_{\max}}\mathbf1_{(0,w_{\max})}(w)\,dw.
\]

F_T und F_w enthalten genau die nicht extern fixierten Variablen; Randgewichte
können also integriert werden, wenn nur Randuhren vorgegeben sind. G_fix ist die
Permutationsgruppe, die alle fixierten Labels und Marken erhält. Das gelabelte
Zählmaß dividiert durch |G_fix| ist invariant; sein Pushforward auf vollständig
markierte Orbits hat die entsprechenden Stabilisatorgewichte. Dies ist eine
explizite Modellwahl, keine Ableitung eines physikalischen Quantenmaßes.

Der Atomanteil erlaubt exakt w=0. Ein rein stetiges positives Dichtemaß gäbe einem
genau vakuumartigen Trägermuster Maß null. Die Summe über die 2^{|F_w|}
Atom-/Positivmuster ist eine Summe über getrennte Trägerstrata; ein binärer
Staubindikator erhält keine erfundene infinitesimale Ableitung. Die Wahrscheinlichkeiten
1/2, die kompakten Regulatoren, das Zählmaß, die Wahl Λ=0 und das fehlende
äußere Randfunktional sind Annahmen. Es gibt hier kein Gesetz für verschiedene N.

Auch auf w=0-Elementen wird ein Hilfsfeld T zugelassen. Wegen nichtlokaler Zeilen
der Materiewirkung kann dieses Feld an positive w koppeln. Seine physikalische
Bedeutung oder sein kontrolliertes Verschwinden im Vakuumgrenzwert ist offen.
Die Wirkung ist konstant verschiebungsinvariant in T; ein festes Integrationsfenster
und externe Zustände sind es nicht. Regulatorunabhängigkeit ist nicht bewiesen.

Für festes N sind Summe und Integrale endlich. Der Kern ist dadurch mathematisch
definiert, aber weder als physikalisches Skalarprodukt noch als Zeitentwicklung
qualifiziert. Eine reine, zusätzlich festgelegte Anfangsdichte wird in Abschnitt 8
für den Normierungstest benutzt. Ein realistischer Kollapszustand ist nicht gewählt.

## 4. Dichte-, Uhr- und Stromvariation

In einem offenen positiven Stratum 0<w_x<w_max gilt

\[
{\partial S_d\over\partial w_x}=-{1\over2}(\Gamma_x+1).
\]

Ein innerer stationärer Punkt verlangt Γ_x=−1. Das Atom w=0 hat keine solche
Tangentialvariation. Endpunkte und Stratumwechsel sind gesondert zu behandeln.
An einem minimalen Element ist Γ=0: Dort existiert kein positiver innerer
Normierungssattel. Anfangskragen beziehungsweise Vorgeschichte können deshalb
nicht aus der physikalischen Modellierung weggelassen werden.

Definiere den gerichteten **Variationsstrom**

\[
j_{y\to x}={1\over2}w_xB_{xy}(T_x-T_y),\qquad
q_z={\partial S_d\over\partial T_z}
=\sum_{z\to x}j_{z\to x}-\sum_{y\to z}j_{y\to z}.
\]

Die freie Uhrvariation gibt q_z=0. Bei jeder Teilmenge A folgt durch Aufheben
innerer Beiträge exakt

\[
\sum_{z\in A}q_z=\sum_{A\to\bar A}j-\sum_{\bar A\to A}j.
\]

Dies ist eine echte Konsequenz der gewählten Wirkung. Der Strom kann wegen der
alternierenden B-Gewichte vorzeichenbehaftet sein. Seine Beziehung zum zuvor
kalibrierten groben Staubstrom und zu einer positiven Ruhemasse ist nicht bewiesen.

Mit Inzidenzmatrix D (−1 am Vorgänger, +1 am Nachfolger) gilt

\[
L={1\over2}D^T\operatorname{diag}(w_xB_{xy})D,\qquad
S_d=-{1\over2}T^TLT-{1\over2}\sum_xw_x,\qquad q=-LT.
\]

L ist symmetrisch, im Allgemeinen indefinit. Obwohl B retardiert ist, enthält
die Euler-Variation Beiträge aus Vergangenheit und Zukunft. Man darf den
retardierten Operator nicht ohne Herleitung an die Stelle von −LT setzen.
Die Symmetrie des Hessians allein beweist jedoch keine physikalische Akausalität;
dafür wären Zustand, Anfangswertproblem und physikalische Quantenevolution
auszuarbeiten. Hier ist nur ein endliches Randwertfunktional definiert.

## 5. Gemeinsame Geometrievariation und interne Grenze

Ein diskreter Move C→C′ muss Ordnungseigenschaften und die fixierten externen
Daten erhalten. Bei festen T,w und unverändertem Maß ergibt sich genau

\[
\Delta S=\hbar\kappa\Delta F_4
-{1\over4}\sum_{y,x}w_x(B'_{xy}-B_{xy})(T_x-T_y)^2.
\]

Die Summe enthält **alle** geänderten Intervalle. Das Umschalten einer Relation
ändert gegebenenfalls auch Gewichte anderer Paare. Ein automatischer transitiver
Abschluss darf vorgegebene Teilordnungen nicht nachträglich verändern. Bei
geänderten Integrationsgebieten, Zuständen oder Maßen gehören deren Beiträge
ebenfalls in die Amplitudenvariation. Eine endliche Umbenennung der Summanden
ist weiterhin nur eine Identität; sie fordert nicht ΔS=0 für jeden Mikromove.

Für C=A⊔B mit isolierten induzierten Teilwirkungen gilt

\[
S_d(C)=S_d(A)+S_d(B)+X_d+R_d,
\]

wobei X_d über Paare zwischen den Blöcken und R_d über interne Paare summiert.
Für jedes Paar ist der Grundfaktor −w_x(T_x−T_y)²/4. In X_d wird er mit B^C_xy
multipliziert, in R_d mit B^C_xy−B^D_xy, D=A oder B. R_d zählt somit interne
Intervallumklassifizierungen. Der Beweis ist die disjunkte Paarzerlegung; die
konstanten Dichteanteile sind additiv. Gemeinsam mit der bereits geprüften
BDG-Verklebung liegt damit die vollständige endliche Kopplung der gewählten
Wirkungen vor. Ein zusätzlicher interner Oberflächenterm würde diese Kopplung
ohne weitere Begründung doppelt zählen.

## 6. Quantenspezifische Variation: Regulatoren erhalten

Für eine freie Uhr gilt auf ihrem Integrationsintervall

\[
\int_{-L}^L dT\,\partial_T(f e^{iS/\hbar})
=[f e^{iS/\hbar}]_{-L}^{L}.
\]

Nur bei nachgewiesen verschwindenden Randbeiträgen wird daraus die übliche
randfreie Schwinger-Dyson-Form. Mit normiertem Gleichmaß, S=0 und f=T sind
linke Seite und Randbeitrag beide 1, nicht 0. Endliche Boxen erlauben kein
stillschweigendes Weglassen. Ebenso ist das Integral über positives kompaktes w
ein endlicher Fourierfaktor, keine Deltafunktion der Normierungsbedingung.
Die w-Stationarität aus Abschnitt 4 ist keine exakte Quanten-Zwangsbedingung.

Für eine kontinuierliche externe Uhrvariable q, bei festem Träger, Maß und
Integrationsgebiet und K≠0, ist außerdem die **vollständige endliche
Amplitudenvariation** wohldefiniert. Lokal wähle einen Logarithmuszweig und setze
W(q)=−iℏ log K(q). Differentiation unter den endlichen Summen und kompakten
Integralen liefert

\[
\partial_q W=\langle\partial_q S_{\rm tot}\rangle_K,\qquad
\partial_r\partial_q W=\langle\partial_r\partial_q S_{\rm tot}\rangle_K
+{i\over\hbar}\left(\langle S_q S_r\rangle_K
-\langle S_q\rangle_K\langle S_r\rangle_K\right).
\]

Hier ist ⟨f⟩_K das Verhältnis der gemeinsamen Geometrie-Feld-Summe mit
Insertion f zu derselben Summe ohne Insertion, nicht ein positives
Wahrscheinlichkeitserwartungsmaß; S_q=∂_qS_tot. Die Integranden sind im
endlichen Modell auf dem kompakten Feldgebiet glatt und beschränkt, sodass
die Differentiation hier zulässig ist. An Nullstellen von K ist W nicht
definiert. Bei Parameterabhängigkeit von Maß, Zustand, Träger oder Gebiet
müssen deren zusätzliche Ableitungen aufgenommen werden. Die Formel ist eine
exakte, im Allgemeinen komplexe Randantwort dieses Amplitudenkandidaten,
noch keine kausale In-in- oder Junction-Gleichung. Sie zeigt auch, weshalb die
Variation einer einzelnen stationären Wirkung die Quantenantwort nicht ersetzt.

## 7. Bedingter Außenfeld-Response

Bei **fester** Geometrie und Dichte zerlege T in gehaltene Variablen X,
zu eliminierende Hilfsuhren E und fixierte äußere Daten b. Für invertierbares
L_EE folgt aus q_E=0

\[
T_E=-L_{EE}^{-1}(L_{EX}T_X+L_{Eb}T_b),\qquad
L_{\rm eff}=L_{XX}-L_{XE}L_{EE}^{-1}L_{EX}.
\]

Eine singuläre Matrix erfordert die gesonderte Behandlung ihrer Verträglichkeits-
und Nullraumbedingungen. Ein unbegründetes Pseudoinverses schließt sie nicht.

**Ausgerechnetes Beispiel:** Fünferkette 0≺1≺2≺3≺4, w=(0,0,1,1,0),
T₀=0, T₄=4, X={2,3}, E={1}; B-Vorfaktor 1. Es gilt

\[
L_{EE}=-4,\qquad T_1={-T_2+9T_3\over8},\qquad
L_{\rm eff}={1\over16}\begin{pmatrix}-55&-17\\-17&145\end{pmatrix},
\quad q_3={17T_2-145T_3\over16}.
\]

Neun rationale Feldpaare erfüllen die eliminierten Uhrgleichungen und die
Gleichheit der reduzierten Wirkung exakt. Das Beispiel zeigt die Abhängigkeit
einer Grenzantwort vom gemeinsam gekoppelten Hilfsfeld. Es löst weder die
w-Normierungsbedingungen noch eine Staubbewegung oder eine Vakuummetrik.
Das w=0-Element 1 ist kein rekonstruierter Außenraum. Die invertible, negative
E-Eigenzahl ist ein stationärer Sattel, kein Minimum. Quantenintegration über
kompakte Felder ist nicht gleich Sattelpunktsubstitution; Determinanten, Phasen
und Boxrandkorrekturen sowie die Geometriesumme bleiben erforderlich.

## 8. Normierungsgegenbeispiel

Jetzt prüfen wir eine **zusätzliche Interpretation**: K soll unmittelbar ein
geschlossenes Evolutionsabbild zwischen zwei jeweils zweidimensionalen
kinematischen Hilberträumen sein. Beide haben das feste Skalarprodukt I₂.
Ihre ausdrücklich deklarierten orthonormalen Labels lauten anfangs T=(0,1),
am Ende T=(2,3). Dies sind keine vollständigen kontinuierlichen Uhrbasen und
kein abgeleiteter physikalischer Staub-Hilbertraum.

Für N=2 existiert im gewählten Träger eine einzige Kausalrelation 0≺1.
w₀=0 ist fixiert; w₁ wird mit 1/2 δ₀+1/2 dw auf (0,1) integriert. ℏ=1,
B-Vorfaktor 1 und T_max=4. Die Geometriewirkung ist für alle Einträge gleich
und entfällt als gemeinsame Phase in K†K. Mit α Anfangs- und β Endlabel:

\[
a={1\over2}+{(\beta-\alpha)^2\over4},\qquad
G(a)={1\over2}+{1\over2}\int_0^1e^{-iaw}dw
={1\over2}+{1\over2}e^{-ia/2}\operatorname{sinc}(a/2),
\]

\[
K=\begin{pmatrix}G(3/2)&G(3/4)\\G(11/4)&G(3/2)\end{pmatrix}.
\]

Für a∈{3/4,3/2,11/4}⊂(0,π) gilt Re G(a)>1/2 und Im G(a)<0.
Daher ist der Realteil jedes Produkts \(\overline{G(a)}G(b)\) größer als 1/4 und

\[
\operatorname{Re}(K^\dagger K)_{01}>1/2.
\]

Damit ist K†K für **keinen** konstanten Faktor c>0 gleich c I₂. Eine einzige
zustands- und quellenunabhängige Normalisierung kann den Kern nicht isometrisch
machen. Das ist ein analytisches Gegenbeispiel im deklarierten endlichen Modell;
es braucht weder statistische Toleranzen noch einen Fit.

Für den festen Anfangszustand ρ₀=|+⟩⟨+|, |+⟩=(1,1)/√2, und
D(J)=diag(1,e^{iJ}) vor K sei

\[
n(J)=\operatorname{Tr}(KD(J)\rho_0D(J)^\dagger K^\dagger),\qquad
Z[J_+,J_-]={\operatorname{Tr}(KD(J_+)\rho_0D(J_-)^\dagger K^\dagger)\over n(0)}.
\]

Für normierte geschlossene Evolution müsste Z[J,J]=1 sein. Hier ergeben sich
gerundet n(0)=2.916131516588 und n(π)=0.0514149637264 und zertifiziert

\[
0.017631222540533480523076038214892713
\le Z[\pi,\pi]\le
0.017631222540533480523076038214892714.
\]

Separates Normieren für jedes J würde das erzeugende Funktional ändern und
repariert nicht dieselbe lineare geschlossene Evolution. Ein positiver
Gram-Dekohärenzausdruck bei festem Zustand ist möglich, garantiert aber diese
Normierungsidentität nicht.

**Reichweite:** Gravitationsamplituden können Zwangsprojektoren beziehungsweise
Rigging-Maps statt Evolutionsoperatoren sein. Der Test schließt diese Deutung,
andere physikalische Skalarprodukte, eine korrekte Constraint-Reduktion,
vollständige kontinuierliche Randräume und kontrollierte Grenzwertfamilien nicht
aus. Insbesondere ist die kleine Ordnung keine physikalische 4D-Staubhistorie.
Die Ablehnung betrifft genau den Zusatz „dieser rohe Kern mit I₂ ist bereits
geschlossene Evolution“. Sie ist kein No-go-Satz für CST.

## 9. Zertifikat, Kontrollen und Entscheidungen

G wird mit rationaler komplexer Taylorrechnung bis Grad p=80 ausgewertet.
Die integrierte Restschranke ist

\[
r(a)={|a|^{p+1}\over2(p+1)!(p+2)}.
\]

Dies folgt aus dem Taylorrest von e^{−iaw} entlang des reellen Integrationsweges,
dessen Ableitungen den Betrag |a|^{p+1} besitzen. Mit r=max r(a) und |G|≤1
ist jeder Gram-Eintrag der ungerundeten rationalen Rechnung bis
ε=2(2r+r²) eingeschlossen. Die Normen n(0),n(π) haben Fehler höchstens 2ε.
Intervallquotienten werden aus positiven Nennergrenzen gebildet.
Alle Vergleiche erfolgen exakt rational. Zertifizierte Dezimalgrenzen werden
nach außen gerundet. Angezeigte nominale komplexe Einträge besitzen zusätzlich
eine konservative Rundungsschranke 10⁻³³, getrennt vom Taylorfehler ausgewiesen.

| Prüfung | Umfang | Ergebnis / Reichweite |
|---|---:|---|
| Gelabelte Ordnungen N=1…5 | 4 473 | Algebraische Trägerkontrolle |
| Produktidentität | 22 095 Stellen | Exakt null Rest |
| Uhrableitung | 22 095 Stellen | Exakt gegen zentrale Differenz der quadratischen Wirkung |
| Dichteableitung | 22 095 Stellen | Exakt gegen zentrale Differenz der linearen Wirkung |
| Konstante Uhrverschiebung | 22 095 Stellen | Exakt invariant |
| Materieverklebung | 130 116 geordnete Zweiblockfälle | Exakt mit Kreuz- und Umklassifizierungsbeitrag |
| Variationsstrom über Schnitte | 130 116 Fälle | Exakter Saldo, keine physikalische Kalibrierung |
| Labelpermutationen N≤4 | 5 377 Fälle | Exakt invariant |
| Zulässige einzelne Relationstoggles N≤4 | 1 240 Instanzen | Exakte gemeinsame Wirkungsdifferenz |
| Intervallträger-Spezialklasse N≤5 | 24 Ordnungen | Teilklasse der Algebraenumeration |
| Bedingte Schurantwort | 9 Feldpaare | Exakt, bei festem C,w |
| Strukturelle Positiv-/Negativkontrollen | 10 | Alle erwarteten Ausgänge |
| Roher Kern als geschlossene Evolution mit I₂ | 1 analytisches Gegenbeispiel | FAIL für diese Realisierung |

Die zentrale Differenz ist hier eine unabhängige Auswertung der Wirkung, keine
approximative Differentiation: Bei quadratischen beziehungsweise linearen
Polynomen ist sie für h=1/3 exakt. Die Testfelder und weiteren Parameter wurden
im lokalen Plan vor der Rechnung fixiert. Der analytische Ausfallmechanismus
war bereits bekannt; dies ist keine blinde Vorhersage oder externe Präregistrierung.

Der unveränderte geerbte Model-Contract prüft einen neuen, eng begrenzten
P1-Datensatz mit model_id `CST-DUST-V1-RAW-K`. Ergebnis: MODEL=FAIL,
CURRENT/CORRESPONDENCE/BOUNCE/REGULARITY/BOUNDARY/TRAPPING/EXTENSION jeweils HOLD.
Der Audit validiert die deklarierte Evidenzstruktur; er beweist nicht selbst die
angegebenen Rechnungen. Frühere P5-HOLD-Ergebnisse werden nicht überschrieben.
Es gibt keine neuen 4D-Dynamikensembles, Sprinklings, Zufallsdaten oder bezahlten Läufe.

## 10. Was zu einem physikalischen Junction law noch fehlt

Die fehlende physikalische Definition ist durch eine bloße Symbolfolge
δ(S_g+S_d)=0 nicht geschlossen. Vor einer kausalen effektiven Anschlussvariation
werden ein begründeter Zustandsraum mit physikalischem Skalarprodukt, eine
Constraint-/Evolutionsinterpretation, Zustände und zulässige Quellen benötigt.
Ein anderer Kandidat ist neu zu versionieren und unabhängig vom gewünschten
Bounce zu begründen; eine nachträgliche Anpassung nur zur Normreparatur ist keine
physikalische Ableitung.

Für eine qualifizierte In-in-Konstruktion wäre anschließend eine gemeinsame
effektive Wirkung Γ_eff[q_+,q_-] aus demselben Innen-/Außenraum-System zu
berechnen. Die Gleichung δΓ_eff/δq_Δ=0 bei q_Δ=0, mit q_Δ=q_+−q_−, ist hier
nur das **Ziel einer noch fehlenden Konstruktion**. Ein gemeinsamer Randresponse
muss Quellen, Maß, Zustand, äußere Daten und alle Kreuzintervalle mitführen.
Einfach −iℏ log K zu variieren liefert ohne diese Voraussetzungen keine reelle
kausale Junction-Dynamik. Das gewünschte Vakuum außen, eine mitbewegte
Materiegrenze, Strom- und gravitative Bilanz sind gemeinsame Lösungsbedingungen.

Danach müssen die ersten Variationen im klassisch kontrollierten Bereich
gegen irrotationalen Staub und die gravitative Rückwirkung geprüft werden.
Verfeinerung benötigt gleiche physikalische Daten, ein Skalenverhältnis für
Diskretheit und Nichtlokalität, Randkontrolle und vorab definierte Toleranzen.
Der vorliegende Regulatortest ersetzt diese Prüfung nicht.

Regularität bleibt eigenständig: Dichte-/Krümmungsobservablen, inverse Momente,
Verteilungsschwänze, Zeitbereich und Verhalten unter physikalisch abgeglichener
Verfeinerung. Weder ein stationärer Hilfsfeldsattel noch ein Minimum des mittleren
Volumens entscheidet diese Frage. Ein globaler Bounce oder ein Horizontanspruch
kann durch den vorliegenden Kandidaten nicht bestätigt werden.

## Literatur und Herkunft

1. D. M. T. Benincasa, F. Dowker, *The Scalar Curvature of a Causal Set* (2010),
   [arXiv:1001.2725](https://arxiv.org/abs/1001.2725). Grundlage des BD-Operators;
   keine Herleitung der hier gewählten Staubamplitude.
2. F. Dowker, S. Liu, J. Lloyd-Jones, *Timelike boundary and corner terms in the
   causal set action*, [arXiv:2501.00139v2](https://arxiv.org/html/2501.00139v2).
   BDG-Biaktion und untersuchte zeitartige Randbeiträge; kein fertiges CST-Staub-Junction-Gesetz.
3. M. Buck, F. Dowker, I. Jubb, S. Surya, *Boundary Terms for Causal Sets* (2015),
   [arXiv:1502.05388](https://arxiv.org/abs/1502.05388). Raumartige Randkonstruktionen.
4. J. D. Brown, K. V. Kuchař, *Dust as a standard of space and time in canonical
   quantum gravity*, Phys. Rev. D 51, 5600 (1995),
   [arXiv:gr-qc/9409001](https://arxiv.org/abs/gr-qc/9409001).
   Kontinuums-Hintergrund für dynamische Staubreferenzfelder; der vorliegende
   Ansatz ist eine wirbelfreie Einschränkung, keine Diskretisierung der gesamten Theorie.
5. E. Calzetta, B. L. Hu, *Closed-time-path functional formalism in curved spacetime:
   Application to cosmological back-reaction problems*, Phys. Rev. D 35, 495 (1987),
   [DOI:10.1103/PhysRevD.35.495](https://doi.org/10.1103/PhysRevD.35.495).
   CTP als Rahmen kausaler Rückwirkung; die endliche Normierungsidentität und das
   Gegenbeispiel oben sind unmittelbar aus der Spurdefinition bewiesen.

Die Materiewirkung, Regulatoren, Maße und kinematischen Randräume dieses Pakets
sind Modellannahmen dieses Arbeitsschritts. Die Literatur wird nicht als Beweis
ihrer physikalischen Gültigkeit verwendet. Geerbte Quellen, Lizenz und Hashes
stehen in `NOTICE` und `inputs/provenance.json`.
