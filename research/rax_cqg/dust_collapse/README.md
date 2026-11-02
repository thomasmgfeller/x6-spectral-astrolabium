# Staubkollaps auf Kausalsets · Dust collapse on causal sets

**Forschungsstand vom 2. November 2026.** Wie genau lässt sich die Masse eines kollabierenden Staubballs aus diskreten Ereignissen bestimmen? Für das homogene, marginal gebundene Innere kennen wir die klassische Masse. Damit lässt sich trennen, wie viel einer gemessenen Abweichung vom endlichen Zeitfenster, von der Beprobungsdichte oder von der Streuung einzelner Kausalordnungen stammt.

**English summary.** The five notes connect a conditional bounce model and finite Benincasa–Dowker–Glaser (BDG) path sums to a distinct calibration problem on a prescribed classical dust background. The analytic curved-spacetime boundary correction reduced the largest error in the **mean** mass current from 9.50% to 0.95% across 18 new high-density cases. All 18 already met the 10% target before correction. Over all 24 cases, the corrected mean passed in 23. The remaining low-density case had a 10.79% error. The mass uncertainty of one sprinkling and a collapse law derived from causal-set histories remain open. The primary reports are in German. [Latest report (PDF)](reports/CST_Staubkollaps_Gekruemmter_Randterm.pdf) · [24 case results (CSV)](curved_boundary/holdout.csv) · [Full verification package (ZIP)](packages/CST_Staubkollaps_Gekruemmter_Randterm_Pruefpaket.zip)

## Von der Kausalordnung zur überprüfbaren Aussage

| Schritt | Was gezeigt oder geprüft wurde | Unterlagen |
|---|---|---|
| 1 · Bedingte Bewegungsgleichung | Ein erreichbares, nichtentartetes Maximum der effektiven Hamiltonfunktion führt im homogenen Modell zur Umkehr. Für die untersuchte Differenzendynamik folgen Minimalradius und Krümmungsgrenze. Ihre Skala und das Sinus-Symbol sind Modellannahmen. | [Herleitung (PDF)](reports/CST_Herleitung_Staubkollaps.pdf) |
| 2 · BDG-Pfadsumme mit Randdaten | Bei acht Ereignissen wurden alle 6 241 beschrifteten Historien der Vergleichsklasse einzeln geprüft. Bei zwölf Ereignissen summiert eine exakte Transferformel über 13 332 166 225 Historien. Ein markierter Anfangsgrad kann die Phasenauslöschung verändern. Die asymptotische Unterdrückung im Staubsektor bleibt offen. | [Beweisschema (PDF)](reports/CST_BDG_Staubkollaps_Beweisschema.pdf) · [Ausführbarer PDF-Anhang (Python)](bdg/bdgpruefung.py) |
| 3 · Volumen und klassische Masse | Zwei verschachtelte Zeitfenster entfernen den Mittelwertfehler für einen quadratischen Volumenverlauf. 35 von 36 Ensemblevergleichen bestanden im ersten Lauf, der offene Fall in einer unabhängigen Nachprüfung. Nur 19 von 36 Einstellungen erreichten höchstens 10 % relative Standardabweichung je Einzelrealisierung. | [Kalibrierung (PDF)](reports/CST_Staubkollaps_Kalibrierung.pdf) · [Code, Referenzen und Daten (ZIP)](packages/CST_Staubkollaps_Kalibrierung_Pruefpaket.zip) |
| 4 · Vergangenheit und Zukunft getrennt | Am Schnitt 0,4 bei Dichte 10⁵ sinkt der mittlere Fluss in Einheiten der Sollmasse von 3,085 auf 2,267 bei längerer Vergangenheit, auf 2,208 bei längerer Zukunft und auf 1,313 bei beidseitiger Verlängerung. Der gemeinsame Beitrag ist durch Ereignispaare mit zwei neu erfassten Endpunkten bestimmt. | [Getrennte Zeitränder (PDF)](reports/CST_Staubkollaps_Getrennte_Zeitraender.pdf) · [144 Erwartungswerte und 4 096 direkt erzeugte Ordnungen (ZIP)](packages/CST_Staubkollaps_Getrennte_Zeitraender_Pruefpaket.zip) |
| 5 · Gekrümmter Randterm | In der vorgegebenen Staubgeometrie enthält die führende Korrektur einen logarithmischen Beitrag und einen berechenbaren Fensterterm. Die Vorhersagen wurden ohne Anpassung an die 24 neuen numerischen Referenzwerte geprüft. | [Herleitung und Prüfung (PDF)](reports/CST_Staubkollaps_Gekruemmter_Randterm.pdf) · [Code und Tabellen](curved_boundary/) · [Originalpaket (ZIP)](packages/CST_Staubkollaps_Gekruemmter_Randterm_Pruefpaket.zip) |

