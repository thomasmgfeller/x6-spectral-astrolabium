# CST-DUST · Neutrale Randquellen und geometrische Auslese an N11 · v0.4

Im elfpunktigen Modell unterscheiden sich die Ordnungen C0 und C1 durch drei bzw. ein vergleichbares Paar im Inneren. Beide entwickeln dasselbe dreimodige Skalarfeldpaket. Die Auslese aus v0.3 kann die Ordnung aus dem Ausgangsfeld eindeutig erkennen oder „unentschieden“ melden. Hier wird geprüft, welche Skalarprodukte und Präparationen mit einer festgelegten Familie von Randeingriffen verträglich sind.

## 1. Welche Randquellen sind neutral?

Wir verwenden den gemeinsamen kanonischen Quotienten und die zweigweise normierten skalaren Karten aus PR 319. Der dimensionslose Phasenraumvektor z enthält zuerst die drei Orte, dann die drei Impulse. Es gilt [xᵢ,pⱼ]=iδᵢⱼ. Für die uniformen Verschiebungen w₋, w₊ sind Qₛ=wₛᵀJz die Generatoren. Beide symplektischen Karten Rⱼ erfüllen Rⱼw₋=w₊. Die Anwendung des aus C1 gewonnenen Randconstraints auch auf C0 bleibt eine Annahme des gemeinsamen Quotienten.

Eine reine Ortsquelle W(t)=exp(itℓx) am vierpunktigen Kragen muss zwei Tests bestehen. Damit sie auf dem Quotienten definiert ist, muss ℓ die Eichrichtung des Randconstraints vernichten. Für Ladungsneutralität muss die Summe ihrer vier Koeffizienten null sein. Auf beiden Kragen sind diese Bedingungen unabhängig.

| Seite und Knotenreihenfolge | Ortsanteil des Eichflusses | Basis der erlaubten ℓ |
|---|---|---|
| Vergangenheit (0,1,2,3) | (−46,−32,−16,0) | (8,−15,7,0), (0,1,−2,1) |
| Zukunft (7,8,9,10) | (0,16,32,46) | (1,−2,1,0), (0,7,−15,8) |

**Operative Annahme.** Die Quellen sollen auf ihrer jeweiligen Seite für jede reelle Stärke t als reversible Isometrien zulässig sein. Neutralität und Eichverträglichkeit folgen aus den linearen Tests. Die physikalische Verfügbarkeit dieser Quellen ist eine zusätzliche Forderung. Wir klassifizieren Skalarprodukte ⟨ψ,Gₛφ⟩ mit beschränktem positivem Gₛ und beschränkter Inverser. Die Isometriebedingungen betreffen die normierten, surjektiven Skalarzweige V₀,V₁. Die gesamte Geometrie-Staub-Auslese besitzt auch einen Randfehlschlag.

## 2. Vollständige Klassifikation für diesen Vertrag

Auf den Eichschnitten des Archivs werden die Quellen durch zwei vergangene Zeilen M und zwei zukünftige Zeilen N dargestellt. Ist Vⱼ†G₊Vⱼ=G₋, muss G₋ mit jeder neutralen Eingangsphase und jeder entlang eines Zweigs zurückgezogenen Ausgangsphase kommutieren. Die exakte metaplektische Transformation linearer Weyl-Operatoren gibt für die gestapelten Zeilen

    W = [M ; N R₀ ; N R₁],    W w₋ = 0,    Rang W = 5.

Der führende Minor der Ordnung fünf beträgt 2233/134720. Damit ist der Zeilenraum genau die fünfdimensionale Menge aller Kovektoren mit ℓw₋=0. Die eingeschränkte symplektische Form hat Rang vier. Ihre einzige zentrale Richtung ist der Ladungskovektor w₋ᵀJ. Als Gegenprüfung liefert bereits die erste vergangene Quelle m mit T=R₀⁻¹R₁ die Ränge 1,2,3,4,5 für die Zeilen m,mT,…,mT⁴. Beide Zweigisometrien implizieren [G₋,V₀†V₁]=0. Darum ist diese zweite Rechnung eine Aussage über die Verträglichkeit der Metrik. Sie setzt keinen experimentellen Rückwärtslauf einer Historie voraus.

