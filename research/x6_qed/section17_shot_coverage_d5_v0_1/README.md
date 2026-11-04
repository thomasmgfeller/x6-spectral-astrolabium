# X6-QED · Erreichbare Fast-Path-Abdeckung auf zufälligen d=5-Shots

**4. November 2026 · DEVELOPMENT · Schritt 2 · NO_GO_5PCT**

Von 44.805 nichtleeren Shots erreichten 1.681 den Margenvergleich nach §17. Das entspricht 3,752 % mit einem zweiseitigen exakten 99-%-Konfidenzintervall von 3,524 % bis 3,989 %. Die vor der Stichprobe definierte Mindestabdeckung von 5 % liegt über der oberen Intervallgrenze. Für dieses Ziel endet der Entwicklungstest der untersuchten Variante mit NO_GO_5PCT. CAL und C0-VALIDATION stehen auf HOLD.

## Stichprobe und Modell

Stim 1.16.0 simulierte 50.000 frische, gleich gewichtete Shots aus dem archivierten Schaltkreis. Der rotierte X-Speicher hat Distanz 5, fünf Runden, 120 Detektoren und eine Depolarisationswahrscheinlichkeit von 0,005 nach Clifford-Gattern. Die übrigen Rauschparameter stehen auf null. Ganze Fehlermuster entstehen beim Simulieren des Schaltkreises und dürfen mehrere Fehler enthalten. Es wurden nur Detektorbits erfasst. Das Ergebnis gilt für dieses Rauschmodell, diesen Suchraum und die syntaktische Observable-Zuordnung.

Die primäre Größe ist die Wahrscheinlichkeit, dass **jeder** Cluster eines nichtleeren Shots beide Observablenklassen erreicht. Für einen späteren C0-Decoder mit unverändertem §17 ist sie eine Obergrenze für die PASS-Quote unter nichtleeren Shots. Das ausgewiesene Intervall beschreibt die Stichprobenunsicherheit der Erreichbarkeit. Ein gewichteter Margentest kann weitere Shots auf HOLD setzen. Logische Fehlerrate, PyMatching-Vergleich, FPGA-Latenz und Verhalten eines physischen Aufbaus wurden in diesem Schritt nicht gemessen.

## Vorab festgelegte Entscheidung

Der interne Entwicklungsplan in shot_protocol.json fixiert Schaltkreis, Graph, syntaktische Zuordnung, Seed, eine einzige Stichprobe mit 50.000 Shots, Nenner, Statuspriorität, Prüfung der Clustergrenze und die Entscheidung anhand eines zweiseitigen Clopper-Pearson-Intervalls von 99 %. Bei nichtleeren Shots sollte mindestens einer von zwanzig die *Möglichkeit* zur Fast-Path-Entscheidung haben. Diese 5 % sind ein für dieses Screening gewähltes Arbeitsziel. Ein anwendungsbezogenes Ziel aus tatsächlichen Zeit- oder Energiekosten wäre getrennt zu begründen. Die Grenze wurde vor der ersten Stichprobe festgelegt und dem Nutzer mitgeteilt.

- Obere Grenze unter 5 % ergibt NO_GO_5PCT.
- Untere Grenze bei mindestens 5 % ergibt REACHABILITY_FEASIBLE_5PCT.
- In allen anderen Fällen ergibt sich INCONCLUSIVE.

Die Intervallrechnung ist auf den beobachteten nichtleeren Nenner bedingt und setzt unabhängig identisch verteilte Shots des festgelegten Simulationsmodells voraus. Die vorab bestimmte Stichprobe wurde vollständig ausgewertet. SHA-256 des Versuchsplans ist `9352d6bd704022d4f36666943df9ee94287203391c425b82523c0a5f0910488b`.

## Vollständige Bilanz

| Ergebnis | Shots | Anteil an den nichtleeren Shots |
|---|---:|---:|
| Jeder Cluster erreicht beide Klassen | 1.681 | 3,75 % |
| Mindestens ein Cluster erreicht nur eine Klasse | 42.294 | 94,40 % |
| Mindestens ein Cluster überschreitet acht Detektoren | 830 | 1,85 % |
| Mindestens ein Cluster ohne zulässige Erklärung, nach Überlaufprüfung | 0 | 0,00 % |
| **Nichtleer gesamt** | **44.805** | **100 %** |

