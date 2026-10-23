# Kaskoden-Frontend - Schaltplan v0.1

[Schaltplan als PDF](../../manuals/Kaskoden_Schaltplan_v0_1.pdf) · [Originales KiCad-Paket herunterladen](../../downloads/Kaskoden_Schaltplan_v0_1_KiCad.zip) · [Photonik-Projekt](../../README.md)

Stand: 23.10.2026. **Erster elektrischer Entwurf, keine Fertigungsfreigabe.**

Das Paket setzt den veröffentlichten PCB-Vorschlag in einen bearbeitbaren
KiCad-Schaltplan um. Es enthält ein dreiblättriges Frontend und einen getrennten,
einblättrigen Empfängeradapter. Die Hochspannungsversorgung, der eigentliche
APD-/Quench-Leistungspfad und die Totzeitlogik gehören noch nicht zu diesem Stand.
Die Schnittstellen zu diesen Baugruppen sind explizit beschrieben.

## Dateien öffnen

- [Kaskoden_Schaltplan_v0_1.pdf](../../manuals/Kaskoden_Schaltplan_v0_1.pdf): vier Schaltplanblätter im A3-Querformat, anschließend zwei Seiten Erläuterung.
- `kicad/Frontend.kicad_pro`: Hauptprojekt; `Frontend.kicad_sch` ist das Wurzelblatt.
- `kicad/Receiver_Adapter.kicad_pro`: separates Adapterprojekt.
- `kicad/Cascode.kicad_sym`: projektlokale Symbole mit expliziten Pins; auch in den Schaltplänen eingebettet.
- `BOM.csv`: 60 Frontend- und 12 Adapterpositionen. Passive Werte sind Startwerte; noch keine bestellfertige BOM.
- `Frontend.net.xml`, `Receiver_Adapter.net.xml`: echte KiCad-Netzlistenexporte.
- `validation.json`: Verbindungskontrolle und algebraische Vorauslegung.
- `topology_sanity.cir`, `.log`, `topology_waveform.csv`: reproduzierbarer, synthetischer SPICE-Topologietest.

Erzeugt und als PDF/Netzliste geöffnet mit KiCad CLI 7.0.11. Kein PCB-Layout,
keine Gerberdaten. Ein vollständiger KiCad-ERC wurde nicht ausgeführt; die CLI
dieser Version stellt dafür keinen Befehl bereit. Die eigene Netzlistenprüfung
ersetzt den ERC und eine unabhängige Schaltplanprüfung nicht.

Die PDF und das ZIP sind unveränderte Veröffentlichungsartefakte. Die hier direkt
lesbare Kopie enthält dieselben Schaltungs- und Prüfdateien; nur diese Navigation
und das lokale Prüfsummenverzeichnis wurden für die Repository-Ablage angepasst.

## Schaltungsentscheidungen

Der Eingangsstrom erzeugt an R101 = 49,9 Ohm eine Spannung. C101 koppelt sie auf
Q101 ein. Q101 arbeitet in Emitterschaltung, Q102 in Basisschaltung. Ein positiver
Sense-Puls senkt `AN_OUT`. Der Komparator erhält deshalb die Schwelle an VP und
`AN_OUT` an VN; Q erzeugt die positive Ereignisflanke. Der Kollektor erhält keine
50-Ohm-Parallelbelastung.

U101A regelt die mittlere Emitterspannung von Q101 über R106/C102 und R105 auf
ca. 142,86 mV. Mit 47 Ohm entspricht das 3,040 mA Emitterstrom. Bei angenommenem
Beta=100 in beiden Transistoren fließen ca. 2,980 mA durch R104. Diese Unterscheidung
zwischen Emitter- und Kollektorstrom ist in der Rechnung berücksichtigt.

U101B puffert die Q102-Basis auf ca. 1,85 V. Das ersetzt den vorläufigen
1,7-V-Untersuchungswert. Unter angenommenen VBE=0,75 V ergibt sich mehr Reserve
am Kollektor von Q101. Reale VBE-Werte, Temperatur und Streuungen sind noch mit
Herstellermodellen zu prüfen. Die langsame Regelung hält einen Mittelwert; sie
korrigiert weder einzelne Pulse noch jede mögliche Grundlinienverschiebung.

Die BAS70-Dioden sind Niederspannungs-Schutzkandidaten. Sie garantieren keine
Quench- oder Hochspannungsfestigkeit. D101/D102 erhöhen die Eingangskapazität;
D103 begrenzt negative Basis-Emitter-Spannungen. C101 ist keine galvanische
Isolation. **J101 darf nicht direkt an die APD-Hochspannung angeschlossen werden.**

R101 allein macht den Eingang nicht zu einer breitbandig angepassten
50-Ohm-Schnittstelle. J101 ist zunächst der Laboreingang; die spätere lokale
APD-Anbindung ersetzt ihn nach der Schutz-/Quench-Auslegung.

