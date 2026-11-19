# CST-DUST · Ein geometrischer Record am skalaren N11-Zukunftsrand

**Etappe 5A · Version 0.2 · 19. November 2026.** Zwei gemeinsam ausgelesene reduzierte Skalarmoden erlauben im deklarierten N11-Randvertrag einen eindeutigen Treffer für eine der beiden Ordnungen, ohne ein Ordnungsregister anzuhängen. Die Konstruktion lässt einen unentschiedenen Ausgang zu. Für das zentrierte Skalarpaket erreicht die feste Auslese der Moden 7 und 8 eine Effizienz von 49,50406544 % je normiertem Einzelzweig. Beim ursprünglichen Dichtewechsel ist der inklusive Kontrast exakt null. Eine andere Anfangsuhrform bei gleicher mittlerer Uhrzeit erzeugt einen numerischen Kontrast. Die physikalische Auswahl der Randpaarung und des Instruments hält Etappe 5A auf **HOLD**.

## Gegenstand und Konventionen

C0 hat drei, C1 ein vergleichbares Paar im markierten Inneren der N11-Ordnung. Die beiden Zweige benutzen den gemeinsamen Vergangenheits- und Zukunftskragen aus PR 293. Die Skalarwirkung liefert die reduzierten symplektischen Karten R₀,R₁ unter einer zusätzlichen gemeinsamen Quantisierung auf H = L²(ℝ³). Insbesondere wird die von C1 geforderte Reduktion auch für C0 angesetzt. Das skalare Eingangspaket ist das normierte zentrierte Gaußpaket. β = 4/√6. In dimensionslosen Koordinaten (x,p) = (√β q, √β π) gilt [xᵢ,pⱼ] = iδᵢⱼ. Der Ausgang hat die drei reduzierten kanonischen Moden 7, 8 und 9. Zu einer Mode gehören Koordinate und Impuls.

Der Rechner rekonstruiert die **beiden reduzierten Karten aus den Ordnungsrelationen** mit der unveränderten Elternrechnung. Zwei unabhängige Darstellungen liefern exakt dieselben Kovarianzen. Für ψⱼ(x) ∝ exp(−xᵀΩⱼ x/2), mit Ω = R+iT, gilt

    V = [[R⁻¹, −R⁻¹T], [−TR⁻¹, R+TR⁻¹T]] / 2 = Rⱼ Rⱼᵀ / 2.

Die Bezeichnung R ohne Index steht hier nur für den Realteil der Präzisionsmatrix, Rⱼ für die jeweilige symplektische Karte.

**Eichprüfung.** Für die aufsteigend geordneten vier Koordinaten und vier Impulse des Ausgangs sei a der Zeilenvektor des linearen Postconstraints A₊, h = J₈aᵀ und e die Zeile für q₁₀. Die Abbildung L entnimmt dem auf die Sektion zurückgezogenen Punkt (I−he/(eh))z die drei verbleibenden kanonischen Paare. Exakt geprüft sind Lh=0, LE₊=I₆ und LJ₈Lᵀ=J₆ für die Sektions-Einbettung E₊. Die Auslese ist also auf diesem Quotienten wohldefiniert. Beispielsweise wird q₈ dort durch q₈−(8/23)q₁₀ und π₇ durch π₇−(116/23)q₁₀ dargestellt. „Zwei Moden“ benennt diese reduzierten Systeme. Eine punktlokale Apparatur an nur zwei unreduzierten Knoten ist dadurch noch nicht konstruiert.

## Welche Information ist zugänglich?

**Eine benannte Randmode.** Für beide Zweige liegt die Determinante jeder einzelnen 2×2-Modenkovarianz strikt über 1/4. Die sechs rationalen Werte stehen in results.json. Jede dieser Gaußmarginalen ist daher unitär äquivalent zu einem thermischen Zustand mit strikt positiver Besetzung jeder Zahlstufe. Ist die Erwartung eines positiven Effekts in diesem Zustand null, verschwindet der Effekt. Ein positiver Treffer, der auf einem Zweig vorkommt und auf dem anderen ausgeschlossen ist, kann an keiner einzelnen dieser drei Moden realisiert werden. Statistische Unterscheidbarkeit bleibt möglich.

**Zwei benannte Randmoden.** Für das vorab gewählte Paar i,j = 7,8 wird k=9 ausgeblendet. Für jede auszuschliessende Ordnung c wähle eine Zeile ℓ mit ℓᵢ=Ωⱼₖ, ℓⱼ=−Ωᵢₖ und ℓₖ=0 (Ω der Ordnung c). Der Operator

    B_c = ℓ(p − i Ω_c x),     N_c = [B_c,B_c†] > 0,     b_c = B_c / √N_c

enthält weder xₖ noch pₖ und erfüllt b_c ψ_c=0. Der Projektor Π_c auf das Vakuum dieser einen synthetisierten kanonischen Mode, mit Identität auf den übrigen Moden, akzeptiert den zugehörigen Einzelzweig sicher. Ein Nichtvakuumtreffer in I−Π_c schliesst diesen Zweig exakt aus. Das Instrument verlangt Zugang zu den konjugierten Quadraturen und eine Vakuum-/Nichtvakuummessung der gebildeten Mode. Eine Messung nur der beiden Feldwerte erfüllt diesen Vertrag nicht.

