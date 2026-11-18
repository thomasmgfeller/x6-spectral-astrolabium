# CST-DUST · Geburtsuhr als Record am gemeinsamen Rand

[Kurzbericht (PDF)](../reports/CST_DUST_Geburtsuhr_Randnorm.pdf) · [Prüfpaket für die Offline-Nachrechnung](../packages/CST_DUST_Geburtsuhr_Randnorm_Pruefpaket.zip) · [Ergebnisse (JSON)](ergebnis.json)

18. November 2026 · Anschluss an PR #305 · endliche AA-Familie mit 33 Ordnungen.

Ein gespeicherter innerer Uhrwert liefert im festen Atom-/Grundpaket einen von null verschiedenen linearen Beitrag zum Auslesegewicht. Die vollständige ausgehende Norm im bisherigen Randprodukt divergiert bereits für jedes positive Uhrfenster. Damit liegt ein berechneter Beitrag eines einzelnen Detektorkanals vor. Die Norm relativ zum leeren Zweig und die physikalische Geburtsrate bleiben offen.

## Was in die Rechnung eingeht

Wir verwenden den gekoppelten AA-Kern mit zwei Randpunkten auf jeder Seite, einem inneren Ereignis, Gravitation mit κ=1, masselosem Skalar, Einheitsbreiten und Gewicht 1/33 pro beschrifteter Ordnung. Beide Randvertauschungen sind berücksichtigt. Für den endlichen Kanal bleiben Eingangs- und Ausgangspaket genau die Atom-/Skalargrundzustände aus PR #305, mit konstanten Randuhrpaketen. Die innere Staubdichte wird über das gesamte ursprüngliche Mass ν=(δ₀+1₍₀,₁₎dr)/2 integriert. Der Wert u=(t₂+1)/2 parametrisiert hier die innere AA-Uhrbox. Seine physikalische Identifikation mit der P3-Staubeigenzeit bleibt offen.

Neu ist die Auslese: Verschiedene Werte der inneren Uhr werden als orthogonale Records in L²([0,1],du) behandelt. Ihre Auflösung und das Mass du sind Teil dieses kontrollierten Versuchs. Die ursprüngliche AA-Wirkung liefert die Phasen. Die Herleitung eines physikalischen Recordprodukts ist offen.

## Positiver Beitrag im festen Ausgangspaket

Nach der inneren Abel-Integration und Paarung der äusseren Skalargrundzustände sei S_C der komplexe skalare Grundpaketfaktor. Der Staubfaktor bei festgehaltenem u lautet für p vergangene Nachbarn des inneren Ereignisses

    Z_p(u) = ∫_[0,1]^p χ(1/2 + b Σ_j (y_j−u)²) dy,     b=4/√6,
    χ(k)   = (1+∫₀¹ exp(−ikr)dr)/2.

Die übrigen Randuhren integrieren zu eins. Beide Randquotienten und die normierten Dichteatome geben zusammen den Faktor 1/8. Mit den 33 ursprünglichen Gravitationsphasen ist der kohärente Koeffizient

    A(u) = (1/264) Σ_C exp(i F₄(C)) S_C Z_{p(C)}(u).

Hier bedeutet der Index von Z die Vorgängerzahl p(C). Die zehn Randorbits entsprechen genau den 33 beschrifteten Summanden. Rechnungen in rationalen Fehlerscheiben ergeben

    Re A(0) ∈ [−0,1352829471854; −0,1352829471853],
    Im A(0) ∈ [ 0,0752062398836;  0,0752062398837].

Behält die Auslese u, ist das Gewicht W(d)=∫₀ᵈ|A(u)|²du. Die Stetigkeit ergibt lim W(d)/d=|A(0)|². Wird zuvor über die Uhr amplitudenseitig summiert, ergibt sich |∫₀ᵈA(u)du|²=d²|A(0)|²+O(d³). Diese verschiedenen Kurzzeitgesetze gelten jetzt für die kohärente Summe mit unveränderten Randpaketen.

