# CSPP v0.17 - Beweis und Aussagegrenzen

29. Oktober 2026. Analytische Fortsetzung von v0.16; keine neue Stichprobe.
Die Aussagen beziehen sich auf genau die bereits verwendete skalare Rekursion,
die nach t=-1 aktiv ist, und auf die vorgeschriebene lokale KG-History davor.
Sie ersetzen keinen intrinsischen diskreten Cauchy-Adapter.

## 1. Festgelegtes Modell

Minkowski-Raum in 3+1 Dimensionen, m=1, rho=3/pi, epsilon=1/16,
q=epsilon*rho=3/(16*pi), a=4*sqrt(q/6)=1/sqrt(2*pi) und
beta=a*epsilon/(a+1). Bei t=-1 ist

    f(x) = exp(1-1/(1-4|x|²)) exp(4 i x_z), |x|<1/2,
    f(x) = 0 sonst;    initiale Geschwindigkeit = 0.

Dies ist dieselbe durch das ursprüngliche Maximum A/e normierte Quelle;
f ist glatt und kompakt getragen. U löst die lokale massive KG-Gleichung
global. Für alle Sprinklingpunkte mit t<=-1 wird h=U vorgeschrieben.
Nur Punkte mit t>-1 werden rekursiv entwickelt.

Für y vor p seien n(y,p) die inneren Sprinklingpunkte im offenen
Alexandrovintervall, V=pi*(T²-r²)²/24, T=p_t-y_t und r=|p_x-y_x|.

    K(p,y) = beta*w(n(y,p)),
    w(n) = sum_{k=0}^3 c_k binom(n,k) epsilon^k (1-epsilon)^(n-k),
    (c_0,c_1,c_2,c_3) = (1,-9,16,-8).

Nicht existierende Binomialterme sind null. Die Faktoren sind
Binomialwahrscheinlichkeiten, daher gilt für jedes n: |w(n)|<=16.
Dieselbe Formel wird an kontinuierlichen Detektor-Abfragepunkten verwendet.
Der Detektor mittelt gleichmäßig über B(d,1/2), d=(0,0,3/2), und die
beiden vollständigen Fenster [3/4,1], [1,5/4].

## 2. Endliche aktive kausale Hülle

Die Vereinigung der kausalen Vergangenheiten aller Detektorpunkte hat auf
einer Zeitscheibe t<5/4 den räumlichen Querschnitt

    B(d,R(t)),   R(t)=7/4-t.

Das folgt aus dem Abstand zu einer Kugel und dem spätesten Endzeitpunkt.
Offene oder geschlossene Grenzen unterscheiden sich nur auf Nullmengen.
Der aktive Teil A besteht aus diesen Querschnitten für -1<t<5/4.
Sein Raumzeitvolumen ist 4875*pi/256 und somit endlich; die Zahl seiner
Poissonpunkte ist fast sicher endlich (Mittelwert 14625/256).

Der größte Abstand vom Ursprung auf einer solchen Scheibe ist
|d|+R(t)=13/4-t. Omega_H={|x|<H-|t|} enthält A genau ab H=21/4:
für t<=0 benötigt man H>=13/4-2t, dessen Supremum bei t nach -1 den
Wert 21/4 hat; für t>=0 genügt H>=13/4. Die Grenze ist scharf.
Beispielsweise liegt (t,x_z)=(-15/16,33/8) bei x_x=x_y=0 in A,
aber außerhalb Omega5. Der Anfangszeitpunkt selbst ist nicht aktiv.

Für H=5 fehlt A nur während -1<t<-7/8. Mit S(t)=5+t und d0=3/2
ist das fehlende Scheibenvolumen die Differenz aus Kugel und Kugellinse:

    V_slice/pi = 4R³/3
      - (R+S-d0)² [d0²+2d0(R+S)-3(R-S)²]/(12d0).

Integration ergibt V_miss=29*pi/1536. Unabhängige Poisson-Inkremente
geben für die ungesampelte Fortsetzung N_miss~Poisson(29/512), auch
bedingt auf eine feste vorhandene Konfiguration innerhalb Omega5.
P(N_miss>=1)=1-exp(-29/512)=0,055066406135... . Das ist eine exakte
Modellwahrscheinlichkeit, kein neuer Test und keine Aussage, dass das Gebiet
in der konkreten Fortsetzung leer sei. Nichts wurde neu gezogen.

Die geometrische Feststellung präzisiert v0.16: Für diesen endlichen
Anfangszeitpunkt und kompakten Detektor gibt es keinen unendlichen aktiven
Block. Unendlich bleibt die vorgeschriebene History-Forcierung.

## 3. Warum eine globale ungewichtete Absolutnorm nicht hilft

