# Kann die verfeinerte N21-Ordnung den Staubrand tragen?

**CST-DUST · Forschungsnotiz 0.1 · 26. November 2026**

Das Zeitfenster um die halbe Modellzeit enthält im veröffentlichten N19-Zweig nur den Sender 16 und den Empfänger 18. Der Versuch setzt dazwischen ein positives Ereignis 19 und ein Staub-Nullereignis 20. Die beiden neuen Ereignisse sind unvergleichbar. Zusammen mit den Ankern würden sie einen zweiseitig beobachtbaren Bereich für eine mögliche Schalenmessung bilden. [Vorstudie zu Zeitfenster und Schalenfläche](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/286fe3adc05dea486adf1e97b8b9664dba9df3d1/research/rax_cqg/dust_collapse/zeitblock_schalenflaeche_und_n19_verfeinerung_v0_1)

**Ergebnis.** Bei den übernommenen Randdaten hat keine der vier N21-Ordnungen eine zulässige gemeinsame stationäre Lösung mit beiden Ankern in x = 1/2 ± 1/64. Sämtliche freien Innenfelder dürfen sich auf der neuen Ordnung ändern. Der Beweis verwendet Bedingungen, die jede Lösung des vollständigen Systems erfüllen müsste. Für jede Anbindung hat mindestens eine notwendige Dichtevariation ein striktes Vorzeichen.

| Zusätzliche Relationen vom alten Ereignis 17 | Notwendige Gleichung | Zertifizierte Schranke |
|---|---|---|
| Weder zu 19 noch zu 20 | Dichtevariation am neuen positiven Ereignis | D₁₉ < −15,50 |
| Nur zu 20 | Dichtevariation am neuen positiven Ereignis | D₁₉ < −15,50 |
| Nur zu 19 | Dichtevariation am Empfänger, falls die vorgelagerten Bedingungen gelten | D₁₈ < −29,87 |
| Zu 19 und zu 20 | Dichtevariation am Empfänger, falls auch D₁₉ = 0 gilt | D₁₈ > 206,95 |

Der Geltungsbereich ist das genannte Zeitfenster, die feste Ordnung der bisherigen 19 Ereignisse, der angegebene Besetzungssektor und die unten definierte endliche Projektwirkung. Untersucht wurden drei Quellen über sieben kontinuierliche Driftzellen mit allen zugelassenen Nachimpulsen. Es ist damit eine konkrete Möglichkeit zur Erzeugung eines schmalen Messbereichs entschieden. Andere Anker, Wirkungen und Zeitfenster sind eigene Aufgaben. Für den physischen Staubball bleiben die acht Radiuswerte am Zielschnitt offen. Sämtliche 60 P3-Einträge stehen auf NOT_RUN.

<div class="page"></div>

## Welche Felder der Test frei lässt

Pro Fall übernehmen wir die vier vergangenen und vier künftigen Randuhren und ihre acht Gewichte aus derselben zertifizierten N19-Lösung. Das sind Dirichlet-Randdaten. Die Enge der archivierten Innenfeldintervalle wird für N21 aufgegeben. Frei sind insbesondere die alten Sender-, Empfänger- und Vorläuferuhren, die Uhr und das positive Gewicht von 19 sowie die Uhr des Punktes 20. Im diskreten Nullsektor haben 15, 17 und 20 Gewicht null. Jedes andere freie Gewicht liegt strikt zwischen null und eins. Die Uhr steigt auf jeder Kausalrelation. Ein Nullgewicht kennzeichnet den gewählten Materiesektor. Für eine physische Aussenmarkierung wären weitere Beobachtungen nötig. [Randfamilie und Gerätemodell](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/286fe3adc05dea486adf1e97b8b9664dba9df3d1/research/rax_cqg/dust_collapse/n19_driftfenster_und_voruhreneichung_v0_1)

Der alte Sender ist notwendig ein Vorgänger und der Empfänger ein Nachfolger beider neuer Ereignisse. Die alte Vergangenheit eines neuen Punkts enthält daher {0,1,2,15,16} und kann zusätzlich nur 17 enthalten. Seine alte Zukunft ist genau {18,7,8,9,10}. Jede der vier unabhängigen Wahlen für 19 und 20 ist transitiv realisierbar. Die vier neuen Ordnungen enthalten 149, 150, 150 und 151 strikte Relationen. Die Intervallkoeffizienten werden auf jeder Ordnung neu berechnet.

