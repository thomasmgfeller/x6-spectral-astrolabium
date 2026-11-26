# Liegt eine zweite stationäre Lösung im Messfenster?

**CST-DUST · Staubkollaps auf einer endlichen Kausalmenge mit 22 Ereignissen · 26. November 2026**

Für die Anbindungen **216427** und **217269** ist die Frage entschieden. Es gibt in der untersuchten N22-Familie keine stationäre Lösung, bei der beide Messuhren im Fenster [31/64, 33/64] liegen. Der Ausschluss gilt für alle drei zugelassenen Senderquellen, das ganze Driftintervall und alle drei zugelassenen Nachimpulse. Er umfasst auch beliebig kleine positive Gewichte an den beiden Geräten.

**Weshalb gerade diese Fälle?** Auf beiden Ordnungen existiert bereits eine stationäre Lösung der vollständigen Feldgleichungen. Die Lage der Uhren in diesen Lösungen liess offen, ob ein weiterer Zweig dieselben Messpunkte ins Fenster bringen könnte. Punkt 19 trägt positives Gewicht, Punkt 20 Gewicht null. Die beiden sind kausal unvergleichbar und haben gemeinsame materielle Anker. Punkt 21 ist ein positiver unmittelbarer Nachfolger von 20. Nur die Uhren von 19 und 20 müssen im Fenster liegen. [N22-Ausgangspunkt auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/75991ca0c97a60ce1400002ef856ec94626b2c99/research/rax_cqg/dust_collapse/n22_ein_drittes_ereignis_fuer_die_staubrandmessung_v0_1)

| Anbindung | Uhr 19 der Referenzlösung | Uhr 20 der Referenzlösung |
|---|---:|---:|
| 216427 | 0,4435093 | 0,5640688 |
| 217269 | 0,4818969 | 0,4766401 |

Die Zahlen sind gerundete Mittelpunkte der erneut zertifizierten Lösungen bei zentraler Drift, Quelle null und verschwindenden Nachimpulsen. Das Fenster reicht von **0,484375 bis 0,515625**. Bei der ersten Referenzlösung liegt je eine Uhr auf jeder Seite des Fensters. Bei der zweiten liegen beide davor. Die Rechnung lässt weitere Lösungen ausserhalb des Fensters offen.

**Zehn weitere Ausschlüsse.** Eine Auswahl nach der Kausalstruktur ergab zehn weitere offene Anbindungen, auf die dieselbe Prüfung anwendbar ist. Alle zehn verfehlen die notwendige Stationaritätsbedingung im gemeinsamen Fenster. Darunter ist **337411**, für die zuvor gerade der Bereich mit nichtverschwindendem Nachimpuls und sehr kleinem Gerätegewicht offen war.

| N22-Register | Ausgeschlossen | Offen |
|---|---:|---:|
| Vor dieser Prüfung | 1 624 495 | 73 |
| Nach dieser Prüfung | **1 624 507** | **61** |

<div class="page"></div>

## Wie der Ausschluss zustande kommt

Auf allen zwölf gewählten Ordnungen liegen die Ereignisse 15 bis 21 kausal zwischen 0 und 7. Zwischen diesen sieben Ereignissen und den sieben freien Staubereignissen gibt es keine direkten Beiträge mit von null verschiedenem Schichtkoeffizienten. Deshalb muss jede Lösung des vollen Systems bereits vier Dichte- und sieben Uhrbedingungen dieses Teilsystems erfüllen. Die freie Uhr von Ereignis 21 darf den gesamten kausal zugelassenen Bereich durchlaufen.

Für ein geordnetes Ereignispaar i, j ist cᵢⱼ durch die Zahl der Ereignisse im offenen Ordnungsintervall festgelegt. Bei null bis drei Zwischenereignissen lautet der Koeffizient 1, −9, 16 oder −8, danach null. Mit Rohuhren Y und Gewichten w lauten die reinen Staubbeiträge

> Dⱼ = 19 + Σᵢ cᵢⱼ (Yⱼ − Yᵢ)²  
> Gⱼ = Σₖ cⱼₖ wₖ (Yₖ − Yⱼ) − wⱼ Σᵢ cᵢⱼ (Yⱼ − Yᵢ).

An 19 und 21 gilt D = 0, an 19 bis 21 gilt G = 0. Für 15 bis 18 sind die Gerätebeiträge zur Uhrbedingung durch 10⁻⁸ eingeschlossen. An 16 und 18 gilt D ≤ 2,001 × 10⁻⁶. Ab Gerätegewicht 10⁻⁸ gilt auch die entsprechende untere Schranke. Darunter wird nur die obere verwendet, weil die positive Trägheitslast bei kleinem Gewicht anwachsen kann.

