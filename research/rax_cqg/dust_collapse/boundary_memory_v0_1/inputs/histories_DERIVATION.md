# CST-DUST: Positive Historien und Schnittkonsistenz v0.1

7. November 2026. Audit `CST-DUST-HISTORIES-CONSISTENCY-001`.
Basis: Main `d9622fb0423725026fab73d6884a499322cb014f`, nach PR 247.

## Ergebnis und Geltungsbereich

Ein stark positives **Hilfs-Dekohärenzfunktional** ist aus der vorhandenen
regulierten Amplitude, einem gewählten Anfangszustand und einem ausdrücklich
festgelegten positiven Randprodukt konstruiert. Der dazugehörige
Historien-Hilbertraum existiert nach Nullraumquotient und Vervollständigung.
Die Wahl des Randprodukts und seine physikalische Interpretation folgen dadurch
nicht aus der CST-Wirkung. Der physikalische Modellschluss bleibt HOLD.

Neu ist ein Hindernis auf den kontinuierlichen Randräumen: Jeder beschränkte
rohe Kern bei endlichen Regulatoren, endlichem N und endlichen positiven
Integrationsmaßen ist ein Hilbert-Schmidt-Operator. Er kann auf einem
unendlichdimensionalen L²-Eingangsraum keine Isometrie bis auf einen einzigen
positiven Skalar sein. Das gilt auch für beschränkt äquivalente positive
Randnormen. Ein konkreter Zweistellen-Kern bestätigt den Unterschied mit
normierten L²-Funktionen; Punktauswertung wird nicht benötigt.

Der Befund schließt eine bestimmte unbedingte Evolutions-/Schnittinterpretation
aus. Er ist kein No-go für CST, für singuläre Grenzkerne, eingeschränkte
physikalische Zustandsräume oder eine anders begründete kovariante Historientheorie.
Alle acht physikalischen Audit-Entscheidungen bleiben HOLD. Frühere spezifische
FAIL-Datensätze werden nicht überschrieben.

## 1. Expliziter Kandidatenvertrag

Für jedes feste endliche N bleiben die vollständigen Ordnungs-, Materie- und
relativen Uhrdaten einer Geschichte erhalten. Die geerbte Wirkung lautet

\[
S=S_g(C)-\frac12\sum_x w_x-\frac14\sum_{y\prec x}
w_xB_{xy}(T_x-T_y)^2.
\]

Die Gewichte w sind integrierte Dichtegewichte, keine bereits kalibrierten
Ruhemassen. Die endliche Geometriesumme enthält wie bisher den Faktor
1/|G_fix|, die Uhren besitzen regulierte positive Produktmaße und die Dichte
das geerbte atomar-stetige Maß. Es gibt keinen zusätzlichen Faktor zum
erneuten Dividieren durch dieselbe Labelgruppe.

Für das neue Hilfs-Randproblem wählen wir kompakte Randkonfigurationsräume
B_in, B_out mit endlichen positiven Maßen und
H_in=L²(B_in,dλ_in), H_out=L²(B_out,dλ_out). Diese sind **angenommene
Hilfs-Randräume**, nicht als physikalisch vollständige Cauchy-Räume bewiesen.
Insbesondere ist nicht gezeigt, dass sie die für nichtlokale CST-Wirkungen
benötigte gesamte Vorgeschichte tragen.

Die Ereignisdomäne ist zunächst die messbare Mengenalgebra der vollständigen
regulierten Patchhistorien. Physikalisch beanspruchte Ereignisse müssten
zusätzlich unter den zulässigen gemeinsamen Umbenennungen invariant sein.
Ein Ereignis E wird als Indikator im vollständigen Integranden eingefügt:

\[
K_E(b,a)=\frac1{|G_{fix}|}\sum_C\int d\nu_{C,b,a}(h)\,
\mathbf1_E(C,h,b,a)e^{iS(C,h,b,a)/\hbar},\quad
(C_E\psi)(b)=\int K_E(b,a)\psi(a)d\lambda_{in}(a).
\]

