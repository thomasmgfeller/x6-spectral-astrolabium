# CST-DUST: kleiner Randzustandsraum v0.1

11. November 2026. Schritt 2 nach dem gemeinsamen Skalarwirkungsansatz
`CST-DUST-KG-MIN-v0.1`, PR #279, Main `91f46fe5f827f823c1c2a9e967c8bd031afb7f0d`.

**Ergebnis:** Ein expliziter, normierter kinematischer Testraum für A → A
mit einem inneren Element ist konstruiert. Der minimale gewählte Raum hat
Gram-Matrix I₄ und Rang 4 pro Rand. Eine aufgelöste Produktfamilie hat Gram-Matrix
I₆ und Rang 6. Nimmt man deren kohärente Zusammenfassung „+“ als zusätzliche
Zustände hinzu, entstehen acht benannte Vektoren, aber nur Rang 6.
Diese Zahlen folgen aus Integralen und exakten Gram-Matrizen. Sie sind keine
Dimensionsbestimmung des vollständigen physikalischen CST-Zustandsraums.

## 1. Anschluss, Geometrie und Felder

Unverändert gelten L={0,1}, I={2}, R={3,4}; L und R sind je eine Zweierantichain A.
Als bisherige Kontrollfamilie dienen die 33 abgedeckten AA-Ordnungen: Element 2
hat mindestens einen Vorgänger in L und einen Nachfolger in R; jedes äußere
Element ist mit mindestens einem Element des jeweils anderen Randes kausal
verbunden. Diese Familie ist weder ein vierdimensionales Ensemble noch ein
Beweis, dass der gewählte Kragen vollständige physikalische Cauchy-Daten trägt.
Die folgenden Randnormen hängen nicht von der Wahl einer einzelnen dieser
Historien ab. Das innere Element erhält keinen zusätzlichen Randindex.

Der Vorgänger trennt Staubuhr T, integriertes Staubdichtegewicht w=vρ und
zusätzliches reelles Skalarfeld Φ. Es gilt [T]=Länge, [w]=Wirkung,
[Φ]=√Wirkung/Länge. Der Atomsektor w=0 bedeutet Abwesenheit von Staub am
betreffenden Punkt. Er bedeutet weder Φ=0 noch skalares Vakuum.

Auf jedem Rand wählen wir gleiche positive Referenzskalen T_b, W und F und setzen
t_j=T_j/T_b, r_j=w_j/W, q_j=Φ_j/F. Der konkrete Kontrollpunkt ist
T_b=ℓ, W=ℏ, F=√ℏ/ℓ mit ℓ>0, ℏ>0. Breiten σ_s=σ_a=1 sind der Standard.
Alle Formeln gelten zusätzlich für beliebige gemeinsame positive endliche Breiten.
Die Festlegungen sind Präparations- und Regulatorkonventionen, keine aus der
Wirkung hergeleiteten physikalischen Skalen oder Vakua.

## 2. Gemeinsames Maß und Skalarprodukt

Für einen Randpunkt sei X=[−1,1] × ({0} ⊔ (0,1)) × ℝ mit

\[
d\lambda(t)=\tfrac12\mathbf1_{[-1,1]}dt,\qquad
d\nu(r)=\tfrac12\delta_0(dr)+\tfrac12\mathbf1_{(0,1)}dr,\qquad dq.
\]

Der disjunkte Dichteträger ist maßtheoretisch wesentlich: Das Atom hat Masse 1/2;
es wird nicht als Nullpunkt der stetigen Quadratur behandelt. Für zwei Punkte:

\[
d\mu_{\rm lab}=\prod_{j=1}^2d\lambda(t_j)d\nu(r_j)dq_j,
\qquad
\langle\Psi,\Xi\rangle_A=\tfrac12\int_{X^2}\overline\Psi\,\Xi\,d\mu_{\rm lab}.
\]

