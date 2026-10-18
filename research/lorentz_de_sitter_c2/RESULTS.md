# Ergebnis: Überdeckung abgesichert, Präzision weiterhin begrenzt

Die neue Stufe schliesst zwei Lücken des vorherigen Versuchs: Die vollständige
geometrische Paarwahrscheinlichkeit wird mit einem expliziten Restfehler
berechnet, und die statistische Schranke berücksichtigt abhängige Paare.
Damit gibt es **modellbedingt mindestens 95% Überdeckung für jedes feste
Datenbudget**. Die Intervalle sind jedoch noch zu breit für eine praktisch
präzise Krümmungsrekonstruktion mit den ausgeführten Budgets.

## Was mathematisch abgesichert ist

Auf dem vorab festgelegten Bereich 0≤h≤0,5 gilt für die bekannte uniforme
de-Sitter-Familie:

| Gegenstand | Ergebnis |
| --- | --- |
| Vollständige C2-Vorwärtsfunktion | Rationale Reihenrechnung mit begrenztem Rest, keine lokale lineare Krümmungsnäherung |
| Breite der Wahrscheinlichkeits-Einschliessung | Gleichmässig höchstens 1,67334·10⁻¹⁴ |
| Monotonie | Rationale untere Grenze >0,0533333333309 für N′V−2NV′ auf z=h²/4∈[0,1/16] |
| Getrennte geometrische Quadratur | Maximale Abweichung 2,53·10⁻¹⁶ an 21 vorab festgelegten Stellen |
| Endliche Überdeckung | Mindestens 95% bei bekanntem Modell, unabhängigen gleichartigen Wolken und festem Budget |
| Präzisionsfreigabe | Nur bei nichtleerem q-Intervall mit positiver Untergrenze und relativem Radius ≤20% |

Die Monotonie folgt aus einer exakten rationalen Ungleichung über das ganze
Intervall. Die 21 Quadraturpunkte sind eine zusätzliche Gegenprüfung und
ersetzen diesen Nachweis nicht. Dezimalzahlen in dieser Tabelle sind gerundete
Anzeigen; die gespeicherten Brüche sind für die Zertifikate massgeblich.

Für M unabhängige Wolken mit je N Punkten wird Ubar, der Mittelwert von
C2/choose(N,2), mit ε≥sqrt(3,69/[2M floor(N/2)]) abgesichert. Die Kettenpaare
innerhalb einer Wolke sind dabei abhängig. Die geometrische Umkehrung und
die Umrechnung zu q=R T² erfolgen nach aussen gerundet mit rationalen Zahlen.
Eine Fehlfreigabe hat unter den Annahmen bei festem M höchstens 5%
Wahrscheinlichkeit; dies ist keine bedingte 95%-Aussage nur unter den
ausgewählten Präzisionsfreigaben. Herleitung und Beweis stehen vollständig
in [DERIVATION.md](DERIVATION.md).

## Neuer Lauf nach öffentlicher Quellenfixierung

Quellen und Prüfvertrag wurden vor dem ersten Ziellauf unter
`c2f165953b846c69f1a23f641639cc0a3c4cdf25` veröffentlicht. Die mathematische
Entwicklung und Tests ausserhalb des Zielgitters lagen vor dieser Fixierung;
die Zielgitterauswertung und neuen Punktwolken folgten danach.

Der Lauf begann am **18.10.2026 um 09:42:13 UTC (11:42:13 Zürich)** und endete
nach 14,99 Sekunden. Spitzen-RSS: 73.760 KiB, plattformabhängig gemessen.
Vier Parameterwerte h=0; 0,1; 0,25; 0,5 mit je 4.096 neuen unabhängigen
Wolken zu 128 Punkten ergeben **16.384 Wolken / 2.097.152 Ereignisse**.

Je Parameterwert wurden diese Wolken in feste Gruppen aufgeteilt:

| Wolken pro Schätzung M | Getrennte Gruppen je h | Überdeckung beobachtet | 20%-Präzisionsfreigaben |
| ---: | ---: | --- | ---: |
| 1 | 4.096 | alle, bei jedem der vier h-Werte | 0 |
| 16 | 256 | alle, bei jedem der vier h-Werte | 0 |
| 256 | 16 | alle, bei jedem der vier h-Werte | 0 |
| 4.096 | 1 | alle vier Einzelintervalle enthalten ihren Modellwert | 0 |

Die Gruppen verschiedener Budgets verwenden dieselben Wolken erneut. Sie
sind über die Budgets hinweg nicht unabhängig; aus den Zeilen wird keine
gemeinsame unabhängige Erfolgsquote gebildet. Insbesondere liefern vier
Einzelintervalle bei M=4.096 keine präzise empirische Überdeckungsrate.
Die Garantie folgt aus dem endlichen Konzentrationsargument und der
kontrollierten Umkehrung, nicht aus den beobachteten 100%.