In der verwendeten Normierung ist der relevante Staubterm 19 Σ wⱼ + Σ cᵢⱼ wⱼ(Yⱼ−Yᵢ)². Für 0, 1, 2 und 3 Ereignisse zwischen i und j gilt c = 1, −9, 16 und −8. Grössere Intervalle haben c = 0. Dⱼ bezeichnet die Ableitung nach dem Gewicht und Gᵢ die mit −1/2 multiplizierte Ableitung nach der Uhr. Der reine Ordnungsterm ändert diese Feldableitungen auf fester Ordnung nicht. [Endliche Wirkung und freie Nulluhren](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/286fe3adc05dea486adf1e97b8b9664dba9df3d1/research/rax_cqg/dust_collapse/schalenvolumen_und_seitenfluss_v0_1)

Die drei Zeiger behalten ihre bisherigen Abtastpaare, Ladungen und Trägheitspunkte. Bei dieser Fortsetzung darf die alte direkte Abfrage 16→18 eine Kausalrelation mit Zwischenereignissen überbrücken. Ein Gerät, das dafür zwingend einen Link verlangt, verliert diese Verbindung bereits durch den Einbau. Neue Kopplungen an 19 oder 20 sind gesondert zu untersuchen. Im aktiven Versuch ist κ = 10⁻¹¹, der Abgleich −κ, der Senderquellwert J = 0 oder ±10⁻⁶ und |vᵢ| ≤ 1,12·10⁻¹² für jeden der drei skalierten Nachimpulse.

<div class="page"></div>

## Warum die Stationarität scheitert

Schreibe s,r für die Uhren des Senders und Empfängers, n,z für die neuen Uhren und u,h für die alten Vorläufer 15 und 17. Der gemeinsame Zeitbezug ist x = (Y−Y₃)/(Y₇−Y₃). Im breiten Zielfenster liegen s,n,z,r in der Rohzeit zwischen 0,023 und 0,144 mit s < n,z < r. Für die neue leere Uhr tritt die Randkombination B(z) auf. Setze bⱼ = wⱼ(Yⱼ−z). Dann gilt

> G₂₀ = w₁₈(r−z) + B(z) = 0, B(z) = −9b₇ + 16b₈ − 8b₉.

Über alle Randfälle gilt −B(z) > 0,00836. Weil w₁₈ < 1 ist, braucht es schon zwischen 20 und 18 einen normierten Zeitabstand über 0,00218. Im engeren archivierten Sende- und Empfangsbetrieb liegt die maximale Rohzeitspanne zwischen 16 und 18 unter 0,001062, während −B(z) dort über 0,00866 liegt. Auf diesem Betriebsfenster scheitert bereits G₂₀. Die Rechnung für das breitere Fenster nutzt weitere Gleichungen.

Dort folgen aus G₂₀ = 0 und G₁₅ = 0 die unteren Schranken w₁₈ > 0,0698 und w₁₆ > 0,0212. Für die zweite Schranke gilt (1−κ)w₁₆(s−u) = 8w₁₈(r−u) + 9w₁₉(n−u) + κv₁. Da u < s < z < r, dominiert schon der erste Summand den gebundenen Impulsterm. Mit L = κΣvᵢ² verlangt die Dichtegleichung am Sender

> (1−κ)(s−u)² = s² + 6s + 6 + J − L/w₁₆².

Daraus folgt 2,4781 < s−u < 2,6230. Ohne den Beitrag von 17 ist der Dichtegradient am neuen Punkt A = 35 + 32n + 8n² − 9(n−u)² + (n−s)² < −15,50. Damit entfallen zwei Anbindungen. Bei 17≺19 verlangt D₁₉ = 0 zusätzlich (n−h)² = −A. Ist 17≺20 abwesend, hat (r−h)² im Empfängergradienten den Koeffizienten −9−κ. Sein übriger Anteil genügt für die negative obere Schranke. Ist 17≺20 vorhanden, lautet der Koeffizient 16−κ. Aus h < n < r folgt (r−h)² > −A und die positive untere Schranke. Die vollständige Empfängerbedingung lautet mit dem Ordnungskoeffizienten c für 17→18

