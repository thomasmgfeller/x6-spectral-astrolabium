# CSPP v0.26: Grenze universeller Stabilität und ein Pfadkriterium

31. Oktober 2026. Deterministische mathematische Untersuchung. Basis: Main
`c156dab194bbe144101382b813112eee339e0e7a` nach PR #158.

## 1. Ergebnis und Status

Für nichttriviale, unverändert auf jede Realisierung angewandte Intervallkerne
ist eine endliche, deterministische l-infinity-Verstärkungsschranke über ALLE
endlichen Kausalsets unmöglich. Das gilt auch für alle Realisierungen eines
idealen Poisson-Sprinklings in einem geeigneten festen beschränkten
Minkowski-Gebiet: Die Verstärkung ist dort wesentlich unbeschränkt, obwohl
sie auf jeder einzelnen endlichen Realisierung endlich ist.

Das ist ein begrenzter Unmöglichkeitssatz zur stärksten Worst-Case-Forderung.
Es ist KEIN Nachweis zeitlicher Instabilität typischer Realisierungen,
keine unendliche Varianz, kein Ausschluss von Hochwahrscheinlichkeits- oder
Energieabschätzungen und kein Fehlernachweis für den festen KG-Detektor.
Insbesondere wird keine wissenschaftshistorische Neuheit beansprucht.

Daneben wird ein hinreichender Satz formuliert, der signierte Pfade vor
der Betragsbildung zusammenfasst. Eine explizite Zweiknoten-Zellenfamilie
zeigt damit eine längenuniforme Schranke trotz fehlender Zeilenkontraktion.
Diese Positivkontrolle ist ein algebraisches Modell, kein neuer GCB-Kandidat.

METHOD = HOLD; G1 = HOLD. Keine neuen Ensembles, keine Parameteranpassung,
keine Websiteänderung und keine neue GitHub-Veröffentlichung in diesem Paket.

## 2. Definitionen und Norm

Sei C ein endliches strikt partiell geordnetes Set, in einer linearen
Erweiterung nummeriert. n(j,i) zählt ALLE Punkte im offenen Intervall
j < z < i, nicht nur Kanten eines Hasse-Diagramms. Fixiere eine reelle Folge
t(n), unabhängig von C und seiner Punktzahl. Der aktive Transfer ist

    K_ij = t(n(j,i)) falls j < i in der Kausalordnung, sonst 0.
    u = Ku + f; R_C = (I-K)^(-1).

Die Norm ist ||v||_infinity = max_i |v_i|, ohne faktorielle, volumetrische
oder punktzahlabhängige Gewichte. Die induzierte Matrixnorm ist die maximale
absolute Zeilensumme. f ist ein beliebiger additiver Fehler in der bereits
diagonalnormalisierten Gleichung. In (B-m²)u=J gilt f=-delta J/D.
Für festes D != 0 ist die Norm für J daher ||R||/|D|; derselbe Ausschluss
gilt. Punktweise begrenzte Eingaben haben nicht automatisch begrenzte
Gesamtenergie, wenn ihre Zahl wächst. Dies ist eine wesentliche Normgrenze.

K ist strikt unterdreieckig. R existiert für jedes endliche C als endliche
Neumannsumme. Das zu prüfende stärkere Ziel lautet sup_C ||R_C|| < infinity.

## 3. Satz A: Exakte Fächer-Gegenfamilie

Annahme: t ist nicht identisch null. Setze

    r = min {n >= 0 : t(n) != 0}, alpha = t(r).

Für jedes M >= 1 konstruiere C_(M,r) aus M unvergleichbaren Punkten y_1,...,y_M,
einer gemeinsamen Kette z_1 < ... < z_r und einem Endpunkt x. Jeder y_i liegt
vor jedem z_j und vor x; jeder z_j liegt vor x. Für r=0 fehlt die Kette.
Es gibt keine weiteren Punkte oder Relationen ausser der transitiven Hülle.

Dann gilt exakt:

    K² = 0,
    R = I + K,
    ||R||_infinity = 1 + M |alpha|.

