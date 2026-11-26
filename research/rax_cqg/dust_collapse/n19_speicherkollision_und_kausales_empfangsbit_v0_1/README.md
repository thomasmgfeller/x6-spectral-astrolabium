# N19 · Welche Information fehlt am Speicherort 7?

**26. November 2026.** Auf dem Viertelhintergrund gibt es zwei vollständig nachgerechnete N19-Zustände mit verschiedenen Quellen und identischen sieben lokalen Ziffern am Speicherort 7. Kein Leser dieser Ziffern kann beide Zustände richtig zuordnen. Ein einziges zusätzliches Bit aus der Empfangsuhr an 18 genügt im geprüften klassischen Modell für die drei Quellstärken, zwölf Hintergründe, zwei Geräte und zwei Transportwege. Es benötigt eine unabhängig bereitgestellte Nulluhr des passenden Hintergrunds. Für die speziell strukturierte 729-Zustände-Verteilung der Vorgängerstudie genügt bereits eine verbesserte Nutzung der vorhandenen Ziffern. [Veröffentlichter Ausgangsstand, PR 393](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/393)

## Wann die vorhandenen Ziffern ausreichen

Seien y=p/(κ₀V) der normierte halbe kanonische Zeigerimpuls **nach der Ortsaufnahme** und x=q/B+2,5y. Es gelten B=10⁻¹², V=10⁻¹⁴ und κ₀=10⁻¹¹. In der endlichen Testverteilung sind x und y je Spur unabhängig aus {−64,0,64} gezogen. Die gespeicherte Anfangsziffer für q=B(x−2,5y) liegt auf dem Raster 2B. Sie bestimmt in diesem speziellen Modell bereits das Impulszentrum:

| Anfangsziffer | Normiertes Impulszentrum |
|---|---:|
| −112, −80, −48 | +64 |
| −32, 0, +32 | 0 |
| +48, +80, +112 | −64 |

Der Leser subtrahiert von der gemessenen Verlagerung zusätzlich den vorhergesagten Impulsbeitrag Ā·(κ₀/κ)·V·y_c. Die Transferzahl Ā ist die Summe inverser Trägheitsgewichte der jeweiligen Spur bis zum Leser. Sie wird aus einem getrennten, quellfreien Referenzhintergrund auf 1/32 gerundet. Die unbekannte Quelle, die Gewichte der gepulsten Lösung und das wahre y sind keine Eingaben bei der Klassifikation. Die nachgerechneten 729 Zustände in jeder der 144 Familien ergeben **104 976 korrekte gemeinsame Entscheidungen** an 18 und 7. Ganzzahlige Verschiebungen auf dem Digitalraster liefern dieselben Differenzziffern. Der Volltest prüft alle Anfangsziffern und fasst identische Residuenberechnungen zusammen.

Für stetige Präparationen prüfen wir Kästen |x−x_c|≤r und |y−y_c|≤r um alle neun Zentren je Spur. Zusätzlich sind ein analoger Anfangsfehler bis B, die beiden Rundungsfehler, die veröffentlichten Geräteabweichungen und weitere ±1/16 in der kalibrierten Transferzahl zugelassen. Die Rechnung schliesst die Rückwirkung der Nachimpulse und die endliche Änderung des nichtlinearen Quellenresiduums ein.

| Halbbreite r | Familien mit positivem Abstand zu beiden falschen Quellen an beiden Orten |
|---:|---:|
| 0 bis 1, auf dem registrierten Raster | 144 von 144 |
| 2 | 138 von 144 |
| 4 | 96 von 144 |

Bei r=4 sind die Impulszentren unter der angegebenen Rundung noch aus der Anfangsziffer unterscheidbar. Schon bei r=4,01 können zwei Zentren dieselbe Ziffer erzeugen. Ortsdaten allein belegen daher keine universelle Impulsmessung. Eine Gegenkontrolle verwendete die Transferzahlen des Referenzhintergrunds für das Viertelgerät. Von den 324 Einzelentscheidungen über Quellen, Wege, Orte und Impulstripel des schwachen Geräts waren dabei 180 falsch oder unentscheidbar.

## Zwei Quellen mit identischem vollständigem Speicherwort

Für den folgenden Vergleich gelten derselbe Viertelhintergrund, derselbe positive Transportweg, κ=10⁻¹¹ und drei gleiche Anfangsorte q=0. Die Impulse beider Zustände liegen innerhalb |y|≤59,08. Die sieben Ziffern enthalten die lokale Uhr, alle drei Endanzeigen und alle drei gespeicherten Anfangsanzeigen. Die einzelnen rationalen Impulswerte wurden nach der Suche erneut in den vollständigen stationären Löser eingesetzt. Die beiden Quellen und sämtliche Digitalisierungen sind durch Intervalle bestätigt.

