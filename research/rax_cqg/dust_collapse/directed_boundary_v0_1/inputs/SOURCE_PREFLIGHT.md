# CST-DUST Materieblöcke: Randvertrag, Schur- und Paritätsprüfung v0.1

Stand: 11. November 2026. Anschluss an PR #277 und die vorherigen Randkern-/Zustandsraumpakete. **PREPARATION_ONLY; physikalische 8×8-Matrix NOT_CONSTRUCTED; alle acht physikalischen Gates HOLD.**

Der Entwurf benennt den richtigen Engpass: Eine gemeinsame Wirkung muss tatsächlich zwischen wohldefinierten Randzuständen ausgewertet werden. Er enthält jedoch noch Voraussetzungen, die nicht aus den bisherigen Artefakten folgen. Diese Fassung korrigiert sie und liefert 25 exakte endliche Kontrollen. Sie gibt keine frei gewählten Zahlen als echte Materieblöcke aus.

## 1. Datenanschluss vor einer neuen Matrix

Der vorhandene Geometriekern zählt Verklebungen zweier induzierter Teilordnungen. Seine Indizes sind nicht bereits Anfangs- und Endzustände einer Zeitentwicklung. Die Zweierkette K ist zudem keine Antikette und damit nicht ohne weitere Konstruktion ein raumartiger Cauchyrand.

Eine erneute vollständige Enumeration der 219 gelabelten Viererordnungen bestätigt:

| Geometrieklassen | ursprüngliche Verklebungsfaser | zusätzliche Einschränkung: keine Relation rechts → links |
|---|---:|---:|
| AA | 35 | 16 |
| AK | 26 | 9 |
| KA | 26 | 9 |
| KK | 20 | 6 |

Die rechte Spalte ist eine **diagnostische Zusatzwahl**, keine neue physikalische Amplitude. Sie erlaubt auch fehlende Kreuzrelationen. Unabhängig erhält man 16=2⁴, 9=3² und 6=binom(4,2). Ihre Laurent-Polynome unterscheiden sich bereits von den Ausgangspolynomen; alle Ordnungs-IDs stehen in results/geometry_carrier_audit.json.

Wenn beide Zweierblöcke vollständig zu Randvariablen erklärt werden, besitzen diese Viererordnungen keine übrigen inneren Feldvariablen. Dann ist der Schurschritt leer, der innere Determinantenfaktor eins. Eine nichttriviale innere Elimination verlangt einen anderen Träger oder eine andere Randzuordnung. Der vorhandene Fünferketten-Schurfall der Staubuhr ist davon verschieden.

Die veröffentlichte stratumweise Planungsreihenfolge bleibt:

$$
(A,0,0_m),(A,0,1_m),(K,0,0_m),(K,0,1_m),
(A,+,0_m),(A,+,1_m),(K,+,0_m),(K,+,1_m).
$$

Die geometrieweise Reihenfolge des neuen Entwurfs wäre zulässig, aber nur zusammen mit einer ausdrücklich gespeicherten Permutation aller Matrizen, Produkte und Zustandslabels. Keine der beiden Reihenfolgen erzeugt die noch fehlenden Zustände.

## 2. Staubuhr und zusätzliches skalares Feld trennen

Die geerbte gemeinsame Amplitude enthält Geometrie C, Uhr T und Dichtegewicht w. Ihre Wirkung lautet

$$
S_d=-\frac12\sum_xw_x-\frac14\sum_{y\prec x}w_x B_{xy}(T_x-T_y)^2
=-\frac12T^{\mathsf T}LT-\frac12\sum_xw_x.
$$

Das ist ein deklarierter regulierter Kandidat; L ist eine im Allgemeinen indefinite Staubuhr-Hesse-Struktur. Ein weiteres reelles Feld Φ ist eine **Modellerweiterung**, solange seine Beziehung zu T,w nicht hergeleitet ist. Dessen Wirkung, Kopplung, Einheiten, Maß und Randzustände fehlen noch als gemeinsame Definition.

