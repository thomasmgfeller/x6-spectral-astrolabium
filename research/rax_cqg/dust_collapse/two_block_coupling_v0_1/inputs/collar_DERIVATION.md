# Vergangenheitskragen: gemeinsame Stationarität und Randzustände v0.1

Datum: 8. November 2026 (Zürich). Basis: Main nach PR 265,
`2b422800dcc0bd79643e1c946069acf8875a5291`.

## 1. Fragestellung und Geltungsbereich

Der Ein-Anker-Kandidat aus PR 265 lässt die positive innere Staub-Normierung am ersten freien Element nicht zu. Der dort ergänzte Kragen erfüllt zwar die Normierung, aber nicht die Uhrgleichung. Hier wird eine **gemeinsame** Lösung gesucht und anschließend die Unsicherheit ihrer Randdaten untersucht.

Wir übernehmen die normierte Materiewirkung (A=1) und die Intervallgewichte B=(1,-9,16,-8,0,…). Die Geometrie bleibt fest. Es gibt genau ein letztes freies Element mit Uhr t und positivem innerem Dichtegewicht 0<w<1; alle Vorgängeruhren und Vorgängerdichten bleiben äußere Daten. Es gibt keine zukünftigen Elemente und keinen zusätzlichen Randwirkungsterm. Das ist ein konditioniertes Variationsproblem, keine Variation einer abgeschlossenen Raumzeit. Die normierten Uhrwerte und der reelle Phasenparameter μ sind Größen des reduzierten Modells; w wird nicht als physikalische Ruhemasse identifiziert.

Alle acht physikalischen Gates bleiben HOLD. Weder ein physikalischer Randzustand noch eine Constraintquantisierung, Observablenalgebra, Anschlussdynamik oder Singularitätsauflösung werden hergeleitet.

## 2. Vollständiges Momentkriterium für ein letztes freies Element

Für die festgehaltenen Vorgänger y setze

\[
b_0=\sum_yB_y,\quad m_1=\sum_yB_yT_y,\quad m_2=\sum_yB_yT_y^2.
\]

Die vom freien Element abhängige Wirkung ist

\[
S_f=-\frac w2 C(t),\qquad
C(t)=1+\frac12(b_0t^2-2m_1t+m_2).
\]

Es folgen \(\partial_wS_f=-C/2\) und
\(q_t=\partial_tS_f=-w(b_0t-m_1)/2\). Für w>0 ist gemeinsame innere Stationarität daher äquivalent zu:

* Falls b₀≠0: t=m₁/b₀, zusätzlich 2+m₂−m₁²/b₀=0 und t>max T_y.
* Falls b₀=0: m₁=0 und m₂=−2. Dann sind **alle** kausal zulässigen t und positiven inneren w stationär.

Das sind notwendige und hinreichende Bedingungen für genau dieses Variationsproblem. Im ersten Fall bleibt w unbestimmt; im zweiten verschwindet die gesamte 2×2-Hessematrix in (t,w), weil C=C′=C″=0. Ein isolierter Sattel oder ein ausgewählter Zustand folgt daraus nicht.

## 3. Minimale Kettenlänge und rationaler Zeuge

In einer Kette sind die Abstände zum letzten freien Element, vom jüngsten Vorgänger aus gezählt, 0<d₁<d₂<d₃<d₄. Die Uhrableitung ist proportional zu

\[
\sum B_y(t-T_y)=
\begin{cases}d_1>0,&m=1,\\d_1-9d_2<0,&m=2,\\d_1-9d_2+16d_3>0,&m=3.\end{cases}
\]

Deshalb gibt es bei höchstens drei Kettenvorgängern keine gemeinsame Stationarität mit w>0. Ab vier Vorgängern ist b₀=1−9+16−8=0; ältere Kettenvorgänger haben Gewicht null. Die Aussage ist nur in dieser Kettenklasse minimal, nicht unter allen endlichen Kausalsets oder bei zusätzlichen Randtermen.

Ein rationaler Zeuge in chronologischer Reihenfolge lautet

