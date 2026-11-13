# Skalare Rand-Insertion und vollständige Quellengewichte

## Fester Ansatz

Die beiden N=11-Ordnungen und ihre vollständige Skalarwirkung werden unverändert verwendet. C₀ ist die Kette; C₁ entsteht durch Entfernen von (4,5) und (5,6) bei Erhaltung von (4,6) und allen übrigen Relationen. B={0,1,2,3,7,8,9,10}, I={4,5,6}. Die gemeinsame Randfunktion ist

\[
f_B(q_B)=\pi^{-2}\exp(-|q_B|^2/2).
\]

Dies ist eine **L²-normierte Schwartz-Testfunktion bezüglich des Lebesguemaßes**, keine L¹-Wahrscheinlichkeitsdichte und kein hergeleiteter physikalischer Zustandsnormvertrag. Alle acht Randbreiten sind fest gleich eins. Die vorab ausgewählte äußere Insertion ist q₀q₁₀.

Mit dem signierten Laplacian L_c, H_c=−βL_c/2, β=4/√6, und P_B,P_I als Koordinatenprojektoren gilt

\[
A_{c,\epsilon}=P_B+\epsilon P_I-iH_c,
\qquad
Z_c(J)=\lim_{\epsilon\downarrow0}\pi^{-2}\int_{\mathbb R^{11}}
\exp[-q^TA_{c,\epsilon}q/2+J_B^Tq_B],dq.
\]

Die Reihenfolge ist gemeinsame Randpaarung und anschließend Entfernung derselben inneren Abel-Dämpfung. Kein Skalarmassenterm und kein physischer Regulator werden eingeführt.

## Exakte Faktorisation

Weil die unveränderte masselose Skalarwirkung weder r noch T enthält und der Randvertrag im Skalarteil faktorisiert ist, sind die skalaren Faktoren unabhängig von ρ:

\[
g_c=Z_c(0),\quad M_c=(A_{c,0}^{-1})_{BB},\quad
Z_c(J)=g_c\exp(\tfrac12J_B^TM_cJ_B).
\]

Die gemeinsame Gaußmatrix A_{c,0} ist in beiden Fällen invertierbar. Aus A_{c,0}v=0 folgt durch den Realteil v_B=0; die geprüfte Rangbedingung rank L_c[:,I]=3 erzwingt anschließend v_I=0. Dies erlaubt Quellableitungen im Abel-Grenzwert. Die Singularität des inneren Blocks von C₁ bedeutet somit keine Singularität der gemeinsam gepaarten Gaußmatrix.

Die vollständige Staub-/Uhrrechnung setzt denselben festen Rand T_b=Δ(b−5), Δ²=√6/38 und r_b=ρ für b∈B ein und liefert gesondert

\[
W_c(\rho)=e^{iF_4(C_c)}\int_{[-3/2,3/2]^3}\frac{d^3T_I}{27}
e^{-i\rho\sum_{b\in B}C_b(T)/2}\prod_{j\in I}D(C_j(T)),
\]
\[
D(C)=\frac12+\frac{1-e^{-iC/2}}{iC},\qquad D(0)=1.
\]

Dabei bleibt die originale innere Dichtemischung aus halbem Atom bei null und halbem Lebesguemaß auf (0,1) erhalten. W enthält bereits Gravitation und sämtliche integrierten Staubbeiträge. **Eine zusätzliche Multiplikation mit exp(iS_on) wäre Doppelzählung.**

Für feste, quellenunabhängige Historienkoeffizienten ω₀,ω₁ lautet die bedingte kohärente Summe daher

\[
\mathcal A(J,\rho)=\omega_0W_0(\rho)g_0e^{J^TM_0J/2}
+\omega_1W_1(\rho)g_1e^{J^TM_1J/2}.
\]

Die Koeffizienten und gemeinsame Kohärenz sind Modellentscheidungen. Diese Rechnung leitet weder ein physikalisches Historienmaß noch ihre Werte ab. Die hier bewiesene ρ-Unabhängigkeit von g und M darf nicht auf W oder künftige geänderte Präparationen übertragen werden.

## Unabhängige Bestimmung des Gaußzweigs

Für C₀ wird zuerst der dreidimensionale Innenblock integriert: H_II hat Signatur +1, also Fresnelphase +π/4. Die verbleibende Randmatrix ist ein acht-dimensionales Schur-Komplement mit strikt positivem reellem Gaußteil.

Für C₁ wird das nichtsinguläre Paar (q₄,q₆) mit Signatur null integriert. q₅ erzeugt eine Fourier-Deltafunktion auf einer Randhyperfläche. Deren Normalenvektor lautet in B-Reihenfolge

