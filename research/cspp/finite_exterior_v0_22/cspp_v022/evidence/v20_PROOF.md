# CSPP v0.20: lokale äußere History und exakte Intervallüberlappung

29. Oktober 2026. Fortsetzung von v0.19 auf Main-Commit
`b3e2c41bb32fec02a08432b40cc95acba013952a` (PR #151).

## Aussage und Grenze

Diese Rechnung liefert eine geschlossene Volumenformel, tatsächliche
Archivzählungen und bedingte Gewichtskerne sowie eine vollständige obere
Schranke für einen **begrenzten History-Wurzelbereich**

    P = [-6,-5] x [-2,2]^3,  |P|=64.

Die Schranke enthält alle diskreten Pfade von einer Historywurzel in P
zum unveränderten, räumlich und zeitlich gemittelten Detektor. Sie enthält
auch Pfade über noch unbekannte aktive Außenpunkte. Sie ist eine bedingte
Erwartungswertschranke, keine Realisierungsgenauigkeit.

P ist eine deterministisch festgelegte Integrationsregion. Die acht
zusätzlichen Auswertungspunkte sind Rechenkontrollen und keine Poissonpunkte,
keine neue Wolke und kein Bestätigungsensemble. Die physikalische History
wird weder abgeschnitten noch verändert. Der komplementäre Wurzelbereich
außerhalb von Omega5 bleibt offen. Die globale Restmajorante aus v0.19
wird durch diese Teilrechnung allein nicht kleiner. METHOD_HOLD, G1 HOLD
und NOT_RUN für eine frische Bestätigung bleiben bestehen.

## 1. Unveränderte Größen

Es gelten die Quelle und Normierung aus v0.19:
f(x)=exp(1-1/h)exp(4iz), h=1-4|x|², innerhalb |x|<1/2, sonst null;
Anfangszeit -1, Anfangsgeschwindigkeit null, Masse 1. Historywerte U(t,x)
sind für t<=-1 vorgeschrieben. Nur t>-1 wird diskret entwickelt.

rho=3/pi, epsilon=1/16, a=1/sqrt(2pi), beta=a/[16(1+a)],
kappa=4976184375/4294967296, gamma=beta*kappa. w(n) ist der unveränderte
viergliedrige Schichtkern. Es gilt |w(n)|<=kappa.

B=Omega5=I(b,c), b=(-5,0), c=(5,0). Der Detektor mittelt normiert über
die Kugel mit Zentrum d0=(0,0,3/2), Radius 1/2, in den Zeitfenstern
W0=[3/4,1] und W1=[1,5/4]. Vier archivierte Omega5-Konfigurationen bleiben
bitgenau erhalten. In ihrem relevanten aktiven Teil liegen 65,49,59,50
Punkte. Die mittlere noch fehlende aktive Punktzahl ist lambda=29/512.

Die v0.16-Detektorkoeffizienten werden als vorhandene validierte Intervalle
weiterverwendet. Ihre räumlichen Integrationsfehler werden nicht entfernt.
Die lokale KG-Referenz aus v0.3/v0.5 wird unverändert erneut ausgeführt.
Alle verwendeten Quelldateien werden gegen den Git-Blob des gepinnten
Main-Commits geprüft; die vier Arrays zusätzlich gegen RUNS.json.

## 2. Geschlossene tatsächliche Überlappung

Für p in B und y vor p ist

    I(y,p) Schnitt B = J+(y) Schnitt I(b,p).

Der obere Rand von B ist bereits durch z vor p vor c erfüllt.
Setze v=p-b, w=y-b, Minkowski-Produkt mit Signatur (+---), und

    h=sqrt(v.v),  u=(v.w)/h,  d=sqrt(u²-w.w).

Im Ruhesystem von I(b,p) liegen b=(0,0), p=(h,0), y=(u,d e).
Im echten Linsenfall sind d>|u| und h>u+d. Bei Zeit s schneiden sich
Kugeln der Radien r=min(s,h-s), R=s-u im Abstand d. Ihr Schnittvolumen ist

    pi (r+R-d)² [d²+2d(r+R)-3(r-R)²]/(12d).

Die Formel folgt auch unmittelbar aus den zwei Kugelkappen mit
x=(d²+r²-R²)/(2d), Kappenhöhen r-x und R-d+x, und
Vcap=pi H²(3r-H)/3. Es werden drei Bereiche integriert:

1. (u+d)/2 bis h/2: r=s, R=s-u, echte Linse;
2. h/2 bis (h+u+d)/2: r=h-s, R=s-u, echte Linse;
3. (h+u+d)/2 bis h: volle kleinere Kugel mit Radius h-s.

Die polynomiale Integration ergibt

    V_overlap = pi h (h-u-d)² (d²+dh-u²)/(24d).

Bei y vor b ist V_overlap=pi h⁴/24; bei b vor y ist die Überlappung
das ganze Intervall I(y,p). Nullränder werden mit den entsprechenden
Grenzfällen behandelt. Bei nicht kausalem y,p ist das Volumen null.
Für s0=(p-y).(p-y) lautet das Gesamtvolumen pi s0²/24. Damit

    mu_out = rho (V_total - V_overlap).

Der Faktor pi kürzt sich bei Multiplikation mit rho=3/pi vollständig.
Die Verzweigungen werden mit exakten rationalen Darstellungen der
archivierten Binary64-Koordinaten entschieden. Quadratwurzeln und die
Volumenformel werden mit Arb eingeschlossen.

Kontrollen: separate validierte Integration der beiden Kugelkappen,
exakte rationale Beispielwerte, Lorentz- und Rotationsinvarianz,
Grenzfälle sowie ein absichtlich falsches Überlappungsvolumen. Die
Wolfram-Symbolrechnung bestätigt zusätzlich dieselbe geschlossene Formel.
Dies ist eine Rechenkontrolle, kein unabhängiges wissenschaftliches Review.

## 3. Archivbedingter Kern

n0(y,p) zählt die bekannten Punkte in I(y,p) Schnitt B. Jede kausale
Relation wird exakt rational ausgewertet; keine Float-Toleranz entscheidet
über ein Intervall. Unter der Endpunkt-Palmverteilung ist die zusätzliche
Punktzahl Poisson(mu_out). Die endliche Formel aus v0.19 berechnet

    F(n0,mu)=E |w(n0+Poisson(mu))|.

Die exakte positive Gewichtsmenge ist {0,1,21,...,70}. Mit r=15/16,
z=mu/16 und b_j=binom(n0,j) epsilon^j r^(n0-j) gilt

    Ew=exp(-z) Sum b_j P_j(z),
    P0=1-9z+8z²-4z³/3, P1=-9+16z-4z²,
    P2=16-8z, P3=-8,
    F=-Ew+2 exp(-mu) Sum_(n in Z+, n>=n0) w(n) mu^(n-n0)/(n-n0)!.

Die ausgewählten Punktkontrollen werden zusätzlich mit einer direkten
Poissonsumme bis 512 und einem Chernoff-Rest eingeschlossen. Alle übrigen
Punktwerte verwenden dieselbe bereits bewiesene endliche Formel.

Für Intervalle von mu wird neben direkter Arb-Auswertung eine obere Tabelle
verwendet: n0=0,...,191; 512 geschlossene mu-Intervalle der Breite 2 bis
1024. Jeder Eintrag ist eine nach oben geprüfte Binary64-Obergrenze einer
Arb-Einschließung. Für einen Zellbereich wird das Maximum aller berührten
Tabellenfelder verwendet. Außerhalb des Tabellenbereichs greift kappa.
Die Speicherung als Float ist hier ausschließlich eine nach oben geprüfte
Majorantenspeicherung, keine Approximation eines zu zertifizierenden Werts.

## 4. Lokale KG-Werte und uniforme Feldhülle auf P

Die acht in PROTOCOL.json festgelegten äußeren Punkte werden bei 128 und
192 Bit mit der existierenden KG-Referenz neu eingeschlossen. Die dortige
Abtrennung des Quellenrandes h<1/64 bleibt durch einen analytischen Rest
gedeckt; sie ist keine Änderung der Quelle. Die Mittelpunktwerte werden
nicht als Feldhülle über eine vierdimensionale Zelle benutzt.

Auf ganz P gilt tau=|t+1| in [4,5] und R=|x|<=sqrt(12).
Somit tau>R+1/2: Lichtkegeloberfläche und masseloser Kirchhoff-Anteil
treffen die kompakte Quelle nicht. Die unveränderte KG-Formel reduziert sich zu

    U(t,x)=tau/(32pi) Integral f(z) G(tau²-|x-z|²) d³z,
    G(A)=0F1(3;-A/4).

Für 0<=A<=25 ist G positiv und monoton fallend. Ein expliziter Nachweis:
G'(A)=-0F1(4;-A/4)/12. Für q=A/4<=25/4 begrenzt die alternierende Reihe

    0F1(4;-q) >= 1-q/4+q²/40-q³/720 > 0.

Die Beträge der Reihenglieder fallen ab n=1; die Ableitung des unteren
Polynoms ist -[(q-6)²+24]/240<0, und sein Wert bei 25/4 ist positiv.
Arb bestätigt G(25)>0. Deshalb ist für jede Zelle C mit Zeitgrenzen und
R_max=max_C |x| die folgende Größe eine uniforme Hülle:

    U_C = tau_max ||f||_1 G(tau_min²-(R_max+1/2)²)/(32pi).

Die L1-Quellnorm wird durch validierte radiale Quadratur und den Rest
(pi/6)exp(1-64) eingeschlossen. Der Quellenphasenfaktor hat Betrag eins.
Alle verwendeten Zellargumente sind positiv und höchstens 25.

## 5. Einschließung der vollständigen Patch-Integrale

P wird mit 2 beziehungsweise 4 gleichen Teilungen je Koordinate vollständig
und ohne Überlappung bis auf Nullränder partitioniert: 16 bzw. 256 Zellen.
Seien t_c,x_c der Mittelpunkt, h_t die zeitliche und h_x die räumliche
Halbbreite. Setze l=h_t+(7/4)h_x und y_-=(t_c-l,x_c), y_+=(t_c+l,x_c).
Da 7/4>sqrt(3), gilt für jeden Zellpunkt y:

    y_- vor y vor y_+,
    I(y_+,p) Teilmenge I(y,p) Teilmenge I(y_-,p).

Dies schließt sowohl n0 als auch mu_out ein. Nichtkausale Unterintervalle
liefern die untere Grenze null. Ein nichtkausales Oberintervall macht den
Beitrag der ganzen Zelle null. Das Maximum der eingeschlossenen Kerne
multipliziert mit beta*rho*|C|*U_C liefert einen oberen ersten History-Antrieb
F_p für jeden der 223 bekannten aktiven Punkte.

Auch der direkte Detektorbeitrag wird über das **gesamte Fenster und
die gesamte Detektorkugel** eingeschlossen. Für W=[l,u] dienen
d_-=(l-1/2,d0), d_+=(u+1/2,d0) als kausale Unter- und Oberpunkte.
Beide liegen in B. Für alle Detektorpunkte d gilt
I(y_+,d_-) Teilmenge I(y,d) Teilmenge I(y_-,d_+).
Die so berechnete uniforme Kernschranke darf unter der normierten
Detektormittelung unverändert verwendet werden. Es werden keine
Detektormittelpunkte anstelle des vollständigen Detektors eingesetzt.

## 6. Transport ohne falsche Unabhängigkeitsannahme

Zerlege die Pfade mit Wurzel in P in solche, deren aktive Knoten sämtlich
in B liegen, und solche mit mindestens einem aktiven Außenknoten.

Für die erste Klasse sind alle Kanten zwischen aktiven Innenpunkten und
zum Detektor durch kausale Konvexität allein von B abhängig. Mit den
archivierten gemittelten Detektorkoeffizienten q und der strikt unteren
Matrix K_ij=beta*w(n_ij) berechnet der Rückwärtslauf

    a_j=q_j+Sum_(i>j) a_i K_ij.

Ein separater Vorwärtslauf mit Einheitsantrieb kontrolliert diese Identität.
Der bekannte Transportbeitrag ist höchstens Sum |a_j| F_j. Das Betragsnehmen
erfolgt erst nach dem eingeschlossenen adjungierten Lauf. Es wird keine
Unabhängigkeit der unterschiedlichen Historyintervalle vorausgesetzt.

Für Pfade mit mindestens einem aktiven Außenknoten wird |K|<=gamma
verwendet. Multivariate Mecke-Integration und die geordneten Zeitintegrale
ergeben für k Außenknoten lambda^k/k!. Die Auswahl bekannter Knoten trägt
höchstens (1+gamma)^n bei. Mit

    D_uniform=beta*rho*kappa Sum_C |C| U_C

folgt daher

    B_unknown <= D_uniform (1+gamma)^n [exp(gamma*29/512)-1].

Diese Grenze ist auch nach eingefügten Palm-Endpunkten gültig, weil die
einheitliche Schichtgewichtsschranke für jede ganzzahlige Zählung gilt.
Ein aktiver Außenpunkt kann auf einem zum inneren Detektor laufenden Pfad
nicht nach einem inneren Punkt auftreten: das würde die kausale Konvexität
von B verletzen. Die beiden Pfadklassen sind vollständig und disjunkt.

Die ausgewiesene Patch-Obergrenze ist

    B_P = D_window + Sum_j |a_j| F_j + B_unknown.

Alle Summen sind positiv majorisiert. Unterschiedliche Präzisionsläufe dürfen
leicht unterschiedliche obere Zahlen liefern, weil Arb-Radien und deren
obere Endpunkte Teil der Majorantenkonstruktion sind. Physikalische Werte
und Volumina werden auf Intervallüberlappung geprüft; Majoranten zusätzlich
auf gültige Zerlegung, Endlichkeit und numerische Stabilität. Ihre kleinen
arithmetischen Radien sind **nicht** die Schärfe der Fehlerobergrenze.

## 7. Restbilanz und nächste offene Arbeit

Mit der v0.19-Pfadzerlegung gilt formal Delta=Delta_P+Delta_complement.
Beide Beiträge können korreliert sein; für obere L1-Grenzen genügt die
Dreiecksungleichung. B_P ist nun eingeschlossen. Für den komplementären
Wurzelbereich wird hier keine neue integrierte Grenze berechnet.

Die v0.19-Gesamtmajorante darf nicht um B_P vermindert werden: zwei obere
Grenzen lassen sich nicht auf diese Weise subtrahieren. Deshalb wird die
bisherige globale obere Schranke unverändert weitergeführt. Ebenso wird
0,001 nicht nachträglich zu einem separaten Patch-Fehlerbudget umgedeutet.

Die nächsten rechnerischen Engstellen sind die noch breite direkte
Detektorhülle, engere gemeinsame Intervalle für n0 und mu, die räumlichen
Flanken außerhalb P sowie der übrige endliche und unendliche Historybereich.
Eine Aufhebung von METHOD_HOLD oder G1 HOLD folgt aus v0.20 nicht.

## Quellen

- Gepinnte Projektquellen v0.3, v0.5, v0.16 und v0.19; Identitäten in
  PROVENANCE.json und evidence/GITHUB_INPUTS.json.
- E. W. Weisstein, Sphere-Sphere Intersection, Wolfram MathWorld,
  https://mathworld.wolfram.com/Sphere-SphereIntersection.html ; die verwendete
  Kappenformel wird oben zusätzlich direkt hergeleitet.
- G. Last, M. Penrose, Lectures on the Poisson Process, Theorem 4.4
  (multivariate Mecke-Formel), bereits Grundlage von v0.19:
  https://www.math.kit.edu/stoch/~last/seite/lehrbuch_poissonp/media/lastpenrose2017.pdf
- FLINT / python-flint, validierte Arb/Acb-Arithmetik und Quadratur:
  https://python-flint.readthedocs.io/en/latest/arb.html
  https://python-flint.readthedocs.io/en/latest/acb.html
