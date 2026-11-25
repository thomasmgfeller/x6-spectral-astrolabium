# Aussenuhrgradienten und eine nicht-radiale Kausalabfrage

CST-DUST · Explorative Prüfung des veröffentlichten Standes nach PR 380

Die Summe mit gleichen Vorfaktoren und der Phase exp(iS) ergibt in den beiden vorgeschlagenen endlichen Familien einen von null getrennten komplexen Quotienten. Eine zusätzliche winkelaufgelöste Kausalrelation trennt das kinematische Kontrollpaar 8,5 und 9,9 analytisch. Beides kann aus dem veröffentlichten Material ohne neue stochastische Simulation geprüft werden. Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.

## Endlicher Phasentest

Auf Typ 1767356 sind Randversatz e=1/6 und relativer Schnitt x=1/2 fixiert. Der alte Kausalverband und die Kragenfelder werden wie in [PR 380](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/380) beibehalten. Je beschrifteter, zugelassener Erweiterung mit einem teilweise stationären Feldzweig wird ein Beitrag mit Vorfaktor eins gezählt. Für N16 werden die sieben positiven inneren Felder neu gelöst. Für N17 kommt ein früheres positives Ereignis hinzu. Die Aussenuhr wird bei der Kandidatenauswahl am festgelegten Uhrwert gehalten. In jeder der 54 bzw. 131 zugelassenen Ordnungen gibt es einen entsprechenden Zweig. Beide Familien werden einzeln ausgewertet.

Die dimensionlose Projektwirkung in der gewählten Phase ist

    S = F4 − (19 Σⱼ wⱼ + Σᵢ≺ⱼ bᵢⱼ wⱼ (Yⱼ−Yᵢ)²)/38.
    G = 19 ∂S/∂Y_z.
    Z = Σ exp(iS),   N_G = Σ G exp(iS),   Q = N_G / Z.

Der Faktor vor S im Exponenten wurde für diesen konkreten Test auf eins gesetzt. Die vollständige Wirkung enthält auch die Beiträge der festgehaltenen Felder. Der Prüfer berechnet sie einmal aus allen Paaren und einmal aus den verbleibenden Kragenbeiträgen nach Anwendung der Dichtegleichung der positiven inneren Punkte. Die beiden Intervalle müssen sich schneiden.

| Familie | Vorzeichen von G | Z, gerundet | N_G, gerundet | Q, gerundet | Gleiches reelles Gewicht, Mittel von G |
|---|---:|---:|---:|---:|---:|
| N16 | 30 positiv, 24 negativ | 2,830837 + 5,891160 i | 4,160395 + 0,500577 i | 0,344723 − 0,540562 i | 0,042655 |
| N17 | 109 positiv, 22 negativ | −6,447933 + 12,092290 i | −3,693456 + 4,369456 i | 0,408158 + 0,087798 i | 0,207538 |

Realer und imaginärer Anteil von Q sowie der Betrag des Nenners sind in beiden Fällen von null getrennt. Die vollständigen Intervallendpunkte stehen in Intervalle.json. Für den unskalierten Wirkungsgradienten sind die Mittelwerte durch 19 zu teilen. Dies sind deterministische Rundungs- und Feldlösungseinschlüsse. Die Unsicherheit über das physische Mass wird dadurch nicht quantifiziert. Ein komplexer Amplitudenquotient definiert für sich keine positive Messverteilung. Die beiden bekannten Kontrollradien sind den 185 Feldzweigen nicht zugeordnet.

Eine quantenphysikalische Vorhersage verlangt eine begründete Summe bzw. Integration über Ordnungen und Felder, eine Regel für Beschriftungen und Symmetrien, Randzustand, Quellen und eine Messvorschrift. Eine Integration über eine freie Uhr kann unter den passenden Bedingungen eine Schwinger-Dyson-Identität liefern. Beim Integrieren einer totalen Ableitung sind Mass, Zustandsfaktoren und Integrationsränder mitzunehmen. Hier ist der Wert der Aussenuhr festgesetzt. Auch die freie Phase zwischen verschiedenen Elementzahlen wäre für eine gemeinsame Summe zu begründen.

Eine festgehaltene Uhrquelle g führt bei stationärem Inneren auf einem glatten Zweig auf die Antwort dS_on/dg. Für eine Messung der Ruhemasse wären die Normierung dieser Quellvariation, ein Leerexperiment und eine unabhängige Masseneichung mit anschliessender Prüfung an zurückgehaltenen Massen erforderlich. Die in PR 380 dokumentierte N17-Quelle mit vier Zukunftskragenempfängern liefert G=−1/64 für jeden Wert dieser Uhr bei festen Nachfolgerdaten. Eine Ortsverschiebung benötigt eine eigene relationale Definition.

## Eine zusätzliche Kausalrelation

Das verwendete Paar glatter 4D-Kontrollmetriken und die gemeinsame kinematische Anfangspräparation sind in der [Studie zur Schalenauslese](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/02605a740289a519b2ec66aa12cd41d237c2f6c6/research/rax_cqg/dust_collapse/n15_arealradius_und_schalenauslese_v0_1) angegeben. Auf der materiellen Grenzfläche r=10 gelten zur halben gemeinsamen Eigenzeit T* die Arealradien 8,5 (A) und 9,9 (B). Zu diesen bekannten Geometrien definieren wir zwei neue, hypothetische Grenzmarker. Sie befinden sich im geodätischen Winkelabstand θ=1/9200 Radiant auf der Einheitssphäre. Der erste Marker bezeichnet ein Ereignis bei T*, der zweite eines bei T*+1/1000. Die zusätzliche Messfrage lautet, ob der erste den zweiten kausal erreichen kann. Die Winkelkalibrierung, gemeinsame Eigenzeit und Identifikation der Grenzfläche sind gewährte Informationen dieses Kontrollversuchs.

