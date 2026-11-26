# Ein drittes Ereignis für die Staubrandmessung

**CST-DUST · N22-Forschungsnotiz 0.1 · 26. November 2026**

**Kann ein zusätzliches Ereignis den N21-Ausschluss aufheben?** Mit einem positiven Nachfolger des leeren Messpunkts besitzt das erweiterte Feldsystem nachweislich stationäre Lösungen. Die nachgewiesenen Lösungen verfehlen das gemeinsame Zielfenster x = 1/2 ± 1/64. Im Fenster sind 1 624 495 von 1 624 568 geprüften Ordnungs- und Gewichtsfällen ausgeschlossen. 73 Fälle bleiben offen.

Die beiden Messpunkte sind der positive Punkt 19 und der leere Punkt 20. Sie liegen kausal unvergleichbar zwischen gemeinsamen alten positiven Ankern. Das zusätzliche Ereignis 21 erhält dieselben alten Vorgänger und Nachfolger wie der Messpunkt, an den es anschliesst. Es wird entweder unmittelbar vor 19 oder unmittelbar nach 20 eingefügt. Seine Uhr ist frei und darf ausserhalb des Fensters liegen. Beide Rollen gehen mit leerem und mit frei positivem Gewicht in die Rechnung ein.

| Lage und Gewicht von 21 | Im Zielfenster ausgeschlossen | Offen |
|---|---:|---:|
| Unmittelbar vor 19, leer | 406 136 | 6 |
| Unmittelbar vor 19, positiv | 406 127 | 15 |
| Unmittelbar nach 20, leer | 406 142 | 0 |
| Unmittelbar nach 20, positiv | 406 090 | 52 |

Die vier Zeilen umfassen je 406 142 Anbindungen. Das ergibt 812 284 verschiedene etikettierte N22-Ordnungen mit jeweils zwei möglichen Gewichtsvorgaben. Der Ausschluss des leeren Nachfolgers gilt für alle Anbindungen dieser Familie. Andere Vergangenheiten und Zukünfte des dritten Ereignisses sind weitere Modellklassen.

