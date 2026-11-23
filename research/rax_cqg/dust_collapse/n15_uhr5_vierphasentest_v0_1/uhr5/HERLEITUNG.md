# Vier frühe Phasen und die physikalische Randpaarung

## Frage und Referenz

Kann die gekoppelte Staubwirkung am Schnitt hinter Ereignis 11 ein frühes phasenempfindliches Ergebnis an Uhr 5 liefern? Alle Aussagen über die Wirkung betreffen N15, Typ 2097151, M=1, e=1/4, die gemeinsame feste Faser mit u₁₁=1/2 und den Präparationsvertrag von PR #362. Die Berechnung verwendet weder den Puls an Uhr 6 noch einen späteren Detektorausgang. Die physische Paarung und ihre Nullrichtungen sind in diesem Sektor offen.

[Ausgangsrechnung, eingefrorener Git-Stand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/652283ff1c1265a02912206825a6be5b8dfcf523/research/rax_cqg/dust_collapse/n15_uhr5_fenstertransport_v0_1/HERLEITUNG.md) · [Trägererhaltung am frühen Schnitt](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/652283ff1c1265a02912206825a6be5b8dfcf523/research/rax_cqg/dust_collapse/n15_uhr5_randimpuls_v0_1/HERLEITUNG.md)

## Phasenspektren des frühen Wirkungsfaktors

In der ursprünglichen Totalordnung steht zwischen 5 und 11 genau das Ereignis 6. Somit hat das Paar 5→11 das Gewicht −9. Bei fester sonstiger Uhrbelegung lautet der einzige Term, der zugleich von der Dichte x=w₁₁/D und der Uhr u=u₅ abhängt,

    S₅,₁₁ = (9/38) D K² x (1/2−u)²,    K=15/4, D=K(3/722)^(1/4).

Alle weiteren frühen Terme sind für die gemischte Differenz in u und x ohne Beitrag. Dies gilt auch für die vorherigen u-abhängigen Dichtevolumina, die bei der Variation von x unverändert bleiben. Der Test variiert beide Grössen in der vollständigen linken Staubwirkung und vergleicht die Ergebnisse mit dem Einzelterm an zwölf rationalen Kontrollkonfigurationen. Die allgemeinen Aussagen folgen aus der Paarliste und dem Polynom.

Die beiden Dichtemitten sind xₐ=255/2048 und xᵦ=257/2048. Die Uhrpakete liegen in I₋, I₊ um 1/4∓d/2 mit derselben Halbbreite h=1/16384 und d=1/(36 D K²). Das relative Phasenprofil der beiden Dichtemitten ist bis auf eine armeinheitliche Phase

    ω(u) = (9/38) D K² (xᵦ−xₐ) (1/2−u)².

Im Zentrum gilt ω(u₋)−ω(u₊)=1/311296 rad. Der Minusarm hat den grösseren Phasenwinkel. Für beliebige u₋∈I₋ und u₊∈I₊ liegen die exakten Extrema bei (1∓2h/d)/311296. Das folgt aus der strikten Monotonie und den einander zu- bzw. abgewandten Intervallenden. Der exakte rationale Aussenabschluss im Prüfer gibt

    3,023369 × 10⁻⁶ < ω(u₋)−ω(u₊) < 3,401385 × 10⁻⁶ rad.

Die Phasenbilder auf dem Einheitskreis sind kompakt und disjunkt. Die geringe Trennung ist mathematisch strikt, für eine ungefähre Isometrie folgt daraus ohne Fehlerbudget keine numerisch robuste Orthogonalität. Dies ist eine Aussage über zwei Dichtemitten und die beiden vollständigen Uhrpakete bei gemeinsam fixierten übrigen Randwerten. Beim Integrieren weiterer Randvariablen können sich die Annahmen an eine gemeinsame Paarung ändern.

## Welche zusätzliche Annahme Orthogonalität erzwingt

