# Validierungsstand

Stand 14. Oktober 2026. Ausschliesslich synthetische/logische Softwarekontrollen.

- 17 Python-Tests bestanden, einschliesslich Vergleich mit dem vorhandenen
  JS-Planer für sämtliche neun Zweierbatches und 36 Ausgangsbelegungen.
- Drei veröffentlichte Kontrollen sind deterministisch reproduzierbar; jede
  verwendet einen anderen Generator als Simulationswahrheit. Diese Information
  geht nicht als Planerparameter ein.
- Die exakte Testgrösse wurde über alle 25 möglichen Binomialzählungen pro
  registrierter Nullwahrscheinlichkeit berechnet und gegen die festgelegte
  Schranke geprüft. Die gemeinsame Schranke folgt aus der Bonferroni-Ungleichung.
- Konstruiertes Gegenbeispiel: Kandidat mit mehr als 99 % vorherigem Gewicht
  wird im Challenge-Gate verworfen. Andere Kontrolle: alle Klassen fallen.
- Neutrale Namen, Registerreihenfolge und mehrfach dargestellte identische
  Kandidaten ändern die Entscheidung nicht. Fremde Ziel- und Bonusfelder werden
  vom geschlossenen Vertrag abgewiesen.
- Keine geometrische Struktur, physikalische Theorie, reale Intervention oder
  allgemeine statistische Entdeckungsleistung wurde damit nachgewiesen.
- Endlicher Suchraum; deklarierte gleiche Klassenprior; feste Punktmodelle;
  unabhängige Replikate; kein Messrauschen im logischen Kontrollfall.
- In-Memory-Gate, keine manipulationssichere Präregistrierung und kein dauerhaftes
  kampagnenübergreifendes Fehlerbudget. Hashes binden Inhalte, nicht Wahrheit.

Der eigene GitHub-Workflow prüft Quelle, Replay, Tests, bestehende Fabric-Tests,
Fingerprint-Tests und Schutz der bisherigen Forschungsbasis. Sein tatsächlicher
Status ist im zugehörigen GitHub-Actions-Lauf nachzusehen; dieses Dokument nimmt
den Erfolg eines noch nicht ausgeführten Remote-Laufs nicht vorweg.
