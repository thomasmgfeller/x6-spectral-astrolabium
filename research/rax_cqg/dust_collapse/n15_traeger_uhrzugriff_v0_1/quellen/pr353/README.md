# Welche Gewichte bestimmen die Massenauslese auf Typ 6840?

CST-DUST · 22. November 2026 · explorative Folgestudie zu [PR #352](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/352)

Bei markierter Masse 4 bestimmen die Staubwirkung und die Feldwerte eines gegebenen Historienpaars seine relative Staubphase. Das relative Amplitudengewicht der verborgenen Feinhistorien bleibt unter den bisher geprüften physikalischen Bedingungen unbestimmt. Bereits bei identischen äusseren Gewichten, identischen Uhren und identischen vier Feldgeschichten sind zwei entgegengesetzte Entscheidungen zur Zwei-Prozent-Grenze möglich. Für eine ausdrücklich festgelegte kontinuierliche Referenzpräparation auf dem ganzen Feldbereich lässt sich der Fehler auf weniger als 0,00446 % einschliessen.

| Präparation auf Typ 6840 | Relativer systematischer Massenfehler bei Zentrum 1/8 | Bei Zentrum 1/4 |
|---|---:|---:|
| Archiviertes Historienpaar, Gewichte 7:4 | 3,66157 % | 3,52242 % |
| Vier feste Historien, äussere Gewichte 7:4, innere Präparation A | 3,65800 % | 3,51891 % |
| Dieselben vier Historien und äusseren Gewichte, innere Präparation B | 0,00486 % | 0,00455 % |
| Kontinuierliches, konditioniertes Produktmass über beide vollständigen Lappen | < 0,00446 % | < 0,00430 % |

Die ersten drei Zeilen sind gerundete Werte aus beidseitigen Einschliessungen. Die vierte enthält garantierte Obergrenzen für die bezeichnete Referenzverteilung. Alle Aussagen verwenden die endliche Quellenmessung aus PR #351, einen festen Ordnungstyp, eine gleichphasige äussere Präparation und den gemeinsamen nichtverschwindenden Skalarfaktor. Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.

## Wirkung, Rand und Amplitudengewicht

Die beiden Originalhistorien besitzen verschiedene äussere Uhrwerte und verschiedene kollektive Anfangsdichten innerhalb desselben Dichtefensters. Ein Dichtezentrum gibt keinen scharfen gemeinsamen Randwert vor. In der konditionierten Zeigeramplitude stehen neben exp(iS) das Integrationsmass, die Randwellenfunktion und die Randpaarung. Der Faktor exp(iS) hat bei reeller Staubwirkung Betrag eins. Auf demselben Ordnungstyp kürzt sich die gemeinsame Gravitationsphase. Unter der deklarierten Skalarannahme gilt das auch für den gemeinsamen Skalarfaktor. Ein zusätzliches Präparationsphasengefälle würde die relative Phase verändern.

Bei der hier vorausgesetzten gleichen reellen Eingangsphase liegt die Differenz S₁−S₂ bei −3,141659 rad für das Zentrum 1/8 und bei −3,028734 rad für 1/4. Die Quellmarker sind X₁,₂ = 4(1 ± 0,01·1023/1024). Beide Originalhistorien liegen strikt im positiven, stetigen Teil des Feldmasses. Im ursprünglichen kontinuierlichen Produktmass hat jeder einzelne dieser Punkte Gewicht null. Das Verhältnis 7:4 kennzeichnet ein separat definiertes atomares Hilfsmass. Eine Aussage über wirksame Gewichte im kontinuierlichen Modell braucht Integrale über Bereiche mit positiver Masse.

## Alle positiven Gewichtsverhältnisse beim Originalpaar

Bezeichne die positiven Amplitudengewichte mit p,n. Nach Abzug der idealen Zeigerphase B = λM = 2 hat das komplexe Zeigerprodukt bis auf einen positiven Faktor die Komponenten

    Re = (p²+n²) cos h + 2pn cos θ
    Im = (p²−n²) sin h,
    θ = S₁−S₂, h = B·0,01·1023/1024.

Um den erlaubten Sektor um exp(iB) einzuhalten, muss Re sin τ ≥ |Im| cos τ mit τ = 0,02 B gelten. Der Sektor liegt vollständig im Hauptzweig. Die Arme verschwinden für ungleiche Gewichte nicht. Bei Gleichheit ist ihr positiver Betrag separat geprüft. Für r = max(p/n,n/p) ≥ 1 ist die Bedingung äquivalent zu

    sin(τ−h) r² + 2 sin(τ) cos(θ) r + sin(τ+h) ≥ 0.

Die streng negativen Werte dieses Polynoms verfehlen das Ziel. Bei Zentrum 1/8 reicht der Bereich oberhalb r=1 erst ab r ≈ 2,995698472 wieder ins erlaubte Band. Auch r=1 verfehlt das Ziel. Bei Zentrum 1/4 ist nur das offene Zwischenintervall von ungefähr 1,012578480 bis 2,957303041 ausgeschlossen. An einer exakten Nullstelle ist der zulässige Grenzwert erreicht. Die rationalen Intervalle der Wurzeln stehen in ergebnis.json.

Gleiche Gewichte illustrieren den Hauptzweig. Bei 1/8 ist das um B zurückgedrehte Produkt reell negativ, die Schätzung ergibt (2−π)/λ und der relative Fehler ist π/2 ≈ 157,08 %. Die mittlere normierte Armintensität beträgt dabei nur 0,00009981 oder weniger. Bei 1/4 ist das korrigierte Produkt reell positiv und die Gleichgewichtsschätzung exakt. Bei 4:1 bestehen beide Paare. Der Zeigerwert wird stets vor einer etwaigen Zusatzbedingung auf positive Schätzwerte ausgewertet.

## Gleiche äussere Randbelegung und vier gleiche Historien

An jedem der beiden äusseren Koordinatenpaare des publizierten Zeugen wird die zweite Belegung mit denselben Uhren und mittleren inneren Dichten ergänzt. Damit gibt es bei jedem Dichtezentrum vier Feinhistorien. Alle vier haben in A und B strikt positive Gewichte, dieselben Wirkungsphasen und dieselben vier Marker. Die beiden äusseren Gewichte des positiven Amplitudenmasses sind in beiden Fällen exakt 7/11 und 4/11. In A erhält der archivierte Zeuge innerhalb jeder Randgruppe 1023/1024 ihres Gewichts. In B erhält der erste Zeuge 1/1024, der zweite 1/512. Der jeweilige Rest entfällt auf die mittlere Dichtebelegung. Eine Summe über alle 16 Paare von Phasoren schliesst das komplexe Zeigerprodukt ein. Eine zweite Rechnung baut die normierten Arme direkt auf. Die Randmarginale und die Kenntnis aller vier Wirkungsphasen lassen die verschiedenen Entscheidungen zu. Das Verhältnis 7:4 der beiden äusseren Punkte ist Teil dieser diagnostischen Kontrolle. Die äusseren Zweipunktmasse sind von den im folgenden Abschnitt integrierten kontinuierlichen Fenstern zu unterscheiden.

## Kontinuierliche Referenz auf dem gesamten Feldbereich

Die zusätzliche Rechenannahme ist ein einziges gemeinsam normiertes Referenzmass. Die beiden äusseren Uhrfenster und das kollektive Dichtefenster tragen konstante gleichphasige Randamplitude. Die inneren Uhren und positiven Dichten tragen das flache Produktmass aus der Hilfsrechnung, eingeschränkt auf den vollständigen PR-352-Bereich, mit gemeinsamer Normierung nach dieser Einschränkung. Eine erneute Normierung je Lappen oder fester Randkonfiguration würde eine andere Präparation ergeben. Auf Typ 6840 liegt der gesamte Bereich strikt innerhalb der Kapazität.

Schreibe D=4Δ−δ, Tⱼ=T₃+D uⱼ und wⱼ=M D fⱼ(u)(1+ηqⱼ). Die sieben qⱼ durchlaufen unabhängig [−1,1] und η=1/100. Die Jacobi-Matrix ist in den Uhren- und Dichtevariablen blockdreieckig. Bis auf konstante Faktoren ist ihre Determinante D¹⁴ ∏fⱼ. Die konstanten Faktoren der positiven Dichtekomponente und des Uhrmasses kürzen sich in der Normierung. ∏fⱼ hängt nur von u ab. Die relative Masse jedes Offsetintervalls ergibt sich daher aus dem Integral von D¹⁴. Auf den linken Lappen entfallen 84,79170 % des konditionierten Referenzmasses. Das ist sein Anteil vor Multiplikation mit der Wirkungsphase.

Für feste Uhren und äussere Dichte sind S=S₀+Σaⱼqⱼ und X=M+Σbⱼqⱼ affin. Es gelten bⱼ=Mηfⱼ und aⱼ=−M D η fⱼ Cⱼ/2, mit Cⱼ=1+Σᵢ kᵢⱼ(Yⱼ−Yᵢ)²/19. Die Ganzzahlen kᵢⱼ folgen aus den 0 bis 3 Ereignissen im offenen Intervall. Bedingt auf die festen Variablen verschwinden beide Linearmittel. Die bedingten zweiten Momente sind Σaⱼ²/3 und Σbⱼ²/3. Setze t=λ/2 und A₀=E exp(iS). Für jeden der beiden vom idealen Markerphasenfaktor befreiten Arme gilt

    |A_arm exp(∓itM) − A₀| ≤ ε
    ε ≤ E [ t sqrt(E_q(S−S₀)² · E_q(X−M)²) + t² E_q(X−M)²/2 ].

Dies folgt aus |exp(ix)−1|≤|x|, der Taylorrestschranke |exp(ix)−1−ix|≤x²/2, E_q(X−M)=0 und Cauchy-Schwarz. Die äussere Erwartung läuft über die übrigen Felder. Zur unteren Schranke c für |A₀| wird auf die mittlere Wirkungsrichtung am Zentrum des linken Lappens projiziert. Über 16 Offsetzellen werden die zwei veröffentlichten Wirkungseinschliessungen geschnitten und das projizierte Minimum mit der jeweiligen Zellenmasse gewichtet. Auch negative Projektionsbeiträge gehen ein. Bei c>ε ist die Winkelstörung jedes Arms höchstens ε/(c−ε). Die relative Massenfehlerschranke ist daher 2ε/[B(c−ε)]. Der Hauptzweig bleibt mit dem gesamten Fehlerbudget zulässig.

| Grösse | Zentrum 1/8 | Zentrum 1/4 |
|---|---:|---:|
| Untergrenze c für die normierte Amplitude | > 0,59574 | > 0,61752 |
| Absolute Armstörung ε | < 0,00002654 | < 0,00002654 |
| Relative Massenfehlerschranke | < 0,00446 % | < 0,00430 % |

Die deterministische numerische Gegenrechnung integriert die sieben Jittervariablen analytisch als Produkt von sinc-Faktoren. Eine Halton-Regel mit je 4 096 Punkten pro Lappen integriert die übrigen neun Variablen. Die numerischen Fehlerwerte des Zeigers liegen bei rund 0,000222 % und 0,000216 %. Die garantierten Obergrenzen der Tabelle stammen vollständig aus den rationalen Einschliessungen.

## Wie genau müsste das effektive Gewicht bekannt sein?

Aus den beiden zertifizierten Vollbox-Rechnungen folgt nachträglich eine hinreichende Stabilitätsschranke. Schreibe μ für das normalisierte positive Referenzmass und ν für ein mögliches komplexes effektives Amplitudenmass nach Herausziehen gemeinsamer Faktoren. Beide verwenden denselben zugelassenen Feldbereich, dieselbe Wirkung und denselben Marker X. Die uniforme Schranke |X−M| ≤ Mη gilt auf diesem Bereich. Wenn die Variationsnorm des Unterschieds höchstens d ist, sinkt die Untergrenze für |A₀| höchstens um d. Für die Differenz zwischen einem korrigierten Zeigerarm und A₀ wächst der Rest höchstens um κd mit κ = tMη = 0,01. Das folgt durch Integration des Faktors exp(iS)[exp(±it(X−M))−1], dessen Betrag höchstens κ ist. Insgesamt gilt bei positivem Nenner

    relativer Fehler ≤ 2(ε+κd) / [B(c−d−ε−κd)].

Die Zwei-Prozent-Grenze ist gewahrt, solange d ≤ [τc−(2+τ)ε]/[τ+(2+τ)κ], mit τ=0,02B. Die Rechnung bestätigt d=0,39 gleichzeitig an beiden Dichtezentren. Für zwei normierte positive Masse entspricht dies einer Totalvariationsdistanz sup_E |μ(E)−ν(E)| von höchstens 0,195. Für komplexe Masse ist die volle Variationsnorm gemeint. Diese Bedingung ist hinreichend. Ein grösserer Abstand entscheidet den Massenfehler nicht. Ein physikalischer Abstand wurde hier nicht bestimmt. Die Garantie ist auf dieses Instrument, seinen Träger, Typ 6840 und Masse 4 beschränkt.

## Offene physikalische Eingabe und Reproduktion

Für eine physikalische Vorhersage braucht es bei vorgegebenem Rand die relativen komplexen Amplituden der inneren Dichtebelegungen oder eine unabhängig begründete Schranke dafür, wie sie von einem spezifizierten Referenzmass abweichen. Das kann aus der gekoppelten Zustandspräparation und der physikalischen Paarung folgen. Ein blosses äusseres Lappengewicht legt diese bedingte Verteilung nicht fest. Der Zeiger selbst gehört zum endlichen Hilfsmodell. Die unabhängige Ruhemasse-Eichung mit Vakuum und positivem Standard sowie der dynamische P3-Pilot sind offen.

Der gesamte Prüflauf benötigt Python ab 3.10 mit der Standardbibliothek. Im entpackten Ordner genügt

```sh
python3 -B pruefbericht.py
```

Der Lauf prüft alle Archivdateien, die Git-basierten Quelldigests, die archivierten Historien, beide Schwellenpolynome, die vier gemeinsamen Randkontrollen und beide kontinuierlichen Referenzen. Die lokalen Prüfpläne dokumentieren Hauptlauf und explorative Ergänzung. In ergebnis.json sind Brüche des relativen Fehlers gespeichert. Prozentwerte erhält man durch Multiplikation mit 100. Die byteidentischen Quellen verweisen über herkunft.json auf [den geprüften Stand von main](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/03698ae2940f76486fa8d26b3b017c8703c8d9dc/research/rax_cqg/dust_collapse).
