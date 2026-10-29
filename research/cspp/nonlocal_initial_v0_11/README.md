# Nichtlokaler Anfangsdatenadapter v0.11

Ein prüfbarer Adapter für die unveränderten Cauchy-Daten des CSPP-Piloten.
Er verwendet eine echte orthogonale Projektion mit überlappenden Gewichten,
eine ausdrücklich deklarierte zeitliche Fortsetzung und Fehlergrenzen bis
zur bisherigen Detektorantwort. **Gesamtstatus: METHOD_HOLD.**

Die Konstruktion beseitigt den strukturellen vollständigen Quellverlust
lokaler Stützpunktabtastung. Sie qualifiziert die vorhandene räumliche
Auflösung und die eingesetzte lineare History jedoch nicht. Die genaue
Ergebnistabelle steht in [RESULTS.md](RESULTS.md); reproduzierbare Rohdaten,
Ballintervalle und Prüfentscheidungen stehen unter `results/`.

## 1. Vertrag und unveränderte Eingaben

Ausgangspunkt ist Commit `e6cd855da6ca9860f8bed0e1450da3db22f2e60b`,
[PR 142](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/142).
Verwendet werden dieselben acht Wolken `d0_r00` bis `d0_r07`, ausschließlich
deren ursprüngliche History-Knoten mit t <= -1 und die vorhandenen
zertifizierten Detektortransferintervalle von v0.10. Keine Wolke wird neu
gezogen; kein Raumzeitknoten wird eingefügt oder verschoben. Masse 1,
Quelldaten, Dichte, Gebiet, Detektor und beide Zeitfenster bleiben erhalten.

Die kompakte Quelle lautet weiterhin

\[
 f(x)=A\exp\!\left[-\frac{1}{1-4|x|^2}\right]e^{4iz}
 \quad (|x|<1/2),\qquad f=0\text{ sonst},\quad g=0.
\]

Das ursprüngliche A normiert die globale L2-Norm von f auf eins.
Die Rechnung erfolgt in Einheiten der bisherigen Amplitude A/e; dies
ändert die physikalische Quelle nicht. Für die Wellen gilt
f_k=exp(ikz), g_k=-i sqrt(1+k²) f_k, k=0,2,4,8. Insbesondere wird bei den
Wellen g nicht auf null gesetzt.

**Informationsvoraussetzung:** Der Adapter erhält die ursprünglichen
Funktionen bzw. zertifizierbare Integrale gegen diese Funktionen. Eine
Liste ihrer Werte an vorhandenen Knoten allein reicht nicht: Ein glatter
Bump in einer knotenfreien offenen Menge hat dieselben Abtastwerte wie die
Nullfunktion. Kein linearer oder nichtlinearer Adapter dieser Werteliste
kann beide Daten unterscheiden. Die neue Information kommt aus den
vorgegebenen f,g, nicht aus neu erzeugten Raumzeitpunkten.

Der Adapter ist ein **Koordinatenadapter im vorhandenen Minkowski-Chart**.
Räumliche Projektionen der History-Knoten werden als Basisorte benutzt.
Dies ist keine intrinsische, allein aus der Kausalordnung gewonnene
Anfangswertformulierung. Integrationspunkte sind Hilfspunkte für Integrale,
keine zusätzlichen Kausalsetknoten.

## 2. Explizite überlappende Gewichte

Seien q_i die räumlichen Koordinaten der N History-Knoten. Setze
D=conv{q_i}. Eine konforme Tetraederzerlegung dieses Körpers benutzt
ausschließlich diese vorhandenen Orte. Auf ihr ist w_i die stetige
stückweise affine Hutfunktion mit w_i(q_j)=delta_ij. Auf jedem Tetraeder
sind die vier beteiligten w_i dessen baryzentrische Koordinaten:

\[
 w_i\geq0,\qquad \sum_i w_i(x)=1\ (x\in D),\qquad
 V_h=\operatorname{span}\{w_1,\ldots,w_N\}.
\]

