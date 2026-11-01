# KVF-Kontrollvergleich v0.14: Modelle, Schranken und Identifizierbarkeit

Die Ergebnisse gelten für den eingefrorenen Kontrollvertrag in CONTRACT.json.
Beide Modelle haben dieselbe flache 3+1-dimensionale Minkowski-Geometrie.
M0 ist ein freies masseloses Skalarfeld im Vakuum; M1 ein freies massives
Skalarfeld mit m ell0 = 1/2. Dies ist ein methodischer Positivkontrollvergleich.
Er prüft weder eine alternative Gravitationstheorie noch eine Photonmasse.
Natürliche Einheiten hbar = c = 1 werden verwendet; m ist eine inverse Länge.
Eine physikalische Referenzlänge ell0 ist für einen Labortransfer noch offen.

## 1. Gemeinsame Feld- und Detektorbeschreibung

Wir verwenden den Standard-Vakuumkern eines freien reellen Skalarfeldes

$$
W_m(x,y)=\int\frac{d^3k}{(2\pi)^3\,2\omega_k}
e^{-i\omega_k(t_x-t_y)+i\mathbf k\cdot(\mathbf x-\mathbf y)},
\quad \omega_k=\sqrt{k^2+m^2}.
$$

Die beiden Feldobservablen sind mit normierten reellen Gaußfunktionen
gemittelt. Die räumliche Standardabweichung je Achse ist sigma, die zeitliche
Standardabweichung tau; beide Zeitmittelpunkte sind gleich. Mit
ell^2 = sigma^2 + tau^2 und eta = tau/ell = 1/2 ergibt sich

$$
H_m(r)=\frac{e^{-m^2\tau^2}}{4\pi^2\ell^2} I(m\ell,r/\ell),
\quad
I(\mu,R)=\int_0^\infty\frac{q^2 e^{-q^2}}{\sqrt{q^2+\mu^2}}
\operatorname{sinc}(qR)\,dq.
$$

H_AA = H_BB = H_m(0), H_AB = H_m(r). Der Imaginärteil des gemittelten
Wightman-Kerns verschwindet bei diesen gleichen Zeitmittelpunkten durch
Symmetrie. Deshalb ist Delta_AB = 0 in beiden Modellen. Er wurde in dieser
Studie nicht gemessen. Gaußfunktionen besitzen unbeschränkte Träger;
die Null ist hier kein experimenteller Nachweis raumartig getrennter
Wechselwirkungsgebiete oder einer gemessenen Mikrokausalität.

Die positiven räumlichen Abstände sind r/ell0 = 1, 2, 3. Die dimensionslose
effektive Breite w = ell/ell0 darf im Entscheidungsmodell in [0.98,1.02]
liegen. Die normierte Feldkorrelation ist

$$
\rho_m(R_0,w)=\frac{I(m\ell_0 w,R_0/w)}{I(m\ell_0 w,0)}.
$$

Konstante positive Kanalverstärkungen heben sich in der normierten
Korrelation auf. Die drei nominalen Werte sind

| r/ell0 | M0 | M1 | Differenz M0 minus M1 |
|---:|---:|---:|---:|
| 1 | 0.8488727670 | 0.8279893544 | 0.0208834126 |
| 2 | 0.5380795069 | 0.4802392358 | 0.0578402712 |
| 3 | 0.2854993807 | 0.2099823638 | 0.0755170169 |

Die in records/M0.json und M1.json angegebenen `scaled_physical_kvf` sind
4 pi^2 ell0^2 mal (H_AA,H_BB,H_AB,Delta_AB). Die simulierten Auslesedaten
werden dagegen je Modell in Einheiten mit Signalvarianz 1 erzeugt. Das
entspricht einer zugelassenen Verstärkungsanpassung und verhindert, dass
eine unbekannte absolute Amplitude als Modellseparator benutzt wird.

## 2. Positive Integralform und unabhängige Rechenwege

Die Laplace-Darstellung von 1/sqrt(q^2+mu^2), gefolgt vom Gaußintegral
über den Impuls und der Substitution z = sqrt(s/(1+s)), liefert

