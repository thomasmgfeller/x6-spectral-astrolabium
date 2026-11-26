# CST-DUST · Ein Impulsspeicher vor dem Sender auf N19

**26. November 2026.** Ein passiver Speicher, der ausschliesslich auf die Staubdaten im kausalen Vorlauf zugreift, kann die zwei bekannten N19-Zustände mit verschiedenem frühestem Uhrimpuls G₀ nicht unterscheiden. Ein zusätzliches klassisches Gerät kann dagegen einen von aussen präparierten Impuls auf den Anfangsrand übertragen und vor dem Sender wieder auslesen. In fünf lokal zertifizierten stationären Lösungen funktioniert diese Kopplung. Bei gleicher Anzeige und unterschiedlicher Senderquelle ändern sich jedoch bereits die früheren Staubuhren. Die Anzeige allein weist somit keine identische Staubpräparation und keine gerichtete Pulsübertragung nach.

## Was ein passiver Speicher lernen kann

Im eingebetteten Ausgangspaket haben zwei vollständig stationäre quellfreie Belegungen identische Staubdaten am Anfangskragen, identische Daten im ganzen strikten Vorlauf von Sender 16 und denselben Gesamtimpuls. Ihre Zukunftsgewichte dürfen verschieden sein. Die Einzelimpulse G₀ unterscheiden sich bei e=1/6 um rund 0,00149394.

Ein Gerät starte mit derselben, von der Wahl zwischen diesen beiden Belegungen unabhängigen Präparation. Jeder passive Schritt verwende nur seine bisherigen Anzeigen, lokale Staubdaten, kausal zugegangene Nachrichten und gleich verteilte geräteinterne Zufallszahlen. Man kann beide Läufe mit denselben Zufallszahlen ausführen. Durch Induktion über den Vorlauf erhält man dann an jedem Leseschritt genau dieselbe Anzeige. Bei gleichen Vorwahrscheinlichkeiten beträgt die Erfolgswahrscheinlichkeit für die Identifikation der Belegung deshalb 1/2, auch für eine zufällige Entscheidungsregel. Für eine Zahlenschätzung folgt aus der Dreiecksungleichung ein grösster erwarteter absoluter Fehler von mindestens der halben Trennung, über das archivierte Hintergrundintervall mindestens 0,00074670813. Das gilt für dieses Paar und diese verfügbaren Daten. Eine bereits mit dem Zweig korrelierte Präparation wäre zusätzliche Eingangsinformation.

## Wie das aktive Gerät den Impuls übergibt

Die Kausalkette 0 ≺ 1 ≺ 2 ≺ 16 ist Bestandteil der festen Ordnung. Die Kragenereignisse 0,1,2 haben jeweils positives Staubgewicht 1/8. Auf diesen drei Ereignissen führen wir zwei klassische Gerätepositionen X,U. Als Trägheitskoeffizienten setzen wir die festen Kragengewichte w₁ und w₂ ein. Die Gerätekoordinaten, die Form der Kopplung, ihre Verstärkung g und die Übertragung eines Positionswerts von 1 nach 2 sind Modellannahmen. Zwei feste Uhrreferenzen definieren a=Y₁+4 und b=Y₀−Y₁+1. Eine gleichzeitige Verschiebung aller vier Anfangsuhren ändert a. Eine zusätzliche Verschiebung der frühesten ändert b.

Die beiden Beiträge zur Gerätewirkung sind

    L₀₁ = w₁[(X₁−X₀+g b)² + (U₁−U₀+a)²],
    L₁₂ = w₂[(X₂−X₁)² + (U₂−U₁)²].

Die halben kanonischen Ableitungen definieren die einlaufenden Impulse P,T in derselben Normierung wie Gᵢ=−½∂A/∂Yᵢ. Für X liefern die Knotengleichungen P=w₁(X₁−X₀+g b)=w₂(X₂−X₁), für U entsprechend T=w₁(U₁−U₀+a)=w₂(U₂−U₁). Bei gegebenen Anfangspositionen und einlaufenden Impulsen bestimmen diese Gleichungen die beiden späteren Positionen vorwärts. Die Endposition wird frei berechnet.