Im Inneren eines Tetraeders überlappen vier Gewichte. Die Stütze jedes
Gewichts ist der Stern seiner angrenzenden Tetraeder; die ganze Basis ist
linear unabhängig, weil sie an den Knoten die Einheitsmatrix ergibt.

SciPy schlägt die Zerlegung lediglich vor. Mit exakten rationalen
Darstellungen der ursprünglichen binary64-Koordinaten prüft der Adapter:
positive Tetraedervolumina, keine doppelten Tetraeder oder Orte, Verwendung
aller Orte, entgegengesetzte Orientierungen jeder inneren Fläche, streng
stützende Randflächen sowie geschlossenen verbundenen konvexen Rand.
Diese positive orientierte 3-Kette mit konvexem Rand überdeckt ihren
konvexen Körper mit Multiplizität eins. Eine überlappende oder lückenhafte
Zerlegung würde diese Ketten-/Randbedingungen verletzen. Bei Mehrdeutigkeit
oder Entartung folgt GEOMETRY_HOLD; es gibt kein Jitter und keinen Ersatzort.

Zusätzlich wird exakt geprüft, ob die geschlossene Quellkugel B_(1/2)(0)
in D liegt. Für jede orientierte Randebene n.x=b müssen Ursprung und
Innenraum auf derselben Seite liegen und b² >= |n|²/4 gelten.

## 3. Die echte nichtlokale Projektion

Definiere für beliebiges u in L2(D)

\[
 M_{ij}=\int_D w_iw_j\,dx,\qquad
 b_i(u)=\int_D w_i u\,dx,\qquad
 c(u)=M^{-1}b(u),\qquad P_hu=\sum_i w_i c_i(u).
\]

Auf einem Tetraeder K ist die lokale Massenmatrix exakt

\[
 M^K_{ij}=\frac{|K|}{20}(1+\delta_{ij}),\quad i,j\in K.
\]

M ist symmetrisch positiv definit: a*Ma=||sum a_i w_i||², und diese Norm
verschwindet aufgrund der nodalen Unabhängigkeit nur für a=0.
Die Gleichung Mc=b ist genau die Orthogonalitätsbedingung
<u-P_hu,v_h>=0 für alle v_h in V_h. Deshalb gelten

\[
 P_h^2=P_h,\quad P_h1=1,\quad
 \|P_hu\|_{L^2(D)}\leq\|u\|_{L^2(D)},\quad
 \int_D P_hu=\int_D u.
\]

Die Integralidentität folgt durch Testen mit 1 in V_h. Sie ist
Konservativität des räumlichen Feldintegrals, keine Behauptung über
Energie-, Wahrscheinlichkeits- oder diskrete KG-Stromerhaltung.

**Nichtlokalität:** c_i hängt über die Integralrechte und M^-1 von
Quelldaten jenseits des eigenen Knotens ab. Es wird ausdrücklich nicht
b_i durch M_ii f(q_i) oder eine lokale Wertemischung ersetzt. M^-1 kann
negative und weitreichende Kopplungen besitzen. Positive Hutfunktionen
implizieren daher weder Positivität der Projektionskoeffizienten noch
L-infinity-Kontraktivität der orthogonalen Projektion.

Wenn D die Quellkugel enthält, ist für die kompakte Quelle

\[
 \int_D f=4\pi A\int_0^{1/2}r^2
 e^{-1/(1-4r^2)}\operatorname{sinc}(4r)\,dr>0.
\]

Denn 0 <= 4r <= 2 < pi und der Radialfaktor ist innen positiv.
Integralbewahrung erzwingt also P_h f != 0, auch wenn alle f(q_i)=0.
Da w_i(q_j)=delta_ij, sind dann auch nicht sämtliche übertragenen
History-Anfangswerte null. Dies beweist keine von null verschiedene
Detektorantwort; diese kann durch Dynamik oder Auslöschung verschwinden.

## 4. Räumliche Fehlergrenzen und Auflösung

Die Projektion ist die beste Approximation in diesem festgelegten Raum:

