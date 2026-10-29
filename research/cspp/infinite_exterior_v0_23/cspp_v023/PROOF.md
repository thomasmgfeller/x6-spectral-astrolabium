# CSPP v0.23: unendlicher Außenhistory-Rest und globale Bilanz

29. Oktober 2026. Basis ist der nach PR #154 verifizierte Main-Commit
`fdf99cd95330eea4151ba32305e9ea8f2f06f2b2`. Dies führt Schritt 2 aus.
Die physikalische Quelle, der Operator, die Archive, die Detektorfenster
und sämtliche statistischen Regeln bleiben unverändert.

## 1. Aussage und disjunkte Wurzelbereiche

Sei B=Omega5=I((-5,0),(5,0)), tau=-t-1 für t<=-1. Die vollständige
äußere History zerfällt bis auf Nullränder in

    D5: 0<=tau<=5, y außerhalb B, auf dem vollständigen KG-Träger;
    Dinf: tau>5, auf dem vollständigen KG-Träger.

Bei tau>5 ist die ganze Zeitscheibe außerhalb B. Für tau<=7/4 ist der
äußere Beitrag exakt null. Der alte Patch P aus v0.20/v0.21 ist schon
genau einmal in D5 enthalten. D5 wird unverändert aus v0.22 übernommen.
Die Fläche tau=5 hat Vierervolumen null und unter dem äußeren Poissonprozess
fast sicher keine Punkte. Die Rechengrenze schneidet die physikalische
History nicht ab. Es werden alle Raumrichtungen behandelt.

Für jede der vier unveränderten Archivkonfigurationen und jedes Fenster
folgt aus den unten bewiesenen integrierbaren Majoranten

    E(|A_infinity-A5| | Archiv in B) <= B_finite_v022 + B_tail_v023.

Es wird eine obere bedingte Erwartungswertschranke berechnet, keine
gemessene Abweichung, keine untere Fehlergrenze und keine Garantie für
eine einzelne Realisierung. METHOD und G1 bleiben HOLD. Das unveränderte
globale Ziel 0,001 ist nicht bewiesen. Eine große obere Grenze widerlegt
weder die Genauigkeit noch die Operatorfamilie.

## 2. Übernommene Konstanten und Pfadstruktur

Es gelten m=1, rho=3/pi, epsilon=1/16,
beta=1/[16(1+sqrt(2pi))], kappa=4976184375/4294967296 und gamma=beta*kappa.
Das Anfangsfeld bei t=-1 ist

    f(x)=exp(1-1/h) exp(4 i z), h=1-4|x|², |x|<1/2,

glatt nullfortgesetzt; die Anfangsgeschwindigkeit ist null. Die exakte
KG-Lösung wird für t<=-1 als History vorgeschrieben. Der Detektor mittelt
normiert über B((0,0,3/2),1/2) und W0=[3/4,1], W1=[1,5/4].

Die in v0.19 validierten Normen Q_J=||(1-Delta)^J f||_2², J=0,...,34,
und M=sqrt(Q_1/(8pi)) werden unverändert verwendet. Es gilt weltweit
|U|<=M und ||U(t)||_2<=sqrt(Q_0); Letzteres folgt direkt aus Plancherel
und |cos(tau sqrt(1+|k|²))|<=1. Die Normintervalle aus 384 und 512 Bit
werden erneut auf Überlappung kontrolliert. Ihre Ableitungsrekursion,
unabhängige Integrationsidentität und ursprüngliche Quadraturen sind
in `evidence/v19_PROOF.md` dokumentiert; sie werden hier nicht als neue
Normberechnung ausgegeben.

Die 65,49,59,50 bekannten aktiven Punkte und die v0.20-Adjungierten a_j
bleiben erhalten. Für unbekannte aktive Punkte gilt lambda=29/512.
Die vollständigen Koordinatenarrays, aktiven Teilmengen und 14 übernommenen
Eingabedateien werden über SHA256 und die Git-Blobs des Basis-Commits geprüft.

## 3. Einseitiger Streifen nahe dem Lichtkegel

Für einen ersten aktiven oder direkten Detektorendpunkt p setze

    sigma=p_t+1>=0, T=p_t-y_t=tau+sigma,
    r=|p_space-y_space|, s=T²-r²>=0.

Teile den kausalen Wurzelbereich bei s=sqrt(tau). Im nahen Teil gilt
r>=sqrt(T²-sqrt(tau)) und, für tau>=5,

    T-r <= tau-sqrt(tau²-sqrt(tau)) <= 1/4.

