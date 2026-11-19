# CST-DUST · Geometrische N11-Auslese bei unbekannten Randpulsen · v0.5

Ein neutraler Puls am vergangenen Rand konnte in v0.4 am fest kalibrierten Dreimodendetektor eine falsche Zweigmeldung erzeugen. Hier wird der Detektor neu gewählt und danach bei unbekannter Pulsstärke festgehalten. Die Ausgänge sind C0 (drei vergleichbare innere Paare), C1 (ein Paar) und unentschieden. Die Auslese benötigt eine einzige Realisierung des skalaren Ausgangszustands. Alle skalaren Raten beziehen sich auf den normierten jeweiligen Einzelzweig.

| Zugang zu den beiden Pulsstärken | Fehlerfreie Trefferrate in beiden Zweigen |
|---|---:|
| Nur der zweite Puls wirkt, Stärke unbekannt | Mindestens 49,56269034 % |
| Beide wirken, erste Stärke exakt protokolliert | Dieselbe Untergrenze |
| Beide variieren unabhängig in einer offenen Menge, keine Stärke protokolliert | Exakt 0 für jeden festen ladungsinvarianten eindeutigen Detektor |
| Beide Stärken exakt protokolliert | Mindestens 95,994466454 % |

Die positiven Werte sind Garantien der angegebenen Instrumente. Für eine unbekannte Stärke wurde kein globales Optimum über alle Detektoren hergeleitet. Exakt null im dritten Fall bedeutet, dass ein Detektor mit ausgeschlossenen Falschmeldungen immer „unentschieden“ melden muss. Eine Unterscheidung mit zugelassenen Fehlern bleibt möglich.

## 1. Eingangsvertrag und Aufbau der Ladungsfasern

Die zwei normierten N11-Skalarkarten Rⱼ stammen aus der kanonischen Reduktion. Wie in v0.3 und v0.4 wird der gemeinsame Randquotient für C0 und C1 verwendet. Diese Wahl und die Skalar-/Staubproduktpräparation sind physikalische Annahmen. Die neutralen Ortsquellen sind einzeln eichverträglich. In der ursprünglichen Kragenreihenfolge 0,1,2,3 haben sie die Koeffizienten (8,−15,7,0) und (0,1,−2,1). Beide Pulsstärken t₁,t₂ sind dimensionslos. Das Feld erhält beim Puls den Faktor exp[i(t₁ℓ₁+t₂ℓ₂)x]. Es wird die gleiche Skalarpräparation in den verglichenen Staubversuchen benutzt.

Am Rand gilt Q₊Rⱼ=Q₋ in Kovektorschreibweise. Das Instrument darf die Ausgangsladung u spektral auflösen. Positive Effekte kommutieren mit allen globalen Feldverschiebungen und wirken daher getrennt auf fast allen Ladungsfasern. In jeder Faser bleiben zwei kanonische Moden, h̄=1. Die Referenzpräparation gibt dort reine Gaußzustände mit Kovarianz Cⱼ und Mittelwert kⱼu. Die beliebige gemeinsame Ladungsdichte p(u) ist bezüglich du normiert. Die transversalen Zustände sind durch das Referenzpaket und die angegebenen Pulse bestimmt.

Sei T die Ausgangskarte mit Q₊ als erstem Ort, J die Standard-Symplektik und M die beiden reduzierten Quellenzeilen. Die Spalten der transversalen Verschiebungsmatrix Dⱼ sind die vier transversalen Zeilen von −TRⱼJMᵀ. Die Ladungszeile ist exakt null. Der Mittelwert wird kⱼu+Dⱼt. Cⱼ ist das Schurkomplement der Ladungsvarianz im Ausgangsblock. Der Prüfer verifiziert für beide Zweige Reinheit CⱼJ₄Cⱼ=J₄/4, die Ladungsvarianz 64639/2116 und die neutralen Quellen direkt.

## 2. Ein unbekannter Puls lässt einen ungestörten Oszillator übrig