$$
I(\mu,R)=\frac12\int_0^1
\exp\left[-\frac{\mu^2 z^2}{1-z^2}-\frac{R^2(1-z^2)}4\right]dz.
$$

Die Umordnung der Integrale ist durch absolute Integrierbarkeit gedeckt:
der Betrag der sinc-Funktion ist höchstens 1 und das entsprechende
Integral für R = 0 ist endlich. Die positive Form vermeidet die
Auslöschung oszillierender Impulsbeiträge. Für mu = 0 gilt außerdem

$$
I(0,0)=\frac12,\qquad \rho_0(R,1)=\frac{2\,\operatorname{Dawson}(R/2)}R,
$$

mit stetiger Fortsetzung 1 bei R = 0. `check.py` vergleicht den
Impulsintegralweg mit der positiven Form an 24 Punkten und den masselosen
Grenzfall an sechs Punkten mit der geschlossenen Formel.

### Einschluss ohne Vertrauen auf die Quad-Fehlerschätzung

Für g(z) als Integrand ohne Faktor 1/2 ist 0 <= g <= 1. Seine logarithmische
Ableitung lautet

$$
\frac{g'(z)}{g(z)}=z\left(\frac{R^2}2-
\frac{2\mu^2}{(1-z^2)^2}\right).
$$

Sie wechselt höchstens einmal von positiv zu negativ. Daher hat g totale
Variation höchstens 2, bei mu = 0 oder R = 0 höchstens 1. Für das
zusammengesetzte Mittelpunktverfahren auf L gleich großen Zellen folgt
aus der Variation auf jeder Zelle

$$
\left|I-\frac1{2L}\sum_{j=0}^{L-1}g((j+1/2)/L)\right|
\le \frac{\operatorname{TV}(g)}{2L}.
$$

`certificate.py` verwendet L = 32768, exakte rationale Exponenten an den
Stützstellen und gerichtete Decimal-Rechnung mit 42 Stellen. Die korrekt
gerundete Decimal-Exponentialfunktion wird durch ihre benachbarten
darstellbaren Werte eingeschlossen. Der analytische Quadraturrest wird
anschließend nach außen addiert. Die SciPy-Ergebnisse sind eine separate
Gegenrechnung; die garantierten Bereiche in certificate.json kommen aus
diesem Variationsargument und der gerichteten Rechnung. Übliche korrekte
Implementierung der Python-Decimal-Operationen wird vorausgesetzt.

## 3. Kontinuierliche Breitenunsicherheit

In der positiven Darstellung ist rho der Erwartungswert von
exp[-R^2(1-z^2)/4] unter einer Dichte proportional zu
exp[-mu^2 z^2/(1-z^2)]. Bei wachsendem R fällt der Integrand punktweise.
Bei wachsendem mu verschiebt der monotone Likelihood-Quotient das Gewicht
zu kleineren z; der auszuwertende Integrand steigt mit z. Daher fällt rho
separat mit mu und mit R. Dieses Argument gilt auch für den masselosen
Grenzfall durch monotone Konvergenz.

Mit a = 0.98 und b = 1.02 enthält folglich das Rechteck

$$
[\rho(m\ell_0 b,R_0/a),\ \rho(m\ell_0 a,R_0/b)]
$$

alle tatsächlichen Werte für w in [a,b]. Dieser Einschluss lässt die
Abhängigkeit beider Argumente von w außer Acht und ist deshalb
konservativ. Die zusätzliche Prüfung von 101 Breiten je Modell und
Abstand ersetzt den analytischen Einschluss nicht.

## 4. Rohdatengesetz und Kalibrierannahmen

Für jeden Versuch werden beide normierten Feldobservablen gemeinsam
ausgelesen. Im Idealmodell kommutieren sie und haben im freien
Gauß-Vakuum eine zentrierte gemeinsame Gaußverteilung. Wir addieren
unabhängig vom Feld ein zentriertes gaußförmiges Detektorrauschen.
Zwischen den Versuchen und zwischen den drei Einstellungsblöcken wird
Unabhängigkeit vorausgesetzt. Es gibt keine nachträgliche Ereignisauswahl.

Die Rauschvarianzen relativ zur jeweiligen Signalvarianz heißen alpha_A,
alpha_B; die Rauschkovarianz relativ zum geometrischen Mittel der
Signalvarianzen heißt beta. Dann ist die beobachtete Rohkorrelation

