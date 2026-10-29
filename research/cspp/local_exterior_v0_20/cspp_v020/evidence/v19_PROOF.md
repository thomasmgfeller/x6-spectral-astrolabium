# CSPP v0.19: Quellnormen und geometrisch begrenzter Rest

29. Oktober 2026. Analytische Fortsetzung von v0.18, PR #150, auf dem
verifizierten Main-Commit 995b2184cb5346aee502d8e69089681181c5853e.
Keine neue Wolke, keine neuen Seeds, keine neue statistische Freigaberegel.

## 1. Ergebnis und genaue Aussage

Die globale Feldmajorante sinkt von etwa 1,520 mal 10^9 auf weniger als
6,429644. Der pauschale Archivfaktor 16 exp(625/8), etwa 1,36 mal 10^35,
wird durch geometrische Faktoren unter 229327 beziehungsweise 1317148
ersetzt. Mit einer integrierten Feldhülle und einem beschränkten Gewichtskern
folgen für die vier vorhandenen Archive und beide Detektorfenster vollständig
transportierte obere Schranken zwischen 2,36 mal 10^14 und 3,39 mal 10^14.
Der genaue Gegenstand ist jeweils

    E[ |A_infinity - A_5| | feste Konfiguration in Omega5 ].

Die Schranken sind gegenüber den in v0.18 ausgewerteten Gesamtmajoranten
um einen Faktor von mehr als 5,28 mal 10^39 kleiner. Sie bleiben jedoch
mehr als 17 Größenordnungen über dem Vergleichsmaßstab 0,001. Das ist
eine Verbesserung eines mathematischen Beweisinstruments, keine Messung
eines Fehlers und kein Nachweis großer physikalischer Fluktuationen.

METHOD_HOLD und G1 HOLD bleiben bestehen. Individuelle Genauigkeit:
NOT_CERTIFIED. Frisches Bestätigungsensemble: NOT_RUN. Eine große obere
Schranke widerlegt weder Genauigkeit noch die Operatorfamilie; eine kleinere
obere Erwartungswertschranke zertifiziert keine einzelne Realisierung.

## 2. Unverändertes Modell und Konventionen

Minkowski-Raum in 3+1 Dimensionen, m=1, rho=3/pi, eps=1/16,
a=1/sqrt(2 pi), beta=a/[16(1+a)]. Das normierte Anfangsfeld bei t=-1 ist

    f(x) = exp(1-1/h) exp(4 i z),  h=1-4|x|^2,  |x|<1/2;
    f=0 außerhalb;  Anfangsgeschwindigkeit=0.

Die glatte Nullfortsetzung und die Normierung entsprechen v0.18.
U ist die lokale massive KG-Lösung. Ihre Werte werden für t<=-1 als
History vorgeschrieben; nur t>-1 wird diskret entwickelt. Fourierkonvention:
f_hat(k)=Integral exp(-i k.x) f(x) dx; inverse Normierung (2 pi)^(-3).

Der Detektor mittelt gleichmäßig und normiert über B((0,0,3/2),1/2),
W0=[3/4,1] beziehungsweise W1=[1,5/4]. B=Omega5 ist der Diamant
|x|<5-|t| mit unterer Spitze b=(-5,0). Für y vor p seien
T=p_t-y_t, s=T^2-|p_x-y_x|^2, V=pi s^2/24. Der Schichtkern ist

    w(n)=sum_(k=0..3) c_k binom(n,k) eps^k (1-eps)^(n-k),
    c=(1,-9,16,-8),  K=beta w(n).

Aus v0.18: |w(n)|<=kappa=4976184375/4294967296 für jedes n>=0.
Setze gamma=beta kappa. Der Nachweis wird erneut kontrolliert: exakte
Auswertung bis n=128 und eine danach monoton fallende positive Hülle.
Die Knotenzahlen der vier Archive bleiben 65,49,59,50; die fehlende aktive
Poissonmasse ist 29/512. Es werden keine neuen Archivkoordinaten erzeugt.

