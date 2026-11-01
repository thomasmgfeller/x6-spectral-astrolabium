# Kann X6 filterempfindliche Zeitversätze vorab erkennen?

**Ergebnis des zeitlich getrennten Archivtests: Ein Vorteil der X6-Freigaberegel ist nicht nachgewiesen.** Bei elf Beben blieben neun von X6 ausgewählte Stationspaare innerhalb des 100-ms-Budgets, bei der SNR-Regel sieben. Der beobachtete Unterschied lässt sich auf zwei Beben zurückführen. In sieben Fällen bestanden beide Regeln und in zwei Fällen bestand keine der beiden Regeln.

| Freigaberegel | Freigaben | Spannweite ≤100 ms | Spannweite >100 ms | Kontrolle unbestimmt | Fehlfreigaben gemäss Vertrag |
|---|---:|---:|---:|---:|---:|
| X6-Suchfenster | 11 | 9 | 1 | 1 | 2 |
| Signal/Rauschen | 11 | 7 | 3 | 1 | 4 |

Die Regeln wählten in vier von elf Fällen dasselbe Paar. Bei einem Beben war im Referenzband nur ein Paar verfügbar. Im Zeitraum 2018–2025 wurden 34 Katalogkandidaten aus 16 Halbjahresblöcken anhand der festgelegten Metadatenregel geprüft. Fünf Blöcke lieferten unter dieser Auswahlregel kein Beben mit geeigneten Pg-Markierungen. Die geforderten zwölf auswertbaren Ereignisse wurden verfehlt. Für die zwei unterschiedlichen Bestehensentscheidungen ergibt der vorab festgelegte einseitige exakte Vorzeichentest p = 0,25 (Schwelle 0,05). Die Auswertung belegt weder eine Überlegenheit noch Gleichwertigkeit der beiden Regeln.

## Eingefrorene Entscheidungen pro Beben

Die Tabelle enthält eigene abgeleitete Filterspannweiten in Millisekunden, gerundet zur Darstellung. Ein Strich kennzeichnet einen unbestimmbaren Kontrollpick. Für das Bestehen wurde mit der im Vertrag festgelegten Mikrosekundenrundung gerechnet.

| Kalenderhalbjahr | X6-Paar | X6-Spannweite | SNR-Paar | SNR-Spannweite |
|---|---|---:|---|---:|
| 2018-H1 | LLS-MUO | 25,0 | MUO-BNALP | 173,3 |
| 2018-H2 | MUO-BNALP | 145,0 | LLS-MUO | 141,7 |
| 2019-H1 | LLS-BNALP | 18,3 | MUO-BNALP | 65,0 |
| 2019-H2 | LLS-MUO | 23,3 | MUO-BNALP | 130,0 |
| 2020-H1 | MUO-BNALP | 80,0 | LLS-BNALP | 35,0 |
| 2020-H2 | LLS-MUO | 16,7 | LLS-MUO | 16,7 |
| 2021-H1 | LLS-BNALP | 35,0 | LLS-BNALP | 35,0 |
| 2021-H2 | MUO-BNALP | 16,7 | MUO-BNALP | 16,7 |
| 2022-H2 | LLS-BNALP | 15,0 | MUO-BNALP | 15,0 |
| 2023-H2 | MUO-BNALP | – | MUO-BNALP | – |
| 2024-H1 | LLS-BNALP | 10,0 | MUO-BNALP | 60,0 |

## Was X6 vorher wissen durfte

Das Referenzband war 2–8 Hz. Beobachtet wurde die Ankunft der regionalen Pg-Welle in einem Fenster rund um die manuelle SED-Markierung. Beide Auswahlregeln hatten denselben Pool von Stationspaaren mit gültigen Referenzpicks. X6 bevorzugte das Paar, dessen Referenzzeitdifferenz beim Verschieben der Suchfenster um ±0,15 s am wenigsten schwanken konnte. Die SNR-Regel bevorzugte das Paar mit dem grösseren Signal-Rausch-Verhältnis an seiner schwächeren Station. Die Vorhersagen wurden mitsamt den Eingangsprüfsummen separat in Git eingefroren. Erst danach wurden die zusätzlichen Bänder 1–5 und 4–12 Hz ausgewertet.

