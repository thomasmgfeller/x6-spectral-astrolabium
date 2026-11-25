# Kohärente Schnittladung auf N15 und Test der markierten Ruhemasse

25. November 2026 · Typ 1767356 · Rechenstudie im endlichen Staubmodell

Die positive Ladung aus PR #375 bleibt für eine gleichphasige Feldpräparation und eine gemeinsame konstante Endauslese auch nach kohärenter Summation innerhalb der 2-%-Transporttoleranz. Bei voller Breite ist die relative komplexe Abweichung auf jedem der 15 Schnitte kleiner als 1,11 × 10⁻⁹. Ein kleiner Randterm ist nachweisbar. Die Interpretation der stationären Dichten als Verweildauern eines positiven markierten Staubstroms scheitert am letzten inneren Ereignis. Beide Resultate betreffen die gewählte endliche Präparation. Der physische P3-Test steht auf HOLD, alle 60 Einträge auf NOT_RUN.

## Paket und Messgrösse

Die unveränderten Quelldateien stammen vom Merge-Commit ea05b04. Das innere Gebiet hat die Ereignisse (4,5,6,11,12,13,14). Gerechnet wird auf dem reellen stationären Zweig mit Zukunftsdichte 1/64 und Versatz e in [1/6−2⁻²²,1/6+2⁻²²]. Die vier Vergangenheitsdichten sind hier gemeinsam auf 1/8 fixiert. Die inneren Uhren und Dichten schwanken unabhängig um ihre vom jeweiligen e abhängigen stationären Werte. Ihre Halbbreiten sind hᵧ=(4−e)/(64·2ᵏ) in Y=T/Δ und hʷⱼ=w*ⱼ/(100·2ᵏ). Die Stufen k=0,1,2,3 entsprechen voller, halber, Viertel- und Achtelbreite der Referenzbox. Diese Boxen liegen im stetigen positiven Dichtesupport.

Wir wählen die reelle konstante Eingangsamplitude auf der Box, das flache Mass de d⁷Y d⁷w und auf allen Schnitten dieselbe konstante Endpaarung. Bei der Rechnung in normierten Würfelkoordinaten wird der Jacobifaktor J(e)=(2hᵧ)⁷∏ⱼ(2hʷⱼ) mitintegriert. In den Zahlen ist das Gesamtmass der jeweiligen Box auf 1 normiert. Voraussetzung für das Herausdividieren der Skalar- und Geometriefaktoren ist, dass sie auf diesem festen Typ als gemeinsamer, nichtverschwindender und von den Staubkoordinaten unabhängiger Faktor eingehen. Eine mehrtypige physische Paarung ist offen.

Sei P der vergangene Kragen, A eines der 15 Ideale zwischen P und Zukunftskragen und qₐ=19Δp(A) die dimensionslose Schnittladung. Für jede Feinhistorie und mit der veröffentlichten Wirkungsnormierung gilt

```text
S = −(1/38) Σⱼ wⱼ [19 + Σᵢ bᵢⱼ (Yᵢ−Yⱼ)²],
qₐ = Σᵢ∈A,ⱼ∉A bᵢⱼ wⱼ (Yᵢ−Yⱼ).
Z = ∫ exp(iS) dµ,       Bₐ = ∫ qₐ exp(iS) dµ,
Qₐ = Bₐ/Z,               rₐ = (Bₐ−Bₚ)/Bₚ.
```

Qₐ ist ein im Allgemeinen komplexer Quotient für die festgelegte Endauslese. Die gemeinsame Normierung Z kürzt sich in der primären relativen Differenz rₐ heraus. Die Gegenrechnung ergibt bei voller Breite Qₚ ≈ 0,3152747072 + 9,97·10⁻¹¹ i. Dies ist eine Ladungsablesung in Modelleinheiten. Weder eine Inferenz einer Born-Wahrscheinlichkeit noch eine extern geeichte Massenskala wird dafür vorausgesetzt.

## 1. Endliche Toleranz und Nachweis eines Restterms

