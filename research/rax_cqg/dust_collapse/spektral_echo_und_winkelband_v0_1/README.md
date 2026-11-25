# Etappe 2a · Was ein symmetrischer Echoanteil über den Radius verrät

**26. November 2026 · Prüfung der beiden vorgeschlagenen Theoreme und der drei numerischen Hypothesen.** Eine symmetrische Auswahl und Auswertung von Paaren ist möglich. Für die Inversion braucht es zusätzlich ein Ausbreitungsgesetz und eine bekannte Abtastverteilung. Die Kappeneigenwerte eines idealen Kontinuums, die Eigenwerte einer endlichen Adjazenzmatrix und der bedingte Anteil unter früh kalibrierten Paaren liefern verschiedene Zahlen. Der vorgeschlagene universelle Mindestumfang und eine universelle Eichsensitivität sind widerlegt. Für die 60 physischen CST-Prüfpunkte gilt weiterhin NOT_RUN.

## Die vier Datenobjekte

1. Auf der späten Zeitscheibe bezeichnet i denselben komovierenden Marker wie zu Beginn des kurzen Abfragefensters. Ein Bit fragt, ob i am Anfang ein Signal zu j am Ende senden kann. In den sphärischen Kontrollen bei gleichem komovierendem Radius ist die Antwort beim Vertauschen der beiden Richtungen gleich. In einem allgemeinen zeitabhängigen inhomogenen Modell muss das Verfahren festlegen, ob beide Antworten, mindestens eine oder ihr Mittel zählt. Die Matrix hat hier Diagonale null.
2. Der vollständige späte Graph benutzt alle verschiedenen Paare. Die frühe Echoauswahl ist eine zusätzliche Maske. Ihr bedingter Anteil Φ ist die Summe der späten Bits über die ausgewählten Paare, geteilt durch deren Anzahl g. Bei g=0 fehlt die Exposition. Ein offenes Bit ist keine Null.
3. Der unmaskierte Kontinuumsoperator mittelt über die ganze Einheitssphäre mit der normierten Flächenverteilung dΩ/(4π). Dieser Operator setzt einen isotropen Kappenkern voraus, der nur von der Trennung der Richtungen abhängt. Bei gleichverteilter dichter Abtastung und geeignetem Spektralkonvergenznachweis ist die skalierte empirische Matrix K/N die naheliegende Approximation.
4. Eine kinematische Kontrollmetrik kann einen solchen Kontinuumsoperator bestimmen, auch wenn keine entsprechende endliche Markerstichprobe beobachtet wurde. Die Radien 8,5 und 9,9 bezeichnen die zwei synthetischen N15-Vergleichsmetriken. Die drei Einstein-Staub-Kontrollen sind andere Historien.

## Inversion unter präzisierten Voraussetzungen

Sind Auswahl und Ausbreitungsregel von Kennungen unabhängig, bleibt der Quotient bei gemeinsamer Umbenennung erhalten. Die entsprechende Rotationsinvarianz setzt voraus, dass Präparation, Auswahl und Messregel bei gemeinsamer Rotation mittransformieren. Statistische Isotropie einer Verteilung allein legt die Antwort einer einzelnen Realisierung nicht fest. Identische Marker zwischen den Zeitschnitten oder eine operational äquivalente Zuordnung der Paare werden weiterhin gebraucht.

Im idealisierten statischen Modell mit Lichtausbreitung auf der Kugelwand ist die Reichweite α=ΔT/R. Bei Lichtausbreitung im gesamten flachen Raum gilt dagegen 2R sin(θ/2)≤ΔT. Schon diese beiden Modelle unterscheiden sich bei endlichem Winkel. Für unabhängige uniforme Richtungen und perfekte Auswahl im wahren Winkelband [a,b] gilt im statischen Wandmodell für den Populationsanteil

    Φ(R) = 0                           für α≤a
         = (cos a−cos α)/(cos a−cos b) für a<α<b
         = 1                           für α≥b.

