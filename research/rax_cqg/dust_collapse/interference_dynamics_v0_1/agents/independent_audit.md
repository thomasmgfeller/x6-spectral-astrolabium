# Unabhängiger Audit der drei Anschlussaufgaben

13. November 2026. Interne KI-Gegenprüfung; keine externe Begutachtung.

## Ergebnis und Reichweite

Die drei Aufgaben sind im neuen **endlichen bedingten Vertrag** substanziell bearbeitet: Das innere Staub-/Uhrgewicht wurde vollständig integriert, ein konsistentes bedingtes Auslesemodell konstruiert und die Wirkungskomposition samt geometrischen Ordnungsobservablen exakt geprüft. Die gemeinsame physikalische Paarung, das ausgezeichnete Historienmaß und die Dynamikdeutung sind weiterhin nicht hergeleitet. Eine Bezeichnung als gelöste physikalische CST-Geometriedynamik wäre deshalb falsch.

Der Audit findet keinen Faktor-, Phasen-, Strata- oder Kompositionsfehler in den geprüften Teilrechnungen. Er ergänzt zwei unabhängige Rechner:

- `checks/independent_audit/check.py`: ursprüngliches Dichtemaß, alle acht inneren Strata, vollständige Randphase, geometriespezifische Quellenableitungsschranken und Doppelzählungskontrolle.
- `checks/independent_audit/audit_quadrature.py`: unabhängige Ordnungs-/Intervallrekonstruktion an drei inneren Uhrpunkten und exakt rationale Zertifizierung sämtlicher angegebenen analytischen Quadraturrest-Dezimalzahlen. Es wird kein neuer vollständiger Quadraturdurchlauf gestartet.

## 1. Vollständiges relatives Gewicht

Für jede der beiden N=11-Ordnungen ist der geprüfte Vertrag

\[
W_c(\rho)=e^{iF_c}\int_{[-3/2,3/2]^3}\frac{d^3T_I}{27}\,
e^{-i\rho P_{B,c}(T_I)/2}\prod_{j\in I}D(C_{j,c}(T_I)),
\qquad P_{B,c}=\sum_{j\in B}C_{j,c}.
\]

Die äußeren Uhren sind Tj=(j−5)Δ mit Δ²=2/(19β), die äußeren Dichten sind rj=ρ. Die inneren Uhren werden über die ganze neue Box integriert. Es gibt keinen zusätzlich eingeschobenen Ordnungsindikator T_i<T_j. Die im vorausgehenden klassischen Zeugen gerichteten Uhren beschränken also nicht stillschweigend den Quantenintegrationsbereich.

Für das ursprüngliche gemischte innere Dichtemaß gilt exakt

\[
D(C)=\frac12+\frac12\int_0^1e^{-irC/2}dr
=\frac12+\frac{1-e^{-iC/2}}{iC},\qquad D(0)=1.
\]

Die numerisch verwendete Form für das positive Integral,

\[
E(C)=e^{-iC/4}\operatorname{sinc}(C/4),\qquad D=(1+E)/2,
\]

ist korrekt. Bei NumPy bedeutet `np.sinc(C/(4*pi))` genau sin(C/4)/(C/4); der zusätzliche π-Faktor ist daher richtig. Das Produkt der drei D-Faktoren hat acht Atom-/Positivstrata, jeweils mit Vorfaktor1/8. Das getrennte Summieren der acht Beiträge stimmt mit der direkten Produktform überein. Ein nur positiver Dichtesektor wäre nicht dasselbe Gewicht.

Die gesamte Wirkung zerfällt exakt in

\[
S=F_c-\rho P_{B,c}/2-\tfrac12\sum_{j\in I}r_jC_{j,c}+S_{\phi,c}.
\]

Damit enthält W bereits sämtliche äußeren Staubwirkungsterme, alle inneren Staubphasen und e^{iF_c}. Die volle skalargepaarte Amplitude lautet a_c=ω_c W_c g_c. **Eine zusätzliche Multiplikation mit e^{iS_on} ist unzulässig.** Als negative Kontrolle zeigt der eigene Rechner: Ein zusätzliches e^{iΔS_on}, ΔS_on=8+23ρ/19, würde der logarithmischen Ableitung des relativen Gewichts künstlich i·23/19 hinzufügen.

Die skalare Faktorisierung ist exakt, weil Sφ weder T noch r enthält und der gemeinsame skalare Randtest unverändert bleibt. Bei Änderung der skalaren Randpakete mit ρ müsste diese Unabhängigkeit neu geprüft werden.

### Was „vollständig“ hier bezeichnet