Wir betrachten den Störpuls aus v0.4, also t₁=0, t₂=t beliebig. Um den Zweig j auszuschliessen, setzen wir d=Dⱼ[:,2] (zweite Spalte, mathematische Indizierung). Wähle eine reelle Zeile a ungleich null mit ad=aCⱼJ₄d=0. Setze b=2aCⱼJ₄, A=(a;b) und n=2aCⱼaᵀ. Die zwei Zeilen A/√n bilden ein kanonisches Paar. Der Prüfer verifiziert AJAᵀ=nJ₂, ACⱼAᵀ=nI₂/2 und Ad=0. Die Modenbildung verwendet beide transversalen Moden. Die beiden Testeinstellungen dürfen unterschiedliche kanonische Paare verwenden.

Nach Abzug von Akⱼu/√n steht dieser Oszillator beim betreffenden Zweig im reinen Vakuum, unabhängig von t. Eine Nichtvakuum-Meldung schliesst j daher exakt aus. Der Detektor wählt vor jeder Auslese zufällig eine der zwei Einstellungen. Bei Nichtvakuum meldet er den jeweils anderen Zweig. Sonst meldet er unentschieden. Die Summe der beiden eindeutigen Effekte ist höchstens I, weil sie eine konvexe Mischung von Projektortests bilden. Zufallswahl und Ladungsauflösung sind unabhängig von der tatsächlichen Ordnung. Ein gemeinsamer operativer Zugang zu diesen idealen Modenmessungen wird im Modell vorausgesetzt.

**Überlapp und Garantie.** Für den anderen Zweig c=1−j hat der geprüfte Oszillator die Kovarianz V=AC_cAᵀ/n und relativ zum Vakuum den Mittelwert m=A[(k_c−kⱼ)u+D_c[:,2]t]/√n. Seine Vakuumwahrscheinlichkeit ist

    P(Vakuum | c, Test gegen j, u, t)
       = exp[−mᵀ(V+I/2)⁻¹m/2] / √det(V+I/2).

Die Kovarianz ist positiv und der Exponent nichtpositiv. Setze α_c=1−1/√det(V+I/2). Bei gewähltem Test werden mindestens 98,95967488 % für C0 bzw. 99,29164235 % für C1 richtig erkannt. Die andere Testeinstellung schliesst die tatsächliche Ordnung aus ihrer eigenen Trefferliste aus. Deshalb müssen die Wahlwahrscheinlichkeiten in die Gesamtquote eingehen.

Wähle die Einstellung, die C0 melden kann, mit Wahrscheinlichkeit w₀=α₁/(α₀+α₁)≈0,50083724 und die andere mit w₁=1−w₀. Die garantierte Rate für jeden Zweig ist B=α₀α₁/(α₀+α₁). Exakte Radikalvergleiche ergeben **0,4956269034 < B < 0,4956269035**. Dieses B maximiert die kleinere Garantie innerhalb der beiden zufällig gemischten Projektortests. Beide Exponenten verschwinden bei u=t=0, daher können Ladungspakete nahe null die Garantie beliebig eng erreichen. Die tatsächlichen Effizienzen η₀,η₁ können verschieden sein. Für das Referenz-Ladungspaket N(0,64639/2116) liefert t=1 die Werte 0,49868560 und 0,49828107. Die Nachrechnung integriert beide Quoten auch direkt über u.

## 3. Zwei unabhängige unbekannte Pulse schliessen jede feste eindeutige Auslese aus

Auf der transversalen Faser ergibt die exakte Rechnung

| Zweig | Rang von Dⱼ | Produkt DⱼᵀJ₄Dⱼ | Von null verschiedener 2×2-Minor |
|---|---:|---|---:|
| C0 | 2 | Nullmatrix | 17833/6197120 |
| C1 | 2 | Nullmatrix | −81/368 |

Die beiden Spalten erzeugen also eine zweidimensionale lagrangesche Verschiebungsebene im vierdimensionalen Phasenraum. Eine lineare reelle symplektische Transformation bringt diese Ebene auf die Ebene reiner Impulsverschiebungen. Im zugehörigen Schrödinger-Bild wird die ursprüngliche reine Gaußwellenfunktion zu einem normalisierbaren Gaußpaket ψᵤ(x), das fast überall ungleich null ist. Die gepulsten Strahlen haben dann bis auf Phasen die Wellenfunktionen exp(it·x)ψᵤ(x), nach invertibler linearer Umparametrisierung der beiden Stärken.

