# N23 · Gemeinsam neu gelöste Innenfelder am frühen Schnitt

Für jede der beiden Kragenpräparationen besitzt eine freie leere Sonde bei fünf der 25 geprüften Ordnungen eine stationäre Lösung im Fenster [15/32,17/32]. Für die übrigen 20 ist eine solche Lösung in diesem Fenster ausgeschlossen. Auf allen nachgewiesenen Lösungszweigen liegen dort ausschliesslich die leeren Ereignisse 17, 20 und 22. Die beiden aus N22 übernommenen Massenablesungen verfehlen die bisherige 2-%-Toleranz. Die Studie schliesst damit die in [PR 413](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/413) begonnene Existenzprüfung für diese beiden endlichen Listen ab.

## Welche Fälle umfasst das Ergebnis?

Die archivierten Eingaben stammen vom [Merge-Commit 3b34531](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/3b34531303a2ce81e83940c2ba4986b9d0fdc7cb). Der N22-Vergleich verwendet die schwere und leichte Präparation aus [PR 412](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/412). PR 413 hatte unter festgehaltenen alten Feldern zwei nichtleere Nachfolgermengen mit einer möglichen Nullstelle der Sondenuhrgleichung im Fenster gefunden. Für diese beiden Mengen waren vier bzw. 21 Vergangenheiten aufgelistet. In jedem dieser Versuche verletzte das unveränderte alte Feld eine Dichtegleichung. Hier dürfen alle 15 freien Uhren und alle elf positiven Innengewichte gemeinsam variieren. Die alten Randfelder, der positive Sektor und die Nullquelle bleiben vorgegeben. Die vier leeren Gewichte an 15, 17, 20 und 22 werden auf null festgelegt. Ihre Uhren sind frei.

Die Grundgesamtheit umfasst die vorher aufgelisteten 25 Ordnungen. Andere Vergangenheiten oder Zukünfte können bei geänderten alten Feldern generell neu in Betracht kommen. Eine Aussage über alle N23-Erweiterungen oder geänderte Materialsektoren ist daraus nicht ableitbar. Die erfolgreichen Lösungen liegen im Fenster, jeweils neben dessen Mittelpunkt. Die physische Radius- oder Masseneichung bleibt offen.

| Zukunft von 22 | Vergangenheiten geprüft | Vergangenheiten mit nachgewiesener Lösung je Präparation | Im Fenster ausgeschlossen je Präparation |
|---|---:|---|---:|
| 7,8,9,10,14,21 | 4 | ∅, {0}, {0,1} | 1 |
| 7,8,9,10,18,21 | 21 | ∅, {0} | 19 |

Das gibt zehn positive Existenzentscheide und vierzig Ausschlüsse, wenn die beiden Präparationen einzeln gezählt werden. Bei den drei bzw. zwei erfolgreichen Ordnungen stimmen innerhalb einer Präparation alle freien Gleichungen überein. Die zusätzlichen Vorgänger betreffen ausschliesslich wirkungslose Terme für das fest leere Gewicht oder feste Randzeilen. Die verschiedenen strikten Ordnungsbedingungen werden für jede Ordnung gesondert geprüft. Auch die für die frühe Schnittladung relevanten Terme stimmen überein. Vier verschiedene Lösungsboxen reichen daher für die zehn Existenzentscheide.

## Uhren und Massendiagnosen

x ist (Y−Y₃)/(Y₇−Y₃). Die Kontrollradien 1 und 2 aus PR 413 werden nicht als Referenzmessung verwendet. Q=−ΣGᵢ für i=0,1,2,3 ist die frühe Ladung. B=Σwⱼ/(Y₇−Y₃) summiert die elf positiven Innengewichte. Die Umrechnungen M_Q=4Q/Q* und M_B=4B/B* behalten genau die N22-Normierungen bei.

| Zusätzlicher innerer Nachfolger neben 21 | Präparation | x₂₂ | x₁₉ | M_Q | M_B |
|---|---|---:|---:|---:|---:|
| 14 | schwer | 0,48598327 | 0,54353452 | 4,181876 | 4,467696 |
| 14 | leicht | 0,48004446 | 0,53808819 | 0,262159 | 0,275972 |
| 18 | schwer | 0,51610684 | 0,53754441 | 4,175324 | 4,527337 |
| 18 | leicht | 0,51030529 | 0,53203679 | 0,261756 | 0,279741 |

