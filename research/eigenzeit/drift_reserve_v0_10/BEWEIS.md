# Kalibrierung mit einer zeitlich verankerten Driftgrenze

## 1. Zielprofil und externe Information

Das Ziel ist der Kontrast K(f) der wissenschaftlichen Beprobungsdichte im vollständigen vierdimensionalen Kausaldiamanten der Vorstudien. K(f) soll höchstens K*=1,002 betragen. Fixiere einen Referenzzustand, der für die Wissenschaftsordnung gelten soll. Die **Zielmittel** p_j sind die Referenznachweiswahrscheinlichkeiten der 16 Zellen in diesem Zustand. Für die Erzeugungsdichte, den Transfer vom Zielzustand zur Wissenschaft und die Variation innerhalb einer Zielzelle sind weiterhin extern belegte Faktoren S=D=C=1,0001 nötig. D bezieht sich hier auf den Transfer des verankerten Zielzustands. Die zusätzliche hier modellierte Abweichung betrifft die Erhebung der Kalibrierversuche gegenüber diesem Zustand. Ihr Betrag muss unabhängig belegt sein.

Mit L=K*/(SDC²) folgt aus K(f)≤SDC²·p_max/p_min: Bei K(f)>K* gibt es ein festes gerichtetes Paar mit z*=p_i−L p_j>0. Die günstige Zielklasse hat p_min≥P=0,49 und p_max/p_min≤r=1,0002. Für sie gilt z*≤−G mit G=P(L−r)>0. Datenquelle und Gruppierung der Wissenschaftsordnung sind von der Kalibrierung unabhängig, bedingt auf den festen Versuchsaufbau.

**Was während der Messung schwanken darf.** Für jede potentielle markierte Gelegenheit h in einer aktiven Zelle j darf die bedingte Trefferwahrscheinlichkeit q_{jh}, gegeben die bisherige Versuchsgeschichte, in folgender Spanne liegen:

    max(0,a_h p_j−ε) ≤ q_{jh} ≤ min(1,a_h p_j+ε).

Die Spanne muss nichtleer sein. Die Chancen werden je Zelle in der vorher vereinbarten Reihenfolge indiziert. Der gemeinsame Faktor a_h liegt in [a,A]=[0,99;1,01]. Dieselbe Faktorfolge gilt für synchron zugeordnete Gelegenheiten aller geprüften Paare. Sie ist extern fixiert oder unabhängig von den Kalibrierzufällen, sodass auf sie konditioniert werden kann. Ihr genauer Wert wird von der Feldregel nicht benötigt. Die **zellabhängige Restabweichung** darf vorhersehbar vom bisherigen Versuch abhängen. Die bedingten Schranken müssen auch bei Kenntnis aller früheren Zähler gelten. Markierte Versuche einschließlich Ausfällen werden vollständig erfasst. Nicht beherrschte gemeinsame Zufallseinflüsse, die diese bedingten Schranken verletzen, sind ausgeschlossen.

Im Hauptentwurf ist ε=20·10⁻⁶ eine absolute Wahrscheinlichkeitsabweichung je Zelle und Gelegenheit, also 0,002 Prozentpunkte. Sie ist weder die relative Änderung gegenüber der vorherigen Quote noch die Unsicherheit eines geschätzten Mittelwertes. Bei konstantem a darf der Rest derselben Zelle zwischen zwei Gelegenheiten um bis zu 40 ppm wechseln. Eine Grenze allein für Schritt-zu-Schritt-Änderungen kann einen dauerhaften Versatz gegenüber dem wissenschaftlichen Ziel nicht ausschließen.

## 2. Vom Driftbereich zum Feldtest

Schreibe b=(1+L)ε. Der erwartete gemessene Paarkontrast darf im Vergleich zum mit dem gemeinsamen Faktor multiplizierten Zielkontrast in beide Richtungen um b verschoben sein. Für einen festen potentiellen Blick ist der Faktor im Mittel der gleiche für i und j. Definiere

    λ = a−2b/G.
    n'_k = 1.000.000 · ceil[n_k/(1.000.000·λ²)].
    t'_k = λ t_k + b,    h'_k = λ h_k − b.

