# N22 · Quellenvergleich bei gleichen Daten vor dem Sender

Für die Anbindung 216141 / 229383 / 0 / + unterscheidet die Uhr 21 drei Quellen an 16 auch dann, wenn die Uhren und Staubgewichte im strikten Sendervorlauf und die vier frühen Uhrimpulse exakt übereinstimmen. Dies gelingt in einer gemischten stationären Randaufgabe, in der zwei Zukunftsuhren und drei Zukunftsgewichte mitbestimmt werden. Eine Folge physischer Messungen mit frei schaltbarem Sender bleibt offen. Grundlage ist [PR 408](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/408).

## Der strengste geprüfte Vergleich

Die vier Vorgänger von 16 sind 0, 1, 2 und 15. An 0, 1 und 2 haben alle drei Lösungen die Uhren −5, −4 und −3 und je das Gewicht 1/8. An 15 beträgt der gemeinsame exakte Uhrwert −1,9910453320338362, das Gewicht ist null. Auch die vier frühen Uhrgradienten G₀, G₁, G₂ und G₃ sind je exakt gleich. Die ersten drei gehören zu materiellen Vorgängern, Knoten 3 liegt ausserhalb des strikten Sendervorlaufs. Als gemeinsame Impulsziele dienen feste rationale, auf 15 Dezimalstellen gerundete Mittelpunkte der zertifizierten zentralen Nullpräparation. Die exakten Brüche stehen in `Ergebnisse.json`.

| Quelle J an 16 | Eingeschlossene Uhr 21, gerundeter Mittelpunkt | Mögliche Empfangscodes |
|---|---:|---:|
| −10⁻⁶ | 0,8146879141 | 4 073 439 bis 4 073 440 |
| 0 | 0,8146844078 | 4 073 422 |
| +10⁻⁶ | 0,8146809015 | 4 073 404 bis 4 073 405 |

Die engste Lücke der benachbarten analogen Uhrbereiche beträgt mehr als 3,506·10⁻⁶ lokale Uhreinheiten. Die Regel aus PR 408 verwendet den zentralen Nullcode 4 073 422 und den Rasterschritt 2·10⁻⁷. Bis einschliesslich −3 Schritte relativ zur verwendeten Referenz gibt sie die positive Quelle aus, ab +3 die negative, dazwischen die Nullquelle. Die Tabelle deckt einen analogen Ablesefehler bis zu einem Viertel Rasterschritt ab. Die Entscheidung stimmt für jeden der drei Referenzfehler −1, 0 und +1. Alle drei Nachimpulse sind null.

Alle Anfangsranduhren und -gewichte, auch an 3, und die Normierungsuhr 7 bleiben fest. Die fünf zusätzlichen Unbekannten sind Y₈, Y₉, w₇, w₈ und w₉. Ihre Wahl verwendet den lokalen Rang der Randgleichungen. Die Empfangsuhr kommt in keiner Zielvorgabe vor. Für jede der drei Quellen schliesst der Prüfer eine Lösung der 25 ursprünglichen Gleichungen und fünf zusätzlichen Bedingungen ein. Alle 152 strikten Kausalrelationen, die strikten Gewichtsgrenzen und die Gerätebereiche werden geprüft. Die grösste Änderung von Y₈ gegenüber dem zentralen Nullkragen beträgt rund 9,34·10⁻⁶. Die fünf Werte werden für den jeweiligen Quellfall bestimmt. Ihre quellunabhängige physische Präparation wurde nicht nachgewiesen.

## Wie der Vergleich aufgebaut wurde

