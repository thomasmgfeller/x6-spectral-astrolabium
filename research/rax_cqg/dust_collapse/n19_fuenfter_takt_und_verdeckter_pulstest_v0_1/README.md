# N19 · Die Nulluhr für den fünften Takt

Nach der vierten, vorab zurückgehaltenen Nullablesung kann der Empfänger im dokumentierten N19-Beispiel den Referenzcode des **anschliessenden** Pulses auf sechs Schritte eingrenzen. Vor der vierten Ablesung sind es zwölf Schritte. Bei der normierten Nachimpulsgrenze 112 erlaubt der geprüfte Leser elf. Alle drei verdeckt ausgewerteten Modellquellen wurden erkannt. Ein nachträglicher Sprung des Hintergrunds erzeugte mit der Zeitreihe allein ein falsches positives Signal. Die Gegenprüfung mit den Uhren an 15 und 17 hielt die Ausgabe an.

## Was die Werte bedeuten

Die laufenden Indizes sind 7 bis 11. An 7, 8 und 9 liegen die drei Kontrollablesungen aus PR 395 vor. Index 10 ist der getrennte Nulllauf. Index 11 ist jeweils der Puls oder die Nullquelle. Ein Schritt entspricht 2·10⁻¹² in der Modelluhr. Gesucht ist der digitalisierte Nullwert **mit angeschlossenem Gerät**. Die vierte Ablesung hat den Wert 42 180 625 615. Ihre im Haupttest angenommene Unsicherheit beträgt einen Schritt.

| Verfügbare Daten vor dem Puls | Exakte äusserste Nullcodes für Index 11 | Gewählte Mitte B | Kleinster garantierter Fehler | Vergleich mit Budget 11 |
|---|---|---:|---:|---|
| Drei frühere Kontrollen | 42 180 625 612 bis 42 180 625 636 | 42 180 625 624 | 12 | überschritten |
| Zusätzlich vierte Kontrolle mit ±1 Schritt | 42 180 625 615 bis 42 180 625 626 | 42 180 625 620 | 6 | 5 Schritte Reserve |
| Zusätzlich vierte Kontrolle mit exakter Ablesung | 42 180 625 617 bis 42 180 625 624 | 42 180 625 620 | 4 | 7 Schritte Reserve |

Diese Grenzen gelten für alle ganzzahligen Folgen, die mit den abgelesenen Fehlerbändern und der vorab festgelegten Schranke für die zweite Differenz C=3 vereinbar sind. Für ungerade Spannweite verwendet der Leser die untere der beiden gleich guten Mitten. Für jedes Intervall enthält daten/Ergebnisse.json zwei vollständige zulässige Folgen, welche die Endpunkte erreichen. Die Folge am unteren Ende des ersten Intervalls endet zum Beispiel mit 609, 612, 612, diejenige am oberen Ende mit 611, 622, 636 (jeweils letzte drei Stellen). Aus denselben ersten drei Messungen kann deshalb kein ganzzahliger Schätzer für Takt 11 weniger als zwölf Schritte garantieren. Das Überschreiten des dokumentierten Budgets lässt für sich allein offen, welche konkreten Quellenentscheidungen noch gelingen.

### Rechenweg

Schreibe x,y,z,w,v für die fünf wahren digitalen Nullcodes und [Lᵢ,Uᵢ] für die ersten drei Fehlerbänder. Für ein festes w und z muss y in allen drei folgenden Intervallen liegen.

1. [L₂,U₂]
2. [ceil((z+L₁−C)/2), floor((z+U₁+C)/2)]
3. [2z−w−C, 2z−w+C]

