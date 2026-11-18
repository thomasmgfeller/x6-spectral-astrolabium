# CST-DUST · Lässt sich die erste Geburtsrate aus der Amplitude bestimmen?

[Offline-Prüfpaket](../packages/CST_DUST_Erste_Geburtsrate_Pruefpaket.zip) · [Ergebnisse (JSON)](ergebnis.json)

**18. November 2026.** Beide Uhrpaarungen aus dem [M=1-Vortest](../m1_pilot_clock_v0_1/README.md) bleiben mit der Ein-Geburts-Amplitude des offenen Uhrmodells vereinbar. Der geerbte Kern bestimmt die Phase, und das vollständige Zählen entfernt sie aus dem Betragsquadrat. Die beiden Vorschläge unterscheiden sich in der relativen Norm des Ein-Geburts-Sektors. Zusätzlich haben wir die gemeinsame Wirkung mit Skalarfeld an 33 Ordnungen mit festen Randpaketen geprüft. Die einzelnen Amplituden fallen linear mit der Fensterbreite. Ihre Quadrate liefern über diesen einzelnen Auslesekanal keine von null verschiedene anfängliche Rate.

## Fester Anfang und klare Zählfrage

Für das **offene Uhrmodell** ist der Zustand der leere innere Anfang, normiert auf eins. Der äussere Anker hat T = −2 und w = 0. Wir übernehmen die veröffentlichte Parametrisierung T = −2+4s, die Zahlgewichtung α=1, den Geburtsfaktor z=1 und das Dichtemass ν=(δ₀+1₍₀,₁₎dw)/2. Der geborene Punkt mit Uhr u hat genau einen Vorgänger. Daher ist die Differenz der Gravitationswirkung null, die Differenz der Staubwirkung gleich −w(1/2+4u²). Vierzig rationale Vergleiche der vollständigen Wirkung, ihrer Inkrementformel und dieses Ausdrucks stimmen überein.

Die Ein-Geburts-Wellenfunktion auf 0<u<d hat den Rohfaktor φᵤ(w)=exp[−iμw(1/2+4u²)]. Ein vollständiger Zähler integriert |φᵤ|² über ν und u. Das gibt d. Der rohe unveränderte Keine-Geburt-Zweig hat Normquadrat eins. Um aus beiden und den weiteren Geburtszahlen Wahrscheinlichkeiten zu gewinnen, braucht der gemeinsame Zustand ein festgelegtes positives Produkt.

In den zwei schon untersuchten Referenzpaarungen gilt h₁(d)=β−1+exp(−d), h₀(d)=(1−β)d+exp(−d) und h₀(0)=1. Daher sind P(N_d=1)=d h₁(d) und P(N_d≥1)=1−h₀(d). Ihr Unterschied beträgt 1−(1+d)exp(−d), höchstens d²/2. Beide Fragen führen am Anfang auf dieselbe Rate β pro Einheit s. Das sind dimensionlose Modelle mit unterschiedlichen Produkten. Eine Umrechnung in P3-Staubeigenzeit ist offen. [Offener Uhrkern](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b595e3c971f4f80ea56c41ea1de0b942d67dce1a/research/rax_cqg/dust_collapse/clock_intervals_v0_1)

## Was die Auslese zur Rate beiträgt

Auf dem gemeinsamen Raum der Uhren und Dichtemarken verwenden wir für jede Uhr denselben positiven Filter auf die in w konstante, normierte Funktion 1. Der Detektor ist die Identität auf dem Uhrraum, tensoriert mit |1⟩⟨1| auf den Marken. Sein zweiter Ausgang ist das orthogonale Komplement im Ein-Geburts-Sektor. Dieser **hier gewählte** Detektor lässt die verschiedenen Uhren unterscheidbar. Er unterscheidet sich von einem Rang-eins-Filter auf das gesamte Uhr- und Dichtepaket. Die Beschränkung auf 0<u<d ist die historische Frage; der Filter bleibt für alle Fenster gleich.

Für χ(t)=∫exp(−itw)dν(w) beträgt die bedingte Erfolgswahrscheinlichkeit bei einer Geburt

    V(d)=d⁻¹ ∫₀ᵈ |χ(μ(1/2+4u²))|² du.

Bei μ=1 liegt V(0⁺) in [0,974260414823; 0,974260414824]. Bei μ=0 gilt V(d)=1. Die Anfangsraten für Erfolg und Ausfall lauten βV(0⁺) und β[1−V(0⁺)]. Die Dezimalzahlen in der Tabelle sind gerundet.

| β | Filtererfolg je Einheit s | Filterausfall je Einheit s | Summe |
| --- | ---: | ---: | ---: |
| 5/4 | 1,217826 | 0,032174 | 1,25 |
| 4/3 | 1,299014 | 0,034319 | 1,333333… |