| Breite | Obere Schranke für maxₐ ∣rₐ∣ | Untere Schranke für ∣rₐ∣ am letzten Schnitt | Volumenquadratur am letzten Schnitt, Betrag |
| --- | ---: | ---: | ---: |
| Voll | 1,11 × 10⁻⁹ | 3,07 × 10⁻¹⁰ | 3,163 × 10⁻¹⁰ |
| Halb | 4,35 × 10⁻¹¹ | 1,92 × 10⁻¹¹ | 1,977 × 10⁻¹¹ |
| Viertel | 1,99 × 10⁻¹² | 1,20 × 10⁻¹² | 1,235 × 10⁻¹² |
| Achtel | 1,02 × 10⁻¹³ | 7,50 × 10⁻¹⁴ | 7,721 × 10⁻¹⁴ |

Alle Werte sind dimensionslose Verhältnisse. „Letzter Schnitt“ bezeichnet das Ideal mit allen sieben inneren Ereignissen unmittelbar vor dem Zukunftskragen. Dort liegt rₐ bei voller Breite numerisch bei −8,95·10⁻¹⁵ − 3,16·10⁻¹⁰ i. Der strikte Nachweis bezieht sich auf die **komplexe** Differenz. Für einzelne Feldgeschichten hatte PR #375 bei derselben vollen Breite eine Abweichung von +13,488 % gezeigt. Die Summation nutzt die Symmetrie der Präparation.

**Herleitung der Schranken.** Bei festem e sei X=qₐ−qₚ und σ=S−S* die Abweichung von der stationären Wirkung. Im Zentrum verschwinden X und alle ersten inneren Ableitungen der Wirkung. X besteht aus linearen und gemischten Dichte-Uhr-Termen. Das flache symmetrische Produktmass hat E[X|e]=0, weil die Störungen in Uhr und Dichte unabhängig und zentriert sind. Für σ bleiben quadratische und kubische Terme:

```text
−38 σ = Σᵢⱼ bᵢⱼ [w*ⱼ (δYᵢ−δYⱼ)²
                 + 2δwⱼ (Y*ᵢ−Y*ⱼ)(δYᵢ−δYⱼ)
                 + δwⱼ (δYᵢ−δYⱼ)²].
```

Der Prüfer bildet die Polynome in den 14 normierten Uniformvariablen. Ihr erstes gemeinsames Moment m=E[Xσ|e] wird durch Integration der Monome bestimmt. Für eine einzelne Koordinate ist das Moment ungerader Ordnung null und bei geradem d gleich 1/(d+1). Die Koeffizienten werden mit nach aussen gerundeten Intervallen eingeschlossen, die Summation der Momentgrenzen erfolgt mit exakten Brüchen. Acht Teilintervalle decken den ganzen Versatzbereich ab.

Seien x und b obere Schranken für ∣X∣ und ∣σ∣. Der Zähler je e hat nach Ausklammern der zentralen Phase einen Betrag höchstens ∣m∣+xb²/2. Für den vorzeichenfesten Zeugen wird an einer gemeinsamen Referenzphase s gedreht. Mit φ≥∣S*−s∣ beträgt die Abweichung des gedrehten Imaginärteils von m höchstens x(b³/6+φb²/2)+∣m∣φ²/2. Das folgt durch die reellen Sinus- und Kosinusreste sowie E[X|e]=0. Die Vorzeicheneinschliessung gilt zusammenhängend über alle e und überlebt den positiven Jacobifaktor. Bei voller Breite gilt b<0,000113 rad und φ<0,0000040 rad. Der gedrehte Realteil des Einheitsphasenfaktors liegt überall über 0,9999999932. Der Eingang qₚ ist im ganzen Paket positiv und sein bedingter Mittelwert ist der Zentrumswert. Damit ist Re(exp(−is)Bₚ)>0,31524 je Einheit Paketmass. Die Nenner sind also von null getrennt. Die obere Ladungsschranke im Zeugen benutzt ∣Bₚ∣≤E[qₚ].

## 2. Bewegte Grenzen und zweiter Rechenweg

Setze U=A ohne P und Vᵤ=Σⱼ∈U ∂/∂Yⱼ. Im Originalintegral ergibt die Differentialidentität qₐ−qₚ=−19 Vᵤ S. Man kann die Translation auf den Integranden anwenden oder durch Variablentausch auf die Boxgrenzen übertragen. Mit nach aussen orientierten oberen und unteren Flächen ergibt sich exakt

