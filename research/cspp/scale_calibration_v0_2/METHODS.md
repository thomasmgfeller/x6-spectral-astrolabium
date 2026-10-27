# CSPP Skalenkalibrierung v0.2 — Herleitung und Grenzen

Dies ist ein festgelegtes Entwicklungsexperiment nach dem negativen skalaren
Pilot v0.1. Alte Daten, Quellsperren und Freigabeentscheidungen bleiben erhalten.
Die neuen Gaußfelder und die einzelne feste Probe dienen zur Fehlerzerlegung;
sie ersetzen **keinen** Test des ursprünglichen E4-G1-Vertrags.

## 1. Erwartungswert ohne Sprinkling-Rauschen

Wir schreiben q=ερ=ℓk⁻⁴, a=4√q/√6 und
P(z)=1−9z+8z²−4z³/3. Für N~Poisson(ρV) gilt exakt

\[
\mathbb E\!\left[{N\choose k}\epsilon^k(1-\epsilon)^{N-k}\right]
=e^{-qV}\frac{(qV)^k}{k!}.
\]

Die Palm-Erwartung der Summe über die Poisson-Punkte liefert deshalb

\[
\mu_H(\phi)=\mathbb E[B_{\epsilon,C}\phi(0)]
=a\left[-\phi(0)+q\int_{D_H}\phi(y)e^{-qV(y,0)}P(qV(y,0))\,d^4y\right],
\qquad D_H=I((-H,\mathbf0),(0,\mathbf0)).
\]

Das ist die endliche flache Version des bekannten BD-Erwartungswerts [1].
Bei festem ℓk hängt μH von Feld und Rand ab, **nicht von ρ**. Mehr unabhängige
Wolken verkleinern die Unsicherheit des empirischen Mittelwerts; mehr Dichte
bei festem ℓk kann die Fluktuationen verändern. Beide Maßnahmen ändern μH nicht.

Felder sind
φ=exp(−(t²+r²)/(2L²)) exp(i(kz−ωt)) mit
(ωL,kL)=(0,0),(.5,0),(0,.5),(.5,.5).
Am Ursprung: φ=1 und □φ=−2/L²+ω²−k². Alle vier Ziele sind ungleich null;
Fehler werden durch |□φ| geteilt. Damit erzeugt bloßes Verlangsamen des
Feldes keinen trivialen Genauigkeitsgewinn durch einen konstanten Nenner.
Diese Schwartz-Felder sind nicht kompakt getragen. Wir übernehmen daher
keinen Kompaktträger-Konvergenzsatz ungeprüft, sondern kontrollieren ihre
äußeren Integrationsanteile eigens.

### Zweidimensionale Integrationsform

Setze u=−t, v=u+r, s=u−r. Dann 0<s<v<H,
V(y,0)=πs²v²/24, d⁴y=(π/2)(v−s)² ds dv nach Winkelintegration.
Das Winkelmittel des Feldes ist
exp(−(u²+r²)/(2L²)) exp(iωu) sinc(kr).
Mit c=√(πq/24) und y=csv wird der Exponentialkern exp(−y²).
`mean_operator.py` integriert in (v,y), getrennt am Wechsel
v=√(8/c). Gauss-Legendre-Ordnungen 96,192,384 sind vorgegeben.
Eine adaptive Integration in den unabhängigen Koordinaten (u,r) prüft
einen vorher gewählten, nicht zur Ergebnismatrix gehörenden Kontrollfall.

Die Formel für μH ist exakt; ihre Gleitkomma-Quadratur ist es nicht.
Der Unterschied 192→384 ist ein Auflösungsindikator, **keine garantierte
Restfehlerschranke**. Sechs von 189 Parameterpunkten verfehlen die geplante
relative Auflösungsgrenze 10⁻⁶ und bleiben QUADRATURE_HOLD.

### Analytische Abschneidefehler

Wegen |φ|≤exp(−v²/(4L²)), (v−s)²/v≤v und
|P(y²)|≤1+9y²+8y⁴+4y⁶/3 sowie
∫₀∞ exp(−y²)(1+9y²+8y⁴+4y⁶/3)dy=7√π folgt

\[
|\mu_\infty-\mu_H|\le 56\pi qL^2 e^{-H^2/(4L^2)}.
\]

Diese absolute Randabschätzung gilt für alle vier Felder. Für den
zusätzlichen y-Abbruch bei Y=8 folgt entsprechend

\[
|\delta\mu_Y|\le8\sqrt\pi qL^2
\int_Y^\infty e^{-y^2}(1+9y^2+8y^4+4y^6/3)\,dy.
\]

