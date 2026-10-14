# ACVM C1 — einzelner Steuerkanal, Referenz 0.1

**Status: ausführbarer Softwarekanal; elektrischer und optischer Nachweis offen.**

C1 implementiert einen begrenzten Befehlsweg vom lokalen Python-Host zu einem
C++-Gerätekern. Der Zieladapter ist ein Raspberry Pi Pico (RP2040) mit MCP4921-DAC.
Der identische Protokoll- und Sequenzkern läuft im nativen Prüfprozess und im
Pico-Quelltext. Nur der native Prozess wurde hier gebaut und ausgeführt.
Die native Ausgabe ist ein protokolliertes Modell, keine Spannung.

| Nachweis | Stand dieser Lieferung |
| --- | --- |
| Planprüfung, binärer Compiler, unabhängiger Leser | Implementiert und geprüft |
| Host ↔ C++-Kern über POSIX-Pseudoterminal | Durchgängiger Lauf und Fehlerfälle geprüft |
| Vollständige Sequenz, Stop, Timeout, Wiederholungen | Softwareprüfungen; Rohprotokolle vorhanden |
| Pico-SDK-Adapter, SPI-Ausgang und Bauanleitung | Quelltext geliefert; Zielbuild noch nicht ausgeführt |
| Reale USB-/SPI-Verbindung und Ausgangsspannung | NOT_PERFORMED |
| Kalibrierter optischer Aktuator, Regelung, Quantenoperation | NOT_PERFORMED |

Die aktuellen Zählwerte und Umgebungsangaben stehen im
[Prüfbericht](VALIDATION.md) und im [maschinenlesbaren Ergebnis](evidence/qualification.json).
Diese Teilimplementierung schliesst die ACVM-Konzeptprüfungen V01–V10 nicht pauschal ab.
Insbesondere sind die komplexen Signal-/FFT-/Driftprüfungen V02–V04 und V08
nicht Bestandteil dieses skalaren Stufenkanals. Der ursprüngliche ACVM- und
Experiment-Records-Konzeptstand bleibt als historische Veröffentlichung erhalten.

## Frischer Checkout: ohne Zusatzpakete

Voraussetzungen für den hier geprüften Weg: Linux/POSIX, Python 3.12, g++ mit C++17.
Es werden weder pip-Pakete noch Hardware für den Softwarelauf benötigt. Die
vorhandene X6-Umgebung kann weiterverwendet werden; `control` benötigt deren
numerische Forschungspakete nicht. Windows ist für diesen Transport nicht qualifiziert.

Im Repository-Wurzelverzeichnis:

```bash
python3 x6.py control doctor
python3 x6.py control compile experimental/control_channel/examples/step-plan.json --output runs/c1-plan.bin
python3 x6.py control demo --output runs/c1-demo
python3 x6.py control verify runs/c1-demo
python3 x6.py control export runs/c1-demo --output exports/c1-demo.zip
python3 x6.py control qualify --output runs/c1-qualification
```

Vorhandene Ausgabepfade werden abgewiesen. Für einen erneuten Lauf neue Namen
verwenden. `demo` startet einen frisch gebauten C++-Prozess an einem virtuellen
seriellen Anschluss; `verify` prüft Dateien, Rohbefehle, Antworten und die unabhängig
rekonstruierte Modellfolge. `verify` gibt **keine** Gerätebefehle aus.
`qualify` prüft zusätzlich Export, erneutes Einlesen und Manipulationen.
Das ZIP enthält Plan, Binärplan, Rohverkehr, Modellereignisse und Ergebnis.
Es ist das versionierte Format `acvm.channel.run/1`, noch kein implementiertes
ACVM Experiment Record und kein `x6.integration.run/1`.

Das separate Quellpaket enthält die C1-Module, Tests, Anleitung und Prüfbelege.
Nach dem Entpacken in dessen Wurzelverzeichnis in allen obigen Befehlen
`python3 x6.py control` durch `python3 -m experimental.control_channel` ersetzen.
Damit lässt sich C1 auch ohne den übrigen X6-Checkout prüfen.

## Funktionsumfang und feste Grenzen

- Ein Kanal, 1–64 Stufen; erste Stufe bei 0 ms, Abstand und letzte Haltezeit ≥10 ms.
- Laufdauer 10–5000 ms, DAC-Codes 0–3276. Ausschliesslich ganzzahlige Codes und
  Millisekunden; keine stillschweigende Umrechnung von Volt, Grad oder Phase.
- Gesamter Plan wird geprüft und geladen, bevor START erlaubt ist.
- Paket-CRC32, Plan-CRC32 und SHA-256-Dateiinventar erfüllen unterschiedliche
  Integritätsaufgaben. Sie authentifizieren weder Gerät noch Messung.
- Host-Lebenszeichen normalerweise alle 50 ms; Geräteleasing 500 ms. Ausbleiben
  führt im laufenden Gerätekern zu FAULT, Code null und Freigabe aus.
- Eine Ereignisverspätung über 20 ms führt zu FAULT. Diese Softwaregrenze ist
  **keine gemessene elektrische Timinggarantie**.
- Identische Befehlswiederholung erzeugt keinen zweiten Start. Geänderte,
  veraltete oder ungeordnete Befehle werden abgewiesen. Kein automatischer
  Wiederanlauf nach Verbindungsverlust, DONE, ABORTED oder FAULT.
- Ctrl+C löst einen bestmöglichen STOP aus; ohne Antwort bleibt dessen Wirkung
  unbestätigt. Das Geräteleasing wirkt unabhängig vom weiterlaufenden Host.

`commanded_dac_code` ist der an den Ausgabetreiber übergebene Code. Der MCP4921
liefert über diese Beschaltung keine Spannungsrückmessung. Ein ACK beweist weder
SPI-Verdrahtung noch Versorgung, Ausgangsspannung oder Bewegung eines Aktuators.

## Physischer Aufbau und nächster Nachweis

Die [Bau- und Messanleitung](HARDWARE.md) legt Anschlüsse, Firmwarebuild und einen
ersten unabhängigen elektrischen Prüfablauf fest. Das [Protokoll](PROTOCOL.md)
beschreibt alle Felder und Zustandsübergänge.

Erst nach dem elektrischen Test wird ein konkret benannter optischer Treiber
mit passender Analogschnittstelle ausgewählt und charakterisiert. Die gelieferte
Implementierung enthält keine Wellenplatten-/Motorabbildung, keine optische
Rückführung und kein schnelles photonisches Feed-forward. Die bestehende
SGNCv007-Auslese bleibt ein getrenntes, lesendes Protokoll; es werden keine
Steuerbefehle an einen Sagnac-Snapshot-Anschluss gesendet.

Originalcode und Dokumentation: Apache-2.0 gemäss Repository-Lizenz.