Die Antichainpunkte sind hier nicht physikalisch unterscheidbar markiert.
Ihre gesamte Ausstattung (t,r,q) wird gemeinsam vertauscht. Definiere
H_A als den S₂-invarianten Teil dieses L²-Raums. P_A=(1+U_swap)/2 ist der
orthogonale Projektor. Der Faktor 1/2 im Skalarprodukt entspricht der Division
des gelabelten Maßes durch |S₂|. Er wird nicht nochmals pro Zustand eingefügt.
Äquivalent kann auf dem Quotienten mit dem Pushforward-Maß integriert werden.

Beim isolierten diskreten Dichtemuster ergeben sich Quotientmassen 1/8 für 00,
1/4 für den Orbit {10,01} und 1/8 für 11. Das ist 1/(2² |Stab(mask)|).
Die stetigen Felder werden dabei weiterhin mittransformiert; deren allgemeine
Stabilisatoren werden nicht mit den reinen Maskenstabilisatoren gleichgesetzt.
Das Randmaß ersetzt kein noch fehlendes physikalisches Historienmaß.

Alle Uhrpakete sind χ(t₁,t₂)=1 auf der Box. Ihr Integral über dλ₁dλ₂ ist 1.
Auch an Atomstellen bleiben die Hilfsuhren erhalten: In der gerichteten
Staubwirkung können ihre Werte an späteres positives w koppeln. Sie zu entfernen
wäre eine weitere Reduktion. Ein globaler Uhrtranslationsquotient und eine
physikalische Entparametrisierung werden hier nicht postuliert.
Die konstanten Boxpakete sind L²-Zustände; damit ist kein Definitionsbereich
eines Uhr-Hamiltonoperators oder einer Impulsableitung qualifiziert.

## 3. Dichtestrata und die genaue Bedeutung von „+“

Eine 1 im Maskennamen bedeutet 0<r<1, eine 0 das Atom. Die Maskenreihenfolge
ist 00,10,01,11. Für das gelabelte Dichtemaß haben alle vier Masken Gewicht 1/4.

| Name | Belegungen | Normiertes Dichtepaket im gelabelten Maß |
|---|---|---|
| 0 | 00 | d₀=2 1₀₀ |
| M | 10 und 01 | d_M=√2(1₁₀+1₀₁) |
| D | 11 | d_D=2 1₁₁ |
| + | 10, 01 und 11 | d₊=(2/√3)(1₁₀+1₀₁+1₁₁) |

Die Pakete sind innerhalb jeder positiven Dichteachse konstant. Die Mengen
M und D sind verschieden; M enthält genau einen positiven Punkt und D zwei.
„+“ bedeutet in diesem Vertrag **mindestens ein positiver Randpunkt**.
Es ist kein Synonym für „beide positiv“ und keine neue vierte disjunkte Maske.

\[
d_+=\sqrt{\frac23}\,d_M+\frac1{\sqrt3}\,d_D.
\]

Hier ist „+“ ein reiner kohärenter Zustand mit relativer Phase null.
Die Maskenwahrscheinlichkeiten darin sind jeweils 1/3, die Orbitgewichte
2/3 für M und 1/3 für D. Der gleiche klassische Maskenbefund könnte auch
aus der gemischten Dichtematrix (2/3)|M⟩⟨M|+(1/3)|D⟩⟨D| entstehen.
Diese hat Reinheit 5/9, während |+⟩⟨+| Reinheit 1 und Nebendiagonale √2/3
in der M,D-Basis besitzt. Die Präparation dieser Kohärenz ist nicht hergeleitet.
Eine angenommene Superselektion würde einen anderen Zustandsvertrag erfordern.

## 4. Skalarpakete, Vertauschung und Parität

Mit q_s=(q₁+q₂)/√2, q_a=(q₁−q₂)/√2 ist der Jacobi-Betrag 1. Setze

