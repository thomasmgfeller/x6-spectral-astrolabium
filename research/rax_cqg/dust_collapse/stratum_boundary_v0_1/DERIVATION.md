# CST-DUST: Stratumwechsel, Randkopplung und Zustandsauswahl v0.1

7. November 2026. Basis: Main nach PR 262,
`4ed1a338f875172f8eb92798e8a8e9046a126f5f`.
Sechs unveränderte Projektquellen einschließlich Lizenz sind in
`provenance.json` mit Git-Blob-Identitäten gepinnt.

## 1. Ergebnis und physikalische Reichweite

Die vorhandene Materiewirkung bestimmt Feldvariationen, aber sie enthält
noch keine qualifizierte Quantisierung auf dem verwendeten Historien-L²-Raum.
Der Mischterm des vorherigen Schritts lässt sich aus den dokumentierten
Definitionen deshalb nicht als physikalische CST-Kopplung identifizieren.
Diese Aussage bezieht sich auf den vorliegenden Vertrag; sie behauptet
keine Unmöglichkeit einer späteren Quantisierung.

Vier zusätzliche Ergebnisse grenzen die offene Aufgabe ein:

1. Die scharfe 1/2-Untergrenze gilt schon für alle Effekte, die nur die
   beiden Dichtestrata erhalten. Innerhalb eines Stratums dürfen sie beliebig
   nichtdiagonal sein. Eine bloße Kinetik innerhalb des positiven Dichtebereichs
   reicht somit nicht.
2. Eine zusätzliche positive quadratische Form koppelt das Dichte-Nullatom
   an die Randspur des kontinuierlichen Anteils. Ihr selbstadjungierter Operator,
   seine Randbedingungen, der Wahrscheinlichkeitsfluss und eine Spektrallücke
   werden vollständig bestimmt. Das ist ein diagnostisches Zusatzmodell,
   keine aus der CST-Wirkung hergeleitete Wechselwirkung.
3. Das Vorzeichen dieser Randkopplung wählt zwei orthogonale kohärente
   Grundzustände aus. Bleibt die Uhrvariable nur Zuschauer, ist der Nullraum
   trotzdem unendlichdimensional. Weitere Zustandsauswahl ist erforderlich.
4. Selbst der zusätzliche Ansatz, die vorhandene Wirkung als Potential
   einzusetzen, lässt den so konstruierten konstanten Zielzustand bei
   nichtverschwindender Kopplung nicht als Eigenzustand bestehen.

**Alle acht physikalischen Gates bleiben HOLD.** Die mathematische Grenze
ist klarer, aber die physikalische Kopplung, das Messinstrument und eine
gravitative Rückwirkung sind nicht hergeleitet. Kein n=5-Produktionslauf,
keine bezahlte Rechenleistung und keine experimentellen Daten.

## 2. Was die vorhandene Wirkung tatsächlich festlegt

Bei fester Kausalordnung und Dichte lautet die geerbte Wirkung

\[
 S_d=-\frac12\sum_xw_x-\frac14\sum_{y\prec x}
             w_x B_{xy}(T_x-T_y)^2
     =-\frac12 T^T L T-\frac12\sum_x w_x,
 \quad L=\frac12 D^T\operatorname{diag}(w_xB_{xy})D.
\]

Ihr Hessian bezüglich der endlich vielen Feldwerte T ist −L. Die
außerdiagonalen Einträge koppeln verschiedene **Ereignis-Feldkomponenten**.
Sie sind keine Matrixelemente zwischen zwei vollständigen Historien Y,Y′.
Im bisher erklärten Raum H=L²(Ω,ν) wird dieselbe reelle Wirkung als
Multiplikation M_S verwendet; exp(iM_S) ist eine diagonale Wirkungsphase.
Ein T-Hessian auf einem endlichdimensionalen Feldraum und ein Generator auf
L² vollständiger Historien wirken auf verschiedenen Räumen. Ihre Gleichsetzung
wäre eine zusätzliche Quantisierungsregel, keine Ableitung.

Für das n=1-Referenzmodell gilt, mit normiertem Uhrrecord x∈(0,1),

\[
 d\nu=dx[\tfrac12\delta_0(dw)+\tfrac12\mathbf1_{(0,1)}dw],
 \qquad S_d(x,w)=-w(\tfrac12+4h^2x^2).
\]

