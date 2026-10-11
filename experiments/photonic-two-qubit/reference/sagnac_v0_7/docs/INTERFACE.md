# Vierdetektor-Ereignisvertrag v0.7 (Zählformat kompatibel mit v0.6)

## Abgrenzung zur geprüften v0.1

| v0.1 | v0.6/v0.7 |
|---|---|
| Herald H, A, B | A+, A−, B+, B− |
| Fenster um akzeptierten H | feste Zeitfenster mit externer Epoche |
| vier Kategorien pro Herald/Fensterpaar | alle 16 Port-Anwesenheitsmuster |
| kein Mehrfachtrefferzähler | Wiederholung pro Trial und zusätzliche Klicks |
| H-only-Hold-off | kein interner Hold-off, keine Klicklöschung |
| 64-bit unsigned Zeit | weiterhin 64-bit unsigned Zeit |
| Register-Snapshot nach End-Watermark | Array-Snapshot nach End-Watermark |

Dies ist eine bewusste Architekturentscheidung. Ein kontinuierlich gepumpter
Sagnac-Aufbau liefert nicht automatisch einen unabhängigen Herald. Feste Fenster
vermeiden einen ergebnisabhängigen Fensterstart, garantieren aber keine gute
Paarausbeute: Ein Paar kann durch eine Fenstergrenze getrennt werden; mehrere
Paare können im selben Fenster liegen. Fensterbreite und Ursprung werden auf
separaten Kalibrierdaten festgelegt und für den Abnahmelauf eingefroren.

## Zeit- und Ereignisformat

`in_kind`: 0=A+, 1=A−, 2=B+, 3=B−, 4=Watermark. 5..7 sind ungültig.
`in_time_ps`: unsigned 64 Bit, gemeinsame kalibrierte Epoche.
`in_calibration_id`: 32 Bit, konstant im gesamten Lauf.

`cfg_setting`: 0=(a0,b0), 1=(a0,b1), 2=(a1,b0), 3=(a1,b1).
Pro Lauf gilt eine feste Einstellung. Umschalten und Einschwingen passieren
vor `start`; keine Klickdaten aus Einschwingzeiten gehören zum Lauf. Die IDs
ersetzen keine physische Winkelkalibrierung. Die CHSH-Auswertung setzt die in
METROLOGY.md festgelegte Winkelkonvention voraus.

Fenster i: `[start+i*W, start+(i+1)*W)`, ganzzahlig in ps.
Stop > Start und (Stop−Start) mod W = 0. Start/Stop dürfen bis zum größten
uint64-Wert reichen; Zeitumlauf ist innerhalb eines Laufs verboten.
Eine Wiederholung zählt ab dem zweiten Ereignis desselben Kanals im selben
Fenster, auch bei identischen Zeitstempeln. Ereignisse bleiben unterscheidbare
Datensätze; eventuelle vorgelagerte Duplikate werden nicht still entfernt.

Alle angelieferten Zeitstempel sind monoton nicht fallend. Bei Gleichheit ist
die Kanalreihenfolge frei. Eine Watermark T garantiert, dass kein später
geliefertes Ereignis einen Zeitstempel < T hat. Ein Ereignis exakt T bleibt
zulässig. Die End-Watermark muss mindestens Stop sein und nach sämtlichen
aufzuzeichnenden Ereignissen eintreffen. Watermarks erzeugen keine Klicks.
Ein Detektorklick bei Stop gehört nicht zum Lauf und setzt ein Fehlerflag.

## Handshake und Abschluss

Ein Ereignis wird nur bei steigender Taktflanke mit `in_valid=1` und
`in_ready=1` übernommen. Der Produzent hält alle Ereignisfelder unter Rückstau
stabil. Ein ausreichend dimensionierter FIFO vor dem Kern ist erforderlich.
Kann der Produzent ein Ereignis nicht bewahren, setzt er `source_error`.
Der Kern ist vollständig synchron zu `clk`; asynchrone Detektor-/Hostsignale
dürfen ohne Erfassungs-/CDC-Stufe nicht direkt angeschlossen werden.