\[
 \|u-P_hu\|_2^2=\|u\|_2^2-b(u)^*M^{-1}b(u)
 =\min_{v_h\in V_h}\|u-v_h\|_2^2.
\]

Diese Identität liefert ein auswertbares Fehlerintervall, nicht nur einen
Vergleich zweier Gitter. Es wird mit der unabhängigen analytischen Grenze
0 <= ||u-P_hu||²/||u||² <= 1 geschnitten. Bei Wellen ist ||f_k||²=|D|.
Für die amplitude-normalisierte kompakte Quelle ist ||f/(A/e)||²=e²/A²,
sofern die Quellkugel in D liegt. Die zertifizierte ursprüngliche
Normalisierung wird aus v0.10 übernommen.

Ein Fehlerintervall vollständig über der Toleranz ist ein belegter
Auflösungsfehler dieses Raums. Ein breites Intervall, dessen Obergrenze
nicht passt, ist lediglich RESOLUTION_HOLD. Es darf nicht als gemessener
Fehler oder Fehleruntergrenze ausgegeben werden.

Für glattes u folgt zusätzlich mit dem nodalen Interpolanten I_hu und
H_K=sup_K ||D²u||_op aus Taylor und der affinen Reproduktion:

\[
 |u(x)-I_hu(x)|\leq\frac{H_K}{2}
 \sum_{i\in K}w_i(x)|q_i-x|^2\leq\frac{H_Kh_K^2}{2},
\]
\[
 \|u-P_hu\|_2\leq\frac12
 \left(\sum_K |K|H_K^2h_K^4\right)^{1/2}.
\]

Hier ist h_K der tatsächliche Tetraederdurchmesser, kein nomineller
mittlerer Knotenabstand. Für komplexe Felder bezeichnet H_K eine Schranke
der komplexen bilinearen Hessianform. An beliebigen x in K gilt ferner
|P_hu-u| <= sum w_i |c_i-u(q_i)| + H_K h_K²/2. Der ausführbare
History-Vertrag benötigt nur die direkt eingeschlossenen nodalen Fehler.

Ein exakter Negativkontrollfall zeigt, warum ein erhaltenes Signal kein
Auflösungsnachweis ist. Auf einem Tetraeder sei u=product_(i=0)^3 lambda_i.
Alle vier Knotenwerte sind null, aber P_hu=1/840. Gleichzeitig gilt

\[
 \frac{\|u-P_hu\|_2}{\|u\|_2}
 =\sqrt{\frac{23}{56}}\simeq0.641.
\]

Der Adapter erhält also Quellinformation und weist dennoch eine
unzureichende Rekonstruktion aus. Dieser Fall ist ein analytischer Test,
nicht die physikalische Quelle und kein zusätzlicher Archivlauf.

## 5. Zeitliche History: notwendige Zusatzannahme

Ein allgemeiner retardierter nichtlokaler Operator benötigt Daten in
einer Vergangenheitsschicht. f und g auf t0 bestimmen diese History
ohne weiteren Vertrag nicht: H und H+(t-t0)² psi können dieselben beiden
Cauchy-Spuren und verschiedene Vergangenheiten besitzen.

Hier wird ausdrücklich die freie massive Klein-Gordon-Cauchyfortsetzung
mit L=1-Delta auf R³ als Referenz gewählt:

\[
 u(\tau)=\cos(\tau\sqrt L)f+
 \frac{\sin(\tau\sqrt L)}{\sqrt L}g,\qquad \tau=t+1.
\]

Sie gilt in beiden Zeitrichtungen. Die tatsächliche implementierte
Archivhistory ist **H1**, nämlich

\[
 h_j=c_j(f)+\tau_j c_j(g),\qquad \tau_j=t_j+1\leq0.
\]

Das ist ein eigenständiger endlicher Adapter aus Anfangsdatenintegralen;
die exakte kompakte Kontinuumshistory wird nicht als Eingabe eingesetzt.
Auf der Anfangsfläche stimmen Wert und Ableitung mit P_hf und P_hg
überein. Die Differenz zu den unveränderten f,g ist Projektionsfehler.

