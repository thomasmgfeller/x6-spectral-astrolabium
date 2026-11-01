# Drei Krümmungen und ein Konfidenzintervall aus einer endlichen Ordnung

## Modell und Ziel

Im vollständigen vierdimensionalen Kausaldiamanten |t|+|x|<1/2 gilt
g_h=(1-ht)^(-2)η mit 0≤h≤1/2. Bei gegebenem N sind die Ereignisse iid aus dem
normierten physischen Vierervolumen gezogen. Die Beobachtung ist die strikte
Kausalordnung. Die beiden äußeren Spitzen werden nicht als Punkte mitgezählt.
Die dimensionslose Krümmung ist q=RT²=48 atanh(h/2)², wobei T die Eigenzeit
der Spitzen ist. Absolute Werte für R erfordern eine eigene Zeitskala.

Die erste Ausgabe ist ein geschlossenes äußeres Intervall für q oder die leere
Menge. Für jedes feste h in der **ganzen** Familie soll die Überdeckung mindestens
95 % betragen. Die zweite Ausgabe ist die Menge der mit der Beobachtung vereinbaren
Rasterwerte h∈{0,1/4,1/2}. Für jeden wahren Rasterwert ist das Erfolgsereignis
die korrekte **einelementige** Menge. Gefordert sind mindestens 80 % unbedingte
Wahrscheinlichkeit dafür und höchstens 5 % Verwerfung des wahren Rasterwerts.
Einzelentscheidungen werden nicht nachträglich herausselektiert. Ein
Zwischenwert kann keine korrekte Raster-Einzelmeldung erzeugen.

## Gemeinsamer Vorwärtswert und Kontrolle der ganzen Familie

Für die Vergleichbarkeit G(X,Y) setze p(h)=E G, r_h(x)=E[G(x,Y)|x],
w(h)=E r_h(X)² und v=w-p². Die exakten Geometrie- und Momentquellen stammen
aus PR 54 und 56 und liegen über das unveränderte v0.2-Paket bei.
certificate() des Moduls exact.py bestätigt strikte Monotonie in z=h²/4
über den ganzen Parameterbereich. Alle verwendeten p-Einschließungen sind
rational und umfassen den Reihenrest.

Für ein geschlossenes h-Teilintervall [a,b] wird der signierte Polynomzähler
W16 der Dreipunktwahrscheinlichkeit w=W/Z³ sowohl nach unten als auch nach
oben begrenzt. Jeder Monomterm verwendet je nach Vorzeichen die richtige
Endpunktpotenz. Der monotone Betrag des Restes wird am rechten Rand begrenzt.
Der Normierer Z steigt in h (positive Potenzreihe in h²). Der positive
Zähler wird durch die jeweils ungünstigen positiven Endpunktschranken für
Z³ dividiert. Für v werden die Quadrate der entgegengesetzten p-Endpunkte
subtrahiert. Über 64 lückenlos überdeckende Zellen ergeben sich die äußeren
Grenzen 0,009993430053≤v≤0,010560145904. Diese sind für alle h gültig;
der zusätzliche Test an jedem Mittelpunkt ist eine Gegenkontrolle.

Der v0.1-Koordinatenwechsel richtet die Kausalrelationen beider Modelle im
selben flachen Diagramm aus. In normierten Nullkoordinaten u=2(t-r), v₀=2(t+r)
ist die Einpunktdichte relativ zum flachen normierten Volumen proportional zu
(1-δu v₀)^(-4), δ=(1-√(1-h²/4))/(1+√(1-h²/4)). Die Quotienten von größtem und
kleinstem unnormiertem Gewicht sind global durch H=((1+δmax)/(1-δmax))⁴
beschränkt. Die normierte Dichte liegt daher zwischen 1/H und H. Wie in v0.2
wird daraus über 128² exakte Zellmassen und lokale obere/untere Schranken des
flachen Vergleichbarkeitsprofils ein einheitliches drittes absolutes Moment
für r_h(X)-p gewonnen. In v0.3 kommen die globalen p- und Dichteendpunkte
zum Einsatz. Die rational ermittelte Obergrenze beträgt 0,0050044789419.

## Alle Paare

Bei N=600000 sei Y=C₂/binom(N,2) und der Radius r=0,00056. Der Referenzbeweis
zerlegt Y-p in eine Summe (2/N)Σ_i(r_h(X_i)-p) und einen entarteten Rest D.
Zwei verschiedene Restpaare sind wegen der bedingten Zentrierung unkorreliert.
Var(D)=2[p(1-p)-2v]/[N(N-1)]. Für 0<t<d gilt daher für beide Vorzeichen

    P(±(Y-p) ≥ d) ≤ Φ(-(d-t)√N/(2√v))
                  + 0,3328 (m3/v^(3/2)+0,429)/√N
                  + Var(D)/(Var(D)+t²).

