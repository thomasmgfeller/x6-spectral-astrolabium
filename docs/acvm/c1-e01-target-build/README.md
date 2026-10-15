# C1/E01: gebauter Firmwarekandidat und offene physische Messung

**Zielbuild PASS; E01 NOT_PERFORMED.** Am 15. Oktober 2026 wurde der vorhandene
C1-Pico-Quelltext erstmals für den RP2040 gebaut. Die UF2-Datei ist ein
**nicht elektrisch geprüfter Firmwarekandidat**. Kein Board wurde geflasht,
keine Stellfolge an Hardware gesendet und keine Spannung oder Fehlerreaktion
physisch gemessen. Der Auftrag „eigenen Hardware-Messweg abschließen“ bleibt
bis zu diesen Messungen offen.

| Teil des Messwegs | Tatsächlicher Stand |
| --- | --- |
| RP2040-Zielsoftware bauen | PASS; Pico SDK 2.3.1, GNU Arm GCC 15.2.1, Release |
| UF2 identifizieren und prüfen | 111 Blöcke, RP2040-Familie, Flash ab `0x10000000`; vollständige Übereinstimmung mit 28.396 Byte Binärprogramm |
| Wiederholter Build | Identische UF2- und BIN-Prüfsummen bei festem Builddatum |
| Stellfolgen kompilieren | Normallauf und separate Fehlerfall-Haltefolge kompiliert; nicht übertragen |
| Reale Normalläufe | **0 von mindestens 10** |
| Physisch gemessene Fehlerfälle | **0 von 6** |
| Elektrische / optische Abnahme | **NOT_PERFORMED / NOT_PERFORMED** |

Der [Buildbericht](evidence/build-report.json), vollständige Konfigurations-/Buildlogs,
[Picotool-Befund](evidence/picotool-info.txt) und
[offene Messvoraussetzungen](evidence/readiness.json) sind gespeichert.
Alle ursprünglichen Firmwarequellen sind unverändert und stammen aus
`cdf185588f87d73f757dc94c60a8b84b2d6de75d`.

## Firmware und Stellfolgen

- [acvm_channel.uf2](firmware/acvm_channel.uf2), 56.832 Byte:
  `70b3b696b78a24b0e7526da4be00778ecbfc58b8361ff0cbfced867ee1b9d29d`
- [acvm_channel.bin](firmware/acvm_channel.bin), 28.396 Byte:
  `a3b5a99430e13fc375d6a6bfbae45bbcb995dead813ab00a7a364460bf4e4fbb`
- [acvm_channel.elf](firmware/acvm_channel.elf): ARM-ELF mit Symbolen; Hash im Buildbericht.
- [nominal-plan.bin](firmware/nominal-plan.bin): unveränderte
  [1,2-s-Stellfolge](../../../experimental/control_channel/examples/step-plan.json),
  sechs Stufen à 200 ms, Codes `0,819,1638,2457,3276,0`.
- [fault-plan.json](fault-plan.json) und [fault-plan.bin](firmware/fault-plan.bin):
  2 s bei Code 1638. Die Fehlerauslösung muss früh genug erfolgen, damit das
  natürliche Sequenzende nicht als erfolgreicher Fehlerstopp fehlinterpretiert wird.

Für eine **nur nominal angenommene** Referenz von 2,500 V wären die fünf Pegel
0, 0,499878, 0,999756, 1,499634 und 1,999512 V. Das sind Designwerte, keine Messdaten.
In E01 wird der Sollwert aus dem **unabhängig gemessenen** Vref berechnet.

## Zielbuild wiederholen

Linux x86-64; Python 3.12, Git und die im
[build-lock.json](build-lock.json) festgelegten Werkzeuge. Die beschriebene
Installation lädt Werkzeuge in einen eigenen Ordner und verändert keine
Shell-Konfigurationsdatei. Sie benötigt Netzwerk; der Build selbst benötigt
keine Verbindung zu Hardware. Der SDK-Installer wurde mit seinem Commit fixiert,
seine Versionsmetadaten liegen unverändert bei. Nicht blind eine neuere SDK- oder
Compilerfassung einsetzen und deren Binärdatei als denselben Kandidaten ausgeben.

Aus dem Repository-Hauptverzeichnis, mit jeweils neuen Zielordnern:

