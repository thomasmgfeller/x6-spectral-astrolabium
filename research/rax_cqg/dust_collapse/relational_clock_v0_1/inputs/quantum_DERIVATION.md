# CST-DUST: Zustandsraum, Skalarprodukt und Constraints v0.1

Stand: 6. November 2026. Kandidat `CST-DUST-QS1-RELABEL`;
Plan `CST-DUST-QUANTUM-STRUCTURE-001`.
Basis: Main nach PR 245, `3595df81b8655a5183cdbf5c5da077aef51e4259`.

**Ergebnis:** Eine positive, unter Umbenennungen reduzierte Hilbertraumstruktur
für gemeinsame endliche Geometrie-Materie-Historien ist explizit konstruiert.
Ihre Constraints entfernen die internen Elementlabels. Sie sind keine
hergeleiteten gravitativen Constraints und definieren noch keinen vollständigen
physikalischen Zustandsraum. Zwei konkrete Abkürzungen scheitern: Der bisherige
rohe Kern lässt sich bei der deklarierten Identifikation der Randräume mit
keinem gemeinsamen positiven Skalarprodukt in normerhaltende Evolution
umdeuten. Das direkte Auferlegen der Staub-Eulergleichung als gewöhnliche
L²-Multiplikatorbedingung entfernt sämtliche nichtleeren Staubstrata.

Diese Aussagen widerlegen weder CST noch eine distributionswertige Rigging-Map,
eine korrekt reduzierte relationale Dynamik oder eine kovariante
Historienformulierung. Eine vollständig physikalische Quantendefinition bleibt
HOLD. Die Konstruktion und die beiden Hindernisse sind unten genau abgegrenzt.

## 1. Konkreter Hilfshistorienraum

Bei festem m sei C eine strikte Ordnung auf N=m+2 Elementen mit fest markiertem
Anfang 0 und Ende m+1 sowie 0≺x≺m+1 für alle m inneren Elemente. C enthält die
gemeinsame Geometrie von Materie und Außenbereich. Interne Labels tragen keine
zusätzliche Physik. Anfangs-/Endmarken werden nicht mitgemittelt.

Vor einer Konditionierung auf Randuhrwerte sind alle T_x kontinuierliche freie
Koordinaten in [−4,4]. Die inneren Dichtegewichte haben das bereits deklarierte
Maß

\[
d\nu(w)=\tfrac12\delta_0(dw)+\tfrac12\mathbf1_{(0,1)}(w)\,dw.
\]

Die beiden Endgewichte sind in dieser Hilfsfamilie null. Das ist eine explizite
Randwahl für die neue kinematische Konstruktion, keine Behauptung über einen
realen Staubball. Der frühere Zweistellen-Kern wird in Abschnitt 5 mit seinen
**unveränderten eigenen** Randbedingungen separat untersucht: Dort ist das
Endgewicht integriert. Beide Konstruktionen werden nicht gleichgesetzt.

Definiere die positive endliche Hilfsmaßstruktur

\[
d\mu_m={1\over m!}\sum_{C\in\Omega^{\rm lab}_{m+2}}
\prod_{x=0}^{m+1}{dT_x\over8}\prod_{x=1}^{m}d\nu(w_x),
\qquad \mathcal H_{\rm aux,m}=L^2(X_m,d\mu_m).
\]

Das Geometriezählmaß muss für die Definition eines Hilbertraums nicht auf eins
normiert sein. Es ist auch nicht die komplexe Gewichtung exp(iS/ℏ). Diese
Wirkungsphase erzeugt keine positive Norm. Das Hilfsmaß und die kompakten
Regulatoren sind Kandidatenannahmen, keine physikalische Auswahl aus CST.

Der dichte Testbereich Φ besteht stratumweise aus glatten Funktionen mit
kompaktem Träger im Innern der Uhrbox und der jeweils positiven w-Intervalle.
Die Atom-/Positivstrata werden als direkte Summe behandelt. Für jedes feste m
sind nur endlich viele Ordnungen beteiligt. Unterschiedliche m werden hier
nicht durch ein dynamisches Sektorgewicht miteinander verbunden.

