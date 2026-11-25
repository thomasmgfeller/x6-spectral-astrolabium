# Nicht-radiale Kausalabfrage an der Stauboberfläche

**CST-DUST · Lokaler Blindtest an 120 neuen 4D-Kontrollen, Transfer auf eine klassische Einstein-Staub-Lösung und Prüfung der N15-Marker.**

Die festgelegte Winkelabfrage entscheidet bei den primären Instrumentfehlern in 89 der 120 neuen Geometrien. In den 31 offenen Fällen liefern zwei erlaubte Kalibrierungen entgegengesetzte Kausalantworten. Alle 60 vorab bestimmten Fälle in den weiter von der Schwelle entfernten Radiusbereichen bestehen. Im gekoppelten klassischen Staubmodell sind die äusseren beiden Massen unterscheidbar. Der veröffentlichte positive N15-Zweig liefert für die Messung keine zwei Ereignisse in den benötigten Uhrfenstern. Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.

## Instrument und Ablauf

Zwei mitbewegte Grenzmarker werden im geodätischen Winkelabstand θ=1/9200 Radiant auf der Einheitssphäre präpariert. Die erste Uhr bezeichnet die gemeinsame Zeit T*, die zweite T*+1/1000, mit c=1. Das Bit gibt an, ob das erste Ereignis das zweite kausal erreichen kann. Bei einer realen Umsetzung bräuchte es eine zuverlässige Präparation, eine gemeinsame Uhr, einen unabhängig kalibrierten Winkel und einen geprüften Nachweis der Erreichbarkeit. Insbesondere bedürfte ein negativer Befund einer Kontrolle von Emission, Verlusten und Detektoreffizienz. Diese Grössen werden in den synthetischen Kontrollen gewährt.

Jeder der beiden Zeitstempel darf unabhängig im gesamten Intervall ±0,000002 liegen. Der Winkelabstand darf um ±0,5 % abweichen. Das primäre Intervall für ΔT/θ reicht damit von rund 9,11761 bis 9,28322. Dies beschreibt die instrumentelle Schwelle. Die genaue Kausalrelation berücksichtigt zusätzlich die veränderliche Geometrie und den kürzesten räumlichen Weg. Die Stressprüfungen multiplizieren beide Fehlergrenzen mit vier und acht.

Der lokale Plan und der ausführbare Leser wurden vor Ziehung des neuen Seeds gehasht. Der Generator bestimmt für jede Krümmung und jeden von vier Radiusbereichen zehn Parametersätze und undurchsichtige Kennungen. Vor der Wertung wurden die Wahrheitstabelle und anschliessend die Antworten des Lesers separat per SHA-256 festgehalten. Erst danach wurden die Urteile mit den Metrikparametern verglichen. Der Leser verarbeitet ausschliesslich die Kennung und zwei binäre Kausalantworten je Fehlerstufe. Bei der Wiederholung läuft er in einem eigenen temporären Verzeichnis, das nur Leser und Aufnahmen enthält. Die Blindwertung ist eine lokale Trennung der Datenzugänge. Es gab keine externe Vorregistrierung, keinen externen Prüfer und keine Beobachtungsdaten.

Die Entscheidung JA bedeutet, dass selbst die ungünstigste erlaubte Kombination aus Uhrzeiten und Winkel eine Verbindung zulässt. NEIN bedeutet, dass selbst die günstigste keine zulässt. Bei OFFEN sind die beiden zertifizierten Antworten verschieden. Die Eckantworten sind systematische Instrumentprüfungen. Eine einzelne idealisierte Ja/Nein-Messung kann diese beiden Prüfungen nicht ersetzen.

## Kinematische Kontrollen

Die Raumzeiten haben die Metrik −dt²+a(t)²[dχ²+sn_K(χ)²dΩ²], mit t=T−T*, a(0)=1 und 1/a(t)=1+h t+q t². Die einfach zusammenhängenden Raumgeometrien haben K=0 oder K=±1/L². Dabei ist sn_K(x) für positive Krümmung sin(√K x)/√K, für negative Krümmung sinh(√|K| x)/√|K| und für K=0 gleich x. Der Marker liegt komovierend bei sn_K(χ)=R* auf dem vom Ursprung aus ersten Ast. Sein anfänglicher Arealradius im Testfenster ist R*. Ein endlicher, präparierter Träger von Testmaterie kennzeichnet die Grenzfläche. Die kinematischen Skalenverläufe sind vorgegeben. Die drei Familien, die gezogenen Parametersätze und Winkelabfragen wurden im früheren Versuch mit den Radien 8,5 und 9,9 nicht verwendet.

Für Emissions- und Empfangszeit t₀,t₁ ist die verfügbare konforme Lichtlaufstrecke B das Integral von 1/a. In konformer Zeit begrenzt das Linienelement die zurücklegbare räumliche Weglänge durch B. Die kürzeste räumliche Geodäte liefert die Gegenrichtung des Kriteriums. Für die beiden Marker ergibt das Kosinusgesetz der Raumform

    sn_K(D/2) = R* sin(θ/2).