Diese Bedingungen sind notwendig und hinreichend. Die zweite Bedingung entsteht durch Elimination von x, die dritte aus |w−2z+y|≤C. Zusätzlich gilt L₃≤z≤U₃. Mit z=2s+p und p gleich 0 oder 1 werden alle Grenzen affin in s. Die neun Vergleiche „untere Grenze ≤ obere Grenze“ liefern die kleinste und grösste zulässige dritte Ziffer für jedes erreichbare w. Daraus folgen die Endpunkte für v als 2w−max(z)−C und 2w−min(z)+C. Die Extremwerte über alle erlaubten vierten Ziffern bestimmen den minimaximalen ganzzahligen Fehler durch Aufrunden der halben Spannweite.

Die vierte Kontrolle wird nur angenommen, wenn **jede** Ziffer ihres angegebenen Fehlerbandes erreichbar ist. Teilweise Überdeckung wird als unentscheidbar protokolliert. Der unabhängige Vergleich mit vollständigem Durchzählen umfasste 5 184 kleine ganzzahlige Fälle. In 278 davon hatte die Menge der möglichen vierten Ziffern Lücken innerhalb ihrer Intervallhülle. Bei C=0 und den ersten drei Bändern [−2,−2], [−2,−1], [−2,0] sind für die vierte Ziffer nur −2 und 1 möglich.

## Stationäres N19-Modell und verdeckte Quellenwahl

Für die Kontrolle wurde der Viertelhintergrund aus PR 395 auf dem positiven Transportweg mit schwachem Gerät verwendet. Die native Referenz verschiebt sich je Takt um sechs Rasterschritte, die Abgleichabweichung ist −κ₀. Der Solver kontrolliert die stationären Gleichungen und schliesst an allen fünf Zeitpunkten jeden der drei normierten Nachimpulse im vollen Intervall [−112,112] ein. Beim Gerät mit abgeschalteter Quelle ergeben sich unabhängig von der Folge der einzelnen Impulse eindeutig die Endziffern 597, 603, 609, 615 und 621. Im Modell ist damit die zweite Differenz überall null. Der Zeitreihenleser erhielt ausschliesslich die Kontrolldaten mit C=3. Die physische Übertragbarkeit der Drift- und Impulsgrenzen erfordert eine eigenständige Eichung.

Der separat berechnete fünfte Nullcode ist 42 180 625 621, einen Schritt über der festgelegten Referenz. Für diesen neuen Zielhintergrund wurde das Fehlerbudget über den gesamten Impulsbereich neu gerechnet. Mit exakter belasteter Referenz liegt die späte Vorzeichenziffer bei negativer Quelle im Intervall [−548,−12], bei positiver Quelle in [12,548]. Die Empfangsschwelle bleibt 125. Bei der Nullquelle liegt die frühe Differenz in [−1,1]. Ein Referenzfehler bis elf erhält alle Entscheidungen dieser Familie. Der Fehlerradius der konkreten Zeitprognose beträgt sechs.

Die drei Läufe A, B und C sind Alternativen desselben fünften Takts, jeweils mit eigener Kennung und denselben vier Nullkontrollen. Eine zufällig permutierte Quellenliste und ein zufälliger geheimer Zusatzwert wurden vor der Auswertung mit SHA-256 gebunden. Die Lesesoftware bekam getrennte Dateien für Referenz, Empfangsuhr, Speicher und empfangenes Bit. Das Empfangsbit wurde gegen das separat rekonstruierte Sendebit geprüft. Erst nach Speichern der Entscheidungen wurde die Quellenzuordnung beim Auswerten geöffnet. Die mitgelieferte Öffnung ermöglicht die Wiederholung. Es handelt sich um einen verblindeten Softwareablauf mit modellierten Beobachtungen, ohne externe Zeitbeglaubigung und ohne statistische Aussage über eine Trefferquote an Geräten.

| Modelllauf | Empfangenes Ergebnis nach Öffnung |
|---|---|
| A | Negativer Puls richtig erkannt |
| B | Nullquelle richtig erkannt |
| C | Positiver Puls richtig erkannt |

## Geometrische Gegenprobe am fünften Takt

