# Amendment01: Präzisionsabhängige Berichtszahlen vergleichen

Nach der vollständig abgeschlossenen128-/192-Bit-Auswertung wurde eine
unzutreffende Gleichheitsforderung im Veröffentlichungsprüfer festgestellt.
Das ursprüngliche `verify_publication.py` verlangt, dass die vollständigen
beiden DECISION-JSON-Dokumente gleich sind. Darin steht aber auch
`population_RMS_lower`: ein mit der jeweiligen Präzision nach unten
gerundeter irrationaler Wert. Seine letzten Stellen sollen sich zwischen
128 und192Bit unterscheiden dürfen.

Beispiel für64 Überschreitungen: die beiden Zahlen unterscheiden sich um
etwa1,65e-39. Die rationalen Clopper-Pearson-Endpunkte, alle Zählungen,
p-Werte, statistischen Entscheidungen und wissenschaftlichen Statuswerte
sind exakt gleich. Das ist kein statistischer Grenzfall.

**Alle vorregistrierten Dateien bleiben bytegleich**, einschließlich des
fehlerhaften ursprünglichen Veröffentlichungsprüfers und FREEZE.json.
Der ergänzte `publication_checks.py` ist eine ausdrücklich nach den Daten
erstellte Kopie dieses Prüfers mit einer eng begrenzten Korrektur:

1. Exakte Zählungen, rationale Endpunkte, p-Werte und Entscheidungen werden
   weiterhin vollständig auf Gleichheit geprüft.
2. Jeder veröffentlichte numerische RMS-Unterwert wird zusätzlich bei256Bit
   gegen die Formel `(1/5)*sqrt(p_lower)` kontrolliert. Der untere Rand der
   gespeicherten Dezimal-Einschließung muss eine gültige untere Schranke sein.
3. Die wissenschaftliche Schwelle, Mehrfachtestkorrektur, Stichprobengröße,
   Seedströme, Fehlerbudgets und Abbruchregeln bleiben unverändert.

Die Originalausgabe mit ihrem erwarteten Verifier-Fehler wird archiviert.
Die eingefrorene Produktion wird nicht auf Grundlage der beobachteten
Ergebnisse umgeschrieben oder mit neuen Wolken ersetzt. Die Korrektur
ändert keinen einzigen Prüfdatenwert und keine G1-/Dirac-Entscheidung.
Der CI prüft weiterhin jede ursprünglich eingefrorene Quelldatei direkt
gegen den öffentlichen Vorregistrierungscommit und benutzt anschließend
den ergänzten Veröffentlichungsprüfer.

Das ist ein dokumentiertes technisches Erratum am Berichtsvergleich,
keine neue statistische Auswertungsmethode. Der ursprüngliche Prüfer
bleibt zur Reproduktion des Fehlers vorhanden; für die Veröffentlichung
und deren Replay gilt `publication_checks.py`.
