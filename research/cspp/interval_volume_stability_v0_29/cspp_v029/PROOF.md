# CSPP v0.29: Intervallvolumen in der positiven Pfadmajorante

1. November 2026. Eigene Ableitung auf Main nach PR #161,
Commit `9a12332fa898408a71fb09128abdc467f84bf0b7`.

## 1. Auftrag und Ergebnisart

Der Anschluss an v0.28 ersetzt die konstante Eintragshülle durch das
Poisson-Mittel des BETRAGS des geglätteten Gewichts. Dieses hängt vom
tatsächlichen Volumen des offenen Kausalintervalls ab. Eine
Binomial-Komposition liefert wieder eine Hülle für alle höheren Dichten.
Die multivariate Mecke-Formel und disjunkte aufeinanderfolgende Intervalle
machen daraus eine positive Volterra-Abschätzung für das gesamte
endliche Zeitfenster, einschliesslich genau einer vorgeschriebenen
Historyeingabe pro Pfad.

Das ist ein Satz über eine klar eingeschränkte Klasse von
Minkowski-Poisson-Kausalsets. Es ist weiterhin KEIN Nachweis signierter
Aufhebung zwischen verschiedenen Pfaden, keine Kovarianzvorhersage und
keine Qualifizierung der tatsächlichen KG-Residuen. METHOD und G1 bleiben
HOLD. Der Genauigkeitsausschluss von theta=21 aus v0.25 wird nicht verändert.
Die numerischen Ergebnisintervalle und sämtliche Parameter stehen in
`results/RESULTS.json`. Ein kleinerer hinreichender Fehlerfaktor ist keine
gemessene Fehlerreduktion und kein Stabilitätsnachweis für jede Realisierung.

## 2. Unveränderte Dynamik, präzisere Gebietsklasse

Fixiere q>0, rho_bar>=q, e_bar=q/rho_bar, endliche reelle Koeffizienten
c_0,...,c_d, a=4 sqrt(q/6) und D=m^2-a*d_local !=0. Setze beta=aq/|D|.
Für rho>=rho_bar und e=q/rho bleibt

    w_e(n) = sum_{k<=min(d,n)} c_k binom(n,k) e^k (1-e)^(n-k),
    K_yz = aq/(D*rho) w_e(N(I(z,y))).

I(z,y) ist das vollständige offene Minkowski-Kausalintervall.
Der zugrunde liegende Prozess ist ein homogener Poisson-Prozess mit
Intensität rho d4z auf dem Zeitband -H<t<T, gegebenenfalls eingeschränkt
auf ein deterministisches Gebiet Omega. Die aktive Zeit beginnt bei 0.
Punkte -H<t<=0 tragen vorgeschriebene Historywerte; sie propagieren nicht
untereinander. Passive Proben sind fest, werden nicht in die Punktwolke
eingefügt und verändern keine Intervallzahlen.

NEUE VORAUSSETZUNG FÜR DIE VOLUMENHÜLLE: Für jedes benutzte kausale Paar
von Punkten in Omega sowie jede Kopplung zu einer passiven Probe enthält
das Zählgebiet das vollständige offene Intervall. Kausal konvexe Gebiete
mit den Proben in ihrem Abschluss genügen, insbesondere Kausaldiamanten.
Der Projektbereich Omega5={|t|+r<5} ist ein solcher Diamant. Die
Zeitverschiebung von t=-1 auf t'=0 lässt T=9/4 und H=4 unverändert.

Für ein beliebig beschnittenes Gebiet hätte N die Poisson-Erwartung
rho*Vol(I intersect Omega). Diese darf nicht durch rho*Vol(I) ersetzt
werden: Das mittlere Betragsgewicht ist nicht als monoton in V bewiesen
und ist im Allgemeinen nicht monoton. Für solche Gebiete bleibt die
konstante v0.28-Hülle zuständig. Die zusätzliche Voraussetzung wird nicht
als stillschweigende Eigenschaft aller früheren Gebiete verwendet.

