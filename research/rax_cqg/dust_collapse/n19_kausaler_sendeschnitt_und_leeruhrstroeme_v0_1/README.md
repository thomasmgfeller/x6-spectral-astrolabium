# CST-DUST · Was lässt sich vor dem N19-Sender präparieren?

**26. November 2026.** Der kausale Vorlauf des Senders 16 enthält drei positive Kragenuhren und die leere Uhr 15. Die ursprüngliche Staubwirkung auf diesem Vorlauf lässt den Wert der leeren Uhr vollständig frei. Sobald ein positiver Sender hinzukommt, trägt er an dieser Uhr den strikt positiven Strom w₁₆(Y₁₆−Y₁₅) bei. In jedem der 32 kausal abgeschlossenen Teilstücke, die den Sender und noch nicht den Empfänger enthalten, ist das der einzige Beitrag zur Uhrgleichung an 15.

Wird Y₁₅ vorgegeben, liefert die ursprüngliche Dichtegleichung eine exakte Vorhersage für die Senderuhr. Bei festem Vorlauf verlangt aber jeder der beiden geprüften Pulse eine andere Strombilanz über dem ersten Sendeschnitt. Hält man stattdessen auch den Zukunftskragen auf seinen Referenzwerten, verändert sich im stationären Lösungszweig bereits Y₁₅. Die Zuordnung von Y₁₅ zu einer physisch vorbereiteten Anfangsgrösse bleibt offen.

## Die Wirkung am Schnitt

Ein Ordnungsideal enthält mit jedem seiner Ereignisse sämtliche kausalen Vorgänger. Wir wählen D als die strikte Vergangenheit des Senders z=16. Aus der Ordnung folgt D={0,1,2,15}. Sein Komplement E umfasst auch mit dem Sender unvergleichbare Ereignisse. Die festen Anfangskragen umfassen 0,1,2,3. Die beiden Mengen sind daher verschieden.

Wir benutzen A=19 Σⱼ wⱼ + Σᵢ≺ⱼ bᵢⱼwⱼ(Yⱼ−Yᵢ)² und Gᵢ=−½∂A/∂Yᵢ in den bisherigen Modell­einheiten. Jeder Volumenterm geht entweder in A_D oder in A_E ein. Von den 80 Paaren mit nichtverschwindendem Schichtkoeffizienten liegen sechs ganz in D, 51 ganz in E und 23 über dem Schnitt. Paare mit verschwindendem Gewicht des Zielereignisses können trotz ihres Schichtkoeffizienten einen verschwindenden Wirkungsbeitrag haben. Für j in E definieren wir

    nⱼ = Σᵢ∈D bᵢⱼ,   tⱼ = Σᵢ∈D bᵢⱼ Yᵢ,   sⱼ = Σᵢ∈D bᵢⱼ Yᵢ².
    A = A_D + A_E + Σⱼ∈E wⱼ(nⱼYⱼ² − 2tⱼYⱼ + sⱼ).

Auf der festgehaltenen Ordnung lassen sich die drei Koeffizienten für jeden gegebenen Zielpunkt aus der Ordnung und den frühen Uhren berechnen. Für seine äussere Dichtegleichung trägt die Klammer bei, für seine Uhrgleichung in der Normierung ∂A/∂Yⱼ der Term 2wⱼ(nⱼYⱼ−tⱼ). Die 4×4-Teilmatrix von b für die frühen Zeilen 0,1,2,15 und die äusseren Spalten 3,4,11,16 hat exakt die Determinante −1472. Die vier linearen Summen tⱼ unterscheiden damit alle vier frühen Uhrwerte, wenn diese frei variiert werden. Die drei positiven Kragenuhren sind in den Quellenversuchen fest vorgegeben.

