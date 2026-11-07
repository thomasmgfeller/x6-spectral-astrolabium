# CST-DUST: Uhrsymmetrie, Constraints und Atomgrenze v0.1

Stand: 7. November 2026. Basis: Main nach PR 264,
`0ee861d67f7d28e2c2762ef01e70f428796f1f53`.

**Ergebnis:** Die vorhandene Materiewirkung begründet eine gemeinsame
Uhrverschiebungsidentität und einen Variationsstrom. Daraus folgt nicht die
binäre Sektorladung des zusätzlichen Referenzmodells. Im geankerten
Historienmodell scheitert bereits am ersten freien Element eine innere
klassische Staub-Normierung. Ihre ungeprüfte Übertragung auf Quantenzustände
ergibt entweder einen leeren Raum oder nur das Dichte-Nullatom. Der regulierte
Amplitudenkandidat selbst legt diese Operator-Constraints nicht fest. Bei
starker Materiephase besitzt seine Materieamplitude für festes endliches n den
Grenzwert 2^(-n), der aus dem ursprünglichen Atomanteil folgt.

Dies ist ein bedingter Audit des vorhandenen Rand- und Maßmodells, kein
CST-No-go, kein physikalisch ausgewählter Zustandsraum und kein Bounce.
Alle acht physikalischen Gates bleiben **HOLD**.

## 1. Zwei deklarierte Gebiete auseinanderhalten

Die gepinnte Variation verwendet feste endliche Kausalordnungen und absolute
kompakte Uhrfenster. Die spätere geankerte Historienreihe verwendet einen
Anfangsanker \(T_0=-2,w_0=0\), n neue Elemente und
\(T_j=T_0+4h x_j\), \(0<x_1<\cdots<x_n<1\).
Der Anker ist Vorgänger jedes neuen Elements; die übrige Ordnung ist natürlich
beschriftet. Das normierte Uhrmaß ist \(n!d^nx\) auf diesem Simplex. Es wird
hier keine zusätzliche physikalische Identität dieser beiden Randverfahren
behauptet. Die jeweilige Domain ist Bestandteil des Amplitudenkandidaten.

Mit dem angegebenen BD-Vorfaktor A=1 lauten die geerbten Formeln

\[
\Gamma_x=\frac12\sum_{y\prec x}B_{xy}(T_x-T_y)^2,\quad
C_x=1+\Gamma_x,\quad a_x=C_x/2,\quad S_d=-\sum_x w_x a_x,
\]

\[
B_{xy}=b(k_C(y,x)),\qquad b=(1,-9,16,-8,0,\ldots).
\]

Alle Beziehungen sind in der projektspezifischen Normierung zu lesen. Das
integrierte Gewicht w hat die Dimension Wirkung, keine Ruhemasse. Eine
physikalische Masse, ein kanonischer Phasenraum und eine quantisierte
Constraintalgebra sind nicht durch diese Formeln allein gegeben.

## 2. Was aus der Uhrsymmetrie folgt

Weil die Wirkung nur Uhrdifferenzen enthält, gilt exakt
\(S_d(T+c\mathbf1,w)=S_d(T,w)\). Ihre Ableitung liefert

\[
j_{y\to x}=\tfrac12w_xB_{xy}(T_x-T_y),\qquad
q_z=\partial_{T_z}S_d=\sum_{z\to x}j_{z\to x}-\sum_{y\to z}j_{y\to z},
\quad\sum_z q_z=0.
\]

Für jede Teilmenge U heben sich innere Ströme weg:
\(\sum_{z\in U}q_z=\sum_{U\to\bar U}j-\sum_{\bar U\to U}j\).
Ein freier stationärer Uhrpunkt erfüllt \(q_z=0\). Dies ist eine gerichtete,
gegebenenfalls vorzeichenbehaftete Variationsbilanz. Die alternierenden
BD-Gewichte erlauben keine automatische Interpretation als positive Staubmasse.