**Dichtheit.** Ist f in L²(R²) orthogonal zu allen diesen Funktionen, verschwindet die Fouriertransformierte von f̄ψᵤ. Dieses Produkt ist integrierbar. Wegen des Gaußabfalls ist es nach Multiplikation mit exp(a|x|) für jedes endliche a noch integrierbar (Cauchy-Schwarz). Seine Fouriertransformierte setzt sich als ganze Funktion fort. Schon ihr Verschwinden für t in einer beliebig kleinen offenen Teilmenge von R² erzwingt durch sukzessive eindimensionale Fortsetzung und Fourier-Eindeutigkeit f̄ψᵤ=0. Damit ist f=0. Die gepulsten Strahlen spannen also für jeden Zweig den gesamten transversalen Hilbertraum dicht auf.

**Folge für die Messung.** Ein positiver Effekt, der bei C0 für jede erlaubte Pulskombination nie klickt, muss alle diese C0-Zustände vernichten. Bei einer festen Referenz-Ladungsdichte, die fast überall positiv ist, folgt die Aussage fasernweise aus der Nichtnegativität des Integranden. Eine abzählbare dichte Menge von Pulsstärken liefert zunächst einen gemeinsamen Ausnahmenullsatz. Die starke Stetigkeit der Verschiebungen liefert den Schluss für die ganze offene Menge. Deshalb ist der C1-Effekt null. Durch Rollenwechsel gilt dasselbe für den C0-Effekt. Bei eingeschränktem Ladungsträger gilt der Schluss auf dem besetzten Träger. Der Ausschluss umfasst auch nichtgaußsche Effekte. Er betrifft einen einzelnen Ausgang, exakte Fehlerfreiheit und fehlenden Zugriff auf beide Pulsstärken. Er gilt bereits bei beliebig kleinen zweidimensionalen offenen Unsicherheiten, nicht für eine bloss endliche Liste diskreter Einstellungen.

## 4. Welches Präparationsprotokoll reicht?

**Eine Stärke ist protokolliert.** Ist t₁ bekannt und t₂ weiterhin beliebig, zentriert der jeweilige Vakuumtest auf A(kⱼu+Dⱼ[:,1]t₁)/√n. Beim zu verwerfenden Zweig hebt dies die gesamte bekannte Verschiebung auf. Der unbekannte zweite Puls verschwindet aus der getesteten Mode wegen ADⱼ[:,2]=0. Beim anderen Zweig ändert sich der relative Mittelwert, während die Kovarianz gleich bleibt. Der Überlapp mit dem Vakuum ist somit durch denselben Determinantenfaktor beschränkt. B und die exakte Fehlerfreiheit gelten für alle u,t₁,t₂. Die Apparatur erhält dabei genau einen reellen, zweigunabhängig erzeugten Einstellwert.

**Beide Stärken sind protokolliert.** Für gegebene u und t kann der Empfänger dieselben beiden bedingten Zweigstrahlen unabhängig von der tatsächlichen Ordnung berechnen und den reziproken Dreiausgangstest aus v0.3 auf dieses Paar einstellen. Für Δμ=(k₀−k₁)u+(D₀−D₁)t gilt

    |s(u,t)| = h exp[−Δμᵀ(C₀+C₁)⁻¹Δμ/4],
    h⁴ = 1/det(C₀+C₁),        η₀(u,t)=η₁(u,t)=1−|s(u,t)|.

Der bedingte symmetrische Test gibt nie eine falsche Meldung und erreicht überall mindestens 1−h. Der exakte Vergleich ergibt 0,95994466454 < 1−h < 0,95994466455. Der Wert bei u=t=0 zeigt die Schärfe der gleichmässigen Grenze. Beim Gauß-Referenzpaket und den Pulsstärken (1,−2) beträgt die Trefferrate je Zweig rund 99,95654 %. Der bekannte Puls wird zur Einstellung der zwei Hypothesen verwendet. Ein unbekannter Zweig muss hierfür nicht rückwärts entwickelt werden.

Das Protokoll ist eine Zusatzressource. Ein exakt bekannter Einstellwert unterscheidet sich von einer Schätzung mit kontinuierlichem Restfehler. Zwei in einer offenen Menge verbleibende, nicht aufgelöste Stärken unterliegen weiterhin dem Ausschluss aus Abschnitt 3. Der Beweis betrifft Fehlerfreiheit. Er setzt keine untere Grössenschwelle für eine praktische Fehlerrate.

