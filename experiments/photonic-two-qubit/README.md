# Photonischer Zwei-Qubit-Versuchsaufbau

**Entwurf und digitale Referenz · Experimental preview · Dokumentationsstand 05.11.2026**

Geplant ist eine polarisationsverschränkte Photonenpaarquelle mit einem Typ-II-ppKTP-Sagnac-Interferometer, zwei lokalen Polarisationsanalysatoren und vier Detektorkanälen. Veröffentlicht werden die vorhandenen Entwurfsunterlagen, CAD-Dateien, Auswertungen und digitalen Referenzkerne. **Es liegen in diesem Paket keine Labormessungen des Gesamtaufbaus vor.**

**English abstract.** This is a proposed photonic two-qubit experiment with a software/RTL reference, not a demonstrated quantum processor. The Sagnac source architecture is supported by published quantum-optics literature. Included numerical results use synthetic data or mechanical models. No physical entanglement, Bell violation, timing accuracy, quantum advantage or hardware readiness is claimed for this implementation.

## Was die Veröffentlichung belegt

| Ebene | Verfügbar | Noch offen |
|---|---|---|
| Optik | Funktionsentwurf und CHSH-Protokoll; Gaussian-Worksheet und maßstäblicher Layoutentwurf; RFQs und Arbeits-BOM mit 83 Positionen; Polarisationstransfer, Filterbudget und spektraler Prüfplan | Lieferantenspezifische Freigabe, mechanisch geprüfte Strahlführung, Aufbau, Charakterisierung |
| Detektion | Elektrischer Referenzvertrag und getrennte Eigenfrontend-/Benchmark-Prüfmatrix; 47 synthetische Softwaretests | Reale Pegel-, Timing-, Verlust- und optische Detektormessungen; APD-/Quenchpfad und Leitungsadapter |
| Digitalteil v0.7 | Vierkanal-Fensterklassifikation, UART-TX, Decoder, CHSH-Auswertung, Simulationstests | Qualifiziertes Detektor/TDC-Frontend, FPGA-Pinplan, Boardtests |
| Astrolabium | Bereits veröffentlichter SGNCv007-Import, lokale Bridge und synthetische Demo | Ende-zu-Ende-Prüfung mit realer Messkette |
| JIG-F1 | Fertigungsentwurf mit STEP, STL, DXF, Bauanleitung und Modellrechnungen | Fertigung, Wiederholbarkeit, Drift, Klebe- und Übergabeversuche |
| Tomografie v0.8 | Separat gekennzeichnete Planung | Protokollerweiterung, Implementierung, Unsicherheitsmodell und Messungen |

Die Bezeichnung „Zwei-Qubit“ beschreibt zwei geplante Polarisationsfreiheitsgrade, einen pro Photonenarm. Sie behauptet weder deterministische Qubit-Erzeugung noch programmierbare Zwei-Qubit-Gatter. Ältere Formulierungen wie „Quantenkern“ sind Projektbezeichnungen. Maßgeblich ist der Status in [SCIENTIFIC_STATUS.md](SCIENTIFIC_STATUS.md).

## Laborbuch und Gerätelauf

**[Betriebspaket v0.1 herunterladen](downloads/X6_Photonik_Laborbetrieb_v0_1.zip)** · [Startanleitung und Geräteliste](laborbetrieb-v0.1/README.md) · [HTML-Laborbuch](laborbetrieb-v0.1/X6_Photonik_Laborbuch.html)

Auf dem Linux-Messrechner das Paket entpacken und `python3 labor_server.py` starten. Ohne Geräteprofil lässt sich der vollständige Ablauf mit vier synthetischen Frames ausprobieren. Der Reiter **06 · Gerätelauf** verbindet sich mit dem lokalen Dienst. Er zeigt Erfassungsstatus, Kanalraten und Geräteantworten an und stellt die archivierten Rohdaten bereit. Der Stand umfasst 19 Softwaretests mit virtuellen Anschlüssen und einem SDK-Testadapter. Geräteabnahme und physischer CHSH-Nachweis stehen aus.

