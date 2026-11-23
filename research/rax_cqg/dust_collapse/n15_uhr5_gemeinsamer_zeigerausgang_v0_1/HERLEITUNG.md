# Kann Uhr 11 die relative Phase der Pakete an Uhr 5 früh anzeigen?

## Der Schnitt und die zwei untersuchten Ausleseregeln

Wir arbeiten auf dem in PR 363 benutzten N15-Typ 2097151 bei Dosis M=1 und e=1/4. Für das Staubinnere gilt K=15/4, D=K(3/722)^(1/4) und Yⱼ=Y₃+Kuⱼ. Hinter Ereignis 11, vor dem rechten Puls, speichert die ursprüngliche zeitliche Verklebung die Uhren (4,5,6,11). Die Uhr 5 wirkt noch in den Paaren 5→12 mit Gewicht 16 und 5→13 mit Gewicht −8. Auslesen eines Uhrfensters und kohärentes Summieren über die gespeicherte Uhr sind verschiedene Operationen.

Als möglichen Zeiger wählen wir die vorhandene Uhr v=u₁₁. Ihr ursprüngliches Fenster [1/2−1/64,1/2+1/64] wird in zwei Hälften geteilt. Es gilt u₆=3/8. Die Zuschaueruhr z=u₄ liegt in [1/8−1/64,1/8+1/64]. Bei der numerischen Auswertung wird z als Randwert weitergegeben und über seine Intensitäten gemittelt. Die Uhr 5 liegt in den flachen, kohärent präparierten Paketen I₋ und I₊ mit Mitten 1/4±s, s=1/(72DK²), und Halbbreite h=1/16384. Die Bedingung x=w₁₁/D bezeichnet die Dichtepräparation. Die numerischen Tabellen verwenden abwechselnd 255/2048 und 257/2048. Der Beweis gilt sogar auf dem gesamten Intervall zwischen den äusseren Grenzen beider Dichtepakete. Die beiden Dichtepräparationen werden nicht als Messergebnisse gezählt. Das spätere, noch offene Band f₁₁=(u₁₂−u₆)/2 wird früh weder ausgewertet noch für die Einstellung des Zeigers benutzt. Für alle betrachteten frühen Werte existieren zulässige Fortsetzungen, etwa mit u₁₂=5/8. Weitere später auferlegte positive Selektionsgewichte in den betrachteten gemeinsamen Zeigervariablen sind von der Vorzeichenschranke erfasst.

Aus der eingefrorenen Wirkung folgt cⱼ=−1/2−Σᵢ bᵢⱼ(Yⱼ−Yᵢ)²/38. Nach exakter flacher Integration über die ursprünglichen Dichtejitter an 4, 5 und 6 lautet die einlaufende Spalte bei u=u₅

    L(u;y) = f₄ f₅ f₆ ∏ⱼ sinc(rⱼ) exp(i θ),
    rⱼ = D fⱼ cⱼ/100,    θ = D[Σⱼ fⱼ cⱼ + x c₁₁],    y=(z,v,x).

Summe und Produkt laufen hier über die drei bereits abgeschlossenen Zellen. Ihre Breiten sind (z+u)/2, (3/8−z)/2 und (v−u)/2. Frühe Beiträge des äusseren Kragens sowie der auf diesem Typ faktorisierte Skalarsektor sind beiden Armen gemeinsam. Positive globale Integrationskonstanten sind unterdrückt. Die Konstruktion behält diese gemeinsame Konvention in allen Zweigen bei.

[PR 363, Vierphasentest und Quellstand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/2334e0a04700184f865c941bdd74febd3fcd91d8/research/rax_cqg/dust_collapse/n15_uhr5_vierphasentest_v0_1) · [Veröffentlichte frühe Amplituden](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/2334e0a04700184f865c941bdd74febd3fcd91d8/research/rax_cqg/dust_collapse/n15_uhr5_randimpuls_v0_1/HERLEITUNG.md)

