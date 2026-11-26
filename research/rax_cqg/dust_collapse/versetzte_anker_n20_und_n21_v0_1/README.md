# Welche zeitlichen Anker können die Staubrandmessung tragen?

**CST-DUST · Forschungsnotiz 0.1 · 26. November 2026**

Die N19-Aufzeichnung enthält im Zielfenster x = 1/2 ± 1/64 zwei positive, kausal geordnete Ereignisse. Die Vorstudie untersuchte zwei neue Messpunkte zwischen genau diesen Ankern. Jetzt dürfen ein früherer und ein späterer Anker den Messbereich von ausserhalb des Fensters umschliessen. Der Versuch übernimmt die veröffentlichten Randuhren und -gewichte, Quellen und Gerätekopplungen. Die Kennungen der alten Ereignisse bleiben bei der Zählung unterscheidbar. [Ausgangspunkt und N21-Wirkungsprüfung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/9c732c5b94482130b8a8286caa64e1bf86885091/research/rax_cqg/dust_collapse/n21_gemeinsame_stationaritaet_im_zielfenster_v0_1)

| Versuch | Ergebnis im Zielfenster |
|---|---|
| Ein neuer leerer Punkt, vorhandener materieller Messpunkt | Alle 570 zulässigen N20-Anbindungen scheitern auch bei frei variierenden Innenfeldern. Materieller Kandidat ist 16 oder 18. |
| Ein neuer positiver und ein neuer leerer Punkt zwischen den zeitlich nächsten äusseren Ankern | Die Anker sind 12 und 14. Alle vier N21-Anbindungen scheitern an der Dichtegleichung des neuen positiven Punkts. |
| Zwei neue Punkte bei freier Wahl alter gemeinsamer Anker | Ein Kandidat benötigt mindestens eines der Ereignisse 15–18 in der Vergangenheit des neuen positiven Punkts. 42 716 etikettierte Anordnungen passieren drei notwendige Vorprüfungen. Ob die beiden neuen Punkte gleichzeitig alle Feldgleichungen erfüllen, erfordert eine weitere Prüfung. |

**Physische Bedeutung.** Eine Staubrandmessung braucht einen materiellen und einen als aussen identifizierten geometrischen Bereich. Der Versuch verlangt zunächst nur einen positiven und einen unvergleichbaren leeren Punkt, die beide im Zielfenster liegen und gemeinsame alte positive Anker auf beiden Zeitseiten haben. Schon diese schwächere notwendige Bedingung lässt sich für die untersuchten N20-Modelle nicht stationär realisieren. Ein Punkt mit Gewicht null allein würde auch bei einem Treffer noch keine äussere Oberfläche nachweisen. Die acht physischen Radiuswerte für zwei Massen und vier Dichten bleiben offen. Alle 60 P3-Einträge stehen auf NOT_RUN.

<div class="page"></div>

## Alle einzelnen Einfügungen

Die vollständige Vergangenheit P des neuen leeren Punkts z ist ein altes Vergangenheitsideal, die Zukunft F ein alter Zukunftsfilter. P und F sind disjunkt und jedes Element von P muss vor jedem Element von F liegen. Diese Bedingungen sind notwendig und hinreichend dafür, dass die alte induzierte Ordnung erhalten bleibt. Die Aufzählung ergibt 1 017 etikettierte Einfügungen. Zwei Verfahren, eines über die topologische Reihenfolge und eines über die Abschlüsse von Antiketten, liefern dieselben Ideale. Eine Darstellung durch ineinander enthaltene Ideale bestätigt die vollständige Liste der Einfügungen.

Von diesen 1 017 gestatten 570 einen alten positiven Punkt m = 16 oder 18, der mit z unvergleichbar ist, sowie mindestens ein gemeinsames altes positives Ankerpaar. Eine Ordnung wird einmal gezählt, auch wenn sie mehrere Marken oder Ankerpaare erlaubt. Auf der archivierten N19-Feldlösung können 404 dieser Ordnungen dem neuen Punkt überhaupt eine kausal zulässige Uhr im Fenster zuweisen. Ihre sieben unterschiedlichen Zukunftsfilter bestimmen eine einfache erste Prüfung.

> G(z) = Σ cⱼ wⱼ (Yⱼ − z) = 0, j in F.

