# Endliche Trennleistung für flach gegen de Sitter aus einer einzigen Ordnung

## Aussage und Beobachtungsmodell

Im vollständigen vierdimensionalen Diamanten D mit |t|+|x|<1/2 ist die Metrik
g_h=(1-ht)^(-2)η. Die zwei einfachen Hypothesen sind h=0 und h=1/2. Die
Eigenzeit zwischen den Spitzen ist T=2 atanh(h/2)/h mit Grenzwert 1. Damit
sind q=RT²=48 atanh(h/2)² gleich 0 und rund 3,131314. N ist fest, die
Ereignisse sind unabhängig und gleichmäßig nach normiertem physischem Volumen
verteilt. Die Beobachtung ist die unbeschriftete strikte Kausalordnung, ohne
zusätzliche Spitze, Koordinate, Uhr oder Intensitätsmessung.

Gesucht wird eine Menge kompatibler Kandidaten. Für jeden der beiden wahren
Parameter h soll die Wahrscheinlichkeit, h zu verwerfen, höchstens 0,05 und
die Wahrscheinlichkeit, den jeweils anderen Kandidaten zu verwerfen,
mindestens 0,80 sein. Das sind unbedingte Aussagen über eine einzelne
Realisierung unter festem Modell. In der Hauptregel sind die beiden
Verwerfungsbereiche disjunkt. Im Zwischenraum bleiben beide Kandidaten.
Die Trennleistung ist keine bedingte Wahrscheinlichkeit dafür, dass ein
bereits ausgegebenes Modell wahr ist.

## Der vollständige Paaranteil

Für G(x,y)=1 bei Vergleichbarkeit und sonst 0 sei
U=Σ_(i<j) G(X_i,X_j)/M, M=N(N-1)/2. Schreibe p=E G, r(x)=E G(x,Y),
v=Var r(X)=w-p² und w=E r(X)². Die exakten rationalen Einschließungen von
p und w werden mit den unveränderten Vorwärtsrechnungen aus PR 54 und 56
reproduziert. Für h=0 gilt p=0,1, w=0,02. Für h=1/2 sind sichere äußere
Dezimalgrenzen 0,1034776344503 ≤ p ≤ 0,1034776344505 und
0,0211369851919 ≤ w ≤ 0,0211578956258.

Die Zerlegung
U-p=(2/N)Σ_i(r(X_i)-p)+D trennt die lineare Projektion und den entarteten Rest.
D ist das Mittel der Terme H_ij=G_ij-r(X_i)-r(X_j)+p. Bedingt auf einen
einzelnen Endpunkt hat H Mittelwert 0. Damit sind H_ij und H_kl für verschiedene
ungeordnete Paare unkorreliert, selbst wenn sie genau einen Endpunkt teilen.
Auch der Rest und die lineare Projektion sind orthogonal in L². Die
Binärvarianz von G zerfällt in 2v+Var H, also gilt exakt

    Var D = 2[p(1-p)-2v]/[N(N-1)].

Man benötigt keine Unabhängigkeit des Rests von der linearen Summe.

## Endliche Fehlerschranke

Sei m3 eine obere Schranke für E|r(X)-p|³. Shevtsovas endliche i.i.d.
Berry-Esseen-Ungleichung liefert für die standardisierte lineare Summe einen
maximalen Abstand zur Standardnormalverteilung von
B=0,3328(m3/v^(3/2)+0,429)/√N. Die untere und obere Richtung sind
gleichermaßen gültig. Geschlossene Schwanzereignisse sind über linksseitige
Grenzwerte der Verteilungsfunktion kontrolliert, da Φ stetig ist.

Für 0<t<d folgt durch Aufteilung der beiden Ereignisse und die einseitige
Cantelli-Ungleichung für ±D

    P(±(U-p) ≥ d)
       ≤ Φ(-(d-t)√N/(2√v)) + B + Var(D)/(Var(D)+t²).

Cantelli folgt beispielsweise durch Markov auf (±D+s)² und Minimierung
bei s=Var(D)/t. Der Vorwärtswert p wird jeweils durch den für die
Schwanzwahrscheinlichkeit ungünstigen Intervallendpunkt ersetzt. In der
Normalverteilung wird v nach oben, im Berry-Esseen-Nenner nach unten
abgeschätzt. Für die obere Restvarianz werden p(1-p) nach oben und v nach
unten gerundet. Die Minimierung über vierzig vorher definierte t-Werte
wählt unter gültigen deterministischen Obergrenzen. Sie verwendet keine
Testwolke.

