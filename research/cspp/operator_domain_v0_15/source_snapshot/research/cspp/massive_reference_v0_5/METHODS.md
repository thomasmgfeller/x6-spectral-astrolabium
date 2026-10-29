# Massive Kontinuumsreferenz und separate räumliche Fehlerkontrolle v0.5

Stand: 28. Oktober 2026. Deterministische Entwicklungsrechnung, keine neue
Sprinkling-Kampagne und keine E4-Bestätigung. Die Basis ist Commit
`c4501cd3d198ae770aedd84e37e11aea40681909`. Die früheren Pakete bleiben unverändert.

## 1. Exakter Umfang

Die ersten 28 Zeilen von `scale_calibration_v0_2/results/source.npz:query`
sind die unveränderten 21 inneren und sieben Detektor-Punktproben. Die
Zentrumsindizes sind 0, 7, 14. v0.3 enthält 28 masselose und sechs massive
Zentrumswerte; v0.5 ergänzt genau die restlichen 25×2=50 Werte. Zusammen
sind dies 84 verschiedene Probe/Masse-Paare. Die übrigen 256 archivierten
Abfragepositionen, ein globaler Lösungsfehler und Dirac-Felder sind nicht
hiermit eingeschlossen.

Die Quelle bleibt f(y)=A exp(−1/h) exp(iky_z), h=1−|y|²/a²>0,
a=1/2, k=4, sonst null, mit Anfangszeit −1 und Anfangsgeschwindigkeit null.
A stammt aus dem eingeschlossenen Normierungsintegral von v0.3; dessen
Unsicherheit einschließlich Randrest wird in jede neue Rechnung getragen.

## 2. KG-Cauchyformel und Quellenkoordinaten

Mit τ=|t+1|, R=|x|, c=x_z/R und dem Kugelmittel M_r gilt

\[
\phi_m=K-\frac{m^2\tau^2}{2}M_\tau f
       +\frac{m^4\tau}{8}V_m,\qquad K=\partial_\tau(\tau M_\tau f),
\]
\[
V_m=\frac1{4\pi}\int_{|x-y|\le\tau} f(y)
\,{}_0F_1\!\left(3;-\frac{m^2(\tau^2-|x-y|^2)}4\right)d^3y.
\]

Insbesondere ist das Vorzeichen des Lichtkegel-Oberflächenterms negativ.
Die unveränderten 27 exakten KG-Ebenenwellen und sechs Kontrollen mit falschem
Vorzeichen aus v0.3 werden erneut geprüft.

Für Quellenradius s=|y| und v=cos(angle(x,y)) lässt sich das Azimut exakt
integrieren. Mit b=a sqrt(1−h_c) erhält man für den berechneten Kern

\[
V_m^{\rm core}=\frac A2\int_l^u s^2e^{-1/h(s)}
 \int_{v_0(s)}^1 e^{ikcsv}
 {}_0F_1\!\left(1;-\frac{k^2s^2(1-c^2)(1-v^2)}4\right)
 {}_0F_1\!\left(3;-\frac{m^2(\tau^2-R^2-s^2+2Rsv)}4\right)dv\,ds,
\]

mit l=max(0,R−τ), u=min(b,R+τ). Im vollständigen Kugelbereich
s≤τ−R ist v₀=−1; sonst v₀=(R²+s²−τ²)/(2Rs). Das Radialintegral wird
an s=τ−R geteilt. Bei τ=R wird v₀=s/(2R) verwendet, damit kein künstlicher
Pol am Ursprung entsteht. Vier unabhängige exakte Kugelschnittvolumina
prüfen Maßfaktor, Support und diese Aufteilung.

Das Oberflächenmittel Mτ wird separat im Winkel μ integriert; K wird aus
der unveränderten eingeschlossenen v0.3-Routine übernommen. Für die
Punktwerte gilt h_c=1/64. Sämtliche Besselprodukte sind ganze 0F1-Funktionen;
es wird kein nichtanalytischer Wurzelzweig eingeführt.

Für reelle z gilt |J₂(z)|≤z²/8 und damit
|0F1(3;−z²/4)|≤1 [1]. Die ausgelassenen Beiträge erfüllen

\[
E_M\le A e^{-1/h_c},\qquad
E_V\le\frac{Aa^3}{3}e^{-1/h_c},
\]
\[
E_{\phi,\rm added}\le\frac{m^2\tau^2}{2}E_M+
\frac{m^4\tau}{8}E_V.
\]