Weitere 5.195 Shots waren leer, also 10,39 % aller 50.000 Shots. Sie wurden separat geführt. Bezogen auf sämtliche Shots erreichten 3,362 % den Margenvergleich über ein nichtleeres Syndrom. Die 33.681 verschiedenen gemessenen Bitmuster wurden mit ihrer tatsächlichen Häufigkeit gewichtet.

Für die Statuszählung gilt die Reihenfolge leer, Überlauf, keine lokale Erklärung, Einzelklasse, alle Cluster zweiklassig. Ein Cluster größer als acht löst unmittelbar HOLD aus. Die Spalte NO_LOCAL_PAIRING bewertet nur Shots ohne solchen Überlauf. Detektorpaare dürfen einfache Detektorpfade bis vier Kanten nutzen. Der terminale Boundary-Pfad hat maximal zwei Kanten einschließlich des Abschlusses, die Clusterbildung verwendet höchstens zwei Detektorhops und innerhalb eines Pfads ist kein dritter aktiver Detektor zulässig. Die Rechenzeit im ersten Lauf einschließlich Modellkontrolle, Erzeugung, Auszählung und Gegenprüfung betrug rund 13,8 s auf dem verwendeten Rechner.

## Gegenprüfung

- Die aus dem Schaltkreis abgeleiteten DEM- und Graphdaten stimmen mit den archivierten Referenzen überein. Vor der Stichprobe reproduzierte der Klassifikator die syntaktischen Klassenmengen aller 1.679 früheren nichtleeren Einzelfehler-Syndrome. Explizite Kontrollen umfassen Größe 8/9, mehrere Cluster, terminale Boundary und ein fehlendes Pairing.
- Zwei Berechnungen der Clusterpartition wurden für alle Shotmuster verglichen. Gleiche Bitmuster verwenden dasselbe geprüfte Ergebnis. Eine zweite Suche mit Halbpfaden und expliziten Paarungsmengen kontrollierte die vorgeschriebenen Fälle ohne Überlauf. Für einen Überlauf wurde die unabhängig festgestellte Clustergröße geprüft.
- Die Kontrolle umfasst alle 1.681 zum Margenvergleich zugelassenen Shots und jeden 199. Shot ab Index 0. Nach Berücksichtigung der Überschneidung sind das 1.921 Shots mit 1.342 verschiedenen Bitmustern.
- Das exakte Binomialintervall wurde zusätzlich mit den entsprechenden Beta-Quantilen abgeglichen. Ein erneuter Lauf aus den archivierten Rohbits reproduzierte die Ergebnistabellen und die Zusammenfassung bytegenau.

## Paket und Reproduktion

results/detectors.b8 enthält exakt 750.000 Byte, zeilenweise 15 Byte je Shot, Detektor 0 im niederwertigsten Bit des ersten Bytes. SHA-256 ist `74de47b06b34e08edf7b8a010c16e7a79bf9f89c2d608dbbc8f338e9116ff671`. results/shot_status.csv dokumentiert jede Shot-ID (0-basiert), Anzahl aktiver Detektoren, Clusterzahl, größte Clustergröße, Status und Gegenprüfung. Die Gruppierung nach aktiven Detektoren ist rein deskriptiv. results/summary.json enthält das primäre Ergebnis.

Vom entpackten Verzeichnis aus arbeiten. Die vollständige Wiederholung der Ergebnisprüfung nutzt die Originalbits, unabhängig von plattformabhängigen Unterschieden der Pseudozufallsfolge. Die Beispielbefehle setzen eine Python-3.12-Umgebung mit den angegebenen Paketversionen voraus. Sie verwenden ein neues Ausgabeverzeichnis und führen die Kontrollassertionen aus.

```sh
python -m pip install -r requirements.txt
sha256sum -c SHA256SUMS.txt
python run.py replay --shots results/detectors.b8
diff results/summary.json replay/summary.json
diff results/shot_status.csv replay/shot_status.csv
diff results/by_detector_count.csv replay/by_detector_count.csv
```

Für die Reproduktion der Erzeugung in einer kompatiblen Stim-Umgebung dient `python run.py regenerated`. Der vorab festgelegte Seed lautet 2688799165999426676. Sämtliche Zahlen im Bericht beruhen auf der einen archivierten Stichprobe.

[Veröffentlichte d=5-Regeln und Schaltkreis](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/afd6efb795193a4d8414d18469ca14f85aa81dc4/research/x6_qed/section17_d5_v0_1) · [SciPy-Dokumentation zur exakten Intervallrechnung](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html)