Die bisherigen Sollwerte sind 4 und 1/4. Beide Massenablesungen liegen bei allen vier Zweigen oberhalb des 2-%-Intervalls. Der knappste positive Messpunkt ist Ereignis 19 im leichten Fall mit Nachfolger 18. Seine untere Uhrgrenze liegt mehr als 0,00078678 über der Fensterobergrenze 0,53125. Die in beiden N22-Präparationen verfügbaren Kontakte zwischen positiven und leeren Ereignissen fehlen auf diesen N23-Zweigen. Die Existenzzertifikate gelten lokal um die jeweilige Lösung. Weitere stationäre Zweige der fünf erfolgreichen Ordnungen werden dadurch nicht ausgeschlossen.

## Gleichungen und Existenzzertifikat

Es gilt die veröffentlichte Schichtregel kᵢⱼ=1,−9,16,−8 für null bis drei Ereignisse im offenen Intervall und sonst null. An den vier ursprünglichen Gerätekanten (15,16), (16,18), (17,18), (18,7) wird 10⁻¹¹ abgezogen. Die Schichten werden auf jeder neuen transitiven Ordnung neu gezählt. Für jede positive innere Dichte gilt Dⱼ=19+Σᵢ kᵢⱼ(Yⱼ−Yᵢ)²=0. Für jede freie Uhr gilt

Gᵢ = Σⱼ kᵢⱼ wⱼ(Yⱼ−Yᵢ) − wᵢ Σₕ kₕᵢ(Yᵢ−Yₕ) = 0.

Damit werden je Ordnung elf Dichte- und fünfzehn Uhrgleichungen geprüft. Das alte N22-Innenfeld liefert nur Startvorschläge. Für die Lösung wird die quadratische Abbildung in allen 26 Koordinaten verwendet. Mit einem gerundeten rationalen Vorkonditionierer C wird x↦x−C F(x) auf einer geschlossenen Box geprüft. Für feste Kragenparameter ist die Abbildung dort kontrahierend und bildet die Box strikt in sich ab. Die Parametereinschlüsse decken die veröffentlichten Kragenintervalle ab. Die grösste obere Schranke der gewichteten Kontraktionsnorm liegt unter 0,0000016. Die grösste obere Schranke der relativen Bildausdehnung einschliesslich Restfehler liegt unter 0,000523. C ist invertierbar, weil CF′ in dieser Norm von der Identität um weniger als eins abweicht. Der Fixpunkt ist somit eine Nullstelle. Alle strikten Relationen, Gerätebereiche, die freien Residuen und der Bereich 0<w<1 werden im Anschluss auf der Lösungsbox geprüft. Für diese Rechnung werden nur die gedruckten rationalen Startwerte und die Standardbibliothek benötigt.

## Ausschlussbeweise

Bei der kleineren Zukunft und der Vergangenheit {0,1,2} liefert die Dichtegleichung an 21 einen direkten Widerspruch. Ihre einzigen Koeffizienten sind +16 an 15, −9 an 16 und jeweils +1 an 17,19,20,22. Wegen 15≺16≺21 gilt Y₂₁−Y₁₅>Y₂₁−Y₁₆>0. Schon die ersten beiden quadratischen Beiträge haben daher eine strikt positive Summe. Die erforderliche Dichtevariation ist grösser als 19. Dieser Ausschluss gilt sogar ohne Beschränkung der Sondenuhr auf das Fenster.

Für die zweite Zukunft werden die 19 Ausschlüsse mit rationalen Ungleichungen nachgewiesen. Die folgenden Einzelheiten legen die für die Zertifikate benutzten notwendigen Bedingungen offen.

