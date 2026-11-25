# Schnitttransport, Präparationsmass und Randpaarung

## Modell

Die Totalordnung lautet (0,1,2,3,4,5,6,11,12,13,14,7,8,9,10). Die sieben mittleren Ereignisse bilden das Staubinnere. Das Paargewicht bᵢⱼ für null bis drei Zwischenereignisse lautet 1,−9,16,−8, sonst null. Die Staubwirkung ist

    S = −Σⱼ wⱼ/2 − (1/38) Σᵢ≺ⱼ bᵢⱼ wⱼ(Yⱼ−Yᵢ)².

Es gelten Δ⁴=3/722, D=Δ(4−e)>0 und Yⱼ=Y₃+(4−e)uⱼ im Inneren. Die beiden äusseren positiven Referenzfenster sind die Intervalle um o=±1/16 mit Halbbreite 1/32, e=o/Δ. In jeder positiven Dosis M liegt wⱼ=DM fⱼ(1+qⱼ), |qⱼ|≤1/100. Die Zellgrenzen in u sind die Mittelpunkte benachbarter Uhren und die beiden festen Enden 0,1. Die eingefrorene Referenzpräparation, die geometrische Ordnung und die skalare Paarung stimmen mit PR #359 überein. Innerhalb dieses einen Typs besitzt die masselose Skalarwirkung keine Abhängigkeit von u oder w. Für die faktorisierte Präparation und dieselbe Skalarpaarung in beiden Armen kann ihr gemeinsamer Faktor ausgeklammert werden. Diese Aussage und die zugehörigen ursprünglichen Rechenverträge sind in quellen/skalar.md und quellen/verklebung.md festgehalten.

## 1 · Transport einer Einfügung

Der Quellenort bleibt der Schnitt hinter 11. Am weitergereichten Uhrwert i∈{4,5,6} wird nur die für den rechten Wirkungsfaktor verwendete Kopie um t=s/√D verschoben, mit s=±1/8. Für jedes betroffene Paar ist der Phasenzuwachs

    dᵢⱼ(t) = bᵢⱼ wⱼ [2(Yⱼ−Yᵢ)t − t²]/38.

Bei einer Zerlegung hinter c∈{11,12,13,14} zerfällt der gesamte Zuwachs in die Summen über 11≺j≤c und j≻c. Der linke Faktor übernimmt die erste Summe, die rechte Kopie der Uhr die zweite. Sobald eine Quelluhr aus dem Vier-Uhren-Speicher verschwindet, kann ihr Abstand zu jedem späteren Ereignis nur noch grösser als vier sein. Ihre spätere Summe ist dann leer. Am unveränderten Schnitt 11 sind insgesamt sechs betroffene Paare vorhanden.

| Quelluhr | Ziele und Gewichte hinter 11 |
|---|---|
| 4 | 12 mit −8 |
| 5 | 12 mit 16, 13 mit −8 |
| 6 | 12 mit −9, 13 mit 16, 14 mit −8 |

Die Polynomkoeffizienten von 38d in wⱼYⱼt, wⱼYᵢt und wⱼt² stimmen bei jeder Aufteilung mit der direkten Intervallzählung überein. Im Test werden die vier Schnitte und drei Uhren ausserdem bei beiden Vorzeichen auf allen 15 Basisdichten verglichen. Die unveränderten ursprünglich präparierten Dichtefaktoren dürfen genau einmal eingehen. Auf der kompakten Box erlaubt die absolute Integrierbarkeit den Wechsel der Integrationsreihenfolge. Die Identität überträgt sich damit auf die bedingten und vollständig integrierten Amplituden. Wird der linke Phasenzuwachs weggelassen, verliert das Dreieckssystem aus PR #359 die Spalten der bereits passierten Zieldichten. Sein Rang sinkt von drei über zwei und eins auf null. Hinter 14 kommt die gesamte verbleibende Massenantwort aus der äusseren Eingangsquelle.

## 2 · Die offene Verweilzelle

Die linke Grenze der Zelle 11 ist (u₆+u₁₁)/2, die rechte (u₁₁+u₁₂)/2. Am Schnitt hinter 11 ist die rechte Grenze noch offen. Für die endgültige Länge folgt f₁₁=(u₁₂−u₆)/2. Alle vorherigen Zelllängen sind bestimmt. Die übrigen noch offenen Zellen hängen weder von u₄ noch von u₅ oder u₆ ab. Diese Aussagen folgen auch durch den im Prüfer ausgeführten Koeffizientenvergleich der Zellgrenzen.

Eine Verschiebung von Y₆ um ±h/√D verändert das normierte u₆ um ±q mit q=Δh/D³ᐟ². Auf dem vollständigen Träger ist 0,02716289 < q < 0,03585860. Setzt man den neuen Uhrwert auch im noch offenen Massfaktor ein, folgt f′=f∓q/2 mit f=f₁₁. Bei gleichen übrigen Uhren liegen die beiden zulässigen Bereiche für w₁₁/(DM) in [0,99 f;1,01 f] und [0,99 f′;1,01 f′]. Für beide Verschiebungsrichtungen ist ihr Abstand mindestens

    0,99 q/2 − 0,02 f  ≥  0,99 q_min/2 − 0,02 · 9/64  >  0,01063313.