Die Verschiebung bewegt T, lässt aber w unverändert. Auf einem zusätzlich
gewählten unbeschränkten kinematischen Uhrraum würde die Translation durch
\(-i\hbar\sum_z\partial_{T_z}\) erzeugt. Dieser Ableitungsoperator ist nicht
der auf w wirkende Multiplikationsprojektor \(\Pi_c\). Auf kompakten Fenstern
benötigen Translationsgeneratoren eigene selbstadjungierte Randbedingungen;
diese wurden nicht ausgewählt. Dass \(\Pi_c\) mit Record-Multiplikation und
Uhrtranslation kommutiert, macht ihn weder zur Noetherladung noch zentral in
der vollständigen physikalischen Algebra.

Eine starre Symmetrie einer Wirkung ist außerdem nicht allein ein Nachweis
lokaler Eichfreiheit. Fixierte äußere Uhrdaten, Präparationen und Messungen
müssen mitbehandelt werden. Die kanonische Staub-Deparametrisierung von Brown
und Kuchař [2] verfügt über eine eigene gekoppelte Constraintstruktur; sie
ist hier nicht durch Austausch eines Symbols übernommen.

## 3. Der erste freie Dichtepunkt hat keinen Normierungssattel

Im offenen positiven Stratum lautet die klassische innere Variation
\(\partial_{w_j}S_d=-C_j/2\). Ein innerer stationärer Punkt verlangt
\(C_j=0\). Für das erste freie Element j=1 ist der einzige Vorgänger der
Anker. Sein Intervall enthält kein weiteres Element, daher \(B_{10}=1\) und

\[
C_1=1+\tfrac12(T_1-T_0)^2
=1+8h^2x_1^2\ge1.
\tag{1}
\]

Diese Ungleichung gilt für jede natürliche Ordnung und jede Anzahl neuer
Elemente n≥1 im angegebenen Ein-Anker-Modell. Der positive Vorfaktor A würde
die Aussage erhalten. Somit existiert dort kein vollständiger reeller innerer
Sattel mit frei variiertem positivem \(w_1\). Das frühere Problem am minimalen
Element verschwindet nicht bereits durch einen einzigen davorliegenden Anker.
Das Atom w=0 besitzt keine entsprechende infinitesimale Dichtevariation;
Endpunkte und verschiedene Trägerstrata dürfen nicht gleichgesetzt werden.

Die Aussage ist randmodellabhängig. Ein zusätzlicher analytischer Zeuge zeigt
dies auf der Kette 0≺1≺2. Halte \(T_0=0,T_1=7/18\) fest und setze
\(T_2=17/36\). Für das freie Element 2 gilt

\[
\Gamma_2=\tfrac12[(T_2-T_1)^2-9(T_2-T_0)^2]=-1.
\]

Ein längerer fixierter Vergangenheitskragen kann die Normierung also überhaupt
erst ermöglichen. Dieser Zeuge liegt außerhalb des vorher fixierten
Kontrollgitters und wurde nach dessen Auswertung analytisch ergänzt. Er ist
keine geprüfte Reparatur: Bei \(w_0=w_1=0,w_2=1/2\) bleibt
\(q_2=25/24\ne0\). Ein vollständiger Sattel, ein physikalischer Randzustand
und dessen Geometrie sind damit nicht gefunden.

## 4. Drei zusätzliche Operator-Constraints und ihre verschiedenen Folgen

Betrachte den bisherigen kinematischen Hilbertraum einschließlich aller
Uhrmoden und des Maßes \(\nu(dw)=\tfrac12\delta_0+\tfrac12dw\) auf (0,1).
Auf dem kompakten Bereich ist \(C_1\) beschränkt und mindestens eins. Die
folgenden Multiplikationsoperatoren können mathematisch definiert werden;
**keiner wird dadurch zu einer hergeleiteten physikalischen Dirac-Bedingung**.

| Zusätzliche Bedingung | Exakter Kern | Problem für das bisherige kohärente Ziel |
|---|---|---|
| \(M_{C_1}\psi=0\) auf dem ganzen Raum | {0} | Verlangt auch am Nullatom eine dort nicht vorhandene Tangentialgleichung. |
| \(\Pi_c M_{C_1}\psi=0\) | erster Dichtewert w₁=0, übrige Moden frei | Jeder positive erste Dichteanteil wird ausgeschlossen. |
| \(M_{w_1C_1}\psi=0\) | derselbe Atom-Unterraum | Ohne Spektrallücke können kleine Residuen physikalische Nähe vortäuschen. |

