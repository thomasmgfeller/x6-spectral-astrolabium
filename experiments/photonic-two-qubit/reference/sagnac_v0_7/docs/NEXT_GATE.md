# Nächste reale Arbeitsstufe nach v0.7

## Bereits umgesetzt

Vierdetektor-Zählkern, Sammelzählung leerer Fenster, vollständiger Snapshot-
Framer, CRC32, UART-Sender, integrierter Top-Level und Linux/Python-Empfänger
sind implementiert. Die synthetische Gesamtkette ist ausgeführt; ihre physische
Übertragung ist noch nicht gemessen. Board-/Detektorkandidaten und die
Kostenentscheidung stehen in HARDWARE.md. Das Spiegelprotokoll bleibt vorbereitet.

## Nächste notwendigen Eingaben aus realer Hardware

- Tatsächlich vorhandenes FPGA-Board mit Revision und vorhandener Entwicklungssoftware.
- Tatsächlicher Raspberry-Pi-Typ und gewählter serieller Anschluss/Adapter.
- Modell und Revision der vier verfügbaren/leihbaren Detektoren.
- Verfügbare Zeitstempelerfassung bzw. Labor-Time-Tagger und Exportformat.

Bis diese Angaben vorliegen, bleibt das Ziel DE10-Nano plus Raspberry ein
expliziter Entwurfsvorschlag. Keine Pinbelegung und keine TDC-Auflösung werden
als Eigenschaften eines unbekannten Gerätes erfunden.

## Elektrischer Ersttest

Nach Festlegung des Boards: Quartus-Projekt samt realem Pinplan und Timing-
Constraints erstellen. Zunächst synthetische Ereignisse innerhalb des FPGA
verwenden und die real empfangenen UART-Frames mit den Referenzdaten vergleichen.
Danach geeignete Eingangsreceiver und kalibrierte Zeitmessung mit einem
bekannten Pulsgenerator charakterisieren. Noch keine optische Aussage aus
solchen Pulsgeneratortests ableiten.

## Tatsächliche Photonenerfassung

Detektoren an den geprüften Receiver/Time-Tagger anschließen. Dunkelmessung,
Totzeit, Zeitjitter, Offsetdrift, Ratenlinearität und Mehrfachtrefferdiagnostik
an unveränderten Rohzeitstempeln untersuchen. Sortierung, FIFO-Überläufe und
Watermarks müssen hardwareseitig nachvollziehbar sein. Erst danach wird die
Fensterbreite für separate Abnahmedaten festgelegt.

## Optik und Klebung

Eine nachjustierbare Referenzquelle liefert das optische Toleranzbudget.
Anschließend MIRROR_TEST.md physisch durchführen. Klebeprozess, Jig-CAD,
Vibration und Langzeitalterung bleiben eigene Freigaben. Eine generische
Synthese oder ein CRC-Test ersetzt keine davon.
