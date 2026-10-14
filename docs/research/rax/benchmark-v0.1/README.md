# RAX-B1 — Benchmarking v0.1

**Abgeschlossen: synthetischer Vergleich adaptiver, fester und zufälliger
Messpläne. Gleiche Messbudgets, getrennte Prüfdaten, vollständige Ergebnisberichte.
Die acht vorab festgelegten Überlegenheitsentscheidungen bleiben unentschieden.**

## Freigegebene Dateien

- [Ergebnisbericht (PDF, 10 Seiten)](RAX_B1_Benchmarking_v0_1.pdf)
- [Vollständiges Reproduktionspaket (ZIP)](RAX_B1_Benchmarking_v0_1_Paket.zip)
- [Veröffentlichungsnachweis und SHA-256-Prüfsummen](PUBLICATION.json)

Die Dateien werden unverändert veröffentlicht. Hinweise im Paket auf eine noch
nicht erfolgte GitHub-Veröffentlichung bezeichnen dessen damaligen Stand.
Diese Übersichtsseite und PUBLICATION.json dokumentieren die anschliessend
freigegebene Veröffentlichung.

## Versuch und Ergebnisse

Drei Planer erhalten jeweils genau 4, 8, 16 oder 32 Akquisitionsbeobachtungen:
Adaptiv maximiert den nächsten erwarteten Informationsgewinn; der feste Plan
minimiert vorab die erwartete Entropie durch exhaustive Suche aller ganzzahligen
Messverteilungen; der zufällige Plan wählt die informativen Aktionen gleichverteilt.
Pro Episode werden 128 zusätzliche Prüfbeobachtungen erst nach Fixierung sämtlicher
Vorhersagen erzeugt. Die Pläne teilen diese Prüfmenge und gepaarte potentielle
Ergebnisfolgen. Entwicklung und Test nutzen getrennte Seed-Domänen.

| Messbudget | Adaptiv | Fest optimal | Zufällig |
| ---: | ---: | ---: | ---: |
| 4 | 0,213006 | 0,217503 | 0,217787 |
| 8 | 0,205448 | 0,209062 | 0,209399 |
| 16 | 0,201714 | 0,203095 | 0,203427 |
| 32 | 0,199193 | 0,199920 | 0,200021 |

Mittlerer Prüf-Brier-Score; kleiner ist besser. Je Wert 4.608 gepaarte Episoden
über neun gleich gewichtete Modell-/Rauschbedingungen. Beide Kontrollfälle
werden separat berichtet. Der beobachtete Fehler ist bei Adaptiv jeweils kleiner;
**sämtliche acht simultanen Hoeffding-Intervalle enthalten jedoch null**.
Die sekundären approximativen Intervalle ersetzen die Hauptentscheidung nicht.

Der gesamte Test umfasst 5.632 Episoden, 67.584 Plan-/Budgetläufe und
1.013.760 Akquisitionsbeobachtungen, gezählt über diese Läufe. Entwicklung:
352 Episoden und 4.224 Läufe. Keine ausgeschlossenen Episoden und kein Frühstopp.
Der Kontrollgenerator ausserhalb des Kandidatenmodells wurde in 512/512 Episoden
verworfen, obwohl der Posterior stark auf einen falschen Kandidaten konzentriert
war. Im reinen Beobachtungskontrollfall ist die kausale Klasse nicht identifizierbar.

## Reproduktion und Prüfung

Das ZIP enthält alle Rohdaten, Aktions-/Ergebnisfolgen, Posteriorwerte,
Quellcodes, den eingefrorenen Vertrag, vollständige Designenumerationen,
Entwicklungs- und Testnachrechnungen sowie ein SHA-256-Inventar. `analysis.json`
enthält 204 Berichtszellen mit voller Präzision. Der PDF-Bericht zeigt sämtliche
132 Stratum-/Budget-/Planzellen und die Einordnung der Ergebnisse.

12 technische Vorabtests, die separate Nachrechnung aller 67.584 Testläufe
und der Abgleich aller 204 Berichtszellen bestanden. Zweiter Implementierungsweg
bedeutet keine externe Person oder Blindprüfung. Die vollständigen Forschungs-
Commits sind im enthaltenen Git-Bundle mit dokumentierter Basisvoraussetzung
bewahrt; die Benchmarkdateien sind zusätzlich ohne Git-Abhängigkeit enthalten.

Nach Entpacken im Paketverzeichnis:

```bash
python verify_package.py
cd benchmark
python -c "import reference; print(reference.verify('evidence/campaign-v0.1', 'test'))"
```

## Geltungsgrenzen

**Nachträglicher Methodenbefund:** Die [RAX-M1-Methodenprüfung](../method-review-v0.1/README.md)
belegt, dass der bisherige Isolationstest einen absichtlich prüfdatenabhängigen
Planer nicht erkennt und der Referenzprüfer eine gezielt erzeugte negative
Index-Aliaszeile akzeptiert. Das historische Bestehen der Prüfungen ist daher
kein umfassender Isolations- oder Vollständigkeitsnachweis. Die Originaldaten
bestehen die mit M1 ergänzte strengere Abdeckungsprüfung und die vollständige
Nachrechnung; sämtliche acht Hauptentscheidungen bleiben unentschieden.
Weitere Grenzen betreffen den Mess-Callback und die Freeze-Selbstauskunft.
Die eingefrorenen B1-Dateien bleiben unverändert; Zusatzprüfer und reproduzierbare
Gegenbeispiele liegen im separat versionierten Methodenpaket.

- Kleiner endlicher synthetischer Kontrollversuch mit bekanntem Leserauschen;
  keine physikalische Validierung und kein ausgeführtes RAX-U2.
- Greedy-EIG ist kein globales Mehrschrittoptimum. Unentschiedenheit beweist
  weder Gleichwertigkeit noch die Abwesenheit eines Vorteils.
- Gleiche Messkosten und gleiche Rechenobergrenzen; unterschiedliche tatsächliche
  CPU-Zeiten. Zufallsplan-/Ergebnisbank-Erzeugung liegt ausserhalb des Online-
  Zeitfensters, daher keine vollständige Gesamtkosten-Rangfolge.
- Keine externe Präregistrierung oder unabhängige personelle Begutachtung.
- Kontrollierte Schreibfehlerprüfungen und Hash-Rücklesen qualifizieren keine
  Stromausfallsicherheit; der frühere U1-Archivvorfall bleibt ungeklärt.

Siehe das [RAX-Forschungsprogramm und den gesamten Evidenzstand](../README.md)
sowie die [RAX-U1-Gegenprüfung](../countercheck-v0.1/README.md).

Copyright 2026 Thomas Gfeller. Originale Projektbeiträge unter
[Apache-2.0](../../../../LICENSE), gemäss
[Lizenzumfang](../../../../LICENSE_SCOPE.md). Verlinkte Literatur behält
ihre jeweiligen Rechte.
