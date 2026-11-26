# CST-DUST N19 · Pulswahl am Empfänger und Paarung zweier Stromläufe

**Ergebnis vom 26. November 2026.** Im stationären N19-Modell kann ein passiver Empfänger mit seiner eigenen Uhr und zwei vorangehenden Leeruhren in einem Lauf die drei vorgegebenen Quellen unterscheiden. Ein absoluter Fehler von höchstens 10⁻¹¹ Modelluhreinheiten je Uhr genügt auf den beiden registrierten Fenstern. Eine zweite Frage ist die Grösse der Senderstromänderung. Dafür liefern vier Staubgewichte und die beiden Leeruhren eine unabhängige Vorhersage. Diese Daten lassen sich in der gegebenen Kausalordnung zuerst bei Ereignis 7 gemeinsam auswerten, nach dem Empfänger bei Ereignis 18. Die Nummern bezeichnen Ereignisse, ihre Reihenfolge ergibt sich aus der Kausalordnung.

Es gelten die unveränderte endliche Ordnung, die native stationäre Materiewirkung, die positiven Materiefenster und ein fester kalibrierter Anfangskragen. Am Sender 16 wirkt allein eine Dichtequelle J ∈ {−10⁻⁶, 0, +10⁻⁶}. Der Senderuhrimpuls und die Empfängergleichungen bleiben ungetrieben. In jeder Fortsetzung sind die Daten ausserhalb des Senders und seiner Zukunft fest. Verschiedene Versuche dürfen unterschiedliche zulässige Ausgangszustände haben. Uhrenwerte, Quellen und Ströme werden in den Einheiten dieser Wirkung angegeben.

[Öffentlicher Ausgangsstand mit der gepaarten Polungsschranke, PR 389](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/389)

## Welcher Puls traf ein?

Die Eingabe besteht allein aus u=Y₁₅, h=Y₁₇ und dem abgelesenen t=Y₁₈. Die ersten beiden Ereignisse liegen in der Vergangenheit von 18. Die Auswertung setzt voraus, dass ihre Uhrenwerte am Empfänger verfügbar sind. Am Sender gibt es keine Ablesung. Es wird auch kein separater Nullversuch benötigt. Für jeden möglichen Quellenwert ℓ liefert die Senderdichtegleichung eine Uhr und die Empfängerdichtegleichung ein prüfbares Residuum

    sℓ = (u² − 6 − ℓ) / [2(u+3)]
    Fℓ = 19 − 8(t+4)² + 16(t+3)² − 9(t−u)² + (t−sℓ)² + (t−h)².

Die Regel wählt das kleinste |Fℓ|. Für die wahre Quelle J ist Fⱼ=0 bei exakten Daten. Die Differenz Fℓ−Fⱼ=(sⱼ−sℓ)(2t−sⱼ−sℓ) erlaubt eine Schranke für die Trennung aller drei Kandidaten. Die kontinuierliche Intervallrechnung überdeckt beide registrierten Fenster sowie e∈[1/6−2⁻²²,1/6+2⁻²²] und gilt für darin zulässige Nullzustände und Pulsfortsetzungen. Aus den Nullfenstern werden u und h mit der chronologischen Wurzel ihrer Dichtezeilen begrenzt. Die Senderuhren aller Kandidaten werden um ihren maximalen Quellenversatz und den Ablesefehler erweitert. Für t wird das gesamte zugelassene Empfangsfenster erweitert. Die Uhren am Anfangskragen in den beiden Dichtezeilen gelten als exakt geeicht.

Bei drei unabhängig beschränkten Uhrfehlern von je höchstens 10⁻¹¹ bleibt der Abstand zweier Kandidatenresiduen am gemeldeten Tripel grösser als 1,8676·10⁻⁹. Die Summe der Beträge der drei partiellen Ableitungen von Fⱼ ist im erweiterten Gebiet kleiner als 58,531. Das wahre Residuum hat daher Betrag unter 5,8531·10⁻¹⁰. Sein Doppeltes liegt unter der garantierten Trennung. Damit bleibt der Gewinner eindeutig, auch zwischen den geprüften Stützstellen.

| Überprüfung | Ergebnis |
|---|---|
| 12 Hintergründe mit je drei Quellen | 36 von 36 Quellen richtig |
| Acht Eckpunkte der unabhängig gestörten drei Uhren je Fall | 288 von 288 richtig |
| Zweiter Rechenweg | Die chronologische Inversion der Empfängerzeile liefert in allen 36 Fällen ein Intervall, das genau ein Quellenetikett enthält. |
| Gröbere Auflösung am Referenzzustand | Nullpuls und positiver Puls unterscheiden sich an 18 um rund 5,60314·10⁻¹⁰. Bei ±3·10⁻¹⁰ allein an dieser Uhr ist ihr Mittelpunkt mit beiden Quellen vereinbar, selbst bei exakten u,h. |