Sei d₁ = ⟨ψ₁|(I−Π₀)|ψ₁⟩ und d₀ = ⟨ψ₀|(I−Π₁)|ψ₀⟩. Für den Test gegen C0 wähle die feste Wahrscheinlichkeit w=d₀/(d₀+d₁). Die Effekte sind

    F_ein  = w (I−Π₀),       F_drei = (1−w)(I−Π₁),
    F_?    = w Π₀ + (1−w) Π₁,       F_ein + F_drei + F_? = I.

Beide eindeutigen Ausgänge haben auf dem normierten richtigen Einzelzweig dieselbe Effizienz η=d₀d₁/(d₀+d₁). Für eine normierte zentrierte Gaußmode mit Kovarianz V_b ist die Vakuumwahrscheinlichkeit 1/√det(V_b+I₂/2). Alle Determinanten werden rational aus den Quadraturen berechnet. Unabhängig wird durch direkte Wirkung von B auf die Wellenfunktion die Identität det(V_b+I₂/2)=(1+⟨b†b⟩)²−|⟨bb⟩|² geprüft. Der falsche Zweig liefert exakt 1, der richtige eine Determinante strikt über 1. Rationale Intervalle der Breite höchstens 2×10⁻¹² für η werden mit Ganzzahlquadratwurzeln erzeugt.

| Zugängliche Moden | Gleiche eindeutige Trefferwahrscheinlichkeit je Einzelzweig |
|---|---:|
| 7, 8 | 49,50406544 % |
| 7, 9 | 49,11112327 % |
| 8, 9 | 49,80586211 % |
| Alle drei, optimaler gemeinsamer Effekt für das feste Zustandspaar | 99,18507672 % |

Die Zweimodenwerte gelten für die konstruierte randomisierte Messung. Die globale Schranke folgt aus der Grambedingung G−ηI ≥ 0 mit Gᵢⱼ=⟨ψᵢ,ψⱼ⟩. Sie ist auf dem Aufspann beider Zustände mittels ihrer reziproken Vektoren erreichbar. Die kleinste Eigenzahl von G ist 1−|⟨ψ₀,ψ₁⟩|. Eine dreimodige optimale Messung benötigt eine andere Apparatur.

## Für welche Eingänge ist ein eindeutiger Treffer belastbar?

Das feste Zweimodeninstrument erlaubt eine exakte Charakterisierung über den kalibrierten Grundzustand hinaus. Für einen Zweig c ist ein falscher Treffer genau dann ausgeschlossen, wenn das Ausgangsbild im Vakuum von b_c liegt. Ziehe beide Bedingungen mit den unitären Skalartransfers V₀,V₁ auf den Eingang zurück. Beide zurückgezogenen Vernichter sind reine Linearkombinationen der drei Eingangsvernichter. Das folgt auch daraus, dass sie dasselbe Eingangsvakuum vernichten. Die zwei Zeilen ihrer Koeffizienten haben für das Paar 7,8 exakt Rang zwei.

Nach einem unitären Wechsel der drei Eingangsmoden ist der **maximale gemeinsame Unterraum ohne falsche Treffer** deshalb |0,0⟩ ⊗ ℱ(ℂ). Zwei Moden müssen im Vakuum liegen, die dritte darf beliebig besetzt sein. Für gemischte Zustände muss ihr Träger in diesem Unterraum liegen. Die rationale komplexe Richtung der freien Mode und ein expliziter Verschiebungstest stehen in results.json. Ein kohärentes Paket mit Einheitsverschiebung in dieser Mode hat weiterhin exakt null Fehlzuordnungen. Seine beiden richtigen Trefferwahrscheinlichkeiten mit derselben Apparatur ändern sich. Die für den Grundzustand ausgeglichene Kalibrierung ist eine zusätzliche Bedingung für die Null des signierten Kontrollmittels. Die späteren Dichte- und Uhrvergleiche verwenden genau den kalibrierten Grundzustand.

Ein universeller Ordnungsrecord für beliebige unbekannte skalare Eingänge auf H ist durch einen skalaren Ausgangseffekt ausgeschlossen. Jede der beiden unitären Karten ist surjektiv. Ein Effekt ohne falsche Treffer auf allen Bildern eines Zweiges müsste folglich auf ganz H verschwinden. Der oben gefundene Unterraum beschreibt die Verträglichkeit mit der konkreten Auslese. Eine Herleitung zulässiger physikalischer Zustände aus der gesamten Wirkungs- und Constraintstruktur steht aus.

## Unbedingte Dichte- und Uhrbilanz