**Was fehlt an Ereignis 15?** Alle in D eingehenden Terme nach 15 tragen den Faktor w₁₅=0. In D geht von 15 kein Term aus. Somit ist A_D für jeden Wert von Y₁₅ gleich. Der spätere Beitrag b₁₅,₁₆w₁₆(Y₁₆−Y₁₅)² macht die Uhr für die Sendergleichung wirksam. Die gemischte Ableitung der Gesamtwirkung nach Y₁₅ und w₁₆ beträgt −2(Y₁₆−Y₁₅) und ist strikt von null verschieden.

In der vollständigen Wirkung hat die Abhängigkeit von einer leeren Uhr i die Form CᵢYᵢ²−2LᵢYᵢ+Konstante mit Cᵢ=Σⱼ bᵢⱼwⱼ und Lᵢ=Σⱼ bᵢⱼwⱼYⱼ. Stationarität ergibt Yᵢ=Lᵢ/Cᵢ. Durch Einsetzen wird der variable Beitrag zu −Lᵢ²/Cᵢ. Für 15 liegt C₁₅ über das gesamte archivierte Hintergrundintervall zwischen −0,051522 und −0,051490. In L₁₅ stehen die Sender- und Empfängerdaten sowie die Daten der späteren Ereignisse 7 und 8. Diese Eliminierung löst die Leeruhr im vollständigen Randwertproblem.

## Wann werden die Leeruhrgleichungen geschlossen?

Für eine leere Uhr i in einem Ideal I sei Kᵢ(I)=Σⱼ∈I bᵢⱼwⱼ(Yⱼ−Yᵢ). Das ist der innere Beitrag zur normierten Uhrgleichung. Auf der vollständigen stationären Ordnung entfällt auf den äusseren Anschluss genau −Kᵢ(I). Bei einem offenen Schnitt müssen die beiden Beiträge erst beim Zusammenfügen null ergeben.

| Ideale auf N19 | Anzahl | Befund |
|---|---:|---|
| Ohne Sender 16 | 69 | Der strikte Sendervorlauf ist eines dieser Ideale. |
| Mit Sender, ohne Empfänger 18 | 32 | K₁₅=w₁₆(Y₁₆−Y₁₅)>0 bei jeder zulässigen positiven Sendemarke. |
| Mit Empfänger, ohne den ersten Zukunftskragen 7 | 16 | K₁₇=w₁₈(Y₁₈−Y₁₇)>0 bei jeder zulässigen positiven Empfangsmarke. |
| Mit Ereignis 7 | 4 | Die spätere Kette erweitert sich schrittweise um 8, 9, 10. |

Die beiden Positivitätsaussagen folgen aus der Ordnung und den positiven Gewichten. Die numerische Zuordnung der späteren Aufhebung beruht auf dem stationären Referenzzweig im ganzen Intervall e∈[1/6−2⁻²²,1/6+2⁻²²]. An 15 tragen genau 16,18,7,8 mit den Gewichten +1,−9,+16,−8 bei. An 17 tragen genau 18,7,8,9 mit +1,−9,+16,−8 bei. Für jeden zulässigen Schnitt mit Empfänger und unvollständiger Beitragsmenge schliesst eine nach aussen gerundete Intervallrechnung null für die betreffende Summe aus. Bei vollständiger Beitragsmenge folgt die exakte Aufhebung aus der ursprünglichen Stationarität. Der kleinste Schnitt, an dem beide Leeruhrgleichungen ohne äusseren Beitrag erfüllt sind und beide Marken vorliegen, endet am Ereignis 9. Er umfasst 18 der 19 Ereignisse. Ereignis 10 fügt keinen Beitrag zu diesen beiden Gleichungen hinzu.