Die erste Ungleichung benutzt die Monotonie in T>=tau. Für die zweite
genügt sqrt(tau)<=tau/2-1/16: bei tau=5 gilt (39/16)²>5, und
die rechte Seite minus sqrt(tau) ist auf [5,infinity) streng steigend.
Mit R=|y_space| folgt

    tau-R <= |p_space|-sigma+1/4 = C_p.

Diese EINSEITIGE Streifenbedingung reicht für den Konturbeweis aus.
Ist C_p<=-1/2, liegt der nahe Teil ganz außerhalb des Quellenlichtkegels
R<=tau+1/2; U verschwindet dort exakt. Auch für negative C_p>-1/2
bleibt der folgende exponentielle Vorfaktor gültig.

Für Endpunktzellen werden obere und untere Radien/Zeitgrenzen verwendet:
C_upper=r_hi-(t_lo+1)+1/4, sigma_upper=t_hi+1. Für einen beliebigen
aktiven Punkt p vor einem Detektorpunkt d aus einem Fenster mit tmax gilt
|p_space|<=2+tmax-p_t und daher einheitlich

    C_p<=tmax+13/4,  sigma<=tmax+1.

Das deckt auch noch unbekannte aktive Punkte außerhalb B ab.

## 4. Engere Konturmajorante ohne asymptotischen Übergang

Fourierkonvention: f_hat(k)=Integral e^(-ik.x)f(x)dx, inverse Normierung
(2pi)^(-3). Für jeden festen tau lässt sich die Kontur auf k+i delta e
verschieben, e=y_space/R, 0<delta<1. Die Fouriertransformierte der glatten
kompakten Quelle ist ganz, und cos(tau sqrt(z)) ist ganz in z; die
seitlichen Integrationsflächen verschwinden durch schnellen Fourierabfall.
Das ist derselbe Konturschritt wie v0.18, nun mit allgemeinem delta.

Schreibe omega=sqrt(1+(k+i delta e)²) mit positivem Realteil. Dann

    Re omega>=sqrt(|k|²+1-delta²),
    |Im omega|<=delta |k|/sqrt(|k|²+1-delta²),
    delta-|Im omega|>=delta(1-delta²)/[2(1+|k|²)].

Die letzte Ungleichung folgt aus 1-sqrt(1-x)>=x/2 und
|k|²+1-delta²<=1+|k|². Setze A=1+|k|² und d=delta(1-delta²)/2.
Für g=exp(delta e.x)f ergibt sich aus tau-R<=C

    |U| <= (2pi)^(-3) exp(delta C)
            Integral exp(-d tau/A) |g_hat(k)| dk.

Konjugation von H=1-Delta liefert
H^J g=exp(delta e.x)(H-2delta e.grad-delta²)^J f.
Auf der Quellstütze ist exp(delta e.x)<=exp(delta/2). Der Betrag des
Fouriermultiplikators des konjugierten Operators ist höchstens
A+delta²<=(1+delta²)A. Somit gilt

    ||H^J g||_2 <= exp(delta/2)(1+delta²)^J sqrt(Q_J).

Nach Cauchy-Schwarz im Fourierintegral und Plancherel verbleibt

    K_J(a)=Integral_R3 (1+|k|²)^(-2J) exp(-a/(1+|k|²)) dk,
    a=delta(1-delta²) tau.

Die Substitution u=1/(1+|k|²) ergibt exakt

    K_J(a)=2pi Integral_0^1 u^(2J-5/2)(1-u)^(1/2)e^(-au) du
           <=2pi Gamma(2J-3/2) a^(-(2J-3/2)).

Hier wurden nur (1-u)^(1/2)<=1 und eine positive Gebietserweiterung
auf [0,infinity) benutzt. Für jedes J>=1 gilt folglich, für ALLE tau>0
im angegebenen Streifen,

    |U| <= C_(J,delta)(C) tau^(-p_J),  p_J=J-3/4,
    C_(J,delta)(C)=exp(delta(C+1/2))(1+delta²)^J sqrt(Q_J)
      *sqrt(Gamma(2J-3/2))/(2pi)
      *[delta(1-delta²)]^(-p_J).

Es wird kein unbekannter Zeitpunkt für das Einsetzen eines asymptotischen
Abfalls vorausgesetzt. Die endliche Familie J=1,...,34 und
delta=j/16, j=1,...,15, liefert ausschließlich Hilfsmajoranten. Sie ändert
keine physikalischen oder statistischen Parameter. Alle gewählten
Koeffizienten und Exponenten werden gespeichert.