## 3. Tatsächliche Quellableitungen statt globaler Cauchy-Maxima

Setze H=1-Delta, u=i z. Schreibe H^J f=f P_J(h,u), P_0=1.
P_J ist ein endliches Laurentpolynom in h mit ganzzahligen Koeffizienten
und ein Polynom in u. Auf dem Polynomanteil sei D=d/dh+h^(-2).
Die Kettenregel für h=1-4r^2 und den unveränderten Träger exp(4 i z) liefert

    P_(J+1) = 17 P_J -16(1-h) D^2 P_J +24 D P_J
              +16u D d_u P_J +d_u^2 P_J +64u D P_J +8 d_u P_J.

Insbesondere P_1=17-8h^(-2)+48h^(-3)-16h^(-4)+64u h^(-2).
Sämtliche Koeffizienten werden als exakte Python-Ganzzahlen geführt;
es gibt keine Gleitkomma-Differentiation. Das Verschwinden aller Ableitungen
am Rand folgt aus exp(-1/h); die nachfolgenden partiellen Integrationen
haben deshalb keine Randterme.

Definiere Q_J=||H^J f||_2^2. Beim Quadrieren von P_J(h,i z) werden
die geraden z-Potenzen exakt gesammelt, einschließlich aller Vorzeichen
aus der komplexen Konjugation. Jedes radiale Moment hat die geschlossene Form

    Integral |exp(1-1/h)|^2 h^(-n) z^(2l) d^3x
      = pi Gamma(l+3/2) U(l+3/2,n,2) / [4^(l+1)(2l+1)].

Hier bezeichnet U(a,b,z) Tricomis hypergeometrische Funktion, nicht das
KG-Feld. Herleitung: Winkelmittel z^(2l)=r^(2l)/(2l+1), dann
sigma=1/h-1. Die verbleibende positive Integralform ist
Integral exp(-2 sigma) sigma^(l+1/2)(1+sigma)^(n-l-5/2) d sigma.
DLMF 13.4.4 liefert genau die angegebene Identität; a=l+3/2>0, z=2>0.
Die endliche signierte Summe wird mit Arb-Intervallen bei 384 und 512 Bit
ausgewertet. Die hohe Präzision schützt vor Auslöschung der hohen Ableitungen.

Unabhängiger Kontrollweg: Q_J=<f,H^(2J)f>. Dabei wird P_(2J) integriert,
ohne P_J zu quadrieren. Beide Wege stimmen für alle J=0,...,34 überein.
Zusätzlich wird Q_1 direkt aus dem radialen Laplaceoperator eingeschlossen:

    Q_1=4 pi Integral_0^(1/2) r^2 [(17b-b''-2b'/r)^2+(64/3)(b')^2] dr,
    b(r)=exp(1-1/(1-4r^2)).

Die validierte Quadratur verwendet r=v/[2 sqrt(1+v^2)], v in [0,16],
und einen analytischen Rest bis infinity. Für v>=16 ist der Integrand
durch (pi/2) 8263 2^8 v^18 exp(-2v^2) begrenzt; sein Integral wird
mit der oberen unvollständigen Gammafunktion eingeschlossen. Dieser Weg
benutzt keine Tricomi-Funktion. Wolfram bestätigt Q_1 zusätzlich numerisch
aus der ursprünglichen radialen Ableitungsformel.

## 4. Neue globale Feldschranke und Konturkonstanten

Da |cos(tau sqrt(1+|k|^2))|<=1 auf reellen k, liefern Cauchy-Schwarz
und Plancherel mit Integral (1+|k|^2)^(-2) d^3k=pi^2:

    |U(t,x)| <= M = sqrt(Q_1/(8 pi))
               = 6,42964363296382919018... .