Die zwei Fehlergrenzen sind eine hinreichende Auflösung für alle zugelassenen Fenster beziehungsweise ein Unmöglichkeitsbeispiel bei gröberer Auflösung. Die optimale Schwelle dazwischen bleibt offen. Die Klassifikation gilt für die drei festgelegten Quellen und die angegebenen passiven Gleichungen. Eine zusätzliche unabhängige Störung am Empfänger wäre eine andere Messaufgabe.

## Wie lassen sich die Stromänderungen zweier Läufe vergleichen?

Für die Vorhersage der Änderung ΔK gegenüber dem jeweiligen Nullarm werden beide Endpunkte einschliesslich ihrer Uhren und Gewichte sowie alle vier späten Randfelder ausgeblendet. Erlaubt sind die Anfangsuhren bei 0–3, die Uhren u,h und die Gewichte an 4,11,12,13. Hier ist der Anfangskragen auf e=1/6 geeicht. Die positiven Dichtezeilen bestimmen die Zwischenzeiten an 4,5,6,11,12,13,14. Der Leser prüft, dass nur eine Wurzel nach allen Vorgängern liegt.

Sei mᵢ=Σₖ bₖᵢ(Yᵢ−Yₖ), wobei die Koeffizienten b aus der N19-Ordnung folgen. Aus der Uhrzeile an 4 und den gemeinsamen Zukunftskoeffizienten L=(−9,16,−8,0) der Zeilen 12 und 13 erhält man

    w₁₄ = [w₁₁(Y₁₁−Y₄) − 9w₁₂(Y₁₂−Y₄) + w₁₃(Y₁₃−Y₄) − w₄m₄] / [8(Y₁₄−Y₄)]
    a = (w₁₂m₁₂−w₁₃m₁₃)/(Y₁₃−Y₁₂)
    W = a−w₁₄,     M = w₁₂m₁₂+Y₁₂a−Y₁₄w₁₄,     P = hW−M.

Auf den Lösungen sind W und M die gewichteten Summen L·w und L·(wY) über die vier späten Randereignisse. Sie werden aus den freigegebenen Daten berechnet. Die ungetriebenen Uhrzeilen an 17 und 16 ergeben für die im Empfangsfenster gewählte Wurzel tⱼ

    wᵣ,ⱼ = P/(tⱼ−h)
    w𝓏,ⱼ = (h−sⱼ)(W+wᵣ,ⱼ)/[−(u+3)]
    Kⱼ = w𝓏,ⱼ(sⱼ−u),     ΔKⱼ = Kⱼ−K₀.

Der Referenzwert T ist die aus diesen Daten vorhergesagte positive Änderung ΔK bei der negativen Quelle. Für den positiven Puls aus Hintergrund A und den negativen aus B ist Qₖₒᵣᵣ = −[ΔK₊(A)/ΔK₋(B)]·T(B)/T(A). Wenn das Modell stimmt, entspricht dies genau dem gepaarten Verhältnis für A. Damit wird eine Änderung der erwarteten Stromstärke zwischen den beiden Ausgangszuständen berücksichtigt. Ein physischer Test braucht für die beiden ΔK eine unabhängige differentielle Strommessung oder jeweils einen passend präparierten und gemessenen Nullarm. Eine Normierung mit den gemessenen Pulsströmen selbst wäre zirkulär.

Zwölf geprüfte Hintergründe umfassen die sechs publizierten Eich- und Randimpulszustände, zwei Variationen der Empfangsuhr, zwei der frühen Leeruhr und zwei neu konstruierte Zustände mit gleichem Empfängergewicht. Die 20 ursprünglichen inneren Gleichungen, positive Gewichte, Chronologie und beide Materialfenster wurden je Null- und Pulsarm geprüft. Die Vorhersagen werden im Ablauf vor dem Vergleich mit den unabhängig aus den vollständigen Feldern fortgesetzten Pulsarmen festgeschrieben. Es handelt sich um modellinterne Rechnungen. Die beiden Prüfpläne besitzen lokale SHA-256-Festlegungen ohne externen Zeitstempel.

