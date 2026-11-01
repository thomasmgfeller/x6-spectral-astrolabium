# KVF-Antwortkanal v0.15: Herleitung und Aussagegrenzen

Die Rechnungen verwenden natürliche Einheiten c=hbar=1 und einen noch nicht
physisch festgelegten Maßstab ell0. Zahlen für Zeiten, Längen, Massen und
Antworten stehen in ell0, ell0, ell0^-1 beziehungsweise ell0^-2.
Dies ist ein neuer Kontrollvertrag mit kompakten Gewichten. Die Gaußfenster
und das Messbudget aus v0.14 werden nicht unverändert übernommen.

## 1. Frei gewähltes, explizites Messmodell

Es gilt (d_t^2 - Laplace + m^2) phi = J in 3+1 Minkowski.
M0 hat m=0, M1 nominell m=1/2. Der Zustand vor der Quelle ist das freie
Gaußvakuum; die retardierte freie Antwort ist zustandsunabhängig.

Für eine Kugel mit Radius a und ein Zeitfenster mit Halbbreite b definieren wir

$$F_a(\mathbf x)=\frac{105}{32\pi a^3}
 (1-|\mathbf x|^2/a^2)^2\,1_{\{|\mathbf x|<a\}},\qquad
\chi_b(t)=\frac{15}{16b}(1-t^2/b^2)^2\,1_{\{|t|<b\}}.$$

Beide Gewichte sind nichtnegativ und auf eins normiert. Die C1-Gewichte
haben genügend Fourier-Abfall für die hier verwendeten freien Feldgrößen;
sie sind keine Behauptung beliebig glatter realer Schaltpulse.
f_A=chi_b(t)F_a(x), f_B=chi_b(t-T)F_a(x-r e_z).
Phi_A und Phi_B sind die entsprechend gemittelten Felder.

Eine klassische Quelle J=j f_A koppelt über H_source(t)=-j chi_b(t) phi(F_A).
Die Quelle hat j mit Einheit Länge. Exakt für das freie Feld gilt

$$\delta\langle\Phi_B\rangle=j R_{BA},\qquad
R_{BA}=\int d^4x\,d^4y\, f_B(x)G_R(x-y)f_A(y).$$

Die Konvention ist (Box+m^2)G_R=delta^4 und
G_R(x-y)=i theta(x0-y0)[phi(x),phi(y)].
Wenn sämtliche B-Zeiten nach sämtlichen A-Zeiten liegen (T>2b), dann
R_BA=Delta_AB=(1/i)[Phi_A,Phi_B] in der Konvention von v0.13.
Liegt B vollständig früher, ist R_BA=0, während Delta_AB im Allgemeinen
nicht null ist. Das Vertauschen von Kommutator und retardierter Antwort
würde einen falschen rückwärts gerichteten Signalkanal erzeugen.

Der bekannte freie Greenkern lautet für t>0

$$G_R(t,d)=\frac{\delta(t-d)}{4\pi d}
-1_{\{t>d\}}\frac{m J_1(m\sqrt{t^2-d^2})}{4\pi\sqrt{t^2-d^2}}.$$

Diese Form folgt auch durch Ableiten von
-d_r[J0(m sqrt(t^2-r^2)) theta(t-r)]/(4 pi r);
siehe [Q2, Anhang A, A.1]. Die übrige Physik jener Arbeit wird nicht
als Modell unseres Experiments übernommen. [Q1] liefert die freie
Kommutator-/Greenfunktions-Grundlage.

## 2. Zwei getrennte Rechenwege

Mit sphärischen Besselfunktionen sind

$$\widetilde F_a(k)=105j_3(ak)/(ak)^3,\qquad
\widetilde\chi_b(\omega)=15j_2(b\omega)/(b\omega)^2.$$

Die Werte bei null sind eins. Für strikt zeitlich geordnete Fenster:

$$R_{BA}=\frac{1}{2\pi^2}\int_0^\infty
\frac{k^2}{\omega_k}\widetilde F_a(k)^2
\widetilde\chi_b(\omega_k)^2
\operatorname{sinc}(kr)\sin(\omega_k T)\,dk,\quad
\omega_k=\sqrt{k^2+m^2}.$$

Die symmetrisierte Vakuumkovarianz H_AB ersetzt sin durch cos und
1/(2 pi^2) durch 1/(4 pi^2). Sie kann bei raumartiger Trennung ungleich
null sein, während die Antwort exakt null ist.

Ein zweiter Weg integriert den positiven Gewichtskern im Ortsraum.
Die dimensionslosen Selbstfaltungen für 0<=w,v<=2 sind

$$C_F(w)=\frac{35(2-w)^6
(5w^5+60w^4+288w^3+656w^2+576w+192)}{270336\pi},$$
$$C_\chi(v)=\frac{5(2-v)^5
(v^4+10v^3+36v^2+40v+16)}{3584}.$$

