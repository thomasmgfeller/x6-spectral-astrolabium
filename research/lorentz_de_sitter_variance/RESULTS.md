# Ergebnis: analytische Varianz senkt hinreichende Budgets weiter

Der vorab festgelegte Haupttest ist bestanden:
`TWO_FOLD_VARIANCE_GAIN_CERTIFIED`. Gegenüber der unveränderten KL-Referenz
sinkt das hinreichende Budget an allen drei vorgegebenen Krümmungen um mehr
als den geforderten Faktor zwei. Die methodische Änderung nutzt eine
analytische Varianzgrenze ganzer Wolken, keine als sicher behandelte
Stichprobenvarianz.

## Mathematischer Fortschritt

Für den binären Vergleichbarkeitskern g gilt p=E g(X,Y) und
w=E[g(X,Y)g(X,Z)]. Der gemeinsame Punkt X verursacht die wesentliche
Abhängigkeit. Für N iid Punkte ergibt sich exakt

    Var(U) = [2p(1−p)+4(N−2)(w−p²)]/[N(N−1)], U=C2/choose(N,2).

Bedingte Intervallvolumina werden durch Lorentztransformierte Polynommomente
integriert. Eine rationale Reihe bis h-Grad 16 und eine uniforme Restschranke
schliessen w ein. 64 vollständige Parameterzellen liefern für N=128 auf
**ganz 0≤h≤0,5** die obere Grenze **Var(U)≤0,000338822592**. Es handelt sich
nicht um eine Interpolation zwischen 64 numerisch getesteten Punkten.
Der flache Referenzwert ist exakt w(0)=1/50.

Das Bennett-Argument arbeitet mit M unabhängigen ganzen Wolken. Die
rationale Inversion seiner Exponentialschranke liefert zusammen mit der
unveränderten geometrischen Umkehrung mindestens 95% Überdeckung bei festem
Budget. Die neue Varianzgrenze ist modellbedingt; sie darf nicht auf einen
anderen Dichteerzeuger übertragen werden. Die vollständigen Rechnungen und
Geltungsbedingungen stehen in [DERIVATION.md](DERIVATION.md).

## Vorab festgelegter Budgetvergleich

| Wahrer h-Wert | KL: hinreichende Wolken | Bennett: hinreichende Wolken | Verhältnis KL / Bennett |
| --- | ---: | ---: | ---: |
| 0,1 | 58.253.604 | 14.202.354 | 4,102× |
| 0,25 | 1.474.733 | 380.869 | 3,872× |
| 0,5 | 31.707 | 10.981 | 2,887× |

Alle Wolken enthalten 128 Punkte. Für die Planung ist der wahre Parameter
vorgegeben. Die jeweilige 2ε- bzw. KL-Planung stellt sicher, dass Überdeckung
und relative 20%-Präzisionsfreigabe bei diesem festen Budget gemeinsam mit
mindestens 95% Wahrscheinlichkeit erreicht werden.

Die ganzzahligen Grenzen bestehen das exakte Zertifikat; der unmittelbar
vorherige Wert verfehlt die Vorgabe. Es sind **hinreichende Grenzen der
festgelegten Verfahren**, keine notwendigen oder statistisch optimalen
Mindestzahlen. Die grossen Planungszahlen bei h=0,1 und 0,25 wurden nicht
simuliert. Auch 14,2 Millionen Wolken bei kleiner Krümmung bleiben teuer.

## Neue Daten nach öffentlicher Quellenfixierung

Quellenstand vor Zielbudgetrechnung und neuer Simulation:
`b51933763dd414c160b05042fd32e9976d8fa47a`. Historische KL-Daten wurden nur
während der Methodenentwicklung zur Betrachtung der Wolkenstreuung genutzt.
Die neue Absicherung selbst stammt aus der analytischen Rechnung.

Der neue Lauf startete am **18.10.2026 um 11:42:21 UTC (13:42:21 Zürich)**
und dauerte **57,94 Sekunden**. Spitzen-RSS: **80.144 KiB**, plattformabhängig.
Nach bestandenem Haupttest wurden genau **45.056 Wolken / 5.767.168 Ereignisse**
gerechnet: je 4.096 Wolken bei h=0; 0,1; 0,25 und 32.768 bei h=0,5.

