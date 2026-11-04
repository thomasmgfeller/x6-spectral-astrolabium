# X6 Photonik · Erfassung am Laborplatz v0.1

Die lokale Bedienoberfläche zeichnet entweder FPGA-Zählerframes oder Rohzeitstempel eines Time Tagger Ultra auf. Der Browser läuft auf dem Tablet oder Messrechner. Der Dienst und die Gerätetreiber laufen auf dem Linux-Rechner, an dem die Instrumente angeschlossen sind. Der Stand ist ein Softwarekandidat zur Inbetriebnahme. Die Hardware-Abnahmen G0–G6 und die physische CHSH-Prüfung stehen aus.

## Erster Lauf ohne Geräte

Python ab 3.11 unter Linux genügt für das mitgelieferte Beispiel, die UART-Erfassung und die seriellen Thorlabs-Protokolle. Paket vollständig entpacken und in dessen Verzeichnis wechseln.

```sh
python3 -m unittest -v
python3 labor_server.py --data ./x6-runs
```

1. Die im Terminal ausgegebene Adresse im Browser öffnen, **06 · Gerätelauf** wählen und den dort ausgegebenen Zugangscode eingeben.
2. Verantwortliche Person und Laufbezeichnung eintragen. Für das Beispiel vier Frames ab Sequenz 100 wählen, lokale Vorbereitung bestätigen und Konfiguration einfrieren.
3. Erfassung starten. Der synthetische Lauf endet nach vier gültigen Frames. Im Archiv sind das Manifest, die eingefrorene Konfiguration, das Journal und die 976 Byte Rohdaten verfügbar.
4. Für eine Diagnose die Datei `capture.bin` im Reiter **03 · Daten-Replay** mit Herkunft **synthetisch** und erster Sequenz **100** öffnen. Im realen UART-Lauf die tatsächlich dokumentierte Herkunft und Sequenz verwenden.

## Geräteprofil anschließen

`examples/` enthält zwei Vorlagen. Seriennummern, Hostpfade, Achsenparameter und kalibrierte Schwellen am konkreten Gerät bestimmen. Eine fehlende Achse oder ein fehlender Shutter wird durch Weglassen des gesamten optionalen Feldes angegeben. Nullfelder sind bewusst unbrauchbar. Geräte- und Kalibrierprofile unter eigener Versionskontrolle führen. Vor jedem Hardwarelauf im Browser eine Kalibrierdatei auswählen. Der Dienst prüft ihren Hash und archiviert die Originalbytes. Die inhaltliche Freigabe der Kalibrierung liegt beim Labor.

```sh
python3 labor_server.py --profile mein-geraeteprofil.json --data /pfad/zum/laufarchiv
```

**Tablet im Labor-WLAN.** Auf dem Messrechner den Dienst an dessen konkrete LAN-IP binden. Zertifikat und privater Schlüssel müssen bereits für diese Adresse eingerichtet sein. Das Tablet muss der ausstellenden Stelle vertrauen. Die Adresse unten ist ein Beispiel.

```sh
python3 labor_server.py --profile mein-geraeteprofil.json --data /pfad/zum/laufarchiv \
  --bind 192.168.10.25 --port 8765 --cert /pfad/labor.crt --key /pfad/labor.key
```

Der Zugangscode wechselt mit jedem Dienststart. Der Dienst erlaubt einen aktiven Lauf je Archiv und prüft Ursprung, Zugriffskennung, Lauf-ID und Befehls-ID. Für die Installation ein lokales Konto mit Zugriff auf die benötigten USB-Geräte und ein exklusiv verwaltetes Archiv verwenden. Verschiedene Serverprozesse mit unterschiedlichen Archiven dürfen nicht dieselben Instrumente ansteuern. Die HTML-Datei allein öffnet das Laborbuch im Offlinebetrieb.

## Geräteauswahl

Die Liste deckt Ansteuerung und Erfassung des bestehenden 405/810-nm-Aufbaus ab. Quelle, Spektralfilter, PBS, Faserkoppler, Temperierung und Mechanik sind im Optikplan beschrieben. Vor Beschaffung Netzteile, Stecker, optische Aperturen und die gewählte Modellausführung am konkreten Aufbau abgleichen.

