# Vorläufiges Hardwareprofil und Beschaffungsentscheidung

Recherche: 11. Oktober 2026. Keine Bestellung, kein verfügbares Laborequipment
oder Eigentum des Nutzers vorausgesetzt. Das Profil ist eine prüfbare Auswahl
für die nächste Engineering-Stufe, kein freigegebener Verdrahtungsplan.

## Zielarchitektur

Vier Detektoren → geeignete 50-Ohm-Eingangsstufe → kalibrierte mehrkanalige
Zeitstempelerfassung → Kanal-Sortierung und FIFO/CDC → Ereigniskern → UART-
Snapshot → Raspberry-Python. Die vier Detektoren repräsentieren A+, A−, B+, B−.
Ein parallel erfasster Rohzeitstempelpfad wird für Kalibrierung, Totzeit- und
Nachpulsdiagnostik benötigt. Der Snapshot-UART ersetzt diesen Pfad nicht.

## Kandidaten

| Teil | Vorläufige Auswahl | Status und Konsequenz |
|---|---|---|
| FPGA | Terasic DE10-Nano, bevorzugt vorhandenes Board | Schon im v0.1-Kontext verwendet; tatsächlicher Besitz und Revision offen. Hersteller nennt drei 50-MHz-Taktquellen und zwei 40-Pin-Erweiterungsleisten. |
| Host | Raspberry Pi mit Linux/Python ab 3.10 | Python-Host läuft ohne Zusatzbibliotheken; tatsächlicher Pi-Typ und serieller Port müssen feststehen. |
| Referenzdetektoren | 4 × Excelitas SPCM-AQRH-14 | Konkreter Kandidat aus Herstellerbestellcode: Ausgangsgruppe 1, Dunkelzählklasse 4. Freistrahlversion; Kopplungsoption gegebenenfalls ändern. |
| Alternative | 4 × MPD PDM | Eigene Pegel-/Timingprüfung nötig; TTL-Zähl- und optionale NIM-Timingausgänge unterscheiden sich. |
| Zeitreferenz | Geliehener/zugänglicher kalibrierter Mehrkanal-Time-Tagger | Für den ersten physikalischen Vergleich; z.B. Swabian Time Tagger 20 mit passender Signalkonditionierung. Kein Gerät beschafft oder angebunden. |
| Eigenes endgültiges TDC-Frontend | Noch nicht ausgewählt | FPGA-Carry-Chain-TDC wäre ein eigenes kalibrierpflichtiges Teilprojekt. Keine 1-ps-Genauigkeit aus dem Zahlenformat ableiten. |

## Elektrische Anforderungen aus Herstellerunterlagen

Excelitas verlangt für den Ausgang 50-Ohm-Abschluss und empfiehlt etwa 1 V
Triggerschwelle. Ausgangshöhe und Pulsbreite sind Variantenmerkmale. Eine
3.3-V-FPGA-Eingangsschwelle darf deshalb nicht ungeprüft mit dem als TTL
bezeichneten BNC-Ausgang gleichgesetzt werden. Modell-/Revisionsangaben müssen
am konkreten Modul bestätigt werden. Der Familienleitfaden nennt 5 V Versorgung
und bis zu 1.2 A pro Modul; vier Module ergeben als daraus abgeleitete obere
Versorgungsabschätzung 4.8 A/24 W vor Reserve. Keine Versorgung aus GPIO-Pins.
Der Gate-Eingang ist kein gewöhnlicher hochohmiger GPIO-Eingang.

MPD beschreibt für PDM einen TTL-Zählausgang und optional einen negativen
NIM-Timingausgang. Die bessere Timingangabe des NIM-Pfads darf nicht dem
TTL-Pfad zugeschrieben werden. Auch dieser Pfad benötigt den passenden
Abschluss und Empfänger. Diese Module werden nicht als billige Alternative
behauptet; ein belastbarer Preis liegt hier nicht vor.

Bei einfacher 50-MHz-Abtastung beträgt die Taktperiode 20 ns. Kürzere Pulse
können vollständig zwischen Abtastflanken liegen. Ein Zwei-Flipflop-
Synchronisierer reduziert Metastabilitätsrisiko, erzeugt aber keine fehlenden
Ereignisse und keine sub-ns-Zeitmessung. Pulsstreckung verbessert gegebenenfalls
die Erfassung, stellt die ursprüngliche Ankunftszeit jedoch nicht wieder her.