**Rolle dieses Raums:** Er ist ein Hilfshistorienraum vollständiger endlicher
Patches. Es ist nicht bewiesen, dass er ein vollständiger physikalischer
Cauchy- oder Randzustandsraum für kausale Entwicklung ist. Bei nichtlokalen
Intervallwirkungen darf ein endlicher Randkragen nicht ohne Schließungsnachweis
an die Stelle der benötigten Vorgeschichte treten. Ein aus einem physikalischen
Dekohärenzfunktional konstruierter Historien-Hilbertraum wäre eine andere,
zusätzlich zu begründende Konstruktion; siehe Abschnitt 8.

## 2. Exakte Umbenennungsconstraints und positives Quotientprodukt

Die endliche Gruppe G_m=S_m wirkt gleichzeitig auf C, T, w und die
Materie-/Vakuumträgermarken. Die beiden äußeren Labels bleiben fest. Weil die
Produktmaße für alle inneren Felder gleich sind, ist

\[
(U_g\psi)(z)=\psi(g^{-1}z),\qquad U_g^\dagger=U_{g^{-1}}
\]

unitär auf H_aux. Die vollständige BDG- und Materiewirkung ist invariant unter
diesem gemeinsamen Umbenennen. Die Materiemarken dürfen nicht unabhängig von
Geometrie und Feldern gelöscht oder als reine Eichlabels behandelt werden.

Für erzeugende Vertauschungen s kann man echte endliche Hilfsconstraints

\[
C_s=I-U_s,\qquad C_s=C_s^\dagger,\qquad
P_m={1\over m!}\sum_{g\in S_m}U_g
\]

definieren. Jedes C_s ist positiv semidefinit, da U_s eine selbstadjungierte
Involution mit Eigenwerten ±1 ist. Direkte Gruppensummation zeigt

\[
P_m^\dagger=P_m,\quad P_m^2=P_m,\quad C_sP_m=0,\qquad
\mathrm{Ran}\,P_m=\bigcap_s\ker C_s.
\]

Die C_s müssen untereinander nicht kommutieren. Die gemeinsame Lösung ist
durch die Gruppeninvarianz dennoch exakt bestimmt. Dies ist kein importierter
kontinuierlicher Hamilton-Constraint und keine Lie-Algebra räumlicher
Diffeomorphismen. Die endliche Gruppe liefert keinen Staubzeitgenerator.

Die positive semidefinite Form

\[
B_{\rm rel}(\psi,\chi)=\langle\psi,P_m\chi\rangle_{\rm aux}
=\langle P_m\psi,P_m\chi\rangle_{\rm aux}
\]

hat Nullraum ker P_m. Nach Quotientbildung und Vervollständigung erhält man
H_rel≅Ran P_m mit positiv definitem Produkt. Für eine komplex-linear im zweiten
Argument gewählte Konvention kann die antilineare Rigging-Form
η_rel(ψ)[χ]=B_rel(ψ,χ) geschrieben werden. **Sie löst nur die Labelconstraints.**
Die Bezeichnung η_rel ist keine physikalische Qualifikation von η_phys.

### Vollständig markierte diskrete Kontrollbasis

In der Unterklasse von Funktionen, die innerhalb jedes Feldstratum konstant
sind, besteht die Basis aus (C,σ), wobei σ die inneren positiven Gewichte
markiert. Jeder diskrete Punkt hat Gewicht 1/(m!2^m). Für einen Orbit O mit
Stabilisator Aut(C,σ) folgt

\[
|O|\,|\mathrm{Aut}(C,\sigma)|=m!,\qquad
\mu(O)={1\over 2^m|\mathrm{Aut}(C,\sigma)|},\qquad
(P_m)_{xy}=\begin{cases}1/|O|,&x,y\in O,\\0,&\text{sonst.}\end{cases}
\]

Der Faktor 2^{−m} stammt aus dem Dichte-Stratummaß und darf nicht verloren
gehen. Für normierte diskrete Basisvektoren ist der invariante Orbitvektor
|O⟩=|O|^{−1/2}Σ_{x∈O}|x⟩. Das Matrixelement 1/|O| ist kein neuer dynamischer
Historienfaktor; die Amplituden-Gruppengewichte werden nicht doppelt angewandt.

