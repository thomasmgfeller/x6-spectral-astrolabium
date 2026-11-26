# N19 · Welche Eichgenauigkeit braucht die Gegenprobe?

Auf dem untersuchten Viertelhintergrund kann der Leser für den fünften Takt jede freigegebene Quelle über das gesamte Driftintervall −10⁻⁶ bis +10⁻⁶ korrekt unterscheiden. Er braucht dafür zwei aktuelle, unabhängig eingelesene Voruhren und ein den Eingabefehlern entsprechendes geometrisches Intervall. Wie oft er eine Quelle überhaupt freigeben kann, hängt stark von der Eichgenauigkeit ab. Bei einem symmetrischen Offset bis 10⁻¹² an jeder Voruhr gab es im ganzen untersuchten Driftintervall keine Freigabe. Sämtliche Zahlen beziehen sich auf die Modelluhr.

## Ausgangspunkt und Reichweite

Die drei frühen Nullkontrollen und die vierte Nullablesung mit einem Schritt Unsicherheit liefern für Takt 11 das Zeitintervall [42 180 625 615, 42 180 625 626] und seine untere Mitte B = 42 180 625 620. Der Quellleser verwendet die Empfangsschwelle 125 und toleriert elf Schritte Fehler der Referenz. Ein Empfangsschritt ist 2·10⁻¹². Der Vergleich mit den Voruhren 15 und 17 findet vor der Ausgabe des Quelllabels statt. Ohne eine geometrische Freigabe bleibt die Ausgabe offen.

Untersucht wurde der positive Transportweg auf dem ursprünglichen Viertelhintergrund mit dem schwachen Gerät κ=κ₀=10⁻¹¹, festem Abgleich −κ₀, den drei Quellwerten −10⁻⁶, 0 und +10⁻⁶ sowie allen drei normierten Nachimpulsen im kontinuierlichen Bereich [−112,112]. Für die Zeiger gelten die Anfangslagen und Auslesefehler des Vorgängerpakets. Die native Uhr am fünften Takt wird zusätzlich um ein beliebiges reelles δ zwischen −10⁻⁶ und +10⁻⁶ verschoben. Der Senderzweig bleibt der in den archivierten Gleichungen definierte. Die Prüfaussage ist konditional auf diese Modellfamilie, den richtigen Zeitbezug und die eingehaltenen Fehlergrenzen.

## Ein kontinuierliches Zertifikat

Die Rechnung zerlegt das Driftintervall ohne Lücke in sieben geschlossene Teilintervalle. Sie schliesst die stationären Lösungen auf jedem Teilintervall mit gerichteter rationaler Intervallarithmetik ein und prüft dort die Bedingungen des archivierten Gerätesolvers. Der gemeinsame native Uhrwert lässt sich vor der Differenzbildung algebraisch eliminieren. Ist x die kleine Wurzel von a·x²+2b·x+c=0, wird x als c/(−b+√(b²−a·c)) eingeschlossen. So lässt sich die Geräteverschiebung gegenüber der nativen Uhr auch auf Intervallen bestimmen, deren Drift viel grösser als ein Rasterschritt ist. Die Auswahl des stetigen kleinen Wurzelzweigs, die Vorzeichen der Nenner, die Ordnungsbedingungen und die Fenster werden im Lauf geprüft. Das Modell und die Formeln für die stationären Lösungen stammen aus dem beigepackten Vorgängerarchiv.

Die Belastungskorrektur der Nullquelle liegt über die ganze Familie zwischen −6,042057·10⁻¹¹ und −6,041984·10⁻¹¹ (nach aussen gerundet). Die Differenz der digitalisierten belasteten und nativen Nullcodes liegt damit jeweils bei −31 oder −30 Schritten. Auf jedem Teilintervall beträgt die zertifizierte Reserve des Lesers mindestens elf Schritte. Jede mit der Gerätefamilie vereinbare belastete Nullziffer ist im geometrischen Band enthalten. Das Verfahren gibt ein Quelllabel erst dann frei, wenn sich Zeit- und Geometrieband überschneiden und **das gesamte geometrische Band** innerhalb B±11 liegt. Diese zweite Bedingung schützt die Quellenentscheidung sogar bei verletzter Zeitprognose, solange Voruhren und Modellbezug stimmen. Die sieben Zertifikate stehen in Dynamik.json.

