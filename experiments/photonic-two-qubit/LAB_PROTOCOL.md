# Laborprotokoll und Freigabestufen

**Vorlage, noch nicht ausgeführt.** Jede Stufe erhält Datum, verantwortliche Person, Geräte-/Firmwarestände, Rohdaten, Auswerteskript und einen begründeten Status PASS/FAIL/NOT_ASSESSED. Anforderungen vor der jeweiligen Messung festlegen. Keine rückwirkende Optimierung von Fenstern, Vorzeichen, Ausschlüssen oder Stoppregeln anhand des gewünschten Ergebnisses.

1. **Design einfrieren.** Strahlplan, Stückliste, Kanalbelegung, tatsächliche Wellenlängen und Pegel festhalten. Gefährdungsbeurteilung für den gewählten 405-/810-nm-Laseraufbau, Abschirmung und Justage durch fachkundige Personen; unsichtbare Strahlanteile und Reflexe berücksichtigen. UV-Klebeprozess und ggf. SPAD-Hochspannung separat freigeben. Ohne gewählte Komponenten lässt sich keine passende Schutzbrille oder elektrische Beschaltung festlegen.
2. **Jig am Dummy prüfen.** Passungen, Vorspannung, Rückzug und kontrollierte Ablösung testen. Wiederholung, Hysterese und Drift messen. Gemessenen Übergabefehler einschließlich Messunsicherheit mit dem vorher abgeleiteten optischen Toleranzbudget vergleichen. CAD-Kollisionsfreiheit ist kein Ersatz für diesen Test.
3. **Detektoren einzeln charakterisieren.** Dunkelzählrate, Totzeit, Nachpulse, Linearitätsbereich und Timing aufnehmen. Bauteildatenblatt ist eine Spezifikation, kein Kalibrierschein des konkreten Exemplars. Keine behauptete photonische Effizienz ohne geeignete Leistungsreferenz und Unsicherheitsbudget.
4. **Zeitbasis und Transport prüfen.** Gemeinsame Referenz, Kanalverzögerungen, Skalierung und Drift bestimmen. Pulsgenerator-Test bis Host durchführen; verlorene Ereignisse, FIFO-Überläufe, Reset, gleichzeitige Treffer und Zeitstempelreihenfolge testen. Kalibrierkennung muss mit dem Lauf übereinstimmen. Ein Abschluss-Watermark und Fehlerflags sind nachzuweisen; fehlender Abschluss ist kein gültiger Nullmesslauf.
5. **Quelle optisch charakterisieren.** Einzel- und Koinzidenzraten, Spektral-/Raumüberlappung und Polarisation erfassen. Pumpabhängigkeit, Mehrpaaranteile, Hintergrund und Langzeitstabilität untersuchen. Rohzählungen einschließlich leerer/mehrdeutiger Fenster aufbewahren. Hintergrundsubtraktionen, falls zusätzlich gezeigt, getrennt von unveränderten Primärergebnissen ausweisen.
6. **Zwei-Qubit-Korrelationen messen.** Zustands- und Messmodell, Analyseachsen, Einstellreihenfolge, Messdauer/Trialzahl, Fensterstart/-breite, Kanalversatzkorrekturen, geplante Statistik und Fehlerbudget vorab protokollieren. Konditionierte und All-Trials-Auswertung gemeinsam berichten. Stationarität und Abhängigkeiten prüfen; bei verletzten Voraussetzungen die aktuelle iid-Schranke nicht als belastbare Signifikanz ausgeben. Blockmessungen nicht als loophole-freies Bell-Experiment bezeichnen.
7. **Erst danach stärkere Aussagen.** Physische Verschränkung nur mit einem zum Mess-/Nachweismodell passenden Witness oder einer entsprechend validierten Zustandsrekonstruktion behaupten. Die optionale v0.8-Tomografie benötigt eine konsistent versionierte Erweiterung von RTL, Transport und Host; sie ist keine vorhandene Funktion.

## Mindestangaben pro Messserie

| Bereich | Aufzubewahren |
|---|---|
| Identität | Lauf-ID, UTC-Zeiten, Git-Commit, Software-/Firmwareversion, Geräte/Seriennummern, Bedienperson |
| Optik | Realer Strahlplan, Kristall-/Filterdaten, Temperatur, Pumpzustand, Analysatorkalibrierung |
| Timing | Kalibrierrohdaten, Referenz, Einheit/Skala, Kanalversätze, Jitter-/Driftbudget, Kalibrier-ID |
| Ereignisse | Möglichst rohe Time-Tags; alle Zähler, Fehlerflags, Fensterdefinition, Überlauf-/Verlustprotokoll |
| Statistik | Vorab-Protokoll, Mess-/Selektionsmodell, Stichprobenumfang, Konfidenz-/Fehlerniveau, Mehrfachtests und Stoppregel |
| Reproduktion | Unveränderte Rohdateien mit Hashes, Skripte, Umgebung, vollständige Ergebnisse einschließlich Fehlläufen |

Snapshot-Dateien allein erlauben nicht jede spätere Timing- oder Selektionsprüfung. Für die erste physische Qualifizierung deshalb auch Roh-Time-Tags sichern, soweit das Messgerät dies ermöglicht. Änderungen nach Sichtung der Daten als explorativ kennzeichnen und mit neuer unabhängiger Messserie prüfen.