| Anzahl | Modell | Aufgabe und Anschluss | Stand des Adapters |
|---:|---|---|---|
| 4 | Excelitas SPCM-AQRH-14-FC | Fasergekoppelter Si-Detektor für A+, A−, B+, B−. Positiver BNC-Puls. Die 1x-Option ist mit nominell 2,2 V spezifiziert. | Zählung über vier TDC-Eingänge. Die Detektoren brauchen Versorgung und lokale Betriebsprüfung. |
| 1 | Swabian Instruments Time Tagger Ultra, 8 physische Eingänge, Performance-Ausführung als Referenz | USB 3 am ausgewählten Linux-Messrechner. Steigende Flanken an Eingängen 1–4. | SDK-Aufzeichnung, Seriennummer, Trigger-Readback, Kanalraten, Segmentzähler, Überlauferkennung und native Rohdateien. |
| 2 | Thorlabs ELL14K | Motorisierte SM1-Drehhalter. Je eine USB-Verbindung mit festem Port und eigener Seriennummer. | Elliptec `in`, `ma`, `gp`. Skalierung aus Gerätedaten. Positionstoleranz, Nullpunkt und Drehsinn werden pro Achse eingefroren. |
| 2 | Thorlabs AHWP05M-980 | Gefasste achromatische Halbwellenplatte für 690–1200 nm im jeweiligen Rotator. | Retardanz und optischen Nullwinkel bei 810 nm messen. |
| 1 + 1 | Thorlabs SH05R/M und KSC101 | Strahlverschluss mit lokalem Steuergerät, USB-VCOM für die Abfrage. | Identifikation und Abfrage des elektrischen Solenoidausgangs. Im Leerlauf kann der Bediener den Ausgang explizit ausschalten und den elektrischen Zustand zurücklesen. Die Anforderung und Rückmeldung stehen in `station.jsonl` im Archivstamm. Mechanische Blattlage, wirksamer Strahlverschluss und Interlock bleiben eigenständige Abnahmen. |
| 1 optional | Terasic DE10-Nano mit passendem X6-Sagnac-v0.7-Bitstream und UART-Adapter | Separater FPGA-Entwicklungspfad. | Passiver SGNCv007-Empfang in vorgegebener Länge. |
| 1 | Linux-Messrechner mit USB 3 und lokalem SSD-Speicher | Vorhandener Rechner mit unterstützter SDK-/OS-Kombination, Tablet als Bediengerät. | Für einen Raspberry Pi das passende ARM64-Herstellerpaket prüfen und den vollen Datendurchsatz lokal nachweisen. |
| je Kanal | 50-Ω-Koax und passende BNC-auf-SMA-Verbindung, FC-kompatible Faser | Elektrische Verbindung vom Detektor zum Tagger, optische Verbindung vom Analysator zum Detektor. | Am Empfänger genau einmal mit 50 Ω abschließen. Pulsform, Polarität, Pegel und Kanalzuordnung am realen Eingang messen. |