Für ein reelles kommutierendes Feld ist der relevante quadratische Ausdruck

$$
S_\Phi=\frac12\Phi^{\mathsf T}H_C(T,w)\Phi,\qquad H_C=H_C^{\mathsf T}.
$$

Ein retardierter d'Alembertoperator ist im Allgemeinen nicht diese symmetrische Hesse-Matrix. Für eine beliebige reelle Matrix D gilt exakt

$$
\nabla_\Phi\!\left(\tfrac12\Phi^{\mathsf T}D\Phi\right)
=\tfrac12(D+D^{\mathsf T})\Phi.
$$

Wird ein Operator mit einem Feldmaß W in eine Wirkung eingesetzt, muss entsprechend die Symmetrie des resultierenden gewichteten Bilinearforms erklärt werden. Eine Symmetrisierung ist eine ausgewiesene Wirkungsentscheidung; sie bewahrt nicht automatisch die ursprüngliche retardierte Feldgleichung. Vorzeichen, Massenterm und Randterme werden hier nicht nachträglich ausgewählt.

Die Literatur zu GCB-Operatoren belegt deren retardierten, nichtlokalen Charakter [L1]. Sie qualifiziert keine hier noch fehlende zusätzliche Materiewirkung. Historiendefinitionen und Sorkin-Johnston-Zustände sind mögliche, getrennt zu begründende Konstruktionen [L2,L3].

## 3. Schurkomplement: stationär, reguliert oder distributionell

Bei festem C,T,w, reell-symmetrischem H und der Zerlegung in äußere Feldwerte b und innere Werte q gilt

$$
S_\Phi(b,q)=\tfrac12 b^{\mathsf T}H_{bb}b+q^{\mathsf T}H_{Ib}b
+\tfrac12q^{\mathsf T}H_{II}q.
$$

Ist H_II invertierbar, folgen

$$
q_*=-H_{II}^{-1}H_{Ib}b,\qquad
H_{\rm eff}=H_{bb}-H_{bI}H_{II}^{-1}H_{Ib}.
$$

Das ist eine exakte stationäre Substitution. Für ein Integral über einen kompakten Bereich führt die Verschiebung q→q−q_* zu einem b-abhängigen verschobenen Integrationsgebiet. Deshalb ist ein kompakter Kern im Allgemeinen **nicht** nur ein konstanter Determinantenfaktor mal exp(i bᵀH_eff b/(2ℏ)). Der bisherige Uhrregulator darf nicht still in eine Integration über die gesamte reelle Achse geändert werden.

Für volle reelle Achsen, Lebesgue-Maß, ℏ>0, eine invertierbare reell-symmetrische Hesse-Matrix und festgelegte Abel-Dämpfung gilt dagegen

$$
\int_{\mathbb R^r}d^rq\,
e^{\frac{i}{\hbar}(\frac12q^{\mathsf T}Hq+j^{\mathsf T}q)}
=(2\pi\hbar)^{r/2}\frac{e^{i\pi\,{\rm sgn}(H)/4}}{\sqrt{|\det H|}}\,
e^{-ij^{\mathsf T}H^{-1}j/(2\hbar)}.
$$

Ein Maßfaktor multipliziert diese Formel zusätzlich. Die Signaturphase ist hier bereits enthalten. Wenn stattdessen n_- negative Eigenwerte verwendet werden, lautet dieselbe Phase e^{iπr/4}e^{-iπn_-/2}; sie darf nicht zusätzlich zu einer bereits phasenbehafteten Determinantenwurzel erneut gezählt werden. Signatur, Morse-Index und Maslov-Index sind ohne präzise Konvention keine austauschbaren Symbole.

Bei Nullrichtungen N gilt als stationäre Verträglichkeitsbedingung

$$
N^{\mathsf T}H_{Ib}b=0.
$$

Die Pseudoinverse allein behandelt die Integration nicht. Auf unbeschränkten Nullachsen entsteht distributionell ein Faktor (2πℏ)^k δ(Nᵀj), bei verschwindender Quelle formal ein unendliches Volumen. Auf kompakten Nullachsen entsteht ein endlicher Fourier-/Volumenfaktor. Ein Quotient ist nur nach Begründung einer Eichsymmetrie samt Maß zulässig. Nicht jede Nullrichtung ist Eichung.