| Rechnung | Führender Koeffizient im u-aufgelösten Grundpaket |
| --- | --- |
| Gekoppelte 33er-Summe | [0,0239574543165; 0,0239574543166] |
| Kontrollrechnung mit ausgeschalteter Gravitationsphase | [0,0940666231502; 0,0940666231503] |
| Kontrollrechnung mit zusätzlicher unterscheidbarer Markierung jeder der 33 beschrifteten Historien | [0,0042504747695; 0,0042504747696] |

Die letzte Kontrolle entspricht der inkohärenten Summe der 33 Quadrate und verändert die Auslese. Die mittlere Kontrolle entfernt nur exp(iF₄), die Staub- und Skalarfaktoren bleiben erhalten. Aus den Unterschieden folgt eine Interferenzwirkung in diesem Kanal. Ein Experiment mit zwei physikalischen Massenpräparationen ist damit offen.

**Fehler und endliche Auflösung.** Die Primärrechnung übernimmt die veröffentlichten komplexen Einschliessungen der zehn skalaren Orbitfaktoren. Sie integriert die Dichtemomente exakt bis Grad 36, mit Taylorrest und rationaler Wurzelhülle. Für die Gravitationsphasen verwendet sie einen separat beschränkten Taylorrest bis Grad 200. Die unabhängig gerechnete Gleitkomma-Gegenprobe verwendet alle 33 Matrizen, die fortgesetzte Wurzel über Einzeleigenwerte und direkte Gaussquadratur.

Aus |Z′_p|≤bp/2 folgt eine explizite Lipschitzkonstante L für A. Der Unterschied von W(d)/d zu |A(0)|² ist höchstens |A(0)|Ld+L²d²/3. Das JSON enthält vollständige Hüllen für d=1/16 bis 1/1024. Bei einer Unterteilung des Fensters in n gleich breite Zellen der Breite Δ wird der Record auf normierte konstante Zellmoden projiziert. Das fehlende Gewicht ist höchstens L²dΔ²/12. Das folgt aus der doppelten Integraldarstellung der Varianz in jeder Zelle. Für d=1/8 stimmen die Ergebnisse von 16 Zellen und kontinuierlicher Auslese in den ersten sechs Nachkommastellen des Quotienten W/d überein. Das betrifft die Auflösung dieses Detektors.

## Was geschieht bei der Summe über alle zukünftigen Randzustände?

Wir lassen das Ausgangspaket weg und behalten den normierten Eingang. Alle ausgehenden Skalarfelder werden im ursprünglichen symmetrischen Randprodukt mit Lebesgue-Mass gemessen. Schon der gemeinsame Atomsektor r₃=r₄=0 hat positive Masskomponente 1/8 und liefert eine divergente Norm. Der frühere Definitionsbereichstest bewies dies für die zeitlich integrierte Antwort. Hier wird nachgewiesen, dass dieselbe Divergenz bei festgehaltenem u und auf jedem noch so kurzen positiven Uhrintervall bestehen bleibt.

Das rationale skalare Schurkomplement jeder Ordnung zerfällt in die Blöcke L_C, X_C, R_C für linke, übergreifende und rechte Felder. Die Ausgangsdämpfung im Gaußexponenten ist Q_C=b² X_Cᵀ(I+b²L_C²)⁻¹X_C. Die 33 Blöcke wurden aus den eingefrorenen Hesse-Matrizen nachgerechnet. 28 besitzen vollen Kreuzrang, fünf haben Rang eins. Ihre ungedämpften Geraden haben drei verschiedene Richtungen, proportional zu (3/26,1), (26/3,1) oder (−1,1). Es gibt keine gemeinsame ausgehende Nullrichtung dieser fünf Terme.

Für s=(q₃+q₄)/√2 und a=(q₃−q₄)/√2 betrachte den Streifen |s|≤1, |a|≤R. Hier fallen 30 der 33 Summanden für |a|→∞ gleichmässig gaußförmig ab. Die Beiträge 25372 und 25496 haben denselben symmetrischen Eingang, Staubfaktor Z₁(u), Phase und Betrag. Der Beitrag 25500 hat Staubfaktor Z₂(u). Die verbleibenden beiden quadratischen Feldphasen sind exp(ib·7a²/4) bzw. exp(ib·17a²/4). Ihr Kreuzterm integriert sich über a zu einem in R beschränkten Fresnelintegral. Das Normquadrat der kohärenten Summe wächst daher linear mit R. Die Randvertauschungssymmetrie der gesamten Summe ist erhalten.

