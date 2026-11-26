# Der Arealradius aus einem endlichen Zeitfenster

**CST-DUST · Forschungsnotiz 0.1 · 26. November 2026**

Lässt sich die äussere Staubfläche aus Messungen vor und nach dem Zielschnitt bestimmen? In zwei klassischen Staubhistorien genügen zeitlich gemittelte Beobachtungen benachbarter Schalen, um den Radius bei halber Referenzzeit auf besser als 2,04 % einzugrenzen. Auf der geprüften N19-Historie fehlen im selben normierten Zeitfenster Ereignisse für die gewählte zweiseitige Ablesung. Der Versuch, die zwei fehlenden Ereignisse zwischen Sender und Empfänger zu ergänzen, stösst auf eine Bedingung der Staubwirkung. [Veröffentlichter Leitartikel und Ausgangsdaten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/e2f74ef37fc572efeff2f2f7cb99b4b4cbeee852/research/rax_cqg/dust_collapse/leitartikel_arealradius_und_zwei_massen_pilot_v0_1)

## Die zeitlich gemittelte klassische Messung

Je Masse werden auf derselben marginal gebundenen Lemaître–Tolman–Bondi-Lösung Anfangsladung, Materialgrenze und Geometrie beobachtet. Der frühere Massenprüfer bestimmt die Verstärkung aus Vakuum und einem einzigen Standard bei M = 1/4. Sie wird auf M = 4 übertragen. Die radiale Stationsreihenfolge und ihre vollständige Abdeckung sind gewährt. Von 641 mitbewegten Stationen begrenzen die Indizes 492 und 493 die Kante. Auf der ganzen Blockdauer bleibt das Materiesignal innen positiv und aussen null. Der Vakuumfall liefert keine Kante. Die innere mitbewegte Scheinschale bei a = 5 umschliesst 17/64 der Materie. Die besetzten Stationen weiter aussen verwerfen sie trotz verschwindendem Seitenfluss.

**Zwei getrennte geometrische Beobachtungen.** Für die vollständig innere und die vollständig äussere Nachbarschale gibt es je ein Eigen-Viervolumen und den Eigenflächeninhalt eines radialen Zeit-Raum-Streifens entlang eines mitbewegten Strahls. Division durch die Blockdauer liefert das mittlere Eigen-Dreivolumen und die mittlere radiale Eigendicke. Diese beiden Kanäle werden in der Kontrolle aus der analytischen Lösung synthetisiert. Beide Mittel erhalten je ein Intervall von ±1 % um den Idealwert. Der Leser verwendet eine gemeinsame obere Grenze 1 für den Betrag der zeitlichen Änderung des Randradius in Einheiten G=c=1. Die Kontrollfamilie erfüllt sie über beide Fenster, weil |dR/dT|² = 2M/R und R am späten Rand des grösseren Fensters für beide Massen grösser als 2M ist.

Auf den marginal gebundenen Schnitten ist der Quotient Q = mittleres Volumen / (4π · mittlere Dicke) ein mit dem positiven Element dℓ dT gewichtetes Mittel von R² in der Schale. Zu jedem Zeitpunkt liegen alle inneren Schalenradien unterhalb der Kante und alle äusseren oberhalb. Mit D = h · T_end, der grössten erlaubten Randbewegung zwischen Blockmitte und Blockende, folgt die garantierte Einschliessung

> √Q_in,min − D ≤ R(T*) ≤ √Q_out,max + D.

Hier gilt x = T/T_end, T_end = 5√5/3, T* = T_end/2. Die gesamte Blockdauer beträgt 2h · T_end. Der Leser verwendet die vorgegebenen Kanäle, die Dauer und die Geschwindigkeitsgrenze. Die Referenzradien gehen erst in die Auswertung seiner Intervalle ein.

<div class="page"></div>

## Wie genau die klassische Kontrolle ist

| Masse | Halbbreite h | Intervall für R(T*), nach aussen gerundet | Maximaler relativer Endpunktfehler, aufgerundet |
|---|---|---|---|
| 1/4 | 1/64 | [9,4087; 9,7584] | 1,874 % |
| 4 | 1/64 | [8,0965; 8,4230] | 2,037 % |
| 1/4 | 1/128 | [9,4378; 9,7293] | 1,570 % |
| 4 | 1/128 | [8,1257; 8,3939] | 1,684 % |

