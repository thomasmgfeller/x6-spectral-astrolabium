# Vollständige skalare Kontinuumsreferenz v0.12

**Referenzstatus: FULL_SCALAR_REFERENCE_READY. Gesamtstatus: METHOD_HOLD; G1 HOLD.**

Die räumlich und zeitlich integrierte Kontinuumsantwort der unveränderten
kompakten massiven Quelle ist für beide bisherigen Detektorfenster
eingeschlossen. Quellenrand, Bessel-Reihenrest und validierte Quadratur
werden getrennt ausgewiesen. Der neue Referenzcode importiert weder
Kausalsetgeometrie noch diskrete Transferkoeffizienten.

Auf denselben acht Archivwolken werden zusätzlich beide bisherigen
H1-Adapter mit der Kontinuumsreferenz verglichen: lokale Cauchy-Abtastung
und nichtlokale P1-Projektion aus v0.11. Die Vergleichsrechnung enthält
624 zertifizierte Kontinuumshistorywerte je Präzision und eine signierte
Fehlerzerlegung für jede der 32 Wolken/Fenster/Adapter-Kombinationen.

Die Zahlen und Attributionsergebnisse stehen in [RESULTS.md](RESULTS.md).
Alle Aussagen gelten für diesen linearen komplexen Feldmittelwert,
Masse 1, die vorgegebenen Fenster und die vorhandenen Entwicklungswolken.
Sie sind keine Intensitäts-, Wahrscheinlichkeits- oder Dirac-Referenz.

## 1. Unveränderte Zielgröße

Für a=b=1/2, d=3/2, k=4 und t0=-1 gilt

\[
 f(y)=A e^{-1/(1-4|y|^2)}e^{4iy_z}\,1_{|y|<1/2},\qquad
 g=0,\qquad \|f\|_{L^2(\mathbb R^3)}=1.
\]

Die Referenz löst die freie KG-Gleichung
u_tt-Delta u+u=0 auf dem ganzen R³. Mit D=B_(1/2)((0,0,3/2)) ist

\[
 \mathcal C_{[t_a,t_b]}=
 \frac{1}{|D|(t_b-t_a)}\int_{t_a}^{t_b}\int_D u(t,x)\,dx\,dt,
 \quad |D|=\frac\pi6,
\]

für [t_a,t_b]=[3/4,1] und [1,5/4]. In der verschobenen Zeit tau=t+1
sind die Endpunkte 7/4, 2 und 9/4. Es wird genau dieselbe Normierung
wie in v0.9/v0.10 verwendet. Die Rechnung gibt sowohl die physikalische
Antwort als auch die durch die bisherige Feldskala F0=A/e geteilte
Antwort aus. Die zweite verwendet f/F0=e exp(-1/h) exp(4iy_z).

Die normale Quellenamplitude A wird unabhängig durch das eingeschlossene
eindimensionale Integral 4 pi integral_0^(1/2) s² exp(-2/(1-4s²)) ds
bestimmt. Alte Quelldaten, Masse und Detektorparameter werden nicht angepasst.

## 2. Das Zeitintegral wird exakt ausgeführt

Schreibe L=1-Delta und S(tau)=sin(tau sqrt(L))/sqrt(L). Da g=0,

\[
 u(\tau)=\partial_\tau S(\tau)f,\qquad
 \mathcal C=\frac{\int_D S(\tau_b)f\,dx-
                         \int_D S(\tau_a)f\,dx}{|D|\Delta t}.
\]

Die Zeitintegration ist somit eine Endpunktdifferenz, keine Abtastung
des Intervalls und keine Mittelpunktsapproximation. Ihr zusätzlicher
Quadraturfehler ist null. Für positive tau lautet der dreidimensionale
Sine-Propagator mit Masse m

\[
 G_S(\tau,r)=\frac{\delta(\tau-r)}{4\pi r}
 -\frac{m}{4\pi}1_{r<\tau}
 \frac{J_1(m\sqrt{\tau^2-r^2})}{\sqrt{\tau^2-r^2}}.
\]

Dies ist die integrierte KG-Cauchyformel des Vorgängers; das negative
Vorzeichen des massiven Volumenterms wird gesondert geprüft. Die neue
Berechnung integriert den gesamten Detektor analytisch vor der
verbleibenden Quellenquadratur. Sie benutzt keine Punktantworten als
Ersatz für ein Volumenintegral.

## 3. Das räumliche Detektorintegral

