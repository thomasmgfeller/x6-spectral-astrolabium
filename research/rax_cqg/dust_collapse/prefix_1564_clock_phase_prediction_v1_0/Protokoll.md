# Vorregistrierung · Sechs Phasenwechsel im Staubuhrpaket

20. November 2026 · CST-DUST · Präfix 1564 · Version 1.0

**Primäre Vorhersage.** Wechselt die Phase innerhalb jedes der beiden bisherigen Staubuhrlappen sechsmal nach der unten festgelegten Maske, beträgt die inklusive skalare Randintensität höchstens **1 %** ihres Referenzwerts. Das gilt bei beiden Dichtezentren und für dieselben Historienkoeffizienten in Referenz- und Zielrechnung. Das Protokoll verwendet den gesamten zehnkomponentigen komplexen Koeffizientenraum als stärkeren Test. Jede bisher zulässige positive Historienverteilung ist darin enthalten.

Die Eingangsintensität als Funktion der Uhrzeit bleibt punktweise gleich. Der Test betrifft die kohärente Addition der Zeitbeiträge vor der Randnorm. Der physikalische Pilot P3 und die Wahl des Historienmasses sind eigenständige Entscheidungen. Der Stand dieser Vorregistrierung ist **REGISTERED / NOT_RUN**.

## Präparation und Geltungsbereich

Die Endtypen sind in der Reihenfolge 766, 926, 990, 1790, 2013, 2014, 2015, 5374, 5566, 27006 angeordnet. Es gelten der ursprüngliche skalare Gauss-Eingang, die geerbte gemeinsame skalare Randpaarung, sämtliche inneren Dichte- und Uhrmasse und die ursprüngliche Gravitationsphase. Die beiden vorgegebenen Dichtezentren sind 1/8 und 1/4. Auf jedem der zwei gleichphasigen rechteckigen Lappen ist die lokale Koordinate u bestimmt durch

$$
T_3=-2\Delta+h/16+u/32,\qquad h\in\{-1,+1\},\quad -1\le u\le1,\qquad
\Delta=\sqrt{2/(19\beta)},\quad\beta=4/\sqrt6.
$$

Für das Ziel wird die bisherige Amplitude in beiden Lappen mit demselben reellen Vorzeichen multipliziert,

$$
s(u)=\operatorname{sgn}(64u^6-80u^4+24u^2-1).
$$

An den sechs Nullstellen kann s=+1 gesetzt werden. Ihre Lage ist u=cos(kπ/7) für k=1,…,6. Von links nach rechts sind die Vorzeichen +, −, +, −, +, −, +. Es gibt keine neue Normierung der Lappen oder der ausgehenden Randzustände. Die Phase zwischen den beiden Lappenzentren bleibt gleich. Alle Eingangsintensitäten, die Lagen und Breiten sind identisch mit der Referenz.

## Eine primäre Grösse für alle Gewichte

Φⱼ ist der normierte skalare Ausgang im Endtyp j mit seiner geerbten Phase. Gᵢⱼ=⟨Φᵢ,Φⱼ⟩. Z⁰ⱼ und Zˢⱼ sind die komplexen Uhr-, Staub- und Gravitationsfaktoren im Referenz- bzw. im neuen Paket. Mit den Diagonalmatrizen D₀=diag(Z⁰ⱼ) und Dₛ=diag(Zˢⱼ) gilt für q≠0

$$
R_\rho(q)=\frac{q^\dagger D_s^\dagger G D_s q}{q^\dagger D_0^\dagger G D_0 q},\qquad
R_* = \max_{\rho\in\{1/8,1/4\}}\;\sup_{q\in\mathbb C^{10}\setminus\{0\}} R_\rho(q).
$$

Der Nenner ist positiv, da G positiv definit ist und alle archivierten |Z⁰ⱼ| von null getrennt sind. Die Norm wird im ursprünglichen Randsektor vor einer Endpostselektion gebildet. Eine spätere Normierung aller Ausgänge auf Eins würde die Prüfgrösse entfernen. Die einzelne Vorhersage lautet R* ≤ 1/100.

## Herleitung vor der Zielrechnung

