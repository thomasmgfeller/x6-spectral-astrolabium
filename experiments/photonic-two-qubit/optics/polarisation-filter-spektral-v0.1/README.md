# Polarisationstransfer, Filterbudget und spektrale Prüfmatrix v0.1

**Rechen- und Prüfstand · 05.11.2026 · Hardware `NOT_RUN` · BOM-Freeze `HOLD`**

Das Paket ergänzt [Gaussian-Worksheet und Layout](../gaussian-layout-v0.1/) sowie [RFQs und Arbeits-BOM](../rfq-bom-v0.1/). Es schließt die ideale Portzuordnung und legt die Rechenvorschriften und Prüfentscheidungen fest. Serienfilterkurven, komplexe Transferdaten und Laborspektren liegen noch nicht vor.

| Bereich | Inhalt | Aussagegrenze |
|---|---|---|
| Polarisation | 16 CW/CCW-Transferschritte; PBS-Ports, physische HWP-Achse, Phasen- und Toleranzmodell | Ideales Modell; keine Komponentenabnahme |
| Filter | Pumpunterdrückung aus Hintergrundzählrate; Transmission, Winkel und Zufallskoinzidenzen; sechs BOM-Positionen | Kataloggrenzen und Entwicklungszuteilungen; keine Serienkurven |
| Spektrum | 23 Prüfungen; A/B und CW/CCW, gemeinsame Spektren, Phase/Kohärenz, Temperatur, Unsicherheit, unabhängige Validierung | Intensitätsüberlapp allein bestätigt keine Kohärenz |

## Dateien

- [Bericht als PDF](X6_Polarisation_Filter_Spektral_v0_1.pdf)
- [Bearbeitbare Excel-Datei](X6_Polarisation_Filter_Spektral_v0_1.xlsx) mit vier Arbeitsblättern und getrennten leeren Messfeldern
- [Vollständiges ursprüngliches Prüfpaket](X6_Polarisation_Filter_Spektral_v0_1_Pruefpaket.zip)
- [Maschinenlesbare Spezifikation und Prüfmatrix](Spezifikation.json), [Rechenergebnisse](Rechenergebnisse.json), [Validierung](Validierung.json)
- [Spektraldaten-Vorlage](Spektraldaten.template.json), [Filterkurven-Vorlage](Filterkurve.template.json), [vorbereitete technische Datenanfrage](Filter_Datenanfrage.txt)

## Reproduktion

Python ab 3.10, ausschließlich Standardbibliothek. Im Verzeichnis dieses Dokuments:

```sh
python -m unittest -v test_analysis
python verify_package.py
python analysis.py
python analysis.py --spectral ausgefuellte_Spektraldaten.json
```

Die 15 Rechentests enthalten Negativkontrollen für falsche Pump-Retardanz, fehlende Phase, identische Intensitäten mit entgegengesetzten Phasen, gleiche Marginalen bei disjunkten gemeinsamen Spektren und fehlende Spektralränder. Die leere Messvorlage wird absichtlich abgewiesen. Die CI ergänzt Paket-, Hash- und Statusprüfungen; sie führt keine Hardwaremessung aus.

`analysis.py` wertet Daten nach der installierten Filter-/Sammelkette aus. Eine Phase pro Rasterzelle setzt ein kohärentes Amplitudenmodell voraus; gemischte Zustände benötigen ein validiertes gegenseitiges Kohärenz-/Dichtematrixmodell. Das Programm erteilt keine Hardwarefreigabe.

Im konservativen Szenario 3 mW bei 405 nm, Detektionswahrscheinlichkeit bis 1 und höchstens 100 pumpbedingte Zählungen/s je Kanal ergibt sich OD ≥13,7865 für den gesamten Pfad. Das ist eine Rechengrenze; gemessene Restleistung vor dem Filter kann sie ersetzen. OD 6 allein schließt dieses Zählratenbudget nicht.

## Herkunft und Status

Die 12 Dateien im ursprünglichen ZIP und das ZIP selbst sind unverändert übernommen. `SHA256.json` beschreibt die ursprünglichen ZIP-Mitglieder; README und Veröffentlichungsprüfung liegen zusätzlich im Repository. `Validierung.json` ist der erhaltene Stand vor Veröffentlichung (daher `github_publication_this_package: NOT_RUN`); der Git-Verlauf dokumentiert den Publikationsschritt.

Grundlage: Commit `f97307cd93070d1a57a62cb2e1c1d4dc232fb45e`. Quellen und neue Zuteilungen sind im Bericht und in `Spezifikation.json` getrennt ausgewiesen. Herstellerunterlagen sind verlinkt, nicht mitgeliefert. Projektmaterial unter der [Lizenz des Repositorys](../../../../LICENSE_SCOPE.md). Es wurde keine Lieferantenanfrage versendet und keine Bestellung ausgelöst.
