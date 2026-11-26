# CST-DUST · Frühe Präparation der Leeruhr und Vorhersage des Senderstroms auf N19

**26. November 2026.** Zwei vollständig stationäre Lösungen haben identische positive Staubdaten vor dem Sender und unterschiedliche Werte der leeren Vorgängeruhr Y₁₅. Selbst wenn man Y₁₅ als zusätzliche Präparation vorgibt, bestimmen auch der ungepulste Senderstrom und alle vier Anfangsimpulse die spätere Stromänderung noch nicht exakt. Zwei vollständige Gegenbeispiele liefern für dieselbe lokale Quelle um rund 1,39·10⁻¹³ verschiedene Änderungen.

Für den geprüften nominalen Vertrag lässt sich der verbleibende Spielraum quantitativ begrenzen. Die ungepulste Empfängeruhr ist als eine zusätzliche Zahl zur Berechnung hinreichend. Ist nur ihr registriertes Zeitfenster bekannt, liefert die Fenstermitte für beide Quellen eine Vorhersage mit weniger als 1,168·10⁻¹² absolutem Fehler. Dies entspricht weniger als 0,0012 % der jeweiligen Stromänderung. Die Schranke setzt unter anderem die bekannten Randimpulse G₀,G₁ und den kalibrierten Nullstrom voraus. Ihre physische Zugänglichkeit vor dem Senden bleibt offen.

## Welche Uhr lässt sich vorbereiten?

Der strikte Vorlauf von Sender z=16 umfasst die drei positiven Kragenereignisse 0,1,2 und die leere Uhr u=15. Für die feste Anfangskalibrierung mit den drei Uhrwerten −5,−4,−3 gilt auf dem positiven Senderzweig exakt

    s = Y₁₆ = (u²−6−J_w)/(2(u+3)),   u = Y₁₅.

Wir halten bei Nullquelle sämtliche Kragenuhren und alle Anfangsgewichte fest. Von den Randgewichten wird allein w₇ verändert. Die elf inneren Uhren und neun positiven inneren Gewichte relaxieren nach der vollständigen ursprünglichen Wirkung. Die vorab vorgesehenen Änderungen ±10⁻⁸ liefern stationäre Lösungen, deren Sender das enge registrierte Fenster verfehlt. Für den anschliessenden, um den Faktor zehn kleineren Versuch erfüllen beide Lösungen wieder beide Fenster. Die positiven Vorlaufdaten stimmen exakt überein. Der Abstand der Werte von Y₁₅ beträgt 2,143963674·10⁻⁶. Die Daten belegen die Mehrdeutigkeit bei verschiedenen zukünftigen Randpräparationen.

| Änderung w₇ | Y₁₅, gerundet | Y₁₆, gerundet | Beide Materialfenster |
|---:|---:|---:|:---:|
| −10⁻⁸ | −2,467548552 | 0,083383994 | nein |
| +10⁻⁸ | −2,467527112 | 0,083281283 | nein |
| −10⁻⁹ | −2,467538905 | 0,083337777 | ja |
| +10⁻⁹ | −2,467536761 | 0,083327506 | ja |

**Ein expliziter Präparationsvertrag.** Als externe Vorgabe dient die bereits registrierte nominelle Fenstermitte x=1/2 bei abgeschaltetem Sender. Mit e=1/6 und dem Referenzendpunkt Y₇=2 entspricht sie s=1/12. Die Senderdichtegleichung hat dann die beiden Wurzeln u=(1±√937)/12. Nur die negative Wurzel liegt kausal vor s. Mit diesem u≈−2,4675379775 existiert ein voll stationärer Nullzustand im Fenster. Dazu reicht eine Änderung des einen Zukunftsgewichts w₇ um rund −1,34641·10⁻¹⁰. Auch die Quellen J_w=±10⁻⁶ lassen sich mit demselben u bei freiem Zukunftskragen fortsetzen. Die Senderuhr ändert sich dann um ∓9,3903411·10⁻⁷. Hier ist die nominale Zeitkalibrierung eine Eingabe, und der passende Zukunftsrand wird berechnet. Eine von den drei frühen Staubuhren allein erzeugte Auswahlregel ist damit weiterhin offen. Die rein lokale Vergleichsregel u=Y₂+(Y₂−Y₁)/2 liefert u=−5/2 und s=1/4, ausserhalb des Senderfensters.

## Gleiche Präparation und verschiedene Stromantworten