Die Tests prüfen stationäre Substitution, Determinanten- und Signaturidentität, den leeren Innenraum, kompatible und inkompatible singuläre Fälle sowie die Fresnelphase. Die kleinen Testmatrizen sind ausdrücklich mathematische Kontrollen.

## 4. Eigenvektor ist nicht Besetzungszustand

Das verallgemeinerte Problem H_eff v_k=λ_k W_b v_k mit W_b>0 kann unter passenden Symmetriebedingungen eine Basis von **Feldprofilen auf den Randelementen** liefern. Ein Profil v_k ist ein Vektor im endlichdimensionalen Konfigurationsraum. Eine Randwellenfunktion Ψ_n[φ] ist dagegen eine Funktion dieses Konfigurationsraums.

Ein Vakuum |0⟩, ein Einteilchenzustand |1⟩ und die zugehörige Oszillatorbreite benötigen zusätzlich eine begründete Quantisierung, eine positive Zustandswahl bzw. komplexe Struktur und die relevante kinetische/zeitliche Interpretation. Eine indefinite Raumzeit-Hesse-Matrix ist keine positive Oszillatorsteifigkeit. Modenindex k und Besetzungszahl n müssen getrennt werden.

Werden in einem Zweier-Randfeld zwei räumliche Moden jeweils auf die Besetzungen n_k=0,1 begrenzt, entstehen bereits vier Fockzustände pro Geometrie/Stratum, also 16 statt acht Gesamtzustände. Eine 8D-Wahl kann Vakuum plus genau eine ausgewählte Einteilchenanregung sein; sie braucht aber eine explizite Auswahl und eine Fehlerkontrolle.

Da der Schurblock beide äußeren Ränder eines ganzen Patches umfasst, liefert sein Spektrum nicht automatisch getrennte lokale Ein- und Ausgangsbasen. Auch eine Modenüberlappung ist erst definiert, wenn die zwei Feldräume samt Maßen durch eine Abbildung identifiziert sind. Ein Integral zweier Funktionen über unterschiedliche Konfigurationsräume hat ohne solche Abbildung keine Bedeutung.

## 5. Der entscheidende neue Befund: bedingte Paritätsauswahl

Voraussetzungen: Die gemeinsame Wirkung, die zulässigen Geschichten, das Feldintegrationsgebiet und das Maß sind unter **gleichzeitiger** Spiegelung aller skalaren Feldwerte Φ→−Φ invariant. Es gibt keine ungerade Quelle oder asymmetrische Präparation. Die Randwellenfunktionen besitzen Paritäten p_i,p_f∈{+1,−1}. Die Dichtestrata 0,+ werden durch diese Feldspiegelung nicht vertauscht.

Dann liefert der Variablenwechsel im vollständigen projizierten Matrixelement

$$
B^{fi}_{s_fs_i}=p_fp_i\,B^{fi}_{s_fs_i}.
$$

Folglich

$$
p_fp_i=-1\quad\Longrightarrow\quad B^{fi}_{s_fs_i}=0.
$$

Das gilt vor und nach Summation über Geometrien und Integration über Staubvariablen, sofern die genannten Voraussetzungen erhalten bleiben. Ein Vakuum-zu-Einteilchen-Element ist daher in einer zentrierten quadratischen Feldtheorie **als allgemeiner Stratum-Mischungstest ungeeignet**. Beide gerichteten ungeraden Kandidaten können null sein, obwohl gerade Materieblöcke stark koppeln.

Es handelt sich um die Gesamtfeldparität. Ohne weitere Symmetrie gilt nicht die separate Erhaltung jeder einzelnen Modenparität. Bei asymmetrischen Randpaketen oder linearen Quellen gilt das Korollar nicht. Der tatsächliche physikalische Block bleibt NOT_COMPUTED, solange Wirkung und Randzustände nicht definiert sind.

