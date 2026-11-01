# CSPP v0.25: Ein zusätzlicher Schichtfreiheitsgrad reicht bei q0 nicht

29. Oktober 2026. Eigene deterministische Entwicklungsrechnung auf Basis von
Main `4c755221b76364c02beca5e7a40c0f8d50931375` nach PR #156.

## 1. Ergebnis und genaue Reichweite

Ein expliziter neuer skalarer Kandidat wurde definiert und geprüft. Die minimale
Erweiterung des bisherigen vierlagigen Schichtkerns um eine fünfte Lage erhält
die algebraischen Infrarotbedingungen und die Normierung auf den üblichen
d'Alembertoperator. Der konkret untersuchte Parameter theta=21 verbessert den
alten Gauß-Zeugen L=2 stark, verfehlt aber den zusätzlich untersuchten Zeugen
L=4. Der neue Zweiskalentest ist Entwicklungsdiagnostik, keine nachträglich
behauptete Vorregistrierung und kein ursprünglicher statistischer Test.

Für die gesamte normierte Familie mit Polynomgrad höchstens vier und der
unveränderten Skala q0=3/(16*pi) gilt für das volle vergangene Mittelwertproblem:

    inf_theta max_{L in {2,4}} |mu_L(theta) - (-2/L²)| / (2/L²)
       = 0.28473298136418543848... > 0.1.

Es handelt sich um einen Ausschluss für alle reellen theta in dieser genau
definierten Familie, nicht um einen endlichen Parameterscan. Er betrifft
weder andere q, höhergradige Kerne, beliebige Randkorrekturen noch alle skalaren
Operatoren. Er beweist keinen Fehleranteil der kompakten KG-Detektorantwort.
Der Kandidat wird für die Fortsetzung dieses erweiterten Kontrollprogramms
verworfen. METHOD und G1 bleiben HOLD.

Die kostenintensivere kompakte Detektorproduktion sowie eine vollständige
spektrale Suche werden nach diesem notwendigen Kontrollfehlschlag begründet
abgebrochen, bevor sie begonnen wurden. Sie sind ausdrücklich NOT_RUN.
Der erste Liefergegenstand des v0.24-Auftrags schliesst begründete Abbrüche ein.

## 2. Identität: neue Gewichte, unveränderte physikalische Aufgabe

Einheiten c=hbar=L0=1, Signatur (-,+,+,+), Box=-partial_t²+Delta.
Die Quelle ist unverändert: f=A exp[-1/(1-4r²)] exp(4iz) auf r<1/2,
sonst null; L2-Norm eins, g=0, t0=-1, m=1.
Die Beobachtung bleibt das gleichmässige komplexe Feldmittel über
B((0,0,3/2),1/2) und die Zeitfenster [3/4,1] bzw. [1,5/4], normiert durch A/e.
Der absolute kompakte Vergleichswert 0.001 wird nicht verändert.

rho=3/pi, epsilon=1/16, q=epsilon*rho=q0 und a=4 sqrt(q/6)=1/sqrt(2*pi).
Für die Anzahl n(y,x) im offenen kausalen Intervall sei

    w_theta(n) = sum_{k=0}^4 c_k(theta) binom(n,k) epsilon^k (1-epsilon)^(n-k),
    B_theta u(x) = a [d_theta u(x) + epsilon sum_{y prec x} w_theta(n(y,x)) u(y)],
    c(theta) = (1,-9,16,-8,0) + theta*(9/8,-141/8,111/2,-63,24),
    d_theta = -1 - 3 theta/8.

Nicht vorhandene Binomialterme sind null. Der hinzugefügte Grad ist eine
zusätzliche UNGEGLÄTTETE Schicht; nach Binomialglättung sind beliebig grosse
Intervallzahlen beteiligt. theta=0 reproduziert exakt den alten Operator.
Die Änderung nur der Gewichte bei unverändertem alten Diagonalwert wäre ein
anderer, falsch normierter Kandidat.

Für theta=21 gilt exakt

    c = (197/8, -3033/8, 2363/2, -1331, 504),   d = -71/8.