\[
(T_0,T_1,T_2,T_3)=(-5/2,-2,-4/3,0),\quad
(B_0,B_1,B_2,B_3)=(-8,16,-9,1).
\]

Dann sind b₀=0, m₁=20−32+12=0 und m₂=−50+64−16=−2. Somit gilt für jedes t>0 und 0<w<1 exakt C=q_t=S_f=0. Dieser Zeuge behebt den gemeinsamen Normierungs-/Uhrwiderspruch des kurzen Kragens, ohne eine eindeutige Dynamik auszuwählen.

## 4. Die Randreaktion bleibt notwendig

Alle vier Vorgängerdichten werden am ursprünglichen Nullatom fixiert. Die geerbten gerichteten Variationsströme sind
\(j_{y\to f}=wB_y(t-T_y)/2\). Am festen Rand ist q_y=j_{y→f}, am freien Element q_t=−Σj. Für beliebige Uhrdaten gilt die homogene Identität

\[
\sum_z T_zq_z=-\sum_xw_x\Gamma_x.
\]

Beim vorliegenden stationären freien Element ist Γ_f=−1, also
\(\sum_{y\in\partial}T_yq_y=w\), obwohl Σq=0. Für t=w=1/2 sind die Randreaktionen exakt
\((-6,10,-33/8,1/8)\); ihre Summe ist null und ihre gewichtete Summe 1/2.

Die festgehaltene Vorgeschichte trägt somit eine nichtverschwindende Reaktion. Diese darf bei einer späteren Variation des Randes nicht weggelassen werden. Die vorzeichenbehafteten j sind hier Variationsgrößen, kein bereits hergeleiteter positiver Massenstrom. Insbesondere ist der Zeuge kein vollständig stationäres geschlossenes Staubsystem.

## 5. Exakte Störungsgesetze und Fehlerbudget

Ersetze T_y durch T_y+δ_y, ohne die Ordnung oder Intervallgewichte zu ändern. Definiere

\[
d^{(1)}=\sum B_y\delta_y,\qquad
d^{(2)}=2\sum B_yT_y\delta_y+\sum B_y\delta_y^2.
\]

Dann gilt identisch

\[
C_\delta(t)=-t d^{(1)}+d^{(2)}/2,\qquad
q_\delta=wd^{(1)}/2.
\]

Gemeinsame Stationarität erfordert d⁽¹⁾=d⁽²⁾=0. Eine Änderung von t kann d⁽¹⁾≠0 nicht reparieren. Die Gradienten B und 2BT der beiden Momentbedingungen sind am Zeugen linear unabhängig; ihre lokale Lösungsmenge hat Kodimension zwei. Gemeinsame Verschiebungen aller vier Randuhren bleiben dagegen auf dieser Menge, solange die freie Uhr kausal danach liegt. Nicht jede korrelierte Unsicherheit verletzt die Bedingungen.

Für |δ_y|≤ε≤1/64 und t∈[1/4,1] bleibt die Ordnung erhalten. Mit Σ|B|=34, Σ|BT|=64 folgt

\[
|C_\delta(t)|\le(34t+64)\epsilon+17\epsilon^2
\le B_\epsilon:=98\epsilon+17\epsilon^2,
\quad |q_\delta|\le17w\epsilon.
\]

## 6. Ein expliziter normierter Randzustand endlicher Breite

Als **zusätzlichen kinematischen Prüfvertrag** wählen wir den Raum
L²(d⁴δ)⊗L²(dt)⊗L²(dν(w)), mit
\(d\nu=\tfrac12\delta_0+\tfrac12 1_{(0,1)}dw\).
Die vier früheren Dichten liegen in normierten Atomzuständen und sind hier ausgeklammert. Wähle

\[
\Psi_{B,\epsilon}=(2\epsilon)^{-2}1_{[-\epsilon,\epsilon]^4},
\quad \phi_t=\frac2{\sqrt3}1_{[1/4,1]},\quad\phi_w=1.
\]

Das Produkt ψ_ε ist normiert. Seine Betragsquadrate erklären vier unabhängige uniforme Randabweichungen, eine uniforme freie Uhr und das ursprüngliche Dichtemaß. Dies ist keine abgeleitete physikalische Präparation und keine Behauptung über reale Messunsicherheiten.