Für K ist bereits die v0.3-Schranke

\[
E_K\le Ae^{-1/h_c}\left(1+k\tau+
 \frac{2\tau(\tau+R)}{a^2h_c^2}\right)
\]

enthalten. Komplexe Restfehler werden als einschließende Rechtecke addiert.
`quadrature_component_radius_upper` umfasst konservativ auch den bereits
in K enthaltenen Randfehler und die Normierungsunsicherheit. Die gespeicherte
Kennzeichnung sagt dies ausdrücklich. Es wird kein Radius nachträglich
subtrahiert, um einen scheinbar engeren Quadraturfehler zu erhalten.

## 3. Einschließende verschachtelte Quadratur

`acb.integral` liefert Integraleinschließungen, sofern der Callback sowohl
den gesamten Eingabeball abdeckt als auch den Analytizitätsvertrag erfüllt
[2]. Für große oder komplexe äußere s-Bälle wird das innere Integral durch
seinen vollständigen Wertebereich auf q∈[0,1] eingeschlossen. Nur für enge
s-Bälle wird zusätzlich innere adaptive Quadratur verwendet. Das vermeidet
eine unerfüllbare innere Genauigkeitsforderung bei breiten äußeren Bällen.

Die Formel ist meromorph in s; ein Ball mit h=0 liefert nichtendliche Werte,
ebenso führen nicht auflösbare Nenner zu nichtendlichen Einschließungen.
Diese werden durch die Quadratur weiter unterteilt oder führen zum Abbruch.
Eine nichtendliche Produktionseinschließung wird nie als Zahl gespeichert.
Die Aufteilung zwischen v₀=−1 und dem Linsenbereich wird am Inneren des
Radialsegments entschieden: Ein nichtpunktförmiger Ball ist nicht beweisbar
kleiner oder gleich sich selbst.

128 und 192 Bit berechnen dieselben 50 Werte separat. Überlappung und der
Vergleich zur früheren Ortsraumquadratur sind Regressionstests; sie ersetzen
weder die Restabschätzung noch den analytischen Callback-Vertrag.

## 4. Eigenständige räumliche Detektorrechnung

Berechnet wird hier ausdrücklich die **skalare** Massenzustands-Gram-Matrix

\[
G_{ij}=\int_D\phi_{m_i}(1,x)\overline{\phi_{m_j}(1,x)}\,d^3x,
\quad m_i\in\{1,2\},\quad
D=\{|x-(0,0,3/2)|<1/2\}.
\]

Dies ist weder die vierkomponentige Dirac-Referenz noch deren normierter
Flavorzustand. Die Null-Anfangsgeschwindigkeit bleibt die skalare
Cauchybedingung; sie wird nicht als Dirac-Anfangsdynamik interpretiert.

Axialsymmetrie reduziert das Detektorvolumen auf R∈[1,2] und
c∈[c_min(R),1], c_min=(R²+2)/(3R). Setzt man
c=1−(1−c_min)(1−u), u∈[0,1], dann gilt

\[
d^3x=\frac{2\pi}3R(R-1)(2-R)\,dR\,du,
\qquad
F(R)=\frac{2\pi}3\left(-\frac{R^4}4+R^3-R^2\right).
\]

Die positive Zellenmasse ist exakt durch
(F(R_hi)−F(R_lo))/8 eingeschlossen. Jede der 648 Raumzellen wird als
**ganzer Wertebereich** ausgewertet, nicht allein in ihrem Mittelpunkt.
Das Quellenintegral benutzt je Teilsegment 128 Radial- und 16 Winkelzellen,
ebenfalls mit vollständigen Intervallbereichen. Das Integral liegt daher
in der Summe aus Zellvolumen mal Zellwertebereich. Ein versteckter
Mittelpunkts-, Auflösungs- oder Quadraturrest bleibt nicht übrig.

Die Kerne K und M werden für τ=2 in Quellenradius umgeschrieben:
μ=(s²−R²−τ²)/(2Rτ), dμ=s ds/(Rτ), s∈[2−R,b]. Für R≤2−b sind ihre
berechneten Kerne null. Das Volumenintegral teilt sich dann in einen vollen
und einen partiellen Quellenbereich. In der partiellen Formel wird
v₀=s/(2R)−(2−R)(2+R)/(2Rs) verwendet, um Auslöschung zu vermindern.

