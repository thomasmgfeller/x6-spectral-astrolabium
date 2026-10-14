# ACVM 0.2 – optischer Aufbau, Ansteuerung und Prüfsoftware

Stand: 14. Oktober 2026. Ausgangspunkt: veröffentlichter C1-Stand `6df5b9f`.
Diese Erweiterung implementiert den Referenzkern und die langsame optische
Bedienkette. **V01–V08 bestehen im Softwaremodell. V09, V10, ein physischer
optischer Regelkreis und schnelles photonisches Feed-forward sind offen.**
Es war kein optischer Aufbau angeschlossen. Die vorhandenen Konzeptdateien und
das veröffentlichte C1-Paket bleiben historische, unveränderte Dokumente.

| Arbeitsbereich | Jetzt vorhanden | Noch für einen physischen Abschluss nötig |
|---|---|---|
| Optischer Aufbau | Komponentenentscheidung, Anschlusstopologie, Kalibrier- und Abnahmeablauf | Komponenten/Revisionen bestätigen, Kristall und Schleifenspiegel spezifizieren, aufbauen und messen |
| Optische Ansteuerung | ELL14-Serielladapter; Wellenplattenwinkel; kalibrierungsgebundener QHQ-Phasensteller; Intensitätssteller HWP/PBS | Motor-/Optik-Seriennummern, Encodermaßstab, Achsnullen, Retardanz und Übertragung messen |
| Regelung | Begrenzter PI-Regler, PM100D-Rückmeldung, Fehlerabbruch, vollständiger Modellvergleich | Kontrollierte und ungeregelte Laborläufe; unabhängige Leistungsmessung und Driftprüfung |
| ACVM | D01-Compiler, unabhängiger Binärleser, Zustandsautomat, Archiv/ZIP, V01–V08, V09/V10-Auswerter | Pico-Zielbuild und elektrische/optische Abnahme; FPGA und schneller Feed-forward-Pfad |

## Frischer Checkout

Linux, Python 3.12 und `g++` (C++17) genügen für die ACVM-Softwareprüfung.
Keine zusätzlichen Python-Pakete und kein angeschlossenes Gerät erforderlich.
Die bestehende `setup --profile core`-Umgebung kann verwendet werden.
Der vollständige Checkout-Test einschließlich bestehender X6-Integrationsmodule
benötigt zusätzlich Git und Node.js ab Version 22 und verwendet genau diesen
Setup-Befehl. Direkte Python-Tests müssen anschließend mit dessen Interpreter laufen.

```sh
python3 x6.py acvm qualify --output runs/acvm-v02
python3 x6.py acvm verify runs/acvm-v02/D01
python3 x6.py acvm export runs/acvm-v02/D01 --output runs/acvm-d01.zip
python3 x6.py acvm verify runs/acvm-d01.zip
python3 x6.py acvm assess-electrical experimental/acvm/examples/electrical-simulated.json --output runs/electrical-analysis.json
python3 x6.py acvm assess-optical experimental/acvm/examples/optical-measurements-simulated.json --output runs/optical-analysis.json
python3 x6.py acvm fit-hwp experimental/acvm/examples/hwp-scan-simulated.json --output runs/hwp-fit.json
python3 x6.py acvm feedforward-budget experimental/acvm/examples/feedforward-assumptions.json --output runs/latency-budget.json
```

Ausgabeziele müssen neu sein. Vorhandene Ergebnisdateien werden nicht
überschrieben. `qualify` schreibt auch bei Fehlern einen FAILED-Bericht.
Der D01-Export enthält alle 512 komplexen Samples, Sollplan, vollständige
Ausführungsereignisse und SHA-256-Inventar. ZIP-Import prüft Pfade, Größen,
Duplikate, alle Bytes und die Übereinstimmung von Plan, Samples und Modelllauf.
Hashes sichern Integrität, keine Urheberschaft oder physische Herkunft.

## Bedienung angeschlossener Geräte