Dies gilt für alle Zeiten und Orte. Es ist keine gemessene Feldamplitude.
Für g=exp(delta e.x)f, |e|=1, 0<=delta<=1/2, gilt auf der Quellstütze
exp(delta e.x)<=exp(1/4). Durch Konjugation des Differentialoperators:

    ||H^J g||_2 <= exp(1/4) (5/4)^J sqrt(Q_J),
    ||H^J g||_1 <= sqrt(pi/6) exp(1/4) (5/4)^J sqrt(Q_J) = D_J.

Begründung der ersten Ungleichung: Der konjugierte Operator lautet
H-2 delta e.grad-delta^2. Sein Fouriermultiplikator hat Betrag höchstens
1+|k|^2+delta^2 <= (5/4)(1+|k|^2). Der L1-Schritt ist Cauchy-Schwarz
auf der unveränderten Quellkugel mit Volumen pi/6.

Der Konturbeweis aus v0.18 gilt unverändert: Auf k+i e/2 erhält man im
Streifen ||x|-tau|<=C die Dämpfung exp(-3 tau/[16(1+|k|^2)]) und den
Vorfaktor exp(C/2). Entlang der relevanten History gilt C=21/4 und für
T>=T0=9/2 außerdem tau>=T/2. Zwei gültige Konstanten werden verglichen:

    C_N^(1)=exp(21/8) N! (32/3)^N D_(N+2)/(8 pi),
    C_N^(2)=exp(23/8) sqrt((2N)!) (16/3)^N
             (5/4)^(N+1) sqrt(Q_(N+1))/sqrt(8 pi).

Die zweite Formel wendet Cauchy-Schwarz direkt auf das verschobene
Fourierintegral an. Nach Quadrieren der Dämpfung wird
exp(-z)<=(2N)!/z^(2N) und J=N+1 benutzt. Damit bleibt im Integral erneut
(1+|k|^2)^(-2). Der Faktor 2^N stammt aus tau>=T/2.
Mit C_N=min(C_N^(1),C_N^(2)) gilt folglich

    |U(y)| <= min(M,C_N T^(-N))  für s<=sqrt(T), T>=9/2.

Beide Konstanten und ihre Auswahl sind gespeichert. N=3,...,32 wird wie
in v0.18 als deterministische Familie von Abschätzungen verwendet. Dies
ist keine Anpassung eines statistischen Tests oder eines physikalischen Parameters.

## 5. Geometrische Intervallüberlappung und Archivkonditionierung

Für jeden aktiven Punkt p eines kausalen Detektorpfades existiert ein
Detektorendpunkt d mit p vor d. Jeder Punkt z in I(y,p) Schnitt B erfüllt
b vor z vor d. Daher gilt stets

    I(y,p) Schnitt B ist Teilmenge von I(b,d).

Dies gilt auch für die noch unbekannten aktiven Punkte außerhalb B; die
unzulässige Annahme p in B wird nicht benötigt. Alle d liegen in B.
Für ein Fenster mit Endzeit tmax maximiert d_t=tmax, |d_x|=1 das Volumen:

    q |I(y,p) Schnitt B| <= Qwin=[(5+tmax)^2-1]^2/128,
    Qwin(W0)=1225/128,  Qwin(W1)=370881/32768.

Dies sind streng geometrische, fensterspezifische Obergrenzen. Sie sind
keine vollständig ausgewerteten Überlappungsvolumina aller tatsächlichen
Archivintervalle und nutzen deren individuelle innere Punktzahlen noch nicht.
Ein exakter Kontrollfall wird separat ausgewertet: y=(-6,0), p=(1,0,0,3/2).
Da y vor b liegt, ist I(y,p) Schnitt B exakt I(b,p). Dann ist
rho |I(y,p) außerhalb B|=2093/16. Der Kontrollfall ist deterministisch
gewählt und wird nicht als neue Archiv- oder Bestätigungsbeobachtung gezählt.

