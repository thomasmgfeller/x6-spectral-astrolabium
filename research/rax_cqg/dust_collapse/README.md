# Staubkollaps auf Kausalsets · Dust collapse on causal sets

## Ein Wegpunkt aus der Kausalordnung · 3. November 2026

Wie genau wird die Eigenzeit eines Staubwegs rekonstruiert, wenn nur die Enden vorgegeben sind? In diesem Versuch wählt die Kausalordnung den Zwischenpunkt. Eine unabhängige Zählung misst anschliessend die Phase des einmal halbierten Weges. Ein Treffer verlangt höchstens 0,10 rad Unterschied zwischen ganzem und geteiltem Weg sowie höchstens 0,20 rad Abstand beider Schätzungen vom Referenzwert 8.

Im vorgegebenen kontrahierenden Staubmodell erreichten bei Referenzbesetzung ν = 1024 genau 696 von 1024 Realisierungen beide Toleranzen, bei ν = 4096 waren es 972 von 1024. Im separat geplanten Zusatzversuch bei ν = 16 384 bestanden 256 von 256 Realisierungen. Das exakte zweiseitige 99-Prozent-Konfidenzintervall reicht dort von 97,95 bis 100 %. ν ist die erwartete Besetzung eines vollständigen flachen Halbintervalls der Dauer 4 t₀. Im Hauptversuch lagen 1021 von 1024 Wegen innerhalb der absoluten Toleranz. Für das gemeinsame Ergebnis war der Vergleich der beiden Unterteilungen ausschlaggebend.

Der Bericht beweist die Konvergenz des Zwischenpunkts bei steigender Dichte für die untersuchten Geometrien und zeigt ein Gegenbeispiel zur pauschalen Halbvolumen-Korrektur am Beobachtungsrand. Die dynamische vierdimensionale Kausalset-Summe und die Singularitätsauflösung bleiben offen.

**English.** With fixed outer endpoints and one waypoint selected by causal order, independent counts met both phase tolerances in 696 of 1024 dust trials at reference occupancy 1024 and 972 of 1024 at 4096. At occupancy 16,384, all 256 fresh trials in a separately planned follow-up passed. The exact two-sided 99% lower confidence limit there is 97.95%. These results concern prescribed backgrounds and one bisection.

[Wegpunkt-Prüfbericht (PDF, 5 Seiten)](reports/Kausalordnung_Wegpunkt_Pruefbericht.pdf) · [Reproduktionspaket mit Code, Rohdaten und Prüfsummen (ZIP)](packages/Kausalordnung_Wegpunkt_Reproduktionspaket.zip)

Die README im ZIP beschreibt den vollständigen Lauf mit Python, NumPy, SciPy und C++17. Für den Abgleich der gelieferten Daten und Ergebnistabellen genügt dieser kürzere Lauf im entpackten Verzeichnis.

```sh
sha256sum -c SHA256SUMS
export OPENBLAS_NUM_THREADS=1
python3 score.py
python3 holdout_check.py
sha256sum -c SHA256SUMS
```

## Wegphasen unter Verfeinerung in vier Dimensionen · 3. November 2026

Auf einer vorgegebenen kontrahierenden Staubraumzeit wurde derselbe markierte Weg auf denselben Poisson-Ereignissen mit vier und acht Abschnitten ausgewertet. Bei vollständiger Beobachtung erfüllten mit der Referenzbesetzung 256 genau 32 247 von 32 768 Realisierungen beide Anforderungen: höchstens 0,10 Radiant Unterschied bei der Unterteilung und höchstens 0,20 Radiant Abweichung vom bekannten Wert für beide Schätzungen. Das sind 98,41 %. Bei Besetzung 64 waren es 76,65 %. Die Referenzbesetzung bezeichnet die erwartete Ereigniszahl in einem vollständigen flachen Intervall der feinsten Abschnittslänge.

Wenn die Beobachtungsebene jedes Intervall genau halbiert, kann die Schätzung unter Verfeinerung stabil bleiben und den richtigen Phasenwert dennoch verfehlen. Für diesen symmetrischen Rand wurde die analytische Korrektur an frischen Realisierungen geprüft. Die Ergebnisse gelten für die markierten Wege auf den vorgegebenen Hintergründen.

