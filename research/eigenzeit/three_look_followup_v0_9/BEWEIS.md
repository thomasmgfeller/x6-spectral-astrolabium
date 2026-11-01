# Drei Messstände bei gezielter Nachmessung

## 1. Modell und Vorgehen

Die Aussage betrifft dieselbe relative Referenzkalibrierung für einen vollständigen 4D-Kausaldiamanten wie in v0.8. Es gibt 16 vorab definierte Zellen. In jeder Zelle j stehen theoretisch unabhängige markierte Bernoulli-Versuche zum festen Mittel p_j bereit. Auch zwischen den Zellen sind die Versuche unabhängig. Ausfälle gehören in den Nenner. Physische Beprobungsdichte f, Erzeugungsdichte s, Referenzeffizienz e und Transfer t_ext erfüllen f proportional zu s·e·t_ext. Die extern begründeten Kontrastgrenzen sind K(s)≤S, K(t_ext)≤D und eine Variation von e innerhalb jeder Zelle um höchstens Faktor C, mit S=D=C=1,0001. Beide Datenquellen werden von diesen Zusagen abgedeckt. Die Wissenschaftsordnung und ihre Zufallsgruppierung sind von der Referenzkalibrierung unabhängig.

Der physische Zielkontrast ist K*=1,002. Sei L=K*/(SDC²). Für K(f)>K* existiert wegen K(f)≤SDC²·p_max/p_min wenigstens ein festes gerichtetes Paar (i,j), i≠j, mit p_i−L p_j>0. Die günstige Klasse hat m=min p_j≥P=0,49 und p_max/m≤r=1,0002. Der Erwartungswert wird jeweils für ein festes zugelassenes Profil über neue vollständige Wiederholungen gebildet.

Zu Beginn sind alle 240 gerichteten Paare offen. An jedem Blick werden ausschließlich die weiterhin offenen Paare anhand ihrer zwei gleich großen kumulierten Zellstichproben geprüft. Sei z_ij=x_i−L x_j mit empirischen Trefferquoten x. Die Priorität an den ersten beiden Blicken hat ein mögliches HOLD. Danach werden Beziehungen mit z_ij≤−t als geklärt aus dem Test entfernt. Keine entfernte Beziehung oder Zelle wird wieder aufgenommen.

| Blick | Kumuliert pro aktiver Zelle | Inkrement je aktiver Zelle | t zur Paarfreigabe | Frühes HOLD bei mindestens einem offenen Paar |
|---|---:|---:|---:|---|
| 1 | 22 Mio. | 22 Mio. | 0,000430 | z_ij≥+0,000110 |
| 2 | 31 Mio. | 9 Mio. | 0,000386 | z_ij≥+0,000010 |
| 3 | 46 Mio. | 15 Mio. | 0,000267 | Endentscheid |

Sind alle Beziehungen geklärt, endet die Kalibrierung mit GO. Verbleiben vor dem letzten Blick Beziehungen, folgt CONTINUE. Im letzten Blick führt jede verbleibende ungeklärte Beziehung zu HOLD. Nur die Endpunkte der offenen Beziehungen werden nachgemessen. Die Stufen, Schwellen und Markierungen sind vorab festgelegt. Reale Nachweisverweise und zeitlich gesicherte Zwischenstände sind erforderlich.

## 2. Gemeinsame Fehler über drei Blicke

U(n,u) ist die nach außen gerundete v0.6-Obergrenze einer einseitigen zentrierten Abweichung von mindestens u>0 eines fest gewählten gewichteten Zellpaars. A(n,t) ist die v0.7-Schranke für P(max z_ij≥−t) in der günstigen Klasse. Beide werden unverändert aus dem Publikationsarchiv übernommen. Man kann potentielle Folgen aller 46 Millionen Versuche jeder Zelle konstruieren, auch wenn im Feld ein Teil nie erhoben wird. Für jedes weiterhin offene Paar ist die tatsächlich gemessene Folge bis zum aktuellen Blick vollständig.