Verwendet werden die erste uniforme i.i.d.-Berry-Esseen-Ungleichung von
Shevtsova für die Projektion, die einseitige Cantelli-Schranke für den Rest
und eine Vereinigungsabschätzung. Die Konstruktion verlangt keine Unabhängigkeit
zwischen der Projektion und dem Rest. Die Referenzroutine minimiert über
vorab definierte t, behält sichere Endpunkte für v, m3 und p und begrenzt
den Normalschwanz rational durch die integrierte Taylor-Untergrenze der
Exponentialfunktion. Sie wurde unverändert aus v0.2 übernommen.

## Achtergruppen

Bei N=900000 werden die Ereignisse unabhängig von der Ordnung zufällig
permutiert und in m=112500 Gruppen der Größe b=8 geteilt. Innerhalb jeder
Gruppe werden alle 28 Paare abgefragt. Y ist die Zahl vergleichbarer
Paare dividiert durch m·28=3150000. Der Radius beträgt 0,00058.

Bedingt auf eine feste datenunabhängige Indexpartition sind die Gruppen
unabhängig, weil die Punkte iid sind. Die gemeinsame Produktverteilung der
Gruppenstatistiken ist für jede solche Partition dieselbe. Eine unabhängige
uniforme Permutation macht die Regel auch bei beliebiger Eingabelabelung als
randomisiertes Verfahren invariant. Die Aussage gilt marginal über Punkte
und unabhängige Gruppierung. Ein datenabhängiges Sortieren oder wiederholtes
Ausprobieren mehrerer Gruppierungen ist nicht abgedeckt.

Der Vergleichbarkeitsanteil Z einer Gruppe liegt in [0,1], hat Mittel p und
Varianz s²=[2p(1-p)+4(b-2)v]/[b(b-1)]. Dies folgt durch Zählen von
Vergleichspaaren mit einem gemeinsamen Endpunkt und unabhängigen disjunkten
Paaren. Es werden nur die m **ganzen Gruppen** als unabhängig behandelt.
Wegen p≤1/2 gilt E|Z-p|³ ≤ (1-p)s². Für obere und untere Schranken
sU²,sL², berechnet aus den einheitlichen p- und v-Grenzen, ergibt sich

    P(±(Y-p) ≥ d) ≤ Φ(-d√m/sU) +
                     0,3328((1-pL)/sL+0,429)/√m.

Für geschlossene Schwanzereignisse folgt die gleiche Schranke über einseitige
Grenzwerte, da die Normalverteilungsfunktion stetig ist. Alle Wurzeln und
Fehleradditionen werden in der sicheren Richtung gerundet.

## Eine Beobachtung liefert zwei verschiedene Antworten

Für jede Methode sei B(d) die jeweilige einseitige Obergrenze. Die wahre
Paarwahrscheinlichkeit liegt mit Wahrscheinlichkeit mindestens 1-2B(r) im Band
[Y-r,Y+r]. Dieses Ereignis allein garantiert bereits beide Arten von
Wahrheitseinschluss. Mehrfachprüfungen gegen die beiden anderen Rasterpunkte
benötigen dafür kein zusätzliches Fehlerbudget.

Für die Rastermeldung werden die äußeren Vorwärtsintervalle [pL_i,pU_i]
direkt mit dem Band geschnitten. Für einen wahren Rasterpunkt i seien

    d_left  = min(r, pL_i - pU_(i-1) - r),
    d_right = min(r, pL_(i+1) - pU_i - r),

wobei ein fehlender Nachbar den entsprechenden Abstand r ergibt. Alle
Abstände sind positiv. Auf dem offenen Ereignis p_i-d_left < Y < p_i+d_right
bleibt i enthalten; wegen der positiven Abstände und der Monotonie sind
alle anderen Kandidaten ausgeschlossen. Also ist der korrekte Alleintreffer
mit Wahrscheinlichkeit mindestens 1-B(d_left)-B(d_right) gesichert.
Die strikten inneren Grenzen behandeln auch Gleichstände vorsichtig.

Für die kontinuierliche Ausgabe werden 1024 geschlossene h-Zellen verwendet.
Zelle j bleibt möglich, wenn pL(h_j) ≤ Y+r und pU(h_(j+1)) ≥ Y-r. Alle
exakten Lösungen liegen in der Vereinigung dieser Zellen. Die äußeren
q-Schranken der ersten und letzten verbliebenen Zelle ergeben das ausgegebene
Intervall. Die begrenzte Gitterauflösung ist somit in der Überdeckung
enthalten. Eine leere kontinuierliche Menge meldet Unverträglichkeit mit
der Familie bei dieser Testregel und kann auch bei einem wahren Modell
im Fehlerereignis vorkommen. Die Liste der Rasterkandidaten wird separat
geprüft und kann bereits leer sein, während das Intervall noch andere
Krümmungen enthält. Wegen der äußeren Zellrundung ist auch am Rasterrand
die explizite Rasterprüfung maßgeblich.