Das betrifft das bedingte Mass bei gleichem Ereignis 12 und allen anderen festen Uhren. Eine Marginalisierung über verschiedene Uhrkonfigurationen kann Überlappung erzeugen. Die disjunkten bedingten Träger bedeuten auch nicht, dass jede einzelne verschobene Amplitude null wird. Im zweiten Versuch wird ihr eigener neuer Träger vollständig integriert.

Die Gauss- und Clenshaw-Curtis-Rechnungen werten beide Fortsetzungen mit der alten Normalisierung aus. Für M=1 ist der ursprüngliche Uhrfaktor D¹⁴∏8fⱼ. Beim Ändern des bedingten w₁₁-Bandes wird nur 8f₁₁ durch 8f′₁₁ ersetzt. In der analytischen w₁₁-Integration wird Df′₁₁ als Dichtemitte und Df′₁₁/100 als Halbbreite verwendet. Der Wirkungskoeffizient von w₁₁ bleibt alt, denn sein Ziel liegt auf der linken Seite des Quellschnitts. Der Faktor 8f′₁₁ ist die geänderte Bandbreite der Integration über w₁₁ im geerbten Mass. Die gleiche Gesamtpräparation bzw. Normierung des Nullarms dient als fester Bezug. Die vier äusseren Eingangsvariationen halten definitionsgemäss die präparierte Dauer und den ursprünglichen Dichtevertrag fest. Separate Normierungen pro Arm kommen nicht zum Einsatz.

Die zwei Vorschriften können als Fortsetzungen von der Diagonalen Y₆,L=Y₆,R gelesen werden. Die Wirkung liest die rechte Koordinate. Die unfertige Dichtezelle liest in einer Fortsetzung die linke und in der anderen die rechte. Auf der ursprünglichen Diagonalen stimmen beide Kerne für sämtliche Feldwerte überein. Die abgeschlossene unverschobene Paarung kann zwischen diesen Fortsetzungen nicht auswählen. Eine unveränderte Kopie des linken u₆ oder der linken Zellgrenze reicht aus, um die erste Fortsetzung zu realisieren. Ob die gekoppelte physikalische Randoperation eine solche Kopie benutzen darf, bleibt offen.

## 3 · Was auf den reduzierten Raum absteigt

Gesucht wird eine gemeinsame komplex-lineare Zusammenfassung beliebiger linker Testwellen, aus der sich alle sechs inneren Antworten und der Nullarm mit den weitergegebenen Randvariablen auslesen lassen. D ist bekannt. Der gewöhnliche Schnitt behält die letzten vier Wirkungsuhren und jede bereits erreichte, noch nicht mit ihrer letzten Uhrvariablen auswertbare Dichte. Hinter 11, 12 und 13 ist das jeweils w₁₁, w₁₂ und w₁₃, hinter 14 keine. Andere Integrationsdarstellungen können äquivalente offene Funktionen behalten. Zusätzliche vollständige historische Daten verändern die Kosten der Zusammenfassung.

Hinter 11 sind alle gezielten Paarphasen noch rechts einsetzbar. Eine komplexe linke Amplitude genügt. Hinter 12 betreffen die schon durchlaufenen Paare aller drei Arme nur das Ziel 12. Für die Arme 5 und 6 sind u₅, u₆, u₁₂ und w₁₂ vorhanden. Für Arm 4 ist u₄ bereits aus dem gewöhnlichen Speicher gefallen. In der linken Integration genügen drei Funktionen, nämlich die ungestörte und die beiden mit dem Paarbeitrag 4→12 multiplizierten Amplituden. Bei festem w₁₂>0 ergeben die zwei Verschiebungen in der verborgenen Variablen Y₄ entgegengesetzte, nichtverschwindende lineare Frequenzen. Zusammen mit der Nullfrequenz sind dies drei linear unabhängige Funktionen auf einem offenen Teil des Trägers. Der obere Rang drei ist damit scharf.

Hinter 13 und 14 ist w₁₂ vollständig integrierbar und gehört nicht mehr zu den festgehaltenen Randdaten. Setze e=1/4, uⱼ am jeweiligen Zentrum und v=100q₁₂, gleichförmig auf [−1,1]. Die Grundphase exp(iS) wirkt bei Konjugation aller Testwellen mit ihrem linken Anteil als gemeinsamer Faktor. Jede der sechs bereits am Ziel 12 eingegangenen Einfügungen liefert in v eine eigene Exponentialfunktion exp(iλₐv) mit

    λᵢ,ₛ = (D/800)(bᵢ₁₂/38)[2(Y₁₂−Yᵢ)s/√D − s²/D].

