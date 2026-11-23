# Randpaarung beim gewöhnlichen Abschluss der Uhr 5

## Fragestellung und Ergebnis

Am Schnitt hinter Ereignis 11 speichert der gewöhnliche N15-Kern Uhr 5 noch. Die Vorgängerstudie fand dort eine phasenblinde Auslese der Uhr 11, wenn der Wert der Uhr 5 weitergegeben wird. Eine ergänzte kohärente Projektion P auf die konstante Mode beider Uhr-5-Pakete und I−P lieferte eine normierte Vergleichsmessung in der positiven Hilfsnorm. Nun prüfen wir erstmals in dieser Reihe die über die zulässigen Randdaten gemittelte Form am ersten Schnitt, der Uhr 5 von selbst integriert. Dabei kann die spätere Paarung selbst eine Norm auf dem frühen Zweimodenraum induzieren.

Der direkte Abschluss liefert eine positive Kandidatenform. Die beiden normierten Paketantworten haben darin eine Überlappung von mindestens 0,99998747 für jede nichttriviale gemeinsame positive diagonale Gewichtung der geprüften Randdaten. Eine Teilung nach dem erhaltenen Wert der Uhr 11 liefert normierte Anteile in dieser Form. Diese Anteile hängen bei kohärent geschlossener Dichte 12 numerisch schwach von einer späteren Pulswahl ab. Wird der Dichtewert bis zur Bildung der Gewichte aufgelöst mitgeführt, verschwindet die untersuchte Pulsabhängigkeit algebraisch. Diese Änderung des Randvertrags bedarf einer eigenen physikalischen Herleitung.

[Veröffentlichter N15-Stand und Vierphasenprüfung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/2334e0a04700184f865c941bdd74febd3fcd91d8/research/rax_cqg/dust_collapse/n15_uhr5_vierphasentest_v0_1) · [Gewöhnlicher Abschluss und zentrale Kontrollauswertung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/2334e0a04700184f865c941bdd74febd3fcd91d8/research/rax_cqg/dust_collapse/n15_natuerlicher_uhrzeiger_v0_1)

## 1. Die gewöhnlichen Spalten hinter 13

Fixiert sind Typ 2097151, markierte Dosis M=1, e=1/4, K=15/4, D=K(3/722)^(1/4) und u₆=3/8. Die inneren Uhren haben Yⱼ=Y₃+Kuⱼ. Die zwei flachen Pakete der Uhr u=u₅ sind um 1/4±s zentriert, s=1/(72DK²), mit Halbbreite h=1/16384. Der frühe Zuschauer z=u₄ liegt um 1/8, die Uhren v=u₁₁, a=u₁₂, b=u₁₃ und c=u₁₄ um 1/2, 5/8, 3/4 und 7/8, jeweils mit Halbbreite 1/64. Die frühen Dichtetags an 11 um 255/2048 und 257/2048 haben Halbbreite h.

Auf der Totalordnung (0,1,2,3,4,5,6,11,12,13,14,7,8,9,10) sind nach Schnitt 11 nur die Schichtpaare 5→12 und 5→13 von u₅ abhängig. Ihre Gewichte sind 16 und −8. Bei gegebenen feinen Dichten xⱼ=wⱼ/D ergibt sich der Faktor

    U(u)=exp{−i DK² [16 x₁₂(a−u)²−8 x₁₃(b−u)²]/38}.

An den Zentren aller Uhren und Dichten ist der Winkel von U am höheren Paket minus demjenigen am tieferen Paket exakt 1/912−1/1368=1/2736 rad. Bei beliebigen zulässigen Uhren und Dichten im untersuchten Fenster liegt die Differenz an den beiden Paketmitten zwischen 0,000053710 und 0,000684365 rad. Diese Aussage betrifft die zwei rechten Paare vor Integration. Der bereits durch die frühe Dichteänderung ausgelöste Phasenwechsel 1/311296 rad ist eine andere Observable.

Für j∈{4,5,6,11,12,13} sei cⱼ=−1/2−Σᵢ bᵢⱼ(Yⱼ−Yᵢ)²/38. Die bereits geschlossenen Zellbreiten lauten f₄=(z+u)/2, f₅=(3/8−z)/2, f₆=(v−u)/2 und f₁₂=(b−v)/2. Die zulässige frühe Dichte 11 liegt im Schnitt des Tagfensters mit [0,99 f₁₁,1,01 f₁₁], f₁₁=(a−3/8)/2. Sein Mittelpunkt und seine Halbbreite seien m und l. Bei leerem Schnitt ist der Ausgang null. Der Faktor l/h erhält die ursprüngliche Vorbereitung auch bei teilweiser Überlappung. Eine nachträgliche Normierung jedes Teilfensters würde die Ergebnisse ändern.

