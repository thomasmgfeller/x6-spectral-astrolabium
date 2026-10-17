# Sequenzielle Eigenzeit und bedingte Ordnungsdiagnostik

Status: **DECLARED_SEQUENTIAL_REFERENCE_CHECK_PASSED**.

Zeituniforme Absicherung nach Howard et al. unter festem Stichprobengesetz; keine Krümmungsidentifikation. Intern ausgeführt und geprüft, keine externe Replikation.

Zeitfehlerbudget 2,5%, einmalige Kettendiagnostik 2,5%; unter dem deklarierten flachen Modell gemeinsame Fehlereigniswahrscheinlichkeit höchstens 5% per Union Bound. Ein nicht signifikanter Kettentest beweist das Modell nicht.

## Sequenzielle Monte-Carlo-Kontrolle

Die Hauptläufe simulieren Binomial-Zählungen unabhängiger Beobachtungsblöcke, keine vollständigen Punktwolken. Ein zusätzlicher Lauf prüft den tatsächlichen Koordinaten-/Relationsdatenweg. Die zeituniforme Garantie stammt aus dem Satz; die Monte-Carlo-Kontrolle beobachtet nur die festgelegten Batch-Endpunkte.

| Fall | Läufe | Präzision erreicht | Median n bei Erreichen | Median K | Pfade mit Fehlüberdeckung |
|---|---|---|---|---|---|
| local_4d | 1024 | 1024 | 2592.0 | 164.0 | 0 |
| global_4d | 1024 | 1024 | 1673216.0 | 169.0 | 0 |
| flat_2d | 1024 | 1024 | 53248.0 | 535.0 | 0 |
| zero_resolution_control | 64 | 0 | None | None | 0 |

Die Medianwerte sind beobachtete Stichprobenbedarfe, keine garantierten Budgets. Die globale und lokale Referenz verwenden unterschiedliche Batchgrößen. Früher berechnete Feststichprobenbudgets sind keine Budgets dieser breiteren sequenziellen Schranke.

## Kettendiagnostik bei festem K

| d | K | Nullmodell-Warnungen / 128 | Dichtestörung im flachen Raum / 128 | Kette / 128 | Antikette / 128 |
|---|---|---|---|---|---|
| 2 | 16 | 2 | 122 | 128 | 128 |
| 2 | 64 | 1 | 128 | 128 | 128 |
| 4 | 16 | 1 | 128 | 128 | 106 |
| 4 | 64 | 1 | 128 | 128 | 128 |

Jeder Nulltest verwendet eine frische unabhängige Referenzbank von 255 Höhen. Zweiseitige Rang-p-Werte schließen Bindungen konservativ ein. Die Dichtestörung ändert die räumlichen Koordinaten, nicht die flache Metrik: Warnungen in dieser Kontrolle sind ausdrücklich kein Krümmungsnachweis.

## Integrierter Geometrielauf

Status PRECISION_REACHED; n=2560, K=165, Eigenzeitintervall [0.08931075368598042, 0.1088433934184303], Punktschätzung 0.09811438 bei wahrem Wert 0,1. Kettendiagnostik: NO_DEVIATION_DETECTED.

## Annahmenverletzung

Eine technische Speicherkorrektur und der anschließende identische Replay
sind in [EXECUTION_HISTORY.md](../EXECUTION_HISTORY.md) dokumentiert.
Alle ursprünglichen Zählblöcke blieben erhalten und wurden exakt abgeglichen.

Beim absichtlich abhängigen Kontrollstrom wird ein einmal gezogener Wert endlos wiederholt. 128 von 128 Pfaden verlieren die Überdeckung. Diese Kontrolle liegt außerhalb der Garantie und zeigt, warum Metadaten oder Software allein kein gültiges Stichprobengesetz herstellen.

Laufzeit: 6.44 s, kein kontrollierter Leistungsvergleich. Quellenfixierung in freeze.json; Zählblöcke in batch_counts.npz; vollständige Referenzhöhen, Stoppergebnisse und p-Werte in summary.json. Keine nachträgliche Wahl eines günstigeren Parameters oder Seeds.
