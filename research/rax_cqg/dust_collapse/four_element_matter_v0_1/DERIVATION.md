# CST-DUST: kontinuierlicher Vier-Element-Sektor v0.1

Stand: 7. November 2026. Basis: Main nach PR 256,
`e4787d04c78a1da43825dbbac670a0e3dfacee51` im Repository
[thomasmgfeller/x6-spectral-astrolabium](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/256).
Zwölf Quellen sind byteidentisch in `inputs/` mit Git-Blob-Identitäten gepinnt.
Die vorausgehende Herleitung steht zusätzlich in `inputs/prior_DERIVATION.md`.

## 1. Fragestellung und eingefrorenes Budget

Ziel ist die vollständige kontinuierliche Feldintegration des Sektors mit
vier neuen Elementen im unveränderten Referenzmaß. Das n=3-Paket begrenzte
die unbekannten Phasensektoren ab n=4 noch ausschließlich durch Normmassen.

Die natürliche Uhrordnung liefert 40 transitive Vorgängermaskentupel. Sie
werden sowohl durch vollständige Enumeration oberer Dreiecksrelationen mit
Transitivitätsfilter als auch rekursiv über Ordnungsideale erzeugt. Beide
Mengen müssen identisch sein. Unbeschriftete Isomorphieklassen ersetzen diese
Summe nicht ohne eine entsprechende Transformation des markierten Maßes.

Der lokale Plan wurde nach einer analytischen Kostenabschätzung, vor neuer
Integralrechnung und vor Implementierung des beschleunigten Kerns eingefroren.
Er ist keine externe Präregistrierung und keine blinde Vorhersage. Es gilt:

| Größe | Festlegung |
|---|---|
| h | 1/4, 1/2 |
| alpha | 1, 2 |
| mu | 0, 1/4, 1 |
| g/pi | 0, 1/18, 1/9 |
| Amplitudenfehler pro Geometrie | höchstens 1e-8 |
| Quadraturbudget | höchstens 5e-9, gleich auf vier Koordinaten verteilt |
| Arithmetikbudget | höchstens 4e-9 |
| Maximale Tensorpunkte je Konfiguration | 1 200 000 |
| Maximale Dichtefunktionsaufrufe für n=4 | 35 000 000 |
| Maximale Laufzeit des nativen Kerns je Konfiguration | 600 Sekunden |

Die Laufzeitgrenze wird durch einen Prozess-Timeout erzwungen. Überlauf,
Fehlerbudget- oder Kostenüberschreitung führt zum Abbruch statt zu einem PASS.
Es wird keine bezahlte Rechenleistung beauftragt. Laufzeiten sind keine
wissenschaftlichen Observablen und gehen nicht in die deterministischen
Ergebnisdateien ein.

Das etwas gröbere Amplitudenziel als im n=3-Paket betrifft ausschließlich den
neuen Sektor. Wegen seiner kleinen Normmasse ist dessen maximal zugelassener
Beitrag zur Erfolgsintervallbreite von Ordnung 1e-11; er liegt deutlich unter
dem verbleibenden höheren Zahlrest. Die bisherigen Sektoren werden unverändert
übernommen, ihre Fehler werden nicht vergrößert oder unterschlagen.

## 2. Unverändertes Maß, vollständige Wirkung

Der Anfangsanker hat T=-2, w=0 und zählt nicht zu n. Die neue Uhr ist
T_j=-2+4h*x_j, mit 0<x1<x2<x3<x4<1. Das Dichtemaß bleibt

\[
 \nu(dw)=\tfrac12\delta_0(dw)+\tfrac12\mathbf1_{(0,1)}(w)dw.
\]

Für jede natürliche Ordnung p lautet die Materiewirkung

\[
 S_d=-\sum_{j=1}^4 w_j a_j,\qquad
 a_j=\tfrac12+4h^2\sum_{y\prec j} B_{k(y,j)}(x_j-x_y)^2,
 \quad B=(1,-9,16,-8),\ B_{k\ge4}=0.
\]

Der Anker x=0 bleibt in der Intervallsumme enthalten. G_p=S_g(p)-1 wird aus
der vollständigen geankerten Ordnung berechnet. 32400 rationale Kontrollen
vergleichen die Polynomform mit vollständiger Wirkung und inkrementeller
Auswertung: 40 Ordnungen, zwei h, fünf Uhrquadrupel, 81 Dichtequadrupel.

Die analytische Dichteintegration ergibt dieselbe charakteristische Funktion:

\[
 \chi(t)=\tfrac12+\tfrac12\frac{1-e^{-it}}{it},\quad\chi(0)=1,\qquad
 A_p(\mu)=24\int_{x_1<x_2<x_3<x_4}\prod_j\chi(\mu a_j)\,d^4x.
\]

Mit x_j=product_(k=j)^4 u_k ist der normierte Jacobian
J=24*u2*u3^2*u4^3. Das vollständige kontinuierliche Maß wird erhalten.
Die Gaußpunkte ersetzen das Integral mit ausgewiesenem Rest; sie definieren
kein neues atomares Feldmaß.

Die Momente k=0,...,3 werden auf zwei Domänen rational verglichen:

\[
 4!\int_{x_1<\cdots<x_4}\prod_jx_j^{b_j}\,d^4x
 =\frac{24}{\prod_{j=1}^4(\sum_{i=1}^j b_i+j)},\qquad
 \int_{[0,1]^4}J(u)\prod_j u_j^{b_j}\,d^4u
 =\frac{24}{\prod_{j=1}^4(b_j+j)}.
\]

Dichtemomente sind d0=1 und dk=1/[2(k+1)] für k>=1. Alle 320 Vergleiche
müssen exakt übereinstimmen. Die Negativkontrolle ohne gesamten Jacobian
prüft ein falsches, aber ebenfalls normiertes Würfelmaß anhand des ersten
Materiemoments. Weitere Kontrollen betreffen den fehlenden Faktor 24 und
eine ausgelassene natürliche Ordnung.

## 3. Der Integrationsbeweis bleibt erhalten

Die geerbten Polynom-, Bernstein- und Gaußroutinen bleiben bytegleich. Für
theta=mu*S_d ist jede einzelne Würfelkoordinate höchstens quadratisch.
Rationale Tensor-Bernstein-Koeffizienten begrenzen |theta'|<=D und
|theta''|<=2A auf der ganzen Uhr-/Dichtedomäne. Mit

\[
 H_0=1,\quad H_1=D,\quad H_k=D H_{k-1}+2A(k-1)H_{k-2}
\]

folgt |partial_j^k exp(i*theta)|<=H_k. Die positive normierte
Dichteintegration erhält diese Schranke. Einschließlich des Jacobians ist
für die nullbasiert nummerierte Koordinate j=0,...,3

\[
 B_{m,j}=4!\sum_{\ell=0}^j\binom m\ell\frac{j!}{(j-\ell)!}H_{m-\ell}.
\]

Der normierte Gauß-Legendre-Rest auf [0,1] hat Konstante
C_q=(q!)^4/[(2q+1)((2q)!)^3]. Der positive Peano-Kern kontrolliert den
komplexen Absolutfehler. Positive Gewichte und Teleskopierung liefern

\[
 |A_p-Q_p|\le\sum_{j=1}^4 C_{q_j} B_{2q_j,j}.
\]

Die jeweils kleinste zulässige gerade Ordnung aus 8,...,64 wird allein aus
den schlimmsten Ableitungsgrenzen der 40 Geometrien gewählt. Es gibt keine
Anpassung an beobachtete Integralwerte. Für mu=0 gilt A_p=1 exakt.

| h | mu | q | Tensorpunkte |
|---|---|---|---:|
| 1/4 | 1/4 | (8,8,10,12) | 7680 |
| 1/4 | 1 | (14,14,16,20) | 62720 |
| 1/2 | 1/4 | (14,14,16,20) | 62720 |
| 1/2 | 1 | (28,28,34,44) | 1172864 |

Über alle Konfigurationen sind das 1 305 984 Tensorpunkte. Von 160
Geometrie-/Element-Kombinationen sind nur 24 Dichtepolynome verschieden.
Ihre gemeinsame Auswertung benötigt 31 343 616 Aufrufe von chi, unter dem
Budget von 35 Millionen. Gleiche Präfixprodukte komplexer Faktoren werden
ebenfalls einmal berechnet und von mehreren Geometrien genutzt. Diese
Wiederverwendung verändert weder Summe, Maß noch Fehlergrenzen.

## 4. Beschleunigte, eingeschlossene Ganzzahlarithmetik

Ein neuer C++-Kern verwendet Intervalle [L,U]/2^60 mit signierten 128-Bit-
Ganzzahlen. Additionen, Subtraktionen und Multiplikationen prüfen den
Überlauf mit Compiler-Builtins; ein Überlauf bricht ab. Die ganzzahlige
Division wird explizit zu Floor/Ceil korrigiert, auch für negative Werte.
Der wissenschaftliche Integrationskern benutzt keine Gleitkommafunktionen
oder libm-Approximationen.