Alle **inneren** Uhr- und gemischten Dichtemaße werden berücksichtigt; alle äußeren Wirkungsbeiträge stehen im Exponenten. Die äußeren T- und r-Werte sind jedoch festgehaltene Dirichlet-Koordinaten. Es werden keine normalisierten äußeren Uhr-/Dichterandpakete und keine äußeren Atomstrata integriert. Dies ist folglich ein vollständiges Gewicht unter dem neuen Dirichlet-/Boxvertrag, keine bereits physikalisch begründete vollständige Randzustandsamplitude des ursprünglichen Piloten.

### Exakte Schranken vor der Quadratur

Da D eine charakteristische Funktion eines positiven normierten Maßes ist, gilt |D(C)|≤1 für reelles C. Die Uhrmaße sind ebenfalls normiert. Deshalb

\[
|W_c|\leq1,
\quad W_c'=-\frac i2e^{iF_c}\mathbb E_T\left[P_{B,c}e^{-i\rho P_{B,c}/2}\prod_I D(C_j)\right].
\]

Die Ableitung ist unter dem Integral zulässig, weil alle Variablen auf kompaktem Gebiet liegen und die Integranden glatt sind. Mit k=βΔ, x=(T4,T5,T6) rekonstruiert der Audit unabhängig

\[
P_{B,0}=\frac{125}{19}+4\beta x_4^2-\frac\beta2x_5^2-8kx_4+2kx_5+kx_6,
\]
\[
P_{B,1}=\frac{112}{19}-\frac\beta2x_4^2+2kx_4+kx_5+kx_6.
\]

Beide sind auf der ganzen Uhrbox strikt positiv. Die exakten Minima und einfacheren rationalen Untergrenzen sind

\[
\min P_{B,0}=\frac{117}{19}-\frac{9\beta}8-\frac{9k}2>\frac{183}{76},
\quad
\min P_{B,1}=\frac{112}{19}-\frac{9\beta}8-6k>\frac{231}{152}.
\]

Hier genügen die durch Quadrieren bewiesenen Schranken β<5/3 und k<5/12. Die Normabschätzung verbessert sich dadurch zu

\[
|W_0'|\leq\tfrac12\mathbb E P_{B,0}=\frac{125}{38}+\frac{21\beta}{16},
\quad
|W_1'|\leq\tfrac12\mathbb E P_{B,1}=\frac{56}{19}-\frac{3\beta}{16}.
\]

Diese Ableitungsschranken gelten für alle reellen ρ im definierten mathematischen Gewicht. Sie zertifizieren keine Nichtnull-Antwort oder Phase; die gewichteten komplexen Integrale können sich weiterhin auslöschen.

### Prüfung des analytischen Quadraturrests

Der geprüfte Tensor-Gauss-Legendre-Ansatz verwendet positive, auf1 normierte Gewichte. Für eine Variable ist der Gaussoperator bis Grad2n−1 exakt. Auf der Bernsteinellipse mit R=7/4 liefert der abgeschnittene Chebyshev-Ausbau den Uniformrest2MR^(−2n)/(1−R^-1). Integral und Quadratur haben je Norm1, sodass ihre Differenz durch4MR^(−2n)/(1−R^-1) beschränkt wird. Teleskopieren über die drei Variablen ergibt die verwendete Summe.

Für eine komplex fortgesetzte innere Uhr und die übrigen reellen Uhren ist

\[
\log M_k\leq\frac{15}{8}\,b_R(a_R+1)
\sum_{(i,j):k\in\{i,j\}}|b_{ij}|r_{j,\max},
\]

mit a_R=(R+R^-1)/2, b_R=(R−R^-1)/2, innerem rmax=1 und äußerem rmax=1/4. Die Vorfaktoren folgen aus β<5/3 und Uhrhalbbreite3/2. **Diese analytische Restabschätzung gilt für 0≤ρ≤1/4; sie darf nicht ohne Anpassung auf den gesamten vertraglichen Quellenbereich 0<ρ<1/2 übertragen werden.** Beide ausgewerteten Quellen1/8 und1/4 sind erfasst.

Die Ableitungsinsertion P_B/2 wird auf derselben Ellipse beschränkt; ihre äußeren Konstanten und sämtlichen Randkanten sind enthalten. Die implementierte Schranke ist konservativ, aber korrekt.

Der unabhängige Audit rekonstruiert alle rationalen logM-Werte und zertifiziert ihre exponentiellen Oberschranken ohne Gleitkommaannahme: Taylorpolynom mit513 Termen plus geometrischer Rest. Damit sind bei n=160 unter anderem die angegebenen absoluten Restschranken

| Ordnung | W-Trunkationsrest | W'-Trunkationsrest |
|---|---:|---:|
| Kette | <1,2×10⁻²⁵ | <1,5×10⁻²² |
| Zwei entfernte Vergleiche | <1,6×10⁻³² | <2,1×10⁻²⁹ |

