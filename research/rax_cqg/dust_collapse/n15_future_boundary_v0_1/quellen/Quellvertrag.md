# Randpräparation für den Massensektor des Staubstroms

**Für den markierten Referenzstrom sind beide Massen am Rand kalibriert. Für den Strom der gekoppelten Wirkung liegt ein ausführbarer Ladungsselektor vor. Seine Kalibrierung auf die physikalischen P3-Massen ist offen.** Für eine neue kanonische Randpräparation wurden zwei orthogonale Impulspakete konstruiert. Ein Gegenbeispiel zeigt, weshalb ihr Impuls auf dem erweiterten Uhrenrand die Stromladung am ursprünglichen Schnitt nicht automatisch misst. Die physikalischen Flächen bei T* und ihr Vergleich über die Historiengewichte bleiben unbestimmt. P3 steht auf **HOLD_NOT_ELIGIBLE / NOT_RUN**.

Grundlage ist [der publizierte Massenstrom-Versuch aus PR #332](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/7ea519b2e1e13379eab78d822cea5ced5320dcf3/research/rax_cqg/dust_collapse/material_current_surface_v0_1). Für die neuen Tests gelten zwei endliche Fenster mit konstruktiv gewählter relativer Halbbreite 1 %. Diese Wahl ist eine Diagnose. Eine physikalische Gesamtunsicherheit lässt sich daraus nicht ableiten. Die erste Untersuchung folgt der vor der Auswertung lokal festgehaltenen Frage in `design.json`. Die Einschränkung auf streng monoton wachsende Uhren und der Vergleich der Längeneinheiten sind ergänzende Analysen. Es gab keine öffentliche Vorregistrierung dieses Pakets.

## 1. Stromladung durch eine gemeinsame Randquelle auslesen

P besteht aus den vier Ereignissen des Anfangskragens. Verschiebe deren vier Uhren gemeinsam um τ und halte alle anderen Felder fest. Dies ist eine relative Verschiebung zum übrigen Gebiet. Mit S als dimensionsloser Wirkung S_phys/ℏ und der Orientierung des Anfangsrandes sei p=−∂S/∂τ bei τ=0. Für die veröffentlichte quadratische Staubwirkung gilt pro Feldgeschichte exakt

`S(τ) = S(0) − τ p + H τ²/2`  
`S(−η/2) − S(+η/2) = η p.`

Die Gravitation und das zusätzliche minimale Skalarfeld ändern sich bei dieser Variation nicht. Dieselbe Ladung ist das Negative der orientierten Schnittsumme Q(P) aus PR #332. Mit β=4/√6, den inneren Dichten w_v und den vier geordneten Vorgängern p_i gilt

`p = (β/2) Σ_v w_v Σ_i b_iv (T_i−T_v)`,  
`H = −(β/2) Σ_v w_v Σ_i b_iv`.

Die Gegenrechnung verwendet die tatsächliche Wirkungs- und Variationsroutine des Projekts. Für jeden der 1 048 Endtypen werden der Randgradient, die Kantenbilanz, die symmetrische Quellendifferenz und der gerade Krümmungsterm mit rationalen Testfeldern geprüft. Der gemeinsame β-Faktor wird analytisch eingesetzt. Er gehört zur selben Randladung in sämtlichen Tests.

Der Selektor multipliziert die einzelne Feldgeschichte mit dem Indikator des Fensters I im Wert g·p, **vor** der kohärenten Summation. g bezeichnet die physikalische P3-Masse pro Einheit dimensionsloser Ladung. Zwei disjunkte Fenster und ihr Rest bilden auf dem deklarierten Hilfsraum komplementäre orthogonale Multiplikationsprojektoren. Ein optionales Register speichert nur „leicht / schwer / Rest“. Es wahrt Kohärenz innerhalb derselben Auswahl. Die Zählquelle exp(iηp) folgt aus der symmetrischen Differenz der Wirkung **derselben Feldgeschichte**. Das Produkt zweier bereits über verschiedene Historien summierter Randamplituden würde andere Kreuzterme einführen.

## 2. Was der bestehende Anfangsrand unterscheiden kann

Für ein inneres Ereignis v mit d inneren Vorgängern ergibt sich die viergliedrige Wirkungszeile allein aus d. Ihre Koeffizienten, von der ältesten zur neuesten Anfangsuhr, lauten:

| d | Koeffizienten |
|---:|---|
| 0 | −8, 16, −9, 1 |
| 1 | 0, −8, 16, −9 |
| 2 | 0, 0, −8, 16 |
| 3 | 0, 0, 0, −8 |
| ab 4 | 0, 0, 0, 0 |

Seien n die inneren Ereignisse mit d≤3. Unter dem deklarierten Hilfsmass hat w je zur Hälfte ein Nullatom und einen kontinuierlichen Anteil auf (0,1). Bei festen zulässigen Anfangsuhren hat die Verteilung von p daher ein Nullatom der Masse **2^(−n)**. Für d=0 verschwindet der Ladungskoeffizient auf keinem der zwei Uhrlappen. Für d=1,2,3 ist er eine nichtkonstante affine Funktion einer kontinuierlichen verborgenen Uhr. Sobald eine sichtbare Dichte kontinuierlich gezogen wird, trifft ihre Summe einen einzelnen vorgegebenen Wert nur auf einer Nullmenge. Der Nachweis gilt auch für streng geordnete Uhren mit kontinuierlichem Mass im offenen Ordnungspolytop. Diese Aussage betrifft das Hilfsmass auf den Feldern, vor Interferenz und physikalischer Paarung.

| n | Anzahl Endtypen | Anteil des Nullatoms |
|---:|---:|---:|
| 4 | 21 | 1/16 |
| 5 | 291 | 1/32 |
| 6 | 534 | 1/64 |
| 7 | 202 | 1/128 |

Ein Selektor, der nur die aktuell am Anfangsrand verfügbaren **Koordinatenwerte** nachgewichtet, behält daher bei jeder nichtverschwindenden Auswahl auch den Nullzweig. Für einen von null verschiedenen Einzelwert hat der Multiplikationsprojektor im kontinuierlichen Hilfsmass umgekehrt Normwirkung null. Ein Fenster endlicher Breite oder eine ausdrücklich distributionelle Präparation ist hier wesentlich.

## 3. Zwei echte Impulspakete auf einem erweiterten Uhrenrand

Für die zusätzliche kollektive Koordinate τ∈ℝ mit dem üblichen L²(dτ) wählen wir den orientierten Generator +i∂τ. Ein normiertes Rechteck im Impulsfenster [l,h) hat bei W=h−l und c=(h+l)/2 die Randwellenfunktion

`φ(τ) = √(W/(2π)) exp(−icτ) sinc(Wτ/2)`, mit sinc(z)=sin(z)/z.

Die beiden Wellenpakete haben Norm eins und gegenseitiges Skalarprodukt null. Der Prüfer vergleicht ihre Fourier-Rücktransformation mit direkter Quadratur. Die individuelle relative Kragenform kann beim Einführen von τ beibehalten werden. Der unbeschränkte Kollektivmodus erweitert den bislang kompakt präparierten Rand.

**Test gegen den Strom am ursprünglichen Schnitt.** Beim zulässigen Endtyp 2324 hat das Ereignis 12 genau einen inneren Vorgänger. Sein Dichtegewicht sei 1/2, alle anderen inneren Dichten seien null. Für den rechten Uhrenlappen mit Offset 1/16 und die innere Uhr −2Δ+9/16 gilt mit Δ²=2/(19β) exakt p(0)=0 und H=β/4>0. Die übrigen inneren Uhren können streng kausal zunehmend zwischen den Kragen gewählt werden.

Die Fouriertransformierte der Einzelphase exp(iHτ²/2) ist im Abel-Sinn eine quadratische Phase mit konstantem, von null verschiedenem Betrag. Dies folgt durch quadratische Ergänzung im mit exp(−ετ²) regulierten Gaußintegral und ε↓0. Die mittlere Phase in jedem der beiden endlichen Fenster verschwindet ebenfalls nicht: Ihr Betrag relativ zum konstanten Fourierbetrag ist bei der schweren Probeeinstellung mindestens 23/25 und bei der leichten mindestens 819199/819200. Die Schranke folgt aus der maximalen Phasenauslenkung im Band und cos z≥1−z²/2. Sie ist ein Überlappungsverhältnis einer Prüfphase, keine Erfolgswahrscheinlichkeit. Der Effekt besteht stetig für benachbarte Felddaten mit kleiner Anfangsladung fort. Ein reiner Fourierfilter des verschobenen Gesamtrandes kann folglich eine Feldgeschichte mit Anfangsladung null passieren lassen. Er präpariert den kanonischen Impuls der neuen Randdarstellung. Die Identifikation mit dem fein aufgelösten Strom am ursprünglichen Schnitt bräuchte zusätzliche Dynamik.

## 4. Die Fenster tatsächlich anwenden

Für die Diagnose g=1 sind die halboffenen Fenster [0,2475;0,2525) und [3,96;4,04). Der Zahlenwert g=1 ist hier die Einheitsprobe des dimensionslosen Instruments. Geprüft wird positiver Träger im deklarierten Feldmass, nicht eine Born-Wahrscheinlichkeit.

| Feldbereich | Leichtes Fenster erreichbar | Schweres Fenster erreichbar |
|---|---:|---:|
| Ursprüngliche unabhängige innere Uhren auf [−3/2,3/2] | 1 048 / 1 048 | 1 048 / 1 048 |
| Zusatzbedingung streng steigender Uhren auf allen kausalen Beziehungen | 1 048 / 1 048 | 957 / 1 048 |

Im ursprünglichen Feldbereich ist p in jeder einzelnen Dichte und Uhr affin. Die Extremwerte auf dem Abschluss genügen zur Bestimmung des wesentlichen Trägers. Für die geordneten Uhren verwendet der Prüfer die 21 792 Ideal-Ecken sämtlicher Ordnungen. Bei festem Dichtevektor ist jede zulässige Uhrbelegung eine konvexe Mischung von Belegungen, die auf einem Ideal den unteren und auf seinem Komplement den oberen Uhrenwert tragen. Danach kann jedes w unabhängig auf 0 oder 1 gesetzt werden. Die Endpunkte der beiden äusseren Uhrenlappen genügen ebenfalls. Offene Randwerte sind Grenzwerte von positiven inneren Massmengen. Durch gemeinsames Skalieren der Dichten lässt sich jeder strikt zwischen 0 und dem Supremum liegende positive Ladungswert annähern, auch auf positiver Massmenge in einem offenen Fenster. Der Prüfer schliesst alle extremalen positiven Schwellen mit rationalen Intervallen ein.

Damit beide Fenster auf **jedem** Ordnungstyp einen positiven Träger besitzen, muss g im ursprünglichen Bereich grösser als rund 0,363890, unter der zusätzlichen Uhrenordnung grösser als rund 1,395117 sein. Die exakte Grenze ist 3,96 geteilt durch das kleinste der 1 048 typweisen Ladungssuprema. Dies sind Anforderungen für volle Typabdeckung; ein physikalischer Projektor könnte bestimmte Typen ausschliessen. Die 91 fehlenden schweren Typen der zweiten Zeile sagen entsprechend nichts über eine Ablehnung des gesamten schweren Massensektors aus.

**Kontrolle der Amplitude.** Für feste übrige Variablen sei p=p₀+c w auf einer Dichteachse, ihr Wirkungsfaktor exp(−iDw/2). Nach Auswahl eines Ladungsfensters erhält man den Atomterm ½·1_I(gp₀) plus die Hälfte des Integrals von exp(−iDw/2) über das auf [0,1] beschnittene erlaubte Dichteintervall [a,b]. Der Prüfer verwendet die exakte sinc-Form des Integrals, einschliesslich c=0, negativem c und D=0. Die beiden Teilfenster und ihre Restintervalle ergeben wieder das ungeschnittene Integral.

Der erste kanonische Endtyp mit einer d=3-Zeile ist 2452. Für eine strikt wachsende Uhrbelegung, festes Skalarfeld null und Ereignis 11 als einzige potentiell positive innere Dichte ergibt sich p≈6,212662760446·w. Die übrigen sechs Dichten bleiben auf ihren Nullatomen. Das leichte Fenster selektiert w≈0,039838…0,040643, das schwere w≈0,637408…0,650285. Die komplexen Beiträge beider Fenster enthalten die sechs Atomfaktoren sowie die Gravitations- und Kragenphasen. Direkte Simpson-Quadratur und analytische Integration stimmen in beiden Fällen bis auf weniger als 10⁻¹³ absolut überein. Die aufgeführten Amplituden gelten bei den festgehaltenen Uhren auf diesem Stratum. Eine vollständige physikalische Annahmerate über Historien wurde nicht berechnet.

## 5. Welche Kalibrierung trägt

Auf einer unabhängig markierten Referenzströmung mit Anfangsmasse M wird die Quelle über S_tag=Σ f_uv(T_v−T_u) gekoppelt. Stromerhaltung liefert S_tag=M(T_Senke−T_Quelle). Die symmetrische Verschiebung der Anfangsuhren liest daher genau M aus. Nullpunkt und Verstärkung werden mit 0 und 1 kontrolliert. Die beiden Zielmassen 1/4 und 4 sind anschliessende Prüfwerte. Auf allen 1 048 Trägern gelingen alle 4 192 Ablesungen exakt. Dieser Referenzstrom verwendet die zusätzlich gesetzten Transportmarken. Die Aktionen S_tag und S_d haben auf den gekoppelten Feldkonfigurationen keine nachgewiesene gemeinsame Massennormierung.

Der Einheitenvergleich präzisiert die offene Messung. Für T_phys=L_τ·τ hätte der dimensionslose Impuls p bei physikalischer Identifikation die Ruhemasse ℏp/L_τ in c=1-Einheiten. Die dimensionslose geometrisierte P3-Masse wäre dann M=(Gℏ/(L_τ L_P3))p. Dass die lokale Rechnung und P3 Zahlen in Modelleigenheiten benutzen, bestimmt weder den Umrechnungsfaktor noch die Identifikation der Observablen.

Eine zusätzliche Konsistenzprobe setzt probeweise den unrenormierten Gravitationskoeffizienten κ=1 der F₄-Phase ein sowie L_τ=ℓ=L_P3. Dann folgt aus der im Wirkungsvertrag angegebenen Formel g=1/(2π√6). Unter genau diesen Hypothesen erreicht **kein einziger** der 1 048 Typen das schwere Fenster, selbst mit den ursprünglichen freien Uhren. Die Quelle allein kann also die unabhängige Längen- und Massenkalibrierung nicht ersetzen. Diese Einheitenwahl wird nicht als physikalischer Wert übernommen.

Der fehlende Test ist eine absolute Vergleichsmessung auf **derselben gekoppelten Anfangspräparation**: eine unabhängig bekannte, positive Schnittmasse und die zugehörige gemessene Ladung p, ergänzt durch eine Vakuumkontrolle. Eine zweite Masse könnte die gemeinsame Verstärkung prüfen. Bei überlagerter oder streuender Ladung ist zusätzlich eine qualifizierte Antwortverteilung des Instruments nötig. Die Flächenform, die physikalische Paarung und der Transport der materiellen Grenze bleiben eigenständige Voraussetzungen. Für beide physikalischen P3-Fenster wurde die Flächenauswertung daher zurückgestellt.

## Offline nachrechnen

Python 3.10 oder neuer und die Standardbibliothek genügen. Im entpackten Ordner:

```sh
sha256sum -c SHA256SUMS
python3 -B run.py --out wiederholung.json --types typen_wiederholung.json
cmp results.json wiederholung.json
cmp by_type.json typen_wiederholung.json
```

`by_type.json` enthält die eingeschlossenen Grenzen und beide Fensterentscheidungen für jeden einzelnen Ordnungstyp. `sources.json` dokumentiert die unveränderten Git-Blobs. Das neue experimentelle Ergebnis ist der endliche Quellen- und Selektortest; die Simulation eines physikalischen Staubballensembles wurde nicht ausgelöst.