Die finite Propagationsdiagnose ist auf Omega5={|t|+r<5} definiert. Alle
Punkte t<=-1 erhalten die exakte KG-Kontinuumshistory. Aktive Unbekannte liegen
auf -1<t<5/4. Passive Detektorproben verändern keine Intervallzahlen.
Diese Eingabeabbildung ist ausdrücklich eine Diagnose mit bekannter History,
kein Ersatz für H1 oder PU-H1 und kein bereits qualifizierter Cauchy-Adapter.
Es werden keine Archivwolken verändert oder neue erzeugt.

Davon getrennt wird der volle kausale Vergangenheitsintegraloperator auf
Gauß-Testfeldern untersucht. Die Gaußintegrale sind absolut integrierbar.
Eine Existenz oder Stabilität des unendlichen inversen KG-Propagators wird
daraus nicht abgeleitet. Finite und unendliche Definition werden nicht vermischt.

## 3. Herleitung der vollständigen minimalen Familie

Sei P(z)=sum c_n z^n/n! und R(s)=sum c_n (s)_n/n!. Dann ist

    integral_0^infinity z^(s-1) exp(-z) P(z) dz = Gamma(s) R(s).

Die 4D-Infrarotbedingungen von Aslanbeigi/Saravani/Sorkin, Gl. (3.14), werden
in unserer Normierung zu

    R(1/2)=R(1)=R(3/2)=0,
    R'(3/2)=-2/3,
    d=-3 R'(1).

Der letzte Schritt benutzt psi(n+1)=H_n-gamma_E und R(1)=sum c_n=0.
Diese Bedingungen betreffen die infrarote Normierung des Mittelwertsymbols.
Sie beweisen weder Genauigkeit bei festem q noch Realisierungs- oder
Propagatorstabilität. Es wird kein allgemeiner Kontinuumssatz für beliebige
Felder oder gekrümmte Raumzeiten zusätzlich behauptet.

Beim alten Kern ist

    R0(s)=-(4/3)(s-1/2)(s-1)(s-3/2).

Jede Differenz zweier normierter Lösungen von Grad <=4 hat die drei genannten
Nullstellen; die Ableitung am dritten Punkt muss ebenfalls verschwinden.
Deshalb ist sie ein Vielfaches von

    Q_R(s)=(s-1/2)(s-1)(s-3/2)^2.

Die Darstellung dieses Polynoms in der Basis (s)_n/n! liefert exakt den
Richtungsvektor (9/8,-141/8,111/2,-63,24). Q_R'(1)=1/8 erklärt die neue
Diagonale. Die Rang-vier-Prüfung über rationale Arithmetik bestätigt, dass
kein weiterer unabhängiger Koeffizient in diesem Grad übersehen wurde.
Dies ist eine eigene Spezialisierung der publizierten IR-Bedingungen.

## 4. Eingeschlossene Mittelwerte statt Anpassung eines Messensembles

Kontrollfelder: phi_L=exp[-(t²+r²)/(2L²)], am Ursprung Box phi_L=-2/L².
L=2 ist der alte notwendige Zeuge; L=4 ist ein hier zusätzlich gewählter
breiterer Entwicklungszeuge. Die kompakte physikalische Quelle bleibt gleich.
theta=21 wurde nach einer explorativen Gleitkommarechnung nahe dem L=2-Fit
gewählt. Auch die zusätzliche Skalenprüfung wird nicht als unabhängig oder
präregistriert bezeichnet. Die nachfolgende Allparameteraussage ist trotzdem
eine deterministische mathematische Aussage mit explizitem Geltungsbereich.

Für N~Poisson(rho V) gilt

    E[binom(N,k) epsilon^k (1-epsilon)^(N-k)] = (qV)^k exp(-qV)/k!.

Campbell-Mecke liefert für das feste Testfeld

    mu_L(theta) = a[d_theta + q integral_{J-(0)} phi_L(y) exp(-qV) P_theta(qV) d4y].

Die Form ist affin in theta. Insbesondere ändert eine Dichteerhöhung bei
FESTEM q diesen Mittelwertkonflikt nicht. Sie ändert gegebenenfalls die
Fluktuationen, die hier nicht simuliert oder unabhängig addiert werden.

