# Glossar: Begriffe ohne Umwege

Die Erklärungen sind Einstiegshilfen. Für eine Rechnung gilt immer die präzise Definition im jeweiligen Modul.

[English](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/glossary.md) · [Wiki-Übersicht](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/)

Quellenstand: 2026-10-18 · `01430ce5f0a648ad63d611a451f0d0fd7ccb16aa`

## Die wichtigsten Begriffe

| Begriff | Bedeutung |
| --- | --- |
| Signal | Wertefolge, meist über die Zeit. |
| Spektrum | Darstellung von Frequenzanteilen oder – bei einer Matrix – ihrer Eigenwerte. Der Kontext entscheidet. |
| Fouriertransformation / FFT | Zerlegung in Schwingungsanteile; FFT ist ein schneller Rechenweg dafür. |
| Phase | Lage eines Schwingungsanteils innerhalb seines Zyklus. |
| Rauschen | Zusätzliche Schwankungen; welche Anteile stören, hängt von der Aufgabe ab. |
| Graph | Knoten und ihre Verbindungen. |
| Laplacematrix | Matrix aus Knotengraden und Verbindungen; hier ein genau definierter Graphoperator. |
| Eigenwert / Spektrallücke | Kennzahl eines Operators / Abstand zwischen bestimmten Eigenwerten. Welche Lücke gemeint ist, muss definiert sein. |
| Kausale Ordnung / Poset | Menge mit gerichteter, transitiver Ordnung; nicht alle Paare müssen vergleichbar sein. |
| Hasse-Diagramm | Darstellung der unmittelbaren Beziehungen einer endlichen Ordnung. |
| Isomorphie | Gleiche Struktur nach einer bijektiven Umbenennung der Knoten. |
| Invariante / Fingerabdruck | Merkmal, das beim erlaubten Umbenennen gleich bleibt; muss nicht eindeutig sein. |
| Intervall K | Im Eigenzeitversuch: Zahl der Ereignisse strikt zwischen zwei markierten Ereignissen. |
| Höhe H | Länge einer längsten Kette; hier in Knoten gezählt. |
| Relationsdichte | Anteil vergleichbarer Paare nach der genau angegebenen Zählkonvention. |
| Minkowski-Modell | Flaches relativistisches Raumzeitmodell; keine Krümmung. |
| 1+1 Dimensionen | Eine Zeit- und eine Raumdimension. |
| Eigenzeit | Zeitmaß entlang einer zeitartigen Verbindung; im Versuch relativ zu einer äußeren Skala. |
| Seed | Startangabe für eine reproduzierbare Zufallsfolge. |
| Baseline | Festgelegtes Vergleichsverfahren. |
| Kontrolle / Gegenbeispiel | Prüffall für eine konkrete Fehlerquelle / Fall, der eine allgemeine Behauptung widerlegt. |
| Holdout | Daten, die nicht zur Anpassung oder Auswahl des Verfahrens verwendet werden. |
| Bootstrap | Wiederholtes Ziehen aus vorhandenen Daten zur Abschätzung einer bestimmten Unsicherheit. |
| RMSE | Wurzel des mittleren quadratischen Fehlers. |
| Commit | Genau bezeichnete Version eines Git-Projekts. |
| Pull Request / PR | Vorschlag, eine Änderung in einen anderen Entwicklungszweig zu übernehmen. |
| CI | Automatisch ausgeführte Integrations- und Prüfabläufe. |
| Replay / Replikation | Erneute Berechnung / Wiederholung eines Befunds; Umfang und Unabhängigkeit müssen benannt werden. |
| Provenienz / Hash | Dokumentierte Herkunft / Prüfsumme von Bytes. |
| Kontinuumslimes | Mathematisch kontrollierter Übergang von diskreten Objekten zu einem kontinuierlichen Grenzmodell. |

## Ein Wort kann mehrere Bedeutungen haben

Ein Graphspektrum ist nicht dasselbe wie das Frequenzspektrum einer gemessenen Schwingung. Ebenso ist eine Spektrallücke nicht automatisch eine physikalische Energielücke. Prüfe immer, welcher Operator, welche Einheit und welches Modell gemeint sind.

- [Mathematischer Vertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SCIENTIFIC_SCOPE.md)
- [Methoden des Signal Labs](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SIGNAL_LAB_METHODS.md)
