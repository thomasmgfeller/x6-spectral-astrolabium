# Zwei winkelkalibrierte Materialmarker aus einer Staubhistorie

**Ergebnis.** Auf derselben klassischen Einstein-Staub-Historie kann die Auslese den Winkel zweier komovierender, präparierter Sonden durch frühe Lichtechos kalibrieren. Aus allen 21 Paaren von sieben asymmetrisch platzierten Sonden bestimmt sie sogar das Paar und seine Senderichtung. Der Ausleser erhält weder Winkel noch spätere Radien oder Massen. Auf dem geprüften positiven N15-Zweig scheitert die Einfügung entsprechender positiver Ereignisse schon an einer notwendigen Uhrbedingung, selbst mit einem früheren neuen positiven Vorfahren. Die 60 physischen P3-Einträge bleiben NOT_RUN.

## Was die klassische Präparation gewährt

Die drei Referenzhistorien mit M=1/4, 1 und 4 sind die zuvor geprüften inhomogenen, marginal gebundenen Lemaître-Tolman-Bondi-Staubkugeln mit Vakuumaussenraum. Anfangs ist a der Eigenabstand vom Mittelpunkt und der Arealradius einer Schale. Der bekannte Anfangsradius des Materieträgers beträgt R₀=10. Ein radiales, anfänglich geeichtes Gitter hat 641 Stationen mit aᵢ/R₀=13i/6400. Der Beobachter lokalisiert auf dem Anfangsschnitt und bei T*=5√5/6 unabhängig die letzte positive Station des zusammenhängenden Materialträgers. In allen drei positiven Lösungen liegt sie bei i=492, a=9,99375. Station 493 befindet sich im Vakuum. Die ausgewählten Sonden befinden sich also an derselben **materiell besetzten inneren Begrenzung der Randklammer**. Die analytische Stützgrenze liegt bei a=10, wo die Dichte dieses Profils bereits null ist.

Die Instrumente sind getrennt identifizierbare, idealisierte, komovierende Streuer ohne Rückwirkung. Der Staub trägt ihre Richtungen mit konstanter Winkelkoordinate. Die radiale Zuordnung und der Transport gehören zur klassischen Präparation. Die unbekannte physische Anordnung selbst ist keine Schlussfolgerung aus einer unmarkierten kugelsymmetrischen Lösung.

## Winkel aus einem frühen Echo

Zu Beginn sendet eine Sonde einen Lichtpuls. Eine zweite antwortet beim frühesten Empfang mit höchstens 10⁻⁷ Zeiteinheiten Verzug. Die erste Sonde registriert die früheste Rückkehr auf derselben Uhr. Der gemessene Abstand Dₘ ihrer zwei Zeitstempel hat die Fehlerhülle E=4,1·10⁻⁶: je Stempel ±2·10⁻⁶ sowie Rundung auf ein Raster von 10⁻⁷. Der Sendetermin besitzt relativ zum Anfangsschnitt eine maximale Verschiebung e₀=2,05·10⁻⁶.

Für aᵢ/R₀=σ und eine zugelassene Unsicherheit δ des Anfangsradius berechnen wir

    R_max = σ(10+δ) + 3e₀
    R_min = σ(10−δ) − 3(e₀+Dₘ+E)
    (Dₘ−E−10⁻⁷)/(2 R_max) ≤ θ ≤ (Dₘ+E)/(2 R_min).

Diese deterministischen Ungleichungen lassen auch radiale Abkürzungen zu. Oberhalb R=7 erfüllt jede kausale Bahn in der verwendeten Metrik |dR/dT|≤1+√(2m(a)/R)<3. Der ganze Echozeitraum ist so kurz, dass auch die konservative Untergrenze über 7 bleibt. Während beider Lichtwege beträgt die Winkelgeschwindigkeit höchstens 1/R_min. Umgekehrt kann ein Signal jede Richtung auf dem komovierenden Grosskreisbogen in höchstens R_max θ Zeit erreichen. Zusammen mit dem Rücksendeverzug folgt die untere Winkelgrenze aus dem spätestmöglichen frühesten Echo. Uhr, R₀ und radiale Anfangsteilung ersetzen die direkte Vorgabe des Winkels. Spätere Uhren- und Winkelfehler werden getrennt behandelt.