Für die erste Zeile gilt \(\|C_1\psi\|\ge\|\psi\|\). Für die zweite
ist der Operator auf dem positiven Stratum ebenfalls mindestens eins. Für die
dritte ist \(w_1C_1>0\) fast überall auf dem positiven Stratum; dort gibt es
keinen exakten Nullvektor. Weil w beliebig nahe an null liegen kann, gibt es
aber normierte approximative Nullfolgen.

Ein explizites Beispiel ist n=1,h=1/2, \(C_1(x)=1+2x^2\). Definiere
\(\psi_\epsilon(x,w)=\sqrt{2/\epsilon}\,1_{(0,\epsilon)}(w)\),
am Atom null, bei normiertem Gleichmaß dx. Dann

\[
\|\psi_\epsilon\|=1,\quad\Pi_a\psi_\epsilon=0,\quad
\|C_1\psi_\epsilon\|^2=47/15,\quad
\|wC_1\psi_\epsilon\|^2=47\epsilon^2/45\to0.
\tag{2}
\]

Der Abstand zum Atomkern bleibt eins. Für aufeinanderfolgende halbierte
Epsilonwerte beträgt das Überlappungsquadrat 1/2; die Folge ist nicht
normkonvergent. Sie konvergiert schwach gegen null, weil für jede feste
L²-Testfunktion die Norm auf (0,ε) gegen null geht. Das entspricht keiner
normierten physikalischen Zustandsgrenze. Der balancierte konstante Zielzustand
hat im selben Beispiel das positive gewichtete Residuum \(47/90\).

Diese Ergebnisse schließen die konkrete naive Constraintübertragung im
gegebenen Randmodell. Sie entscheiden nicht die tatsächliche CST-Quantisierung.
Falls die spätere physikalische Theorie einen anderen Raum wählt, müssen
Messziel und Referenzvertrag darauf neu definiert werden.

## 5. Ward-Identität mit tatsächlichem Integrationsrand

Für einen freien Uhrwert in einer **festen absoluten** Box gilt

\[
\int_{-L}^{L}\frac{dT}{2L}
\left(\partial_T f+\frac{i}{\hbar}f q_T\right)e^{iS/\hbar}
=\frac{[f e^{iS/\hbar}]_{-L}^{L}}{2L}.
\tag{3}
\]

Für mehrere freie Uhren, festen Träger, feste Maße und äußere Uhrdaten b
folgt aus \(\sum_z\partial_{T_z} e^{iS/\hbar}=0\), dass die Summe der
äußeren Ableitungen der Amplitude gleich minus der Summe ihrer freien
Boxrandterme ist. Eine randfreie Ward- oder Zwangsgleichung benötigt daher
zusätzliche Begründung.

Ein nichttrivialer Ein-Link-Test integriert w bereits exakt. Mit
\(a(t-b)=1/2+(t-b)^2/4\), \(K_L(b)=(2L)^{-1}\int_{-L}^{L}\chi(a(t-b))dt\)
und \(\mu=\hbar=W=1\) gilt

\[
K_L'(b)=-\frac{\chi(a(L-b))-\chi(a(-L-b))}{2L}.
\tag{4}
\]

Bei b=1/2,L=1 sind die Argumente 9/16 und 17/16; der Imaginärteil dieser
Ableitung ist mit rationalen Einschlüssen strikt negativ. 117 unabhängige
Koeffizientenvergleiche prüfen (4) bis Ordnung 12, indem links die integrierten
Polynome nach b abgeleitet und rechts die Endpunkte ausgewertet werden.

**Keine Verwechslung mit dem geankerten Produktionsfenster:** Werden alle
Uhren einschließlich Anker und Grenzen gemeinsam verschoben, bleibt das
relative Fenster \(T_j=T_0+4h x_j\) gleich parametrisiert und die Amplitude
exakt invariant. Gleiches gilt für die geordneten Uhrdifferenzen und ihren
Jacobian. Der Boxrandtest beweist keine Verletzung dieser gemeinsamen
Translationsinvarianz. Er zeigt, warum festgehaltene absolute Ränder nicht
still verschwinden dürfen.

## 6. Das bereits verwendete Dichteintegral ist keine Delta-Bedingung