Die mitgelieferten Profile sind ausdrücklich **nicht ausführbare Vorlagen**.
Zahlen wie `pulses_per_degree=1000` sind Testwerte und keine ELL14-Spezifikation.
Erst ein ausgefülltes Inbetriebnahmeprotokoll begründet ein `MEASURED`-Profil.
Die Software kann die Wahrheit dieser Deklaration nicht authentifizieren.

Nach der dokumentierten Inbetriebnahme, mit tatsächlichem Port und Profil:

```sh
python3 x6.py acvm move --profile mein-motorprofil.json --port /dev/serial/by-id/MEIN-GERAET --degrees 22.5 --output runs/move-001
python3 x6.py acvm phase --profile mein-qhq-profil.json --port /dev/serial/by-id/MEIN-BUS --radians 1.5707963267948966 --output runs/phase-001
python3 x6.py acvm loop --profile mein-regelprofil.json --port /dev/serial/by-id/MEIN-MOTOR --calibration meine-kalibrierung.json --meter USB0::HERSTELLER::MODELL::SERIAL::INSTR --visa-backend @py --output runs/loop-001
```

`move --degrees` erwartet **Motorwinkel**, keine Analysatorachse. Für lineare
Analyse mit auf H/V ausgerichteter QWP gilt im idealen Fall
`Motorwinkel = kalibrierter Nullwinkel + Richtung × Analysewinkel/2`.
Die QWP muss hierfür korrekt ausgerichtet sein. Allgemeine elliptische
Analysebases benötigen das kalibrierte Jones-Modell.

`phase` verwendet drei getrennt adressierte Motoren für Q–H–Q in Strahlrichtung.
Es prüft alle Zielwinkel vor Ausgabe, identifiziert alle drei Geräte und bewegt
sie nacheinander. Während der Bewegung ist kein definierter Endzustand zugesagt;
Messung/Photonenauswertung erst nach abgeschlossener Bewegung und Einschwingen.
Bei einem Teilfehler können bereits bewegte Achsen in ihrer neuen Position stehen.
Der Befehl bestätigt keine optisch gemessene Phase.

`loop` ist ein langsamer Intensitätsregelkreis für klassisches Referenzlicht
um 810 nm. Er nutzt eine monotone, gemessene HWP/PBS-Kennlinie, begrenzte
Stellgeschwindigkeit, Anti-Windup, eine endliche Laufzeit und Abbruch bei
unplausibler/veralteter Messung. Nach Abschluss wird eine konfigurierte
Parkstellung angefordert. Bei Verbindungsverlust bleibt deren Zustand UNKNOWN.
Eine Motorparkstellung ist kein verifizierter Strahlverschluss.

Nur für diesen echten PM100D-Pfad benötigt man PyVISA samt lokal passendem
VISA-/USB-Backend. Die getestete Softwarequalifikation umfasst die VISA-ähnliche
Testschnittstelle, **keine Installation oder Verbindung zu einem PM100D**.
Die [PyVISA-Dokumentation](https://pyvisa.readthedocs.io/en/latest/introduction/resources.html)
beschreibt Backend, Zeitlimits und Terminatoren. Keine automatische Geräteauswahl.
PM100D2/PM100D3, LCC25, TFLN-Treiber und beliebige SCPI-Geräte sind nicht freigegeben.

## Unterlagen

- [Ausführbares Quellpaket mit Rohberichten](ACVM_Optik_Referenz_v0_2.zip),
  [Paket-Prüfnachweis](PACKAGE.json); nach Entpacken zuerst `START_HERE.txt` lesen.
- [Aufbau und konkrete Komponenten](HARDWARE.md)
- [Kalibrierung und Laborabnahme](CALIBRATION.md)
- [Architektur, Formate und Nachweisgrenzen](ARCHITECTURE.md)
- [Prüfmatrix und Ergebnisse](VALIDATION.md)
- [Primärquellen](SOURCES.md)
- `evidence/`: unveränderte Rohberichte der durchgeführten Softwareprüfungen.

Die SGNCv007-Erfassung bleibt ein getrennter, lesender Messpfad. Es wurden keine
Motorbefehle in diesen Snapshot-Datenstrom oder in die Browseroberfläche eingebaut.
