# N22 · Wie viele Zukunftsrandwerte können beim Quellenwechsel gleich bleiben?

**Im geprüften Gebiet sind es genau zwei von sieben.** Jedes der 21 möglichen Paare lässt sich auf die zentrale Nullpräparation festlegen. Für jede Wahl existieren stationäre Lösungen für alle drei Quellen. In derselben Umgebung ist für jede der 35 Dreiergruppen ausgeschlossen, dass zwei unterschiedliche Quellen alle drei Werte gemeinsam haben. Die Aussage gilt für die einzelnen Koordinaten Y₈, Y₉, Y₁₀, w₇, w₈, w₉ und w₁₀. Die Normierungsuhr Y₇ ist bereits separat festgelegt.

Untersucht ist die endliche Ordnung 216141 / 229383 / 0 / + bei verschwindenden Nachimpulsen. Die frühen Uhren und Gewichte sind fest. Für Y₁₅ und die vier frühen Uhrimpulse G₀ bis G₃ gelten dieselben fünf exakten Ziele wie im vorigen Versuch. Die Quellterme am Sender 16 sind −10⁻⁶, 0 und +10⁻⁶. Der bisherige Leser verwendet am gemeinsamen Nachfolger 21 weiterhin sein ursprüngliches Raster, dieselben Schwellen und Fehlerbudgets. [Ausgangsstudie auf GitHub, PR 409](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/409)

## Alle 21 Paare mit festen Randwerten

Je Paar werden fünf Zukunftsrandwerte und die 25 ursprünglichen freien Felder gemeinsam bestimmt. Der Prüfer schliesst für jeden Quellterm eine stationäre Lösung mit allen 152 strikten Kausalrelationen und den zugelassenen Gewichten und Gerätewerten ein. Er prüft ferner, dass sich bei unterschiedlicher Quelle tatsächlich alle fünf übrigen Zukunftsrandwerte unterscheiden. Die 63 Fälle zählen die 21 Randvorgaben mit je drei Quellen. Sie sind keine unabhängigen Messungen.

| Quelle J | Fälle | Sichere Hülle der Empfangscodes an Uhr 21 |
|---|---:|---:|
| −10⁻⁶ | 21 | 4 073 439 bis 4 073 440 |
| 0 | 21 | 4 073 422 |
| +10⁻⁶ | 21 | 4 073 404 bis 4 073 405 |

Alle zulässigen Rundungen und Ablesefehler bis zu einem Viertel Rasterschritt sind enthalten. Der Leser unterscheidet die Quellen auch bei einem unabhängigen Fehler von einer Stufe im Referenzcode. Bei festem J hat die Hülle der 21 geprüften analogen Werte von Y₂₁ eine Breite von weniger als 2·10⁻¹⁷. Das ist eine numerische Einschliessung für diese Lösungen. Ob eine exakte Identität besteht, bleibt offen.

## Alle 35 Dreiergruppen mit gleichen Randwerten

Für zwei Zustände ist die Differenz der 30 stationären Gleichungen und Zielbedingungen exakt die Jacobimatrix am arithmetischen Mittelpunkt mal Felddifferenz, zuzüglich der linearen Quellenänderung. Dies folgt daraus, dass jedes Residuum höchstens quadratisch in den Feldern und affin in J ist. Die fünf Zielwerte sind für beide Zustände gleich. Wenn drei der sieben Zukunftskoordinaten gleich sind, bleiben für die Differenz 25 innere Koordinaten, vier weitere Zukunftskoordinaten und der Quellterm. Die resultierende homogene Gleichung hat eine quadratische Matrix der Dimension 30.

Für jede Dreiergruppe gilt im gesamten gemeinsamen Prüfgebiet eine nach aussen bewiesene Normschranke für I − C A. Hier ist A die erweiterte Sekantenmatrix und C eine feste numerische Vorkonditionierung für diese Gruppe. Die grösste der 35 oberen Normschranken ist 0,618264382321. Da jede kleiner als eins ist, ist A überall im Gebiet invertierbar. Damit muss auch die Quelldifferenz verschwinden. Die drei gemeinsamen Zukunftswerte dürfen beliebige Werte innerhalb des Prüfgebiets annehmen.

