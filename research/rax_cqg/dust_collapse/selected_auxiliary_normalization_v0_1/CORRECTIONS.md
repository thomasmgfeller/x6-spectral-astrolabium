# Korrekturen des eingereichten Normierungsartefakts

Die drei geprüften Uploads sind durch SHA-256 in [provenance.json](provenance.json) identifiziert. Das frühere Skript und seine Daten werden nicht als korrigierte Ausführung erneut veröffentlicht.

| Bisheriger Punkt | Korrektur |
|---|---|
| Acht Dimensionen implizit als vorhandener Randraum behandelt | Vier ausdrücklich ausgewählte von sieben Hilfsraum-Orbits, ergänzt um ein externes zweidimensionales Testlabel |
| Geometrieweise Gramgewichte fest eingebaut | Gewichte aus der Quelle gezogen und der stratumweisen v0.2-Basis zugeordnet |
| Beidseitige inverse Wurzel unabhängig von der Kernrolle | Koeffizienten- und kovariante Konvention getrennt; Standard erhält den bereits deklarierten formalen Operator |
| Große Singularwerte als Ergebnis eines bloßen Basiswechsels | Als zusätzlicher kovarianter Zuordnungsvergleich reproduziert |
| Geometrieblock aus Indizes 0,4 herausgegriffen | Tatsächliche Basislabels geprüft; Geometrieblock bei fester Stratum-/Testmarke hat in v0.2 Indizes 0,2 |
| Tensorrest als „Mischung“ | Stratum-/Testlabel-Masken auf beiden Matrixrichtungen |
| Gram vor der Prüfung hermitisiert | Nicht-Hermitizität zuerst geprüft; nur dokumentierte Rundungsreste bis zur numerischen Toleranz zulässig |
| delta_chi=1.0 und channel_dim=2 | Keine erfundene Uhrschrittweite; delta_chi=null, präzise Basis-/Rollenmetadaten |
| Nur Matrixgröße geprüft | Quelle, Hash, Rolle, Konvention, Basis, Indizes, Phase, Endlichkeit und Pflichtidentitäten geprüft |
| Fehlende Aussagegrenze im Datenprodukt | Alle acht physikalischen Gates HOLD; physikalische Materiematrix NOT_CONSTRUCTED, physikalischer Mischblock NOT_COMPUTED |

Der alte Normalisierer reproduziert auf seinem ursprünglichen geometrieweise geordneten Input die eingereichten Werte. Wendet man ihn unverändert auf die veröffentlichte stratumweise v0.2-Basis an, meldet er dennoch Erfolg und einen „Mischungsrest“ von **502.31464243041927**. Der tatsächliche Stratum-Mischblock bleibt dabei exakt null. Test 18 konserviert diesen Fehler als Negativkontrolle.

Die neue Version führt Matrix, Gram und Basis konsistent mit. Test 12 prüft einen zusätzlichen, nichttrivialen Basiswechsel. Tests 7 und 8 prüfen beide Kernkonventionen an nichtkommutierenden bzw. unterschiedlichen Produkten; diese algebraischen Positivkontrollen werden nicht als physikalische Produkte ausgegeben.

Die vorgeschlagene Prüfung unterschiedlicher Ein-/Ausgangsprodukte bleibt als wissenschaftliche Frage zulässig. Eine automatische Aufwertung als „physikalisch sinnvollere Möglichkeit“ entfällt: Produkte müssen unabhängig aus den jeweiligen Räumen begründet sein. Für positive diagonale Produkte ist die hier untersuchte Zuordnung bei z=1 bereits durch ein positives Nebendiagonalelement ausgeschlossen.