Zwei Rechenwege kontrollieren V(d). Der erste integriert die Phasendifferenz zweier unabhängig gezogener Marken. Der zweite entwickelt die geschlossene Formel |χ(t)|²=1/4+sin(t)/(2t)+(1−cos t)/(2t²) mit stetigem Wert bei null. Die Koeffizienten stimmen exakt überein. Die Taylor-Restschranke und nach aussen gerundete Intervalle sind für μ=0, 1/4, 1, beide β und sieben positive dyadische Fenster im Ergebnis gespeichert. Die Phase verändert Erfolge und Ausfälle. Der informative Unterschied zwischen den beiden Gesamtgeburtsraten stammt weiterhin aus der Sektornorm. [Publizierter Wirkungs- und Messvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b595e3c971f4f80ea56c41ea1de0b942d67dce1a/research/rax_cqg/dust_collapse/operational_matter_v0_1)

## Gegenprobe mit der gemeinsamen Gravitation-Staub-Skalar-Amplitude

Der zweite Vertrag hat zwei äussere Zweierantichains und ein inneres Ereignis. Die alten und neuen äusseren Pakete werden fest im publizierten Dichteatom und skalaren Grundzustand mit Einheitsbreiten gewählt. Das innere Dichtemass enthält Atom und kontinuierlichen Anteil. Das zusätzliche Skalarfeld ist masselos. Seine Integrale werden im veröffentlichten Abel-Grenzwert genommen. Für jede der 33 Ordnungen C berechnen wir den Betrag **ihres einzelnen Beitrags** mit Historienkoeffizient eins. Die Gravitationsphase bleibt im Beitrag erhalten und fällt aus seinem Betrag heraus. Bei einer kohärenten Summe können sich Beiträge zusätzlich aufheben.

In diesem Vertrag hat jede Uhr das Mass dt/2 auf [−1,1]. Wir setzen u=(t₂+1)/2 und beschränken nur die innere Integration auf 0<u<d. Beide äusseren Pakete, ihre Uhren und ihre Integrationsmasse bleiben unverändert. Diese lokale Fensterkoordinate gehört zur AA-Randamplitude. Ihre Gleichsetzung mit s oder der P3-Staubeigenzeit ist keine Voraussetzung der Rechnung.

Die bekannte skalare Majorante ist von der inneren Uhr und dem Regulator unabhängig. Die Beschränkung kostet im normierten Uhrmass genau einen Faktor d. Folglich gilt für alle ursprünglichen festen Pakete |M_C(d)|≤B_C d. Für den einzeln ausgewerteten Grundkanal ergibt sich sogar die führende Konstante exakt bis auf kontrollierte Integrale.

Setze b=4/√6, H=H₀/(va) in der Notation der publizierten Hessiandatei, c=−H₂₂=(p+q)/2, p bzw. q die Zahlen der inneren Vorgänger bzw. Nachfolger am Rand. Mit Randindexmenge B={0,1,3,4} ist E=H_BB+H_B2 H_2B/c. Die 33 rationalen Matrizen wurden direkt aus den Ordnungsrelationen rekonstruiert. Es gilt c≥1. Aus dem inneren Fresnelintegral und dem äusseren Grundpaketintegral folgt

    lim |M_C(d)/d|² = π³ |Z_p|² / [2 b c √det(I+(8/3)E²)],
    Z_p = ∫_[0,1]^p χ(1/2 + b Σ_j y_j²) dy.

Der Vorfaktor berücksichtigt beide Randquotienten und normierte Atom- und Grundpakete. Insbesondere ist der Staubfaktor 1/8 vor dem verbleibenden Phasenmittel. Der Grenzwert folgt aus Stetigkeit auf der kompakten Uhrbox und der integrierbaren Majorante. Ein direkter Weg zur Formel setzt t₂=−1 und t_j=−1+2y_j für die p Vorgängeruhren. Alle Kantengewichte zum inneren Punkt sind Linkgewichte. Die q künftigen Randdichten sind in diesem Kanal null. Für endliches d ist die Änderung des gemittelten Z_p gegenüber dem Grenzwert im Betrag höchstens bp d/4, da |(y−u)²−y²|≤2u und ∫w dν=1/4.

Jeder der 33 Werte für lim |M_C(d)/d|² ist strikt positiv. Die gemeinsame nach aussen gerundete Hülle reicht von 0,000624445474 bis 0,307490929118. Die individuellen Intervalle und rationalen Determinanten stehen im JSON. Der auditierte Wert ist das Quadrat der **Amplitudensteigung**. Für die Ableitung des Betragsquadrats gilt dagegen für jeden solchen Beitrag und jede feste endliche Linearkombination

    lim |M(d)|²/d = 0.