**English.** With four versus eight segments on a prescribed contracting dust spacetime, 98.41% of trials at reference occupancy 256 met both phase tolerances, compared with 76.65% at 64. A centered observation boundary can leave the estimate stable while biasing its absolute value. An independent run checks the correction for that symmetric boundary.

[4D-Verfeinerungsbericht (PDF, 5 Seiten)](reports/CST_Wegphasen_4D_Verfeinerung.pdf) · [Prüfpaket mit Code und Ergebnistabellen (ZIP)](packages/CST_Wegphasen_4D_Verfeinerung_Pruefpaket.zip)

Wiederholung im entpackten Verzeichnis mit Python, NumPy und SciPy:

```sh
sha256sum -c SHA256SUMS
export OPENBLAS_NUM_THREADS=1
python3 run.py
python3 check_points.py
python3 curvature.py
python3 check_half.py
```

## Wegabhängige Staubphasen · 3. November 2026

In 58 von 75 endlichen Kausalordnungen unterscheiden die Zählungen zweier aufeinanderfolgender Intervalle Wege mit gleichen Endpunkten. Keine der 32 geprüften Einstellungen erfüllt die vorab festgelegte Regel für eine Vorhersage des späteren Volumens. Bei der gravitativen Kopplung $g=4\pi/5$ schliesst ein reproduzierbares Zertifikat die Freigabe des klassischen Zielzählwerts eins für jede Phasenstärke aus, wenn dieselbe reelle Funktion der Intervallzahl auf beide Wegsegmente angewandt wird. Der Satz gilt für die untersuchten 75 Geometrien, die beiden Paketaufteilungen, den normierten Transport und den gemeinsamen eindimensionalen Endraum.

**English.** The two-interval duration distinguishes paths with identical endpoints in 58 of 75 finite geometries. None of 32 settings qualifies for a late-volume prediction. At the stated coupling, the certificate excludes release of target count one for any phase strength in the specified two-block model. The four-dimensional collapse dynamics and singularity question remain open.

[Bericht zu den Wegphasen (PDF, 5 Seiten)](reports/CST_Staubtransport_Wegphasen.pdf) · [Code, Ergebnistabellen und Ausschlusszertifikat (ZIP)](packages/CST_Staubtransport_Wegphasen_Pruefpaket.zip)

Zur Reproduktion im entpackten Verzeichnis ausführen. Die ersten beiden Rechnungen verwenden NumPy und SciPy. Für das Zertifikat genügt die Python-Standardbibliothek.

```sh
sha256sum -c SHA256SUMS
python3 calibrate.py
python3 phase.py
python3 certify.py
```

## Erhaltener Massenfluss · 3. November 2026

In 75 endlichen Kausalordnungen überquert die anfänglich festgelegte Masse $M=3$ alle 1 006 zulässigen Schnitte unverändert. Wird im Inneren absichtlich eine Einheit entnommen, lautet die Folge der vier gemessenen Flüsse $(3,3,2,2)$. Beim normierten Transport und der untersuchten Wegphase erhalten alle Geometrien denselben Materiefaktor. Keine der 24 geprüften Einstellungen erfüllt die vorab festgelegte Regel für eine Vorhersage des späteren Volumens. Die Massenerhaltung gilt im gewählten diskreten Transportmodell. Eine vierdimensionale Kollapsdynamik und die Singularitätsauflösung bleiben offen.

**English.** The initially prepared mass crosses all 1,006 admissible cuts of 75 finite geometries unchanged. Normalized routing with the chosen path phase leaves their relative amplitudes unchanged. None of the 24 settings qualified for a late-volume prediction.

[Bericht zum Massenfluss (PDF, 4 Seiten)](reports/CST_Staubtransport_Massenfluss.pdf) · [Prüfpaket mit Code und Ergebnistabellen (ZIP)](packages/CST_Staubtransport_Massenfluss_Pruefpaket.zip)

