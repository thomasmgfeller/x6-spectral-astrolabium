# Bestimmt die N15-Geometrie den Radius der Stauboberfläche?

Typ 1767356 · Stationärer Zweig und volles Uhr- und Dichtepaket · 25. November 2026

Zwei sphärische Vergleichsgeometrien beginnen mit Radius 10. Ihre mitbewegten Oberflächen schrumpfen. Zur gemeinsamen Eigenzeit x = 1/2 betragen die Arealradien 8,5 und 9,9. Beide Geometrien liefern auf allen 15 Ereignissen dieselbe Ordnung und dieselben Uhr- und Dichtewerte. Auch sämtliche radialen Radarzeiten, das räumliche Gesamtvolumen der Kugel und die positive integrierte Materialmenge stimmen im jeweiligen Paar überein. Der kleinste unvermeidliche relative Fehler eines gemeinsamen Punktschätzers beträgt für dieses Paar exakt 7/92, rund 7,61 %. Zwei zusätzliche Volumenablesungen an der Materialgrenze trennen es. Alle Angaben sind Modellrechnungen in den geometrischen Einheiten des Projekts.

## Endliche Daten und Vergleichsfrage

Verwendet werden der stationäre N15-Typ mit Zukunftsdichte 1/64, der Randversatz e = 1/6 ± 2⁻²², die sieben inneren Uhren mit der vollen Halbbreite (4−e)/64 und die inneren Dichten mit ±1 % relativer Halbbreite. Die vier vergangenen Dichten betragen 1/8. Der mitgelieferte Originalcode rekonstruiert die stationäre Mitte mit nach aussen gerundeter Intervallarithmetik. Der vorherige Befund zum Vorzeichen des endlichen Wirkungsstroms steht unabhängig von der folgenden Konstruktion.

Für den Identifizierbarkeitstest gewähren wir beiden Vergleichsgeometrien dieselbe perfekte Eichung T = T_end (Y−Y₃)/(4−e), T_end = 5√5/3, und dieselbe bekannte Materialgrenze. Beides ist eine Zusatzannahme des Tests. Der P3-Vertrag verlangt diese Grössen auf der physischen Präparation. Das vereinbarte R₀ = 10 geht in die Herstellung der Kontrollen ein. Die spätere Schalenablesung erhält keinen Radius.

Alle 15 Ereignisse liegen als explizite Realisierung auf demselben auswärts gerichteten Strahl. Für die festen Radialkoordinaten in den Einheiten c = 1 gilt rᵢ = 10 + (243/250)(aᵢ−1). Die Werte a₀ bis a₁₄ lauten

    0,54  0,53  0,52  0,55  0,25  0,47  1  0,59  0,60  0,61  0,62  0  0,069  0,35  0,58

Ereignis 6 sitzt auf dem fest zugeordneten äussersten Materiallabel. Die kleinste Koordinate beträgt 9,028. Weiter innen liegen keine Ereignisse dieser Realisierung. Für jede der 105 Paarungen gilt entweder Tⱼ−Tᵢ > |rⱼ−rᵢ| in der archivierten Richtung oder |Tⱼ−Tᵢ| < |rⱼ−rᵢ|. Die Intervallrechnung zertifiziert 99 zeitartige und sechs raumartige Paare auf der ganzen Box. Die kleinste garantierte Distanz zur Lichtschranke ist grösser als 0,00457 in der gemeinsamen Längeneinheit. Ein zweiter Durchgang rekonstruiert die Ordnung aus T+r und T−r. Da eine nicht radiale Bewegung die räumliche Weglänge vergrössert, gilt die Klassifikation auch für beliebige kausale Kurven in den vierdimensionalen Kontrollmetriken.

## Zwei sphärische Geometrien zur selben Uhr

Mit u = r/10 und x = T/T_end verwenden wir

    ds² = −dT² + dr² + r² [1−d(x) f(u)] dΩ²,
    f(u) = (−65u² + 154u⁴ − 81u⁶)/8,
    R_ar(T,r) = r √[1−d(x) f(u)].