## Wenn Uhr 5 erhalten bleibt

Auf dem positiven Hilfsraum mit getrennten Trägern führt das Ablesen einer v-Hälfte B auf die Ergebnisform

    Fᴮₐᵦ = δₐᵦ ∫ᴮ Eₜ |Lₐ(t;y)|² dν(y).

Eₜ ist das normierte flache Mittel auf [−h,h], Lₐ(t;y)=L(1/4±s+t;y). Für den numerischen Referenzfall sind z und v gleichverteilt und x fest. Der Gesamtform entspricht die Diagonalmatrix G=ΣᴮFᴮ. Für gleiche, in G normierte Armgewichte ergibt die untere Hälfte in allen vier Phasen 0,468790105. Ihre absolute Höhe ist eine Aussage zur angegebenen Hilfspaarung. Die Phasenblindheit folgt algebraisch aus den disjunkten Trägern und bleibt bei gemeinsamen positiven klassischen Gewichten erhalten.

## Wenn Uhr 5 vorzeitig zu einer gemeinsamen Amplitude summiert wird

Definiere bₐ(y)=EₜLₐ(t;y). Dieser Vorschlag ersetzt die gespeicherten Uhrwerte durch denselben kohärenten Ausgang. Für eine beliebige positive skalare Gewichtung ν der sichtbaren Variablen ergibt sich die gemeinsame Form Hₐᵦ=∫bₐ* bᵦ dν. Hier bezeichnet * komplexe Konjugation. Eine normerhaltende vollständige Auslese zweier orthogonaler Eingänge verlangt H₋₊=0, auch bei anderer positiver Normierung der beiden Arme. Prüfen lässt sich diese notwendige Bedingung ohne Kenntnis eines späteren Erfolgs.

Setze L₀=L(1/4;y). Die endlichen Pakete liegen innerhalb von 0,001098391 um diese Mitte. Für alle erlaubten Zuschaueruhrwerte, Zeigerwerte und Dichten ergibt die nach aussen gerundete Intervallrechnung |rⱼ|≤0,000526 und |∂ᵤ log L|≤2,2954423. Sie verwendet die vollständigen Paarlisten und deren Ableitungen, f′=(1/2,0,−1/2) sowie sinc(r)≥1−r²/6 und |sinc′(r)|≤|r|/3, die aus dem Cosinusintegral folgen. Die positive Amplitude erlaubt eine stetige Wahl des Logarithmus in u. Für q=sup|∂ᵤ log L|·(s+h)<1 ist |L/L₀−1|≤exp(q)−1≤q/(1−q). Diese Schranke gilt auch nach dem Paketmittel. Mit η≤0,002527666 folgt

    Re(b₋* b₊)/|L₀|² ≥ 1−2η−η² ≥ 0,99493827.

Alle nichtleeren Ausgänge mit positivem Gewicht haben deshalb denselben positiven Realteil ihres Kreuzterms. Keine Zerlegung oder positive skalare Umgewichtung dieses gemeinsamen Zeigers kann den zum Normerhalt erforderlichen Gegenbeitrag erzeugen. Eine beliebige feste Umphasung der beiden Pakete rotiert alle diese Beiträge gemeinsam.

Auch die quantitative Nähe zur Proportionalität lässt sich über jede nichtverschwindende positive, endliche Ergebnisgewichtung absichern. Aus ‖b₊−b₋‖≤2η‖L₀‖ und ‖b₊‖≥(1−η)‖L₀‖ folgt für den Abstand von b₊ zur Geraden durch b₋

    r = |H₋₊| / √(H₋₋H₊₊) ≥ √[1−(2η/(1−η))²] ≥ 0,999987156.

