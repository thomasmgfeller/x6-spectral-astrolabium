# Gemeinsame GUM-Auswertung v0.14

Grundlage sind JCGM 100:2008 Abschnitt 8, die Ergänzung Amd.1:2026 sowie
JCGM 102:2011 Abschnitte 6 und 7. Die acht Schritte sind unten vollständig
für den synthetischen Auslesevertrag ausgearbeitet. Ein Ergebnis hängt
weiterhin von der Gültigkeit seiner Eingangsmodelle ab. Es liegt keine
reale 2-ppm-Feldkalibrierung vor.

## 1. Messmodell

Für jeden der drei Einstellungsblöcke werden bei bekanntem Nullmittel
die zweiten Momente s_AA, s_BB und s_AB aus allen n Paaren gebildet.
Drei gemeinsame Kalibriergrößen n_A, n_B und n_C beschreiben die
additiven Rauschvarianzen und die Rauschkovarianz in den erklärten
synthetischen Ausleseeinheiten. Der Eingangsvektor X hat zwölf Komponenten.

Mit a_j = s_AA,j - n_A, b_j = s_BB,j - n_B und
c_j = s_AB,j - n_C ist die Ausgabefunktion

$$
F_j(X)=\rho_j=\frac{c_j}{\sqrt{a_jb_j}},\qquad j=1,2,3.
$$

Die korrigierten zweiten Momente werden zusätzlich als neun linear
transformierte Ausgangsgrößen samt Kovarianz berichtet. Der gemeinsame
Überdeckungsbereich in dieser Studie gilt für den dreidimensionalen
Korrelationsvektor. Die neun Momente und drei daraus berechneten Quotienten
werden nicht als zwölf unabhängige Messgrößen behandelt. Delta_AB hat
keinen gemessenen Eingang und bleibt als UNMEASURED ausgewiesen.

## 2. Eingangsschätzwerte

Jeder Block enthält n = 41045 synthetische Paare. Ihre erzeugenden
Signalvarianzen sind 1, ihre Rauschvarianzen 0.05 und ihre
Rauschkovarianz 0. Es wird keine Stichprobe neu erzeugt, weil ein
Schätzwert weiter vom Nominalwert entfernt liegt. Die vollständigen
Eingangsschätzwerte stehen in records/M0.json und M1.json.

## 3. Standardunsicherheiten und zugeordnete Verteilungen

Für Z_i = (X_i^2,Y_i^2,X_iY_i) wird die Typ-A-Kovarianz der
Mittelwerte als empirische Kovarianz von Z, dividiert durch n, bestimmt.
Die bekannt vorausgesetzten Nullmittel werden nicht aus denselben
Daten erneut geschätzt. Bei unbekannten Nullpunkten müsste das
Messmodell entsprechend erweitert werden.

Die drei Typ-B-Verteilungen sind unabhängig und rechteckförmig:
n_A und n_B liegen in [0.048,0.052], n_C in [-0.001,0.001].
Ihre Standardunsicherheiten sind 0.002/sqrt(3), 0.002/sqrt(3)
und 0.001/sqrt(3). Jeder gezogene Kalibrierwert gilt gemeinsam für
alle drei Einstellungsblöcke. Diese Verteilungen sind deklarierte
synthetische Annahmen, keine Zertifikate eines realen Standards.

Für die neun Typ-A-Eingänge wird eine zentrierte multivariate
Gauß-Näherung im Mahalanobis-Ellipsoid mit Radius 8 abgeschnitten.
Mit d = 9 und

$$
\kappa=\frac{F_{\chi^2_{d+2}}(64)}{F_{\chi^2_d}(64)},
\qquad \Sigma=U_A/\kappa
$$

hat die abgeschnittene Verteilung exakt den zugeordneten Erwartungswert
x_A und die Kovarianz U_A. Dies folgt aus Rotationssymmetrie und
dem abgeschnittenen zweiten radialen Moment der Normalverteilung.
Der entfernte Anteil der zugrunde liegenden Normalverteilung ist
etwa 2.257e-10. Die gewählte Dichte ist eine explizite Approximation
für die Kenntnis über die Mittelwerte, keine Behauptung über deren
exaktes Stichprobengesetz. Ihr kompakter Träger erlaubt eine
deterministische Prüfung, dass nach jeder erlaubten Rauschkorrektur
a_j > 0, b_j > 0 und c_j^2 < a_j b_j gelten. Scheitert diese Prüfung,
bricht die Auswertung mit HOLD_PDF_SUPPORT ab.

## 4. Kovarianzen

Die empirischen zweiten Momente eines Paars sind korreliert. Ihre
vollständigen 3x3-Blöcke werden erhalten. Die drei synthetischen
Versuchsblöcke und ihre Referenzkalibrierung sind im Vertrag unabhängig;
dies begründet die blockdiagonale Eingangskovarianz. Die gemeinsam
verwendeten Referenzen erzeugen nach der Transformation nichtverschwindende
Kovarianzen zwischen den drei Ausgangskorrelationen.