Mit s=-t-r, v=-t+r, d4y=(pi/2)(v-s)² ds dv, c0=sqrt(pi*q/24)
und y=c0*s*v folgt die bereits im Projekt verwendete Besselreduktion:

    mu_L = a[d + 12 integral_0^infinity y P(y²) exp(-y²)
                 * (K1(y/(2*c0*L²))-K0(y/(2*c0*L²))) dy].

Für z>0 ist 0<K1(z)-K0(z)<1/z. Positivität folgt aus der reellen
Integralrepräsentation; z K1(z)<=1 folgt aus (zK1)'=-zK0 und dem Grenzwert 1.
Für p_n=c_n/n! ergeben sich deshalb die vollständigen Fehlerränder

    E_low <= 8 sqrt(pi) q L² delta sum |p_n| delta^(2n),
    E_high <= 8 sqrt(pi) q L² sum |p_n| T_n(Y),
    T_0(Y)=sqrt(pi) erfc(Y)/2,
    T_n(Y)=Y^(2n-1) exp(-Y²)/2 + (2n-1) T_(n-1)(Y)/2.

Wir verwenden delta=2^-80 und Y=10, jeweils 128 und 192 Bit. Die endliche
Integration nutzt Acb mit abs_tol=rel_tol=1e-28. Für den Besselzweig werden
nur komplexe Bälle mit positivem Realteil akzeptiert. Die ausgelassenen
Enden werden nach aussen addiert; der Produktionsradius muss <1e-18 sein.
Die Entscheide verwenden Bälle; Mittelpunkte sind ausschliesslich Anzeigen.

Gerundete Anzeigen für theta=21:

| L | Sollwert | mu_L(21) | relativer Mittelwertfehler |
|---|---:|---:|---:|
| 2 | -0.5 | -0.49923737394920645 | 0.152525210159 % |
| 4 | -0.125 | -0.23081117428142904 | 84.648939425143 % |

Der erste Wert ist nur ein notwendiger Mittelwert-PASS, kein RMS-PASS.
RMS >= Betrag des Bias; die zusätzliche zweite Kontrolle scheitert deshalb
bereits vor einer Varianzanalyse. Aus den IR-Bedingungen folgt kein Ausweg
für die hier festgehaltene, grobe Skala.

## 5. Ausschluss für alle reellen Parameter ohne Suchgitter

Schreibe den relativen SIGNIERTEN Fehler als e_L(theta)=A_L-B_L theta.
Die eingeschlossenen Werte belegen A_2,A_4,B_2,B_4>0. Die Bedingungen
|e_L|<=0.1 erlauben die folgenden gerundeten Parameterintervalle:

    L=2: theta in [17.97385415207392, 24.11988836390632],
    L=4: theta in [ 6.33649496592046,  9.43499878923625].

Die angezeigten Dezimalenden sind keine neuen exakten Intervallgrenzen;
die Ball-Endpunkte stehen in CERTIFICATE_*.json. Dort wird ihre Trennung
mit positiv eingeschlossener Lücke 8.53885536283766... bewiesen.

Für jedes theta gilt die exakte Eliminationsidentität

    B4 e2(theta)-B2 e4(theta) = B4 A2-B2 A4.

Da B2,B4>0, liefert die Dreiecksungleichung

    max(|e2|,|e4|) >= |B4 A2-B2 A4|/(B2+B4).

Gleichheit tritt bei theta*=(A2+A4)/(B2+B4) auf, wo e2=-e4. Somit folgt
das oben angegebene scharfe Zweiskalen-Minimaxresultat; theta* ist ungefähr
12.29697803448351. Dieser Wert wird nicht als freigegebener Kandidat
ausgegeben: sein notwendiger maximaler Fehler ist noch 28.4732981364 %.
Keine Parameterwahl oder endliche Suche ist für den Ausschluss nötig.

## 6. Retardierung, finite Stabilität und Momentexistenz

