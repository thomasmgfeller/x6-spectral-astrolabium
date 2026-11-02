# EPTA radio pulsar timing in the Causal Stability Lab

**Der geprüfte Filter erhält keine Freigabe für diesen Versuch.** Die Auswertung verwendet 22 556 freigegebene Radio-Ankunftszeiten von acht Pulsaren. Für J0030+0451 reproduziert TEMPO2 den gewichteten RMS der 4 069 festen Timing-Residuen mit 2,455759 µs. EPTA veröffentlicht 2,45583 µs. Der Vergleich prüft für diesen Pulsar Anzahl und aggregierte Streuung. Ein externer punktweiser Residuenvergleich ist offen. [Im Stabilitätslabor öffnen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/causal-stability/#epta) · [EPTA-Referenz für J0030+0451](https://epta.pages.in2p3.fr/epta-dr2/J0030%2B0451.html)

## Ergebnis

Die Messung liefert Abtastzeiten, Richtungen am Himmel, TOA-Unsicherheiten und feste Timing-Residuen. Die unten genannten Fehlalarme und Treffer stammen aus Simulationen. In beiden Verfahren waren die Auswertezeiten und die simulierten Eingaben identisch. Für jedes Verfahren wurde aus 4 095 separaten Nullsimulationen eine Schwelle für nominell 5 % Fehlalarme kalibriert.

| Verfahren | Fehlalarme in 2 048 neuen Nullversuchen | Treffer in 2 048 neuen Signalversuchen |
|---|---:|---:|
| Ungefilterte Referenz | 132 (6,45 %, Wilson-95-%-Intervall 5,46–7,59 %) | 115 (5,62 %, 4,70–6,70 %) |
| Filter aus dem CSPP-Kontrollgraphen | 104 (5,08 %, 4,21–6,12 %) | 107 (5,22 %, 4,34–6,27 %) |

Filter minus Referenz ergibt −0,39 Prozentpunkte Trefferquote. Das gepaarte approximative 95-%-Intervall beträgt −1,77 bis +0,99 Prozentpunkte. Die beobachteten Fehlalarmraten unterscheiden sich. Die ungefilterte Referenz verfehlt die Kalibrationskontrolle auf den zurückgehaltenen Nullversuchen. Die Daten tragen deshalb keinen Leistungsvergleich bei nachgewiesen gleicher Fehlalarmrate. Keine der vier vorab festgelegten Freigabebedingungen für die Kombination ist erfüllt. [Protokoll vor der Auswertung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/909eacf2d5c43193e2c0dfac2231702bfb960f10/research/epta_filter_v1/protocol.json) · [Ergebnisdatei mit allen Paaren](reference.json)

### Gleiche beobachtete Fehlalarmrate

Ein ergänzender Vergleich nach Einsicht in das vorab festgelegte Ergebnis setzt beide Schwellen so, dass auf denselben 2 048 Nullversuchen genau 102 Fehlalarme auftreten (4,98 %). Die 2 048 getrennten Signaldurchläufe gehen nicht in die Schwellenwahl ein. Bei diesen Schwellen ergeben sich **94 Treffer ohne Filter und 106 mit Filter** (4,59 % und 5,18 %). Die gepaarte Differenz ist +0,59 Prozentpunkte. Ihr bedingtes approximatives 95-%-Intervall bei diesen festen Schwellen reicht von −0,73 bis +1,91 Prozentpunkte. Es erfasst die Streuung der Signalversuche. Die Unsicherheit der Schwellenwahl kommt hinzu. Dieser deskriptive ROC-Vergleich stellt Gleichheit auf der beobachteten Nullstichprobe her. Beide Vergleiche sind mit einer Trefferquotendifferenz von null vereinbar.

## Was mit der Amplitude passiert

Bei der Wiedergabe mit den gemessenen Residuen wird für jede Signalinjektion die Änderung der 28 Kreuzprodukte bestimmt. Der auf das erwartete Winkelmuster projizierte Wert ist eine **vorzeichenbehaftete Schätzung der korrelierten Leistung**. Seine Einheit nach Division durch die eingespeiste Leistung ist 1. Die Schätzung kann auch negativ werden. Die Monte-Carlo-Mittelwerte und ihre Unsicherheiten sind sehr gross. Z. B. reicht das 95-%-Intervall des Mittelwerts für die ungefilterte Referenz von rund −3 927 bis +11 719. Daraus lässt sich keine präzise physikalische Amplitude ableiten.

Eine ergänzende Rechnung bestimmt die Erwartung bei denselben Zeiten ohne Monte-Carlo-Streuung. Sei $M_p$ die Abbildung von den eingespeisten Fourierkoeffizienten zu den geschätzten Koeffizienten für Pulsar $p$. Die Hellings–Downs-Korrelation zweier verschiedener Pulsare sei $Γ_{pq}$, die diagonale normierte Koeffizientenkovarianz $D$. Dann beträgt der Mittelwert des normierten Paarwerts

$$
E[c_{pq}]/A^2 = \tfrac12\,\Gamma_{pq}\,\mathrm{tr}(M_p D M_q^{\mathsf T}).
$$

Für die ungefilterte Referenz ist der projizierte Erwartungswert 1,000 und der Kosinus zum erwarteten Winkelmuster 1,000. Nach Filterung und derselben Auswertung ergeben sich −38,52 und −0,116. Der negative Wert ist ein Effekt der Filter- und Regressionskette. Bei J2322+2057 etwa erreicht die Konditionszahl der gewichteten Designmatrix rund 62 Millionen. Bei lückenhafter Abdeckung eines gemeinsamen Zeitfensters können sich sehr unterschiedliche Fourier- und Trendkoeffizienten fast gleich gut anpassen. Die grossen Zahlen sind kein Mass für eine beobachtete Verstärkung von Gravitationswellen. Eine direkte Kontrolle mit symmetrisch eingespeisten Basisvektoren prüft die Spurformel unabhängig. Diese Zusatzdiagnose ändert die vorab festgelegte Entscheidung nicht.

## Daten, Filter und Statistik

- **Zeitbasis.** Version 2.1 der EPTA DR2, Auswahl DR2full. TEMPO2 verwendet das veröffentlichte Modell jedes Pulsars, die JPL-Ephemeride DE440 und TT(BIPM2021). Ein privates Laufzeitverzeichnis übernimmt die drei freigegebenen Uhrenkorrekturen, insbesondere die korrigierte Nançay-Datei. Exportiert werden topozentrischer und baryzentrischer MJD, unaufgehelltes Residuum bei fester Timinglösung in µs und formaler TOA-Fehler in µs. Die Berechnung injiziert in Residuen bei festgehaltenem Timing-Modell. Eine erneute vollständige Anpassung aller astrophysikalischen Parameter nach jeder Injektion wäre ein anderer Versuch.
- **Kausaler Filter.** Die Transferzeile stammt unmittelbar aus der versionierten JavaScript-Engine des Labs, Preset CSPP, fünf aktive Knoten, drei History-Eingänge, θ = 21. Für einen konstanten Eingang wird auf Verstärkung 1 normiert. Die Gewichte 0,243625, 0,330849 und 0,425526 wirken auf Vorgängerepochen zu 360 und 180 Tagen sowie die aktuelle Epoche. Fehlt in einem vorab festgelegten 60-Tage-Fenster eine Vorgängerepoche, entfällt der Zeitpunkt bei beiden Verfahren. Das ist eine eigens definierte Anwendung des endlichen Kontrollgraphen auf Radiozeitreihen.
- **Abtastung.** Fourierphasen werden an den tatsächlichen baryzentrischen Ankunftszeiten berechnet. Daten und Fourierfunktionen werden innerhalb eines MJD-Tages invers-varianzgewichtet zusammengefasst. Unabhängiges weisses TOA-Rauschen kann nach dieser linearen Mittelung exakt mit der Varianz des Tagesmittels gezogen werden. Es wird kein gleichmässiges Zeitgitter interpoliert.
- **Null und Signal.** Acht feste Himmelsrichtungen, 28 verschiedene Paare, fünf Moden $k/T$ bis etwa 6,6 nHz. Das Nullmodell enthält unabhängiges rotes Rauschen je Pulsar mit 0,60 µs Ensemble-RMS und die formalen weissen TOA-Fehler. Das zusätzliche Signal hat 0,30 µs Ensemble-RMS, ein diskretes Leistungsspektrum proportional zu $k^{-13/3}$ und die Hellings–Downs-Kovarianz. Diese Parameter definieren eine begrenzte Simulation. Der reale Himmel kann weitere gemeinsame oder instrumentelle Störquellen enthalten.
- **Schätzung.** Gemeinsame gewichtete Regression auf Konstante, linearen und quadratischen Trend sowie die fünf Sinus-/Kosinuspaare. Das Skalarprodukt der Fourierkoeffizienten zweier Pulsare, halbiert, ist der Paarwert. Ein Fit ohne Achsenabschnitt auf die 28 Hellings–Downs-Werte liefert den Detektionswert. Es gibt vier getrennte Zufallsströme für Schwellen, Fehlalarme, Treffer und die Injektion in gemessene Residuen. Wilson-Intervalle beschreiben binomiale Anteile. Das gepaarte Intervall verwendet die Streuung der Trefferunterschiede derselben Realisation. Die nominelle Fehlalarmrate ist eine Eigenschaft des angegebenen Nullmodells.

[EPTA-Methoden und Datensatz](https://doi.org/10.1051/0004-6361/202346841) · [EPTA-Suche nach dem winkelkorrelierten Hintergrund](https://doi.org/10.1051/0004-6361/202346844) · [Datenkredit und Lizenz](ATTRIBUTION.md)

## Abschluss und Reproduktion

Die Messreihe wurde am 2. November 2026 abgeschlossen. Der Monatszeitplan, der Start bei Änderungen an main und der manuelle Start der EPTA-Neuberechnung sind aufgehoben. Der letzte geprüfte Datenstand mit Zusammenfassung, Quellenangabe und Timing-Residuen bleibt öffentlich abrufbar. [Abschliessender Produktionslauf](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/41464258179) · [Datenzweig](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/epta-data)

Wiederholung ab Repositorywurzel, Linux x86-64, Python 3.12 und Node.js. Der Standardweg verwendet den öffentlichen Zenodo-Endpunkt. Für einen Offline-Lauf akzeptiert `--archive` die identisch geprüfte ZIP-Datei. Die Daten und Modellversionen sind an den in [protocol.json](protocol.json) und [tempo2.lock](tempo2.lock) angegebenen Stand gebunden.

```sh
bash research/epta_filter_v1/install-tempo2.sh /tmp/x6-epta-tempo
python3.12 -m venv /tmp/x6-epta-py
/tmp/x6-epta-py/bin/pip install numpy==2.3.5
OPENBLAS_NUM_THREADS=1 /tmp/x6-epta-py/bin/python -m agent.epta_filter --tempo-prefix /tmp/x6-epta-tempo --output runs/epta
/tmp/x6-epta-py/bin/python research/epta_filter_v1/check_replay.py runs/epta
/tmp/x6-epta-py/bin/python -m unittest discover -s tests/python -p test_epta.py -v
```
