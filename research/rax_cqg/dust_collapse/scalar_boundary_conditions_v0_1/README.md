# CST-DUST · Welche Randbedingungen folgen aus der skalaren Wirkung?

[Kurzbericht (PDF)](../reports/CST_DUST_Skalare_Randbedingungen.pdf) · [Offline-Prüfpaket (ZIP)](../packages/CST_DUST_Skalare_Randbedingungen_Pruefpaket.zip) · [Ergebnisse (JSON)](ergebnis.json)

18. November 2026 · Exakte Prüfung der 33 AA-Ordnungen nach PR #306

**Ergebnis.** Im gemeinsamen skalaren Ausgangsraum gibt es keinen von null verschiedenen Zustand, der die aus allen fünf rangdefizienten Ordnungen abgeleiteten Impulsbedingungen gleichzeitig stark erfüllt. Das gilt auch für temperierte Distributionen. Für jede dieser Ordnungen einzeln lässt sich das skalare Grundpaketgewicht pro Einheitslänge der ungedämpften Richtung exakt berechnen. Die Wirkungsgleichungen dieser Rechnung bestimmen weder die Paarung verschiedener solcher Ausgänge noch deren Gewicht relativ zum leeren Zweig.

## Unveränderte Ausgangslage

Der Eingangsrand trägt zwei skalare Werte x=(q₀,q₁), der Ausgangsrand zwei Werte y=(q₃,q₄). Das einzige innere Ereignis trägt q₂. Wir verwenden das dimensionslose b=4/√6, den masselosen Skalar, die unveränderten Hesse-Matrizen und den normierten Atom-/Skalargrundeingang der 33er-Kontrollfamilie. Der innere Uhrwert u kann wie in PR #306 erhalten bleiben. Gravitation und Staub multiplizieren die skalare Amplitude einer festen Ordnung mit Faktoren, die von y unabhängig sind. Die folgenden Gleichungen gelten daher bei jedem u. In den Formeln bezeichnet b den Skalar-Wirkungsfaktor. Die Geburtsrate β aus dem P3-Kandidaten ist eine separate Grösse.

PR #306 hat zwei Ausgangsbefunde gesichert. Für ein festes Grundpaket ist das Gewicht pro kleiner Uhrfensterbreite zwischen 0,0239574543165 und 0,0239574543166 eingeschlossen. Die Summe über sämtliche skalaren Ausgänge mit dem bisherigen Randprodukt divergiert auf jedem positiven Uhrfenster. Hier prüfen wir, ob sich die Divergenz durch eine gemeinsame starke Projektion auf die aus der Wirkung folgenden Bedingungen beseitigen lässt.

## Ableitung aus der Wirkung

Nach stationärer Elimination von q₂ beziehungsweise exakter Abel-Integration bleibt in jeder Ordnung C die dimensionslose skalare Phase

    S_C(x,y) = b/2 (xᵀL_C x + 2 xᵀX_C y + yᵀR_C y).
    p_y = ∂_y S_C = b (X_Cᵀx + R_C y).

Für v aus ker X_C fällt x aus der Impulsgleichung heraus. Mit p=−i∇_y lautet die Bedingung am Ausgang

    C_(C,v) = vᵀ(p − bR_C y),     C_(C,v) exp(i S_C) = 0.

Sie gilt folglich auch nach Eingangspaarung. Ihre Koeffizienten stammen ausschliesslich aus dem Schurkomplement der veröffentlichten Wirkung. 28 Ordnungen haben Rang zwei und liefern auf diesem Weg keine ausgangsseitige skalare Bedingung. In jeder der fünf übrigen gibt es genau eine. Die gemeinsame Verschiebung aller Skalarwerte lässt die Wirkung in allen 33 Fällen invariant. Sie verschiebt zugleich den Eingang und ist deshalb keine zusätzliche Bedingung an den Ausgang eines festgehaltenen Eingangs.

| Ordnung | v (primitive ganze Koordinaten) | R_C v |
| --- | --- | --- |
| 9116 | (3, 26) | (26, −26) |
| 17308 | (26, 3) | (−26, 26) |
| 25372, 25496 | (1, −1) | (7/2, −7/2) |
| 25500 | (1, −1) | (17/2, −17/2) |