Die Normen bleiben die ungewichteten Maximumsnormen der
diagonalnormalisierten additiven aktiven/passiven Fehler eta_f und der
vorgeschriebenen Historyfehler eta_h. Für einen ursprünglichen Quellfehler
delta J ist vor Anwendung eta_f >= ||delta J/D|| zu verwenden. Die
Feld-/Detektornormierung wird nicht verändert.

## 3. Satz A: Volumenabhängige Hülle für ein ganzes Dichteintervall

Sei S=sup_n |w_e_bar(n)|<infinity, b_n=|w_e_bar(n)| und

    Psi(mu) = exp(-mu) sum_{n>=0} b_n mu^n/n!,
    A_bar(V) = Psi(rho_bar*V).

Dann gilt für jedes V>=0 und jede rho>=rho_bar

    E |w_(q/rho)(Pois(rho V))| <= A_bar(V) <= S.             (1)

Bei rho=rho_bar ist die erste Ungleichung eine Gleichheit. Damit ist
A_bar die kleinste punktweise obere Hülle der Erwartungsbeträge über
diesen Dichtebereich. Dies betrifft keine optimale Schranke der
tatsächlichen Propagatornorm.

BEWEIS. Setze p=rho_bar/rho=e/e_bar. Bedingt auf N=n gilt die in v0.28
bewiesene Identität

    w_e(n) = E[w_e_bar(M) | N=n],  M|N=n ~ Bin(n,p).

Jensen für den Betrag gibt |w_e(n)|<=E[b_M|N=n]. Für
N~Pois(rho V) ergibt Poisson-Ausdünnung M~Pois(rho_bar V). Das beweist
(1); b_n<=S liefert die zweite Grenze. Bei V=0 ist Psi(0)=|c_0|.
Es werden keine Punkte der tatsächlich simulierten Wolke gelöscht. QED.

Ferner ist Psi stetig differenzierbar und

    Psi'(mu) = E[b_(N+1)-b_N],  N~Pois(mu),
    |Psi'(mu)| <= S.                                        (2)

Die termweise Differentiation ist auf kompakten mu-Intervallen durch
b_n<=S gerechtfertigt; am Ursprung gilt die rechtsseitige Formel.
Die Lipschitzgrenze wird für zertifizierte Intervallzellen benutzt.
Psi wird dabei nicht durch |E w| ersetzt. Bereits die positiven
Wahrscheinlichkeiten für zwei entgegengesetzt signierte Gewichte machen
Jensens Ungleichung im Allgemeinen strikt.

## 4. Satz B: Erwartete positive Pfadsumme ohne Pfadunabhängigkeit

Definiere Z_A als Summe der Produkte |K| über alle nichtleeren kausalen
Pfade von einer aktiven Fehlerquelle zu einer festen passiven Probe x.
Definiere Z_H analog, jedoch mit genau einem Startpunkt in der History
und danach ausschliesslich aktiven Punkten. Verwendet werden Ketten
der vollen Kausalrelation; es ist keine Einschränkung auf Hasse-Kanten.
Für jede endliche Realisierung folgt aus der endlichen Neumannsumme

    |delta u_x| <= eta_f*(1+Z_A) + eta_h*Z_H.                 (3)

Für ein festes geordnetes Tupel y_k prec ... prec y_1 prec x sind die
offenen Intervalle zwischen aufeinanderfolgenden Tupelpunkten paarweise
disjunkt. Keiner der übrigen Tupelpunkte liegt in einem solchen offenen
Intervall: Das würde seiner kausalen Reihenfolge widersprechen. Dasselbe
gilt bei einem History-Startpunkt. Unter der Mecke-Einfügung dieser
Tupelpunkte erhalten die benutzten Zählungen deshalb KEINEN zusätzlichen
deterministischen Punkt. Die Poisson-Beschränkungen auf die disjunkten
Intervalle sind unabhängig.

