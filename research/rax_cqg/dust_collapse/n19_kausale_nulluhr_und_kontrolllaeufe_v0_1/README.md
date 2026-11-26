# N19 · Wie erhält der Empfänger seine Nulluhr?

Der Einbit-Leser aus [PR 394](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/394) unterscheidet drei Quellen am N19-Staubball. Dafür brauchten der Empfänger an Knoten 18 und der Speicher an Knoten 7 bisher den Wert der Uhr, den der unbelastete Hintergrund bei ausgeschalteter Quelle hätte. Dieses Paket prüft, welche früheren Daten den Wert festlegen und wie eine Eichung am angeschlossenen Gerät die Auslese ermöglicht. Alle Uhren, Impulse und Ablesungen in den Tests stammen aus stationären N19-Modelllösungen.

## Was der Sender vor der Pulswahl wissen kann

Zwei quellfreie Lösungen stimmen an sämtlichen Knoten im strikten Vorlauf des Senders 16 überein (0, 1, 2, 15). Auch am Sender selbst stimmen Uhr, Gewicht und ungepulster Strom überein, ebenso die frühen Randdaten und die vier Anfangsimpulse. Trotzdem zeigt die unbelastete Empfangsuhr einmal 42 180 125 645 und einmal 42 181 125 645. Bei einem Rasterschritt von 2·10⁻¹² hat jeder Schätzer aus diesen gemeinsamen Daten in mindestens einem Fall einen absoluten Fehler von mindestens 10⁻⁶. Das folgt aus der halben Distanz der beiden möglichen Werte. Der Nachweis benutzt zwei zulässige Lösungen des Modells sowie die linearen Erhaltungsbedingungen des archivierten Lösers.

Selbst nach der Pulswahl können die vorhandenen Anzeigen mehrdeutig sein. Auf zwei unterschiedlichen zulässigen Hintergründen erzeugen eine positive Quelle und die Nullquelle dasselbe vollständige Wort aus fünf Ziffern an 18 und sieben Ziffern an 7. Bei einer gemeinsamen Skalierung der Hintergrundgewichte ausserhalb des Anfangskragens um 1/8 genügt ein maximaler normierter Nachimpuls von 61,241332. Geräteweg, Trägheit und Anzeigevorschrift sind gleich. Die Sendergewichte und ein Teil der frühen Randimpulse unterscheiden diese beiden Hintergründe. Das Beispiel beschreibt einen Beobachter, der nur die genannten Anzeigen erhält.

## Zwei Möglichkeiten zur Eichung

**Zwei frühere Knotenuhren.** Mit unabhängig verfügbaren Werten u = Y₁₅ und h = Y₁₇ folgt der unbelastete Referenzwert T₀ aus den quellfreien Dichtegleichungen. Setze s = (u²−6)/(2(u+3)), b = 16+9u−s−h und c = 35−9u²+s²+h². Die im Empfangsfenster liegende Wurzel ist T₀ = c/(−b+√(b²−c)). Beide Knoten liegen vor dem Empfänger und dem Speicher. Knoten 17 ist mit dem Sender 16 kausal unvergleichbar. Beide Knotenuhren tragen im Modell Staubgewicht null. Für eine Messung braucht es daher eine unabhängige Aufnahme und Übertragung dieser Werte.

Auf dem ganzen untersuchten Rechteck beträgt die gemeinsame analoge Fehlergrenze bei Raster 10⁻¹² und verschwindendem Offset weniger als 7,985·10⁻¹². Für Raster 2·10⁻¹² und Offset bis 10⁻¹² je Uhr steigt sie auf 3,194·10⁻¹¹. Im zweiten Fall reichen die Intervalle bei Impulsgrenze 96 für alle 192 digitalen Entscheidungen. In 384 zusätzlichen, direkt durchgerechneten Randproben lieferten die gerundeten Eingaben ebenfalls das richtige Quelllabel.

**Drei frühere Nullablesungen mit angeschlossenem Gerät.** Der Empfänger bestimmt vor dem nächsten Puls einen Referenzcode B aus drei gleich weit auseinanderliegenden Kontrollläufen mit ausgeschalteter Quelle. Für die wahren, bereits digitalisierten Nullwerte muss eine unabhängig festgelegte Schranke |Nᵢ₊₁−2Nᵢ+Nᵢ₋₁| ≤ C bis zum Zielzeitpunkt gelten. Die Unsicherheit jeder einzelnen Kontrolle darf separat angegeben werden. Der Leser bestimmt die engste ganzzahlige Intervallhülle für den nächsten Nullwert und verwendet ihre gerundete Mitte. Eine unabhängige vollständige Enumeration prüft das Verfahren in 10 125 kleinen Fällen. Drei Kontrollen allein begründen keinen Wert für C.

Bei der Auslese setzt der Empfänger das Bit, wenn sein Uhrwert mehr als 125 Schritte von B entfernt liegt. Bei gesetztem Bit liefert die vorzeichenbehaftete Differenz aus lokaler Uhr, drittem Zeiger, dessen Anfangswert und B am Speicher das Pulsvorzeichen. Ein gemeinsames B und die Zuordnung zu Gerät und Lauf sind vorab vereinbart. Sowohl die drei Zeigerimpulse als auch die zulässigen Geräteabweichungen dürfen bei Null- und Signallauf voneinander abweichen. Der Vergleich gilt für dieselbe native Hintergrundpräparation am Zielzeitpunkt.