Da jede reelle Quellenstärke zugelassen ist, erzeugt das Weyl-Produkt alle Weyl-Operatoren des Zeilenraums (bis auf eine Phase). In kanonischen Koordinaten mit Q₋ als erster Ortsvariablen enthält dieser Raum Q₋ und beide Weyl-Paare der zwei transversalen Moden. Ein beschränkter Operator, der mit exp(itQ₋) für alle t kommutiert, wirkt getrennt auf den kontinuierlichen Ladungsfasern. Auf jeder Faser wirkt die Schrödinger-Darstellung der zwei vollständigen Weyl-Paare irreduzibel, ihr Kommutant besteht aus Skalaren. Es genügt, zuerst rationale Parameter zu verwenden und die starken stetigen Weyl-Gruppen fortzusetzen, sodass ein gemeinsamer Ausnahmenullsatz genügt. Der Spektralsatz und der Transport durch V₀ liefern somit alle Lösungen

    G₋ = f(Q₋),     G₊ = f(Q₊),     0 < m ≤ f(u) ≤ M < ∞ fast überall.

Umgekehrt erfüllen diese Operatoren sämtliche Quellen- und Zweigbedingungen, weil die Quellen Q erhalten und beide Zweige dieselbe Ladung transportieren. f kann eine beliebige messbare Funktion innerhalb solcher Schranken sein. Bei gleichzeitiger Transformation von Zuständen und Effekten kann eine alternative Darstellung unitär äquivalent sein. Eine Änderung beobachteter Raten verlangt eine spezifizierte Änderung der physikalischen Präparation oder Identifikation über die Darstellungen hinweg.

**Welche Zusatzannahme würde f festlegen?** Die Einzelquelle exp(ij x₃) auf der Vergangenheit steigt auf den Quotienten ab und verschiebt Q₋ um j. Die entsprechende zukünftige Koordinate ist x₇. Ist schon eine dieser einseitigen Familien für jedes reelle j eine reversible Isometrie, muss f unter allen Translationen invariant und somit fast überall konstant sein. Bei nur einer festen Ladungsverschiebung genügt eine periodische Gewichtung. Ein geschlossener Eingriff exp(ij x₇) Vⱼ′ exp(−ij x₃) mit festem Zweig j′ transportiert die Ladung weiterhin und lässt f frei. Das sind unterschiedliche Annahmen über den Zugriff auf ausgetauschte Ladung. Mit einer idealen kanonischen Referenz (X,P) tauscht exp(ij(x₃−X)) entgegengesetzte Ladungen aus. Eine Gesamtmetrik F(Q₋+P) bleibt frei. Ist die Referenzmetrik dagegen unabhängig auf I festgelegt und die Produktmetrik f(Q₋)⊗I verlangt, erzwingt der Austausch für alle j die Konstanz von f. Ein solcher Austauschkontakt ist in der N11-Wirkung bislang nicht ausgezeichnet.

## 3. Wie stark hängt der geometrische Treffer von der Ladungspräparation ab?

Die Ladung u trägt bei beiden Zweigen dieselbe Verteilung. Die Unterscheidung erfolgt auf den beiden übrigen Moden. Auf jeder Faser haben die bei der Referenzpräparation erzeugten reinen Zweigzustände φ₀(u),φ₁(u) den Überlappbetrag sₐ(u)=h exp(−gu²/2). Der Prüfer berechnet h und g aus den rationalen Schurkomplementen der Kovarianzen neu und vergleicht sie mit PR 319. Die Wirkungen der eindeutigen Auslese sind die reziproken Rang-eins-Effekte im jeweiligen Zweigaufspann, ausserhalb dieses Aufspanns auf null fortgesetzt. Bei der Referenzpräparation sind beide Zweige gleich effizient, falsche Treffer sind ausgeschlossen.