Reproduktion mit Python und NumPy im entpackten Verzeichnis:

```sh
sha256sum -c SHA256SUMS
python3 transport.py
python3 score.py
```

## Endliche Staubkopplung · 3. November 2026

Für dieselben 6 241 beschrifteten Kausalordnungen sinkt bei der dimensionslosen Dichteobergrenze $s=0{,}5$ der Betrag der Summe von 2 668,574 bei ausgeschalteter gravitativer Phase auf 72,277 bei $g=4\pi/5$. In einer getrennten Klasse mit 75 Historien erfüllt keine der 24 Parametereinstellungen die vorab gewählte Regel für eine Vorhersage des späteren Zählwerts. Bei festgehaltener idealer Staubzeit ergibt die unabhängige lokale Dichteintegration eine mittlere Dichte von $\Sigma/2$. Halbiert sich das mitbewegte Volumen, halbiert sich die so berechnete Masse. Damit scheitert diese Modellwahl an der Erhaltung der Staubmasse.

**English.** Switching on the gravitational phase reduces the amplitude magnitude to 2.71% of its value on the same 6,241 orders at the stated coupling and density cutoff. None of the 24 window tests met the prediction rule. At fixed ideal dust time the chosen local density measure fails the classical mass-conservation test. The calculation leaves singularity resolution open.

[Prüfbericht (PDF, 4 Seiten)](reports/CST_Staubkopplung_Endliche_Summe.pdf) · [Prüfpaket mit Code und Ergebnistabellen (ZIP)](packages/CST_Staubkopplung_Endliche_Summe_Pruefpaket.zip)

Zur Reproduktion das Prüfpaket entpacken und im entpackten Verzeichnis mit Python und NumPy ausführen. Die Referenzauswertung verwendet Python 3.12.14 und NumPy 2.3.5.

```sh
sha256sum -c SHA256SUMS
python3 run.py
python3 score.py
```

## Vom Staubkollaps zur Quantendynamik · 3. November 2026

Im homogenen Staubmodell mit Dirichlet-Randbedingung lässt sich der Erwartungswert des Volumens exakt aus dem Anfangszustand berechnen. Bei einem kontrahierenden Zustand erreicht er ein positives Minimum. Im selben Modell kann das inverse zweite Volumenmoment am Minimum divergieren. Für die vierdimensionale Kausalset-Summe gibt Gleichung (21) auf Seite 7 eine hinreichende Fehlerschranke. Ob die staubgekoppelte Summe ihre Voraussetzungen erfüllt, bleibt offen. [Herleitung und Gegenbeispiele (PDF, 10 Seiten)](reports/CST_Staubkollaps_Quantendynamik_Herleitung.pdf)

**English.** The report derives the mean volume for a specified homogeneous quantization. A counterexample shows why a positive minimum of the mean volume alone cannot establish a curvature bound. Predicting the volume directly from dust-coupled causal-set histories remains open.

**Interaktives Staubball-Labor.** Im Raumzeitdiagramm lassen sich die Stauboberfläche und das kausale Einzugsgebiet durch das Messfenster verfolgen. Die zwölf unabhängigen Kausalordnungen wurden am festen Schnitt 0,47 im periodischen Referenzwürfel ausgewertet. Die Glättung bei effektiver Dichte 600 000 trifft das ±10-Prozent-Band in einem von zwölf Fällen bei Eingangsdichte 1,2 Millionen, der lokale Strom in keinem. Die Beobachtungen und die offenen Probeläufe bei sechs Millionen sind getrennt. [Labor öffnen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/staubball/index.html?lang=de) · [English lab](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/staubball/index.html?lang=en) · [Forschungsbericht (PDF)](reports/CST_Staubkollaps_Geglaetteter_Massestrom.pdf) · [Prüfpaket (ZIP)](packages/CST_Staubkollaps_Geglaetteter_Massestrom_Pruefpaket.zip) · [Normierte Messwerte](smoothed/full_scores.csv) · [Rohsummen und Punktzahlen](smoothed/full.csv) · [Freiwillige Probeläufe](https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues/192)