Für einen Quellenpunkt y mit R=|y-d e_z| gilt hier 1<=R<=2 und R>b.
Für jede radiale integrierbare Funktion F folgt durch Kugelkalottengeometrie

\[
 \int_D F(|x-y|)\,dx=
 \frac\pi R\int_{R-b}^{R+b}
 r\,[b^2-(r-R)^2]F(r)\,dr.
\]

Der Test F=1 ergibt exakt |D|=pi/6. Für G_S erhält man

\[
 \int_D G_S(\tau,|x-y|)dx=\frac{P_\tau(R)}{4R},
\]
\[
 P_\tau(R)=[b^2-(\tau-R)^2]1_{|\tau-R|<b}
 -\frac{m^2}{2}\int_{R-b}^{\min(R+b,\tau)}
 r[b^2-(r-R)^2]\,{}_0F_1\!\left(2;-\frac{m^2(\tau^2-r^2)}4\right)dr.
\]

Das Integral ist null, wenn seine obere Grenze unter der unteren liegt.
Die drei analytischen Regionen sind R<tau-b (vollständig innerhalb des
Kegels), |R-tau|<b (partiell) und R>tau+b (außerhalb).
Grenzflächen sind Maß-null-Mengen; das Polynom des Oberflächenterms
verschwindet an ihren Übergängen.

Der gesamte Detektorball ist erfasst. Es wird keine Detektorspitze und
kein räumlicher Randstreifen ausgelassen.

## 4. Exakte Winkelmomente und eine verbleibende Radialquadratur

Setze y in Quellenkugelkoordinaten mit s=|y| und Winkel zur z-Achse.
Die Änderung auf R=|y-d e_z| erfüllt
y_z=(d²+s²-R²)/(2d) und d³y=2 pi s R ds dR/d.
Der Faktor R kürzt den Nenner der Detektorformel:

\[
 J(\tau):=\int_D S(\tau)(f/F_0)dx
 =\frac\pi{2d}\int_0^a s e^{1-1/(1-4s^2)}
 e^{ik(d^2+s^2)/(2d)}
 \int_{d-s}^{d+s}e^{-ikR^2/(2d)}P_\tau(R)\,dR\,ds.
\]

Die Reihe von 0F1(2;-x) wird bis n=N=16 verwendet:

\[
 {}_0F_1(2;-x)=\sum_{n=0}^N\frac{(-x)^n}{n!(n+1)!}+\mathcal R_N.
\]

Dadurch wird P_tau auf jeder der drei Regionen zu einem Polynom in R.
Seine Koeffizienten und die r-Stammfunktionen werden exakt rational
berechnet. Die Quellen-Winkelintegrale sind endliche Summen von

\[
 I_j(l,u)=\int_l^u R^j e^{\beta R^2}dR,\qquad \beta=-ik/(2d).
\]

I0 wird durch erf an den Endpunkten ausgewertet, I1 durch
(exp(beta u²)-exp(beta l²))/(2 beta), und für j>=2 gilt

\[
 I_j=\frac{u^{j-1}e^{\beta u^2}-l^{j-1}e^{\beta l^2}
                  -(j-1)I_{j-2}}{2\beta}.
\]

Für k=0 wird das exakte Monomintegral verwendet. Die komplexe
Quadratwurzel in I0 ist eine feste Konstante, kein variabler Zweig im
Integrationsgebiet. Die restlichen Integranden sind in s meromorph mit
ausgeschlossenen Stellen h=1-4s²=0. Ein Ball, der h=0 enthält, liefert
im Callback nichtendliche Werte. Alle tatsächlich integrierten
Radialsegmente liegen strikt innerhalb des Quellrandes.

Die s-Intervalle werden vor der Quadratur an |tau-b-d| und |tau+b-d|
geteilt, soweit diese Punkte im berechneten Quellkern liegen. Dadurch
ist die Auswahl der R-Regionen auf jedem Segment fest; in analytischen
Callbacks werden keine unkontrollierten min/max-Entscheidungen getroffen.

## 5. Getrennte rigorose Restgrenzen

**Quellenrand.** Berechnet wird s<=a sqrt(1-hc), hc=1/64. Auf dem
ausgelassenen Rand ist |f/F0|<=exp(1-1/hc). Aus |J1(z)/z|<=1/2 für
reelle z folgt für das Detektormittel eines S-Endpunkts

\[
 E_{\rm edge}(\tau)/|D|\leq
 (\tau+m^2\tau^3/6)e^{1-1/h_c}.
\]

