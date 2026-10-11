# Snapshot-Transport SGNCv007

Alle Komponenten gehören zu derselben FPGA-Taktdomäne. Die UART-Leitung ist der
langsame Ausgang für fertige Snapshots. Sie transportiert keine hochratigen
Detektorzeitstempel und steuert weder Laser noch Detektorgates.

## Binärformat

Feste Länge 244 Byte. Mehrbytezahlen unsigned, Little Endian.

| Byteoffset | Länge | Inhalt |
|---|---|---|
| 0 | 8 | ASCII SGNCv007 |
| 8 | 1 | Version 7 |
| 9 | 1 | Setting 0..3 |
| 10 | 1 | unveränderte Core-Fehlerflags |
| 11 | 1 | reserviert, muss 0 sein |
| 12 | 4 | Kalibrier-ID |
| 16 | 8 | Startzeit in ps |
| 24 | 8 | Stopzeit in ps |
| 32 | 8 | Fensterbreite in ps |
| 40 | 8 | Snapshot-Sequenznummer |
| 48 | 192 | 24 Zähler zu je 8 Byte, Indizes gemäß INTERFACE.md |
| 240 | 4 | CRC32 über Bytes 0..239 |

CRC-Variante CRC-32/ISO-HDLC: reflektiertes Polynom 0xEDB88320,
Initialwert 0xFFFFFFFF, finales XOR 0xFFFFFFFF. Der Python-Decoder prüft mit
zlib.crc32 unabhängig von der bitweisen VHDL-Implementierung.
CRC erkennt zufällige Übertragungsfehler; sie authentifiziert keine Quelle und
schützt nicht gegen absichtliche Manipulation. Counter-Identitäten und
Core-Fehlerflags werden zusätzlich auf Anwendungsebene geprüft.

## Sequenz und Wiederanlauf

Die erste erwartete Sequenzkennung wird vom Messplan an den Empfänger übergeben.
Innerhalb der erfassten Frames muss sie genau um eins steigen. Kein Umlauf,
keine stillschweigende Wiederholung, kein automatisches Überspringen kaputter
Frames. Bei einem Ausfall wird die Aufnahme als ungültig markiert; Rohbytes
bleiben erhalten. Ein späterer bewusster Neustart erhält eine neu dokumentierte
Epoche/Startkennung. Ohne persistenten externen Laufmanager ist die Sequenz
kein Schutz gegen unbemerkte Geräte-Resets zwischen getrennten Aufnahmen.

`sagnac_uart_top` friert cfg_sequence beim ersten START nach Reset ein. Er sendet
nach Core-Abschluss genau einen Frame. Neue Läufe benötigen Reset, wobei der
äußere Controller die Sequenz fortschreibt. `run_complete` bedeutet fertiger
Core-Snapshot, `transmit_complete` zusätzlich Abschluss des UART-Stopbits.
Erst dann darf der Controller das Top-Level für den nächsten Lauf zurücksetzen.
Ein Reset während Übertragung führt zu einer unvollständigen Aufnahme, die der
Host verwirft. Laufsteuerung und Sequenzspeicherung sind externe Aufgaben.

Der Framer selbst nimmt einen Snapshot per send_valid/send_ready an und kopiert
ihn intern. byte_valid/byte_ready schützen die Ausgabe unter Rückstau; während
byte_ready=0 bleiben Byte und Valid stabil. Der UART-Sender verarbeitet 8N1,
LSB zuerst, Leitung im Ruhezustand High. CLKS_PER_BIT bestimmt die Baudrate.
50 Takte/Bit bei tatsächlich 50 MHz entsprechen 1 Mbaud; eine erfolgreiche
FPGA-Timinganalyse ist Voraussetzung für diesen Betriebspunkt.

## Raspberry-/Linux-Empfänger

`capture_serial.py` erfasst eine vorab festgelegte Framezahl von einem explizit
angegebenen Gerät. Er setzt 8N1 ohne Hardwareflusskontrolle, speichert Rohbytes,
prüft Länge, CRC und Sequenz und stellt danach das bestehende Zählformat bereit.
Er verändert keine GPIO-Funktion und führt keinen automatischen Neustart oder
Portscan aus. Der serielle Port muss vorher korrekt konfiguriert sein.

Die Prüfkette liest das simulierte UART-Wellenformsignal mit einem separaten
Empfänger ab. Zusätzlich ist die Linux-Erfassung über ein Pseudoterminal mit
stückweiser Zustellung und bewusst unvollständiger Übertragung geprüft. Das
prüft Software-I/O, nicht Kabelqualität, Pinzuordnung oder reale Bitfehlerraten.
