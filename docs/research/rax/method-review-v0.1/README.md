# RAX-M1 — Methodenprüfung v0.1

**Abgeschlossen: interne nachträgliche Prüfung des veröffentlichten
RAX-B1-Benchmarks auf Datenlecks, falsche Unabhängigkeitsannahmen und überzogene
Aussagen. Zwei Validierungsfehler sind reproduzierbar belegt; hinzu kommen
Grenzen bei der Datenabschottung und der Freeze-Selbstauskunft. Die Originaldaten
bestehen die Zusatzprüfungen. Alle acht Hauptentscheidungen bleiben unentschieden.**

## Freigegebene Dateien

- [Methodenbericht (PDF, 7 Seiten)](RAX_M1_Methodenpruefung_v0_1.pdf)
- [Vollständiges Beleg- und Reproduktionspaket (ZIP)](RAX_M1_Methodenpruefung_v0_1_Paket.zip)
- [Veröffentlichungsnachweis und SHA-256-Prüfsummen](PUBLICATION.json)

PDF und ZIP entsprechen unverändert den freigegebenen Dateien. Hinweise im ZIP,
wonach die Methodenprüfung noch nicht auf GitHub veröffentlicht sei, bezeichnen
den Stand vor dieser Freigabe. Diese Seite, PUBLICATION.json und der zugehörige
Repository-Commit dokumentieren die anschliessende Veröffentlichung.

## Befunde und Wirkung

| ID | Reproduzierbarer Befund | Einordnung für den ursprünglichen B1-Lauf |
| --- | --- | --- |
| M1 | Ein negativer Episodenindex wird als Alias der letzten Episode akzeptiert. Eine veränderte Kopie besteht Referenz und Analyse mit 511 bzw. 513 Kontrollzeilen statt je 512. | Fehler der semantischen Vollständigkeitsprüfung. Die veröffentlichten Originaldaten enthalten diesen Fehler nicht und bestehen die strengere Prüfung aller Zellen. |
| M2 | Der Holdout-Isolationstest verändert eine unbenutzte Variable. Ein absichtlich prüfdatenabhängiger Planer besteht den Einzeltest. | Das Test-OK belegt keine Isolation. Die vollständige separate Referenz weist die getestete Vorhersagemanipulation zurück. |
| M3 | Python-Introspektion auf den tatsächlichen Mess-Callback liest 64 potentielle Ergebnisse vor der ersten verbuchten Messung bei Budget 4. | Kein solcher Zugriff im eingefrorenen Originalplaner festgestellt. Die kooperative Schnittstelle ist keine wirksame Sandbox für fremde Planer. |
| M4 | freeze() schreibt test_outcomes_inspected=false trotz bereits vorliegender und eingesehener Testdateien. | Die volle Referenz verwirft die Kopie wegen falscher Zeitreihenfolge. Die ursprüngliche Chronologie ist korrekt; eine Selbstauskunft beweist keine Blindheit. |

Alle Eingriffe betreffen temporäre Kopien oder vorübergehend ersetzte
Funktionsbindungen. In den Kopien werden Dateiprüfsummen bewusst neu berechnet:
das prüft die semantische Validierung und behauptet keinen Angriff auf die
unveränderte Git-Veröffentlichung. Die 36 ursprünglichen Benchmarkdateien
bleiben bytegleich.

## Unabhängigkeit und Aussagegrenzen

B1 zählt korrekt 4.608 gepaarte Modell-Episoden je Hauptkontrast. Die 67.584
Plan-/Budgetzeilen sind keine ebenso vielen unabhängigen Versuche. Bonferroni
benötigt keine Unabhängigkeit zwischen den acht Kontrasten; die Unabhängigkeit
zwischen Episoden und innerhalb binomialer Messreihen bleibt eine Voraussetzung
des Generatormodells.

Exakte Gegenbeispiele zeigen, dass vollständig abhängige Wiederholungen die
tatsächliche Überdeckung eines vermeintlichen 95-%-Intervalls auf 0 % senken
können. Eine Auswahl anhand derselben Prüfdaten senkt den erwarteten Brier-Fehler
eines unveränderten Vorhersagers im dokumentierten Beispiel von 0,41 auf
0,235534. Diese Fehlanwendungen wurden im Originalbenchmark nicht festgestellt.
Der Bericht trennt tatsächliche Prüflücken von solchen Annahmen-Stresstests und
von unzulässigen Weiterinterpretationen, die der veröffentlichte B1-Bericht
teilweise bereits ausdrücklich ausschliesst.

## Reproduktion und ergänzende Prüfregeln

Das Paket enthält das unveränderte veröffentlichte B1-Archiv, alle neuen
Prüfquellen und Ergebnis-JSONs, relevante manipulierte Einzelzeilen und Digests,
den Methodenvertrag, den Bericht sowie ein SHA-256-Inventar. Die grossen
veränderten Kopien werden aus den enthaltenen Rezepten erneut erzeugt.

Nach dem Entpacken im Paketverzeichnis:

```bash
python verify_package.py
python reproduce.py --workdir ../new-reproduction
```

Der Zielordner muss neu sein und ausserhalb des Pakets liegen. Geprüfte Umgebung:
Linux/POSIX, Git, Python 3.12.14, NumPy 2.3.5 und SciPy 1.17.0. Die Reproduktion
benötigt kein Netzwerk und legt einen lokalen Hilfs-Checkout an. Dieser ist kein
Ersatz für den historischen Quell-Freeze. Zeitstempel und Laufzeiten dürfen
variieren; Befunde, exakte Brüche, Digests und Zählungen müssen übereinstimmen.
Für Gleitkommazahlen gelten die dokumentierten numerischen Toleranzen.

Der vollständige Einstieg wurde in einem frischen Verzeichnis ausgeführt:
**neun Prüfblöcke reproduziert, exakte Beispiele separat nachgerechnet und sechs
Testmethoden für die Zusatzregeln bestanden.** Die zweite Implementierung
stammt vom selben Autor; es liegt keine externe oder blinde Begutachtung vor.

`hardened_checks.py` ergänzt Indexbereich/-typ, kanonische Identität, exakte
Episode/Budget/Plan-Abdeckung und einen Vorabcheck auf sichtbare Testartefakte.
Diese Regeln sind beigefügt und getestet, aber nicht rückwirkend in die
eingefrorenen B1-Quellen eingebaut. Eine Prozessarchitektur für nicht
vertrauenswürdige Planer wurde hier nicht implementiert oder zertifiziert.

Die Methodenprüfung ändert keine primäre B1-Entscheidung und ist keine neue
Bestätigungskampagne, kein ausgeführtes RAX-U2 und keine physikalische Validierung.

Siehe [RAX-B1-Benchmark](../benchmark-v0.1/README.md) und
[RAX-Forschungsprogramm](../README.md).

Copyright 2026 Thomas Gfeller. Originale Projektbeiträge unter
[Apache-2.0](../../../../LICENSE), gemäss
[Lizenzumfang](../../../../LICENSE_SCOPE.md). Verlinkte Literatur und separat
lizenzierte Bestandteile behalten ihre jeweiligen Rechte.
