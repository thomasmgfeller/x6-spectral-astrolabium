# CST-DUST · Welche N11-Auslese respektiert die Skalarverschiebung?

**Etappe 5A · v0.3 · 19. November 2026.** Die masselose N11-Skalarwirkung erhält eine gemeinsame lineare Ladung. Die aus PR 318 bekannten zwei Vakuumbedingungen werden durch die skalaren Randconstraints und diese Erhaltung allein nicht ausgewählt. Fordert man zusätzlich, dass ein Messinstrument unter einer konstanten Skalarverschiebung invariant ist, so ist ein eindeutiger Treffer an jedem einzelnen Paar der drei benannten Randmoden ausgeschlossen. Auf allen drei reduzierten Moden zusammen ist für das zentrierte Eingangspaket eine optimale, in beiden Zweigen gleiche Trefferwahrscheinlichkeit von **98,6776103253 %** möglich. Sie bezieht sich auf einen normierten Einzelzweig. Die vollständige Bilanz für den Staubversuch steht in Abschnitt 5.

## 1. Eine von beiden Ordnungen transportierte Ladung

C0 ist die N11-Kette mit drei vergleichbaren inneren Paaren, C1 hat eines. Der Nachlauf rekonstruiert die zwei symplektischen Karten R₀,R₁ aus den vergleichbaren Paaren und den Skalar-Hessematrizen. Er benutzt den in PR 293 begründeten, für C0 zusätzlich gewählten gemeinsamen kanonischen Quotienten. In dimensionslosen Paaren z=(x,p) mit x=√β q und p=√β π gilt [xᵢ,pⱼ]=iδᵢⱼ. J ist die zugehörige symplektische Matrix mit oberem rechten Einheitsblock. Die Indizes der reduzierten Ausgangsmoden sind 7, 8 und 9.

Für beide vollen elfdimensionalen Hessematrizen gilt Hc·1=0. Die Wirkung bleibt unter xᵢ→xᵢ+t für sämtliche Knoten bei unveränderten Impulsen invariant. Die ursprünglichen linearen Randconstraints A₋, A₊ sind ebenfalls invariant. Beide N11-Geometrien erfüllen ihre Randbedingungen für die gesamte verschobene Familie. Beim Zurückkehren auf die Sektionen x₀=0 bzw. x₁₀=0 erhält die Translation die folgenden reduzierten Richtungen:

    w₋ = (7/23, 15/23, 1, −241/46, −119/46, 116/23)ᵀ
    w₊ = (1, 15/23, 7/23, −116/23, 119/46, 241/46)ᵀ.

R₀w₋=R₁w₋=w₊. Die Generatoren sind Q₋=w₋ᵀJ z₋ und Q₊=w₊ᵀJ z₊. Sie stimmen mit dem auf die Sektion eingeschränkten Gesamtimpuls der vier Randknoten überein. Für die metaplektischen Zweigoperatoren folgt Vc† Q₊ Vc=Q₋. Der exakte Rang von R₁−R₀ ist fünf. Damit ist die Ladung bis auf einen Faktor die einzige lineare Ausgangsgrösse, deren Zurückziehung für beide Karten übereinstimmt. Höhere oder nichtlineare Erhaltungsgrössen werden durch diese Rangrechnung nicht klassifiziert.

Die starre Verschiebung ist hier eine globale Symmetrie der Wirkung. Die zusätzliche Instrumentbedingung [F,exp(itQ₊)]=0 für jeden reellen Wert t beschreibt eine Auslese ohne äussere Referenz für den Skalarfeldnullpunkt. Weder Q=0 noch eine Identifikation aller verschobenen Zustände wird der Theorie auferlegt. Ein Präparationsapparat mit eigener Feldreferenz beschreibt einen anderen Versuch.

## 2. Weshalb die Vakuumbedingungen nicht aus dieser Symmetrie folgen

Im Instrument von PR 318 werden zwei aus den Moden 7 und 8 gebildete Oszillatoren b₀,b₁ auf Vakuum getestet. Ein Nichtvakuumtreffer im Test gegen C0 zeigt C1 an, ein Treffer im Test gegen C1 zeigt C0 an. Für das kalibrierte Grundpaket sind falsche Treffer exakt ausgeschlossen. Für bⱼ=αⱼz/√Nⱼ und eine Verschiebung t gilt im eigenen Zweig

    bⱼ → bⱼ + t αⱼ w₊ / √Nⱼ,     γⱼ = |αⱼ w₊|²/Nⱼ > 0.