Die Vorwärtssimulation löst pro Richtung Hin- und Rückweg im vollständigen radial und zeitlich veränderlichen Feld. Sie bestimmt beim Schiessen den Startwinkel des Lichtstrahls, so dass er beim zweiten komovierenden Marker endet. Als Kontrollgrössen werden zwei RK4-Auflösungen mit vier und acht Schritten je Bogen verglichen. Die Bittoleranz und die Garantie über alle Uhrenfehler folgen aus separaten mathematischen Schranken. Sie setzen keine numerische Genauigkeitsgarantie der Schiessmethode voraus.

Für die Vorwärtsschranken wird der volle zulässige Zeitraum t_max aus der konservativen oberen Echolaufzeit festgelegt. Der LTB-Skalenfaktor der Winkelschale ist R/a=(1−3Ts/2)^(2/3), s=√(2m/a³)≤√0,02. Aus dem abnehmenden m/a³ folgt R'≥R/a bei T≥0. Für t_max<0,003 begrenzt 0,145 den Betrag von ∂T(R/a). Für kurze negative Startzeiten gilt R'≥1−0,225 e₀ wegen −a s'≤1,5s. Die räumliche Metrik dominiert damit das Quadrat von c=1−0,145t_max mal der anfänglichen euklidischen Metrik in vollen drei Raumdimensionen. Jeder der beiden Lichtwege benötigt mindestens c mal die anfängliche Sehnenlänge. Daher ist die gesamte früheste Echolaufzeit mindestens 4a c sin(θ/2). Der Prüfer benutzt hierfür die rationale untere Sinusschranke und testet alle ganzzahligen Uhrdifferenzen, die mit diesen Hüllen vereinbar sind. Eine von der physisch erreichbaren Zeit abweichende Tickfolge im erweiterten Bereich kann die Garantie nur konservativer machen.

## Auswahl und spätes Signal

Der Zielwinkel ist θ₀=1/9200. Zulässig sind ±0,5 %. Sechs komovierende Reflektoren wurden zunächst mit Abständen 0,96, 0,985, 1,000, 1,015, 1,04 und 1,09 mal θ₀ relativ zum Sender präpariert. Nur der Vorwärtsrechner kennt diese Abstände. Der Leser akzeptiert einen Reflektor, wenn sein ganzes Winkelintervall innerhalb der Toleranz liegt. Er muss genau einen Treffer finden. Alle möglichen Reihenfolgen der sechs Aufnahmen ergeben dieselbe Auswahl. Zusätzlich wurde die Zertifizierung auf den ganzen kontinuierlichen Bereich [0,9999;1,0001] θ₀ für den Zielreflektor geprüft, während die übrigen Abstände festgehalten werden.

Der volle Echo-Graph ist eine anschliessend festgehaltene Zusatzfrage. Die sieben Punkte liegen darin auf einem gemeinsamen kurzen Grosskreisbogen. Alle 21 Paar-Echos pro Masse werden unabhängig vom vorgesehenen Sender berechnet. Die ursprünglichen sechs Messwerte werden dabei exakt als Teil des Graphen wiedergefunden. Genau eine ungerichtete Kante erfüllt beim präzisen Anfangsstandard die Winkeltoleranz unter allen zugelassenen Zeitfehlern. Null und zwei Treffer erzeugen eigene Diagnosen. Für die Orientierung sendet von den beiden Endpunkten derjenige mit der grösseren Summe gemessener Echolaufzeiten zu den übrigen fünf Punkten. Selbst im ungünstigsten Fehlerquader beträgt der Abstand der beiden Summen mindestens 105 793 Ticks. Alle 5 040 Umbenennungen je Masse lassen den ausgewählten physikalischen Pfeil erhalten. Bei lediglich zwei gleichberechtigten Sonden bleibt die Richtung ohne weitere Information offen.