Für beliebiges p >= 0 ist die explizite Erweiterung

\[
 h_j^{(p)}=\sum_{r=0}^{p}(-1)^r\left[
 \frac{\tau_j^{2r}}{(2r)!}c_j(L^rf)+
 \frac{\tau_j^{2r+1}}{(2r+1)!}c_j(L^rg)\right].
\]

Die Integrale der ursprünglichen Cauchy-Jets werden projiziert. Es wird
**nicht** L auf stückweise affine Rekonstruktionen angewandt; deren zweite
Ableitungen hätten Flächendistributionen. Auch P_h L = L P_h wird nicht
angenommen. Der Code enthält diese allgemeine History-Funktion; auf den
acht Archivwolken wurde ausschließlich p=0 ausgeführt und bewertet.

Für kompakte glatte Daten auf R³ gilt die Sobolev-Abschätzung
||v||_infinity <= ||L v||_2/sqrt(8 pi). Die Konstante folgt direkt aus
Fourier-Cauchy-Schwarz und integral_(R³)(1+|k|²)^(-2) dk=pi².
Taylor mit Integralrest der unitären KG-Evolution ergibt

\[
 R_p(\tau)\leq\frac{1}{\sqrt{8\pi}}\left[
 \frac{|\tau|^{2p+2}}{(2p+2)!}\|L^{p+2}f\|_2+
 \frac{|\tau|^{2p+3}}{(2p+3)!}\|L^{p+2}g\|_2\right].
\]

Die zusätzliche g-Schranke ist Teil des allgemeinen Vertrags.
Sei delta_(r,j)(f) eine eingeschlossene obere Schranke für
|c_j(L^r f)-(L^r f)(q_j)|. Dann folgt ohne Kommutatorannahme

\[
 |h_j^{(p)}-u(\tau_j,q_j)|\leq R_p(\tau_j)+
 \sum_{r=0}^p\left[
 \frac{|\tau_j|^{2r}}{(2r)!}\delta_{r,j}(f)+
 \frac{|\tau_j|^{2r+1}}{(2r+1)!}\delta_{r,j}(g)\right]=:\epsilon_j.
\]

Für den kompakten Archivlauf wird die bewiesene Normschranke von v0.10
für ||L² f|| verwendet. Für die nicht global L2-integrierbaren ebenen
Wellen wird diese Sobolev-Formel **nicht** verwendet: Ihr exakter
Vergleich exp[i(kz-sqrt(1+k²)tau)] liefert direkt ein Fehlerintervall.
Große |tau| bleiben als großer Historyfehler sichtbar.

## 6. Stabilität und endliche Fehlerweiterleitung

Räumliche L2-Stabilität folgt aus ||P_h||=1. Für nodale Auswertung gilt

\[
 |(P_h\delta u)(q_j)|\leq
 \sqrt{(M^{-1})_{jj}}\,\|\delta u\|_{L^2(D)}.
\]

Dies ist die Norm des Riesz-Repräsentanten der j-ten nodalen Auswertung
auf V_h. Für H1 ergibt sich damit
|delta h_j| <= sqrt((M^-1)_jj)(||delta f||_2+|tau_j| ||delta g||_2).
Es besteht keine von der Geometrie unabhängige L-infinity-Garantie.
Die Rechnungen liefern auch lambda_min(M) >= 1/||M^-1||_infinity und
kappa_2(M) <= ||M||_infinity ||M^-1||_infinity als überprüfbare Grenzen.

Für das vorhandene kausal geordnete Dreieckssystem schreibe
v_I=K_II v_I+K_IH h+s. K_II ist strikt untere Dreiecksmatrix, daher

\[
 R=(I-K_{II})^{-1}=\sum_{r=0}^{n_I-1}K_{II}^r,\qquad
 e_I\leq |R|\bigl(|K_{IH}|e_H+e_s\bigr).
\]