Die multivariate Mecke-Formel liefert daher für einen Pfad mit k
Poissonpunkten den erwarteten Beitrag

    rho^k integral product_edges [(beta/rho)
                   E |w_e(Pois(rho*V_edge))|] d4y_1...d4y_k.

Die rho-Potenzen kürzen sich; (1) begrenzt den Integranden durch
beta^k product A_bar(V_edge). Es gibt keinen weiteren Faktor 1/k!:
Die kausale Reihenfolge bestimmt die Tupelanordnung bereits eindeutig.
Bei rho=rho_bar und vollem Band ist die Formel für die positive
Pfadsumme exakt. Für höhere Dichten oder Teilgebiete ist sie eine obere
Schranke. Tonelli erlaubt die Summe über sämtliche Pfadlängen.

Wesentlich ist die Konfigurationsabhängigkeit der Gewichte: Die blosse
Formel für faktorielle Momentmasse reicht für diesen Schritt nicht aus;
die Einfügungen in der Mecke-Formel wurden ausdrücklich behandelt.
Zwischen ZWEI verschiedenen Pfaden wurde nirgendwo Unabhängigkeit
vorausgesetzt. Linearität des Erwartungswertes benötigt sie nicht.

## 5. Räumliche Integration und Volterra-Form

Im 1+3-Minkowski-Raum hat ein Intervall mit Zeitabstand s und räumlichem
Abstand r<=s das Volumen V=pi*(s^2-r^2)^2/24. Im Ruhesystem folgt dies
aus zwei Kegeln: 2 integral_0^(tau/2) (4pi/3)t^3 dt=pi*tau^4/24;
Lorentz-Invarianz des Volumens liefert tau^2=s^2-r^2.

Definiere den nichtnegativen Zeitkern

    h(s) = 4*pi*beta integral_0^s r^2 A_bar(pi*(s^2-r^2)^2/24) dr,
    g(t) = integral_t^(t+H) h(s) ds.

Seien F und J die positiven Volterra-Lösungen

    F(t) = 1 + integral_0^t h(s) F(t-s) ds,
    J(t) = g(t) + integral_0^t h(s) J(t-s) ds.                (4)

Dann gilt für die Probe zur Zeit t<=T

    E Z_A <= F(t)-1,   E Z_H <= J(t).                         (5)

BEWEIS. Räumliche Inkremente einer geordneten Kette sind unabhängig
integrierte Vektoren; die lineare Transformation von Punktkoordinaten
zu Inkrementen hat Determinante eins. Die Intervallvolumina hängen
jeweils nur vom entsprechenden Inkrement ab. Jeder zusätzliche aktive
Schritt faltet deshalb mit h. Der erste History-Schritt integriert über
Startzeiten -H<t_h<=0 und ergibt g(t). Damit sind F=sum h^{*k}*1 und
J=sum h^{*k}*g, jeweils k>=0. Es wird kein weiterer History-Schritt
eingefügt. Für ein zulässiges Teilgebiet werden lediglich mögliche
Tupel aus der vollen Bandintegration entfernt. QED.

Aus A_bar<=S folgt h(s)<=(4*pi*beta*S/3)s^3. Somit dominieren die
konvergenten v0.28-Reihen alle diese Reihen auf kompakten Zeitfenstern;
Existenz, Endlichkeit und Eindeutigkeit der stetigen Volterra-Lösungen
folgen auch durch Iteration dieser Majorante.

Die für die Numerik entscheidende Monotonie gilt trotz möglicher
Oszillation von Psi. Mit v=s^2-r^2 wird

    h(s) = 2*pi*beta integral_0^(s^2)
                  sqrt(s^2-v) A_bar(pi*v^2/24) dv.

Integrand und Integrationsbereich wachsen mit s. Daher ist h
nichtabnehmend; ebenso g, F und J durch die positiven Faltungsreihen.

## 6. Gemeinsames Fehlerbudget und Quantoren