Die Legendre-Nullstellen und positiven Gewichte werden zunächst unverändert
in 160-Bit-Intervallen erzeugt und rational geprüft. Ihre Umrechnung auf
60 Nachkommabits rundet nach außen. Dasselbe gilt für das mit der
Machin-Identität rational eingeschlossene pi und für alle Polynomkoeffizienten.
Die 60 Bits sind Nachkommabits, keine Behauptung von 60 korrekten Ergebnisbits.
Die tatsächlich akkumulierte Intervallbreite ist entscheidend.

Die Argumentreduktion wählt ein ganzzahliges Vielfaches von pi/2 und prüft
|x|<=1 für das gesamte reduzierte Intervall. Kosinusgrad 32 und Sinusgrad 33
haben Reste <=1/34! beziehungsweise <=1/35!. Für |t|<=1 wird chi bis Grad 36
entwickelt; der Rest beträgt höchstens 1/(2*38!). Jeder dieser Reste ist
kleiner als 2^-60, weshalb jeweils eine zusätzliche Einheit an beiden
Intervallenden genügt. Für größere |t| wird die geschlossene Sinus-/Kosinus-
Form mit einem ausdrücklich von null getrennten Divisor verwendet.

Alle Rechen-, Umrechnungs- und Funktionsfehler sind so im komplexen
Rechteck enthalten. Für dessen Mittelpunkt t ist die Summe der reellen und
imaginären Halbbereiten ein sicherer komplexer Radius. Der analytische
Quadraturrest wird separat addiert. Die Auswertung der Gravitationsphasen
und der Summe über Geometrien erfolgt wieder im geerbten 160-Bit-Python-Code.

Der Kern wird vor der neuen Hauptrechnung kontrolliert:

- 168 signierte rationale Additions-, Subtraktions-, Produkt- und Quotientenkontrollen.
- 52 Einschlussprüfungen für exp(it) und chi(t) gegen 160-Bit-Referenzintervalle,
  einschließlich kleiner, negativer und großer Argumente.
- Ein absichtlich erzeugter 128-Bit-Überlauf muss zurückgewiesen werden.
- Alle 28 nichttrivialen n=3-Geometrieamplituden aus PR 256 werden mit dem
  nativen Kern erneut integriert und innerhalb der Summe beider Fehlergrenzen
  bestätigt.

Die Kontrollen ersetzen die Herleitung der Intervallregeln nicht. Ebenso
setzen die Zertifikate einen korrekt arbeitenden Compiler und Prozessor voraus;
eine formale Beweisprüfung der gesamten Implementierung ist nicht erfolgt.
`g++` mit `__int128`-Unterstützung ist eine neue Nachrechnungsabhängigkeit.
Der Quelltext ist vollständig enthalten, ausführbare Binärdateien nicht.

## 5. Kohärenter Vier-Element-Kanal und Rest

\[
 a_4(g,\mu)=\frac1{40}\sum_p e^{igG_p}A_p(\mu),\qquad v_4=|a_4|^2,
 \qquad c_4=\frac{40h^4}{24}\,2^{-6\alpha}.
\]

Die Sichtbarkeit ist bei festem h unabhängig von alpha. Alpha beeinflusst
die Präparation zwischen verschiedenen Elementzahlen. Die bisherigen
Amplituden n=0,...,3 samt Fehlern werden aus den gepinnten Vorgängerergebnissen
übernommen. Für |a-t|<=epsilon und |a|<=1 ist die Sichtbarkeit durch
|t|^2 +/- (2*epsilon+epsilon^2), geschnitten mit [0,1], eingeschlossen.

Die neue bekannte Normierung ist Z4=sum_(n<=4)c_n. Zum direkten Vergleich
bleiben Z6 und die bisherige alpha-unabhängige obere Normrestschranke gleich:

\[
 \delta_6=\frac{h^7}{7!(1-h/8)},\quad Z_{max}=Z_6+\delta_6,\quad
 R_{max}=Z_{max}-Z_4=(Z_6-Z_4)+\delta_6.
\]

Die Feldphasen n=5,6 sind unbekannt, ihre Normmasse aber exakt bekannt.
Für n>6 wird die analytische Normschranke benutzt. Es werden keine
Feldintegrale für n>=5 behauptet. Mit S_L,U=sum_(n<=4)c_n*v_n,L,U gilt

\[
 S_L/Z_{max}\le p_{count,\infty}\le(S_U+R_{max})/Z_{max}.
\]

