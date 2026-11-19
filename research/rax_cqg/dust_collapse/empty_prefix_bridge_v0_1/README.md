# CST-DUST · Der Nullzweig am leeren Anfang der Staubuhr

Etappen 3–4 · 19. November 2026 · Stand v0.1. Ausgangscommit [3caa6d8](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/3caa6d8e3b7f13afb23e4ccb5380b15b8feaff12).

## Ergebnis

Für die fest präparierte AA-Randfamilie gibt es eine normtreue Zuordnung auf der eindimensionalen leeren Anfangslinie. Der absolute Geburtsfluss bleibt offen. Eine einzige kohärente Auslese, die den Nullzweig sicher akzeptiert und alle Dreipaket-Paarungen erhält, ist mit dem vollständigen orthogonalen Geburtsrecord beider Referenzuhren unvereinbar. Für eine ausgewählte Auslese mit einem ergänzenden Ausgang existiert eine ausdrückliche gemeinsame Zuordnung. An zwei Schnitten bleiben dieselben komplexen Kreuzterme erhalten. Die absolute Akzeptanz der Auslese entscheidet darüber, welche Referenzprodukte zulässig sind.

## Präparation und Uhr

AA bezeichnet zwei unvergleichbare Ereignisse am Eingangsrand und zwei am Ausgangsrand. In der Nullfamilie gibt es kein inneres Ereignis. Entfernt man in den 33 Ordnungen der publizierten Ein-Geburts-Familie den inneren Punkt und schränkt die transitive Ordnung ein, entstehen sieben beschriftete Randordnungen mit Häufigkeiten 2,5,2,5,5,5,9 (Masken 6,7,9,11,13,14,15). Wir behalten ihre kohärenten Koeffizienten n/33, Dichteatome und das skalare Eingangsgrundpaket bei. Jede Nullordnung hat dieselbe leere innere Ordnung. Der äussere Anker der offenen Uhr mit T=−2 und w=0 ist zusätzlich vorgegeben. Die Einschränkung auf die inneren Punkte vergisst den Kragen und das Feld.

Schreibe G₀ für die mit diesen Daten erzeugte und in einem der beiden veröffentlichten Dreipaketprodukte auf eins normierte Nullantwort. Der lineare Präparationsoperator J₀(z|∅⟩)=zG₀ ist auf dieser Linie isometrisch. Die komplexe Phase wird durch die publizierten Paketpaarungen referenziert. J₀ setzt die gewählte Randpräparation voraus. Aus dem leeren Präfix allein lassen sich weder Kragen noch Gewichte rekonstruieren.

Für die offenen Uhren gilt h₀(s)=(1−β)s+exp(−s) und h₁(s)=β−1+exp(−s). Auf dem Keine-Geburt-Pfad liefert der Transport von a nach b den Faktor √[h₀(b)/h₀(a)] in der phasenfreien Konvention des diagonalen Referenztransports. Die Faktoren teleskopieren bei jedem Zwischenschnitt. Die Überlebenswahrscheinlichkeiten h₀(s) und anfänglichen Raten β werden aus der jeweiligen Referenz übernommen. Auf d=1/8 unterscheiden sich die beiden h₀(d) exakt um d/12=1/96. Mehrfachgeburten sind im vollständigen Modell erlaubt. Der gemeinsame 0/1-Ausschnitt wird hier relativ zum Nullzweig gewichtet und nicht auf eine Gesamtwahrscheinlichkeit von eins nachnormiert.

## Gemeinsame, prüfbare Auslese

Im Rohraum der Null- und Ein-Geburts-Antworten auf (0,d) verwenden wir
‖(z,f)‖²=|z|²+κ∫|f(u,w)|² du dν(w), κ=h₁(d)/h₀(d). Der normierte Markenvektor des offenen Wirkungszweigs ist φᵤ(w)=exp[−iw(1/2+4u²)] (μ=1). Das feste f für ein Zeitfenster I ist 1_I(u)φᵤ(w). Sein Normquadrat lautet relativ zum leeren Zweig κ|I|. Disjunkte Geburtszeiten und verschiedene Ereigniszahlen sind in diesem vollständigen Referenzrecord orthogonal. Die Zuordnung benutzt dieselbe dimensionslose Fensterkoordinate u in beiden Modellen. Eine physikalische Kalibrierung dieser Wahl ist offen.