C_chi wird gerade fortgesetzt. Außerhalb der Träger sind beide null.
Symbolische Integration bestätigt integral 4 pi w^2 C_F(w) dw=1 und
integral C_chi(v) dv=1. Das Ortsraumintegral mittelt den Besselschwanz
über w in [0,2], v in [-2,2], z in [-1,1], mit Gewichten
4 pi w^2 C_F(w), C_chi(v), 1/2 und
t=T+bv, d^2=r^2+a^2 w^2+2rawz.

Bei K=400 begrenzen die expliziten endlichen Sinus-/Kosinusdarstellungen
von j3 und j2 den absoluten weggelassenen Antwortanteil durch

$$\frac{105^2 15^2 A_K^2 B_K^2}{24\pi^2 a^8 b^6 K^{12}},$$
$$A_K=1+6/(aK)+15/(aK)^2+15/(aK)^3,\quad
B_K=1+3/(bK)+3/(bK)^2.$$

Nominell sind das etwa 5.35e-17. Dies ist eine analytische Schranke des
unendlichen Integralschwanzes, keine Zertifizierung aller Gleitkommafehler.
Die endliche Quadratur wird mit 32/64 Punkten je Teilintervall und
12/20 Punkten des anderen Rechenwegs kontrolliert. Die Primärentscheidung
stützt sich auf die folgende rationale Schranke, nicht auf Rundungsreste.

## 3. Robuste Träger- und Antwortschranke

Festgelegt sind r in [0.99,1.01], a in [0.245,0.255],
b in [0.098,0.102], m_M1 in [0.49,0.51] und |delta T|<=0.02.

Beim raumartigen Test T=0.25 ist der kleinste räumliche Abstand 0.48;
die größte Zeitdifferenz ist 0.474. Alle Trägerpaare sind daher strikt
raumartig. Für T=-2 ist die Quelle überall später als die Auslese.
Beide Einstellungen liefern in beiden Modellen exakt R=0.

Beim späten Test T=2 gilt t_min=1.776>d_max=1.52.
Der Abstand zur Lichtkegeloberfläche ist mindestens 0.256. Damit fällt
der Delta-Anteil für jede zulässige Parameterwahl weg. M0 liefert exakt
null. Für M1 setzen wir z=m sqrt(t^2-d^2). Dann

$$z^2\le 47913021/39062500<8,\qquad
1-z^2/8\le 2J_1(z)/z\le1.$$

Die letzte Ungleichung folgt aus der alternierenden Potenzreihe
sum_k (-z^2/4)^k/[k!(k+1)!], deren Beträge in diesem Bereich abnehmen.
Positivität und Normierung der Faltungsgewichte sowie
333/106 < pi < 22/7 geben exakt

$$0.008085297011005455\ldots\le -R_{M1}
\le0.010349324324324324\ldots.$$

Die rationalen Endpunkte stehen im Zertifikat. Für die Entscheidungsregel
wird konservativ nur -R_M1>=0.008 benutzt. Nominell lautet die unabhängige
Ortsraumrechnung R_M1=-0.009054974392663.
Diese Trennung ist eine Massensensitivität in derselben flachen Geometrie.
Sie rekonstruiert weder Krümmung noch eine eindeutige Raumzeit.

## 4. Explizite Sonde und ihre Rückwirkung

Als mathematische Auslesereferenz dient ein einzelner idealisierter
Zeiger mit [Q,P]=i, vernachlässigbarer freier Entwicklung und
H_probe(t)=lambda chi_b(t-T) P phi(F_B). Er ist anfangs vom Feld unabhängig.
P ist konstant; lambda hat Einheit Länge. Weil freie Feldkommutatoren
c-Zahlen sind, endet die Magnus-Reihe nach dem quadratischen Term:

$$U_B=\exp[-i\lambda P\Phi_B+i\lambda^2 K_{BB}P^2/2],\quad
K_{BB}=\int f_B(x)G_R(x-y)f_B(y)\,dx\,dy.$$
$$Q_{\rm out}=Q+\lambda\Phi_B-\lambda^2K_{BB}P
                 +\lambda jR_{BA}.$$

Bei zentriertem Zeiger mit symmetrisierter Q-P-Kovarianz C_QP folgt

$$\operatorname{Var}(Q_{\rm out})=
V_Q+\lambda^2H_{BB}+\lambda^4K_{BB}^2V_P-2\lambda^2K_{BB}C_{QP}.$$

Die Quellwirkung verschiebt den Mittelwert kohärent; sie ändert beim
freien Feld die zusammenhängende Feldkovarianz nicht. Die Sondenquelle
-lambda P f_B verändert aber spätere Feldgrößen. Für einen späteren
Auslesetest C entsteht der Zusatz -lambda P R_CB und damit insbesondere
ein zusätzlicher Varianzanteil lambda^2 V_P R_CB^2. Das ist eine
Rückwirkungsbilanz, keine vernachlässigte Störung.