## Einstieg und Unterlagen

- **[Referenzdetektion elektrisch qualifizieren; Eigenfrontend getrennt charakterisieren v0.1](hardware/detection-qualification-v0.1/README.md)** — 15 Referenzprüfungen, 10 Frontendprüfungen, sieben optische Detektormetriken; PDF, leere Messvorlagen und 47 bestandene Softwaretests. Reale Hardwarequalifikation `NOT_RUN`, BOM-Freeze `HOLD`.

- **[Polarisationstransfer, Filterbudget und spektrale Prüfmatrix v0.1](optics/polarisation-filter-spektral-v0.1/README.md)** — 16 CW/CCW-Transferschritte, vier Excel-Arbeitsblätter, 23 Prüfungen und 15 bestandene Rechentests. Serienfilterkurven, komplexe Transferdaten und reale Spektren fehlen; Hardware `NOT_RUN`, BOM-Freeze `HOLD`.

- **[ppKTP-/PBS-/HWP-Anfragen und komponentengenaue BOM v0.1](optics/rfq-bom-v0.1/README.md)** — [Gesamt-PDF](optics/rfq-bom-v0.1/X6_Photonik_RFQ_BOM_v0_1.pdf), [Excel-BOM](optics/rfq-bom-v0.1/X6_Photonik_BOM_v0_1.xlsx), [vollständiges Paket](optics/rfq-bom-v0.1/X6_Photonik_RFQ_BOM_v0_1_Pruefpaket.zip). Drei englische Anfragen mit 31 Prüfpunkten; 83 BOM-Positionen und Zuordnung aller 35 optischen Layoutpositionen. 32 `OPEN`, 51 `HOLD`; Hardware `NOT_RUN`. Anfragen vorbereitet, nicht versendet.

- **[Pump-Eingangsprofil und Systemziele v0.1](optics/pump-input-v0.1/README.md)** — [ausfüllbares PDF](optics/pump-input-v0.1/X6_Pump_Eingangsprofil_Systemziele_v0_1.pdf), [Prüfpaket](optics/pump-input-v0.1/X6_Pump_Eingangsprofil_v0_1_Pruefpaket.zip); Bezugsebenen P0/P1/PC, Messplan und digitale Vorlagen für die nächste Strahlrechnung. Tatsächliche Pumpquelle und Messwerte offen; Hardware `NOT_RUN`, Beschaffung `HOLD`.

- **[Optikplan v0.2 · Quellenüberlappung und Messkette](optics/optikplan-v0.2/README.md)** — [PDF](optics/optikplan-v0.2/Optikplan_v0_2.pdf), [Prüfpaket](optics/optikplan-v0.2/Optikplan_v0_2_Pruefpaket.zip), Rechenmodell und Kalibrierprogramme für spektrale Unterscheidbarkeit, zeitlichen Restversatz, vier Faserkopplungen und Paarjitter. Optische und elektrische Laborabnahme stehen auf `NOT_RUN`.

- **[X6-QED C0.1 · Anschluss an den Zwei-Qubit-Versuchsaufbau](../../docs/research/x6-qed/README.md)** — Synthetische Eingangsprüfung für den d=5-Decoderpfad und gemeinsamer Herkunftsnachweis. Photonik-Snapshots werden am QED-Eingang abgewiesen. CAL und C0-VALIDATION stehen auf HOLD.

- **[Optikplan v0.1 mit CHSH-Abnahmeprotokoll](optics/optikplan-v0.1/README.md)** — [PDF](optics/optikplan-v0.1/Optikplan_v0_1.pdf), [DOCX](optics/optikplan-v0.1/Optikplan_v0_1.docx), [Prüfpaket](downloads/Optikplan_v0_1_Pruefpaket.zip); Bauteilspezifikationen, vierkanalige elektrische Schnittstelle, fester Messplan und bedingte CHSH-Auswertung. 11 Softwaretests bestanden; Hardware und realer CHSH-Nachweis NOT_RUN.