Seien v₀ die drei Paketkoordinaten des Nullzweigs und v₁,v₂ die Koeffizienten der Geburtsantwort gruppiert nach Zahl der Vorgänger. Für t=1 oder 4 seien w₁(t),w₂(t) die vererbten positiven Längendichtegewichte. Mit r=1−‖v₀‖² und Koordinaten in ℂ³⊕ℂ⊕ℂ² verwenden wir

    G₀=(v₀,√r,0,0)
    A₁=(v₁,0,√[r w₁],0),    A₂=(v₂,0,0,√[r w₂])
    F(u)=Z₁(u)A₁+Z₂(u)A₂,    G_I=∫_I F(u)du.

Dabei folgt Zₚ(u)=∫dν(w) ∫_[0,1]^p exp{−iw[1/2+b Σ(yⱼ−u)²]} dᵖy mit b=√(8/3) aus der AA-Wirkung. Die Formel polarisiert das publizierte Dreipaketprodukt für alle betrachteten Fenster und ist hier die ausdrückliche Fortsetzung des Vergleichsvertrags. Die separate spätere Uhr-/Dichteauslese der aus zwei AA-Hälften verklebten Geometrie ist ein anderer Messversuch.

Ein möglicher gemeinsamer Rohoperator für den ausgewählten Ausgang lautet

    S(z,f)=zG₀+∫F(u) ⟨φᵤ,f(u,·)⟩_ν du,       K=√η S .

Der Markenfilter und die einheitliche positive Skalierung η sind Modellannahmen. Für beide β gilt dieselbe Rohvorschrift. Die Domänennorm enthält das jeweilige κ. η ist die Wahrscheinlichkeit dieses Ausgangs, bedingt auf den normierten Nullzweig. Die Quotienten der Erfolgsgewichte relativ zum erfolgreichen Nullzweig erhalten alle verglichenen AA-Paarungen. Für ein zulässiges Instrument gilt K†K ≤ I. Hinzunahme von (I−K†K)^(1/2) als zweitem Ausgang ergibt ein normerhaltendes Instrument auf der betrachteten Domäne. In der Summe beider Ausgänge verschwinden die Kreuzterme orthogonaler Eingänge. Der neue Modelloperator spezifiziert weder eine physikalische Geburtsmessung noch einen eindeutigen ergänzenden Detektor.

## Ausschluss und zwei Schnitte

Im Gesamtfenster ist C=⟨G₀,G_(0,d)⟩. Die Intervallrechnung schliesst Re C zwischen −0,0100200 und −0,0100199 ein, Im C zwischen 0,0014268 und 0,0014269. Für η=1 hat die Differenz zwischen Eingangs- und Ausgangs-Grammatrix auf Nullzweig und Gesamtgeburt die erste Diagonale null, die gemischten Elemente −C und −C* und die Determinante −|C|²<0. Beide Referenzprodukte scheiden für die verlustfreie kohärente Auslese aus. Dieser Ausschluss betrifft ausdrücklich auch die Paarungen zwischen verschiedenen Geburtszahlen.

Ein einziges Gitter mit Kanten 0,1/24,1/16,1/8 trägt beide Schnitte. Die Norm des Gesamtfensters stimmt in beiden Zerlegungen mit ‖G_L‖²+‖G_R‖²+2 Re⟨G_L,G_R⟩ überein. Die gemischte Nullpaarung stimmt komplex mit ⟨G₀,G_L⟩+⟨G₀,G_R⟩ überein. Das Intervallverfahren rekonstruiert die Paketkoeffizienten aus allen 33 Ein-Ereignis- und sieben Nullordnungen. Die Datei ergebnis.json enthält die vier komplexen Schnittbilanzen und die auf acht Dezimalstellen eingeschlossenen Schwellen des endlichen Teilraums.

## Nachweis für die kontinuierliche Uhr im Fenster d=1/8

Die vier kanonischen Eingänge sind der Nullzustand und die drei disjunkten Zeitintervalle mit dem Wirkungs-Markenvektor. Ihre Eingangs-Grammatrix ist H=diag(1,κℓ₁,κℓ₂,κℓ₃). Für die aus G₀ und den drei G_I gebildete Gram-Matrix B_AA ist H−η B_AA ≥ 0 genau das Kontraktionskriterium auf ihrem Spann. Hermitesche Schur-Pivots mit Intervallarithmetik klammern die Grenze ein. Für jeden getesteten Grenzfall sind die positiven Pivots oder ein negativer Pivot nach positivem führendem Block vom Nullwert getrennt.