1. **Quellterm und äussere Präparation kreuzen.** Bei zentraler Drift ergibt die Kombination der drei N19-Präparationslabels K mit den drei unabhängig gesetzten N22-Quelltermen J neun Fälle. Auf allen neun stationären Lösungen liefert die bisherige Digitalregel J. Bei festem J beträgt die gesamte Variation der Empfangsuhr über die drei K weniger als 7,07·10⁻⁸. Bei gemeinsamem Nullkragen und verschiedenem J unterscheiden sich jedoch die freien Uhren 15. Die drei Diagonalfälle sind zusätzlich mit den bereits veröffentlichten Zertifikaten abgeglichen.
2. **Die freie Anfangsuhr 3 prüfen.** Vier Dichtegleichungen an 16, 18, 19 und 21 und sieben Uhrgleichungen an 15 bis 21 bilden ein geschlossenes Teilsystem. Seine wirksamen äusseren Knotendaten kommen ausschliesslich von 0, 1, 2, 7, 8, 9 und 10. Uhr 3 fehlt. Eigene Kontraktionsnachweise isolieren lokal die drei Lösungen dieses Teilsystems bei gemeinsamem Nullkragen. Ihre Uhr-15-Intervalle sind paarweise disjunkt. Eine alleinige Variation an 3 kann auf diesen Zweigen den Unterschied nicht aufheben.
3. **Uhr 15 abgleichen.** Wird Y₈ freigegeben, gibt es für alle drei Quellen Lösungen für jedes vorgegebene Y₁₅ im gemeinsamen Band von ±10⁻⁸ um den Referenzwert. Die analogen Empfangsbereiche bleiben über das ganze Band getrennt. Im inneren Band ±5·10⁻⁹ liefert die alte Digitalregel bei allen zugelassenen Fehlern den richtigen Quellwert. An beiden äusseren Endpunkten gibt es geprüfte falsche Entscheidungen für die Nullquelle. Bei diesem Ein-Uhr-Abgleich unterscheiden sich unter anderem G₀ und G₁ zwischen den drei Familien.
4. **Auch die frühen Impulse abgleichen.** Die fünf Randfreiheiten des strengsten Vergleichs liefern bei dem zentralen vorgegebenen Y₁₅ drei Lösungen mit gleichen G₀ bis G₃. Die Aussage zum kontinuierlichen Y₁₅-Band in Schritt 3 gehört allein zum Ein-Uhr-Abgleich.

## Nachweis und Wiederholung

Der Prüfer konstruiert numerische Zentren mit Dezimalarithmetik. Nach aussen gerundete Intervallarithmetik prüft anschliessend die gesamte Fixpunktabbildung. Die normierte Bildschranke und die Kontraktionsschranke liegen für jede ausgewiesene Lösung unter eins. Die lokale Eindeutigkeit bezieht sich jeweils auf die geprüfte Umgebung und die konkreten Randbedingungen. Eine zweite Auswertung aus den einzelnen Kantenbeiträgen kontrolliert 10 200 Einträge der Jacobimatrizen durch exakte rationale Differenzen. Der Leser und seine beiden Fehlerbudgets stammen unverändert aus dem beigefügten Vorgängerpaket. Die physischen Messungen zählen null, der Arealradius bleibt offen und alle 60 physischen P3-Prüfpunkte stehen auf `NOT_RUN`.

Die Rechnung läuft offline mit Python ab 3.10 und der Standardbibliothek. Nach dem Entpacken im Paketverzeichnis ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

Das Versuchsregister führt die neun gekreuzten Punktfälle, neun Abgleiche bei festem oder variablem Zielwert, zwei Randpunktkontrollen und die drei Abgleiche mit festen Impulszielen auf. Ergebnisse.json enthält zusätzlich die rationalen Uhrenintervalle, fünf Randkorrekturen je Impulsabgleich, die drei Zertifikate des geschlossenen Teilsystems und zwei konkrete Fehlablesungen. Die ersten drei Prüfschritte, die geänderte Wahl des Randknotens, die nachträgliche Kontrolle der Digitalgrenze und der schärfere Impulsabgleich sind in getrennten, lokal auf SHA-256 festgelegten Plänen dokumentiert.
