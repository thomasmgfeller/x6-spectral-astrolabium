# CST-DUST · Erweiterungsstabilität bei 14 Ereignissen (v0.5)

Die dritte Einfügung prüft die bisherige N13-Stabilitätsgrenze unter demselben Rand- und Detektorvertrag. Beide N11-Eltern tragen anfangs je das Amplitudengewicht 1/2. Jede gibt den gleichen Anteil λ ab und darf ihn frei auf ihre erreichbaren N12-, N13- und zugelassenen N14-Nachkommen verteilen. Gemeinsame Endgeometrien werden kohärent addiert. Die erste Dichte beträgt 1/8, die zweite 1/4. Der vierteilige q₇-Detektor zählt pro Versuch drei akzeptierte Ausgänge und den Fehlschlag. Als Referenz dient [N13 v0.4 auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/71d8e32186a81e6f3ef571450397eafe357dc174/research/rax_cqg/dust_collapse/extension_stability_v0_4).

## Befund

| Träger | Für alle erlaubten Aufteilungen gesichert bis | Explizite Verletzung bei |
|---|---:|---:|
| Zwei Eltern, fünf N12- und alle 23 erreichbaren N13-Typen (v0.4) | 5,1179 % | 5,1180 % |
| Dieselben 30 Typen und die zehn N14-Typen mit Eliminationsbreite drei | 5,0282 % | 5,0283 % |
| Alle 139 zulässigen N14-Typen zusätzlich | 1,6 % unter den geprüften N11-Eingangsschranken | 5,0283 % auf beiden endlichen Gittern |

Die Prozentwerte bezeichnen Anteile des Amplitudengewichts. Die ersten beiden Zeilen beruhen auf rationalen Ungleichungen für die numerischen Auslesematrizen beider Gitter. Ein PDF-Bericht liegt im Paket. Die [Herleitung der allgemeinen unteren Grenze](Schranke.md) benennt die Voraussetzungen für die exakten Uhrintegrale.

## Drei Einfügungen und ihre Reihenfolge

Das Inventar untersucht alle möglichen dritten Einfügungen nach einem zulässigen N13-Präfix. Von den 23 N13-Eltern führen 531 verschiedene Eltern-Tochter-Paare zu 238 unterschiedlichen N14-Endtypen. 139 Typen bestehen die geerbte Skalarprüfung. Es bleiben 413 Eltern-Tochter-Paare und 4 280 vollständige markierte Pfade (vor der letzten Skalarprüfung 5 240). Jede N13-Elternordnung hat mindestens eine zulässige Tochter. Die Auszählung der Einfügungen ist durch das Löschen eines ausgezeichneten Ereignisses mit Automorphismuskorrektur an allen 318 unmarkierten Ordnungen auf sechs inneren Ereignissen kontrolliert. Ein unabhängiger ganzzahliger Rangtest bestätigt die Einstufung aller 238 erreichten Endtypen.

Die Austauschbarkeit der drei Einfügungsmarken verlangt Zulässigkeit in jeder der sechs Reihenfolgen. 924 von 1 834 Vorwärtspfaden aus der Kette und 1 026 von 2 446 aus der Ein-Kanten-Ordnung erfüllen das. Ein exakter rationaler Zeuge pro Ausgangshistorie belegt, dass sich die bisherige **austauschsymmetrische** markierte N13-Paarverteilung unter dieser Zusatzbedingung erhalten lässt. Jeder in allen Reihenfolgen zulässige Pfad hat dabei positives Gewicht. Zusammen tragen 101 Endtypen Gewicht. Der maximal beimischbare Gleichverteilungsanteil auf diesen Pfaden beträgt 1386/2635 bzw. 19/49. Die Lösungsräume haben mindestens 119 bzw. 153 freie Dimensionen. Bei den zehn berechneten N14-Typen tragen in diesen Lösungen vier Endtypen Gewicht. Die Detektorantwort der gesamten austauschsymmetrischen Verteilung bleibt offen.

## Detektorprüfung

