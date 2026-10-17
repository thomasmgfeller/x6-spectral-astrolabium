# Ausführung und technische Speicherkorrektur

Der erste vorab fixierte Lauf berechnete die sequenziellen Studien, die
Kettenkontrollen und den geometrischen Integrationslauf. Beim anschließenden
Schreiben von summary.json brach er ab: Der Standard-JSON-Encoder konnte
einen numpy.int64-Wert für die Anzahl von Testverwerfungen nicht speichern.

Erhalten sind die ursprüngliche Quellenfixierung, sämtliche gezogenen
Zählblöcke und die ursprüngliche run.py-Fassung unter
`results-incomplete-serialization/`. Dieser erste Lauf wird nicht als
abgeschlossene Veröffentlichung seiner Ergebnisse gewertet.

Die Reparatur konvertiert ausschließlich den Verwerfungszähler mit `int(...)`
in einen Python-Integer. Stichprobengesetze, Seeds, Hypothesen, Fehlerbudgets,
Schranken, Stoppregeln, Referenzhöhenberechnung und Teststatistiken blieben
unverändert. Anschließend erfolgte ein vollständiger Replay mit exakt
denselben Seeds; es wurde kein günstigerer Lauf ausgewählt.

[execution_repair.json](results/execution_repair.json) bestätigt:

- Zwischen den beiden Quellenfixierungen änderte sich nur run.py.
- Die archivierte ursprüngliche run.py stimmt mit ihrem ursprünglichen Hash überein.
- Alle archivierten Zählblöcke sämtlicher Kontroll- und Zielströme sind exakt identisch.

Der erfolgreiche Lauf enthält eine neue Quellenfixierung für die reparierte
Ausgabefassung. Die [interne Gegenprüfung](results/verification.json) prüfte
die Quellenbindung, ausgewählte vollständige Controller-Replays, sämtliche
Stopppunktzählungen, 2.048 Rang-p-Werte sowie den geometrischen Integrationslauf.
Dies ist keine externe Replikation.
