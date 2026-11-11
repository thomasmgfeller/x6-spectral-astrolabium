# Randkern-Benchmark: Definitionen und Korrekturen

Die mathematische Referenz sind die im [Provenienzmanifest](provenance.json)
auf einen Commit gepinnten Vorgänger. Alle Aussagen gelten innerhalb ihrer
deklarierten endlichen Modelle. Die fünf Ergebnisdateien sind getrennte Datensätze.

## 1. Geometrischer Verklebungskern

Für eine endliche strikte Ordnung C lautet die geerbte Wirkungszahl

$$F_4(C)=|C|-N_0+9N_1-16N_2+8N_3.$$

N_k zählt Paare mit genau k inneren Elementen. Für feste induzierte innere
Ordnungen A und B wird über alle zulässigen Kreuzrelationen summiert:

$$K_{AB}(z)=\sum_{X\in\mathcal G(A,B)}z^{F_4(C_X)-F_4(A)-F_4(B)}.$$

Die vollständige Differenz enthält Kreuzpaare und interne Intervallumklassifizierungen.
Ein transitive closure, der die vorgegebenen inneren Ordnungen verändert, wäre
kein zulässiges Element derselben Faser. Der Replay filtert die vollständige
Enumeration von 219 gelabelten Viererordnungen nach beiden Einschränkungen.

Mit A=Zweierantikette und C=Zweierkette ergeben sich

$$K_{AA}=2z^{-4}+8z^{-3}+16z^{-2}+8z^{-1}+1,$$
$$K_{AC}=K_{CA}=z^{-19}+4z^{-2}+4z^{-1}+1+8z^7+6z^8+2z^{16},$$
$$K_{CC}=2z^{-18}+z^{-2}+2z^{-1}+1+6z+4z^8+4z^{17}.$$

Die Fasergrößen sind 35,26,26,20. Bei der zusätzlichen Phasenparametrisierung
z=exp(iκ) sind dies Amplituden. Die Kontrollwahl z=i legt keinen physikalisch
passenden κ fest. In der Reihenfolge (A,C) gilt

$$K_{\rm geom}(i)=\begin{pmatrix}-13&5-11i\\5-11i&2+8i\end{pmatrix}.$$

Die geerbte Komposition lautet

$$Z_{2,2}(z)=\sum_{[A],[B]}
\frac{z^{F_4(A)+F_4(B)}}{|\operatorname{Aut}A||\operatorname{Aut}B|}K_{AB}(z).$$

Der Replay bestätigt deren koeffizientenweise Gleichheit mit der vollständigen
gelabelten Summe dividiert durch 4. Die Faktoren für die inneren Ordnungen und
deren Wirkungsphasen gehören in diese Formel; K allein ist nicht Z.

Die Indizes sind Teilordnungen einer Verklebung. Sie sind nicht durch diese
Konstruktion als Anfangs-/Endzustände einer Uhrentwicklung identifiziert.
Mit einer rein diagnostischen I₂-Konvention ergibt sich

$$K_{\rm geom}^\dagger K_{\rm geom}
=\begin{pmatrix}315&-143+205i\\-143-205i&214\end{pmatrix}.$$

Dies ist keine neue physikalische MODEL-Entscheidung. Insbesondere ist diese
Matrix nicht der frühere Zweistellen-Uhrkern aus Abschnitt 3.

## 2. Labelquotient und Basisnormierung

Die geerbte Hilfsfamilie besitzt m innere Elemente zwischen zwei fest markierten
Endpunkten, kontinuierliche normierte Uhrmaße und

$$d\nu(w)=\tfrac12\delta_0(dw)+\tfrac12\mathbf1_{(0,1)}dw.$$

Die endliche Gruppe S_m benennt Geometrie, Felder und positive Trägermarken
gemeinsam um; Endlabels bleiben fest. Auf dem Hilfshistorienraum ist

$$P_m=\frac1{m!}\sum_{g\in S_m}U_g,
\qquad P_m^\dagger=P_m=P_m^2.$$

Für Funktionen, die innerhalb jedes kontinuierlichen Stratum konstant sind,
hat jeder diskrete Punkt x=(C,σ) das Gewicht a_m=1/(m!2^m). Jeder Orbit O erfüllt

$$|O|\,|\operatorname{Aut}(C,\sigma)|=m!,\qquad
\mu(O)=\frac1{2^m|\operatorname{Aut}(C,\sigma)|}.$$

In der normierten Punktbasis ist P_xy=1/|O| innerhalb eines Orbits und sonst
null. Für unnormierte Punktindikatoren δ_x ist dagegen

$$\langle\delta_x,P_m\delta_y\rangle_{\rm aux}=a_m(P_m)_{xy}.$$