Ein festes wahres ungünstiges Paar muss für eine Fehlfreigabe an wenigstens einem der drei Blicke irrtümlich geklärt worden sein. Die unbedingte volle Paarstichprobe an diesem Blick genügt zur oberen Abschätzung. Damit gilt

    P(falsches GO) ≤ U(n₁,t₁)+U(n₂,t₂)+U(n₃,t₃)
                  ≤ 0,002440370943 + 0,001320662609 + 0,005961782889
                  = 0,009722816441.

Günstiges HOLD erfordert ein entsprechendes Ereignis am ersten, zweiten oder letzten potentiellen Blick. Die Einbeziehung auch der nicht mehr aktiv gemessenen Paare kann diese Mengen nur vergrößern. Daraus folgt

    P(HOLD | günstiges Profil) ≤ A(n₁,−0,000110)+A(n₂,−0,000010)+A(n₃,0,000267)
                               ≤ 0,000005902432 + 0,000001776176 + 0,002521651872
                               = 0,002529330480.

Die Blicke sind abhängig. Keine dieser Rechnungen setzt Unabhängigkeit der Blickentscheidungen oder der 240 Paare voraus. Beide ausgegebenen Schranken bleiben unter den v0.8-Werten. Bei K(f)≤K* erhält man durch ein HOLD stets den vollen Krümmungsbereich. Bei K(f)>K* setzt jede Fehlüberdeckung ein falsches GO voraus. Die unbedingte Überdeckung einschließlich HOLD bleibt daher mindestens 0,951569406. Für einen wahren Rasterpunkt beim günstigen Profil gilt aufgrund der getrennten Wissenschaftsdaten P(richtige Einzelausgabe)≥(1−0,002529330480)·0,803252245≥0,801220554613. Die Überdeckung ist eine Aussage über alle abgeschlossenen Wiederholungen.

## 3. Bedingte Wahrscheinlichkeit für gemeinsam genutzte Endpunkte

Sei M_l die Anzahl tatsächlich weitergeführter Zellen nach Blick l, einschließlich null für früh beendete Läufe. Jede solche Zelle hat mindestens eine am aktuellen Blick offene inzidente Beziehung. Im Beweis dürfen wir sowohl das bisherige Überleben als auch globale HOLD-Entscheidungen ignorieren und das entsprechende Ereignis am potentiellen festen Blick untersuchen. Die folgende Konditionierung bezieht sich ausschließlich auf diese volle, im Voraus konstruierte Stichprobe.

**Nahe Halbeffizienz.** Für 0,49≤m≤0,60 liegen sämtliche p_j zwischen 0,49 und 0,60012. Deshalb ist v=p_j(1−p_j) in [0,239,0,25]. Für Y=±(x_j−p_j) liefert der Satz von Berry und Esseen

    P(Y≥u) ≤ S_n(u) = min(1, Φ̄(z_min) + 0,56 / √(0,239 n)),
    z_min = u √(n/0,25) für u≥0, sonst u √(n/0,239).