Für die beste gemeinsame positive Normierung gilt min_c ‖cH−I‖=(λmax−λmin)/(λmax+λmin)≥r in Operatornorm. Die letzte Ungleichung folgt aus der Eigenwertformel der positiven 2×2-Matrix und gilt auch nach separater Skalierung der Eingangsarme. Wird nur dieser gemeinsame Ausgang als Teilergebnis cH≤I behalten, beträgt sein mittleres Gewicht auf dem gleichwahrscheinlichen Gemisch der zwei orthonormalen Arme höchstens 1/(1+r)≤0,500003211. Diese Obergrenze betrifft diese Form der Summation, nicht die Effizienz eines physikalisch bestimmten Detektors. Die beiden numerischen Dichtepräparationen liefern unter flacher Gewichtung jeweils r≈0,999999946. Die Schranke erfasst ausschliesslich positive, diagonal ausgewertete Zeigergewichte. Eine kohärente Projektion auf Überlagerungen verschiedener v, eine geänderte Kopplung oder eine andere physikalische Paarung ist eine andere Klasse.

## Ein vollständiger Vergleich unter positiver Hilfsnorm

Wir belassen nun beide Uhrintervalle als Ausgangskoordinaten. Bei festem y projiziere P auf die Funktion, die auf ihrer Vereinigung konstant ist. Die Hilfsnorm ist die Summe beider normierter Paketintegrale. Die normierte konstante Mode hat daher auf jedem Paket den Wert 1/√2. Der zweite Ausgang ist I−P und enthält auch alle innerhalb der Pakete nichtkonstanten Anteile. Für beide Zeigerhälften folgt genau

    Fᴮ_P = Hᴮ/2,    Fᴮ_R = Fᴮ−Hᴮ/2,    Fᴮ_P+Fᴮ_R=Fᴮ.

Die Gegenrechnung integriert die Restamplitude selbst. Für den Eingangsarm a hat sie auf dem Ausgangspaket k die Form δₖₐ Lₐ(t;y)−bₐ(y)/2. Damit lassen sich Positivität, Viertelphasen und Vollständigkeit ohne numerische Subtraktion nahe beieinanderliegender grosser Wahrscheinlichkeiten kontrollieren. Die physikalische Annahme liegt im projizierenden Eingriff über zwei getrennte Uhrfenster und in der verwendeten Ausgangspaarung. Der ursprüngliche N15-Übergang gibt die Amplituden L und das identische Weiterreichen von u vor. Eine physische Realisierung von P oder I−P ist darin offen. Auch die frühe Eingangsgrammatrix G ist hier eine durch die positive Hilfsnorm zurückgezogene Vergleichsform. Die Hilfsrechnung ist keine Herleitung der physikalischen Zustandsnorm.

Nach Division jedes Arms durch √Gₐₐ lauten die vier Wahrscheinlichkeiten des P-Ausgangs (auf beiden v-Hälften zusammen)

| Frühe Dichte x | 0 | π/2 | π | 3π/2 |
|---|---:|---:|---:|---:|
| 255/2048 | 0,9999998022 | 0,5004104274 | 0,0000001954 | 0,4995895702 |
| 257/2048 | 0,9999998009 | 0,5004120378 | 0,0000001967 | 0,4995879598 |

Die Werte im Gegenausgang ergänzen jede Spalte für jede Präparation auf 1. Für die niedrige Dichte liefern die beiden Zeigerhälften im P-Ausgang die normierten Kreuzterme 0,2343949613−0,0001893972i und 0,2656048421−0,0002210314i. In der Restprojektion werden die jeweils entgegengesetzten Werte direkt gefunden. Das zeigt, wie ein kompensierender Beitrag aussehen kann und welche zusätzliche Operation ihn hervorbringt. Der grosse Unterschied zwischen den Eingangsphasen 0 und π beschreibt die Empfindlichkeit der gewählten Projektion gegenüber der präparierten Phase. Er misst nicht die Zuordnungsgüte zwischen den beiden eng benachbarten Dichten.

[Normierte Messungen und positive Ergebnisformen, Watrous, Kapitel 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf)

## Warum eine frühe Summenzeile den gewöhnlichen Anschluss verliert