Hier gilt f₁₂=1/8, M=1. Spätere oder andere bereits verarbeitete Beiträge hängen bei festgehaltenen übrigen Variablen nicht von v ab. Die kleinste Trennung der sieben Frequenzen einschliesslich λ₀=0 übersteigt 4,78464·10⁻⁵. Der Einschluss stammt aus 256-Bit-Intervallarithmetik. Ableiten einer angenommenen linearen Abhängigkeit bei v=0 bis zur sechsten Ordnung ergibt eine Vandermonde-Matrix mit von null verschiedener Determinante. Die Stetigkeit erhält die strikte Trennung in einer Umgebung der zentralen Uhren, in der das Präparationsmass positiven Träger hat. Unabhängige Antwortfunktionale können nicht durch weniger als sieben gemeinsam gespeicherte komplex-lineare Komponenten faktorisieren. Die sieben getrennt fortgetragenen Amplituden erreichen diese Schranke. Das Ergebnis gilt für beliebige linke Testwellen dieser Darstellung. Es zählt weder benötigte physische Qubits noch unabhängig präparierte Experimente.

Ein konstruktiver Zeuge für den Rangverlust der einzelnen kohärent reduzierten Amplitude ist die auf der festen v-Faser normierte Testwelle √3 v mit zurückgedrehter linker Grundphase. Ihre ungestörte Einfügung hat Integral null. Nach dem positiven Puls an Uhr 4 beträgt der Betrag des bedingten v-Integrals

    √3 |∫₀¹ v sin(λ₄₊ v) dv| ∈ [0,00006711816865; 0,00006711816875].

Die Schranken folgen aus |λ|/3−|λ|³/30 ≤ |∫ v sin(λv)dv| ≤ |λ|/3. Die 32-Punkt-Gaussregel prüft den Betrag auf einem zweiten Weg. Für eine lineare Abbildung Q₀ auf die ungestörte kohärente Amplitude müsste ein nachträglicher Operator O mit Q₄₊=O Q₀ jede Nullrichtung von Q₀ erhalten. Der Zeuge verletzt diese notwendige Bedingung. Die auf diesem festen Typ faktorisierte Skalarpaarung multipliziert beide Abbildungen mit demselben Faktor und behebt den Informationsverlust nicht. Damit ist die spätere Realisierung auf dem bereits so projizierten Kanal ausgeschlossen. Das sagt nichts Abschliessendes über eine andere physikalische Paarung oder einen grösseren gekoppelten Zustandsraum aus.

Die sieben Zeilen der Faserabbildung sind trotz mathematischer Unabhängigkeit sehr nahe aneinander. Es gibt einen normierten Koeffizientenvektor, der die Potenzen der sieben λ von Grad 0 bis 5 annihiliert. Der Integralrest der Exponentialreihe liefert auf dem reellen Intervall den Betrag ≤ |λv|⁶/720. Für die gleichförmige L²-Norm gilt ||v⁶||=1/√13. Damit ist die kleinste singuläre Zahl höchstens √7 max|λ|⁶/(720√13), die grösste wegen des Nullarms mindestens eins. Die rigorose Konditionsuntergrenze übersteigt 2,16·10²⁵. Diese Aussage betrifft die sieben gleich normierten Zeilen auf der angegebenen Faser. Sie ist keine Fehlerverstärkung der direkt aus den elf vorwärts berechneten Phasen gewonnenen Massenwerte.

## 4 · Was eine physikalische Paarung zusätzlich leisten müsste

Für die Darstellung als diagonale Hilfsphasen Vₐ ist eine gegebene hermitesche Gram-Matrix G genau dann invariant, wenn Gₕₖ[exp(i(δₐ(k)−δₐ(h)))−1]=0 für alle Historien h,k und alle betreffenden Arme. Diese Gleichung folgt direkt durch Einsetzen in Vₐ† G Vₐ=G, beispielsweise auf zwei endlichen Testkomponenten. Für kontinuierlich variable Schrittweite müssen bei einem nichtverschwindenden Kreuzterm die linearen und die quadratischen Koeffizienten der Phasen der beiden Geschichten übereinstimmen. Die drei quadratischen Kombinationen sind auf (w₁₂,w₁₃,w₁₄)/D invertierbar. Gemeinsame Isometrie für alle Schritte in dieser Darstellung verlangt daher Gleichheit dieser drei skalierten Dichten zwischen so gekoppelten Komponenten. Die Prüfergebnisse für die diskreten ±h beruhen nicht auf dieser zusätzlichen Forderung kontinuierlicher Schritte.

Eine kontrollierte Einfügung auf einer feineren Geschichte vor der Projektion ist davon verschieden. Die nächste offene physikalische Entscheidung ist, ob ein äusserer Eingriff die bedingte Präparation der Dichte an 11 überhaupt mitverschiebt. Auf der positiven Referenz ist diese Frage wegen der disjunkten bedingten Bänder entscheidbar, falls ein unabhängig hergeleiteter Zugriff auf w₁₁ oder eine dazu äquivalente Randgrösse vorliegt. Eine erneute Anpassung der Eichung an die markierte Masse 1 würde diese Wahl nicht entscheiden. Es wird kein P3-Datensatz erzeugt.