exakt rational gegen die analytische Formel abgesichert. Auch alle angegebenen n=64/96/128-Schranken bestehen dieselbe Prüfung.

**Nicht eingeschlossen sind Fehler der Float64-Knoten, -Gewichte, Arithmetik und elementaren Funktionen.** Die kleinen Unterschiede aufeinanderfolgender Gitter sind Konsistenzdiagnosen, keine Fehlereinschließung. Die numerischen komplexen Gewichte, Quotienten, Phasenableitungen und daraus gebildeten Antworten dürfen deshalb nicht als vollständig zertifizierte Intervalle bezeichnet werden. Auch Quotienten benötigen einen von null getrennten Nenner; die numerische Nichtnullbeobachtung ersetzt keinen allgemeinen Satz für alle ρ.

## 2. Auslese und physikalische Randzustände

Der bedingte Recordansatz ist algebraisch konsistent. In der benutzten Konvention

\[
D_{cd}=a_c\overline{a_d}\langle e_d|e_c\rangle,
\quad \eta=\begin{pmatrix}1&\gamma\\\bar\gamma&1\end{pmatrix},
\quad |\gamma|\leq1
\]

ist D stark positiv. Die Darstellung der Recordvektoren mit E†E=ηᵀ stimmt mit dieser Konvention überein; ein zusätzlicher Transpositions- oder Konjugationswechsel ist nicht nötig. Für die Vereinigung der beiden kohärenten Alternativen ist Z=Σ_cd D_cd maßgeblich, nicht trD. Eine Normierung auf Z setzt Z>0 voraus. Bei γ=1 können die normierten Diagonaleinträge größer als1 sein; sie sind dann keine klassische Wahrscheinlichkeitsverteilung über ungemessene Geometriehistorien.

Die expliziten CP-Beispiele mit gemeinsamem Gain und orthogonalem Failure-Ausgang sind gültige abstrakte Instrumentkonstruktionen. Ihre synthetischen Amplituden werden korrekt nicht als N=11-Messdaten ausgegeben. Ein solcher endlicher Positivitätsbeweis bestimmt weder eine physische Randnorm noch die fehlende Historiengewichtung oder den physisch vorhandenen Umweltüberlapp.

Die freie Gewichtskonstruktion für beliebige aufgelöste Klassenfraktionen zeigt Unterbestimmtheit an einem festen Quellenwert. Für eine Antwortkurve müssen dieselben Gewichte und dasselbe γ über alle Präparationen und ρ hinweg festbleiben. Ein gesondertes Fitten für jeden Quellenwert würde den Vertrag ändern. Der Zustandsraumagent wurde auf diese Einschränkung hingewiesen.

Die skalare Gaußpaarung ist eine wohldefinierte komplexe Testfunktionalpaarung. Der Faktorπ^-2 ist für acht Randkoordinaten korrekt L2-normalisiert. Die getrennten Fresnel-/Schur- beziehungsweise Fourier-Delta-/Hyperflächenrechnungen stimmen mit der gemeinsamen Determinantenstruktur überein. Daraus folgt keine positive physische Kovarianz. Insbesondere sind die Einfügungen q0q10 und ihre normierten komplexen Quotienten keine Born-Korrelationen oder geometrischen Detektorablesungen.

**Status von Aufgabe2:** Konsistente bedingte Möglichkeiten und die verbleibende Identifizierbarkeitslücke sind konstruiert. Physische Uhr-/Dichterandzustände, Maß und Kohärenz sind weiterhin nicht abgeleitet.

## 3. Zusammensetzung und geometrische Observablen

Die Kompositionsprüfung rekonstruiert die ursprünglichen offenen Intervalle einschließlich aller schnittübergreifenden Intervallbeiträge. Für die geprüften natürlichen Prefixschnitte stimmen sämtliche Monomkoeffizienten der vollständigen Wirkung, ihrer inkrementellen Zerlegung und der wieder zusammengesetzten Teilwirkungen exakt. Das Weglassen eines echten Kreuzterms wird korrekt zurückgewiesen.

Der vollständige kausale Prefix mit allen behaltenen Feldern ist ausreichende Memory. Er ist eine mathematische Buchführung und kein zusätzliches orthogonales Messregister. Ein solches Register würde gegebenenfalls gerade die gewünschte Interferenz zerstören. Kopieren ist als Punktmaßkernδ_x(dy_old) zu formulieren, nicht als unbegründete Lebesgue-δ-Dichte gegen das gemischte Atom-/Positivmaß. Der Kompositionsbericht hält diese Unterscheidung ausdrücklich fest.