## Schnittstellen

| Anschluss | Belegung / Vertrag |
|---|---|
| J301 | 1 = extern geregelte +3,3 V; 2 = GND. Pilotbetrieb mit 100-mA-Stromlimit. Keine Verpolschutzschaltung vorhanden. |
| J101 | Mitte = SENSE, Schirm = GND. Zunächst 5-25 mV positive Pulse tatsächlich am Knoten; 1/10 kHz, 5/20/100 ns Breite. Anstiegszeit und reale Spannung messen. |
| J203 | 1 GND, 2 SCLK, 3 SDIN, 4 SYNC_N, 5 CMP_EN, 6 3V3_DAC-Messanschluss. 3,3-V-Hostlogik; Pin 6 nicht fremdspeisen. |
| J201 / J202 | Q / QN, jeweils eigenes 50-Ohm-Kabel. Nicht mit dem üblichen Scope-Abschluss 50 Ohm nach GND verbinden. |
| J302 -> J403 | 1 = gemeinsame 3V3_CML/3V3_TERM, 2 = GND. Keine unabhängigen Versorgungen parallelschalten. |
| J404 | 1 EVENT_3V3, 2 GND, 3 QUENCH_3V3, 4 GND. Zwei ungeprüfte RAW-Logiksignale; kurze Verbindungen, keine langen ungetriebenen Kabel. |

Der Adapter terminiert **am Empfangsende** jede CML-Leitung mit 49,9 Ohm nach
3V3_TERM. U401 ist die nicht intern terminierte Variante **SN65LVDS34D**, nicht
SN65LVDT34. Die beiden Eingangsgruppen liegen am selben kurzen Endpunkt, damit
zwei aktive Logikausgänge entstehen. Ihre gemeinsame Eingangskapazität von
nominal etwa 10 pF je Leitung ist ein offener Last-/Reflexionspunkt. Dieser
Adapter ist ein Funktionskandidat und kein Nachweis eines 50-ps-Zeitpfades.

U401 kann bei fehlendem Eingang ein HIGH liefern. Deshalb dürfen weder
`EVENT_3V3` noch `QUENCH_3V3` als selbständig gültige Ereignisse behandelt werden.
Die externe Logik muss Start, Kabelverlust, Shutdown, Hold-off und Wiederfreigabe
qualifizieren. `QUENCH_3V3` ist nur eine Anforderung; es treibt weder eine APD noch
einen Hochspannungsschalter. Der analoge LE/HYS-Pin dient hier der Hysterese,
nicht einem bereits qualifizierten Quench-Blanking.

## DAC und Einschaltfolge

1. Hostausgänge bei unversorgtem Frontend hochohmig halten. CMP_EN zunächst LOW;
   externe Ereignis-/Quench-Verarbeitung gesperrt halten. R203 erzwingt Shutdown.
2. Versorgung einschalten, REF2V5 und den Servo mindestens 1 s einschwingen lassen
   und die DC-Werte prüfen. Diese Zeit ist eine vorläufige Betriebsregel, keine
   gemessene Einschwinggarantie.
3. SPI, MSB zuerst, 24 Bit, Datenübernahme auf fallender SCLK-Flanke:
   `04 01 01` setzt GAIN (REF-DIV=1, BUFF-GAIN=1),
   `03 00 00` aktiviert DAC und interne Referenz. SYNC_N rahmt jeweils 24 Takte ein.
4. Erst nach Prüfung von `AN_OUT` eine passende Schwelle schreiben. Beispiel:
   `08 E1 48` entspricht nominal rund 2,2 V im 2,5-V-Bereich. Dies ist kein
   universell geeigneter Schwellenwert für alle Amplituden.
5. Nach jeder Schwellenänderung mindestens 1 ms warten und den Wert an VTH prüfen.
   Dann CMP_EN HIGH; vor externer Ereignisfreigabe nochmals mindestens 10 us warten
   und den stabilen Ruhezustand prüfen. Keine SPI-Schaltaktivität während der Messung.

Nominal gilt `code = round(VTH / 2.5 * 65536)`, begrenzt auf 0...65535. Der DAC
hat im SPI-Modus keinen Rücklesekanal; eine Spannungsmessung ist erforderlich.
Offset, Hysterese und Eingangsbias des Komparators gehören zur Schwellenkalibrierung.

## Was tatsächlich geprüft ist

- **PASS:** KiCad CLI liest beide Schaltpläne und exportiert vier PDF-Blätter.
- **PASS:** 183 angeschlossene Pins stimmen zwischen realem Netzlistenexport und
  Verbindungsvertrag überein. Kritische Pinzuordnungen und unerwartet offene Netze
  werden zusätzlich geprüft. NC-Pins bleiben ausdrücklich offen.