**Physikalische Reichweite.** Für eine Messung zur halben Modellzeit müssen 19 und 20 im selben vorgegebenen Zeitfenster liegen. Die 73 offenen Fälle erfüllen bislang nur die notwendigen Intervalltests. Ob sie die vollständigen Feldgleichungen im Fenster lösen, ist offen. Auch die Zuordnung eines leeren Punktes zur materiellen Aussenseite, der Arealradius und die 60 physischen P3-Checkpoints bleiben offen. Im P3-Register stehen alle 60 Einträge auf NOT_RUN. [Ausgangspunkt auf GitHub · PR #401](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/401)

<div class="page"></div>

## Was der neue Zwischenpunkt ändert

Der Test übernimmt die induzierte N19-Ordnung, die acht Randuhren mit ihren Gewichten, die Wirkung und die drei Zeigerkanäle aus der veröffentlichten Familie. Die alten Innenfelder dürfen sich neu einstellen. Punkt 21 erhält keine eigene Gerätequelle. Für jeden freien Punkt gilt die Uhrgleichung. Ein positives Gewicht in (0, 1) verlangt zusätzlich die Dichtegleichung. Die neuen Punkte koppeln über die auf N22 erneut gezählten offenen Kausalintervalle. Die zugehörigen Koeffizienten für null bis drei Zwischenpunkte sind 1, −9, 16 und −8, danach null.

**Eine von Hand prüfbare Vorzeichenumkehr.** In 3 550 Anbindungen hat Punkt 19 genau die alten Vorgänger 0 und 17. Schreibe n = Y₁₉, h = Y₁₇ und m = Y₂₁. Fügt man 21 vor 19 ein, gilt −5 = Y₀ < h < m < n. Auf N21 war die Dichtevariation am neuen positiven Punkt kleiner als −182,87. Auf N22 wird dieselbe Variation zu

> D₁₉ = 19 + 16(n+5)² − 9(n−h)² + (n−m)² > 19 + 7(n+5)² > 195,64.

Beide Schranken gelten im gesamten Zielfenster. Das zusätzliche Ereignis dreht das Vorzeichen tatsächlich um. Die notwendige Nullstelle entsteht in dieser Familie bei keinem der beiden neuen Gewichte.

**Wie die übrigen Fälle geprüft wurden.** Die Aufzählung beginnt mit allen 406 142 Projektionen, einschliesslich der auf N21 schon ausgeschlossenen. Bei beiden Rollen entfallen 12 878 Anbindungen durch die Zeitordnung zum alten Rand. Liegt 21 vor 19, bleibt die Uhrgleichung von 20 bei ausschliesslich alten Randnachfolgern unverändert. Das schliesst 268 544 weitere Anbindungen aus. Liegt 21 nach 20, bleibt die Vergangenheit von 19 unverändert. In 165 588 weiteren Fällen schliesst die frühere Vorgängerprüfung den Fall aus. Pro Gewichtssektor verbleiben somit 124 720 bzw. 227 676 neu zu prüfende Feldsysteme.

Die Rechnung verengt Uhren und Gewichte mit nach aussen gerundeter Ganzzahlarithmetik. Beim Unterteilen wird ein Fall erst ausgeschlossen, wenn alle Teilboxen widersprüchlich sind. Zusätzlich werden Uhrgleichungen über Gruppen von Ereignissen summiert. Beiträge zwischen zwei Ereignissen derselben Gruppe heben sich dabei exakt auf. Wo die Unterteilung ihr Rechenbudget erreicht, steht der Fall als offen im Register. Die Randdaten überdecken 168 Teilfälle der veröffentlichten Drift-, Quellen- und Impulsfamilie. [Wirkung, Randdaten und N21-Vergleich](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/95ca8505f8b679f1ae484fb8ea08b5f97fc4ba6c/research/rax_cqg/dust_collapse/n21_vollstaendige_pruefung_des_messpaars_v0_1)

<div class="page"></div>

## Wo stationäre Messpaare tatsächlich liegen

Für zwei Anbindungen mit positivem Nachfolger wurden Lösungen des vollständigen freien Feldsystems eingeschlossen. Die drei Zeiger beginnen bei null und folgen ihren Abtastlücken mit verschwindendem Nachimpuls. Die Kalibrierkopplung −κ ist aktiv. Alle positiven Gewichte liegen strikt zwischen null und eins. Die Uhren steigen auf jeder Kausalrelation. Die alte Zeitreferenz lautet x = (Y−Y₃)/(Y₇−Y₃). Das Zielfenster reicht von 0,484375 bis 0,515625.

| Register-ID und Randpräparation | Normierte Uhr von 19 | Normierte Uhr von 20 |
|---|---:|---:|
| 216427, zentrale Drift, Senderquelle null | 0,4435093 | 0,5640688 |
| 217269, zentrale Drift, Senderquelle null | 0,4818969 | 0,4766401 |

Die Tabellenwerte sind gerundete Mittelpunkte. Für jede ausgewiesene Uhr ist der zertifizierte Einschluss schmaler als 0,00000006. Beim ersten Paar liegt das Fenster zwischen den beiden Uhren. Beim zweiten liegen beide davor. Für ID 217269 wurden zusätzlich die Driftmitte und beide Driftenden mit allen drei zugelassenen Senderquellen kombiniert. In allen neun punktweise geprüften Präparationen bleibt x₁₉ < 0,481901 und x₂₀ < 0,476647. Andere Wurzeln auf denselben Ordnungen bleiben möglich.

**Existenznachweis.** Die numerische Näherung dient nur als Zentrum. Um jedes Zentrum werden die 14 freien Uhren und 11 positiven Gewichte durch rationale Intervalle eingeschlossen. Ein exakter inverser Mittelpunkt-Jacobioperator A präkonditioniert das Gleichungssystem F. Für die Abbildung X ↦ X − A F(X) werden der normierte Mittelpunktfehler β und die Schranke q für die Ableitung mit Bruchrechnung nach oben begrenzt. In allen zehn Boxen gilt β + q < 0,001. Damit bleibt die Abbildung im Inneren der jeweiligen Box und ist dort kontrahierend. Das sichert Existenz und lokale Eindeutigkeit für die zugehörigen eingeschlossenen Randwerte.

**Anschluss.** Die 73 offenen Zeilen sind einzeln adressierbar. Bei ID 337411 im positiven Nachfolgersektor müsste jede Lösung im Fenster mindestens einen von null verschiedenen Nachimpuls und ein Gewicht unter 10⁻⁸ an Gerät 16 oder 18 haben. Für die beiden Ordnungen mit nachgewiesenen Lösungen ausserhalb des Fensters ist der nächste gezielte Test die Suche nach einem zweiten Wurzelzweig im Fenster.

**Offline nachrechnen.** Im entpackten Paket startet `python3 -B pruefen.py` die Prüfung mit Python ab 3.11 und g++ für C++17 auf Linux. Der Lauf rekonstruiert das Fallregister und die Nachweise, vergleicht die dekomprimierten Register bytegenau und prüft die zehn Existenzboxen. Offene_Faelle.tsv enthält die 73 Restfälle. P19, F19, P20 und F20 kodieren alte Vorgänger und Nachfolger als Bitmasken. Register.tsv.gz enthält alle vier Entscheidungen je Projektion. Teilungen.tsv.gz dokumentiert die vertieften Prüfungen. Eingaben, lokaler Prüfplan und die späteren Zusatzkontrollen liegen mit Prüfsummen bei.
