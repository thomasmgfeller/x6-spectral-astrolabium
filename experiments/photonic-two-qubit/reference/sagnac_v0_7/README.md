# Sagnac-Messkette v0.7 – Durchsatz und Raspberry-Hosttransport

Stand: 11. Oktober 2026. Ausführbare digitale Referenz, keine physisch geprüfte
FPGA-/Detektorbaugruppe. Das gemeinsame Zähl- und Statistikformat bleibt mit
v0.6 kompatibel; die neue Transportkennung lautet SGNCv007.

## Umgesetzt und ausgeführt

- Leere Zeitfenster werden in einem Schritt gesammelt gezählt. Eine Milliarde
  leere Fenster benötigt im Test sechs Steuerzyklen vom Start bis Snapshot;
  mit zwei weit auseinanderliegenden Klicks sind es 14 Zyklen.
- VHDL-Snapshot-Framer: 244 Byte, vollständige Metadaten und 24 uint64-Zähler,
  CRC32 und 64-Bit-Sequenzkennung; stabil unter Rückstau.
- VHDL-UART 8N1 und integriertes `sagnac_uart_top`: ein Lauf und ein Frame pro
  Reset. Standalone-Steuerung und FPGA-Pinbelegung sind noch nicht enthalten.
- Python-Decoder und Linux-UART-Erfassung, mit Erhaltung unvollständiger Rohdaten.
- **28 RTL-Szenarien, 17 Python-Testmethoden bestanden.** Darunter sämtliche
  1952 Einzelbitänderungen eines Frames sowie ein Pseudoterminal-Test.
- Gesamtkette ausgeführt: Stimulus → RTL → UART-Bits → unabhängiger UART-Empfänger
  in der Testbench → CRC-/Sequenzprüfung → Python-Korrelationen.
- GHDL-Synthese für Kern, Framer, UART und Top-Level erfolgreich. Keine Quartus-
  Timing-Closure oder Hardwarefrequenz daraus abgeleitet.

Das synthetische CHSH-Beispiel ist gegenüber v0.6 numerisch unverändert:
S_cond = −2.8253650438389006; S_all = −1.4125. Alle physikalischen Aussagen
bleiben NOT_ASSESSED. Die Klebe-/Optikprüfung ist weiterhin ein Versuchsplan.

## Reproduzieren

Python ab 3.10, ausschließlich Standardbibliothek; GHDL mit VHDL-2008.

```bash
python3 sim/run_tests.py --ghdl ghdl
python3 -m unittest discover -s host -p 'test_*.py' -v
python3 host/frame_codec.py examples/synthetic_chsh_capture.bin --origin synthetic --first-sequence 100 --output decoded.json
python3 host/analyze.py decoded.json --output analysis.json
python3 host/budget.py
```

`GHDL` kann alternativ als Umgebungsvariable gesetzt werden. Tests erzeugen
build/ und erneuern die mitgelieferten Beispiele und Ausführungsprotokolle.
UART-Erfassung auf einem konfigurierten Linux-System, erst nach elektrischer
Prüfung und einem aktiven Sender:

```bash
python3 host/capture_serial.py --device /dev/serial/by-id/DEIN_ADAPTER --baud 1000000 --frames 4 --first-sequence 100 --origin hardware --raw capture.bin --output capture.json
python3 host/analyze.py capture.json --output analysis.json
```

Der Gerätepfad ist ein zu ersetzender Platzhalter. Das Programm konfiguriert
keine GPIO-Pins und startet keine FPGA-Messung. Die Serielle-Konsole darf den
gewählten Port nicht gleichzeitig verwenden. Bei Fehlern bleiben empfangene
Rohbytes erhalten; CLI-Exitcode 2 kennzeichnet die gescheiterte Erfassung oder
Auswertung. Ein Exitcode 0 bedeutet keine physische Quantenfreigabe.

## Hardwareentscheidung

Vorläufiges Entwicklungsziel: vorhandenes DE10-Nano, sofern verfügbar;
Raspberry Pi als Host. Besitz und Boardrevision sind nicht bestätigt.
Vier Excelitas SPCM-AQRH-14 dienen als konkreter Detektor-Referenzkandidat;
MPD PDM als Alternative mit anderem elektrischem Interface.

**Frugalitätsbefund:** Vier neue SPCM-AQRH-14 sind bei dem beobachteten
Händler-Einzelpreis zusammen ca. 27'235 USD, vor Nebenkosten. Daher zunächst
Leih-/Kooperationshardware für die physische Referenzprüfung suchen. Das ist
keine Beschaffungsauslösung. Einzelpreise sind keine Projektkostenfreigabe.
Details, Quellen und offene Herstellervarianten: docs/HARDWARE.md.

## Orientierung

- docs/INTERFACE.md: Rohereignisse und Zähler, jetzt mit Sammelzählung.
- docs/TRANSPORT.md: vollständiges Binärformat und Reset-/Sequenzvertrag.
- docs/HARDWARE.md: Kandidaten, elektrische Grenzen, Anschlusskonzept.
- docs/THROUGHPUT.md: nachvollziehbares bedingtes Durchsatz-/FIFO-Budget.
- docs/METROLOGY.md: unveränderte wissenschaftliche Grenzen der Auswertung.
- docs/MIRROR_TEST.md: physisch noch auszuführender Strahlstabilitätstest.
- docs/NEXT_GATE.md: konkrete Voraussetzungen der Hardware-Inbetriebnahme.
- VALIDATION.md und validation/: ausgeführte Prüfungen.

TDC, Detektoreingangsstufe, kanalübergreifende Sortierung, FIFO/CDC und physische
Kalibrierung bleiben offen. Ein GPIO-Synchronisierer ersetzt keine Nanosekunden-
Zeitmessung. UART überträgt Snapshots; hochratige Rohzeitstempel benötigen einen
eigenen Erfassungs-/Speicherweg. Lizenz des Codes: MIT.