Die nichtnegative innere Maßmasse sei gleichmäßig endlich. Bei endlich vielen
Ordnungen, normierten kompakten Feldmaßen und reeller Wirkung ist
|K_E|≤M_N mit einem endlichen, von a,b,E unabhängigen M_N. Randzustände und
Ereignisse werden nicht aus einem gewünschten Bounce ausgewählt. Eine
Sektorsumme über unbeschränktes N, Regulatorentfernung oder Rand-GHY-Physik ist
hier nicht definiert. Die mathematische Konstruktion kann eine solche
physikalische Auswahl nicht ersetzen.

## 2. Positives Dekohärenzfunktional und Nullraum

Sei ρ ein positiver Spurklasseoperator auf H_in mit Tr ρ=1. Ein positives,
beschränktes M_out definiert das gewählte Ausgangsprodukt. Im berechneten
Referenzfall ist M_out=I. Setze

\[
D_0(E,F)=\operatorname{Tr}\bigl(\rho C_E^\dagger M_{out}C_F\bigr),
\quad Z_\rho=D_0(\Omega,\Omega),\quad D=D_0/Z_\rho\quad(Z_\rho>0).
\]

**Satz.** Für festes ρ und Z_ρ>0 ist D hermitesch, biadditiv, normiert und
stark positiv. Für beliebige endliche Ereignisfamilien E_i und Koeffizienten z_i:

\[
\sum_{ij}\overline{z_i}D(E_i,E_j)z_j
=\frac{\|M_{out}^{1/2}(\sum_i z_iC_{E_i})\rho^{1/2}\|_{HS}^2}{Z_\rho}\ge0.
\]

Hermitizität folgt durch Konjugation der Spur. Für disjunkte E,F gilt
C_(E∪F)=C_E+C_F durch Linearität der vollständigen Integration; daraus folgt
Biadditivität. Die Normierung folgt aus der Definition von Z_ρ. Bei Z_ρ=0
ist die normalisierte Definition nicht zulässig; es gibt keinen stillen Ersatz
durch eine kleine Zahl.

Auf dem freien komplexen Vektorraum der Ereignisse definiert D eine
semidefinite Form. Der Nullraum wird ausquotientiert, anschließend wird
vervollständigt. Dies ist die übliche Historien-Hilbertraumkonstruktion [1].
Sie erbt ihre physikalische Information aus D und begründet dieses nicht
rückwirkend. Der starke Positivitätsbegriff ist durch seine
Kompositionseigenschaften motiviert [2]; er allein wählt weder die
Staubdynamik noch das Randprodukt aus.

Für ein **festes** kompaktes Patch mit den obigen endlichen Maßen ist sogar
die Integration über seine messbaren Ereignisse kontrollierbar: Bei einer
monotonen Folge von Indikatoren konvergieren die beschränkten Kerne punktweise
und per dominierter Konvergenz in Hilbert-Schmidt-Norm. Damit konvergieren die
zugehörigen Ereignisvektoren. Diese Aussage betrifft weder unendliche
Wachstumshistorien noch einen Grenzübergang N→∞. Deren Fortsetzbarkeit ist
ein separates Problem [3].

### Kein automatisches Wahrscheinlichkeitsmaß

Für disjunkte E,F gilt

\[
\mu(E\cup F)=\mu(E)+\mu(F)+2\operatorname{Re}D(E,F),\quad \mu(E)=D(E,E).
\]

Starke Positivität und D(Ω,Ω)=1 beseitigen Interferenz nicht. Die Diagonalen
einer beliebigen Partition dürfen daher nicht als klassische
Bounce-Wahrscheinlichkeiten bezeichnet werden. Reelle Offdiagonalen müssen
für additive Wahrscheinlichkeiten verschwinden; die stärkere übliche
Dekohärenzforderung setzt die vollständigen Offdiagonalen null. Eine
physikalisch geeignete Ereignis-/Dekohärenzstruktur bleibt zu begründen.

## 3. Das verdoppelte relative Uhrmaß

Die positive Randkontraktion identifiziert den finalen Uhrwert in Bra und Ket.
Deshalb sind zwei getrennt reduzierte Einzelhistorien im Allgemeinen nicht
mit unabhängigen relativen Maßen zu integrieren.

