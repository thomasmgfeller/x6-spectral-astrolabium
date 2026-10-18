# Ergebnis: weniger Datenbedarf, erste abgesicherte Präzisionsfreigaben

Der vorab festgelegte Haupttest ist bestanden:
`TWO_FOLD_BUDGET_GAIN_CERTIFIED`. An allen drei festgelegten nichtnull
Krümmungen liegt der nachgewiesene Gewinn über dem verlangten Faktor zwei.
Die binäre KL-Schranke nutzt dieselbe C2-Beobachtung, denselben geometrischen
Nachweis und dieselbe Behandlung abhängiger Paare wie die Referenz.

## Hinreichende Entwurfsbudgets

Für die Planung ist der wahre Parameter jeweils vorgegeben. Das Budget
stellt unter den bekannten Modellannahmen sicher, dass Überdeckung und
20%-Präzisionsfreigabe gemeinsam mit mindestens 95% Wahrscheinlichkeit
erreicht werden. Die Zahlen bezeichnen unabhängige Wolken zu je 128 Punkten.

| Wahrer Parameter h | Bisherige Hoeffding-Regel | Neue KL-Regel | Verhältnis bisher / neu |
| --- | ---: | ---: | ---: |
| 0,1 | 161.627.557 | 58.253.604 | 2,775× |
| 0,25 | 4.066.682 | 1.474.733 | 2,758× |
| 0,5 | 85.871 | 31.707 | 2,708× |

Es sind **verfeinerte hinreichende Grenzen der beiden festgelegten
Zertifikatsverfahren**, keine statistisch optimalen oder notwendigen
Mindestzahlen. Die exakten Zertifikate bestehen beim angegebenen ganzzahligen
Budget und verfehlen die Vorgabe jeweils beim unmittelbar vorherigen Wert.
Die alte 2ε-Regel wird auf ganze Budgets verfeinert; ihr früheres grobes
Potenzen-von-vier-Gitter wird nicht als Minimum ausgegeben. Die grossen
Planungszahlen bei h=0,1 und 0,25 wurden nicht simuliert.

Die KL-Intervalle werden nach aussen mit rationalen Logarithmusgrenzen
berechnet. Die Pinsker-Ungleichung zeigt, dass ihre exakte Konfidenzmenge
bereits in der Hoeffding-Menge liegt. Die zusätzliche Schnittbildung mit dem
bisherigen ausgegebenen Intervall erhält deshalb die 95%-Absicherung ohne
weitere Fehleraufteilung. Die Wahrscheinlichkeit einer falschen
Präzisionsfreigabe ist modellbedingt bei festem Budget höchstens 5%; dies ist
keine bedingte 95%-Aussage unter ausgewählten Freigaben. Vollständige
Ableitung: [DERIVATION.md](DERIVATION.md).

## Neuer Lauf nach öffentlichem Prüfvertrag

Der öffentliche Quellenstand lautet
`09e0cf0802b3ab52ae18bd0e1a132befc914a42d`. Entwicklung und Kontrollen ausserhalb
des Zielgitters gingen der Fixierung voraus; Zielbudgets und neue Punktwolken
folgten danach. Der Lauf begann am **18.10.2026 um 10:39:17 UTC
(12:39:17 Zürich)**. Laufzeit: **81,38 Sekunden**; Spitzen-RSS: **83.156 KiB**
(plattformabhängig). Insgesamt **77.824 Wolken / 9.961.472 Ereignisse**.

Bei h=0; 0,1; 0,25 wurden jeweils 4.096 Wolken gerechnet. Feste Gruppen von
256 bzw. 4.096 Wolken: alle Intervalle beider Verfahren enthalten den
Modellwert, keine 20%-Präzisionsfreigabe. Bei h=0,5 wurden die vorab
festgelegten 65.536 Wolken in diese Gruppen gegliedert:

| Wolken pro Schätzung M | Gruppen | Hoeffding: 20%-Freigaben | KL: 20%-Freigaben | Überdeckung beobachtet |
| ---: | ---: | ---: | ---: | --- |
| 256 | 256 | 0 | 0 | alle, beide Verfahren |
| 4.096 | 16 | 0 | 1 | alle, beide Verfahren |
| 16.384 | 4 | 1 | 4 | alle, beide Verfahren |
| 65.536 | 1 | 1 | 1 | beide Einzelintervalle |