Hier ist Φ̄ der obere Standardnormalverteilungsschwanz. Für eine zentrierte Bernoulli-Variable ist das absolute dritte Moment höchstens die Varianz. Der Satz mit Konstante 0,56 gilt für die unabhängigen Summanden. Eine linke Grenze der Verteilungsfunktion behandelt ein Atom am Schwellenwert. Die Formel ist eine endliche Fehlerschranke. [Shevtsova, Informatics and Applications 7 (2013)](https://www.mathnet.ru/eng/ia252).

Teile die Zellmittel in zwei Hälften des möglichen Bereichs [m,mr], mit k oberen und 16−k unteren Zellen. Bei einer gerade betrachteten Zelle wird ihre Hälfte im Beweis nochmals in vier Teile untergliedert. Schreibe p=m(1+b) und [a_l,a_u] für die relativen Offsets der betrachteten Teilzelle, [b_l,b_u] für die Offsets der Hälfte einer Nachbarzelle. Diese unbekannten Gruppen werden im Test nicht geschätzt. Für das Ereignis einer offenen Beziehung beim aktuellen Klärungsabstand t sind die folgenden positiven unteren Abstände zulässig:

    ausgehend    g_out = 0,49 (L−1+L b_l−a_u)−t
    eingehend    g_in  = 0,49 (L−1+L a_l−b_u)−t.

Gegeben die zentrierte eigene Quote Y=x_i−p_i, muss für eine ausgehende offene Beziehung −(x_j−p_j) > (g_out−Y)/L sein. Für eine eingehende Beziehung wird stattdessen Y=−(x_i−p_i) betrachtet, dann muss x_j−p_j > g_in−L Y sein. Je Richtung ist die entsprechende bedingte Nachbarwahrscheinlichkeit durch S_n((g−wY)/s) begrenzt, mit (w,s)=(1,L) oder (L,1). An einem festen potentiellen Blick bleiben die anderen Zellstichproben beim Konditionieren auf die eigene unabhängig. Deshalb ist die bedingte Wahrscheinlichkeit mindestens eines Treffers in derselben Richtung nach oben begrenzt durch

    F(y)=1−[1−S_n((g_lo−wy)/s)]^a · [1−S_n((g_hi−wy)/s)]^b,

wobei a,b die verbleibenden Nachbarzahlen in den beiden Hälften sind. F ist monoton wachsend. Für feste Schnittstellen z₀<…<z_h liefert partielle Summation mit der einseitigen Schranke für Y

    E[F(Y)] ≤ F(z₀) + Σ_l [F(z_{l+1})−F(z_l)] S_n(z_l) + [1−F(z_h)]S_n(z_h).

Die Formel entsteht durch obere Treppenapproximation der monotonen Funktion; außerhalb der beiden äußersten Schnittpunkte gelten F(z₀) und 1 als obere Werte. Die Rechnung verwendet 201 gleichmäßig angeordnete Schnittpunkte von −0,0005 bis +0,0005. Im Code werden Produkte der Gegenwahrscheinlichkeiten nach unten und Fehlerobergrenzen nach oben gerundet. Die resultierende Treppenfunktion bleibt monoton, was bei jeder Auswertung geprüft wird. Addiere die Schranken beider Richtungen und deckele bei eins. Maximiere innerhalb jeder Hälfte über die vier möglichen Teilzellen. Die Summe über alle Zellen und das Maximum über k=0,…,16 begrenzen E[M_l].

**Höhere Nachweisrate.** Für m≥0,60 darf die Varianz beliebig klein werden. Hier wird ausschließlich die vorherige v0.8-Paarabschätzung verwendet, mit der stärkeren unteren Grenze 0,60 für m. Für die drei Richtungen gelten die Mindestabstände 0,60(L−r), 0,60(L−1−(r−1)/2) und 0,60(L−1). Das Maximum der beiden Klassenabschätzungen ist eine uniforme Schranke. Man kann sie mit der ursprünglichen klassenübergreifenden Paarabschätzung minimieren.

**Rundung.** Für S_n rundet der Rechner das Normalargument nach unten auf ein Hundertstel. Unterhalb −6 setzt er die obere Wahrscheinlichkeit auf eins, oberhalb +6 benutzt er den Wert bei +6. Es gilt 0,398941<1/√(2π)<0,398944. Das Integral von exp(−x²/2) von 0 bis |z| wird rational durch die integrierten Taylor-Polynome von exp(−s) der Grade 81 und 82 eingeschlossen. Deren gerade bzw. ungerade Restgliedvorzeichen gelten für s≥0. Quadratwurzeln, Produkte und die abschließende Kostenrechnung werden in sicheren Richtungen behandelt. Die Hauptzertifizierung benutzt ganze und rationale Zahlen. Alle 17 Gruppensummen je Blick sind maschinenlesbar enthalten.

## 4. Aufwand, Vergleichsplan und Grenzen

Pfadweise gilt B=16·22 Mio.+9 Mio.·M₁+15 Mio.·M₂, mit M₂≤M₁≤16. Für dieselben günstigen Parameter über alle Laufwiederholungen liefert die gerichtete Rechnung

| Plan/Blick | E[weitergeführte Zellen] höchstens |
|---|---:|
| v0.9, nach 22 Mio. je aktiver Zelle | 5,245391984584 |
| v0.9, nach 31 Mio. je aktiver Zelle | 1,297471778352 |
| v0.8, nach 27 Mio. mit derselben verbesserten Rechnung | 1,441258515592 |

Daher gilt **E[B₉]≤418.670.605**. Das veröffentlichte v0.8-Zertifikat gab 480.785.992 an. Bei unveränderter v0.8-Regel liefert die neue Beweismethode schon 459.383.912. Nur der weitere Unterschied ist bei dieser Methode dem anderen Messplan zuzurechnen, auch hier handelt es sich um einen Vergleich von Obergrenzen. Als nachweisbare Verbesserung der tatsächlich erwarteten Kosten gilt für jedes günstige Profil E[B₉]/E[B₈]≤418.670.605/432.000.000. Denn jeder qualifizierte v0.8-Lauf benötigt mindestens seine erste Stufe. Das garantiert **mindestens 3,08 %** mittlere Einsparung. Der Maximalaufwand beträgt weiterhin 736 Millionen. Die Untersuchung bestätigt keine globale Optimalität.

**Kontrolle ohne Mittelblick.** Behalte die erste und letzte v0.9-Regel bei und führe alle zunächst ausgewählten Zellen direkt zu 46 Millionen. Mit exakt denselben potentiellen Messwerten beträgt die Einsparung durch den zusätzlichen Blick in jedem Durchlauf genau 15 Mio.·(M₁−M₂)≥0. GO/HOLD kann sich ändern. Diese Kontrolle ersetzt nicht den Vergleich mit der tatsächlich publizierten v0.8-Regel.

**Getrennt unsichere Profile.** Für ein festes Paar mit p_i−L p_j≥0,0002 ist die Chance einer Fortsetzung nach Blick 1 höchstens U(n₁,0,0002−h₁), mit den positiven HOLD-Schwellen h. Nach Blick 2 ist sie zusätzlich begrenzt durch U(n₁,0,0002+t₁)+U(n₂,0,0002−h₂). Entweder ist das betrachtete Paar früh fälschlich geklärt worden, oder es müsste am zweiten festen Blick den frühen Stopp verpasst haben. Setze für einen weiterlaufenden Block höchstens 16 Zellen an. Dies ergibt für diese Zusatzklasse E[B₉]≤454.435.704. Ein zu großer physischer Kontrast allein begründet den verwendeten Abstand nicht.

## 5. Unabhängige numerische Prüfung

Neben der Prüfung der Normaltafel und der einseitigen Zellgrenzen an Binomialverteilungen wird die erwartete Zahl der potentiell aktiven Endpunkte für feste Testprofile ein zweites Mal berechnet. Bei beobachtetem Eigenzähler c sind beide Richtungen zu einer anderen Zelle mit Zähler k genau dann geklärt, wenn

    ceil((c+nt)/L) ≤ k ≤ floor(Lc−nt).

Die Wahrscheinlichkeit für alle Nachbarn innerhalb dieses Intervalls ist das Produkt der jeweiligen Binomial-Intervallwahrscheinlichkeiten. Summieren über den Eigenzähler mit seiner Binomialmasse und dann über alle Zellen liefert den Erwartungswert für den potentiellen einzelnen Blick ohne vorherige Stopps. Die separate SciPy-Kontrolle schneidet bei fünf Quadratwurzeln der Versuchszahl beiderseits des Mittels ab. Die ausgelassene Masse ist nach Hoeffding gering; die Kontrolle ist numerisch und kein Bestandteil des rationalen Beweises. Zwölf solche Festprofilwerte, 1.230 einseitige Binomialkontrollen, 1.203 Normaltafelprüfungen und eine exakte Enumeration kleiner vollständiger Datenpfade stehen im Prüfprotokoll.

Die ursprüngliche Geometrieregel bleibt auf eine unabhängige Ordnung von 3,2 Millionen Ereignissen beschränkt. Ohne bestätigte Referenz- und Transferzusagen oder bei terminalem HOLD wird die gesamte Modellfamilie ausgegeben. Bei CONTINUE gibt es keine Geometrieentscheidung. Die externe Abdeckung, Ausfallszählung, Unabhängigkeit und Vorabfestlegung müssen für alle drei Stufen gelten. [Geometrie v0.4](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/167) · [Kalibriermodell v0.5](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/168) · [Paartests v0.6](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/169) · [Stoppregel v0.7](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/170) · [Selektive v0.8-Regel](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/171).