Für Φ(-z) rundet das Programm z nach unten, begrenzt es auf 4 und integriert
die Taylor-Untergrenze für exp(-x²/2) bis zur ungeraden Ordnung 31 in x²/2
exakt. Die Untergrenze der Integrationskonstante 0,3989422 folgt aus π<355/113.
Die Integralschranke wird vom Wert 1/2 abgezogen. Nach jeder letzten
Fehleraddition wird nach oben auf 10^-9 gerundet.

## Zertifikat des dritten absoluten Moments

Die in v0.1 hergeleitete kausale Umparametrisierung des Diamanten bringt
beide Modelle in eine gemeinsame Karte. Mit U₀=2(t-r), V₀=2(t+r), S=U₀V₀
hat das gekrümmte Punktgesetz die normierte Dichte
d_h=(1-δS)^(-4)/Z relativ zum flachen. Hier ist
δ=(1-√(1-h²/4))/(1+√(1-h²/4)), Z=E₀[(1-δS)^(-4)].
Der byteidentische v0.1-Code schließt Z mit rationalen Momenten und
geometrisch begrenztem Rest ein. Daraus werden globale Konstanten L und H
für L≤d_h≤H gewonnen. Die unveränderte Ordnungsrelation und Positivität geben

    L r₀(x) ≤ r_h(x) ≤ H r₀(x).

r₀ ist die flache Summe der normierten Volumina der Teilintervalle von der
unteren Spitze bis x und von x bis zur oberen Spitze. In normierten
Nullkoordinaten lautet sie

    r₀ = [(1+U₀)²(1+V₀)²+(1-U₀)²(1-V₀)²]/16.

Für symmetrische Integranden in U₀,V₀ kann das ganze Quadrat mit Dichte
3(V₀-U₀)²/8 anstelle des geordneten Halbquadrats benutzt werden. Es wird in
G²=128² gleich große Zellen mit Indizes i,j=0,...,G-1 zerlegt. Durch exakte
Integration ist die flache Zellmasse [6(i-j)²+1]/G⁴. Per Monotonie der
beiden einzelnen Summanden liegt r₀ zwischen

    l = [(ij)²+((G-i-1)(G-j-1))²]/G⁴,
    u = [((i+1)(j+1))²+((G-i)(G-j))²]/G⁴.

Auf jeder Zelle ist |r_h-p| höchstens max(0,p_oben-Ll,Hu-p_unten).
Daher begrenzt die Summe aus Zellmasse mal H mal Kubus dieses Maximums
das dritte absolute Moment. Sämtliche Summen werden mit ganzen Zahlen und
rational nach außen gerundeten Endpunkten gebildet. Dies begrenzt auch den
Fehler innerhalb jeder Zelle. Die separate Gauß-Quadratur in audit.py ist
eine numerische Kontrolle und wird zur Freigabe nicht benötigt.

## Konkrete ganzzahlige Regel und Richtungen

N=30.000 ergibt M=449.985.000. Bei C₂≥46.010.967 wird h=0 verworfen,
bei C₂≤45.527.232 wird h=1/2 verworfen. Dazwischen bleiben beide zulässig.
Diese Grenzen sind das Auf- bzw. Abrunden von 0,10225 M und 0,101175 M.
Für eine Nichteindeutigkeit werden beide Kandidaten ausgegeben.
Die Rechnung benutzt die etwas konservativeren reellwertigen Grenzen.

| Wahrheit | Fehlalarm höchstens | Verwerfung der Alternative mindestens |
|---|---:|---:|
| h=0 | 0,047204836 | 0,803098016 |
| h=1/2 | 0,048898005 | 0,807104470 |

Die einzelnen Beiträge der Schranke sowie die gewählte Resttoleranz stehen
in certificate.json. Deren Zeilen sind nach wahrer Geometrie gruppiert.

## Zweite Konstruktion mit disjunkten Paaren

Eine zufällige, von Ordnung und Geometrie unabhängige Paarung zerlegt N=96.000
Ereignisse in 48.000 disjunkte Paare. Für jede feste, datenunabhängige
Indexpaarung sind ihre Vergleichbarkeiten i.i.d. Bernoulli(p). Die gleiche
Produktverteilung gilt marginal bei einer unabhängigen zufälligen Paarung.
Für eine unbeschriftete Ordnung wird die Paarung uniform gewählt, sodass
das randomisierte Verfahren invariant gegenüber einer Umnummerierung ist.
Das gilt nicht automatisch für eine datenabhängige Auswahl vergleichbar
erscheinender Partner oder eine Paarung nach topologischer Sortierung.