Das Budget von 100 ms gilt für die Spannweite über alle drei Bänder. Es entspricht einem 0,10-s-Auswertefenster aus dem Pilotversuch. Eine unbestimmbare Kontrollzeit gilt in der Entscheidung als Fehlfreigabe und wird in der Tabelle separat gezählt. Die drei Stationspaare eines Bebens sind voneinander abhängig. In den Test geht deshalb pro Methode nur ein freigegebenes Paar pro Beben ein.

## Daten, Methode und Reproduktion

Quelle ist der Schweizerische Erdbebendienst an der ETH Zürich, National Seismic Networks of Switzerland, Netz CH. Der historische Test umfasst die Kalenderhalbjahre 2018–2025. Die lokale Wellenverarbeitung folgt dem Urnerboden-Pilot für 2017, mit 120 oder 200 Hz gemäss der Stationsepoche. Die manuelle Pg-Markierung liefert beiden Methoden ein gemeinsames Suchfenster. Das Experiment prüft deshalb weder automatische Ereigniserkennung noch die Genauigkeit gegenüber einem unabhängigen wahren Ankunftszeitpunkt.

- [Netzwerk-DOI](https://doi.org/10.12686/sed/networks/ch) · [SED-Datendienst](https://www.seismo.ethz.ch/en/knowledge/earthquake-data-and-analysis-tools/fdsn-web-services/) · [SED-Nutzungshinweise](https://www.seismo.ethz.ch/de/service/Disclaimer/)
- [Vorab festgelegter Vertrag](CONTRACT.md) · [Katalogauswahl und Ausfälle](cohort.json) · [Vorhersagen im Referenzband](predictions.json) · [Kontrollergebnisse pro Stationspaar](results.json)
- [Methode des Urnerboden-Piloten](../../../docs/research/cspp/causal-stability-lab/SED.md) · [Quellcode](../../../agent/sed_prediction.py)

Der öffentliche Datensatz enthält ausschliesslich eigene abgeleitete Resultate, Eingangsprüfsummen und Quellenkennungen. Die offiziellen Katalogantworten, Wellenformen, Stationsantworten und einzelnen Pg-Zeitpunkte werden im lokalen wissenschaftlichen Lauf im Arbeitsspeicher verarbeitet. Vor einer Wellenformabfrage muss das Netz samt Stations- und Kanalepoche ausdrücklich offen sein. Die CI rechnet ohne SED-Zugriff aus den eingefrorenen Daten nach.

Die Archivprüfung hatte zwei getrennte Phasen. Nach der Referenzberechnung blieben die korrigierten Arbeitsfenster ausschliesslich im RAM, bis die Vorhersagen auf GitHub feststanden. Dann wurde genau die gehashte Vorhersagedatei gegen die Kontrollbänder ausgewertet. Die öffentliche CLI erlaubt ausserdem eine vollständige Nachrechnung mit frischen Abrufen: Sie vergleicht Eingangshashes, Scores und Freigaben vor der Kontrolle. Der Hash schliesst die exakten korrigierten Float64-Werte ein. Ein veränderter Archivstand oder ein Softwarewechsel mit numerisch abweichender Antwortkorrektur macht sich somit ausdrücklich bemerkbar.

Mit Python 3.12 im Hauptverzeichnis:


```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r agent/sed-requirements.txt
python -m agent.sed_prediction verify --prediction-sha256 d03e62ce1eda687670b162864237fb472cf97ac2278984b3a33a95eff815f755
```

Für eine neue lokale Kontrollrechnung legt man eine Kopie der zwei eingefrorenen Eingabedateien in einem neuen Ergebnisverzeichnis an.

```sh
mkdir -p runs/sed-prediction-replay
cp research/sed_filter_prediction/v1/cohort.json research/sed_filter_prediction/v1/predictions.json runs/sed-prediction-replay/
python -m agent.sed_prediction evaluate --directory runs/sed-prediction-replay --prediction-sha256 d03e62ce1eda687670b162864237fb472cf97ac2278984b3a33a95eff815f755
cmp runs/sed-prediction-replay/results.json research/sed_filter_prediction/v1/results.json
```

Für vollständige Neuberechnungen implementiert die CLI zusätzlich die getrennten Stufen `cohort` und `predict`. Quellenrevisionen können zu abweichenden Eingängen führen. Ein bestehender Stage wird nur bei identischem Inhalt akzeptiert.

[Vorabprotokoll in Git](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/43645f701591632541c3e739374bbdc1d7ecc8d7) · [Eingefrorene Vorhersagen vor Öffnung der Kontrollbänder](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/3d711a8cff8bdc70654e9dd83111a762b936934d)
