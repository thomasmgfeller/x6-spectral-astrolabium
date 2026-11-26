# CST-DUST N19 · Gemeinsame Präparation vor der Pulswahl

**26. November 2026.** Ein klassisches Gerät kann im erweiterten stationären N19-Modell an Ereignis 0 mit einer einzigen Verteilung von Position und kanonischem Impuls vorbereitet werden. Dieselbe Verteilung liefert für beide untersuchten Trägheiten, beide Transportwege und jeden der zwölf Hintergründe aus PR 390 eine eindeutige Quellenauslese am Empfänger 18 und später am Speicherort 7. Die Aussage ist für eine beschränkte Zustandsmenge deterministisch. Für die unten festgelegte Gaußpräparation ergibt sich bei einem Rundungsraster von 2·10⁻¹² eine gemeinsame Erfolgswahrscheinlichkeit von mindestens **99,999995 %**. Das ist eine analytische Modellschranke. Die Schrittweite, die Wirkungsnormierung und die Ankopplung an die einzelnen Verbindungsströme sind apparative Voraussetzungen.

Die Rechnung verwendet die Quellen J ∈ {−10⁻⁶, 0, +10⁻⁶}, e=1/6 und die zwölf stationären Nullhintergründe der Vorgängerstudie. Zwischen den Quellarmen jedes Hintergrunds bleiben die früheren Staubfelder fest. Der spätere Rand darf sich stationär anpassen. Zwei Trägheiten, zwei Transportwege, zwölf Hintergründe und drei Quellen ergeben 144 geprüfte Familien. Sie prüfen jeweils eine ganze kontinuierliche Menge von Gerätezuständen und die angegebenen Abgleichfehler. Alle Zahlen verwenden die Einheiten der Modellwirkung. [Veröffentlichter Ausgangsstand, PR 390](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/390)

## Wie gelangt ein vorbereitetes Gerät zum Empfänger?

Die transitive Reduktion der N19-Ordnung liefert genau zwei Ketten unmittelbarer Nachbarn von 0 nach 18:

- 0 → 1 → 2 → **15** → 16 → 18
- 0 → **17** → 18

Die hervorgehobenen Ereignisse haben Staubgewicht null. Die einzige solche Kette von 0 zum Sender 16 führt über 15. Fordert man auf jedem besuchten Ereignis positives natives Staubgewicht und auf jedem Glied unmittelbare Nachbarschaft, fehlt folglich eine durchgehende Trägerkette. Beim üblichen freien Geräteterm κwⱼ(ΔX)² am Ziel j mit wⱼ=0 ist auch der daraus folgende Impuls null, unabhängig von der Positionsdifferenz. Damit lässt sich ein frei präparierter Impuls dort nicht aus der Gleichung weitertransportieren.

| Geprüfte Transportregel | Zusätzliche Modellannahme |
|---|---|
| Positive Träger | Alle drei Spuren gehen über 0,1,2,16,18,7. Der Übergang 2→16 überspringt genau 15. Die Ordnung und die Staubwirkung enthalten die Relation 2≺16, deren nativer Schichtkoeffizient −9 beträgt. Der positive kinetische Transportterm für den Gerätezeiger wird gesondert eingeführt. |
| Unmittelbare Nachbarn | Die erste Spur läuft über 15 und 16. Die zweite und die Zeitstempelspur laufen über 17. Für das freie Glied nach 15 dient κw₂ als Trägheit, für das nach 17 entsprechend κw₀. Diese beiden Kragengewichte sind auf 1/8 geeicht. Separate Sondenpositionen dürfen damit auf den leeren Ereignissen existieren. Die nativen Staubgewichte dort bleiben genau null. |

Die tatsächlichen Abtastungen bleiben bei beiden Regeln auf 15→16 und 16→18 für die erste Spur, auf 17→18 für die zweite und auf 18→7 für den Zeitstempel. Die übrigen Übergänge übertragen Geräteposition und Impuls. In beiden Fällen ist die ursprüngliche Staubwirkung um ein Instrument erweitert.

## Ein Anfangszustand für jede Quellenwahl

Auf einem Geräteglied mit Trägheitsgewicht μ gilt bei Einheitsverstärkung

    L = κμ(ΔX−d)² + δwⱼd²,     P = 2κμ(ΔX−d) = 2p.

