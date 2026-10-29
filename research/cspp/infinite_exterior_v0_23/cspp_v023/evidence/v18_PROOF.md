# CSPP v0.18 - Explizite und vollständig transportierte Restmajoranten

29. Oktober 2026. Fortsetzung von v0.17, PR #149, Merge
808cd43ddc840a6fd87c9095e7698b58f85846a7. Analytische Entwicklungsarbeit
mit vier vorhandenen Archiven; keine neue Wolke oder statistische Freigaberegel.

## 1. Ergebnis und Reichweite

Der Existenzbeweis aus v0.17 erhält hier numerisch eingeschlossene
Quellkonstanten und eine Majorante für ALLE kausalen Transportpfade.
Für die vier festen Omega5-Archive wird der Erwartungswert des absoluten
Restes über unabhängige ideale Poissonfortsetzungen außerhalb Omega5
begrenzt. Die Abhängigkeit zwischen Forcierung und Pfadgewichten wird
durch die multivariate Mecke-Identität behandelt, nicht durch eine
unzulässige Faktorisierung von Erwartungswerten.

Die neue globale Schichtgewichtsschranke ist exakt
kappa=4976184375/4294967296=1,15860821097157895565... . Sie ersetzt
die grobe Zahl 16 in der Abschätzung aktiver Pfade. Daraus folgen bedingte
Pfadfaktoren von etwa 2,73 bis 3,79. Diese moderaten Faktoren machen die
globale Majorante noch nicht praktisch brauchbar: Bereits die pauschale
Feldschranke M0 liegt bei etwa 1,52 Milliarden; die pauschale
Archivkonditionierung kostet einen weiteren Faktor von etwa 1,36*10^35.

Die kleinsten im erklärten analytischen Gitter erhaltenen Obergrenzen für
E[|A_infinity-A5| | Archiv] liegen daher bei etwa 1,3 bis 1,8*10^54.
**Das sind große OBERGRENZEN, kein Nachweis großer tatsächlicher Fehler.**
Der konkrete Rest kann sehr viel kleiner sein. Die Rechnung erlaubt weder
eine Genauigkeitsfreigabe noch eine Verwerfung der Operatorfamilie.

## 2. Unveränderte Definitionen

Minkowski-Raum in 3+1 Dimensionen, m=1, rho=3/pi, eps=1/16,
q=3/(16*pi), a=1/sqrt(2*pi), beta=a/[16(1+a)]. Bei t=-1 sind

    f(x)=exp(1-1/(1-4|x|²)) exp(4 i x_z),   |x|<1/2,
    f=0 außerhalb;   Anfangsgeschwindigkeit=0.

Die lokale KG-Lösung U schreibt die History bei t<=-1 vor. Nur t>-1
wird diskret entwickelt. Die Quelle bleibt durch ihr ursprüngliches
Maximum A/e normiert. Der Detektor mittelt über die Kugel mit Mittelpunkt
(0,0,3/2), Radius 1/2, in den beiden ganzen Fenstern [3/4,1], [1,5/4].

    w(n)=sum_{k=0}^3 c_k binom(n,k) eps^k (1-eps)^(n-k),
    c=(1,-9,16,-8),   K(p,y)=beta*w(n(y,p)).

Für y vor p: T=p_t-y_t, s=T²-|p_x-y_x|²>0,
V=pi*s²/24. Die aktive Hülle A hat Volumen 4875*pi/256 und liegt
vollständig in Omega_(21/4). In B=Omega5 fehlen darin nur Punkte mit
Poisson-Mittelwert lambda_miss=29/512. Diese v0.17-Geometrie bleibt unverändert.

## 3. Scharfe globale Gewichtsschranke

Schreibe r=15/16 und u=1/15. Dann ist

    w(n)=r^n [1-9nu+8n(n-1)u²-(4/3)n(n-1)(n-2)u³].

Rationale Auswertung für 0<=n<=128 ergibt den größten Betrag bei n=8:
|w(8)|=kappa. Für n>=128 gilt die positive Majorante

    |w(n)| <= B(n)=r^n [1+9nu+8n²u²+(4/3)n³u³].