Der akzeptierte skalare Zustand ist jetzt kohärent, ψ_out=A₀ψ₀+A₁ψ₁. Der gemeinsame positive Drei-Moden-Rand, alle Phasen und Amplitudenkoeffizienten bleiben die der bisherigen N11-Rechnung. Im geerbten konstanten Analysator ist A_c = ∫ f W_c dμ/2. Bei der inklusiven Auslese werden die kollektiven Labels (r,t) wie im Vorgänger mitgeführt und **alle** Randmoden summiert. Die folgenden Formeln gelten dort punktweise mit A_c = f(r,t)W_c(r,t)/2 und anschliessender Integration. Die Skalarzweige werden bei jedem (r,t) kohärent addiert. Die Wahl, die kollektiven Labels am Ausgang zu erhalten, ist eine eigene Randannahme.

    p_ein  = η |A₁|²,     p_drei = η |A₀|²,
    S      = |A₀|² + |A₁|² + 2 Re(A₀* A₁ ⟨ψ₀,ψ₁⟩),
    p_?    = S − p_ein − p_drei,      p_Randfehlschlag = 1 − S.

Die Kontraktivität folgt aus |W_c|≤1, der Unitarität der Skalarzweige und den Koeffizienten 1/2, beim konstanten Analysator zusätzlich aus der Kontraktivität der normierten Projektion. Die gesamte Interferenz innerhalb des akzeptierten Ausgangs bleibt im unentschiedenen Ergebnis enthalten. Positive Eindeutigkeit eines Treffers begründet keine Zuordnung der unentschiedenen Fälle zu klassischen Historien. Für die Dichtezentren 1/8 und 1/4 im gekoppelten inklusiven Hauptversuch ergeben sich je **10,93024610 %** mit einem Paar und **4,24342217 %** mit drei. **15,25405128 %** bleiben am akzeptierten Skalarausgang unentschieden, **69,57228044 %** sind Randfehlschläge.

X zählt +1 für ein Paar, −1 für drei und 0 für die beiden übrigen Fälle. Die gemeinsame Staubkontrolle verwendet weiterhin die vollständige Staubwirkung von C0 für beide Zweige und ihre eigenen Gravitationsphasen und Skalartransfers. Auf dem zentrierten Skalarpaket ist dann ⟨X⟩=0 für jedes der geprüften Uhr-/Dichtepakete, weil beide Treffer dieselbe Effizienz haben und |A₀|=|A₁| gilt. Die einzelnen Trefferwahrscheinlichkeiten können sich dabei ändern.

| Änderung der Anfangspräparation | Alle kollektiven Moden, gekoppelt | Konstante Mode, gekoppelt | ⟨X⟩-Änderung in der Kontrolle |
|---|---:|---:|---:|
| Dichtezentrum 1/8 → 1/4, gleiches Uhrpaket | exakt 0 | −0,00000170231 | exakt 0 |
| Ein → zwei Uhrfenster, gleiche mittlere Uhrzeit und Dichte 1/8 | −0,00178912616 | +0,00003990205 | exakt 0 |

Im inklusiven Dichteversuch gilt stärker die exakte Null für jeden der vier einzelnen Ausgänge. Die Änderung der Dichte wirkt punktweise als gemeinsame Phase und die Uhrmarginalen stimmen überein. Der Vorzeichenwechsel des Uhrkontrasts zwischen den beiden Analysatoren begrenzt seine physikalische Deutung. Die Werte für Projektion und Übertrittshäufigkeiten sind numerisch. Der Vergleich auf drei Gittern ersetzt keine vollständige Einschliessung des numerischen Fehlers.

## Nachrechnung und Quellen

Python 3 mit NumPy, SymPy und mpmath genügt. Im entpackten Verzeichnis ausführen.

    python3 -B verify.py

Der Prüfer gleicht alle archivierten Quelldateien per SHA-256 ab, rekonstruiert die kanonischen Karten in einem temporären Ordner, prüft die Gaußrechnung und wiederholt die vierteiligen Wahrscheinlichkeitsbilanzen für beide Kerne und Messweisen. Die drei verwendeten Quadraturgitter haben 32/6, 64/8 und 96/12 Knoten je innerer Uhr bzw. je äusserem Uhrfenster. sources.json enthält die exakten Repository-Pfade zu Commit 2937e3390866413544630e86771c5f9633afd5d4. contract.json legt den primären Vergleich, das Modenpaar und die Auslese fest. Die Charakterisierung des Eingangsunterraums ist eine anschliessende algebraische Erweiterung.

- Projektquellen sind [PR 293 zum gemeinsamen Randvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/293), [PR 294 zur Präparation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/294) und [PR 317 zur geometrischen Auslese](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/317).
- Die thermische Normalform und Gaußkonventionen sind bei [Weedbrook et al., Gaussian Quantum Information, Abschnitte II.B–C](https://arxiv.org/abs/1110.3234) dargestellt. Der Artikel normiert die Vakuumkovarianz auf I, hier ist sie I/2.
- Zur eindeutigen Zustandsunterscheidung siehe [Barnett und Croke, Quantum state discrimination](https://arxiv.org/abs/0810.1970). Die N11-Kovarianzen, Quoten und Eingangsbedingungen in dieser Studie ergeben sich aus der separaten Projektrechnung.