Hier ist d die ausgewählte native Uhrdifferenz oder null auf einem freien Glied. Die Koeffizienten gleichen denen aus PR 390. Bei κ=1 ist ein gemeinsamer Abgleichfehler |δ|≤10⁻¹¹ auf den vier Abtastungen zugelassen. Bei κ=10⁻¹¹ ist δ=−κ, womit sich auf einem abtastenden Glied direkt κwⱼ[(ΔX)²−2ΔX d] ergibt. Die unabhängigen Gerätevariationen an jedem inneren Punkt erhalten P. Gegeben (q,p) am Punkt 0, lautet der Vorwärtsschritt daher Xⱼ=Xᵢ+d+p/(κμ). Eine Eingabe des Quellenetiketts oder ein gemessener späterer Endimpuls wird dafür nicht gebraucht. Bei der Variation der Staubfelder lässt sich dieselbe Erhaltung durch die Impulsrandterme −2pX₇ darstellen.

Sei A die Summe der inversen Trägheitsgewichte 1/μ bis zum jeweiligen Leser. Die Positionsabweichung von der idealen Summe der Uhrdifferenzen lautet exakt q+A p/κ. A hängt von der vollständig zurückgekoppelten Lösung ab. Der Leser muss weder A noch die Anfangsabweichung kennen. Am Empfänger nimmt er nur t und die beiden lokalen Geräteanzeigen. Bei 7 nimmt er Y₇ und die drei gespeicherten Positionen und bildet aus dem Zeitstempel zunächst die Empfangsuhr t. Alle Eingaben werden vor der Klassifikation gerundet.

Für die identische Präparation in beiden Geräten setzen wir ein einziges Mal κ₀=10⁻¹¹ und je Spur

    v₀ = p/κ₀,      b = q+250v₀,      B=10⁻¹²,      V=10⁻¹⁴,
    E = (b/B)²+(v₀/V)².

Drei Ensemblespuren werden unabhängig gleich präpariert. Quelle, Transportregel, tatsächliches κ und Hintergrund treten in E nicht auf. Es ist möglich, alle Anfangswerte auf der gefüllten Ellipse E≤1 zuzulassen. Für den Gaußversuch werden b/B und v₀/V stattdessen unabhängig mit Mittelwert null und Standardabweichung 1/3 gezogen. Dieselbe Gaußdichte wird in allen folgenden Reichweitentests verwendet. Es wird kein ungünstiger Lauf entfernt.

Eine explizite lokale Vorbereitung der Korrelation ist klassisch möglich. In den skalierten kanonischen Koordinaten x=q/B und y=p/(κ₀V) startet das Gerät mit einer runden Verteilung gleicher Phasenraumfläche. Setze c=250V/B=5/2 und z=(√(c²+4)+c)/2. Zwei positive harmonische Viertelperioden mit den Transfermatrizen R₁ und R_z, wobei R_z die Zeilen (0,z) und (−1/z,0) hat, ergeben −diag(z,1/z). Eine anschliessende Uhrzeigerdrehung mit cos(2θ)=c/√(c²+4) und sin(2θ)=2/√(c²+4) richtet die Ellipse aus. Die resultierende Formmatrix hat Zeilen (1+c²,−c) und (−c,1). Damit wird die gewünschte q-p-Korrelation vor der Quellenwahl erzeugt. Die Drehungen und die schaltbaren harmonischen Geräteparameter sind Annahmen über den Präparator am Anfangsrand. Sie erhalten das Phasenraumvolumen. Insbesondere muss der Eingangsapparat die kleine Ausgangsfläche bereits bereitstellen. Eine Kühlung oder Temperatur in Kelvin wird aus dieser Konstruktion nicht abgeleitet.

## Rückwirkung und Fehlernachweis

Jede tatsächlich durch einen positiven inneren Knoten j laufende Spur trägt p²/(κwⱼ²) zur Dichtegleichung bei. Auf der positiven Brücke tragen am Sender alle drei Spuren bei, auf dem unmittelbaren Weg nur die erste. Am Empfänger tragen auf beiden Wegen alle drei bei. Ein freier Übergang, dessen Trägheit aus einem festgehaltenen Kragengewicht stammt, belastet dessen Randableitung. Die Gewichte 0–2 sind Randdaten. Die berechnete Rückwirkung auf die inneren Uhren folgt aus denselben abtastenden Verbindungen wie in PR 390. Die um δ veränderten vier Uhrzeilen bleiben enthalten.