```sh
git clone --depth 1 --branch 2.3.1 https://github.com/raspberrypi/pico-sdk.git /tmp/c1-sdk
git -C /tmp/c1-sdk submodule update --init --depth 1 lib/tinyusb
git init /tmp/c1-installer
git -C /tmp/c1-installer remote add origin https://github.com/raspberrypi/pico-sdk-tools.git
git -C /tmp/c1-installer fetch --depth 1 origin 4ddc34c32f58be6ddf4fefb966f8e7f367063db9
git -C /tmp/c1-installer checkout --detach FETCH_HEAD
python3 /tmp/c1-installer/installer/install_pico_tools.py 2.3.1 \
  --only arm-toolchain,cmake,ninja,picotool --install-dir /tmp/c1-tools --no-rc-include \
  --bundles docs/acvm/c1-e01-target-build/versionBundles.json \
  --toolchains-ini docs/acvm/c1-e01-target-build/supportedToolchains.ini \
  --picotool-tag v2.3.1-0
. /tmp/c1-tools/picorc
python3 -B tools/build_c1_pico.py --sdk /tmp/c1-sdk \
  --picotool-dir /tmp/c1-tools/picotool/2.3.1/picotool --output /tmp/c1-target-build
python3 -B tests/control-channel/test_pico_build.py
```

Erwartet: `TARGET_BUILD_PASS`, identische UF2-/BIN-Hashes und
`electrical_validation: NOT_PERFORMED`. Der Prüfer kontrolliert SDK- und
TinyUSB-Commit, saubere SDK-Quellen, Firmwarequellenhashes und Werkzeugversionen.
Das feste `SOURCE_DATE_EPOCH` verhindert, dass allein ein anderer Kalendertag die
Firmware ändert; das eingebettete Datum ist damit **kein Nachweis des realen
Buildzeitpunkts**. Logs und Werkzeughashes werden festgehalten. Fehlgeschlagene
Builds bleiben im neuen Zielordner erhalten; vorhandene Ordner werden nicht verändert.

Die Action [C1 RP2040 target build](../../../.github/workflows/x6-c1-pico-build.yml)
wiederholt diesen Build bei relevanten Änderungen. Sie öffnet und flasht kein
Gerät. Ein grüner CI-Job ist ausschließlich ein Buildnachweis. Fünf
Beschädigungsfälle prüfen UF2-Familie, Flash-Adresse, doppelte Blöcke, Nutzdaten
und Kürzung; ein weiterer Test schützt vorhandene Ergebnisordner.

## Den tatsächlichen E01-Lauf vorbereiten

Die [bestehende Bauanleitung](../control-channel-v0.1/HARDWARE.md) gilt weiterhin:
originaler Pico, MCP4921, externe vermessene Referenz, hochohmiger Messgeräteeingang,
VOUT und GP2 auf unabhängigen Messkanälen. Die Firmware enthält keine
Spannungsrückmessung und keinen hardwareunabhängigen DAC-Abschaltpfad.

1. [E01_profile.template.json](E01_profile.template.json) in einen neuen
   Messordner kopieren. Reale Geräte-/Seriennummern, Verdrahtungsfoto, Last,
   Temperatur, Kalibrierbelege und Vref-Messung ergänzen. Die `null`-Felder sind
   bewusst **nicht durch angenommene Messwerte ersetzt**.
2. Vor der Datenerhebung Flankendefinition, GP2-Schwelle, Vor-/Nachlauf,
   Instrumentexport, maximal zulässige Abtastlücke und Unsicherheitsrechnung
   festlegen. Für die Fehlerfälle Zeitbezug, Erwartungen und gegebenenfalls
   zusätzliche Grenzen ebenfalls vorher festschreiben. Das ausgefüllte Profil
   mit Datum und SHA-256 fixieren und unverändert auf alle Prüfläufe anwenden.
3. Den UF2-Hash prüfen und erst am **identifizierten tatsächlichen Board** im
   BOOTSEL-Modus flashen. Flashvorgang und USB-Gerätepfad protokollieren.
4. Scope/DAQ scharf schalten, dann genau einen Normallauf ausführen:

```sh
python3 x6.py control run \
  --plan experimental/control_channel/examples/step-plan.json \
  --port /dev/serial/by-id/DER_TATSAECHLICHE_PICO --output runs/E01-N01-host
python3 x6.py control verify runs/E01-N01-host
```

   Den Platzhalter durch den vorher identifizierten Gerätepfad ersetzen. Für
   `N02` bis mindestens `N10` jeweils neue Host- und Instrumentdateien anlegen.
   Ein ACK oder `DEVICE_EXECUTION_REPORTED` ersetzt die Instrumentaufnahme nicht.
5. [E01_runs.template.json](E01_runs.template.json) als lückenloses Laufregister
   führen. Auch fehlgeschlagene, unvollständige und abgebrochene Versuche behalten;
   zusätzliche Versuche anhängen. Rohdateien im nativen Instrumentformat und
   zusätzlich als verlustfreier Export archivieren. Host-Session, Run-ID,
   Firmware-/Planhash und Instrumentaufnahme eindeutig zuordnen.