- **[Neu: erster Kaskoden-Schaltplan v0.1](hardware/cascode-schematic-v0.1/README.md)** — [PDF](manuals/Kaskoden_Schaltplan_v0_1.pdf), [KiCad-Paket](downloads/Kaskoden_Schaltplan_v0_1_KiCad.zip); vier Schaltplanblätter, Stückliste und geprüfte Pinverbindungen. Vereinfachter SPICE-Modelltest bestanden; keine Hardware- oder Fertigungsfreigabe.
- **[Kaskoden-Frontend / vierlagiger PCB-Entwurf v0.1](hardware/pcb-cascode-v0.1/README.md)** — [PDF direkt](manuals/PCB_Kaskoden_Frontend_Entwurf_v0_1.pdf); Startwerte und Abnahmeplan, alle Hardwareprüfungen NOT_RUN.
- [Wissenschaftlicher Status und Aussagegrenzen](SCIENTIFIC_STATUS.md)
- [Optischer Funktionsentwurf und offene Bauteilspezifikationen](OPTICAL_DESIGN.md)
- [Stufenweises Laborprotokoll](LAB_PROTOCOL.md)
- [Reproduktion der Software- und Modellprüfungen](REPRODUCE.md)
- [Literatur, Datenblätter und Quellenkritik](SOURCES.md)
- [Herkunft und Dateiprüfsummen](PROVENANCE.json) sowie [Lizenzumfang](LICENSES.md)
- [Astrolabium-Anbindung](../../docs/SAGNAC_INTEGRATION.md)

Astrolabium: [Research App](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/).

## Aktueller Entwicklungsstand zum Herunterladen

| Paket | Inhalt / Einordnung |
|---|---|
| [Optikplan v0.1 – vollständiges Prüfpaket](downloads/Optikplan_v0_1_Pruefpaket.zip) | PDF/DOCX, Protokollvorlage, 80 Messsegmente, statistischer Prüfer, 11 Tests, synthetisches Beispiel und Prüfsummen; keine Hardwarefreigabe |
| [Sagnac v0.7 komplett](downloads/Sagnac_v0_7_UART_Host_und_Hardwareplan.zip) | RTL, Host, Tests, Hardwareplan, Metrologie, synthetische Beispiele und ursprüngliche Prüfprotokolle |
| [Sagnac v0.7 im Browser lesen](reference/sagnac_v0_7/README.md) | Unveränderte Quelltextauswahl; komplette historischen Logdateien im ZIP |
| [JIG-F1 Baupaket v0.1.1](downloads/JIG_F1_FabLab_Baupaket_v0_1_1.zip) | Vollständige CAD- und Fertigungsunterlagen; Dokumentationskorrektur, Geometrie v0.1 unverändert |
| [JIG-F1 Bauanleitung v0.1.1 (PDF)](manuals/JIG_F1_Bauanleitung_v0_1_1.pdf) | 14 Seiten; getrennte 1:1-Druckseiten für P02 und P03; Ausdruck am Kontrollmaß prüfen |
| [Einkanal-Messkette v0.2](downloads/Photonische_Messkette_v0_2_Einkanal.zip) | Separates SPAD/AQC-Entwicklungsprojekt mit Python-Auswertung; kein fertig qualifizierter Sagnac-Detektor |
| [Einkanal-Prüfbericht (PDF)](manuals/Photonische_Messkette_v0_2_Pruefbericht.pdf) | Ursprünglicher Bericht mit synthetischen Tests und offenen Hardwarefreigaben |
| [Kaskoden-Schaltplan v0.1 (PDF)](manuals/Kaskoden_Schaltplan_v0_1.pdf) | Vier Schaltplanblätter plus Auslegung/Prüfstand; Analogfrontend und separater CML-Empfängeradapter |
| [Kaskoden-Schaltplan v0.1 (KiCad-Paket)](downloads/Kaskoden_Schaltplan_v0_1_KiCad.zip) | Bearbeitbare Projekte, BOM, Netzlisten, Verbindungsprüfung und synthetischer SPICE-Modelltest; HV/Quench und Qualifikation offen |
| [Kaskoden-PCB-Entwurf v0.1 (PDF)](manuals/PCB_Kaskoden_Frontend_Entwurf_v0_1.pdf) | Vierlagiger Einzelkanal, Kaskoden-Startwerte, 50-Ω-Ausgänge und vorgeschlagene Abnahme; kein geroutetes PCB oder Fertigungsnachweis |
| [Optionale Tomografie v0.8](optional/Sagnac_v0_8_Optionaler_Weiterentwicklungsvektor.txt) | Planung, nicht implementiert oder aktiviert |