Ein nichtverschwindender gerader Mischblock wäre zunächst Evidenz für eine Mischamplitude in der deklarierten endlichen Familie. Er wäre noch kein Nachweis, dass Materie diese Mischung vermittelt, kein Zeitübergang und kein Bounce. Für eine Zuschreibung an eine konkrete Materiekopplung braucht es einen aus derselben Wirkung definierten Entkopplungsvergleich mit identischen Randpräparationen und Maßen.

## 6. Korrigierte erste Zeugen

Nach Schließen der offenen Definitionen sind beispielsweise B_(A,0,vac);(A,+,vac) und B_(A,0,1);(A,+,1) paritätserlaubte erste Kandidaten. Zur Prüfung einer geraden Anregung kann B_(A,0,2);(A,+,vac) hinzukommen; dafür muss der Kontrollraum ausdrücklich über n=0,1 hinaus erweitert werden.

Die leere Historienfaser impliziert einen Nullblock. Eine nichtleere Faser garantiert keinen Nichtnullblock, weil Phasenauslöschung möglich bleibt. Numerisch klein ist nicht exakt null. Ein Nichtnull-Zeuge verlangt eine Fehlerumgebung, die den komplexen Ursprung ausschließt; ein allgemeines Nullresultat verlangt ein Symmetrie-/Trägerargument oder eine entsprechend starke exakte Rechnung.

Ein einzelnes Nullresultat beweist keine Superselektion. Dazu wäre zusätzlich die passende Sektorstruktur der gesamten qualifizierten Dynamik und Observablen nötig. Das Dichte-Nullatom ist weiterhin kein Materievakuum.

## 7. Gemeinsame Summe, Maß und Norm

Ein korrekt deklarierter kovarianter Ansatz hätte die Form

$$
B_{\beta\alpha}=\frac1{|G_{\rm fix}|}\sum_{C\in\Omega_{\rm lab}}
\int d\mu_C(T,w,\Phi)\,
\overline{F_\beta(b_f)}F_\alpha(b_i)
\exp\!\left[\frac{i}{\hbar}(S_g+S_d+S_\Phi+S_{\rm boundary})\right].
$$

F_α enthält die tatsächlichen Randpakete und Stratumträger. Diese Formel ist ein **Vertragstyp**, noch kein berechneter Datensatz. Die Feldintegration darf nur unter den Bedingungen aus Abschnitt 3 geschlossen ausgeführt werden; bei von T,w abhängiger Hesse-Matrix bleiben auch Schurblock, Determinante und Phase innerhalb der Staubintegrale.

Die gelabelte Summe mit 1/|G_fix| kann nach exakt begründeter Orbitabbildung durch markierte Stabilisatorgewichte ersetzt werden. Der Hilfsraumwert 1/(2^m|Aut(C,σ)|) enthält bereits den integrierten Dichte-Stratumfaktor und gilt für stratumskonstante Indikatoren der damaligen Hilfsfamilie. Ihn nochmals mit dem vollständigen Dichtemaß zu multiplizieren würde diesen Faktor doppelt zählen.

Für dν(w)=½δ_0+½1_(0,1)dw sind die Normen der konstanten Atom-/Positivindikatoren tatsächlich beide 1/2. Das ist kein allgemeines Normgesetz für echte Randpakete: Die positive Funktion f(w)=w besitzt etwa Normquadrat 1/6. W_b als diskretes Gewicht auf Feldprofilen ist außerdem nicht automatisch das Maß dμ_b(φ) für Wellenfunktionen.

Die Gram-Matrix muss aus denselben tatsächlichen Randzuständen und demselben positiven Randprodukt berechnet werden. Erst ihr Rang entscheidet über acht unabhängige Zustände.

## 8. Konvention, Verklebung, Trunkierung

Für Koeffizientenabbildungen A gilt Â=G_out^(1/2) A G_in^(-1/2). Für kovariante Matrixelemente B=G_out A gilt B̂=G_out^(-1/2) B G_in^(-1/2). Bei einem vollständigen gemeinsamen Zwischenraum lautet die kovariante Komposition