Wir lassen jede normierte Ladungsdichte p(u) bezüglich du zu und halten die normierten transversalen Eingangsstrahlen bei jedem u fest. Die entsprechenden reinen Zustände entstehen durch Multiplikation des Referenzpakets mit √(p/p₀) und einer beliebigen gemeinsamen ladungsabhängigen Phase. p₀ ist überall positiv. Die Multiplikation definiert auf diesem Paket einen normalen Zustand, auch wenn der Multiplikator als Operator unbeschränkt ist. Mischungen dieser Präparationen sind zulässig. Dies ist eine Zustandsklasse im festen Skalarprodukt. Es wird keine gemeinsame physikalische Einrichtung zur Präparation aller dieser Zustände vorausgesetzt.

    η[p] = 1 − h ∫ p(u) exp(−g u²/2) du,       1 − h < η[p] < 1.

Beide offenen Grenzen sind scharf. Schmale Gaußdichten um null nähern die untere Grenze an. Ins Unendliche verschobene Gaußdichten nähern die obere Grenze an. Bei festem zweiten Moment m>0 ergibt Jensens Ungleichung η ≤ 1−h exp(−gm/2). Die obere Grenze ist für absolut stetige Dichten strikt, da Gleichheit einen festen Wert von u² verlangen würde. Um sie bei exakt gleichem m anzunähern, dienen zwei gleichgewichtete Gaußpakete mit Varianz ε und Zentren ±√(m−ε). Die untere Grenze bleibt auch bei festem m scharf. Eine zentrierte Gaußmischung mit Gewichten 1−ε und ε sowie Varianzen ε und [m−(1−ε)ε]/ε reicht für hinreichend kleines ε>0.

| Präparation und Kennzahl | Trefferwahrscheinlichkeit je normiertem Skalarzweig |
|---|---:|
| Infimum für freie Ladungsdichte, feste transversale Strahlen | 95,99446645 % |
| Zentriertes Referenzpaket N(0,v) | 98,67761033 % |
| Gleichgewichtete Mischung der Ladungsdichten N(±√(3v/4),v/4) | 99,16142222 % |
| Supremum bei festem zweiten Moment v | 99,93277960 % |

Beide Beispielpräparationen haben exakt Mittelwert null und Varianz v=64639/2116. Für einen Gaußanteil mit Zentrum μ und Varianz a gilt ∫p exp(−gu²/2)=(1+ga)⁻¹ᐟ² exp[−gμ²/(2(1+ga))]. Eine unabhängige numerische Integration reproduziert beide Raten. Die gemeinsame Ladungsverteilung für beide Zweige, die Entkopplung der Skalarpräparation von Staub/Uhr und die festgehaltenen bedingten Strahlen sind für die Übertragung auf das ursprüngliche Experiment wesentlich.

Die inklusive Dichteänderung des signierten geometrischen Scores bleibt exakt null. Die ursprüngliche Dichtevariation erzeugt bei der inklusiven Integration dieselbe Uhrmarginale und nur eine gemeinsame lokale Phase. Für den Uhrwechsel vom schmalen Fenster auf zwei Fenster ergibt sich ΔS=η[p]d, mit S=P(ein Paar)−P(drei Paare) und dem archivierten d≈−0,003614099463. Die offene Spanne für diesen eingesetzten Uhrwert ist (−0,00361409946, −0,00346933550). Die gemeinsame Staubtransferkontrolle ergibt für den signierten Kontrast null. Die exakte skalare Faktorenrechnung ersetzt keine Fehlergrenze für die ursprüngliche numerische Uhrquadratur.

## 4. Gegenprobe am festen Detektor

