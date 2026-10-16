# Kausale Ordnungen und Raumzeitfragen

Hier geht es um die Frage, welche Struktur in Beziehungen steckt, bevor man eine räumliche Zeichnung voraussetzt.

[English](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/causal-orders.md) · [Wiki-Übersicht](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/)

Quellenstand: 2026-10-16 · `08c64744caa584c940b45a8825d0b099ae0c92fb`

## Ereignisse und ihre Reihenfolge

Eine kausale Ordnung beschreibt, welche Ereignisse vor welchen anderen liegen können. Denke an drei Arbeitsschritte: A muss vor B passieren und B vor C. Dann muss auch A vor C liegen. Diese Folgerung heißt Transitivität.

Manche Paare haben keine vorgegebene Reihenfolge. In einer kausalen Raumzeitinterpretation können sie räumlich getrennt sein. Bei einem beliebigen erzeugten Netzwerk ist diese physikalische Interpretation aber noch nicht begründet.

Ein Hasse-Diagramm zeichnet nur die unmittelbaren Beziehungen. Die vollständige Relationsmatrix enthält zusätzlich alle Beziehungen, die durch Transitivität folgen. Eine hübsche Anordnung der Punkte auf dem Bildschirm ist noch keine gemessene Geometrie.

## Warum ein Spektrum nicht alles verrät

Eine gezeichnete Ordnung kann durch Umnummerieren ihrer Knoten anders aussehen und dennoch dieselbe Struktur haben. Isomorphie bedeutet hier: Es gibt eine bijektive Zuordnung der Knoten (jeder Knoten wird genau einmal zugeordnet), die alle gerichteten Beziehungen erhält. Die Zuordnung muss nicht die einzig mögliche sein.

Ein Fingerabdruck fasst die Struktur in wenigen Zahlen oder Häufigkeiten zusammen. Verschiedene Strukturen können dabei denselben Fingerabdruck erhalten – ähnlich wie verschiedene Menschen gleich groß sein können.

| Kürzel im Projekt | Was dahintersteckt |
| --- | --- |
| H7 | Eine konkret festgelegte Kombination von Spektren und Zählgrößen; keine eindeutige Kennung. |
| N1 | Lokale Nachbarschaftsprofile. |
| Q1 | Spektren gezielter Einpunkt-Erweiterungen. |
| R2 | Wiederholte Verfeinerung von Merkmalen geordneter Knotenpaare. |
| P123 | Histogramme gemeinsamer Vorgänger und Nachfolger für Ein-, Zwei- und Dreiermengen. |

Die veröffentlichten Gegenbeispiele zeigen Grenzen solcher Zusammenfassungen. Die vollständige gerichtete Relation und eine exakte Isomorphieprüfung bleiben die Vergleichsreferenz.

## Was leisten die faireren Kontrollen?

Zwei Erzeuger sind leicht zu unterscheiden, wenn einer viel dichtere oder höhere Ordnungen liefert. Deshalb wurden Vergleichspaare mit gleicher Knotenzahl N, Relationszahl R und Höhe H ausgewählt. Höhe meint hier die Länge einer längsten Kette, gezählt in Knoten.

Im veröffentlichten Hauptvergleich bei N=64 brachte P123 keinen nachgewiesenen Zusatznutzen: Die Basis erreichte 54,30 %, die Kombination 50,39 %. Vier von neun Vergleichszellen hatten zu wenige passende Paare und blieben ohne Leistungsbewertung. Das Ergebnis grenzt eine getestete Methode ein; es beweist keine allgemeine Unmöglichkeit geometrischer Erkenntnis.

- [Kontrollstudie mit Originaldaten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_matched_controls/README.md)
- [Gegenbeispiele und Rekonstruktionsgrenzen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_relational_boundary/README.md)

## Die nächste konkrete Frage: Eigenzeit

Eigenzeit bezeichnet die Zeit entlang einer zeitartigen Verbindung. Im festgelegten flachen 1+1-Modell ist das Ziel ihr Verhältnis zum bekannten äußeren Zeitmaßstab. Das ist eine statistische Schätzaufgabe zwischen zwei markierten Ereignissen.

Die Referenz zählt Punkte im offenen Intervall zwischen den Markierungen. In diesem Modell motiviert das die Schätzung sqrt(K/(N−2)). Der Maßstab und die Dimension sind dabei vorgegeben. Dieselbe endliche Ordnung kann mehrere verschiedene geometrische Einbettungen besitzen.

Der hier beschriebene veröffentlichte Referenzstand enthält Zieldefinition und Prüfvertrag aus PR #42. Der anschließende numerische Lauf wird gesondert dokumentiert; dieser Wiki-Stand erklärt ihn nicht pauschal für veröffentlicht oder physikalisch bestätigt.

- [Eigenzeit: Definition, Beispiel und Vertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/README.md)
- [Causal-Set-Labor öffnen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/rax-cqg-lab.html)
- [Grenzen des Browsermodells](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/research/rax/cqg-benchmark-v0.2.0/README.md)
