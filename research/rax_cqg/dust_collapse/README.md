# Staubkollaps auf Kausalsets · Dust collapse on causal sets

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
