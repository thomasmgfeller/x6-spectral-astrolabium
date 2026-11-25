# Radius aus gezählten Raumzeitereignissen

CST-DUST · N15-Typ 1767356 · 25. November 2026

Die sechs kinematischen Kontrollradien des vorherigen Versuchs lassen sich aus geometrischen Ereigniszählungen in zwei kurzen Schalenzeitfenstern rekonstruieren. An der halben gemeinsamen Eigenzeit ergeben gerundete Radarzeitpaare die Intervalle [8,2883; 8,7711] für den Kontrollradius 8,5 und [9,5662; 10,1377] für 9,9. Die feste synthetische Stichprobe umfasst 695 935 lokale Echozeitpaare in sechs Aufnahmen. Im tatsächlichen N15-Datensatz fehlen die benötigten Expositionen. P3 steht auf HOLD_NOT_ELIGIBLE, alle 60 physischen Einträge auf NOT_RUN.

## 1. Was ein Ereignis hier misst

Der geometrische Referenzprozess streut zufällige Punkte proportional zum **Eigen-Viervolumen**, auch im stofffreien Aussenraum. Die Zähldichte λ hat Einheiten L⁻⁴. Die Erwartung in einer Raumzeitregion ist λ mal deren Vierervolumen. Der Feldwert wᵢ eines vorhandenen Staubereignisses ist eine andere Eingabe. Für den physikalischen CST-Kandidaten ist die Gültigkeit dieser Zählstatistik offen. [S. Surya, The causal set approach to quantum gravity](https://doi.org/10.1007/s41114-019-0023-1)

Gewährt sind in den Kontrollen die markierte mitbewegte Oberfläche, eine fehlerfreie Zuordnung zur Innen- oder Aussenseite, eine vollständige radiale Radarabdeckung der ganzen Sphäre und die bekannte gemeinsame Uhr x=T/T_end mit T_end=5√5/3. Beide Kontrollmetriken haben radial ds²=−dT²+dr². Für den radialen Kontakt eines Ereignisses mit einem seiner Winkelrichtung zugeordneten Oberflächenbeobachter gelten in x-Einheiten

    x = (Empfang + Emission)/2,
    Abstand vom Materialrand = T_end (Empfang − Emission)/2.

Die Eingabe des Auslesers enthält die beiden auf 2⁻¹⁸ gerundeten Zeitstempel und eine Seitenmarke. Ein Aussenereignis kann auch im Vakuum ein geometrisches Echo liefern. Der Radarzugriff und der Detektor sind synthetische Annahmen, deren physikalische Realisierung offen ist. Ein einzelner Beobachter auf einem Strahl liefert die geforderte Winkelabdeckung nicht.

## 2. Vom Vierervolumen zum Radius am Schnitt

Seien z die Zielzeit, H=T_end/m die Dauer einer Aufnahme und s=R₀/n die radiale Schalendicke. Die untere Grenze verwendet den **inneren** Streifen in [z,z+1/m]. Die obere verwendet den **äusseren** Streifen in [z−1/m,z]. Die im Radius nach aussen wachsende Fläche A(T,r) nimmt in beiden Kontrollmetriken im verwendeten Randstreifen zeitlich ab. Deshalb liegt der Mittelwert von A über die spätere innere Zelle unter A(z,Rand) und der über die frühere äussere Zelle darüber. Das ist die Brücke zwischen vierdimensionalen Zählungen und einem zweidimensionalen Flächenwert. Die zeitliche Monotonie muss unabhängig belegt sein. Bei Richtungswechsel der Fläche, etwa vor und nach einem Bounce, benötigt die Auslese eine andere Driftkontrolle.

Die Ableitungen werden direkt an den Originalmetriken geprüft. Es gilt A=4πr²[1−d(x)f(r/R₀)], d′≥0, f>0 im gesamten benutzten Randstreifen und ∂ᵣA>0. In der Gegenkontrolle bei z=1/2, n=64 und m=32 wurden die Zeitfenster vertauscht. Selbst bei idealer Zählung wird die vermeintliche untere Radiusgrenze für A um 11,79 % zu gross und die vermeintliche obere für B um 9,72 % zu klein.

Die Rundung jeder Echozeit verursacht höchstens g/2 Fehler in x und T_end g/2 im Abstand, g=2⁻¹⁸. Innen zählt der Ausleser nur Ereignisse, deren gesamte Zeit- und Abstandshülle ins Fenster passt. Aussen zählt er alle, deren Hülle es berühren kann. Das garantiert N_in,sicher ≤ N_in,wahr und N_aussen,möglich ≥ N_aussen,wahr, selbst bei ungünstigster Rundung. Die zugrunde liegenden Seitenmarken sind fest. Bei fehlender Aufnahme liefert der Ausleser MISSING_EXPOSURE. Eine nachgewiesen vollständige, aber leere Aufnahme liefert eine untere Grenze null und eine positive obere Poisson-Grenze.

Für die nominale Dichte λₙ gilt das Kontrollintervall [0,99λₙ; 1,01λₙ]. Die Garwood-Grenzen G₋(k) und G₊(k) des Poisson-Mittels werden mit einseitiger Fehlerwahrscheinlichkeit a=0,05/(2·524) gebildet. Für k>0 gilt G₋=Quantil_a der Gamma(k,1)-Verteilung, für k=0 gilt G₋=0. G₊ ist das (1−a)-Quantil der Gamma(k+1,1)-Verteilung. Der blinde Ausleser berechnet

    R_unten² = G₋(N_in,sicher) / [4π · 1,01λₙ · H · s],
    R_oben²  = G₊(N_aussen,möglich) / [4π · 0,99λₙ · H · s].

Widersprüchliche Grenzen werden als INCONSISTENT ausgegeben. Für jedes wahre λ im zugesicherten Band beträgt das Nichtüberdeckungsrisiko je Kontrollradius höchstens 2a. Diese Aussage gilt aufgrund der monotonen Zählschranken auch bei den gerundeten Zeitstempeln. Die sechs Fälle teilen das gleiche Design. Es wurde der im Projekt dokumentierte Ansatz 0,05/524 je Vergleich beibehalten. [Exakte Poisson-Inferenz](https://stat.ethz.ch/R-manual/R-devel/RHOME/library/stats/html/poisson.test.html) · [Originaler P3-Vertrag und Fehleraufteilung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ea05b04677917d8e970c3bb0888d024a479cd500/research/rax_cqg/dust_collapse/correspondence_v0_1/DERIVATION.md)

## 3. Wie die Zähldichte gewählt wurde

Die Archivgeometrie liefert exakte polynomiale Raum- und Zeitintegrale bis auf die gemeinsamen Konstanten π und T_end. Für den Zeitanteil wird H₅(t)=10t³−15t⁴+6t⁵ mit konstanter Fortsetzung integriert. Die Kurzzeitänderung wird bei jeder Prüfung über die wirkliche Fensterbreite integriert. Eine separate verschachtelte Quadratur der ursprünglichen Flächenelemente prüft die Mittelwerte beider gewählten Designs.

Für eine positive Stichprobenaussage werden vor den Zufallsziehungen zwei ganze Schwellen berechnet. k_min ist die kleinste innere Zählung, für die die untere Radiusgrenze mindestens 0,95 R beträgt. k_max ist die grösste äussere Zählung, für die die obere höchstens 1,05 R beträgt. R kommt nur bei der **Bewertung der bekannten Kontrollen** vor. Der Ausleser benötigt R nicht.

Für die Leistungsprognose wird innen eine garantiert mitgezählte Teilzelle verwendet. Ihre Zeitgrenzen rücken um je einen Tick nach innen, ihre äussere Abstandsgrenze um mindestens T_end g. Aussen wird das umfassende Fenster um einen Tick je Zeitende und mindestens T_end g in der Dicke erweitert. In beiden Rechnungen wird der radiale Guard mit 3,73g nach aussen gerundet. Der niedrigste innere Erwartungswert verwendet 0,99λₙ, der höchste äussere 1,01λₙ. Die Summe der zwölf ungünstigen Poisson-Schwänze und der sechs Überdeckungsrisiken 2a wird von eins abgezogen. Der resultierende Wert begrenzt die Wahrscheinlichkeit von unten, dass **alle sechs Intervalle gleichzeitig ihren Sollwert enthalten und vollständig im jeweiligen ±5-%-Band liegen**. Diese gemeinsame untere Schranke benötigt keine Unabhängigkeit zwischen den sechs Aufnahmen.

Das Raster enthält 30 Kombinationen aus Schalendicke und Fensterdauer sowie 13 Dichtefaktoren. Der lokale Prüfplan wurde vor Ausführung der Designrechnung festgeschrieben. Die Auswahl erfolgte auf den analytischen Kontrollgeometrien. Die festgelegte Punktstichprobe wurde anschliessend erzeugt. λ_ref=92,894688446 L⁻⁴ stammt aus der früheren Ganzkugelkontrolle. Die absolute physische CST-Zähldichte ist offen.

| Auswahl | λₙ/λ_ref | s/R₀ | H/T_end | Untergrenze für gemeinsamen Erfolg | Grösster geometrischer Radiusfehler ohne Rauschen oder Rundung |
| --- | ---: | ---: | ---: | ---: | ---: |
| Gesamtintervall innerhalb ±5 % | 128 | 1/64 | 1/256 | 99,927 % | 1,384 % |
| Zusätzlich geometrischer Anteil höchstens 0,75 % | 256 | 1/128 | 1/512 | 99,791 % | 0,490 % |

Die Schwellen gelten für die getesteten Zweierpotenzen und diesen Ausleser. Bei 64λ_ref erreicht die beste gemeinsame untere Erfolgsschranke im ersten Raster 83,43 %. Für das zweite Raster erreicht die beste zulässige Kombination bei 128λ_ref 39,08 %. Das ist keine obere Schranke auf die dort erreichbare Leistung.

Für die früheren vier Referenzstufen wurde zusätzlich eine **obere** Erfolgsgrenze berechnet. Bei exakt nominaler Rate kann die gesicherte Innenzählung höchstens die ideale Innenzählung erreichen. Die mögliche Aussenzählung ist mindestens so gross wie die ideale Aussenzählung. Die beiden idealen Poisson-Zellen eines Versuchs sind disjunkt und unabhängig. Das Produkt der entsprechenden beiden Schwellenwahrscheinlichkeiten ist eine Obergrenze für diesen Fall. Das Minimum dieser Obergrenzen über die sechs Fälle begrenzt deren gemeinsamen Erfolg. Anschliessend wird über die 30 Designs maximiert.

| Stufe | Obere Schranke des gemeinsamen Erfolgs, nominale Rate |
| --- | ---: |
| 1λ_ref | 0,000311 % |
| 2λ_ref | 0,004055 % |
| 4λ_ref | 0,081015 % |
| 8λ_ref | 1,721 % |

Die nominellen Erwartungszahlen je einzelner idealer Zelle liegen beim 128er-Design zwischen 23 677 und 34 383, beim 256er-Design zwischen 11 920 und 17 058 (nach aussen gerundet). Die feineren Zellen erklären, weshalb beim zweiten Design trotz höherer Dichte weniger Ereignisse je Zelle ankommen.

Eine ergänzende Budgetdiagnose prüft für jede ganze Zählung von 1 000 bis 100 000 die Verschiebung des jeweiligen Radiusendpunkts durch die einseitige statistische Grenze gegenüber dem Einsetzen der beobachteten Zählung selbst. Im 128er-Design liegt sie unter 1,285 %, im 256er-Design unter 1,817 % des jeweiligen wahren Kontrollradius. Chernoff-Schranken begrenzen das Risiko, dass eine der zwölf Zählungen den angegebenen Bereich verlässt, auf weniger als 10⁻³⁵⁹⁸ in beiden Designs. Diese Diagnose betrifft den statistischen Beitrag zur Intervallgrenze. Die anfängliche Präparation, die physische Randzuordnung, die kalibrierte Messabbildung, das tatsächliche Zählmass und übrige Teile des P3-Budgets sind eigenständig nachzuweisen.

## 4. Durchlauf mit gerundeten Einzelechos

Pro Seite entsteht eine lokale Poisson-Punktwolke durch Ausdünnung einer umschliessenden homogenen Stichprobe in Zeit und radialem Abstand. Die Akzeptanz ist proportional zum lokalen Flächenelement r²(1−d f). Der Faktor 4π integriert die beiden isotrop verteilten Winkel exakt. Die Zeitfenster der Aufzeichnung enthalten zusätzliche Randzonen. Nur die drei ganzen Spalten Emission, Empfang und Seite werden an den Ausleser weitergegeben. Die Rohdaten enthalten weder wahren Ereignisort noch Referenzradius. Sämtliche Aufnahmen benutzen die nominale Rate 128λ_ref, einen im Prüfplan festgelegten Seed und separate Teilströme.

| Zeit | Fall | Sichere Innenzählung | Mögliche Aussenzählung | Radiusintervall | Sollradius |
| --- | --- | ---: | ---: | --- | ---: |
| 1/4 | A | 24 956 | 25 884 | [8,4212; 8,8775] | 8,59232 |
| 1/4 | B | 33 120 | 34 657 | [9,7173; 10,2555] | 9,97938 |
| 1/2 | A | 24 184 | 25 260 | [8,2883; 8,7711] | 8,50000 |
| 1/2 | B | 32 109 | 33 857 | [9,5662; 10,1377] | 9,90000 |
| 3/4 | A | 23 423 | 24 591 | [8,1552; 8,6556] | 8,40666 |
| 3/4 | B | 32 156 | 33 348 | [9,5733; 10,0620] | 9,81998 |

Die sechs beobachteten Treffer stammen aus einem synthetischen Kontrolllauf. Die Wahrscheinlichkeiten im vorherigen Abschnitt stammen aus den Poisson-Schwänzen, unabhängig von diesem einzelnen Ausgang. Quantile und Wahrscheinlichkeiten wurden mit Gleitkommaarithmetik ausgewertet. Eine intervallarithmetische Zertifizierung statistischer Spezialfunktionen wurde nicht durchgeführt.

## 5. Abgleich mit N15 und Nachrechnung

Die 15 archivierten Uhrintervalle des stationären Typs 1767356 wurden samt voller Paketbreite einzeln mit beiden gewählten Fenstergrössen verglichen. Keines berührt eines der drei benötigten Fenster. Hinzu kommen die fehlende vollständige Winkelabdeckung und das fehlende unabhängige Vierervolumenmass auf der dynamischen Präparation. Darum lässt sich für diesen Typ kein physisches Nullzählergebnis oder Radiusintervall angeben. Nach wie vor fehlen auch die unabhängige Ruhemasse-Eichung und eine physische Freigabe des P3-Registers.

Für eine Fortsetzung auf dem gekoppelten Ensemble ist ein überprüfbarer Datensatz mit gemeinsamer Staubuhr, beobachteter Materialgrenze, Innen-/Aussenmarke und vollständiger räumlicher Annahme der Echos bzw. einer gleichwertigen geometrischen Schalenzuordnung erforderlich. Eine von der gesuchten Oberfläche unabhängige Kalibrierung der Zähldichte und des Streuungsgesetzes muss die Zählungen in Eigen-Viervolumina übersetzen.

    python3 -B auslese.py Instrument.json Radarzeitpaare.npz
    python3 -B pruefen.py

Der erste Aufruf liest nur Instrumentdaten und Echozeitpaare. Der zweite prüft alle Prüfsummen, zählt die archivierten Echos erneut, reproduziert die Rohdaten aus dem festen Seed und überprüft die Designauswahl, die Zahlenwerte, die Negativkontrollen und das P3-Register. Verwendet wurden Python 3.12, NumPy 2.3.5 und SciPy 1.17.0. Für den exakten Vergleich mit den archivierten Zufallsdaten sind diese Versionen empfohlen. Die Berechnung lief lokal. Das Prüfpaket enthält die Zahlen in voller Rechengenauigkeit, den lokalen Prüfplan und die Herkunftsnachweise. [Ausgangspunkt des stationären N15-Zweigs](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/ea05b04677917d8e970c3bb0888d024a479cd500/research/rax_cqg/dust_collapse/n15_stationaerer_staubstrom_v0_1)