Für einen homogenen Poissonprozess gilt unter der Endpunkt-Palmverteilung
N~Poisson(rho*V). Die erzeugende Funktion liefert

    E[w(N)] = exp(-qV) P(qV),
    P(z)=1-9z+8z²-(4/3)z³,
    E[|w(N)|] <= exp(-qV) Pbar(qV),
    Pbar(z)=1+9z+8z²+(4/3)z³.

Schreibe s=T²-r²>0 und c=pi*q/24=1/128. Nach Winkelintegration ist
d⁴y=2*pi*sqrt(T²-s) ds dT. Auf jedem festen s-Intervall, auf dem
P(cs²) nicht null ist, bleibt der Kern vom wachsenden T unabhängig.
Insbesondere auf 1<=s<=2 ist P positiv. Das Integral der absoluten
Mittelwert-Kernmasse enthält daher eine positive Konstante mal
Integral sqrt(T²-s) dT und divergiert bis T=infinity.

Auch die erwartete absolute diskrete ungewichtete Zeilenmasse ist unendlich:
w(0)=1 impliziert E|w(N)|>=P(N=0)=exp(-rho*V). Campbell-Mecke und
dasselbe s-Intervall liefern die Divergenz. Aus einem unendlichen Erwartungswert
allein folgt hier ausdrücklich KEINE behauptete fast sichere Divergenz.

Die signierten Momente erklären, warum absolute und signierte Fragen
auseinanderfallen. Mit alpha=(j+1)/2 gilt

    Integral_0^infinity s^j exp(-cs²) P(cs²) ds
      = Gamma(alpha)/(2*c^alpha) * S(alpha),
    S(alpha)=-(4/3)(alpha-1/2)(alpha-1)(alpha-3/2).

Die Momente j=0,1,2 verschwinden. Das rechtfertigt weder einen Austausch
nicht absolut konvergenter globaler Integrale noch einen Schluss vom
Mittelwertoperator auf einen zufälligen Propagator. Eine KG-spezifische
gewichtete Abschätzung wird benötigt.

## 4. Schneller Abfall der festgelegten KG-History im Lichtkegelstreifen

Lemma: Für jedes feste C und jede Potenz N existiert D_(C,N)<infinity mit

    |U(t,x)| <= D_(C,N) * tau^(-N),
    tau=|t+1| >= tau_0(C),   ||x|-tau|<=C.

Außerdem ist U global beschränkt durch
M0=(2*pi)^(-3)||f_hat||_L1<infinity. Beides folgt aus der Fourierdarstellung

    U(t,x)=(2*pi)^(-3) Integral exp(i k*x) cos((t+1)*sqrt(1+|k|²)) f_hat(k) dk.

Hier ist f_hat eine Schwartzfunktion. Zum nachvollziehbaren Nachweis des
Lemmas zerlege jede der beiden Exponentialphasen mit einem glatten Cutoff
bei R=tau^(1/8). Der hochfrequente L1-Rest ist O(R^(-M)) für jedes M.
Für |k|<=2R, e=x/|x| und psi=(x/tau)*k +/- sqrt(1+|k|²) gilt bei
hinreichend großem tau, gleichmäßig im angegebenen Streifen:

    partial_e psi >= |x|/tau - |k|/sqrt(1+|k|²)
                  >= (1/20)*R^(-2) > 0.

Eine explizite Wahl ist tau_0(C)=max(1,(20C)^(4/3)): Für R>=1 gilt
1-2R/sqrt(1+4R²)>=1/(10R²), und C/tau<=1/(20R²).

Alle k-Ableitungen von psi ab Ordnung zwei sind gleichmäßig beschränkt.
Für b=1/partial_e psi gilt daher
|partial_e^j b|<=C_j R^(2j+2). Integriert man L-mal mit
exp(i*tau*psi)=(i*tau*partial_e psi)^(-1) partial_e exp(i*tau*psi)
partiell, enthalten die adjungierten Terme L Faktoren b und zusammen
höchstens L Ableitungen dieser Faktoren. Ihre L1-Schranke ist deshalb
C_L*tau^(-L)*R^(4L)=C_L*tau^(-L/2). Die benötigten L1-Normen der
Cutoff-Amplituden und ihrer Ableitungen sind durch Schwartzseminormen
von f_hat beschränkt, unabhängig von R>=1. Wahl L>=2N, M>=8N beweist
das Lemma. Komplexer Träger exp(4 i x_z) und Zeitumkehr ändern das nicht.

Dies ist ein eigenes elementares Argument im exakt flachen Fall. Der
allgemeinere schnelle Abfall massiver Wellen entlang Nullrichtungen ist
auch in Sussman, Theorem 1 und dessen anschließender verstärkter Formulierung,
beschrieben. Der Beweis hier verwendet kein aus einer Abbildung abgelesenes
Abfallgesetz und keinen numerisch angepassten Exponenten.