Hier sind n_k,t_k,h_k die veröffentlichten v0.9-Werte. Nur bei λ>0 liefert diese Skalierung einen Messplan. Die Formeln schlagen ein Budget vor. Die tatsächlichen endlichen Fehler werden anschließend für jedes ausgewiesene Budget erneut direkt zertifiziert.

Bei ε=20 ppm gelten kumuliert **29, 41, 61 Millionen** Versuche pro aktiver Zelle. Der erste Block umfasst 29 Millionen, die Zusatzblöcke 12 und 20 Millionen. Ein offenes Paar wird bei beobachtetem z=x_i−Lx_j≤−t'_k geklärt. Ein frühes HOLD hat Priorität, wenn ein noch offenes Paar z≥h'_k erfüllt. Die Schwellen als ungefähre Werte in ppm der Paardifferenz:

| Blick | t' für Klärung bei z≤−t' | h' für HOLD bei z≥h' |
|---|---:|---:|
| 1 | 415,521015 | 56,023347 |
| 2 | 377,098882 | −31,299683 |
| 3 | 273,184476 | verbliebene offene Paare ergeben HOLD |

Beide Schwellen sind im zweiten Blick negativ und klar voneinander getrennt. Gerechnet wird mit rationalen Zahlen. Erst wenn alle gerichteten Paare geklärt sind, endet die Kalibrierung mit GO. Nach CONTINUE werden nur Endpunkte der offenen Beziehungen weiter erhoben. Die Auswertung verlangt externe Nachweisverweise und Driftgrenzen, die mindestens so streng wie der Hauptentwurf sind. Bei unzureichender äußerer Information gibt sie HOLD_ASSUMPTIONS und die volle Geometriefamilie aus.

## 3. Warum auch vorhersehbare Zellabweichungen abgedeckt sind

Im Modell lässt sich jede binäre Beobachtung in chronologischer Reihenfolge durch eine frische, unabhängige Gleichverteilte U_{jh} und den Test U_{jh}≤q_{jh}(Vorgeschichte) erzeugen. Externe Randomisierung der Versuchsregel darf entsprechend mitgeführt werden. Man kann alle U auch für potentiell ausgelassene Gelegenheiten vorab anlegen. Setze l_{jh}=max(0,a_hp_j−ε) und u_{jh}=min(1,a_hp_j+ε). Pfadweise liegt jede beobachtete Bernoulli-Variable zwischen 1{U_{jh}≤l_{jh}} und 1{U_{jh}≤u_{jh}}. Für vollständige potentielle Präfixe kann man ausgelassene q innerhalb ihrer Spanne fortsetzen. Die beiden Randvariablen derselben Gelegenheit sind gekoppelt. Für verschiedene Gelegenheiten und Zellen sind die Randbeobachtungen bei festem Faktorpfad unabhängig.

Damit liegt jede empirische gerichtete Differenz zwischen den Vergleichen „unterer Zähler von i gegen oberen Zähler von j“ und „oberer Zähler von i gegen unteren Zähler von j“. Für ein wahres ungünstiges Paar mit z*>0 beträgt der Erwartungswert des unteren Randvergleichs mindestens −b. Für eine günstige Orientierung mit d≤L p_j−p_i beträgt der Erwartungswert des oberen Randvergleichs höchstens −a d+b. Dabei ist d positiv; das Abschneiden an 0 und 1 verbessert diese einseitigen Schranken. Sie gelten für die unabhängigen Randvariablen, nicht als Behauptung einer Unabhängigkeit der adaptiv gestörten Originaldaten.