## Was die letzte Korrektur misst

Seien $s$ der Schnittzeitpunkt, $U=T_s-s$ die verbleibende Eigenzeit bis zur klassischen Singularität der Referenz und $P,F$ die erfasste Vergangenheit und Zukunft. Für $p=P/U>0$, $0<f=F/U<1$ und $\Lambda=\lambda U^4$ lautet die Hochdichteentwicklung bei festem Fenster

$$
\frac{\mathbb E[M_B]}{M}=1+
\frac{B(p,f)-\frac{17\sqrt{6}}{10\pi}\log\Lambda}{\sqrt{\Lambda}}
+O_{p,f,\delta}(\Lambda^{-1/2-\delta}),\qquad 0<\delta<1/4.
$$

$M_B$ ist der diskrete Massestrom mit Materiegewicht am späteren Endpunkt. Die Korrektur dividiert ihn durch den aus den ersten beiden Termen berechneten Erwartungsfaktor. Sie setzt die Zeitskala $U$ voraus. Auf den 18 höheren Dichtefällen betrug der maximale absolute Mittelwertfehler 9,50 % ohne Korrektur, 3,66 % mit der flachen Referenzformel und 0,95 % mit der Staubformel. Bei der niedrigsten Dichte blieb im späten Fenster mit längerer Vergangenheit ein Restfehler von 10,79 %. Das Prüfmaterial trennt die vorausberechneten Faktoren von der numerischen Referenzintegration. [Versuchsdefinition](curved_boundary/design.json) · [Vorhersagen](curved_boundary/predictions.csv) · [Referenzwerte](curved_boundary/reference.csv) · [Alle Vergleiche](curved_boundary/holdout.csv)

## Anschluss an die bisherigen Forschungen

- **RAX-CQG** liefert die Fragestellung nach einer gravitativen Summe über kausale Historien. Der endliche Benchmark definiert Ordnungen, Intervallzahlen und Modellgrenzen. Schritt 2 verwendet solche Intervallzahlen für die normierte 4D-BDG-Wirkung in einer eigens definierten Schichtklasse. Die Schritte 3–5 rechnen auf einer vorgegebenen klassischen Geometrie. [Forschungsarchitektur](../../../docs/research/rax/cqg-v0.1/README.md) · [Modellvertrag des Benchmarks](../benchmark-v0.2.0/MODEL_CONTRACT.md)
- **Eigenzeit** untersucht, welche geometrischen Grössen aus endlichen kausalen Daten mit welcher Unsicherheit rekonstruierbar sind. Hier wird diese Frage auf Volumen und Massestrom mit bekannten Staubmarken übertragen. Der frühere geglättete Benincasa–Dowker-Operatorvergleich hat eigene Gewichte und Akzeptanzkriterien. [Eigenzeit in 3+1 Dimensionen](../../eigenzeit_4d/README.md) · [Geglättete BD-Referenz](../../lorentz_bd_reference/README.md)
- **Zwei Pulse** sind eine ergänzende Studie zu Streuung und ausfallenden Registrierungen in derselben Poisson-Raumzeit. Ihre Abstandsstatistik bezieht sich auf doppelt registrierte Pulse. [Zweipuls-Studie, Bericht und Daten](../../eigenzeit/two_pulse_links/README.md)

Eine dynamische Herleitung eines Rückpralls aus der CST ist offen. Ebenso offen ist nach der Randkorrektur die Massenunsicherheit einer einzelnen Realisierung im geprüften Hochdichte-Bereich. Eine neue Prüfung sollte Bias und Varianz des korrigierten Flusses auf getrennt erzeugten Kausalordnungen ausweisen. Die veröffentlichten Ergebnisse stammen aus Modellrechnungen und synthetischen Ordnungen.

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

Erwartet werden sechs bestandene Vergleiche je höherer Dichtestufe und fünf von sechs im Belastungstest. Die vier veröffentlichten ZIP-Pakete der Reihe und der ergänzenden Pulsstudie enthalten eigene Prüfsummen. Wer Ergebnisse zitiert, kann Berichtstitel, Datum und den verwendeten Git-Commit angeben. [Zitationsmetadaten](../../../CITATION.cff) · [Lizenzumfang](../../../LICENSE_SCOPE.md)