Entscheidend für die kurze Uhrstrecke ist eine in u uniforme Abschätzung. Es gilt Re χ(k)=(1+sin(k)/k)/2≥1/3 für jedes hier vorkommende k≥0. Bis k=3 ist der Sinus nichtnegativ, für k≥3 gilt sin(k)/k≥−1/3. Damit ist Re Z_p(u)≥1/3 punktweise. In der Röhrenabschätzung aus dem Definitionsbereichstest ersetzt dies die alte Schranke 3/16. Alle skalaren Faktoren bleiben dieselben. Schreiben wir G(u) für die vollständige Ausgangsantwort und Ω_R für den beschriebenen Streifen einschliesslich des ausgehenden Dichteatoms, so folgt für jedes 0<d≤1

    liminf_(R→∞) [1/(2Rd)] ∫₀ᵈ ‖1_(Ω_R)G(u)‖²_H du
        ≥ [(1/3)/(3/16)]² · (zertifizierte alte Untergrenze)
        > 1/7 031 250.

Das Integral über u ist mit der Untergrenze vereinbar, etwa direkt durch das Lemma von Fatou für die nichtnegativen Normdichten. Die Abschätzung ist asymptotisch in R und gilt für die gekoppelte Summe einschliesslich aller Kreuzterme. Für die vollständige ausgehende Feldachse ist das Gewicht in jedem positiven Fenster unendlich. Eine vollständige Randmodensumme kann diesen Befund über eine im Testraum dichte orthonormale Familie rekonstruieren. Das Weglassen der fünf Ordnungen würde die eingefrorene Historiensumme ändern.

## Physikalische Entscheidung

Der gespeicherte Uhrwert liefert den linearen Beitrag des festen Randkanals. Zur Normierung einer physikalischen Geburt müsste derselbe Vertrag das Gesamtgewicht aller Ausgänge und die relative Norm des leeren Zweigs bestimmen. Im bisher verwendeten Randprodukt scheitert bereits die Endlichkeit für diesen normalisierten Eingang. Damit entscheidet diese Auslese weder zwischen β=5/4 und β=4/3 noch über die Eignung anderer physikalisch hergeleiteter Randprodukte. Der P3-Pilot bleibt bei 0 von 38 physikalischen Vergleichen für M=1.

## Nachrechnen und Quellen

Python 3.10 oder neuer und die Standardbibliothek genügen. Im Verzeichnis dieser Studie oder des entpackten Prüfpakets ausführen.

    python3 -B -O record.py --out replay.json
    python3 -B -O gegenprobe.py

replay.json lässt sich byteweise mit ergebnis.json vergleichen. Die Kontrolle enthält 42 unabhängige numerische Vergleiche und fünf Tests der Zeitzellen. Der numerische Vergleich ist eine interne Gegenrechnung. Die angegebenen Einschliessungen beruhen auf den analytischen Schranken und den übernommenen publizierten Skalarzertifikaten. Alle Quellen im Paket sind auf den Git-Stand 7633ce1f4fb070b0d06546cfa682273438017a1e gebunden.

[Erste Geburtsrate, PR 305](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/7633ce1f4fb070b0d06546cfa682273438017a1e/research/rax_cqg/dust_collapse/first_birth_rate_v0_1) · [Skalarphasen und Uniformgewichte](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/7633ce1f4fb070b0d06546cfa682273438017a1e/research/rax_cqg/dust_collapse/parity_mixing_v0_1) · [Definitionsbereich und Streifenschranke, Gl. 12–19](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7633ce1f4fb070b0d06546cfa682273438017a1e/research/rax_cqg/dust_collapse/coupled_kernel_domain_v0_1/DERIVATION.tex)
