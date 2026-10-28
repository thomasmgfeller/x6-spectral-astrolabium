# Ergebnisse: nichtlokaler Anfangsdatenadapter v0.11

**Status: METHOD_HOLD.** Konstruktion und Fehlerrechnung sind prüfbar; die geforderte Genauigkeit ist nicht qualifiziert.

## Geprüfter Umfang

- 12 analytische Tests bestanden.
- 9.720 eingeschlossene Zielgrößen zwischen 128 und 192 Bit verglichen; alle überlappen.
- Dieselben acht Archivwolken; keine neuen Kausalsetknoten oder Zufallswolken.
- Alle acht Tetraederzerlegungen rational zertifiziert; alle acht Projektionsgebiete enthalten die ursprüngliche Quellkugel.
- Die exakte Projektion löscht die kompakte Quelle in keiner der acht Wolken vollständig aus. Das schließt d0_r01, d0_r04 und d0_r06 mit zuvor leerer lokaler Quellhistory ein.
- Dieser Nichtauslöschungsnachweis folgt aus Integralbewahrung und dem positiven Quellintegral. Er ist kein Nachweis einer von null verschiedenen Detektorantwort.

## Räumlicher Fehler der unveränderten Wellen

Relative L2-Projektionsfehler auf dem jeweiligen konvexen Projektionsgebiet D. Die Dezimalwerte sind gerundete Anzeigen; vollständige Ballintervalle stehen in den Rohdaten. Da die Projektion L2-optimal ist, sind diese Fehler zugleich die beste erreichbare Genauigkeit im hier festgelegten kontinuierlichen P1-Raum.

| Wolke | History-Knoten | Tetraeder | k=2 | k=4 | k=8 |
|---|---:|---:|---:|---:|---:|
| d0_r00 | 75 | 365 | 35.028 % | 80.003 % | 98.593 % |
| d0_r01 | 89 | 446 | 31.143 % | 77.263 % | 98.937 % |
| d0_r02 | 57 | 269 | 32.664 % | 78.320 % | 99.203 % |
| d0_r03 | 86 | 433 | 25.568 % | 73.344 % | 98.891 % |
| d0_r04 | 85 | 422 | 28.952 % | 76.692 % | 98.982 % |
| d0_r05 | 72 | 360 | 31.580 % | 80.055 % | 99.102 % |
| d0_r06 | 87 | 427 | 28.280 % | 76.981 % | 98.897 % |
| d0_r07 | 73 | 357 | 23.669 % | 71.203 % | 99.155 % |

Alle 24 nichtkonstanten Wellenfälle überschreiten die festgelegte relative Toleranz 0.001 nachweislich. Die acht konstanten Felder werden mathematisch exakt reproduziert und bestehen die numerische Prüfung. Die hier verwendete Partition der Eins allein bietet also keine ausreichende Wellenauflösung. Diese Aussage betrifft genau diesen P1-Raum, nicht jede denkbare nichtlokale Abbildung.

## Kompakte Quelle und zeitliche History

Für die acht kompakten räumlichen Projektionsfehler liefern die festen Unterteilungstiefen 0, 2 und 4 noch keine entscheidenden Grenzen. Nach Schnitt mit der allgemeinen Projektionsschranke bleibt jeweils im Wesentlichen das zulässige relative Intervall [0,1]. Dies ist fehlende Genauigkeitsqualifikation; daraus folgt keine positive Fehleruntergrenze für die kompakte Quelle.

Auf allen Archivknoten wird ausdrücklich H1 = P f + (t+1) P g verwendet. Allgemeine höhere History-Polynome und ihre Reste sind hergeleitet und als Funktion verfügbar; sie wurden nicht als weitere Archivmethoden getestet. Die kompakte Historygrenze benutzt die konservative globale KG-Restschranke des Vorgängers. Wellen werden direkt mit ihrer exakten Kontinuumshistory verglichen.

| Prüfpunkt | Bestanden | Bedeutung |
|---|---:|---|
| Räumliche Projektionsbudgets | 8/40 | Acht Konstanten; 24 belegte Überschreitungen; acht kompakte Fälle unentschieden |
| Historyfehler bis zum Detektor | 0/80 | Kein Anfangsdatenbudget qualifiziert |
| Kombinierter Integrationsradius | 0/80 | Bestehende Transferintervalle plus neue Lastintegration bleiben zu breit |

Auch das exakte Erhalten von Konstanten auf der Anfangsfläche macht die lineare History nicht zur exakten massiven Zeitentwicklung. Die null bestandenen Historybudgets sind konservative Budgetentscheidungen; sie sind nicht 80 gemessene Fehleruntergrenzen.

## Stabilität und Aussagegrenzen

Die berechneten oberen Schranken für die spektrale Konditionszahl der Massenmatrix liegen zwischen 36.427 und 93.258. Die ideale Projektion ist L2-kontraktiv. Nodal- und Detektornormen sind separat eingeschlossen; daraus folgt keine universelle zeitliche Stabilität des nichtlokalen Operators.

Die Vorgeschichte wird gegenüber der ausdrücklich angenommenen freien KG-Cauchyfortsetzung kontrolliert. Eine solche History folgt nicht allein aus f,g für einen beliebigen retardierten nichtlokalen Operator. Die geometrische Konstruktion nutzt außerdem die vorhandenen Raumkoordinaten und ist nicht intrinsisch aus der Kausalordnung gewonnen.

G1 bleibt HOLD. Eine vollständige kompakte Kontinuumsdetektorreferenz, die Operator-/Gebietsqualifikation, physikalische Rauschinterpretation und Dirac-Freigabe sind nicht Bestandteil dieses Ergebnisses.

## Reproduzierbarkeit

Die vollständige Herleitung steht in README.md, der ausführbare Adapter in adapter.py, der Archivlauf in run.py und die unabhängige Ausgabekontrolle in verify.py. Die endgültigen Läufe verwendeten Python-FLINT 0.9.0, NumPy 2.3.5 und SciPy 1.17.0. Beide Präzisionsläufe benötigten hier jeweils weniger als eine Minute. Ein Leistungsbenchmark wird daraus nicht abgeleitet.

Der Methodenstand ist lokal gehasht, jedoch nicht öffentlich vorregistriert. Vorläufige Ergebnisse einer zu breiten reinen Wertebereichsintegration bleiben in development_draft/ dokumentiert. Die endgültige Wellenintegration nutzt analytische Simplexmomente mit bewiesenem Rest. Daten und Toleranzen wurden nicht nachgezogen.