Jeder ihrer vier Terme fällt dort monoton, denn
r*((129/128)^3)<1 begrenzt alle aufeinanderfolgenden Quotienten.
Zudem ist B(128)<kappa, ebenfalls exakt rational geprüft. Das beweist
|w(n)|<=kappa für ALLE nichtnegativen ganzen n. Die scheinbar naheliegende
Schranke 1 ist falsch; n=8 ist eine explizite Negativkontrolle.
Im Folgenden gamma=beta*kappa=0,02065032490315605... .

## 4. Explizite Quellkonstanten aus komplexen Kreisscheiben

Für einen reellen Einheitsvektor e und 0<=delta<=1/2 definiere
g_(delta,e)(x)=exp(delta*e*x) f(x), mit Nullfortsetzung außerhalb der
Quellkugel. Alle benötigten Richtungen werden gleichzeitig kontrolliert.

Sei im Inneren h=1-4|x|² in (0,1]. Für komplexe Inkremente mit
|z_j-x_j|<=h/40 bleibt der Nenner 1-4 sum z_j² innerhalb eines
Kreises um h mit Radius h/5: Die Änderung ist höchstens
4*sqrt(3)*(h/40)+12*(h/40)²<h/5. Daraus folgen

    Re[1/(1-4 sum z_j²)] >= 5/(9h) > 1/(2h),
    |g_(delta,e)(z)| <= exp(11/8) exp(-1/(2h)).

Im zweiten Schritt wurden delta|x|<=1/4 und
(delta*sqrt(3)+4)*(h/40)<=1/8 benutzt. Die 4 stammt unverändert
vom komplexen Träger exp(4 i x_z).

Die mehrdimensionale Cauchyabschätzung liefert für Multiindizes alpha,
n=|alpha|,

    |partial^alpha g(x)|
      <= alpha! * 40^n * h^(-n) * exp(11/8) * exp(-1/(2h)).

Das Maximum des h-abhängigen Faktors ist
m_0=exp(-1/2) beziehungsweise m_n=(2n/e)^n für n>=1.
Diese Darstellung zeigt zugleich das Verschwinden aller Ableitungen
am Rand der Quellkugel; die glatte Nullfortsetzung ist zulässig.

Setze

    S_j=sum_{a+b+c=j} [j!/(a!b!c!)] (2a)!(2b)!(2c)!,
    D_J=(pi/6) exp(11/8) sum_{j=0}^J binom(J,j) 40^(2j) S_j m_(2j).

Da pi/6 das Quellvolumen ist, folgt gleichmäßig für alle e und delta:

    ||(1-Delta)^J g_(delta,e)||_L1 <= D_J.

Dies ist eine bewusste Dreiecksabschätzung ohne Ausnutzung der inneren
Ableitungsaufhebungen. Alle D_J sind explizite endliche Summen.
Beispielsweise S_0=1, S_1=6, S_2=96 und S_5=14618880.
Die Koeffizienten werden unabhängig durch wiederholte Anwendung des
formalen Laplaceoperators auf Ableitungsmultiindizes geprüft.

## 5. Quantitativer KG-Abfall durch Konturverschiebung

Mit tau=|t+1| gilt

    U(t,x)=(2*pi)^(-3) Integral exp(i k*x)
      cos(tau*sqrt(1+|k|²)) f_hat(k) d³k.

Die Fouriertransformierte der glatten kompakten Quelle ist ganz und fällt
in jedem festen imaginären Streifen schneller als jede inverse Potenz.
Die Funktion cos(tau*sqrt(z)) ist als Funktion von z ganz. Deshalb kann
die Integrationskontur auf k+i*e/2 verschoben werden; die Randflächen
verschwinden im Grenzübergang. Wähle e=x/|x|, bei x=0 beliebig.
Das Argument ist für jedes feste tau gültig; es setzt keinen unbekannten
asymptotischen Übergang voraus.

Für omega=sqrt(1+(k+i*e/2)²) mit positivem Realteil ist
Re(omega)>=sqrt(|k|²+3/4) und

    |Im(omega)| <= |k|/[2*sqrt(|k|²+3/4)],
    1/2-|Im(omega)| >= 3/[16*(1+|k|²)].

Hier wird keine Stationärphasen-Näherung verwendet. Für | |x|-tau |<=C
folgt direkt

    |U(t,x)| <= (2*pi)^(-3) exp(C/2) D_J
      Integral (1+|k|²)^(-J)
        exp(-3*tau/[16*(1+|k|²)]) d³k.

