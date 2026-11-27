# N22 · Gleiche späte Randimpulse beim Quellenwechsel

**Jedes Paar der vier späten Uhrimpulse lässt sich gemeinsam vorgeben. Drei gleiche späte Uhrimpulse schliessen im geprüften Feldgebiet einen Quellenwechsel aus.** Die Summe aller vier bleibt in allen Fällen exakt gleich. Die Untersuchung knüpft an die sieben einzelnen Randuhren und -gewichte in [PR 410](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/410) an und verwendet die schon für den frühen Rand definierte Impulskonvention aus [PR 409](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/409).

## Welche Daten gemeinsam vorgegeben werden

Geprüft wird die endliche Ordnung 216141/229383/0/+ mit Quelle J an 16 und Empfangsuhr 21. Der frühe Kragen, Y₇, die Uhr am Sendervorgänger 15 und die vier frühen Impulse sind wie in PR 410 festgelegt. Die drei Nachimpulse der Geräte sind null. Alle sieben späten Feldkoordinaten aus PR 410 sind im neuen Versuch frei. Die zwei zusätzlichen Gleichungen geben späte Impulse vor.

Für eine gerichtete Kante i→j mit Koeffizient kᵢⱼ beträgt ihr Beitrag zum Uhrimpuls am Ausgang i genau kᵢⱼ wⱼ (Yⱼ−Yᵢ). Am Eingang j geht derselbe Betrag mit umgekehrtem Vorzeichen ein. Daher gilt die Summe aller 22 Uhrimpulse identisch null. Die 14 freien Uhrgleichungen haben den Wert null. Auf jeder stationären Lösung ist folglich die Summe von G₇ bis G₁₀ das Negative der Summe von G₀ bis G₃. Das verwendete J tritt in der Dichtegleichung an 16 auf.

Die vier Einzelziele stammen allein aus dem zentralen Nullquellenfall mit festem Y₁₀ und w₁₀ aus PR 410. Die ersten drei sind vorab auf 15 Nachkommastellen gerundete Werte aus der Mitte der veröffentlichten Feldbox. Der vierte folgt exakt aus der Bilanz. In die Formeln für die vier späten Impulse geht Uhr 21 auf dieser Ordnung auch über keine direkte Kante ein.

| Grösse | Gemeinsames Ziel in der Modellnormierung |
|---|---:|
| G₇ | 0,284260768629664 |
| G₈ | −0,329463256783844 |
| G₉ | −0,066957254135818 |
| G₁₀ | 0,293745323598963 |
| Summe aller vier | 0,181585581308965 |

## Sechs Paare und 18 stationäre Fälle

Für jedes Paar und jede Quelle zertifiziert eine Intervallkontraktion eine stationäre Lösung der 32 Gleichungen. Der Prüfer kontrolliert sämtliche 152 strikten Kausalrelationen, die zulässigen Geräte- und Gewichtsbereiche sowie die Stör- und Rundungsgrenzen der unveränderten Leseregel. Zehn Lösungsboxen liegen vollständig im Gebiet aus PR 410. Das erweiterte, konvexe Feldrechteck enthält die 63 veröffentlichten sowie alle 18 neuen Boxen und das gesamte frühere Prüfgebiet. Die beiden Gebiete werden getrennt ausgewertet.

| Quelle an 16 | Paarvorgaben | Empfangscodes an 21 |
|---|---:|---:|
| −10⁻⁶ | 6 | 4 073 439 bis 4 073 440 |
| 0 | 6 | 4 073 422 |
| +10⁻⁶ | 6 | 4 073 404 bis 4 073 405 |

Bei zwei festen Einzelimpulsen sind die Änderungen der übrigen zwei exakt entgegengesetzt. Die folgende Tabelle gibt äussere Hüllen für beide benachbarten Quellenwechsel in steigender Richtung. Die Zahlen sind Millionenstel der Impulseinheit des Modells. Die vollständigen rationalen Einzelintervalle stehen in Impulsaustausch.tsv.

| Feste Knoten | Änderung berichtet an | Entgegengesetzte Änderung an | Intervall in Millionsteln |
|---|---:|---:|---:|
| 7 und 8 | 9 | 10 | [−1,743; −1,741] |
| 7 und 9 | 8 | 10 | [−0,576; −0,575] |
| 7 und 10 | 8 | 9 | [−0,860; −0,859] |
| 8 und 9 | 7 | 10 | [−0,522; −0,521] |
| 8 und 10 | 7 | 9 | [−0,745; −0,744] |
| 9 und 10 | 7 | 8 | [−5,547; −5,544] |

## Warum drei gemeinsame Impulse den Quellenwechsel ausschliessen

Zwei beliebige stationäre Lösungen im Gebiet haben dieselben frühen Daten und Ziele. Bei Gleichheit einer beliebigen Dreiergruppe später Impulse bleibt wegen der Bilanz auch der vierte gleich. Für den diagnostisch entscheidenden Rückschluss auf J wird die Jacobi-Matrix um die Quellspalte und die drei Impulszeilen erweitert. Die 32 Feldkoordinaten und J ergeben 33 Differenzen. Die Residuen sind höchstens quadratisch. Daher gilt die Matrixgleichung für die Differenzen exakt am arithmetischen Mittelpunkt beider Feldzustände.

Für jede der vier Dreiergruppen hat die gewichtete Unendlichnorm von I − C A eine nachgewiesene obere Schranke kleiner eins. Hier bezeichnet A die erweiterte Matrix am jeweiligen Mittelpunkt und C einen festen Vorkonditionierer für Gebiet und Dreierauswahl. Die grössten oberen Schranken betragen 0,134406741682 für das Rechteck aus PR 410 und 0,139413687064 im erweiterten Gebiet. Damit ist A dort invertierbar. Gleiche Impulse erzwingen gleiche Quelle. Das gilt für beliebige gemeinsame Impulswerte im Vergleich zweier solcher Lösungen, einschliesslich Werten ausserhalb der gewählten Nullquellen-Ziele.

Bei verschiedenen Impulsen werden drei rechte Seiten mit eingeschlossen. Für die Auswahl 7, 9 und 10 gilt im erweiterten Gebiet

    |ΔJ| ≤ 3,081471894140 · max(|ΔG₇|, |ΔG₉|, |ΔG₁₀|).

Bei einem Quellenabstand von 10⁻⁶ ändert sich daher mindestens einer dieser Impulse um mehr als 3,245 · 10⁻⁷ Modell-Impulseinheiten. Für die beiden äusseren Quellen verdoppelt sich die Untergrenze. Eine Impulseichung und ein physischer Eingriff am Sender sind offen. Die 60 physischen P3-Prüfpunkte stehen weiter auf NOT_RUN.

## Reproduktion

Python ab 3.10 mit der Standardbibliothek genügt. Nach dem Entpacken im Paketverzeichnis ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

Der Prüfer rekonstruiert Ordnung, Kantenkoeffizienten und Gerätekonventionen aus dem mitgelieferten, auf SHA-256 festgelegten Paket von PR 410. Er erzeugt die Zertifikate neu und vergleicht Ergebnisse.json sowie die drei TSV-Register mit der Ausgabe. Die unabhängige Auswertung der Kanten kontrolliert 4 356 Ableitungseinträge per rationalem Zentralquotienten und 792 Residuenkomponenten der exakten Mittelpunktformel. Pruefplan.md enthält den vor der Rechnung festgelegten Prüfvertrag. Ergebnisse.json enthält die Lösungsboxen, die beiden Gebietsverweise beziehungsweise -grenzen, die rationalen Gewichtungen und die Vergleichsschranken.