Sei Uₓ die Multiplikation mit exp(iS₅,₁₁) auf dem Hilfsraum der beiden Paketintervalle. Betrachte beschränkte positive semidefinite Formen mit Gram-Operatoren Gᵢ und Gₒ auf diesen Fasern. Fordert man für BEIDE Dichtemitten dieselbe Ein- und dieselbe Ausgangspaarung sowie Isometrie des jeweiligen reinen Phasenfaktors, so muss Uₐ†GₒUₐ=Gᵢ=Uᵦ†GₒUᵦ gelten. Also kommutiert Gₒ mit W=Uᵦ Uₐ†. Der Projektor auf jedes der getrennten spektralen Pakete ist eine Funktion von W. Daher ist P₋GₒP₊=0. Weil Uₐ die Träger erhält, gilt ebenso P₋GᵢP₊=0. Dieses Argument braucht weder eine diskrete Approximation des Uhrpakets noch einen Integralkern für G. Auf einem Nullraum ist zusätzlich der physikalische Quotient zu bilden. Für eine positive Wahrscheinlichkeit muss die jeweilige Präparation dort eine positive Norm haben.

Auf der Zweipunktreduktion an den Paketmitten lässt sich die Empfindlichkeit exakt angeben. Liegen die beiden Isometrieresiduen in Operatornorm unter εₐ und εᵦ, dann folgt durch Subtraktion der Nebendiagonale

    2 sin(1/(2·311296)) |(Gₒ)₋₊| ≤ εₐ+εᵦ.

Der Verstärkungsfaktor beträgt rund 311 296. Bei auf eins normierten Diagonalen wäre eine Summe der Residuen unter 3,21 × 10⁻⁸ hinreichend, um einen relativen Kreuzterm von 1 % auszuschliessen. Diese skalare Fehlerabschätzung gilt an den beiden Paketmitten. Ein Fehlerbudget für die physikalische Dynamik und eine entsprechende Operatornormschranke für die vollständigen Intervalle bleiben offen.

Der ursprüngliche Kern legt diese gemeinsame Isometrie der zwei bedingten Faktoren nicht fest. Die Dichten sind Präparationsalternativen. Eine physische Entwicklung könnte nur nach Integration über Dichten und weitere Freiheitsgrade normiert sein. Selbst eine Isometrie jeder Alternative erlaubt unterschiedliche Ausgangspaarungen. Für jedes positive G mit Kreuzterm kann man beispielsweise Gₒ(x)=Uₓ G Uₓ† setzen. Dann gilt die Isometrie identisch, auch wenn der Eingangskreuzterm von null verschieden ist. Als ausführbare Illustration verwendet der Prüfer die Zweipunktdiskretisierung an den Paketmitten und G₋₊=1/2. Die beiden ausgehenden Kreuzterme unterscheiden sich im Betrag ihrer Differenz um sin(1/(2·311296)). Der allgemeine Gegenbeweis durch Konjugation gilt ebenso für beschränkte positive Formen über den vollständigen Paketen. Die Konstruktion weist die Freiheit nach und legt keine physikalische Paarung fest.