Die v0.6-Paarschwanzschranke U(n,v) ist auch für unabhängige, nicht identisch verteilte Bernoulli-Summanden anwendbar. Im Exponential- und Kippungsbeweis treten nur die aufsummierte Varianz nv≤n(1+L²)/4 und die gemeinsamen Gewichtsschranken auf. Unter exponentieller Kippung bleiben die einzelnen Bernoulli unabhängig. Die gekippte Varianz jedes Summanden beträgt mindestens seine ursprüngliche Varianz mal exp(−|θ|L). Die dritte absolute zentrale Momentensumme ist höchstens L mal die gekippte Gesamtvarianz. Der allgemeine Berry–Esseen-Satz liefert damit denselben Faktor 0,56. Deterministische Summanden werden mit Varianz null behandelt. [Originaler Paartest](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/169) · [Shevtsova, Informatics and Applications 7 (2013)](https://www.mathnet.ru/eng/ia252).

Ein festes physisch ungünstiges Paar muss für jede Fehlfreigabe an einem der Blicke die negative Klärungsschwelle erreichen. Selbst nach Selektion sind seine beiden Präfixe bis zu seinem Klärungsblick vollständig erhoben. Die unbedingte Vereinigung über die vollen potentiellen Blicke gibt

    P(falsches GO) ≤ Σ U(n'_k,t'_k−b)
                  ≤ 0,002382396641 + 0,001263848816 + 0,005713792598
                  = 0,009360038055.

Für die günstige Klasse teile die wahren Zielmittel wie in v0.7 am Mittelpunkt von [m,mr] mit m=min p_j. Für die Orientierungen hoch→niedrig, innerhalb einer Hälfte und niedrig→hoch sind die Mindestlücken d=P(L−r), P[L−1−(r−1)/2] und P(L−1). In einem frühen HOLD setzt man U(n',a d−b+h') je Orientierung ein, im letzten HOLD U(n',a d−b−t'). Mit k hohen Zellen gibt es je k(16−k) Paare beider Kreuzrichtungen und insgesamt k(k−1)+(16−k)(15−k) innerhalb der Hälften. Das Maximum über k=0,…,16 und die Summe über die Blicke liefern

    P(HOLD bei günstigem Ziel) ≤ 0,000005156224 + 0,000001480384 + 0,002168812544
                               = 0,002175449152.

Vor der numerischen U-Auswertung werden positive Abstände bis auf 10⁻¹² nach unten gerundet. Sämtliche ausgewiesenen Fehlerterme sind nach oben gerundet. Die Feldgrenzen von v0.9 liegen bei 0,009722816441 und 0,002529330480 im damaligen stationären Modell. Für dieselbe **unveränderte** Regel unter dem neuen 20-ppm-Modell liefert die Rechnung nur Obergrenzen von 0,026560124245 und 0,016351850560. Eine schwächere Obergrenze allein beweist noch keine Verletzung. Die separate Simulationshypothese in Abschnitt 6 prüft dies für ein konkretes unsicheres Profil.

## 4. Messaufwand und Geometrie

Für den Aufwand zählen nur Endpunkte tatsächlich offener Paare. Für jede mögliche ausgehende Beziehung dominiert der obere Randvergleich mit einer oberen Fokuszelle und unteren Nachbarn. Für eingehende Beziehungen sind die Vorzeichen vertauscht. Innerhalb jeweils **einer** Richtung sind die Randbeobachtungen der verschiedenen Nachbarzellen bei fixiertem Fokus-Randzähler unabhängig. Daher ist die in v0.9 bewiesene Integration über den gewichteten Fokuszähler weiterhin zulässig. Ein Konditionieren auf den originalen adaptiven Verlauf wäre hierfür nicht gerechtfertigt.

Für 0,49≤m≤0,59 liegen alle Randwahrscheinlichkeiten bei 20 ppm in [0,48;0,60]. Ihre Einzelvarianzen sind mindestens 0,239 und höchstens 1/4. Für unabhängige, heterogene Summanden gelten die v0.9-Normaleinschließungen für den zentrierten Zähler mit der tatsächlichen mittleren Varianz. Für einen Fokusoffset in [a_l,a_u] und eine Nachbarhälfte in [b_l,b_u], definiert relativ zum wahren m, gehen die Abstände aP(L−1+L b_l−a_u)−b−t' bzw. aP(L−1+L a_l−b_u)−b−t' ein. Der Beweis benutzt weiterhin vier Unterteilungen je Fokushälfte, 201 Integrationsschnittpunkte und die gerichtete Normaltafel. Für m≥0,59 ersetzt der Rechner P durch 0,59 im varianzunabhängigen Paarschwanz und begrenzt je Zelle die Vereinigung der inzidenten Beziehungen. Man nimmt das Maximum der Klassen und darf dann die frühere globale Paarvereinigung zusätzlich zum Abschneiden verwenden. [Originale bedingte Endpunktrechnung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/172).

Die mittleren weiterzuführenden Zellen sind bei günstigem Ziel über **alle** Läufe auf 4,916075006424 bzw. 1,197468053336 begrenzt. Der tatsächlich verbrauchte Aufwand ist 464 Mio. + 12 Mio.·M₁ + 20 Mio.·M₂. Folglich ist E[B]≤**546.942.262**. Das Maximum beträgt 976 Millionen. Die Tabelle in records/certificate.json rechnet die Fehler zusätzlich für hypothetische, vorab gewählte Toleranzen von 0, 5, 50, 100 und 150 ppm aus. Nur 20 ppm sind im Feldprüfer implementiert. Die anderen Budgets sind Sensitivitätsrechnungen und kein nachträgliches Wahlrecht.

Bei GO wertet das unabhängige v0.4-Verfahren 3,2 Millionen wissenschaftliche Ereignisse im vollständigen 4D-Kausaldiamanten aus. Bei HOLD bleibt der ganze Modellbereich enthalten. Überdeckung ≥min(0,951569406,1−0,009360038055)=0,951569406. In der günstigen Klasse ist am wahren Rasterpunkt die Wahrscheinlichkeit der korrekten Einzelausgabe mindestens (1−0,002175449152)·0,803252245≥0,801504810584. Diese Werte gelten über alle vollständigen Wiederholungen einschließlich HOLD. Sie sind keine bedingte Vertrauenswahrscheinlichkeit nach beobachtetem GO.

## 5. Scharfe Grenze der Trennbarkeit im Zählmodell

Setze ε_c = aP(L−r)/[2(1+L)] = 169,564537… ppm. Für ε<ε_c ist der Abstand aG−2b strikt positiv. Jede günstige Anlage hat selbst am ungünstigsten oberen Randvergleich den Mittelwert höchstens −aG+b, jedes physisch unsichere Ziel hat mindestens ein Paar mit unterem Randmittelwert größer als −b. Ein fester Trennwert in der Mitte und die endliche Zahl fester Paare erlauben nach der Bernoulli-Konzentration bei hinreichend großem festem n beliebig kleine beidseitige Fehler. Dieser Existenznachweis liefert keine Optimalität der oben gewählten Stufen.

Für ε>ε_c wähle ε₀ mit ε_c<ε₀≤ε hinreichend nahe an ε_c, damit alle folgenden Wahrscheinlichkeiten zulässig bleiben. Die gemeinsame Faktorfolge sei konstant a. Zwei Zielzellen im günstigen Modell haben Hoch- und Tiefwerte H=Pr und T=P. Im zweiten Modell haben sie H'=H+2ε₀/a und T'=T−2ε₀/a. Damit gilt H'/T'>L. Die anderen 14 Zellen können in beiden Modellen P haben. Wähle die provozierten Trefferwahrscheinlichkeiten q_H=aH+ε₀=aH'−ε₀ und q_T=aT−ε₀=aT'+ε₀ für alle Gelegenheiten gleich und alle übrigen q=aP. Die beiden Welten liefern **exakt dieselben Beobachtungsgesetze**, auch für Entscheidungen mit Abbruch oder Zellwahl. Es genügt die Unterklasse unabhängiger Bernoulli-Daten. Ein externer Nachweis, welcher der zwei Zustände vorliegt, wäre zusätzliche Information.

Damit das zweite Ziel auch physikalisch wirklich unsicher ist, sei auf einem Anteil η>0 der hohen Zelle die Effizienz C mal so groß wie auf ihrem Rest. In der niedrigen Zelle sei sie auf Anteil η um Faktor C kleiner. Die zwei Basiswerte werden durch 1+η(C−1) bzw. 1−η(1−1/C) dividiert, sodass die Zielmittel H',T' exakt gelten. In der hohen Zelle schöpfen Erzeugung und Transfer S und D aus. Dann ist der physische Kontrast mindestens

    S D C² (H'/T') [1−η(1−1/C)] / [1+η(C−1)].

Für genügend kleine η ist dieser Wert strikt größer als K*. In der günstigen Welt reichen zellkonstante Effizienzen und dieselben äußeren Maximalgrenzen. Bei ε₀=180 ppm und η=0,001 beträgt der unsichere Kontrast rund 1,0020860. Beide Welten haben dennoch dieselbe GO-Wahrscheinlichkeit für jede rein zählende Regel. Die Ziele von höchstens 1 % Fehlfreigabe und mindestens 99,7 % Verfügbarkeit sind so nicht zugleich erfüllbar.

Am exakten Rand ε=ε_c ist der Quotient zunächst genau L. Vergrößere H' geringfügig, verkleinere T' entsprechend, lasse η ausreichend klein und passe die beiden beobachteten Wahrscheinlichkeiten auf der unsicheren Seite mit denselben zulässigen Residuen an. Die resultierenden Gesetze beliebig nahe am Grenzgesetz sind tatsächlich unsicher. Für jede beschränkte endliche Versuchszahl konvergieren die Wahrscheinlichkeiten aller Entscheidungsereignisse gegen die des günstigen Grenzgesetzes. Somit fehlt auch hier eine **uniforme** endliche Trennung mit den verlangten Fehlern. Die Aussage betrifft Zielgüte gegen physische Unsicherheit mit nur den festgelegten Zählern und äußeren Schranken; sie schließt andere Referenzinformationen oder direkt gemessene räumliche Effizienzprofile nicht aus.

## 6. Vorab fixierter Fehlfreigabetest

Der Belastungsfall unsafe_mask verwendet ein komplementäres Zielpaar mit Verhältnis L·1,00001, weitere Zellen bei 0,5, seltene Teilgebiete der Masse 0,001 und die obige physische Konstruktion. Die gemeinsame Verstärkung ist 0,99, der hohe Zellrest −20 ppm und der niedrige +20 ppm. Das liegt in der neuen Modellklasse. Schon ein stationärer, gegenläufiger Versatz zum Ziel genügt für diesen Belastungsfall. Ein eigenes Szenario mit wechselnder Verstärkung und vergangenheitsabhängigem Vorzeichen prüft zusätzlich zeitliche Variation.

Für die unveränderte v0.9-Zählregel wird einseitig P(GO)≤0,01 gegen P(GO)>0,01 im Belastungsfall bei α=0,01 getestet. Fälle, Ziel, Schätzung und 12 neue Batches von je 5.000 Wiederholungen stehen im lokalen Freeze. Bei k=992 von 60.000 ist die gerichtete obere Binomialschwanzwahrscheinlichkeit höchstens 10⁻¹⁵. Die unabhängige SciPy-Rechnung ergibt ungefähr 3,72·10⁻⁴⁹. Der numerische Stresstest verwirft die 1-%-Grenze für diese simulierte Anlage. Auf denselben Daten liefert v0.10 356 von 60.000 Freigaben. Das ersetzt die obige, modellweite Fehlerschranke nicht. Es liegen keine realen Zählungen oder gemessenen Gerätedriftgrenzen vor.