Die Rechnung schliesst Quadrat- und Kubikwurzeln rational ein. Zur unabhängigen Kontrolle der Zeitmittel gilt auf jeder Station R³ = a³(1−kx)² mit k² = 125 m(a)/(2a³). Für eine Schale [a,b] überschreitet ihr gemitteltes reduziertes Volumen V/(4π) den Wert bei T* um exakt 125 · [m(b)−m(a)] h²/18. Der Korrekturterm verschwindet in der äusseren Vakuumschale. Die Kombination (4V̄(h/2)−V̄(h))/3 liefert im idealen Modell den Mittelpunktwert. Die Tabelle benutzt beide Fenster einzeln und enthält die Zuschläge für die Randbewegung und beide Instrumentkanäle. Die Prozentwerte sind deterministische Schranken für diese Kontrollen.

## Was die 19 Ereignisse im Zeitblock hergeben

Der geprüfte N19-Viertelzweig hat 17 positive und zwei leere Ereignisse mit den Kennungen 15 und 17. Ein leeres Ereignis ist hier ein Punkt mit Staubgewicht null. Seine physische Zugehörigkeit zum Aussenraum müsste eigens gemessen werden. Wir testen zunächst die schwächere Möglichkeit, ein solches Ereignis und ein unvergleichbares positives Ereignis zu finden. Für einen beidseitig begrenzten lokalen Messbereich verlangen wir zusätzlich ein gemeinsames positives Ereignis in ihrer strikten Vergangenheit und eines in ihrer strikten Zukunft. Dieses verabredete Messverfahren lässt sich auch ohne räumliches Dreiecksnetz prüfen.