Die Vakuumwahrscheinlichkeit des verschobenen Oszillators ist exp(−t²γⱼ). Alle sechs γ für die drei möglichen Modenpaare sind im Prüfer strikt positiv und rational. Für das feste kalibrierte Paar 7,8 erzeugt bereits t=0,1 falsche Treffer von **1,9752892 % bei C0** und **1,0261460 % bei C1**, jeweils einschliesslich der festgelegten Wahlwahrscheinlichkeit des Tests. Der Parameter t bezeichnet eine dimensionslose Skalarverschiebung. Das verschobene Eingangspaket erfüllt denselben linearen Randconstraint und hat dieselbe Verteilung der Ladung Q₋. Diese Bedingungen können das unverschobene Paket oder den ganzen fehlerfreien Unterraum aus v0.2 daher nicht erzwingen.

**Ausschluss für alle invarianten Effekte auf einem benannten Modenpaar.** Die Zweimodenmarginale einer der reinen dreimodigen Gaußfunktionen hat einen reinen Vakuummodus bⱼ und einen treuen thermischen Modus. Der Prüfer verifiziert für jede Marginale die symplektischen Eigenwerte 1/2 und ν>1/2. Der letztere ist der symplektische Eigenwert der ausgelassenen Mode. Deshalb ist der Träger in diesen Koordinaten |0⟩⊗H. Ein positiver Effekt mit verschwindender Wahrscheinlichkeit im betreffenden Zweig muss diesen gesamten Träger vernichten. Ein verschiebungsinvarianter Effekt muss auch sämtliche verschobenen Träger vernichten. Die Verschiebung wirkt auf bⱼ mit einer von null verschiedenen komplexen Amplitude. Die Träger enthalten damit |tα⟩⊗H für jedes reelle t, α≠0. Solche kohärenten Einmodenzustände haben dichten linearen Aufspann: Das Bargmann-Überlapp eines orthogonalen Vektors ist eine ganze Funktion und verschwindet auf einer Geraden, also identisch. Der Effekt ist folglich null. Der Beweis gilt in beiden Erkennungsrichtungen, auch für nichtgaußsche positive Effekte. Der Zugriff ist auf eines der drei benannten Modenpaare beschränkt; räumliche Lokalität auf dem unreduzierten Kragen wird nicht unterstellt.

## 3. Konstruktiver Ausweg mit allen drei reduzierten Moden

Die Spektraldarstellung von Q₊ zerlegt den Ausgang nach seinem kontinuierlichen Ladungswert u. Ein invarianter Effekt wirkt getrennt auf den Ladungsfasern. Beide normierten Zweige haben dieselbe Ladungsdichte p(u), eine zentrierte Normalverteilung mit Varianz v=64639/2116. In jeder Faser verbleiben zwei reine normierte Gaußzustände φ₀(u), φ₁(u). Ihre Überlappbeträge haben die Form

    |s(u)| = h exp(−g u²/2),     0<h<1,  g>0.

Eine unabhängige Ladungsmessung allein kann die Zweige folglich nicht unterscheiden. Die unterscheidende Information steckt in den beiden verbleibenden Moden bei gegebener Ladung. Die optimale symmetrische eindeutige Zustandsunterscheidung in jeder Faser hat Trefferwahrscheinlichkeit 1−|s(u)|. Der Beweis folgt aus der Positivität der Gram-Matrix nach Abzug der eindeutigen Effekte. Gleiche Erfolgswahrscheinlichkeiten bis zu ihrer kleinsten Eigenzahl sind mit den reziproken Vektoren im Zweigaufspann erreichbar. Allgemein ist auch das arithmetische Mittel der beiden Fehlwahrscheinlichkeiten mindestens |s(u)|. Die punktweise symmetrische Wahl erreicht deshalb das Optimum bei gleicher **gesamter** Zweigeffizienz. Die faserweise konstruierten begrenzten Effekte bilden zusammen ein invariantes Dreiausgangsinstrument mit einem unentschiedenen Ergebnis.

    η = 1 − ∫p(u)|s(u)| du = 1 − h/√(1+vg).

