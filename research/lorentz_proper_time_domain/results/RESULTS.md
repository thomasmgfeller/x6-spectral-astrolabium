# Bedingte Eigenzeitschätzung in flachen Diamanten

Status: **CONDITIONAL_FLAT_MODEL_CHECK_PASSED**.

Ein fester lokaler Lauf, keine externe Replikation. Die nominalen 95%-Intervalle beruhen auf dem Binomialmodell. Keine Aussage über gekrümmte Raumzeiten, unbekannte Stichprobengesetze oder industrielle Leistung.

49,152 unabhängige Punktwolken, 31,457,280 Hintergrundpunkte, 24 Zellen. Laufzeit 4.44 s auf dieser Maschine; kein Leistungsvergleich.

Die Binomialformeln sind analytisch exakt; ihre Summen und Quantile werden in float64 ausgewertet. Empirische Deckung darf zufällig unter 95% liegen und wird gegen die tatsächliche konservative Modelldeckung geprüft.

| d | m | theta | Lage | RMSE MC | RMSE Modell | Deckung MC | Deckung Modell |
|---|---|---|---|---|---|---|---|
| 2 | 256 | 0.1 | central | 0.038038 | 0.038062 | 0.9854 | 0.9846 |
| 2 | 256 | 0.1 | boosted_shifted | 0.038926 | 0.038062 | 0.9829 | 0.9846 |
| 2 | 256 | 0.5 | central | 0.026789 | 0.027161 | 0.9580 | 0.9567 |
| 2 | 256 | 0.5 | boosted_shifted | 0.027752 | 0.027161 | 0.9492 | 0.9567 |
| 2 | 1024 | 0.1 | central | 0.015992 | 0.015935 | 0.9609 | 0.9584 |
| 2 | 1024 | 0.1 | boosted_shifted | 0.015501 | 0.015935 | 0.9648 | 0.9584 |
| 2 | 1024 | 0.5 | central | 0.013431 | 0.013544 | 0.9595 | 0.9529 |
| 2 | 1024 | 0.5 | boosted_shifted | 0.013745 | 0.013544 | 0.9487 | 0.9529 |
| 3 | 256 | 0.1 | central | 0.093611 | 0.093162 | 0.9971 | 0.9977 |
| 3 | 256 | 0.1 | boosted_shifted | 0.092717 | 0.093162 | 0.9961 | 0.9977 |
| 3 | 256 | 0.5 | central | 0.027951 | 0.027904 | 0.9600 | 0.9628 |
| 3 | 256 | 0.5 | boosted_shifted | 0.027688 | 0.027904 | 0.9663 | 0.9628 |
| 3 | 1024 | 0.1 | central | 0.062008 | 0.062466 | 0.9810 | 0.9796 |
| 3 | 1024 | 0.1 | boosted_shifted | 0.063460 | 0.062466 | 0.9800 | 0.9796 |
| 3 | 1024 | 0.5 | central | 0.013947 | 0.013822 | 0.9556 | 0.9528 |
| 3 | 1024 | 0.5 | boosted_shifted | 0.013844 | 0.013822 | 0.9521 | 0.9528 |
| 4 | 256 | 0.1 | central | 0.101394 | 0.101594 | 1.0000 | 0.9997 |
| 4 | 256 | 0.1 | boosted_shifted | 0.101243 | 0.101594 | 1.0000 | 0.9997 |
| 4 | 256 | 0.5 | central | 0.030647 | 0.031276 | 0.9644 | 0.9622 |
| 4 | 256 | 0.5 | boosted_shifted | 0.031645 | 0.031276 | 0.9658 | 0.9622 |
| 4 | 1024 | 0.1 | central | 0.098026 | 0.098142 | 0.9966 | 0.9951 |
| 4 | 1024 | 0.1 | boosted_shifted | 0.097997 | 0.098142 | 0.9961 | 0.9951 |
| 4 | 1024 | 0.5 | central | 0.014844 | 0.015246 | 0.9624 | 0.9614 |
| 4 | 1024 | 0.5 | boosted_shifted | 0.015211 | 0.015246 | 0.9585 | 0.9614 |

## Auflösungsgrenze

| d | m | theta | E[K] | P(K=0) | obere 95%-Grenze bei K=0 |
|---|---|---|---|---|---|
| 2 | 256 | 0.1 | 2.560000 | 0.076315 | 0.119609 |
| 3 | 256 | 0.1 | 0.256000 | 0.774043 | 0.242760 |
| 4 | 256 | 0.1 | 0.025600 | 0.974724 | 0.345846 |

Eine hohe Deckung bei kleinen Intervallen bedeutet keine hohe Genauigkeit: breite Intervalle können korrekt sein, obwohl die Punktschätzung meistens null ist.

## Kontrollen und Grenze

48 vorab festgelegte zweiseitige Binomialtests, Bonferroni-Familienniveau 1%. Alle p-Werte bleiben in summary.json. Zwölf volle Relationsmatrizen wurden getrennt aufgebaut, auf strikte Ordnung geprüft und mit dem vorhandenen Merkmalsextraktor verglichen. Die restlichen Wolken werden nur über die beiden Kegeltests gezählt; dies ist kein Laufzeitbenchmark vollständiger Ordnungsanalysen.

freeze.json fixiert Quellen vor den neuen Ziehungen. counts.json enthält alle K-Werte; Seeds und Generator stehen im Vertrag. verify.py prüft Rohzählungen, Quantilinversion, Kausalitäts-Gegenbeispiele und die Quellenbindung. Ein sauberer diskreter Poset zertifiziert keine Minguzzi-Kontinuumsbedingung.