D ist die kürzeste räumliche Entfernung. Die Gleichung folgt auch aus den Skalarprodukten zweier Einbettungsvektoren auf der Drei-Sphäre bzw. dem Hyperboloid. Beide Seiten werden auf dem steigenden Hauptast verglichen, im hier betrachteten Winkel- und Zeitbereich deutlich vor jedem Umkehrpunkt. Eine Kausalverbindung existiert genau dann, wenn B≥D. Auch räumliche Abkürzungen im Inneren sind damit berücksichtigt.

Späteres Senden und früherer Empfang verringern B, eine Winkelvergrösserung vergrössert D. Darum reichen die zwei gegensätzlichen Ecken des Fehlerquaders, selbst bei beliebigen Korrelationen innerhalb der zugelassenen Grenzen. Zwei Implementierungen prüfen jede Ecke mit rationalen Einschliessungen. Die erste vergleicht die beiden sn-Funktionen mit Taylorrest und integriert die inverse Skala als Polynom. Die zweite begrenzt die inverse sn-Funktion über ihr Ableitungsintegral und berechnet B unabhängig mit der für dieses Polynom exakten Simpson-Regel. Alle 960 ausgewerteten Eckantworten stimmen überein, einschliesslich der doppelten nominalen Ecken bei Fehlerfaktor null.

| Instrumentfehler | JA | NEIN | OFFEN | Eindeutig |
|---|---:|---:|---:|---:|
| Ideale Uhren und Winkel | 60 | 60 | 0 | 120 |
| Primärgrenzen | 47 | 42 | 31 | 89 |
| Vierfache Grenzen | 29 | 30 | 61 | 59 |
| Achtfache Grenzen | 17 | 19 | 84 | 36 |

| Radiusbereich bei T* | Geometrien | JA bei Primärgrenzen | NEIN | OFFEN |
|---|---:|---:|---:|---:|
| 7,8 bis 8,9 | 30 | 30 | 0 | 0 |
| 9,05 bis 9,19 | 30 | 17 | 0 | 13 |
| 9,21 bis 9,35 | 30 | 0 | 12 | 18 |
| 9,5 bis 10,8 | 30 | 0 | 30 | 0 |

Unter allen 89 robusten Primärentscheidungen gab es keine Abweichung von der unabhängigen nominalen Kausalrechnung. Alle offenen Fälle behalten diesen Status bei jeder folgenden Fehlervergrösserung. Die 89/120 sind ein Ergebnis des fest vorgegebenen, geschichteten Designs. Daraus folgt keine Erfolgswahrscheinlichkeit für eine zufällige CST-Historie und keine relative Radiusschätzung mit 1 % Genauigkeit.

## Transfer auf die klassische Einstein-Staub-Lösung

Als gesonderte dynamische Kontrolle verwenden wir die bereits bekannte inhomogene, marginal gebundene Lemaître-Tolman-Bondi-Lösung mit Vakuumaussenraum aus dem Projekt. Ihr eingeschlossener Massenparameter m(a) liegt zwischen null und M. Die komovierende Materialgrenze liegt bei a=10. Die Winkelmarken liegen auf genau dieser bekannten Grenzfläche. Die hier verwendeten Marker haben durch die mathematische Referenz eine ideale Ortszuordnung. Eine endliche Unsicherheit des Materialrandes wäre ein eigener Beitrag zum Messbudget.

Auf der Weltrohrwand ist der Arealradius bei Emission ein oberer Wert für das ganze anschliessende kurze, kollabierende Zeitintervall. Liegt dieser obere Wert unter ΔT/θ, erreicht eine Kurve auf der Wand den zweiten Marker. Der Gegenbeweis für NEIN berücksichtigt auch innere oder äussere Umwege. Aus dem Linienelement und der Staubgleichung folgt entlang jeder kausalen Bahn |dR/dT|≤1+√(2m(a)/R). Für R≥7 und M≤4 ist dies kleiner als 3. Bereits der konservative Wert R_Emission−3ΔT liegt in allen Fällen über 7. Ein erster Austritt aus dem Gebiet wäre also unmöglich. Liegt dieser untere Radius über ΔT/θ, reicht die verfügbare Zeit auch auf einer beliebigen Raumzeitbahn nicht für den vorgegebenen Winkel. Das Ergebnis bleibt monoton in den beiden Zeitgrenzen (Warten auf den komovierenden Weltlinien ist möglich) und im Winkel (eine kürzere Winkelbewegung bei gleichem Radialpfad ist kausal möglich). Alle Eckurteile für die drei Massen sind zertifiziert.

| M | R(T*), gerundet | Ideale Abfrage | Primärgrenzen | Vierfache Grenzen | Achtfache Grenzen |
|---|---:|---|---|---|---|
| 1/4 | 9,57887 | NEIN | NEIN | NEIN | OFFEN |
| 1 | 9,14826 | JA | OFFEN | OFFEN | OFFEN |
| 4 | 8,25482 | JA | JA | JA | JA |