\[
h_0(q)=\frac{1}{\sqrt{\pi\sigma_s\sigma_a}}
\exp\!\left[-\frac12\left(\frac{q_s^2}{\sigma_s^2}
+\frac{q_a^2}{\sigma_a^2}\right)\right],\qquad
h_1(q)=\sqrt2\frac{q_s}{\sigma_s}h_0(q).
\]

Direkte Integration liefert ∫|h₀|²d²q=∫|h₁|²d²q=1 und ∫h₀h₁d²q=0.
Verwendet werden ∫e^(−x²)dx=√π, ∫x e^(−x²)dx=0 und
∫x²e^(−x²)dx=√π/2. Das sind die ersten beiden normierten Hermite-Gaußpakete
in einer gewählten symmetrischen Richtung; die zweite Richtung bleibt im
Grundpaket. Standardorthogonalität: NIST DLMF §18.3, https://dlmf.nist.gov/18.3.
Eine energetische Teilchen- oder Vakuuminterpretation wird nicht behauptet.

Vertauschung lässt q_s fest und kehrt q_a um. Beide gewählten Pakete sind
deshalb S₂-invariant. Unter Gesamtfeldumkehr q→−q hat h_n Parität (−1)^n.
Das antisymmetrische Einzelpaket h_a=√2 q_a h₀/σ_a würde bei symmetrischer
Dichte durch P_A auf null projiziert. Es darf dann nicht als normierter
zusätzlicher Zustand gezählt werden. Dagegen ist die Korrelation
2(1₁₀−1₀₁)h_a insgesamt vertauschungsinvariant, normiert im Quotientmaß
und orthogonal zu den hier gewählten Produktpaketen. Auch sie bleibt außerhalb
des kleinen Versuchsraums. Diese Kontrolle verhindert eine falsche
Vollständigkeitsbehauptung selbst bei Betrachtung niedriger skalarer Moden.

## 5. Normierte Zustände und tatsächlich berechnete Gram-Matrizen

Definiere für s∈{0,M,D,+}, n∈{0,1}

\[
\Psi_{s,n}=\sqrt2\,\chi\,d_s\,h_n.
\]

Der vordere Faktor √2 kompensiert genau den Quotientfaktor 1/2. Damit
G_(s,n),(s',m)=⟨Ψ_(s,n),Ψ_(s',m)⟩_A=⟨d_s,d_s'⟩_ν δ_nm.
Die Normierung wurde also mit demselben Maß wie das Skalarprodukt vorgenommen.

**Primärer kleiner Versuch:** Reihenfolge (0,0),(0,1),(+,0),(+,1).
Direkte Integration ergibt G_min=I₄ und Rang 4. Das sind vier unabhängige
Zustände pro Rand, nicht acht durch getrennte Benennung von Ein- und Ausgang.
Ein- und Ausgang sind isomorphe Kopien; ihre direkte Summe hätte als bloße
Buchhaltung Dimension 8, die Übergangsmatrix zwischen ihnen aber Größe 4×4.

**Aufgelöste Kontrolle:** Reihenfolge (0,0),(0,1),(M,0),(M,1),(D,0),(D,1).
Es folgt G_res=I₆ und Rang 6 innerhalb dieser deklarierten Produktfamilie.

**Redundanzprüfung:** Werden alle acht Vektoren in der Reihenfolge
(0,0),(0,1),(M,0),(M,1),(D,0),(D,1),(+,0),(+,1) aufgenommen, gilt

\[
G_{\rm red}=\begin{pmatrix}
1&0&0&0\\
0&1&0&\sqrt{2/3}\\
0&0&1&1/\sqrt3\\
0&\sqrt{2/3}&1/\sqrt3&1
\end{pmatrix}\otimes I_2.
\]