## 5. Vollständige Integration der nahen Hülle

Für jeden Endpunkt werden die gültigen Hüllen M und C_J tau^(-p_J)
über die vollständige feste Partition [5,8], [2^j,2^(j+1)] für
j=3,...,47, [2^48,infinity) integriert. Auf jeder endlichen Zelle
wird die kleinste gültige integrierte Obergrenze gewählt, nicht ein
Punktwert. Auf der letzten Zelle werden nur J>=3 verwendet, also p_J>2.

Die benötigten Primitive sind exakt:

    Integral_L^U (tau+sigma)tau^(-p) d tau
      = (U^(2-p)-L^(2-p))/(2-p)
        +sigma (U^(1-p)-L^(1-p))/(1-p),
    Integral_L^infinity (tau+sigma)tau^(-p) d tau
      = L^(2-p)/(p-2)+sigma L^(1-p)/(p-1), p>2.

Keiner der Viertel-Exponenten ist 1 oder 2. Für M ist die Integration
ein Polynom. Die Summe der Zellobergrenzen heißt J_near(L;sigma,C).
Der nahe Teil ist damit bis infinity geschlossen. Die Auswahl kleiner
Obergrenzen aus einer endlichen bewiesenen Familie ist keine statistische
Modellauswahl und beansprucht kein globales Optimum aller Abschätzungen.

## 6. Bedingter Kern und geometrische Überlappung

Die punktweise Schranke |w(n)|<=kappa und die Poisson-Faltung aus v0.19
gelten unverändert. Mit z=s²/128, Pbar(z)=1+9z+8z²+(4/3)z³ gilt

    E(|w(n0+N)| | B)<=D exp(-s²/128)Pbar(s²/128), D=16 exp(Q).

Für bekannte Endpunkte oder Detektorendpunkte in B ist
Q=[(p_t+5)²-|p_space|²]²/128 eine obere Grenze für
epsilon rho |I(y,p) Schnitt B|, denn dieser Schnitt liegt in I(b,p).
Für eine Endpunktzelle genügen t_hi und r_lo. Für beliebige aktive p vor
einem Detektorpunkt d gilt stattdessen I(y,p) Schnitt B Teilmenge I(b,d),
also einheitlich Qwin=[(5+tmax)²-1]²/128. Die Bedingung p in B wird hier
ausdrücklich nicht benötigt. Qwin bleibt 1225/128 bzw. 370881/32768.

Für jedes S=8,12,...,128 ist deshalb die stückweise Hülle

    H_S(s)=kappa für 0<=s<=S,
           D exp(-s²/128)Pbar(s²/128) für s>S

gültig. I0(S)=Integral_0^infinity H_S(s)ds und sämtliche folgenden Momente
sind endliche positive Summen oberer unvollständiger Gammafunktionen.
Die direkte Wurzelintegration benutzt d³y=2pi sqrt(T²-s) ds nach
vollständiger Winkelintegration. Wegen sqrt(T²-s)<=tau+sigma folgt für
den nahen Teil

    B_near <=6 beta I0(S) J_near(L;sigma,C).

Die Erweiterung des s-Integrals auf [0,infinity) majorisiert diesen Teil;
sie ändert nicht dessen Definition. Es werden keine archivierten Punkte
neu gezogen und keine unabhängigen Produkte von Historyintervallen angenommen.

## 7. Zwei gültige Grenzen für den fernen Teil

Setze M_m=Integral_(sqrt(L))^infinity s^m H_S(s)ds. Mit |U|<=M,
Tonelli und vollständiger Zeitintegration erhält man

    B_far,L1 <=6 beta M [(M_4-L² M_0)/2 +sigma(M_2-L M_0)].

Die Differenzen entstehen aus der exakten Integration eines positiven
Integranden über L<tau<s². Hier werden keine voneinander unabhängigen
oberen Fehlergrenzen subtrahiert.

Eine zweite, wesentlich kleinere Grenze benutzt die globale Quell-L2-Norm.
Für jede Zeitscheibe liefert räumliches Cauchy-Schwarz

    Integral_{s>sqrt(tau)} H_S(s)|U| d³y
      <=sqrt(Q_0) sqrt[2pi(tau+sigma)
                         Integral_(sqrt(tau))^infinity H_S(s)² ds].

