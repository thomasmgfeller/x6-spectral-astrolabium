# Welche Zellen müssen bei einer Fortsetzung erneut gemessen werden?

## 1. Messmodell und Ziel

Die Modellklasse ist dieselbe wie in v0.7. Es gibt 16 vorab definierte Zellen. Ein markierter Versuch in Zelle j liefert einen Bernoulli-Treffer mit Wahrscheinlichkeit p_j. Innerhalb und zwischen den Zellen sind die potentiellen Versuche unabhängig, die p_j bleiben in beiden Stufen gleich, Ausfälle gehen in den Nenner ein. Die Erzeugungsdichte s, die Referenzeffizienz e und der Transfer t bilden die wissenschaftliche Dichte f proportional zu s·e·t pro physischem Vierervolumen. Für das Verhältnis K von wesentlichem Supremum zu wesentlichem Infimum sind K(s)≤S, K(t)≤D und eine Variation von e innerhalb jeder Zelle um höchstens den Faktor C extern abzusichern. Hier ist S=D=C=1,0001. Die Referenz- und Wissenschaftsverteilungen werden von diesen Grenzen abgedeckt. Die Wissenschaftsordnung samt zufälliger Gruppierung ist von der Referenzmessung unabhängig.

Das physische Ziel ist K(f)≤K*=1,002. Aus K(f)≤SDC² p_max/p_min folgt für jedes unsichere Profil K(f)>K* die Existenz eines festen gerichteten Paares i≠j mit p_i−L p_j>0, wobei L=K*/(SDC²)≈1,00159930. Als günstig bezeichnen wir dieselbe Klasse wie in v0.7, mit m=min_j p_j≥P=0,49 und p_max/m≤r=1,0002. Alle positiven Garantien setzen gültige externe Nachweise voraus. Ist ihre Gültigkeit offen, lautet das Feldergebnis HOLD.

## 2. Operative Regel

Der erste Messblock umfasst n₁=27.000.000 Versuche je Zelle. Für die empirischen Trefferquoten x_i definiere z_ij=x_i−L x_j. Der erste Maximalwert über i≠j ist max(x)−L min(x), auch bei Gleichständen. Die Entscheidung ist vorab festgelegt.

1. Gilt für mindestens ein Paar z_ij≥+0,000020, beende die Messung mit HOLD.
2. Markiere jede gerichtete Beziehung mit z_ij≤−0,000369 als für diese Entscheidung ausreichend geprüft. Die übrigen gerichteten Paare bilden E. Bei leerem E endet die Messung mit GO.
3. Bei Fortsetzung ist V(E) die Menge aller Zellen, die als erster oder zweiter Endpunkt wenigstens eines Paares in E auftreten. Ausschließlich diese Zellen erhalten je 19.000.000 zusätzliche Versuche. Sie erreichen kumuliert n₂=46.000.000. Jeder Endpunkt wird unabhängig davon, in wie vielen offenen Paaren er vorkommt, nur einmal nachgemessen.
4. Für jedes (i,j)∈E berechne z_ij aus den kumulierten 46 Millionen Versuchen beider Endpunkte. GO genau dann, wenn jedes dieser Paare z_ij≤−0,000267 erfüllt. Andernfalls HOLD.

Die Abschlusstests enthalten immer die Daten beider Stufen. Eine bereits geprüfte Beziehung wird nicht erneut geöffnet. Der Algorithmus verlangt im zweiten Feldblock exakt die ausgewählten IDs und die **inkrementellen** Versuche. Die erste Entscheidung, ihre Zählungen und der Auswahlplan müssen vor jeder Nachmessung unveränderlich festgehalten werden. Selektive Änderungen der Zellmittel zwischen den beiden Stufen fallen außerhalb des Modells.

## 3. Weshalb die datenabhängige Auswahl die Risikogarantie erhält

Für den Beweis denken wir für jede Zelle vorab n₂ zulässige Zufallsversuche. Die im Feld ausgelassenen Daten werden im Beweis ausschließlich als potentielle Beobachtungen verwendet. Jedes bis zur zweiten Stufe offene Paar hat tatsächlich beide komplette Stichproben. Schreibe U(n,u) für die gerichtete v0.6-Schranke für eine einseitige zentrierte Abweichung eines beliebigen Paarvergleichs (in Quoten) um mindestens u>0. Sie gilt für beide Vorzeichen und alle Zellmittel. Die implementierte Rechnung umfasst 100 Varianzbereiche und nach außen gerundete rationale Schranken. [Herleitung und Zertifikat der Vorstudie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/169).