Hält man alle anderen reellen Uhren und Dichten fest, ist der von u abhängige Wirkungsfaktor eine Phase f(u)=exp[i(au²+bu+c)]. Dichten, die der Referenzprüfer analytisch integriert hat, können hier mit ihrem positiven normierten Mass wieder eingesetzt werden. Für jeden Endtyp sind |a|≤Aⱼ und |b|≤Bⱼ in der archivierten dritten Kragenkoordinate bereits nach oben begrenzt. Es werden ausschliesslich diese Referenzgrenzen, die alten Betragsgrenzen und die alte skalare Gram-Schranke eingelesen.

Die Maske s ist das Vorzeichen des Chebyshev-Polynoms zweiter Art U₆. Sie löscht im gleichverteilten Lappenmittel jedes Polynom vom Grad höchstens fünf aus. Nach u=cos θ ist sin θ mal ein solches Polynom eine Linearkombination der Sinusfunktionen mit Frequenzen 1 bis 6. Das Vorzeichen von sin(7θ) ist zu all diesen Funktionen auf [0,π] orthogonal. Das normierte Mittel des Betrags des monischen Polynoms U₆/64 ist 1/64, da das Integral von |sin(7θ)| auf [0,π] gleich 2 ist.

Interpoliere f an den sechs Nullstellen. Der Rest ist das monische Knotenpolynom mal eine sechste dividierte Differenz, deren Betrag höchstens sup|f⁽⁶⁾|/6! ist. Die Simplex-Integralform der dividierten Differenz gilt auch für das komplexe f. Aus f(u+t)=f(u)exp[i(2au+b)t+iat²] erhält man damit

$$
\left|\tfrac12\int_{-1}^{1}s(u)f(u)\,du\right|\le C_j,
\qquad C_j=\frac1{64}\sum_{k=0}^3\frac{A_j^k(2A_j+B_j)^{6-2k}}{k!(6-2k)!}.
$$

Alle übrigen Uhren- und Dichtemittel im Faktor Zⱼ können für diese Abschätzung wiederhergestellt werden. Ihre normierten Gewichte sind positiv, und die übrigen Phasen haben Betrag eins. Einschliesslich beider gleichphasiger Lappen gilt |Zˢⱼ|²≤Cⱼ²/768, weil der Faktor eines Lappens 1/√3072 beträgt.

Der alte Prüfer berechnet g=3220693/5000000 als eins abzüglich der grössten oberen ausserdiagonalen Gram-Zeilensumme. Da die Diagonale eins ist, gilt gI ≤ G ≤ (2−g)I. Sei mⱼρ die archivierte positive Untergrenze für |Z⁰ⱼ|. Dann ist

$$
\sup_{q\ne0}R_\rho(q)\le\frac{2-g}{g}\max_j\frac{C_j^2}{768\,m_{j\rho}^2}.
$$

Die Bruchrechnung ergibt bei 1/8 höchstens 0,74283 % und bei 1/4 höchstens 0,74712 % (nach oben gerundet). In beiden Rechnungen bestimmt Typ 926 die konservative Schranke. Dies sind prognostische Obergrenzen aus alten Daten. Die neuen integrierten Amplituden und das tatsächliche Maximum bleiben bis zum Folgelauf offen.