**Überdeckung.** Die Driftabweichung liegt in [−10⁻⁶, 10⁻⁶], die Quelle bei −10⁻⁶, 0 oder +10⁻⁶. Für jede der drei Nachimpulskomponenten gilt |vₐ| ≤ 1,12 × 10⁻¹² bei κ = 10⁻¹¹. 256 geschlossene Driftintervalle ergeben mit den drei Quellen 768 geprüfte Parameterzellen. Die gemeinsame Randhülle überdeckt alle diese Eingaben. Die Normierung x = (Y − Y₃)/(Y₇ − Y₃) wird mit nach aussen gerundeten Randuhren umgerechnet. Für jedes der beiden Geräte werden die Gewichtsbereiche [0, 10⁻⁸] und [10⁻⁸, 1] gekreuzt. Dadurch sind die Übergänge und beide Klein­gewichtsbereiche abgedeckt.

Die Restfunktionen sind höchstens quadratisch in den elf freien Variablen. Ihre Änderung längs einer Strecke folgt exakt aus der Ableitung im Streckenmittelpunkt. Rationale Zeilenkombinationen dieser Gleichungen verschärfen die Intervallschranken. Eine numerische Matrix wählt die Kombinationen. Jeder Ausschluss wird mit nach aussen gerundeter Ganzzahlarithmetik geprüft. Jede Teilung überdeckt die gesamte Elternbox.

**Ergebnis der Überdeckung.** In den 48 Suchbäumen enden alle 254 242 Blattboxen in einem Widerspruch. Für 216427 waren 180 162 Blattboxen erforderlich, für 217269 waren es 10 639. Das Maschinenprotokoll führt alle vier Gewichtsbereiche jeder Anbindung einzeln auf.

<div class="page"></div>

## Kontrollen und offene Messung

Die zwei veröffentlichten Referenzlösungen wurden mit allen 25 freien Feldgleichungen erneut eingeschlossen. In beiden Fällen ist die Summe aus normiertem Mittelpunktfehler und Kontraktionsschranke kleiner als 0,001. Mit den Referenzuhren darf der neue Ausschlusstest keine der beiden Lösungsboxen verwerfen. Beide Kontrollen bestanden.

Eine zweite Ordnungsrekonstruktion erzeugt die Schichtkoeffizienten aus dem transitiven Abschluss. Exakte symmetrische Differenzen der diskreten Wirkung prüfen an einem rationalen Testpunkt je Ordnung die elf Staubbeiträge und alle 121 Einträge ihrer Ableitung. Alle **1 584 Vergleichswerte** sind in den berechneten Intervallen enthalten.

| Neu entschiedene B+-Anbindungen | Register-IDs |
|---|---|
| Gezielte Suche nach weiteren Wurzeln | 216427, 217269 |
| Ergänzende Auswahl nach Kausalstruktur | 216428, 216632, 216998, 217063, 337061, 337062, 337411, 372758, 373022, 373026 |

**Wo die Suche weitergeht.** Von den 61 offenen Fällen haben sechs einen leeren Vorgänger von 19, fünfzehn einen positiven Vorgänger von 19 und vierzig einen positiven Nachfolger von 20. Bei 31 dieser vierzig trennen sich die Geräte- und Staubgleichungen weiterhin. Dort fehlt mindestens eine der geprüften Kausalrelationen zu Referenzereignis 7. In 21 Fällen betrifft das allein Messpunkt 19, dessen Uhr bereits durch das Messfenster beschränkt ist. Diese 21 bilden die erste Gruppe für den Anschluss. Die fehlenden Relationen stehen für jede ID in Ergebnisse.json.

Ein Messpaar im gemeinsamen Fenster ist eine notwendige Bedingung der hier untersuchten Randmessung. Die zwölf Ausschlüsse betreffen endliche etikettierte Ordnungs- und Gewichtsfälle. Der physische Arealradius bleibt offen. Alle 60 P3-Prüfpunkte stehen auf NOT_RUN.

**Offline nachrechnen.** Im entpackten Prüfarchiv startet `python3 -B pruefen.py` die Rekonstruktion mit Python ab 3.11 und g++ für C++17 unter Linux. Sie benötigt nur die enthaltenen Eingaben. Ergebnisse.json enthält Randhülle, Suchbäume und Kontrollschranken. Offene_Faelle.tsv enthält die 61 verbliebenen Zeilen mit den ursprünglichen IDs. Die letzte Spalte dieser Tabelle stammt aus der früheren Zusatzprüfung mit begrenzter Trägheitslast. SHA256SUMS umfasst Eingaben, Prüfplan, Erweiterung und Ergebnisse.
