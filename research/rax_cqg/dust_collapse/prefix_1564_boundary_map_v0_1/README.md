# CST-DUST · Ein Ereignis am Präfix 1564 ausintegrieren

20. November 2026 · v0.1. Der Bericht und die Herleitung behandeln die 16 markierten Fortsetzungen mit unveränderter Randpräparation. Enthalten sind die vollständigen skalaren Korrekturmatrizen, Deltanormalen, geänderten Intervallkoeffizienten, Gravitationsphasen, Normierungsdaten, ein exaktes Nichtnull-Zeugnis des Staubfaktors und die rationalen Daten für den äusseren Rand. Der physikalische Gewichtungsentscheid bleibt offen.

## Reproduktion

Das Verzeichnis entpacken. Mit Python 3, NumPy, SymPy und mpmath im entpackten Verzeichnis ausführen. Verwendete Versionen stehen in requirements.txt. Der Prüfer arbeitet lokal, der ursprüngliche Datensatz ist im inneren ZIP enthalten. Ein C-Compiler wird für diese Untersuchung nicht benötigt.

~~~sh
python3 -B boundary.py replay.json
python3 compare.py result.json replay.json
~~~

Der zweite Befehl vergleicht alle rationalen Ergebnisse exakt und die numerischen Gleichgitter-Kontrollen mit ihren eigenen Toleranzen.

boundary.py baut jede markierte Ordnung aus ihren Relationen neu auf. Der Prüfer vergleicht die sukzessive Integration mit der direkten Randreduktion und alle äusseren Präzisionsmatrizen mit der kanonisch umnummerierten ursprünglichen Implementation. clock_check.py integriert die markierte neue Uhr zuerst. Zum Vergleich wertet es den Archivcode auf der unmarkierten Endordnung mit dessen eigenständig bestimmter Eliminationsreihenfolge aus. Die zwei kleinen Gitter prüfen die Zusammensetzung bei gleicher Diskretisierung an beiden Lappen und Dichten. Ihre Differenz zwischen Rechenwegen ist keine Fehlerschranke für das kontinuierliche Integral. Der Nichtnull-Beweis der beiden singulären Staubbeiträge ist analytisch.

Die Schlüssel von result.json folgen den Bezeichnungen der Herleitung. Die oberen Dreiecke symmetrischer Matrizen verwenden die alten Rohfeldindizes 0 bis 12. Nicht gelistete Einträge sind null. delta_interval_weights enthält auch die Einträge der neuen Marke 13. Bei der nackten Elternordnung sind die Gewichte zu dieser Marke per Definition null.

## Quellen

[Stand von main und ursprünglicher Selektionsversuch](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/1638acd19961c840fb0b3d35135a947e4dba0f4e/research/rax_cqg/dust_collapse/prefix_1564_selection_v0_1) · [Herleitung der geerbten skalaren Randpaarung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/1638acd19961c840fb0b3d35135a947e4dba0f4e/research/rax_cqg/dust_collapse/history_measure_state_space_v0_1/Randsektor.md).

Methodischer Kontext zur Wahl einer Abbildung zwischen zwei Diskretisierungen bei B. Dittrich, *From the discrete to the continuous – towards a cylindrically consistent dynamics* ([arXiv:1205.6127](https://arxiv.org/abs/1205.6127)). Die hier berechneten Abbildungen und Ausschlüsse folgen aus dem archivierten CST-DUST-Vertrag.

Das innere Original-ZIP ist unverändert und enthält seine Herkunfts- und Lizenzdateien. SHA-256 ist 4a2b985578e9bf41662af0dede7c2054c8406de4f49d077891f505b0fffd917e.
