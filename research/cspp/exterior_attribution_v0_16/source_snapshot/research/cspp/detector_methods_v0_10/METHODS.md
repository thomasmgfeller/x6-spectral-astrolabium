# Analytisches Zeitintegral und kontrollierte lokale Anfangsdaten: v0.10

Dies ist Methodenentwicklung auf denselben acht bekannten Archivwolken wie
v0.9. Quellen, Wellenzahlen, Masse, Dichte, Gebiet, räumlicher Detektor und
beide Zeitfenster bleiben unverändert. Der zusätzliche H3-Vergleich ändert
den diskreten Adapter, nicht die physikalischen Cauchy-Daten. Keine Wolke
wird neu gezogen oder wegen ihres Ergebnisses ersetzt.

## 1. Zeitintegral ohne Zeitzellen

Für einen festen räumlichen Punkt x tritt der ursprüngliche Wolkenpunkt y
zur Zeit a_y(x)=t_y+|x-y| in die Query-Vergangenheit ein. Für jeden
ursprünglichen kausalen Nachfolger z von y gilt a_z(x)>a_y(x), nach der
Dreiecksungleichung und der strikten ursprünglichen Zeitordnung. Sortiere
die Eintrittszeiten dieser Nachfolger zu a_(1),...,a_(s).

Mit w_n=beta*w_e(n) und R(a)=min(Delta_t,max(0,t_b-a)) ist exakt

    integral_I K_py dt = w_0 R(a_y)
                        + sum_(k=1..s) (w_k-w_(k-1)) R(a_(k)).

Die Gewichte dürfen ihr Vorzeichen wechseln. Gleichzeitige Eintritte
geben denselben R-Wert; ihre Differenzen teleskopieren. Nachfolger mit
t>=t_b tragen exakt null bei. Die bisherige Abschneidung der aktiven
Wolke bei t<5/4 bleibt deshalb korrekt. Virtuelle Queries werden weiterhin
nicht in die Wolke eingefügt.

Auf einer räumlichen Box werden alle Eintrittszeiten nach unten und oben
eingeschlossen. Das k-te Element der sortierten unteren bzw. oberen
Endpunkte begrenzt das k-te tatsächliche Ordnungselement. Das bleibt auch
bei wechselnden oder gebundenen Reihenfolgen gültig: Ordnungsstatistiken
sind koordinatenweise monoton. Es wird keine gemeinsame feste Reihenfolge
über eine ganze räumliche Zelle angenommen.

## 2. Der gesamte Detektorball mit exaktem Volumengewicht

Die Parametrisierung

    r=(1/2)*u^(1/3), cos(theta)=v, phi=2*pi*w,
    (u,v,w) in [0,1] x [-1,1] x [0,1]

hat konstantes Volumengewicht. Jede der n^3 gleich großen Parameterzellen
besitzt exakt 1/n^3 des normierten Kugelvolumens. Die Pole und der Ursprung
sind Maß-null-Mengen. Ihre fehlende Koordinatenglattheit wird nicht für
eine Quadraturordnung verwendet. Es gibt keine ausgelassene Kugelrandregion.

Trigonometrie, Wurzel und Koordinatenbereiche jeder Parameterzelle werden
bei 256 Bit eingeschlossen. Daraus entstehen nach außen gerundete dyadische
räumliche Boxen. Minimale und maximale Abstände zu jeder Box liefern
Eintrittsintervalle mit 80 dyadischen Nachkommabits. Gewichte und signierte
Gewichtsdifferenzen erhalten 100 Bits. Alle Endpunktprodukte und Summen
im Zeitintegral sind danach exakte Ganzzahlarithmetik. Die abschließenden
Divisionen und Feldlösungen bleiben Arb-Einschließungen.

Die festen Gitter n=4,8,16 enthalten 64,512,4096 räumliche Zellen. Pro
Wolke werden insgesamt 4672 Zellen ausgewertet, jeweils für beide Fenster.
Vorherige gültige Koeffizienten- und Feldintervalle werden geschnitten.
Es gibt keine Richardson-Extrapolation, keinen empirischen Fehlerfaktor
und keine angenommene Konvergenzordnung. Die Rundung dyadischer Endpunkte
ist Teil der Einschließung. Alte v0.9-Intervalle dienen einer unabhängigen
Überlappungsprüfung und werden nicht zum Verengen der neuen Resultate benutzt.

Alle ursprünglichen Kausalrelationen und Zählwerte kommen unverändert aus
dem vollständigen v0.7-CPU-Kern. Die neue kontinuierliche Query-Geometrie
wird vollständig durch zertifizierte Eintrittsintervalle behandelt. Der
CPU-Vergleich erfasst beide Stufen, einschließlich aller Geometrie-Hashes.

## 3. Tatsächliche Grenzen lokaler Taylor-Histories

