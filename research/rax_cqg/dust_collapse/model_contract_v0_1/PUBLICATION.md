# CST-DUST Model Contract v0.1

**6. November 2026 · Prüfvertrag spezifiziert; physikalischer CST-Modellschluss bleibt HOLD.**

Der Vertrag legt für den Zielkandidaten `CST-DUST-C1` die Modellklasse, einen endlichen Staubball mit Außenraum, physikalische Messgrößen und einen ersten Korrespondenztest vor der klassischen Singularität fest. Regularität erhält an **jedem Prüfpunkt eine eigene Entscheidung**. Ein Bounce-PASS verändert diese Entscheidung nicht.

- [Vertrag als PDF (zehn Seiten)](../reports/CST_DUST_Model_Contract_v0_1.pdf)
- [Lesbare Vertragsfassung](CONTRACT.md) und [maschinenlesbarer Vertrag](contract.json)
- [Unverändertes Originalpaket (ZIP)](../packages/CST_DUST_Model_Contract_v0_1_Pruefpaket.zip)
- [Entscheidungsprüfer](gate.py), [P0-Beispielrecord](examples/checkpoint_P0.json), [Nachrechnung](verify.py) und [Ergebnisse](results/verification.json)

## Getrennte Entscheidungen

Die acht Entscheidungen heißen `MODEL`, `CURRENT`, `CORRESPONDENCE`, `BOUNCE`, `REGULARITY`, `BOUNDARY`, `TRAPPING` und `EXTENSION`. Für den noch unvollständigen CST-Zielkandidaten stehen sie sämtlich auf **HOLD**. Ausführungszustände wie `NOT_RUN` bleiben davon getrennt.

Der Standardumfang der Regularitätsaussage ist ausdrücklich begrenzt: kontrollierte physikalische Dichte- und Krümmungsmomente mit uniformer Integrierbarkeit und Konvergenz im deklarierten Raumgebiet und Zeitintervall, zunächst bei fester Mittelungsskala. Damit sind weder punktweise Krümmungsbeschränktheit für jede Realisierung noch globale kausale Vollständigkeit bewiesen. Das inverse Volumenmoment erhält nur mit einer separat begründeten physikalischen Verbindung die Bedeutung einer Dichte- oder Krümmungskontrolle.

## Erster Korrespondenztest und Zulassung

`PST-FB-01` verwendet die klassische endliche Einstein-Staub-Referenz mit `G=1`, Anfangsradius `R0=10` und den Massen `1/4, 1, 4`. Das gemeinsame Fenster endet bei der Hälfte des frühesten Kollapszeitpunkts, `T≈3,72678`. Radius, Dichte, Hubble-Rate und Beschleunigung erhalten 5-%-Toleranzen, Massen- und Flussbilanzen 2 %. Die Fehlerbudgets umfassen Statistik und systematische Beiträge. Diese Zahlen sind vorab festgelegte Leistungsanforderungen, keine Naturkonstanten.

Die sieben Pflichten `D1-D7` bleiben offen: insbesondere vollständiger Historienträger, diskrete Staubwirkung und Maß, Randbeiträge, Anfangszustand, physikalische Observablen, Außenraum und vollständiger Laufplan. Der dynamische Test ist daher **HOLD / NOT_RUN**. Es wurden keine neuen CST-Ensembles erzeugt. Ein endlicher Test auf vier Auflösungen ersetzt keinen Grenzwertsatz.

## Ausgeführte Kontrollen

15 klassische Referenzfälle mit je fünf algebraischen Identitäten sowie 17 Kontrollen der Entscheidungslogik bestehen. Der maximale relative Identitätsrest beträgt ungefähr `1,11e-15`. Diese Gleitkommakontrollen sind keine Intervallzertifikate und keine CST-Dynamikdaten.

Die Kontrollen prüfen unter anderem, dass ein Bounce-PASS Regularität nicht hochstuft, endliche Stichproben keine uniformen Schranken belegen und ein Gegenbeispiel aus einem anderen Geltungsbereich den Zielkandidaten nicht widerlegt. `gate.py` prüft deklarierte, als geprüft markierte Evidenz und Datei-Hashes; es verifiziert keine mathematischen Beweise und erteilt keine automatische physikalische Freigabe.

## Veröffentlichung und Nachrechnung

Das Original-ZIP, alle 20 Archivmitglieder und die PDF wurden bytegleich übernommen. Die Aussage in der ursprünglichen Anleitung, dass der Erstellschritt keine GitHub-Veröffentlichung enthielt, bleibt als Herkunftssnapshot erhalten. Diese Seite dokumentiert die anschließende Publikation.

```sh
python3 research/rax_cqg/dust_collapse/model_contract_v0_1/publication_check.py --replay
```

Die Veröffentlichungskontrolle benötigt nur Python 3.10 oder neuer. Sie prüft Archiv, vollständige Prüfsummen, PDF-Gleichheit, Quellenherkunft und wissenschaftliche Aussagegrenzen. Die erneute Erzeugung des JSON-Vertrags und die Nachrechnung erfolgen in einer temporären Kopie; archivierte Ergebnisse werden nicht überschrieben. Strukturen und Entscheidungen müssen exakt übereinstimmen, numerische Ergebnisse mit `atol=1e-12`, `rtol=1e-12`. Der CLI-Erfolg eines gültigen Entscheidungsrecords ist kein physikalisches PASS.

**English.** The contract fixes separate decisions for classical correspondence, bounce, moment regularity, finite-ball matching, trapping and causal extension. Regularity is assessed at every checkpoint and never inferred from a mean-volume minimum. Fifteen classical reference cases and seventeen decision-logic controls pass. The full coupled CST candidate and singularity resolution remain on HOLD.

Projektbeiträge gemäß [Lizenzumfang](../../../../LICENSE_SCOPE.md). Quellen und ihre Aussagegrenzen stehen im [Vertrag](CONTRACT.md) und im [Herkunftsmanifest](inputs/provenance.json).