Für jede eingeschlossene Impuls- und Abgleichbox wird die registrierte Wurzel der quadratischen Empfängergleichung ausgewählt und die zweite Wurzel vom Fenster getrennt. Eine stetige Selbstabbildung eines kompakten Intervalls um die native Senderuhr sichert eine Lösung für jede genaue Eingabe der Familie. Die späteren Randgewichte und Momente vervollständigen die Uhrgleichungen. Die anschliessende unabhängige Knotenauswertung kontrolliert die elf Uhrzeilen, neun freien Dichtezeilen, sämtliche Impulsgleichungen, beide Materialfenster, Positivität und strikte Kausalordnung. Die Rechnung ist eine stationäre Fortsetzung mit vorab festgehaltenem Vorlauf. Eine vollständig aus den frühen Staubdaten erzeugte Zeitentwicklung bleibt offen.

Für die Ellipse E≤m² und ein Gerät mit Trägheit κ ist der Positionsfehler ohne Rundung eingeschlossen durch

    |q+A p/κ| ≤ m√[B²+V²(A κ₀/κ−250)²].

Dies folgt aus der Stützfunktion der Ellipse. Da die Hülle von A über alle zugelassenen Impulse bestimmt wird, gilt die Schranke auch für impulsabhängige Gewichte. Die anschliessende Rechnung verwendet denselben Drei-Quellen-Klassifikator wie PR 390. Wenn die geschätzte Empfangsuhr um eₜ schwankt, verschiebt dies beide rekonstruierten Leeruhren in gleicher Richtung. Daher ist der Ableitungsfaktor dieses Fehlers Fₜ+Fᵤ+Fₕ. Das Verfahren propagiert gesondert die beiden individuellen Gerätefehler und den Lastbeitrag zum wahren Residuum. In einer zertifizierten Familie bleibt der Abstand zweier Kandidatenresiduen grösser als das Doppelte der oberen Schranke für das wahre Residuum. Das sichert die richtige Quelle auch zwischen den konkret durchgerechneten Anfangspunkten.

## Wie zuverlässig ist die Auslese?

| Bedingung | Befund am Empfänger 18 und am Speicher 7 |
|---|---|
| Dieselbe beschränkte Präparation in (q,P), Raster 2·10⁻¹² | Für alle drei Spuren mit E≤4 gelingt die Quellwahl in allen 144 Familien. Bei E≤9 reicht dieselbe Abschätzung für 69 Familien. |
| Dieselbe Gaußverteilung, gleiches Raster | Für eine Spur beträgt die Wahrscheinlichkeit von E≤m² genau 1−exp(−9m²/2). Für alle drei Spuren mit m=2 ergibt sich (1−exp(−18))³ ≈ 0,99999995431006. Dies ist eine gemeinsame **Untergrenze** für korrekte Auslese an beiden Orten, pro Familie. |
| Binäre Rundung auf [−8,8), beschränkter Kern E≤1 | 41 Gesamtbits genügen in allen 144 Familien. Die getesteten 39 und 40 Bits erhielten mit dieser Abschätzung kein durchgängiges Zertifikat. Alle benutzten Analogwerte liegen strikt innerhalb des Messbereichs. Das Raster bei 41 Bit ist gröber als 2·10⁻¹². |
| Konkrete Ununterscheidbarkeit | Bei 33 Gesamtbits liefern Nullpuls und negativer Puls am nominalen, unbelasteten und zentral vorbereiteten Gerät dieselben gerundeten Eingaben für beide Leser. Jede Regel aus diesen Ziffernfolgen hat bei mindestens einer der beiden Quellen einen Fehler. Die optimale Bitgrenze bleibt offen. |
| Breitere Präparation in das schwache Gerät eingesetzt | Ein Anfangszustand mit pᵤ=10⁻¹⁴, qᵤ=−2,5·10⁻¹² und beiden übrigen Spuren im Zentrum gehört zur für κ=1 skalierten Ellipse. Wird er unverändert in das schwache Gerät eingesetzt, lesen beide Transportregeln einen Nullpuls an 18 und 7 fälschlich als negative Quelle. |

Die Wahrscheinlichkeitsaussage setzt die festgelegte Verteilung am Anfang, das genannte digitale Raster und die modellierte nicht invasiv abgelesene Anzeige voraus. Ereignisse ausserhalb der geprüften Ellipse dürfen für die Untergrenze vollständig ausfallen. Die 41-Bit-Aussage wurde für den kleineren Kern gesondert berechnet. Ein Bauplan für eine störungsarme physische Digitalisierung folgt daraus noch nicht.