`MEAN.json` speichert gewöhnliche Gleitkomma-Auswertungen dieser analytischen
Schranken. Sie werden nicht als nach außen gerundete Maschinenzertifikate
ausgegeben und ersetzen insbesondere keinen Quadraturfehlernachweis.

## 2. Neue Wolken bei konstantem ℓk

Bekannte Dichte ρ=ν4/(512π/3), ν4=(1024,4096,16384).
Es werden 16 neue unabhängige Poisson-Wolken pro Dichte erzeugt, ohne
Nachziehen oder Auswahl. SeedSequence enthält Phase=1, Szenario=3 und
Master-Seed 202610270602. Die frühere Bestätigungsphase bleibt unbenutzt.

Für die Probe am Ursprung braucht der retardierte Operator ausschließlich
D8, nicht die gesamte umgebende Ω8. D8 hat dasselbe Vierervolumen wie Ω4;
deshalb ist die erwartete simulierte Punktzahl genau ν4. Dies ist eine
exakte Einschränkung auf den kausalen Abhängigkeitsbereich, keine
Unterbeprobung und keine Umdeutung der Dichte. Nach Zeitsortierung wird der
unveränderte Intervallkern von v0.1 verwendet.

Die Teilgebiete D4,D6,D8 entstehen aus derselben Wolke über −t+r<H.
Da sie kausal konvex sind und denselben oberen Endpunkt haben, ändern
zusätzliche äußere Punkte keine Intervallzahl zwischen einem behaltenen
Punkt und der Probe. Das wird auf Kontrollwolken ausdrücklich geprüft.
Alle drei Ränder und ℓk=(1,1.5,2) sind pro Wolke gepaart.
ε=ℓk⁻⁴/ρ liegt in allen Zellen in (0,1].

Für jedes Feld wird die komplexe Identität ausgewertet

\[
B_C\phi-\Box\phi=
(B_C\phi-\mu_H)+(\mu_H-\mu_{64})+(\mu_{64}-\Box\phi).
\]

Die drei Terme diagnostizieren die Sprinkling-Fluktuation, den endlichen
Rand und den verbleibenden Nichtlokalitätsbias. Bei Verwendung numerischer
μ-Werte kommen deren Quadratur- und Abschneideunsicherheiten hinzu.
Die Beträge der drei Terme dürfen sich aufheben; sie sind keine unabhängigen
zufälligen Fehler, deren empirische Beträge einfach quadratisch addiert
werden dürften. Auch Randvergrößerung muss den gesamten Fehler nicht
monoton verbessern. Die Trennung ist eine Identität und eine quantitative
Diagnose, noch kein vollständiges E4-Fehlerzertifikat.

Stichproben-SD verwendet ddof=1. SEM=SD/√16 wird nur deskriptiv berichtet,
ohne Normalverteilungs- oder Überdeckungsgarantie. Kein Potenzgesetzfit,
kein adaptives Stoppen und keine bestätigende Freigabe aus M=16.

## 3. Unabhängige Referenz für dieselbe kompakte Quelle

Die Quelle aus E4/v0.1 bleibt unverändert:
f(x)=A exp(−1/(1−r²/a²)) exp(ik0 z) für r<a,
a=.5, k0=4, ∫|f|²d³x=1, t0=−1 und ∂tφ(t0)=0.
Dies ist die klassische freie KG-Gleichung; daraus werden keine
Teilchendetektionswahrscheinlichkeiten oder Flavorgrößen abgeleitet.

Für τ=|t+1| sei Mr f(x) das Mittel auf der Kugeloberfläche mit Radius r.
Die retardierte KG-Greenfunktion hat den Lichtkegelterm und den inneren
Besselterm. Ableiten der Faltung für Anfangsgeschwindigkeit null ergibt [2–4]

\[
\phi_m(\tau,x)=\frac{d}{d\tau}[\tau M_\tau f(x)]
-\frac{m^2\tau^2}{2}M_\tau f(x)
+m^2\tau\int_0^\tau
 r^2\frac{J_2(m\sqrt{\tau^2-r^2})}{\tau^2-r^2}M_r f(x)\,dr.
\]

Dabei geht J2(ms)/s² für s→0 gegen m²/8. Der negative Oberflächenterm
ist wesentlich; ein bloßes Ableiten des Integranden würde ihn verlieren.
Die Ableitungsidentität für J1(z)/z steht in [3]. Der m=0-Fall ist
Kirchhoffs Formel, mit exakter Huygens-Stütze für die kompakte Quelle.