Wähle h=S². Zeitliches Cauchy-Schwarz mit dem Gewicht (tau+h)^(-1)
und Integral_L^infinity (tau+h)^(-2)d tau=1/(L+h) liefert

    B_far,L2 <= beta rho sqrt(Q_0)
      sqrt[2pi/(L+h) Integral_(sqrt(L))^infinity
                            (P(s²)-P(L)) H_S(s)² ds],
    P(x)=x^4/4 +(2h+sigma)x³/3
             +(h²+2h sigma)x²/2 +h² sigma x.

P(s²)-P(L) ist nichtnegativ für s>=sqrt(L). Es ist das EXAKTE Integral
von (tau+h)²(tau+sigma) zwischen L und s². Diese neue Grenze benötigt
keinen punktweisen Dispersionssatz und bleibt nach der Archivkonditionierung
gültig, weil U deterministisch und H_S bereits eine bedingte Kernhülle ist.

Im äußeren Zweig ist H_S²=D² exp(-s²/64) Pbar(s²/128)². Die exakten
Koeffizienten des quadrierten Polynoms sind
(1,18,97,440/3,88,64/3,16/9). Die Momente mit Potenzen 0,2,4,6,8
schließen den ganzen unendlichen Rest ein. Das Minimum der beiden
gültigen Far-Grenzen wird verwendet. Für jeden Endpunkt wird anschließend
das beste S innerhalb des festen Gitters gewählt.

## 8. Detektor und vollständiger diskreter Transport

Der direkte Detektorbeitrag wird mit der unveränderten radialen Dichte
p(r)=-4r³+12r²-8r auf [1,2] normiert gemittelt. Wie in v0.22 zerlegen
16 radiale und acht zeitliche Intervalle jedes ganze Fenster. Ihre
rationalen Massen sind positiv und summieren sich exakt zu 1. Die neue
Tail-Obergrenze wird über jede Endpunktzelle uniform eingeschlossen.
Es gibt keinen ausgelassenen Kugelrand und keine Mittelpunktapproximation.

Für jeden der 223 bekannten aktiven Endpunkte wird eine eigene Tail-Grenze
F_tail,j mit seinem Radius, seiner Zeit und seiner geometrischen
Überlappungshülle berechnet. Der bekannte Transport ist

    B_known=sum_j |a_j| F_tail,j.

Die ursprünglichen validierten adjungierten Koeffizienten einschließlich
ihrer Integrationsradien werden übernommen. Alle rein inneren aktiven
Kanten liegen wegen kausaler Konvexität in B und hängen nicht von der
äußeren Konfiguration ab.

Für Pfade mit mindestens einem unbekannten aktiven Außenpunkt wird die
einheitliche Endpunkthülle D_uniform des jeweiligen Fensters verwendet:

    B_unknown=D_uniform (1+gamma)^n [exp(gamma lambda)-1], lambda=29/512,
    B_tail=B_direct_detector+B_known+B_unknown.

Der multivariate Mecke-Schritt entspricht v0.19/v0.20: alle weiteren
eingefügten aktiven Kettenpunkte liegen später als der erste Endpunkt p
und nicht im offenen ersten Historyintervall I(y,p). Dessen bedingte
Kernhülle bleibt gültig; die übrigen Kanten werden punktweise durch gamma
begrenzt. Es wird kein Erwartungswert abhängiger Faktoren auseinandergezogen.
Die zeitgeordneten Außenpunkte liefern lambda^k/k!, die Teilmengen der
bekannten Punkte höchstens (1+gamma)^n. Das exp-Term minus eins wählt
genau die Klasse mit mindestens einem unbekannten aktiven Knoten.

Als Kontrolle wird die gröbere Grenze
D_uniform(1+gamma)^n exp(gamma lambda) ebenfalls gespeichert. Sie
majorisiert dieselbe Tail-Pfadsumme. Der neue Endpunktweg ist in allen
acht Fällen enger. Die erste Historykante nutzt weiterhin eine bedingte
universelle Gewichtshülle; die tatsächlichen archivabhängigen n0/mu-Kerne
werden hier nicht vollständig geometrisch integriert.

## 9. Kombination, Existenz und Aussagegrenzen

Zunächst gelten alle Argumente auf endlichen History-Zeitschnitten.
Die positiven, summierbaren Majoranten und Tonelli erlauben den Übergang
zum unendlichen Bereich. Endlicher bedingter Erwartungswert der absoluten
Pfadsumme impliziert deren fast sichere absolute Konvergenz unter der
äußeren Poissonverteilung. Der kombinierte Rest ist in bedingtem L1
definiert. Für seine disjunkten Wurzeln gilt

    Delta=Delta_D5+Delta_Dinf,
    E(|Delta| | B)<=B_finite_v022+B_tail_v023.