Das Atom bei w=0 und der stetige Anteil sind unabhängige L²-Komponenten.
Ein L²-Vektor hat zunächst überhaupt keinen wohldefinierten Randwert f(0).
Eine Verbindung von Atomwert und kontinuierlicher Randspur benötigt einen
zusätzlichen Definitionsbereich, etwa H¹-Regularität und eine Randform.
Die diskrete Atommasse darf nicht stillschweigend differenziert werden.
Das Dichte-Nullatom ist zudem kein bereits hergeleiteter Fock-Vakuumzustand.

Die Wirkung enthält in dieser Definition keine Ableitung einer Wellenfunktion
nach w. Ein Term −κ∂²_w, sein Kontrollzeitparameter, κ, die Bedingungen an
w=0 und am Regulatorrand w=1 sind weitere Modellangaben. Die Normierung
∂S/∂w=0 in einem offenen positiven Stratum identifiziert ebenfalls keinen
Quantenoperator zwischen Atom und stetigem Anteil. Das war bereits in der
gepinnten Variationsherleitung getrennt worden.

## 3. Stärkerer Ausschluss: Erhaltung der Strata genügt

Sei H=H_a⊕H_c mit Dichteprojektoren Π_a,Π_c. Im vollständigen Referenzraum
enthalten beide Komponenten auch die Uhrvariable x. Wähle normierte
a∈H_a,c∈H_c und ψ_±=(a±c)/√2, P_+=|ψ_+><ψ_+|.

Für jeden Effekt 0≤E≤I mit [E,Π_a]=0 gilt

\[
 \langle\psi_+,E\psi_+\rangle
 =\langle\psi_-,E\psi_-\rangle
 =\tfrac12(\langle a,Ea\rangle+\langle c,Ec\rangle)=q.
\]

Der Zielprojektor hat Werte 1 und 0. Deshalb

\[
 \|E-P_+\|\ge\max(1-q,q)\ge\tfrac12.
\]

Die Grenze wird von E₀=(|a><a|+|c><c|)/2 erreicht. Auf span{a,c} hat
E₀−P_+ die Eigenwerte ±1/2; auf dem orthogonalen Komplement ist er null.
Also gilt exakt

\[
 \boxed{\inf_{0\le E\le I,\,[E,\Pi_a]=0}\|E-P_+\|=\tfrac12.}
\]

Diese Klasse ist größer als die voll recorddiagonale Klasse aus PR 262.
Zum Beispiel darf E innerhalb H_c verschiedene positive Dichtewerte oder
Uhrmoden mischen. Ein solcher Effekt kann andere Phasen erkennen; vollständige
Phasenblindheit wird hier **nicht** behauptet. Unterscheidbar bleiben jedoch
nicht die beiden relativen Vorzeichen zwischen den Strata.

Für einen festen unabhängigen Zeigerstart σ und Zeigerauslese F gilt:
Kommutiert die gemeinsame unitäre Kopplung W mit Π_a⊗I, so kommutiert
E=Φ_σ(W†(I⊗F)W) mit Π_a. Auch Krausoperatoren, die die beiden Strata
erhalten, bleiben unter Produkten, klassischer Rückkopplung und Summen
über akzeptierte Zweige blockdiagonal. Aus blockdiagonalen Anfangszuständen
entsteht keine Kreuzkohärenz. Eine positive Konditionierungswahrscheinlichkeit
ändert daran nichts; die Zielfidelität bleibt höchstens 1/2.

Bei unbeschränkten Generatoren ist die Aussage über die unitäre Gruppe
beziehungsweise über reduzierende Unterräume zu formulieren. Ein formaler
Kommutator auf wenigen Testfunktionen genügt nicht. Die Bedingungen müssen
auch auf die Operatordomänen und Randbedingungen zutreffen.

Der Vergleich setzt beide Testzustände im erklärten Raum voraus. Physikalische
Constraints oder eine ausdrücklich geänderte Observable können eine neue
Aufgabe definieren; die Aussage ist kein allgemeiner CST-Ausschlusssatz.

## 4. Eine vollständig deklarierte Randform

