# CSPP v0.22: vollständige endliche Außenhistory

29. Oktober 2026. Basis: Main `ff990b1ffe04259f963525e51aa106925b23cf6f`.
Dies ist Schritt 1 der Fortsetzung von v0.21. Der vollständige unendliche
Rest wird hier noch nicht kombiniert. METHOD und G1 bleiben HOLD.

## 1. Aussage, Konditionierung und unverändertes Modell

Für jede der vier unveränderten archivierten Omega5-Konfigurationen und
beide ursprünglichen Detektorfenster wird eine obere Grenze für
`E(|Delta_D5| | Archiv in B)` konstruiert. Delta_D5 umfasst alle diskreten
Pfade mit einer Historywurzel im nachfolgend definierten D5, einschließlich
der Pfade über unbekannte aktive Außenpunkte. Es handelt sich um eine
bedingte Erwartungswertschranke, nicht um eine realisierungsweise Garantie,
keine untere Fehlerschranke und keinen beobachteten physikalischen Fehler.

Die Quelle ist unverändert:

    f(x)=b(|x|) exp(4 i z), b(s)=exp(1-1/h), h=1-4s², 0<=s<1/2,
    f=0 außerhalb; Anfangszeit -1, Anfangsgeschwindigkeit 0, Masse m=1.

Für t<=-1 ist U die vorgeschriebene exakte KG-History; nur t>-1 wird
diskret entwickelt. rho=3/pi, epsilon=1/16, beta=a/[16(1+a)] mit
a=1/sqrt(2pi), kappa=4976184375/4294967296, gamma=beta*kappa.
Die schon bewiesene punktweise Schichtgewichtsschranke |w(n)|<=kappa
gilt auch unter Palm-Einfügungen. B=Omega5=I((-5,0),(5,0)).
Der Detektor ist die normierte Kugelmittelung um (0,0,3/2), Radius 1/2,
mit normierten Zeitmitteln W0=[3/4,1], W1=[1,5/4].

Die elf übernommenen Eingaben sind gegenüber den Git-Blobs des gepinnten
Main-Commits und SHA256 verifiziert. Die vier vollständigen archivierten
Koordinatenarrays und ihre aktiven Teilmengen bleiben identisch. Es werden
keine Wolken, Zufallszahlen oder statistischen Regeln hinzugefügt.
Die v0.20-Adjungierten einschließlich ihrer Detektorquadraturfehler werden
als vorhandene validierte Intervalle übernommen. Ihre damaligen Beweise
sind in `evidence/v20_PROOF.md` enthalten.

## 2. Lückenlose räumliche und zeitliche Abdeckung

Setze tau=-t-1. Die deterministische Rechengrenze ist t=-6, also tau=5.
Diese Grenze verändert weder die physikalische History noch den Operator.
Aus der KG-Retardierungsformel und dem Quellenradius folgt endliche
Ausbreitung: U=0 für R=|x|>tau+1/2. Für 0<=tau<=4 hat B auf dieser
Historyzeitscheibe Radius 4-tau; für tau>4 ist die Zeitscheibe von B leer.
Wenn tau<=7/4, liegt der ganze Feldträger in B. Deshalb ist der gesamte
endliche, potenziell nichtverschwindende äußere Wurzelbereich genau

    D5={7/4<tau<=5, max(0,4-tau)<R<tau+1/2, alle Raumrichtungen}.

Es gibt keine ausgelassenen räumlichen Flanken. Für -11/4<=t<=-1
verschwindet die äußere History exakt; außerhalb des angegebenen
Feldträgers ebenfalls. Nullränder beeinflussen die Integrale nicht.

Wir teilen D5 an R=tau-1/2 in das tiefe Innere und die Wellenfront.
Das tiefe Innere beginnt erst bei tau>9/4. Beide Teile werden mit
rationalen tau/R-Rechtecken der Seitenlänge 1/n, n=8,16,32, geschnitten.
Alle Schnittzeiten der affinen Randlinien werden exakt rational ermittelt.
Auf jedem Teilintervall [l,u] ist das Volumen

    (4pi/3) Integral_l^u [R_hi(tau)^3-R_lo(tau)^3] d tau.