Das Spektrum ist {0,0,1,1,1,1,2,2}; Rang 6. Für jedes n gilt die exakte
Nullrelation Ψ_(+,n)−√(2/3)Ψ_(M,n)−Ψ_(D,n)/√3=0.
Die zwei unabhängigen vom Primärraum ausgelassenen Dichterichtungen lauten
Ψ_(Δ,n)=Ψ_(M,n)/√3−√(2/3)Ψ_(D,n), n=0,1. Sie sind orthogonal zum Primärraum.
Eine Zusammenfassung nach „+“ verliert also Zustandsrichtungen; sie beseitigt
sie nicht durch eine physikalische Zwangsbedingung.

H_A selbst ist unendlichdimensional. Insbesondere existieren weitere Uhr-,
Dichte- und skalare Paketformen. Ein Rang gilt immer nur für die geprüfte
Familie und das deklarierte Skalarprodukt. Sektororthogonalität beweist
weder Superselektion noch dynamisch verschwindende 0↔+-Übergänge.

## 6. Ein- und Ausgang vergleichen; Maße korrekt transportieren

Die Randidentifikation ordnet die beiden unmarkierten Antichains einander zu.
Beide möglichen Bijektionen wirken auf den gewählten invarianten Paketen gleich.
Gemeinsame Skalen, Breiten, Uhrpakete und Dichtemasken machen diese Identifikation
unitär. Unter ihr sind die vier Eingangspakete dieselben vier Funktionen wie
die Ausgangspakete; der Kreuzüberlapp ist I₄. Matrixzeilen sind ausgehend,
Matrixspalten eingehend, wie im bestehenden Basisvertrag.

Bei absichtlich verschiedenen skalaren Breiten bleibt jeder Rand intern
normiert, aber der Kreuzüberlapp ist nicht automatisch I. Mit
R_s=2σ_s^in σ_s^out/((σ_s^in)²+(σ_s^out)²) und analog R_a erhält man
S₀₀=√(R_s R_a), S₁₁=R_s√(R_s R_a), S₀₁=S₁₀=0.
Beispiel: (σ_s^in,σ_s^out)=(1,2), σ_a=1 gibt 2/√5 bzw. 8/(5√5).
Ein solcher Überlapp ist kein Übergangskern der Dynamik.

Bei dμ'=r dμ mit r>0 werden Zustände durch Ψ'=r^(−1/2)Ψ transportiert.
Soll derselbe Integraloperator dargestellt werden, muss sein Kern zugleich
K'(y,x)=r_out(y)^(−1/2)K(y,x)r_in(x)^(−1/2) erhalten. Ein bloßer Maßwechsel
bei unveränderten Funktionen verändert dagegen Normen und Matrixelemente.
Insbesondere entfällt bei Wechsel zum gelabelten Maß der Faktor √2 in Ψ;
der zugehörige Zweirand-Kern skaliert um 1/2. Randquotient, volle
Historienautomorphismen und ein späteres Verklebungsmaß sind getrennt zu prüfen.

Für das dimensionale Skalarmaß dΦ₁dΦ₂ lautet das normierte Feldpaket
ψ_Φ(Φ)=F^(−1)h(Φ/F). Der Gaußadapter kann direkt in q arbeiten:
H_q=F²H_Φ und Ω_q=ℏ diag(σ_s^(−2),σ_a^(−2)) in (q_s,q_a), anschließend
mit derselben orthogonalen Transformation in (q₁,q₂). Die Breitenmatrix
im Gaußexponenten exp(−qᵀΩ_q q/(2ℏ)) darf nicht mit H_q verwechselt werden.

## 7. Anschluss des inneren Elements und spätere Projektion

Bei einer festen Kontrollhistorie definieren wir den inneren Kandidatenfaktor

\[
d\mu_{I,\epsilon}=d\lambda(t_2)d\nu(r_2)dq_2\,
e^{-\epsilon q_2^2/2},\qquad \epsilon>0.
\]