$$
B_{21}=B_2\,G_{\rm mid}^{-1}\,B_1,
$$

während Koeffizientenabbildungen als A_2 A_1 komponieren. In einer endlichen Trunkierung steht zwischen beiden Operatoren nur der Projektor auf den behaltenen Raum; eine Rest-/Leckagekontrolle ist erforderlich. Bei nichtlokaler Wirkung muss die Vollständigkeit des Randkragens selbst erst belegt werden.

Ein symmetrischer Wirkungskern erzwingt weder Unitarität noch die Reziprozität derselben orientierten Amplitude. Eine Adjungiertenrelation benötigt eine genau definierte Orientierungsumkehr, Randzustandsabbildung und komplexe Konjugation.

Eine praktische Modenkontrolle umfasst sowohl die Änderung der behaltenen Matrixelemente bei Vergrößerung des Kontrollraums als auch, für einen definierten Operator und normierte Einbettungen, die Größe ||(I−P_out) A P_in||. Für allgemeine Transferamplituden ist das nicht ohne Weiteres eine Verlustwahrscheinlichkeit.

Vier Geometriepaare × vier Stratumkombinationen × vier Ein-/Ausgangszustandspaare ergeben **64 komplexe Einträge je Phase**. Bei z=1,−1,i sind es **192**, vor zusätzlichen Parametergittern und Kontrollmoden.

## 9. Verbindlicher nächster Datensatz

open_inputs.json listet elf noch fehlende oder unqualifizierte Eingaben. Pro zugelassener Geschichte müssen Geometrie, kausale Matrix, Intervallzählung, volle Gravitation einschließlich Randkonvention, tatsächliche Feld-/Staubdaten, Rand- und Innenindizes sowie die maßbewahrende Gruppenwirkung erhalten bleiben.

Zusätzlich benötigt werden: Feld-Hesse-Matrix und ihre Herkunft; Integrationsdomäne und Regulator; Nullraumbehandlung; echte Randwellenfunktionen samt Zustand/Polarisation; positives Produkt; Kernkonvention; Paritätsprüfung; Determinantenphase; Trunkierungs-/Quadraturbudget; ein Entkopplungsvergleich für die behauptete Materievermittlung.

Ohne diese Eingaben wird keine numerische physikalische Matrix ausgegeben. Fehlende Werte bleiben unbekannt und werden nicht als Nullen gespeichert. Die vorhandene Pipeline liefert hier **Vorbereitung, exakte Trägerprüfung und einen bedingten Auswahlsatz**, keine abgeschlossene Extraktion echter CST-Materieblöcke.

## Quellen und Reproduktion

Die unveränderten Projektquellen sind in inputs/ enthalten und auf Main-Commit fdf1deb6ac071056d533a0937e21c238f42b2974 gepinnt. provenance.json enthält Originalpfade, Git-Blob-Hashes und SHA-256. Die Ursprungsartefakte unterscheiden bereits Staub-Schurantwort, zusätzliche Skalarfelder und fehlende Fockzustände.

- [L1] Aslanbeigi, Saravani, Sorkin: Generalized Causal Set d'Alembertians (2014), https://arxiv.org/abs/1403.1622.
- [L2] Sorkin: Scalar Field Theory on a Causal Set in Histories Form (2011, Fassung 2017), https://arxiv.org/abs/1107.0698.
- [L3] Nomaan X: Quantum Field Theory On Causal Sets (2023), https://arxiv.org/abs/2306.04800.

Die neuen Paritäts-, Maß- und Schurargumente sind im Text hergeleitet. Die Literatur wird nicht als Nachweis eines hier bereits konstruierten physikalischen Randprodukts verwendet.

    python analyze.py
    python verify.py

Der Prüfer kontrolliert Quellhashes und reproduziert beide Ergebnisdateien in einem frischen Verzeichnis bytegleich. Das PDF ist eine kompakte Lesefassung; diese Markdown-Datei enthält die vollständigen Definitionen.