Die vorhandenen E01-Grenzen bleiben: mindestens 10 kSamples/s je Kanal; feste
Plateaufenster 50–150 ms nach dem Sollwechsel; `|Mittel−Soll|+U95 ≤25 mV`,
Nullcode separat; `|Zeitfehler|+U95 ≤20 ms` relativ zur gemessenen GP2-Startflanke.
Der Start bei Code null erzeugt keine VOUT-Flanke: GP2 dient hier als Zeitmarke.
Alle tatsächlichen Pegelwechsel und das Ende müssen im Rohsignal vorhanden sein.

`U95` muss zum jeweils **verglichenen Unterschied** gehören, einschließlich
Referenz-, Instrument-, Drift- und relevanter Abtastunsicherheit. Eine einzelne
Datenblattgenauigkeit ist kein vollständiges Budget. Korrelierte Scope-Samples
dürfen nicht ungeprüft als unabhängige Wiederholungen durch `sqrt(N)` heruntergeteilt
werden. Unzureichende Messauflösung oder fehlender Zeitbezug ergibt INCONCLUSIVE.
Die auswertende Importroutine wird erst an das tatsächlich benannte Instrumentformat
gebunden; dieses Paket behauptet noch keinen ausgeführten Hardware-Datenimport.

## Sechs Fehlerfälle separat messen

| Fall | Unabhängig aufzuzeichnen / besondere Grenze |
| --- | --- |
| Host-Prozessabbruch | Tatsächlichen Prozessabbruch von regulärem STOP unterscheiden. Ctrl+C versucht bereits STOP und ist daher kein reiner Leasing-Test. GP2 und VOUT müssen nach dem letzten akzeptierten POLL innerhalb 550 ms einschließlich Unsicherheit aus bzw. im Nullband sein. |
| STOP | Vollständigen Befehlsempfang und beide Ausgangsreaktionen unabhängig zeitlich zuordnen; ACK allein genügt nicht. |
| Vollständiger Befehl mit falscher CRC | FORMAT-Fehler und physische Reaktionen beobachten. Führendes Rauschen oder ein unvollständiger Frame prüft einen anderen Pfad. |
| USB-Abziehen | Protokollieren, ob mit VBUS zugleich Pico/DAC stromlos werden. Ein Versorgungsausfall beweist nicht den weiter versorgten Leasing-Pfad. Keine improvisierte Rückspeisung; die konkrete Stromversorgung vorher festlegen. |
| Pico-Reset | GP2 und VOUT getrennt aufnehmen. Ein externer DAC kann seinen letzten Code bis zum neuen SPI-Wort behalten. |
| Unterbrochenes SPI | Die Grenze gezielt sichtbar machen: ACK/Kommandocode kann trotz falscher Ausgangsspannung korrekt aussehen. Eine beobachtete Abweichung darf nicht als bestätigte Abschaltung gewertet werden. |

Für den 550-ms-Nachweis reicht die Host-Uhr nicht. Benötigt wird eine unabhängige
Aufnahme des letzten gültigen POLL oder ein nachweislich **früherer** Zeitbezug
mit begründeter Unsicherheit. Ein erst nach dem Ereignis gesetzter Marker kann
die gemessene Reaktionszeit künstlich verkürzen. Fehlende externe Zeitinformation
wird nicht durch eine Software-Zeitangabe ersetzt.

Der endgültige Bericht trennt nominale Spannungs-/Zeitübereinstimmung, gemessene
Fehlerreaktionen und bekannte Grenzen. Er behauptet keine generelle Fehlersicherheit
und keine optische oder Quantenqualifikation. **Für die Fortsetzung fehlen der
identifizierte reale Aufbau, das unabhängige Messgerät und seine Rohaufnahmen.**

## Quellen und Lizenzen

Eigene Build-/Testsoftware: Apache-2.0 wie das Repository. Firmware enthält
unveränderte Pico-SDK-/TinyUSB- und Compiler-Laufzeitbestandteile; zugehörige
Hinweise stehen in [licenses/](licenses/). Die GCC- und Newlib-/Libgloss-Abschnitte
wurden unverändert aus `license.txt` der verwendeten Arm-Toolchain übernommen;
die Compilerwerkzeuge selbst werden hier nicht mitgeliefert. Die beiden
unveränderten Versionsmetadaten stammen aus Raspberry Pis Pico-VS-Code-Projekt
(MPL-2.0); Herkunft und Hashes stehen im Build-Lock.

Primärquellen: [Pico C/C++ SDK](https://www.raspberrypi.com/documentation/microcontrollers/c_sdk.html),
[SDK-Release 2.3.1](https://github.com/raspberrypi/pico-sdk/releases/tag/2.3.1),
[fixierter Werkzeug-Installer](https://github.com/raspberrypi/pico-sdk-tools/tree/4ddc34c32f58be6ddf4fefb966f8e7f367063db9).
Die elektrische Beschaltung und ihre Primärquellen bleiben in der C1-Bauanleitung.