Der neue Kern hängt nur von vergangenen Punkten und intrinsischen
Intervallzahlen ab. Er ist kausal retardiert und unter Umnummerierung
kovariant. Bei theta=21 gilt für jede Masse m>=0

    D=m²-a*d=m²+71*a/8 >0,
    u_i=sum_{j prec i} T_ij u_j - J_i/D,
    T_ij=(a*epsilon/D) w_21(n(j,i)).

Für den aktiven Block K auf einer endlichen Wolke ist K strikt dreieckig.
Damit det(I-K)=1 und (I-K)^(-1)=sum_{k=0}^{N_A-1} K^k. Dies beweist die
eindeutige Definition jedes solchen finiten History-Problems, einschliesslich
leerer aktiver oder History-Mengen. Es ist kein Stabilitätsbeweis für
unendliche Vergangenheit oder wachsende Dichte.

Aus w(n)=E[c_X], X~Binomial(n,epsilon), folgt |w(n)|<=1331.
Setze beta=a*epsilon/D und gamma=1331 beta. Für m=1 ist gamma ungefähr
7.308927861. Für beliebige History-Störungen mit ||delta h||_infinity<=eta
und J=0 ergibt die positive Pfadsumme für einen passiven Detektorpunkt

    |delta u_p| <= gamma N_H (1+gamma)^(N_A) eta.

Sie gilt auch für positive, normierte Detektormittel, wenn N_A alle für das
gesamte Fenster benötigten aktiven Knoten umfasst. Für aktive additive
Gleichungsfehler f gilt ||(I-K)^(-1) f||_infinity <= (1+gamma)^N_A ||f||_infinity.
Die fallbezogene engere Schranke entsteht durch v_H=1,
v_i=sum |T_ij|v_j und G_p=sum |T_pj|v_j.

Auf einem unabhängig definierten, zeitartig kollinearen Kontrollgraphen mit
drei Historyknoten, fünf aktiven Knoten und einer passiven Probe liefert
direkte dichte Ballinversion dieselben Historybasisantworten wie die
Vorwärtsrekursion. Die tatsächliche induzierte Historynorm beträgt etwa
0.6186537891, die positive Pfadmajorante etwa 0.8665237920. Das ist nur
ein Kontrollgraph, kein Archiv- oder Populationsbefund.

Für jedes endliche deterministische Gebiet und bounded |h|<=M sind alle
ganzzahligen absoluten Momente der finiten Ausgabe endlich: Die disjunkten
Poissonzählungen N_H und N_A sind unabhängig, daher

    E|A|^p <= (gamma M)^p E[N_H^p]
                  exp(lambda_A*((1+gamma)^p-1)),  p=1,2,... .

Die normierte Ausgabe benötigt M in derselben Feldnormierung. Diese Aussage
ist bedingt auf das ideale Poissongesetz und eine uniforme Historyhülle;
sie ist keine Auswertung der gemeinsamen Originalmomente. Ohne solche Hülle
wird die Folgerung nicht verwendet. Die Konstante wächst sehr stark.
Eine grosse Majorante beweist keine Instabilität; endliche Momente beweisen
keine brauchbare Fehlergrenze. Unendliche KG-History, Samplerfehler und
dichteuniforme oder spektrale Stabilität bleiben unqualifiziert.

## 7. Vollständige Fehleridentität und begründeter Abbruch

Für den genau definierten finiten Kandidaten mit exakter KG-History sei U
die unveränderte Kontinuumslösung. Auf aktiven Knoten und passiven Proben
seien r_i=U_i-sum_j T_ij U_j. Dann folgt exakt

    E_O = A_discrete - A_continuum
        = -mean_detector(r_p) - Q_A (I-K)^(-1) r_A.

Dies gilt für den linear normierten Detektor; Q_A ist der vollständig
integrierte Proben-zu-Aktiv-Transfer. Die zweite Komponente darf nicht
weggelassen werden. Bei approximierter History, Quadratur und numerischem
Solve kommen deren signierte Differenzen hinzu. Es ist keine Summe
unabhängiger Varianzen. Ein Aussengebietsfehler käme bei Vergleich mit einer
definierten unendlichen Lösung zusätzlich hinzu.