## 5. Ausgangsschätzung

Die erste Auswertung verwendet F(x). Zusätzlich wird der Erwartungswert
E[F(X)] durch gemeinsame Verteilungsfortpflanzung bestimmt. Beide Werte
werden getrennt angegeben, da das Quotientenmodell nichtlinear ist.
Die beobachtete Differenz enthält auch numerischen Monte-Carlo-Fehler;
sie wird nicht vollständig als nachgewiesener Nichtlinearitätsbias gedeutet.

## 6. Fortpflanzung

Die Ableitungen eines Ausgangs nach (s_AA,s_BB,s_AB) sind

$$
(-\rho/(2a),-\rho/(2b),1/\sqrt{ab}).
$$

Die Ableitungen nach (n_A,n_B,n_C) haben das entgegengesetzte Vorzeichen.
Mit dieser 3x12-Matrix J wird nach JCGM 102, Gleichung (3),
U_rho = J U_X J^T berechnet. Eine separate Schleifensumme prüft die
Matrixrechnung; zentrale Differenzen prüfen die Ableitungen.

Die Monte-Carlo-Auswertung folgt JCGM 102 Abschnitt 7.1.7:
Anzahl der Ziehungen wählen; gemeinsam aus der angegebenen Eingangs-PDF
ziehen; F auswerten; die resultierenden Vektoren als Verteilungsdarstellung
verwenden; Erwartungswert und Kovarianz schätzen; einen gemeinsamen
Überdeckungsbereich bilden. Es werden pro Modell eine Million Ziehungen
für Mittelwert/Kovarianz und eine weitere unabhängige Million zur
Bestimmung des Bereichsradius verwendet. Weitere 100000 unabhängige
Ziehungen dienen seiner numerischen Kontrolle.

Die Budgets sind vorab festgelegt. Das ist die Variante nach Abschnitt
7.2.1; es ist keine Implementierung des adaptiven Verfahrens aus 7.8.
Die numerische Streuung der Mittelwerte wird aus zehn Teilblöcken
berichtet, die Quantilunsicherheit durch ein 99-%-Ordnungsstatistikintervall.
Eine vorgegebene numerische Toleranz wird durch die bloße Anzahl der
Ziehungen nicht garantiert.

## 7. Gemeinsamer Überdeckungsbereich

Für den MC-Mittelwert v_MC und die MC-Kovarianz U_MC wird ein Ellipsoid

$$
(\rho-v_{MC})^T U_{MC}^{-1}(\rho-v_{MC})\le q_{0.95}
$$

gebildet. Sein Radius ist das empirische 95-%-Quantil der quadratischen
Abstände aus der zweiten, unabhängigen Ziehungsmenge. Die unabhängige
Kontrollmenge liefert 94995/100000 beziehungsweise 95049/100000 Treffer.
Die 99-%-Binomialintervalle der Kontrollwahrscheinlichkeiten sind
[0.948147,0.951710] und [0.948696,0.952241]. Beide enthalten 0.95.

Das ist eine numerische Überdeckungsprüfung bezüglich der zugeordneten
Eingangs-PDF. Sie beweist keine 95-%-Häufigkeitsüberdeckung für reale
Feldmessungen und keine 1-%-Modellfehlerrate. Letztere kommt separat
aus dem in DERIVATION.md angegebenen Rohdatenmodell und der
Hoeffding-Schranke. Die Auswertung führt diese zwei Bedeutungen nicht
zusammen.

## 8. Berichtete Ergebnisse

| Modell | Abstand | rho = F(x) | Standardunsicherheit erster Ordnung |
|---|---:|---:|---:|
| M0 | 1 | 0.848898 | 0.001881 |
| M0 | 2 | 0.532804 | 0.003843 |
| M0 | 3 | 0.287915 | 0.004828 |
| M1 | 1 | 0.828469 | 0.002018 |
| M1 | 2 | 0.477139 | 0.004078 |
| M1 | 3 | 0.220975 | 0.004997 |

Die MC-Standardunsicherheiten weichen um höchstens rund 0.167 % von
den Werten erster Ordnung ab. Die numerischen Standardfehler der
MC-Mittelwerte liegen zwischen 2.02e-6 und 4.48e-6. Diese Zahlen sind
Numerikdiagnostik und keine erreichte Unsicherheit des Feldmessgeräts.
Die gemeinsame Kalibrierung erzeugt positive Kreuzkovarianzen; die
vollständigen Matrizen und die Bereichsradien stehen in den JSON-Protokollen.

Insbesondere ist die Unsicherheit der Korrelation bei Abstand 3 etwa
0.005 in absoluten dimensionslosen Einheiten. Die 2-ppm-Zielgröße aus
v0.12 beschreibt eine andere Messgröße und wird nicht auf diesen
Kontrollvergleich übertragen. Für die Feldanwendung bleiben Detektortransfer,
Nullpunkte, Zeitabhängigkeit, reale Kalibrierungen und Zustandsnachweis offen.