## Wann eine Freigabe gelingt

Die Voruhrwerte u=Y₁₅ und h=Y₁₇ bestimmen die native Empfangsuhr T(u,h). Auf dem ganzen archivierten Rechteck ist ∂T/∂u positiv und ∂T/∂h negativ. Der neue Leser bestimmt deshalb die untere Schranke an der Ecke (u_min,h_max) und die obere an (u_max,h_min). Anschliessend rechnet er die analoge Geräteverschiebung hinzu und rundet einmal. Die Ziffern der Voruhren entstehen durch Rundung auf den nächsten Rasterwert, bei Gleichstand aufwärts. Bei einem Raster r und einer Offsetgrenze b kann jede wahre Uhrkoordinate um bis zu r/2+b von der Mitte ihrer Ziffer abweichen.

| Raster beider Voruhren | Max. Offset je Uhr | Freigegebene Verschiebung δ in Empfangsschritten, gerundet | Mögliche Ziffernpaare bei δ=0 mit Freigabe |
|---|---:|---|---:|
| 10⁻¹² | 0 | ungefähr (−8,129726; +6,433249] | 1 von 1 |
| 2·10⁻¹² | 0 | ungefähr (−4,819959; +3,123482] | 1 von 1 |
| 10⁻¹² | 10⁻¹² | keine | 0 von 9 |
| 2·10⁻¹² | 10⁻¹² | keine | 0 von 4 |

Die Klammern geben die Offenheit der tatsächlichen algebraischen Grenzen an. Freigabefenster.json enthält rationale Einschliessungen aller Grenzen. Für diese vier Einstellungen stimmen die Fenster der Eckenauswertung mit der früheren Intervallformel überein, wenn dieselben Raster- und Offsetannahmen eingesetzt werden. Der originale ausführbare Schutzleser des Vorgängers war auf Raster 10⁻¹² und Offset null beschränkt.

Die Fenster ergeben sich durch Umkehr der Quantisierung. Für jedes mögliche Ziffernpaar entscheidet der Leser, ob er die Quelle freigibt. Auf der Driftfamilie ist u fest, während h streng mit der nativen Empfangsuhr abnimmt. Für zusammenhängende zugelassene h-Ziffern von a bis b ist das zugehörige h-Intervall [(a−½)r,(b+½)r). Bei unbekanntem Offset wird dieses Intervall für mögliche Freigaben erweitert und für garantierte Freigaben entsprechend verkleinert. Die Umkehrfunktion T(u,h) liefert die stetigen Driftgrenzen. Weiter entfernte Ziffern lassen sich ausschliessen, weil bei einer Freigabe der wahre belastete Nullcode innerhalb B±11 liegen muss. Das erzwingt bereits −12,637 < δ/(Empfangsschritt) < 10,365. Das Ergebnis setzt keine Verteilung der Drift oder der Offsets voraus.

## Wie gross darf der unbekannte Offset bei δ=0 sein?

Die ergänzende Untersuchung nach den vier Primärläufen bestimmt die garantierte Freigabe bei ungestörter fünfter Präparation. Die beiden Offsets dürfen unabhängig voneinander jeden Wert innerhalb ihrer jeweiligen symmetrischen Schranke annehmen.

| Raster | Beide Uhren mit gleicher Offsetgrenze | Nur Uhr 15 mit Offset | Nur Uhr 17 mit Offset |
|---|---:|---:|---:|
| 10⁻¹² | Grenze ≈ 4,6159381·10⁻¹³ | ≈ 4,61594·10⁻¹³ | alle Eingaben bis einschliesslich 10⁻¹² |
| 2·10⁻¹² | Grenze ≈ 3,5929139·10⁻¹³ | ≈ 5,23119·10⁻¹³ | ≈ 6,31561·10⁻¹³ |