| Vergleich | Befund |
|---|---|
| Alle 144 geordneten Kombinationen | 117 rohe Verhältnisse ausserhalb der publizierten Schranke [0,99999973; 1,000944]. Nach Normierung liegen alle 144 darin, im untersuchten Satz zwischen 1,00000028556 und 1,00000086982. |
| G₀ und G₁ identisch, zwei verschiedene Zustände | 2,99828044 ergibt korrigiert 1,00000028557, die umgekehrte Zuordnung ergibt aus 0,33352489 den Wert 1,00000086981. |
| Gleichheit der Referenzantwort | Alle 66 unterschiedlichen Hintergrundpaare im Hauptsatz haben bei exakten Eingaben trennbare T. Als zusätzliche Kontrolle haben zwei verschiedene vollständige Historien mit verschobenen Zukunftsgewichten identische Eingaben, identisches T und gleiche Stromänderungen. Eine Übereinstimmung von T belegt nur die Übereinstimmung dieser Antwortgrösse. |
| Gegenrechnung | Über die Kausalordnung neu ermittelte Schichtkoeffizienten, direkte späte Momente und unabhängige Intervall-Gauss-Elimination der drei Uhrzeilen stimmen in 36 stationären Lösungen mit der Vorhersage überein. |

Die vier Gewichte können bei 14 erstmals zusammenkommen. Die erste gemeinsame Sammelstelle für alle sechs Eingaben und das Anfangsprofil ist 7. Im Empfängerkegel liegen nur 0,1,2,15,16,17,18. Ein konstruiertes Paar zeigt die Grenze einer früheren Amplitudenkontrolle. Die beiden Nullzustände unterscheiden sich dort einzig im verborgenen Sendergewicht. Bei jeder der zwei Polungen bleiben alle im Kegel ablesbaren Uhren und alle übrigen Gewichte identisch. Dies folgt aus den gleichen Anfangsuhren, den gleichen u,h, der jeweils gleichen Quelle und dem gleichen Nullwert von wᵣ, der über wᵣ,ⱼ=wᵣ,₀(t₀−h)/(tⱼ−h) gleich fortgesetzt wird. Dennoch unterscheiden sich die Senderstromänderungen. Jeder Schätzer aus den so zugelassenen Kegeldaten muss für mindestens einen der beiden Zustände mindestens 9,99 % relativen Fehler zulassen, bei jeder Polung. Für zwei mögliche positive Beträge L<H am selben Messwert ist die optimale maximale relative Abweichung (H−L)/(H+L).

## Welche Auflösung verlangt der Stromvergleich?

Für die zwölf geprüften Hintergründe wurden vollständige unabhängige Eingabefehlerboxen propagiert. Bei relativen Gewichtsfehlern bis 10⁻⁶ und absoluten Fehlern der beiden Leeruhren bis 10⁻⁸ beträgt der garantierte relative Fehler von T höchstens 0,016241 %. Bei zusätzlich höchstens 0,025 % relativem Fehler jeder gemessenen Stromänderung liegt das gemeldete Qₖₒᵣᵣ in [0,99917526; 1,00176967]. Das erfüllt die festgelegte Modelltoleranz von ±0,2 % für diese Hintergründe.

Wird eine kleine Änderung ΔK aus zwei absoluten Stromablesungen gewonnen, genügen je Ablesung höchstens 3,05·10⁻¹² absolut oder 7,17·10⁻¹¹ relativ, jeweils als getrennte hinreichende Bedingung für dasselbe Fehlerbudget. Die modellbasierte Subtraktion eines aus den vier Gewichten geschätzten K₀ ist empfindlich. Ein gemeinsamer zulässiger Verstärkungsfehler von 10⁻⁶ in allen vier Gewichten verschiebt K₀ in sämtlichen zwölf Fällen um mehr als den Betrag des negativen Testpulses. Alle genannten Auflösungen sind Anforderungen in Modellgrössen.

## Physischer Anschluss und Reproduktion

Die Uhren 15 und 17 sitzen an Ereignissen mit verschwindendem Staubgewicht. Als nächstes ist zu prüfen, ob ein materielles System dem Empfänger die für die Quellwahl nötige Uhreninformation mit begrenzter Rückwirkung übermitteln kann. Die Ordnung erlaubt das Zusammentreffen bei 18. Eine materielle Speicherung oder Übertragung mit der nötigen Genauigkeit ist noch offen. Alle 60 physischen P3-Prüfpunkte stehen auf `NOT_RUN`.

Nach dem Entpacken startet `python3 -B pruefen.py` mit Python ab 3.10 die Offline-Prüfung. Sie kontrolliert SHA-256, reproduziert die mitgelieferte Vorgängerkette und vergleicht alle vier neuen JSON-Berichte bytegenau. Die rationalen Intervallgrenzen in den JSON-Dateien sind massgebend. Das Paket enthält die Programme, Prüfpläne, Eingaben, Lizenz und Reproduktionsergebnisse.