Die Implementierung integriert das Polynom exakt. Unabhängige geschlossene
Gesamtformeln sind

    |D5|/pi = [(11/2)^4-2(9/4)^4]/3 = 110567/384,
    |D_deep|/pi = [(9/2)^4-2(7/4)^4]/3 = 50087/384,
    |D_front|/pi = 315/2.

Auf jeder Gitterstufe stimmen die Zellvolumina exakt mit allen drei Werten
überein. Ein separater rationaler Querschnittstest prüft Anschluss und
Überlappungsfreiheit auf sämtlichen durch die Geometrie bestimmten offenen
Zeitabschnitten. Die Zellzahlen sind 688, 2664 und 10480.

Der alte Patch P=[-6,-5] x [-2,2]^3 liegt vollständig im tiefen Inneren
von D5: tau in [4,5], R<=sqrt(12)<7/2. Er ist genau einmal enthalten.
Seine v0.21-Schranke wird deshalb NICHT zusätzlich addiert. Auch ist ein
direkter Schärfevergleich der alten Patch- und neuen Gesamtbereichsgrenze
wegen der verschiedenen Integrationsgebiete nicht zulässig.

## 3. KG-Formel und tiefes Innere

Die unveränderte KG-Referenz liefert bei m=1

    U = K_wave - (tau²/2) M_sphere
        + tau/(32pi) Integral_{B(x,tau) Schnitt B(0,1/2)} f(z) G(A) dz,
    A=tau²-|x-z|², G(A)=0F1(3;-A/4).

M_sphere ist das normierte sphärische Mittel von f;
K_wave ist das Mittel von f+tau n.grad(f) über z=x+tau n.
Es gilt 0<=A<=25. Der bereits in v0.20 verwendete vollständige Nachweis
für G wird hier erneut geprüft:

    G'(A)=-0F1(4;-A/4)/12,
    0F1(4;-q)>=1-q/4+q²/40-q³/720>0 für 0<=q<=25/4.

Die Beträge der alternierenden Reihenglieder fallen ab dem Glied n=1.
Die Ableitung des unteren Polynoms ist -[(q-6)²+24]/240<0; am rechten
Endpunkt ist es positiv. Arb schließt außerdem G(25)>0 ein. Also
0<G(A)<=1, monoton fallend.

Im tiefen Inneren ist die ganze Quelle innerhalb des Lichtkegels;
Oberflächen- und Kirchhoff-Terme verschwinden, auch im Grenzfall durch
das glatte Verschwinden des Bumps am Quellenrand. Für eine Zelle mit
Koordinatenhüllen [tau0,tau1], [R0,R1] setze

    Amin=max(0,tau0²-(R1+1/2)²),
    U_deep <= tau1 ||f||_1 G(Amin)/(32pi).

Auch wenn die rechteckige Hülle den Frontbereich berührt, bleibt diese
Schranke auf dem tatsächlichen tiefen Zellteil gültig. Amin=0 ist dann
die sichere Ersatzgrenze. ||f||_1=4pi J2(0) wird neu eingeschlossen.

## 4. Vollständige Wellenfrontschranke

Auf D_front gilt tau>=7/4 und R>=5/4. Auf der Lichtkugel lässt sich das
normierte Flächenmaß einer radialen Integrandenhülle als s ds/(2R tau)
schreiben, |R-tau|<=s<=1/2. Vor dem Betragsnehmen werden die beiden
Oberflächenterme kombiniert:

    (1-tau²/2) f + tau n.grad(f)
      = b(s) exp(4iz) [1-tau²/2 -4(s²+tau²-R²)/h² +4i tau n_z].

Dies folgt aus grad(b)=-8z b/h² und
2 tau n.z=s²+tau²-R². Mit |n_z|<=1, tau²/2-1>0 und
der Dreiecksungleichung erhalten wir eine uniforme, richtungsunabhängige
Hülle. Für eine Zelle definieren wir

    L=max(0,R0-tau1,tau0-R1),
    delta0=tau0²-R1², delta1=tau1²-R0²,
    J1(L)=Integral_L^(1/2) s b(s) ds,
    Jabs(L,delta)=Integral_L^(1/2) s b(s)|s²+delta|/h² ds.

