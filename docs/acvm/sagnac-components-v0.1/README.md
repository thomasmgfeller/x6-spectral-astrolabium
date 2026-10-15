# Kristall, Sagnac-Schleife und Kristallofen

**O02 KSO 01 · Revision 0.1 · 15. Oktober 2026 · Anforderungs- und Prüfspezifikation**

[Die vollständige technische Spezifikation herunterladen](Sagnac_Kristall_Schleife_Ofen_Spezifikation_v0_1.docx)
(Word, zehn Seiten). Die Datei ist bytegleich mit der vom Projektinhaber zur
Veröffentlichung freigegebenen Fassung. [Prüfsummen und Veröffentlichungsumfang](manifest.json).

Die Spezifikation konkretisiert die offenen Quellenkomponenten des
[ACVM-Optikprofils 0.2](../optical-v0.2/README.md). Sie enthält die optische
Geometrie, Anforderungen an Kristall und Spiegel, die temperaturgeregelte
Kristallaufnahme, ein thermisches Modell, Kalibrierabläufe und zwölf
Abnahmeprüfungen.

## Auslegung und Status

Die Zahlen sind gewählte Projektanforderungen, keine gemessenen
Geräteeigenschaften oder bestätigten Lieferantenzusagen.

| Gegenstand | Auslegung |
| --- | --- |
| Kristall K1 | Kollinearer Typ-II-ppKTP, 10,0 ±0,1 mm Länge; beide Ausbreitungsrichtungen |
| Wellenlängen | Nominell 405 → 810 + 810 nm; endgültige Auslegung anhand der gemessenen Pumpenwellenlänge |
| Freie Nutzfläche | Mindestens 2 × 1 mm, getrennt von den Aussenmassen zu bestätigen |
| Phasenanpassung | Anfrageziel 40 °C; Angebotsfenster 35–50 °C; Polungsperiode und Temperatur vom Hersteller gemeinsam auslegen |
| Schleife L1 | Ein gemeinsamer gegenläufig durchlaufener Dreiecksweg, Seiten 120 / 120 / 169,71 mm |
| Spiegel M1/M2 | AOI 22,5° zur Normalen; Ziel R ≥99,5 % für s und p über 403–407 sowie 800–820 nm |
| Ofen O1 | Zu qualifizierender Bereich 30–60 °C; lokaler PI/PID und unabhängiger Übertemperaturschutz |
| Temperaturstabilität | Startziel ±0,10 K; engeres funktionales Budget aus gemessener Tuningkurve und Phasendrift |
| KSO01–KSO12 | **NOT_RUN** |
| Bestell- und Fertigungsfreigabe | **Offen** |

**Geometrische Präzisierung:** Für dieses rechtwinklig-gleichschenklige
Dreieck beträgt der Einfallswinkel an beiden Aussenspiegeln 22,5° zur
Flächennormalen. Die frühere pauschale 45°-Angabe aus O02-M1 wird für diese
Geometrie ersetzt. Der Strahlentwurf ist noch keine kollisionsgeprüfte
CAD-Baugruppe.

## Wissenschaftlicher Geltungsbereich

Die Veröffentlichung ist eine Grundlage für Lieferantenanfragen und
Detailkonstruktion. Sie dokumentiert keine neuen physikalischen Messungen,
keine bestandene Hardwareabnahme und keinen funktionierenden Quantenprozessor.
Geometrische und einfache Auslegungsrechnungen wurden geprüft; die
chargenspezifische Kristallauslegung, Beschichtungsdaten und thermischen
Eigenschaften des realen Verbunds stehen aus.

Herstellerangaben, Literaturbefunde, gewählte Anforderungen und eigene
Rechenbeispiele werden im Dokument unterschieden. Die vorhandenen
Softwareprüfungen V01–V08 erhalten durch diese Dokumentveröffentlichung
keinen zusätzlichen optischen Nachweis. V09/V10 und schnelles photonisches
Feed-forward behalten ihren bisherigen offenen Nachweisstatus.

Das bestehende ACVM-Quellpaket und seine historischen Prüfdaten bleiben
unverändert. Es wird kein Ofenadapter implementiert und kein Gerät aktiviert.

## Quellen und Rechte

Primärpublikationen und Herstellerunterlagen sind in Abschnitt 9 des
Dokuments referenziert. Fremde Publikationen und Datenblätter werden verlinkt,
nicht mitverteilt.

Originale Projektdokumentation folgt der
[Apache-2.0-Lizenz](../../../LICENSE) und dem
[Lizenzumfang des Repositorys](../../../LICENSE_SCOPE.md).