Eine besonders einfache sichere Auswertung verwendet die kausale
Rekursion e_i <= sum_(j<i)|K_ij|e_j+rho_i. Sie benötigt keine Bedingung
||K||<1, kann aber starke endliche Verstärkung zeigen. Bei gestörten
Koeffizienten gehört der Beitrag |delta K| |v_tilde| in rho. Dies ist
eine endliche Stabilitätsgrenze, kein Langzeit- oder Kontinuumslimesbeweis.

Der bisherige lineare Detektor hat bereits die Form A=T h. Für denselben
diskreten Operator, dasselbe Gebiet und dasselbe Fenster gilt deshalb

\[
 |A(h)-A(h_{\rm KG})|\leq\sum_j|T_j|\epsilon_j.
\]

Die v0.10-Transferbälle werden vollständig übernommen, nicht nur ihre
Mittelpunkte. Beim H1-Adapter seien d_f=T^T und d_g=diag(tau)T^T. Dann
ist die exakte Datennorm des idealen linearen Adapters

\[
 \|\mathcal A\|_{L^2(D)\oplus L^2(D)\to\mathbb C}^2
 =d_f^*M^{-1}d_f+d_g^*M^{-1}d_g.
\]

Die Gleichheit folgt aus den beiden Riesz-Repräsentanten in V_h und der
Produktnorm; Zeit ist in den bisherigen Einheiten L0=c=1 gemessen.
Die Implementierung liefert eine obere Einschließung dieser Norm.

Für eine ausgegebene Mittelpunktsantwort kommt deren komplexer Ballradius
hinzu. Ein Radiusbudget pro Real-/Imaginärkomponente ist bei Umrechnung
in einen komplexen Absolutfehler mit dem euklidischen Radius zu behandeln.
Die gesamte physikalische Abweichung benötigt außerdem
|A_diskret(h_KG)-A_Kontinuum|. Dieser Operator-/Gebietsfehler wird durch
den neuen Adapter **nicht** qualifiziert. G1 bleibt HOLD.

## 7. Zertifizierte Integration und Numerik

Für die kompakte Quelle wird jeder Tetraeder durch deterministische
längste-Kante-Bisektion in 1, 4 und 16 Subtetraeder zerlegt. Die
Integrale jedes Hutfaktors über eine Unterzelle sind exakt deren Volumen
mal dem Mittelwert seiner vier Eckwerte. Ein Arb-Rechteck für f auf der
ganzen Unterzelle liefert wegen w_i >= 0 ein gültiges Integralrechteck.
Radiale Minima werden konservativ über die umschließende Box, radiale
Maxima über die Tetraederecken begrenzt. Schneidet eine Zelle die
Quellkugel, wird ihr Beitrag auch bei vier äußeren Ecken nicht auf null
gesetzt. Der Bump-Rand ist in der Einschließung enthalten.

Für die Wellen wird eine engere analytische Methode verwendet. Unter
dem Gewicht lambda_i hat die baryzentrische Zufallsvariable eine
Dirichlet(2,1,1,1)-Verteilung. Mit den z-Knoten, wobei z_i zweimal
vorkommt, sind ihre Momente vollständige homogene Polynome h_n.
Um die Intervallmitte z_c gilt für die lokale Last

\[
 \int_K\lambda_i e^{ikz}\,dx=
 \frac{|K|}{4}e^{ikz_c}
 \sum_{n=0}^{80}\frac{(ik)^n h_n(z_0-z_c,\ldots,z_3-z_c,z_i-z_c)}{(5)_n}
 +r_i,
\]
\[
 |r_i|\leq\frac{|K|}{4}\frac{(|k|a)^{81}}{81!},\qquad
 a=(\max z_i-\min z_i)/2.
\]

Die Restschranke nutzt die Ableitungsnorm eins von exp(i x) auf der
reellen Achse. Alle Summen, Matrizen und Lösungen sind Arb/Acb-Bälle;
die Geometrie ist rational. Ein unabhängiger eindimensionaler
Acb-Integrationsvergleich prüft die Momentformel im Referenztetraeder.