BEWEIS. Die Intervalle zwischen y_i und x enthalten genau die r Kettenpunkte.
Jede andere vergleichbare Paarung hat weniger als r Intervallpunkte:
n(y_i,z_j)=j-1, n(z_i,z_j)=j-i-1 und n(z_i,x)=r-i.
Die entsprechenden t-Werte verschwinden nach Definition von r. Somit hat
K ausschliesslich die M Einträge K_(x,y_i)=alpha. Kein Produkt zweier
solcher Einträge ist möglich; K²=0. Die Endzeile von I+K hat absolute
Summe 1+M|alpha|, jede andere Zeile Summe 1. Das beweist die Formel.
Die Eingabe f_x=1, f_(y_i)=sign(alpha), f_(z_j)=0 hat Norm 1 und erreicht
die Schranke am Endpunkt. Also ist sup_M ||R||=infinity. QED.

Für jeden festen Zielwert L ist bereits
M > (L-1)/|alpha| ein expliziter Zeuge gegen die Schranke L.
Die Norm muss nicht nur durch eine grobe Majorante gross sein: Sie wird erreicht.

HISTORY-VARIANTE. Die y_i können als vorgeschriebene History, z_j als aktive
Punkte und x als passive Probe behandelt werden. Die aktiven Antworten aus
der History sind null, und A=alpha sum_i h_i. Folglich ist die genaue
History-zu-Probe-Norm M|alpha|. Auch gleichsinnige Störungen genügen.
Eine einzelne passive Probe ist nicht das festgelegte räumlich-zeitliche
KG-Detektormittel; dessen Verhalten wird daraus nicht abgeleitet.

## 4. Lorentzsche Realisierbarkeit und Poisson-Quantoren

Die Fächer sind keine bloss abstrakten, nicht einbettbaren Ordnungen.
Für r fest und jedes M wähle in 1+3 Minkowski-Raum:

    y_i = (0, i/[4(M+1)], 0, 0), i=1,...,M;
    z_j = (1 + j/[2(r+1)], 0, 0, 0), j=1,...,r;
    x   = (2, 0, 0, 0).

Alle y_i sind strikt raumartig getrennt; alle verlangten geordneten Paare
sind strikt zeitartig. Sämtliche Punkte liegen im festen Diamanten
Omega = {|t-1| + |spatial_position| < 3}. Endliche strikte Ungleichungen
haben einen positiven Mindestabstand von ihrer jeweiligen Grenze.
Daher existieren für jedes M disjunkte offene vierdimensionale Umgebungen
U_v mit positivem Volumen, so dass JEDE Wahl eines Punkts aus jeder U_v
dieselbe Ordnung ergibt und alle U_v in Omega liegen.

Unter einem homogenen Poisson-Prozess mit beliebigem festem rho>0 hat das
Ereignis 'genau ein Punkt in jedem U_v, kein weiterer in Omega' die
Wahrscheinlichkeit

    exp[-rho Vol(Omega)] rho^(M+r+1) product_v Vol(U_v) > 0.

Das folgt direkt aus den unabhängigen Poissonzahlen auf disjunkten Mengen
(Last/Penrose, Definition 3.1). Auf diesem Ereignis gilt Satz A exakt.
Folglich gilt für jedes endliche L:

    P( ||R_C||_infinity > L ) > 0.

Die essentielle obere Grenze ist unendlich, schon bei festem Gebiet und
fester Dichte. Ein deterministisches C(rho,Omega)<infinity mit
P(||R_C||<=C(rho,Omega))=1 existiert für diese Klasse nicht.

Das behauptet NICHT P(||R_C||=infinity)>0: Diese Wahrscheinlichkeit ist im
endlichen Gebiet null. Auch folgt NICHT, dass das Ereignis bei wachsender
Dichte häufig wird. Für jedes rho werden geeignete M und Umgebungen gewählt;
die Wahrscheinlichkeit kann extrem klein sein. Keine Ereignisfolge in einer
gekoppelten Dichteverfeinerung wird hier untersucht. Ein Satz mit zugelassener
Ausfallwahrscheinlichkeit delta>0 bleibt möglich.

