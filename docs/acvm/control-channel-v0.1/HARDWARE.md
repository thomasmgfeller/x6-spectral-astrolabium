# C1: Aufbau und unabhängiger elektrischer Nachweis

**Referenzentwurf, noch nicht aufgebaut oder vermessen. RP2040-Zielbuild inzwischen PASS.**
Firmwarekandidat, reproduzierbarer Build und offene E01-Messvorlagen stehen im
[Build- und Messpaket](../c1-e01-target-build/README.md).
Dieser Ablauf ist der nächste notwendige Nachweis. Der Softwarebericht darf
nicht als abgeschlossener Hardwaretest bezeichnet werden.

## Festgelegter Kanal

Originaler Raspberry Pi Pico mit RP2040, USB-CDC; externer MCP4921 im PDIP-8,
gemeinsame 3,3-V-Versorgung und Masse; externe, separat vermessene 2,500-V-Referenz.
SPI0 läuft im Entwurf mit 1 MHz, Mode 0, MSB zuerst. Das 16-Bit-Wort ist
`0x3000 | code`: ungepufferte Referenz, Verstärkung 1, aktiver Ausgang.
LDAC liegt an Masse. Ideal gilt `Vout = Vref * code / 4096`.
Codes 0–3276 entsprechen nominal ungefähr 0–1,9995 V; reale Werte und Nullpunkt
werden gemessen. Der Codebereich begrenzt keine Spannung unabhängig von Vref.

| Anschluss | Verbindung |
| --- | --- |
| Pico 3V3 OUT, physischer Pin 36 | MCP4921 Pin 1 VDD |
| Pico GND, z. B. Pin 23 | MCP4921 Pin 7 VSS und Referenzmasse |
| Pico GP17, Pin 22 | MCP4921 Pin 2 CS; externer 10-kΩ-Pull-up nach 3,3 V |
| Pico GP18, Pin 24 | MCP4921 Pin 3 SCK |
| Pico GP19, Pin 25 | MCP4921 Pin 4 SDI |
| MCP4921 Pin 5 LDAC | Masse |
| Separat gemessene 2,500-V-Referenz | MCP4921 Pin 6 VREF |
| MCP4921 Pin 8 VOUT | Hochohmiger Eingang des unabhängigen Messgeräts |
| Pico GP2, Pin 4 | Freigabesignal / Zeitmarke; externer 10-kΩ-Pull-down nach Masse |

100 nF unmittelbar an VDD/VSS; Referenzversorgung nach deren eigener
Herstellerbeschaltung abblocken. Zuerst Versorgung, Pinorientierung und
Referenzspannung ohne angeschlossenen optischen Treiber prüfen. Für die Messung
einen hochohmigen Tastkopf verwenden, keinen 50-Ω-Abschluss am DAC.
GP2 ist ein 3,3-V-Logiksignal, kein Leistungs- oder Laseranschluss.
Eine spätere Verbindung zu einem optischen Treiber braucht ein eigenes,
bestätigtes Schnittstellenprofil einschließlich Polarität und Aus-Zustand.

STOP und Fehlerpfade setzen GP2 zuerst niedrig und fordern dann DAC-Code null an.
Bei Reset kann der externe DAC seinen vorherigen Wert behalten, bis ein neues
SPI-Wort ankommt. Der GP2-Pull-down ersetzt daher keine bestätigte Abschaltung
eines angeschlossenen Geräts. Ohne Rückmessung bleiben Busfehler und klemmende
Ausgänge unentdeckt. Der RP2040-Watchdog ist im Adapter auf 250 ms konfiguriert;
auch sein Verhalten wird auf dem tatsächlichen Aufbau geprüft.

## Firmware bauen und identifizieren

Benötigt werden Pico SDK, CMake, GNU Arm Embedded Toolchain und ein Buildwerkzeug.
Der [festgelegte Build](../c1-e01-target-build/README.md) wurde mit Pico SDK 2.3.1
und GNU Arm GCC 15.2.1 ausgeführt; UF2, Werkzeugversionen, Quellenhashes und Logs
sind archiviert. SDK und Compiler werden über das dortige Rezept bezogen.
Die folgenden allgemeinen Befehle ersetzen nicht die festgelegten Versionen.

```bash
export PICO_SDK_PATH=/absoluter/pfad/pico-sdk
cmake -S experimental/control_channel/firmware -B runs/c1-pico-build -DPICO_BOARD=pico
cmake --build runs/c1-pico-build
sha256sum runs/c1-pico-build/acvm_channel.uf2
```

UF2 im BOOTSEL-Modus auf den ausdrücklich ausgewählten Pico kopieren.
Es gibt kein automatisches Flashen. Nach dem Neustart den zu diesem Board
gehörenden USB-Gerätepfad ermitteln und verwenden:

```bash
python3 x6.py control run --plan experimental/control_channel/examples/step-plan.json --port /dev/serial/by-id/DER_TATSAECHLICHE_PICO --output runs/c1-hardware-001
python3 x6.py control verify runs/c1-hardware-001
```

Erfolg bedeutet hier zunächst `DEVICE_EXECUTION_REPORTED`. Auch ein erfolgreich
geprüfter Befehlsbeleg enthält weiterhin `electrical_validation: NOT_PERFORMED`.
Der elektrische Bericht mit den unabhängigen Messdaten ist ein eigenes Artefakt;
ein Import solcher Daten oder eine automatische Hardwarefreigabe ist in C1
noch nicht implementiert.

## E01: vor dem ersten Lauf festzuhaltender Prüfplan

Diese Grenzen sind **vorgeschlagene Abnahmekriterien für einen langsamen
Labor-Stufenkanal**, keine Herstellerzusage oder bereits erzielte Genauigkeit.
Vor Messbeginn Profilversion, Aufbau, Last, Temperatur, Instrumente,
Kalibrierstatus, Rohdatenformat und Unsicherheitsrechnung festhalten.

1. Pico, DAC, Referenz und Messgeräte mit Modell/Seriennummer identifizieren;
   Verdrahtung fotografieren. Firmwarehash und Host-Commit dokumentieren.
2. Vref unabhängig messen. Oszilloskop/DAQ an VOUT und GP2 anschliessen;
   mindestens 10 kSamples/s pro Kanal, vollständige 1,2-s-Sequenz plus Vor-/Nachlauf
   speichern. Dieser Zielwert ist eine Prüfplanwahl; die Messunsicherheit muss
   die untenstehenden Grenzen tatsächlich auflösen können.
3. Für jede 200-ms-Stufe das feste Fenster 50–150 ms nach dem Sollwechsel
   auswerten. Sollwert aus dem gemessenen Vref und dem festen Code berechnen.
   Code null separat bewerten, nicht aus einem Fit wegkalibrieren.
4. Vorgegebene Grenzen: `|Mittelwert − Sollwert| + U95 ≤ 25 mV`;
   für Code null `|Mittelwert| + U95 ≤ 25 mV`. Übergangszeiten relativ zur
   gemessenen GP2-Flanke: `|Zeitfehler| + U95 ≤ 20 ms`.
   Nicht auflösbare Messungen ergeben INCONCLUSIVE, keinen PASS.
5. Mindestens zehn vollständige Testläufe, alle Fehlversuche behalten.
   Wird vorher mit separaten Kalibrierläufen eine Korrektur entwickelt,
   diese vor den zehn Testläufen einfrieren. Keine Optimierung auf den Prüfläufen.
6. Mit unabhängigem Scope GP2 und VOUT beim Host-Prozessabbruch prüfen:
   Zeitbezug letztes gültiges POLL; Ziel Freigabe aus und Ausgang im Nullband
   innerhalb 550 ms einschließlich Messunsicherheit. Host-Zeitstempel allein
   reichen für diese elektrische Grenze nicht: USB-Paketempfang extern erfassen
   oder einen begründeten konservativen Zeitbezug dokumentieren.
7. STOP, beschädigten Befehl, USB-Abziehen, Pico-Reset und unterbrochene
   SPI-Leitung einzeln prüfen. Die unterbrochene SPI-Leitung zeigt ausdrücklich
   die Grenze des Rückmeldeverfahrens: Code-ACK darf nicht als Spannungsnachweis gelten.

Ergebnisumfang: vollständige Rohdaten, Run-ID/Session, Plan- und Firmwarehash,
vorgegebene Kriterien, Auswerteskript, alle Messunsicherheiten und alle
Fehl-/Abbruchläufe. E01 belegt höchstens diesen konkreten elektrischen Aufbau
unter den angegebenen Bedingungen; es schliesst V10 oder eine Quantenprüfung
nicht ab. Eine optische Stufe benötigt danach einen benannten Aktuator,
eine gemessene Stellkurve, Einschwingverhalten, Verluste, Drift und getrennte
Kalibrier-/Prüfdaten. Die Sagnac-Analysatorachsen sind keine Motorwinkel.

## Primärquellen für die Beschaltung

- [Microchip MCP4901/4911/4921, DS22248A](https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/22248a.pdf): Pinbelegung Tabelle 3-1, SPI/Wortformat Kapitel 5, analoge Grenzen und Beschaltung.
- [Offizielle Pico-Pinbelegung](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf).
- [Pico SDK Hardware-APIs](https://www.raspberrypi.com/documentation/pico-sdk/hardware.html), [Runtime-APIs](https://www.raspberrypi.com/documentation/pico-sdk/runtime.html).

Abgeglichen am 14.10.2026. Datenblatt-Typwerte wurden nicht als gemessene
Systemeigenschaften übernommen.