Diese Gleichung folgt durch Variation der neuen leeren Uhr. Die eingehenden Beiträge verschwinden mit ihrem Gewicht. Nach 0, 1, 2 oder 3 Zwischenereignissen beträgt der Intervallkoeffizient 1, −9, 16 bzw. −8. Für grössere Intervalle ist er null. Bei festen alten Feldern ist G affin in z. Daher genügen die Endpunkte jedes zeitlich zulässigen Bereichs. Die anschliessenden Intervalle sind nach aussen gerundet.

| Alte Zukunft von z | Einfügungen mit zeitlicher Überlappung | Intervall für G(z) |
|---|---|---|
| 7,8,9,10 | 94 | [−0,01665; −0,00736] |
| 14 und 7,8,9,10 | 17 | [−0,00952; −0,00613] |
| 14,18 und 7,8,9,10 | 3 | [0,03362; 0,03675] |
| 18 und 7,8,9,10 | 8 | [−0,01033; −0,00730] |
| 8,9,10 | 94 | [0,17935; 0,19543] |
| 9,10 | 94 | [−0,16321; −0,15348] |
| 10 | 94 | [0,01865; 0,01977] |

Die Eingaben überdecken die drei Quellen, sieben geschlossene Driftzellen und alle drei unabhängig zugelassenen Nachimpulse. Jede Driftzelle wurde achtfach unterteilt. In den 168 Teilfällen wird zuerst die stationäre N19-Referenz überprüft. Die weitere N20-Prüfung übernimmt jeweils nur die Hülle der acht Randuhren und ihrer Gewichte. Der Zeitbezug bleibt x = (Y−Y₃)/(Y₇−Y₃).

<div class="page"></div>

## Was bei freien Innenfeldern geschieht

Erneut gehen alle 570 Ordnungen in die Prüfung ein, einschliesslich der 166 Fälle, denen auf den alten Feldern bereits ein kausaler Zeitpunkt fehlte. Die alten freien Uhren und positiven Gewichte dürfen sich neu einstellen. Es gelten die strikte Uhrordnung und 0 < w < 1 im positiven Sektor. Die Punkte 15 und 17 bleiben alte Nullereignisse. Das Gerät behält seine bisherigen kausalen Abtastpaare, auch wenn die Einfügung aus einem alten Link eine Relation mit Zwischenpunkt macht. An z greift kein Gerätekanal an.

**400 Ordnungen mit ausschliesslich künftigen Kragenereignissen in F.** Die neue Uhrgleichung enthält ausschliesslich feste Randfelder. Sie verfehlt null auf dem ganzen Zielfenster, unabhängig von der Bewegung aller alten Innenfelder. Für diese Aussage ist selbst ein weiterer neuer Punkt unschädlich, sofern er mit z unvergleichbar bleibt. Er kann dann zu keinem offenen Intervall zwischen z und einem Nachfolger von z gehören.

**161 weitere Ordnungen.** Zuerst werden die Zeitordnung zum Kragen und die sieben freien Staubfelder auf der Seite 4,5,6,11,12,13,14 geprüft. Die Dichtegleichungen sind in der jeweiligen Uhr höchstens quadratisch. In kausaler Reihenfolge werden alle Wurzeln eingeschlossen. Bei festem z folgen die Gewichte in umgekehrter Reihenfolge aus den Uhrgleichungen. Enthält ein Nenner null, wird das gesamte zulässige Gewicht freigegeben oder die Gleichung durch Intervallvergleich ausgeschlossen. Für den neuen Punkt wird der verbleibende Uhrgradient auf jedem überlebenden Zweig geprüft. Bei 17 Ordnungen mit 14 als einzigem innerem Nachfolger bestätigt zusätzlich die direkte Eliminierung von w₁₄ aus den beiden Uhrgleichungen das Ergebnis.

**9 Ordnungen auf dem Empfängerzweig.** Nur Ereignis 16 kommt jeweils als materieller Partner infrage. Seine Uhr und die neue leere Uhr liegen im Zielfenster. Die Empfängeruhr darf über das Fenster hinaus bis zum künftigen Kragen laufen. Aus G(z) = 0 wird zunächst das Produkt w₁₈(Y₁₈−z) eingeschlossen. Die Nulluhrgleichung an 17, Senderdichte und Senderuhr, die Uhrgleichung an 15 sowie Empfängerdichte und Empfängeruhr begrenzen die übrigen Variablen. Die Fallteilung bei w₁₆ = 10⁻⁶ umfasst auch beliebig kleine positive Sendergewichte. Jede Teilbox widerspricht mindestens einer notwendigen Bedingung.

