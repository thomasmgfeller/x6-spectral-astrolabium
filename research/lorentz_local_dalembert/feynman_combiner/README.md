# Feynman-Kombinator — Gewichtsdiagnose und Fusionsreferenz v0.1

20. Oktober 2026. Basis: `560f717c0e25c957bc58bb9df5ec5ac6ad23cad0`.
**WEIGHT_POLICY_HOLD; HOLD_PHASE3.** Diese Arbeit enthält eine retrospektive
Gewichtsdiagnose und eine synthetische Fusionskontrolle. Kein Sensorversuch,
kein qualifizierter dynamischer Einbettungsfilter und kein Neuheitsnachweis.
„Feynman-Kombinator“ ist ein Projektname; die Implementierung ist klassische
statistische Fusion, kein Feynman-Pfadintegral.

## 1. Die offenen Operatorgewichte

Alle 48 archivierten Wolken der gemeinsamen Stützpunkt-/Rahmensuche bleiben
im Nenner. 17 liefern Stützpunkte (0/16, 1/16, 16/16). Keine neue Auswahl,
keine Simulator-Koordinaten und kein Nachoptimieren der Rahmen.
Die gespeicherten intrinsischen Merkmale z werden durch die gespeicherte
Skala s geteilt. Die neun Momentbedingungen lauten
D a = (0,0,0,-2,2,2,0,0,0), mit Zeilen z_mu, z_mu² und sqrt(2) z_mu z_nu.
B f = sum_i a_i (f_i-f_root)/s². Konstante Felder verschwinden exakt.
Das flache eta wird hier vorausgesetzt; erfüllte Momente sind keine unabhängige
Metrikmessung.

Für die neue adaptive Stützmenge wird eine ausdrücklich neue Vergleichsbasis
gebildet: a_time=-(C+3)s²/tau_i² und a_shell=C s²/(n_side tau_i²),
C=8.379310344827585 aus dem bisherigen Vertrag, tau_i aus den gespeicherten
Root-Intervallzahlen und bekannter Dichte. Das ist eine diagnostische
Übertragung der früheren Regel, kein bereits qualifizierter Operator.
Die Unlösbarkeit bei festen Zeitgewichten gilt genau für diese Übertragung.

| Dichte | Stützmenge | Feste Zeitgewichte lösbar | Freie negative Zeitgewichte lösbar | Ohne Vorzeichenbindung lösbar |
|---:|---:|---:|---:|---:|
| 2048 | 0/16 | 0/16 | 0/16 | 0/16 |
| 8192 | 1/16 | 0/16 | 1/16 | 1/16 |
| 32768 | 16/16 | 1/16 | 12/16 | 16/16 |

„Negativ“ bedeutet im LP nichtpositiv; übrige Gewichte nichtnegativ.
Alle 51 Probleme besitzen geprüfte primal-duale Optimalitäts- oder numerische
Trennzertifikate; kein ungelöster Fall. Bei hoher Dichte erreichen 1/16, 8/16
und 13/16 die diagnostische Massenobergrenze 2 mal Basis. Diese Grenze wird
nur als bereits gebräuchlicher Vergleichswert berichtet, nicht als neue
nachträglich registrierte wissenschaftliche Abnahme.

Die Gewichte minimieren die absolute Koeffizientenmasse, **nicht** die
Rauschvarianz. Für unabhängiges Feldrauschen mit Varianz sigma² ist die
bedingte Ausgangsvarianz sigma² [sum_i a_i² + (sum_i a_i)²]/s⁴.
Der zweite Term ist wesentlich: alle Differenzen teilen denselben Rootwert.
Bei beliebig korreliertem Feldrauschen mit marginalen Varianzen <=sigma²
liefert die quadrierte volle L1-Masse eine obere Schranke. Beides konditioniert
auf feste Gewichte; Rekonstruktions-, Auswahl-, Dichte- und Geometriefehler
sind darin NICHT enthalten.