Fixiere in einer unsicheren Anlage ein einziges Paar mit wahrem positivem Abstand. Wird die Anlage freigegeben, muss **dieses** Paar entweder schon in Stufe 1 die negative Freigabeschwelle unterschritten oder erreicht haben, oder es war offen und hat die Abschlussschwelle bestanden. Ein frühes HOLD kann nie zu GO führen. Das zweite Ereignis liegt im unbedingten Ereignis, dass das potentielle vollständige Paar bei n₂ bestanden hätte. Damit ist keine bedingte Verteilungsannahme nach Auswahl und keine Unabhängigkeit der zwei Blicke nötig. Die Vereinigungsabschätzung ergibt

    P(Fehlfreigabe) ≤ U(n₁,0,000369)+U(n₂,0,000267)
                    ≤ 0,003791892909 + 0,005961782889 = 0,009753675798.

Ein unionsartiger physischer Nullfall wird durch das Bestehen aller erforderlichen Einzelbeziehungen geprüft. Die Rechnung mit einem festen ungünstigen Paar ist mit dem klassischen Intersection–Union-Prinzip verwandt. [Berger und Hsu, Statistical Science 11 (1996)](https://www.public.asu.edu/~rlberge1/papers/statsci96.pdf).

In der günstigen Klasse kann HOLD nur aus dem frühen HOLD oder einem nicht bestandenen potentiellen Endvergleich unter allen 240 Paaren entstehen. Mit der in v0.7 bewiesenen Grenze A(n,t) für P(max z_ij≥−t) folgt

    P(HOLD) ≤ A(n₁,−0,000020)+A(n₂,0,000267)
            ≤ 0,000009328352 + 0,002521651872 = 0,002530980224.

Beide Schranken sind kleiner als die Werte 0,009826212273 und 0,002531676912 in v0.7. Diese Gegenüberstellung vergleicht die **Garantien**. Die tatsächlichen Fehlfreigaben in einer bestimmten Anlage können in beide Richtungen abweichen. Für identische Stufengrößen und Schwellen gilt im gemeinsamen potentiellen Datensatz: Eine Freigabe bei erneuter Abschlussprüfung aller 240 Paare führt auch zur Freigabe bei Abschlussprüfung der noch offenen Paare. Die Umkehr kann scheitern. Die Zahlen im Pilot quantifizieren diese Unterschiede separat.

## 4. Wie viele Endpunkte zu erwarten sind

Sei M die **tatsächlich nachgemessene** Zellenzahl, also null bei frühem GO oder HOLD. Pfadweise ist B=16 n₁+(n₂−n₁)M der gesamte Referenzaufwand. Bei Fortsetzung kann M jeden im jeweiligen Graphen möglichen Wert von 2 bis 16 einnehmen. Beispielsweise können acht hohe und acht niedrige Zellen sämtlich offene Kreuzbeziehungen besitzen. Der Höchstaufwand ist deshalb weiterhin 736.000.000. Die erste Stufe kostet 432.000.000 Versuche.

Für eine uniforme obere Erwartungsschranke teilen wir die wahren p_i bei m(1+r)/2 in k obere und l=16−k untere Zellen ein. Das Verfahren benötigt die wahren Gruppen nicht. Setze g=P(L−1), w=P(r−1), t₁=0,000369. Für ein einzelnes beim ersten Blick noch nicht freigegebenes gerichtetes Paar sind die folgenden Wahrscheinlichkeitsschranken zulässig.

| Richtung | Untere Schranke für L p_j−p_i | Obere Schranke für P(Paar offen vor globalem HOLD) |
|---|---:|---:|
| obere Zelle i → untere j | g−w | a=U(n₁,g−w−t₁) |
| beide in derselben Hälfte | g−w/2 | b=U(n₁,g−w/2−t₁) |
| untere Zelle i → obere j | g | c=U(n₁,g−t₁) |

Die Lücken folgen aus p_i−p_j≤m(r−1), m(r−1)/2 bzw. 0 sowie m≥P. Alle in U eingesetzten Abstände sind positiv. Eine obere Zelle muss nur nachgemessen werden, wenn mindestens eine ihrer **eingehenden oder ausgehenden** Beziehungen offen ist. Ihre Auswahlwahrscheinlichkeit ist daher höchstens min(1,2(k−1)b+l(a+c)). Analog ist eine untere Zelle mit Wahrscheinlichkeit höchstens min(1,2(l−1)b+k(a+c)) ausgewählt. Ein globales frühes HOLD kann diese Zahlen nur verkleinern. Für eine leere Gruppe entfällt der betreffende Summand.

    E[M] ≤ max über k=0,…,16 von
           k min(1,2(k−1)b+l(a+c)) + l min(1,2(l−1)b+k(a+c))
         ≤ 2,567683746784.

Es werden Indikatorerwartungen addiert. Überlappende Beziehungen müssen nicht unabhängig sein. Das numerische Maximum fällt bei k=8 an. Alle 17 Einschließungen stehen im maschinenlesbaren Zertifikat. Diese Schranke gilt über **alle** Wiederholungen eines festen günstigen Profils, nicht bedingt auf CONTINUE. Multiplizieren mit 19 Millionen und Aufrunden liefert

    E[B] ≤ 480.785.992 Referenzversuche.

Da jeder gültige v0.7-Durchlauf bereits für Stufe 1 mindestens 528 Millionen benötigt, gilt für jedes günstige Profil E[B₈]/E[B₇] ≤ 480.785.992/528.000.000. Die tatsächliche mittlere Einsparung ist damit mindestens **8,94 %**. Die publizierte obere Erwartungsschranke von v0.7 (575.174.011) wird um **16,41 %** gesenkt. Diese beiden Prozentsätze haben verschiedene Nenner. Ein einzelner v0.8-Durchlauf kann teurer sein als sein gepaartes v0.7-Gegenstück.

Hat ein bestimmtes Paar sogar p_i−L p_j≥0,0002, so ist die Wahrscheinlichkeit, dass früh HOLD erfolgt, mindestens 1−U(n₁,0,0002−0,000020)≥0,872819684371. Die Verwendung von M≤16 bei ausgebliebenem frühen HOLD liefert E[B]≤470.662.816 für diese Zusatzklasse. Der Abstand ist keine Folge eines beliebigen K(f)>K*. Die adaptiven Informationsuntergrenzen für mindestens ein schwieriges günstiges Profil aus v0.7 bleiben anwendbar, da das neue Verfahren begrenzt viele Versuche nutzt und seine Zellwahl von bereits erhobenen Daten abhängt. Ein optimaler Messplan ist weiterhin offen.

## 5. Gegenbeispiel zur Wahl nur des Minimums und Maximums

Die erste Stufe liefert 13.492.000 Treffer in C01, 13.508.500 in C02, 13.507.000 in C03 und je 13.500.000 in C04 bis C16. Am ersten Blick sind genau C02→C01 und C03→C01 offen. C01 ist das Minimum und C02 das Maximum. In beiden Fortsetzungen haben C01 und C02 je 9.500.000 zusätzliche Treffer. In Fortsetzung A hat C03 ebenfalls 9.500.000 zusätzliche Treffer, in B dagegen 9.520.000. Bei übereinstimmenden Messwerten der zwei Extremzellen liefert die v0.8-Regel in A GO und in B HOLD. Beide Datensätze benötigen 489 Millionen Versuche. Die Eingaben sind unter examples/ ausführbar. Die Beobachtung allein der beiden Extremzellen kann diese Entscheidungen nicht reproduzieren. Eine grundsätzlich andere Regel mit eigenen Fehlergrenzen wird dadurch nicht ausgeschlossen.

## 6. Geometrie und Anwendungsgrenze

Nach GO folgt das unveränderte v0.4-Verfahren für einen vollständigen vierdimensionalen Kausaldiamanten, 3,2 Millionen unabhängige wissenschaftliche Ereignisse, 400.000 disjunkte Achtergruppen und 11.200.000 Vergleichbarkeitsabfragen. Die Rasterpunkte sind h∈{0,1/4,1/2}. Für die kontinuierliche Familie ist q=RT²=48 atanh(h/2)² mit 0≤h≤1/2. Bei HOLD bleiben alle drei Modelle und das volle q-Intervall enthalten. Bei CONTINUE wird kein Krümmungsergebnis ausgegeben.

Für K(f)≤K* kann bei HOLD keine Fehlüberdeckung entstehen. Für K(f)>K* kann eine Fehlüberdeckung nur bei einer Fehlfreigabe entstehen. Daher bleibt die Überdeckung bei mindestens 0,951569406 über alle abgeschlossenen Wiederholungen einschließlich HOLD. Bei einem wahren Rasterpunkt in der günstigen Klasse ergibt die Trennung der Datenquellen P(richtige Einzelausgabe) ≥ (1−0,002530980224) · 0,803252245 ≥ 0,801219229453. Die Werte sind nicht bedingt auf einen bereits beobachteten GO-Fall. Die günstigen Nachweisraten allein belegen die externen Kontrastgrenzen nicht.

Quellen der Modellannahmen, übernommenen Berechnung und gestoppten Informationsuntergrenze: [v0.4, Geometrie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/167) · [v0.5, Kalibriermodell](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/168) · [v0.6, Varianzschranken](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/169) · [v0.7, zwei Messstände](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/170).
