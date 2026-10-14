# Prüfung — X6 Experiment Fabric 0.1

14. Oktober 2026. Aussagebereich: Software und synthetische Kontrollfälle.

| Prüfung | Ergebnis |
|---|---|
| Node.js-Kern und Fehlerszenarien | 15 Tests bestanden; lokaler Lauf mit Node.js v24.19.0 |
| Zwei parallele Worker | Vier abgeschlossene Pakete, acht synthetische Beobachtungen |
| Export und Replay | PASS für [control-run.json](examples/control-run.json) |
| Unabhängige Python-Numerik | 156 Likelihood-Einträge sowie Planoptima, Informationswerte und Posterioren bestanden; Toleranz 10⁻¹⁰ |
| Browser-Worker | Eigenes verpflichtendes GitHub-CI-Gate mit Playwright 1.62.1; konkreter Laufstatus im GitHub-Actions-Lauf des Commits |
| Lokale Browserinstallation | Chromium-Download lieferte kein gültiges Archiv; deshalb kein lokaler Browser-PASS ausgewiesen |
| Netzwerk, reale Geräte, Kalibrierung, physikalische Modelltrennung | Nicht Gegenstand dieser Ausgabe |

Die 15 Kernprüfungen umfassen Informationsredundanz und Synergie, gemeinsame Störgrössen, Reihenfolgeunabhängigkeit, widersprüchliche Beobachtungen, exklusive Probenbelegung, Fähigkeits-/Budgetgrenzen, ungültige Wahrscheinlichkeiten, gleichzeitige Duplikatzustellung, unvollständige Pakete, abgelaufene Versuche und identische Retry-Replikate, falsche Herkunft/Qualität/Hashes, veränderte Schwellen, verweigerte physische Ausführung sowie Replay mit Manipulationskontrolle.

Die Browserprüfung verlangt acht Worker-Instanzen, vier Ereignisse, erfolgreichen Replay des Browserexports durch den Node-Referenzpfad, Desktop-/Mobilbreite ohne Seitenüberlauf, funktionierendes Zurücksetzen, keine Seitenfehler und keine externen Requests. Die gemeinsamen Koordinator-/Worker-Kerne sind kein Nachweis zweier unabhängiger Laborstandorte.

Datei- und Ereignishashes müssen exakt stimmen. Neu berechnete Gleitkommawerte im browserübergreifenden Replay dürfen um höchstens 10⁻¹²·(1+max(|a|,|b|)) abweichen; ganzzahlige Identifikatoren, Seeds und Zähler bleiben exakt. Bei Plan-Nutzwerten innerhalb 10⁻¹² entscheidet eine feste lexikografische Zuweisungsreihenfolge nach Kosten. Die unabhängige Python-Referenz verwendet eine absolute Toleranz von 10⁻¹⁰.

Der mechanische Kontrolllauf liefert einen relativen Anteil von 0,995949 für seinen erzeugenden Kandidaten. Das ist weder eine empirische Trefferquote noch ein Nachweis einer allgemeinen Einsparung. Ein unverändertes Zeit-/Messbudget und separate Bestätigungsdaten sind Voraussetzung eines künftigen Nutzenbenchmarks.