## Der gemeinsame starke Kern ist null

Setze a=(q₃−q₄)/√2 und s=(q₃+q₄)/√2. In dieser orthonormalen Basis schreiben die Ordnungen 25372 bzw. 25496 und 25500 dem gleichen Impuls zwei verschiedene Bedingungen vor:

    C₁ = p_a − (7b/2) a,      C₂ = p_a − (17b/2) a,
    [C₁,C₂] = 5 i b I.

Die Differenz der beiden Gleichungen würde aψ=0, jede für sich dann auch p_aψ=0 erzwingen. Der Kommutator verlangt folglich 5ibψ=0. Da die Multiplikation mit a und die Ableitung auch auf temperierten Distributionen definiert sind, gilt das Resultat dort ebenfalls. Als Gegenkontrolle stimmen die Bedingungen der Ordnungen 25372 und 25496 miteinander überein. Eine gemeinsame Umphasung aller Randzustände konjugiert den Kommutator und lässt seinen konstanten Wert erhalten.

Die Matrix aller fünf Poissonklammern der linearen Impulsbedingungen hat Rang zwei. Ihre fünf Koeffizientenzeilen spannen einen dreidimensionalen Raum auf. Sein Zentrum wird von p₃+p₄ erzeugt, wie die Summe der ersten zwei Zeilen und die Klammern im JSON zeigen. Dieses Zentrum ist eine algebraische Aussage über die Gesamtheit der Zeilen. Es liefert keine zusätzliche Bedingung für den einzeln propagierten Zustand jeder Ordnung.

### Wie nah kann ein normiertes Paket beiden Bedingungen kommen?

Für jedes normierte Schwartz-Paket gilt

    (‖C₁ψ‖² + ‖C₂ψ‖²)/2 ≥ 5b/2 = 10/√6.

Der Betrag des Kommutatorerwartungswertes ist höchstens 2‖C₁ψ‖‖C₂ψ‖. Das arithmetische Mittel der Normquadrate ist damit mindestens 5b/2. Die Schranke ist scharf. Mit δ=5b/2 und beliebigem normiertem Schwartz-Paket φ(s) realisiert

    ψ(s,a) = φ(s) (δ/π)^(1/4) exp[−δa²/2 + i (6b)a²/2]

Gleichheit. Nach Entfernung der gemeinsamen Phase sind die beiden Operatoren p_a ± δa. Das Gaußpaket besitzt ⟨p_a²⟩=δ/2 und ⟨a²⟩=1/(2δ). Das Paket ist unter Vertauschung der beiden Ausgangsfelder invariant. Schon die beste solche Annäherung lässt daher einen strikt positiven mittleren quadratischen Fehler. Der Zahlenwert gilt für die angegebenen normierten Generatoren und Koordinaten.

## Was für eine einzelne Ordnung funktioniert

Sei v̂ die Einheitsnullrichtung, e eine dazu senkrechte Einheitsrichtung, h=v̂ᵀy und z=eᵀy. Nach Entfernung der bekannten Phase exp(ib yᵀR_C y/2) lautet die einzelne Bedingung ∂_h f=0. Die allgemeine Lösung hat die Form exp(ib yᵀR_C y/2) f(z), gegebenenfalls distributionell. Für die Grundpaketantwort gilt f∈L²(dz). Die Mittelung des Normquadrats über −H≤h≤H mit Faktor 1/(2H) liefert für jedes H>0 dasselbe transversale Integral. Wir wählen hier als Vergleichsmass die Einheitslänge in den bisherigen dimensionslosen euklidischen Feldkoordinaten.

Mit α_C=−b H₂₂⁽⁰⁾ und der Konvention aus Gl. (12)–(13) des publizierten Definitionsbereichstests gilt für die reine skalare Antwort I_C auf den Skalargrundzustand

    |I_C(y)|² = 8π² exp(−q z²) / [α_C √det(I+b² L_C²)],
    q = tr[b² X_Cᵀ (I+b² L_C²)⁻¹ X_C] > 0.
    N_C = ∫ |f(z)|² dz = (8π^(5/2)/b) √d_C.

| Ordnung | q | d_C im reduzierten skalaren Normquadrat N_C |
| --- | --- | --- |
| 9116, 17308 | 548/217 | 9/69185 |
| 25372, 25496 | 51484/59785 | 9/12871 |
| 25500 | 1225/1231 | 9/1423450 |