Die resultierenden Intervallradien enthalten sowohl räumliche Variation
innerhalb der Detektorzellen als auch die konservativen Quellenzellbereiche
und Rundung. Diese Anteile werden **nicht** als separat gemessene Fehler
behauptet. Separat gespeichert werden die folgenden analytischen Reste.

### Quellenrand und kleine Detektorspitze

Für diese räumliche Rechnung gilt h_c=1/32. Mit R≤2 und τ=2 werden die
obigen E_K,E_M,E_V gleichmäßig auf dem ganzen Detektor begrenzt; ihre Summe
für Masse m sei e_m. Dieser gröbere Quellenrand hat ein eigenes Budget.

Aus sup e^(−1/h)/h²=4e⁻² für 0<h≤1 folgt

\[
F_0=A/e,\qquad F_1=A(8e^{-2}/a+k/e),
\]
\[
|\phi_m|\le B_m=F_0+\tau F_1+
\frac{m^2\tau^2}2F_0+\frac{m^4\tau a^3}{24}F_0.
\]

Der Fehler im Produkt wird somit durch
B_i e_j+B_j e_i+e_i e_j begrenzt. Multipliziert mit π/6 liefert dies den
separaten Quellenrandfehler des Detektorintegrals.

Die Spitze 2−δ<R<2 mit δ=10⁻⁷ wird ausgelassen. Ihre eingeschlossene
exakte Masse ist π/6 minus die Summe der positiven Zellenmassen; zusätzlich
prüft der Audit V_tip≤2πδ²/3. Ihr Beitrag ist höchstens V_tip B_i B_j.
Die geometrisch verdichteten Radialstreifen verhindern einen unaufgelösten
Nenner am künstlichen Endpunkt R=2. Es gibt keinen unbehandelten Gebietssaum.

### Ergebnisstatus und Grenzen

Die räumlichen Einschließungen sind endlich, bleiben bei 192 Bit stabil,
sind aber für den gesonderten Komponentenradius-Screen 10⁻³ zu breit.
Dieser Screen ist **keine** Umrechnung des E4-Spurabstandsbudgets. Die
Zellbereiche müssen verbessert werden; mehr Rechenpräzision allein beseitigt
die Überabschätzung nicht. Negative untere Anzeigegrenzen werden nicht
still auf null beschnitten, und keine Matrix wird still renormiert.

Acht Vergleiche prüfen, dass diese Quellenradius-Bereiche die scharfen
Punktzertifikate enthalten. Vier exakte Detektormomente (1, z, z², R²)
prüfen Geometrie, positives Maß und Spitzenrest. Ein Fehlertransport zur
Dirac-Detektor-Dichtematrix und deren bedingter Normierung bleibt offen.

## 5. Reproduzierbarkeit

`FREEZE.json` fixiert ausführbaren Code, Protokoll und frühere Eingaben vor
dem Produktionslauf, nach einer ausdrücklich explorativen Vorprüfung.
`SHA256SUMS` umfasst das vollständige neue Paket. Der Verifier prüft auch
unter `python -O`, dass alle 84 Identitäten vollständig sind und die
räumliche Statusentscheidung aus den gespeicherten Radien folgt. CI
wiederholt beide Präzisionen in einem temporären Ausgabeverzeichnis.

Die gesamten Intervalle hängen von korrekter FLINT/Arb-Implementierung und
den beschriebenen analytischen Ableitungen ab. Es wurde kein unabhängiges
externes Review durchgeführt. G1 bleibt HOLD, G2/G3 bleiben NOT_RUN.

## Primärquellen und unveränderte Grundlagen

1. NIST DLMF, [10.14.4](https://dlmf.nist.gov/10.14#E4), ν=2, reelles Argument.
2. [python-flint acb.integral](https://python-flint.readthedocs.io/en/latest/acb.html#flint.acb.integral),
   Analytizitätsvertrag; ausgeführt ist Version 0.8.0 / FLINT 3.3.1.
3. [v0.2: KG-Cauchyformel und unabhängige Ortsraumreferenz](../scale_calibration_v0_2/METHODS.md).
4. [v0.3: Normierung, Kirchhoff-Term und ursprüngliche Restschranken](../certified_budget_v0_3/METHODS.md).