Die analytische Elimination der linearen Dichtegewichte ist **bereits** im
veröffentlichten Vier-Element-Kern enthalten [1]. Es wird keine zusätzliche
Dimensions- oder Laufzeiteinsparung daraus beansprucht. Für das geerbte Maß
und \(u=\mu aW/\hbar\) lautet der Faktor

\[
\chi(u)=\frac12+\frac12\int_0^1e^{-iut}dt
=\frac12+\frac{1-e^{-iu}}{2iu},\qquad\chi(0)=1.
\tag{5}
\]

Er ist glatt und keine Distribution \(\delta(a)\). Stärker noch:

\[
\operatorname{Re}\chi(u)=\tfrac12+\tfrac12\frac{\sin u}{u}
\ge\frac{1-1/\pi}{2}>\frac13
\quad\text{für alle reellen }u.
\tag{6}
\]

Beweis: Für |u|≤π ist sin(u)/u≥0. Für |u|>π ist es mindestens
−1/|u|≥−1/π. Bei u=0 gilt die stetige Fortsetzung. Damit verschwindet kein
einzelner Dichtefaktor auf der reellen Achse. Insbesondere projiziert das
regulierte Integral den nach (1) verbotenen klassischen Normierungssattel
nicht als exakte Quantenbedingung aus. Andere Integrationen können weiterhin
Interferenznullstellen verursachen; (6) ist keine globale Amplitudenuntergrenze
für beliebige Produkte oder Geometriesummen.

Für a≠0 liefert das Vergrößern des **normierten** Dichtefensters W→∞ den
Grenzwert 1/2, nicht eine Deltafunktion. Eine andere Multiplikatorintegration
oder ein anderes Maß würde einen anderen Quantisierungskandidaten definieren
und benötigt eine eigene physikalische Begründung.

## 7. Exakte Atomgrenze bei starker Materiephase

Für jede feste endliche geankerte Ordnung p mit n neuen Elementen ist die
Materieamplitude ohne den äußeren Gravitationsphasenfaktor

\[
A_p(\mu)=n!\int_{0<x_1<\cdots<x_n<1}
\prod_{j=1}^{n}\chi(\mu a_j(x))\,d^nx.
\]

Jedes \(a_j(x)=1/2+4h^2\sum_{y\prec j}B_{jy}(x_j-x_y)^2\) ist ein
nicht identisch verschwindendes Polynom: Bei zusammenfallenden Uhrwerten
am Ursprung hat es den Wert 1/2. Seine Nullmenge besitzt daher Lebesgue-Maß
null. Außerhalb der endlichen Vereinigung dieser Nullmengen gilt
\(\chi(\mu a_j)\to1/2\). Gleichzeitig ist \(|\chi|\le1\), weil (5) die
charakteristische Funktion eines positiven normierten Maßes ist. Dominierte
Konvergenz im normierten Uhrmaß beweist

\[
\boxed{\lim_{|\mu|\to\infty}A_p(\mu)=2^{-n}.}
\tag{7}
\]

Der überlebende Term ist das Stratum, in dem alle integrierten Dichtegewichte
null sind; sein Maßgewicht ist 2^(-n). Das ist noch kein physikalisch
identifizierter Vakuumzustand. Bei n=1,2,3 lauten die Grenzwerte 1/2,1/4,1/8.
Die Aussage gilt auch für andere feste endliche n, verlangt dafür aber keinen
numerischen Produktionslauf. Sie liefert keine uniforme Konvergenzrate über
alle Geometrien und n, keine Vertauschung mit einer unendlichen n-Summe und
keinen gravitativen oder physikalischen semiklassischen Grenzwert. Bei zugleich
skalierter Gravitationsphase kann die vollständige komplexe Amplitude weiter
oszillieren.

Für den ersten Dichtefaktor ist zusätzlich eine einfache uniforme Schranke
verfügbar. Aus \(|\chi(u)-1/2|\le\min(1/2,1/|u|)\) und \(a_1\ge1/2\)
folgt bei W=ℏ=1:

\[
\left|A_p(\mu)-\tfrac12A_p^{(w_1=0)}(\mu)\right|
\le\min(1/2,2/|\mu|).
\tag{8}
\]

