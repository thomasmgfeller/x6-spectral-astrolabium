# X6-QED · Klassenerreichbarkeit nach §17

**4. November 2026 · DEVELOPMENT · CAL und C0-VALIDATION auf HOLD**

Für 55 von 1.679 verschiedenen nichtleeren Syndromen erreicht jeder lokale Cluster beide Observablenklassen. In diesen Fällen kann der spätere Decoder die Klassenminima vergleichen. Die Zahl setzt die unten festgelegte Lokalitätskonvention und die syntaktische Zuordnung der Observable-Masken voraus.

## Geprüfte Eingaben

Der [Repository-Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/203a1849e3b09cfbdb1d38b388ee0c57efa14991) enthält einen d=5-Kontrollgraphen mit genau einer möglichen Fehlerkante. Für das aktive Syndrom D108 liefert diese Kante ausschließlich Observablenklasse 1. §17.2 ergibt HOLD. Der Kontrollgraph ist in main_fixture.json enthalten.

Für den weitergehenden Versuch wurde ein eigener Entwicklungsschaltkreis festgelegt. Stim 1.16.0 erzeugt einen rotierten X-Speicher der Distanz 5 mit fünf Runden und 120 Detektoren. Die Depolarisationswahrscheinlichkeit nach Clifford-Gattern beträgt 0,005. Alle übrigen Rauschparameter stehen auf den Stim-Standardwerten null. Diese Parameter entsprechen dem [d=5-Beispiel von PyMatching](https://github.com/oscarhiggott/PyMatching/blob/master/src/pymatching/matching.py). PyMatching wurde für diese Strukturauszählung nicht als Decoder ausgeführt.

Das mit getrennten graphartigen Komponenten erzeugte DEM enthält 1.958 ausgeführte Fehlerterme mit 3.718 Komponenten. 1.456 Terme haben mehrere Komponenten. Jeder Term wurde einzeln als ganzes Ereignis ausgewertet. Nach Zusammenfassung gleicher Detektorvektoren ergeben sich 1.679 verschiedene nichtleere Syndrome. Ein leeres Eingabesyndrom wurde gesondert als Kontrolle berücksichtigt. Mehrfachfehler-Shots und stochastische Auftretenshäufigkeiten sind nicht Gegenstand dieser Auszählung.

## Lokale Regel

Die genauen Festlegungen stehen in protocol.json. Aktive Detektoren mit höchstens zwei Detektorhops Abstand werden transitiv zu Clustern zusammengefasst. Die Boundary dient ausschließlich als Endpunkt. Detektorpaare können einfache Pfade bis vier Kanten verwenden, ein Boundary-Pfad umfasst höchstens zwei Kanten einschließlich der Abschlusskante. Im Inneren eines Pfades darf kein dritter aktiver Detektor liegen. Ein aktiver Endpunkt darf genau einmal zugeordnet werden. Pfade können sich überlappen. Erklärungen mit derselben Parität sind für die Klassenexistenz gleichwertig. Alle beobachteten Cluster hatten Größe 1 oder 2 und lagen unter der Grenze 8.

Für jeden Cluster werden die möglichen Paritäten aller erlaubten Zuordnungen aufgezählt. Ein nichtleeres Syndrom erreicht den Margenvergleich nur, wenn **jeder** Cluster beide Klassen erreicht. Das ist eine explizite Auslegung der HOLD-Fortpflanzung im Entwicklungsversuch. Die bloße Existenz beider XOR-Paritäten für den gesamten Shot genügt dafür nicht. Es wurden keine Pfadkosten, Entscheidungsgrenzen oder logischen Fehlerraten bewertet.

## Ergebnis für die syntaktische Zuordnung

| Anzahl aktiver Detektoren | Verschiedene Syndrome | Jeder Cluster erreicht beide Klassen | Durch Einzelklasse blockiert |
|---:|---:|---:|---:|
| 1 | 72 | 0 | 72 |
| 2 | 506 | 55 | 451 |
| 3 | 480 | 0 | 480 |
| 4 | 621 | 0 | 621 |
| **Gesamt** | **1.679** | **55** | **1.624** |

Für alle Einträge existiert mindestens eine lokale Erklärung je Cluster. 254 Syndrome besitzen beide XOR-Paritäten auf Shot-Ebene. 199 davon haben zusätzlich einen Cluster mit nur einer Klasse. Die 55 verbleibenden Syndrome enthalten je zwei aktive Detektoren ohne direkte Boundary-Kante. Unter allen 167 Syndromen ohne direkt randbenachbarten aktiven Detektor sind das 55/167, unter 1.512 randbenachbarten Syndromen 0/1.512. Diese Randbezeichnung beschreibt ausschließlich die Graphadjazenz.

Die Datei **results/development_syndromes.csv** nennt Detektor-IDs, Cluster, erreichbare Klassen, Randlage und Entscheidung für jedes Syndrom. Die Filter `policy=syntactic` und `section17=ALL_CLUSTERS_BOTH` ergeben die 55 Fälle. Beispielsweise enthält diese Auswahl D3/D6 und D3/D7. `reachable_per_cluster=01` bezeichnet die Menge aus 0 und 1. Die Spalte `whole_source_count` zählt Fehlerterme, die dasselbe Syndrom erzeugen. Sie ist keine Wahrscheinlichkeit.

## Empfindlichkeit der Separator-Zuordnung

Die primäre Auszählung folgt X.9. Im gezielten Vergleich erhält jeweils die erste Teilkante das gesamte Observable-XOR der Quelle, die übrigen erhalten null. Detektorkomponenten, Quellwahrscheinlichkeiten und die gesamte Wirkung jedes Quellereignisses bleiben gleich. Beide XOR-Invarianten werden für jede Quelle geprüft. Für den Suchraum ändern sich die lokal verfügbaren Masken. Es ergeben sich 563 verschiedene Kombinationen aus Endpunkten und Maske gegenüber 502 in der primären Variante. Die Rechnung fasst gleiche Endpunkte mit gleicher Maske nur für die Existenzprüfung zusammen. Die Einzelquellen sind in results/development_sources.json mit Wahrscheinlichkeit, Komponentenzuordnung und Maske enthalten.

Unter dieser gezielten Änderung kommen 979 von 1.679 Syndromen durch §17. Alle 55 ursprünglichen Fälle sind enthalten. 924 Fälle kommen hinzu. Das macht die Repräsentationsabhängigkeit für dieses Modell nachprüfbar. Die alternative Zuordnung dient ausschließlich der Empfindlichkeitsanalyse. Die Auszählung begründet keine Auswahl des Kandidaten anhand seiner höheren Quote.

## Reproduktion und Laufzeit

Benötigt werden Python 3.12 und Stim 1.16.0. Nach der Installation der Abhängigkeit kann das Paket lokal wiederholt werden.

```sh
python -m pip install stim==1.16.0
python measure.py replay
diff results/summary.json replay/summary.json
diff results/development_syndromes.csv replay/development_syndromes.csv
```

measure.py verwendet eine vollständige Tiefensuche für einfache Pfade und eine rekursive Paarungssuche. verify.py konstruiert Pfade durch Zusammenfügen zweier Halbpfade und zählt Paarungsmengen ohne die Rekursion des ersten Verfahrens explizit auf. Beide Verfahren erhielten denselben ausgelesenen Graphen. Für **jedes** Eingabesyndrom und beide Konventionen stimmten Cluster und Klassenmengen überein. Spielzeugkontrollen prüfen zusätzlich einen Fall ohne Paarung, den Separator-Gegenfall, die terminale Boundary und XOR-Aufhebung. Die Gegenprüfung betrifft die Suchlogik, sie verwendet denselben Stim-Parser und dieselben Lokalitätsannahmen.

Die erste Rechnung dauerte intern 1,326 s, mit Python-Start und Import rund 1,58 s. Drei frische Prozesswiederholungen dauerten 1,20, 1,29 und 1,37 s. Der Median beträgt rund 1,29 s. Alle Ergebnisdateien außer der Zeitmessung waren byteidentisch. Die Laufzeiten beziehen sich auf diesen Rechner und schließen den Bau des Graphen, beide Maskenzuordnungen, beide Suchverfahren und die Ausgabe ein. Die Erstinstallation von Stim und die Vorbereitung des Versuchs sind ausgenommen.

Die Ergebnisse sind vollständige Anzahlen für die angegebenen endlichen Eingangsmengen. Die PASS-Quote und das Fehlerrisiko auf zufälligen Shots erfordern eine getrennte Stichprobe, eingefrorene Entscheidungen und ein eigenes Auswertungsprotokoll.