| Vorab geprüfte Impulsgrenze m | Stammfamilien korrekt | Zusätzliche Familien korrekt | Zulässiger Zusatzfehler von B in Schritten, einschliesslich Registerkopie |
|---:|---:|---:|---:|
| 64 | 144/144 | 48/48 | 38 |
| 96 | 144/144 | 48/48 | 38 |
| 112 | 144/144 | 48/48 | 11 |

m begrenzt den Betrag jedes der drei Nachimpulse in Einheiten κ₀V mit κ₀=10⁻¹¹ und V=10⁻¹⁴. Eine Familie umfasst den ganzen Impulsbereich, die zulässigen Zeigeranfangslagen und den Geräteabgleich. Die 144 Stammfamilien ergeben sich aus zwölf Hintergründen, zwei Wegen, zwei Trägheiten und drei Quellen. Vier weitere Hintergründe aus PR 394 ergeben 48 zusätzliche Familien. Diese Zahlen zählen Parameterfamilien, keine unabhängigen Experimente.

## Zurückgehaltene vierte Nullablesung

Im synthetischen Beispiel lauten die drei früheren Ziffern 42 180 625 598, 42 180 625 602 und 42 180 625 610. Mit C=3 und einem Schritt Unsicherheit je Ablesung ergibt sich B=42 180 625 617 mit höchstens fünf Schritten Fehler. Der unabhängig berechnete vierte Nulllauf liefert 42 180 625 615. Alle drei Quellfälle werden mit der zuvor bestimmten Referenz richtig gelesen.

Bei diesem schwachen Gerät liegt die belastete Nullanzeige modellbedingt 30 bis 31 Schritte unter der unbelasteten. Nach dieser Korrektur liefern die beiden Knotenuhren und die Zeitreihe den gemeinsamen Bereich [42 180 625 612, 42 180 625 619]. Eine zweite Gegenprobe verschiebt den Hintergrund unmittelbar nach der dritten Kontrolle um 10⁻⁶. Die Zeitreihe meldet darauf für eine Nullquelle einen positiven Puls. Die unabhängigen Knotenuhren liefern jetzt ein disjunktes Intervall und decken den Sprung auf. Diese Gegenprobe zeigt, was ein bei allen drei früheren Messungen unsichtbarer Driftwechsel bewirken kann.

## Die ganzzahlige Grenze des Lesers mit exakter Eichziffer

Eine ergänzende Rechnung nach dem vorab festgelegten Test bei m=112 prüft die ganzzahligen Stufen 113 bis 118. Für eine exakte, zum Hintergrund passende belastete Nullziffer sind bis m=117 alle 192 Familien abgedeckt. Die Rechnung berücksichtigt, dass die beiden Ziffern der dritten Zeigerspur dieselbe Anfangslage enthalten. Für jede Phase q liegt Q(q+A)−Q(q+B) zwischen Abrundung und Aufrundung von (A−B)/Rasterschritt. Bei 117 beträgt die kleinste zertifizierte Zusatzreserve null Schritte. Die konservative Laufsoftware verwendet weiterhin die in der Tabelle aufgeführten, vorab geprüften Grenzen.

Bei m=118 liefert das schwache Viertelgerät auf dem positiven Transportweg für einen positiven und für einen negativen Puls jeweils ein gesetztes Empfangsbit und exakt null als späte Vorzeichenziffer. Beide werden als unentscheidbar zurückgewiesen. Die übrigen beiden Zeigerimpulse, alle drei Anfangslagen und der Ableseoffset sind für diese Gegenbeispiele null. Damit ist 117 unter den ganzzahligen Impulsgrenzen die letzte für diese Ausleseregel und diese Modellfamilien mit exakter Geräte-Nullziffer. Eine Schwelle für beliebige Leser oder für reellwertige Zwischenstufen erfordert eine eigene Untersuchung.

## Reproduktion und Messstand

Nach dem Entpacken lässt sich die gesamte Rechnung mit Python 3.10 oder neuer und der Standardbibliothek offline wiederholen. Die drei lokalen Plan-Hashes dokumentieren die Redaktionsstände. Die ergänzende Grenzsuche bei 113 bis 118 ist explorativ. Die frühere Version ist mit Lizenz und festem SHA-256 im Paket enthalten.

    python3 -B pruefen.py
    python3 -B referenzprotokoll.py eichen Beispiel_Nullserie.json > bezug.json
    python3 -B referenzprotokoll.py senden bezug.json Beispiel_Empfang.json > paket.json
    python3 -B referenzprotokoll.py lesen bezug.json Beispiel_Speicher.json paket.json
    python3 -B referenzprotokoll.py eichen Messstand.json

Der vollständige Lauf prüft die Prüfsummen, reproduziert den archivierten Vorgänger und vergleicht die acht neuen Ergebnis- und Beispiel-Dateien bytegenau. Die Software prüft Zeitreihenfolge, Fehlerbudget und Zuordnung der Daten. Eine Kennung für Takt, Drift oder Geräteeichung dokumentiert den angegebenen Bezug. Die unabhängige Begründung der Schranken und die Herkunft der Messwerte sind im jeweiligen Versuch zu belegen.

Für den empirischen Anschluss fehlen hier unabhängig dokumentierte Nullmessungen. Der nächste aussagekräftige Versuch ist eine Serie am selben Aufbau mit festem Takt, drei abgeschlossenen Nullmessungen, einer vorher zurückgehaltenen vierten Nullmessung und unabhängig bestimmter Drift- und Impulsgrenze. Anschliessend folgt die verdeckte Pulswahl mit geprüfter Übertragung des Bits. **Physische Eichmessungen im Paket: 0. Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.**