Finite und unendliche Beiträge dürfen korreliert sein; die
Dreiecksungleichung erfordert keine Unabhängigkeit. Keine obere Grenze
wird von einer anderen subtrahiert, kein früherer Patch ein zweites Mal
addiert und der endliche Anteil nicht nochmals mit einem Pfadfaktor
multipliziert. Der Vergleich mit v0.19 betrifft dieselbe globale Größe.

Die vollständigen neuen oberen Grenzen liegen rund bei 3,17 bis 3,75
mal 10^10. Gegenüber v0.19 ist das etwa Faktor 6982 bis 9130 enger.
Der unendliche nahe Lichtkegelteil dominiert; der endliche Beitrag von
ungefähr 0,48 bis 0,55 ist numerisch klein, bleibt aber ausdrücklich
enthalten. Das Ziel 0,001 bleibt um mehr als 13 Größenordnungen verfehlt
im Sinne dieses oberen Beweisinstruments, nicht eines beobachteten Fehlers.

Die ergänzende L=2^j-Tabelle, j=3,...,40, zeigt abfallende gültige Grenzen
für den NOCH ENTFERNTEREN Rest tau>L. Sie ersetzt nicht den Bereich
5<tau<=L. Die vollständige Bilanz benutzt stets den Tail ab tau=5.
Große ausreichende L-Werte sind keine notwendigen Gebietsgrößen und keine
Empfehlung, entsprechend große Poissonwolken zu simulieren.

Schritt 2 ist damit mathematisch und rechnerisch geschlossen. Es folgt
keine Freigabe der Methode, kein Verwerfen der Operatorfamilie und keine
neue Bestätigungsstichprobe. Schritt 3 muss die Aussagekraft des noch
groben nahen Tail-Budgets berücksichtigen.

## 10. Prüfungen und Quellen

Die Rechnung wird bei 128 und 192 Bit durchgeführt. Die Ergebnisse werden
auf Endlichkeit, positive vollständige Teilbereiche, dieselben Eingaben,
korrekte Transportzerlegung und Präzisionsstabilität geprüft. Kleine
arithmetische Radien sagen nichts über die Schärfe der Fehlermajorante.

Unabhängige positive Quadraturen prüfen 12 radiale Fourierintegrale,
12 Kernmomente, 19 endliche/unendliche Potenzintegrale und sechs
Far-Polynomintegrale. Die Fourierkontrolle benutzt u=sin²(theta), also
K_J(a)=4pi Integral_0^(pi/2) sin^(4J-4)(theta)cos²(theta)
exp(-a sin²(theta))d theta. Halbzahl-Gammawerte werden separat durch
Fakultäten geprüft. 12 direkte Poissonsummen bis 2048 besitzen einen
Chernoff-Rest. Vier absichtlich falsche Hypothesen werden zurückgewiesen.

Für positive Gauß-Polynomintegrale in den Gegenquadraturen wird bis B>=256
integriert. Bei maximalem Polynomgrad d und Rate c gilt für B²>=d/c
die Restgrenze f(B)/(cB), weil die logarithmische Ableitung danach
höchstens -cB ist. Beim Far-Polynom wird P(s²) als positive obere Hülle
für P(s²)-P(L) im Quadraturrest verwendet. Es wird kein Rest weggelassen.

Der isolierte vollständige Replay verlangt Byteidentität aller fünf
numerischen Ergebnisdateien und unveränderte Ausgangsdateien. Die
Selbstprüfungen sind kein unabhängiges wissenschaftliches Review und
keine Beweisassistent-Verifikation.

Primärgrundlagen, jeweils nur für die benannte Identität:

- Last/Penrose, Lectures on the Poisson Process (2017), Theorem 4.4,
  multivariate Mecke-Identität:
  https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf
- DLMF 8.2.2, obere unvollständige Gammafunktion:
  https://dlmf.nist.gov/8.2#E2
- DLMF 13.4.1, positive Beta-/Kummer-Integralrepräsentation:
  https://dlmf.nist.gov/13.4#E1
- Die projektspezifischen Kontur-, Geometrie- und Transportbeweise sind
  eigene Herleitungen mit den unveränderten Vorgängern in `evidence/`.
  Quellenstand 29.10.2026; Laufzeit python-flint 0.8.0, Python 3.12.14.