Sei L=1-Delta, tau=t+1, g=0 und phi(tau)=cos(tau*sqrt(L))*f für die
massive freie Kontinuumsgleichung auf R^3. Die deklarierten Adapter sind

    H1=f,                 H3=f-tau^2*L*f/2.

Für die Fourierkonvention f(x)=(2*pi)^(-3) integral fhat(k)e^(ikx) dk
folgt aus Cauchy-Schwarz und Plancherel

    ||psi||_infty <= ||L psi||_2 / sqrt(8*pi),

denn integral_R3 (1+|k|^2)^(-2) dk = pi^2. Die L2-Norm von
cos(tau*sqrt(L)) ist höchstens eins. Taylor mit Integralrest liefert daher

    |phi(tau,x)-H1(x)| <= tau^2 ||L^2 f||_2 /(2 sqrt(8*pi)),
    |phi(tau,x)-H3(tau,x)| <= tau^4 ||L^3 f||_2 /(24 sqrt(8*pi)).

Diese Formeln gelten auch bei negativer History-Zeit; verwendet werden
gerade Potenzen. Für allgemeines g wäre eine zusätzliche Abschätzung nötig;
hier bleibt g exakt null. Das sind konservative Approximationsobergrenzen,
keine Schätzungen oder Untergrenzen des tatsächlichen History-Fehlers.

Für f=A*exp(-1/h)*exp(4iz), h=1-4r^2>0, werden L^2 f und L^3 f als
exakte Polynome in x,y,z,h^-1 mit gaußschen ganzzahligen Koeffizienten
berechnet. Der Bump und alle Ableitungen werden außerhalb r<1/2 null
fortgesetzt. Es entstehen keine Randdistributionen, weil der Bump dort
mit sämtlichen Ableitungen verschwindet. Für jeden Monomterm gilt

    |x^p y^q z^r| <= (1/2)^(p+q+r),
    sup_(0<h<=1) h^-n exp(-1/h) = n^n exp(-n)  (n>=1),

und für n=0 ist das Maximum exp(-1). Dreiecksungleichung und
sqrt(Vol(B_1/2)) geben explizite eingeschlossene L2-Oberwerte. Diese
bewusst groben Normschranken können eine Qualifikation verweigern, selbst
wenn ein tatsächlicher Fehler kleiner wäre. Ein fehlgeschlagenes Budget
beweist daher keine entsprechende Fehleruntergrenze.

## 4. Weiterleitung bis zur Beobachtungsgröße

Wie in v0.9 wird A=T*h mit endlichem retardiertem Dreieckssystem berechnet.
Für jeden ursprünglichen History-Knoten j ergibt die obige Formel einen
normierten Fehleroberwert e_j. Somit gilt für denselben diskreten Operator

    |A(H)-A(exakter Kontinuumshistory)|/(A/e)
          <= sum_j |T_j| * e_j.

Das schließt den Anfangsdatenfehler bis zur Detektorantwort ein. Es
qualifiziert weder den diskreten Operator noch seine Gebietsabschneidung
gegen das Kontinuum. Bei Wellen bleiben der direkte Orakelvergleich und
der signierte Operator-/Gebietsbeitrag separat verfügbar. H3 erhält wie
H1 zusätzlich eigene Rundungs- und Float-Lösungsdiagnosen. Das Budget
von 0,001 der Feldskala gilt getrennt für Integration und diese
Anfangsdatenobergrenze.

Ein strukturelles Hindernis ist stärker als die Beschränkung auf H1/H3:
Außerhalb der kompakten Quellstütze verschwinden ALLE lokalen Cauchy-Jets
L^r f und L^r g. Jede endliche, ausschließlich aus diesen lokalen Jets
gebildete Taylor-History bleibt dort null. Hat eine Archivwolke keinen
History-Knoten in der Quellstütze, bleibt die homogene diskrete Lösung
für diese ganze Adapterklasse null. Eine höhere Taylor-Ordnung allein
kann fehlende Quellinformation deshalb nicht ersetzen. Das ist keine
Behauptung, dass jede nichtlokale Anfangsdatenabbildung scheitert.

## 5. Entscheidungen und Grenzen

Alle acht bekannten Wolken, beide Fenster und alle Gitterstufen werden
beibehalten. Die ursprünglichen fünf H1-Felder werden separat von dem
zusätzlichen kompakten H3-Feld ausgewiesen. Ressourcen- oder numerische
Probleme werden als solche ausgewiesen. Unzureichende räumliche
Einschließungen oder Anfangsdatenobergrenzen ergeben METHOD_HOLD.

Eine vollständige kompakte massive Kontinuumsdetektorreferenz und ein
prädiktiver Zweipunkt-Kovarianzkern sind weiterhin nicht qualifiziert.
Es gibt weder neue unabhängige Stichproben noch eine Quantengravitations-
oder Rauschinterpretation. G1 bleibt HOLD; Dirac bleibt zurückgestellt.