Für das Zeitfenster werden die beiden Endpunktgrenzen addiert und durch
Delta t geteilt. Diese Schranke benötigt keine Ableitungen des abrupt
abgeschnittenen Kerns, weil zuerst die Zeitintegration ausgeführt wurde.

**Bessel-Reihe.** Für X=m²tau²/4 ist eine positive Majorante

\[
 B_N(X)=\frac{X^{N+1}}{(N+1)!(N+2)!}
 \left(1-\frac{X}{(N+2)(N+3)}\right)^{-1},
\]

sofern der Quotient kleiner als eins ist. Auf dem gesamten Integrationsgebiet
gilt 0<=m²(tau²-r²)/4<=X. Deshalb

\[
 E_{\rm series}(\tau)/|D|\leq m^2\tau^3 B_N(X)/6.
\]

Auch diese Endpunktgrenzen werden für das Fenster addiert und durch
Delta t geteilt. Es wird nicht vorausgesetzt, dass die abgeschnittene
Reihe exakt ist oder dass zwei Auflösungen den Rest schätzen.

**Quadratur und Rundung.** `acb.integral` schließt die verbliebenen
eindimensionalen Radialintegrale ein; die absolute und relative
Zielgenauigkeit sind jeweils 1e-22. Polynom-, Moment-, Summen- und
Divisionsarithmetik erfolgen ebenfalls in Arb/Acb. Ihr gemeinsamer
Komponentenradius steht getrennt von den analytischen Resten in den
Rohdaten. Ein kleinerer gemessener Gleitkommaunterschied wird nicht als
Fehlergrenze verwendet. Die Normierungsunsicherheit von A wird zusätzlich
in die physikalischen, unskalierten Werte übertragen.

## 6. Signierte Trennung der vier Fehlergruppen

Die endliche diskrete Lösung sei v[h], linear in ihrer History h.
Die exakten räumlich-zeitlichen Detektorkoeffizienten seien q und der
zugehörige Historytransfer T, also q v[h]=T h. Für q und T werden die
vollständigen zertifizierten v0.10-Intervalle des feinsten Gitters benutzt.
Die Geometrie und alle Intervallzählwerte werden neu berechnet und gegen
die alten Hashes geprüft.

Definiere h_KG als die zertifizierte exakte Kontinuumshistory, h_P als
die ideale History des jeweils ausgewählten Adapters, h_tilde als eine
festgelegte binary64-Realisierung der initialen Werte, q_hat als
binary64-Mittelpunkte der Querykoeffizienten und v_tilde als den
tatsächlich ausgeführten binary64-Dreieckssolve. Die neue numerische
Realisierung ist vollständig deklariert; sie wird nicht als identisch
zu jeder historischen Float-Implementierung ausgegeben.

Mit a_num=q_hat v_tilde lautet die exakte signierte Bilanz

\[
 a_{\rm num}-\mathcal C=E_A+E_O+E_I+E_S,
\]
\[
 E_A=T(h_P-h_{\rm KG}),\qquad
 E_O=Th_{\rm KG}-\mathcal C,
\]
\[
 E_I=\underbrace{T(\tilde h-h_P)}_{\text{Anfangsdaten-Integration/-Rundung}}
     +\underbrace{(\hat q-q)v[\tilde h]}_{\text{Detektorintegration}},
\]
\[
 E_S=\hat q\bigl(\tilde v-v[\tilde h]\bigr)
 \quad\text{einschließlich finaler Float-Summation}.
\]

Die Implementierung berechnet ES als a_num-q_hat v[h_tilde], sodass
auch die letzte Skalarprodukt-Rundung eingeschlossen ist. EA bezeichnet
den idealen Adapterfehler; die Unsicherheit der nichtlokalen Lastintegrale
wird zusätzlich im Anfangsdaten-Integrationsterm sichtbar. Deren
Korrelation mit EA darf nicht durch Addition unabhängiger Varianzen
ersetzt werden. Der Operator-/Gebietsbeitrag EO wird bewusst zusammen
ausgewiesen; eine Trennung zwischen Operatorform und Gebietsabschneidung
würde weitere Vergleichsrechnungen erfordern.

