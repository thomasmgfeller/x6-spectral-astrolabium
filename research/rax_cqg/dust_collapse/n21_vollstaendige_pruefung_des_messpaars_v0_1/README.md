# Kann das N21-Modell den Staubrand zur halben Modellzeit messen?

**CST-DUST · Forschungsnotiz 0.1 · 26. November 2026**

**Ergebnis.** Keine der 406 142 untersuchten N21-Ordnungen trägt ein stationäres Messpaar im Fenster x = 1/2 ± 1/64. Die Aussage gilt für alle Anbindungen zweier neuer, kausal unvergleichbarer Ereignisse an die festgelegte N19-Ordnung mit mindestens einem gemeinsamen alten positiven Anker in der Vergangenheit und einem in der Zukunft. Die Anker dürfen ausserhalb des Fensters liegen. Die Ereigniskennungen bleiben unterscheidbar. Jede Ordnung zählt einmal, auch wenn mehrere Ankerpaare möglich sind.

| Notwendige Bedingung in der Reihenfolge des Tests | Ausgeschlossen | Verbleibend |
|---|---:|---:|
| Gemeinsame alte Anker und unvergleichbare neue Punkte | – | 406 142 |
| Zeitordnung zu den acht vorgegebenen Randuhren | 12 878 | 393 264 |
| Zulässige Vergangenheit des neuen positiven Punkts 19 | 165 588 | 227 676 |
| Zulässige Zukunft des neuen leeren Punkts 20 | 184 960 | 42 716 |
| Uhrordnung und gemeinsame notwendige Feldgleichungen | 42 716 | **0** |

Von den zuletzt verbliebenen 42 716 Ordnungen scheiden 42 646 bereits ohne Unterteilung des Feldbereichs aus. Bei 70 Ordnungen musste der Bereich in Teilintervalle zerlegt werden. Jede der 14 407 abschliessenden Teilboxen liefert einen Widerspruch. Die bekannte stationäre N19-Referenz besteht die Kontrolle mit denselben Rechenregeln.

**Was damit für den Staubball entschieden ist.** Das Hinzufügen genau dieses Messpaars reicht unter den übernommenen Rand- und Gerätebedingungen für eine Schalenmessung zur halben Modellzeit nicht aus. Die materielle Aussenseite, ein Arealradius und die physikalische Fortsetzung des Kollapses bleiben offen. Die 60 P3-Einträge stehen weiterhin auf NOT_RUN. [Veröffentlichte Modellgrundlage und Vorversuch](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/9c732c5b94482130b8a8286caa64e1bf86885091/research/rax_cqg/dust_collapse/n21_gemeinsame_stationaritaet_im_zielfenster_v0_1)

<div class="page"></div>

## Woher der Widerspruch kommt

Die Uhr steigt auf jeder Kausalrelation. Die normierte Zeit ist x = (Y−Y₃)/(Y₇−Y₃). Die beiden neuen Ereignisse haben x im geschlossenen Zielfenster. Punkt 19 hat ein freies Gewicht zwischen null und eins. An Punkt 20 ist das Gewicht null und die Uhr frei. Die alten Nullereignisse sind 15 und 17. Nur die acht Randuhren und ihre Gewichte sind vorgegeben. Alle alten Innenfelder dürfen sich ändern. Die drei Zeiger behalten ihre veröffentlichten Abtastwege. Die neuen Punkte erhalten keine zusätzliche Quelle.

Für jedes geordnete Paar i ≺ j zählt der Test die Ereignisse im offenen Intervall neu. Bei null, einem, zwei oder drei Zwischenereignissen ist der Koeffizient cᵢⱼ gleich 1, −9, 16 bzw. −8. In grösseren Intervallen verschwindet er. Der Staubanteil der Dichtevariation am positiven Punkt j und die Uhrvariation an i lauten in der Projektnormierung

> Dⱼ = 19 + Σₖ≺ⱼ cₖⱼ(Yⱼ−Yₖ)². Gᵢ = Σᵢ≺ₖ cᵢₖ wₖ(Yₖ−Yᵢ) − wᵢ Σₖ≺ᵢ cₖᵢ(Yᵢ−Yₖ).

**Eine von Hand prüfbare Familie.** In 1 205 der 42 716 Fälle hat Ereignis 19 genau die alten Vorgänger 0 und 17. Zwischen 0 und 19 liegt 17. Setzt man n = Y₁₉ und h = Y₁₇, so ist Y₀ = −5 < h < n. Die beiden neuen Ereignisse sind unvergleichbar, daher trägt 20 zu dieser Variation nichts bei. Es folgt im gesamten Zielfenster

> D₁₉ = 19 − 9(n+5)² + (n−h)² < 19 − 8(n+5)² < −182,87.

Schon diese eine Gleichung schliesst die ganze Familie aus, bei beliebiger zulässiger Wahl der Gewichte und der künftigen Anker. Eine separate Rechnung mit exakten Brüchen prüft 50 mögliche Vergangenheiten, in denen 16 und 18 vor Punkt 19 fehlen. Sie liefert für 21 879 Ordnungen ein striktes Vorzeichen von D₁₉. Bei 5 066 weiteren Anordnungen dieser Teilmenge reicht diese Abschätzung allein nicht aus.