Für feste nichtnegative eta_f, eta_h und 0<delta<1 liefert Markov auf
eta_f Z_A+eta_h Z_H aus (3)-(5), mit Wahrscheinlichkeit mindestens 1-delta,

    |delta u_x| <= eta_f + [eta_f*(F(T)-1)+eta_h*J(T)]/delta.  (6)

Diese Aussage gilt gleichzeitig für alle Eingabefehler innerhalb der
festgelegten Hüllen, auch wenn die Vorzeichen vom Kausalset abhängen.
Sie gilt für jedes fest gewählte rho>=rho_bar mit denselben Konstanten,
jedoch nicht als ein gemeinsames Ereignis für unendlich viele Dichten.

Ein festes deterministisches Detektormass mit Totalvariation Q wird
durch Integration gegen |mu| und Tonelli behandelt. Die rechte Seite
von (6) erhält den Faktor Q. Es wird weder Unabhängigkeit der Proben
noch eine zufällige Normierung durch deren Anzahl angenommen. Für das
positive normierte Detektormittel ist Q=1. Die Schranke wächst nicht
mit einer räumlichen Gebietserweiterung innerhalb der zugelassenen
Klasse. Sie kontrolliert kein globales Maximum über immer mehr Proben
und erklärt einen Gebietsfehler gegenüber anderer Dynamik nicht für null.

Für gleiche Eingabehüllen eta und Q=1 gelten

    B_active = 1 + (F(T)-1)/delta       bei exakter History,
    B_joint  = 1 + (F(T)-1+J(T))/delta bei beiden Fehlerarten.

Ein Ausgabebudget b ist hinreichend durch eta<=b/B abgesichert.
UNTERE Grenzen eines eingeschlossenen B sind lediglich untere Grenzen
dieser mathematischen MAJORANTE, keine unteren Grenzen der wirklichen
Fehler oder Propagatornormen. Zur garantierten Anwendung wird die obere
Grenze von B beziehungsweise die untere Grenze des erlaubten eta benutzt.

## 7. Vollständig kontrollierte numerische Auswertung

Die Projektparameter bleiben q=3/(16*pi), rho_bar=3/pi, T=9/4,
H=4, m=1, delta=1/100, Q=1 und b=1/1000. Die beiden Koeffizientensätze
und Diagonalen stehen unverändert im Programm und in v0.28.
Mit a=1/sqrt(2*pi) vereinfacht sich

    mu = rho_bar V = (s^2-r^2)^2/8,
    4*pi*beta/3 = a/[4*(1-a*d_local)].

Das Programm verwendet ausschliesslich Integer und rationale Zahlen.
Ein Intervall wird als zwei Integer geteilt durch 10^P dargestellt.
Jede Multiplikation, Division und Skalierung rundet links nach unten,
rechts nach oben. Quadratwurzeln werden über ganzzahlige Quadratwurzeln
eingeschlossen. Die pi-/a-Einschliessung wird aus der ausdrücklich
ausgewiesenen, unveränderten v0.27-Routine übernommen.

1. Poisson-Reihe: b_0,...,b_512 werden exakt rational ausgewertet. Die
   positive Reihe ohne exp(-mu) wird bis n=512 summiert. Für den Rest
   gilt mit t_n=mu^n/n! und mu<514

       sum_{n>=513} b_n t_n <= S*t_513/[1-mu/514].

   Im benötigten Bereich mu<=625^2/2048=190.73486328125 ist der Nenner
   positiv. exp(-mu) wird durch eine positive Taylorreihe für exp(mu/2^m)
   bei mu/2^m<=1, geometrische Restkontrolle, Kehrwert und wiederholtes
   Quadrieren eingeschlossen. Ein Abschneiden der unendlichen Reihe
   ohne Rest wird nicht verwendet.