| Wahre Quelle | Nachimpulse (yᵤ, yₕ, yₜ) | Empfangsuhrziffer an 18 |
|---|---|---:|
| −10⁻⁶ | (58,908; 58,877; −58,900) | 42 180 625 335 |
| 0 | (−59,049; −59,080; 59,057) | 42 180 625 615 |

Das Speicherwort beider Zeilen ist exakt `[1000000000000, 1275949542060, 2283265466784, 957819374525, 0, 0, 0]`. Auch für die Quellen 0 und +10⁻⁶ gibt es auf demselben Hintergrund ein gemeinsames Wort mit |y|≤59,146. Die Werte sind nachgewiesene Beispiele. Eine kleinste Kollisionsgrenze wurde nicht bestimmt. Für die kleinere Box |y|≤48 trennen sich bei passend geeichter Nulluhr die drei Wertebereiche der späten Uhrdifferenz in allen 48 Geräte-, Wege- und Hintergrundkombinationen. Die Mindestlücke beträgt 38 digitale Schritte.

Eine zweite Gegenprobe vermeidet die Annahme, der Präparator richte die Impulse nach der Quelle. Wir konstruieren **eine einzige quellenunabhängige Verteilung auf 17 Punkten**. Alle sechs Mittelwerte sind null, alle Varianzen genau 1/9, alle Kreuzkovarianzen null. Damit stimmt auch die gesamte kanonische Kovarianz in (q,P) mit der früher geprüften Gaußpräparation überein. Höhere Momente und Abhängigkeiten der Koordinaten unterscheiden sich. Zwei symmetrische Paare tragen die Kollisionszustände. Eine rationale LDL-Zerlegung der positiven Restkovarianz liefert sechs weitere symmetrische Paare. Am Ursprung liegt die verbleibende Wahrscheinlichkeit.

Bei drei unabhängig und gleich häufig gewählten Quellen berechnen wir für jedes vollständige Wort die gemeinsame Masse jeder Quelle. Jede Entscheidung muss mindestens die gesamte Masse der jeweils unterlegenen Quellen verfehlen. Durch Wahl der jeweils häufigsten Quelle ist diese Schranke erreichbar. Über die 51 Kombinationen aus Quelle und Zustand beträgt der **kleinstmögliche Fehler am Speicher genau 1/4 000 000** bzw. 0,000025 %. Mit dem unten definierten Empfangsbit ist er für diese Verteilung null. Die Überschneidungen der Wortmassen und die rationalen Gewichte aller 17 Zustände stehen in `Kovarianzzeuge.json`.

## Welches zusätzliche Bit genügt?

Bezeichne Q eine auf das Raster 2·10⁻¹² gerundete Position oder Uhr in ganzen Schritten. T₀ ist die Uhr des quellfreien, unbelasteten Referenzhintergrunds und wird vor dem Test aus einem unabhängigen Bezug bereitgestellt. Eine zusätzliche Unsicherheit von ±10⁻¹¹ ist eingerechnet. Die beiden Orte verwenden folgende Regel:

1. An 18 setze das Bit auf 1, falls |Q(T₁₈)−Q(T₀)| > 125, sonst auf 0. Der Empfänger kann bei gesetztem Bit auch das Vorzeichen aus der eigenen Uhrabweichung lesen.
2. An 7 berechne D₇=Q(T₇)−Q(Xₜ,₇)+Q(qₜ,₀)−Q(T₀). Bei Bit 0 melde die Nullquelle. Bei Bit 1 entscheidet das Vorzeichen von D₇ zwischen den beiden Pulsen.

Weg, Versuchskennung und Identität der Nulluhr sind vorab verabredet. Die zusätzliche zustandsabhängige Nachricht enthält genau ein Bit. Der Leser an 7 benötigt für diese Regel nur seine Uhr und die dritte Zeigerspur mit ihrer Anfangsreferenz. Die Impulse der beiden übrigen Spuren werden weiterhin in der Rückwirkung auf die Staublösung berücksichtigt. Die Nullreferenz des Zeigers darf um B abweichen.

| Unabhängige Grenzen jeder der drei Spuren | Zertifizierte Modellfamilien mit einem Bit | Kleinster vorzeichenrichtiger Betrag von D₇ bei einem Puls |
|---|---:|---:|
| bis 64 | 144 von 144 | 91 Schritte |
| bis 96 | 144 von 144 | 15 Schritte |
| bis 112 | 143 von 144 | die Schranke reicht einmal nicht |