**Kontrollen.** Bei unabhängig um ±10⁻⁶ erweiterten künftigen Randgewichten und um ±10⁻⁴ erweiterten Rohuhren 8–10 bleiben alle 570 Ausschlüsse bestehen. Die Uhr 7 bleibt für die Normierung fest. Exakte symmetrische Differenzen der Feldwirkung bestätigen 570 neue Uhrgradienten und 292 weitere Variationen. Eine synthetische Gegenprobe mit bekannter stationärer leerer Uhr liefert die erwartete Null zwischen zwei entgegengesetzten Vorzeichen.

<div class="page"></div>

## Zwei neue Punkte und der nächste Suchbereich

Auf der ursprünglichen N19-Familie liegt der nächste alte positive Punkt unterhalb des Fensters bei x ≈ 0,45929 (Ereignis 12), der nächste oberhalb bei x ≈ 0,82904 (Ereignis 14). Sie sind durch einen Link verbunden. Nun werden ein neuer positiver Punkt n und ein neuer leerer Punkt z unvergleichbar zwischen diese Anker gesetzt. Zur Prüfung bleiben die Ankerkennungen fest. Ihre inneren Feldwerte werden aus den notwendigen Gleichungen bestimmt.

Jeder neue Punkt kann Ereignis 13 zusätzlich in seine Vergangenheit aufnehmen. So entstehen genau vier volle Ordnungen. Die freie Uhr von z verlangt w₁₄(Y₁₄−z) − 9w₇(Y₇−z) + 16w₈(Y₈−z) − 8w₉(Y₉−z) = 0. Eine Entscheidung gelingt bereits am positiven Punkt n. Seine Dichtevariation lautet D = 19 + Σ cᵢ(n−Yᵢ)². Die alten Vorfahren von n spüren auf ihren Dichteachsen keine neue Intervallunterteilung. Ihre Uhren lassen sich in allen kausal zulässigen Wurzeln aus den früheren Randuhren bestimmen.

| Alte Vergangenheit von n | Befund für D im Zielfenster |
|---|---|
| Ohne 13 | D > 45,53 für beide Anbindungen des leeren Punkts. Die quadratische Gleichung hat keine reelle Wurzel. |
| Mit 13 | D > 12,88 für beide Anbindungen des leeren Punkts. Die beiden reellen Rohzeitwurzeln liegen bei rund −1,95505 und 1,34467, ausserhalb des Zielfensters. |

**Folgerung über dieses Ankerpaar hinaus.** Die zusätzliche Untersuchung umfasst alle 18 nichtleeren alten Vergangenheitsideale von n, die nur den Vergangenheitskragen und den gerätefreien Staubzweig enthalten und einen alten positiven Zukunftsanker erlauben. In 17 Fällen gibt es keine kausal zulässige Wurzel im Zielzeitfenster. Ein Ideal scheitert bereits an der Zeit eines Vorgängers. Deshalb muss bei zwei neuen unvergleichbaren Messpunkten mindestens eines der alten Ereignisse 15, 16, 17 oder 18 vor n liegen. Ein Ereignis des künftigen Kragens kann bei dieser Zielzeit kein Vorgänger sein.

**Verbleibende Kandidaten.** Eine vollständige Kombination zweier Einfügungen mit gemeinsamen alten positiven Ankern und ohne erzwungene Vergleichbarkeit der neuen Punkte liefert 406 142 etikettierte Anordnungen. Die Zeitordnung zu den Kragen lässt 393 264, die Bedingung an die Vergangenheit von n noch 227 676 zu. Der Ausschluss einer reinen Kragenzukunft von z reduziert diese Zahl auf 42 716. Der Wert zählt Kandidaten nach genau diesen drei Vorprüfungen. Er kann bereits anderweitig ausgeschlossene Fälle enthalten. Die nächste gezielte Rechnung betrifft die gemeinsamen Nulluhr- und Dichtegleichungen dieser Gerätezweige, bevor einzelne Radien abgelesen werden können.

**Nachrechnen.** Im entpackten Ordner mit Python 3.11 oder neuer `python3 -B pruefen.py` ausführen. Alle Quellen, der lokale Prüfplan, die beiden nachträglichen Ergänzungen und die rationalen Intervallzertifikate sind enthalten. Der Prüfer vergleicht die Ergebnisse bytegenau mit Ergebnisse.json. [Veröffentlichter Ausgangsstand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/400)