**Vollständige Aufzählung.** Auf der ganzen Ordnung gibt es 19 solche gemischten Paare und 143 verschiedene Tupel mit beiden Ankern. Die zweite Aufzählung über die offenen kausalen Intervalle findet dieselben Tupel. Alle 171 einzelnen Vertauschungen der Ereignisnamen ergeben die entsprechend umbenannten Kandidaten. Die Bedingung selbst ist für jede Umbenennung invariant, weil sie nur Ordnung und Gewichtszeichen verwendet. Ein offener Ordnungsbereich enthält eine endliche Ereigniszahl. Für seine Umrechnung in ein physisches Eigen-Viervolumen einer spezifizierten Schale braucht es eine Volumeneichung und die geometrische Zuordnung des Bereichs. Eine räumliche Abstandsauslese aus Ordnung und Volumen erfordert eigene Skalenannahmen. [Eichhorn, Surya und Versteegen, *Induced Spatial Geometry from Causal Structure*](https://arxiv.org/abs/1809.06192)

<div class="page"></div>

## Zeitliche Reichweite der N19-Ablesung

Die Kosten einer Gruppe sind der grösste Abstand ihrer Ereignisse von der Modellzeit x=1/2. Für jede Lösung finden wir das Minimum über alle Gruppen. Auf dem positiven Zweig mit schwachem Gerät wurden alle drei Quellen 0, ±10⁻⁶, sieben geschlossene Driftzellen zwischen −10⁻⁶ und +10⁻⁶ sowie die drei unabhängig begrenzten normierten Nachimpulse bis 112 geprüft. Die Uhr xᵢ = (Yᵢ−Y₃)/(Y₇−Y₃) gehört zur jeweiligen Lösung. Ihre physische Zuordnung zur P3-Staubuhr ist offen. Die erste mögliche Halbbreite liegt überall zwischen 0,66544465213129 und 0,66544465213130 für das gemischte Paar und zwischen 0,80434782608695 und 0,80434782608696 für das vollständige Ankerquartett.

| Modellfenster um x=1/2 | Sicher enthaltene positive Ereignisse | Nullereignisse |
|---|---|---|
| ±1/256 und ±1/64 | 16, 18 | 0 |
| ±1/16 | 12, 16, 18 | 0 |
| ±1/8 und ±1/4 | 11, 12, 13, 16, 18 | 0 |
| ±1/2 | 3, 4, 5, 6, 7, 11, 12, 13, 14, 16, 18 | 0 |

Über alle zertifizierten Zellen stimmen die sicher enthaltenen und die durch die Intervallrechnung noch möglichen Kandidaten überein. Im klassischen Arbeitsfenster ±1/64 sind nur 16 und 18 vorhanden. Der Pfeil 16≺18 ist ein Link. Sein offenes Intervall hat Kardinalität null. Diese Null ist eine Zählung im endlichen Modell. Der Eigeninhalt einer Innenschale oder Aussenschale bleibt unbestimmt.

## Was bei zwei zusätzlich eingesetzten Ereignissen geschieht

Im kleinen Fenster sind für das beanspruchte Quartett mindestens ein weiteres positives und ein leeres Ereignis erforderlich, sofern die vorhandene Fensterbelegung erhalten bleibt. In der reinen Ordnung genügen zwei neue, unvergleichbare Ereignisse zwischen 16 und 18. Beide können zwischen ihren Ankeruhren datiert werden. Wir prüfen jetzt die freie Dichtegleichung des neuen positiven Punkts n, wenn er keine eigene Quelle oder Gerätekopplung erhält. Dies ist die explorative Ergänzung nach der ersten Aufzählung. [Staubwirkung und lokale Dichtevariation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/e2f74ef37fc572efeff2f2f7cb99b4b4cbeee852/research/rax_cqg/dust_collapse/schalenvolumen_und_seitenfluss_v0_1)

**Genau zwei relevante Vergangenheiten.** Das alte Vergangenheitsideal von n enthält die Vergangenheit von 16 samt 16 und liegt in der strikten Vergangenheit von 18. Zulässig sind P₀ = {0,1,2,15,16} und P₁ = P₀ ∪ {17}. Beide lassen sich unter Erhalt der alten Ordnung realisieren. Das zweite neue Ereignis bleibt mit n unvergleichbar. Zusätzliche Zukunftsrelationen des neuen Paars ändern die eingehende Dichtegleichung von n bei festem Ideal nicht.

<div class="page"></div>

## Die Dichtegleichung der beiden Anbindungen

In der Normierung der Projektwirkung muss G(y) = 19 + Σ cᵢ(y−Yᵢ)² verschwinden. Die Koeffizienten cᵢ ergeben sich aus der Anzahl der Ereignisse im offenen Intervall zwischen i und n. In der Reihenfolge 0,1,2,15,16 sind es 0,−8,16,−9,1. Für P₁ kommt der Koeffizient +1 bei 17 hinzu.

- **P₀.** Lässt man die neue Uhr zwischen den beiden Ankeruhren frei variieren, ergibt die direkte Einschliessung −20,955 < G(y) < −20,738. Sie schliesst die nötige Null auf allen 21 Zellen aus.
- **P₁.** Hier stimmen die Eingangskoeffizienten mit denen des bisherigen Empfängers 18 überein. Direkte Intervallauswertung liefert ein Intervall über null. Die stationäre Empfängergleichung des alten Gerätezweigs liefert zusätzlich G(Y₁₈) = κ[(Y₁₈−Y₁₆)²+(Y₁₈−Y₁₇)²−Σvⱼ²/w₁₈²] > 2,0853·10⁻¹⁰. Dabei ist κ = 10⁻¹¹ und vⱼ sind die drei in Geräteeinheiten skalierten Nachimpulse. Im ganzen Ankerintervall gilt G′(y) < −3,414. Links vom Empfänger ist der Wert daher noch grösser. Auch diese Anbindung scheitert an der notwendigen Gleichung.

**Geltungsbereich.** Die zweite Schranke verwendet die Gleichungen der vorhandenen N19-Lösung. Der Nachweis schliesst die Einfügung mit Übernahme ihrer Felder und mit genau diesen Ankern aus. Für eine neu stationarisierte 21-Ereignis-Historie ändern sich die Intervallkoeffizienten und die alten Geräte- und Randgleichungen. Über deren Lösungen trifft diese Rechnung keine Entscheidung. Sie liefert auch keine allgemeine Schranke für nichtlokale Flächenoperatoren.

**Folgerung für P3.** Für keine der acht Zielzellen bei zwei Massen und vier Dichten liegt nun eine physisch geeichte Flächenmessung vor. Alle 60 P3-Einträge stehen auf NOT_RUN. Die nächste konkrete Theoriefrage ist, ob beim erneuten gemeinsamen Lösen der alten und neuen Felder unter einer vorab festgehaltenen Randpräparation ein gerichteter Zeitblock mit materieller Kante und äusserem Nullkontakt entsteht. Für den Radius sind danach eigenständige Volumen-, Dicken- und Masseneichungen sowie ein Fehlerbudget erforderlich.

### Nachrechnen

Das Archiv entpacken und im entpackten Ordner mit Python 3.11 oder neuer `python3 -B pruefen.py` ausführen. Es benötigt die Standardbibliothek. Der Prüfer validiert alle Dateihashes, liest die Originalmodelle und das P3-Register, wiederholt die Intervallrechnungen und vergleicht die maschinenlesbaren Ergebnisse bytegenau. Prüfplan und nachträgliche Ergänzungen sind jeweils separat gekennzeichnet. Die genauen rationalen Grenzen stehen in Ergebnisse.json.