$$
\theta=\frac{\rho+\beta}{\sqrt{(1+\alpha_A)(1+\alpha_B)}}.
$$

Der eingefrorene Vertrag setzt harte Grenzen
alpha_A, alpha_B in [0.048,0.052] und beta in [-0.001,0.001] voraus.
Diese Werte sind Designannahmen, keine Messbelege. Innerhalb der Box ist
die Rauschkovarianzmatrix positiv definit. Zusätzlich gelten im
Kontrollmodell exakt bekannte Nullpunkte und Abstände, konstante positive
Gains und der spezifizierte Vakuumzustand. Für ein Labor fehlen hierfür
Nachweise; insbesondere sind Nullpunktfehler und zeitliche Abhängigkeit
noch kein Teil einer freigegebenen Gesamtbilanz.

Für positive rho erhält man den konservativen Bereich

$$
\theta\in[(\rho_{\min}-0.001)/1.052,
          (\rho_{\max}+0.001)/1.048].
$$

## 5. Einfache Entscheidung mit endlicher Fehlerschranke

Für zwei zentrierte gemeinsam gaußverteilte Größen gilt

$$
p=P(\operatorname{sgn}X=\operatorname{sgn}Y)
=\frac12+\frac{\arcsin\theta}{\pi}.
$$

Ein kurzer Beweis schreibt X = U und
Y = theta U + sqrt(1-theta^2) V für unabhängige Standardnormalvariablen.
Der Winkel von (U,V) ist gleichverteilt. Der Winkelanteil mit verschiedenen
Vorzeichen beträgt arccos(theta)/pi. Das Komplement liefert die Formel.
Sie ist hier eine Eigenschaft des ausdrücklich angenommenen
Gauß-Rohdatengesetzes; Zentrierung allein genügt dafür nicht.

Nach außen gerundete Reihen für arcsin und die Machin-Formel für pi liefern
bei R0 = 3 die konservativen Grenzen

$$
p(M0)\ge a=0.58358,\qquad p(M1)\le b=0.56860.
$$

R0 = 3 wurde vor den synthetischen Daten anhand der größten garantierten
Lücke unter den drei festgelegten Abständen gewählt. Sei S die Zahl
gleicher Vorzeichen aus n unabhängigen Versuchen. Mit

$$
n=\left\lceil\frac{2\log100}{(a-b)^2}\right\rceil=41045,
\qquad k=\lfloor n(a+b)/2\rfloor=23645
$$

lautet die Regel: S > k wählt M0, sonst M1. Hoeffdings Ungleichung gibt

$$
P_{M0}(S\le k)\le e^{-2n(a-k/n)^2}<0.009817,
$$

$$
P_{M1}(S>k)\le e^{-2n((k+1)/n-b)^2}<0.009885.
$$

Die Schranken gelten gleichmäßig über die angesetzte Breiten- und
Rauschbox, bedingt auf das gesamte Rohdatenmodell. n ist ein hinreichendes
Budget dieser Regel, kein bewiesenes Minimum. Die Entscheidung verwendet
nur R0 = 3; für den dreikomponentigen GUM-Vergleich werden je Modell drei
Blöcke gleicher Größe verwendet, insgesamt 123135 Paare.

Die zwei Modellfälle sind alternative Wahrheiten. Die zwei Fehlergrenzen
werden nicht addiert, um ein angebliches zusätzliches 2-%-Ereignis unter
einer einzelnen Wahrheit zu erzeugen. Außerhalb beider Modellfamilien
ist diese erzwungene Zweifachentscheidung kein Gültigkeitstest. Ein
realer unbekannter Zustand braucht eine eigene Prüfung auf
Modellabweichung und darf nicht allein durch diese Regel freigegeben werden.

Die exakten Binomialschwänze an den konservativen Endpunkten sind numerisch
etwa 0.104538 % und 0.108949 %. Eine Decimal-Rekursion mit 50 und 70 Stellen
prüft diese Werte unabhängig von SciPy. Die formale Fehlerschranke bleibt
die oben angegebene Hoeffding-Grenze.