Die Ungleichung exp(-z)<=N!/z^N, J=N+2 und
Integral (1+|k|²)^(-2) d³k=pi² ergeben für jedes ganze N>=0 und tau>0

    |U(t,x)| <= exp(C/2) N! (16/3)^N D_(N+2)/(8*pi*tau^N).

Ohne Konturverschiebung folgt zusätzlich die globale Feldschranke

    |U(t,x)| <= M0=D_2/(8*pi) < 1,520*10^9.

Für alle p im aktiven Detektorvergangenheitsgebiet liefert die Zerlegung
s<=sqrt(T) aus v0.17 den Streifen C=21/4. Bei T>=9/2 gilt tau>=T/2.
Damit sind die zuvor unbestimmten Konstanten jetzt explizit:

    C_N=exp(21/8) N! (32/3)^N D_(N+2)/(8*pi),
    |U(y)| <= C_N*T^(-N)   im Bereich s<=sqrt(T).

Der frühere Hilfsübergang L0=1024 ist für diese neue Abschätzung nicht
mehr erforderlich. Das Rechengitter beginnt bei L=8. Das verändert
keine physikalische Skala, Quelle oder statistische Schwelle.

## 6. Ein-Schritt-Rest und explizite Archivkonditionierung

Sei

    Pbar(z)=1+9z+8z²+(4/3)z³,
    c=1/128,
    Cnear=21/(1+1/sqrt(2*pi)),
    Cfar=81*sqrt(2)/(1+1/sqrt(2*pi)).

Die Poisson-Gewichtsmajorante ist E|w(N)|<=exp(-qV)Pbar(qV).
Der Nachweis aus v0.17 bleibt mit den jetzt expliziten Konstanten gültig:

    b_N(L)=Cnear*C_N*L^(2-N)/(N-2)
      + Cfar*M0*exp(-L/256)*(256L+65536),   N>2, L>=9/2.

Dies begrenzt gleichmäßig in p den Erwartungswert der absoluten
direkten History-Forcierung mit T>L. Insbesondere begrenzt es die
kleinere Menge tau>L, weil T=tau+(p_t+1)>=tau.

Nun wird die vorhandene endliche Konfiguration in B=Omega5 festgehalten
und nur außerhalb B ein unabhängiger idealer Poissonprozess betrachtet.
Für ein Intervall sei n0 die feste innere Punktzahl und
z0=eps*rho*|I\B|. Die Faltung mit der Binomialverteilung ergibt

    E|w(n0+N)| <= exp(-z0) sum_{j=0}^3 b_(n0,j) R_j(z0),
    b_(n0,j)=binom(n0,j) eps^j (1-eps)^(n0-j),
    R_0=Pbar, R_1=9+16z+4z², R_2=16+8z, R_3=8.

Die b_(n0,j) sind nichtnegative Wahrscheinlichkeiten mit Summe <=1.
Jedes R_j ist koeffizientenweise durch 16*Pbar begrenzt. Zudem gilt
z0<=qV und qV-z0<=q|B|=625/8. Daher

    E[|w(n0+N)| | Archiv] <= D_B exp(-qV)Pbar(qV),
    D_B=16*exp(625/8) < 1,360*10^35.

D_B ist für jedes endliche Archiv gültig, aber absichtlich sehr grob:
Die tatsächlichen n0 und Überlappungen |I intersect B| wurden durch
globale Maxima ersetzt. Diese Zahl ist weder ein gemessener
Verstärkungsfaktor noch ein Nachweis großer physikalischer Fluktuationen.

## 7. Vollständiger kausaler Transport ohne Unabhängigkeitsannahme

Schreibe die endliche aktive Inverse als Pfadsumme. Ein Beitrag zur
Detektorantwort hat eine Historywurzel y und eine streng zeitgeordnete
Kette aktiver Punkte y vor p_k vor ... vor p_1 vor p. Jede aktive Kante
hat Betrag <=gamma. Die Historykante ist beta*w(n(y,p_k))*U(y).

Wende die multivariate Mecke-Identität auf die unbekannten Kettenpunkte
und auf y an. Die zusätzlich eingesetzten aktiven Kettenpunkte liegen
alle SPÄTER als p_k und daher nicht im offenen Historyintervall I(y,p_k).
Sie verändern dessen Punktzahl nicht. Die übrigen aktiven Gewichte
werden punktweise durch gamma begrenzt. So bleibt die bedingte
Historymajorante D_B*b_N(L) gültig, ohne Erwartungswerte von abhängigen
Zufallsgrößen auseinanderzuziehen.