\[
w=(8,-16,9,-1,-1,9,-16,8).
\]

Die verbleibende sieben-dimensionale Gaußintegration erfolgt auf w⊥; der Delta-Jacobian 1/[(β/2)‖w‖] ist enthalten. Diese Konstruktion bestimmt das Vorzeichen und die Phase unabhängig vom bloßen Quadrat eines Determinantenwertes. Eine beliebige Hauptwurzel der finalen Determinante wird nicht eingesetzt.

Bei 80 Dezimalstellen Arbeitspräzision ergibt sich

\[
\frac{g_1}{g_0}=0.32978734312186989071
+0.17268215485161972212\,i.
\]

Die vollständigen 8×8-Matrizen M_c werden unabhängig sowohl durch Inversion von A_{c,0} als auch durch Schur-/Hyperflächenpaarung berechnet. Sämtliche Einträge stimmen besser als 10⁻⁶⁰ überein. Exakte Determinanten und Kofaktoren kontrollieren zusätzlich die algebraische Herkunft. Die numerischen Übereinstimmungen sind Hochpräzisionskontrollen; sie werden nicht als nach außen gerundetes Intervallzertifikat ausgegeben.

## Feste Insertion q₀q₁₀

Die beiden komplexen Insertionswerte h_c=(M_c)_{0,10} sind exakt

\[
h_0=\frac{7854915472178409302214
-4822961275758549461847\sqrt6\,i}
{189326035314894714543751},
\]

\[
h_1=\frac{44296212360591230479983}{352093981721850448867297}
-\frac{28357855261070796511595\sqrt6\,i}{704187963443700897734594}.
\]

Numerisch:

| Ordnung | h_c |
|---|---|
| C₀ | 0,0414888288296631 − 0,0623992054508608 i |
| C₁ | 0,1258079224869701 − 0,0986416684114146 i |

Somit ist h₁−h₀ exakt ungleich null. Weil die linearen J-Ableitungen bei J=0 verschwinden, lautet das normalisierte Amplituden-Insertionsverhältnis

\[
\mathcal H(\rho)=\left.\frac{\partial_{J_0}\partial_{J_{10}}\mathcal A(J,\rho)}
{\mathcal A(0,\rho)}\right|_{J=0}
=\frac{h_0+R(\rho)h_1}{1+R(\rho)},
\]
\[
R=\frac{\omega_1W_1g_1}{\omega_0W_0g_0}.
\]

Diese Quotientform setzt ω₀W₀g₀≠0 und 1+R≠0 voraus. Die direkte Summenform bleibt auch bei einem einzelnen verschwindenden Historienbeitrag gültig, solange die gesamte Amplitude nicht null ist.

Die Quellenableitung ist

\[
\mathcal H'=\frac{(h_1-h_0)R'}{(1+R)^2}
=\frac{(h_1-h_0)\omega_0\omega_1g_0g_1(W_0W_1'-W_1W_0')}
{(\omega_0g_0W_0+\omega_1g_1W_1)^2}.
\]

Die zweite Gleichung vermeidet die Division durch ein einzelnes W. Die Ableitungsidentität wurde symbolisch geprüft. Bei zwei nichtverschwindenden festen Koeffizienten und nichtverschwindender Gesamtamplitude trägt der skalare Teil einen Quellenkontrast genau dann, wenn der Staub-/Uhr-Wronskian W₀W₁′−W₁W₀′ nicht verschwindet. Ob dies in der vollständigen Rechnung zutrifft, entscheiden deren gesonderte W- und W′-Werte; aus der bloßen stationären Wirkungsdifferenz wird es hier nicht abgeleitet.

## Interpretation und Reproduktion

ℋ ist eine **komplexe Lorentzsche Amplituden-Insertion**. Sie kann komplex sein, negative Realteile besitzen oder bei destruktiver Gesamtauslöschung unbeschränkt werden. Sie ist keine positive Kovarianz, kein experimentell abgelesener Randkorrelator, keine Erfolgswahrscheinlichkeit und kein Beweis physikalischer Geometriedynamik. Eine solche Interpretation benötigt erst einen begründeten physikalischen Zustand und Messvertrag.

Der eigenständige Prüfer `checks/scalar_response/check.py` benötigt nur Python, SymPy und mpmath. Er rekonstruiert beide Ordnungen, führt die exakten Determinanten-/Kofaktorprüfungen durch, bestimmt die unabhängigen Fresnel-/Delta-Zweige, vergleicht sämtliche Randinsertionsmatrixeinträge und prüft die Quellenableitungsidentität. `results.json` enthält die Matrizen und Ergebnisse. Es werden keine fremden Skripte importiert und keine Uhrquadraturen durchgeführt.