Auf das zentrierte Referenzeingangspaket wirkt einmal der vergangene Puls exp[i(x₁−2x₂+x₃)]. Dieser Puls kommutiert mit Q₋. Seine vollständige Ladungsverteilung bleibt exakt gleich. Wir prüfen den normierten Zweig C0 mit dem unveränderten reziproken Effekt für C1. Eine C1-Meldung ist hier eine Falschzuordnung.

In der kanonischen Ausgangskarte mit Q₊ als erstem Ort bezeichnen Cⱼ die transversalen bedingten 4×4-Kovarianzen und kⱼu die Mittelwerte. Der Puls verschiebt C0 bei festem u um den transversalen Vektor dₚ. Mit Z=(C₀+C₁)⁻¹ setzen wir A=dₚᵀZdₚ/4, B=dₚᵀ(2C₀)⁻¹dₚ/4 und L=(k₀−k₁)ᵀZdₚ/2. Die Beträge der beiden Überlappe des verschobenen Zustands mit den alten Strahlen sind sₐ(u) exp(−A−Lu) für φ₁ und exp(−B) für φ₀. Das folgt durch Einsetzen der verschobenen Mittelwerte in die Überlappformel für reine Gaußzustände. Für den C1-Effekt mit reziprokem Vektor proportional zu (I−|φ₀⟩⟨φ₀|)φ₁ ergibt die umgekehrte Dreiecksungleichung

    P(falsch | C0,u) ≥ [(1−sₐ)/(1−sₐ²)²] sₐ² |exp(−A−Lu) − exp(−B)|².

Der Prüfer erhält A≈0,036353, B≈1,398589 und L≈0,029799 als exakte Brüche. Auf |u|≤1 ist A+|L|<1/10 und B>1. Dort ist exp(−A−Lu)>9/10, exp(−B)<1/2 und 1/30<sₐ<1/20. Die zentrierte Ladungsdichte hat im Intervall Masse >1/8. Das liefert die konservative, strikt positive Grenze

    P(C1-Meldung | normierter C0-Zweig, Puls) > (1/8)(19/20)(1/30)²(2/5)²
                                                = 19/900000 ≈ 0,00211111 %.

Vor dem Puls beträgt diese Wahrscheinlichkeit exakt null. Die angegebene Grenze ist weder ein Schätzwert der vollständigen Fehlerquote noch eine Untergrenze für jeden denkbaren Detektor. Sie betrifft den konkret festgehaltenen Rang-eins-Effekt am normierten Skalarzweig. Ein neu kalibrierter Effekt wäre ein neues Experiment.

**Etappe 5A bleibt offen (HOLD).** Im N11-Quotienten sind die zulässigen Randmetriken unter den genannten Quellen vollständig bestimmt. Für den bekannten Uhreingriff ist das Vorzeichen innerhalb der beschriebenen Präparationsklasse robust. Für einen physikalischen Rückwirkungsnachweis fehlen die aus der Gesamtwirkung begründete Realisierbarkeit der Quellen, die transversale Präparation und die Staub-/Uhrpaarung.

## Offline nachrechnen

Im entpackten Ordner mit Python 3, SymPy und mpmath ausführen. Geprüft mit SymPy 1.14.0 und mpmath 1.3.0. Die Rechnung benötigt kein Netzwerk.

    python3 -B verify.py
    sha256sum -c SHA256SUMS

Der Prüfer verifiziert die vier archivierten Eingaben, rekonstruiert die beiden Karten aus den N11-Ordnungen und vergleicht die neuen Resultate mit results.json. contract.json hält die getesteten Forderungen fest. provenance.json nennt den vollständigen Git-Commit, Ursprungspfad und SHA-256 jeder übernommenen Datei.

[Ausgangspunkt und Ladungsinstrument · PR 319](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/319) · [Schrödinger-Darstellung und Weyl-Relationen · LMU, Anhang F](https://www.mathematik.uni-muenchen.de/~schotten/GEQ/GEQ.pdf)