Zwei erhaltene Zellen j≤k müssen pL(h_k)-pU(h_(j+1))≤2r erfüllen.
Daher begrenzt das Maximum von qU(h_(k+1))-qL(h_j) unter dieser notwendigen
Bedingung die Länge **jeder nichtleeren ausgegebenen Menge**. Die Kontrolle
erfolgt einmal mit zwei monotonen Zeigern, einmal über alle 524800 Zellpaare.
Die Grenzen betragen 1,019751493 (alle Paare) und 1,055928767 (Achtergruppen).
Es sind absolute Breiten in q, keine relativen Fehlerradien.

## Notwendige Ereigniszahl

Sei A die Affinität der Einpunktgesetze zweier unterschiedlicher Modelle in
der gemeinsam ausgerichteten Karte. Für N iid Punkte ist die Affinität A^N.
Die Reduktion auf die Ordnung, das Hinzufügen eines unabhängigen Zufallsseeds
und danach die Reduktion auf die Kategorien „nur i“, „nur j“, „übrige“
können die Affinität gegenüber den vollständigen Koordinaten nicht verringern.
Dies folgt durch Cauchy-Schwarz auf jeder Kategorie bzw. Integration über
den gemeinsamen Zufallswert.

In der ersten Kategorie ist die Wahrscheinlichkeit unter i mindestens 0,80,
unter j höchstens 0,05, denn sie verwirft j. In der zweiten Kategorie sind
die Rollen vertauscht. In der Identität 1-A_kat = (1/2)Σ(√p_k-√q_k)²
liefern bereits diese beiden disjunkten Kategorien zusammen mindestens
(√0,80-√0,05)²=9/20. Folglich muss A^N ≤ 11/20 sein. Mit der rationalen
Untergrenze L≤A² der aus v0.1 übernommenen Affinitätsrechnung muss
L^N≤121/400 gelten. Gerichtete ganzzahlige Potenzierung schließt für die
Paare (0,1/4), (0,1/2), (1/4,1/2) die Ereigniszahlen bis einschließlich
217346, 13015 und 22815 aus. Die größte dieser drei Schranken gilt für jeden
Test mit dem v0.3-Dreifachziel. Sie ist keine Behauptung optimaler Stichprobengröße.
Die v0.2-Frage betraf den einzelnen Kontrast flach gegen h=1/2.

## Daten und Gültigkeitsbereich

Die beiden Radiusentscheidungen stammen aus deterministischer Planung anhand
der Modellmomente. Der lokale Freeze umfasst Modell, Verfahren, Gates, Quellcode,
Zertifikat und Kontrollresultate vor Erzeugung der Pilotfälle. Im Pilot
sind die Entscheidungen für alle 120 Beobachtungsdatensätze rekonstruierbar:
gespeichert sind genau 112500 Gruppenzahlen je Fall (13,5 Millionen insgesamt),
separate Simulationswahrheiten und Fingerabdrücke. Pro Fall werden die ersten
256 Gruppen zusätzlich mit einem zweiten Kausalprädikat geprüft. Je prüfbarer
Wahrheit verwenden zwei gleich große Teilgruppen die ursprüngliche und die
ausgerichtete konforme Karte. Der Auswerter erhält keine Wahrheit oder
Simulationskoordinaten. Die Seeds sind reproduzierbar; das Verfahren ist keine
extern beaufsichtigte Verblindung. Beim Vollzählverfahren wurden der Beweis,
die Umkehrung und strukturierte Ordnungen einschließlich einer mit 600000
Ereignissen geprüft. Der Zufallspilot in voller Größe betrifft die Achtergruppen.

Das Modell setzt die Beprobung, Dimension und den vollständigen Diamanten
voraus. Beliebige Raumzeiten, variable unbekannte Dichte, eine Hasse-Liste
ohne transitive Abfragen und eine absolute Krümmung ohne Zeitskala liegen
außerhalb der Garantie. Die zugängliche transitive Relation bzw. ihre
Ausgangsgrade sind Eingabevoraussetzungen.

## Quellen

- Vorstudien und Reproduktionsstand: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/163 und https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/165
- Vorwärtsrechnung und gemeinsames Ankermoment: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/54 und https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/56
- I. Shevtsova (2011), On the absolute constants in the Berry-Esseen type inequalities for identically distributed summands. Erste Strukturungleichung im Abstract: https://arxiv.org/abs/1111.6554