**Gerät und kleine Gewichte.** Im Gerät gilt κ = 10⁻¹¹, der Abgleich ist −κ, die Senderquelle ist 0 oder ±10⁻⁶ und jeder der drei Nachimpulse hat Betrag ≤ 1,12·10⁻¹². Die genaue Dichtevariation an 16 und 18 enthält den positiven Term L/w² mit L = κ Σ vₐ². Der Prüfer lässt Gewichte beliebig nahe null zu. Für w < 10⁻⁸ nutzt er nur eine obere Schranke für den reinen Staubgradienten. Für w ≥ 10⁻⁸ beträgt dessen zulässiger Betrag höchstens 2,001·10⁻⁶. Die Abweichung der freien Geräte-Uhrgradienten vom reinen Staubausdruck ist kleiner als 10⁻⁸. Jede exakte stationäre Lösung müsste diese erweiterten Bedingungen erfüllen.

<div class="page"></div>

## Wie sich der Ausschluss nachprüfen lässt

**Vollständigkeit.** Die Aufzählung setzt für jeden neuen Punkt eine abgeschlossene Vergangenheit und Zukunft in die alte Ordnung ein. Alle alten Vergangenheitsereignisse müssen vor allen alten Zukunftsereignissen liegen. Ausgeschlossen werden Anbindungen, die über ein altes Ereignis eine Relation zwischen 19 und 20 erzwingen. Die alte induzierte Ordnung bleibt erhalten. Eine zweite Konstruktion prüft alle Teilmengen der 19 alten Kennungen auf Abgeschlossenheit und rekonstruiert dieselben 42 716 Anbindungen. Für die vorausgehenden Ausschlüsse werden die 18 gerätefreien Vergangenheitsideale und alle vier möglichen reinen Kragenzukünfte nochmals geprüft.

**Feldrechnung.** Bei jeder Anbindung werden die Intervallkoeffizienten auf der vollständigen N21-Ordnung neu gebildet. Aus Dichtegleichungen folgen Schranken für Uhren und positive Zeitabstände. Die Uhrgleichungen beschränken Uhren und Gewichte. Es werden nur Werte entfernt, die eine notwendige Bedingung verletzen. Die Ganzzahlrechnung rundet an Intervallgrenzen nach aussen, in Einheiten von 10⁻⁹. Wo nötig überdecken die beiden Teilboxen zusammen den gesamten Elternbereich. In den 42 646 direkten Fällen ist der letzte Widerspruch 39 100-mal eine Dichtebedingung, 3 252-mal eine Uhrgleichung und 294-mal die Zeitordnung. Die Zuordnung kann mit der Prüfreihenfolge wechseln.

**Gegenproben.** 1 265 exakte symmetrische Differenzen der vollständigen feldabhängigen Wirkung kontrollieren die Uhr- und Dichtegradienten auf 55 Ordnungen. 305 rationale Intervalltests prüfen die Rechenoperationen. Das Ausgangsmodell wird über 168 Randteilfälle aus den archivierten Daten rekonstruiert. Anschliessend werden die künftigen Randgewichte unabhängig um ±10⁻⁶ sowie die Randuhren 8 bis 10 um ±10⁻⁴ erweitert. Die Zeitreferenz 7 bleibt fest. Auch bei dieser Erweiterung und einer anderen Reihenfolge der Gleichungen scheiden sämtliche 42 716 Anordnungen aus.

**Nächster unterscheidbarer Versuch.** Wer denselben N19-Ausgangspunkt, dasselbe Zeitfenster und dieselben Geräte beibehält, kann als kleinste Erweiterung der Ereigniszahl N22 untersuchen. Ein drittes neues Ereignis kann die Zwischenpunktzahlen und damit die bisher ausschliessenden Koeffizienten ändern. Seine Rolle, sein Gewicht und seine zulässigen Kausalrelationen sind vor der Rechnung festzulegen. Ob ein solches Messpaar stationär wird, ist offen.

**Offline nachrechnen.** Im entpackten Ordner mit Python 3.11 oder neuer und g++ für C++17 den Befehl `python3 -B pruefen.py` ausführen. Der Lauf kompiliert den Prüfer, vergleicht die SHA-256-Summen und reproduziert Register.tsv und Ergebnisse.json bytegenau. Das Register erfasst je Ordnung Vergangenheit P und Zukunft F der neuen Punkte als Bitmasken. Bit i steht für das alte Ereignis i. Es enthält den letzten Widerspruch bzw. die Widersprüche aller Teilboxen. Das vorige Ankerpaket mit den Quellen liegt unter basis/Ankerpaket.zip. Der lokale Prüfplan und die später festgelegte Randkontrolle sind mit eigenen Prüfsummen dokumentiert. [Öffentlicher Ausgangsstand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/400)