Ein angenommenes Ereignis wird gehalten, während dadurch abgeschlossene Fenster
gezählt werden. v0.7 schließt ein belegtes Fenster einzeln und addiert danach
alle sicher leeren Fenster bis zum neuen Ereignis/Watermark als Block.
Die Anzahl ist floor((min(Ereigniszeit,Stop)−Fensterstart)/W). Zeitordnung und
Watermark-Vertrag sind dafür entscheidend. Statistik und Fenstergrenzen ändern
sich gegenüber v0.6 nicht. Der Zähleraddierer sättigt auch beim Blocküberlauf.
Es werden logisch höchstens fünf Core-Takte bis zur nächsten Ereignisannahme
benötigt; reale Taktfrequenz und die Kombinatorik für konstante Division/
Multiplikation müssen im FPGA-Werkzeug geprüft werden. Kein Timing-Versprechen
folgt aus GHDL-Synthese. FIFO/CDC und Durchsatzmessung bleiben Hardware-Gates.

`snapshot_ready` wird erst nach vollständigem Abschluss gesetzt. Dann sind
Zähler, Flags, Start/Stop, Kalibrier-ID und Setting eingefroren. Weiterer Input
und START werden ignoriert. Ein neuer Lauf benötigt Reset; Reset verwirft den
bisherigen Snapshot. Der Host liest erst nach READY, bestätigt den vollständigen
Transport und setzt erst danach zurück. Die Implementierung liefert ein Array. Der neue Snapshot-Framer und UART-Top
stellen den Transport laut TRANSPORT.md bereit; sie sind kein kompatibler
Registerbus zum v0.1-Hostadapter.

## Zähler

Alle Ausgänge sind 64 Bit; im Überlauftest wird intern bei 4 Bit gesättigt.

| Index | Bedeutung |
|---|---|
| 0..15 | Anzahl Fenster mit Maske m; bit0 A+, bit1 A−, bit2 B+, bit3 B− |
| 16 | alle abgeschlossenen Fenster N, einschließlich leerer |
| 17 | Fenster mit mindestens einem wiederholten Kanal |
| 18..21 | alle angenommenen Klicks in A+, A−, B+, B− |
| 22 | zusätzliche Klicks nach dem ersten je Kanal/Fenster |
| 23 | Fenster mit A+ UND A− oder B+ UND B− |

Die neun eindeutigen Kategorien `{0,+,−} × {0,+,−}` verwenden Masken
0,1,2,4,5,6,8,9,10. Die übrigen sieben Masken bleiben erhalten und werden
zusätzlich in Zähler 23 zusammengefasst. Zähler 17 und 23 können sich
überschneiden und dürfen nicht als disjunkte Fehlermengen addiert werden.
61 Fenster mit zweimal A+ ergeben n_repeat=61, n_extra=61, Maske1=61,
aber n_multiport=0. Aus diesen Zahlen folgt keine Ursache des Zweitklicks.

## Fehlerflags

| Bit | Ursache |
|---|---|
| 0 | mindestens ein Sättigungsversuch eines Zählers |
| 1 | rückwärts laufender Zeitstempel (einschließlich vor Start) |
| 2 | vom Produzenten gemeldeter Erfassungs-/Pufferverlust |
| 3 | abweichende Kalibrier-ID |
| 4 | ungültige Start-/Stop-/Fensterkonfiguration |
| 5 | ungültige Ereignisart oder Detektorklick außerhalb des Laufs |
| 6 | START während eines aktiven Laufs |
| 7 | reserviert; Host behandelt gesetztes Bit als Fehler |

Jedes gesetzte Flag sperrt die wissenschaftliche Auswertung. Teilzähler bleiben
Diagnostik. Ohne abschließende Watermark entsteht bei gültiger Konfiguration
kein fertiger Snapshot. Ein Watchdog muss diesen Fall extern melden und darf
keine vollständigen Nullzähler erfinden.