Der Quotient zweier beschränkter U-Statistiken konvergiert unter diesen Stichprobenannahmen für positives Bandmass zu diesem Wert. Bei einer anderen bekannten Paarverteilung ist die bedingte Verteilungsfunktion der Winkel einzusetzen. Für strenge Monotonie im Übergang muss sie jedem offenen Teilintervall positive Masse geben. Eine endliche Stichprobe hat nur endlich viele mögliche Anteile k/g. Statistisch isotrope Muster können etwa durch gemeinsame Zufallsrotation einer festen Konfiguration erzeugt werden und dennoch eine völlig andere oder leere Winkelstichprobe liefern.

Bei θ₀=1/9200 und a,b=(1∓0,005)θ₀ reicht der strenge Übergang nur von R=1840/201 bis R=1840/199, rund 9,15423 bis 9,24623. Innerhalb der gesamten Vergleichsspanne [8,5;9,9] ist der Anteil auf den beiden äusseren Bereichen konstant. Aus Φ allein beträgt der kleinste garantierbare relative Punktfehler auf dem unteren Teilintervall 263/7097≈3,706 %, auf dem oberen 1301/38101≈3,415 %. Dies folgt aus (R_max−R_min)/(R_max+R_min). Die beiden *einzelnen* Alternativen 8,5 und 9,9 werden in diesem neuen Instrument dagegen eindeutig getrennt. Der frühere exakte Wert 7/92 gehört zur alten radialen Auslese.

**Gegenbeispiel mit gleichem Radius und verschiedenen Φ.** Man verwende räumlich flache Metriken −dT²+a(T)² d𝐱² und eine komovierende Kugel bei χ=10. Früh haben beide a=1 und identische Echos. Bis T* stimmen sie überein, mit a(T*)=0,93 und glattem Anschluss. Später sei 1/a=(100/93)(1+cH(s)), s=(T−T*)/ΔT, H=10s³−15s⁴+6s⁵. Beide wählen eine kontrahierende Fortsetzung. Für c=0,001 und c=0,05 betragen die konformen Lichtbudgets B=(100/93)ΔT(1+c/2), denn ∫₀¹H=1/2. Die exakte Kausalbedingung ist 20 sin(θ/2)≤B. Das erste Budget ist kleiner als die kürzeste, das zweite grösser als die längste Sehne des ganzen Zielbands. Bei R(T*)=9,3 ergibt sich somit für jede nichtleere Paarauswahl im Band einmal Φ=0 und einmal Φ=1. Diese zweimal stetig differenzierbaren kinematischen Gegenmodelle prüfen die allgemeinen Hypothesen. Eine zusätzliche Beschränkung auf Lösungen der endlichen Staubwirkung erfordert eine eigene Prüfung.

## Spektrum und der Quotient 1,3565

Für den unmaskierten Kontinuums-Kappenkern 1_{x·y≥cos α} ergibt die Funk-Hecke-Formel auf S²

    μ_l = (1/2) ∫_{cos α}¹ P_l(t) dt,     Vielfachheit 2l+1.
    μ₀ = (1−cos α)/2,     μ₁ = sin²α/4,
    μ₀−μ₁ = (1−cos α)²/4.

