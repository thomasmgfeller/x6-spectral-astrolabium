# Die Kohärenz der inneren Uhren am offenen Endrand

CST-DUST · N15, Ordnungstyp 2097151 · 25. November 2026 · Anschluss an [PR #373](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/373).

Im festgelegten Randmodell genügen zwei aus derselben Ablesung gebildete Häufigkeiten, um beide Komponenten der Eingangskohärenz der kollektiv verschobenen Uhren zu bestimmen. Es genügen die gewöhnlichen Dichten w₈ und w₉. Das Ergebnis setzt gleiche Eingangspopulationen, eine bekannte Dichteklasse und einen kalibrierten Endeffekt voraus. Der Unterschied zwischen gleichphasigem Eingang und Mischung beträgt im veröffentlichten Endfenster nur rund 6,443 · 10⁻¹⁶ in einer Einzelwahrscheinlichkeit. Die Zahlen sind Vorhersagen aus der Wirkung. Es liegen keine physischen Zähldaten vor.

## Offline prüfen

Im vollständig entpackten Ordner mit Python ab 3.10 ausführen. Die Standardbibliothek genügt.

    python3 -B pruefen.py

`endrand.py` berechnet nach aussen gerundete 256-Bit-Intervalle und prüft die dreieckige Umkehrung der Phasenkoeffizienten an 13 rationalen Profilen. `quadratur.py` verwendet eine getrennte Implementierung der 50 Paarterme in Rangreihenfolge und zwei Gauss-Auflösungen. Die archivierten Ausgaben sind `ergebnisse.json` und `quadratur.json`. Der Prüfer kontrolliert die Dateien, die Quelleingaben und beide Neuberechnungen. `Pruefplan.md` dokumentiert die im Verlauf ergänzten Tests. Es gab keine externe Vorregistrierung.

## Präparation und drei Randöffnungen

Die früheren Fenster, die festen Dichteprofile, alle inneren Jitter und die gemeinsame Auslese entsprechen PR #373. Zwei konkurrierende Eingänge werden innerhalb derselben späteren Dichteklasse verglichen. Beim ersten Paar wechselt das Uhr-4-Paket mit seinem vorbereiteten Dichteprofil. Beim kollektiven Paar wechseln die sieben inneren Uhren alternierend. Die sieben tatsächlichen inneren Dichten stimmen auf den gepaarten Feingeschichten jeweils überein. Beide Anfangsdichten 1/8 und 1/4 liefern denselben gemeinsamen früheren Faktor, der in den normierten Ergebnissen wegfällt.

In allen drei Fällen bleibt Y₇=2 fest. Y₈,Y₉,Y₁₀ variieren unabhängig um 3,4,5 mit Halbbreite η=2⁻²⁰. Die vier Enddichten werden mit flacher Produktpaarung gelesen.

| Öffnung | w₇ und w₁₀ | w₈ und w₉ |
|---|---|---|
| Veröffentlicht | 1/8 ± η | 1/8 ± η |
| Nur 8 und 9 erweitert | 1/8 ± η | 1/8 ± 1/8 |
| Vier breite Dichtefenster | 1/2 ± 1/2 | 1/2 ± 1/2 |

Die beiden erweiterten Auslesen sind neue Kontrollen. Die Endpunkte haben unter dem flachen Mass Gewicht null. Die beiden Dichteklassen sind getrennte Modellpräparationen. Eine unbekannte Mischung der Klassen wäre ein weiterer Inferenzparameter.

## 1. Zweigidentifikation am Endrand

Für jede Eingangsoption wird die komplexe Endwelle über alle inneren Variablen integriert und anschliessend einzeln normiert. Bei gleichen bedingten Vorchancen ist die optimale Zweigtrefferquote (1+T)/2 mit dem reinen Spurabstand T=√(1−|⟨L,R⟩|²). Auch eine kohärente Messung über den gesamten Endwürfel ist hier zugelassen. Ein Ablesen der Koordinaten allein verwendet lediglich das Betragsquadrat der Welle.

| Zweigpaar | Veröffentlichter Endrand | Vier breite Dichtefenster |
|---|---:|---:|
| Getrennte Uhr-4-Pakete | höchstens 50,000000000000022 % | höchstens 50,0000000143020 % |
| Kollektiv verschobene Uhren | 50,0000048489 bis 50,0000048509 % | 52,53757 bis 52,53853 % |

Die Aussagen gelten für beide Dichteklassen. Für das kollektive Paar im breiten Fenster erreicht bereits ein kohärenter Vergleich der zwei Hälften von w₈ mindestens 51,3363 % im Modell. Nach Ausgleich der mittleren Referenzphasen der beiden Zweige wird ein fester ±i-Vergleich zwischen den Hälften verwendet. Eine entsprechende physische Phasenoperation ist offen. Für direkt abgelesene Randkoordinaten liegt die optimale Zweigtrefferquote im selben breiten Versuch unter 50,000472 %. Die stärkere Unterscheidung steckt somit hauptsächlich in den relativen Randphasen. Ein im Inneren zusätzlich kopiertes, dauerhaft orthogonales Zweigbit würde beide Eingänge bei verfügbarer Kopie perfekt unterscheiden. Beim kollektiven Paar kann beispielsweise ein Uhrwert ein solches Bit liefern. Die Staubdichten sind in dessen beiden Zweigen paarweise gleich.

**Fehlerkontrolle.** Für jede normierte Zweigwelle wird die Endphase des Zweigmittelpunkts abgespalten. Das verbleibende Argument ändert sich beim Übergang vom mittleren zum beliebigen Endpunkt auf jeder inneren Geschichte höchstens um

    E = Σ |bᵢⱼ|/38 [ W(2 |Zⱼ−Ȳᵢ| R+R²) + 2(w₀+W) kⱼ R ].

Die Summe läuft über zehn innere Endkanten. R=K/2²² mit K=15/4 ist die wahre innere Uhrhalbbreite, W die Enddichtehalbbreite, kⱼ die Enduhrhalbbreite. Die Amplitude am Zentrum hat nach Weglassen gemeinsamer Faktoren Betrag mindestens m>0,99, begrenzt mit der vollständigen Phasenspanne beider Uhr-5-Pakete. Mit e=E/m liegt die tatsächliche normierte Welle im Spurabstand höchstens e/(1−e) vom reinen Referenzphasor. Für die einzelnen Uhr-4-Pakete ist die gesamte gemischte Endphase pro gepaarter Geschichte gleich. Die Differenz der auf das Zentrum normierten historischen Gewichte kann vor dem Integral abgezogen werden. Das ergibt die schärferen Einzeluhrgrenzen.

Beim kollektiven Paar ist die relative Referenzphase eine Summe über j von βⱼhⱼ+vⱼ(w₀+hⱼ)δYⱼ. Dabei ist hⱼ=wⱼ−w₀. Die vier β-Werte betragen näherungsweise (+0,078223; −0,106957; +0,105978; −0,046560). Ihre Produkte mit den Dichteauslenkungen sind dimensionslose Phasen. Das flache Mittel der linearisierten Phase faktorisiert in sinc-Faktoren. Die bilinearen Restterme haben eine nach oben abgeschätzte Phase Σ|vⱼ|Wkⱼ. Positive, den Zweigen gemeinsame Umgewichtungen sind zusätzlich in der JSON-Datei begrenzt. Die präzisen Tabellenintervalle oben gelten für die flache Paarung.

## 2. Kohärenz aus zwei passiven Zählstatistiken

Hier wird eine andere Frage gestellt. Bei festem Zweigpaar wird die Präparation mit gleichen Amplituden und fester Phase gegen die gleich bevölkerte, in den Zweigen intern kohärente Mischung getestet. Dafür genügt das Betragsquadrat der gemeinsamen Endwelle. Ein praktisch formulierbares Ereignis B lautet: w₈ und w₉ liegen beide oberhalb oder beide unterhalb ihrer jeweiligen Fenstermitte. Die Referenz ist die Mitte der jeweiligen Auslese. Alle angenommenen Ereignisse gehen in den Nenner ein.

| Randöffnung | P(B bei gleicher Phase) − P(B bei Mischung), äussere Grenzen |
|---|---:|
| Veröffentlicht | +6,4424 bis +6,4440 in 10⁻¹⁶ |
| Nur 8 und 9 erweitert, gleicher Mittelpunkt | +1,1068 bis +1,1071 in 10⁻⁵ |
| Vier breite Dichtefenster | +1,77056 bis +1,77098 in 10⁻⁴ |

Die unabhängige Quadratur liefert rund 6,44318 · 10⁻¹⁶, 1,10693 · 10⁻⁵ und 1,77077 · 10⁻⁴. In der breiten Kontrolle sind dies etwa 50,01771 % gleichseitige Ergebnisse für den gleichphasigen Eingang gegenüber etwa 50 % für die Mischung. Es handelt sich um einen Unterschied von 0,01771 Prozentpunkten. Erkennbar wird ein Ensemblesignal. Das einzelne Ereignis verrät den ursprünglichen Zweig kaum.

**Zählaufwand.** Bei bekannter Klasse, exakt kalibrierter Auslese und unabhängigen angenommenen Ereignissen kann man die Schwelle mittig zwischen den zertifizierten Wahrscheinlichkeitsintervallen legen. Für deren Abstand δ begrenzt Hoeffdings einseitige Ungleichung den Fehler unter jeder der beiden Hypothesen durch exp(−Nδ²/2). N=⌈6/δ²⌉ genügt für höchstens 5 %. Im breiten Versuch genügen unter diesen Annahmen 191 392 700 angenommene Ereignisse. Für den veröffentlichten Rand liefert dieselbe konservative Schranke rund 1,45 · 10³¹. Dies sind hinreichende Modellgrössen für einen festen Test. Es wurden keine solchen Läufe gestartet.

**Komplexer Phasenbezug.** Aus denselben Ereignissen wird zusätzlich gezählt, wie oft w₈ oberhalb seines Mittelpunkts liegt. Setze s₈=sgn(w₈−w₀), s₉=sgn(w₉−w₀). Für die drei Gewichte k=1,s₈,s₈s₉ lauten die kalibrierten Koeffizienten dₖ=∫k(|L|²+|R|²)/2 und cₖ=∫k L*R. Der komplexe Kohärenzfaktor γ sitzt im Eintrag rechts/links der Eingangsdichtematrix als γ/2. Für gleichen unbekannten Gesamtfluss F und gemeinsame, modellierte Effizienz lauten die drei erwarteten Summen

    Sₖ = F [ dₖ + Re(cₖ) Re(γ) − Im(cₖ) Im(γ) ].

Die Zeilen der reellen Matrix M sind [dₖ,Re(cₖ),−Im(cₖ)]. Ihre Determinante bleibt in jeder der drei Öffnungen und für beide Dichteklassen von null getrennt. In der hier festgelegten gemeinsamen Normierung liegt sie beim veröffentlichten Fenster um −1,31 · 10⁻²², bei alleiniger Erweiterung von 8 und 9 um −2,96 · 10⁻⁷ und bei vier breiten Dichten um −1,89 · 10⁻⁵. Durch Rechnung mit den normierten Momenten (1,⟨s₈⟩,⟨s₈s₉⟩) und anschliessende Division durch die erste Lösungskomponente entfällt F. Die relative Phase ist an die kalibrierten Modellzweige gebunden. Die Kalibrierung ist auf dem endlichen Modell berechnet. Eine physisch bestimmte Responsematrix und reale Häufigkeiten sind weiterhin offen.

Die Gegenrechnung erzeugt direkt aus Born-Intensitäten bei γ=0,37−0,42i und gemeinsamem Faktor 0,73 erwartete Zählanteile. Die Kalibrierung aus einer anderen Quadratur liefert in beiden erweiterten Fenstern beide Komponenten mit einem numerischen Fehler unter 10⁻⁷ zurück. Dieser synthetische Test verwendet erwartete Häufigkeiten ohne Stichprobenrauschen.

**Warum das winzige Vorzeichen belastbar ist.** Für zwei Feingeschichten am gleichen Enduhrwert hängt die relative Phase linear von jeder Enddichte ab. Setze x=WΔCⱼ. Der flache Durchschnitt von exp(i x u) auf −1≤u≤1 ist sinc(x). Mit dem Vorzeichengewicht sgn(u) ist er i(x/2)sinc²(x/2). Für s₈s₉ erscheinen dadurch explizit zwei kleine Faktoren und ihr Vorzeichen. Die Differenz fast gleicher Gesamtwahrscheinlichkeiten wird so bereits vor der numerischen Integration gebildet. Die Matrixeinträge und die Quotienten sind nach aussen eingeschlossen. Die Gegenrechnung integriert die positiven und negativen Halbachsen mit Gauss-Knoten.

## 3. Was die Randphase prinzipiell eindeutig bestimmt

Bei festen zukünftigen Uhren ist der innere Anteil am Koeffizienten der Enddichte wⱼ gleich Cⱼ=−Σᵢ bᵢⱼ(Zⱼ−Yᵢ)²/38. Alle nur vom Zukunftsrand abhängigen Terme sind bekannt. Direkt beteiligt sind ausschliesslich die inneren Uhren 11,12,13,14. Für j=10 ist allein Y₁₄ unbekannt, danach für j=9 nur noch Y₁₃, für j=8 nur noch Y₁₂ und für j=7 nur noch Y₁₁. Die Kante zur jeweils neu bestimmten Uhr hat b=−8. Nach Abzug der bekannten Terme steht für sie (8/38)(Zⱼ−Yᵢ)² fest. Die kausale Ordnung Zⱼ>Yᵢ wählt die Wurzel eindeutig.

Für ein kompaktes, endliches komplexes Randmass dieser vier späten Uhren ist die Endamplitude nach Entfernen der bekannten Endphase seine Fouriertransformierte in den vier C-Koordinaten. Sind die komplexen Amplituden mit Phasenreferenz auf einer offenen Menge der vier w-Werte exakt bekannt, bestimmen alle Ableitungen an einem inneren Punkt sämtliche Momente des phasengewichteten Masses. Polynome sind auf kompakten Teilmengen von ℝ⁴ dicht in den stetigen Funktionen. Zusammen mit der Dreiecksumkehr folgt Eindeutigkeit dieses **amplitudengewichteten späten Marginals**. Frühe Felder sind darin bereits integriert. Reine Intensitätsdaten enthalten allgemein weniger Information. Die Zweikomponenten-Rekonstruktion in Abschnitt 2 benutzt die wesentlich kleinere, kalibrierte Zustandsfamilie.

Der Unterschied zwischen Eindeutigkeit und erreichbarer Genauigkeit lässt sich konstruktiv prüfen. Bei festen Enduhren kann man allein Y₁₁ so verschieben, dass fünf äquidistante C₇-Werte mit Abstand h=2⁻²⁴ in seiner ursprünglichen Uhrhalbbreite liegen. Alle übrigen C-Werte bleiben gleich. Auf gerade und ungerade Stützstellen werden die geraden bzw. ungeraden Binomialgewichte der vierten Ordnung verteilt und jeweils auf eins normiert. Die resultierenden zwei positiven effektiven Masse haben disjunkte Träger. Für jedes 0≤w₇≤1 unterscheiden sich ihre komplexen Randamplituden im Betrag höchstens um 2(h/2)⁴ < 1,58 · 10⁻³⁰. Das folgt direkt aus der vierten endlichen Differenz. Es ist ein Beispiel im Raum effektiver Masse, keine dritte Behauptung über die physische Präparation der beiden Prüfpakete.

## Quellen und Status

- [Kohärenzstudie und Originalpräparationen, PR #373](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/373)
- [Geöffneter N15-Zukunftsrand im geprüften Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/5b66021572570258788e65f1ad6f612b1ed68f2d/research/rax_cqg/dust_collapse/n15_dichte12_offener_zukunftsrand_v0_1)
- [Watrous, The Theory of Quantum Information, Kapitel 3, Satz 3.4](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf)
- [Polynomapproximation auf kompakten Teilmengen, Proposition A.2](https://galton.uchicago.edu/~lalley/Courses/383/Wigner.pdf)
- [Hoeffding, Probability Inequalities for Sums of Bounded Random Variables](https://doi.org/10.1080/01621459.1963.10500830)

Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN. Die Rechnung bestimmt, was der angenommene Endrand auslesen könnte. Die physische Randpaarung, ihre Kalibrierung, die tatsächliche Eingangskohärenz und die Massenkalibrierung sind offen.
