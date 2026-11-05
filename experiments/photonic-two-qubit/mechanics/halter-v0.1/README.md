# Halterzeichnungen und CAD v0.1

**Konstruktionsentwurf · 05.11.2026 · Fertigungsfreigabe HOLD · Hardware NOT_RUN**

Sechs eigene CAD-Bauteile und neun bemaßte A3-Zeichnungsblätter konkretisieren Sockel, Stativ, Linsen-/Filterfassung und Moduladapter für den geplanten Aufbau mit 75 mm Strahlhöhe. Die Geometrien sind Entwurfsentscheidungen; reale Glas- und Herstelleranschlüsse sind noch nicht bestätigt.

## Zeichnungen und CAD

- [Zeichnungssatz als PDF](X6_Halterzeichnungen_v0_1.pdf) – neun A3-Blätter, Einzelteilansichten 1:1 bei Druck mit 100 %.
- [Vollständiges CAD-Paket](X6_Halterzeichnungen_v0_1_CAD.zip) – unverändertes ZIP mit PDF, sechs STEP-Volumenkörpern, neun DXF-Blättern, Konstruktionsquelle und Nachweisen.
- [Detaillierte Montage- und Fertigungsgrenzen](README.txt), [Bauteilregister](Bauteile.json), [Validierung](Validierung.json), [Kollisionsprüfung](Kollisionspruefung.json).

| Teil | Funktion | CAD | Zeichnung |
|---|---|---|---|
| H01 | Sockel 50 × 35 × 12 mm mit Langlöchern | [STEP](H01.step) | [DXF](H01_Zeichnung.dxf) |
| H02 | Stativ Ø12 × 41 mm, M6 unten / M4 oben | [STEP](H02.step) | [DXF](H02_Zeichnung.dxf) |
| H03A | Starre Linsen-/Filterfassung, Ø25,4-mm-Szenario | [STEP](H03A.step) | [DXF](H03A_Zeichnung.dxf) |
| H03B | Deckring für H03A, Durchlass Ø22 mm | [STEP](H03B.step) | [DXF](H03B_Zeichnung.dxf) |
| H04 | Moduladapter 60 × 40 × 8 mm | [STEP](H04.step) | [DXF](H04_Zeichnung.dxf) |
| H05 | Faserkoppleradapter 70 × 40 × 8 mm | [STEP](H05.step) | [DXF](H05_Zeichnung.dxf) |

H01 + H02 + H03A ergeben nominal 12 + 41 + 22 = 75 mm ohne Zwischenlagen. H04/H05 benötigen einen anderen Stativabschluss mit M6 oben und eine anhand des tatsächlichen Moduls bestimmte Höhe. Gewinde sind im STEP als Kernlöcher dargestellt; DXF-Dateien enthalten vollständige Zeichnungsblätter und sind keine direkt verwendbaren CNC-Konturen.

## Nachgewiesene Engstelle

Bei zentriert unter O04 und DM angeordneten, zum globalen Raster parallelen H01-Sockeln beträgt der optische Achsabstand 32,212 mm gegenüber 35 mm Sockeltiefe. Die Sockel überlappen damit bereits nominal um 2,788 mm und bei +10 mm O04-Hub um 12,788 mm. **Diese Montageanordnung ist nicht einbaubar.** Seitlich versetzte Befestigungen oder ein gemeinsamer Träger müssen ausgelegt werden. Die Prüfung ist auf dieses Szenario begrenzt; eine globale 3D-Kollisionsfreigabe liegt nicht vor.

H03 ersetzt keine kinematischen Spiegelhalter oder motorisierten Wellenplattenhalter. H04/H05 sind Adapter, keine fertigen PBS-, Kristallofen- oder Fünfachs-Faserkoppelmodule. Glasranddicke, Krümmung, Zwischenlagen, Klemmkraft, freie Apertur, Modulanschlussmaße, Kabel- und Justagezugänge bleiben vor Fertigung zu schließen. Optische Zentren sind keine Grundplatten-Bohrkoordinaten.

## Reproduktion und Integrität

Die ursprünglichen 24 ZIP-Mitglieder und das ZIP selbst sind unverändert veröffentlicht. Zusätzliche Veröffentlichungshilfen sind dieses README und `publication_check.py`. Die Prüfung benötigt Python ab 3.10 und nur die Standardbibliothek:

```sh
python publication_check.py
```

Die ursprüngliche CAD-Prüfung bestätigte sechs gültige zusammenhängende Volumenkörper, Außenmaße und STEP-Reimport mit Volumengleichheit sowie neun fehlerfreie DXF-Blätter und neun visuell geprüfte A3-PDF-Seiten. Die CI prüft Dateiintegrität, Paketgleichheit, Quellenbindung und die unveränderten Statusgrenzen; sie führt keine neue mechanische oder physische Abnahme durch.

Für eine Neugenerierung `build.py` zusammen mit `Layout_Quelle.json` in eine **separate Arbeitskopie** übernehmen. CadQuery 2.7.0, ezdxf 1.4.4, ReportLab und DejaVu-Schriften werden benötigt. Die erneute Ausgabe überschreibt dort Dateien und setzt die Sichtprüfung wieder auf PENDING. STEP-Header und PDF-Metadaten können zeitabhängig sein; reproduzierbar sind die Geometrien, nicht zwingend die Exportbytes.

Quellstand: `eb6022d19179e32e1e652502cdb5556911a4483e`. Verknüpfte Vorarbeiten: [Gaussian-/Layoutentwurf](../../optics/gaussian-layout-v0.1/README.md), [RFQs und BOM](../../optics/rfq-bom-v0.1/README.md), [Detektionsqualifikation](../../hardware/detection-qualification-v0.1/README.md). Projektbeiträge gemäß [Lizenzumfang](../../../../LICENSE_SCOPE.md). Keine Bestellungen oder Hardwaremessungen.