Die bekannte Ausgangslösung verleiht der Fläche, dem Massenstandard und der Uhr hier ihre Bedeutung. Der LTB-Transfer ist eine zusätzliche Prüfung auf einer schon untersuchten Lösung. [Ausgangslösung und Flusskontrolle](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/02605a740289a519b2ec66aa12cd41d237c2f6c6/research/rax_cqg/dust_collapse/schalenvolumen_und_seitenfluss_v0_1)

## Kann die CST-Historie die Marker liefern?

Für den tatsächlichen positiven Typ 1767356 wurden alle 15 publizierten Intervalle der relativen Uhr x=T/T_end verwendet. Selbst bei achtfachen Fehlergrenzen trifft keines das Emissions- oder Empfangsfenster. Der Abstand zum jeweils nächsten archivierten Uhrintervall ist grösser als 0,02506 bzw. 0,02533 in x. Die explizite kontrastierende Realisierung der alten Ereignisse liegt auf einem einzigen radialen Strahl. Ihr Record enthält für die angeforderte Messung kein kalibriertes nicht-radiales Markerpaar. Eine fehlende Exposition liefert kein NEIN-Bit.

Ein bedingter Ausschluss lässt sich auf gestaffelte Marker erweitern. Man behalte die alte 15er-Ordnung als induzierte Teilordnung, die angegebenen Kragen und den positiven alten Innenzweig bei. Alle hinzugefügten Ereignisse seien freie, strikt positiv besetzte Materieereignisse und ihre Uhren lägen innerhalb des kurzen gemeinsamen Zeitbands. Jede nichtleere endliche Ergänzung enthält ein bezüglich der neuen Ereignisse minimales Ereignis v. Alle Vorgänger von v sind alt. Auch die Vergangenheit dieser Vorgänger enthält keine neuen Ereignisse. Ihre Dichtegleichungen sowie die Schichtzahlen in der Dichtegleichung von v sind deshalb identisch mit denen, die man allein aus seinem alten Vergangenheitsideal berechnet. Der unabhängige Zukunftsbereich ist für diese notwendige Gleichung ohne Bedeutung.

Die Wiederholung über sämtliche 23 alten Ideale und alle kausal möglichen alten positiven Uhrzweige ergibt neun mögliche Uhrintervalle für v, ohne offene Zweige. Keines berührt das gemeinsame Band, das beide Fenster selbst bei achtfachen Fehlern umfasst. Der kleinste zertifizierte Abstand beträgt über 0,04070 in x. Damit kann auch eine zeitlich leicht gestaffelte Ergänzung aus zwei oder mehr ausschliesslich positiven neuen Markern in genau diesem Zeitband die Messung nicht bereitstellen. Die Aussage gilt für den publizierten Bereich e=1/6±2⁻²². Frühere neue Vorfahren ausserhalb des Bands, zusätzliche leere Ereignisse vor den Markern, andere Kragen, andere Materiezweige und eine ausgedehnte relationale Messung fallen ausserhalb dieses Satzes.

Die frühere N16/N17-Prüfung betraf eine freie leere Aussenuhr und gegebenenfalls einen positiven Vorläufer. Unter 182 bzw. 11 943 der dort definierten Ordnungen entstand kein stationärer Kandidat an der geprüften mittleren Zielzeit. Ein geometrischer Beobachter, eine geänderte physische Präparation oder eine über längere Zeit entwickelte Ordnung bräuchten eine eigene Herleitung. Der aktuelle CST-Befund lautet MISSING_EXPOSURE. Die physische P3-Zulassung bleibt HOLD_NOT_ELIGIBLE. [Endliche Ausgangsrechnung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/380) · [Alte Uhrintervalle und Geometrie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/02605a740289a519b2ec66aa12cd41d237c2f6c6/research/rax_cqg/dust_collapse/n15_arealradius_und_schalenauslese_v0_1)

## Reproduzieren

Nach dem Entpacken mit Python ab 3.10 und der Standardbibliothek ausführen.

    sha256sum -c SHA256SUMS
    python -B pruefen.py

Pruefplan.md enthält die Kriterien vor der Auswertung. Aufnahmen.json und Blindurteile.json enthalten die verblindeten Eingaben und Antworten, Schluessel.json enthält Geometrien, wahre Radien und Schichtung. Ergebnisse.json enthält die Zahlen nach Öffnung des Schlüssels, die LTB-Eckantworten und die exakten Grenzen für die CST-Uhren. Die Prüfdateien unter basis/ stammen bytegetreu vom Git-Stand 02605a740289a519b2ec66aa12cd41d237c2f6c6. Die Quellenprüfsummen sind separat festgehalten. Die Versuchsparameter sind synthetische Instrumentannahmen, kein physischer Standard für P3.