## 5. Absolute Summierbarkeit der History-Forcierung

Alle aktiven Abfragepunkte und Detektorpunkte p liegen im kompakten Abschluss
der Hülle aus Abschnitt 2. Damit gelten -1<=p_t<=5/4 und
|p_x|<=13/4-p_t. Für entfernte History, T=p_t-y_t, zerlege nach
s=T²-|p_x-y_x|² in s<=sqrt(T) und s>sqrt(T).

Im ersten Gebiet ist bei T>=9/2 der History-Zeitabstand
tau=-(y_t+1)=T-(p_t+1)>=T/2. Außerdem

    ||y_x|-tau| <= |p_x|+(p_t+1)+|T-sqrt(T²-s)|
                 <= 21/4.

Das Streifenlemma liefert gleichmäßig in p und y einen Faktor
C_N*T^(-N). Im zweiten Gebiet genügt |U|<=M0; dort bewirkt der
Gewichtsfaktor exp(-cs²) einen exponentiell kleinen Rest.

Die folgenden Integrale sind exakt:

    J1=Integral_0^infinity exp(-cs²) Pbar(cs²) ds = 7*sqrt(24/q),
    J2=Integral_0^infinity exp(-cs²/2) Pbar(cs²) ds = 27*sqrt(48/q).

Campbell-Mecke, die positive Majorante aus Abschnitt 3 und
sqrt(T²-s)<=T ergeben für L>=L0 und N>2. Man kann ausdrücklich
L0=1024 wählen: tau>=T/2>=512 und 512³>105⁴ garantieren das
Streifenlemma mit C=21/4. Dies ist ein Hilfspunkt der Abschätzung,
keine geänderte physikalische oder statistische Schwelle.

    E sum_{y history, T>L} |beta*w(n(y,p))*U(y)|
      <= Cnear*C_N * L^(2-N)/(N-2)
         + Cfar*M0 * exp(-L/256)*(256L+65536),

    Cnear = 21/(1+1/sqrt(2*pi)) = 15,0113412784793...,
    Cfar  = 81*sqrt(2)/(1+1/sqrt(2*pi)) = 81,8842207838265... .

Hier wurde im zweiten Gebiet
exp(-cs²)<=exp(-cT/2)*exp(-cs²/2) benutzt. In jeder endlichen
T-Spanne ist das kausale Volumen endlich, |w|<=16 und U beschränkt.
Damit ist die gesamte absolute Forcierungsreihe für jeden festen p im
Erwartungswert endlich, gleichmäßig auf dem kompakten Abfragegebiet.
Die Forcierungsreihe ist somit fast sicher absolut konvergent.

**Die Quellkonstanten C_N und M0 wurden hier nicht numerisch
eingeschlossen.** Die Formel ist eine bewiesene summierbare
Majorante mit unevaluierten Quellkonstanten, kein Zahlenzertifikat für den Rest.
T ist ein Zeitabstand; der Bereich T>L ist auch nicht der gesamte geometrische
Rest außerhalb Omega5. Der endliche Restteil muss zusätzlich behandelt werden.

## 6. Vom einzelnen Knoten zur vollständigen Detektorantwort

Campbell-Mecke ein zweites Mal, nun für die endlichvolumige aktive Hülle,
zeigt, dass mit Wahrscheinlichkeit eins alle tatsächlich vorhandenen aktiven
Knoten eine absolut summierbare History-Forcierung besitzen. Dies ist stärker
als eine lediglich punktweise Aussage für einen vorher festgelegten p.
Tonelli über den kompakten Raumzeitdetektor zeigt zusätzlich die fast sichere
Integrierbarkeit der absoluten direkten Historysumme im Detektor.

Ordne die endlich vielen aktiven Knoten kausal. K_AA ist streng dreieckig.
Mit g_A(p)=sum_history K(p,y)h(y) folgt

    v_A = (I-K_AA)^(-1) g_A,
    (I-K_AA)^(-1) = sum_{j=0}^{n_A-1} K_AA^j.

Für n_A=0 ist der aktive Beitrag leer. Die normierten Detektorkoeffizienten
Q_A haben komponentenweise |Q_i|<=16*beta. Die Antwort ist somit

    A_infinity = averaged_detector[g(p)] + Q_A (I-K_AA)^(-1) g_A,