Seien n_B die bekannten aktiven Knoten des Archivs in A und
lambda_miss=29/512 der Mittelwert der fehlenden aktiven Punkte.
Nach Weglassen räumlicher Kausalbedingungen hat jede gewählte Teilmenge
höchstens eine zeitliche Reihenfolge. Summieren über m bekannte und l
unbekannte Punkte ergibt

    G_B=sum_{m=0}^{n_B} binom(n_B,m) gamma^m
          * sum_{l=0}^infinity (gamma*lambda_miss)^l/l!
       =(1+gamma)^n_B exp(gamma*lambda_miss).

Für beide normierten Detektorfenster gilt somit

    E[|vollständig transportierter Historyrest tau>L| | Archiv]
       <= G_B*D_B*b_N(L).

Ohne Archivkonditionierung lautet der entsprechende Faktor
G0=exp(gamma*14625/256)<3,254. Dann steht rechts G0*b_N(L), ohne D_B.
Diese Formeln sind Schranken für die vollständig transportierte
ERWARTUNG. Sie behaupten keine realisierungsuniforme Verstärkung
und keine Unabhängigkeit zwischen Quelle, Geometrie und Transport.

Die archivierten aktiven Knotenzahlen sind 65, 49, 59, 50. Daraus folgen
die nach oben gerundeten Faktoren 3,781; 2,726; 3,344; 2,782.
Die Quelldatei mit diesen Geometriezahlen wird unverändert mitgeliefert.
Keine neue Wolke wird erzeugt und keine fehlende aktive Realisierung
stillschweigend auf leer gesetzt.

## 8. Vom Zeitrest zum geometrischen Rest hinter Omega5

Kausale Konvexität liefert eine wichtige Vereinfachung: Liegen Historywurzel
und Detektorpunkt beide in Omega5, so liegen auch alle aktiven Punkte
eines verbindenden kausalen Pfades und alle Intervallzählpunkte darin.
Deshalb ist A_infinity-A5 exakt die Summe jener vollständigen Pfade,
deren HISTORYWURZEL außerhalb Omega5 liegt. Die Wirkung unbekannter
aktiver Punkte ist bereits in diesen Pfaden enthalten. Ein zusätzlicher
unabhängiger aktiver Fehlerterm wird nicht hinzugefügt.

Bei tau=-(y_t+1) hat die KG-History Stütze in |y_x|<=tau+1/2.
Bis tau=7/4 liegt diese Stütze vollständig in Omega5. Für 7/4<tau<4
ist der ausgelassene Stützenquerschnitt eine Kugelschale mit Radien
tau+1/2 und 4-tau; danach fehlt die ganze Quellstütze.
Für L>=4 hat die ausgelassene Stütze bis tau=L Poisson-Mittelwert

    mu_ext(L)=(L+1/2)^4-6561/128.

Für den endlichen Teil gilt die universelle punktweise Gewichtsschranke
gamma und |U|<=M0. Mit Abschnitt 7 folgt deshalb

    E[|A_infinity-A5| | Archiv]
      <= G_B * [gamma*M0*mu_ext(L) + D_B*b_N(L)] = B5_N(L).

Dies ist erstmals eine vollständig explizite, numerisch ausgewertete
L1-Majorante für den gesamten geometrischen Rest der vier Archive.
Sie ist jedoch zu grob, um das Genauigkeitsziel zu beurteilen.

Für die Beziehung zu größeren Diamanten genügt
H>=max(21/4,2L+3/2): Dann liegen alle aktiven Punkte und sämtliche
nichtverschwindenden Historywerte mit tau<=L in Omega_H. Folglich

    E[|A_infinity-A_H| | Omega5-Archiv] <= G_B*D_B*b_N(L).

Auch dies mittelt über unbekannte Fortsetzungen außerhalb des ursprünglichen
Omega5-Archivs; es ist keine Konditionierung auf ein neu erzeugtes Omega_H.

## 9. Auswertung, Grenzen und Entscheidung