* In A nimmt der Arealradius auf r=10 weiter ab. Er beträgt im ganzen kurzen Intervall höchstens 8,5. Eine Kurve auf dem kürzesten Winkelbogen mit konstanter Winkelgeschwindigkeit θ/ΔT hat daher in der Metrik des Projekts eine Bahngeschwindigkeit höchstens 8,5/9,2 < 1. Sie ist zeitartig.
* In B muss jede mögliche kausale Verbindung wegen |dr/dT|≤1 während des Intervalls bei r≥9,999 bleiben. Für die Winkelmetrik R=r√(1−d_B f) gilt f≤1 und d_B≥0. Mit T_end>3, H(s)≤10s³ für 0≤s≤1 und H≤1 erhält man d_B≤199/5000+(161/625)10(64/3000)³ < 0,04. Folglich gilt auf jeder möglichen Bahn R>9,79. Bei lokaler Lichtgeschwindigkeit eins kann ihre Winkellänge höchstens ΔT/9,79 betragen. Das liegt unter dem verlangten Winkelabstand ΔT/9,2. Ein radialer Umweg kann die Ereignisse ebenfalls nicht verbinden.

Die Antwort trennt genau diese beiden idealisierten Welten. Die publizierten N15-Daten enthalten keine solchen Ereignisse. Die Konstruktion wurde in Kenntnis der zwei Kontrollen entwickelt. Aussagen über Messfehler, Zugang zu den Markern, Verallgemeinerung und kontinuierliche 1-%-Präzision benötigen ein eigenes Instrumentmodell und unabhängige Testfälle.

Für den alten Record ist sogar die kontinuierliche kinematische Familie d_s=(1−s)d_A+s d_B möglich. Die beiden Funktionen stimmen an allen alten Ereignissen überein, der Radialteil der Metrik ist fest, und das gesamte Kugelvolumen ist unabhängig von d. Die in der Ausgangsstudie konstruierte mitbewegte Testmaterie behält dieselben gemessenen Feldwerte und integrierten Mengen. Der Radius am Zielzeitpunkt läuft von 8,5 bis 9,9. Wenn das Rauschen nur vom alten Record abhängt, ist die Verteilung der beobachtbaren Daten für alle s gleich. Entlang dieser Richtung verschwindet die Fisher-Information, sofern der Score definiert ist. Ein anderes physisches Gesetz zur Erzeugung von Records wäre eigens anzugeben.

Die deterministische Zwei-Punkt-Schranke (9,9−8,5)/(9,9+8,5)=7/92 bezieht sich auf den grösstmöglichen relativen Fehler eines gemeinsamen Punktschätzers. Ein lokal berechnetes Fisher-Informationsmass benötigt eine Wahrscheinlichkeitsverteilung für die jeweils beobachtbaren Daten. Eine kleine Cramér-Rao-Untergrenze allein bestätigt keine erreichbare Genauigkeit. Auch aus deterministischen Cluster- oder Spektralmerkmalen des ursprünglichen identischen Kausalsets folgt keine Trennung. Eine neue Dynamik kann die Menge zulässiger Geometrien einschränken. Ihre Vorhersagen müssen unabhängig geprüft werden.

## Reproduktion

Im entpackten Verzeichnis mit Python ab 3.10 und Standardbibliothek ausführen.

    sha256sum -c SHA256SUMS
    python -B pruefen.py
    python -B gegenrechnung.py

Der Prüfer nimmt an genau einer Stelle des hashfixierten Original-Lösers die Felder jedes zugelassenen Zweigs ab. Er wiederholt die 182 bzw. 11 943 endlichen Ordnungen. Bei N16 enthält das Original die Gradienten je Kandidat. Bei N17 sind dort Häufigkeiten und der nächste Zeuge archiviert. Der Replay rekonstruiert deshalb den vollständigen N17-Satz. Es gibt keine neuen Zufallsziehungen. Er erzeugt die Tabelle Kandidaten.csv und vergleicht sie und die Resultatintervalle mit den beigefügten Dateien. Zur Auswahl der Zeilen bezeichnen die Bitmasken alte Ereignisse mit IDs 0 bis 14. Die u-Masken entfallen bei N16 und sind als null gespeichert. Die CSV-Spalten S_lo bis G_hi und die numerischen Intervallendpunkte in Intervalle.json haben den gemeinsamen Nenner 10¹⁴.

Für die komplexen Phasen halbiert der Prüfer die Argumente bis |s|≤1/4, schliesst die trigonometrischen Funktionen mit Taylorpolynomen der Ordnung 18 und der Lagrange-Restschranke ein und verwendet die Doppelwinkelformeln. Division erfolgt erst nach Nachweis eines strikt positiven Nennerbetragsquadrats. Die Winkelabschätzung nutzt exakte Bruchrechnung. Die unabhängige Gegenrechnung löst die quadratischen Gleichungen direkt in den ursprünglichen Uhrkoordinaten mit Gleitkommaarithmetik, berechnet die Phasen mit der komplexen Exponentialfunktion der Standardbibliothek und vergleicht beide Quotienten mit den strengen Intervallen. Lizenz und Urheberhinweise der übernommenen Dateien liegen unter quelle/.