Jabs ist als Integral eines Betrages affiner Funktionen konvex in delta.
Deshalb genügt das Maximum der beiden Endpunkte. Die Frontgrenze lautet

    W_C = (tau1/2-1/tau1+4) J1(L)/(2R0)
          +2 max[Jabs(L,delta0),Jabs(L,delta1)]/(R0 tau0).

Die vergrößerte Integrationsuntergrenze L liegt nie über dem tatsächlichen
|R-tau|. Der Koeffizient tau/2-1/tau+4 ist monoton steigend; alle
Nenner wurden in die konservative Richtung ersetzt.

Für den Volumenterm genügt auf der Front G<=1. Die Quellenmasse
M(tau,R)=Integral_{B(x,tau)} b(|z|) dz ist zunehmend in tau und
abnehmend in R. Letzteres folgt aus der Schichtdarstellung des radial
fallenden b als positives Gemisch konzentrischer Kugelindikatoren:
Das Schnittvolumen zweier Kugeln nimmt mit ihrem Abstand ab. Ein
elementarer Beweis betrachtet senkrecht zur Verbindungslinie die
Überlappung zweier symmetrischer Intervalle, deren Abstand R zunimmt.
Somit gilt auf der gesamten Zelle

    V_C <= tau1 M(tau1,R0)/(32pi),  U_C=min(M_global,W_C+V_C).

M_global ist die unveränderte v0.19-Sobolevgrenze. Es werden ausschließlich
nach oben eingeschlossene Endpunkte für die Majoranten ausgewählt.

## 5. Quellenmomente und unabhängige Quadratur

Mit zL=1/(1-4L²), e=exp(1), a_source=1/2 gilt

    b(L)=exp(1-zL),
    J1(L)=e Gamma(-1,zL)/8,
    J3(L)=Integral_L^a s³ b(s) ds
         =e [Gamma(-1,zL)-Gamma(-2,zL)]/32.

Die Substitution z=1/h liefert diese Formeln unmittelbar aus
Gamma(v,z)=Integral_z^infinity e^(-u)u^(v-1)du. Außerdem

    A0=Integral_L^a s b/h² ds=b(L)/8,
    A2=Integral_L^a s³ b/h² ds=L² b(L)/8+J1(L)/4.

Für delta>=-L² ist Jabs=A2+delta A0, für delta<=-1/4 ist
Jabs=-A2-delta A0. Dazwischen liegt die einzige Nullstelle bei
s=sqrt(-delta); die Aufteilung dort ergibt

    Jabs=J1(sqrt(-delta))/2-A2-delta A0.

Für eine teilweise schneidende Quellenkugel mit L=|R-tau|<1/2 ist

    M(tau,R)=4pi[J2(0)-J2(L)]  (nur wenn tau>R)
      +pi/R [(tau²-R²)J1(L)+2R J2(L)-J3(L)].

Bei R+1/2<=tau ist M=||f||_1, bei R>=tau+1/2 ist M=0.
Die Formel folgt aus dem Quellenwinkelanteil
[tau²-(R-s)²]/(4Rs) im partiellen Bereich. J2(L)=Integral_L^a s²b(s)ds
wird mit validierter acb-Quadratur bis s=sqrt(63/64)/2 eingeschlossen.
Der positive Randrest beträgt höchstens exp(-63)/24; für L hinter dieser
Grenze wird allein dieses Restintervall verwendet. Die Quelle wird nicht
abgeschnitten. `verify.py` prüft alternative Substitutionen:

    u=1/h-1:
    J1=1/8 Integral_(uL)^infinity e^-u/(1+u)² du,
    J3=1/32 Integral_(uL)^infinity e^-u u/(1+u)³ du,
    Jabs=1/8 Integral_(uL)^infinity e^-u |u/[4(1+u)]+delta| du;
    u=v²:
    J2=1/8 Integral_(vL)^infinity v²e^(-v²)/(1+v²)^(5/2) dv.