Sei n0 die feste innere Intervallzahl und mu=rho |I außerhalb B|.
N ist unter der Endpunkt-Palmverteilung Poisson(mu). Die Binomialfaltung
aus v0.18 und ihre nichtnegative Koeffizientenmajorante liefern

    E[|w(n0+N)| | B] <= Dwin exp(-s^2/128) Pbar(s^2/128),
    Dwin=16 exp(Qwin),  Pbar(z)=1+9z+8z^2+(4/3)z^3.

Zusätzlich gilt die punktweise Schranke kappa. Statt Dwin über das ganze
Integral auszumultiplizieren, werden beide Schranken zugleich benutzt.

## 6. Exakter bedingter Gewichtskern für die weitere lokale Rechnung

Die Implementierung enthält zusätzlich eine endliche exakte Formel für
E|w(n0+Poisson(mu))|. Sie wird in der universellen Gesamtmajorante noch
nicht mit individuellen Archivüberlappungen integriert. Schreibe r=15/16,

    w(n)=r^n P(n),
    P(n)=1-9n/15+8n(n-1)/225-4n(n-1)(n-2)/10125.

Alle Koeffizienten von P(128+x) sind negativ. Die positiven Gewichte
liegen deshalb in einer endlichen, exakt bestimmten Menge Zplus unter 128.
Mit z=mu/16, b_j=binom(n0,j) eps^j r^(n0-j) und

    F0=1-9z+8z^2-(4/3)z^3, F1=-9+16z-4z^2,
    F2=16-8z, F3=-8

gilt E w=exp(-z) sum_(j=0..min(3,n0)) b_j F_j und exakt

    E|w| = -Ew +2 exp(-mu) sum_(n in Zplus, n>=n0)
                    w(n) mu^(n-n0)/(n-n0)!.

49 deklarierte Paare (n0,mu) werden gegen eine direkte Poissonsumme bis
2048 und einen rigorosen Chernoff-Rest verglichen. Die Identität berücksichtigt
die feste Archivzahl. Sie ersetzt das nötige geometrische Volumeninput nicht.

## 7. Integration der beschränkten Feld- und Kernhüllen

Für eine beliebige positive Trennstelle S definiere die stückweise Majorante

    H_S(s)=kappa                  für 0<=s<=S,
           Dwin exp(-s^2/128)Pbar(s^2/128) für s>S.

Jeder Zweig begrenzt den bedingten absoluten Gewichtskern. Die Momente
I_m(S)=Integral_0^infinity s^m H_S(s) ds für m=0,4 sind explizit:

    I_m=kappa S^(m+1)/(m+1)+Dwin K_m(S),
    K_m(S)=sum_(j=0..3) a_j Gamma((m+2j+1)/2,S^2/128)
                         /[2 (1/128)^((m+1)/2)],
    (a0,a1,a2,a3)=(1,9,8,4/3).

Für das nahe Lichtkegelgebiet ist d^4y=2 pi sqrt(T^2-s) ds dT
und sqrt(T^2-s)<=T. Es genügt daher I_0 mal

    J_N(L)=Integral_L^infinity T min(M,C_N T^(-N)) dT.

Mit R=(C_N/M)^(1/N) gilt für L<R:
J_N(L)=M(R^2-L^2)/2+C_N R^(2-N)/(N-2); für L>=R:
J_N(L)=C_N L^(2-N)/(N-2). Beide Ausdrücke stimmen am Übergang überein.

Im fernen s-Gebiet s>sqrt(T) genügt M. Tonelli für nichtnegative
Integranden ergibt

    Integral_L^infinity T Integral_sqrt(T)^infinity H_S(s) ds dT
      = (1/2) Integral_sqrt(L)^infinity (s^4-L^2) H_S(s) ds
      <= (1/2) Integral_sqrt(L)^infinity s^4 H_S(s) ds.