Das Gebiet ist ein einziges abgeschlossenes Rechteck in den Feldkoordinaten. Die Konstruktion umfasst die 63 Lösungsboxen und erweitert ihre Hülle bei jeder aktiven Koordinate um mindestens 2 % ihrer Spannweite je Seite, mindestens 10⁻⁹ bei Uhren und 10⁻¹¹ bei Gewichten. Die exakten Endpunkte stehen in Ergebnisse.json unter `domain`, in Einheiten von 10⁻²⁸. Der Ausschluss benötigt nur, dass der Mittelpunkt in diesem Gebiet liegt und die angegebenen Daten an beiden Enden gleich sind. Er gilt insbesondere für beliebige Lösungen innerhalb des Gebiets. Andere stationäre Zweige, andere Ordnungen und anders definierte Randobservablen erfordern eine eigene Prüfung.

## Eine Mindeständerung für die drei Zukunftsuhren

Für die Dreiergruppe Y₈, Y₉ und Y₁₀ wird auch die rechte Seite der Sekantengleichung bei verschieden gesetzten Uhren eingeschlossen. Die vier Zukunftsgewichte dürfen sich dabei ändern. Für zwei Lösungen mit den gleichen frühen Daten und Zielen ergibt sich

    |ΔJ| ≤ 0,233839693681 · max(|ΔY₈|, |ΔY₉|, |ΔY₁₀|).

Bei benachbarten Quellen muss sich daher mindestens eine dieser drei Uhren um mehr als **4,276·10⁻⁶** lokale Uhreinheiten verschieben. Welche Uhr das ist, kann vom verglichenen Paar abhängen. Zwischen den beiden entgegengesetzten Quellen verdoppelt sich die Untergrenze. Die Konstante ist eine abgesicherte obere Schranke für die Antwort von J, ohne Optimalitätsanspruch.

Mit demselben hypothetischen Raster von 2·10⁻⁷ und unabhängig bis zu 5·10⁻⁸ analogem Fehler je Ablesung unterscheiden sich die absoluten Ziffern an wenigstens einer Zukunftsuhr bei benachbarten Quellen um mindestens 20 Schritte. Der Vergleich setzt eine gemeinsame Kalibrierung voraus und schliesst Rundungsbindungen ein. Ein entsprechendes Messgerät am Zukunftsrand wurde nicht erprobt. Ein physischer Sendeversuch mit unabhängig präpariertem Zukunftsrand und der Arealradius bleiben offen. Alle 60 physischen P3-Prüfpunkte stehen auf `NOT_RUN`.

## Prüfpaket und Wiederholung

Python ab 3.10 mit der Standardbibliothek genügt. Nach dem Entpacken im Paketverzeichnis ausführen.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

- `Paarregister.tsv` führt die 63 stationären Fälle mit Quellwert, Uhrenintervall, Empfangscodes und Kontraktionsnachweis über die Bildnorm auf.
- `Dreierregister.tsv` enthält den Ausschlussstatus und die nach oben gerundete Norm für alle 35 Matrizen.
- `Ergebnisse.json` enthält die Feldintervalle, das gemeinsame Prüfgebiet, die positiven Skalierungsvektoren, die Vergleichsschranke für die drei Zukunftsuhren und deren rationalen Nachweis.
- `Pruefplan.md` und `Uhrenaufloesung.md` dokumentieren den Haupttest und die nach dem vollständigen Scan ergänzte Frage zur Ableseauflösung. Beide Texte sind im Paket auf SHA-256 festgelegt.
- `basis/Sendervorlauf.zip` enthält die unveränderten Eingaben aus PR 409. Der Prüfer rekonstruiert daraus Ordnung, Wirkung, Nullkragen, Leseregel und Randziele. Eine direkte zweite Auswertung der Kantenbeiträge kontrolliert die exakte Sekantenidentität an 1 890 Residuenkomponenten.