Unter diesem Maß sind EC=Eq=0. Trotzdem sind beide Residuen positiv:

\[
\|C\psi_\epsilon\|^2=\frac{21751}{24}\epsilon^2+\frac{134}{15}\epsilon^4,
\quad \|q\psi_\epsilon\|^2=\frac{67}{12}\epsilon^2,
\quad \|wC\psi_\epsilon\|^2=\frac16\|C\psi_\epsilon\|^2.
\]

Beweis: Mit δ_y=εη_y und unabhängigen η∼Unif[-1,1] ist
C=εΣB_y(T_y−t)η_y+(ε²/2)ΣB_yη_y². Der Kreuzterm hat verschwindenden Mittelwert. ΣB=0, ΣB²=402 und
\(K(t)=\sum B_y^2(T_y-t)^2=402t^2+1560t+1568\).
Mit Et=5/8 und Et²=7/16 ist EK=21751/8; daraus folgt der quadratische Beitrag ε²EK/3. Der vierte Beitrag ist ε⁴ΣB²/45=134ε⁴/15. Für q verwendet man Ew²=1/6 und Eη²=1/3.

Die gemeinsame exakte Momentfläche hat Lebesgue-Maß null; kein von null verschiedener L²(d⁴δ)-Zustand kann ausschließlich darauf getragen sein. Das ist eine Aussage über dieses deklarierte Maß, kein Verbot eines anders hergeleiteten physikalischen Skalarprodukts.

Die Überlappungsamplitude von Ψ_B,ε und Ψ_B,ε/2 ist 1/4, ihr Quadrat 1/16. Die normierten schmaler werdenden Zustände sind nicht norm-Cauchy und konvergieren schwach gegen null: für jedes f∈L² ist ihr Überlappungsbetrag durch ||f·1_cube||₂ beschränkt, was gegen null geht. Der exakt scharfe Kragen ist klassische äußere Information beziehungsweise ein verallgemeinerter Zustand; er ist kein normierter L²-Grenzzustand dieser Folge.

## 7. Bedingte Rückkehramplitude und nichtvertauschbare Grenzen

Auf dem erklärten kinematischen Raum definiere den unitären Multiplikationsoperator D_μ=exp(−iμwC/2) und die auf denselben normierten Zustand bezogene Amplitude

\[
A_\epsilon(\mu)=\langle\psi_\epsilon,D_\mu\psi_\epsilon\rangle
=E_{\delta,t}\chi(\mu C_\delta(t)/2),
\quad \chi(u)=\frac12+\frac{1-e^{-iu}}{2iu},\quad\chi(0)=1.
\]

Es handelt sich um einen ausdrücklich konditionalen Rückkehrvertrag, nicht um einen hergeleiteten physikalischen Detektor. |A|² ist die entsprechende mathematische Rückkehrwahrscheinlichkeit; es wird nicht nachträglich renormiert oder ein Dichtesektor umgewichtet.

Bei exakt festem stationärem Kragen ist C≡0 und A₀(μ)=1. Für jedes ε>0 ist C jedoch ein nicht identisch verschwindendes Polynom in (δ,t); seine Nullmenge hat Maß null. Daher gilt χ(μC/2)→1/2 fast überall für |μ|→∞. Mit |χ|≤1 liefert dominierte Konvergenz

\[
\lim_{|\mu|\to\infty}A_\epsilon(\mu)=\frac12\quad(\epsilon>0).
\]

Für festes μ gilt dagegen A_ε→1 bei ε→0. Folglich

\[
\lim_{|\mu|\to\infty}\lim_{\epsilon\to0}A_\epsilon=1,
\qquad
\lim_{\epsilon\to0}\lim_{|\mu|\to\infty}A_\epsilon=\frac12.
\]

Die zugehörigen iterierten Rückkehrwahrscheinlichkeiten sind 1 und 1/4. Dies widerspricht dem festen endlichen Atomgrenzsatz aus PR 265 nicht: Die Voraussetzung nichtidentischer Nullpolynome entfällt, wenn man den neuen Kragen exakt einstellt und seine Daten aus der Integration entfernt. Die Randklasse wurde geändert.