Bei ε>0 machen der gemeinsame Skalarregulator, die vollständige äußere Gaußdämpfung und die kompakten Uhr-/Dichtemaße die integrierten Ausdrücke absolut konvergent. Dann ist Fubini zulässig. Der Abelgrenzwert wird erst nach der gemeinsamen Randpaarung genommen; getrennte Produkte singulärer Teilgrenzwerte sind damit nicht legitimiert. Die Wirkungskomposition leitet keine Wahrscheinlichkeiten für das Entstehen einer neuen Ordnung und kein ausgezeichnetes bedingtes Historienmaß her.

Die Zahl vergleichbarer ungeordneter Paare im inneren Dreierbereich ist eine wohldefinierte randmarkiert-kovariante Ordnungsobservable O mit Werten3 und1. Der Nachweis umfasst die transportierten inneren Relabelings. Er benötigt keine eingebettete Radiusinterpretation.

Für ausdrücklich aufgelöste Klassenrecords lautet der bedingte Mittelwert

\[
\langle O\rangle_{\rm res}=(3+\lambda)/(1+\lambda),
\quad\lambda=|a_1/a_0|^2.
\]

Die geprüfte Ableitung −4λ/(1+λ)²·∂ρlog|W1/W0| ist korrekt bei festen skalaren Faktoren und Historiengewichten. Sie ist gegenüber reinen Klassenphasen blind. Der kohärente Amplitudenquotient (3a0+a1)/(a0+a1) kann dagegen komplex sein oder außerhalb[1,3] liegen; er ist kein Born-Mittelwert. Die Gegenbeispiele2−i und5 bestätigen genau diese Grenze.

ρ ändert gemeinsame äußere Dichtekoordinaten. Es ist keine Zeitvariable und bislang keine kalibrierte Masse. Eine ρ-abhängige Randantwort sowie exakte Prefixkomposition ergeben daher noch keine physikalische geometrische Zeitentwicklung. Für Kollaps, Außenraum und vierdimensionale Verfeinerung gelten die bereits festgehaltenen offenen Voraussetzungen weiter.

**Status von Aufgabe3:** Exakte vollständige-Memory-Komposition, echte finite Ordnungsobservablen und bedingte Quellenantworten liegen vor. Eine abgeleitete physikalische Geometriedynamik liegt weiterhin nicht vor.

## 4. Abschließende Prüfung der kombinierten Antwort

Die Kombination in `checks/combined_response/check.py` verwendet feste Gewichte ω0=ω1=1, dieselbe skalare Randgaußfunktion und a_c=W_c g_c. Eine zweite stationäre Wirkungsphase wird nicht eingefügt. Mit R=a1/a0 und h_c=(A_c^-1)0,10 lautet die kohärente Testfunktionaleinfügung H=(h0+R h1)/(1+R); ihre Ableitung (h1−h0)R(∂ρlogW1−∂ρlogW0)/(1+R)² stimmt mit der unabhängigen algebraischen Prüfung überein.

Zwischen ρ=1/8 und ρ=1/4 ergeben die gespeicherten numerischen Werte ΔH≈−0,02969735+0,05745731i und die getrennt definierte aufgelöste Ordnungsantwort 2,473594→2,347464. Beide stimmen mit den angegebenen Formeln und den skalaren Faktoren überein. Die Zahlen sind bedingte Antworten unter dem gewählten Vertrag; H ist komplex und keine positive physische Kovarianz. Die beiden Quellenpräparationen verändern den vergangenen und zukünftigen Dichtekragen gemeinsam.

Der sechsseitige Ergebnisbericht trennt den analytischen Quadraturrest von nicht eingeschlossenen Gleitkommafehlern und benennt die fehlende physische Rand-/Historienauswahl. Damit ist die Statusdarstellung der drei Aufgaben konsistent. Einzige redaktionelle Präzisierungen: Die freie Realisierbarkeit jeder Klassenfraktion gilt an einem festen Quellenwert; solche frei gewählten Resultate heißen bedingte Vorhersagen, solange der physische Vertrag fehlt. Keine mathematische Blockade der vorliegenden bedingten Konstruktion wurde gefunden.

## Gesamturteil

Die Rechnung geht über den zuvor allein bekannten stationären Phasenunterschied hinaus: Die vollständigen inneren Gewichte einschließlich Atomstrata und Randwirkung sind verfügbar, die stationäre Phasensteigung wird nicht als Integralergebnis eingesetzt, und die Zusammensetzung ist direkt kontrolliert. Der klar verbleibende Engpass ist die physische Rand-/Historieninterpretation desselben mathematischen Vertrags. Weitere Nachkommastellen oder die Umbenennung einer Quellenantwort in Zeitentwicklung schließen ihn nicht.
