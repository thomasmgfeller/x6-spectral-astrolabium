# Wissenschaftlicher Status

Stand 12.10.2026. Diese Veröffentlichung ist ein prüfbarer Entwicklungsstand, keine unabhängige Begutachtung oder Zertifizierung.

## Aussage und benötigter Nachweis

| Aussage | Zulässiger Status heute | Für eine stärkere Aussage erforderlich |
|---|---|---|
| Sagnac-Quelle kann Polarisationsverschränkung erzeugen | Durch Fachliteratur für dortige Aufbauten gestützt | Für unseren Aufbau: dokumentierte Quelle, Kalibrierung und geeigneter Zustandsnachweis |
| Unsere Quelle erzeugt einen bestimmten Bell-Zustand | Ziel, nicht beobachtet | Korrelationen/ggf. Tomografie mit Unsicherheit; Phase, Balance und Ununterscheidbarkeit charakterisieren |
| Digitalteil zählt definierte synthetische Ereignisse korrekt | Durch benannte Software-/RTL-Tests prüfbar | Frontend-, Board- und Ende-zu-Ende-Messungen für physische Eingänge |
| CHSH-Auswertung funktioniert für Modellbeispiele | Synthetische Softwareprüfung | Vorab festgelegtes Versuchsdesign, Rohdaten, Kalibrierung, Messmodell und begründete Statistik |
| Lokales verborgenes-Variablen-Modell ausgeschlossen | Für diesen Aufbau nicht nachgewiesen | Geeignetes Bell-Experiment einschließlich relevanter Nachweis-, Lokalitäts- und Auswahlbedingungen |
| Jig hält optische Toleranzen ein | Ungeprüft | Gemessene Drift, Hysterese, Wiederholung und Strahlversatz beim Lösen/Kleben |
| Edge-Quantencomputer, QPU oder universelle Gates | Nicht nachgewiesen | Spezifizierte Operationen, physische Realisierung und geeignete Benchmarks |
| QKD-Sicherheit, topologischer Schutz, Angriffserkennung | Nicht nachgewiesen | Eigene Sicherheits-/Physikmodelle und separate Evidenz |

## CHSH: Zwei verschiedene Auswertungen

Die v0.7-Referenz verwendet vier feste lokale Einstellpaare und vorab definierte Zeitfenster. Das konditionierte Ergebnis verwendet nur Fenster mit genau einem belegten Ausgang pro Arm. Leere Fenster, Einzelarm-Ereignisse und gleichzeitig belegte Plus-/Minus-Ausgänge sind darin ausgeschlossen. Mehrfachtreffer desselben Kanals bleiben als Kanalbelegung erhalten. Diese Selektion verlangt ein begründetes Nachweismodell bzw. eine Fair-Sampling-Annahme; sie schließt die Detection-Loophole nicht.

Die zusätzliche All-Trials-Auswertung ordnet jedem Fenster lokal einen Wert ±1 zu: ausschließlich Minus belegt bedeutet −1, sonst +1. Sie zeigt ausdrücklich den Einfluss leerer und mehrdeutiger Fenster. Ein anderes Resultat dieses Zweigs ist kein Softwarewiderspruch. Auch dieser Zweig allein schließt keine Lokalitäts-, Zeit- oder Einstellwahlprobleme.

Für beide Zweige gilt S = E00 + E01 + E10 − E11. Die Prüfstatistik T = −S ist vorab auf die beabsichtigte Singlet-Konvention ausgerichtet. Eine nachträgliche Wahl des günstigeren Vorzeichens ist durch die veröffentlichte einseitige Schranke nicht abgedeckt. Die Hoeffding-Schranke im Referenzmodell setzt unabhängige, identisch verteilte ±1-Produkte innerhalb jedes Einstellblocks und gültige Ereigniszuordnung voraus. Sie ist kein universeller Nachweis bei Gedächtniseffekten, Drift, beliebigem optionalem Stoppen oder nachträglich gewählten Parametern.

Die vier blockweise gemessenen Einstellungen sind keine schnellen zufälligen Einstellwahlen pro Trial. Die Beispielwerte (u.a. konditioniertes S ≈ −2,825) stammen aus generierten Daten und dürfen nicht als gemessene Bell-Verletzung zitiert werden. Details, Zählmasken und Fehlerbehandlung: [METROLOGY.md](reference/sagnac_v0_7/docs/METROLOGY.md).

## Einheiten, Simulation und Hardware

- 64-Bit-Zeitstempel in ps beschreiben das Datenformat. Daraus folgt weder eine Auflösung noch eine Genauigkeit von 1 ps. Angaben zu 32 Bit in älteren Dokumenten betreffen teilweise Registerschnittstellen und andere Architekturen.
- GHDL-Simulation und generische Synthese belegen keine FPGA-Taktfrequenz, Quartus-Timing-Closure, CDC-Sicherheit oder elektrischen Pegel.
- v0.7 sendet einen Snapshot pro Reset. Ein UART-RX-Steuerpfad, automatische Messreihensteuerung und optische Aktoren sind nicht enthalten.
- `origin=hardware` ist eine Herkunftsdeklaration, kein kryptografischer Echtheitsnachweis und kein physikalisches Gütesiegel. CRC prüft Übertragungsfehler.
- Frühere H/A/B-Herald-Kennzahlen sind kein CHSH-Ergebnis. Die geplante kontinuierlich gepumpte Zwei-Photonen-Quelle liefert nicht automatisch einen unabhängigen dritten Herald-Kanal.
- v0.8 bleibt optional. Lokale Einheitsrotationen erhalten die Singulärwerte der Korrelationsmatrix eines festen Zustands; zeitliche Mischung verschiedener Zustände/Rotationen muss dies nicht tun. Solche Invarianten identifizieren weder eindeutig einen Angriff noch eine Rauschursache.

## Kosten und Offenheit

90–180 CHF im Jig-Handbuch ist eine eigene Materialplanung für den Jig, ohne Optik, Detektoren, Zeitmessung, Werkzeuge und Arbeitszeit. Der v0.7-Hardwareplan enthält eine damalige Händlerbeobachtung von 6.808,75 USD pro Referenzdetektor (vier: 27.235 USD), kein heutiges Angebot und keine Gesamtkalkulation. Andere Detektoren oder Eigenentwicklungen sind nicht allein anhand des Stückpreises gleichwertig. Für einen belastbaren Systemvergleich fehlen eine eingefrorene Stückliste und gemessene Leistungsdaten. Preis- und Verfügbarkeitsangaben vor Beschaffung erneut prüfen.

Eine Veröffentlichung macht einen Entwurf zugänglich; sie ersetzt weder unabhängige Reproduktion noch Peer Review. KI-Unterstützung und Konzeptbilder sind Teil der Entstehung, keine experimentelle Evidenz.