Der vollständig skalare Kontrollfall zeigt damit, warum das Quadrieren eines fest gepaarten Randmatrixelements eine lineare Zählrate verlieren kann. Interferenz mit einem Vakuumzweig kann linear sein; zu ihrer Deutung als Wahrscheinlichkeit einer Geburt wäre ein positives, vollständig definiertes Ereignisinstrument nötig. Ein unendlicher Satz von Randzuständen könnte beim Summieren ein anderes Verhalten haben. [AA-Amplitude und Majorante](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b595e3c971f4f80ea56c41ea1de0b942d67dce1a/research/rax_cqg/dust_collapse/amplitude_existence_v0_1)

## Wo eine unabhängige Auswahlgleichung ansetzen kann

Ein uhrdiagonaler Anteil in einer physikalischen Ein-Geburts-Paarung setzt u=u′ zwischen den beiden Kopien der Amplitude. Er reduziert das doppelte Uhrintegral auf ein einfaches. Als explizite hinreichende Struktur betrachte eine positive Paarung mit Kern G(u,u′)=K(u)δ(u−u′)+R(u,u′) auf den Dichte- bzw. übrigen Marken. Angenommen, R ist lokal in Operatornorm beschränkt, K ist am Anfang normstetig, der Vakuumzweig hat positive Norm g₀ und die markierte Ein-Geburts-Amplitude ist normstetig am Anfang. Dann folgt für z=1 und die gegebene Uhrnormierung

    lim ⟨1_(0,d) φ, G 1_(0,d) φ⟩/(d g₀)
        = ⟨φ₀,K(0)φ₀⟩/g₀.

Der R-Anteil ist betragsmässig durch d² sup‖R‖ sup‖φᵤ‖² beschränkt. Der uhrdiagonale Anteil liefert durch Mittelung den angegebenen Grenzwert. Für die Referenzpaarung gilt am Anfang K(0)=β I und g₀=1. Das reproduziert den eingesetzten Wert. Eine unabhängige Bestimmung verlangt den markenaufgelösten physikalischen Randeffekt samt Norm relativ zum leeren Zweig. Liegt ein physikalisches Dekohärenzfunktional vor, ist die entsprechende Primärgrösse das Quantenmass des frühen Geburtsereignisses. Für seine Interpretation als klassische Alternative ist zusätzlich das Verhältnis zum Keine-Geburt-Zweig auf Interferenz zu prüfen. Der Satz behandelt die angegebene Struktur des Kerns; allgemeinere singuläre Kerne sind offen.

Eine zusätzliche exakte Kontrolle macht die Reihenfolge zweier Grenzübergänge sichtbar. Für μ=0 projizieren wir die auf (0,d) getragene Geburtswelle auf die normierten konstanten Moden fester dyadischer Uhrzellen der Breite Δ. Der erfasste Anteil der Ein-Geburts-Norm ist für am Ursprung ausgerichtete dyadische Breiten min(1,d/Δ). Dies wurde für 81 Paare geprüft. Bei festem Δ fällt er im Kurzzeitlimit auf null. Verfeinert man zuerst den vollständigen Satz von Uhrzellen, erfasst er die ganze Norm. Die Zellprojektion ist eine mathematische Kontrolle. Eine physikalisch begründete Auflösung der Identität am gemeinsamen Rand bleibt aus der Theorie herzuleiten.

**Entscheidung.** Der Versuch, β aus einem einzelnen der 33 festen Matrixelemente über |M(d)|²/d zu bestimmen, ergibt für diesen Ansatz null. Im vollständigen Zählvergleich des Uhrmodells bleiben 5/4 und 4/3 beide zulässig. Der veröffentlichte P3-Status bleibt HOLD_NOT_ELIGIBLE. In diesem Lauf wurden null physikalische P3-Vergleiche ausgeführt.

## Nachrechnung

Python 3.10 oder neuer, Standardbibliothek. Nach dem Entpacken:

    python3 -B -O rechnung.py --out nachrechnung.json
    python3 -B -O gegenprobe.py

Die erste Ausgabe ist byteweise mit ergebnis.json vergleichbar. Sie enthält exakte Bruchrechnungen oder analytische Restschranken; ausgegebene Dezimalintervalle sind nach aussen gerundet. Die Gegenprobe liest das mitgelieferte Ergebnis, berechnet die skalare Determinante direkt im komplexen Fünferraum, integriert die ursprünglichen Phasen numerisch und kontrolliert die drei Uhrkanäle. Die numerische Gegenprobe ist ein zweiter Rechenweg und liefert keine zusätzlichen zertifizierten Stellen.

Git-Quellstand b595e3c971f4f80ea56c41ea1de0b942d67dce1a. Die Repository-Pfade und Git-Blob-Prüfsummen stehen in [quellen.json](quellen.json). Der weiterverwendete Uhrtest des vorangegangenen Prüfpakets ist separat SHA-256-geprüft. Alle Rechnungen lassen sich ohne Netzwerk ausführen.