Die Koordinaten dienen nur als Existenzbeweis. Der Operator selbst benutzt
ausschliesslich die Ordnung und Intervallzahlen. Es wird kein bevorzugter
Frame in die Dynamik eingeführt. Eine zeitliche Translation bringt r=0
mit History vor t=-1 und Probe nach t=-1 auch in das aktive v0.25-Zeitband;
dies ersetzt weiterhin nicht den konkreten KG-Detektor.

## 5. Anwendung auf v0.25 einschliesslich des Sonderfalls

Unverändert aus v0.25:

    a = 1/sqrt(2*pi), epsilon=1/16, m=1,
    c(theta)=(1,-9,16,-8,0)+theta*(9/8,-141/8,111/2,-63,24),
    d(theta)=-1-3theta/8, D(theta)=1-a*d(theta),
    t(n)=(a*epsilon/D) sum_k c_k binom(n,k) epsilon^k (1-epsilon)^(n-k).

Nur D!=0 ist hier zugelassen. Bei D=0 ist diese normalisierte Dynamik
nicht definiert; daraus wird kein zusätzlicher Stabilitätsbefund erzeugt.

Für theta!= -8/9 ist c_0=1+9theta/8 ungleich null. Daher r=0 und
alpha=(a*epsilon/D)c_0. Für theta=-8/9 gilt c_0=0, aber c_1=20/3,
d=-2/3 und t(1)=a*epsilon²*(20/3)/(1+2a/3) !=0. Satz A greift mit r=1.
Somit entgeht KEIN nichtsingulärer Parameter der gesamten v0.25-Familie
diesem Worst-Case-Ausschluss. Dies ist ein analytischer Allparameterbefund,
kein Suchgitter. Er ist unabhängig vom bereits bekannten Zweiskalenfehler.

Für theta=21, c_0=197/8 und D=1+71a/8, ist

    alpha_21 = 197a / [128(1+71a/8)] > 0.

Die Dezimalanzeige und rationale Einschliessung werden in results/RESULTS.json
ausgewiesen. Für diese Konstante ist ||R|| exakt 1+M*alpha_21.

ALLGEMEINERE ENDLICHE SCHICHTKERNE. Für 0<epsilon<=1 und einen nichtnull
Koeffizientenvektor sei r der erste nichtnull Index. Dann ist w(n)=0 für
n<r und w(r)=c_r epsilon^r !=0 (bei epsilon=1 gelten dieselben binomialen
Grenzwerte). Eine weitere feste Schichtzahl oder das Nullsetzen von c_0
beseitigt den Ausschluss deshalb nicht. Auch rho-abhängige Gewichte helfen
gegen den Allrealisierungsanspruch nicht, sofern bei JEDEM fixierten rho
ein nichttrivialer, realisierungsunabhängiger Kern vorliegt. Eine vom lokalen
Grad abhängige Normalisierung wäre ein anderer Operator und müsste erneut
auf Normierung und Genauigkeit geprüft werden.

## 6. Satz B: Interne Pfade eliminieren, dann abschätzen

Zerlege die aktiven Variablen in interne Variablen e und verbleibende
Variablen b. Nach der entsprechenden Blockzerlegung lautet das System

    e = K_ee e + K_eb b + f_e,
    b = K_be e + K_bb b + f_b.

Da jeder induzierte kausale Teilgraph azyklisch ist, existiert
R_e=(I-K_ee)^(-1). Elimination liefert exakt

    L = K_bb + K_be R_e K_eb,
    b = L b + f_b + K_be R_e f_e,
    e = R_e f_e + R_e K_eb b.

L fasst direkte und alle ueber interne Punkte laufenden Pfade SIGNIERT
zusammen. Die Pfade gehen in der ursprünglichen Ordnung nach vorne;
L ist in der induzierten Ordnung der b-Punkte strikt unterdreieckig.
Angenommen, über die ganze betrachtete Familie gelten uniforme Grenzen

    ||R_e|| <= C_e, ||R_e K_eb|| <= U,
    ||K_be R_e|| <= V, ||L|| <= r_0 < 1.

Dann folgt mit C_b=(1+V)/(1-r_0)

    ||(I-K)^(-1)|| <= max{C_b, C_e + U*C_b}.

