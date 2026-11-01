# Urnerboden 2017 · Ankunftszeitdifferenzen an drei Schweizer Stationen

Für das Erdbeben vom 6. März 2017 bei Urnerboden (Lokalmagnitude 4,6) vergleicht X6 drei vertikale Breitbandkanäle des Schweizerischen Erdbebendienstes an der ETH Zürich. Die Stationen LLS, MUO und BNALP haben im gewählten Zeitraum jeweils einen HHZ-Kanal mit 120 Hz sowie eine manuelle Pg-Markierung. Pg bezeichnet hier den im SED-Katalog zugeordneten regionalen P-Welleneinsatz in der Erdkruste. Die manuelle Zuordnung legt das Suchfenster fest. Die Zeitdifferenzen berechnet X6 aus den Signalen.

## Quellen und öffentliche Ergebnisse

Die Quelldaten stammen vom **Schweizerischen Erdbebendienst (SED) an der ETH Zürich**, National Seismic Networks of Switzerland, Netzwerkcode CH. Im FDSN-Katalog lautet die Ereignis-ID `smi:ch.ethz.sed/sc3a/2017epaqsp`.

- [Netzwerk-DOI 10.12686/sed/networks/ch](https://doi.org/10.12686/sed/networks/ch) und [SED-Netzwerkbeschreibung](https://networks.seismo.ethz.ch/en/networks/ch/)
- [SED-Ereignisbericht](https://www.seismo.ethz.ch/en/news-and-services/bssed-imagewithtext/Home-Summary-of-the-magnitude-4.6-Urnerboden-Earthquake-00002/) und [SED-FDSN-Webdienste](https://www.seismo.ethz.ch/en/knowledge/earthquake-data-and-analysis-tools/fdsn-web-services/)
- [Hinweise zum Datenzugang und zur Zitierung](https://seismo.ethz.ch/de/knowledge/earthquake-data-and-analysis-tools/waveform-data/) und [Nutzungshinweise des SED](https://www.seismo.ethz.ch/de/service/Disclaimer/)

Das Netz ist als offen gekennzeichnet. In den geprüften Netzwerk- und DOI-Metadaten ist keine konkrete Lizenz für die Weiterveröffentlichung der Originaldaten bezeichnet. Der SED gestattet die Quellenangabe und Verlinkung und beschreibt Einschränkungen für die Weiterverbreitung seiner Online-Inhalte.

Der lokale Import wertet die offiziellen Antworten im Arbeitsspeicher aus. Vor dem Wellenformabruf prüft er für die ganze gewählte Epoche die ausdrückliche Einstufung als offen auf Netzwerk-, Stations- und Kanalebene. Rohdaten, StationXML, QuakeML, fremde Abbildungen, Logos und einzelne SED-Phasenzeiten werden weder in Git noch in öffentliche Build-Artefakte übernommen. Der Apache-2.0-Lizenzumfang des Projektcodes erstreckt sich nicht auf die SED-Quelldaten.

Das gespeicherte Ergebnis enthält Quellenkennungen, eigene Eingangsprüfsummen und Methodeneinstellungen, drei Paarvergleiche und deren Prüfstatus. Eine Positivliste prüft vor dem Schreiben auch die verschachtelten Felder. Ein Abbruch ersetzt kein vorhandenes Ergebnis. Auf GitHub läuft der Test ohne Zugriff auf Messdaten des SED. Derselbe veröffentlichungsfähige Inhalt bleibt bei einer späteren Zenodo-Archivierung im Repository.

## Reproduzieren

Für die lokale, wissenschaftliche und nicht gewerbliche Nachrechnung im Repository-Hauptverzeichnis mit Python 3.12:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r agent/sed-requirements.txt
python -m agent.sed_three_station
python -m unittest discover -s tests/python -p test_sed_three_station.py -v
```

Jeder Aufruf lädt Ereignis, Instrumentenantworten und die kurzen Messfenster frisch über die öffentliche ETH-Schnittstelle. Gespeichert wird `runs/sed/summary.json`. Ein Vergleich mit `app/causal-stability/sed-data/summary.json` prüft die lokale Auswertung gegen das veröffentlichte Ergebnis. Die drei SHA-256-Werte beziehen sich auf die zeitlich zugeschnittenen, unkalibrierten Abtastwerte als vorzeichenbehaftete 32-Bit-Ganzzahlen in Little-Endian-Reihenfolge. Revisionen im Archiv können spätere Nachläufe verändern.

## Ergebnis des Referenzlaufs

| Stationspaar | 1–5 Hz | 2–8 Hz | 4–12 Hz | Spannweite |
|---|---:|---:|---:|---:|
| LLS → MUO | 2,117 s | 2,142 s | 2,133 s | 25,0 ms |
| LLS → BNALP | 4,683 s | 4,850 s | 4,958 s | 275,0 ms |
| MUO → BNALP | 2,567 s | 2,708 s | 2,825 s | 258,3 ms |

Im lokalen Varianzvergleich bestanden alle neun Stations-/Bandkombinationen die im Verfahren beschriebenen Kontrollen. Der zusätzliche Pegeltest lag bei LLS im ersten Band sowie bei BNALP im zweiten und dritten Band bereits am linken Rand über der Schwelle. Die betroffenen Pegelzeiten wurden verworfen. Das Lab zeigt für jedes Band beide Prüfstatus.

## Verfahren und Aussagegrenze

1. X6 verwendet genau einen bevorzugten Ursprung, das feste Ereignis und je eine zugeordnete manuelle Pg-Markierung auf CH.STATION..HHZ. Das Wellenformfenster reicht von 60 Sekunden vor bis 35 Sekunden nach der Katalog-Ursprungszeit. Lücken, Überlappungen, fehlende Ränder, mehrdeutige Epochen und unzureichende Instrumentenantworten stoppen den Lauf.
2. Die vollständige Instrumentenantwort wird mit ObsPy auf Bodengeschwindigkeit in m/s entfernt. Der Frequenzvorfilter liegt bei 0,3 / 0,6 / 15 / 20 Hz. Der anschliessende Butterworth-Bandpass vierter Ordnung läuft als Vorwärtsfilter getrennt in 1–5, 2–8 und 4–12 Hz. Die FFT-basierte Antwortkorrektur kann Signalenergie zeitlich verschieben. Die Filterlaufzeit und die Form des Signals gehören zur beobachteten Empfindlichkeit.
3. Für jedes Band untersucht X6 einen Abschnitt von ±1 s um die manuelle Markierung. Für jede Teilung k mit wenigstens 0,10 s Daten auf jeder Seite wird k log(Varianz vorher) + (n−k) log(Varianz nachher) berechnet. Das Minimum markiert den ersten Abtastwert im zweiten Segment. Die Teilung muss innerhalb von ±0,85 s liegen. Die Varianz danach muss mindestens das Neunfache der Varianz davor betragen. Der RMS-Pegel im zweiten Segment muss mindestens das Sechsfache des Rauschniveaus erreichen. Das Rauschniveau ist der Median der nachlaufenden 0,10-s-RMS-Werte von 45 bis 15 Sekunden vor der Ursprungszeit. Ein gültiger Einsatz mit demselben Verfahren im separaten Ruhefenster von −12 bis −10 s sperrt das betreffende Ergebnis.
4. Zusätzlich bleibt der zuerst erprobte Pegeltest ausgewiesen. Er prüft, ob 0,08 s lang die Schwelle von sechs Rauschpegeln überschritten wird. Bereits am linken Rand aktive Auslösungen werden ausdrücklich markiert. Solche Fälle in der Erprobung waren Anlass für den anschliessenden lokalen Varianzvergleich. Beide Verfahren wurden am selben Ereignis untersucht.
5. Angezeigt wird die Zeit am zweiten Standort abzüglich der Zeit am ersten. Gibt es für eine Station im Varianzverfahren keinen belastbaren Einsatz, bleibt die betreffende Paardifferenz offen. Die Spannweite wird nur bei drei verfügbaren Bandwerten berechnet. Die drei Paare teilen sich dieselben Stationszeiten und bilden keine drei unabhängigen Wiederholungen.

Die Tabelle beschreibt die Filterabhängigkeit des automatischen Einsatzes für dieses Ereignis. Die absoluten Laufzeiten, eine statistische Unsicherheit oder die allgemeine Güte eines Phasenpickers werden damit nicht bestimmt. Bei 120 Hz entspricht ein Abtastschritt 8,33 ms. Die protokollierten Dezimalstellen dienen der Nachrechnung.