Kein ausgegebenes KL-Intervall ist breiter als seine Referenz. Es gab keinen
leeren Modellbereich und keine beobachtete Fehlfreigabe. Die Gruppen
verschiedener Budgets verwenden dieselben Wolken erneut: keine gepoolte
unabhängige Erfolgsquote. Vier Gruppen bei M=16.384 und ein Intervall bei
M=65.536 erlauben keine präzise Schätzung einer Erfolgswahrscheinlichkeit.

Die relativen Radien bei h=0,5, M=16.384 liegen mit KL zwischen **9,75% und
13,62%**, mit Hoeffding zwischen **19,56% und 24,17%**. Im vollständigen
M=65.536-Datensatz ergeben sich:

| Methode | q-Intervall, gerundet | Relativer Radius |
| --- | --- | ---: |
| Hoeffding | [2,605757; 3,131314] | 9,16% |
| KL | [2,839543; 3,131314] | 4,89% |

Der wahre Modellwert ist q≈3,131314. Die obere Grenze h≤0,5 war vorab fest
und hilft an dieser Prüfstelle bei der Präzision. Die Ergebnisse gelten
nicht automatisch für einen erweiterten Parameterbereich. Dass einzelne
beobachtete Intervalle schon unter dem hinreichenden Entwurfsbudget
qualifizieren, widerspricht dessen konservativer Worst-Case-Planung nicht.

## Kontrollen und bleibende Grenzen

Die gesamte Kampagne wurde aus den fixierten Zufallsstarts mit einem
getrennten Kausalitätsprädikat reproduziert. C2-Zählungen, Relationshashes,
alle rationalen Intervallentscheide und die Budgetplanung stimmen überein:
`PASS_FULL_KL_REPLAY`. Acht Logarithmus- und 15 KL-Einschliessungen wurden mit
90-stelliger getrennter Rechnung geprüft; die Quellen sind bytegleich zum
öffentlichen Prüfstand. Diese interne Gegenprüfung ist keine externe Replikation.

Ein exakt ausgewerteter binärer abhängiger Paarkern mit N=64 liefert bei
korrektem effektiven Umfang floor(N/2) eine Überdeckung von **99,9180%**.
Die unzulässige Annahme unabhängiger aller choose(N,2) Paare erreicht nur
**29,2019%**. Eine weitere exakte Faltung dreier unabhängiger Wolken mit N=8
ergibt **99,8450%**. Die Kontrollen illustrieren die notwendige Behandlung
der Abhängigkeit; sie ersetzen nicht den allgemeinen Beweis.

Der flache Dichtezwilling behält dieselben kausalen Relationen. Bei h=0,5
schliesst das enge uniforme Modellintervall q=0 aus, obwohl dieser Zwilling
als anderes Dichtemodell möglich bleibt. Er wird ausdrücklich als
`OUTSIDE_UNIFORM_DENSITY_ASSUMPTION` geführt. Das ist **keine Identifikation
von Krümmung bei unbekannter Dichte**. Absolute R-Werte benötigen zusätzlich
eine unabhängige Zeitskala T. Optionales Stoppen ist nicht abgesichert.

## Dienlicher nächster Schritt

Jetzt ist eine externe Prüfung der Herleitung und eine Replikation sinnvoll,
besonders der uniformen Geometrie, der KL-Umkehrung und der Entwurfszertifikate.
Für weitere Effizienzarbeit sollte zuerst ein analytischer Umgang mit der
U-Statistik-Varianz gegen diese eingefrorene KL-Referenz geprüft werden.
Eine solche datenabhängige Schranke braucht einen eigenen vorab fixierten
Vertrag und eine endliche Absicherung; die bisher negative Informationsstudie
bleibt unverändert. Bei h=0,1 bleibt der konservative Datenbedarf hoch.
Zusätzliche Grossläufe ohne belegten Gewinn sind derzeit nicht begründet.