K ist damit binomialverteilt. Bei K≥4909 wird h=0 verworfen, bei K≤4856
wird h=1/2 verworfen. Das Verfahren benötigt höchstens 48.000 Anfragen nach
ungerichteter Vergleichbarkeit, entsprechend maximal 96.000 gerichteten
Matrixeinträgen. Voraussetzung ist eine Abfragemöglichkeit der transitiven
Relation. Der Aufwand für den Aufbau der Transitivhülle aus Hasse-Kanten ist
nicht eingerechnet.

Die Binomialmasse wird am Modus auf 1 normiert. Alle angrenzenden relativen
Massen werden mit den Binomialquotienten in beide Richtungen berechnet. Jede
Division wird mit ganzen Zahlen auf der Skala 2^124 nach außen gerundet.
Schließlich wird die untere/obere Schwanzsumme durch die obere/untere
Gesamtmasse dividiert. Alle 48.001 möglichen K sind enthalten. Für den
gekrümmten Fall genügt die untere p-Grenze sowohl beim oberen Fehlalarm
(unterer Schwanz) als auch bei der unteren Trennleistung (oberer Schwanz).
Die Rundungsfehler und die Unsicherheit im geometrischen Vorwärtswert sind
damit in der jeweiligen Richtung eingeschlossen.

| Wahrheit | Fehlalarm höchstens | Verwerfung der Alternative mindestens |
|---|---:|---:|
| h=0 | 0,049746209 | 0,805147462 |
| h=1/2 | 0,048628579 | 0,809239933 |

## Notwendige Elementzahl für jeden Test

Sei A die Affinität der beiden Einpunktgesetze in der gemeinsamen Karte von
v0.1. Dort wurde A²≥L mit L>0,99990813817824586 rational zertifiziert.
Für das binäre Ereignis E, das flache Modell zu verwerfen, gilt mit
a=P₀(E), b=P₁(E) durch zweimal Cauchy-Schwarz und Produktstruktur

    A^N ≤ √(ab)+√((1-a)(1-b)).

Das gilt auch für einen aus der Ordnung randomisierten Test, indem ein
unabhängiger Zufallswert mit in den gemeinsamen Beobachtungsraum genommen
wird. Der Übergang zu einem Ereignis kann die Affinität nur vergrößern.
Für a≤0,05 und b≥0,80 wird die rechte Seite bei a=0,05 und b=0,80 maximal.
Das folgt auch aus der Darstellung als Kosinus der Differenz der Winkel
arcsin(√a) und arcsin(√b). Damit ist L^N≤(1/5+√0,19)² notwendig.
Rationale Untergrenzen für L^N und eine Obergrenze für die rechte Seite
schließen alle N≤9856 aus. Ab N=9857 schließt diese Rechnung das Ziel
nicht mehr aus. Die engere Untergrenze nutzt getrennte Fehlalarm- und
Leistungsziele anstelle der alleinigen Totalvariationsdifferenz aus v0.1.
Zusammen mit der vollständigen Paarregel liegt die unbekannte kleinste
hinreichende Elementzahl für diese beiden einfachen Hypothesen zwischen
9857 und 30000, einschließlich der Grenzen.

## Reproduzierbarkeit und Literatur

1. Ursprungsversuch und ausgerichtete Karte: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/163
2. Vorwärtsrechnung für p: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/54
3. Gemeinsamer Endpunkt und Intervallrechnung für w: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/56
4. W. Hoeffding (1948), A Class of Statistics with Asymptotically Normal Distribution. https://doi.org/10.1214/aoms/1177730196
5. I. Shevtsova (2011), On the absolute constants in the Berry-Esseen type inequalities for identically distributed summands. Verwendet wird die erste Strukturungleichung im Abstract. https://arxiv.org/abs/1111.6554

Die vier großen Einzelbeispiele sind nach der lokalen Fixierung berechnet.
Sie prüfen den Programmweg und liefern keine Schätzung mit ausreichender
Stichprobengröße für eine unabhängige empirische Leistungsaussage. Schwächere
Krümmungen, unbekannte Dichte, Randmasken und absolute R-Werte benötigen
eigene Behandlungen. Die Herleitung und Wiederholung sind projektintern.