Für gekoppelte Folgen ε→0 gilt: μ ε→0 ergibt A→1; |μ|ε→∞ ergibt A→1/2. Für die zweite Aussage schreibe C=ε(L+εQ). L=ΣB(T−t)η ist ein nichtverschwindendes Polynom. Außerhalb seiner Nullmenge ist |μC|→∞; wieder gilt dominierte Konvergenz. Eine allgemeine Rate wird nicht behauptet.

## 8. Endliche, rigorose Amplitudenbudgets

Mit V=wC/2 sind EV=0 und EV²=EC²/24. Elementare reelle Exponentialreste liefern

\[
|A_\epsilon-1|\le d_\epsilon(\mu):=
\min\{2,\ |\mu|B_\epsilon/8,\ \mu^2EC^2/48\}.
\]

Also liegt die konditionale Rückkehrwahrscheinlichkeit in
\([\max(0,1-d_\epsilon)^2,1]\).
Der Code integriert die multivariaten Polynom-Momente bis Ordnung vier exakt mit rationalen Zahlen. Der Grad-vier-Taylor-Mittelpunkt ist
\(\sum_{k=0}^4(-i\mu)^kEV^k/k!\), mit EV⁰=1 und
\(EV^k=EC^k/[2^{k+1}(k+1)]\) für k>0. Ein gültiger komplexer Fehlerradius ist

\[
r_5\le |\mu|^5B_\epsilon^5/46080.
\]

Denn Ew⁵=1/12 und der reelle Exponentialrest hat Betrag höchstens |μV|⁵/5!. Diese Einschließungen brauchen weder Monte Carlo noch einen großen Integrationslauf.

## 9. Reproduzierbarkeit und nächste Entscheidung

Der Plan wurde nach analytischem Kandidatenentwurf, vor den endlichen Kontrollen eingefroren; er ist keine externe Präregistrierung. SHA-256:
`682435483bb05733b6a60591bcd1d0d19e869e303f5c6ccddc4893647e698b27`.

216 exakte Kettenfälle (135 gemeinsam stationär, 81 kurze nichtstationär), 2187 Randstörungsfälle, drei normierte Pakete mit Momenten bis Grad vier, zwölf Amplitudenbudgets und neun explizit zurückgewiesene Negativannahmen ergänzen die Beweise. Ketten mit bis zu acht festgehaltenen Vorgängern bedeuten hier nur eine einzelne freie Variationszeile; das ist kein n=5-Produktionslauf. Fünf Ergebnisdateien werden isoliert bytegleich nachgerechnet. Die Negativkontrollen testen definierte Fehlerannahmen; sie sind weder externe Replikation noch ein Beweisassistent.

Der nächste physikalische Schritt ist die Begründung einer Randpräparation samt Maß/Skalarprodukt und Randwirkung beziehungsweise gemeinsamer Randvariation. Sie müsste die Reaktionsbilanz tragen und entscheiden, ob die Momentfläche dynamisch ausgewählt wird. Ein willkürlich darauf eingeschränkter Träger wäre eine neue Modellannahme. Danach wäre eine zugehörige Constraint- und Observablenkonstruktion zu prüfen. Ein größerer Rechenlauf ersetzt diese fehlende Modellentscheidung nicht.

## Quellen und Abgrenzung

* Projektbasis: [PR 265](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/265); alle sechs übernommenen Dateien einschließlich Lizenz sind mit Git-Blob-Identitäten und Commit-URLs in `provenance.json` fixiert.
* [Benincasa und Dowker, 2010, arXiv:1001.2725](https://arxiv.org/abs/1001.2725), korrigierte Fassung: Hintergrund der kausalen skalaren Operatoren. Der hier geprüfte Staub- und Randvertrag ist eine zusätzliche Projektkonstruktion.
* [Brown und Kuchař, 1995, arXiv:gr-qc/9409001](https://arxiv.org/abs/gr-qc/9409001): eigenständige kanonische Staubkonstruktion; keine bereits gegebene Quantisierung des vorliegenden CST-Historienraums.