Zum Vergleich wurde zunächst pro Gerät die zu seinem eigenen κ skalierte Ellipse getestet. Sie besteht ebenfalls in allen 144 Familien. Die Kontrolle ohne anfängliche q-p-Korrelation besteht bei gleicher kanonischer Fläche auch. Die Korrelation reduziert die grösste zertifizierte Positionsabweichung am Speicher von weniger als 4,929·10⁻¹² auf weniger als 2,532·10⁻¹². Für diese Auswertung wurden zusätzlich 1 536 konkrete Phasen-, Hintergrund-, Geräte- und Quellkombinationen jeweils an beiden Orten digital klassifiziert. Der Versuch mit dem **identischen kanonischen** Anfangszustand fügt 576 digitale Einzelentscheidungen hinzu. Die Wahrscheinlichkeit oben folgt aus Integration und Intervallschranken, nicht aus einer Stichprobenquote.

## Welche physische Ressource fehlt?

Der kanonische Impuls ist P=2p. Die Fläche der Ellipse E≤1 im (q,P)-Raum beträgt 2πκ₀BV pro Spur. Für den hier tatsächlich gemeinsam benutzten Gaußzustand gilt √det Σ=2κ₀BV/9. Verglichen mit der für das starke Gerät allein passenden Vorbereitung ist die dafür erforderliche kanonische Fläche um den Faktor 10¹¹ kleiner.

Wird der **Eingangszeiger** als kanonischer Quantenmodus mit [q,P]=iℏ_eff modelliert, muss seine Kovarianz √det Σ≥ℏ_eff/2 erfüllen. Die hier gewählte Gaußkovarianz ist daher nur bei ℏ_eff≤4κ₀BV/9 verträglich. Das ergibt rund 4,44·10⁻³⁸ für den gemeinsamen Zustand und rund 4,44·10⁻²⁷ für die auf das starke Gerät zugeschnittene Alternative. Das sind Grenzen für diese konkreten Eingangszustände. Eine Quantenwahrscheinlichkeit für den nichtlinearen Staub- und Messprozess wird daraus nicht abgeleitet. [Weedbrook et al., Gaussian Quantum Information, Gl. 17 und 45](https://arxiv.org/pdf/1110.3234)

Eine zusätzliche Kontrolle betrachtet nur einen Zeiger bei festgehaltenen klassischen Staubfeldern. Die beiden idealen Positionsobservablen auf derselben Spur enthalten q+AᵣP/(2κ) und q+A₇P/(2κ). Da A₇−Aᵣ=1/w₇, verlangt ihre Unschärferelation σᵣσ₇≥ℏ_eff/(4κw₇). Würde man an beiden Orten höchstens 10⁻¹² RMS-Zeigerbreite fordern, erhielte man am kleinsten getesteten w₇ die notwendige Schranke ℏ_eff≤1,573·10⁻²⁶κ. Diese Zusatzfrage betrifft Zeigerbreiten vor einer Messung. Die getrennt vorgegebene elektronische Rundungsauflösung ist eine andere Grösse.

Schreibt man die physische Gesamtwirkung als S₀ mal die dimensionslose Modellwirkung, ist ℏ_eff=ℏ/S₀. Alle stationären Gleichungen allein legen S₀ nicht fest. Das Multiplizieren der gesamten Wirkung einschliesslich der Quell- und Randterme mit demselben positiven Faktor lässt ihre stationären Punkte unverändert. Der nächste physikalische Nachweis ist daher eine unabhängige Wirkungs- oder Impulskalibrierung für den Zeiger und seine Präparation. Erst damit lässt sich entscheiden, ob eine materielle Quelle die geforderte Phasenraumfläche und eine hinreichend störungsarme Auslese gemeinsam bereitstellen kann. Alle **60 physischen P3-Prüfpunkte** stehen auf `NOT_RUN`.

## Reproduktion

Nach dem Entpacken genügt `python3 -B pruefen.py` mit Python ab 3.10 und der Standardbibliothek. Das Programm prüft die SHA-256-Listen, reproduziert das im ZIP mitgelieferte Vorgängerpaket und vergleicht alle vier neuen JSON-Ergebnisse bytegenau. Eine Gegenrechnung prüft 218 partielle Ableitungen mittels exakter rationaler Wirkungsdifferenzen und vier exakte Identitäten nach Elimination der Gerätekoordinaten. Die Prüfpläne und Ergänzungen wurden vor ihren jeweiligen Rechnungen lokal gehasht. Die genauen Intervalle und die identischen ganzzahligen Ausgabecodes des 33-Bit-Gegenbeispiels stehen in den JSON-Dateien.