Für Orbitindikatoren f_O=1_O gilt

$$G_{OO'}=\langle f_O,P_m f_{O'}\rangle_{\rm aux}
=\delta_{OO'}\mu(O).$$

In der normierten Orbitbasis e_O=f_O/√μ(O) ist die Gram-Matrix daher I.
Die Einheit ist dann hergeleitet, nicht willkürlich gewählt. Beide Konventionen
werden gespeichert. Nullrichtungen des Labelprojektors und echte Dichte-Nullatome
sind verschieden; das Atom wird nicht als Nullvektor entfernt.

Der Replay umfasst m=0,1,2: jeweils 1,2,12 markierte Zustände und 1,2,7 Orbits.
P²=P, Symmetrie, Orbit-Stabilisator-Identität und Gram-Normen werden exakt geprüft.
Die normierten Gram-Matrizen folgen durch die angegebene analytische Normierung.
Verschiedene positive Markenzahlen werden durch P nicht vermischt. Das beweist
nur eine Eigenschaft der Labelreduktion, keine dynamische Superselektion.

Dieser Raum enthält vollständige Hilfshistorien mit einer speziellen Randwahl.
Er ist noch kein physikalischer Cauchy- oder Randzustandsraum. Auch die Gruppe
S_m dieses Beispiels ist nicht ungeprüft mit der blockweisen Gruppe der
geometrischen Verklebung gleichzusetzen. Ein gemeinsames Randprodukt benötigt
eine tatsächliche Abbildung der Zustände und ihrer Maße.

## 3. Die ursprüngliche Uhrkern-Negativkontrolle

Hier wird exakt der Kandidat CST-DUST-V1-RAW-K übernommen. Für eine einzige
Relation 0≺1 ist das Anfangsgewicht null und das Endgewicht integriert.
Mit ℏ und B-Vorfaktor jeweils 1 gilt

$$G(a)=\tfrac12+\tfrac12\int_0^1e^{-iaw}dw,\qquad
K=\begin{pmatrix}G(3/2)&G(3/4)\\G(11/4)&G(3/2)\end{pmatrix}.$$

Die Spalten sind die kinematischen Uhrlabels (0,1), die Zeilen (2,3).
Die zusätzlich festgelegte Identifikation ist Translation um +2. Es sind
endliche orthonormale Labels; sie sind keine normierten Punktauswertungszustände
eines kontinuierlichen L²-Raums. Die gemeinsame geometrische Phase ist für die
folgenden Invarianten unerheblich.

Schon im ursprünglichen Produkt I₂ gilt Re(K†K)_01>1/2, also K†K≠cI₂ für jedes
c>0. Der stärkere Test fragt nach K†MK=cM mit einem gemeinsamen M>0. Wäre dies
erfüllt, wäre M^(1/2)KM^(-1/2)/√c unitär. Seine beiden Eigenwerte hätten daher
gleichen Betrag, und für det K≠0 müsste gelten

$$R=\frac{(\operatorname{tr}K)^2}{\det K}\in[0,4]\subset\mathbb R.$$

Die geerbte rationale Taylorrechnung bis Grad 80 benutzt die Restschranke

$$r(a)=\frac{|a|^{81}}{2\,81!\,82}.$$

Rationale Rechteckintervalle werden ohne Fließkommaentscheidung propagiert.
Die Ausgabe reproduziert das ältere Zertifikat, insbesondere

$$\operatorname{Im}R\in
[-2.4527328506264341446412621423239,
-2.4527328506264341446412621423238].$$

Auch die positive untere Schranke für |det K|² wird reproduziert. Das Ergebnis
ist **FAIL_EVERY_COMMON_POSITIVE_METRIC für diesen Kern und diese Identifikation**.
Zwei unterschiedlich und unabhängig begründete Randprodukte, eine Rigging-Map,
vollständige Randräume oder andere Regulatorfamilien sind dadurch nicht ausgeschlossen.
Ein neues Produkt aus dem zu prüfenden K zu fitten wäre keine unabhängige Begründung.

Der Test wird zusätzlich mit dem bekannten positiven Kontrollfall
K=S diag(1,i)S⁻¹, S=[[1,1],[0,1]], M=[[1,−1],[−1,2]], sowie dem negativen
Fall diag(1,2) geprüft. Das sind ausdrücklich synthetische Kontrollmatrizen.

## 4. Stationäre Schurantwort und Nullatom

Für die geerbte Staub-Uhrwirkung bei fester Geometrie und Dichte gilt

$$L=\tfrac12D^T\operatorname{diag}(w_xB_{xy})D,\qquad
S_d=-\tfrac12T^TLT-\tfrac12\sum_xw_x.$$

Der feste Vorgängerfall ist die Fünferkette mit w=(0,0,1,1,0), T₀=0, T₄=4,
gehaltenen Variablen X={2,3} und eliminierter Variable E={1}. Hier ergeben sich

$$L_{EE}=-4,\quad T_1=\frac{-T_2+9T_3}{8},\quad
L_{\rm eff}=\frac1{16}\begin{pmatrix}-55&-17\\-17&145\end{pmatrix}.$$

Für T₂,T₃∈{−1,0,1} werden neun neue rationale Substitutionen geprüft:
die eliminierte Uhrgleichung verschwindet und volle/reduzierte Wirkung stimmen
überein. Diese Zustände sind keine Lösungen aller Dichte- und Geometriegleichungen.

Die Hesse-Matrix ist nicht eine bereits identifizierte Oszillatorsteifigkeit.
Ihre Eigenvektoren erzeugen ohne kinetische Normierung, Uhrdeutung und
Quantisierung keine Zustände |0⟩ und |1⟩. Im vollständig dichtefreien Fall w≡0
ist L=0; eine gewöhnliche Schur-Inverse fehlt. Ein einzelnes Atom w₁=0 schaltet
dagegen Kopplungen an positive Nachbardichten nicht aus: Im Beispiel ist L₁₁=−4.

Die Vorgängeramplitude integriert innere Uhren über kompakte Intervalle.
Sattelpunktsubstitution ersetzt dieses Integral nicht. Selbst für eine geeignete
unbeschränkte Gaußintegration gehören Determinante, Phase, Maß und gegebenenfalls
Nullmoden zur vollständigen Amplitude. Ein zusätzliches skalares Feld Φ mit
quadratischer Wirkung wäre bis zum Nachweis seiner Beziehung zu T,w eine
deklarierte Modellerweiterung.

## 5. Was für eine gemeinsame 8×8-Matrix fehlt

Die Zahl 2 Geometrietypen × 2 Strata × 2 Materiezustände ist zunächst eine
Indexplanung. Konkrete Randfunktionen f_(α,s,n), ihre Träger, Präparation,
Gruppenwirkung und Integrationsmaße müssen feststehen. Erst der Rang ihres
Quotient-Gramprodukts entscheidet, ob acht unabhängige Zustände vorliegen.
Die dazu fehlenden Angaben stehen in [OFFENE_RANDBASIS.json](OFFENE_RANDBASIS.json).

Für kovariante Matrixelemente eines tatsächlich definierten Randoperators gilt
die Normalisierung K_tilde=G_out^(-1/2) K G_in^(-1/2). Für eine
Koeffizientenabbildung A gilt dagegen A_tilde=G_out^(1/2) A G_in^(-1/2).
Das folgt durch Basiswechsel; die Konvention gehört in die Daten. Eine gemeinsame
zeitliche Entwicklung benötigt darüber hinaus Uhridentifikation, Komposition,
Stetigkeit, Unitarität und kontrollierte Generatorzweige. Ein Matrixlogarithmus
eines beliebigen Verklebungskerns liefert diese Eigenschaften nicht.

Ein bei einzelnen Parametern verschwindender Block beweist keine Superselektion:
K_AC(−1)=0 und K_AC(i)=5−11i zeigen im geometrischen Beispiel bereits die
Möglichkeit exakter Phasenauslöschung. Das ist kein 0/+‑Stratumdatensatz.
Dynamische Entkopplung benötigt erhaltene Sektoren der qualifizierten
Evolutionsfamilie. Superselektion verlangt zusätzlich die entsprechende
Blockstruktur aller zulässigen Observablen. Ein gesicherter nichtverschwindender
K_0+ wäre zunächst ein Mischbeitrag der angegebenen Randamplitude, noch kein
Nachweis eines physikalischen Zeitübergangs oder einer linearen Feldkopplung.

## 6. Getrennte Statuswerte

Die 41 PASS-Kontrollen prüfen Quellidentität, endliche Algebra, Projektoren,
Intervalle und stationäre Substitution. Die Ergebnisse sind bekannte
Reproduktionen mit expliziten kleinen Ergänzungen, keine externe Replikation.
Alle acht physikalischen Gates des neuen Benchmarks bleiben HOLD.
Das ältere spezifische MODEL=FAIL wird als parent_raw_kernel_decision erhalten.
K_0+, K_Schur,0 und K_Schur,+ der vorgeschlagenen neuen Materiekonstruktion sind
NOT_COMPUTED; ihre unbekannten Werte werden nicht durch Nullen oder synthetische
Ersatzdaten belegt. Die gesamte 8×8-Matrix bleibt NOT_CONSTRUCTED.