In der Legendre-Entwicklung des Kerns steht (2l+1)μ_l vor P_l, mit Gleichheit im Integral- bzw. L²-Sinn. Beim Indikatorsprung ist eine punktweise Gleichheit am Rand nicht zugesichert. Bei einer anderen Massnormierung ändern sich auch diese Koeffizienten. Für die zeilennormierte Kontinuumsmittelung ist der Dipolwert μ₁/μ₀=(1+cos α)/2. Der Grad-eins-Eigenwert, die Differenz zum konstanten Modus und ein Graph-Laplacian-Spalt sind auseinanderzuhalten. Die Formeln für die unmaskierte Kappe und ihren Spalt stehen bereits bei Singer. Sie tragen keine generelle Neuheitsbehauptung. [Singer, Kappenoperator und Spalt, Abschnitt 4](https://arxiv.org/pdf/0905.3174) · [Araya Valdivia und De Castro, sphärische Graphen und latente Distanzen](https://ydecastro.github.io/research/paper27.pdf)

Im statischen Wandmodell folgt für die beiden Radien μ₁,A/μ₁,B≈1,35653979074. Der Kleinwinkelausdruck ist (99/85)²≈1,35653979239; der Quotient der beiden *spektralen Lücken* beträgt dagegen rund 1,84020021. Unter der frühen engen Bandmaske ist der späte B-Kern auf dem gesamten Band null, der Quotient seiner Dipole hat einen verschwindenden Nenner.

**Die beiden tatsächlich publizierten kinematischen Kontrollen.** Die radiale Metrik lautet −dt²+dr² und die Winkelmetrik R(t,r)²dΩ². Auf der Wand r=10 ist h(t)=1/R(t,10) genau bekannt. Die sicher erreichbare Winkeldistanz beträgt mindestens ∫h dt. Die vollständige kausale Winkelkappe kann durch einen radialen Umweg grösser werden. Jeder verbindende Pfad hat |ṙ|≤1 und |r−10|≤ΔT/2. Die Identität 1−f=(u²−1)²(81u²+8)/8 für das veröffentlichte Profil mit u=r/10 liefert im betroffenen Kragen |∂r(1/R)|≤L=1/40. Dort gilt auf der Wand h≥1/10. Mit E=∫ṙ²dt und √(1−ṙ²)≤1−ṙ²/2 ist der Zusatzwinkel nach oben begrenzt durch

    L (ΔT³ E/3)^(1/2) − E/20  ≤ L² ΔT³/(6·0,1).

Die erste Ungleichung nutzt ∫|r−10|dt≤(ΔT³E/3)^(1/2), die zweite maximiert über E≥0. Wegen der sphärischen Symmetrie ist jede kleinere Winkeldistanz auf demselben Radialpfad erreichbar. Eine etwaige Nichtannahme des maximalen Winkels ändert den Kontinuumsoperator nicht. Der erste Prüfer kombiniert diese Schranke mit monotonen Riemannsummen über 1024 Intervalle. Die zweite Rechnung verwendet f≤1, einen separaten Umwegbeweis und 2048 Teilintervalle. Nach aussen gerundet ergibt ihre gemeinsame Einschliessung

    1,35654026 < μ₁,A/μ₁,B < 1,35654036.

Dies ist eine modellabhängige optische Rechnung für die vollständige, ideal dicht belegte Sphäre bei festem ΔT. Die Vergleichsmetriken gewähren einen unabhängig bezeichneten materiellen Schnitt, bekannte Raumzeitfunktionen und exakte Uhren. In beiden numerischen Verfahren sind trigonometrische Funktionen, Wurzeln und Zeitintegrale rational eingeschlossen. [N15-Kontrollmetriken und 7/92](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/eb27671709306634e9cd96915dafe8996105daf9/research/rax_cqg/dust_collapse/n15_arealradius_und_schalenauslese_v0_1)

## Endliche Modellmatrizen aus den LTB-Echos

Auf N15 fehlen passende Marker im Sende- und Empfangsfenster. Der Rang der geforderten Matrix ist damit unbestimmt. Allgemein hat ein endlicher einfacher ungerichteter Graph ohne Diagonale Rang null, falls er leer ist. Jede Kante hat einen 2×2-Hauptminor mit Determinante −1 und ergibt daher Rang mindestens zwei. Bei drei oder mehr Richtungen kann die ganze Matrix bei zwei verschiedenen Radien identisch sein. Eine Haar-rotierte Konfiguration mit allen Abständen oberhalb beider Kappen hat z.B. in beiden Fällen die Nullmatrix und ein isotropes Verteilungsgesetz.

Für die sieben komovierenden Sonden aus PR 382 liest das Skript alle archivierten frühen Echo-Hüllen. Für jedes Paar führt es die dortige Winkelkalibrierung und die dortigen späten LTB-Reichweitenschranken auf der letzten besetzten Station erneut aus. Beide Ausbreitungsrichtungen sind spiegelbildlich äquivalent, solange die Uhren gleich behandelt werden. Frühe Maske, spätes Bit und offene Schranken werden separat protokolliert.

| M | Sicher erreichbar | Sicher unerreichbar | Offen | Nur das eine früh kalibrierte Paar B–D |
|---|---:|---:|---:|---|
| 1/4 | 15 | 5 | 1 | NEIN |
| 1 | 17 | 3 | 1 | OFFEN |
| 4 | 21 | 0 | 0 | JA |

Bei M=4 ist die gesamte 7×7-Matrix exakt die Adjazenz von K₇ mit Eigenwerten 6 und −1 (sechsfach). Der maskierte Anteil ist hier ein Einzelbit. Die Programme rechnen die charakteristischen Polynome sämtlicher mit den Hüllen verträglichen Matrixvervollständigungen mit ganzen Zahlen. Eine unabhängige Determinantenberechnung überprüft jedes Polynom an acht Stützstellen. Dies sind modellseitig abgesicherte Aussagen aus den archivierten Uhrzeiten und den Ausbreitungsschranken. Es gab keine neue physische Signalmessung. Die sieben Sonden sind auf einem kleinen Bogen angeordnet und bilden keine unabhängige uniforme Kugelstichprobe. [LTB-Archiv und Quelldaten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/382)

## Sondenzahl und die Bedeutung der 2 %

Für unabhängige, gleichverteilte Richtungen, ideale Winkeleichung und den Winkelbereich θ₀±w mit w=θ₀/200 ist

    p_Band = (cos(θ₀−w)−cos(θ₀+w))/2 = sin(θ₀) sin(w) ≈ 5,907372389·10⁻¹¹.
    E[g] = N(N−1)p_Band/2;   P(g≥1) ≤ E[g].

Bei 48 Richtungen liegt die Trefferwahrscheinlichkeit unter 6,664·10⁻⁸, bei 64 unter 1,191·10⁻⁷. Ein universelles N aus der geforderten Isotropie allein existiert nicht. Ordnet man beliebig viele Sonden in einem Gebiet mit Winkeldurchmesser unter dem unteren Bandrand an und rotiert die Anordnung als Ganzes zufällig, liegen sämtliche Paare ausserhalb des Bandes. Gezielt präparierte Paare wie in PR 382 unterliegen einem anderen Design.

Die Auswertung liefert eine engere Schranke für eine andere, klar definierte Zahl. Sei s_n die Wahrscheinlichkeit einer leeren Auswahl nach n Richtungen und k=n−1. Die Vereinigungsfläche der Winkelringe der k alten Richtungen ist höchstens kp. Die zweigliedrige Bonferroni-Ungleichung liefert die andere Seite. Der unbedingte Erwartungswert einer Schnittfläche zweier Ringe beträgt p², wie durch Bedingen auf einen unabhängigen Testpunkt folgt. Multiplikation mit dem Indikator „bisher leer“ kann diese positive Fläche nur verkleinern. Daher gilt für kp<1

    (1−kp)s_(n−1) ≤ s_n ≤ (1−kp)s_(n−1) + k(k−1)p²/2.

Mit s₁=1 und nach aussen gerundeten Ganzzahlintervallen auf dem Raster 10⁻²⁶ liegt die kleinste Zahl für P(g≥1)≥0,95 zwischen **318 471 und 318 478 einschliesslich**. Vor 318 471 liegt die Leerewahrscheinlichkeit oberhalb von 5 %; ab 318 478 liegt sie darunter. Die Endpunkte stehen im Ergebnis-JSON. Eine Poisson-Näherung und die Unabhängigkeit aller Paarindikatoren werden nicht vorausgesetzt. Schon bei einem einzigen Treffer ist die Genauigkeit von Φ oder des Radius offen. Die Randsondenzahl ist überdies eine andere Grösse als eine 4D-Sprinklingdichte.

Das P3-Cap von 2 % bezieht sich beim 5-%-Radiusvergleich auf den Stichprobenbeitrag zur normierten Radiusunsicherheit. Für den Gesamtvertrag wird die Fehlerwahrscheinlichkeit über 524 Vergleiche kontrolliert. Ein Radius-Stichprobenplan benötigt einen identifizierbaren Bereich, ein Unsicherheitsmodell, den Einfluss des zufälligen Nenners und eine Auswertung in Radiuseinheiten. Die Zahl der möglichen Paare allein begründet kein binomiales Präzisionsintervall. [P3-Prüfvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/eb27671709306634e9cd96915dafe8996105daf9/research/rax_cqg/dust_collapse/correspondence_v0_1/DERIVATION.md) · [Hoeffding, U-Statistiken](https://doi.org/10.1214/aoms/1177730196)

## Eichsensitivität

Eine saubere Sensitivität benötigt einen bestimmten Schätzer. Im statischen flachen Raum gilt für ein bekanntes, unverändertes Paar mit früher Rundlaufzeit τ=4R₀ sin(θ/2) und **gemessener später Schwellenzeit** ΔT_crit=2R sin(θ/2) exakt R=2R₀ ΔT_crit/τ. Bei fixierten Rohzeiten ist die logarithmische Ableitung nach R₀ gleich eins. Ein einzelnes Bit zu einem vorgegebenen ΔT liefert nur eine Ungleichung. Ein Sprung der kalibrierten Paarmenge kann eine Ableitung zusätzlich verhindern.

Als dynamische Gegenprobe genügt ein kugelsymmetrischer metrischer Kragen mit ds²=−dt²+dr²+R(t)²dΩ². Anfänglich sei R konstant und τ=2R₀θ. Später sei R(t)=R*−vt>0 mit bekannter v>0. Die exakte Reichweite ist ∫dt/R(t). Am Schwellenzeitpunkt folgt mit z=vτ/(2R₀)

    R* = vΔT_crit/(1−exp(−z)),      γ = z/(exp(z)−1).

Für z=0,1 liefert die rationale Exponentialabschätzung γ≈0,95083319. Schon dieses zulässige kinematische Beispiel widerlegt den universellen Wert. Bei Wiederholung können unabhängige zentrierte Zeitfehler in geeigneten Mittelwerten abnehmen. Ein gemeinsamer Zeit- oder Längenfehler, die Verwendung derselben Sonden in vielen Paaren und die Selektion nach verrauschten Echos benötigen eine eigene Rechnung. In PR 382 sind verschiedene R₀-Unsicherheiten und Auswahlentscheidungen dokumentiert, aber kein differenzierbarer physischer Radiusschätzer.

## Reproduktion

Die beiden Ausgangsfragen werden als explorativer Methodentest untersucht. Die Stichprobenzahlen sind bedingte Designsätze. Eine erstmals in der gesamten Literatur berichtete Kennzahl wird nicht beansprucht.

    python -B etappe2a_spektral_echo.py
    python -B etappe2a_spektral_echo.py --json
    python -B pruefen.py

Das eigenständige Skript benötigt Python ab 3.10 und die Standardbibliothek. Ohne das Unterverzeichnis basis/ führt es die analytischen Tests aus. Für die endlichen LTB-Matrizen wird der Stand von PR 382 per Hash geprüft. Die Dateien sind im Paket enthalten. Alternativ liest --pr382-zip das unveränderte Originalarchiv der Materialmarkerstudie. Der Gesamtprüfer kontrolliert die Paketprüfsummen, wiederholt die Hauptauswertung und vergleicht sie mit den beiden Gegenrechnungen. Der analytische und der LTB-Teil erzeugen keine neuen CST-Historien. Die native Fläche und der unabhängig massenkalibrierte physische P3-Kandidat bleiben offen.