Bei hoher Dichte beträgt das Verhältnis der IID-Feldrauschverstärkung zur
Basis für freie negative Zeitgewichte 1.26–93.12, ohne Vorzeichenbindung
1.26–12.14. Das sind Werte der gefundenen L1-Optima, keine unteren Schranken
für jede zulässige Gewichtung. Ein varianzoptimierendes QP kann andere
Gewichte finden. Die Halbierungsantworten sind Sensitivitätsdiagnostik,
keine unabhängigen Stichproben oder kalibrierte Fehlerkovarianz.

**Folgerung:** Rang neun allein reicht nicht. Die feste Zeitregel wird auf
15/16 hochdichten gespeicherten Designs durch Trennzertifikate ausgeschlossen.
Das schliesst andere Stützmengen, weichere Momentbedingungen oder andere
Gewichtsregeln nicht aus. Freie Gewichte benötigen noch eine begründete
Rauschgrenze und eine frische Ableitungsprüfung.

## 2. Kombinator und Kalman-Schnittstelle

Operatorgewichte a_i und Fusionsgewichte w_j sind verschiedene Grössen.
Rekonstruktionen müssen dieselben Ereignisse, Skala, Zeitrichtung und einen
festgelegten gemeinsamen Koordinatenrahmen verwenden. Lorentz-/Translations-
Freiheiten dürfen nicht als Messstreuung behandelt werden. Eine aus Daten
bestimmte Ausrichtung trägt ihrerseits Unsicherheit bei.

Für gestapelte Rekonstruktionen z, A=[w_1 I ... w_m I], sum w_j=1:
z_comb=A z, R_comb=A R_joint A^T. R_joint enthält alle Kreuzkovarianzen.
Die Streuung mehrerer Rekonstruktionen EINER Wolke schätzt gemeinsame Fehler
nicht zuverlässig. Vollständige Duplikate dürfen die Unsicherheit nicht senken.
Unbekannte Kreuzkovarianz wird nicht stillschweigend auf null gesetzt.
Covariance Intersection ist eine mögliche konservative Alternative, wenn
bereits belastbare marginale Fehlergrenzen vorliegen; sie repariert keine
unbekannten systematischen Verzerrungen.

Prädiktion x_minus und P_minus benötigen ein eigenes Dynamikmodell F,Q.
Flache Lorentz-Geometrie allein liefert keine Bewegungsgleichung für die
Landmarken. Beobachtungsindex k ist keine fundamentale Wachstumszeit.

Die Referenz `fusion.update` verlangt C=Cov(x_true-x_minus, v) ausdrücklich:
S=H P H^T+R+H C+C^T H^T,
K=(P H^T+C) S^-1,
x_plus=x_minus+K(z-H x_minus),
P_plus=P-(P H^T+C) S^-1 (H P+C^T).
Bei C=0 ergibt sich die gewöhnliche Kalman-Korrektur. Wiederverwendete alte
Frames können C ungleich null erzeugen. Zeitliche Messkorrelation verlangt
zusätzlich ein Zustandsmodell oder eine gemeinsame Batch-Auswertung.

Die API behält Prädiktion, kombinierte Messung, Innovation, Gain und Posterior
getrennt. Kovarianzen müssen positiv semidefinit sein. Singuläre Inversionen
werden abgewiesen; kein stilles diagonales Zusatzrauschen. Die mitgelieferte
BLUE-Gewichtswahl ist nur für skalare Kanäle implementiert.

## 3. Ausgeführte synthetische Kontrolle

2000 Kalibrierdraws, 20000 getrennte Testdraws, Seeds 2026102001/2026102002.
Drei skalare Rekonstruktionen teilen Rauschen mit Varianz 0.9 und besitzen
je zusätzliche unabhängige Varianz 0.1. Unabhängige Prädiktionsvarianz 1.
Gleiche Daten für alle vier Arme, keine Testdatenanpassung. Ein Schritt,
wahre Zielgrösse null, keine dynamische oder kausale Rekonstruktion.