| Kontrollbedingung | Beobachtung |
|---|---|
| R₀ exakt, beliebige zulässige Stempel- und Rundungsfehler | Eine eindeutige Auswahl je Masse. Das zurückgegebene Winkelintervall liegt über alle Fälle zwischen 0,99587 und 1,00446 mal θ₀. |
| R₀ mit Halbbreite 0,01 | Die drei nominalen Aufnahmen wählen dasselbe Paar. Zulässige gegensinnige Stempelfehler (−2 und +2 Mikro-Projektzeiteinheiten) verhindern bereits die vollständige Zertifizierung. |
| R₀ mit Halbbreite 0,1 | Der Leser kann bei keiner möglichen Aufnahme der sechs Reflektoren einen Zielwinkel zertifizieren. |
| Fehlender Materialrand, fehlender bzw. doppelter Treffer, mehrdeutige Kennung oder streifende Zielgrenze | Der Prüfer weist die Auswahl zurück bzw. meldet Mehrdeutigkeit. |

Für diese Fehlerhülle und die tatsächlich präparierten Kontrollgeometrien beträgt die maximal über alle eingeschlossenen Ziel-Ticks hinreichende Halbbreite des R₀-Standards rund 0,00543370, relativ zu 10 also rund 0,05434 %. Der Prüfer berechnet sie aus beiden Enden des geforderten Winkelbandes. Dies ist ein Instrumentbudget innerhalb der angegebenen Familie.

Beim späteren Einwegsignal werden die ±2·10⁻⁶ des bisherigen Versuchs je Zeitstempel verwendet. Der frühe Empfänger wird wiedererkannt und mit der Staubbewegung bis T* verfolgt. Am besetzten Marker und auf der analytischen Stützgrenze geben die berechneten Laufzeitschranken denselben Status:

| M | Ergebnis aus verfügbaren Winkelschranken, einschliesslich zulässiger Instrumentfehler |
|---|---|
| 1/4 | Verbindung ausgeschlossen |
| 1 | Offen |
| 4 | Verbindung gesichert |

Für M=1 gelingt im leichten Fehlerfall der Nachweis der Erreichbarkeit; im schwierigen Fehlerfall sind die benutzten Hüllen unentscheidend. Wenn der Prüfer nachträglich den tatsächlich präparierten Winkel exakt einsetzt, ist die Verbindung bei M=1 an beiden Uhrecken gesichert. OFFEN beschreibt also die Zertifizierung aus den zugelassenen Daten. Die positive Randstation und die exakte Stützgrenze wurden separat gerechnet. Die Fortsetzung von der inneren Station zur Stützgrenze benutzt die sphärische Symmetrie und die feste Winkelkoordinate.

## Positive Vorläufer im diskreten Modell

Für die früheste der angestrebten positiven neuen Marken z im Messzeitband wird die gesamte mögliche strikte Vergangenheit betrachtet. Neben alten Ereignissen kann sie null oder einen früheren neuen, strikt positiven Punkt u enthalten. Dessen Uhr ist frei und darf auch deutlich vor dem Band liegen. Für einen alten Vergangenheitsidealsatz P_z werden alle alten Vergangenheiten P_u⊆P_z und alten Nachfolger F_u innerhalb P_z zugelassen, die Transitivität erlauben. Dazu kommen u≺z und alle Relationen der alten induzierten Ordnung. Die direkte Ideal-/Filter-Konstruktion und die unabhängige Projektion aller alten Ein-Punkt-Erweiterungen erzeugen dieselben Fälle.

Auf jedem alten freien positiven Vorgänger, auf u und auf z erzwingt die lokale Dichtevariation 19+Σᵢ bᵢⱼ(Yⱼ−Yᵢ)²=0. Die Kragen sind wie in PR 380 festgehalten. Der Bereich für e beträgt 1/6±2⁻²². Alle reellen Wurzelzweige werden in kausaler Reihenfolge auf einem nach aussen gerundeten Raster der Breite 10⁻¹⁴ eingeschlossen. Zwei äquivalente quadratische Gleichungen verwenden als Ursprung null und die dritte Vergangenheitskragenuhr. Beide berücksichtigen bei konstanten Polynomen, linearen Fällen und Grenzberührungen die Möglichkeit von Zweigen. Unentschiedene Ordnungsvergleiche dürfen Zweige bestehen lassen. Nur der Schnitt der Vereinigungen beider äusserer Hüllen wird gewertet. Es blieb kein singulärer Fall ungeklärt.