Die neue kompakte KG-Ausgabe, ihre gesamte Fehlerbilanz und das unendliche
Propagatorspektrum werden nicht numerisch ausgewertet: Bereits der
notwendige erweiterte Mittelwerttest hat den Kandidaten ausgeschieden.
Ein L=2-PASS kann diesen Abbruch nicht aufheben. Insbesondere werden die
alten kompakten Referenzwerte oder H1/PU-H1-Zertifikate nicht zu Resultaten
des neuen Operators umetikettiert. Eine positive Genauigkeitsfreigabe wird
nicht behauptet; die noch offenen Arbeiten sind maschinenlesbar NOT_RUN.

## 8. Validierung und nächste Konsequenz

Neun Quellen wurden gegen Git-Blobs und SHA256 geprüft. 21 rationale
Identitäten und sieben finite Kontrollprüfungen bestehen je Präzision.
40 Ballziele überlappen bei 128/192 Bit. Zwei alte Mittelwerte werden
reproduziert: L=2 direkt; L=4 über die Skalierungsidentität
mu(q,4)=mu(16q,2)/4 mit der archivierten epsilon=1-Kontrolle.

Sechs zusätzliche Gleitkomma-Doppelintegrale in Nullkoordinaten bestätigen
die Besselreduktion; grösste Abweichung etwa 3.51e-13. Ihr Rest jenseits
H=64 wird analytisch begrenzt, ihre endliche SciPy-Quadratur bleibt jedoch
diagnostisch und ist kein zweites Zertifikat. 128 rationale Gewichte werden
zusätzlich auf die Binomialhülle geprüft. Falsche Schichtkoeffizienten,
falsche lokale Diagonale und ausgelassene aktive Pfade werden erkannt.

Der isolierte Replay reproduziert beide Produktionsdateien bytegenau und
lässt sämtliche Eingaben unverändert. Prüfungen und Intervalle ersetzen
kein externes Peer Review und keine Beweisassistent-Verifikation.

Die nächste sinnvolle Entwicklung muss diese eindimensionale Familie bei
festem q verlassen. Vor einem weiteren Fit sind mehrskalige Kontrollen und
die spektralen Stabilitätskriterien festzulegen. Eine weitere Schicht oder
eine neue q-Skala wäre ein eigener Kandidat mit eigener Methodenprüfung;
zwei angepasste Kontrollwerte wären weiterhin kein allgemeiner Nachweis.
Frische Ensembles und ein statistisches Design bleiben gesperrt.

## Quellen und ihre begrenzte Verwendung

1. Projektstand nach PR #156, genaue Git-URLs und Hashes in evidence/SOURCES.json.
   Der v0.24-Auftrag erlaubt ausdrücklich notwendige Kontrollen mit begründeten
   Abbrüchen. Projektwerte, Quelle und Detektor stammen aus diesen Dateien.
2. Aslanbeigi, Saravani, Sorkin (2014), Generalized Causal Set d'Alembertians,
   arXiv:1403.1622, https://arxiv.org/pdf/1403.1622 , Gl. (3.14).
   Verwendet werden die IR-Koeffizientenbedingungen; Familie, Kandidat und
   Zweiskalenausschluss sind eigene Rechnungen. Ein fremder Stabilitätsbefund
   wird nicht auf den neuen Kandidaten übertragen.
3. Belenchia, Benincasa, Dowker (2016), https://arxiv.org/html/1510.04656v2 .
   Kontext zur Skalentrennung: ein Mittelwertgrenzwert qualifiziert eine
   feste grobe Nichtlokalitätsskala nicht automatisch.
4. NIST DLMF, https://dlmf.nist.gov/10.32 , reelle K-Bessel-Integralidentitäten.
   Die Anwendung auf den konkreten Gaußkern ist oben hergeleitet.
5. python-flint, https://python-flint.readthedocs.io/en/latest/acb.html .
   Analytischer Callback-Vertrag; ausgeführt ist Version 0.8.0, deren lokale
   Laufzeitdokumentation geprüft wurde. Neuere Online-Versionen ändern die
   Laufzeitbindung nicht.