Die 624 KG-Historywerte werden mit der bereits zertifizierten
Off-center-Ortsraumformel ausgewertet. Sie dienen ausschließlich dem
Vergleich. Sie ersetzen weder den lokalen noch den nichtlokalen Adapter.
Die sehr kleinen numerischen und Quellenrandunsicherheiten dieser
Orakelwerte werden bis zum Detektor fortgepflanzt und gesondert berichtet.
Die neue volle Detektorreferenz entsteht unabhängig von dieser
punktweisen Historyrechnung.

Jeder signierte Beitrag erhält ein komplexes Intervall und Grenzen für
seinen Betrag. Ein dominanter Beitrag wird nur deklariert, wenn seine
Betragsuntergrenze größer ist als die Summe aller anderen Betragsobergrenzen.
Sonst lautet die Zuordnung UNRESOLVED. Der direkte Gesamtfehler wird
zusätzlich eng aus a_num-C berechnet; breite, korrelierte Zwischenintervalle
werden nicht als ein präzises Maß des Gesamtfehlers missverstanden.

## 7. Prüfungen und Reproduktion

15 analytische Tests kontrollieren Kugelvolumen, Lichtkegelterm, Vorzeichen
des ersten massiven Terms, Polynom/Bessel-Kernel, unabhängige direkte
Gaußmomentquadratur, k=0, kausales Nullsignal, benachbarte Zeitfenster,
Quellenrandänderung, Reihenrest, Quellen-Normierung und die signierte
Fehlerzerlegung. Die vollständigen Läufe bei 128 und 192 Bit vergleichen
886 Intervalle derselben Zielgrößen und prüfen 64 signierte Bilanzen.
Fehleroberwerte verschiedener Präzisionen werden nicht fälschlich als
dieselbe reelle Zielgröße auf gegenseitige Überlappung geprüft.

Eine zusätzliche unabhängige Fourier-Diagnose verwendet

\[
 \widehat{f/F_0}(p)=4\pi\int_0^a s^2e^{1-1/(1-4s^2)}
 \operatorname{sinc}(|p-k e_z|s)ds
\]

zusammen mit dem exakten Kugelfaktor
3(sin(bp)-bp cos(bp))/(bp)^3 und dem exakten Zeitfaktor
(sin(omega tau_b)-sin(omega tau_a))/(omega Delta t).
Sie verwendet eigene Gauß-Legendre-Gitter und Fourier-Abschneidungen.
Ihr kleiner numerischer Unterschied ist eine Zusatzkontrolle der
unabhängigen Darstellung, **kein** Zertifikat ihres Fourier-Abschneidefehlers.

```bash
cd research/cspp/full_continuum_v0_12
python -m pip install -r requirements.txt
python -m unittest -v test_continuum test_ledger
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B run.py \
  --bits 128 --out results/BENCHMARK_128.json.gz
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B run.py \
  --bits 192 --out results/BENCHMARK_192.json.gz
python -B verify.py
python -B fourier_diagnostic.py
python -B report.py
```

`FREEZE.json` hält den lokalen Methodenstand und die verwendeten früheren
Dateien vor den vollständigen Archivläufen fest. Kleine Vorprüfungen und
Entwicklungsdiagnosen gingen dem voraus. Dies ist keine öffentliche
Vorregistrierung und keine unabhängige neue Sprinkling-Bestätigung.

## 8. Quellen und Reichweite

1. NIST DLMF 10.2.2: Bessel-Reihe.
   https://dlmf.nist.gov/10.2#E2
2. NIST DLMF 10.14.4 mit nu=1: reelle Bessel-Majorante.
   https://dlmf.nist.gov/10.14#E4
3. Python-FLINT 0.9.0, `acb.integral`: Intervall- und Analytizitätsvertrag.
   https://python-flint.readthedocs.io/en/latest/acb.html
4. Unveränderte KG-Cauchyformeln und punktweise Referenz:
   `../scale_calibration_v0_2/METHODS.md`,
   `../massive_reference_v0_5/METHODS.md`.
5. Unveränderte diskrete Detektordefinition und Transferintervalle:
   `../detector_transfer_v0_9/PROTOCOL.json`,
   `../detector_methods_v0_10/METHODS.md`.

Der abgeschlossene Referenzpunkt betrifft genau die kompakte Quelle,
Masse 1 und die zwei festen linearen Detektorfenster. Die Kontinuumsreferenz
schließt nicht automatisch den diskreten Operator, seine Gebietsfehler,
die offene nichtlokale Historyfrage oder einen physikalischen
Fluktuations-/Kovarianzkern ab. METHOD_HOLD und G1 HOLD bleiben bestehen.