Zunächst wird die Uhr x weggelassen. Der unitäre Wechsel
u(w)↦(u(0)/√2,u|_(0,1)/√2) identifiziert das gewichtete Dichtemodell mit

\[
 \mathcal H_w=\mathbb C\oplus L^2(0,1),\qquad
 \|(a,f)\|^2=|a|^2+\int_0^1|f(w)|^2dw.
\]

Wir **setzen zusätzlich** κ>0, λ≥0 und s∈{−1,+1} und definieren

\[
 Q=\mathbb C\oplus H^1(0,1),\qquad
 q_s[a,f]=\kappa\int_0^1|f'|^2dw+\lambda|a-sf(0)|^2.
\]

Hier parametrisiert w einen Dichte-Record, keinen räumlichen Abstand.
Die Lokalisierung einer Kopplung bei diesem Recordrand beweist keine
raumzeitliche Lokalität oder Kausalität. Insbesondere sind κ,λ,s und der
Kontrollzeitparameter keine aus der Staubwirkung bestimmten Konstanten.

Q ist dicht in H_w. Der Spurwert f(0) ist auf H¹ stetig. Mit κ>0 ist die
Formnorm (||u||²+q_s[u])^(1/2) äquivalent zur Produktnorm auf C⊕H¹:
die untere Schranke folgt aus dem enthaltenen Ableitungsterm, die obere aus
der Spurabschätzung. Damit ist q_s nichtnegativ und abgeschlossen. Der
Darstellungssatz für abgeschlossene quadratische Formen liefert einen
eindeutigen nichtnegativen selbstadjungierten Operator A_s **zu dieser Form**.
Er liefert keine Auswahl der Form selbst.

Partielle Integration von q_s((b,g),(a,f)) bestimmt ihn:

\[
 A_s(a,f)=(\lambda(a-sf(0)),-\kappa f''),
\]
\[
 D(A_s)=\{(a,f):f\in H^2(0,1),\quad
 f'(1)=0,\quad \kappa f'(0)=\lambda(f(0)-sa)\}.
\]

Die am unteren Rand auftretende Koeffizientengleichung ist
−κ f′(0)−sλ(a−sf(0))=0; sie fixiert das Vorzeichen. Am oberen Rand
steht κ f′(1)=0. Eine unabhängige Anwendung von Neumann-Bedingungen an
beiden Enden bei λ>0 wäre ein anderer Operator und würde die Kopplung
im Allgemeinen beseitigen beziehungsweise überbestimmen.

Für λ=0 entsteht 0⊕(−κ∂²_w)_Neumann. Die Strata reduzieren den Operator.
Für λ>0 reduzieren sie ihn nicht: Die Projektion (a,f)↦(a,0) erhält die
angegebene Domäne im Allgemeinen nicht. Entsprechend kann die zugehörige
unitäre Gruppe Übergänge zwischen beiden Komponenten erzeugen.

### Normbilanz und Strom

Für reguläre Lösungen von iℏ∂_t(a,f)=A_s(a,f) definiere

