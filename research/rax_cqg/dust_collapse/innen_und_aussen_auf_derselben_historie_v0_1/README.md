# Innen und aussen auf derselben diskreten Staubhistorie

**CST-DUST · Räumlicher Präparations- und Auslesetest · 25. November 2026**

Die endliche Projektwirkung besitzt auf einem explizit räumlich aufgelösten, offenen Kontrollträger eine zeitabhängige positive Lösung. Dieselbe Historie umfasst den stärker besetzten Innenbereich, den Übergang und den schwächer besetzten Aussenbereich. Eine Auslese aus Radarzeiten und lokalen Wirkungsantworten erkennt auf fünf gemeinsamen Schnitten aussen rund 0,655 % der inneren Dichte. Die separat ausgelesene Summe der Strombeträge fällt im selben Verhältnis. An einer vorgeschriebenen scharfen Grenze zu exakt leerem Raum scheitert dagegen die freie Uhrgleichung schon an einer einzigen Aussenstation.

| Gebiet zwischen den beiden Endstationen | Aussen-/Innenmittel der Dichte | Aussen-/Innenmittel der Strombeträge | Entscheidung zum vorab festgelegten 1-%-Kriterium |
|---|---:|---:|---|
| 96 Stationsabstände | 85,5215 % | 85,5215 % | überschritten |
| 3 072 Stationsabstände | 0,65496 % | 0,65496 % | auf allen fünf Schnitten unterschritten |

Der Vergleich verwendet ein festes Zeit-Raum-Gitter mit einer räumlichen Dimension, örtlich adressierbaren Uhren und zwei offenen räumlichen Enden. Seine Ordnung und die Form der Randpräparation sind Modellentscheidungen. Er liefert eine Messkontrolle für die Staubwirkung und ihren Strom. Vierdimensionale Geometriedynamik, Staub-Ruhemasse und Arealradius der materiellen Oberfläche sind offen. Die 60 physischen P3-Einträge stehen auf NOT_RUN.

## Gemeinsamer Träger und unabhängige räumliche Markierung

Ein Ereignis hat den Bauindex (t,j). Die Stationen liegen bei 0 ≤ j ≤ L und die Ticks bei 0 ≤ t ≤ T. Vergleichbarkeit bedeutet positive Zeitdifferenz und Δt ≥ 12|Δj|. Signale können die später geprüfte Grenze in beiden Richtungen überqueren. Das Intervall wird an seinen räumlichen Enden weder periodisch geschlossen noch an einer Materiekante abgeschnitten. Die vier äussersten Stationen an beiden Enden und die ersten und letzten 48 Ticks sind Rand. Alle anderen Dichten und Uhren erfüllen die entsprechenden freien Gleichungen. Auf einem endlichen Gitter werden Werte im Rand als Präparationsdaten gewährt; ihre freie Variation ist hier keine Randbedingung.

Die Referenzstation 0 kann ein Ereignis an Station j am spätesten bei t−12j erreichen und frühestens bei t+12j ein Echo empfangen. Die halbe Echozeitdifferenz ergibt 12j Ticks. Dies liefert auf dieser einseitigen offenen Linie eine eindeutige Ordnung der Stationen, unabhängig vom Materialfeld. Der Versuch gewährt ein ideales Echo in beiden Bereichen, vollständige Exposition und Zugang zu den selektiven Uhrquellen. Die Echozeit ist ein Radar-Abstand; eine zweidimensionale Flächenmessung ist separat erforderlich.

Für Dichte und Strom verwenden wir die ursprüngliche Projektwirkung

    S = −Σᵥ wᵥ [19 + Σᵤ bᵤᵥ (Yᵥ−Yᵤ)²]/38.