**Vorwärts mitführbare Daten.** Beim Hinzufügen eines zulässigen Ereignisses j wird Kᵢ um bᵢⱼwⱼ(Yⱼ−Yᵢ) erhöht. Für die neue leere Uhr selbst startet K bei null. Ein Schnitt kann die bisher aufgelaufenen Beiträge so ohne zukünftige Felddaten mitführen, sobald die jeweils neu hinzugekommenen Felder gegeben sind. Bei festgehaltenen Uhren und zunächst frei variierenden positiven Gewichten w₁₆,w₁₈ haben die beiden Ströme nach dem Empfang eine dreieckige Ableitungsmatrix mit Determinante (Y₁₆−Y₁₅)(Y₁₈−Y₁₇)>0. Damit sind sie in diesem Feldraum voneinander unabhängig. Dieser Rang zählt keine Freiheitsgrade des vollständig stationären Zweigs. Das Mitführen der Bilanz bestimmt die neu hinzukommenden Gewichte und den ursprünglichen Wert von Y₁₅ bislang nicht.

## Vorhersage und vollständige Fortsetzungen

Die Dichtezeile am positiven Sender verwendet ausschliesslich dessen Vorgänger. Für die drei festen frühen Uhren −5,−4,−3 und u=Y₁₅ lauten die vier Schichtkoeffizienten −8,16,−9,+1. Ihre Summe ist null, daher ist die Sendergleichung linear in der gesuchten Senderuhr:

    J_w = u² − 6 − 2(u+3)Y₁₆,
    Y₁₆ = (u²−6−J_w)/(2(u+3)).

Bei festem u und J_Y=0 ist die Verschiebung gegenüber dem Nullarm exakt −J_w/[2(u+3)]. Am nominalen Hintergrund beträgt die Steigung rund −0,939033853. Schon die beiden beispielhaften frühen Werte u=−2,4675380 und −2,4675379 erfüllen die lokale Vorlaufstationarität und liefern über diese Gleichung bei J_w=0 verschiedene Senderuhren im registrierten Fenster. Diese Beispiele prüfen nur Vorlauf und Dichtezeile. Sie liefern keinen vollständigen stationären Zustand.

Wir vergleichen zwei Fortsetzungen bei e=1/6 mit denselben Quellen und ohne Ziel am Empfänger. Die Werte in der Tabelle sind gerundete Differenzen gegen den jeweiligen quellfreien Referenzzustand.

| Randdaten | J_w | ΔY₁₅ vor dem Senden | ΔY₁₆ am Sender | ΔY₁₈ am Empfänger |
|---|---:|---:|---:|---:|
| Beide Kragen fest | −10⁻⁶ | +1,63314·10⁻⁷ | +1,56645·10⁻⁷ | −2,61186·10⁻⁷ |
| Beide Kragen fest | +10⁻⁶ | −1,63314·10⁻⁷ | −1,56646·10⁻⁷ | +2,61186·10⁻⁷ |
| Felder ausser Sender und seiner Zukunft fest | −10⁻⁶ | exakt 0 | +9,39034·10⁻⁷ | −5,59802·10⁻¹⁰ |
| Felder ausser Sender und seiner Zukunft fest | +10⁻⁶ | exakt 0 | −9,39034·10⁻⁷ | +5,60314·10⁻¹⁰ |

Bei festen Kragen schliesst eine Kontraktionsrechnung je eine lokale Lösung der zwanzig inneren Gleichungen ein. Im zweiten Vertrag lassen sich alle zwanzig Gleichungen mit denselben frühen Feldern erfüllen. Die algebraische Konstruktion hält den Zukunftspunkt 7 fest und ändert Uhren und Gewichte an 8,9,10. In beiden Verträgen bleiben Ordnung, Gewichtsstrata und Materialfenster erhalten. Die Futures im zweiten Versuch wurden zu den Quellen konstruiert. Die Rechnung belegt keinen Mechanismus, der diese Werte ohne spätere Randinformation erzeugt.

## Welchen Strom verlangt jeder passende Anschluss?