| Zahl neuer positiver Vorfahren von z | Vergangenheitsordnungen | Fälle mit verbleibenden Uhrwurzelintervallen | Garantierter Mindestabstand zum gesamten Messzeitband in x=T/T_end |
|---|---:|---:|---:|
| 0 | 23 | 9 | >0,04070 |
| 1 | 1 656 | 53 | >0,03210 |

Das Messzeitband enthält beide in PR 381 geprüften Fenster bei achtfachen Zeitfehlern. In der zweiten Zeile enden die letzten darunterliegenden Uhrintervalle spätestens bei x=0,46789030; die ersten darüberliegenden beginnen frühestens bei x=0,54117755 (nach aussen gerundet). Die positive Dichtegleichung ist schon eine notwendige Bedingung. Zusätzliche freie Gleichungen und beliebige neue Zukunftsereignisse können einen ausgeschlossenen Wert im gegebenen Vergangenheitskegel nicht herstellen. Die 53 überlebenden Vergangenheiten sind Kandidaten bei anderen Uhrzeiten, keine zertifizierten Gesamtlösungen.

Der Satz setzt die feste alte Ordnung und den positiven alten Sektor voraus. Er schliesst mehrere frühere neue Vorfahren, leere Vorereignisse, andere Kragen, andere Zeitauslesen und kohärente Summen nicht ein. Ausserhalb des Zielkegels darf die Historie grösser sein. Das Programm prüft auch alle 7! Permutationen der inneren Labels des alten Zweigs bei festen Kragen. Nur Identität und Vertauschung 4↔5 erhalten die alte Ordnung. Die so beschriebene endliche Symmetrie hat für sich keine kalibrierte Winkelbedeutung.

## Warum die Markierungen eine physische Voraussetzung sind

Eine unmarkierte, exakt kugelsymmetrische Staubhistorie bleibt unter jeder räumlichen Rotation gleich. Eine mit Rotationen verträgliche Vorschrift, die aus dieser Historie ein bestimmtes Paar auf der Oberfläche auswählt, müsste dieses Paar unter jeder Rotation unverändert lassen. Schon die Bahn eines einzelnen Oberflächenpunkts unter der Rotationsgruppe ist die ganze Sphäre; keine endliche nichtleere Punktmenge erfüllt diese Bedingung. Auch ein ungeordnetes Paar löst das Problem nicht. Rotationsinvariante Aussagen über alle Paare mit einer gegebenen Trennung sind hingegen möglich.

In der klassischen Prüfung bricht die asymmetrische Verteilung der beobachtbaren Sonden diese Symmetrie. Die Auswahl ist relabel-invariant und der Winkel ist messbar. Die Projektwirkung hat solche Sonden bisher nicht erzeugt. Ein diskreter Weg könnte unterscheidbare materielle Strukturen aus einer ausgedehnten Präparation tragen oder gleich über alle geometrisch geeigneten Paare eine Observable definieren; für beide Wege fehlen die zugelassene physische Messung und die Masseneichung. Der P3-Status bleibt HOLD_NOT_ELIGIBLE.

## Reproduktion und Quellen

Mit Python ab 3.10 und Standardbibliothek im entpackten Verzeichnis ausführen.

    sha256sum -c SHA256SUMS
    python -B pruefen.py

Echoaufnahmen.json enthält die Beobachtungsdaten des ersten Versuchs ohne Massen und wahre Winkel. Netzaufnahmen.json enthält die 21 Paarwerte je Kontrollhistorie und die zugehörigen äusseren Fehlerhüllen. Der Kontrollschlüssel und die zertifizierten Vergangenheiten sind separat beigefügt. Die metrischen Rohzeiten werden numerisch ausgewertet und nur als ganzzahlige Instrumentticks gespeichert. Die Vorwärts- und Messschranken sowie die diskreten Uhrausschlüsse verwenden nach aussen gerundete bzw. exakte Arithmetik. Der Hauptplan wurde vor Beginn lokal fixiert, die genauere Definition der Reflektoren vor der Echoauswertung und der Zusatzplan für die ungeordnete Auswahl nach dem ersten Senderversuch. Die Kontrollen sind synthetisch und explorativ.

[Ausgangspunkt und bisheriger Blindtest](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/381) · [Projektwirkung und klassische Kontrolllösung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/380) · [Klassische LTB-Staubgleichungen](https://doi.org/10.1103/PhysRevD.47.5357)