\[
 j(w)=\frac{2\kappa}{\hbar}\operatorname{Im}(\bar f f'),\quad
 \partial_t|f|^2+\partial_w j=0.
\]

Aus den Domänenbedingungen folgt

\[
 j(1)=0,\quad j(0)=\frac{2s\lambda}{\hbar}\operatorname{Im}(\bar a f(0)),
 \quad \partial_t|a|^2=-j(0).
\]

Somit ist d/dt(|a|²+∫|f|²)=0. Für allgemeine H_w-Anfangsdaten folgt die
Normerhaltung aus Selbstadjungiertheit; eine punktweise Stromformel setzt
zusätzliche Regularität voraus. Dieser Strom transportiert Wahrscheinlichkeit
im **Zusatzmodell**, keine bereits kalibrierte Staubmasse durch Raumzeit.

## 5. Grundzustand, Lücke und nicht ausgewählte Randphase

Für λ>0 verlangt q_s=0 sowohl f′=0 als auch a=sf(0). Der Kern ist genau
eindimensional:

\[
 \ker A_s=\operatorname{span}\{\psi_s\},\qquad
 \psi_s=(s,1)/\sqrt2.
\]

Für λ=0 ist der Kern zweidimensional; Atom und konstante stetige Mode sind
unabhängig. Positivität und Normerhaltung allein wählen also keine der beiden
Situationen und kein s aus. Bei festgehaltenem Vergleichseffekt P_+ liefern
die Grundzustände für s=+1 und s=−1 die Werte 1 und 0.
Beide Formen sind reell, nichtnegativ und invariant unter einer gemeinsamen
globalen Phase. Diese Eigenschaften lösen die relative Vorzeichenwahl nicht.

Ein unitärer Wechsel, der das Atom mit −1 multipliziert, bildet die beiden
Formen ineinander ab. Wenn **auch** Ziel, Zustände und Instrument mitgeführt
werden, ist dies nur ein Darstellungswechsel. Der Gegenvergleich hält den
deklarierten Zielprojektor fest; er behauptet keine Ungleichwertigkeit korrekt
transportierter Beschreibungen.

Eine explizite untere Lückenschranke lässt sich ohne Spektralnumerik gewinnen.
Für (a,f)⊥ψ_s setze b=sa und m=∫f=−b. Dann gilt

\[
 |f(0)-m|\le\|f'\|/\sqrt3,\qquad
 2|b|^2\le|b-f(0)|^2+\tfrac13\|f'\|^2.
\]

Ferner folgt direkt aus Cauchy-Schwarz und der Doppelintegralidentität

\[
 \|f-m\|^2=\tfrac12\iint|f(x)-f(y)|^2dxdy
 \le\tfrac16\|f'\|^2.
\]

Damit

\[
 \|(a,f)\|^2=2|b|^2+\|f-m\|^2
 \le|a-sf(0)|^2+\tfrac12\|f'\|^2,
 \qquad \boxed{\Delta_w\ge\min(\lambda,2\kappa)>0.}
\]

Die Einbettung C⊕H¹→C⊕L² ist kompakt. A_s hat daher kompakten Resolventen;
die Lücke gehört zum wohldefinierten Zusatzmodell. Die Schranke ist nicht
als optimal behauptet. Eine Grundzustandsprojektion ist weder automatisch
ein verfügbarer Detektor noch eine Präparation: Unitarität allein führt
einen beliebigen Anfangszustand nicht in diesen Grundzustand.

## 6. Unbeschränkte Randkopplung: keine falsche Übernahme des Normbudgets

Die neue Form liegt nicht ohne Weiteres in der beschränkten V-Klasse aus
PR 262. Der Spurwert f(0) ist bezüglich der L²-Norm unbeschränkt. Zum Beispiel
hat ein glatter, nahe null konzentrierter Hügel f_ε(w)=ε^(−1/4)χ(w/ε),
χ(0)=1, eine gegen null gehende L²-Norm, während |f_ε(0)|² divergiert.
Für (0,f_ε) ist der Formunterschied zu λ=0 deshalb nicht durch eine
Konstante mal ||(0,f_ε)||² beschränkt. Auch die Operatordomänen ändern sich.

Somit darf γ=∫||V||dt/ℏ aus dem beschränkten Vorgänger nicht einfach mit
λ eingesetzt werden. Die Selbstadjungiertheit ist hier durch die Form
kontrolliert; ein endliches zeitabhängiges Betriebsfehlerbudget wäre eine
weitere Aufgabe.

Die endlichen Kontrollmatrizen illustrieren genau diese Trennung. Mit m
stetigen Zellen und Gewichtsmatrix G_m=diag(1,1/m,…,1/m) sei

\[
 q_{m,s}=\kappa m\sum_{j=1}^{m-1}|f_{j+1}-f_j|^2+
             \lambda|a-sf_1|^2,\qquad H_{m,s}=G_m^{-1}L_{m,s}.
\]

Die Differenz H_λ−H_0 hat im gewichteten Raum Norm λ(m+1); ihr rein
außerblockdiagonaler Anteil hat Norm λ√m. Beide Aussagen folgen aus dem
entsprechenden Rang-eins- beziehungsweise Zweiblockquadrat. Bei festem λ>0
wachsen sie mit m. Dies ist weder ein physikalischer Divergenznachweis noch
ein Beweis fehlender Selbstadjungiertheit des kontinuierlichen Modells.
Die Matrizen dienen als endliche Analoga; in diesem Paket wird keine
Konvergenz ihrer Propagatoren oder Spektralfehler zertifiziert.

## 7. Die Uhrvariable ist keine harmlose Zusatzdimension

Zurück im vollständigen n=1-Raum gilt
H=L²((0,1)_x)⊗H_w. Ein alleiniger Dichteoperator I_x⊗A_+ besitzt den Kern

\[
 L^2((0,1)_x)\otimes\operatorname{span}\{\psi_+\}.
\]

Sein Grundraumprojektor ist I_x⊗P_w, aber der bisherige Zielprojektor ist
P_x⊗P_w, wobei P_x auf die konstante normierte Uhrmode projiziert. Ihr
Abstand ist eins: (I_x−P_x)⊗P_w ist ein nichtverschwindender Projektor.
Ein normiertes Uhrprofil orthogonal zur Konstanten liefert beim ersten Effekt
Erfolg eins und beim zweiten null. Die Einbettungsfalle aus PR 262 besteht
hier im vollständigen kontinuierlichen Raum, nicht nur in einem 3×3-Beispiel.

Eine **weitere Zusatzwahl** A_x=−κ_x∂²_x mit Neumann-Rändern und κ_x>0
führt zur selbstadjungierten positiven Tensor-Formsumme

\[
 A_{\rm full}=A_x\otimes I+I\otimes A_+.
\]

Sie hat den gewünschten eindimensionalen konstanten Grundraum und eine
Lücke mindestens min(π²κ_x,λ,2κ). Dies folgt aus dem Neumann-Spektrum in x
und der zuvor bewiesenen Dichtelücke. Die Wahl einer Ableitung nach dem
historischen Uhrrecord x ist selbst keine Ableitung einer physikalischen
CST-Zeitentwicklung. Auch hier ist die Konstruktion diagnostisch, nicht
die gesuchte Dynamik oder Detektorrealisierung.

## 8. Rückbindung an die geerbte Wirkung: ein exakter Residualtest

Es wäre unzulässig, S_d ohne weitere Begründung einen Hamiltonoperator zu
nennen: Wirkung und Energie sowie historische Uhr und Kontrollzeit sind
verschiedene Begriffe. Prüfen lässt sich aber der ausdrücklich zusätzliche
dimensionslose Ansatz

\[
 H_\eta=A_{\rm full}+\eta M_{S_d}.
\]

M_S ist für festes h beschränkt und reell, also ist diese Störung auf
D(A_full) selbstadjungiert und nach unten beschränkt. Sie identifiziert
keine physikalische Umrechnung von Wirkung in Energie. Der bisherige
normierte Zielvektor ψ ist konstant und A_fullψ=0. Daher

\[
 \|(I-P_+)H_\eta\psi\|^2
 =\eta^2\{\langle S_d^2\rangle_\nu-\langle S_d\rangle_\nu^2\}.
\]

Aus dem Atom-/Gleichmaß folgen exakt

\[
 \langle S_d\rangle=-\tfrac18-\tfrac{h^2}{3},\qquad
 \langle S_d^2\rangle=\tfrac1{24}+\tfrac{2h^2}{9}+\tfrac{8h^4}{15},
\]
\[
 \boxed{\operatorname{Var}_\nu(S_d)
 =\tfrac5{192}+\tfrac{5h^2}{36}+\tfrac{19h^4}{45}>0.}
\]

Bei η≠0 ist der konstante Zielvektor somit kein Eigenzustand dieses
Zusatz-Hamiltonoperators. Das ist ein exakter Eigenvektor-Residualtest,
keine Fehlerschätzung für einen experimentellen Detektor und kein Verbot
anderer Messungen. Ein geeignetes Gegenpotential könnte den Zielvektor
erneut erzwingen, wäre aber wiederum zu begründen und nicht aus dem
gewünschten Ergebnis auszuwählen.

## 9. Exakte Kontrollen und verbleibende physikalische Entscheidung

Der Plan wurde nach der analytischen Herleitung und vor den endlichen
Kontrollrechnungen eingefroren. Die Python-Standardbibliothek genügt.

| Kontrolle | Umfang | Bedeutung |
|---|---:|---|
| Blockerhaltende Effekte | 36 | Gleiche Antworten auf beide Vorzeichen; scharfe Grenze |
| Gewichtete Randmatrizen | 72 | Formpositivität, Nullräume, Domänenanalogon und Normskalierung |
| Rationale Cayley-Abbildungen | 72 | Exakte gewichtete Unitarität; 54 gekoppelte Fälle mit Kreuzkohärenz |
| Green-Identitäten auf Polynomen | 216 | Randvorzeichen und Operator/Form-Übereinstimmung |
| Wahrscheinlichkeitsbilanzen | 72 | Atomverlust plus kontinuierlicher Zufluss exakt null |
| Zusätzliche Uhrmoden | 6 | Degeneration und Komplementfehler eins |
| Geerbte n=1-Wirkung | 45 Punkte | Unabhängige Ankerform gegen Polynom |
| Wirkungs-/Eigenresiduen | 9 | Exakte Momentformel; Nichtstationarität bei η≠0 |
| Negativkontrollen | 7 | Erwartete Fehlbehauptungen zurückgewiesen |

Eine Cayley-Abbildung (I−itH/2)(I+itH/2)^(−1) ist ein genau unitärer
**Kontrolloperator**, nicht die exakt ausgewertete Zeitentwicklung exp(−itH).
Die kontinuierlichen Sätze beruhen auf den obigen Beweisen, nicht auf
einer Extrapolation der kleinen Gitter. Vier wissenschaftliche Dateien
werden isoliert bytegleich reproduziert. Das ist keine externe Replikation
oder formale Beweisassistentenprüfung.

Die physikalische Entscheidung ist jetzt konkreter: Die Theorie muss zuerst
festlegen, ob das Dichte-Nullatom und der positive Dichtesektor im physikalischen
Zustandsraum überlagert und durch zulässige Operationen verbunden werden können.
Falls eine echte Superselektion besteht, ist der vorliegende Rang-eins-
Zielvertrag auf diesem physikalischen Raum zu ändern; ein Detektor darf eine
solche Superselektion nicht bloß als Modellannahme verletzen. Falls Übergänge
zulässig sind, müssen Quantenalgebra, Domäne, Kopplung und ihre kausale Bedeutung
aus einem begründeten Materie-/Randmodell hervorgehen. Danach sind Auslese,
Präparation, Betrieb und Rückwirkung zu qualifizieren.

Die zusätzliche Familie q_s ist als **mathematisch konsistent, physikalisch
nicht ausgewählt** eingestuft. Weitere n=5-Feldintegrale können diese
Definitionslücke nicht entscheiden. MODEL, CURRENT, CORRESPONDENCE, BOUNCE,
REGULARITY, BOUNDARY, TRAPPING und EXTENSION bleiben HOLD.

## Quellen und Abgrenzung

- Projektbasis: [PR 262](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/262).
  Die gepinnten Materie- und Variationsherleitungen liefern S_d und den
  Unterschied zwischen offenem Stratum, Atom und Variationsstrom.
- Gerald Teschl, *Mathematical Methods in Quantum Mechanics*, zweite Auflage,
  §2.3, Satz 2.14: https://radon.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe2.pdf .
  Verwendet wird der Darstellungssatz für dicht definierte abgeschlossene
  halbbeschränkte Formen. Die spezielle Randform, ihre Domäne und die
  Abschätzungen werden hier separat hergeleitet.
- Steven Johnston, *Feynman Propagator for a Free Scalar Field on a Causal Set*,
  https://arxiv.org/abs/0909.0944 . Ein feldtheoretischer Quantisierungspfad
  auf einem Kausalset; keine Herleitung der hiesigen Staub-Historienkopplung.
- Emma Albertini, Fay Dowker, Arad Nasiri, Stav Zalel, *In-in correlators and
  scattering amplitudes on a causal set*, §2.2,
  https://arxiv.org/html/2402.08555v2 . Die dortige Konstruktion startet von
  einem retardierten Propagator und einer Feldoperatoralgebra. Sie darf nicht
  mit dem hier benutzten Multiplikationsraum vollständiger Staubhistorien
  gleichgesetzt werden. Eine Abbildung zwischen diesen Modellen ist offen.

Die Quellen wurden am 7. November 2026 geprüft. Externe Volltexte werden nicht
verteilt. Es wird weder eine vollständige Literaturübersicht noch Neuheit
der verwendeten allgemeinen Operatorargumente beansprucht.