BEWEIS. Die geometrische Reihe begrenzt (I-L)^(-1) durch 1/(1-r_0).
Die rechte Seite des b-Systems hat Norm höchstens (1+V)||f||inf. Damit
||b||<=C_b||f||inf. Rückeinsetzen ergibt
||e||<=(C_e+U*C_b)||f||inf. Die volle Maximumsnorm ist das Maximum
beider Blocknormen. QED.

Die Elimination muss VOR der Betragsbildung erfolgen. Damit bleiben auch
Aufhebungen zwischen Pfaden UNTERSCHIEDLICHER Länge erhalten. Alle vier
Grenzen sind erforderlich: Ein kleiner reduzierter Transfer kann grosse
interne Verstärkung oder grosse Ein- und Auskopplung nicht verdecken.
Der Satz ist eine elementare Schurkomplement-/Resolventenabschätzung,
kein neu beanspruchtes Grundprinzip. Seine Anwendung auf eine qualifizierte
Poisson-GCB-Familie ist weiterhin offen. Die untenstehende Positivkontrolle
zeigt dagegen eine vollständig definierte Familie, die alle Annahmen erfüllt.

HISTORY/DETEKTOR. Aus ||R||<=C, ||H||<=H_0, ||q_A||_1<=Q_A und
||q_H||_1<=Q_H folgt

    |delta A| <= (Q_H+Q_A*C*H_0)||delta h||_infinity
                 + Q_A*C ||delta f||_infinity.

Jede dieser Kopplungsgrenzen muss zum selben Familienindex passen.
Ein stabiler aktiver Block kontrolliert nicht automatisch die History.

ROBUSTHEIT. Wenn zusätzlich ||Delta K||<=delta und C*delta<1, folgt aus
I-K-Delta K=(I-K)(I-R Delta K)

    ||(I-K-Delta K)^(-1)|| <= C/(1-C*delta).

Dies ist eine Matrixnormbedingung. Eine kleine Änderung jeder einzelnen
Kante impliziert bei wachsender Zahl von Vorgängern KEINE uniforme delta.
Nicht uniforme Diagonalgewichte zur Normänderung dürfen das Wachstum nicht
verstecken: Für a_0||v||inf<=||v||_*<=b_0||v||inf müssen a_0,b_0 uniform
sein; dann überträgt sich die Abschätzung nur mit Faktor b_0/a_0.

## 7. Explizite Positivkontrolle und Zusammenbruch der Aufhebung

Für n=1,...,N, y_0=0, definiere eine kausale Zellenfamilie

    x_n = f_(x,n) + A y_(n-1),
    y_n = f_(y,n) + B x_n + C y_(n-1).

Die algebraische Elimination summiert den direkten und den zweistufigen Pfad:

    y_n = (f_(y,n)+B f_(x,n)) + g y_(n-1),  g=AB+C.

Für ||f||inf<=1 sind die genauen Zeilennormen

    row_y(n)=(1+|B|) sum_(j=0)^(n-1) |g|^j,
    row_x(n)=1+|A|(1+|B|) sum_(j=0)^(n-2) |g|^j

(die letzte Summe ist bei n=1 leer). Die Eingabekoordinaten der Summanden
sind verschieden, daher sind die absoluten Zeilensummen erreichbar.
Das Maximum beider Ausdrücke bei n=N ist die exakte induzierte Norm.
Für |g|<1 folgt die längenuniforme, praktisch nutzbare Schranke

    ||R_N|| <= max{ (1+|B|)/(1-|g|),
                    1+|A|(1+|B|)/(1-|g|) }.

Bei |g|=1 wächst bereits row_y linear; bei |g|>1 exponentiell in N.
Dies sind Knotenzellen, keine kalibrierte physikalische Zeit.

