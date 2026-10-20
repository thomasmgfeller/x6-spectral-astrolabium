# Einbettungskovarianz: konkrete Voraussetzung für Ansatz 2

Stand: 20. Oktober 2026. Gegenstand ist der vorhandene Code in PR #69,
insbesondere `cg_inference.py`, `cg_relations.py` und `variance_weights.py`.
**HOLD_EMBEDDING_COVARIANCE bleibt bestehen.** Der Metadatenversuch verändert
Operatorgewichte. Er liefert weder Koordinatenkorrekturen noch eine validierte
Einbettungskovarianz. Ansatz 3 bleibt bis zur Identifizierbarkeit zurückgestellt.

## Welche Matrizen vorhanden sind

| Größe | Bedeutung | Verwendbarkeit für Ansatz 2 |
|---|---|---|
| `sigma² B Bᵀ` | Bedingte Kovarianz der Feldrauschanteile mehrerer skalarer Operatorantworten, einschließlich geteilter Ereignisse | Exakt unter bekanntem IID-Feldrauschmodell; keine Koordinatenkovarianz |
| Saubere Residualkovarianz | Streuung von Operatorfehlern über Kalibrierwolken und deklarierte Felder | Enthält Rekonstruktions-, Diskretisierungs-, Auswahl- und Feldabhängigkeit; keine isolierte Einbettungsunsicherheit |
| `G + mu muᵀ` im neuen Pilot | Zweites sauberes Fehlermoment einschließlich verbleibendem Bias | Arbeitswert für den skalaren Filter; keine bedingte Kovarianz und kein Koordinatenprior |
| Moment-QP-Hesse-Matrix `I + 11ᵀ` | Feldrauschkosten für Gewichte einschließlich Root | Ihre Inverse ist keine Einbettungskovarianz |
| Euklidische Projektionsstrafe | Minimale Koordinatenverschiebung innerhalb einer konvexen inneren Approximation | Derzeit isotrop; besitzt noch keine statistisch kalibrierte Präzision |

Die Geometrie besitzt drei Koordinaten je ausgewähltem Stützpunkt. Die Anzahl
und Auswahl dieser Punkte wechseln zwischen Wolken. Die bisherige 2×2-Matrix
vergleicht dagegen zwei skalare Antworten derselben Wolke. Die Matrixgrößen
und die statistischen Bedeutungen sind verschieden.

## Minimaler sauberer Anschluss

1. **Zielgröße definieren.** Entweder eine Koordinatenfehlerverteilung in einem
   festgelegten, identifizierten Lorentz-Bezugsrahmen oder Unsicherheit von
   invarianten Gram-/Intervallgrößen. Rootfixierung beseitigt Translation,
   aber nicht sämtliche Lorentz-Freiheiten. Die Wahl gehört in den Prüfvertrag.
2. **Kalibrierung auf vollständige Rekonstruktionen beziehen.** Dieselben
   Intervalle und Landmarken beeinflussen mehrere Punkte. Auswahl, Guards und
   aktive Relationsbedingungen gehören zum Verfahren. Eine Hesse-Matrix für
   festgehaltene Auswahl erfasst diese Unsicherheiten nicht vollständig.
3. **Kleine positiv semidefinite Modellklasse festlegen.** Bei nur 90 bisher
   nutzbaren Wolken wäre eine frei geschätzte hochdimensionale Kovarianz
   unzureichend abgesichert. Eine strukturierte Kovarianz benötigt explizite
   gemeinsame Komponenten und darf geteilte Daten nicht unabhängig zählen.
4. **Unabhängig validieren.** Vor der Verwendung: neue Wolken, separater
   Mittelwertfehler, standardisierte Residuen, Richtungs-/Blocküberdeckung,
   Ausfallquote, Kondition und Transfer auf vorab festgelegte Wolkenmerkmale.
   Empirische Streuung über Wolken ist nicht automatisch bedingte Unsicherheit
   einer bestimmten beobachteten Ordnung.
5. **Erst danach die Projektionsmetrik ersetzen.** Für festes positives
   Präzisionsmodell im identifizierten Unterraum wird
   `(X-X0)ᵀ precision(C) (X-X0)` minimiert; die bisherigen exakten Relations-
   constraints bleiben bestehen. Die Zielfunktion ist dann weiterhin konvex.
   Eine gleichmäßige Skalierung der einzigen Zielfunktion ändert den Minimierer
   nicht. Abstände, Operatorfehler und Relationsverträglichkeit werden getrennt
   bewertet. Die Projektion ist nur eine hinreichende innere Approximation;
   ihr Scheitern beweist keine Nichteinbettbarkeit.

## Warum Ansatz 3 noch nicht folgt

Bei `z=h(X)+b+epsilon` kann ein uneingeschränktes `b` jede Änderung von `X`
absorbieren. Eine gemeinsame Iteration braucht eine eingeschränkte Bias-Klasse,
zusätzliche unabhängige Information und einen Rang-/Identifizierbarkeitsnachweis
nach Behandlung der Bezugsrahmenfreiheit. Wiederholte Verwendung derselben
Messung liefert keine neue unabhängige Evidenz. Ein Zielwert aus den verborgenen
Simulatorkoordinaten darf nur einen ausdrücklich als solchen bezeichneten
Oracle-Referenzversuch steuern.

Methodischer Hintergrund: [Ceres: Covariance Estimation und Gauge Invariance](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html);
[Brynjarsdóttir & O’Hagan (2014): Modellabweichung und Parameterkonfundierung](https://www.tonyohagan.co.uk/academic/abs/simmach.html).
Diese Quellen begründen keine Validierung unseres eigenen Rekonstruktors.