Hinter 13 trägt Uhr 5 keinen Speicherindex mehr. Für y=(v,a,b,x₁₃) ist die native Spalte Bₖ(y) das flache kohärente Mittel in z und im Paketoffset t von

    A(z,u;y) = (l/h) exp(iΘ) sinc(D l c₁₁)
                × ∏ⱼ fⱼ sinc(D fⱼ cⱼ/100),       j∈{4,5,6,12},
    Θ = D (Σⱼ fⱼ cⱼ + m c₁₁ + x₁₃ c₁₃).

Die Dichte 12 ist hier entsprechend dem ursprünglichen Vertrag auf Amplitudenebene über ihr gesamtes Jitterintervall integriert. Gemeinsame konstante Faktoren werden in allen Vergleichszweigen gleich behandelt. Unser numerisches Referenzmass ν ist gleichförmig in v,a,b und der Hilfsvariable c. Zu jedem (c,a) integriert es flach über den zulässigen x₁₃-Bereich mit f₁₃=(c−a)/2 und berücksichtigt seinen Jacobifaktor f₁₃. Die Variable c liefert ausschliesslich den Träger der noch offenen Dichte 13. Die Wirkung wird bis einschliesslich Ereignis 13 gerechnet. Es wird weder Vollständigkeit dieser Randpaarung über alle Ordnungstypen noch eine vollständige Spätentwicklung behauptet.

## 2. Schranke für sämtliche positiven diagonalen Gewichtungen

Auf den nichtleeren Tags sind alle sinc-Faktoren positiv, da ihre Betragsargumente höchstens 0,0007821 betragen. Die Rechnung in einschluss.py benutzt die vollständigen Paarlisten und die Ableitungen der Zellbreiten. Sie nutzt sinc(r)≥1−r²/6 und |sinc′(r)|≤|r|/3 aus der Cosinusdarstellung. Rationale Zahlen und auswärts gerundete 256-Bit-Intervalle ergeben für die pulsfreie Wirkung über die gesamten beschriebenen Fenster

    |∂ᵤ log A| ≤ 2,26735778,    |∂z Θ|/64 ≤ 0,00723948.

Der Faktor l/h ist unabhängig von u und z. Leere Tags werden vor jeder Division entfernt. Setze ρ=s+h, q=ρ sup|∂ᵤ log A| und δ=sup|∂z Θ|/64. Bei u₀=1/4 liegt der Betrag des kohärenten Referenzmittels B₀=E_z A(z,u₀;y) bei mindestens (1−δ²/2) E_z|A(z,u₀;y)|. Dies folgt durch Rotation auf die zentrale Phase und cos δ≥1−δ²/2. Der Quotient des Integranden am Paketpunkt und in dessen zentraler Referenz weicht höchstens exp(q)−1≤q/(1−q) von 1 ab. Nach beiden Integralen gilt daher

    |Bₖ/B₀−1| ≤ η = q/[(1−q)(1−δ²/2)] ≤ 0,002496729.

Insbesondere gilt Re(B₋*B₊)/|B₀|²≥1−2η−η²≥0,995000309. Bei Hᵢⱼ=∫ Bᵢ*Bⱼ dν ist für jede gemeinsame nichtverschwindende positive Diagonalgewichtung mit endlichen positiven Normen

    r=|H₋₊|/√(H₋₋ H₊₊) ≥ √[1−(2η/(1−η))²] ≥ 0,99998747.

Der Beweis projiziert B₊ orthogonal zur Geraden durch B₋ und verwendet ‖B₊−B₋‖≤2η‖B₀‖. Der reelle Kreuzterm behält auch nach dem gewöhnlichen Schliessen der zwei Uhren sein Vorzeichen. Das schliesst die Orthogonalisierung der ursprünglichen Arme durch gemeinsame positive skalare Gewichte über y aus. Auf dieser Festtyp-Referenz und bei der gewählten flachen kohärenten frühen Präparation werden keine Vorzeichen oder komplexen Endfilter eingebaut.

## 3. Was eine kohärente Ausgangspaarung leisten müsste

