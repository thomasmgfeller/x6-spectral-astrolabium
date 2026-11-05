# ppKTP-/PBS-/HWP-Anfragen und Arbeits-BOM v0.1

**Stand 05.11.2026. Gesamt-BOM: HOLD. Reale Hardwareprüfung: NOT_RUN.**

Drei ausgearbeitete englische Lieferanfragen mit 31 einzeln beantwortbaren Anforderungen und eine komponentengenaue Arbeits-BOM mit 83 Positionen. Alle 35 optischen Positionen des [Gaussian-/Layoutentwurfs v0.1](../gaussian-layout-v0.1/README.md) sind zugeordnet. Das Paket wurde nicht an Lieferanten versendet; Angebote, Bestellungen und Herstellerzusagen liegen nicht vor.

## Dateien

| Datei | Inhalt |
|---|---|
| [Gesamtdokument (PDF)](X6_Photonik_RFQ_BOM_v0_1.pdf) | 18 Seiten mit Befunden, Integration, BOM, Quellen und allen drei Anfragen |
| [Bearbeitbare BOM (XLSX)](X6_Photonik_BOM_v0_1.xlsx) | Drei Blätter: BOM, Angebote und Lieferantworten; Preisformeln je Währung und Umfang |
| [Vollständiges Prüfpaket (ZIP)](X6_Photonik_RFQ_BOM_v0_1_Pruefpaket.zip) | Unverändertes geliefertes Paket einschließlich Einzelanfragen und Prüfsummen |
| [ppKTP-Anfrage (PDF)](RFQ-KTP.pdf) / [Text](RFQ-KTP.txt) | Raicol: Bulk-Typ-II, Polung, Temperatur, bidirektionale Spektren, Achsen und Fassung |
| [PBS-Anfrage (PDF)](RFQ-PBS.pdf) / [Text](RFQ-PBS.txt) | Newlight: Ports, Extinktion, Phase, Dispersion und reale Glaswege |
| [HWP-Anfrage (PDF)](RFQ-HWP.pdf) / [Text](RFQ-HWP.txt) | Newlight: Halb/Halb bei 405/810 nm, Retardanz, Achsen und Gruppenlaufzeit |
| [BOM und RFQ-Daten (JSON)](BOM_und_RFQ_Daten.json) | Artikelkandidaten, Mengen, Anforderungen, Quellen und leere Angebotsfelder |
| [Dokumentarische Validierung](Validierung.json) / [Workbook-Prüfung](workbook_checks.txt) | Umfang und Grenzen der bereits ausgeführten Prüfungen |
| [SHA-256](SHA256.json) | Identität der zwölf Dateien des Originalpakets; kein physikalischer Nachweis |

## Beschaffungsstatus und entscheidende Lücken

| Status | Positionen | Bedeutung |
|---|---:|---|
| VERIFIED | 0 | Auswahl und Schnittstellen für den Einsatzzweck vollständig dokumentiert geprüft |
| OPEN | 32 | Auswahl oder Lieferdaten fehlen |
| HOLD | 51 | Konkrete Spezifikationslücke oder entscheidende Abhängigkeit blockiert den Freeze |

Bestätigte **Katalogangaben** werden separat ausgewiesen. Sie machen eine Zeile nicht automatisch zu einer systemseitig verifizierten oder bestellfertigen Position. Fehlende Hersteller-Bestellcodes bleiben leer; interne Spezifikations-IDs sind keine Hersteller-Artikelnummern. Historische Katalogquellen belegen keine aktuelle Lieferbarkeit oder Preise. Die Mechanikposition `MECH-POST` enthält noch eine unbekannte Menge und muss vor Bestellung aufgelöst werden.

- `PBS0012-405/810` ist ein konkreter 12,7-mm-Kandidat. Die veröffentlichte Familienangabe **>300:1** belegt das Projektziel **1000:1 je relevantem Port und Band** nicht. Das bisherige Worksheet nahm zudem einen 10-mm-Würfel an.
- `WPD03-H810-H405` ist die angefragte Halb/Halb-Ausführung. `WPD03-H810-F405` ist kein gleichwertiger Ersatz. Reale Dicke, spektrale Retardanz, Achsen und differentielle Gruppenlaufzeit fehlen.
- Der ppKTP ist eine kundenspezifische Anfrage. Polungsperiode und Arbeitstemperatur werden anhand der tatsächlichen Pumpwellenlänge festgelegt.
- Filterkurven, CW/CCW- und A/B-Spektren, Halterumrisse und die elektrische Detektor-/Zeitstemplerkette müssen geschlossen werden. Referenzdetektoren und Zeitstempler werden bevorzugt als Leihgeräte eingeplant; Bestand ist nicht vorausgesetzt.

Die vollständigen Primärquellen und ihr jeweiliger Geltungsumfang stehen im PDF, im Quellenregister der BOM und im JSON. Grundlage sind [Optikplan v0.1](../optikplan-v0.1/README.md), [Pump-Eingangsprofil/Systemziele v0.1](../pump-input-v0.1/README.md) und der Layoutentwurf, gelesen bei Commit `85615bf4fe9995aa5a69a95a258067aebaaf9656`.

## Prüfung und Benutzung

Die vorhandene Prüfung umfasst Dateiintegrität, eindeutige BOM-IDs, Zuordnung der 35 Layoutpositionen, vier Detektor-/Faser-/Endkopplungskanäle, zwei gemeinsame Sammellinsen und die 31 RFQ-Anforderungen. Die Excel-Preisformeln wurden mit fehlenden Werten, echter Null, Währung, Angebotsreferenz, Mengen und Umfangsänderung geprüft. Native Excel-Ausführung wurde nicht getestet. PDF-Seiten und Tabellenblätter wurden visuell kontrolliert. Diese Aussagen beziehen sich auf die gelieferten Dateien; sie sind keine Messungen am Aufbau.

Angebote je RFQ-ID in `Lieferantworten` dokumentieren, garantierte Werte von typischen Angaben trennen und jede Abweichung explizit bewerten. Preise erst aus konkreten Angeboten eintragen. Basis, Prüfmittel und Optionen sowie verschiedene Währungen werden getrennt betrachtet; erfasste Teilbeträge sind kein vollständiges Budget. Der Eigen-SPAD-/CML-Pfad und FPGA-Pfad bleiben getrennte Entwicklungsoptionen.

Vor Bestellfreeze: tatsächliche Pumpmessung, Lieferantworten, aktualisierte Strahlrechnung einschließlich 810-nm-Kopplung, mechanische Kollisionsprüfung und elektrische Schnittstellenprüfung schließen. Wareneingang und Systemabnahme erhalten eigene Messnachweise.

Die übrigen Dateien entsprechen bytegenau dem gelieferten Paket; diese README ergänzt ausschließlich die GitHub-Navigation. Die Repository-Inventare erfassen auch das ZIP und diese README. Lizenz: [Apache-2.0](../../../../LICENSE); Herstellerunterlagen werden verlinkt, nicht als fremde Volltexte mitverteilt.