| Variante | Posterior-RMSE | Abdeckung nomineller 95%-Intervalle |
|---|---:|---:|
| Einzelmessung + Kalman | 0.7036 | 95.07% |
| Fusion mit fälschlicher Unabhängigkeit + Kalman | 0.7666 | 80.00% |
| Kalibrierte gemeinsame Kovarianz + Kalman | 0.6928 | 95.06% |
| Gleiche Gewichte, konservative Varianz 1 + Kalman | 0.6933 | 95.42% |

Das zeigt den vorgesehenen Fehlerfall der Doppelzählung. Die Stichprobe
belegt keine allgemeine Überlegenheit oder garantierte Abdeckung. Die
konservative Varianz 1 folgt hier aus den bekannten marginalen Varianzen;
sie ist keine allgemein gelöste Kovarianzschätzung für Kausalsets.
Fünf gezielte Softwarekontrollen bestehen: Duplikate, korrelierte Kalman-
Korrektur, ungültige Kovarianz, Kausalverletzung und skalare BLUE-Normierung.

## 4. Kontrollierter Folgeversuch — vor einer Durchführung zu fixieren

1. Zunächst ein QP für gemeinsame Moment-/Varianzoptimierung auf separaten
   Entwicklungswolken prüfen. Verfügbarkeit, volle Koeffizientenmasse,
   Root-Rauschen, Auswahlstabilität und tatsächliche Auflösung protokollieren.
   Operatorprüfung auf unabhängigen glatten Feldern und frischen Wolken;
   angepasste Momente niemals als Validierungsfelder zählen.
2. Für mehrere Rekonstruktionen eine feste Ereigniszuordnung und
   Koordinateneichung definieren. Jede Messung erhält Rohdaten-IDs,
   Rekonstruktions-ID, Aufnahmezeit, Verfügbarkeitszeit und Modellversion.
   Alle Rekonstruktionen einer physischen Wolke bleiben in derselben
   Kalibrier-/Testgruppe. Überlappende Fenster bleiben im selben Sequenzblock.
3. R_joint aus Fehlern gegenüber bekannter Simulationswahrheit auf separaten
   physischen Wolken/Sequenzen kalibrieren. Gemeinsamen Bias gesondert messen;
   bei Realdaten braucht es eine unabhängige Referenz. Zwei Einfärbungen
   derselben Wolke ersetzen diese Kalibrierung nicht.
4. Vergleichen: ungefilterte Einzelrekonstruktion, Kombinator allein,
   Einzelrekonstruktion+Kalman, Kombinator+Kalman und konservative Fusion.
   Naive Unabhängigkeitsfusion bleibt Negativkontrolle. Identische Rohdaten,
   Verzögerung und Budgets; keine nachträgliche Kovarianzvergrösserung auf Tests.
5. Störungen: gemeinsame Fehler, vollständige Duplikate, überlappende Fenster,
   Ausfälle, Dichtemissspezifikation, Drift und Modellwechsel. Metriken:
   RMSE/Bias, 95%-Abdeckung, NIS/NEES, Innovationsautokorrelation, kausale
   Fehlrelationen, Verfügbarkeit, Laufzeit und Latenz. Unsicherheiten auf
   Sequenzebene berechnen; Ausfälle bleiben im Nenner.
6. Kausalität hat zwei getrennte Prüfungen: (a) gerichtete Relationen und
   Lichtkegelverträglichkeit vor/nach Fusion/Korrektur, (b) kein Zugriff auf
   zum Ausgabezeitpunkt noch nicht verfügbare Daten. Bestehende Stützen mit
   Vergangenheit UND Zukunft sind eine Offline-Rekonstruktion. Online ist
   eine deklarierte Verzögerung oder eine neu validierte retardierte Auswahl
   nötig. `causal_check` prüft nur (a), keine Online-Zulässigkeit.
7. Fehlende Kalibrierung, unaufgelöste Datenüberlappung oder Kausalverletzung:
   keine Messfreigabe. Eine reine Prädiktion wird als solche ausgewiesen.
   Keine lautlose Projektion auf den Lichtkegel und kein Wegfiltern von
   Innovationswarnungen. Modellabweichung kann Rauschen, Drift oder falsches
   Modell bedeuten; sie ist kein Krümmungsnachweis.