Wir vergleichen jeweils zwei Nullzustände und ihre Fortsetzungen bei gleicher reiner Dichtequelle J_w und J_Y=0. Es gilt die native Wirkung mit passivem Empfänger r=18. Innerhalb jedes Pulsvergleichs bleiben alle Felder ausser z und seiner kausalen Zukunft genau wie in seinem Nullzustand. Zwischen den beiden Nullzuständen dürfen Daten ausserhalb des gemeinsamen Sendervorlaufs verschieden sein. In beiden Familien stimmen die vier Anfangsuhren und -gewichte, der ganze Vorlauf einschliesslich Y₁₅, die Senderuhr und das Sendergewicht sowie der ungepulste Strom K₀=w_z(s−u) exakt überein. Die Zeitfenster und die zur Normierung verwendete Uhr Y₇ bleiben gleich.

| Familie | Weitere Gleichheiten im Nullzustand | Differenz der Stromänderungen bei J_w=+10⁻⁶ | Bei J_w=−10⁻⁶ |
|---|---|---:|---:|
| Alle inneren Uhren identisch | G₀, G₃ und Summe aller vier Gᵢ | −5,36738·10⁻¹⁵ | +5,36249·10⁻¹⁵ |
| Vier einzelne Anfangsimpulse identisch | G₀, G₁, G₂ und G₃; ausserhalb des Zukunftskragens bleiben alle Uhren bis auf 17 und 18 identisch | −1,3890023·10⁻¹³ | +1,3890019·10⁻¹³ |

Die Tabelle zeigt die Antwort des Hintergrunds mit positivem Familienparameter minus die Antwort des Hintergrunds mit negativem Familienparameter. Jeder Stromunterschied wurde auswärts gerundet und von null getrennt. Für die zweite Familie beträgt die Antwort bei positiver Quelle beispielsweise −9,764931616·10⁻⁸ im einen und −9,764945506·10⁻⁸ im anderen Hintergrund. Der Unterschied ist klein und entscheidet die exakte Identifizierbarkeit. Die Zahlen stammen aus Modellrechnungen ohne Messrauschen.

Wir konstruieren die Nullzustände über neun positive innere Gewichte und die acht Gewichts- und ersten Momentgrössen (wⱼ,wⱼYⱼ) am Zukunftskragen. Bei festen inneren Uhren sind die elf freien Uhrgleichungen in diesen 17 Variablen linear. In der ersten Familie wird das Empfängergewicht um ±10⁻⁶ verändert. In der zweiten Familie wird die ungepulste Empfängeruhr zur Konstruktion um ±10⁻⁶ verschoben. Ihre positive Dichtezeile bestimmt den Wert der früheren, mit dem Sender unvergleichbaren Uhr 17. Damit bleiben alle neun Dichtezeilen erfüllt. Die übrigen Gleichungen fixieren das Sendergewicht, die angegebenen Impulse und die Normierungsuhr. Eine zertifizierte reguläre 17×17-Matrix bestimmt in jedem Fall die benötigten Gewichte und Momente. Im darauf folgenden Pulsversuch ist kein Empfängerziel vorgegeben. Alle zwanzig inneren Gleichungen, Uhrordnung, Gewichtsstrata und beide Materialfenster sind für jeden Arm geprüft.

## Warum sich die Antwort auf eine zusätzliche Zahl reduzieren lässt

Schreibe u=Y₁₅, s=Y₁₆, h=Y₁₇ und t=Y₁₈ für den Nullzustand. Nach der Quelle seien d=ΔY₁₆ und q=ΔY₁₈. Die ungetriebenen Uhrzeilen an z und h koppeln mit demselben Vektor an den Zukunftskragen. Subtraktion ihrer Ausgangsgleichungen eliminiert die Zukunftsmomente. Mit m_z=−(u+3) ergibt sich aus der Differenz der Uhrströme und der passiven Empfängerzeile exakt

    ΔK = w_z d [1+(s+d−u)/(s−h)]
         + w_r q (s+d−u)(s+d−h) / [m_z(t+q−h)].

Hier ist d=J_w/(2m_z). Für q wird die im registrierten Empfangsfenster liegende Wurzel der quadratischen Empfängerdichtegleichung verwendet. Die andere Wurzel liegt ausserhalb des ganzen Fensters. In der ersten Familie sind alle Uhren gleich. Daher ändert sich die Antwort allein über den Koeffizienten des Empfängergewichts. Diese Identität und eine getrennte Auswertung der vollständigen Fortsetzung liefern denselben Unterschied.