Diese Zahlen sind Gewichte je Feldlänge, vor Multiplikation mit Staub-, Rand- und Historienfaktoren. Sie enthalten keine Kreuzterme zwischen Ordnungen. Eine getrennte Summierung der fünf Normen würde voraussetzen, dass der Detektor die jeweilige Historie unterscheidet. Die kohärente Auslese aus PR #306 erlaubt diese Ersetzung nicht.

## Entscheidung und offene physikalische Prüfung

| Gegenstand | Entscheidung |
| --- | --- |
| Gleichzeitige starke Erfüllung aller einzelnen Ausgangsbedingungen in einem gemeinsamen skalaren Zustand | **FAIL** für diesen Projektionskandidaten. Sein Bild ist der Nullraum {0}. |
| Gewicht pro Einheitslänge für die isolierten fünf singulären Skalarantworten | Exakt bestimmt mit dem oben ausgewiesenen transversalen Mass. |
| Physikalisches Randprodukt der kohärenten Geburtsamplitude relativ zum leeren Zweig | **HOLD**. Die homogenen Einzelgleichungen sind mit einer beliebigen positiven Reskalierung eines angenommenen Geburtssektorprodukts verträglich. Für eine physikalische Norm muss zusätzlich die Paarung zwischen verschiedenen Historien und mit der Vakuumnorm begründet werden. |
| Physikalischer P3-Pilot, M=1, erste Dichtestufe | 0 von 38 vorbereiteten Vergleichen. Der Lauf bleibt offen. |

Die Wirkung verlangt die jeweilige Einzelbedingung für den zugehörigen Kern. Die Übertragung aller Einzelbedingungen auf die kohärente Summe war der geprüfte zusätzliche Ansatz. Der Ausschluss betrifft genau diesen Ansatz. Ein verbleibender Ansatzpunkt ist die Verklebung an einem gemeinsamen Zwischenrand mit den ursprünglichen Kreuztermen. Entscheidend wäre, ob sie ein positives, endliches Paarungsgewicht für die Geburtsantwort und eine relative Norm gegenüber dem leeren Zweig festlegt. Ein frei gewählter Streifencutoff oder eine Anpassung an die beiden vorgeschlagenen Geburtsraten würde diese Frage offenlassen.

## Reproduktion

Die Rechnung benötigt Python ab 3.10 mit der Standardbibliothek. Die folgenden Befehle im Verzeichnis dieser Studie oder im entpackten ZIP ausführen. Die Repository-Fassung liest die Eingaben aus den in `quellen.json` verzeichneten Studien. Das ZIP enthält dieselben Eingaben für die Offline-Nachrechnung.

    python3 -B randbedingungen.py --out nachrechnung.json
    python3 -B gegenprobe.py
    cmp ergebnis.json nachrechnung.json

Die Hauptrechnung überprüft die Git-Blob-Kennungen, berechnet Schurkomplemente, Richtungen, Klammern und reduzierte Normfaktoren in rationaler Arithmetik. Die Gegenprobe rekonstruiert die fünf mal fünf Hesse-Matrizen direkt aus den Kausalrelationen, variiert die volle Wirkung auf stationär fortgesetzten Randbasisvektoren und prüft alle vier Randvertauschungen pro Ordnung. Hinzu kommen fünf unabhängige transversale Integrationen, zehn Polynomtests des Kommutators und fünf Breitentests. Die Gleitkommaquadratur ist eine Kontrolle der exakten Formel. Es wurden keine dynamischen vierdimensionalen P3-Historien erzeugt.

Die Pfade in quellen.json beziehen sich auf research/rax_cqg/dust_collapse im angegebenen Commit.

[PR #306](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/306) · [Geburtsuhr und Randnorm](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/c914556d092870557e2e7ee1e559ea925c5744c2/research/rax_cqg/dust_collapse/clock_record_norm_v0_1) · [Herleitung der skalaren Antwort, Gl. 12 und 13](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/c914556d092870557e2e7ee1e559ea925c5744c2/research/rax_cqg/dust_collapse/coupled_kernel_domain_v0_1/DERIVATION.tex)