und für jedes Fenster fast sicher endlich. Für H>=21/4 sind alle aktiven
Knoten erfasst. Kausale Konvexität von Omega_H erhält alle Intervallzahlen
zwischen bereits enthaltenen Endpunkten. Daher konvergieren die Antworten
der verschachtelten Diamanten gegen diese Antwort: absolute Summierbarkeit
der History, ein nun fester endlicher aktiver Inversenblock und dominierte
Konvergenz für die direkte Detektorintegration genügen.

Es wird keine dichteuniforme oder realisierungsuniforme Schranke auf diese
Inverse behauptet. Ihr Gewinn ist endlich für jede endliche Realisierung,
kann aber von deren Knoten und Kanten abhängen. Insbesondere darf ein
Erwartungswert von Gewinn mal Forcierung nicht ohne Beweis faktorisiert werden.

Die Existenz gilt auch für unabhängige Poissonfortsetzungen jeder festen
endlichen Archivkonfiguration in einem beschränkten Gebiet B. Für ein
Intervall zerfällt seine Punktzahl in einen festen Teil n0<=N_B und
einen Poissonteil mit Mittelwert mu=rho*|I\B|. Die exakte Identität lautet

    E[binom(n0+N,k) eps^k (1-eps)^(n0+N-k)]
     = exp(-eps*mu) sum_{j=0}^{min(k,n0)}
       binom(n0,j) eps^j (1-eps)^(n0-j) (eps*mu)^(k-j)/(k-j)!.

Da eps*mu<=qV und exp(-eps*mu)<=exp(q|B|)*exp(-qV), folgt eine
Majorante D_B*exp(-qV)*Pbar(qV) mit einer endlichen, vom festen Archiv
abhängigen Konstanten D_B. Die vorigen Integrabilitätsargumente bleiben
gültig; die endlichen vorgeschriebenen Archivbeiträge sind unproblematisch.
Das bestimmt keine konkrete noch unbekannte Fortsetzung.

## 7. Anschlussentscheidung

Erreicht: scharfe endliche aktive Hülle, exakte noch fehlende aktive Geometrie,
analytische absolute Historysummierbarkeit und fast sichere Existenz der
vollständigen Antwort für das festgelegte Modell. Dadurch wird die in v0.16
offene Existenzfrage präzisiert und analytisch beantwortet.

Weiter NOT_CERTIFIED: ein numerischer, transportierter Rest ab Omega5 für
die vier Archive und damit eine globale Genauigkeitsentscheidung zum Ziel
0,001. Die acht endlichen Genauigkeitsausschlüsse aus v0.16 bleiben gültig
für Omega5. Sie sind kein automatisch bewiesener Ausschluss der unendlichen
Fortsetzung. Ihre notwendige Reparaturgröße bleibt eine notwendige Bedingung,
keine Untergrenze des tatsächlichen unbekannten Rests.

Nächster Rechenschritt: die Quellseminormen durch analytische Ableitungs-
und Fourier-L1-Schranken explizit einschließen; den endlichen Bereich außerhalb
Omega5 sowie den zufälligen aktiven Transport gemeinsam behandeln. Eine
neue Stichprobe oder eine neue statistische Freigaberegel wird dabei nicht
stillschweigend eingeführt. METHOD_HOLD und G1 HOLD bleiben bestehen.

## 8. Herkunft und unabhängige Kontrollen

Projektbasis: PR #148, Merge 5c075bfae81ee6ab5edea72a8ec9aa9ed3583b69;
Quellcommit 4088a427a5b3fa6a8c2bad7363b64a5c991dcd85.
https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/148

E. Sussman, Massive Wave Propagation Near Null Infinity, Annals of PDE 12,
Article 9 (2026), Theorem 1; DOI 10.1007/s40818-026-00232-8.
https://arxiv.org/abs/2305.01119
https://link.springer.com/article/10.1007/s40818-026-00232-8
Nur externer Kontext für den KG-Abfall, keine Quelle unserer Volumenwerte
oder numerischer Quellkonstanten. Das flache Fourierargument steht oben.

G. Last und M. Penrose, Lectures on the Poisson Process, Cambridge University
Press (2017), Theorem 4.1 (Mecke-Gleichung), Kapitel 3 (Poissonprozess).
https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf
Diese Identität erlaubt die hier verwendeten nichtnegativen Integranden,
die sowohl vom Endpunkt als auch von der übrigen Punktkonfiguration abhängen.

Die Volumenpolynome werden zusätzlich zur Kugellinsenformel unabhängig durch
axiale Kreisscheibenintegration mit rationaler Intervallzerlegung berechnet.
Wolfram bestätigt die beiden exakten Volumina, die Momentfaktorisierung und
den ersten Restkoeffizienten; sein unveränderter Output ist beigelegt.
Die algebraischen Kontrollen sind keine automatische formale Verifikation
des gesamten analytischen Beweises und keine externe wissenschaftliche Prüfung.