**Forschungsstand vom 2. November 2026.** Wie genau lässt sich die Masse eines kollabierenden Staubballs aus diskreten Ereignissen bestimmen? Für das homogene, marginal gebundene Innere kennen wir die klassische Masse. Damit lässt sich trennen, wie viel einer gemessenen Abweichung vom endlichen Zeitfenster, von der Beprobungsdichte oder von der Streuung einzelner Kausalordnungen stammt.

**English summary.** The six notes connect a conditional bounce model and finite Benincasa–Dowker–Glaser (BDG) path sums to a distinct calibration problem on a prescribed classical dust background. The analytic curved-spacetime boundary correction reduced the largest error in the **mean** mass current from 9.50% to 0.95% across 18 new high-density cases. All 18 already met the 10% target before correction. Over all 24 cases, the corrected mean passed in 23. The remaining low-density case had a 10.79% error. Four additional cases at a new time cut, with the past and future windows exchanged, reduced the mean error to 0.74–9.61%. [Additional results (CSV)](additional_windows/results.csv). The corrected local current failed the single-order target in all four high-density settings. At density 600,000, neither group of 16 independent orders produced an estimate within 10% of the known mass. At density six million, simultaneous 99% upper confidence bounds on the hit probability were 56.5% and 53.0%, against a 95% target. A collapse law derived from causal-set histories remains open. The primary reports are in German. [Single-order report (PDF)](reports/CST_Staubkollaps_Einzelmessung.pdf) · [Single-order replay (ZIP)](packages/CST_Staubkollaps_Einzelmessung_Pruefpaket.zip) · [Mean-current derivation (PDF)](reports/CST_Staubkollaps_Gekruemmter_Randterm.pdf) · [24 case results (CSV)](curved_boundary/holdout.csv) · [Mean-current verification package (ZIP)](packages/CST_Staubkollaps_Gekruemmter_Randterm_Pruefpaket.zip)

## Von der Kausalordnung zur überprüfbaren Aussage

| Schritt | Was gezeigt oder geprüft wurde | Unterlagen |
|---|---|---|
| 1 · Bedingte Bewegungsgleichung | Ein erreichbares, nichtentartetes Maximum der effektiven Hamiltonfunktion führt im homogenen Modell zur Umkehr. Für die untersuchte Differenzendynamik folgen Minimalradius und Krümmungsgrenze. Ihre Skala und das Sinus-Symbol sind Modellannahmen. | [Herleitung (PDF)](reports/CST_Herleitung_Staubkollaps.pdf) |
| 2 · BDG-Pfadsumme mit Randdaten | Bei acht Ereignissen wurden alle 6 241 beschrifteten Historien der Vergleichsklasse einzeln geprüft. Bei zwölf Ereignissen summiert eine exakte Transferformel über 13 332 166 225 Historien. Ein markierter Anfangsgrad kann die Phasenauslöschung verändern. Die asymptotische Unterdrückung im Staubsektor bleibt offen. | [Beweisschema (PDF)](reports/CST_BDG_Staubkollaps_Beweisschema.pdf) · [Ausführbarer PDF-Anhang (Python)](bdg/bdgpruefung.py) |
| 3 · Volumen und klassische Masse | Zwei verschachtelte Zeitfenster entfernen den Mittelwertfehler für einen quadratischen Volumenverlauf. 35 von 36 Ensemblevergleichen bestanden im ersten Lauf, der offene Fall in einer unabhängigen Nachprüfung. Nur 19 von 36 Einstellungen erreichten höchstens 10 % relative Standardabweichung je Einzelrealisierung. | [Kalibrierung (PDF)](reports/CST_Staubkollaps_Kalibrierung.pdf) · [Code, Referenzen und Daten (ZIP)](packages/CST_Staubkollaps_Kalibrierung_Pruefpaket.zip) |
| 4 · Vergangenheit und Zukunft getrennt | Am Schnitt 0,4 bei Dichte 10⁵ sinkt der mittlere Fluss in Einheiten der Sollmasse von 3,085 auf 2,267 bei längerer Vergangenheit, auf 2,208 bei längerer Zukunft und auf 1,313 bei beidseitiger Verlängerung. Der gemeinsame Beitrag ist durch Ereignispaare mit zwei neu erfassten Endpunkten bestimmt. | [Getrennte Zeitränder (PDF)](reports/CST_Staubkollaps_Getrennte_Zeitraender.pdf) · [144 Erwartungswerte und 4 096 direkt erzeugte Ordnungen (ZIP)](packages/CST_Staubkollaps_Getrennte_Zeitraender_Pruefpaket.zip) |
| 5 · Gekrümmter Randterm | In der vorgegebenen Staubgeometrie enthält die führende Korrektur einen logarithmischen Beitrag und einen berechenbaren Fensterterm. Die Vorhersagen wurden ohne Anpassung an die 24 neuen numerischen Referenzwerte geprüft. | [Herleitung und Prüfung (PDF)](reports/CST_Staubkollaps_Gekruemmter_Randterm.pdf) · [Code und Tabellen](curved_boundary/) · [Originalpaket (ZIP)](packages/CST_Staubkollaps_Gekruemmter_Randterm_Pruefpaket.zip) |
| 6 · Masse einer einzelnen Kausalordnung | Der korrigierte lokale Strom verfehlt das Ziel für Einzelmessungen in allen vier Hochdichtefällen. Die direkten Vollzählungen und die gepaarten Schranken prüfen unterschiedliche Aspekte der Streuung. | [Einzelmessung (PDF)](reports/CST_Staubkollaps_Einzelmessung.pdf) · [Code, Protokolle und Einzelwerte (ZIP)](packages/CST_Staubkollaps_Einzelmessung_Pruefpaket.zip) |