Dieser Ausgang gehört zum kohärenten Filter mit erhaltener Zahl. Ein reiner
Elementzähler wäre phasenblind. Alle 36 neuen Zahlkanal-Intervalle müssen
in ihren Vorgängerintervallen liegen. Für den kohärenten Filter über alle
Zahlen wird der rohe neue Einschluss mit dem gültigen alten Intervall
geschnitten; beide sind gespeichert. Der phasenfreie Fall g=mu=0 bleibt
exakt eins bei unbegrenzter Elementzahl.

## 6. Interpretation und verbleibende Grenze

Alle vorgegebenen Fälle bestehen. Der maximale Einzelgeometrie-Quadraturrest
ist kleiner als 1.041e-9, der maximale eingeschlossene Arithmetikrest kleiner
als 1.841e-12. Ihre Summe bleibt unter dem Ziel 1e-8. Die nachfolgenden
Dezimalzahlen dienen der Orientierung; die Zertifikate enthalten rationale Werte.

| h | alpha | Restgrenze vorher n>=4 | Restgrenze jetzt n>=5 | entfernte Schrankenmasse |
|---|---:|---:|---:|---:|
| 1/4 | 1 | 8.1506816305e-5 | 2.2589012357e-6 | 97.23 % |
| 1/4 | 2 | 1.2676480812e-6 | 1.2064831462e-8 | 99.05 % |
| 1/2 | 1 | 1.0475939610e-3 | 5.8140310029e-5 | 94.45 % |
| 1/2 | 2 | 1.7365422168e-5 | 1.1133640602e-6 | 93.59 % |

Bei h=1/2, alpha=1, g=0, mu=1 ist der unbegrenzte Zahlkanal-Erfolg nach außen
gerundet in [0.932902157804; 0.932960298115] eingeschlossen. Im Vorgänger
war das Intervall [0.932749749421; 0.933797343383]. Alle 36 neuen Intervalle
liegen in ihren Vorgängern, einschließlich der exakt phasenfreien Fälle.

Bei alpha=2 macht die konservative n>6-Normschranke jetzt etwa 81.85 %
(h=1/4) beziehungsweise 94.91 % (h=1/2) der verbleibenden oberen Restmasse
aus. Das ist ein Anteil an der Fehlerschranke, keine gemessene tatsächliche
Wahrscheinlichkeit dieser Elementzahlen.

Das Ergebnis betrifft ein ausdrücklich gewähltes kontinuierliches
Referenzmaß. Es liefert keine physikalische Auswahl von Dichtemaß, kohärentem
Historienzugriff oder Endrandbedingung. Alle acht Gates MODEL, CURRENT,
CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION bleiben
HOLD. Weder 4D-CST-Dynamik noch Rückwirkung, Bounce oder Junction Law sind
dadurch hergeleitet.

Vor einer nächsten teuren Feldintegration sollte die verbliebene Normschranke
analytisch untersucht werden. Insbesondere ist die geerbte n>6-Schranke für
alpha=2 absichtlich konservativ: Sie benutzt nur alpha>=1. Ein Vergleich
mit einer alpha-abhängigen kombinatorischen Schranke kann zeigen, wie viel
Intervallbreite ohne weitere Feldintegration vermeidbar ist. Das wäre ein
eigenständiger nächster Schritt; hier bleibt die alte Schranke zum fairen
Vergleich unverändert.

## 7. Reproduktion und Primärquellen

`python3 -O -B analyze.py` kompiliert den Kern vorübergehend und erzeugt sechs
Ergebnisdateien. `python3 -O -B replay.py` wiederholt alles einschließlich
Kompilation und vollständiger neuer Integralrechnung in einem frischen
Verzeichnis. Jede der sechs Dateien muss bytegleich sein. Das ist
Reproduzierbarkeit derselben Implementierung, keine externe Replikation.
`python3 -B verify_package.py` prüft das vollständige SHA-256-Manifest.

1. [NIST DLMF §3.5(v)](https://dlmf.nist.gov/3.5#v): Standardformel der
   Gaußquadratur. Die konkrete Bernstein-/Ableitungsabschätzung ist in der
   geerbten und vorliegenden Herleitung ausgeführt.
2. [GCC: Integer Overflow Builtins](https://gcc.gnu.org/onlinedocs/gcc/Integer-Overflow-Builtins.html):
   dokumentierte Überlaufprüfung für arithmetische Ganzzahloperationen.
3. [GCC: 128-bit Integers](https://gcc.gnu.org/onlinedocs/gcc/_005f_005fint128.html):
   Plattformvoraussetzung für die verwendete Ganzzahlerweiterung.

Quellen geprüft am 7. November 2026; externe Texte werden verlinkt, nicht kopiert.
