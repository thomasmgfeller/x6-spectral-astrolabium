# Ausgewählte Hilfsbasis und Kernkonventionen

## 1. Was die Quelle trägt

Die unverändert eingebettete [Orbitquelle](inputs/label_quotient.json) beschreibt Funktionen, die innerhalb eines kontinuierlichen Uhr-/Dichtestratums konstant sind. Sie reduziert interne Umnummerierungen in einem **Hilfsraum von Historien**. Sie ist keine Herleitung eines physikalischen Rand- oder Cauchyraums.

Für m=2 gilt bei festgehaltenem äußeren Rahmen:

$$
G_7=\mathrm{diag}(1/8,1/4,1/8,1/4,1/4,1/4,1/4).
$$

| Quellindex | Repräsentant (Ordnungscode, positive Maske) | Zahl positiver Marken | Stabilisator | Indikatornorm² | Auswahl |
|---:|---|---:|---:|---:|---|
| 0 | (2190, 0) | 0 | 2 | 1/8 | A0 |
| 1 | (2190, 1) | 1 | 1 | 1/4 | ausgelassen |
| 2 | (2190, 3) | 2 | 2 | 1/8 | A+ |
| 3 | (2254, 0) | 0 | 1 | 1/4 | K0 |
| 4 | (2254, 1) | 1 | 1 | 1/4 | ausgelassen |
| 5 | (2254, 2) | 1 | 1 | 1/4 | ausgelassen |
| 6 | (2254, 3) | 2 | 1 | 1/4 | K+ |

Insbesondere ist der Stabilisator einer gemischt markierten Antikette kleiner als der einer vollständig gleich markierten Antikette. Ein pauschales Geometriegewicht für alle Materiemarken wäre falsch.

Sei $E_4=(e_0,e_3,e_2,e_6)$ die Auswahlmatrix in der Siebenerbasis. Mit dem externen Testfaktor $\mathbb C^2$ setzen wir $E=E_4\otimes I_2$, $G_p=G_7\otimes I_2$ und

$$
G=E^\dagger G_p E,\qquad J=EG^{-1/2}.
$$

Dann $J^\dagger G_pJ=I_8$. Die unnormierten Indikatoren E haben dagegen gerade Gram G. Das beweist einen positiven ausgewählten Hilfsraum. Es beweist weder eine Dynamik, die den ausgewählten Unterraum erhält, noch eine Eliminierung der drei ausgelassenen Orbits.

## 2. Zwei Darstellungen derselben Abbildung

Für eine Koeffizientenabbildung $A:V_{\rm in}\to V_{\rm out}$ gilt

$$
\widehat A=G_{\rm out}^{1/2}A G_{\rm in}^{-1/2},\qquad
A^\dagger G_{\rm out}A=G_{\rm in}
$$

als Isometriebedingung. Definiert man stattdessen die kovarianten Matrixelemente $B_{ij}=\langle f_i^{\rm out},Tf_j^{\rm in}\rangle$, gilt $B=G_{\rm out}A$, also

$$
\widehat B=G_{\rm out}^{-1/2}B G_{\rm in}^{-1/2}
=\widehat A,\qquad
B^\dagger G_{\rm out}^{-1}B=G_{\rm in}.
$$

Die beidseitige inverse Wurzel ist somit nur für B die passende Formel. Man darf sie nicht ohne Umdeutung auf eine als A deklarierte Matrix anwenden.

## 3. Darstellungstransport und zusätzliche Zuordnungen

Die [Geometriequelle v0.2](inputs/geometry_z1.json) bezeichnet $A_e$ ausdrücklich als Koeffizientenabbildung in einer orthonormalen **formalen** Testbasis. Wir identifizieren diese Testbasis zusätzlich mit den normierten ausgewählten Orbitindikatoren J. Diese Identifizierung liefert keinen bereits bekannten vollen Historienoperator.

Für den reinen Darstellungstransport nach den unnormierten Indikatoren lautet die korrekte Formel:

$$
A_f=G^{-1/2}A_eG^{1/2},\qquad
B_f=GA_f=G^{1/2}A_eG^{1/2}.
$$

Beide Normalisierungen geben wieder $A_e$. Ein Basiswechsel kann den Isometriebefund desselben Operators nicht ändern.

Zwei davon verschiedene Vergleiche ordnen dieselben Quellzahlen zusätzlich zu:

$$
\begin{array}{lll}
\text{assign coefficients}:&A_f:=A_e,&
\widehat A=G^{1/2}A_eG^{-1/2},\\
\text{assign covariant}:&B_f:=A_e,&
\widehat B=G^{-1/2}A_eG^{-1/2}.
\end{array}
$$

Für $g=\mathrm{diag}(1/8,1/4)$ und $K_g(1)=\left(\begin{smallmatrix}35&26\\26&20\end{smallmatrix}\right)$ entstehen die zweidimensionalen normierten Blöcke

$$
U_{\rm transport}=\begin{pmatrix}35&26\\26&20\end{pmatrix},\quad
U_{\rm coeff}=\begin{pmatrix}35&13\sqrt2\\26\sqrt2&20\end{pmatrix},\quad
U_{\rm cov}=\begin{pmatrix}280&104\sqrt2\\104\sqrt2&80\end{pmatrix}.
$$

Die vollständigen Matrizen sind jeweils $I_2\otimes U\otimes I_2$. Die exakt berechneten Polynome für die quadrierten Singularwerte sind:

| Modus | Polynom |
|---|---|
| transport | $x^2-2977x+576$ |
| assign_coefficients | $x^2-3315x+576$ |
| assign_covariant | $x^2-128064x+589824$ |

Jeder Singularwert tritt vierfach auf. Bei transport sind sie $(55\pm\sqrt{2929})/2$, bei assign_covariant $180\pm4\sqrt{1977}$. Für beide symmetrischen Blöcke sind beide Eigenwerte positiv. Der kovariante Vergleich ergibt daher exakt $\|U^\dagger U-I_8\|_2=64031+1440\sqrt{1977}$. Das reproduziert den früheren großen Wert unter einer ausdrücklich zusätzlichen Zuordnung.

Die Singularwerte sind in jedem Fall verschieden. Folglich kann kein einzelner von null verschiedener Skalar den jeweiligen gesamten Testkern isometrisch machen. Eine Polarzerlegung würde einen neuen Operator auswählen; sie wird hier nicht durchgeführt. Ohne hergeleitete Uhr und geschlossene Quantenevolution wird auch kein physikalischer Hamiltonoperator aus einem Logarithmus konstruiert.

## 4. Unterschiedliche Produkte: eine eingeschränkte Obstruktion

Für die Koeffizientenzuordnung $A=K_g(1)$, ein positives diagonales Ausgangsprodukt $G_{\rm out}=\mathrm{diag}(u,v)$ und ein diagonales Eingangsprodukt gilt exakt

$$
(A^\dagger G_{\rm out}A)_{12}=910u+520v>0.
$$

Es kann nicht gleich dem verschwindenden Nebendiagonalelement von $G_{\rm in}$ sein. Für die kovariante Zuordnung $B=K_g(1)$ gilt entsprechend

$$
(B^\dagger G_{\rm out}^{-1}B)_{12}=910/u+520/v>0.
$$

Damit lösen **unterschiedliche positive diagonale** Produkte in dieser ausgerichteten Indikatorbasis das Isometrieproblem bei z=1 nicht. Der reine Transport hat ebenfalls positive Blockeinträge, sodass dieselbe Vorzeichenobstruktion gilt, ohne dass dafür die Zahlen 910 und 520 unverändert bleiben müssten.

Das Argument erfasst keine beliebigen nichtdiagonalen Produkte, andere Phasen oder eine vollständige CST-Amplitude. Insbesondere wäre $G_{\rm in}:=A^\dagger G_{\rm out}A$ für invertierbares A algebraisch positiv, aber eine aus dem geprüften Operator nachträglich definierte Metrik ist keine unabhängige physikalische Herleitung.

## 5. Was Nullblöcke sagen

Für alle drei Zuordnungen bleiben Ein-/Ausgangsstrata und Testlabels unvermischt. Die Messung verwendet Masken $s_i\ne s_j$ bzw. $m_i\ne m_j$ auf der tatsächlich deklarierten Basis und umfasst beide Richtungen. Diese Kontrollnullen folgen aus der Zuschauerannahme und dem diagonalen ausgewählten Produkt.

Sie bestimmen nicht den physikalischen Block $K_{0+}$, keine gemeinsame Materiewirkung und keine Superselektionsregel. Die Negativkontrolle des älteren rohen Uhrkerns im Randkern-Benchmark betrifft einen anderen Operator und bleibt separat.

Alle verwendeten Quellbytes sind mit Commit und Git-Blob in [provenance.json](provenance.json) festgehalten; die lokale Rechnung benötigt keinen Netzwerkzugriff.