```text
Bₐ−Bₚ = 19 i ∫ de J(e) exp(iS*) Σⱼ∈U
         [ E_face+ exp(iσ) − E_face− exp(iσ) ] / (2hᵧ),
```

bis auf die beidseitig identische Gesamtnormierung des Masses. Die Flächenmittel laufen über alle anderen inneren Uhren und sämtliche Dichten. Zentren, Breiten und J variieren mit e. In der **Differenz** der beiden Uhrtranslationen verschwindet der gemeinsame Vergangenheitsanteil. Vᵤ wirkt bei festem e nur auf innere Uhren. Die Dichtegrenzen sind hier Funktionen von e allein. Somit tragen nur die gezeigten Uhrflächen zur Differenz bei. Ein gleichzeitiges Neupräparieren nach dem Quellenpuls wäre ein anderes Instrument.

Die unabhängige numerische Rechnung bestimmt die zentralen Felder mit 60 Dezimalstellen aus den unreduzierten Kantenpolynomen. Bei festen Uhren ist die Wirkung affin in allen Dichten. Ihre Integration liefert Sinc-Faktoren und deren Ableitungen für die Ladung. Über e und die restlichen sieben bzw. sechs Uhren verwendet der Prüfer zwei Produkt-Gaussregeln mit drei und vier Knoten pro Koordinate. Der Volumenweg summiert die Ladung auf gerichteten Kanten. Der Flächenweg summiert die oberen und unteren Uhrflächen. Auf den Flächen ist das Abziehen von 1+iσ zur Stabilisierung exakt, denn der Unterschied ihrer konstanten und mittleren linearen Beiträge verschwindet an der stationären Präparation. Bei voller Breite beträgt der grösste Unterschied der beiden Rechenwege auf der feineren Stufe weniger als 5,4 × 10⁻²¹ relativ zum Eingang. Diese Auflösungsprobe ergänzt die analytischen Schranken.

## 3. Endliche Quellenarme und Fehlerbudget

Zwei Arme verwenden S(Y±h1ₐ,w) mit h=1/64 in Y-Einheiten und denselben ursprünglichen Integrationsfenstern. Die Quelle ändert auf diesem festen Typ ausschliesslich die Staubuhrargumente der Wirkung. Die Endauslese muss beide komplexen Amplituden gegen dieselbe Phasen- und Amplitudenreferenz erfassen. Die Quellverschiebungen erhalten die strikte Kausalordnung im gesamten getesteten Paket.

```text
S(Y±h1ₐ) = S ∓ h qₐ/19 + h²Kₐ,
Kₐ = −Σᵢ∈A,ⱼ∉A bᵢⱼ wⱼ/38,
B̂ₐ = 19 [Zₐ(−h)−Zₐ(+h)] / (2ih).
```

Der Integrand der Ablesung ist exp(iS) qₐ exp(ih²Kₐ) sinc(hqₐ/19). Mit ∣qₐ∣≤qₘₐₓ und ∣Kₐ∣≤Kₘₐₓ ist der absolute Fehler pro Armpaar höchstens qₘₐₓh²[Kₘₐₓ+(qₘₐₓ/19)²/6] je Einheit Paketmass. Bei voller Breite beträgt die so zertifizierte relative Schnittabweichung des endlichen Verfahrens höchstens 4,49 × 10⁻⁶. Die direkte Zweiarmrechnung liefert maximal 1,643 × 10⁻⁶. Die gewählte endliche Quelle kann den wesentlich kleineren Ward-Rest ohne weitere Korrektur nicht auflösen.

Bei **angenommenem** absolutem komplexem Fehler ε=2 × 10⁻⁶ pro normierter Armamplitude erhöht sich der absolute Fehler einer aus zwei Armen bestimmten Ladung um höchstens 19ε/h. Unter dieser Voraussetzung beträgt die maximale Abweichung zweier endlicher Ablesungen relativ zum gemessenen Eingang weniger als 1,556 % über alle vier Breiten. Es wurden keine physikalischen Ereignisse gemessen. Eine reine Intensitätsmessung eines einzelnen Arms liefert die geforderten komplexen Amplituden nicht.