2. Kontinuierliche mu-Zellen: Für jede Zelle der Breite dmu wird Psi
   am rationalen Mittelpunkt eingeschlossen. Gleichung (2) erweitert
   das Intervall um S*dmu/2 auf die gesamte Zelle; anschliessend wird
   mit [0,S] geschnitten. Das numerische Gitter ist damit kein Ersatz
   für die Kontrolle zwischen Gitterpunkten.

3. Räumliche Schalen: Die Zelle [mu_j,mu_(j+1)] hat bei festem s den
   radialen Faktor

       [(s^2-sqrt(8mu_j))_+^(3/2)
        -(s^2-sqrt(8mu_(j+1)))_+^(3/2)].

   Multiplikation mit a/[4(1-a*d_local)] und den konstanten Zellhüllen
   integriert die radiale Massverteilung genau bis auf nach aussen
   eingeschlossene Quadratwurzeln. Der letzte Term wird bei r=0
   abgeschnitten. Es handelt sich nicht um unzertifizierte Quadratur.

4. Zeitrekursion: Setze d=dt, h_j^-/h_j^+ als Grenzen von h(jd).
   Die Monotonie liefert für jede der Lösungen Y=F,J mit Forcing f=1,g

       L_n = f_n^- + d sum_(j=1)^n h_(j-1)^- L_(n-j),
       U_n = [f_n^+ + d sum_(j=2)^n h_j^+ U_(n-j+1)]
             / [1-d*h_1^+].

   Der Nenner wird positiv geprüft; der erste obere Summand mit dem
   unbekannten U_n wurde auf die linke Seite gebracht. Für g werden
   linke/rechte Rechtecksummen von h über [t,t+H] verwendet. Y(0)=f(0).
   Induktion beweist L_n<=Y(nd)<=U_n, unabhängig von einer vermuteten
   numerischen Konvergenzordnung.

Die Läufe (P,dt,dmu)=(120,1/32,1/16), (120,1/64,1/32) und
(160,1/64,1/32) liefern jeweils gültige Einschliessungen. Ihr Schnitt
ist wieder gültig; Überlappung wird geprüft. Die ausgegebenen Grenzen
werden nochmals nach aussen auf 12 Dezimalstellen gerundet. Die Breite
stammt vorwiegend aus der Raum-/Zeitdiskretisierung, nicht aus dem
Integer-Rundungsfehler. Es wird keine Genauigkeit von 120 Dezimalstellen
für die tatsächliche Lösung behauptet.

Konservative nach oben gerundete Anzeigen des neuen zertifizierten
Budgets (die vollständigen Intervalle in RESULTS.json sind bindend):

| Fall | B_active v0.28 | B_active v0.29, obere Grenze | B_joint v0.28 | B_joint v0.29, obere Grenze |
|---|---:|---:|---:|---:|
| theta=0 | 54.325096... | 41.055 | 3601.924202... | 1955.877 |
| theta=21 | 584.886646... | 321.952 | 82030.233862... | 34819.303 |

Für theta=21 liegt die neue positive gemeinsame Majorante im
zertifizierten Intervall [30931.978601098938,34819.302675775900].
Die alte v0.28-Majorante ist mindestens um Faktor 2.355883879296 grösser
als die neue. Die gesamte Intervallbreite wird mitgeführt; ein einzelner
Gleitkomma-Schätzwert wird nicht als zertifizierter Wert ausgegeben.
Für das Ausgabebudget 0.001 genügen konservativ eta_f<=3.10e-6 bei
exakter History oder eta_f=eta_h<=2.87e-8 bei beiden Fehlerarten.
Diese Voraussetzungen sind für die tatsächlichen Projektresiduen
weiterhin nicht nachgewiesen. Die Zahlenvergleiche beziehen sich auf
die gemeinsame, intervallvollständige Gebietsklasse.

## 8. Kontrollen, Ausschlüsse und nächster Auftrag