Alle 3 671 markierten Zustände mit m=0,…,4 zerfallen in 234 Orbits.
85 035 Gruppenwirkungen bestätigen die Projektorzeilen. 4 817 gemeinsame
Geometrie-/Feldumbenennungen bestätigen die Wirkung exakt. Die hierbei
benutzten Polynom-Testfelder können außerhalb der kompakten Regulatorbox liegen;
das sind algebraische Invarianzprüfungen, keine Stichproben des Quantenmaßes.
Die Maßinvarianz folgt separat aus der gemeinsamen Permutation identischer
Faktoren. Bei m=1 bleiben Vakuum- und Materiemarke zwei verschiedene Orbits.

## 3. Observablen und fehlende dynamische Reduktion

Eine beschränkte, reelle, vollständig labelinvariante Funktion O(C,T,w) wirkt
als selbstadjungierter Multiplikator auf H_aux und erhält H_rel. Beispiele sind
die Relationenanzahl, die Anzahl positiver Dichtegewichte oder symmetrische
Feldfunktionen. Das qualifiziert diese Größen als Observablen der
**Labelreduktion**, noch nicht als gravitative Dirac-Observablen.

Für eine kanonische physikalische Konstruktion müssten weitere Constraints,
ihre Definitionsbereiche, gemeinsame Lösung beziehungsweise geeignete
Rigging-Map und die dazu passende Observablenalgebra hergeleitet werden. Die
neue Struktur enthält weder einen symplektischen Phasenraum für dynamische
Geometrievariationen noch einen aus der CST-Amplitude gewonnenen Hamiltonoperator.
Wirkungsstationarität allein liefert diese fehlenden Daten nicht.

Ein geeigneter allgemeiner Zieltyp ist

\[
\Phi\subset H_{\rm aux}\subset\Phi^*,\qquad
\eta_{\rm phys}:\Phi\to\Phi^*,\qquad
B_{\rm phys}(\psi,\chi)=\eta_{\rm phys}(\psi)[\chi]\ge0
\ \text{auf der Diagonale},
\]

mit Constraint-Annihilation und einer passenden Adjungiertheitsbeziehung für
physikalische Observablen. Quotient und Vervollständigung der positiven Form
ergeben erst dann H_phys. Die Bedingungen der Refined Algebraic Quantization
sind nicht automatisch für CST erfüllt [1,2]. Eine distributionswertige η muss
kein beschränkter orthogonaler Projektor auf H_aux sein; η² kann sogar als
gewöhnliches Operatorprodukt undefiniert sein.

## 4. Warum das direkte Auferlegen der Staub-Eulergleichung scheitert

Aus dem vorigen Wirkungsansatz stammt auf einem positiven Dichtestratum

\[
\partial S_d/\partial w_x=-\tfrac12(\Gamma_x+1),\qquad
\Gamma_x={1\over2}\sum_{y\prec x}B_{xy}(T_x-T_y)^2.
\]

Untersucht wird die zusätzliche, nicht hergeleitete Vorschrift,
C_x(T)=Γ_x(T)+1 als Multiplikationsconstraint C_xψ=0 im gewöhnlichen
H_aux aufzuerlegen, für jede Stelle mit positivem Dichtegewicht.

**Satz für die frei kontinuierlichen Uhren dieser Hilfsfamilie:** Auf jedem
nichtleeren Staubstratum ist der gemeinsame L²-Lösungsraum dieser Bedingungen
{0}. Auf dem vollständig leeren Staubstratum gibt es keine dieser Bedingungen.

**Beweis.** Für eine besetzte Stelle x ist C_x ein reelles Polynom in den freien
Uhren. Bei konstantem T ist C_x=1; das Polynom ist daher nicht identisch null.
Seine Nullmenge besitzt Lebesgue-Maß null. Das folgt beispielsweise induktiv aus
der endlichen Nullstellenzahl eines nichtverschwindenden Polynoms in einer
Variablen und Fubini für die verbleibenden Variablen; die Menge, auf der alle
Koeffizienten verschwinden, ist wiederum eine polynomiale Nullmenge niedrigerer
Dimension. C_xψ=0 erzwingt, dass ψ fast überall außerhalb dieser Nullmenge null
ist. Eine L²-Funktion mit Träger in einer Nullmenge ist das Nullelement.
Der gemeinsame Kern liegt bereits in diesem trivialen Einzelkern. Die
zusätzlichen Dichteintegrale ändern dies nach Fubini nicht. ∎

7 249 besetzte Stellen der markierten Kontrolle bestätigen den konstanten
Polynomwert 1 exakt. Diese endlichen Kontrollen illustrieren den allgemeinen
Beweis; sie ersetzen ihn nicht.