Vor der Ergebnisproduktion wurden die analytischen Kandidaten N=3,...,32
und L=2^j, j=3,...,80 festgehalten. Auswahl der kleinsten gültigen
Obergrenze ist deterministische Schrankenoptimierung, keine Anpassung
einer statistischen Freigaberegel. Alle Gitterwerte werden ausgegeben.
Die gewählte N-Ordnung wird anschließend durch Intervallvergleiche als
kleinste der jeweiligen endlichen Familie bestätigt.

Die besten ausgewerteten B5_N(L) treten bei L=2^38 und N=11 auf.
Nach oben gerundet lauten sie für d0_r00 bis d0_r03:
1,80*10^54; 1,30*10^54; 1,59*10^54; 1,32*10^54.
Keine dieser Zahlen ist eine Untergrenze des tatsächlichen Rests.
Auch die acht endlichen Genauigkeitsausschlüsse aus v0.16 werden dadurch
nicht automatisch auf die unendliche Fortsetzung übertragen.

Auf dem erklärten Gitter fällt die bedingte transportierte FERNE History-
Majorante erstmals bei L=2^48=281474976710656 unter den Vergleichsmaßstab
0,001. Dort liefert N=32 für alle vier Archive weniger als 4,719*10^-9.
Ein hinreichender Diamantparameter wäre H=2L+3/2. Die formale zusätzliche
History-Stütze hätte bereits einen Poisson-Mittelwert von rund 6,28*10^57.
Das ist eine Diagnose der Grobheit DIESER Abschätzung. Es ist weder eine
notwendige Gebietsgröße noch eine allgemeine Rechenkostenuntergrenze.
Ohne Archivkonditionierung liegt der erste entsprechende Gitterwert bei
L=2^44. Auch dieser Wert ist kein Genauigkeitszertifikat für die vier Archive.

Eine Aussage E|R|<=b ist außerdem keine Aussage |R|<=b für eine konkrete
Realisierung. Markovs Ungleichung ergäbe lediglich P(|R|>eta)<=b/eta.
Es wird kein neues alpha gewählt und keine Wahrscheinlichkeitsschwelle
als bereits bestanden ausgegeben. Der Maßstab 0,001 dient hier nur zum
Vergleich der L1-Majoranten; das ursprüngliche individuelle Fehlerziel
bleibt unverändert und NOT_CERTIFIED.

**Entscheidung:** Keine Gebietserweiterung oder neue Stichprobe auf Basis
dieser globalen Majorante starten. Der nächste sinnvolle rechnerische
Ansatz muss die tatsächlichen Quellableitungen und Archiv-Intervallüberlappungen
nutzen, anstatt M0 und D_B durch diese pauschalen Maxima zu ersetzen.
Der moderate Pfadfaktor allein ist in der vorliegenden Abschätzung nicht
der dominierende Engpass. METHOD_HOLD und G1 HOLD bleiben bestehen.

## 10. Validierung und Herkunft

Rationale globale Schichtgewichtskontrolle mit Beweis des unendlichen
Restbereichs; unabhängige Laplace-Koeffizientenrekursion; unabhängige
exakte Stützenvolumenintegration; endliche positive Pfadgraphen;
drei Negativkontrollen; 857 Intervallvergleiche zwischen 128 und 192 Bit;
Prüfung unveränderter Eingabedateien. Wolfram bestätigt zusätzlich kappa,
ausgewählte S_j, ein Stützenvolumen, das Fourier-Radialintegral sowie M0
und D5. Symbolhinweise seines Ausgabekanals werden unverändert archiviert;
die ausgewerteten Zahlen stimmen mit den lokalen Einschließungen überein.

Die Programmprüfungen kontrollieren Algebra und numerische Einschließungen.
Sie sind keine automatische formale Verifikation der Kontur- und
Mecke-Argumente und keine unabhängige wissenschaftliche Begutachtung.

Projektbasis und unveränderte Modellbeschreibung:
https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/149

G. Last und M. Penrose, Lectures on the Poisson Process, Cambridge
University Press (2017), Theorem 4.4, multivariate Mecke-Identität.
Die Quelle begründet den Einsatz konfigurationsabhängiger nichtnegativer
Integranden; die konkrete Pfadmajorante dieses Berichts ist hier hergeleitet.
https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf

Der Quellnorm- und Konturbeweis in Abschnitten 4-5 ist eine eigene
elementare Herleitung für die exakt vorgegebene flache KG-Lösung.
Es wird kein neuer physikalischer Operator und kein angepasster Abfallexponent
als experimentell bestätigt bezeichnet.