Mit j=100, lambda=0.5, V_Q=V_P=0.5 und C_QP=0 erfüllt der Zeiger die
Heisenberg-Untergrenze. Nach Division des Rohwerts durch lambda*j ist
seine Varianz nominell etwa 3.45e-4 in ell0^-4. Die verwendete gesamte
synthetische Kovarianz kann diesen unabhängigen Anteil enthalten und
besitzt danach noch eine positiv definite technische Restkovarianz.
Dieser Konsistenztest konstruiert kein physisches Gerät. Eine räumlich
ausgedehnte Sonde mit einem einzigen Zeiger ist eine Idealisierung;
die kausale Realisierung verteilter Kopplung, Verstärkung und späterer
Auslese gehört in einen separaten lokalen Detektorvertrag [Q3].

## 5. Kalibrierkontrast und endliche Entscheidungsregel

Pro Einstellung und Block werden vier Quellzeichen (+,-,-,+) mit
gleichzeitigem Signal- und Referenzkanal erfasst. D ist der Mittelwert von

$$B_{i,s}=\frac14\sum_{t=1}^4 v_t
            (Y_{{\rm signal},i,t,s}-Y_{{\rm ref},i,t,s}).$$

Konstante Offsets und lineare Drift innerhalb des Blocks fallen exakt
heraus, ebenso ein identischer, vorzeichenabhängiger Beitrag in beiden
Kanälen. Die Gewichte summieren sich zu null und sind orthogonal zu
(-1.5,-0.5,0.5,1.5). Quadratische Drift bleibt dagegen erhalten.
Alle nicht entfernten ungeraden Beiträge und Drifteffekte müssen in
der unabhängig belegten Restschranke |c_s|<=0.0005 enthalten sein.

Das Messmodell lautet D_s=K R_s+c_s+epsilon_s mit 0.99<=K<=1.01.
Die vier Blockkontraste dürfen korreliert sein. Zwischen Blöcken wird
Unabhängigkeit vorausgesetzt; für die primäre Komponente gilt
E exp(t epsilon_i)<=exp(t^2 sigma^2/2), sigma<=0.05.
Dies ist eine harte Modellannahme, keine aus den Daten bereits bewiesene
Eigenschaft einer Apparatur.

Im späten Test liegen die ungünstigsten Mittelwerte bei -0.0005 (M0)
und -0.00742 (M1). Ihre Lücke g beträgt 0.00692.
Die Regel entscheidet bei D_late<-0.00396 für M1, sonst für M0.
Aus dem Chernoff-Argument für unabhängige subgaußsche Blöcke folgt
für jede Richtung P(error)<=exp[-n g^2/(8 sigma^2)].
Bei n=2048 beträgt dies 0.007420065755<0.01.
Das Zertifikat belegt exp[n g^2/(8 sigma^2)]>100 mit einer endlichen
Summe positiver rationaler Taylor-Terme; numerische Logarithmen sind
für die Entscheidung über die Schranke nicht erforderlich.

2048 Blöcke bedeuten 8192 Quellstellungen mit parallelem Referenzkanal
für die primäre Einstellung. Alle vier Einstellungen zusammen verwenden
32768 Quellstellungen beziehungsweise 65536 skalare Rohwerte pro Modell.
Das Budget ist hinreichend unter diesem Vertrag und nicht minimal.

## 6. Gegenbeispiele und Nichtidentifizierbarkeit

Ist der ungerade Rest einstellungsabhängig unbeschränkt, kann
c_1(s)=K[R_0(s)-R_1(s)]+c_0(s) sämtliche Mittelwerte beider Modelle
gleichsetzen. Bei gleicher Gesamtrauschverteilung sind dann alle
Rohdatengesetze gleich. Die Nullkontrollen bleiben dabei null:
Ein bestandener raumartiger Nulltest allein schließt diesen Alias nicht aus.

Eine AR(1)-Folge mit Korrelation 0.9 und derselben marginalen Varianz
vergrößert die Mittelwertvarianz bei n=2048 um den Faktor 18.9121.
Die genaue gaußsche Endpunkt-Fehlerrate steigt auf ungefähr 23.57 %.
Das unabhängige Budget gilt dann nicht.

Schließlich besitzt das klassische Klein-Gordon-Feld denselben
retardierten Greenkern. Die Antwort allein weist keine Quantenphysik
nach; insbesondere bestimmt der freie Kommutator nicht den Vakuumzustand.
Auch das Hinzufügen eines endlichen Vektors symmetrisierter Gaußmomente
begründet hier keinen Ausschluss aller klassischen Modelle.

Das Zwei-Schlüssel-Prinzip bleibt deshalb operational: eine unabhängig
belegte Kalibrierung und ein unter ihr informativer Modelltest.
Beide können gemeinsame Fehlerquellen haben. Alle physischen Freigaben
bleiben HOLD_FIELD_TRANSFER, bis reale Referenzen, Pulse, Zustands- und
Detektormodell sowie unabhängige Versuche belegt sind.