Am positiven Ereignis 2 genügt die Bewegung auf dem zweiten, ungekoppelten Glied. Der Leser bildet P=w₂(X₂−X₁) und T=w₂(U₂−U₁). Er benötigt die gespeicherten oder übertragenen Positionen von Ereignis 1. Ein direkt aus der Staubwirkung abgeleiteter Transport dieses Geräts steht aus.

Die halbe Ableitung der Gerätewirkung bei festen Gerätepositionen beträgt am Staubknoten 0 genau gP und am Staubknoten 1 genau T−gP. Variieren wir die gleichen zwei Randrichtungen wie in der Vorstudie, lauten die Randgleichungen der gekoppelten Wirkung daher

    G₀ = gP,       Σᵢ₌₀³ Gᵢ = T.

Zur Kontrolle ergibt das Eliminieren der beiden zyklischen Gerätekoordinaten bei vorgegebenen Impulsen den Zusatz 2gP b + 2T a − (P²+T²)(1/w₁+1/w₂). Die rückwirkende Kopplung liefert also genau die beiden für die Randgleichungen erforderlichen Terme. Das Gerät kann einen präparierten Zahlenwert in das erweiterte Modell einbringen. Die Ausgangswirkung allein liefert weder die Wahl dieser Impulse noch die Kopplung.

## Fünf nichtlineare Kontrollen

Wir verwenden e=1/6, g=1, T=−0,078302831 und P=−8,404505923 als Referenzeinstellung. Die beiden rationalen Zahlen sind vorab gerundete Impulse aus der früheren vollständigen N19-Lösung. Die Eichung benutzt damit Informationen über den gesamten Referenzzustand. Alle Zahlen für das neue Experiment wurden vor seinem ersten Rechenlauf festgehalten. Bei verändertem P und bei der späteren Senderwahl bleibt T exakt gleich. Der einzige für die Pulsarme veränderte Term der Staubwirkung ist −J_w w₁₆. Die äusseren Zukunftsuhren und -gewichte bleiben fest. Für die Fensterprüfung werden sowohl die ursprüngliche Koordinate als auch die am veränderten Kragen normierte Koordinate verwendet.

| ΔP | Senderquelle J_w | Vor dem Puls gelesene Änderung ΔP | Änderung der frühesten Staubuhr ΔY₀ | Änderung der Empfängeruhr ΔY₁₈ |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |
| −10⁻⁶ | 0 | −10⁻⁶ | −1,95208·10⁻⁶ | +1,32187·10⁻⁶ |
| +10⁻⁶ | 0 | +10⁻⁶ | +1,95207·10⁻⁶ | −1,32189·10⁻⁶ |
| 0 | −10⁻⁶ | 0 | −9,49173·10⁻⁸ | −1,80762·10⁻⁷ |
| 0 | +10⁻⁶ | 0 | +9,49177·10⁻⁸ | +1,80761·10⁻⁷ |

Die Staubuhrdifferenzen sind gerundete Modellwerte. Die Anzeige folgt exakt aus den Gerätegleichungen. Die nichtlinearen Einschliessungen bestätigen für jeden Arm die zwanzig inneren Staubgleichungen, die beiden Randgleichungen, positive Gewichte auf dem gewählten Zweig, strikte Uhrordnung und eindeutig dieselben beiden materiellen Marken. Kein Empfängerwert geht in die Präparation oder die Lösungsgleichungen ein.

Die beiden Senderarme haben bei festem P,T am Punkt 2 dieselben beiden **Positionsdifferenzen** wie der Nullarm. Die einzelnen Gerätepositionen und alle vier Staubuhren im strikten Sendervorlauf unterscheiden sich. Beispielsweise ändert sich Y₀ gegenüber dem Nullarm in jedem Senderarm um mehr als 9,49·10⁻⁸ im Betrag. Damit beschreiben die Unterschiede am Empfänger eine stationäre Antwort auf geänderte Randwertlösungen. Sie sind kein Laufzeitnachweis. Würde zusätzlich die ganze Feldänderung auf den Sender und seine Zukunft beschränkt, blieben die vier in der Staubantwort-Vorstudie geprüften passiven Knotengleichungen unverändert. Ihr dortiger Eindeutigkeitsbeweis bei festem Zukunftskragen schliesst weiterhin eine Änderung an den beiden Endpunkten in den registrierten Fenstern aus. Der Apparat koppelt nur am Anfangskragen.