## Historische Entwicklungsstufen

Diese vollständigen Originale dienen der Nachvollziehbarkeit. Sie sind keine austauschbaren Komponenten der heutigen Messkette.

- [Sagnac v0.6](downloads/Sagnac_v0_6_Referenzkern_und_Pruefprotokoll.zip): Vorgänger des Vierdetektor-Referenzkerns.
- [Photonische Messkette v0.1 – Auswertung](downloads/Photonische_Messkette_v0_1_Auswertung.zip) und [Digitalkern](downloads/Photonische_Messkette_v0_1_Digitalkern.zip): früherer **H/A/B-Herald-Ansatz**, mit anderer Messgröße und Ereignisdefinition.
- [JIG-F1 Originalpaket v0.1](downloads/JIG_F1_FabLab_Baupaket_v0_1.zip) und [ursprüngliche separate Bauanleitung](archive/JIG_F1_Bauanleitung_original_v0_1.pdf): historische Fassungen; für Druckvorlagen v0.1.1 verwenden. Die beiden ursprünglichen PDFs haben denselben Text, aber unterschiedliche Renderfassungen.

## Abbildungen richtig lesen

![Prinzipübersicht mit Entwicklungsstatus](figures/Sagnac_Schemas_v0_7_Option_v0_8.png)

Prinzipübersicht aus dem Entwurfsstand. Kein maßstäblicher Strahlplan; keine elektrische Verdrahtungsanweisung. „Quantenkern“ bezeichnet hier das geplante Experiment.

![KI-Konzeptvisualisierung eines geplanten Labors, kein Foto und keine Messdaten](figures/AI_CONCEPT_NOT_PHOTO.png)

**KI-Konzeptvisualisierung, kein Foto eines aufgebauten Experiments.** Geräteformen, Beschriftungen, Leitungen und Anzeigen sind illustrativ. Insbesondere ist die abgebildete FPGA-Platine keine Festlegung gegenüber dem noch offenen Boardplan. Maßgeblich sind die schriftlichen Spezifikationen.

## Nutzen und Beiträge

Der unmittelbare Nutzen liegt in überprüfbaren Ereignisdefinitionen, nachvollziehbarer Auswertung, Testfällen für Fehlzustände und einem nachbaubaren mechanischen Entwurf. Community-Beiträge sind besonders für Optikreview, Timing/CDC, Kalibrierung, statistische Annahmen und unabhängige Reproduktion hilfreich. Messdaten bitte mit vollständigem Protokoll, Rohdaten und Unsicherheiten beitragen; Bilder oder einzelne Kennzahlen genügen nicht als Validierung.

Eine spätere lokale/„Edge“-Auswertung kann Datenübertragung und Reaktionszeiten reduzieren. Für das Gesamtsystem gibt es noch keine gemessenen Latenz-, Leistungsaufnahme- oder Kostenvorteile. Eine GF-651-Anbindung ist hier nicht spezifiziert; ohne belastbare Schnittstellen- und Chipunterlagen wird keine Kompatibilität behauptet.