Normiere beide nativen Spalten einzeln und richte ihre relative Phase so aus, dass ihr Skalarprodukt r≥0 reell ist. Auf ihrer Spanne seien u und v die beiden Einheitsvektoren. Sollen sie unter einem positiven, invertierbaren Operator M orthogonal sein, müssen u+v und u−v gleich grosse M-Normen besitzen. In der Referenznorm sind ihre Normquadrate 2(1+r) und 2(1−r). Daraus folgt

    κ(M)=λmax(M)/λmin(M) ≥ (1+r)/(1−r).

Ist r=1, kann eine positive invertierbare Form die Kollinearität nicht ändern. Für r<1 ist die Schranke scharf. Gewichte die normierten Summen- und Differenzrichtungen mit 1/(1+r) und 1/(1−r). Die Eingangsarme werden dadurch orthogonal und gleich normiert. Die numerische SVD-Rechnung prüft die resultierende Identität direkt. Dieser Operator ist aus den zwei zu orthogonalisierenden Spalten konstruiert. Er ist damit ein mathematischer Vergleich für die Kosten einer solchen Änderung, keine unabhängige Herleitung der Paarung aus der Wirkung.

Die Fensterabschätzung ergibt κ≥159 617. Beim angegebenen flachen Ausgangsmass benötigt selbst diese optimal auf die Zweierspanne zugeschnittene Paarung κ≈42 410 837 (niedriger Tag) bzw. κ≈42 387 755 (hoher Tag). Dies sind Verhältnisse der Gewichte im Skalarprodukt. Der Quotient der singulären Werte der Amplitudenabbildung ist die Quadratwurzel. Numerisch wird 1−r² stabil über die direkte Residualnorm nach orthogonaler Projektion bestimmt. Die JSON-Datei enthält zur Kontrolle auch die maximale gemeinsame Erfolgswahrscheinlichkeit 1−r einer kontraktiven Filterung, welche zwei einzeln normierte Spalten mit gleicher Erfolgsnorm orthogonal abbildet. Diese theoretische Erfolgsquote bezieht sich auf den gewählten Filter, nicht auf P3.

## 4. Früher P-Zweig gegenüber dem gewöhnlichen Ausgang

Zerlege die Amplitude vor dem Puls in den frühen Faktor L an 4,5,6,11 und den rechten Faktor R an 12,13. Der frühe Vergleichsprojektor P lässt auf den zwei Uhr-5-Paketen nur die gemeinsam konstante Mode stehen. Bei jedem z und noch offenen x₁₁ folgt für Arm k nach der Fortsetzung

    Bₖ = E_z E_t (Lₖ Rₖ),
    Bᴾₖ = E_z[(E_t Lₖ)(E_t R₋+E_t R₊)/2],    Bᴿₖ=Bₖ−Bᴾₖ.

Die Dichte 11 kann für beide Rechenwege am selben Punkt integriert werden, da ihr Fenster und R unabhängig von der frühen Projektionswahl in Uhr 5 sind. Der Prüfer berechnet Bᴿ zusätzlich durch Integration der beiden Restpakete. Die vollständige Amplitudensumme stimmt für sämtliche Quadraturpunkte. Werden P und I−P tatsächlich als zwei unterscheidbare frühe Records registriert, addieren sich am Ende dagegen die Gewichte. Mit der vorgeschlagenen Endpaarung ist damit H′=(Bᴾ)†Bᴾ+(Bᴿ)†Bᴿ. Für gleiche Rohpakete und die vier Phasen (0, π/2, π, 3π/2) ergeben sich folgende Differenzen. Bezugsgrösse ist der feste Mittelwert der beiden einzelnen Armgewichte im unbeeinflussten Lauf, nicht die teils sehr kleine Norm eines destruktiv interferierenden Eingangs.

| Früher Tag | Δ bei 0 | Δ bei π/2 | Δ bei π | Δ bei 3π/2 |
|---|---:|---:|---:|---:|
| niedrig | −2,956×10⁻⁷ | +3,60821×10⁻⁴ | +2,952×10⁻⁷ | −3,60821×10⁻⁴ |
| hoch | −3,061×10⁻⁷ | +3,72257×10⁻⁴ | +3,058×10⁻⁷ | −3,72258×10⁻⁴ |