Die Rechnung liefert die rationale Einschliessung **0,986776103253 ≤ η ≤ 0,986776103254**. Der bedingte Wert bei u=0 liegt bei 95,99446645 %. Er bezieht sich auf die stetige Ladungsfaser. Ein einzelner scharfer Ladungswert besitzt im normalisierten Paket Wahrscheinlichkeit null. Lässt man die Invarianzforderung für das Instrument weg, beträgt die optimale Dreimodeneffizienz aus PR 318 rund 99,18507672 %. Alle Werte in diesem Abschnitt setzen das kalibrierte zentrierte Paket und die bisherige skalare Paarung voraus. Der Aufbau ist ein mathematischer Effekt mit idealem Ladungszugriff. Die Genauigkeit einer Apparatur mit endlicher Auflösung wurde nicht berechnet.

**Zwei unabhängige Rechnungen.** In der ersten wird Q als erste Koordinate eines explizit symplektischen Randkoordinatenwechsels gewählt. Aus den bedingten Gaußkovarianzen C₀,C₁ der verbleibenden Moden und ihren Mittelwerten k₀u,k₁u folgt

    h⁴ = 1/det(C₀+C₁),     g = (k₀−k₁)ᵀ(C₀+C₁)⁻¹(k₀−k₁)/2.

In der zweiten wird die Kreuzcharakteristik ⟨ψ₀|exp(itQ)|ψ₁⟩ direkt in den ursprünglichen Ortsdarstellungen berechnet. Sie ergibt s exp(−κt²/2) mit komplexem κ und s=⟨ψ₀,ψ₁⟩. Für Q=aᵀx+bᵀp und d=ia−Ω₁b gilt

    κ = bᵀΩ₁b − iaᵀb − dᵀ(conj(Ω₀)+Ω₁)⁻¹d.

Die Fouriertransformation liefert p(u)s(u) einschliesslich Phase. Die Identitäten h⁴=|s|⁴v²/|κ|² und g=Re(1/κ)−1/v stimmen rational mit der ersten Rechnung überein. Numerisch ist κ≈0,48018239+1,16969446i. Eine direkte Ladungsquadratur bestätigt das integrierte Ergebnis. Die angegebene Schranke für η stammt aus einem Ganzzahl-Wurzeltest am exakten rationalen (1−η)⁴.

## 4. Welche Auswahl der Randpaarung bleibt offen?

Im übernommenen skalaren Schrödingerraum sind die Zweigkarten unitär. Für jede reelle, beschränkte Funktion f mit positiver Untergrenze sind auch die Paarungen ⟨·,f(Q₋)·⟩ und ⟨·,f(Q₊)·⟩ positiv, verschiebungsinvariant und erfüllen Vc† f(Q₊) Vc=f(Q₋) für beide Zweige. Ladungserhaltung und gemeinsamer unitärer Zweigtransport allein zeichnen das bisherige Produkt also nicht aus. Zusätzliche Bedingungen, etwa an die ganze kanonische Observablenalgebra, können die Freiheit einschränken.

Ein expliziter Vergleich hält die koordinatenförmige Präparationsfunktion und die faserweisen Effekte fest und normiert den Zustand im jeweils gewählten Produkt. Für f(u)=1+½ cos(u/√v) wird die gemessene Ladungsdichte proportional zu f(u)p(u). Daraus folgen rund **98,50489694 %** optimale gleiche Trefferwahrscheinlichkeit, gegenüber **98,67761033 %** im Standardprodukt. Die analytischen Gaußintegrale wurden gegen unabhängige Quadratur geprüft. Bei gleichzeitiger isometrischer Mitführung des Zustands und aller Observablen durch f(Q)¹ᐟ² sind die Darstellungen äquivalent. Der Zahlenunterschied konkretisiert daher die zusätzlich benötigte Festlegung der Präparation relativ zur Paarung.

**Ein stärkerer Versuch, eine Präparation auszuwählen.** Fordert man ausdrücklich, dass beide Zweige denselben vollständigen skalaren Ausgangsdichteoperator liefern, müsste der normalisierte Eingangszustand unter dem relativen metaplektischen Operator V₀†V₁ invariant sein. Für T=R₀⁻¹R₁ ergibt sich das charakteristische Polynom

    (z−1)² (53888000z⁴ − 1322948967z³ + 2814038669z² − 1322948967z + 53888000) / 53888000.