## 6. Frische synthetische Kontrollen

development/FREEZE_PRE_RUN.sha256 fixiert Vertrag, Kernprogramme und
Zertifikat vor der Erzeugung der Rohdaten, der GUM-Monte-Carlo-Ziehungen
und der Endpunktkampagne. Alle Seeds sind dokumentiert. Bei der
anschließenden Arithmetikprüfung wurde die Rundungsrichtung eines
Nenners im arcsin-Rest explizit korrigiert. Vertrag, Wahrscheinlichkeitsgrenzen,
Budget, Entscheidung und Rohdaten wurden dadurch nicht geändert; es gab
keine neue Datenauswahl. development/REVIEW.json und die archivierte
Vorversion dokumentieren dies. FREEZE.sha256 fixiert den abschließenden
Stand für die Reproduktion.

- M0: 24229 gleiche Vorzeichen aus 41045, Entscheidung M0.
- M1: 23233 gleiche Vorzeichen aus 41045, Entscheidung M1.
- Endpunktkampagne: jeweils 20000 unabhängige synthetische Binomialläufe;
  18 falsche M1-Entscheidungen unter M0, 23 falsche M0-Entscheidungen unter M1.
- Die 99-%-Clopper-Pearson-Intervalle für die beobachteten Fehlerraten sind
  [0.04473 %,0.16040 %] beziehungsweise [0.06262 %,0.19235 %].

Die Kampagne illustriert die analytische Aussage. Sie ersetzt weder ihren
Beweis noch eine experimentelle Prüfung der Eingangsannahmen. Die
Rohdaten sind vollständig in raw/ enthalten; die GUM-Auswertung nutzt
dieselben Daten, weshalb ihre Ergebnisse keine unabhängigen
Bestätigungen der Vorzeichenentscheidung sind.

## 7. Explizite Nichtidentifizierbarkeit bei unkontrolliertem Rauschen

Bei jedem Abstand r sei d_r = rho_0(r)-rho_1(r). Wähle als Rauschmatrizen

$$
N_0=\begin{pmatrix}0.1&0\\0&0.1\end{pmatrix},\qquad
N_1(r)=\begin{pmatrix}0.1&d_r\\d_r&0.1\end{pmatrix}.
$$

Alle drei N1 sind positiv definit; ihr kleinster Eigenwert ist mindestens
0.02448298. Beide Modelle erzeugen dann exakt dieselben beobachteten
Kovarianzmatrizen mit Diagonalen 1.1 und Kreuzterm rho_0(r). Da die
Rohdatengesetze zentriert gaußförmig sind, stimmen ihre gesamten
Beobachtungsverteilungen überein. Das gilt auch für alle drei Blöcke
gemeinsam, wenn die Blöcke unabhängig sind.

Dieser Alias verwendet einstellungsabhängiges Rauschen außerhalb der
festgelegten Kalibrierbox. Er zeigt, weshalb unabhängig begrenztes
korreliertes Detektorrauschen für die Interpretation nötig ist. Unter
gleichen Priorwahrscheinlichkeiten kann bei identischen Gesetzen kein
Verfahren eine mittlere korrekte Entscheidung über 1/2 garantieren,
unabhängig von der Zahl der Versuche.

Außerdem kann allein bei R0 = 3 ein masseloses Modell mit
w = 0.8656043504 die nominale massive Korrelation nachbilden. Dieser
Wert liegt außerhalb [0.98,1.02] und ist ein weiterer Hinweis auf die
Bedeutung der Breitenkalibrierung; er ist kein Alias des vollständigen
Drei-Abstands-Vektors.

## 8. Konsequenz für den Teststand

Die Korrelationskomponenten des KVF besitzen unter dem festgelegten
Kontrollmodell einen nachgewiesenen Separator und ein endliches Budget.
Ein Antwortkanal, ein Quantennachweis gegenüber klassischen
Korrelationsmodellen, reale Feldkalibrierung und eine Übersetzung zu
einem Quantengravitationsmodell stehen weiterhin aus. Eine klassische
Gaußsimulation kann die hier verwendeten Korrelationsdaten reproduzieren.
Der Befund ist daher eine Qualifikation des Kontrollverfahrens im Modell.
