# CST-DUST · Zwei Einfügungen bei festem Rand (v0.3)

Die Studie setzt [PR #296](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/296) um einen Grössenschritt fort. Untersucht werden dieselben zwei Anfangshistorien, dieselben vier vergangenen und vier künftigen Randereignisse, dieselben Uhr- und Dichtepakete und die vier Ausgänge des q₇-Detektors. Erfolg umfasst links, Mitte oder rechts pro präpariertem Versuch. ΔP ist P(Erfolg bei 1/4) minus P(Erfolg bei 1/8). Alle Gewichtungen sind reelle nichtnegative Koeffizienten einer **kohärenten** Amplitudensumme. Eine Verteilung auf markierte Wege ist hier eine Zähl- und Gewichtskonvention.

## Vom ersten zum zweiten Zusatzereignis

In jedem Schritt wird die ursprüngliche Ordnung nach Löschen des letzten Ereignisses exakt wiederhergestellt. Die Einfügungsreihenfolge gibt die Reihenfolge dieser algebraischen Konstruktion an. Die beiden neuen Punkte dürfen auch unvergleichbar sein. Ihre Einfügung ist keine Evolution in Staubzeit. Gegenüber allen äusseren Randereignissen gelten dieselben Relationen wie für die früheren inneren Punkte.

| Ursprüngliche innere Ordnung | Markierte Zwei-Schritt-Wege | Zulässiger Zwischen- und Endtyp | Auch nach Vertauschen zulässig | Nur in der ersten Reihenfolge zulässig | Zulässige Endtypen über einen zulässigen Zwischenzustand |
|---|---:|---:|---:|---:|---:|
| Kette | 170 | 86 | 70 | 16 | 20 |
| Eine Kante | 238 | 102 | 72 | 30 | 22 |

Die 408 Wege führen zusammen auf 58 verschiedene Endgeometrien. Die exakte Rangprüfung ergibt 24 zulässige Endtypen. Davon sind 23 auf mindestens einem zulässigen Weg erreichbar. Typ 510 besteht die Endprüfung, aber bei beiden hier betrachteten Ausgangshistorien fehlt ein zulässiger Weg zu ihm. Der gemeinsame Auslesevertrag für sämtliche positiven Wege bleibt offen. Zum unabhängigen Zählvergleich werden alle transitiven Vorwärtsrelationen über fünf Punkte und ihre Beschriftungsorbits erzeugt. Es ergeben sich 4231 beschriftete Ordnungen in 63 Isomorphieklassen, einschliesslich der hier nicht erreichbaren Formen.

Die Typnummer ist die kleinste Bitmaske der Vorwärtsrelationen über alle topologischen Beschriftungen. Bit 0 bezeichnet das erste lexikografische Paar. In den markierten Weglisten entsprechen die lokalen Nummern 0–4 den physischen Knoten 4, 5, 6, 11, 12. Beispielsweise führt ein Weg aus der Kette über N12-Typ 63 zum zulässigen N13-Typ 255. Vertauscht man die Einfügungsmarken, erhält man denselben Endtyp über den ausgeschlossenen N12-Typ 31.

## Zwei gleiche Elterngewichte legen die Wege nicht fest

Jede ursprüngliche Historie behält den Gesamtkoeffizienten 1/2. Die folgenden Vergleiche sind je Elternhistorie auf eins normiert. Die erste Vorschrift verteilt das Gewicht zunächst gleich auf alle sieben zulässigen markierten N12-Einfügungen und dann gleich auf deren zulässige markierte N13-Fortsetzungen. Die zweite verteilt es gleich auf alle gemeinsam zulässigen vollständigen Wege in der vorgegebenen Einfügungsreihenfolge.

| Distanz in Totalvariation, auf den Koeffizienten gemessen | Kette | Eine Kante |
|---|---:|---:|
| Schrittweise Vorschrift gegen ihre eigene Markierungsvertauschung, auf den Wegen | 124/539 ≈ 23,01 % | 61/196 ≈ 31,12 % |
| Schrittweise gegen gleich gewichtete vollständige Wege, nach Zusammenfassen der Endtypen | 810/23177 ≈ 3,49 % | 46/2499 ≈ 1,84 % |
| Schrittweise gegen symmetrische Ergänzung, nach Zusammenfassen der Endtypen | 11348/83545 ≈ 13,58 % | 40/147 ≈ 27,21 % |

Die markierten Wege einer Vorschrift und ihre reine Umbenennung haben nach Vergessen der Markierungen stets dieselbe Endtypverteilung. Die zweite und dritte Tabellenzeile vergleichen tatsächlich verschiedene Gewichtsvorschriften. Sie beschreiben keine Detektorwahrscheinlichkeiten.

Auf den 70 beziehungsweise 72 beidseitig zulässigen Wegen lässt sich **exakt** eine vertauschungssymmetrische Vorschrift mit denselben sieben N12-Randgewichten je Elternhistorie konstruieren. Man bildet eine 7 × 7-Tabelle möglicher erster Einfügungen in den beiden Reihenfolgen. Für die Kette sind 47 Tabellenzellen besetzt, für die Einzelkante 49. Unter allen Permutationen der sieben Spalten werden jeweils 3720 beziehungsweise 5040 zulässige vollständige Zuordnungen gefunden. Jede besetzte Zelle kommt mindestens einmal vor. Der Mittelwert der Zuordnungsmatrizen, geteilt durch sieben, hat in jeder Zeile und Spalte Summe 1/7. Inverse Permutationen sichern die Symmetrie. Das Zellengewicht wird gleich auf seine zulässigen markierten Vervollständigungen verteilt. Jeder beidseitig zulässige Weg erhält positives Gewicht. Die Vorschrift ist eine mathematische Möglichkeit. Ihre vollständige dynamische Auslese und eine physikalische Auswahl sind offen.

## Gemeinsamer Drei-Stufen-Versuch

Der Träger wächst von zwei N11- auf zusätzlich fünf N12- und sieben berechnete N13-Typen. Alle 23 sequentiell zulässigen N13-Typen besitzen einen strukturell untersuchten Skalarzweig. Eine vollständige Uhrenintegration liegt für sieben vor. Zuerst werden alle fünf Typen berechnet, bei denen die exakte Umordnung der Summen maximal drei innere Uhrvariablen gleichzeitig benötigt. So bleiben zwei der fünf N12-Elterntypen ohne berechnete Tochter. Für diese werden vor Einsicht in die N13-Auslese zusätzlich die kleinsten zulässigen Typnummern mit Vier-Uhr-Kontraktion gewählt, N12-53 → N13-165 und N12-63 → N13-183. Damit hat jeder N12-Elterntyp mindestens eine berechnete Tochter. Weitere elf Typen mit vier und fünf Typen mit fünf simultanen Uhrvariablen bleiben dynamisch offen.

Die Ursprungsgewichte betragen je 1/2. Beide ursprünglichen Eltern geben denselben Anteil λ an die N12-Stufe ab. Auf der zweiten Stufe gibt jede N12-Historie den Anteil μ ihres eigenen Gewichts ab. Bei der Auswahl mit sieben N13-Typen beträgt das gesamte N13-Gewicht λμ. In der kleineren Fünferauswahl verbleibt ein Elternanteil vollständig auf N12, falls ihm eine berechnete Tochter fehlt. Die Ergebnisdatei weist das tatsächlich übertragene Gewicht aus. Die zwei Vergleichsvorschriften gewichten innerhalb jeder Faser entweder jede zulässige markierte Einfügung oder jeden unterschiedlichen berechneten Tochtertyp gleich. Die bedingte Renormierung über berechnete Typen ist ausdrücklich Teil dieses Versuchs.

| Stufenanteile (λ, μ) | ΔP in 10⁻⁶, gleiche Einfügungsgewichte | ΔP in 10⁻⁶, gleiche Typgewichte |
|---|---:|---:|
| (0, 0), N11-Referenz | −6,68047 | −6,68047 |
| (0,05, 0), kleine N12-Erweiterung | −6,03337 | −6,03669 |
| (0,05, 1), derselbe Anteil vollständig auf N13 | −6,03099 | −6,03009 |
| (1, 0), vollständiger Ersatz durch N12 | −0,80689 | −1,07733 |
| (1, 1), vollständiger Ersatz durch N13 | −0,61815 | −0,75218 |

Die unveränderten Toleranzen betragen pro Dichte 10 % der ursprünglichen Erfolgswahrscheinlichkeit als Totalvariationsabstand und 25 % relative Änderung des vorzeichenbehafteten vierteiligen Dichtekontrasts in halber L¹-Norm. Ausserdem muss das Vorzeichen von ΔP erhalten bleiben. Die Tabelle bezieht sich auf die kohärente Uhr. `nested_comparisons` enthält alle vier Ausgänge für fünf Präparationen und Vergleiche sowohl mit N11 als auch mit der unmittelbar vorhergehenden Mischung.

## Für alle Gewichte im berechneten Sektor

Bei **insgesamt höchstens 5 % abgegebenem N11-Gewicht**, zu gleichen Anteilen beider ursprünglicher Eltern, bleiben für jede erlaubte Aufteilung auf berechnete N12- und N13-Nachkommen alle drei Kriterien erfüllt. Dazu darf auch der ganze abgegebene Anteil bis N13 weiterlaufen. Das sind keine zusätzlichen fünf Prozent pro Stufe. Für die beiden ursprünglichen Eltern gibt es zusammen 99 Paare von möglichen Endpunkten, Zählung einschliesslich der N12-Zwischenstufe. Jede erreichbare Gewichtsaufteilung liegt in ihrer konvexen Hülle. Für w = (1−λ)b + λv wird die normierte Abweichung durch 2λ(1−λ)A + λ²B beschränkt. A wird über alle Eltern-Endpunkt-Kreuzterme und B über alle Endpunktpaare maximiert. Über das ganze genannte Intervall bleibt die Niveauabweichung unter 0,987 ihrer Toleranz und die Kontrastabweichung unter 0,394 ihrer Toleranz. Die ergänzende Berechnung auf beiden Gittern ergibt denselben auf ganze Promille abgerundeten Radius. Für jeden nichtverschwindenden reellen Gewichtsvektor auf den 14 berechneten Typen ist die Erfolgsänderung negativ. Die maximale Gershgorin-Obergrenze der symmetrischen Differenzmatrix beträgt −1,23528 × 10⁻⁶.

## Vollständiger Ersatz und Rückkehr in die Toleranzen

Werden die N12-Zwischengewichte der beiden veröffentlichten Standardvorschriften festgehalten, kann **keine** anschliessende Verteilung auf die sieben berechneten N13-Endtypen alle Kriterien erfüllen. Bei vollständigem Ersatz beträgt der Erfolg bei Dichte 1/8 höchstens 25,99 % beziehungsweise 33,87 % des ursprünglichen Erfolgs. Für das Niveaukriterium wären mindestens 90 % erforderlich, denn der Totalvariationsabstand ist mindestens die absolute Änderung der gesamten Erfolgswahrscheinlichkeit. Die Erfolgseffekte sind positiv, also ist der Erfolg konvex im Gewichtsvektor. Je Vorschrift genügen alle 30 deterministischen Tochterzuordnungen, um das Maximum zu begrenzen. Die Prüfung der positiven Definitheit sowie der Eckwerte verwendet exakte Brüche der numerischen Matrixeinträge.

Ein **nachträglich ausgewähltes Beispiel** erhält beide N11-Elterngewichte, wählt auf der Zwischenstufe aber 249/250 für Typ 11 und 1/250 für Typ 14. Die ganze Kettenhälfte läuft über Typ 11. Von der Einzelkantenhälfte laufen 62/125 über Typ 11 und 1/250 über Typ 14. Anschliessend geht Typ 11 vollständig in N13-Typ 184 und Typ 14 in N13-Typ 22 über. Es handelt sich um eine adaptiv gefundene, auf zwei Endtypen konzentrierte Verteilung mit Nullgewichten auf den übrigen Zweigen.

| Stufe dieser einen Gewichtung | ΔP in 10⁻⁶ | Niveauabweichung bei 1/8 und 1/4 | Kontraständerung | Kriterien |
|---|---:|---|---:|---|
| N12 | −3,80857 | 13,93 %, 14,41 % | 42,99 % | verfehlt |
| N13 | −5,57523 | 9,69 %, 9,75 % | 16,96 % | erfüllt |

Entlang dieser Zweitypenmischung liegt das numerisch bestimmte zulässige Endintervall bei rund **0,1474 % bis 0,7029 %** auf N13-Typ 22, der Rest liegt auf Typ 184. Die Grenzen werden durch alle Vorzeichenformen der L¹-Toleranzen bestimmt. Das Beispiel weist nach, dass ein einzelner passender Endpunkt nach einem zwischenzeitlichen Scheitern auftreten kann. Es begründet keine bevorzugte Dynamik.

## Daten, Rechenkosten und Reproduktion

`study.json` fixiert die Auswahl vor Zählung und Rechnung. `supplement.json` dokumentiert die nach der Zählung und vor der N13-Uhrenrechnung festgelegte Ergänzung. Die allgemeine Zwei-Schritt-Schranke und die Endpunktsuche sind ergänzende Diagnosen. Die Zeitfolge ist lokal dokumentiert, ohne externe Präregistrierung.

`results.json` enthält die genauen Ränge, alle 408 markierten Wege mit rationalen Koeffizienten, die beiden Gewichtskampagnen, die Vorzeichen- und Endpunktprüfungen. `clocks_n13.json` enthält die verfeinerten Uhrenintegrale. `upstream/ORIGIN.json` bindet elf unveränderte Eingabedateien an den vorherigen Git-Stand. Drei Python-Abhängigkeiten sind in `upstream/requirements.txt` festgelegt. Bei vorhandenen Abhängigkeiten wird im entpackten Verzeichnis lokal ausgeführt:

```sh
python -B verify.py
```

Bei Bedarf installiert `python -m pip install -r upstream/requirements.txt` die Abhängigkeiten in einer eigenen Python-Umgebung. Der Prüflauf kontrolliert die Prüfsummen, erzeugt neue Rechnungen in einem temporären Ordner und vergleicht alle Ergebnisse. Getestet mit Python 3.12, einem CPU-Thread und ohne externen Rechendienst. Die Quadraturen verwenden je nach Typ 32, 48 oder 64 Knoten pro innerer Uhr sowie 6, 8 oder 10 pro äusserem Uhrfenster. Die direkte fünfdimensionale Kontrollsumme bei vier Knoten pro Achse stimmt für alle sieben berechneten Typen auf besser als 1,5 × 10⁻¹⁵. Der grösste beobachtete Unterschied zwischen den letzten Effektmatrizen beträgt 2,56 × 10⁻¹⁴. Die unabhängige Abel-Kontrolle bei ε = 10⁻²⁸ ergibt Präzisions- und Phasenabweichungen unter 3,8 × 10⁻²². Die numerischen Integrale besitzen hier ein empirisches Fehlerbudget. Die Beschränkungen auf einen festen Rand, die ausgewerteten Geometrien und endliche Grösse gelten weiterhin.

[Publizierter Ausgangsversuch und Quellen auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/0bc355d124e7c451a9bcab6d5a409b50fea96057/research/rax_cqg/dust_collapse/extension_stability_v0_2)