Zusätzlich zum doppelten Eigenwert 1 mit nur einem Eigenvektor liegen vier einfache reelle Wurzeln in (0,044;0,045), (0,608;0,609), (1,643;1,644) und (22,252;22,253). Exakte Wurzelzählung prüft alle vier Intervalle. Auf einer kontrahierenden Weyl-Richtung würde Invarianz die stetige Charakteristik eines normalen Zustands für jede Verschiebung auf derselben Geraden gleich ihrem Wert 1 am Ursprung setzen. Damit müsste der Zustand im Null-Eigenraum des zugehörigen nichttrivialen linearen Quadraturgenerators liegen. Dieser hat im regulären Schrödingerraum rein kontinuierliches Spektrum und keinen solchen Eigenvektor. Es gibt deshalb keinen normalen Zustand mit identischen vollständigen Zweigausgängen. Die Forderung gleicher Ausgänge ist ein zusätzlich geprüfter Kandidat. Eine einzelne Präparation darf unter den zwei Ordnungen verschiedene Ausgänge erzeugen.

## 5. Rückwirkung und verbleibendes physikalisches Hindernis

Die beiden eindeutigen Effekte vernichten jeweils den falschen Zweig. Ihre unbedingten Wahrscheinlichkeiten sind deshalb η|A₁|² und η|A₀|². Die akzeptierte Gesamtnorm S enthält weiterhin die gesamte komplexe Interferenz. Unentschieden trägt S−η(|A₀|²+|A₁|²), der Randfehlschlag 1−S. Bei der inklusiven Auslese werden diese Ausdrücke punktweise über die kollektiven Uhr- und Dichtemoden integriert. Für den ursprünglichen gekoppelten Dichteversuch liegen die vier Wahrscheinlichkeiten bei beiden Zentren gerundet bei **21,787515 %, 8,458513 %, 0,181692 % und 69,572280 %**.

| Eingriff | Änderung von P(ein Paar)−P(drei Paare), alle Randmoden | Konstante Randmode | Entkoppelte Kontrolle |
|---|---:|---:|---:|
| Dichtezentrum 1/8 auf 1/4 | exakt 0 | −0,00000339325 | exakt 0 für den signierten Kontrast |
| Ein auf zwei Uhrfenster, gleiche mittlere Uhr und Dichte 1/8 | −0,00356630699 | +0,00007953770 | exakt 0 für den signierten Kontrast |

Die inklusive Dichtenull gilt auch einzeln für alle vier Wahrscheinlichkeiten. Die neue Auslese bewahrt die gemeinsame Anfangsdichtephase und dieselbe Uhrmarginale. Der gekoppelte Uhrkontrast nutzt die archivierten Uhrintegrale von PR 317/318. Die rationale Schranke für die skalare Treffereffizienz gilt unabhängig von diesen numerischen Uhrwerten. Für den Uhrkontrast liegt weiterhin keine vollständige Fehlereinschliessung vor.

**Etappe 5A bleibt auf HOLD.** Die gemeinsame Skalarladung, die Ausschlüsse und das invariante Dreimodeninstrument sind für den benannten N11-Quotienten hergeleitet. Der projektierte gemeinsame Raum, die Zustandspräparation relativ zur Ladung und die kollektive Staub-/Uhrpaarung sind physikalisch weiter zu bestimmen. Weder die mathematisch optimale Messung noch die Wahl einer relativen Feldreferenz folgt allein aus der Gesamtwirkung.

## Offline nachrechnen

Python 3 mit SymPy und mpmath genügt. Im entpackten Ordner ausführen.

    python3 -B verify.py

Die Nachrechnung nutzt die in provenance.json mit Commit und SHA-256 belegten Daten. Sie rekonstruiert die kanonischen Karten in einer temporären Kopie, prüft die sechs lokalen Träger, den gemeinsamen Ladungstransport, das globale Faseroptimum und die Wahrscheinlichkeitsbilanzen. Bei den Uhr- und Dichteintegralen werden die publizierten Werte weiterverwendet. Die Eingabeauswahl und die neu geprüften mathematischen Forderungen stehen in contract.json.

[Projektbasis · PR 318](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/318) · [Skalarquotient · PR 293](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/293) · [Gaußzustände und bedingte Kovarianzen · Weedbrook et al.](https://arxiv.org/abs/1110.3234) · [Eindeutige Zustandsunterscheidung · Barnett und Croke](https://arxiv.org/abs/0810.1970) · [Vollständigkeit kohärenter Systeme · Perelomov](https://arxiv.org/abs/math-ph/0210005)