Insbesondere begrenzt I_4/2 den gesamten Beitrag mit T>=T0.
Für 0<T<T0 genügt kappa M und das Volumen des abgeschnittenen Vergangenheitskegels
pi T0^4/3. Wegen rho=3/pi, K=beta w ist der direkte Frühbeitrag
höchstens gamma M T0^4. Zusammen folgt die uniforme direkte Historymajorante

    Bdir(N,S)=gamma M T0^4 +6 beta [I_0(S) J_N(T0)+M I_4(S)/2].

Hier wurde der Bereich außerhalb B durch den gesamten Historybereich
vergrößert. Das ist eine obere Schranke und keine Aussage, dass im festen
Archiv zusätzliche Punkte zufällig gezogen würden. Gegenüber der alten
Aufteilung in ein großes Stützenvolumen bis L plus Fernrest vermeidet
diese Integration den künstlich anwachsenden L^4-Term.

Für den entfernten Zeitrest tau>L, L>=T0, genügt ebenfalls T>L. Die
gespeicherte Zeitrestschranke benutzt 6 beta [I_0 J_N(L)+M/2 mal das
s^4-Moment ab sqrt(L)]. Sie ist separat vom gesamten geometrischen Rest.

## 8. Korrelierter Transport bis zum Detektor

Der unveränderte Pfadbeweis aus v0.18 wird mit der neuen direkten Majorante
angewendet. Multivariate Mecke integriert die außerhalb B unbekannten
Historywurzeln und aktiven Kettenpunkte. Alle eingesetzten aktiven Punkte
einer Kette liegen später als deren frühester aktiver Punkt p; sie liegen
deshalb nicht im offenen Historyintervall I(y,p). Die übrigen aktiven
Kantengewichte werden punktweise durch gamma begrenzt. Die bedingte
Kernmajorante bleibt so unter der Palm-Einsetzung gültig.

Nach Weglassen räumlicher Kausalbedingungen hat jede gewählte Teilmenge
höchstens eine zeitliche Reihenfolge. Für n_B bekannte aktive Knoten und
fehlende aktive Poissonmasse lambda=29/512 ergibt die gesamte Pfadsumme

    G_B=(1+gamma)^(n_B) exp(gamma lambda),
    E[|A_infinity-A5| | B] <= G_B Bdir(N,S).

Die Faktoren liegen unverändert ungefähr zwischen 2,73 und 3,79. Dabei
wird kein Erwartungswert eines abhängigen Produkts faktorisiert. Die volle
aktive Hülle beider Fenster wird für jedes Fenster benutzt; das ist konservativ.

Warum nur äußere Historywurzeln fehlen: B ist kausal konvex. Liegen Wurzel
und Detektorpunkt in B, liegen sämtliche dazwischenliegenden Pfad- und
Intervallpunkte ebenfalls in B. A_infinity-A5 enthält deshalb genau die
vollständigen Pfade mit Historywurzel außerhalb B. Ein separater, fälschlich
unabhängiger Fehler für die fehlenden aktiven Knoten wird nicht addiert.

## 9. Numerische Entscheidungen und Reichweite

Das deklarierte Gitter besteht aus N=3,...,32 und S=8,12,...,128. Die
Minima der Gesamtmajorante liegen bei N=3 und S=52 (W0) beziehungsweise
S=56 (W1). Strikte Intervallvergleiche bestätigen die Auswahl innerhalb
dieser endlichen Familie. Es wird kein globales Optimum aller Methoden behauptet.
Der frühere Volumen-Split wird mit denselben neuen Konstanten zusätzlich
gerechnet; seine besten Werte liegen weiterhin ungefähr bei 10^21 und
sind damit deutlich gröber als die integrierte Hülle bei 10^14.

Nach oben gerundete Gesamtobergrenzen:

    Archiv       W0              W1
    d0_r00       3,278e14        3,388e14
    d0_r01       2,364e14        2,443e14
    d0_r02       2,900e14        2,997e14
    d0_r03       2,413e14        2,494e14