Die Auswahl für die Uhrrechnung erfolgte anhand der Eliminationsbreite. Sie bezeichnet die maximale Zahl von inneren Uhren in einem gemeinsamen Zwischenfaktor. Unter den 139 Typen haben 10, 49, 62 und 18 die Breiten 3, 4, 5 und 6. Die vor der Auslese festgelegte erste Auswahl umfasst die ersten acht Typen minimaler Breite nach kanonischer Maske. Nach dem kurzen ersten Lauf wurden die verbleibenden beiden Breite-3-Typen als separater Zusatztest berechnet. Das Prüfpaket weist beide Ergebnisse getrennt aus. Die Gitter (32,6) und (48,8) sowie die gekreuzten Auflösungen (32,8) und (48,6) isolieren den Einfluss innerer und äusserer Quadratur. Eine direkte Sechs-Uhren-Summe auf kleinem Gitter und eine unabhängige gedämpfte Skalarrechnung prüfen die zehn neuen Zweige.

Die ursprünglichen 30 Typen und alle fünf Kontroll- bzw. Hauptpräparationen sind in der Gitterprüfung enthalten. Auf dem erweiterten 40-Typen-Träger ergibt die exakte Rechnung für die kohärente Hauptpräparation strikte Konvexität des Erfolgs, abnehmende akzeptierte Ausgänge bis λ = 0,06 und ein negatives Vorzeichen der Dichteantwort. Eine Tangente der Erfolgsmatrix liefert bei 5,0282 % eine untere Schranke über beide erreichbaren Tochtermischungen. Das Niveau bleibt bei beiden Dichten über 90 % des N11-Referenzerfolgs. Der separate vierteilige Kontrasttest und der Vorzeichentest sind erfüllt. Der vorab festgelegte Achter-Satz ergibt dieselbe Klammer.

**Gegenbeispiel.** Beide Eltern geben ihren gesamten transferierten Anteil an N14-Typ 760. Zulässige Wege sind beispielsweise N11-Kette → N12_15 → N13_23 → N14_760 und N11-Ein-Kanten-Ordnung → N12_14 → N13_205 → N14_760. Bei 5,0283 % fällt der Erfolg bei Dichte 1/4 auf 89,9998697 % des N11-Erfolgs, bei der alten unteren Grenze 5,1179 % auf 89,8283435 %. Eine solche Aufteilung gehört auch zur vollen N14-Familie. Die zusätzlich untersuchte austauschsymmetrische Gewichtsvorschrift und die freie Gewichtsaufteilung des Gegenbeispiels sind getrennte Versuche.

129 zulässige N14-Typen haben bislang keine individuelle Uhr- und Detektorauswertung in diesem Paket. Das Inventar erfasst sie vollständig. Für den vollen Träger ist die erste Verletzung zwischen der allgemeinen unteren Schranke und dem berechneten Gegenbeispiel offen. Die Einfügungszahl bezeichnet die Grössenstufe einer endlichen Historienfamilie. Eine physikalische Wachstumsgewichtung oder Kollapsentwicklung ist weiterhin offen.

## Lokale Wiederholung

Das Paket enthält die 33 unveränderten Referenzdateien der verlinkten v0.4-Fassung unter `upstream/`. Die getestete Umgebung ist Python 3.12 mit den Versionen in `upstream/v03/upstream/requirements.txt`. Nach Bereitstellung der Abhängigkeiten genügt im entpackten Verzeichnis

```sh
python -B verify.py
```

Der Prüfer arbeitet lokal mit einem Thread für die numerischen Bibliotheken. Er kontrolliert die SHA-256-Prüfsummen, erstellt das vollständige Inventar erneut, prüft die rationalen Pfadzeugnisse und die analytische Schranke, berechnet die zehn Uhrintegrale und wiederholt beide Detektorvergleiche. Die neu berechneten Vorstufen werden an die jeweils nächste Rechnung weitergereicht. Die optionale erneute Suche nach einem symmetrischen Gewichtszeugen in `exchange.py --discover` benötigt zusätzlich SciPy.

| Datei | Inhalt |
|---|---|
| growth.json | Jede Eltern-Tochter-Multiplizität, skalare Einstufung und unabhängiger Rangtest |
| exchange.json, exchange_certificate.json | Symmetrische Pfadgewichte, N14-Marginalen und rationale Zeugnisse |
| clock14.json, clock14_extra.json | Uhrintegrale des ersten Achter-Satzes und der beiden Ergänzungen |
| readout14.json, readout14_extra.json | Auslese, erreichbare Träger, Gittervergleich, Gewichts- und Gegenbeispiele |
| analytic.json, Schranke.md | Allgemeine Schranken, N11-Eingangsprüfung und Herleitung |
