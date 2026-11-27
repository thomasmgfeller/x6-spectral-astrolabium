# Drei unterscheidende Sondenbahnen am frühen N22-Schnitt

Die publizierte flache Geometriekontrolle besitzt am Schnitt x=1/2 genau drei getestete inertiale Fortsetzungen, deren Materieseiten sich zwischen den Kugeln mit Radius 1 und 2 unterscheiden. Dieser Test kombiniert erstmals die drei Ablesungen und prüft ausserdem, ob eine beliebig grosse endliche Ergänzung durch leere Sonden ihre freie Uhrgleichung lösen kann. Die beiden Randpräparationen werden separat mit ihren rational eingeschlossenen Kragenfeldern geprüft.

[Geometrie, stationäre Einzelsonden und Eingabedateien aus PR 413](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/2c08c72af7fa7d075f50decc48c9531d64d61c66/research/rax_cqg/dust_collapse/n22_aeussere_materiegrenze_und_n23_sonden_v0_1)

## Gleicher Ablesezeitpunkt

Die drei Fortsetzungen von 3, 4 oder 5 durch 11 sind in der kleinen Kugel innen, in der grossen aussen. Ihre drei Orte am Schnitt x=1/2 sind auch bei den zugelassenen Uhrintervallen voneinander getrennt. Die kleinste zertifizierte untere Schranke ihres quadrierten räumlichen Abstandes überschreitet in beiden Präparationen 6,3·10⁻⁹ in den Längeneinheiten der Kontrolle. Die gleichzeitig eingefügten Punkte sind kausal unvergleichbar. Alle haben als alte Zukunft genau die vier Kragenereignisse 7,8,9,10.

Es gibt drei Paaranordnungen auf N24 und eine Dreieranordnung auf N25 je Präparation. Bei den Paaranordnungen lassen sich je vier, bei der Dreieranordnung acht positive/leere Besetzungsmuster prüfen. Alle 20 Muster je Präparation sind ausgeschlossen. Der Prüfer rekonstruiert jede vollständige Ordnung und kontrolliert, dass jede Sondenzeile und jede in ihrem Nachweis benutzte frühe Dichtezeile dieselben Schichtkoeffizienten wie im Einzelversuch besitzt. Bei positivem Gewicht gilt die dort bewiesene strikte Schranke D < −1,31 für die Dichtevariation im Fenster. Bei leerem Gewicht scheitert die freie Uhrgleichung. Diese Ausschlüsse gelten auch dann, wenn die übrigen freien Innenfelder auf der festgehaltenen Ordnung erneut stationär werden sollen, unter den ursprünglichen Kragenvorgaben und bei positiver Besetzung der Vorläufer 4,5,6,11.

## Beliebig viele leere neue Ereignisse

**Aussage.** Sei e eine zusätzliche leere, quellenfreie Sonde, die in der induzierten alten Ordnung genau 7≺8≺9≺10 als alte Zukunft hat. Sie erfülle 15/32 ≤ x_e < 1. Die gemeinsame Zeit sei streng ordnungserhaltend. Die Uhren der neuen Ereignisse seien freie Variationsstellen. Sind alle neuen Ereignisse in der strikten Zukunft von e leer, ist eine stationäre Lösung unter den beiden archivierten Kragenpräparationen ausgeschlossen. Endlich viele neue Ereignisse genügen für das Argument; ebenso reicht lokale Endlichkeit zwischen e und dem alten Kragen. Neue Ereignisse ausserhalb der Zukunft von e dürfen andere Gewichte haben.

**Beweis.** Wähle v maximal unter den neuen Ereignissen mit e≼v≺7, einschliesslich e. Die Menge ist nicht leer. Alle alten Nachfolger von v sind auch Nachfolger von e. Zugleich folgen 7,8,9,10 auf v. Zwischen v und 7 liegt weder ein altes noch ein neues Ereignis. Somit ist k(v,7)=1. Für j=7,8,9,10 liegen genau j−7 alte Ereignisse zwischen v und j. Die Anzahl hⱼ der zusätzlichen Zwischenereignisse erfüllt 0=h₇≤h₈≤h₉≤h₁₀. Sobald die Gesamtzahl vier erreicht, verschwindet der Schichtkoeffizient. Daher genügt es, die hⱼ bei vier zu kappen. Die 35 monotonen Vierertupel ergeben acht mögliche Schichtvektoren. Die vier Geräteglieder des Vorgängermodells betreffen ausschliesslich alte Ereignispaare.

Am leeren v ist Gᵥ=Σⱼ k(v,j)wⱼ(Yⱼ−Yᵥ) über den vier alten Kragenpunkten, da sämtliche neuen Nachfolger das Gewicht null haben. Für jede feste Realisierung der Kragenfelder hängt Gᵥ affin von der normierten Uhr xᵥ ab, wobei 15/32≤xᵥ<1 gilt. In sieben Fällen hat Gᵥ an beiden Endpunkten dasselbe strikte Vorzeichen. Der achte Fall liefert Gᵥ=w₇(Y₇−Yᵥ)>0 durch die strikte Kausalrelation. Diese Prüfung verwendet die vollständigen rationalen Intervallgrenzen beider Präparationen. Sie schliesst eine stationäre Uhr für v und damit eine stationäre Erweiterung aus.

| Schichtvektor von v zu 7,8,9,10 | Vorzeichen für beide Präparationen auf [15/32,1) |
|---|---|
| (1,−9,−8,0), (1,−9,0,0), (1,−9,16,−8), (1,−8,0,0) | negativ |
| (1,−9,16,0), (1,16,−8,0), (1,16,0,0) | positiv |
| (1,0,0,0) | positiv bis zum offenen Endpunkt |

Für eine dieser freien leeren Bahnen erfordert ein noch möglicher Erweiterungsversuch bei denselben Randbedingungen mindestens einen positiven **neuen** kausalen Nachfolger der Sonde. Seine Existenz könnte die lokale Vorzeichenbilanz ändern. Ob dafür ein mit der einen oder anderen Kontrollkugel vereinbarer Ort und eine Lösung sämtlicher Feldgleichungen existieren, ist offen. Die übrigen ursprünglichen Ereignisse dürfen sich durch die Erweiterung keine zusätzlichen alten Nachfolger der Sonde erschliessen. Eine extern geführte Uhr mit eigener Quelle ist ein anderer Messvertrag. Die N24/N25-Erweiterungen früherer Arbeiten mit ursprünglich terminaler N23-Sonde besitzen einen anderen Ausgangsbereich.

## Reproduktion

Das Prüfpaket enthält die drei archivierten Dateneingaben, die unverändert übernommenen geometrischen und Einzelsonden-Routinen sowie den neuen Prüfer. Er berechnet alle Vorzeichen, Distanzuntergrenzen, Ordnungen und Belegungszahlen und gleicht die Ergebnisdatei byteweise ab. Alle Zahlen im JSON sind exakte ganze Zahlen oder rationale Brüche.

```sh
sha256sum -c SHA256SUMS
python3 -B pruefen.py
```

Die Rechnung betrifft stationäre lokale Modellgleichungen auf den angegebenen Ordnungen. Eigenfläche, physischen Radius und unabhängigen Massenstandard liefert sie nicht. Die acht physischen Pilotradien und alle 60 P3-Prüfpunkte bleiben NOT_RUN.