**Herstellerunterlagen.** [Excelitas SPCM-AQRH](https://www.excelitas.com/product/spcm-aqrh) · [Swabian Geräteserie](https://www.swabianinstruments.com/static/downloads/time-tagger-series-product-brochure-feb-2026.pdf) · [SDK und Betriebssysteme](https://www.swabianinstruments.com/time-tagger/downloads/) · [SDK-Messklassen](https://www.swabianinstruments.com/static/documentation/TimeTagger/api/measurements/index.html) · [ELL14-Handbuch](https://thorlabs-prod4us-store.govirto.com/api/thorlabs-products/support-documents/ELL14K/DTN000522-D02.pdf) · [Elliptec-Protokoll](https://www.thorlabs.com/Software/Elliptec/Communications_Protocol/ELLx%20modules%20protocol%20manual_Issue10.pdf) · [Wellenplattendaten](https://www.thorlabs.com/catalogpages/v21/916.pdf) · [Shutter und Controller, Herstellerdaten](https://www.thorlabs.com/catalogpages/Obsolete/2025/SC10.pdf) · [KSC101-Protokoll](https://www.thorlabs.com/Software/Motion%20Control/APT_Communications_Protocol.pdf)

## Ablauf je Quelle

**SGNCv007.** UART-Pfad und Baudrate am Host konfigurieren. Den erwarteten ersten 64-Bit-Sequenzwert am Sender bestimmen. Erst den Empfänger starten, dann die Ausgabe am FPGA lokal auslösen. Kein Flush, kein Resynchronisieren. Magic, Version, Länge, fortlaufende Sequenz, CRC32, Flags, Konfiguration und Bilanz der Zähler werden geprüft. Der Dienst speichert gelesene Bytes auch bei einem ungültigen Frame oder einer Zeitüberschreitung. Die vier Kanalraten beziehen sich auf das Zeitintervall des letzten gültigen Frames.

**Time Tagger.** Offizielles Swabian-SDK einschließlich Python-Bindings für die verwendete Python- und OS-Version installieren. Die Implementierung richtet sich nach der API 2.22.6. Die Kanäle 1/2/3/4 entsprechen A+/A−/B+/B−. Das SDK muss über die tatsächliche Seriennummer genau das ausgewählte Gerät öffnen. Der Dienst prüft den Zustand der internen Testsignale, Ereignisteiler und Triggerschwellen. Diese Prüfung vor Ort mit eingespeisten Referenzpulsen ergänzen.

* **Einzelsegment.** Dauer 1–3600 s. Keine Motorbewegung und keine automatische Winkelzuweisung. Geeignet für Dunkel- und Referenzmessungen. Ein Segment mit null Pulsen kann regulär enden.
* **Stellfolge.** Es gilt die byteidentische Datei `examples/schedule.csv` aus dem Optikplan. Jeder Lauf umfasst 80 Segmente zu 30 s, insgesamt 40 min Erfassung und mindestens 2 min 40 s Einschwingzeit, zusätzlich Positionierung, USB- und Dateizeit. Die Achsen örtlich referenzieren und optisch kalibrieren. Der Dienst liest beide Encoder nach der jeweiligen Bewegung zurück und wartet anschließend zwei Sekunden. Danach startet die zeitbegrenzte SDK-Messung. Übergänge sind Aufzeichnungslücken zwischen Segmenten. Jedes Segment hat eine eigene native `.ttbin`-Aufzeichnung, ggf. mit SDK-Teildateien, sowie Metadaten für Einstellung, Achsenrückmeldung, Kanalzählungen und Segmentabschluss.
* **Laufende Anzeigen.** Die vier Raten sind SDK-Mittelwerte seit Segmentbeginn. Die gespeicherten Tags, Überläufe und Encoderpositionen haben eigene Anzeigen. Fehlende Werte bleiben als unbekannt sichtbar. Ein Überlauf oder widersprüchliche Endzähler beendet den Lauf als Fehler.
* **Abbruch.** Der Host beendet die Erfassung und startet kein weiteres Segment. Ein bereits an den ELL14 übermittelter Fahrbefehl kann am Gerät zu Ende laufen. Eine unterbrochene Aufzeichnung bleibt zur Fehleranalyse erhalten. Laserfreigabe, Öffnen des Shutters und unmittelbares Unterbrechen des Strahls erfolgen am Messplatz.

**Wissenschaftliche Grenze.** Die 80 Segmente liefern segmentierte Hersteller-Rohdaten. Für eine Primärmessung nach OPTIK-CHSH-0.1 fehlen die geprüfte Überführung in das kanonische 24-Byte-Ereignisformat, die Behandlung der Übergänge und die unabhängig validierte Ereignispaarung. Die Auswertung der separaten FPGA-Fensterframes ist im Reiter 03 verfügbar. X6-QED benötigt einen Surface-Code-Detektorvektor und einen passenden FrozenGraph. Der Photoniklauf erhält deshalb keine QED-Freigabe.

## Archiv und Überprüfung

Jeder Lauf bekommt ein neues Verzeichnis unter `--data`. Das Manifest dokumentiert den Abschlusszustand und SHA-256 je Datei. Im eingefrorenen Profil stehen die Identität der ausgeführten Software, die Geräteparameter und der Hash der Kalibrierdatei. Unterbrechungen ohne Abschluss werden beim nächsten Start mit demselben Archiv als `INTERRUPTED` aufgenommen. Liegt ein Schreibfehler vor, Datenträger prüfen und das gesamte Laufverzeichnis sichern. Der Dienst überwacht während der Erfassung eine Mindestreserve von 64 MiB. Der Lasttest muss den tatsächlich verfügbaren Platz und die Schreibrate über die volle geplante Laufdauer prüfen.

```sh
python3 verify_run.py x6-runs/LAUF_ID
```

Die Prüfung erkennt fehlende, zusätzliche und veränderte Dateien relativ zum lokalen Manifest. Für eine unabhängige Archivkopie das Manifest separat aufbewahren. Bei Kopie über die Oberfläche alle im Manifest aufgeführten Dateien mitnehmen. `COMPLETE` bezeichnet den Abschluss der Aufzeichnung. Das Manifest enthält separat `physical_qualification: NOT_RUN`.

## Erste Prüfungen am realen Platz

1. Mit gesperrtem Strahlweg Bedienoberfläche, Datenträger, Abbruch und erneutes Verbinden testen. Detektorpegel und Quellenidentität protokollieren.
2. Einen elektrisch charakterisierten Testpuls nacheinander auf 1–4 geben. Kanalzuordnung, Polarität, Raten und Rohdateien prüfen. Danach Gleichzeitigkeit, feste Offsets, Differenzjitter und Verlust unter Last bestimmen.
3. Achsen referenzieren, jede der vier Einstellungen mit unabhängigem Polarisationsnachweis prüfen. Beim Shutter den angezeigten Magnetzustand und die physische Unterbrechung getrennt prüfen.
4. Dunkellauf, Kalibrierung, Drift und Negativkontrollen nach Optikplan archivieren. Erst mit unabhängig geprüfter Rohdatenkette und bestandenen technischen Toren den wissenschaftlichen Primärlauf freigeben.

## Herkunft

Die beiden Dateien unter `vendor/` mit der Endung `.py`, das synthetische Binärbeispiel, Messplan und Protokoll stammen aus X6-Referenzstand `69db6c69dc580b6d2889d5ee5c5aa4d90034e85f`. Die unveränderten Sagnac-Module stehen unter der beigefügten MIT-Lizenz. Für die X6-Anteile gilt die im Paket enthaltene Apache-2.0-Lizenz. Hersteller-SDKs sind separat zu beziehen. [X6-Referenzstand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/69db6c69dc580b6d2889d5ee5c5aa4d90034e85f)