## Was die letzte Korrektur misst

Seien $s$ der Schnittzeitpunkt, $U=T_s-s$ die verbleibende Eigenzeit bis zur klassischen Singularität der Referenz und $P,F$ die erfasste Vergangenheit und Zukunft. Für $p=P/U>0$, $0<f=F/U<1$ und $\Lambda=\lambda U^4$ lautet die Hochdichteentwicklung bei festem Fenster

$$
\frac{\mathbb E[M_B]}{M}=1+
\frac{B(p,f)-\frac{17\sqrt{6}}{10\pi}\log\Lambda}{\sqrt{\Lambda}}
+O_{p,f,\delta}(\Lambda^{-1/2-\delta}),\qquad 0<\delta<1/4.
$$

$M_B$ ist der diskrete Massestrom mit Materiegewicht am späteren Endpunkt. Die Korrektur dividiert ihn durch den aus den ersten beiden Termen berechneten Erwartungsfaktor. Sie setzt die Zeitskala $U$ voraus. Auf den 18 höheren Dichtefällen betrug der maximale absolute Mittelwertfehler 9,50 % ohne Korrektur, 3,66 % mit der flachen Referenzformel und 0,95 % mit der Staubformel. Bei der niedrigsten Dichte blieb im späten Fenster mit längerer Vergangenheit ein Restfehler von 10,79 %. Das Prüfmaterial trennt die vorausberechneten Faktoren von der numerischen Referenzintegration. [Versuchsdefinition](curved_boundary/design.json) · [Vorhersagen](curved_boundary/predictions.csv) · [Referenzwerte](curved_boundary/reference.csv) · [Alle Vergleiche](curved_boundary/holdout.csv)

## Zusatzprüfung mit vertauschten Zeitfenstern

Am neuen Schnitt $s=0{,}47$ wurden Vergangenheit $P$ und Zukunft $F$ vertauscht und zwei weitere Beprobungsdichten geprüft. Alle vier Vorhersagen wurden mit dem veröffentlichten Randterm vor Auswertung der Referenzintegrale berechnet. Die Tabelle zeigt den relativen Fehler des **erwarteten** Massestroms gegenüber der bekannten klassischen Staubmasse.