## 5. Welcher Rückwirkungskontrast überlebt?

Seien η₀,η₁ die Zweigeffizienzen nach Mittelung über dieselbe Skalarpräparation in allen verglichenen Läufen. Beim Einpulsinstrument gilt B ≤ η_c ≤ w_c auch dann, wenn t₁ mitgeführt wird. Ein eindeutiger Effekt vernichtet die jeweils falsche Komponente, sodass der Interferenzterm in diesem Trefferkanal exakt verschwindet. Die eindeutigen Wahrscheinlichkeiten faktorisieren in die jeweiligen rohen Staub-Gewichte und η_c. Die inklusive Antwort auf den Dichtewechsel bleibt null, da sich auf beiden Zweigen bei unveränderter Uhrmarginale nur die gemeinsame Dichtephase ändert. Die folgende Tabelle betrifft den separaten Uhrwechsel vom schmalen zum geteilten Fenster. Der Score ist P(ein Paar)−P(drei Paare).

Die archivierten rohen Gewichtsänderungen sind a≈−0,005806477824 (C1, gekoppelt) und b≈−0,002192378361 (C0, gekoppelt). Die gemeinsame Staubtransferkontrolle benutzt für beide Ordnungen b. Beim zuvor symmetrischen Instrument verschwand der signierte Kontrollwert. Beim neuen Instrument ergibt die Zweigabhängigkeit der Effizienzen einen im Allgemeinen von null verschiedenen Kontrollwert. Wir geben deshalb beide Beiträge und ihre Differenz an.

| Uhrkontrast | Formel | Äussere numerische Grenzen, nach aussen gerundet |
|---|---|---:|
| Gekoppelt | aη₁−bη₀ | [−0,00181178; −0,00177982] |
| Gemeinsamer Staubtransfer | b(η₁−η₀) | [−0,000007752; +0,000011424] |
| Gekoppelt abzüglich Kontrolle | (a−b)η₁ | [−0,00180403; −0,00179124] |

Die Grenzen für die Differenz folgen direkt aus der Formel mit η₁. Bei t₂=1 und dem Referenz-Ladungspaket ist der gekoppelte Wert −0,00179995050, der Kontrollbeitrag +0,00000088686 und die Differenz −0,00180083736. Die Detektorwahl und die Kenntnis der Pulse müssen in beiden Kontrollarmen gleich sein. Der exakte Nachweis betrifft die skalaren Garantien. Die Zahlen für die Uhr bleiben an die publizierte Quadratur gebunden. Eine vollständige Einschliessung ihres numerischen Fehlers steht aus.

**Etappe 5A bleibt auf HOLD.** Die Anzahl der unkontrollierten Eingangsrichtungen entscheidet hier über die Existenz einer exakten geometrischen Auslese. Der Beweis verwendet das gemeinsame N11-Skalarmodell, die genannten Eingangsstrahlen, die idealen Modentests und gegebenenfalls eine zusätzliche Einstellinformation. Welche dieser Präparationen, Messungen und Staub-/Uhrpaarungen aus der vollständigen physikalischen Wirkung hervorgehen, ist offen.

## Offline nachrechnen

Im entpackten Verzeichnis mit Python 3, SymPy 1.14.0 und mpmath 1.3.0 ausführen.

    sha256sum --check SHA256SUMS
    python3 -B verify.py

Das Skript rekonstruiert die Zweigkarten aus den archivierten N11-Ordnungen und berechnet beide Vakuumtests, den Rang der Verschiebungsräume, die scharfen skalaren Untergrenzen der beschriebenen Instrumente und die Kontrollwerte. Der analytische Dichtheitsbeweis steht in Abschnitt 3. provenance.json bezeichnet Commit, Pfad und SHA-256 aller archivierten Eingaben. contract.json nennt den Operations- und Präparationsvertrag. results.json enthält die vollständigen unnormierten Moden, Exponenten und exakten rationalen Daten.

[Ausgangspunkt · PR 320](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/320) · [Gaußzustände und Kovarianzen · Weedbrook et al.](https://arxiv.org/abs/1110.3234) · [Eindeutige Zustandsunterscheidung · Barnett und Croke](https://arxiv.org/abs/0810.1970)