Bei den drei kleineren h-Werten enthalten alle Intervalle beider Verfahren
den Modellwert; bei Gruppen von 256 und 4.096 Wolken gibt es keine
20%-Freigaben. Bei h=0,5 ergeben sich:

| Wolken je Schätzung M | Getrennte Gruppen | KL: 20%-Freigaben | Bennett: 20%-Freigaben |
| ---: | ---: | ---: | ---: |
| 256 | 128 | 0 | 0 |
| 4.096 | 8 | 0 | 5 |
| 8.192 | 4 | 3 | 4 |
| 16.384 | 2 | 2 | 2 |
| 32.768 | 1 | 1 | 1 |

Alle geprüften Intervalle enthalten den jeweiligen Modellwert. Es gab keine
beobachtete Fehlfreigabe und keinen ausgeschlossenen Modellbereich. Die
Gruppengrössen verwenden dieselben Wolken erneut; sie werden nicht zu einer
unabhängigen Erfolgsquote gepoolt. Insbesondere vier oder acht Gruppen sind
keine präzise Schätzung einer Populationswahrscheinlichkeit.

Bei M=8.192 liegen die relativen Radien mit Bennett zwischen **9,88% und
12,14%**, mit KL zwischen **18,32% und 20,93%**. Im gesamten M=32.768-Datensatz:

| Methode | q-Intervall, gerundet | Relativer Radius |
| --- | --- | ---: |
| KL | [2,620486; 3,131314] | 8,88% |
| Bennett | [2,853590; 3,131314] | 4,64% |

Der wahre Wert ist q≈3,131314. Die feste obere Modellgrenze hilft hier bei
der Präzision. Eine relative Präzisionsfreigabe betrifft den harmonischen
Mittelpunkt des Intervalls; die Überdeckung ist keine bedingte 95%-Aussage
nur unter ausgewählten Freigaben.

## Erhaltenes Gegenbeispiel zur allgemeinen Dominanz

Bei h=0,5, M=256, Gruppe 47 (nullbasiert), C2-Summe 221.597, ergibt Bennett
den gesamten h-Bereich [0; 0,5], während KL eine positive Untergrenze hat.
Das neue Intervall ist dort breiter. Alle übrigen geprüften Bennett-Intervalle
liegen im jeweiligen KL-Intervall; daraus wird kein allgemeiner Satz gemacht.

Die beiden 95%-Intervalle werden **nicht nachträglich geschnitten oder nach
beobachteter Breite ausgewählt**. Dafür wäre ein zusätzlicher Nachweis oder
eine Fehleraufteilung nötig. Der belegte Hauptgewinn betrifft die hinreichenden
Budgets der festgelegten Verfahren, nicht universelle Dominanz jeder Ausgabe.

## Prüfpaket und weitere Grenzen

[REVIEW.md](REVIEW.md) benennt die entscheidenden Beweisstellen,
Falsifikationsmöglichkeiten und Reproduktionsbefehle. Die interne Gegenprüfung
verwendet symbolische Momente, eine getrennte geometrische Kugelschnitt-
Quadratur und exakte endliche Kontrollen. Sie prüft insbesondere falsche
Paarunabhängigkeit, eine ungesicherte Nullvarianz und duplizierte Wolken.
Der vollständige Replay kontrolliert zusätzlich jede neue Punktwolke,
jeden Relationshash sowie alle Intervall- und Budgetentscheide.

Die externe Prüfung und Replikation bleiben offen. Eine flache Geometrie
mit anderer Dichte kann dieselben Kausalrelationen besitzen; das neue enge
Intervall widerlegt diesen Dichtezwilling nicht. Er wird ausdrücklich als
`OUTSIDE_UNIFORM_DENSITY_ASSUMPTION` geführt. Absolute Krümmung benötigt
zusätzlich eine unabhängige Zeitskala. Freies Nachschauen und Stoppen sind
nicht abgesichert. Frühere negative Forschungsresultate bleiben unverändert.

Als nächster fachlicher Schritt ist jetzt die explizite Empfindlichkeit
gegenüber begrenzten Dichte- und Zeitskalenfehlern sinnvoll: Unter welchen
zusätzlichen Kenntnissen bleibt eine Präzisionsfreigabe überhaupt möglich?
Ein engeres statistisches Intervall allein löst diese Identifizierbarkeitsfrage
nicht. Das Prüfpaket ermöglicht parallel eine externe Kontrolle des erreichten
mathematischen Referenzstands.