| Beprobungsdichte | Vergangenheit $P$ | Zukunft $F$ | Ohne Korrektur | Mit Staubkorrektur |
|---:|---:|---:|---:|---:|
| 600 000 | 0,11 | 0,24 | +39,01 % | +9,16 % |
| 600 000 | 0,24 | 0,11 | +41,08 % | +9,61 % |
| 6 000 000 | 0,11 | 0,24 | +9,00 % | +0,74 % |
| 6 000 000 | 0,24 | 0,11 | +9,49 % | +0,78 % |

Bei der höheren Dichte lag der Fehler schon vor der Korrektur in beiden Orientierungen unter 10 %. Die Zusatzprüfung betrifft dieselbe vorgegebene Geometrie wie die Hauptserie. Die anschliessende Prüfung an einzelnen Kausalordnungen folgt im nächsten Abschnitt. [Vier Ergebnisse mit beiden Referenzintegralen (CSV)](additional_windows/results.csv) · [Eigenständiges Prüfpaket (ZIP)](packages/CST_Randkorrektur_Vier_Zusatzfaelle.zip)

Zur Reproduktion das Zusatzpaket in ein neues Verzeichnis entpacken und dort mit Python 3.12, NumPy 2.3.5 und SciPy 1.17.0 ausführen. Die Spalten `raw_error` und `corrected_error` in `results.csv` enthalten Bruchteile der Sollmasse. [Quellstand der verwendeten Randkorrektur](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/dd78ba05f4d91b6e62579ab41621be5cecaa079c/research/rax_cqg/dust_collapse/curved_boundary)

```sh
OPENBLAS_NUM_THREADS=1 python3 check_windows.py
```

## Einzelmessung des korrigierten Massestroms

Vorab gefordert waren mindestens 95 % Treffer im Band von ±10 % um die bekannte Staubmasse. Am Schnitt $s=0{,}47$ verfehlt der lokale Strom dieses Ziel in allen vier Hochdichtefällen. Die Tabelle unterscheidet direkt beobachtete Treffer von statistischen Obergrenzen. [Bericht mit Herleitung (PDF)](reports/CST_Staubkollaps_Einzelmessung.pdf) · [Prüfplan](single_order/design.json)

| Beprobungsdichte | Vergangenheit / Zukunft | Fehler des Mittelwerts | Ergebnis für eine Einzelmessung |
|---:|---|---:|---|
| 600 000 | 0,11 / 0,24 | +9,16 % | 0 von 16 vollständigen Ordnungen im Band |
| 600 000 | 0,24 / 0,11 | +9,61 % | 0 von 16 vollständigen Ordnungen im Band |
| 6 000 000 | 0,11 / 0,24 | +0,74 % | Trefferwahrscheinlichkeit höchstens 56,5 % |
| 6 000 000 | 0,24 / 0,11 | +0,78 % | Trefferwahrscheinlichkeit höchstens 53,0 % |

Bei sechs Millionen Ereignissen pro Einheit Vierervolumen wurde für jede Orientierung in 128 unabhängigen Paarversuchen ein kleiner zukünftiger Kegel neu beprobt. Der Rest jeder gepaarten Ordnung ist gemeinsam. Die daraus abgeleiteten Grenzen gelten für die ganze Kugel, mit gemeinsamer 99-Prozent-Absicherung. Die genaue Gesamtvarianz ist bei dieser Dichte offen. [Schranken für alle vier Fälle (CSV)](single_order/high_bounds.csv)

Die direkten Kohorten bei 600 000 sind getrennte Stichproben. Die Spalte `raw` enthält den Strom vor Division durch den in der Zusammenfassung angegebenen Faktor `Rpred`. [Direkte Auswertung und Korrekturfaktoren (CSV)](single_order/direct_high_summary.csv) · [Einzelwerte mit längerer Zukunft (CSV)](single_order/high_second.csv) · [Einzelwerte mit längerer Vergangenheit (CSV)](single_order/high_full.csv)