> D₁₈ = 19 − 8(r−u)² + (16−κ)(r−s)² + (c−κ)(r−h)² + (r−n)² + (r−z)² + L/w₁₈² = 0.

Der Wert von c ist 1, −9 oder 16, je nachdem, ob 17 vor keinem, einem oder beiden neuen Ereignissen liegt. Die Uhrvariation an 19 ist ebenfalls im Prüfer implementiert. Bereits die genannten notwendigen Bedingungen widersprechen sich für beliebige zulässige Werte der übrigen Innenfelder.

<div class="page"></div>

## Wie stark das Ergebnis vom Rand abhängt

Nach dem Test der festgelegten Randfamilie wurden die drei Dichtegleichungen separat geprüft. Es genügt hier, die frühen Rohuhren Y₀ = −5, Y₁ = −4, Y₂ = −3, die oben angegebenen Quellen und das vergrösserte Rohzeitfenster [0,023; 0,144] beizubehalten. Die übrigen Randuhren und -gewichte treten in dieser Abschätzung nicht auf. Ein geänderter Zeitbezug müsste die Abbildung des Zielzeitpunkts in dieses Rohzeitfenster erneut begründen.

**Verschwindende Zeigerimpulse.** Für L = 0 hängen die drei Dichtegleichungen nur noch von den Uhren und den vorgegebenen Kopplungen ab. Der Ausschluss gilt dann im ganzen Sektor positiver Innengewichte. Ein Wechsel allein der künftigen Randgewichte kann unter diesen Voraussetzungen keine der vier Anbindungen ermöglichen.

**Zugelassene Zeigerimpulse.** Falls w₁₆ und w₁₈ beide mindestens 10⁻¹⁷ betragen, gilt L/w² ≤ 0,37632 an beiden Ankern. Die drei Vorzeichenschranken im grösseren Rohzeitfenster sind dann A < −12,07, D₁₈ < −26,45 bzw. D₁₈ > 151,86. Jede denkbare Lösung mit anderen Randdaten und den übrigen genannten Vorgaben müsste folglich einen von null verschiedenen Impuls und mindestens ein Ankergewicht unter 10⁻¹⁷ besitzen. Diese hinreichende Ausschlussschwelle ist in den Modelleinheiten gewählt. Ob in dem verbleibenden Bereich eine Lösung existiert, ist offen.

**Kontrollen.** Sechs relevante Variationen pro Ordnung wurden mit exakten symmetrischen Differenzen der vollständigen feldabhängigen Wirkung bei rationalen Testfeldern überprüft. Dabei wurden die Zeigertrajektorien beim Variieren festgehalten. Die N19-Positivkontrolle prüft die archivierten stationären Felder und die Wechselwirkung erneut. Für die Hauptschranken werden die beiden signierten Randmomente ausgenutzt, die der Übergang vom unbelasteten zum belasteten Gerätezustand exakt erhält. Acht Unterteilungen je Driftzelle ergeben 168 zusätzliche direkte Rechnungen aus den belasteten Randfeldern ohne diese Vereinfachung. Sie bestätigen alle vier Ausschlüsse. Auch die Kontrolle mit entkoppelten Zeigern bei denselben Randdaten ergibt die vier Widersprüche.

**Konsequenz für die nächste Konstruktion.** Eine andere Platzierung des äusseren Messpunkts, etwa mit einem früheren oder späteren Anker, fällt ausserhalb dieser vier Ordnungen. Für einen solchen Versuch lässt sich die notwendige freie Uhrgleichung am leeren Punkt unmittelbar nach der Wahl der Ordnung prüfen. Der Arealradius, seine Eichung und eine Fortsetzung des Kollapses bleiben eigenständige Aufgaben.

**Offline nachrechnen.** Im entpackten Ordner mit Python 3.11 oder neuer `python3 -B pruefen.py` ausführen. Das Paket enthält die referenzierten Modelldaten, den lokal festgelegten Prüfplan, die gekennzeichnete Ergänzung und alle rationalen Schranken in Ergebnisse.json. Der Prüfer vergleicht die neue Ausgabe bytegenau mit dem archivierten Ergebnis. Ausgangspunkt ist [PR #399](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/399).