Die Aussage gilt **vor** festen Randuhrwerten und unter dem gewählten
absolut stetigen Uhrmaß. Auf bereits singulären oder konditionierten Flächen
muss neu geprüft werden; ein Polynom kann nach einer speziellen Fixierung
identisch null werden. Distributionelle Lösungen in Φ* können existieren,
auch wenn der gewöhnliche L²-Kern leer ist. Das ist kein No-go für Staub oder
für eine korrekte Dirac-Quantisierung. Vor allem wurde nicht bewiesen, dass die
Eulergleichung überhaupt als genau dieser kanonische Constraint zu verwenden ist.

## Gemeinsames Skalarprodukt

Der unveränderte frühere Kern lautet bei ℏ=A=w_max=1

\[
G(a)=\tfrac12+\tfrac12\int_0^1e^{-iaw}dw,\qquad
K=\begin{pmatrix}G(3/2)&G(3/4)\\G(11/4)&G(3/2)\end{pmatrix}.
\]

Er bildet die ausdrücklich endlichen kinematischen Uhrlabels (0,1) auf (2,3)
ab; das anfängliche Dichtegewicht ist null, das endgültige integriert. Wir
untersuchen zusätzlich die festgelegte Identifikation beider Labelräume durch
Translation um 2 und **ein gemeinsames** positives Hermitesches M. Gesucht wäre

\[
K^\dagger M K=cM,\qquad M>0,\quad c>0.
\]

c erlaubt einen beliebigen einzigen Normierungsfaktor; eine gemeinsame komplexe
Phase der Gravitationswirkung ist unerheblich. Für unterschiedliche unidentifizierte
Randräume ist eine Spur von K zunächst nicht sinnvoll; die Identifikation gehört
deshalb ausdrücklich zur geprüften Zusatzinterpretation.

**Notwendiges Kriterium.** Falls M existiert, ist M^{1/2}KM^{−1/2}/√c unitär.
Die beiden Eigenwerte von K haben daher gleichen Betrag. Für det K≠0 folgt

\[
R={(\operatorname{tr}K)^2\over\det K}
=2+{\lambda_1\over\lambda_2}+{\lambda_2\over\lambda_1}
=2+2\cos(\theta_1-\theta_2)\in[0,4].
\]

Dieses notwendige Kriterium ist unter gemeinsamer Basisänderung und beliebiger
von null verschiedener skalarer Multiplikation von K invariant. Es wird nicht
als hinreichendes allgemeines Kriterium verwendet.

Die rationalen Intervallrechnungen ergeben

\[
|\det K|^2\in
[0.019907015704867842217891511662565,
 0.019907015704867842217891511662566],
\]

\[
\operatorname{Im}R\in
[-2.4527328506264341446412621423239,
 -2.4527328506264341446412621423238].
\]

Damit ist R nicht reell; sein Realteil liegt zusätzlich bei etwa 22,2335.
**Für diese Identifikation existiert kein gemeinsames positives M**, auch nicht
zusammen mit einem frei gewählten konstanten Normierungsfaktor. Die frühere
Ablehnung allein für I₂ ist damit in genau diesem Sinn verstärkt.

Die endliche Umbenennungsgruppe des Zweistellenfalls mit fixierten Endlabels
ist S₀={e}. Die oben konstruierte Labelreduktion wirkt hier als Identität und
kann das Gegenbeispiel daher nicht verändern.

### Was durch diesen Satz nicht ausgeschlossen wird

Für invertierbares K lässt sich zu einem gegebenen M_out>0 stets
M_in=K†M_outK definieren. Das macht K bezüglich **zweier** Produkte formal
isometrisch. Ohne unabhängige Begründung der beiden Produkte wird damit die
gesuchte Norm jedoch durch den zu prüfenden Kern festgelegt. Anders begründete
ungleiche Randprodukte werden durch den gemeinsamen-M-Satz nicht widerlegt.
Auch Polarzerlegung ersetzt K durch einen anderen Operator; sie ist keine
Ableitung unveränderter Amplituden aus CST.