- **MODELLTEST BESTANDEN:** ngspice 42, synthetische BJT-/Diodenparameter und ideale
  Biasverstärker. Nominaler DC-Punkt und ein kleiner positiver Puls sind plausibel.
  Die Rohdaten liegen bei; das sind keine Messdaten und keine Herstellermodelle.
- **NOT_RUN:** Bauteil-SPICE über Toleranz/Temperatur, Servo-Stabilität/Start,
  Komparator, CML-Leitungen/Adapter, EM, ERC, reale Hardware, HV und Quench.

Die algebraische Reserveprüfung zeigt: Bei 3,135 V Versorgung kann ein
50-mV-Eingangspuls Q102 aus dem angenommenen aktiven Bereich treiben. Daher
zunächst 5-25 mV als Funktionsbereich untersuchen; 50/100 mV dienen der
Aussteuerungs- und Erholungsprüfung. Das ist eine Begrenzung der Vorauslegung,
keine garantierte Spezifikation der realen Schaltung.

Die 50-Ohm-Ziele des PCB-Vorschlags bleiben Routing- und Messanforderungen.
Ein Schaltplan allein stellt sie nicht her. Die Ziele 50 ps Paarstreuung und
200 ps kalibrierter Restfehler bleiben offen.

## Reproduktion

Aus dem Paketverzeichnis, mit KiCad CLI und Python 3:

```bash
kicad-cli sch export netlist --format kicadxml -o Frontend.net.xml kicad/Frontend.kicad_sch
kicad-cli sch export netlist --format kicadxml -o Receiver_Adapter.net.xml kicad/Receiver_Adapter.kicad_sch
python3 validate_design.py
ngspice -b topology_sanity.cir > topology_sanity.log 2>&1
```

Das SPICE-Deck simuliert nur die analoge Topologie. Es lässt ADCMP607, DAC-Dynamik,
Versorgungssequenz, Überlastbegrenzung des Op-Amps, Rauschen und Leitungseffekte weg.
Seine Parameter dürfen nicht als Kennwerte der realen Bauteile übernommen werden.

## Vor dem Routing

1. BFP420- und OPA2333-Herstellermodelle integrieren; DC, Start, Regelstabilität,
   Pulslängen/Rate, Versorgung und Temperatur unabhängig prüfen. Bei Sättigung
   oder wiederholten Schwellwertübertritten die Schaltung korrigieren.
2. Empfängeradapter mit vollständigen Lasten und Leitungen prüfen. Wenn er das
   Zeitbudget verfehlt, einen geeigneteren Empfänger/Fan-out auswählen.
3. APD-Bias, Leistungsschalter, Schutz, Totzeit und Quench-Rückstrom als eigenes
   Blatt auslegen; erst an Ersatzlasten, danach am Detektor testen.
4. KiCad-ERC und unabhängige Pin-/Footprint-Prüfung durchführen. Für ADCMP607
   (CP-12-5, Exposed Pad nominal 1,50 x 1,50 mm) und die konkreten SMA-Stecker
   fehlen freigegebene Footprints. Andere zugewiesene Footprints sind Kandidaten.
5. Hersteller-Stackup bestätigen, dann vierlagiges Layout mit Impedanzcoupon.
   Kein Fertigungsauftrag aus dieser Version.

## Quellen und Grundlage

Die Schaltung und Symbole sind eigene Entwurfsarbeit. Herstellerunterlagen werden
verlinkt, nicht mitgeliefert. Pinbelegungen wurden anhand dieser Primärquellen geprüft:

- [ADCMP606/607 Rev. C, S. 7/10/14](https://www.analog.com/media/en/technical-documentation/data-sheets/ADCMP606_607.pdf)
- [DACx0501 SBAS794E, S. 3/21-23/31](https://www.ti.com/lit/ds/symlink/dac80501.pdf)
- [BFP420 Rev. 3.0, S. 1](https://www.infineon.com/assets/row/public/documents/30/49/infineon-bfp420-datasheet-en.pdf)
- [OPAx333 SBOS351E, S. 4](https://www.ti.com/lit/ds/symlink/opa2333.pdf)
- [BAS70, 01.10.2022, S. 1/3](https://assets.nexperia.com/documents/data-sheet/BAS70.pdf)
- [SN65LVDS33/34 SLLS490B, S. 1/4-6](https://www.ti.com/lit/ds/symlink/sn65lvds33.pdf)
- [Veröffentlichter PCB-Vorschlag, Ausgangsstand PR #125](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/125)

Quellenzugriff: 23.10.2026. Das Paket übernimmt nicht den Nachweisstatus eines
Herstellers oder eines bestehenden Repository-Tests für die neue Hardware.

Eigene Projektbeiträge: Apache-2.0 entsprechend dem X6-Projektumfang.