Die Radialmetrik und die Uhr eines mitbewegten Beobachters bei festem r sind exakt gleich. Eine radial hin- und zurücklaufende Lichtmarke benötigt die Eigenzeit 2|Δr|. Das ist eine Aussage für radiale Signale. Der Arealradius misst dagegen die Fläche der vollständigen Symmetriesphäre. [Geometrische Definition des Arealradius](https://www.mdpi.com/2218-1997/4/10/109)

Sei H(s) das Polynom 10s³−15s⁴+6s⁵ auf [0,1], fortgesetzt durch 0 links und 1 rechts. Für jeweils eine Zielzeit z verwenden wir d_A(x) = (199/5000)H(x) + (161/625)H(64(x−z)+1) und d_B(x) = (199/5000)H(x) + (161/625)H(64(x−z)). Beide sind zweimal stetig differenzierbar. Ihre Werte und die lokalen Metriken stimmen ausserhalb (z−1/64,z+1/64) überein. Der Übergang findet für A früher statt. Wegen H′(s) = 30s²(1−s)² im Inneren schrumpfen beide Oberflächen während 0 < x < 1 streng. Sie haben dieselbe Anfangsgeometrie, Anfangsgeschwindigkeit und Endgeometrie. Die Anfangsgeschwindigkeit der Kontrollen ist null. Der Projektvertrag enthält zusätzlich einen eigenen dynamischen Test der Anfangsgeschwindigkeit.

Für z = 1/2 reicht die ereignisfreie Lücke mindestens von x = 0,475 bis x = 0,813. Kein Ereignis liegt in der verwendeten Übergangszone. Dasselbe wurde für die beiden separaten Gegenpaare bei z = 1/4 und 3/4 geprüft. Die zwei anderen Paare verlegen jeweils den Zeitpunkt des einzigen Übergangs. Die Tabellenzeilen beschreiben je einen eigenen Versuch.

Für alle drei Paare liegt d zwischen 0 und 1487/5000. Die Identität 1−f = (u²−1)²(81u²+8)/8 sichert die positive Winkelmetrik. Am Ursprung gilt f = O(u²) und die räumliche Geometrie ist regulär. Die Ableitung der reduzierten Fläche u²(1−d f) ist 2u[1−d g] mit g = f+u f′/2. Auf dem ganzen Prüfgebiet 0 ≤ u ≤ 9/8 gilt g < 13/4. Der Prüfer begrenzt die Bernstein-Koeffizienten auf 128 rationalen Teilintervallen. Die Fläche wächst damit radial auch in beiden Schalen an der Oberfläche.

## Welche Daten identisch bleiben

Das Eigenvolumen bis u, geteilt durch 4πR₀³, ist

    V(u)/(4πR₀³) = u³/3 − d(x)(−13u⁵ + 22u⁷ − 9u⁹)/8.

Bei u = 1 verschwindet der zweite Term für jedes x. Beide gesamten Kugelvolumina betragen daher an jedem Schnitt 4000π/3. Auch das integrierte Vierervolumen der gesamten materiellen Weltröhre ist auf jedem gemeinsamen Zeitintervall gleich. Einzelne Schalenvolumina können sich ändern. Der Prüfer bestätigt die Integrale unabhängig durch eine für die Flächenpolynome exakte Neunpunkt-Quadratur.

Eine positive, geodätisch mitbewegte Testmaterie lässt sich für beide Geometrien eines Paares konstruieren. An jedem Abtastradius setze man b(rᵢ) = wᵢ [1−d(xᵢ) f(rᵢ/R₀)]. Diese Werte sind für A und B gleich, positiv, und die Radien sind paarweise verschieden. Zwischen ihnen interpolieren wir monoton mit H, im innersten Bereich konstant. Für r > 10 ist b = 0. Nun sei ρ(T,r) = b(r)/[1−d(x) f(r/R₀)] und der Viererstrom J = ρ ∂_T. Dann stimmt ρ an allen 15 Ereignissen mit dem jeweiligen gespeicherten wᵢ überein. Auf jeder mitbewegten Schale gilt identisch

    ρ dV = 4π b(r) r² dr,       ∂_T(ρ √det g_Raum) = 0.

Die positive Materialmenge jeder Schale bleibt somit erhalten, auch über die Staub-Vakuum-Grenze fliesst keine Materie. Beim rationalen Beispielfeld prüft das Programm alle 15 Dichtewerte und integriert die Materialmenge. Das Argument mit der positiven Interpolation gilt punktweise für jede Belegung im Paket. Die Gesamtmaterialmenge ist in einem Paar identisch. Diese zu Kontrollzwecken konstruierte Testmaterie liefert keine Eichgleichung für die N15-Wirkungsladung oder die drei P3-Ruhemassen.

Der endliche Ordnungs- und Feldsatz ist paarweise identisch. Jede rein daraus berechnete Auslese erhält dieselben Eingaben, einschliesslich diskreter Intervallzählungen und der in der vorherigen Studie verwendeten Randquellen. Die Konstruktion macht keine Annahme über die Gleichheit von Gewichten einer zusätzlichen Kontinuumsdynamik oder von Lichtmessungen unter einem von null verschiedenen Öffnungswinkel.

## Drei unabhängige Gegenpaare

| Zielzeit x | Radius A | Radius B | Kleinster ungünstigster relativer Fehler |
| --- | ---: | ---: | ---: |
| 1/4 | 8,59232 | 9,97938 | 7,469 % |
| 1/2 | 8,50000 | 9,90000 | 7,609 % |
| 3/4 | 8,40666 | 9,81998 | 7,754 % |

Für zwei wahre Werte a < b bei identischer Eingabe minimiert 2ab/(a+b) den grösseren der beiden relativen Betragsfehler. Der Wert dieses grösseren Fehlers ist (b−a)/(b+a). Die Aussage betrifft eine garantierte relative Punktgenauigkeit über das jeweilige Vergleichspaar. Die prozentuale Grenze ist keine statistische Konfidenzaussage und kein beobachteter Fehler einer physischen P3-Vorhersage.

## Dieselbe geometrische Auslese mit zusätzlichen lokalen Daten

Wir übernehmen den unveränderten Ausleser der Schalenstudie. Ihm werden zwei räumliche Eigenvolumina unmittelbar innerhalb und ausserhalb der bei r = 10 mitbewegten Grenze, Radarzeiten radialer Nachbarmarker, Reflexionszeit und Uhreinheit übergeben. Für jede synthetische Volumenablesung gilt ein Intervall von ±1 %. Jeder Emissions- und Empfangszeitstempel hat eine absolute Intervallhalbbreite von 1 % der nominalen einfachen Lichtlaufzeit. Beide Stempel dürfen unabhängig variieren. Die radiale Metrik ist zeitlich konstant, die radiale Driftschranke daher null. Die Kontrollauslese verwendet A_in = V_in/ℓ_in als untere und A_out = V_out/ℓ_out als obere Flächengrenze. Alle Ausgabeschranken sind nach aussen gerundet.

| Halbbreite δr/R₀ | Radius A bei x = 1/2 | Radius B bei x = 1/2 | Befund |
| --- | ---: | ---: | --- |
| 1/8 | [8,1425; 9,6693] | [9,2111; 10,6650] | Intervalle überlappen |
| 1/16 | [8,2303; 8,9701] | [9,5015; 10,3207] | getrennt, A überschreitet +5 % |
| 1/32 | [8,3054; 8,7462] | [9,6500; 10,1578] | beide vollständig innerhalb ±5 % |

Bei 1/32 trennt die Auslese alle drei Paare und hält für jede der sechs Geometrien die 5-%-Grenze ein. Für x = 1/2 wurden auch 1/64, 1/128 und 1/256 wiederholt. 1/32 ist die gröbste hier getestete Dicke, bei der beide Radien dieses mittleren Paars innerhalb der Toleranz eingeschlossen werden. Die Volumina werden aus der jeweiligen synthetischen Geometrie erzeugt. Dieses ideale Gesamtfehlerexperiment ist vom vollständigen P3-Budget mit separaten Teilgrenzen zu unterscheiden. [Vorhandener Schalenprüfer und frühere Kontrollen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ea05b04677917d8e970c3bb0888d024a479cd500/research/rax_cqg/dust_collapse/packages/CST_DUST_P3_Massentransport_und_Oberflaeche_Pruefpaket.zip)

## Nachrechnung und physischer Anschluss

Die Datei `ergebnisse.json` enthält alle 105 Kausalabstände, Intervallgrenzen und Auslesewerte. Für die Nachrechnung genügen Python ab 3.10 und die Standardbibliothek. Der erste Befehl kontrolliert die Prüfsummen und berechnet alle Ergebnisse neu. Die beiden weiteren Befehle lesen die archivierten Schalendaten unabhängig vom Generator aus.

    python3 -B pruefen.py
    python3 -B quellen/auslesen.py < Schale_A.json
    python3 -B quellen/auslesen.py < Schale_B.json

Es handelt sich um neu konstruierte, sphärische und kinematische Modellgeometrien. Ihre Testmaterie ist inhomogen. Eine Lösung der gekoppelten CST- oder Einstein-Staubgleichungen, den Schwarzschild-Anschluss und eine typische vierdimensionale Zufallsstreuung begründet dieser Versuch nicht. Alle Stichprobenpunkte liegen auf einem Strahl. Eine unabhängig bestimmte Dynamik, eine definierte Ensembleverteilung, räumliche Beobachtungen in verschiedenen Richtungen oder lokale Schalenvolumina können die Mehrdeutigkeit aufheben. Der Versuch belegt die fehlende Eindeutigkeit aus den benannten endlichen Daten, auch wenn man dem Modell zusätzliche radiale Messungen, eine Grenze und eine Uhrkalibrierung zugesteht.

Für P3 fehlen die eigenständige physikalische Masseneichung und die auf derselben dynamischen Präparation gewonnenen Oberflächen- und Schalenbeobachtungen samt Fehlerbudget. Die 60 Einträge des mitgelieferten Registers stehen auf NOT_RUN. Die geometrischen Vergleichsmodelle und die Wahl ihrer Übergangsfenster sind explorativ. Es wurden keine externen Rechenläufe gebucht. [Stationärer Ausgangszweig](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/ea05b04677917d8e970c3bb0888d024a479cd500/research/rax_cqg/dust_collapse/n15_stationaerer_staubstrom_v0_1) · [Physischer P3-Vertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ea05b04677917d8e970c3bb0888d024a479cd500/research/rax_cqg/dust_collapse/correspondence_v0_1/DERIVATION.md)
