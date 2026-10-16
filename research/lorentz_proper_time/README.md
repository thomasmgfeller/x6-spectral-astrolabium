# Normierte Eigenzeit aus einer markierten kausalen Ordnung

**Status: Erster Ziel-Datenlauf und interne Gegenprüfung abgeschlossen.**
Anschluss an [PR #41](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/41).
Der unveränderte [Vertrag](contract.json) aus
[PR #42](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/42)
wurde mit 6.912 Ordnungen ausgeführt. Die Intervallreferenz erfüllt die
vorab festgelegten Hauptkriterien im bekannten flachen 1+1-Modell:
RMSE 0,031614 bei m=256, gegenüber 0,177785 für die Dichte-/Höhenregression.
Die größte exakt abgeglichene Zusatzkontrolle bleibt mit 63 statt 128 Paaren
ohne Leistungsbewertung. [Ergebnisse, Grenzen und Reproduktion](RESULTS.md)
trennen diese beiden Befunde. Die folgenden Abschnitte erläutern weiterhin
die Zieldefinition und den ursprünglichen Versuchsplan.

## 1. Die konkrete geometrische Frage

Wie genau lässt sich die zeitartige Distanz zwischen zwei **markierten**
Ereignissen aus der endlichen gerichteten Ordnung statistisch schätzen?

Das bekannte Referenzmodell ist ein flacher 1+1-dimensionaler
Minkowski-Diamant. In dimensionslosen Nullkoordinaten u,v in (0,1) setzen wir

\[
t=T(u+v)/2,\qquad x=T(u-v)/2,\qquad c=1.
\]

Die äußeren, nicht mitgezogenen Diamantspitzen haben Eigenzeitabstand T.
Für markierte Punkte p,q mit u_p<u_q und v_p<v_q ist die Zielgröße

\[
\theta(p,q)=\tau(p,q)/T
          =\sqrt{(u_q-u_p)(v_q-v_p)},\qquad 0<\theta<1.
\]

Die Raumzeitfläche des ganzen Diamanten ist T²/2. Die Fläche des
Intervalls zwischen p und q ist T² theta²/2. Ihr Verhältnis ist a=theta².
T und d=2 sind Modellvorgaben. Der Versuch rekonstruiert weder die Dimension
noch eine absolute Zeiteinheit aus der Ordnung.

Das Verfahren erhält die Relationsmatrix, die beiden markierten Knoten und
N. Koordinaten und wahre Eigenzeiten liegen ausschließlich beim Erzeuger und
Auswerter; sie sind keine Eingaben des Schätzers. Eine Schnittstelle muss
zusätzliche, unerlaubte Felder zurückweisen. Die Markierungen sind beim
Umnummerieren mitzuführen.

## 2. Zwei Identifizierbarkeitsgrenzen

**Absolute Skala.** Gemeinsame Skalierung aller physikalischen Koordinaten
und T mit s>0 erhält die Ordnung und theta, verändert aber tau um den Faktor s.
Ohne externe Skala kann die endliche Ordnung keine absolute Zeit liefern.

**Auch theta ist bei endlichem N nicht exakt bestimmt.** Betrachte im selben
Einheitsdiamanten die vier Punkte (1/10,1/10), (2/10,2/10), (3/10,3/10) und
entweder (4/10,4/10) oder (8/10,8/10), mit dem ersten und letzten Punkt markiert.
Beide Einbettungen ergeben dieselbe vollständige Viererkette:

| Größe | Einbettung A | Einbettung B |
| --- | ---: | ---: |
| N | 4 | 4 |
| Strikte Relationen R | 6 | 6 |
| Globale Höhe H, in Knoten | 4 | 4 |
| Strikte Intervallpunktzahl K | 2 | 2 |
| Innere längste Kette ell, in Knoten | 2 | 2 |
| theta | 3/10 | 7/10 |

Das ist ein deterministisches Gegenbeispiel gegen exakte punktweise
Identifizierbarkeit, kein Zufallsexperiment und keine typische Fehlerrate.
Selbst Kenntnis der ganzen Ordnung behebt diese endliche Mehrdeutigkeit nicht.
Das Forschungsziel ist daher eine kalibrierte statistische Genauigkeit unter
genannten Annahmen. Die Beispielpunkte und Sollwerte stehen in
[design_examples.json](design_examples.json).

## 3. Referenzschätzer und exakte Modellrechnung

Zuerst werden die beiden Endpunkte unabhängig gleichverteilt gezogen und nur
auf p<<q konditioniert. **Erst danach** werden m=N−2 Hintergrundpunkte
unabhängig gleichverteilt im gesamten Diamanten erzeugt. Ein Paar wird nicht
nach Sichtung der Hintergrundordnung oder seines Intervallinhalts gewählt.
Jede neue Ordnung liefert genau ein markiertes Paar.

Sei K die Zahl der Punkte im strikten Intervall p<z<q; beide Endpunkte sind
ausgeschlossen. Bedingt auf die Endpunkte liegt jeder der m Hintergrundpunkte
mit Wahrscheinlichkeit a=theta² im Intervall. Deshalb gilt im idealen
kontinuierlichen Gleichverteilungsmodell vor weiterer Auswahl

\[
K\mid p,q\sim\operatorname{Binomial}(m,a),\quad
\widehat a=K/m,\quad E[\widehat a\mid p,q]=a,\quad
\operatorname{Var}(\widehat a\mid p,q)=a(1-a)/m.
\]

Die geometrische Referenz ist V: theta_hat=sqrt(K/m). Sie ist endlich **nicht**
erwartungstreu: wegen der Konkavität der Wurzel gilt
E[theta_hat|p,q]<=theta. Auch K=0 bleibt im Datensatz.

Unter der gewählten Endpunktverteilung sind Delta u und Delta v unabhängig
mit Dichte 2(1−z) auf (0,1). Daraus folgen
E[a]=1/9, E[a²]=1/36, E[theta]=64/225 und

\[
E[(\widehat a-a)^2]=1/(12m).
\]

Diese exakten Aussagen betreffen a und das unselektierte kontinuierliche
Referenzmodell. Sie sind keine Erwartungstreue- oder Deckungszusage für theta,
für das gestörte Gitter oder für nach R,H selektierte Teilmengen. Der
52-Bit-Zufallsgenerator approximiert das kontinuierliche Modell.

**Lokale Kettenreferenz L.** ell ist die Höhe des strikten Intervalls in
Knoten; bei K=0 gilt ell=0. Somit hat eine längste Kette von p bis q
ell+2 Knoten und ell+1 Kanten. Wir verwenden theta_hat_L=ell/(2 sqrt(m)),
auf [0,1] begrenzt, und archivieren auch den unbegrenzten Wert. Die bekannte
asymptotische Zweidimensionskonstante m_2=2 begründet diesen Vergleich,
aber keine endliche Fehlergarantie oder erwartungstreue Schätzung.

## 4. Warum innere Schnittprofile hier keine neue Skaleninformation liefern

Bedingt auf die Endpunkte und K=k sind die k inneren Punkte unabhängig
gleichverteilt im Rechteck (u_p,u_q)×(v_p,v_q). Die Transformation

\[
u'=(u-u_p)/(u_q-u_p),\qquad
v'=(v-v_p)/(v_q-v_p)
\]

führt sie auf unabhängige gleichverteilte Punkte des Einheitsquadrats und
erhält alle kausalen Vergleiche. Damit hängt die Verteilung der **inneren
Ordnung bei festem k** nicht von Lage, Seitenverhältnis oder Fläche des
Rechtecks ab. Im hier definierten Zufallsmodell ist sie bedingt auf K
unabhängig von theta.

Folge: Ein inneres Schnittprofil oder ell trägt über K hinaus keine weitere
statistische Information über theta in diesem Modell. Durch bedingtes
Mitteln kann ein ausschließlich auf K und innerer Ordnung beruhender
Schätzer bei quadratischem Verlust auf einen K-Schätzer reduziert werden,
ohne seinen mittleren Fehler zu vergrößern. Das macht sqrt(K/m) nicht
automatisch zum optimalen K-Schätzer; endliche Bias-Korrektur oder eine
andere Verlustfunktion bleiben andere Fragen.

Diese Argumentation gilt **nicht** für Merkmale der äußeren Ordnung, für
gekrümmte oder inhomogene Modelle oder ohne erneute Prüfung nach globalem
R,H-Matching. Sie ist auch keine Aussage gegen die Nutzung von Schnittprofilen
für andere Ziele. Eine neue mathematische Priorität wird nicht beansprucht.

## 5. Festgelegter erster Versuch

Der [Vertrag](contract.json) fixiert den folgenden Umfang vor neuen Zielziehungen:

| Bestandteil | Festlegung |
| --- | --- |
| Hintergrundpunkte m | 64, 144, 256; Gesamtzahl N=m+2 |
| Kalibrierung | Je m 256 unabhängige uniforme Ordnungen |
| Test | Je m und Familie 1.024 neue Ordnungen; insgesamt 6.912 Ordnungen einschließlich Kalibrierung |
| Familien | Uniformer Hintergrund und gestörtes ausgedünntes Gitter; identisches Endpunktgesetz |
| V | sqrt(K/m), ohne Fit |
| L | ell/(2 sqrt(m)), Vergleich beschreibend |
| C0 | Konstante 64/225 |
| D | Nur globale Relationsdichte und Höhe: feste quadratische OLS-Regression auf uniformer Kalibrierung, keine Parameterwahl am Test |
| Hauptvergleich | Uniform, m=256, alle 1.024 Testordnungen |
| Unsicherheit | 5.000 gepaarte Bootstrap-Ziehungen vollständiger Ordnungen; Kalibrierung festgehalten |
| Zusatzkontrolle | Uniform gegen gestörtes Gitter, exakt auf N,R,H abgeglichen, je Größe mindestens 128 Paare |
| Kein ausreichender Abgleich | INSUFFICIENT_COMMON_SUPPORT; keine Lockerung und keine Ersatz-Hauptanalyse |

Das Gitter verwendet m ohne Zurücklegen gezogene Punkte aus einem
s×s-Gitter mit s=2 sqrt(m), Zellmitten und unabhängiger Störung von
höchstens 0,2 Zellen je Koordinate. Seine Einbettung liefert einen definierten
Zielwert; die uniforme Binomialrechnung wird nicht darauf übertragen.
Für nicht eingebettete Dreischichtkontrollen wird keine Eigenzeit erfunden.

Die globale Vergleichsregression D verwendet bei jeder Größe die festen
Spalten 1,r,h,r²,rh,h², mit r=R/binomial(N,2), h=H/N. Der SVD-Cutoff ist
10^−12 relativ zum größten Singulärwert. Alle Schätzer, die außerhalb
[0,1] liegen können, werden fest auf diesen Bereich begrenzt; Rohwerte bleiben
erhalten. Es gibt kein Fitten von V oder L und keine nachträgliche
Wahl eines besten Klassifikators. P123 wird in diesem Versuch nicht ausgewertet.

Die Zusatzkontrolle paart ausschließlich nach globalem N,R,H und einer
festen Hash-Priorität der IDs. K, ell, Zielwerte, Koordinaten und Fehler werden
dabei nicht benutzt. Dadurch bleibt der Anschluss an PR #41 erhalten.
Matching verändert die Zielverteilung; Ergebnisse werden ausdrücklich
getrennt vom unselektierten Modelltest berichtet. Die 50%-Regel der früheren
Klassifikation ist kein Regressionskriterium.

**Qualifikation im deklarierten Modell** verlangt gleichzeitig:

1. RMSE(V)<=0,05 bei m=256.
2. Mindestens 10 % weniger mittleren quadratischen Fehler als sowohl D als auch C0.
3. Für beide gepaarten MSE-Differenzen liegt die obere 95%-Bootstrap-Grenze unter null.
4. Alle Integritäts- und Vollständigkeitsprüfungen bestehen.

Die Grenzen 0,05 und 10 % sind vorab gewählte technische Abnahmekriterien,
keine Naturkonstanten und keine ausgerechnete Teststärke. Alle Bedingungen sind
erforderlich; es wird nicht das günstigere der beiden Vergleichergebnisse gewählt.
Ein Scheitern heißt NO_QUALIFICATION_DEMONSTRATED, kein Nachweis prinzipieller
Unmöglichkeit. Ausführungsfehler oder unvollständige Hauptdaten heißen INCONCLUSIVE.
Alle anderen Größen, L-Vergleiche und Gitterübertragungen bleiben beschreibend.
Nahe theta=0 werden keine relativen Fehler als Hauptkriterium verwendet.

## 6. Designprüfungen und Ausführungsstand

Abgeschlossen sind Zieldefinition, Annahmen, Begründung, Gegenbeispiel,
Fallzahlen und Auswertungsvertrag. Die deterministischen Kleintests rechnen
ausschließlich mit rationalen Zahlen bzw. kleinen exakten Binomialsummen:

- gleiche Ordnung, verschiedene Zielwerte;
- Erhalt unter Umnummerierung mit transportierten Markierungen;
- Lorentz-Boost (u,v)->(2u,v/2) und gemeinsamer Skalierung;
- normierte Rechteckabbildung erhält die innere Ordnung;
- leeres, kettenförmiges und antikettenförmiges Intervall;
- exakte erste und zweite Binomialmomente;
- analytische Momente des festgelegten Endpunktgesetzes.

Ausführen ohne Zusatzbibliotheken:

~~~sh
python3 -B -O research/lorentz_proper_time/check_design.py
~~~

Die [Design-CI](../../.github/workflows/lorentz-proper-time-design.yml) prüft diese
Beispiele und den maschinenlesbaren Vertrag. Der getrennte
[Reproduktionsworkflow](../../.github/workflows/lorentz-proper-time-run.yml)
wiederholt zusätzlich die vollständige archivierte Monte-Carlo-Studie.
Kleine Beispiele prüfen die Rechnungen; der
allgemeine Skalierungs-/Unabhängigkeitsbefund beruht auf dem Argument oben.

Generator-/Schätzerschnittstelle, Leckage- und Replay-Prüfungen sowie der erste
Datenlauf sind inzwischen implementiert und intern geprüft. Der Rechenstand
ist an Commit `9aca530f2bd0b8ec68e7262013a5c8b3c8bce575` gebunden.
[RESULTS.md](RESULTS.md) enthält Ergebnisse und Chronologie; die historischen
Statusfelder in Vertrag und Quellenfixierung bleiben unverändert.
Offen bleiben externe Replikation, ausreichende Vergleichspaare bei m=256
und Untersuchungen außerhalb des festgelegten Modells. Ein neuer Versuch
benötigt einen eigenen vorab festgelegten Vertrag; spätere Änderungen dürfen
den alten Lauf nicht rückwirkend umdefinieren.

## 7. Literatur und Reichweite

- G. Brightwell und R. Gregory, *Structure of random discrete spacetime*,
  Phys. Rev. Lett. 66, 260 (1991), [DOI](https://doi.org/10.1103/PhysRevLett.66.260).
  [Öffentlicher Vorabdruck, S. 5–6](https://ntrs.nasa.gov/api/citations/19900019113/downloads/19900019113.pdf):
  Zusammenhang längster Ketten und zeitartiger Distanz, Zweidimensionskonstante.
- R. Ilie, G. B. Thompson und D. D. Reid, *A numerical study of the correspondence
  between paths in a causal set and geodesics in the continuum*,
  [arXiv:gr-qc/0512073](https://arxiv.org/abs/gr-qc/0512073).
  Numerische Untersuchungen in flachen und ausgewählten gekrümmten Modellen.
- M. E. Aghili, L. Bombelli und B. B. Pilgrim, *Path length distribution in
  two-dimensional causal sets*, [arXiv:1805.07312](https://arxiv.org/abs/1805.07312).
  Pfadlängenstatistik als verwandter, eigenständiger Untersuchungsgegenstand.

Die Algebra und der neue Prüfvertrag sind hier explizit hergeleitet; die
Publikationen haben diesen konkreten Versuch nicht ausgeführt. Ein erfolgreicher
Test qualifiziert einen Schätzer im genannten synthetischen Modell. Er liefert
keinen allgemeinen Mannigfaltigkeitsnachweis, keine Krümmungsrekonstruktion,
keinen bewiesenen Kontinuumslimes und keine physikalische Validierung.
Externe Replikation bleibt offen.
