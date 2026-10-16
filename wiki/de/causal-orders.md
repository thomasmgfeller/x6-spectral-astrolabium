# Kausale Ordnungen und Raumzeitfragen

Hier geht es um die Frage, welche Struktur in Beziehungen steckt, bevor man eine räumliche Zeichnung voraussetzt.

[English](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/causal-orders.md) · [Wiki-Übersicht](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/)

Quellenstand: 2026-10-16 · `967c7662f005d887918cac9350e5bbaf76f653a9`

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

## Eigenzeit: Was wurde jetzt geprüft?

Eigenzeit ist die Zeit, die eine mitbewegte Uhr entlang ihres Weges misst. In diesem Versuch geht es um den Eigenzeitabstand einer geraden zeitartigen Verbindung zwischen zwei markierten Ereignissen in einem bekannten flachen Modell mit einer Raum- und einer Zeitdimension (1+1). Gesucht wird das Verhältnis theta = tau/T zum vorgegebenen äußeren Zeitmaßstab T.

Die einfache Referenz V zählt die K Ereignisse, die strikt zwischen den Markierungen liegen. Bei m = N−2 Hintergrundpunkten lautet ihre Schätzung sqrt(K/m). Anschaulich: Ein größeres Zeitintervall enthält im gleichmäßig befüllten Modell im Mittel mehr Punkte. Die Endpunkte selbst werden nicht mitgezählt. Koordinaten und wahre Testzielwerte erhält der Schätzer nicht.

Der erste Datenlauf ist mit vollständigen Rohdaten, Bericht und Reproduktionscode veröffentlicht. Er umfasst 6.912 Ordnungen: 768 für die Kalibrierung und 6.144 für Tests. Die Hauptbewertung war vorab auf 1.024 uniforme Testordnungen bei m=256, also N=258, festgelegt.

| Verfahren | RMSE im Hauptvergleich |
| --- | --- |
| V: Intervallpunktzahl | 0,031614 |
| D: globale Dichte-/Höhenregression | 0,177785 |
| C0: feste Konstante | 0,176774 |
| L: lokale längste Kette (beschreibend) | 0,084021 |

RMSE fasst die Schätzfehler zusammen; kleiner bedeutet hier genauer. Die Zahlen sind in Einheiten der normierten Eigenzeit angegeben. 0,031614 bedeutet nicht 3,16 % relativen Fehler bei jedem einzelnen Ereignispaar. V erfüllt die festgelegte Grenze 0,05 und alle weiteren Hauptkriterien. Das bedingte 95%-Bootstrap-Intervall der RMSE ist [0,030068; 0,033199]. Dabei bleibt die Kalibrierung fest.

D nutzt nur globale Größen und keine lokalen Merkmale der Markierungen. Der Abstand zu D ist deshalb keine Überlegenheit gegenüber allen möglichen Schätzern. V ist eine bekannte Referenz; dieser Versuch weist keinen spektralen Zusatznutzen nach.

- [Ergebnisbericht und Reproduktion](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/RESULTS.md)
- [Definition, Annahmen und ursprünglicher Vertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/README.md)

## Welche Grenzen bleiben?

Die Zusatzkontrollen vergleichen uniforme Ordnungen mit einem gestörten Gitter bei exakt gleicher Knotenzahl, Relationszahl und Höhe. Bei m=64 und m=144 wurden jeweils 128 Paare ausgewertet. Bei m=256 waren nur 63 statt der geforderten 128 Paare verfügbar. Diese größte Zusatzkontrolle bleibt INSUFFICIENT_COMMON_SUPPORT und erhält keine Leistungsbewertung; die Grenze wurde nicht nachträglich gelockert.

- Dimension und äußerer Zeitmaßstab sind vorgegeben, nicht aus der Ordnung entdeckt.
- Dieselbe endliche Ordnung kann verschiedene Eigenzeiten zulassen; die Schätzung bleibt statistisch.
- Die Ergebnisse gelten für das festgelegte synthetische Modell. Gekrümmte Räume, andere Dimensionen und physische Messungen sind damit nicht geprüft.
- Externe Replikation und stärkere lokale Vergleichsschätzer bleiben offen. Die früheren negativen P123-Ergebnisse bleiben bestehen.

## Wie lässt sich der Befund nachprüfen?

Das Archiv enthält alle 6.912 vollständigen Ordnungen, Referenzkoordinaten, Markierungen und Einzelvorhersagen. Die interne Gegenprüfung überprüft 27.648 Vorhersagen und alle Ordnungen samt Umnummerierungen. Der GitHub-Prüflauf wiederholt die gesamte Studie ohne Netzwerkzugang und vergleicht die Ergebnisse. Dies ist interne Reproduktion, keine unabhängige externe Bestätigung.

Die Anleitung im Ergebnisbericht nennt Softwareversionen, Quellencommit und Befehle. Das ursprüngliche Archiv und der fixierte Rechenstand bleiben unverändert. Die Dokumentation unterscheidet außerdem den datierten Quellencommit von einem unabhängig belegten Zeitpunkt öffentlicher Vorabregistrierung.

- [Prüfbericht der Gegenrechnung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/results/verification.json)
- [Rohdatenarchiv und Prüfsummen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/lorentz_proper_time/results/RESULTS.json)
- [Veröffentlichung und GitHub-Prüfungen: PR #44](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/44)
- [Causal-Set-Labor (eigenständiger Browserprototyp)](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/rax-cqg-lab.html)