1. Für die positiven Innenpunkte 16,18,19,21 werden die Dichtegleichungen beibehalten. Für das positive terminale Ereignis 21 ergibt die freie Uhrgleichung Σᵢ kᵢ₂₁(Y₂₁−Yᵢ)=0. Damit lässt sich Y₂₁ nach oben begrenzen. Die übrigen benötigten inneren Uhren ausser 22 haben den kausalen Nachfolger 7. Der frühe Kragen und das Sondenfenster geben die weiteren Uhrschranken.
2. Liegt eines der alten leeren Ereignisse e=17,20 vor 22, schreibe z=Y₂₂ und W=w₁₈+w₂₁. Aus G₂₂=0 folgt w₁₈(Y₁₈−z)+w₂₁(Y₂₁−z)=L(z). Hier ist L(z) die Summe cⱼ wⱼ(Yⱼ−z) über 7,8,9 mit c=(9,−16,8). Aus Gₑ=0 folgt H(z)+(z−Yₑ)(C−9W)=δ. Dabei verwendet H dieselbe Summe mit c=(−65,136,−72), C=16w₇−8w₈, und δ ist 10⁻¹¹ w₁₈(Y₁₈−Y₁₇) für e=17 und sonst null. Im gesamten Fenster sind H<0, L>0, δ≥0. Aus Y₀<Yₑ<z folgen W≤(C+H/(z−Y₀))/9 und Yₑ≤z+H/C. Die exakte Fensterüberdeckung liefert Y₂₁>3,2955, Yₑ<−1,1841 sowie W<0,00270 im schweren bzw. W<0,00270/16 im leichten Fall. Y₂₁ kann hier als terminale Uhr hinter dem späten Normierungsereignis liegen und wird nicht künstlich auf das Intervall bis Y₇ beschränkt.
3. Für einen alten leeren Punkt, dessen Zukunft durch die neue Sonde unberührt bleibt, ist die Differenz seiner Uhrgleichung zu G₂₂ linear in z−Yₑ. Wenn der andere Punkt vor 22 liegt, ist der Betrag der Steigung durch die Schranke für W nach unten begrenzt. Die Gerätekorrektur bewirkt eine Rohuhrenabweichung unter 10⁻⁶. Liegen beide Punkte vor 22, folgt dieselbe Schranke für |Y₁₇−Y₂₀| aus der Steigung C−9W. Liegt keiner vor 22, hat 20 exakt dieselbe Uhr wie 22. Die gemeinsame Steigung kann dann nicht verschwinden, da die zusätzliche Korrektur an 17 wegen w₁₈>0 und 17≺18 strikt von null verschieden ist.
4. Die ausgehende Impulssumme an 18 in Richtung des späten Kragens ist im benötigten Bereich negativ, einschliesslich der Gerätekorrektur (18,7). Bei vorangehendem leerem Punkt liefert dies mit der oberen Schranke für W auch Σᵢ kᵢ₁₈(Y₁₈−Yᵢ)<−3. Für die Vergangenheit {0,1,2,15,16} werden zusätzlich alle Uhrgleichungen 15 bis 22 berücksichtigt. Die leichten positiven Gewichte dürfen dazu mit 16 multipliziert werden, da diese Uhrgleichungen in den beteiligten Gewichten homogen sind. Für die gesamte gemeinsame Kragenhülle werden Rundungsfehler der späten Daten in den Uhrgleichungen mit einer explizit geprüften Reserve unter 10⁻⁷ eingeschlossen.
5. Quadratische Monome werden als zusätzliche Variablen geführt. Intervallproduktgrenzen, die vier linearen McCormick-Ungleichungen sowie Tangenten und Sekanten an Quadrate kausaler Uhrdifferenzen sind notwendige Bedingungen. Pro Teilbox ergibt eine nichtnegative rationale Kombination dieser Ungleichungen eine linke Seite, deren kleinster zulässiger Wert strikt über der rechten Seite liegt. Leere Ausgangsintervalle zählen ebenfalls als Ausschluss. Die Teilungen überdecken jeweils beide geschlossenen Hälften. Insgesamt werden für die 19 Nachweise 82 Endboxen geprüft. Die Gewichte der Beweiszeilen und die Teilungsbäume enthält Lineare_Zertifikate.json. Ein numerischer Optimierer wurde zum Auffinden der Vorschläge benutzt. Der Prüflauf prüft die Widersprüche mit exakten Brüchen ohne diesen Optimierer.

## Reproduktion und Forschungsstand

Nach dem Entpacken im Studienverzeichnis ausführen. Python ab 3.10 mit Standardbibliothek genügt.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
python3 -B gegenprobe.py
```

Die Gegenrechnung zählt sämtliche Schichten über Vorgänger-/Nachfolgerschnitte neu, summiert die ein- und ausgehenden Gleichungen separat und kontrolliert die Jacobi-Matrix aller vier Lösungszeugnisse an den Mittelpunkten durch exakte symmetrische Differenzen. Der Hauptlauf prüft die Ausschlusszertifikate sowie die gespeicherte Ausgabe byteweise. Fallregister.tsv enthält 50 Zeilen für die Kombinationen von Ordnung und Präparation. Stationaere_Feldboxen.json enthält die vier vollständigen kontinuierlichen Feldboxen, Uhren, Gewichte und beide Massenablesungen. Ergebnisse.json ordnet sämtliche Ordnungen den Zeugnissen zu.

Die vier primären Vergangenheiten standen vor der Rechnung fest. Der Vergleich mit den weiteren 21 folgte nach dem ersten numerischen Befund. Die internen Prüfpläne besitzen Prüfsummen. Eine öffentliche Blindregistrierung erfolgte nicht. Die physische Masseneichung, der äussere Rand und seine Eigenfläche bleiben offen. Die acht physischen Pilotradien und alle 60 P3-Prüfpunkte bleiben NOT_RUN.