## 4. Kann dieselbe Dichte als markierte Ruhemasse geeicht werden?

Die sechs maximalen Transportpfade des ursprünglichen positiven Markermodells enden bei Ereignis 14 und laufen anschliessend zum Ausgang 7. Wir lassen für diese Gegenprobe beliebige nichtnegative Pfadanteile mit beliebiger positiver Gesamtdosis zu. Auf jedem Pfad verteilt die Verweildauerregel die gesamte Zeitspanne von Y₃ bis Y₇ auf die inneren Ereignisse. Die letzte Zelle beginnt am Mittelpunkt der letzten beiden inneren Uhren. Hat dieser Pfad den vorletzten inneren Knoten v, beträgt sein Anteil an 14

```text
f₁₄ = [Y₇−(Yᵥ+Y₁₄)/2] / (Y₇−Y₃).
```

Die Anteilsuntergrenze jedes einzelnen Pfads gilt für jede positive Mischung, auch bei feldabhängigen Gewichten. Sogar wenn die letzte Zellgrenze irgendwo zwischen Yᵥ und Y₁₄ liegen darf, bleibt auf jedem Pfad der Mindestanteil (Y₇−Y₁₄)/(Y₇−Y₃). Auf der gesamten Box ergibt sich:

| Anteil an Ereignis 14 | Volle Breite | Achtelbreite |
| --- | ---: | ---: |
| Tatsächlich vorhandenes w₁₄ / Σw, nach oben gerundet | ≤ 0,404 % | ≤ 0,397 % |
| Erforderlich bei der bisherigen Mittelpunktregel | ≥ 34,01 % | ≥ 35,38 % |
| Erforderlich bei frei liegender letzter Zellgrenze zwischen den Ereignissen | ≥ 15,52 % | ≥ 16,89 % |

Selbst zusätzliche unabhängige relative Dosisfehler von bis zu 1 % an allen inneren Ereignissen lassen bei voller Breite mindestens 15,26 % im verallgemeinerten Markermodell übrig. Die massenunabhängige Quotientenbildung schliesst eine Reparatur durch Wahl einer anderen positiven Gesamtdosis aus. Bei derselben gleichphasigen Endpaarung liegt auch der Betrag des Quotienten der zwei tatsächlichen Dichteeinfügungen unter 0,404 %. Dazu genügen die positive Dichtesumme und die oben nachgewiesene gemeinsame Phasenkegelschranke. Die Verweildauerprüfung ist eine nachträgliche Erweiterung des lokalen Prüfplans. Sie schliesst die geprüfte Identifikation aus, sofern die letzte innere Zelle die Zeit bis zum Ausgang trägt. Eine andere physikalisch begründete Zuordnung von Dichte und transportierter Masse bleibt eine eigene Frage.

## Nachrechnung und offener P3-Status

```sh
python3 -B pruefen.py
OPENBLAS_NUM_THREADS=1 python3 -B pruefen.py --quadratur
```

Der erste Aufruf wiederholt die rationalen Schranken, die Prüfung der sechs Pfade und den Vergleich mit den archivierten Quadraturdaten. Der zweite berechnet die Volumen- und Flächenintegrale zusätzlich neu und benötigt NumPy. Referenzlauf mit Python 3.12 und NumPy 2.3.5. Die Basisdateien wurden gegen die Git-Blob-IDs des Merge-Commits geprüft. Der lokale Prüfplan liegt mit SHA-256 bei.

Der endliche kohärente Transporttest ist für die deklarierte Präparation ausgeführt. Der physische P3-Lauf benötigt eine unabhängige Ruhemasse-Eichung und eine geometrisch bestimmte materielle Oberfläche bei T*=5√5/6 auf derselben dynamischen Präparation. Alle 60 physischen Prüfpunkte sind NOT_RUN. [Veröffentlichte Basisstudie und Definition der Feldbox](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/ea05b04677917d8e970c3bb0888d024a479cd500/research/rax_cqg/dust_collapse/n15_stationaerer_staubstrom_v0_1) · [Vorstudie zur markierten Verweildauer](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/ea05b04677917d8e970c3bb0888d024a479cd500/research/rax_cqg/dust_collapse/synchronized_distributed_dust_v0_1)