Der Folgeversuch ist noch nicht ausgeführt. Numerische Abnahmeschwellen,
Dynamikmodell, frische Seeds und Budget werden nach der Entwicklungsphase
und vor den Zieldaten eingefroren. Keine Aussage über 3+1 oder Krümmung.

## Reproduktion und Quellen

Vom Repository-Root, mit NumPy und SciPy:

```sh
OPENBLAS_NUM_THREADS=1 python research/lorentz_local_dalembert/feynman_combiner/audit_weights.py
OPENBLAS_NUM_THREADS=1 python research/lorentz_local_dalembert/feynman_combiner/test_fusion.py
```

`weight_audit.json` enthält Input-SHA256, Designs, Basen, Gewichte,
Primal-/Dualzeugen und alle Nenner; `synthetic_results.json` die Fusionswerte.
Der Audit nutzt den bestehenden LP-Löser samt separaten Zertifikatprüfungen.
Die importierten LP- und Designfunktionen sind durch den Basiscommit gebunden.

- [Vorherige gemeinsame Machbarkeit](../joint_feasibility/RESULTS.md)
- [Welch & Bishop, Kalman-Einführung](https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf)
- [Split Covariance Intersection with Correlated Components](https://arxiv.org/abs/2403.03543)

Die Fusionsformeln sind bekannte Schätztheorie. Der mögliche Forschungsbeitrag
liegt in der geprüften kausalen Rekonstruktion samt Fehlerkalibrierung und
Datenprovenienz; dieser Nachweis steht noch aus.

## Fortsetzung: Varianzoptimierung und unabhängiger Pilot

Die nächste Stufe ist im [Kalibrierprotokoll](CALIBRATION_PROTOCOL.md) und im
[Vertrag](calibration_contract.json) vor den neuen Wolken festgelegt.
Öffentlicher Freeze: `315d7c31507a852edc84b9e52dece561c81c72b3`.
Die retrospektive QP-Entwicklung liefert 30 geprüfte Lösungen. Bei hoher
Dichte reduziert das unbeschränkte QP die bedingte IID-Feldrauschvarianz
auf 0.298–0.838 der bisherigen L1-Lösung; die 12/16 vorzeichenbeschränkten
Machbarkeitsfälle bleiben 12/16. Neue physische Kalibrier-/Testwolken
prüfen zusätzlich die tatsächliche geometrische Fehlerstreuung.
Die Bias-Korrektur ist spezifisch für die deklarierte Testfeld-Verteilung;
Übertragung auf andere Felder, Dichten oder Sensoren ist nicht nachgewiesen.

Die Bootstrap-Vergleiche des Piloten konditionieren auf die eingefrorene
Kalibrierung. Sie erfassen deren Schätzunsicherheit nicht vollständig.
Auch der Faktor (1+1/n) für die geschätzte Bias-Korrektur macht aus der
empirischen Kovarianz keine garantierte Fehlergrenze.

Abgeschlossen: [Ergebnisbericht des unabhängigen Piloten](CALIBRATION_RESULTS.md).
31/32 Kalibrier- und 30/32 Testwolken liefern bewachte Antworten. Der
zusätzliche Posterior-RMSE-Gewinn durch Fusion beträgt nur 0.54% statt der
verlangten 5%; `CALIBRATION_HOLD`. Die Relationsdiagnose zeigt weitere
Grenzen der Einbettung. Rohdaten, Fehlerkovarianz und Zertifikate sind archiviert.

Fortsetzung: [Getrennte wolkenbedingte Feldrauschkovarianz und Relationskorrektur](../conditional_geometry/RESULTS.md). 32 frische Testwolken, 30 vollständig auswertbar; Fehlrelationen in 28/30 → 0/30 akzeptierten Rekonstruktionen. Rauschbedingter Filtergewinn nur 1,82%, zusätzliche Fusion ohne Nutzen: `CONDITIONAL_HOLD; HOLD_PHASE3`.