Ein zusätzliches bedingtes Korollar ergibt sich, wenn die beiden nichtentarteten
diagonalen Uhrmatrizen selbst Observablen mit denselben Eigenvektoren bleiben
sollen. Ihre Selbstadjungiertheit erzwingt diagonale positive M_in und M_out.
Für M_out=diag(u,v), u,v>0, gilt wegen Re G(a)>1/2 und Im G(a)<0 für alle drei
Argumente des Kerns

\[
\operatorname{Re}(K^\dagger M_{\rm out}K)_{01}>(u+v)/4>0.
\]

Diese Matrix kann kein positives diagonales M_in sein, auch nach skalarer
Normierung. Das ist ein analytisches Korollar der vorigen Amplitudenformel,
kein neuer angepasster Test. Es gilt nicht, wenn T nach Reduktion bloß ein
äußerer Zeitparameter ist oder andere Observablen zu begründen sind.

Die endlichen Uhrlabels sind ferner keine normierten Punktzustände des
kontinuierlichen L²-Raums. Punktauswertung ist dort unbeschränkt: normkonstante
Funktionen √n φ(n(T−T₀)) können an T₀ unbegrenzt wachsen. Ein physikalischer
Randvergleich benötigt daher geeignete Testzustände oder Wellenpakete und ein
begründetes Maß. Das Gegenbeispiel wird nicht auf einen ungetesteten vollständigen
Kontinuumsraum übertragen.

## 6. Positivkontrolle: Constraint und relationale Evolution zusammen

Eine vollständig lösbare **mathematische Referenz**, nicht ein CST-Hamiltonian,
ist H_aux=L²(R,dτ)⊗C² mit Schwartz-Testbereich und

\[
\widehat C=-i\partial_\tau+H,\qquad H=\operatorname{diag}(1,-1),\quad\hbar=1.
\]

C ist auf dem üblichen selbstadjungierten Impulsbereich plus beschränktem H
selbstadjungiert. In unitärer Fourierdarstellung ist C diagonal mit Werten
p+E_a. Die Gruppenmittelung ist distributionswertig; auf Testfunktionen
definiert sie die positive Form

\[
B(f,g)=\sum_{a=1}^2\overline{\widetilde f_a(-E_a)}\,
\widetilde g_a(-E_a),\qquad H_{\rm phys}\cong\mathbb C^2.
\]

Dies folgt aus (2π)^{−1}∫ds exp[is(p+E_a)]=δ(p+E_a). Die Form annihiliert C
und besitzt den erwarteten Nullraum der Testfunktionen mit beiden verschwindenden
Fourierauswertungen. Die Quotientabbildung ist surjektiv auf C². Obwohl die
Constraint-Lösungen nicht in L² über der ganzen Zeitachse liegen, haben sie
eine wohldefinierte positive physikalische Norm.

\[
\Psi(\tau)=e^{-iH\tau}\psi,\qquad
i\partial_\tau\Psi=H\Psi,\qquad
U(\tau_2+\tau_1)=U(\tau_2)U(\tau_1),\quad U^\dagger U=I.
\]

Bei τ=kπ/2 sind alle Matrixeinträge Gaußsche rationale Zahlen. Vier
Normprüfungen, 16 Kompositionsprüfungen und vier distributionswertige
Constraint-Proben stimmen exakt. Die Proben benutzen Fourierfunktionen
exp(1−p²)(a+bp), deren Werte bei p=±1 rational sind. Sie sind keine
numerischen Approximationen von Deltafunktionen.

Zusätzlich besteht K=S diag(1,i)S^{−1}, S=[[1,1],[0,1]], die exakte
M-Normprüfung mit M=[[1,−1],[−1,2]]>0. Der Kontrollkern diag(1,2) scheitert
an R=9/2>4. Der Prüfweg erkennt somit sowohl einen gültigen nichttrivialen
M-Fall als auch einen ungültigen Fall.

Dies zeigt, wie Constraint- und Evolutionsdeutung zusammenpassen können. Die
Staubzeitreduktion von Brown und Kuchař liefert dazu eine relevante
Kontinuumsreferenz [3], aber keine Herleitung des hier fehlenden CST-Hamiltonians.
Im Außenraum ohne Staub darf das zuvor eingeführte Hilfsfeld T nicht ohne
weiteren Nachweis als physikalische globale Uhr verwendet werden. Kaustiken,
Uhrmonotonie und das gemeinsame Ein-/Außenraum-Anfangswertproblem bleiben offen.

## 7. Warum die positive Struktur die Dynamik nicht auswählt