Für gleiche Offsetschranken ist der jeweilige Grenzwert als Entfernung der wahren Voruhr zum nächsten entscheidenden Quantisierungssprung bestimmt. Beim feineren Raster kommt an Uhr 15 eine höhere Ziffer hinzu. Sie ist bereits am exakten Grenzwert möglich und überschreitet das Fehlerbudget. Beim gröberen Raster kommt an Uhr 17 eine tiefere Ziffer hinzu. Aufgrund der Gleichstandsregel darf hier die exakte Grenze erreicht werden. Alle bis dahin möglichen Ziffernpaare erfüllen das Budget. Die einzelnen Schwellen in der zweiten und dritten Zahlenspalte wurden durch monotone rationale Intervallsuche geprüft. Die Lage der Uhr innerhalb der Rasterzelle gehört zur Präparation. Für andere Anfangsanzeigen sind diese Angaben neu zu bestimmen.

Ein unmittelbares Kalibrierziel für das feinere Raster wäre beispielsweise ein unabhängig belegter gemeinsamer Maximalfehler von 4,6·10⁻¹³ je Uhr bei dieser Referenzpräparation. Der Beleg muss auch den Zeitpunkt der tatsächlichen Auslese abdecken. Die hier berechnete Zahl ist eine Modellanforderung. Physische Eichdaten stehen aus.

## Wenn die Voruhranzeige stehenbleibt

Bei einer ganzzahligen Verschiebung um n Empfangsschritte ist der belastete Nullcode für alle zulässigen Nachimpulse genau 42 180 625 621+n. Dies folgt aus der Einschliessung der analogen Belastung und der Translationsregel beim Runden um ganze Schritte. Die Zeitreferenz ist eins kleiner als der Nullcode bei n=0. Bei ausgeschalteter Quelle setzt der zeitbasierte Empfänger sein Bit daher genau dann auf null, wenn −126≤n≤124.

Bei n=+125 und n=−127 liefert die konkrete Nullprobe mit drei verschwindenden Nachimpulsen jeweils ein gesetztes Bit. Aktuelle Voruhren sperren beide Ausgaben. Werden die zwei Voruhrziffern des stabilen Hintergrunds unter dem aktuellen Laufbezug weitergeführt, meldet der gleiche Leser einen positiven beziehungsweise negativen Puls. Eine ausdrücklich falsche Taktkennung wird zurückgewiesen. Physisch muss deshalb belegt werden, dass die Uhren für den jeweiligen Lauf neu ausgelesen und ihre Ziffern übertragen wurden. Ein passender Eintrag im Laufprotokoll allein kann eine stehengebliebene Anzeige nicht erkennen.

## Reproduktion und Messstand

Python ab Version 3.10 und die Standardbibliothek genügen. Aus dem entpackten Ordner starten:

    python3 -B pruefen.py
    python3 -B pruefen.py --mit-vorgaenger

Der erste Lauf reproduziert die neuen Ergebnisdateien bytegenau und prüft die vollständigen Quellenpakete per SHA-256. Der zweite wiederholt zusätzlich die archivierten Rechnungen. Zur Gegenkontrolle wurden an 95 einzelnen Driftwerten, darunter Punkte auf beiden Seiten aller gefundenen Übergänge, die stationären Anzeigen direkt berechnet. Geprüft wurden dabei 2 850 Ziffernpaar-Konstellationen und 318 freigegebene Quellenvergleiche über beide Bandmethoden. Sie dienen der Kontrolle der analytischen Intervallrechnung. Sie sind keine unabhängigen Messungen einer Zuverlässigkeitsrate.

Der folgende Aufruf verwendet die aktuellen Voruhren der positiven Driftgegenprobe und beendet die Auslese mit DISJOINT_REFERENCES und Rückgabecode 2:

    python3 -B uhrvergleich.py beispiel/Referenz.json beispiel/Voruhren_aktuell.json beispiel/receiver.json beispiel/memory.json beispiel/received.json

Mit beispiel/Voruhren_festgehalten.json an zweiter Stelle liefert der Gegenversuch die falsche positive Klasse für dieselbe Nullquelle. Für den Eckenauswerter können die beiden unabhängigen Grenzen als rationale Zeichenketten bias15 und bias17 oder gemeinsam als bias angegeben werden. Der Leser setzt den geprüften Modellzweig und dessen Impulsgrenze voraus.

**Physische Messungen im Paket: 0. Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.** Die Studie prüft die lokale Quellenunterscheidung. Der Nachweis eines dynamischen Bounce erfordert die dafür vorgesehenen Staubballtests.

[Grundlage der Nulluhr auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/395)
