# CSPP v0.18: Quantitative Restmajoranten

v0.18 ergänzt die Konvergenzherleitung aus v0.17 um explizite KG-Quellkonstanten,
eine scharfe globale Schichtgewichtsschranke und vollständig transportierte
bedingte Erwartungswertschranken für die vier vorhandenen Omega5-Archive.
Die Summation aller kausalen Pfade berücksichtigt die Abhängigkeit zwischen
Forcierung und Geometrie.

Die bedingten Pfadfaktoren liegen zwischen etwa **2,73 und 3,79**. Die besten
ausgewerteten Obergrenzen für den gesamten geometrischen Rest liegen dennoch
um **10^54**: Pauschale Quell- und Archivschranken dominieren diese Abschätzung.
Eine große Obergrenze beweist keinen großen tatsächlichen Fehler und verwirft
die Operatorfamilie nicht. Die abklingende ferne History-Majorante ist von dem
weiterhin fehlenden endlichen Historybereich zu unterscheiden.

**METHOD_HOLD und G1 HOLD bleiben bestehen. Das individuelle Fehlerziel ist
NOT_CERTIFIED.** Eine bedingte Erwartungswertschranke ist kein Fehlerzertifikat
für eine konkrete Realisierung. Keine neue Zufallswolke, kein neuer Seed und
keine Änderung von Quelle, Fehlerziel oder statistischer Freigaberegel.

- [Bericht mit vollständiger Herleitung (PDF)](Quantitative_Restmajoranten_v0_18.pdf)
- [Vollständiges unverändertes Rechenpaket (ZIP)](CSPP_Quantitative_Restmajoranten_v0_18.zip)
- [Lesbare Herleitung und Aussagegrenzen](quantitative_tail_v0_18/PROOF.md)
- [Vorab erklärtes analytisches Gitter](quantitative_tail_v0_18/PROTOCOL.json)
- [Ergebnisse bei 192 Bit](quantitative_tail_v0_18/results/BOUNDS_192.json)
- [Algebraische Kontrollen und Präzisionsvergleiche](quantitative_tail_v0_18/results/CHECKS.json)
- [Bedingte Restmajoranten als Grafik (PNG)](majorants.png)

## Reproduktion

```sh
python3 -m pip install python-flint==0.8.0
python3 -B research/cspp/quantitative_tail_v0_18/publication_check.py --replay
```

Python 3.12. Der Publikationsprüfer kontrolliert PDF und ZIP, alle 22 originalen
Paketdateien sowie 21 SHA-256-Einträge. Anschließend berechnet der enthaltene
Reproduktionslauf die 128- und 192-Bit-Ergebnisse in einem temporären Verzeichnis
neu und vergleicht alle drei wissenschaftlichen JSON-Dateien exakt.
857 Präzisionsvergleiche und drei Negativkontrollen bestehen.
Der [GitHub-Workflow](../../../.github/workflows/cspp-quantitative-tail.yml)
führt diese Prüfung auf Pull Requests und main aus. Die algebraischen und
numerischen Kontrollen ersetzen keine unabhängige wissenschaftliche Begutachtung
der Kontur- und Mecke-Argumente.

PDF, ZIP und extrahierte Originaldateien bleiben bytegleich zur ausgelieferten
Fassung. `NOT_PUBLISHED` im ursprünglichen `PACKAGE.json` beschreibt den damaligen
Stand vor dieser Publikation; die Publikationsmetadaten stehen außerhalb des
unveränderten Pakets in `PUBLICATION.json`.

**Grafik-Ergänzung:** Die optionale PNG-Kopie im Originalpaket ist leer.
Die enthaltene SVG-Grafik und die Grafik im PDF sind vollständig. Die hier
verlinkte PNG-Datei wurde mit der unveränderten Zeichenfunktion aus
`build_report.py` und den unveränderten 192-Bit-Ergebnissen neu erzeugt.
Ihr Hash und die Korrektur sind in `PUBLICATION.json` dokumentiert.

Der nächste Forschungsansatz ist die gezielte Einschließung tatsächlicher
Quellableitungen und geometrischer Intervallüberlappungen. Eine astronomische
Gebietserweiterung wird aus dieser groben Majorante nicht abgeleitet.

Basis: [v0.17 / PR #149](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/149),
Merge `808cd43ddc840a6fd87c9095e7698b58f85846a7`.