Für den kontinuierlichen Rest reduziere zuerst jede Dichtefaser auf φᵤ. Der Operator verschwindet auf ihrem orthogonalen Komplement. Auf dem entstehenden gewöhnlichen Uhrraum sei P die Projektion auf binweise konstante Funktionen und die komplette Nulllinie. Es gilt SS†=SP(SP)†+S(I−P)[S(I−P)]†. Der Normzuwachs des positiven Operators ist höchstens die Spur des zweiten Summanden. Wegen |Zₚ|≤1 und |Z′ₚ|≤bp/4 ist F Lipschitz mit L′≤b(‖A₁‖+2‖A₂‖)/4. Die Ableitungsschranke benutzt ∫w dν=1/4 und ∫₀¹|y−u|dy≤1/2. Auf einer Zelle der Länge ℓ gilt

    ∫‖F−F_mittel‖²du = (1/2ℓ)∫∫‖F(u)−F(v)‖²du dv ≤ (L′)²ℓ³/12.

Der Zuwachs ist somit höchstens ε=(L′)²Σℓ³/(12κ). Liegt η_max(P) zwischen a und b₊, folgt für das ganze Uhrfenster 1/(1/a+ε) ≤ η_max ≤ b₊. Die Schranke ist für den angenommenen Zweigraum und das feste Endfenster gültig. Für alle 0<d≤1/8 und beide β funktioniert beispielsweise η=0,98. Dafür genügen κ≥1 und ‖S‖²≤1+d(‖A₁‖+‖A₂‖)²/κ. Die Gruppennormsumme ist kleiner als 0,2935 bzw. 0,2769.

| Relative Sektornorm | Regulator t | η_max, kontinuierliches Intervall bei d=1/8 |
|---|---:|---|
| β=5/4 | 1 | [0,99938192; 0,99938237] |
| β=5/4 | 4 | [0,99938207; 0,99938245] |
| β=4/3 | 1 | [0,99943144; 0,99943186] |
| β=4/3 | 4 | [0,99943158; 0,99943193] |

Eine separat festgelegte und ausreichend genau bekannte Akzeptanz im offenen Intervall (0,99938245; 0,99943144) würde im erklärten Vertrag β=5/4 ausschliessen und β=4/3 zulassen, für beide Regulatoren. 0,9994 ist ein rechnerisches Beispiel, kein gemessener oder vorab abgeleiteter Wert. Die Konstruktion ist keine eindeutige Fortsetzung unter allen möglichen Instrumenten. Ihre Prüfung von zwei Unterteilungen eines Endfensters ersetzt auch keinen Beweis der zeitlichen Zusammensetzung eines vollständigen gekoppelten Transports.

## Nachrechnen

Für die Hauptrechnung werden Python 3.10+ und mpmath 1.3.0 benötigt. Die numerische Gegenprobe benutzt NumPy, hier 2.3.5. Beide laufen offline auf einem CPU-Kern.

    python -B pruefen.py --out nachrechnung.json
    cmp ergebnis.json nachrechnung.json
    OPENBLAS_NUM_THREADS=1 python -B gegenprobe.py

Der Bytevergleich bezieht sich auf die Referenzumgebung (Python 3.12). Die numerischen JSON-Anzeigen sind gerundet. Die entscheidenden Vorzeichen sowie die Unter- und Obergrenzen für η werden vor Ausgabe mit 50 Dezimalstellen Intervallarithmetik und den rationalen Uhrhüllen geprüft. Die Gegenprobe bestimmt die Paketvektoren aus den vollen vier- bzw. fünfdimensionalen Gaußmatrizen und integriert die Uhr- und Vorgängerkoordinaten mit zwei Gauss-Ordnungen. Ihre vier maximalen Akzeptanzen liegen innerhalb der ausgewiesenen Kontinuumsintervalle.

Die ursprünglichen Quelldateien stehen unter quellen/ mit Lizenz und in quellen.json mit Pfad, Commit und Git-Blob-ID. Bericht und neue Programme werden unter derselben Apache-2.0-Lizenz bereitgestellt. Der physikalisch offene Eingang ist eine unabhängig festgelegte inklusive erste Geburtsnorm relativ zum Nullzweig bei derselben Uhr und Präparation, oder im engeren Auslesevertrag die absolute Kalibrierung der akzeptierten Nullzweige. P3 M=1 bleibt bei 0/38 auf der ersten Dichtestufe.