Eine zusätzliche Prüfung nach den ersten Läufen beseitigt die Abhängigkeit dieses Ergebnisses von der Wahl einer bestimmten Zukunftskonstruktion. Sie gilt bei rein lokaler Dichtequelle, passivem Empfänger, festgehaltenen Feldern ausser Sender und seiner Zukunft und in den archivierten Fenstern. Sei d=ΔY₁₆ und q=ΔY₁₈. Die Senderdichtezeile legt d fest. Die Empfängerdichtezeile ergibt genau

    q² + 2(mᵣ−d)q + d(d−2(Yᵣ−Y_z)) = 0,
    mᵢ = Σₖ bₖᵢ(Yᵢ−Yₖ).

Die zweite Wurzel wäre eine Empfängerverschiebung über 3,4491. Das ganze Empfangsfenster erlaubt weniger als 0,000033. Damit ist q festgelegt. Weiter haben 12 und 13 verschiedene Uhren und dieselbe Kopplungszeile v=(−9,16,−8,0) zu den vier Zukunftsereignissen. Ihre ungetriebenen Uhrgleichungen geben v·Δw_F=v·Δ(wY)_F=0. Die Zeile der leeren Uhr 17 hat dieselben Zukunftskopplungen und liefert Δ(wᵣYᵣ)=Y₁₇Δwᵣ. Dies bestimmt Δwᵣ. Die ungetriebene Senderuhr hat ebenfalls die Zukunftskopplung v. Ihre Gleichung bestimmt Δw_z, weil m_z von null getrennt ist. Alle benötigten Unterschiede sind damit festgelegt, bevor die einzelnen Zukunftsuhrwerte gewählt werden.

Für den ersten Schnitt nach dem Senden gilt K₁₅=w_z(Y_z−Y₁₅). Gegenüber dem Nullarm erhält man auf dem gesamten zertifizierten Hintergrundintervall die äusseren Schranken

| J_w | Notwendiges ΔK₁₅ beim ersten Schnitt nach dem Senden |
|---:|---:|
| −10⁻⁶ | [+9,7625; +9,7674]·10⁻⁸ |
| +10⁻⁶ | [−9,7674; −9,7625]·10⁻⁸ |

Der äussere Anschluss muss jeweils die entgegengesetzte Änderung liefern. Kein über alle drei Arme vorab gleich gesetzter Wert dieses **nach** dem Senden entstandenen Stroms ist mit den geprüften Bedingungen vereinbar. Im Vorlauf ist K₁₅ dagegen für alle Arme exakt null und liefert keinen Wert für Y₁₅. Diese Unterscheidung erlaubt einen eindeutigen Test für ein vorgeschlagenes Vorwärtsgesetz. Es müsste aus einer begründeten frühen Präparation ein positives Sendergewicht und den passenden, quellabhängigen Ausgangsstrom erzeugen.

## Reproduktion

Nach dem Entpacken mit Python ab 3.10 und der Standardbibliothek ausführen.

    python3 -B pruefen.py

Der Lauf reproduziert die unveränderte Vorstudie aus PR 388 und deren eingebettete Vorgänger. Schnitt.json enthält die vollständige Zerlegung und die Ordnungsideale als Zählung und Klassen, Fortsetzungen.json die Lösungseinschliessungen und Feldunterschiede. Anschluss.json enthält den Ausschluss der zweiten Wurzel und die notwendigen Ströme. Die unabhängige Gegenrechnung rekonstruiert alle 121 Ideale über Antiketten, wertet 121 Wirkungszerlegungen mit exakten rationalen Feldern aus und kontrolliert die Stromfortschreibung auf 300 einzelnen Erweiterungen und 281 Paaren vertauschbarer Erweiterungen. Sie prüft ausserdem die quadratische Eliminierung beider Leeruhren und die gemischte Wirkungsableitung. Die rationalen Testfelder sind algebraische Kontrollwerte. Die Übertragung auf den stationären Referenzzweig stammt aus den zertifizierten Vorstudien und den Intervallrechnungen. Beide Prüfpläne haben lokale SHA-256-Festlegungen ohne externen Zeitstempel.

Alle 60 physischen P3-Prüfpunkte stehen auf `NOT_RUN`.

[Ausgangsstand auf GitHub, PR 388](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/388)