H′ und H sind somit numerisch verschieden. Ein allgemeines frühes Instrument darf die Statistik einzelner späterer Observablen verändern. Gegenstand dieses Tests ist die stärkere Hypothese, dass gerade das hier integrierte unbeeinflusste Endgewicht die physische Gesamtnorm für diesen Eingriff darstellt. Das Ergebnis ist ein Hindernis für diese konkrete Kombination aus Randform und frühem Gerät.

## 5. Eine vollständige späte Zweiteilung und ihre Pulsabhängigkeit

Uhr 11 ist hinter 13 noch als Koordinate v vorhanden. Durch Aufteilung ihres Fensters bei 1/2 entstehen positive Formen F_low und F_high, deren Summe H ist. Für Eingänge mit positiver H-Norm ist p_low=(ψ†F_low ψ)/(ψ†Hψ) eine normierte bedingte Wahrscheinlichkeit in diesem Kandidaten. Alle späteren Fenster im Referenzmass sind dabei einbezogen. Die Form ist ein Rücktransport einer Randstatistik; ihre operative Interpretation als früh gespeichertes Bit ist zu prüfen.

Beim niedrigen Dichtetag ergeben sich für die vier Rohphasen im pulsfreien Lauf 0,49995904, 0,49993615, 0,58752065 und 0,49998231. Bei Phase π beträgt bereits die gesamte Endnorm nur rund 4,0×10⁻⁶ des mittleren Armgewichts. Eine grosse Änderung eines normierten Anteils bei einem solchen Eingang bestimmt keine entsprechend grosse absolute Ereignisrate. Für den Plus- gegenüber dem Minuspuls ist die Differenz bei π rund 2,28×10⁻⁹ im niedrigen, rund 2,36×10⁻⁹ im hohen Tag. Beide unabhängigen Quadraturverfahren reproduzieren diese sehr kleinen Änderungen. Für diese integrierten Zahlen wird kein formaler Quadraturfehlereinschluss behauptet. Der Pulsvergleich ist eine Diagnose des vorgeschlagenen Auslesevertrags, kein Nachweis rückwärts gerichteter Signalübertragung.

## 6. Wo die Pulsspur entsteht

Setze die ursprüngliche rechte Verschiebung von Uhr 6 auf Δ=±1/(8√D). In den Beiträgen bis 13 sind ausschliesslich die Koeffizienten der Ziele 12 und 13 betroffen. Bei festen x₁₂ und x₁₃ multipliziert der Puls beide Pakete mit derselben Phase

    exp{i D[x₁₂ δc₁₂ + x₁₃ δc₁₃]},
    δcⱼ=b₆ⱼ [2 K(uⱼ−3/8) Δ−Δ²]/38,   (b₆₁₂,b₆₁₃)=(−9,16).

Dieser Faktor hängt weder von z noch von u₅ ab. Deshalb bleibt bei festem x₁₂ jede Intensität für beide Pulse und den Nullarm gleich, auch nach kohärenter Integration von z und u₅. Die x₁₃-Phase fällt aus den diagonal ausgewerteten Endgewichten. Wird zuerst x₁₂ kohärent integriert, können verschiedene x₁₂ innerhalb derselben Amplitude interferieren. Das ist die Stelle, an der eine Pulsabhängigkeit der getesteten Auswertung entsteht.

Als Vergleich teilen wir den ursprünglichen Dichtejitter in B gleich breite Klassen. Innerhalb jeder Klasse werden amplitudenrichtig die exakten flachen Mittel berechnet. Die Originalvolumina bleiben als gemeinsamer f₁₂-Faktor erhalten. Zwischen den Klassen werden die bedingten Gewichte mit den Klassenanteilen gemittelt, also mit 1/B. Diese explizite Vorschrift interpoliert zwischen genau der ursprünglichen kohärenten Mittelung bei B=1 und der Auswertung bei erhaltenem Dichtewert. Ein klassischer Registereintrag oder ein Dekohärenzmechanismus wäre für die Klassen zusätzlich zu begründen.

| Auswertung x₁₂, niedriger Tag, Phase π | p_low(Pluspuls) − p_low(Minuspuls) |
|---|---:|
| 1 Klasse, bisherige Vorschrift | +2,280×10⁻⁹ |
| 2 Klassen | +5,699×10⁻¹⁰ |
| 4 Klassen | +1,425×10⁻¹⁰ |
| x₁₂ aufgelöst, Gewichte gemittelt | exakt 0 aus der Phasenfaktorisierung |