Die Knotenuhren 15 und 17 liegen kausal vor Empfänger 18 und Speicher 7. Knoten 17 ist mit Sender 16 unvergleichbar. Beim geschützten Leser wird der Vergleich daher vor der **Ausgabe des Quelllabels** benötigt. Der neue Leser berücksichtigt die Belastungskorrektur aus PR 395. Die Zulässigkeit dieser Korrektur ist für beide hier getesteten Zielhintergründe separat mit dem Solver geprüft. Der im Test verwendete Voruhrenraster ist 10⁻¹² mit verschwindendem Offset.

Auf dem stabilen Hintergrund überlappen die beiden Vorhersagen im Bereich 42 180 625 617 bis 42 180 625 626. Nach einem Sprung um 10⁻⁶ unmittelbar nach der vierten Kontrolle liefert die Geometrie 42 181 125 617 bis 42 181 125 626. Die Zeitreihe liefert weiter 42 180 625 615 bis 42 180 625 626. Bei ausgeschalteter Quelle meldet die alleinige Zeitauswertung nun fälschlich einen positiven Puls. Der geschützte Leser gibt bei disjunkten Referenzen kein Quelllabel aus. Bei überlappenden Referenzen prüft er zusätzlich, dass das ganze geometrische Band innerhalb der elf Schritte um B liegt. Ein einzelner bestandener Vergleich garantiert keine allgemeine Erkennung von Driftwechseln.

## Offline nachrechnen

Python 3.10 oder neuer mit Standardbibliothek genügt. Aus dem entpackten Studienordner laufen die folgenden Befehle.

    python3 -B pruefen.py
    python3 -B pruefen.py --mit-vorgaenger

Der erste Befehl prüft die Prüfsummen, wertet die drei anonymen Datensätze aus und reproduziert die neuen Rohdaten und Ergebnisse bytegenau. Der zweite Befehl wiederholt zusätzlich die archivierte Vorgängerkette. Einzelaufrufe mit den Eingabedateien der Studie sind ebenfalls möglich.

    python3 -B folgetakt.py referenz daten/Kontrollen.json daten/Vierte_Null.json Puls-A
    python3 -B folgetakt.py lesen daten/A_Referenz.json daten/A_receiver.json daten/A_memory.json daten/A_received.json
    python3 -B voruhren.py daten/A_Referenz.json daten/Sprung_Voruhren.json daten/Sprung_receiver.json daten/Sprung_memory.json daten/Sprung_received.json

Der letzte Befehl liefert die erwartete Sperre DISJOINT_REFERENCES mit Rückgabecode 2. Die übrigen Negativkontrollen decken unter anderem ein gekipptes Bit, ein fremdes Paket, ein falsches Zeitfenster und eine geänderte Quellenöffnung ab.

## Anschluss an Messdaten

Am realen Aufbau sind vor der Auswertung der Pulsdaten die Umrechnung in Modellziffern, der Aufbau und der Abgleich, die Unsicherheiten der Anzeigen, ein gleichmässiger Takt sowie die unabhängigen Belege für Drift- und Impulsgrenzen zu dokumentieren. Dasselbe Gerät muss drei zeitgestempelte Nullkontrollen sowie eine vierte, bis zur Festlegung der Vorhersage zurückgehaltene Nullablesung liefern. Danach wird die Referenz für den fünften Takt vor der Pulswahl festgeschrieben. Zur Prüfung der Übertragung gehören Sende- und Empfangsprotokoll des Bits sowie die Speicheranzeige zur selben Laufkennung. Für die geometrisch geschützte Auswertung braucht es zusätzlich eine unabhängige Auslese und Übertragung der Voruhren. In der Modellgeometrie tragen diese Knoten kein Staubgewicht.

Physische Nullmessungen in diesem Paket: 0. Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN. Die Auslese klassischer N19-Quellen entscheidet weder die Dynamik des kollabierenden Staubballs noch seine Fortsetzung an der klassischen Singularität.

Ausgangspunkt und Originalquellen sind im mitgelieferten Offline-Archiv erhalten. [PR 395 auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/395)
