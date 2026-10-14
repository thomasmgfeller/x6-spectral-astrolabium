# Primärquellen und geprüfte Grenzen

Abruf: 14.10.2026. Produktangaben sind Herstellerangaben, keine eigenen Messwerte.
Keine Preise oder Liefertermine werden zugesagt. Hersteller-PDFs werden nicht
als eigene Dokumente weiterverteilt. Wo der Originalserver nur eine leere Seite
lieferte, wurde eine Kopie des **Herstellerhandbuchs** gelesen; kein Blog ersetzt
die Protokollspezifikation. Das konkrete gelieferte Gerät bleibt abzugleichen.

| Quelle | Verwendete Information |
|---|---|
| [Kim, Fiorentino, Wong 2006](https://doi.org/10.1103/PhysRevA.73.012316) | Bestehende Sagnac-Grundlage; keine neue Quelle eigener Messwerte. |
| [TOPTICA TopMode 405 HP](https://www.toptica.com/products/single-mode-diode-laser/topmode?variant=TopMode+405+HP) | CW-Pumpe, Wellenlänge, Bandbreite, Leistung; Variante eindeutig benennen. |
| [Raicol ppKTP-Auswahl](https://raicol-quantum.com/2022/08/03/ppktp-selection-guide/) | Typ-II 405→810 als Auswahlrichtung; keine konkrete Polungsperiode/Solltemperatur für unseren Kristall. |
| [Newlight 405-nm-SPDC-Komponenten, Hersteller-PDF](https://www.newlightphotonics.com/QE-parts-list-2023-pump405nm.pdf) | WPA03-H/Q-405/810, Abmessungen, Beispielspiegel und Filter. Katalogstand 2023, heutige Lieferdetails offen. |
| [Newlight duale Wellenplatten](https://www.newlightphotonics.com/wp-dual.html) | WPD03-H810-H405; Unterschied gegenüber Halb-/Vollwellenkombination. |
| [Newlight duale PBS](https://www.newlightphotonics.com/SPDC-Components/Broadband-Polarizing-Beamsplitters-SPDC) | PBS0025-405/810 und Wellenlängenpaar. |
| [Thorlabs montierte PBS](https://punchout.thorlabs.com/newgrouppage9.cfm?objectgroup_id=4137) | CCM1-PBS252/M, 620–1000 nm, SM1/30-mm-Cage. |
| [Thorlabs DMLP650](https://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=3313&pn=DMLP638) | Trennung 405/810 liegt in den angegebenen Reflexions-/Transmissionsbereichen; Phasenwirkung separat messen. |
| [Thorlabs Longpass](https://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=6082&pn=FELH0900) | FELH0750; Abgrenzung zu FESH0750 mit entgegengesetzter Funktion. |
| [Thorlabs NIR-Bandpass](https://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=16235&pn=FB780-10) | FBH810-10; Einfallswinkel und tatsächliche Filterkurve prüfen. |
| [Thorlabs Spiegel](https://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=139) | BB1-E02 garantiert nicht beide 405/810-nm-Wellenlängen; deshalb keine Freigabe als Schleifenspiegel. |
| [Thorlabs Elliptec-Protokoll Issue 9, Mai 2025](https://www.thorlabs.com/Software/Elliptec/Communications_Protocol/ELLx%20modules%20protocol%20manual_Issue9.pdf), [Herstellerhandbuch-Kopie](https://device.report/m/0d9ac10047d68a2cad671957287621af3b9c807a5c4d0e4fc66824f93f416594) | Seiten 4–11, 30, 38–39: Bus, Geräteinformation, Status, Absolute Move, Stop, Position. Code ist eine eigene begrenzte Umsetzung. |
| [Thorlabs Rotationshalter-Übersicht](https://www.thorlabs.com/NewGroupPage9_PF.cfm?ObjectGroup_ID=246) | ELL14 mit SM1-Apertur gegenüber ELL18 mit Plattform; keine mechanische Austauschbarkeit unterstellt. |
| [Thorlabs PM100D](https://www.thorlabs.de/NewGroupPage9.cfm?ObjectGroup_ID=3341&pn=PM100D), [Herstellerhandbuch Rev. I, 13.04.2023, Kopie](https://manuals.plus/m/3c729437217688e9b50f1a162a8b21ad3591b66d929390c1077f91d887ac6774) | Legacy PM100D/S120C, SCPI-Kapitel, Einheit/Wellenlänge/Sensor-ID. Kein Treibertest an realem Gerät. |
| [PyVISA, Ressourcen](https://pyvisa.readthedocs.io/en/latest/introduction/resources.html) | Explizite Ressource, I/O-Zeitlimit und Terminatoren; Backend separat vom Labor bereitzustellen. |
| [Thorlabs LCVR-/Controller-Unterlagen](https://www.thorlabs.de/NewGroupPage9_PF.cfm?Category_ID=21&Guide=10&ObjectGroup_ID=4182) | LCVR benötigt geeigneten AC-Antrieb; C1-DC-DAC ist kein direkter Ersatz. |

Das Sagnac-Ausgangsprofil mit Detektoren und Time-Tagger ist bereits in
`experiments/photonic-two-qubit/reference/sagnac_v0_7/docs/HARDWARE.md`
dokumentiert. Hier wird daraus kein neuer elektrischer oder optischer Test abgeleitet.