## Gegenproben und Ablesegenauigkeit

* Die vollständig unpräparierten Register (P,T)=(0,0), eine vom Staub entkoppelte X-Spur (g=0) und der aus der ersten Staubverbindung errechnete Vorschlag P=1/8 bei g=1 verfehlen den nominalen Zweig in der vorab festgelegten Umgebung. In der Koordinatenbox mit Radius 10⁻⁴ um die Referenz gilt dort −8,419763 ≤ G₀ ≤ −8,389251. Der Ausschluss ist auf diese Box beschränkt.
* Die gleichzeitige Umpolung (g,P)→(−g,−P) erhält beide Staubrandkräfte und alle fünf Staublösungen, wenn die gesamte jeweilige P-Präparation umgepolt wird. Die X-Anzeige wechselt ihr Vorzeichen. Die U-Spur bleibt gleich.
* Bei w₂=1/8 unterscheiden sich die freien Gerätewege zweier benachbarter P-Einstellungen um 8·10⁻⁶. Haben beide abgelesenen Positionen jeweils einen unbekannten absoluten Fehler kleiner als 2·10⁻⁶, liegen die drei vorbereiteten Impulse bei Zuordnung zur nächsten Einstellung eindeutig auseinander. Das ist eine Anforderung an einen hypothetischen Leser, ohne gemessene Geräteauflösung.
* Eine ergänzende Rechnung prüft die Grenze schwacher Kopplung. Bei festem G₀≠0 gilt auf dem freien Glied w₂(ΔX)²=G₀²/(w₂g²). Für g=1, 1/2 und 1/10 beträgt der positive X-Anteil der Gerätewirkung gerundet 565,09, 2 260,34 und 56 508,58. Eine beliebig schwache Kopplung kann denselben Randimpuls daher nur mit unbeschränkt wachsendem Gerätebeitrag aufprägen. Diese Grösse ist ein Term der Modellwirkung. Eine Umrechnung in eine physikalische Energie fehlt.

## Reproduktion und offener Versuch

Nach dem Entpacken genügen Python ab 3.10 und die Standardbibliothek.

    python3 -B pruefen.py

Der Prüfer reproduziert das mitgelieferte Ausgangspaket samt seinen N19- und N17-Vorstudien. Dezimale Newton-Schritte liefern für die neuen Fälle Vorschläge. Auswärts gerundete Intervall-Kontraktionen zertifizieren jeweils Existenz und lokale Eindeutigkeit für die exakten rationalen Eingaben. Die geschlossenen Ausdrücke für die Gerätepositionen vervollständigen die Lösungen. Eine Gegenrechnung rekonstruiert die Schichtgewichte aus der Kausalordnung, setzt die Knotengleichungen direkt ein und überprüft die unreduzierte Gerätewirkung in 18 rationalen Fällen per exakten Differenzen. Alle fünf Lösungseinschliessungen, Fenster, Koordinaten und verglichenen Differenzen stehen in Register.json. Die ergänzenden Kontrollen stehen in Gegenrechnung.json. Die beiden Plantexte wurden jeweils lokal vor dem beschriebenen Lauf gehasht, ohne externen Zeitstempel.

Der nächste physikalische Test ist die Präparation an einem Schnitt vor dem Sender aus der ursprünglichen Staubwirkung. Dazu müssen die über den Schnitt reichenden Wirkungsterme bestimmt und die von der späteren Senderwahl unabhängig festzuhaltenden Anfangsdaten identifiziert werden. Die jetzige Rechnung liefert dafür eine überprüfbare Gegenprobe mit gleichem frühen Geräteeintrag und verschiedenen frühen Staubuhren. Alle 60 physischen P3-Prüfpunkte bleiben auf `NOT_RUN`.

[Öffentliche Ausgangsstudie auf GitHub, PR 387](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/387)