Numerische Fehler und Restfehler sind eingeschlossen. Eine kleine
Gleitkommadifferenz wird nicht als Zertifikat verwendet. Für verschiedene
Präzisionen werden nur Intervalle derselben Zielgröße auf Überlappung
geprüft, nicht verschieden berechnete konservative Fehleroberwerte.

## 8. Entscheidungen und Reproduktion

Die mathematische Existenz des Adapters und ein positiver Quelltransfer
werden von seiner Genauigkeitsqualifikation getrennt ausgewiesen:

| Prüfung | Entscheidung bei Nichterfüllung |
|---|---|
| Bestehende Orte, konforme Zerlegung, Quellüberdeckung | GEOMETRY/COVERAGE_HOLD |
| Positives invertierbares M; endliche Balllösung | NUMERIC_HOLD |
| Relativer L2-Projektionsfehler <= 0.001 | RESOLUTION_HOLD oder belegtes Überschreiten |
| Anfangsdaten-/Historyfehler am Detektor <= 0.001 | METHOD_HOLD |
| Komponentweiser Antwort-Radius <= 0.001 | METHOD_HOLD |

Die L2-Toleranz ist ein neu deklarierter räumlicher Adapterprüfpunkt;
sie ersetzt keinen alten wissenschaftlichen Gate-Wert. Die beiden
Detektorbudgets verwenden die bisherige Amplitudenskala. Selbst wenn
alle Budgets bestünden, wäre das nur DEVELOPMENT_BUDGETS_ONLY.

```bash
cd research/cspp/nonlocal_initial_v0_11
python -m pip install -r requirements.txt
python -m unittest -v test_adapter
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B run.py --bits 128 --out results/BENCHMARK_128.json.gz
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B run.py --bits 192 --out results/BENCHMARK_192.json.gz
python -B verify.py
```

`FREEZE.json` hält den lokalen Methodenstand vor den endgültigen Läufen
fest. Das ist ausdrücklich **keine öffentliche Vorregistrierung** und
keine unabhängige Bestätigung auf frischen Daten. Die bereits bekannten
Archivwolken wurden zur Methodenentwicklung verwendet. Vorläufige reine
Wertebereichsquadratur war für Wellen zu breit; sie wurde durch analytische
Momente ersetzt. Die vorläufigen Resultate und ihr damaliger Quellenhash
bleiben in `development_draft/` erhalten. Physik, Wolken, Tetraederorte,
Unterteilungstiefen und Toleranzen wurden dabei nicht geändert.

## 9. Einordnung und Quellen

Die Projektions- und Fehlerformeln oben werden hier für diesen Adapter
hergeleitet. Die allgemeine Partition-of-unity-Idee ist etablierte
Finite-Elemente-Methodik; sie ist kein neuer Satz über Kausalsets.

1. Melenk, J. M.; Babuška, I. (1996): The Partition of Unity Finite Element
   Method: Basic Theory and Applications. ETH SAM Report 96-01.
   https://doi.org/10.3929/ethz-a-004284735
2. Aslanbeigi, S.; Saravani, M.; Sorkin, R. D. (2014): Generalized causal
   set d'Alembertians. JHEP 06, 024.
   https://doi.org/10.1007/JHEP06(2014)024
   Diese Arbeit begründet nicht die Stabilität des hier gewählten Adapters.
3. Unveränderter lokaler Vorgänger: `../detector_methods_v0_10/METHODS.md`
   und `ADAPTER_OBSTRUCTION.md` am oben angegebenen Commit.

Offen bleiben eine hinreichend genaue History auf den tatsächlich langen
Vergangenheitsintervallen, eine ausreichende räumliche Approximation bei
festen Knoten, engere kompakte Lastintegrale sowie die unabhängige
Operator-/Gebietsqualifikation. Die Ergebnisse liefern weder einen
physikalischen Rauschnachweis noch eine Dirac-Freigabe.