Das eigenständige Archiv enthält die Startwerte, C++- und Python-Implementierungen, numerische Gegenprüfungen und alle Messwerttabellen. Aus einer entpackten Arbeitskopie prüfen die folgenden Befehle die Auswertung der archivierten Daten. Die enthaltene `README.txt` beschreibt auch den erneuten Aufbau der Ordnungen. [Vollständiges Prüfpaket (ZIP)](packages/CST_Staubkollaps_Einzelmessung_Pruefpaket.zip)

```sh
sha256sum -c SHA256SUMS.txt
python3 analyze.py
python3 summarize_full.py
```

## Anschluss an die bisherigen Forschungen

- **RAX-CQG** liefert die Fragestellung nach einer gravitativen Summe über kausale Historien. Der endliche Benchmark definiert Ordnungen, Intervallzahlen und Modellgrenzen. Schritt 2 verwendet solche Intervallzahlen für die normierte 4D-BDG-Wirkung in einer eigens definierten Schichtklasse. Die Schritte 3–6 rechnen auf einer vorgegebenen klassischen Geometrie. [Forschungsarchitektur](../../../docs/research/rax/cqg-v0.1/README.md) · [Modellvertrag des Benchmarks](../benchmark-v0.2.0/MODEL_CONTRACT.md)
- **Eigenzeit** untersucht, welche geometrischen Grössen aus endlichen kausalen Daten mit welcher Unsicherheit rekonstruierbar sind. Hier wird diese Frage auf Volumen und Massestrom mit bekannten Staubmarken übertragen. Der frühere geglättete Benincasa–Dowker-Operatorvergleich hat eigene Gewichte und Akzeptanzkriterien. [Eigenzeit in 3+1 Dimensionen](../../eigenzeit_4d/README.md) · [Geglättete BD-Referenz](../../lorentz_bd_reference/README.md)
- **Zwei Pulse** sind eine ergänzende Studie zu Streuung und ausfallenden Registrierungen in derselben Poisson-Raumzeit. Ihre Abstandsstatistik bezieht sich auf doppelt registrierte Pulse. [Zweipuls-Studie, Bericht und Daten](../../eigenzeit/two_pulse_links/README.md)

Eine dynamische Herleitung eines Rückpralls aus der CST ist offen. Als nächster Kandidat kommt ein über Kausalschichten gemittelter Strom mit vorab festgelegter physikalischer Mittelungsskala infrage. Sein Mittelwertfehler und seine Trefferwahrscheinlichkeit auf einzelnen Ordnungen müssen auf frischen Daten geprüft werden. Die veröffentlichten Ergebnisse stammen aus Modellrechnungen und synthetischen Ordnungen.

## Reproduktion

Vom Repository-Stamm aus lässt sich die endliche Phasensumme mit Python 3.10 oder neuer und der Standardbibliothek prüfen.

```sh
python3 research/rax_cqg/dust_collapse/bdg/bdgpruefung.py
```

Für den aktuellen Massestromtest wurden Python 3.12, NumPy 2.3.5 und SciPy 1.17.0 unter Linux verwendet. Die folgenden Befehle rechnen die Hauptprüfung in einer Arbeitskopie neu. Die genauere Prüfung des logarithmischen Koeffizienten verwendet zusätzlich erweiterte Gleitkommapräzision. [Vollständige Befehle und Präzisionsanforderungen](curved_boundary/README.txt)

```sh
replay_dir=$(mktemp -d)
cp -R research/rax_cqg/dust_collapse/curved_boundary "$replay_dir/"
cd "$replay_dir/curved_boundary"
sha256sum -c SHA256SUMS.txt
python3 coefficient_checks.py
python3 prediction.py
python3 reference.py
python3 evaluate.py
```

Erwartet werden sechs bestandene Vergleiche je höherer Dichtestufe und fünf von sechs im Belastungstest. Die vier ursprünglichen ZIP-Pakete der Reihe und der ergänzenden Pulsstudie enthalten eigene Prüfsummen. Wer Ergebnisse zitiert, kann Berichtstitel, Datum und den verwendeten Git-Commit angeben. [Zitationsmetadaten](../../../CITATION.cff) · [Lizenzumfang](../../../LICENSE_SCOPE.md)