Uhr- und Dichteintegration bleiben kompakt; der zusätzliche Skalarregulator
wird nicht als physikalischer Zustand oder Wahrscheinlichkeit normalisiert.
Der innere Punkt besitzt keine nichttriviale Permutationsgruppe. Eingesetzt
werden T=T_b t, w=W r und Φ=F q in die unveränderte gemeinsame Wirkung.
Für festes ℓ>0 ist der innere Skalarblock aller 33 bekannten AA-Kontrollen
invertierbar; der Vorgänger beweist |H_II|≥v(a+μ²)>0. Diese endliche Schranke
und der Abel/Fresnel-Anschluss ersetzen keinen gleichmäßigen
Kontinuumsgrenzwert oder eine physikalische Kernnormierung.

Ein später festzulegender Kern K_ε liefert die Matrix

\[
M_{\alpha\beta}(\epsilon)=\int d\mu_A(b_{out})d\mu_A(b_{in})\,
\overline{\Psi_\alpha(b_{out})}K_\epsilon(b_{out},b_{in})
\Psi_\beta(b_{in}).
\]

Das fixiert Orientierung, Konjugation und Randnormierung. In diesem Schritt
wird kein physikalischer Kern K, kein Historiengewicht und kein M₀₊ berechnet.
Ein Skalarprodukt auf Randfunktionen ist auch keine aus der Amplitude
abgeleitete physikalische Norm. Nach einem begründeten Constraint-/Rigging-Verfahren
kann eine andere Gram-Matrix einschließlich zusätzlicher Nullrichtungen entstehen.

## 8. Prüfungen, Grenzen und nächster Anschluss

20 automatisierte Kontrollen bestehen. Dazu gehören direkte Gaußintegrale,
Atom- und Orbitgewichte, Projektorinvarianz, Labelduplikate, exakte Ränge und
Nullrelationen, die vom Viererraum ausgelassenen Richtungen, kohärenter Zustand
gegen Mischung, Parität und Vergleich unterschiedlicher Breiten. Die Ergebnisse
stehen exakt in `results/gram_matrices.json`; `verify.py` kontrolliert zusätzlich
Paket-Hashes, die mitgeführten Git-Blobs und bytegleichen Ergebnis-Replay.

Die vier normierten Zustände sind ein nachprüfbares Ergebnis für einen
deklarierten kinematischen Kandidaten. Ihre Präparation, das physikalische
Skalarprodukt, das Historienmaß, die gravitative Randwirkung und die
Trunkierungsfehler sind weiter offen. Alle acht physikalischen Gates bleiben
HOLD; `physical_kernel=NOT_CONSTRUCTED`, `physical_K_0plus=NOT_COMPUTED`.

Der nächste konkrete Rechenschritt ist die regulierte Projektion der bekannten
AA-Kandidatenwirkung auf diese vier Pakete, mit zusätzlich festgelegtem
Historiengewicht und Kernvorfaktor. Dabei sind mindestens die zwei Δ-Richtungen
und höhere skalare Besetzungen als Austrittskanäle zu prüfen. Ein positiver
Gram-Rang allein beweist weder dynamische Geschlossenheit noch Unitarität,
Rückwirkung, Junction-Physik, Bounce oder Singularitätsauflösung.

## Quellen und Herkunft

- Repository-Vorgänger PR #279 und commitfixierte Eingaben in `provenance.json`:
  https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/279
- Gerichteter Randvertrag PR #278: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/278
- NIST DLMF §18.3, Hermite-Orthogonalität: https://dlmf.nist.gov/18.3
- Benincasa/Dowker, *The Scalar Curvature of a Causal Set*, arXiv:1001.2725v4:
  https://arxiv.org/abs/1001.2725v4. Herkunft des BD-Operatorprogramms, keine
  Begründung des hier gewählten Randmaßes oder physikalischen Zustandsraums.

Die neue Randkonstruktion und ihre Rangberechnungen sind eigene algebraische
Ableitungen unter den offen aufgeführten Modellentscheidungen. Externe
Literatur wird nicht als Beweis für diese Entscheidungen ausgegeben.