Schon auf dem Referenzraum C² sind H₀=0 und H₁=diag(1,−1) beide
selbstadjungiert und erzeugen unitäre Entwicklung. Für ψ=(1,1)/√2 und die
Observable σ_x erhält man bei τ=π/2 die verschiedenen Erwartungswerte +1 und −1.
Die Hilbertraumstruktur allein wählt keinen der beiden Operatoren aus.

**Es wird nicht behauptet, dass beide Hamiltonians die CST-Amplitude reproduzieren.**
Das Beispiel isoliert nur die Unterbestimmtheit durch Zustandsraum, Positivität
und Labelconstraints. Ein physikalischer Hamiltonian müsste zusätzlich aus der
Gesamtamplitude beziehungsweise einer begründeten kanonischen Reduktion stammen,
deren klassischer Grenzfall und Randanschluss kontrolliert sind.

## 8. Eine kovariante Historienalternative bleibt möglich

Eine kanonische Constraint-/Hamilton-Konstruktion ist nicht die einzig mögliche
Quantendefinition. In einem Historienansatz kann ein stark positives
Dekohärenzfunktional D auf Ereignissen eine semidefinite Form und nach
Nullraumquotient einen Historien-Hilbertraum erzeugen [4]. Für endlich viele
Ereignisse ist die Konstruktion durch die entsprechende Gram-Matrix gegeben.
Die physikalische Dynamik steckt dann bereits in D, nicht erst in der positiven
Hilbertraumvervollständigung.

Für unser Programm wären ein aus der gemeinsamen Geometrie-Materie-Amplitude
und dem Zustand begründetes D, Normierung, Additivität, Kovarianz, geeignete
Verklebungs-/Verfeinerungsverträglichkeit und die tatsächlich benutzte
Ereignisdomäne zu kontrollieren. Die Fortsetzung auf größere Ereignisalgebren
ist eine eigenständige Frage; sie kann selbst bei bekannten Modellen schwierig
sein [5,6]. Eine kleine positive Gram-Matrix oder ein auf einen einzelnen Zustand
normierter Ausdruck allein liefert diese Qualifikation nicht.

Dieser alternative Zweig wird hier nicht ausgeführt oder ausgeschlossen. Die
im eingefrorenen Plan geprüfte Route betrifft die endliche Labelreduktion,
den naiven gewöhnlichen L²-Constraint und die gemeinsame-M-Evolutionsdeutung.
Ein Wechsel zu einer Historien-Quantendynamik benötigt einen neuen expliziten
Modellvertrag, keine nachträgliche Umbenennung des fehlgeschlagenen Tests.

## 9. Zertifizierung und separate Entscheidungen

G wird bis Taylorgrad p=80 mit rationaler Arithmetik berechnet. Für jeden
komplexen Eintrag gilt die Restschranke

\[
r(a)={|a|^{p+1}\over2(p+1)!(p+2)}.
\]

Reell- und Imaginärteile werden jeweils mit ±r eingeschlossen. Rationale
Rechteck-Intervallarithmetik propagiert diese Einschließungen durch Determinante,
Spurquadrat, Konjugation und Division. Die untere Schranke für |det K|² ist
positiv. Alle Entscheidungen erfolgen vor der Anzeige exakt rational;
32-stellige Dezimalgrenzen sind nach außen gerundet. Es gibt keine angepasste
Toleranz, Stichprobe oder Monte-Carlo-Aussage.

| Prüfung | Umfang | Ergebnis |
|---|---:|---|
| Markierte Zustände, m=0…4 | 3 671 | vollständige kleine Kontrollklasse |
| Gruppenwirkungen | 85 035 | direkte Summe stimmt mit Orbitprojektor überein |
| Orbit-/Projektorblöcke | 234 | exakte Idempotenz und korrekte Stabilisatorgewichte |
| Gemeinsame Wirkungsumbenennungen | 4 817 | exakte Invarianz |
| Nichtverschwindende Normierungspolynome | 7 249 | konstanter Testwert 1 |
| Gemeinsames positives M für vorherigen K | allgemeiner 2×2-Satz und Intervallzertifikat | ausgeschlossen im deklarierten Identifikationsmodell |
| Referenz-Norm-/Kompositionskontrollen | 4 / 16 | exakt bestanden |
| Distributionelle Constraint-Proben | 4 | exakt bestanden |