[Referenzstudie auf GitHub](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/1638acd19961c840fb0b3d35135a947e4dba0f4e/research/rax_cqg/dust_collapse/prefix_1564_selection_v0_1) · [C. de Boor, Divided Differences, Genocchi-Hermite-Formel](https://pages.cs.wisc.edu/~deboor/sat/papers/2/2.pdf)

## Vorab festgelegte Auswertung

Im Folgelauf werden die Zielamplituden bei beiden Dichten und für alle zehn Endtypen direkt aus der unveränderten Wirkung berechnet. Ein zusätzlicher, getrennter Vorwärtslauf wurde zum Zeitpunkt der Festlegung nicht ausgeführt. Für jedes neue komplexe Z ist ein Fehlerkreis mit Radius höchstens 1/50000 vorgeschrieben. Die Einteilung in sieben Teilintervalle pro Lappen ist bindend. Die sechs exakten Nullstellen definieren das Ziel. Für die Quadratur werden sie mit rationaler Vorzeichenbisektion in Intervallen der Breite höchstens 2⁻⁵⁰ eingeschlossen. Das erneute Zusammenfügen aller sieben Segmente mit positivem Vorzeichen muss mit dem archivierten Referenzamplitudenkreis überlappen. Das kontrolliert Lagen, Masse und Normierung.

Für jeden Endtyp werden aus dem direkten Zielkreis sichere Betragsgrenzen lⱼ und uⱼ gebildet. Die alten Betragsgrenzen sind mⱼ und Mⱼ. Der festgelegte Auswerter setzt

$$
L_\rho=\max_j l_j^2/M_j^2,\qquad
U_\rho=\frac{2-g}{g}\max_j u_j^2/m_j^2.
$$

Die untere Schranke folgt aus den zehn Basisvektoren des deklarierten komplexen Testraums. Die obere folgt aus der Gram-Einschliessung für alle Linearkombinationen. Die konservative Einschliessung könnte bei einer Grenzentscheidung unentschieden bleiben. Die rein analytische Vorabschätzung ersetzt die neuen Eingaben für die Wertung nicht.

| Status des Folgetests | Vorab festgelegte Bedingung |
|---|---|
| PASS | Beide direkten oberen Grenzen liegen bei höchstens 1 %. |
| FAIL | Mindestens eine direkte untere Grenze liegt über 1 %. |
| HOLD | Sonst, insbesondere bei einer überschrittenen Fehlergrenze, fehlenden Eingangsfeldern oder einer misslungenen Referenzkontrolle. |

Nur ein vollständiger qualifizierter Lauf liefert eine Sachentscheidung. Ein formaler FAIL bezieht sich zunächst auf den deklarierten komplexen Testraum. Änderungen von Maske, Präparation, primärer Grösse oder Entscheidungsschwelle erfordern eine neue Version. Ein bestandenes Ergebnis an diesem Präfix wäre ein Test des endlichen kohärenten Modells und seines Rechenwegs. Für das physikalische Historienmass von P3 oder einen Bounce wäre gesonderte Evidenz nötig.

## Fehlerbudget für den vorbereiteten Folgelauf

Jedes Teilintervall wird in der Form u=p+hv mit v in [−1,1] integriert. Der Gaussgewichtsvektor wird mit h multipliziert. Die sieben positiven h summieren sich zu eins. Für die quadratischen und linearen Koeffizienten gelten A_neu≤Ah² und B_neu≤h(B+2A|p|). Der Prüfer fordert für jede Zelle B_neu≤B. Für reelle v bleiben die alten Schranken in allen anderen Koordinaten gültig. Daher addieren sich die sieben gewichteten Gauss-Fehler auf höchstens das alte Koordinatenbudget. Dasselbe gilt für die positive Betragsmajorante der Gitterauswertung bei Verwendung der sieben Vorzeichen.

Das alte Budget pro normiertem Lappen beträgt höchstens 8/32768 für die Integration und 1/5000 für die Auswertung. Es gelten dieselben binary64-Annahmen, Knoten-, Gewichts- und Phasenkontrollen. Die dyadischen Zellenmittelpunkte und Halbbreiten sind exakt darstellbar. Die zusätzliche gerundete affine Transformation der äusseren Knoten bleibt innerhalb der im alten Zeitfehlerbudget verwendeten 2⁻⁴³. Ein Versatz jeder Nullstelle um höchstens 2⁻⁵¹ verändert das normierte vorzeichenbehaftete Mittel bei Integrandenbetrag ≤1 um insgesamt höchstens 6·2⁻⁵¹. Für die zusätzlichen Multiplikationen mit h und das Addieren von sieben Zellergebnissen wird zusätzlich 10⁻⁸ pro normiertem Lappen reserviert. Mit 2/√3072 < 37/1000 liegt der gesamte Radius somit unter 1/50000. Er wird für Ziel- und Kontrollsumme verwendet. Die Referenz behält ihren archivierten Radius 1/60000.