Für diesen separaten Gegenzeugen fixiere v=1/2, u₁₂=5/8, u₁₃=3/4 und x₁₂=1/8. Sie liegen innerhalb der ursprünglichen Zellpräparation. Die frühen Ergebnisse haben diese Festlegung nicht verwendet. Unter der unverschobenen Fortsetzung kommt im Schritt bis 12 als einziger von u₅ abhängiger rechter Phasenfaktor U(u)=exp[−i A(5/8−u)²] hinzu, A=(16/38)DK²/8. Gemeinsame rechte Faktoren werden bei fixierten Zuschauern entfernt. Verglichen werden die frühe Zeile b und die nach diesem gewöhnlichen Schritt gleich gebildete Zeile b′ₐ=Eₜ(Lₐ Uₐ). Beide auf alle Zweimodeneingänge aus einer einzigen komplexen linearen Zusammenfassung zurückzugewinnen, erfordert Proportionalität.

Die Determinante b₋b′₊−b₊b′₋ ist das doppelte Paketmittel von L₋L₊(U₊−U₋), mit unabhängig integrierten Pakettoffsets. Die Differenz der Winkel von U ist positiv, an den Mitten exakt 1/912 rad und überall zwischen (1−2h/d)/912 und (1+2h/d)/912, d=2s. Nach Rotation um die gemeinsame Zentralphase und Division durch L₀² enthält der Integrand den Faktor 2 sin(Δθ/2). Der verbleibende Realteil ist mindestens 1−2η−η²−A[(3/4)(s+h)+(s+h)²]. Dazu verwendet man |exp(iε)−1|≤|ε|. Mit sin(t)≥t−t³/6 ergibt sich für den gesamten ausgewiesenen frühen z- und x-Bereich auf dieser Fortsetzung

    |b₋b′₊−b₊b′₋| / |L₀|² ≥ 0,001026153.

Damit ist der Rang der beiden Zeilen auf dem festgelegten Zweimodenraum genau zwei. Für drei z und die beiden Dichtemitten ergibt die numerische Gegenrechnung rund 0,00109646. Ein Eingang, der im frühen Summenausgang verschwindet, kann in der späteren linearen Auswertung also einen Beitrag liefern. Das Resultat betrifft die Erhaltung beider linearer Antworten für jeden Eingang auf der angegebenen Faser. Es belegt keine frühe Beobachtung des späteren Uhrwerts und keine allgemeine physische Hilbertraumdimension.

## Stand und Reproduktion

Der ursprüngliche frühe Zeiger ist in der geprüften Hilfspaarung phasenblind. Der untersuchte gemeinsame Amplitudenausgang hat deutliche Interferenz, scheitert jedoch als vollständiges Instrument auf orthogonalen Eingängen. Sein klassisches Umgewichten kann diesen Fehler über die angegebenen vollen Fenster nicht beheben. Eine zusätzliche kohärente Projektion mit Restkanal erfüllt die Bilanz im Hilfsmodell. Ihre physikalische Randkopplung, die positive physische Paarung und die unabhängige positive Masseneichung sind offen. Alle 60 physischen P3-Prüfpunkte führen NOT_RUN.

Der rationale Beweis und die numerischen Rechnungen sind getrennt. Der erste verwendet exakte Brüche und auswärts gerundete 256-Bit-Intervalle. Die numerischen Referenzwerte beruhen auf Gauss-Legendre mit je 14 Punkten und analytischen Dichteintegralen. Eine zweite Auswertung benutzt Clenshaw-Curtis mit je 15 Punkten, eine getrennt aufgebaute Paarliste und direkte Gaussquadratur mit sechs Knoten über jeden Dichtejitter. Beide prüfen die Wahrscheinlichkeiten zudem einmal als Matrixform und einmal direkt aus den vier Ausgangswellen. Die JSON-Dateien unterscheiden die streng nach aussen geschlossenen Schranken und die gerundeten Quadraturresultate. Die zwei lokalen Pläne enthalten keinen externen Zeitstempel.
