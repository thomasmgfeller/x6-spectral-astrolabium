# Was ein verschobener Uhrwert am Schnitt tatsächlich misst

**CST-DUST · 25. November 2026 · N15-Typ 2097151 · markierte Dosis 1.** Das Signal aus PR #370 setzt beim dortigen zweiten Gegenpaar voraus, dass die rechte Wirkung eine verschobene Uhr 4 erhält und die spätere Dichtepräparation ihren alten Wert weiterverwendet. Gibt es am Schnitt nur einen weitergereichten Uhrwert und setzen alle offenen Faktoren diesen Wert ein, unterscheiden sich die Ausgangswellen der beiden Klassen bei jeder zulässigen Stellung nur um dieselbe globale Phase. Eine neue Kontrollpräparation entfernt genau diese Abhängigkeit der späteren Dichtefenster. Damit liefert ein Austausch zweier Uhrintervalle einen nachgewiesenen Kontrast, auch wenn die Dichtepräparation keine unverschobene Kopie der laufenden Uhr erhält.

[Ausgangsversuch, PR #370](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/370) · [Definition der beiden Dichteklassen, PR #369](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/369) · [Früherer Transport von Uhrfenstern](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b85390f25644db9c5ca00e23a104a6a02c25bda7/research/rax_cqg/dust_collapse/n15_uhr5_fenstertransport_v0_1)

## 1. Zwei Fortsetzungen derselben Nullstellung

Die innere Ordnung ist 4≺5≺6≺11≺12≺13≺14. Hinter 11 führt die Wirkung noch die Uhren 4, 5, 6 und 11 mit. Uhr 4 hat genau ein verbleibendes Ziel, Ereignis 12 mit Gewicht b=−8. Setze y=Y₄, t=h/√D, D=(15/4)(3/722)^(1/4) und xⱼ=wⱼ/D. Der Wert D stammt aus der unverschobenen Präparation. Beim Übergang von y auf y+t ändert sich der Wirkungskoeffizient von w₁₂ um

    δc(t) = (−8/38) t [2(Y₁₂−y)−t].

Die früher gezählten Terme bleiben in der linken Amplitude. Die anderen Zielkoeffizienten der rechten Wirkung hängen nicht von y ab. Uhren, Tag an 11, Dichtejitter und beide Uhr-5-Lappen stammen aus PR #369. Für das hintere Tripel sind n=(1,9r/16,9(r−1)/8), r=(Y₁₄−Y₁₂)/(Y₁₄−Y₁₃), q(y)=Σ cⱼ(y)nⱼ, Q₀=−5/4 und ε=2⁻¹⁴. Die zwei Klassen verschieben die drei Dichtezentren um ±εQ₀n/q. Die Jitter haben jeweils Halbbreite 2⁻²⁰. Bei demselben übrigen Feldsatz ist q(y+t)=q(y)+δc(t).

| Präparation und Zugriff | Nenner der Dichteverschiebung | Ungerader Anteil der Phase nach dem Puls, vor Abzug der globalen Phase |
| --- | --- | --- |
| Publiziertes Paar, ausschliesslich die Wirkung gepulst | q(y) | DεQ₀ q(y+t)/q(y) |
| Publiziertes Paar, dieselbe Uhr für alle offenen Faktoren | q(y+t) | DεQ₀ |
| Neue Kontrolle, fester Sollwert in der Dichtepräparation | q(ȳ) | DεQ₀ q(y+t)/q(ȳ) |

Der Phasenabstand zwischen hoch und niedrig ist jeweils das Doppelte der letzten Spalte. In der zweiten Zeile kürzt sich der ganze Quotient. Die beiden bedingten Dichteboxen sind Translationen mit gleichem Volumen und Jacobi-Determinante eins, auch nach der Verschiebung. Die Gravitationsphase und die skalare Randwelle sind für beide Klassen identisch. Nach kohärenter Summation gilt deshalb Z_hoch=exp(2iDεQ₀) Z_niedrig, gleichzeitig für alle Arme und Zukunftswerte. Jede klassenblinde kohärente Verarbeitung derselben Uhr vor diesem bedingten rechten Kern erhält die Proportionalität, solange sie auf dem zulässigen Bereich wirkt, alle späteren Selektoren die Ausgangsuhr benutzen und der Vergleich dieselbe Randpaarung erhält. Das folgt durch Linearität auch für Mischungen mehrerer zulässiger Uhrargumente. Ein zusätzliches Gedächtnis, auf das die rechte Präparation getrennt zugreift, verändert die Voraussetzung. In der ersten Zeile arbeitet die Dichteauswahl gerade mit einem solchen festgehaltenen Argument.

## 2. Eine Präparation, die ohne zweite Kopie der Uhr auskommt

Die neue Kontrolle setzt ausschliesslich im Nenner des hinteren Tripels den nominalen Wert ȳ=−7/4+(15/4)/8 ein. Die übrigen Uhren gehen weiterhin mit ihren jeweiligen Werten in q ein. Die tatsächliche Uhr 4 bleibt in der linken und der weiterlaufenden Wirkung dynamisch. Die zustandsabhängigen früheren Dichten werden wie zuvor präpariert. Die späteren neutralen Mittelpunkte und die beiden Momente des weitergereichten Uhr-6-Pulses benötigen y nicht. Deshalb kann ein einziger Uhrwert am Schnitt alle zukünftigen Faktoren versorgen. Die beiden späten Präparationen bleiben mit späteren Uhren korreliert. Ihre autonome Herstellung ist damit nicht hergeleitet.

Für jede Klasse ändert sich im unverschobenen Versuch ein einzelnes Dichtezentrum um höchstens 3,776·10⁻¹¹ in x-Einheiten. Die Totalvariationsdistanz zwischen den alten und neuen **positiven Präparationsmassen** ist kleiner als 0,00005718. Zum Beweis koppelt man die Uhren identisch und vergleicht die drei bedingten uniformen Jitterboxen. Ihre fehlende Überlappungsfraktion ist höchstens die Summe der drei absoluten Zentrumsbewegungen geteilt durch die jeweilige volle Breite. Auf den geprüften Boxen bleiben die Dichten innerhalb der ursprünglichen 1-%-Bänder und beide Klassen auf ihrer jeweiligen Seite der absoluten und relativen Schwelle an 12.

Die neue Kontrolle kann die frühere exakte Gleichheit auf jeder Einzelgeschichte nicht einfach erben. Wenn nur die drei hinteren Dichten zwischen Partnern differieren und deren Differenzen bei festgehaltenen übrigen Feldern von y unabhängig sind, gilt auf jedem offenen y-Intervall

    ∂²ᵧ(S_hoch−S_niedrig) = (8/19) (w₁₂,hoch−w₁₂,niedrig).

Eine überall konstante Phasendifferenz ist in dieser Familie mit einer Dichtedifferenz an 12 unvereinbar. Für die neue Kontrolle wird die Abweichung deshalb ausdrücklich begrenzt. Nach Abzug von ±DεQ₀ ist ihr Betrag im Nullarm pro Klasse kleiner als 4,048·10⁻¹¹ rad. Der unverschobene neutrale Staubanteil hat nach Ausklammern des gemeinsamen frühen Faktors einen Betrag über 0,99999997 relativ zum positiven Paketvolumen. Setzt man diese untere Grenze auf c und die Phasenabweichung auf e, liegt jede normierte Randwelle im Spurabstand höchstens e/(c−e) vom neutralen Strahl. Das folgt durch orthogonale Projektion und die Normuntergrenze c−e. Die Dreiecksungleichung gibt T_passiv≤2e/(c−e) für die beiden Klassen. Mit gleichen Vorchancen ist ihre optimale Trefferquote an diesem unverschobenen, bereits geschlossenen Rand kleiner als **50,00000000405 %**. Die Wirkungsdaten des modifizierten Paares rechtfertigen hier eine Obergrenze. Eine exakte Gleichheit der passiven Ausgänge ist für dieses Paar offen.

## 3. Ein reversibler Test mit demselben Uhrregister

Auf der flachen markierten Uhrkoordinate vertauschen wir das eingehende Intervall I und das gleich breite, disjunkte Intervall I+t durch Translation. Auf der übrigen Achse wirkt die Identität. Halb offene Intervalle legen den Austausch auf ihren Grenzen fest. Die Abbildung ist eine Involution mit Betrag des Jacobi-Faktors eins. Sie ist unitär in der flachen Hilfsnorm. Das Kontrollsignal darf einen Referenzarm vorsehen. Es enthält weder den Dosiswert noch die Dichteklasse oder eine spätere Uhrablesung.

Im Hauptversuch hat I um ȳ die Halbbreite R=(15/4)2⁻²². Wir wählen h=1/32. Der Uhrversatz beträgt rund 0,03203 in Y. Sowohl das Anfangs- als auch das Zielintervall liegt vollständig im breiteren Modellfenster u₄=1/8±1/64. Zum Fensterrand bleiben mehr als 0,00708 in u. Gegenüber den benachbarten Uhren bleibt der kleinste Abstand über 0,4329 in Y. Der ältere Schritt h=1/8 wird als Kontrolle der früheren Wirkungsquelle reproduziert. Für eine tatsächliche Bewegung des Registers reicht er über dieses breite Fenster hinaus. In einem zweiten, noch engeren Versuch wird zunächst für beide Klassen dieselbe untere Hälfte des ursprünglichen schmalen Pakets ausgewählt. Diese Hälfte und die obere werden mit t=R vertauscht. Alle Werte verbleiben im schmalen Paket. Die Trefferquoten dieses zweiten Tests gelten bedingt auf die gemeinsame Vorauswahl.

Sei P die Wahrscheinlichkeit der Projektion auf (|0⟩+i|t⟩)/√2 nach kohärentem Schliessen des Uhrwerts. ΔP=P(Plus|hoch)−P(Plus|niedrig). Die folgende Tabelle gibt nach aussen gerundete Einschlüsse bzw. exakte Nullen. Sie gelten für beide frühen Dichtezentren 1/8 und 1/4 und für das offene siebenkoordinatige Zukunftsfenster aus PR #370.

| Versuch | Publiziertes Paar, nur Wirkung | Publiziertes Paar, gemeinsame Uhr | Kontrolle mit festem Sollwert, gemeinsame Uhr |
| --- | --- | --- | --- |
| Breites Modellfenster, ΔP in 10⁻⁶ | [−1,436183, −1,436044] | 0 | [−1,436223, −1,436003] |
| Zwei benachbarte schmale Pakethälften, ΔP in 10⁻¹¹ | [−4,04386, −4,04348] | 0 | [−4,29661, −3,79075] |

Die feste Zuordnung »Plus bedeutet niedrig« erreicht im breiten Versuch mit der Kontrollpräparation **50,0000718 %** Treffer. Beim kleinen Austausch beträgt der numerisch unabhängig gegengerechnete Unterschied der Pluswahrscheinlichkeiten rund −4,044·10⁻¹¹. Er bleibt auf dem ganzen akzeptierten Bereich im zertifizierten Intervall. Diese Werte sind bedingte Modellwahrscheinlichkeiten mit einer kohärenten Endprojektion. Zweigweise unterscheidbare und vollständig ausgespurte Armmarken löschen den Interferenzterm dieses Detektors.

Auch der bereits publizierte Drei-Stellungs-Schätzer X=(19/8)(Φ₊+Φ₋)/h² wurde bei h=1/32 berechnet. Φ ist das Argument der Überlappung der offenen Randwellen mit dem Nullarm. Für die neue Kontrolle liegt die Anzeige für die niedrige Klasse zwischen 0,1249397390 und 0,1249399184, für die hohe zwischen 0,1250600816 und 0,1250602610. Beide liegen sicher auf unterschiedlichen Seiten von 1/8. Beim Original mit gemeinsam verschobener Auswahl liefern die beiden Klassen exakt dieselbe Anzeige, eingeschlossen zwischen 0,1249999112 und 0,1250000888. Die zugrunde liegenden Dichten der beiden Originalklassen sind dennoch verschieden. Diese Anzeige vergleicht jetzt unterschiedlich bewegte Präparationen. Sie rekonstruiert deren individuelle ursprüngliche Dichte nicht.

## 4. Wo die gewöhnliche Verklebung endet

Solange Uhr 4 am Schnitt als dieselbe Koordinate weitergereicht wird, identifiziert die gewöhnliche Verklebung ihre linke und rechte Belegung. Die Wirkungsfaktoren sind bei gegebenem Uhrargument multiplikativ. Eine Integration anderer Felder kann ein vom Uhrwert abhängiges Gewicht erzeugen. Sie erzeugt vor dem letzten Gebrauch der Uhr keinen Übergang in ein disjunktes Uhrintervall. Mit den Fenstermultiplikatoren P_I, P_J und J=I+t gilt für jeden solchen uhrdiagonalen Operator K exakt P_J K P_I=0. Der vorgeschlagene Austausch U hat dagegen ‖P_J U P_I‖=1 in der flachen Hilfsnorm. Auf normierten Eingangswellen mit Träger I ist ‖(U−K)ψ‖≥1, wenn beide dieselben Ein- und Ausgaberäume besitzen. Dies ist eine Aussage über das im Referenzmodell tatsächlich weitergereichte Argument vor dessen Elimination. Eine kontrollierbare offdiagonale Uhrkopplung aus der vollständigen physikalischen Dynamik steht aus.

Auch eine spätere Bearbeitung nur der bereits geschlossenen äusseren Randwelle kann im breiten Kontrollversuch den aktiven Kontrast nicht deterministisch reproduzieren. Seine garantierte Grösse übersteigt die passive Spurabstandsgrenze um einen Faktor über 17 740. Selbst ein gemeinsames Filter mit ausdrücklich ausgewiesenem Fehlschlag müsste in mindestens einer Klasse mit Wahrscheinlichkeit höchstens **0,005637 %** erfolgreich sein, um diesen Kontrast bedingt auf Erfolg erreichen zu können. Das ist eine Schranke für eine nachträgliche Simulation aus einer einzelnen normierten passiven Randwelle. Sie begrenzt weder die Erfolgsrate der frühen Quelle noch Versuche mit weiteren unabhängigen Eingabekopien.

Zum Beweis hat eine gemeinsame Messung der passiven Zustände mit den drei Ausgängen Erfolg-plus, Erfolg-minus und Fehlschlag einen klassischen Totalvariationsabstand höchstens T_passiv. Bei Erfolgsraten p,q und bedingten Pluswahrscheinlichkeiten a,b ist dieser Abstand mindestens min(p,q)|a−b|. Denn die Dreiecksungleichung auf den beiden Erfolgsausgängen kostet höchstens |p−q|/2, und genau dieser Term kommt vom Fehlschlag hinzu. Also gilt min(p,q)≤T_passiv/|ΔP|. Der Zusammenhang zwischen Spurabstand, Messungen und optimaler Binärunterscheidung ist im Standardresultat von Holevo und Helstrom formuliert. [Watrous, *The Theory of Quantum Information*, Kapitel 3, Satz 3.4](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf)

## 5. Nachrechnung und Geltungsbereich

registertest.py schliesst die ursprünglichen Uhr- und Dichteboxen mit nach aussen gerundeter 256-Bit-Arithmetik ein. Für jede Klasse und jeden Arm wird die gemeinsame globale Phase entfernt. Die Paarung geschieht bei gleichem Zukunftswert, danach wird positiv über diesen integriert. Bei symmetrischen Phasen S₀±g bildet der Prüfer die Differenz als 2i exp(iS₀) g sinc(g) vor der Integration. Bei A und B für Referenz- und Quellarm werden ΔIm(A*B) und Δ(‖A‖²+‖B‖²) separat unter Erhaltung des kleinen Unterschieds berechnet. Die frühe Dichte liefert beiden Armen denselben, von den inneren Feldern unabhängigen Faktor und kürzt sich aus den Wahrscheinlichkeiten. Der Fehler beim Übergang von Feinhistorienmitteln zu Phasen integrierter Überlappungen wird wie in PR #370 durch Rθ³/[6(1−Rθ²/2)] begrenzt, wenn |θ−Eθ|≤Rθ<1.

Die unabhängige Gegenrechnung bewegt im chronologischen Ablauf einen Eintrag im Vier-Uhren-Speicher, baut die drei Dichtezentren für jede Variante neu auf, integriert die Dichtejitter analytisch und rekonstruiert den komplexen Überlappungswert aus vier Ausgangsintensitäten. Zwei Gitter verwenden 6×8 bzw. 10×20 Zukunfts- und innere Uhrpunkte je Lappen. Eine exakte Prüfung an 90 rationalen Fällen kontrolliert die Koeffizienten. Weitere Kontrollen prüfen die Umkehrbarkeit an Intervallgrenzen und die globale Phase für drei verschiedene lineare Zwei-Moden-Operationen.

Die Aussage über die ursprüngliche gemeinsame Uhr ist eine Identität des angegebenen Wirkkerns und seines translationsinvarianten bedingten Masses. Die neue Präparation, der reversible Austausch und die Phasenreferenz sind explizite Elemente eines Hilfsversuchs. Die gewöhnliche Verklebung bestimmt diesen Austausch nicht. Alle 60 archivierten physischen P3-Einträge stehen auf NOT_RUN, die physische Paarung und die unabhängige positive Masseneichung sind offen.

Im entpackten Paket mit Python 3.10 oder neuer ausführen. Die Standardbibliothek genügt.

    python3 -B pruefen.py

ergebnisse.json enthält die Intervallschranken, quadratur.json die unabhängigen Rechnergebnisse und operator.json die Schnittkontrollen. Die zur Nachrechnung benötigten Auszüge aus den Vorstudien stehen in vorstudie/. Herkunft.json nennt die Git-Pfade am Stand b85390f und die SHA-256-Werte.