Bei dieser Einstellung sinkt der Wert bei jeder der zwei Verdopplungen annähernd um Faktor vier. Drei endliche Werte sind kein universelles Skalengesetz. Die 144 direkten Kontrollen des gemeinsamen Phasenfaktors benutzen zwei andere Randkonfigurationen, beide Pulsrichtungen und drei Jitterwerte. Die Aussage bei aufgelöstem x₁₂ ist algebraisch für alle zulässigen Werte. Der Mittelwert über dieses feine Register ist eine Gegenrechnung und bislang keine aus der ursprünglichen Wirkung gefolgerte Version von P3.

### Wie weit ist die Dichtediagonalität notwendig?

Bei fixierten äusseren Werten ist der relative Operator der beiden Pulse auf der Dichtefaser, bis auf eine konstante Phase, Multiplikation mit exp(iλx₁₂). Hier liegt |λ| zwischen 0,10155705 und 0,115098. Der Phasendurchmesser des gesamten ursprünglichen Dichtebandes unterschreitet 0,0003237141 rad. Die Exponentialfunktion ist auf diesem Band injektiv. Verlangt man für **jede** komplexe Dichtewelle in L² dieses Bandes dieselbe beschränkte positive Endform M und Gleichheit der Gesamtnorm bei den beiden Pulsen, so folgt U₊†MU₊=U₋†MU₋. Damit kommutiert M mit dem relativen Multiplikator und seinen Spektralprojektoren. Wegen der Injektivität sind darunter sämtliche Projektionen auf messbare Dichtebereiche. Auf der skalaren Faser ist M folglich selbst Multiplikation mit einer beschränkten nichtnegativen Funktion. Bei zusätzlichen inneren Freiheitsgraden ist ein matrixwertiges Fasergewicht denkbar. Auf der kontinuierlichen skalaren Faser hat ein von null verschiedener Multiplikator unendlichen Rang. Dies erklärt, weshalb eine endliche Klassenbildung das universelle Kriterium nicht garantiert. Der Schluss setzt freie Dichtewellen und gemeinsame faserweise Norminvarianz voraus. Vier geprüfte Präparationen oder die Gleichheit eines einzelnen normierten Quotienten reichen dafür nicht.

Die gewöhnliche kohärente Reduktion bei festen übrigen Daten hat nur die lineare Zeile h↦∫h(x) exp(i D c₁₂ x)dx. Beispielsweise ergibt eine in zwei gleich breite Hälften aufgeteilte Vorzeichenwelle mit entgegengesetzter Wirkungsphase das Integral null bei positiver feiner L²-Norm. Aus dieser einzelnen Zahl kann eine spätere lineare Fortsetzung die verlorene Dichteinformation für beliebige Eingangswellen nicht wiederherstellen. Eine Erklärung über reale Records muss untersuchen, ob die Dichte schon vor der Reduktion an ein noch vorhandenes Feld oder an unterscheidbare Ordnungszweige koppelt. Der Beweis schliesst einen solchen Mechanismus in einem grösseren Zustandsraum nicht aus.

[Spektralsatz und kommutierende Spektralprojektoren, Dana Williams](https://www.math.dartmouth.edu/~dana/bookspapers/ln-spec-thm.pdf)

## Rechenkontrollen und Reichweite

Die strengen Fenstergrenzen stammen aus einschluss.py. Die numerische Hauptrechnung verwendet in jeder Achse sechs Gauss-Legendre-Knoten. Jede Zeigerhälfte und jedes durch die Dichtefenster-Schnittpunkte getrennte u₁₂-Teilintervall werden separat integriert. Die zweite Rechnung verwendet sieben Clenshaw-Curtis-Knoten, die anders erzeugte Paarliste und eine Taylor-Auswertung der symmetrischen Dichtemittel. Für den Klassenvergleich sind die Ordnungen fünf und sechs. Die Integration für den vollständig aufgelösten Jitter benutzt fünf zusätzliche Gaussknoten. Die unabhängige Kontrolle des pulsfreien Spezialfalls und der beiden Pulsvorzeichen gegen die publizierten zentralen Interferenzbalancen ist in verifizieren.py enthalten. Die Quelldateien sind mit Git-Stand und SHA-256 identifiziert. Die lokalen Prüfpläne besitzen keinen externen Zeitstempel.

Die physische frühe Randkopplung, die Herkunft einer positiven Dichtepaarung und die unabhängige Masseneichung bleiben offen. Alle 60 physischen P3-Einträge stehen auf NOT_RUN.