Im Zweistellenbeispiel mit konstantem Eingangszustand stehen drei freie
Uhren a,a',b mit Maß da da' db/(2L)³. Die beiden Dichteintegrale bleiben
unabhängig. Setze r=a-b, r'=a'-b, s=b. Der Jacobi-Faktor ist eins und

\[
W^{(2)}_L(r,r')=
\frac{[2L-\{\max(0,r,r')-\min(0,r,r')\}]_+}{(2L)^3}.
\]

**Beweis:** Für festes r,r' muss s zugleich in [-L,L], [-L-r,L-r] und
[-L-r',L-r'] liegen. Die gemeinsame Länge liefert den Zähler. Daher ist
das Maß normiert und positiv. Seine Dimension ist Zeit⁻². Seine beiden
Marginalen sind die bekannten Dreiecksmaße, aber

\[
E[rr']=L^2/3,\qquad E[r^2]=E[(r')^2]=2L^2/3.
\]

Dies folgt direkt aus der gemeinsamen Uhr b. Das Produkt zweier unabhängiger
Dreiecksmaße hätte E[rr']=0 und wäre eine andere Randkontraktion. Nichtkonstante
Zustände, feste Randuhren und Ereignisindikatoren müssen **vor** der Integration
über s mitgeführt werden; dann genügt W^(2) allein im Allgemeinen nicht.

75 exakte Momentprüfungen vergleichen zwei unabhängige Herleitungen für
p,q=0,…,4 und L=1/2,1,2. Die erste expandiert (a-b)^p(a'-b)^q unter dem
ursprünglichen Produktmaß. Die zweite benutzt die sechs Ordnungskammern der
drei Uhren. Für die geordneten Abstände u,v≥0, u+v≤2L gilt pro Kammer

\[
\int\frac{u^pv^q(2L-u-v)}{(2L)^3}du\,dv
=(2L)^{p+q}\frac{p!q!}{(p+q+3)!}.
\]

Das ist die konkrete Umsetzung vollständiger relativer Randdaten im
verdoppelten Zweistellenproblem, keine neue Eichgruppenmittelung. Gemeinsame
Uhrverschiebungen lassen das Ergebnis bei Mittransformation von Regulator,
Zustand und Ereignissen unverändert. Ein frei verschobener Vakuumknoten wird
nicht zusätzlich ausquotientiert.

## 4. Der genaue Schnittkonsistenzsatz

Sei v_E ein Ereignisvektor am bisherigen Schnitt und J ein **bereits
hergeleiteter gemeinsamer linearer Fortsetzungsoperator**, sodass die gehobene
Geschichte den Vektor Jv_E erhält. M und M' seien die unabhängig festgelegten
Produkte an beiden Schnitten. Der erreichbare Raum V ist der lineare Abschluss
der Ereignisvektoren, nicht automatisch der gesamte Hilfsraum.

**Satz.** Die unnormierten Gramformen bleiben für alle Ereignispaare bis auf
denselben Skalar c>0 erhalten genau dann, wenn

\[
\langle v,(J^\dagger M'J-cM)w\rangle=0\quad\text{für alle }v,w\in V.
\]

Beweis: Die Gleichheit der Ereignis-Grammatrizen setzt sich sesquilinear auf
ihren Spann fort; Stetigkeit liefert den Abschluss. Die Rückrichtung folgt
durch Einsetzen der Ereignisvektoren. Für normierte D mit nichtverschwindenden
Gesamtnormen ist c=Z'/Z. Ein passender Skalar für einen einzigen Gesamtvektor
genügt nicht für alle Ereignispaare. Für sämtliche Anfangspräparationen müsste
auch diese Anforderung entsprechend erweitert werden.

Bei vollständigem V und M=M'=I ist die Bedingung J†J=cI. Verschiedene
physikalisch begründete Randprodukte und ein vergrößerter Ausgangsraum sind
zulässig. Eine offene Systementwicklung kann beispielsweise eine eigene
Umgebungs-/Krausstruktur erfordern; sie wird hier weder angenommen noch aus der
CST-Amplitude abgeleitet.

**Wesentliche Einschränkung:** Die Existenz dieses J ist für die nichtlokale
vollständige CST-Geschichte nicht bewiesen. Die frühere Wirkungsverklebung
rechtfertigt nicht automatisch einen Markov-Kern auf bloßen Randuhrwerten.
Der Satz ist ein prüfbares notwendiges und hinreichendes Kriterium **innerhalb
der angegebenen linearen Fortsetzungsdarstellung**, kein universelles
Unitäritätsaxiom aller kovarianten Historientheorien.

21 exakte Kontrollen unterscheiden unitäre und skaliert unitäre Fortsetzung
von diag(1,2). Letztere versagt auf dem vollen zweidimensionalen Spann, besteht
aber auf der ersten Koordinatenachse. Diese Positivkontrolle verhindert, dass
der erreichbare Unterraum stillschweigend mit dem gesamten Raum gleichgesetzt wird.

## 5. Kontinuierliches Kompaktheitshindernis

**Satz für die deklarierte Rohkernfamilie.** Wenn |K(b,a)|≤M_N, beide Randmaße
endlich und H_in unendlichdimensional sind, gilt

\[
\|K\|_{HS}^2=\int|K(b,a)|^2d\lambda_{out}(b)d\lambda_{in}(a)<\infty.
\]

Damit ist K kompakt. Für jede Orthonormalfolge φ_n gilt φ_n⇀0 und
||Kφ_n||→0. Wäre K†K=cI mit c>0, hätte jedes Bild stattdessen Norm √c.
Widerspruch. Dies beweist außerdem

\[
\|K^\dagger K-cI\|_{op}\ge c.
\]

Die Ungleichung folgt aus den Erwartungswerten an φ_n im Grenzwert.
Eine einzige skalare Normierung kann den Fehler deshalb nicht gleichmäßig
auf dem gesamten Eingangsraum klein machen.

Sind andere Randprodukte durch beschränkte positive Operatoren mit
beschränkt positiven Inversen gegeben, so ist
M_out^(1/2) K M_in^(-1/2) ebenfalls kompakt. Auch hier ist keine solche
Isometrie auf einem unendlichdimensionalen vollständigen Raum möglich.
Unbeschränkt umgewichtete, singuläre, distributionelle oder nach
Constraint-Reduktion wesentlich kleinere Räume sind nicht erfasst.

Der Beweis gilt bei jedem festen endlichen N oder endlicher Sektorsumme unter
dem angegebenen gleichmäßigen Kernlimit. Er entscheidet keine unendliche
N-Summe und keine Regulatorentfernung. Eine Folge kompakter Operatoren kann
stark gegen einen nichtkompakten Operator konvergieren: Projektionen auf die
ersten n Basisvektoren konvergieren stark gegen I, aber ihr Operatornormabstand
zu I bleibt eins. Ein begründeter Grenzprozess ist somit nicht ausgeschlossen;
er wäre auf Zustandsdomäne und Konvergenzart separat zu prüfen.

## 6. Zertifizierter Test mit echten L²-Randfunktionen

Der frühere Zweistellen-Kern wird als kontinuierlicher Integralkern verwendet:

\[
K(b,a)=G(1/2+(b-a)^2/4),\quad
G(q)=\frac12+\frac12\int_0^1e^{-iqw}dw.
\]

Anfangsdichte null, Enddichte mit dem bisherigen atomar-stetigen Maß integriert;
die gemeinsame Gravitationsphase fällt aus D heraus. Dies ist die eine
zulässige Zweistellenordnung, keine 4D-Raumzeit oder neue dynamische
Geometrieensemble-Rechnung. Im allgemeinen Satz bleibt L>0 frei; das
zertifizierte Rechenbeispiel benutzt **ausdrücklich L=1** und da/2, db/2.
Die frühere Hilfsbox L=4 wird nicht umgeschrieben.

Die normierten orthogonalen Eingänge φ₀(a)=1 und φ₁(a)=√3 a ergeben

| Größe | Zertifiziertes Intervall, konservativ verkürzt |
|---|---|
| Z₀=||Kφ₀||² | [0.94928176583590, 0.94928176583593] |
| Z₁=||Kφ₁||² | [0.00164658069420, 0.00164658069423] |
| Z₀/(Z₀+Z₁) | [0.99826844924727, 0.99826844924730] |

Die exakten rationalen und nach außen gerundeten 24-stelligen Grenzen stehen
in `results/continuum_certificates.json`. Aufgrund der gemeinsamen Parität
von Kern und Box ist ⟨Kφ₀,Kφ₁⟩=0 exakt, auch ohne Taylorabschneidung.

Eine Präparation mit einem **klassisch mitgeführten** Etikett 0/1 und je
Wahrscheinlichkeit 1/2 erhält nach Normierung auf das erfolgreiche K-Ergebnis
die Etikettwahrscheinlichkeit Z₀/(Z₀+Z₁), nicht 1/2. Dies ist legitime
Nachselektion eines Filters, aber keine unveränderte unbedingte Evolution.
Der Test ist keine Aussage über physikalische Staubwahrscheinlichkeiten.
Die Zustandsnormierung allein liefert daher nicht die fehlende
präparationsunabhängige Schnittregel. Allgemein ist D₀ linear in ρ, D₀/Z_ρ
aber nicht notwendigerweise affin in vorgegebenen Mischungsgewichten.

### Ereignisrechnung statt bloßer Gram-Behauptung

Für ψ=1 teilen drei disjunkte Anfangsuhrintervalle [-1,-1/3), [-1/3,1/3),
[1/3,1] die Historien in drei Atome. Der Endwert b bleibt vollständig
integriert. Diese drei Atome erzeugen acht Ereignisse. Ihre normierte
Grammatrix wird als kontinuierliches Dreifachintegral berechnet. Es gilt

\[
\sum_{i=1}^3D(E_i,E_i)\in
[0.33390672525746,\;0.33390672525750],\quad D(\Omega,\Omega)=1.
\]

Eine reelle Offdiagonale ist zertifiziert positiv. Die große Differenz ist
Interferenz; sie ist kein Normierungsfehler. 64 Hermitizitäts-, 432
Biadditivitäts-, eine Normierungs-, 64 Grad-zwei-Identitäten und 64 positive
quadratische Proben sind exakt ausgeführt. Die Identitäten werden für die
integrierten Taylorpolynome exakt geprüft; für den ungekürzten Kern folgen
sie aus der allgemeinen Gram-Konstruktion. Die endlichen Positivproben
ersetzen den allgemeinen Beweis nicht.

### Fehlerschranke

Auf dem Testgebiet gilt 1/2≤q≤3/2. Der Taylorgrad p=40 hat nach Integration
über w den gleichmäßigen komplexen Kernfehler

\[
r\le\frac{(3/2)^{p+1}}{2(p+1)!(p+2)}.
\]

Dies benutzt den Rest entlang der reellen Achse mit |d^k e^(-ix)/dx^k|=1.
Der konstante Vakuumanteil ist exakt. Alle verbleibenden Polynomialintegrale
sind rational komplex. Die normierten Maße und Cauchy-Schwarz geben für
normierte Eingänge einen Bildfehler höchstens r; für jede verwendete
Grammatrixkomponente genügt ε=2r+r². Positive Nenner werden vor jeder
Intervallteilung zertifiziert. Anzeigen werden nach außen gerundet; es gibt
keine angepasste statistische Toleranz.

25 rationale Werte vergleichen die direkte Potenzreihe in q unabhängig mit
der Expansion als Polynom in b-a. Ergänzend integrieren unabhängige
Gauss-Legendre-Rechnungen mit 64 und 96 Punkten die geschlossene Formel
G(q)=1/2+(e^(-iq)-1)/(-2iq). Diese Gleitkommakontrolle ist kein
Intervallzertifikat und kein Bestandteil der Standardbibliothek-Nachrechnung.

## 7. Entscheidungen und nächster physikalischer Modellschluss

| Aussage | Entscheidung |
|---|---|
| Endliches Hilfs-D mit deklariertem Randprodukt | PASS, konditional |
| Gemeinsames relatives Bra-/Ket-Uhrmaß | PASS, unter den angegebenen freien Uhren |
| Eine konstante Normierung des Rohkerns für alle kontinuierlichen Hilfszustände | FAIL in der angegebenen kompakten Kernfamilie |
| Diagonalen der geprüften interferierenden Partition sind klassische Wahrscheinlichkeiten | FAIL |
| Markov-Fortsetzung auf bloßen CST-Randuhren hergeleitet | Nein |
| Physikalisches D und geeignete Ereignisse | HOLD |
| Unendliche Historien-/Regulatorfortsetzung | NOT_EXECUTED |
| MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING, EXTENSION | jeweils HOLD im neuen Audit |

**Nächster konkreter Schritt:** Einen eigenständigen Vertrag für physikalische
Randdaten und zulässige Zustände festlegen, der die nötige nichtlokale
Vorgeschichte enthält, und einen daraus begründeten Fortsetzungs-/Verfeinerungspfad
angeben. Das positive Randprodukt darf nicht erst nachträglich passend zum
gewünschten Kern definiert werden. Ein kontrollierter eingeschränkter
Zustandssektor oder ein begründeter singulärer Grenzübergang sind mögliche
Forschungsrouten, hier aber nicht als bereits erfolgreiche Lösung ausgewählt.
Vor weiteren Bounce-Rechnungen ist an diesem Vertrag die Schnittkonsistenz
und die klassische Korrespondenz zu prüfen.

Es gibt keine Behauptung vollständiger Eichquantisierung, gravitativer
Anomaliefreiheit, eines CST-Junction-Gesetzes, gemeinsamer Außenraumdynamik
oder Singularitätsauflösung. Das Hilfs-Randproblem ersetzt nicht die
physikalische Stauboberfläche.

## 8. Reproduzierbarkeit und Quellen

`python3 -O -B analyze.py` reproduziert fünf exakte Ergebnisdateien mit der
Standardbibliothek. `replay.py` führt dies isoliert aus. `verify_quadrature.py`
ist die separate NumPy-Kontrolle. Der lokale Plan wurde vor der Rechnung
gehasht; die wesentlichen Mechanismen waren bekannt. Keine externe
Präregistrierung, kein blinder Test. `supplement_01.json` legt die nach dem
ersten Kernlauf ergänzten gemeinsamen Maßmomente und Quadraturen offen.
Ein anfänglicher Implementierungslauf brach wegen einer fehlenden skalaren
Divisionsmethode ab, bevor Ergebnisdateien geschrieben wurden; nach der
Korrektur wurden dieselben geplanten Kriterien verwendet.

Die fünf Vorgängertexte wurden **bytegleich** übernommen; ihre SHA-256-Werte
und der konkrete Main-Commit stehen in `inputs/provenance.json`. Die frühere
LF-Präzisierung im Gauge-Paket bleibt unverändert in dessen Originaltext
enthalten. Keine alten Artefakte oder Ergebnisdatensätze werden ersetzt.

1. F. Dowker, S. Johnston, R. D. Sorkin, *Hilbert Spaces from Path Integrals*,
   J. Phys. A 43, 275302 (2010), [arXiv:1002.0589v3](https://arxiv.org/abs/1002.0589v3).
   Allgemeiner Historien-Hilbertraum; kein spezifisches CST-Staubmodell.
2. F. Dowker, H. Wilkes, *An Argument for Strong Positivity of the Decoherence
   Functional*, [arXiv:2011.06120v2](https://arxiv.org/abs/2011.06120v2).
   Motivation über Komposition; keine Auswahl unseres Randprodukts.
3. F. Dowker, S. Johnston, S. Surya, *On extending the Quantum Measure*,
   J. Phys. A 43, 505305 (2010), [arXiv:1007.2725v1](https://arxiv.org/abs/1007.2725v1).
   Die unendliche Ereignisfortsetzung ist eine zusätzliche Frage.

Die Kompaktheits-, Normierungs-, Schnitt- und Maßargumente sind oben
ausgeführt. Sie werden nicht als neues allgemeines Naturgesetz oder als
literaturbelegte physikalische CST-Lösung ausgegeben.