[Satz über Spektralprojektoren beschränkter normaler Operatoren](https://www.math.dartmouth.edu/~dana/bookspapers/ln-spec-thm.pdf) · [Frühere N15-Prüfung der Isometrieannahme, Abschnitt 4](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/652283ff1c1265a02912206825a6be5b8dfcf523/research/rax_cqg/dust_collapse/n15_schnitttransport_randpaarung_v0_1/HERLEITUNG.md)

## Physisch normierter Vierphasentest

Für Rohpakete e₋,e₊ sei vφ=(e₋+exp(iφ)e₊)/√2. Schreibe Nφ=vφ†Gvφ für die Präparationsnorm und wφ=vφ†Fvφ für die Ergebnisform. Ein zulässiger Effekt erfüllt 0≤F≤G und die Wahrscheinlichkeit ist pφ=wφ/Nφ für Nφ>0. Ein vollständiges binäres Instrument muss beide Formen F und G−F realisieren. Für eine Nullrichtung von G verschwinden beide positiven Formen.

    F₋₊ = [(N₀p₀−Nπpπ) − i(Nπ/₂pπ/₂−N₃π/₂p₃π/₂)]/2.

Einsetzen von N allein in dieselbe Differenz liefert G₋₊. Für physisch orthonormale Pakete sind alle Nφ=1. Falls die Normen variieren, ist F₋₊ eine Matrixkomponente in der gewählten Rohbasis. Ein physisch konstanter Münzeffekt F=cG hat dort beispielsweise den Kreuzterm cG₋₊. Für die vorgegebene Familie ist die Wahrscheinlichkeit genau dann konstant, wenn F₋₊=cG₋₊ mit c=(F₋₋+F₊₊)/(G₋₋+G₊₊), sofern alle Präparationen definiert sind. Die physische Orthogonalisierung darf die Bedeutung der beiden disjunkten Paketpräparationen nicht stillschweigend ändern.

| Kontrolle (Reihenfolge 0, π/2, π, 3π/2) | Wahrscheinlichkeiten | Ergebnis |
|---|---|---|
| G=I, Auslesen des Minus-Paketträgers | 1/2, 1/2, 1/2, 1/2 | Phasenblind, auch nach Uₓ |
| G=I, Diagonale des Vergleichseffekts 1/2, F₋₊=(1+i)/8 | 5/8, 3/8, 3/8, 5/8 | Beide Quadraturen korrekt. Dieser Vergleichseffekt ist zusätzlich gewählt. |
| G mit Diagonale 1 und G₋₊=1/2, F=diag(1/2,0) | 1/6, 1/4, 1/2, 1/4 | Rohform F₋₊=0. Wer die vier Nφ=(3/2,1,1/2,1) ignoriert, erhält scheinbar den Betrag 1/6. |
| Dasselbe G, F=G/2 | 1/2, 1/2, 1/2, 1/2 | Konstante Auslese trotz F₋₊=1/4 in der Rohbasis. |

Für die dritte Zeile sind beide Formen positiv, wie etwa det(G−F)=1/4 und die positiven Diagonalen zeigen. Sie ist ein Beispiel für normierte Zustandsstatistik und beansprucht keine Realisierung durch den Staubkern.

## Vollständige trägertreue Messung im Zweimodenraum

Wir betrachten eine beliebige Anzahl von Krausoperatoren Kⱼ=diag(aⱼ,bⱼ), die je eine unveränderte Paketform pro Arm mit einem komplexen Skalar multiplizieren. Für das vollständige Instrument gelte vor und nach dem Eingriff dieselbe Gram-Matrix G mit positiven diagonalen Normen. Aus Σ Kⱼ†G Kⱼ=G erhält man Σ|aⱼ|²=Σ|bⱼ|²=1. Für G₋₊≠0 folgt zusätzlich Σ conj(aⱼ)bⱼ=1 und daher Σ|aⱼ−bⱼ|²=0. Jedes Ergebnis ist in diesem Fall proportional zu G, seine Wahrscheinlichkeit ist zustandsunabhängig. Für G₋₊=0 sind die Ergebnisformen diagonal und damit phasenblind auf den beiden ursprünglichen Paketen. Ein frei gewählter positiver Kreuzterm allein macht dieses vollständige Instrument also in keinem der beiden Fälle zu einer frühen Phasenmessung. Das gilt im Zweimodenmodell unter der genannten Vollständigkeit, nicht für beliebige dynamisch gekoppelte Apparateräume.

## Entscheidung

Die ursprüngliche Wirkung liefert auf der angegebenen frühen Faser eine streng getrennte, dichteabhängige Phasenprägung. Unter den ausdrücklich geprüften Paarungs- und Trägerannahmen fehlt ein früher phasenempfindlicher Messeffekt. Der allgemeine physikalische Vierphasentest bleibt mangels hergeleiteter Ergebnisformen und Normen offen. Ein verbleibender Ansatz ist ein aus der gemeinsamen Randwirkung hergeleiteter Übergang zwischen den Paketträgern samt positivem vollständigem Instrument. Die unabhängige positive Masseneichung steht ebenfalls aus. Alle 60 physischen P3-Prüfpunkte im eingefrorenen Quellregister führen NOT_RUN.

Für einen künftigen konkreten Kopplungskandidaten T und ein früh ausgelesenes Zeigerereignis Q ist die direkt prüfbare Grösse die Überlappung der beiden Ausgangspakete im selben Zeigerereignis. Bei ausgangsseitig physischer Norm und orthogonalem Zeigerprojektor gilt F₋₊=⟨T e₋,Q T e₊⟩. Ist T vollständig isometrisch und sind die Eingangsarme physisch orthogonal, muss die Summe dieser Überlappungen über alle Zeigerereignisse null sein. Ein einzelner von null getrennter Beitrag wäre deshalb zusammen mit seinem kompensierenden Gegenbeitrag, dem vollständigen Instrument und den Eingangsnormalisierungen aus der Randwirkung herzuleiten. Für den bereits faktorisierten Skalarsektor auf diesem festen Typ entsteht eine solche Überlappung aus einer blossen Phasenmultiplikation und einem unabhängigen Zeiger nicht.