Die ersten Integrale enden bei u=128, mit positiven Resten höchstens
e^-128/8, e^-128/32 und (1/4+|delta|)e^-128/8. Das letzte endet bei
v=16 mit Rest e^-256/1048576: für v>=16 ist der Integrand höchstens
v e^(-v²)/(8*16^4). Sechs Quellenkugel-Massen werden separat über ihren
Winkelanteil im v-Integral überprüft; der ausgelassene Rest ist sicher
kleiner als (pi/6)e^-256. Alle Kontrollen sind Einschließungen.

## 6. Kausale Winkelanteile und vollständiger Detektor

Die Feldhülle ist von der Raumrichtung unabhängig. Deshalb kann für
jeden ersten Endpunkt p mit Radius r_p und Zeit t_p der vollständige
Winkelanteil kausaler Historywurzeln verwendet werden. Für R,r_p>0 und
Delta=tau+t_p+1>=0 ist er

    chi=clip_[0,1]([Delta²-(R-r_p)²]/[4Rr_p]).

Dies ist die sphärische Kappenformel aus |x-p_space|<=Delta. Bei Delta<0
ist der Anteil null; bei einer Zellhülle mit R=0 oder r_p=0 wird sicher
1 verwendet. Delta wird am oberen Zeitrand und der Quotient durch
Arb-Intervallauswertung eingeschlossen. Beim Quadrat eines Intervalls,
das null enthält, wird Multiplikation und Schnitt mit [0,infinity)
verwendet. Das vermeidet eine nichtendliche generische Potenzauswertung
von python-flint 0.8.0. Ein gezielter Regressionstest deckt diesen Fall ab.

Für einen bekannten aktiven Punkt j ist der obere erste Antrieb

    F_j=beta rho kappa Sum_C |C| U_C sup_C chi(p_j).

Es wird ausdrücklich die punktweise kappa-Hülle benutzt. Die schärferen
archivbedingten n0/mu-Kerne aus v0.20/v0.21 werden auf dem neuen vollen
Gebiet noch nicht berechnet. Das ist eine konservative Wahl, keine
Änderung des physikalischen Schichtkerns.

Nach Integration über alle Wurzelrichtungen hängt chi nur von Radius
und Zeit des Detektorendpunktes ab. Die exakte normierte radiale Dichte
der verschobenen Detektorkugel lautet für 1<=r<=2

    p(r)=4r[1/4-(r-3/2)²]=-4r³+12r²-8r,
    Integral_1^2 p(r)dr=1,
    Stammfunktion -r^4+4r³-4r².

16 radiale Intervalle und je 8 Zeitintervalle zerlegen jedes ganze
Detektorfenster. Ihre Massen sind exakte positive rationale Zahlen und
summieren sich je Fenster zu 1. Die gewichteten oberen chi-Werte liefern
den direkten Beitrag D_window. Kein Detektor-Mittelpunkt ersetzt ein
Volumen- oder Zeitintegral. Auch die Polarkappen sind vollständig erfasst.

## 7. Diskreter Transport und Ergebnisschranke

Die Pfadzerlegung und der Mecke-Nachweis aus v0.20 gelten für beliebige
äußere Historywurzelbereiche und somit für D5. Die bekannten inneren
Kanten und gemittelten Detektorkoeffizienten bleiben unverändert. Mit den
übernommenen adjungierten Koeffizienten a_j ist der bekannte Beitrag
Sum_j |a_j| F_j. Der erste Historyantrieb benutzt hier die obige neue
vollständige Gebietsintegration.

Für Pfade mit mindestens einem unbekannten aktiven Außenknoten gelten
die gleichmäßigen Kantenschranken auch nach Palm-Einfügungen. Die Auswahl
bekannter Knoten ergibt höchstens (1+gamma)^n; die geordneten Außenknoten
werden durch lambda^k/k!, lambda=29/512, majorisiert. Mit

    D_uniform=beta rho kappa Sum_C |C| U_C

folgt deshalb ohne Unabhängigkeitsannahme zwischen Historyintervallen

    B_unknown=D_uniform (1+gamma)^n [exp(gamma*29/512)-1],
    B_D5=D_window+Sum_j |a_j| F_j+B_unknown.