Beispiel A=2, B=1, C=-2: g=0 und ||R_N||<=5, mit Gleichheit für N>=2,
obwohl ||K_N||inf=3 für N>=2. Satz B gilt nach Elimination aller x_n mit
C_e=1, U=2, V=1, r_0=0 und liefert genau die Schranke 5. Die absolute Pfadmajorante hätte den
Rückkopplungsfaktor |AB|+|C|=4 und wächst. Die signierte Kontrolle erhält
die Aufhebung und bleibt konstant. Für C=-2+e ist g=e: Die Aufhebung bleibt
bei |e|<1 kontrolliert; bei |e|>=1 geht die uniforme Schranke verloren.

Dieser Operator wird auf einem gerichteten azyklischen Graphen definiert;
seine transitive Hülle ist eine Kausalordnung, aber seine Kantengewichte
sind NICHT durch die GCB-Intervallformel erzeugt. Er erfüllt keine hier
nachgewiesene 4D-Infrarotnormierung. Er dient ausschliesslich als exakte
Positiv-/Negativkontrolle des mathematischen Instruments.

## 8. Reproduktion, Grenzen und nächster präziser Auftrag

`python3 reproduce.py` benötigt für die mathematischen Kontrollen nur die
Python-Standardbibliothek. Es prüft Quellenhashes, rekonstruiert Ordnungen
aus rationalen Minkowski-Koordinaten, zählt Intervalle und vergleicht eine
dichte Gauss-Jordan-Inverse mit kausaler Vorwärtsrekursion. Die endlichen
Fächer und Zellen werden in rationaler Arithmetik geprüft. Die v0.25-
Konstanten werden durch eine rationale Machin-pi-Einschliessung und
ganzzahlige Quadratwurzelgrenzen eingeschlossen; Dezimalzahlen sind Anzeigen.
Falsche Intervallzahlen, weggefallene Pfade und falsche Vorzeichen werden
als Negativkontrollen geprüft. Das ist keine automatische formale
Verifikation des unendlichen Satzes; dessen Beweis steht oben.

Die wissenschaftliche Entscheidung lautet: Eine allrealisierungsuniforme
l-infinity-Schranke wird für diese nichttrivialen, unverändert angewandten
Intervallkerne verworfen. Eine physikalische Operatorfamilie ist damit
nicht insgesamt verworfen. Die nächste positive Stabilitätsaufgabe muss
zuerst Norm, Zeitfenster und Quantoren festlegen: geometrisch eingeschränkte
Familie ODER probabilistische Kontrolle mit expliziter Ausfallwahrscheinlichkeit.
Eine endliche Rechenserie darf diese Wahl nicht ersetzen.

Für den nächsten Anschluss bietet sich an: Auf festen physikalischen
Zeitfenstern bei q fest und epsilon=q/rho eine hochwahrscheinliche Schranke
für signierte, gebündelte Pfade untersuchen, einschliesslich lokaler
Punktkonzentration und History-/Detektorkopplungen. Zuerst analytische
Voraussetzungen und Budget; keine Freigabe eines neuen Bestätigungsensembles.
Der parallele Grad-5-Genauigkeitsauftrag aus v0.25 bleibt offen und wird
durch dieses Stabilitätsergebnis nicht als erledigt markiert.

## Quellen und Abgrenzung

1. Projektquellen, unveränderliche Git-URLs, Git-Blobs und SHA256:
   `evidence/SOURCES.json`. Definitionen stammen aus v0.25 und dem Labor.
2. Aslanbeigi, Saravani, Sorkin (2014), Generalized Causal Set d'Alembertians,
   https://arxiv.org/html/1403.1622v1 , insbesondere Abschnitte 1 und 3.5.
   Kontext: gemittelte Operatoren, IR-Normierung und wachsende Moden.
   Deren Modenkriterium wird nicht mit unserer diskreten Worst-Case-Norm
   gleichgesetzt. Der hier bewiesene Fächersatz wird ihnen nicht zugeschrieben.
3. Last, Penrose (2017), Lectures on the Poisson Process, Definition 3.1,
   https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf . Verwendet werden
   nur Poisson-Zählverteilungen und Unabhängigkeit disjunkter Mengen.

Eigene Herleitung und reproduzierbare endliche Kontrollen. Kein externes
Peer Review und keine Beweisassistent-Verifikation. Kein umfassender
Prioritätsvergleich mit der Stabilitätsliteratur.