Die entfernte Zeitrestmajorante fällt auf dem unveränderten L=2^j-Gitter
in allen acht Fällen spätestens bei L=2^34 unter 0,001. In sieben Fällen
geschieht dies schon bei 2^33. Dies ist weder ein Zertifikat für den
gesamten Rest hinter Omega5 noch eine notwendige Gebietsgröße. Es folgt
keine Empfehlung, entsprechend große Poissongebiete zu erzeugen.

Offen bleiben die präzisen, orts- und zeitabhängigen KG-Feldwerte im
relevanten endlichen Historybereich, die tatsächlichen Überlappungsvolumina
und n0-Werte aller beitragenden Archivintervalle sowie deren gemeinsame
Integration im transportierten Rest. Die neue geometrische Hülle ersetzt
diese lokale Auswertung nicht. Die Funktion für den exakten bedingten Kern
stellt dafür einen jetzt geprüften Baustein bereit.

Anschlussentscheidung: keine neue Bestätigungsstichprobe und keine große
Gebietserweiterung. Als Nächstes einen endlichen äußeren Historybereich
mit validierter KG-Quadratur, tatsächlichen Archivzählungen und lokal
eingeschlossenen Überlappungsvolumina auswerten; nur den verbleibenden
Fernteil mit der bewiesenen Hülle abdecken. Vorher keine globale
Fehlerzuordnung oder Genauigkeitsfreigabe behaupten.

## 10. Validierung, Quellen und Herkunft

960 Intervallvergleiche zwischen 384 und 512 Bit; 35 Quellnormen über eine
zweite Integrationsidentität; eine direkte validierte Quadratur mit
analytischem Rest; 129 exakte Gewichtspolynomidentitäten und unendliche
Vorzeichen-/Gewichtskontrollen; 49 bedingte Kernkontrollen; drei
Negativkontrollen; exakte Geometriekontrolle. Fünf mitgelieferte
Vorgängerdateien stimmen bytegenau mit den gepinnten Git-Objekten überein.
Wolfram bestätigt Q_1, M und beide Geometriekonstanten numerisch/exakt;
der unveränderte externe Output und der Anfragecode sind archiviert.

Die Kontrollen prüfen Algebra, Implementierung und numerische Einschließungen.
Sie sind keine externe wissenschaftliche Begutachtung des gesamten Kontur-,
Geometrie- oder Mecke-Beweises. Zwei Normwege teilen sich die exakte
Differentialrekursion und teilweise dieselben Spezialfunktionen; die
direkte Quadratur und Wolfram-Gegenrechnung betreffen ausdrücklich J=1.

Quellen (jeweils nur für die benannte Grundlage):

1. G. Last und M. Penrose, Lectures on the Poisson Process (2017), Theorem 4.4:
multivariate Mecke-Identität für konfigurationsabhängige nichtnegative Integranden.
https://www.math.kit.edu/stoch/~last/seite/lehrbuch_poissonp/media/lastpenrose2017.pdf

2. T. Tao, Nonlinear dispersive equations, Kapitel 2, Exercise 2.19:
Fourierdarstellung des massiven KG-Propagators. Die konkreten Konstanten
dieses Berichts werden hier hergeleitet.
https://www.math.ucla.edu/~tao/preprints/chapter.pdf

3. NIST Digital Library of Mathematical Functions, 13.4.4:
positive Integralrepräsentation von Tricomis U(a,b,z).
https://dlmf.nist.gov/13.4.E4

4. python-flint / Arb: Intervallarithmetik, Tricomi- und Gammafunktionen;
Runtime hier unverändert python-flint 0.8.0. Keine statistischen Konfidenzintervalle.
https://python-flint.readthedocs.io/en/latest/arb.html

5. Projektbasis, CSPP v0.18, PR #150:
https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/150

Die neuen Quell-, Geometrie- und Integrationsmajoranten sind eigene
Herleitungen für das genau festgelegte Modell. Die Quellen werden nicht
als Bestätigung der neuen numerischen Gesamtentscheidung ausgegeben.