Die vier bekannten aktiven Knotenzahlen sind 65,49,59,50. Diese drei
Beiträge decken disjunkt den direkten Pfad, rein bekannten aktiven
Transport und Pfade mit unbekannten aktiven Außenknoten ab. Fubini/Tonelli
und die Dreiecksungleichung sind zulässig, da alle verwendeten Majoranten
auf dem endlichen Gebiet integrierbar sind.

Die drei Gitterstufen sind ausschließlich mathematische Verfeinerungen
derselben deterministischen Region. Sie ändern weder Statistik noch
Wolken. Die tatsächlich beobachtete Abnahme der oberen Zahlen wird
geprüft, aber keine asymptotische Konvergenzrate behauptet. Der feinste
192-Bit-Lauf liefert die im Bericht aufgerundeten oberen Grenzen.

## 8. Grenzen, Prüfungen und nächster Schritt

Die Wellenfront dominiert die neue absolute Feldmajorante. Weil Beträge,
die punktweise kappa-Hülle und richtungsunabhängige Feldhüllen verwendet
werden, sind die Grenzen konservativ. Ihre winzigen arithmetischen
Radien sind nicht die Unsicherheit oder Schärfe der Fehlermajorante.
Unterschiedliche Präzisionsläufe dürfen leicht verschiedene gültige obere
Zahlen liefern; physikalische Werte werden auf Intervallüberlappung,
Majoranten auf Stabilität und korrekte Zerlegung geprüft.

Zusätzlich laufen 30 vorab im Code festgelegte KG-Punktkontrollen pro
Präzision mit der unveränderten Originalreferenz, 50 unabhängige Moment-
und 6 Quellenmassenquadraturen, exakte Volumenkontrollen, kausale
Kappenprüfungen, Eingabeidentitätsprüfungen und gezielte Negativkontrollen.
Die Kontrollpunkte sind keine neuen Poissonpunkte und ersetzen keine
Zellhülle. Der vollständige isolierte Wiederholungslauf vergleicht alle
neun numerischen Ergebnisdateien bytegenau. Diese Selbstkontrollen sind
kein unabhängiges wissenschaftliches Review.

Der offene Wurzelbereich ist nun t<-6 auf dem vollständigen KG-Träger.
Er ist in dieser Version noch nicht in ein neues gemeinsames Restbudget
integriert. Die alte globale v0.19-Majorante wird unverändert weitergeführt;
man darf obere Schranken weder voneinander subtrahieren noch den alten
Patch doppelt addieren. Das unveränderte Gesamtziel 0,001 wird nicht zu
einem separaten Teilgebietsbudget umgedeutet. Selbst die neue endliche
Schranke genügt nicht für einen Nachweis dieses Ziels. METHOD_HOLD und
G1 HOLD bleiben bestehen; eine frische Bestätigung bleibt NOT_RUN.

Nächster Schritt: eine zu D5 disjunkte und mit derselben Konditionierung
und Pfadzerlegung kompatible Grenze für t<-6 herleiten und erst danach
eine vollständige globale Bilanz bilden. Dieser Auftrag umfasst nur
Schritt 1 und führt diesen nächsten Schritt nicht vorweg.

## Quellen und reproduzierbare Belege

- Unveränderte KG-Referenz: `vendor/legacy/massive_reference_v0_5/reference.py`
  und `vendor/legacy/certified_budget_v0_3/source.py`.
- Bisheriger Transportbeweis: `evidence/v20_PROOF.md`, Abschnitte 1 und 6.
- DLMF 8.2.2, obere unvollständige Gammafunktion:
  https://dlmf.nist.gov/8.2#E2 (abgerufen 29.10.2026).
- python-flint, Arb-Intervallarithmetik:
  https://python-flint.readthedocs.io/en/latest/arb.html
  (abgerufen 29.10.2026; Rechnung fest auf python-flint 0.8.0).
- Vollständige Gebietszellen, Intervallzahlen, Prüfungen und Quellidentitäten
  liegen in `results/`, `PROVENANCE.json` und `evidence/MAIN_TREE.json`.