Bei gegebenem u, gegebenen Anfangskragen, K₀,G₀ und G₁ reicht im nominalen Vertrag eine einzige zusätzliche Zahl **t des ungepulsten Hintergrunds**. Die Rekonstruktion benutzt folgende Beziehungen.

1. Die Senderdichtezeile bestimmt s, anschliessend gilt w_z=K₀/(s−u). Die drei Dichtezeilen an 4,5,6 sind identisch und linear in ihrer jeweiligen Uhr. Daher gilt Y₄=Y₅=Y₆=v mit bekanntem v. Aus G₀ folgt die Summe w₄+w₅+w₆.
2. Die Zeile G₁ bestimmt damit R=w_r(t−Y₁). Sind zusätzlich t und Y₁ bekannt, folgt w_r=R/(t−Y₁). Bei identischen inneren Uhren, K₀, G₀ und G₁ ist also zwingend auch w_r gleich. Das erklärt, warum die zweite Familie die Uhren 17 und 18 gemeinsam variiert.
3. Auf dem kausal geordneten Zweig bestimmt die ungetriebene Empfängerdichtezeile h=t−√[8(t+4)²−16(t+3)²+9(t−u)²−(t−s)²−19]. Damit sind auch der Wurzelzweig für q und alle Grössen der Formel für ΔK bestimmt.

Die Implementierung rekonstruiert die Antwort der zweiten Familie auf diesem Weg und vergleicht sie mit der vollständigen Fortsetzung. Eine frühe Messung von t wird dabei nicht vorausgesetzt.

## Wie gross ist die verbleibende Unsicherheit?

Für die nominalen Werte von u, G₀, G₁, K₀ und die festen Anfangskragendaten setzen wir für t nur das publizierte Empfangsfenster voraus. Alle 128 aneinander anschliessenden Teilintervalle des Fensters werden mit Intervallrechnung vollständig ausgewertet. Als einzelner Schätzwert dient die Vorhersage bei festgehaltener Fenstermitte. Die zulässige Hülle gilt für jeden kompatiblen Nullzustand und seine betrachtete Fortsetzung, auch wenn einzelne Fensterwerte keine vollständige Fortsetzung besitzen.

| Quelle | Hülle für ΔK über das gesamte Empfangsfenster | Maximale absolute Abweichung der Mittelpunktschätzung |
|---:|---:|---:|
| −10⁻⁶ | [+9,7648222; +9,7650558]·10⁻⁸ | <1,168·10⁻¹² |
| +10⁻⁶ | [−9,7650600; −9,7648264]·10⁻⁸ | <1,168·10⁻¹² |

Die relative Schranke von 0,0012 % bezieht sich auf die Stromänderung bei diesen beiden Quellen und dieser Kalibrierung. Sie setzt die Schnitt- und Randdaten sowie das Zeitfenster voraus. Die projektweite 5-%-Prüfung für physische Radien und die Masseneichung sind eigenständige Versuche.

## Reproduktion

Nach dem Entpacken genügen Python ab 3.10 und die Standardbibliothek.

    python3 -B pruefen.py

Der Prüfer reproduziert zuerst das ursprüngliche Sendeschnitt-Paket und dessen eingebettete Vorstudien. Uhrwahl.json enthält die beiden fehlgeschlagenen Fensterproben und die zertifizierten zulässigen Uhrpräparationen. Stromzeugen.json dokumentiert beide Familien, die linearen Invertierbarkeitsschranken, Gewichtsdifferenzen und Pulse, Fensterschranke.json die vollständige Fehlerhülle. Eine zweite Intervall-Elimination berechnet die absoluten Felder der stärkeren Familie unabhängig von der primären Differenzlösung. Vier rationale Kontrollen prüfen die reduzierte Stromformel exakt. Die Gleichheit der festgehaltenen Grössen folgt aus den Gleichungen der Konstruktion. Die Intervalle schliessen die Lösungen ein und sichern die Vorzeichen der Unterschiede ab. Prüfplan und Ergänzungen sind jeweils lokal mit SHA-256 festgehalten, ohne externen Zeitstempel.

Alle **60 physischen P3-Prüfpunkte bleiben auf `NOT_RUN`**. Entscheidend für einen physikalischen Anschluss ist jetzt, welche der hier als Eingabe benutzten Grössen eine realisierte frühe Staubpräparation tatsächlich zugänglich macht.

[Öffentliche N19-Ausgangsstudien, PR 388](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/388)