Der neue P1-Datensatz `CST-DUST-QS1-RELABEL` hat acht physikalische HOLDs.
Der getrennte Datensatz `CST-DUST-V1-RAW-K-COMMON-M` hat MODEL=FAIL und sieben
HOLDs. Das frühere FAIL wird nicht in ein PASS umgedeutet. Der geerbte
Model-Contract bleibt unverändert; sein Audit prüft die deklarierte
Evidenzstruktur, nicht automatisch die mathematischen Beweise.

Der Plan wurde lokal vor der Rechnung fixiert. Die strukturellen Hindernisse
wurden vor der numerischen Zertifizierung erwartet; keine blinde Vorhersage
und keine externe Präregistrierung. Es gibt keine neuen physikalischen
4D-Ensembles, Sprinklings, Zufallsdaten oder bezahlten Läufe.

## 10. Ergebnisgrenze für das Staubballprogramm

Definiert und geprüft sind H_aux, der dichte Testbereich, die endliche
Umbenennungsdarstellung, ihre Constraints, η_rel, das positive Quotientprodukt
und eine Klasse labelinvarianter Observablen. Vollständig physikalische
dynamische Constraints, η_phys oder ein aus CST abgeleiteter relationaler
Hamiltonian sind nicht gewonnen. Die vorhandene Amplitude und ihre endlichen
Variationen legen diese fehlende Quantendefinition nicht durch bloßes
Normieren oder Umbenennen fest.

Ein weiterer dynamischer Kandidat muss unabhängig von einem gewünschten
Bounce begründet und versioniert werden. Er muss die gemeinsame
Geometrie-Materie-Amplitude beziehungsweise eine begründete Änderung davon,
Zustände, Observablen und die Innen-/Außenraumkopplung konsistent verbinden.
Erst danach werden kausale Anschlussgleichung, Korrespondenz, Verfeinerung und
globale Entwicklung qualifizierbar. Regularität behält eigenständige Dichte-,
Krümmungs-, inverse-Moment- und Tail-Prüfungen. Ein globaler Bounce oder
Singularitätsauflösung wird hier nicht behauptet.

## Primärquellen

1. D. Giulini, D. Marolf, *On the Generality of Refined Algebraic Quantization*,
   Class. Quantum Grav. 16, 2479 (1999),
   [arXiv:gr-qc/9812024](https://arxiv.org/abs/gr-qc/9812024).
   Bedingungen für RAQ und die Beziehung von Rigging-Map und physikalischem Produkt.
2. D. Marolf, *Group Averaging and Refined Algebraic Quantization: Where are we now?*
   (2000), [arXiv:gr-qc/0011112](https://arxiv.org/abs/gr-qc/0011112).
   Gruppenmittelung und ihre Voraussetzungen; kein CST-spezifischer Abschluss.
3. J. D. Brown, K. V. Kuchař, *Dust as a standard of space and time in canonical
   quantum gravity*, Phys. Rev. D 51, 5600 (1995),
   [arXiv:gr-qc/9409001](https://arxiv.org/abs/gr-qc/9409001).
   Kontinuumsreferenz einer Staubzeitreduktion.
4. F. Dowker, S. Johnston, R. D. Sorkin, *Hilbert Spaces from Path Integrals*
   (2010), [arXiv:1002.0589](https://arxiv.org/abs/1002.0589).
   Hilbertraumkonstruktion aus dem Dekohärenzfunktional.
5. F. Dowker, S. Johnston, S. Surya, *On extending the Quantum Measure*
   (2010), [arXiv:1007.2725](https://arxiv.org/abs/1007.2725).
   Fortsetzbarkeit von Quantenmaßen als eigene Bedingung.
6. S. Surya, S. Zalel, *A Criterion for Covariance in Complex Sequential Growth
   Models* (2020), [arXiv:2003.11311](https://arxiv.org/abs/2003.11311).
   Spezifische CST-Wachstumsfamilien; nicht die hier verwendete BDG-Staubamplitude.

Die verwendeten elementaren Gruppen-, L²- und Spektralargumente sind oben
ausgeführt. Die Literatur wird nicht als Nachweis eines physikalischen
Zustandsraums unseres Kandidaten verwendet. Die unveränderten Vorgängereingaben
und ihre SHA-256-Werte stehen in `inputs/provenance.json`.
