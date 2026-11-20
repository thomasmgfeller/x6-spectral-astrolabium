# CST-DUST · Neun freie Gewichtsrichtungen am Präfix 1564

20. November 2026. Dieses Paket prüft, wie viele Informationen für die Auswahl der **gesamten** lokalen Fortsetzung fehlen. Am markierten N13-Präfix 1564 sind alle neun normierungserhaltenden Richtungen der zehn bedingten linearen Amplitudenkoeffizienten lokal frei. Das gilt auf dem veröffentlichten endlichen Träger unter Erhaltung der vollständigen N13-Marginale und der Austauschbarkeit der drei Einfügungsmarken. Eine physikalische Gewichtsregel bleibt offen.

## Voraussetzungen und Rechnung

Für jeden unter den sechs Markenumbenennungen zulässigen Orbit o sei x(o) der reelle Koeffizient **pro markiertem Pfad**. M(p,o) zählt dessen Pfade mit markiertem Präfix p. Die archivierte Verteilung b verlangt Mx = b. Sie enthält bereits die Normierung. Eine zulässige Gewichtsänderung erfüllt daher Mδx = 0. Die archivierte Lösung ist auf allen zugelassenen Pfaden strikt positiv. Der Prüfer rekonstruiert sie aus ihrem Gleichverteilungsanteil und Rest und vergleicht jede einzelne Komponente von Mx mit b.

Für p = 1564 zählt B(j,o) die Pfade desselben Orbits, die an diesem Präfix den Endtyp j erreichen. Der Vektor der bedingten Koeffizienten ist q = Bx/b(p), wobei b(p) = 1/147. Die Dimension seiner möglichen Änderungen ist der Rang der übereinander angeordneten Matrizen M und B abzüglich des Rangs von M. Wegen der strikt positiven Ausgangslösung sind hinreichend kleine Änderungen mit beiden Vorzeichen zulässig.

| N11-Elternordnung | Orbitvariablen | Rang M | Freie Dimensionen bei fester Marginale |
| --- | ---: | ---: | ---: |
| Kette | 154 | 35 | 119 |
| Eine Kante | 191 | 38 | 153 |

Am Präfix 1564 in der Ein-Kanten-Familie führen 16 markierte Pfade zu zehn Endtypen. Der gemeinsame Rang von M und B ist 47. Damit beträgt die Dimension der möglichen lokalen Gewichtsänderungen exakt 47 − 38 = 9. Die Summe der zehn Koeffizienten ist eins, also ist neun zugleich die grösstmögliche Dimension. Die Tabelle präzisiert die in der Studie zur Erweiterungsstabilität v0.5 veröffentlichten Dimensionsuntergrenzen für die zwei vollständigen Träger.

## Neun explizite Gegenproben

In certificate.json steht für jeden der neun anderen Endtypen j eine rationale Änderung des ursprünglichen markierten Pfadgewichts. Sie erzeugt bei p = 1564 exakt die Änderung e_j − e_1790 der bedingten Koeffizienten, gemessen pro Einheit des Schrittparameters. Alle anderen lokalen Koeffizienten sind dabei konstant. Für jeden der neun Versuche einzeln bleiben bei beiden Schritten +1/36 und −1/36 sämtliche Pfadgewichte strikt positiv. An anderen Präfixen dürfen sich die **bedingten Fortsetzungen** ändern. Die **Masse jedes N13-Präfixes** bleibt exakt erhalten.

Jede Gegenprobe benennt die markierten Orbits, deren Koeffizienten sich ändern. Der A/B-Tausch der früheren Studie ist in dieser lokalen Basis der Transfer von 1790 nach 5374. Eine skalare, reguläre lineare Bedingung genügt bei bekannter nichtverschwindender Empfindlichkeit für diesen isolierten Parameter. Für eine lineare Identifikation aller zehn Koeffizienten ist auf der vollständigen lokalen Familie Rang neun erforderlich. Eine strukturierte mikroskopische Theorie kann mehrere solcher Bedingungen gleichzeitig liefern. Ein einzelnes physikalisches Observable kann auch dann vorhersagbar sein, wenn seine Variation entlang der verbleibenden freien Richtungen verschwindet.

Die Aussage betrifft eine Umgebung des publizierten positiven Zeugen. Ob jeder Punkt des gesamten Zehner-Simplex erreichbar ist, wird hier offengelassen. Die Rechnung verwendet weder einen Detektor noch neue Uhrenintegrale und trifft keine Entscheidung über Dekohärenz, physikalische Randnorm, Korrespondenz oder den Ausgang des Kollapses.

## Nachrechnen

Das ZIP entpacken und im entpackten Verzeichnis ausführen. Der erste Prüfer benötigt nur die Python-Standardbibliothek. Er kontrolliert den Hash des Originalpakets, dekodiert die in den Gegenproben genutzten Orbits, prüft beide Vorzeichen und vergleicht die neun lokalen Änderungen mit ihren Sollvektoren.

~~~sh
python3 verify_moves.py
~~~

Für die vollständige Neukonstruktion mit exakter Rangrechnung wird zusätzlich SymPy benötigt. Die Fassung wurde mit SymPy 1.14.0 geprüft.

~~~sh
python3 check.py CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip > replay.json
~~~

replay.json lässt sich nach dem Einlesen als JSON mit certificate.json vergleichen. check.py enumeriert alle markierten Pfade beider Träger, bildet die ganzzahligen Rangmatrizen und berechnet die neun rationalen Zeugen. verify_moves.py verwendet keine Funktionen aus check.py.

## Herkunft

Das enthaltene Original-Prüfpaket aus PR 326 ist unverändert. Seine Lizenz- und Herkunftsangaben stehen im inneren ZIP. Der SHA-256-Wert lautet `4a2b985578e9bf41662af0dede7c2054c8406de4f49d077891f505b0fffd917e`. Die zusätzliche Rangrechnung und die expliziten Verschiebungen stammen vom 20. November 2026.

[Originalstudie am fixierten Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/1638acd19961c840fb0b3d35135a947e4dba0f4e/research/rax_cqg/dust_collapse/prefix_1564_selection_v0_1) · [Erweiterungsstabilität v0.5](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/1638acd19961c840fb0b3d35135a947e4dba0f4e/research/rax_cqg/dust_collapse/extension_stability_v0_5)