Die Reproduktion prüft sechs eingefrorene Projektquellen gegen Git-Blob
und SHA256. Auf allen 407 natürlich nummerierten Ordnungen bis fünf
Punkte wird die Disjunktheit benachbarter Kettenintervalle und das Fehlen
weiterer eingefügter Kettenpunkte darin kontrolliert. Endliche rationale
Binomialfälle prüfen die bedingte Jensen-Hülle. Zehn Poissonwerte werden
zusätzlich mit unabhängiger exakter Fraction-Arithmetik eingeschlossen.
Die Zeitrekursion muss die analytischen v0.28-Ergebnisse bei konstantem
Kernel enthalten; die räumliche Schalenintegration muss für eine
konstante Hülle das analytische Kegelvolumen reproduzieren. Diese
endlichen Prüfungen ergänzen die Beweise; sie
sind keine Beweisassistent-Verifikation oder externe Reproduktion.

Die gemeinsame Zählung zweier überlappender Intervalle zeigt die Grenze
des Arguments präzise. Für Volumina V1,V2 und Überlappung W lautet die
gemeinsame erzeugende Funktion

    E[z1^N1 z2^N2] = exp(rho*[V1(z1-1)+V2(z2-1)
                                      +W(z1-1)(z2-1)]).

Sie folgt durch Zerlegung in drei disjunkte Mengen. Bei W>0 kann der
letzte Term nicht weggelassen werden. Für zwei eingefügte Pfade kommen
ausserdem deterministische Einfügungen fremder Pfadpunkte in die
Intervalle hinzu. Die Einzelkettenrechnung beweist deshalb keine
Varianz, keine Kovarianz und keine signierte Aufhebung zwischen Pfaden.
Entsprechende falsche Varianten werden als Negativkontrollen erkannt.

Auch die positive Majorante selbst kann bei einem nichttrivialen
Kernel keine zeituniforme Schranke liefern: h(s)>0 für s>0 und h ist
nichtabnehmend. Für festes s0>0 wächst bereits
F(T)>=1+integral_0^T h(s)ds>=1+(T-s0)h(s0) unbegrenzt. Ebenso wächst
die unendliche History. Das ist ein Ausschluss für DIESES positive
Beweisverfahren, kein Instabilitätsbeweis für die signierte Dynamik.

Der nächste begrenzte Auftrag ist die Mecke-/Poisson-Formel für zwei
Pfade samt Überlappungsvolumina, gemeinsamen Knoten und Einfügungszahlen.
Erst danach ist eine kontrollierte zweite Momenten- oder signierte
Pfadabschätzung sinnvoll. Der getrennte Grad-5-Genauigkeitsauftrag bleibt
offen. Keine neuen Zufallswolken, keine geänderten q-/Fehlerbudgets und
keine Förderung von METHOD oder G1 werden aus v0.29 abgeleitet.

## Quellen und Zuschreibung

- Projektbasis am oben fixierten Commit: sechs Dateien mit exakten
  Pfaden und Hashes in `evidence/SOURCES.json`. Neue Herleitungen und
  Rechnungen sind in diesem Paket als eigene Arbeit dokumentiert.
- Last / Penrose, *Lectures on the Poisson Process*, Version 21.08.2017,
  Theorem 4.4 (multivariate Mecke-Formel), Theorem 5.2 (Beschränkung auf
  disjunkte Mengen), Corollary 5.9 (Ausdünnung), gedruckte Seiten 30,
  39 und 44. https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf
- Aslanbeigi / Saravani / Sorkin, *Generalized Causal Set d'Alembertians*,
  JHEP 1406 (2014) 024, https://arxiv.org/abs/1403.1622. Kontext:
  Langwellige Normierung und dynamische Stabilität sind getrennte
  Fragen. Deren Modenbefunde werden nicht als Beweis für (6) verwendet.

Keine wissenschaftshistorische Prioritätsbehauptung, kein externes Peer
Review, keine Beweisassistent-Verifikation. Eine Veröffentlichung auf
GitHub erfolgt nicht innerhalb dieses Entwicklungsschritts.