Der Time Tagger 20 ist laut Hersteller ein 50-Ohm-Gerät mit empfohlenem
Eingangsbereich 0..3 V und mindestens 1 ns Pulsbreite. Diese Angaben betreffen
den Referenzkandidaten, nicht unseren FPGA-Eingang. Jede Verbindung ist gegen
die tatsächlich verwendete Detektorvariante abzugleichen.

## Snapshot-Verbindung zum Pi

Logisch: FPGA `tx` → RX eines verifizierten 3.3-V-UART-Empfängers, gemeinsames
Signalbezugspotential. Alternativ ein geeigneter USB-zu-3.3-V-UART-Adapter.
Raspberry-UARTs arbeiten laut offizieller Dokumentation mit 3.3 V; 5-V-Pegel
sind nicht zulässig. RS-232-Pegel sind ebenfalls kein direkter Ersatz.
Physische FPGA-Pins bleiben bis zur Bestätigung von Boardrevision, Bankspannung
und Pinplan offen. Deshalb enthält dieses Paket keine ungeprüfte QSF-Pinbelegung.
Pi-Pinmux und UART-Gerätename unterscheiden sich nach Modell; keine automatische
Annahme über `/dev/serial0`. Der integrierte DE10-USB-UART ist nicht automatisch
mit dem neuen FPGA-TX-Signal verbunden.

## Frugalität und reale Preisgrenze

Bei der Recherche zeigt DigiKey für SPCM-AQRH-14 einen Einzelpreis von
6'808.75 USD. Vier zum Einzelpreis: 27'235 USD, ohne weitere Komponenten,
Versand und Abgaben. Abruf ist kein verbindliches Angebot; Land und Verfügbarkeit
können den Preis verändern. Dieser Wert macht den Referenzaufbau als kompletten
Neukauf für unser frugales Ziel ungeeignet.

Arbeitsentscheidung: digitale Entwicklung weiterführen; erste optische
Referenzmessung mit geliehenen oder gemeinsam genutzten Detektoren und
Zeitmessgeräten vorbereiten. Erst nach Messung von benötigter Effizienz,
Jitter, Dunkelrate und Wiederholbarkeit lässt sich eine günstigere eigene
Detektorkette sinnvoll spezifizieren. Ein vorhandenes/geprüftes Gebrauchtgerät
wäre separat zu bewerten. Es wurde niemand angeschrieben und nichts bestellt.

## Primärquellen

- Terasic Spezifikation: https://www.terasic.com.tw/cgi-bin/page/archive.pl?CategoryNo=165&Language=English&No=1046&PartNo=2For
- Terasic Dokumentenverzeichnis, Handbuch für Rev. E 2.6 vom 20.02.2025:
  https://www.terasic.com.tw/cgi-bin/page/archive.pl?Language=English&No=1046&PartNo=4Mini-B
- Excelitas Familienleitfaden Rev.2023-1:
  https://www.excelitas.com/de/sites/default/files/assets/product/document/27464.pdf
- Excelitas aktuelle Produktseite: https://www.excelitas.com/product/spcm-aqrh
- MPD: https://micro-photon-devices.com/products/single-pixels/pdm
- MPD Datenblatt: https://www.micro-photon-devices.com/datasheet/MPD_PDM_Datasheet.pdf
- Swabian elektrisches Interface:
  https://www.swabianinstruments.com/static/documentation/TimeTagger/sections/hardware.html
- Raspberry Pi, Herstellerdokumentation:
  https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/configuration/interfaces.adoc
- Preis direkt beim Anbieter:
  https://www.digikey.com/en/products/detail/excelitas-technologies/SPCM-AQRH-14/5885848

Die Excelitas-Webseite und ältere Familienunterlagen nennen teils unterschiedliche
Umgebungsbereiche und Modellangaben. Für eine endgültige Bestellung/Schaltung
ist deshalb das Datenblatt der angebotenen konkreten Variante maßgeblich.