Hier integriert \(A_p^{(w_1=0)}\) weiterhin alle Uhren und übrigen Dichten;
es ist kein verkleinertes Kausalset, weil die Uhr des ersten Elements in
späteren Wirkungszeilen bleibt. Bei |μ|=16,64,256 sind die Schranken 1/8,
1/32,1/128. Sie begrenzen nur den positiven ersten Dichtestratum-Beitrag,
nicht den gesamten Rest zur Grenze 2^(-n) für n>1.

## 8. Kontrollen und Konsequenz für den nächsten Vertrag

Der vor den endlichen Kontrollen eingefrorene Plan hat SHA-256
`e492ce4b3735ff4c1f346f2e2d3606e416c9509a6f9743477472064a18392c08`.
Er ist keine externe Präregistrierung. Die zusätzliche Kragenkonstruktion in
Abschnitt 3 ist als nachträglicher analytischer Zeuge getrennt ausgewiesen.

Die Python-Standardbibliothek genügt. Kontrollen: 270 Wirkungsfälle mit bis zu
drei neuen Elementen, 972 exakte Ableitungskomponenten, 810 gemeinsame
Uhrverschiebungen, 3564 Schnittbilanzen, 90 erste-Dichtepunkt-Fälle,
vier approximative Nullzustände, 117 Ward-Koeffizienten und zehn komplexe
charakteristische Funktionswerte mit rationalen Fehlerradien. Die Funktion
exp(−iu) wird bis |u|≤1 heruntergeteilt, mit Taylorgrad 48 eingeschlossen und
durch wiederholtes Quadrieren zurückgeführt. Jede Rundung auf 40 Dezimalstellen
wird dem Fehlerradius nach außen zugeschlagen. Für ein Quadrieren gilt
\(r_{neu}\le2r+r^2\) vor dem zusätzlichen Rundungsbeitrag. Es werden keine
Gleitkommawerte als Zertifikate ausgegeben.

Acht Negativkontrollen weisen die konkreten Fehlinterpretationen zurück.
Fünf Ergebnisdateien einschließlich der zusammenfassenden Verifikation
werden isoliert bytegleich nachgerechnet. Das ist keine externe Replikation
oder Beweisassistentenprüfung. Kein n=5-Produktionslauf und keine
kostenpflichtige Rechenleistung werden gestartet.

Der nächste physikalische Vertrag muss zuerst **Vergangenheitskragen und
Randzustand, zulässige Dichtevariation und Quantisierungsregel** gemeinsam
bestimmen. Ein frei gewählter Multiplikations-Constraint oder die bloße
Sektorladung aus dem Referenzmodell darf diese Entscheidung nicht ersetzen.
Der aktuelle Kandidat kann als reguliertes Amplitudenmodell weiter untersucht
werden, trägt aber noch keine daraus hergeleitete physikalische Algebra.
MODEL, BOUNDARY, CURRENT, CORRESPONDENCE, TRAPPING, REGULARITY, EXTENSION und
BOUNCE bleiben HOLD.

## Primärquellen

1. [Projektstand nach PR 264](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/264),
   sechs unverändert kopierte Dateien mit Commit-URLs und Git-Blob-Identitäten
   in `provenance.json`. Insbesondere die Variation, der Referenzvertrag und
   der Vier-Element-Kern bestimmen hier den geprüften Kandidaten.
2. J. D. Brown, K. V. Kuchař,
   [Dust as a Standard of Space and Time in Canonical Quantum Gravity](https://arxiv.org/abs/gr-qc/9409001),
   Phys. Rev. D 51, 5600 (1995). Vergleich für eine eigene kanonische
   Staub- und Constraintkonstruktion; keine bereits vorhandene CST-Ableitung.
3. D. M. T. Benincasa, F. Dowker,
   [The Scalar Curvature of a Causal Set](https://arxiv.org/abs/1001.2725),
   Phys. Rev. Lett. 104, 181301 (2010), korrigierte arXiv-Fassung.
   Bezug für kausale skalare Operatoren und den formalen Kontinuumsoperator;
   keine Quelle für die hier zusätzlich untersuchte Quantisierung des
   Staub-Historienraums oder dessen physikalische Randbedingungen.