Bei h=0,5 und M=4.096 ergibt sich etwa
**q∈[0,842844; 3,131314]**, bei wahrem q=3,131314. Der relative Radius des
harmonischen Mittelpunkts beträgt **57,58%**. Die 20%-Freigabe wird deshalb
verweigert. Bei den drei kleineren h-Werten schliesst das Intervall q=0 ein;
eine relative Präzisionsfreigabe ist ebenfalls nicht möglich.

## Wie teuer ist diese konservative Garantie?

Die folgende Planung erweitert die eingeschlossene wahre Paarwahrscheinlichkeit
um **2ε** und prüft das grösste mögliche Intervall auf dem Überdeckungsereignis.
Wenn dieses die 20%-Vorgabe erfüllt, sind Überdeckung und Präzisionsfreigabe
bei festem Budget gemeinsam mit mindestens 95% Wahrscheinlichkeit abgesichert.

| Festgelegter wahrer h-Wert | q=R T² ungefähr | Erster ausreichender Gitterwert: unabhängige Wolken à 128 Punkte |
| --- | ---: | ---: |
| 0 | 0 | keine relative Präzisionsvorgabe möglich |
| 0,1 | 0,120200 | 268.435.456 |
| 0,25 | 0,757907 | 4.194.304 |
| 0,5 | 3,131314 | 262.144 |

Das Gitter enthält die Potenzen von vier von 1 bis 268.435.456. Die Zahlen
sind **hinreichende Entwurfsbudgets**, keine notwendigen oder optimalen
Mindestzahlen. Die wahre Krümmung ist hier zur Planung vorgegeben; sie wird
nicht aus denselben Daten gewählt. Diese grossen Wolkenzahlen wurden nicht
simuliert. Bei h=0,5 hilft zusätzlich die vorab festgelegte obere Modellgrenze;
das Ergebnis lässt sich nicht auf einen erweiterten Bereich übertragen.

Die viel kleineren Zahlen der Vorgängerstudie waren Normalapproximationen
für Zufallsstreuung. Die vorliegende allgemeinere endliche Absicherung ist
bewusst konservativ. Der Unterschied ist kein nachgewiesener intrinsischer
Informationsverlust und kein Anlass, diese grossen Läufe sofort zu starten.

## Kontrollen und verbleibende Grenzen

Eine exakte Gegenkontrolle mit einem binären Paarkern demonstriert den
Abhängigkeitsfehler: Bei N=128 erreicht die unzulässige Behandlung aller
8.128 Paare als unabhängig nur **27,5146% Überdeckung**. Die korrekte
Schranke erreicht im selben Beispiel **99,9742%**. Dies ist ein analytischer
Bernoulli-Gegenfall, keine Überdeckungszahl der de-Sitter-Simulation.

SymPy bestätigt die räumliche Integralidentität und 24 Monomialintegrale
einschliesslich hoher Grade exakt. Alle 16.384 Relationen werden aus den
festgelegten Zufallsstarts mit einem zweiten Kausalitätstest reproduziert;
C2-Zahlen, Intervalle, Zertifikate und Budgetentscheidungen werden vollständig
nachgerechnet. Alle Originalausgaben sind gehasht. Das ist interne
Softwareverifikation, keine externe wissenschaftliche Replikation.

Die Gültigkeit setzt uniforme physische Volumendichte voraus. Dieselben
Relationen lassen sich weiterhin als flache Geometrie mit nichtuniformer
Dichte lesen. Die zugehörigen Gegenfälle werden als ausserhalb der Annahmen
gekennzeichnet; aus einem solchen Datenbild darf nicht eindeutig auf Krümmung
geschlossen werden. Absolute R-Werte benötigen zusätzlich eine unabhängige
Zeitskala T. Optionales Stoppen, überlappende Wolken oder unbekannte
Erfassungsfehler sind nicht durch den vorliegenden Satz abgesichert.

## Entscheidung für die Weiterentwicklung

**Keine grossen zusätzlichen Simulationsläufe.** Die geometrische Lücke ist
im festgelegten Modell geschlossen; die nun sichtbare Hürde ist die Breite
der konservativen statistischen Schranke. Der nächste begrenzte Versuch
sollte eine schärfere, weiterhin endlich gültige Schranke für binäre
U-Statistiken mit der jetzigen Referenz vergleichen. Abbruchkriterium:
keine Übernahme, wenn die bewiesene Überdeckung oder die Berücksichtigung
der Paarabhängigkeit verloren geht. Die bestehende Rechnung bleibt dabei
als konservative Vergleichsreferenz erhalten.

Parallel bleiben ein externer Beweis-/Reproduktionsaudit und eine konkrete,
unabhängig begründete Dichte-/Erfassungsannahme nötig. Der Browserdemonstrator
behält seine bisherige flache Referenz; keine neue Uhrfreigabe.