Der Azimutwinkel kann für den Träger exp(ik0 z) analytisch integriert werden:
bei R=|x|, c=z/R und μ=n·x/R liefert er
exp(ik0(z+rcμ)) J0(k0 r√(1−c²)√(1−μ²)).
Der verbleibende Winkel und das Radialintegral werden durch
Gauss-Legendre-Quadratur mit 64,128,256 Knoten berechnet.
Grenzen werden auf den tatsächlichen Quellensupport eingeschränkt; ein
Wechsel zwischen voller und angeschnittener Kugel wird ausdrücklich geteilt.
R=0, τ=0 und der Besselgrenzwert werden gesondert behandelt.

Geprüft werden die 28 unveränderten Proben von v0.1 und 256 fest ausgewählte
archivierte Abfragekoordinaten. Diese Koordinaten sind Diagnosepunkte,
keine 284 unabhängigen statistischen Realisierungen. Alle komplexen Werte
bleiben gespeichert. Eine Quellenformel wird mit 27 exakt bekannten
KG-Ebenenwellen, Anfangsdaten, Zeitumkehr und Support-Nullkontrollen geprüft.

Unabhängig davon wird die Fourier-Rechnung auf einer Box der Länge 8 für
N=64,128,256 wiederholt. Alle 28 Proben liegen exakt auf Gitterknoten;
die Zeitentwicklung wird direkt zu den vier angefragten Zeiten berechnet.
Es gibt hier keine räumliche oder zeitliche Interpolation. Die Kontinuums-
stütze erreicht im untersuchten Zeitfenster keine periodische Kopie.
Der Vergleich zum alten Verfahren ändert Box, Auflösung und Interpolation
gemeinsam; er isoliert deren einzelne Beiträge nicht.

Auflösungsübereinstimmung der Ortsraumrechnung auf Maschinengenauigkeit
ist kein beweisbarer Restfehler. Auch die unabhängige Fourier-Übereinstimmung
an endlich vielen Proben ist keine globale Normschranke. Sie wird daher
nicht in den E4-Detektor-Trace-Abstand umgedeutet. Der vorab festgelegte
0,1%-Diagnosewert wird nicht erreicht. **REFERENCE_HOLD bleibt bestehen.**

## 4. Status und Folgeentscheidung

Der Pilot verkleinert bei fester Nichtlokalitätsskala nachweisbar in den
gespeicherten Stichproben die SD; er beweist keine allgemeine Varianzrate.
Die Erwartungswertrechnung zeigt, warum das allein den systematischen Bias
nicht beseitigt. Kleine ℓk sind rechnerisch untersuchbar, ohne damit zu
behaupten, dass ein endliches Causal Set bei demselben ℓk schon genau genug ist.
Der Kontinuums-Cauchy-Löser liefert unabhängige Diagnosen. Ein intrinsischer
diskreter Cauchy-Adapter ist damit weiterhin nicht validiert.
G1 bleibt HOLD; Dirac, Flavor und Kohärenz werden nicht ausgeführt.

## Primärquellen

1. Belenchia, Benincasa, Dowker: *The Continuum Limit of a 4-dimensional
   Causal Set Scalar d'Alembertian*, [arXiv:1510.04656v2](https://arxiv.org/html/1510.04656v2),
   Gleichungen (5), (110), (111), Abschnitt IV. Nur Erwartungswert und
   Skalenkonstruktion werden übernommen, keine allgemeine Varianzgarantie.
2. N. Beisert: *Quantum Field Theory I*, ETH Zürich, 2025 HS,
   [Abschnitt 3.5, retardierter KG-Propagator](https://people.phys.ethz.ch/~nbeisert/lectures/QFT1-25HS-Notes.pdf).
3. NIST Digital Library of Mathematical Functions,
   [§10.6.6, Bessel-Ableitungen](https://dlmf.nist.gov/10.6#E6).
4. Y.-Q. Gu: *Green Functions of Relativistic Field Equations*,
   **Version 1 (2006)**, Theorem 1, Gleichungen (3.11)–(3.13),
   [Autoren-Volltext](https://www.researchgate.net/publication/2068528_Green_Functions_of_Relativistic_Field_Equations).
   Die dort angegebene arXiv-Nummer hep-th/0612214 trägt in späteren Versionen
   einen anderen Titel/Inhalt; deshalb wird ausdrücklich die ursprüngliche
   Version genannt. Verwendet wird nur die KG-Integralformel, keine darüber
   hinausgehende Interpretation des Artikels.