Die Koeffizienten b=1,−9,16,−8 werden aus null bis drei strikt zwischenliegenden Ereignissen bestimmt. Ab vier Zwischenereignissen verschwindet b. Sämtliche Beiträge bleiben auch quer zum späteren Materialübergang in der Summe. Hier werden die bisherigen Projektkoeffizienten als endliches Modell auf einem Kontrollträger eingesetzt. Eine dimensionsgerechte 1+1-Kontinuumsdiskretisierung oder eine 4D-CST-Verfeinerung folgt daraus nicht. [Ausgangsstudie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/378) · [Dimensionsabhängigkeit der kausalen Operatoren](https://doi.org/10.1088/0264-9381/30/19/195016)

## Welche Gleichungen der Träger erfüllt

Für eine freie Station sind die folgenden 14 Zukunftsverschiebungen (d,s) wirksam.

| Stationsversatz s | Zeitabstand d | b |
|---|---|---|
| 0 | 1, 2, 3, 4 | 1, −9, 16, −8 |
| +1 und −1 | 12, 13 | 1, 16 |
| +2 und −2 | 24 | −9 |
| +3 und −3 | 36 | 16 |
| +4 und −4 | 48 | −8 |

Auf einem kürzesten Weg über n Stationsabstände liegen n−1 Zwischenereignisse. Bei zusätzlicher Verzögerung u liegen bereits auf den n+1 Stationen des direkten Segments (n+1)(u+1)−2 Ereignisse im offenen Intervall, für n≥1. Bei kleinen u, für die dieser Wert kleiner als vier ist, ist auch kein Umweg über eine weitere Station erreichbar. Für die eigene Station reichen vier vertikale Vorgänger. Diese Zählung gilt an räumlichen Enden für vorhandene Zielstationen. Zwei Implementierungen schlagen die wirksamen Relationen aus der Ordnung nach.

Für Y=h t gilt Σ b d²=−83. Die Dichtegleichung 19+h²Σ b d²=0 setzt h²=19/83. Für die relativen Uhrabstände und alle Materiegleichungen ist das ausreichend. Die Uhr wächst auf jeder Kausalrelation streng; auf den Archivaufnahmen entspricht ein Tick der Uhrzeit h. Bei positiver Dichte erfüllt diese Uhr die Dichtegleichung im ganzen freien Bereich. An einer Dichte null wird wie im Vorgängermodell keine stetige Dichtevariation verlangt. Für die freie Uhr ergibt sich aus Σ b d=391 die rückwärts gerichtete lineare Gleichung

    391 w(t,j) = Σ_(d,s) b d w(t+d,j+s).

Im homogenen Fall und im Vakuum gilt sie identisch. Bei vorgegebener Uhr bestimmen 48 zukünftige Schichten und die räumlichen Randwerte die früheren freien Werte eindeutig per Rückwärtseinsetzen. Das ist eine Randwertrechnung an der endlichen Wirkung.

## Eine scharfe Kante scheitert trotz richtiger Lokalisierung

Als Kontrolle setzen wir w=1/4 für j≤32 und w=0 weiter aussen, auf allen Schichten. Das Instrument grenzt die Kante zwischen 32 und 33 ein. Die Sternsumme der Strombeträge reicht bis Station 36, und an Station 37 verschwindet sie exakt im Modell. An der leeren Station 36 gibt es genau eine wirksame Zukunftskante zu einer besetzten Station, mit Versatz (48,−4) und b=−8. Alle übrigen Ausgänge und sämtliche Eingänge tragen null. Daher ist dort 19(∂S/∂Y)/h=−96. Die Stationaritätsbedingung verlangt null.

Das Vorzeichenargument überlebt beliebige strikt kausal wachsende Uhren und positive Amplituden auf der letzten besetzten Station, solange diese statische Trägerkante und die freie Aussenstation über das vollständige Wechselwirkungszeitfenster erhalten bleiben. Es schliesst eine solche kompakte Präparation auf diesem Träger aus. Bewegte, zeitlich begrenzte oder anders gekoppelte Ränder bedürfen eigener Untersuchungen.

## Zeitabhängige positive Vergleichslösung

Im zweiten Versuch werden Randdaten der Form w(t,j)=qᵗrʲ/2 gewählt. Das frei variierte Innere muss dieselben Gleichungen erfüllen. Einsetzen in die Rekursion verlangt

    P(q;r) = Σ_(d,s) b d [qᵈ rˢ − 1] = 0.

Für die acht ursprünglich festgelegten Werte zwischen 1/2 und 63/64 ergibt die Gleichung keine Wurzel im vereinbarten Zeitratenintervall [1/2,2]. Der Nullbefund betrifft diese acht räumlichen Raten und den separierbaren Ansatz. In der vor der Zusatzrechnung festgelegten Folge feinerer Raten liegt der erste Treffer bei r=511/512. Seine beiden zulässigen Zeitraten sind rund 0,999728385338 und 0,999899084914. Die Auswahlregel für die geringere Zeitänderung wählt die zweite Rate. Für das ganze endliche Gebiet gilt 0<w≤1/2. Der Zeitfaktor ist aus der freien Gleichung bestimmt. Das räumliche Verhältnis und die mit diesem Modus kompatiblen Randwerte sind gewählt.

Eine Prüfung durch Bernstein-Koeffizienten mit Vorzeichenwechselzählung und eine unabhängige Sturm-Kette zählen alle Wurzeln im deklarierten Intervall. Die benutzte algebraische Wurzel liegt in einem rationalen Intervall der Breite unter 10⁻³². Alle Potenzen werden mit nach aussen gerundeten ganzzahligen Intervallen berechnet. Als zweite Entwicklungsrechnung bestimmt der Prüfer 3 168 freie Dichten auf 33 Stationen über 96 Zeitschritte aus Zukunfts- und Seitenwerten ohne Profilparameter im Rekursionsschritt. Jede Einschliessung überlappt die der algebraischen Lösung; die breiteste liegt unter 5 × 10⁻²⁴. Die exakte Übereinstimmung folgt für exakte Randdaten durch Einsetzen und die Eindeutigkeit der Rekursion.

## Was die Instrumente empfangen

Eine Dichteablesung verwendet vier Stellungen zweier aufeinanderfolgender Uhren derselben Station. Die Zeitverschiebung in jedem Arm beträgt ±1/8 Tick. Die Uhren bleiben kausal geordnet. Für die gemischte zweite Antwort in Y-Einheiten gilt 19 Hᵤᵥ = bᵤᵥ wᵥ. Auf der direkten vertikalen Kante ist b=1. In der lokalen Messung wird die Änderung der ganzen Wirkung gegenüber der unverschobenen Geschichte erfasst. Die unveränderten Terme kürzen sich. Der Generator summiert alle von den Pulsen betroffenen Kantenpolynome. Zwei Stellen verschiedener Stationen lassen sich ebenso abfragen. Zusammen mit ihrem positiven Uhrabstand liefert die gemischte Antwort den jeweiligen vorzeichenbehafteten Strom in Projektkonvention.

Die zweite Auslese kontrolliert alle 14 eingehenden und 14 ausgehenden Kanten an jeder ausgewählten freien Station. Sie summiert die Beträge einzeln; Gegenströme können sich in dieser Anzeige nicht kompensieren. Für das gewählte Profil ist die so gemessene Aktivität ein positiver konstanter Faktor mal w(t,j), denn alle lokalen Dichteverhältnisse lauten qᵈrˢ. Dass die räumlichen Verhältnisse beider Observablen übereinstimmen, ist eine Vorhersage derselben Profilfamilie. Das sind zwei unterschiedliche Messverfahren innerhalb dieser Lösung und kein zweiter physikalischer Datensatz.

Die Rohdatei enthält 16 126 Dichteaufnahmen mit jeweils vier Armwerten und Radarzeitpaar sowie 2 968 Vierarmaufnahmen für die Kanten. Die Daten sind deterministische Modellantworten. Auf den vollständigen Trägern wird die algebraische Lösung implizit verwendet; nur die Messaufnahmen und die unabhängige Rekursionsprobe werden materialisiert. Beim grössten Träger sind 3 073 × 86 017 = 264 330 241 Ereignispositionen mathematisch beschrieben. Es wurde keine Punktwolke dieser Grösse erzeugt.

Im Rohformat werden die Wirkungsänderungen mit 10 624 multipliziert und in Einheiten von 10⁻¹⁰ gerundet. Je Wert wird eine ganze letzte Einheit Fehler zugelassen. Das entspricht höchstens 1/(10 624 · 10¹⁰) in der normierten Wirkung und höchstens 5·10⁻¹¹ für die einzelne rekonstruierte Dichte. Dies ist eine angenommene synthetische Messauflösung. Im schlechtesten der fünf grossen Schnitte würde der gemittelte Dichtevergleich zusätzlich einen absoluten Fehler von weniger als 1,12·10⁻⁵ in beiden Bereichen tolerieren. Die genaue Position des Schwellenübertritts ist empfindlicher. Reale Instrumentfehler und Kohärenz nach Integration über Feinhistorien stehen offen.

## Reichweite und Messergebnisse

Innen- und Aussenbereich werden vor der Messung in Radar-Abständen festgelegt; jeder umfasst fünf Stationen. Der Radius oder eine wahre Grenze werden nicht an die Auslese übergeben. Auf dem Ausgangsgitter liegen die Stationen innen bei 4–8 und aussen bei 84–88. Für die Verlängerungen gelten die im Zusatzplan festgelegten proportionalen Positionen. Auf dem grössten geprüften Gitter sind dies 190–194 und 2 762–2 766. Der Quotient beträgt daher r²⁵⁷². Beim Verdoppeln der räumlichen Reichweite beginnt er auf dem Ausgangsgitter bei 85,52 %, und bei 1 536 Abständen liegt er noch bei 8,09 %. Bei 3 072 Abständen liegt er erstmals im Verdopplungsraster unter 1 %. Die absolute physikalische Längenskala ist offen.

| Gemeinsamer Tick, L=3 072 | Inneres Dichtemittel, gerundet | Äusseres Dichtemittel, gerundet | Aussen/innen |
|---:|---:|---:|---:|
| 38 400 | 0,00712714 | 0,0000466800 | 0,65496 % |
| 42 240 | 0,00483740 | 0,0000316830 | 0,65496 % |
| 46 080 | 0,00328328 | 0,0000215042 | 0,65496 % |

Die Auslese prüft an jedem der fünf Schnitte alle erfassten freien Stationen. Sie findet die Grenze für das relative 1-%-Kriterium jeweils zwischen Station 2 547 und 2 548. Diese Lage ist innerhalb des Profils zeitlich konstant, während die Dichte sinkt. Jeder Punkt bleibt streng positiv. Es entsteht eine rückverfolgbare Schwellenfläche auf einer räumlichen Linie; daraus folgt kein exakt leeres Gebiet und keine mitbewegte Stauboberfläche des P3-Staubballs.

Das homogene Profil verfehlt das relative Aussenkriterium, die leere Kontrollgeschichte hat keinen positiven Innenstandard, und die räumlich gespiegelte Geschichte weist nach aussen ansteigende Dichte auf. Fehlende Echos, doppelte Einträge und unvollständige Kantenabdeckung werden erkannt.

## Reproduktion und physischer Status

Im entpackten Ordner, mit Python ab 3.10 und der Standardbibliothek:

    python -B pruefen.py

Der Prüfer reproduziert die Rohdaten, vergleicht sie nach Dekompression byteweise, liest die gespeicherten Dichte- und Stromsignale separat ein, prüft die ursprüngliche Wirkung auf 18 repräsentativen Kanten- und Nullkopplungsfällen und verifiziert die Ergebnisdatei. Die Prüfpläne dokumentieren auch die nachträglichen Erweiterungen. Es gab keine externe Vorregistrierung.

Ein nächster physikalischer Test ist eine zeitlich veränderliche, räumlich lokalisierte materielle Begrenzung auf einem geometrisch dynamischen Träger, mit unabhängiger Prüfung des Seitenflusses und einer positiven Schnittmasse. Die 1-%-Schwelle aus diesem Funktionsversuch ist eine gewählte Messdefinition. Die 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.