Die Grenzen in der ersten Spalte beziehen sich auf den Betrag des normierten Nachimpulses. Die Aussage gilt pro Familie für den ganzen dreidimensionalen Impulsbereich, beliebige |q|≤1 und die vorgegebenen Geräteabweichungen. Die Nullquelle weicht an 18 um höchstens 36 Schritte von der Nulluhrziffer ab. Jede Pulsquelle liegt in vorzeichenrichtiger Richtung mindestens 244 Schritte entfernt. Bei m=64 dürfte der schon kalibrierte gemeinsame Referenzcode zusätzlich um bis zu 89 ganze Schritte verschoben sein, bei m=96 um bis zu 14. Das ist eine rechnerische Reserve unter dem angegebenen Fehlermodell.

Die Kollision bei |y|≤59,08 zeigt, dass ein Leser an 7 mit dem bisherigen Datenumfang den Bereich |y|≤64 nicht gleichmässig auflösen kann. Der Bitnachweis gibt für diesen Vertrag die minimale **zusätzliche Information im schlechtesten Fall** an. Er setzt die passende quellfreie Kalibrierung und einen korrekt übertragenen Bitwert voraus. Er bestimmt weder die minimale Energie des Speichers noch die globale Impulsschwelle dieser Konstruktion.

## Hintergrundwechsel und dynamischer Registerterm

Eine absolute Empfangsuhr ohne passenden Nullbezug kann ebenfalls mehrdeutig sein. Für eine positive Quelle und für einen ungetriebenen, leicht zeitlich verschobenen Hintergrund erhalten wir dieselbe Ziffer 42 180 625 895. Die vier frühen nativen Uhrenimpulse bleiben bei der Konstruktion des alternativen Nullhintergrunds erhalten. Die jeweils separat ermittelten Nullcodes unterscheiden die beiden Fälle. Vier zusätzliche, vorher für den Leser unbenutzte Hintergründe bestehen mit ihrer eigenen Nulluhr bei m=96 in 48 von 48 Fällen. Ein gekipptes Bit kann eine falsche Quellwahl auslösen. Eine fehlende oder falsch zugeordnete Nachricht wird zurückgewiesen.

Die N19-Ordnung enthält die unmittelbare Relation 18→7. Als konkrete klassische Erweiterung benutzen wir zwei Register C₁₈ und C₇. Ein lokaler glatter Komparator f(d) ist für |d|≤100 null und für |d|≥150 eins. Hier ist d die analoge Uhrdifferenz in digitalen Schritten. Zwischen den Bereichen verwenden wir 3z²−2z³ mit z=(|d|−100)/50. Auf allen zertifizierten Eingängen reproduziert f die eingefrorene digitale Entscheidung. Die zusätzliche Modellwirkung lautet

    (C₁₈−f)²/2 + (C₇−C₁₈)² − L C₇.

Bei vorgegebener Endlast L haben die beiden Registergleichungen die eindeutige Lösung C₁₈=f+L und C₇=f+3L/2. Der Beitrag zur Uhrenvariation ist proportional zu −L f′. Auf beiden konstanten Bereichen verschwindet er exakt. Im Übergangsbereich kann er ungleich null sein. Für |L|≤1/8 und zusätzlichen Registerlesefehler ≤1/8 beträgt die gesamte Ausgangsabweichung höchstens 5/16. Zur Bitschwelle 1/2 verbleibt ein Abstand von mindestens 3/16. Die beiden positiven Steifigkeiten sind hier feste Geräteparameter. Die Rechnung beschreibt eine stationäre Geräteerweiterung und enthält keinen experimentellen Nachweis eines physischen Übertragungskanals.

## Reproduktion und Messstand

Python ab 3.10 und die Standardbibliothek genügen. Nach dem Entpacken:

    python3 -B pruefen.py
    python3 -B leseprotokoll.py senden Beispiel_Empfang.json > paket.json
    python3 -B leseprotokoll.py lesen Beispiel_Speicher.json paket.json

Der erste Befehl prüft die SHA-256-Dateien, reproduziert den eingefrorenen Vorgänger und vergleicht acht neue JSON-Dateien bytegenau. Die weiteren Befehle demonstrieren die getrennten lokalen Eingaben an den beiden Orten. Die Paketkennung darf keine Information über die Quelle enthalten. Für den Modelltest sind alle Beispieldaten synthetisch. Vier lokal gehashte Prüfpläne dokumentieren die Reihenfolge der Untersuchungen. Die 125-Schritt-Schwelle wurde nach einer ersten unbelasteten Modellabschätzung festgelegt und vor der Kollisions- und Intervallrechnung eingefroren.

Der nächste physische Nachweis benötigt eine unabhängige Eichung der Nulluhr am selben Aufbau, einen störungsgeprüften Bittransport und eine getrennte Messung des Impulses nach der Ortsaufnahme. Im ausgewerteten N19-Stand liegen keine entsprechenden Gerätemessungen vor. **Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.**
