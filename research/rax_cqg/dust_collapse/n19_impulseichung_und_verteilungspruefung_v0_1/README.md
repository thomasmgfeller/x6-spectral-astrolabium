# N19 · Impulseichung und Test der gemeinsamen Speicherpräparation

**26. November 2026.** Für die gemeinsame Gaußpräparation von PR 391 ergibt sich bei kanonischer Quantisierung eine notwendige Wirkungsskala von rund **2 372,79 J·s**. Die stationären N19-Daten bestimmen ihren Wert nicht. Unabhängig davon lässt sich im klassischen N19-Modell eine Präparation mit exakt derselben Kovarianz konstruieren, die bei ausgeschalteter Quelle an beiden Orten einen Puls vortäuscht. Für ein überprüfbares Zuverlässigkeitsziel von 95 % enthält dieses Paket daher einen zweiten Versuch, der ohne Gaußannahme auskommt. Alle neuen Rohdaten sind synthetisch. Der Messstand am N19-Gerät umfasst null Läufe. [Ausgangsrechnung und 144 zertifizierte Modellfamilien, PR 391](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/391)

## 1. Welche physische Wirkung setzt die Gaußpräparation voraus?

In Modellkoordinaten gilt je Spur P = 2p, v₀ = p/κ₀ und b = q + 250v₀. Die Referenzbreiten sind B = 10⁻¹², V = 10⁻¹⁴, κ₀ = 10⁻¹¹. Die beiden standardisierten Grössen b/B und v₀/V haben in der ausgewählten Gaußpräparation jeweils Varianz 1/9 und sind unabhängig. Die Determinante der kanonischen Kovarianz liefert √det Σ = 2κ₀BV/9. Für einen kanonischen Quantenzeiger mit physischer Wirkung S₀ mal Modellwirkung fordert die Unschärferelation

    ℏ/S₀ ≤ 4κ₀BV/9,       S₀ ≥ 9ℏ/(4κ₀BV).

Das ergibt 2 372,7865897 J·s für denselben Eingang beider Geräte. Für den allein auf κ = 1 zugeschnittenen Eingang sinkt die Schwelle auf 2,3727865897 × 10⁻⁸ J·s. S₀ ist die Normierung der gesamten dimensionslosen Wirkung. Die Rechnung setzt weder die Energie eines Eichpulses fest noch beweist sie eine quantenmechanische Auslesewahrscheinlichkeit. Eine globale Multiplikation der vollständigen quellfreien stationären Wirkung mit S₀ lässt dieselben Positionen zu. Zur numerischen Übersetzung verwenden wir den im SI exakt festgelegten Wert von h und ein rational eingeschlossenes π. [NIST, fundamentale Konstanten](https://physics.nist.gov/cuu/pdf/wallet_2022.pdf)

## 2. Wie kann man S₀ messen?

Für die erste Spur liegen auf beiden Transportwegen die zwei freien Glieder 0→1→2 vor dem Sender 16. Ihre Zielgewichte sind auf allen zwölf Hintergründen μ = 1/8. Für x = ℓq trägt der freie Zeiger den physischen Impuls S₀P/ℓ. Bei abgeschalteter Staubquelle und einem bekannten äusseren Impuls I am mittleren Ereignis ergibt die Variation der beiden kinetischen Terme

    D = q₂ − 2q₁ + q₀ = G I,        G = ℓ/(2κμS₀).

Jeder Lauf darf mit eigener Position und Geschwindigkeit beginnen. Bei zwei gleich langen physisch freien Schritten Δτ geht ein zeitlich ausgedehnter Kraftstoss mit dem Dreiecksgewicht max(0, 1−|t−t₁|/Δτ) in I ein. Für ein mittig liegendes Rechteck der Dauer 0,4Δτ gehen genau 90 % des Gesamtimpulses ein. Die Auswertung setzt pro Segment eine konstante Kraft oder einen zeitlich scharfen Stoss voraus. Ungewisse Pulsformen und Zeitlagen müssen durch die gelieferten Grenzen abgedeckt werden.

Pro Trägheit werden vier zeitlich gleich beabstandete Läufe mit Impulsvorzeichen + − − + kombiniert. Der Kontrast eliminiert konstante und linear driftende Hintergründe. Nur die erste Stärke bestimmt den Gewinn. Für die zurückgehaltene grössere Stärke muss das vollständige Intervall des gemessenen Gewinnverhältnisses innerhalb ±2 % liegen. Ein Nullblock und dritte Differenzen prüfen weitere Abweichungen. Eine quadratische Drift kann einen einzelnen Viererkontrast nachahmen. Die Grenzen müssen deshalb auch verbleibende systematische Kräfte und Synchronisationsfehler abdecken. Eine getrennte Kalibrierung über S₀ = mℓ²/(2κμΔτ) setzt die physische Identifikation als freie translatorische Masse voraus. Der Auswerter verlangt Vereinbarkeit der beiden Messwege und überlappende Impulsresultate beider Trägheiten.

| Vorgegebene synthetische Wirkung in J·s | Schnitt der beiden Impulseichungen in J·s, ungefähr | Vergleich mit der gemeinsamen Schwelle |
|---:|---:|---|
| 3 000 | 2 995,38 bis 3 004,62 | darüber |
| 2 000 | 1 996,95 bis 2 003,06 | darunter |
| 2 372,8 | 2 369,17 bis 2 376,44 | unentschieden |

Optisch ist eine unabhängige Gegenrechnung möglich. Ein ideal normal reflektiertes Photon der Wellenlänge λ gibt 2h/λ Impuls ab. Bei γ separat geeichten Michelson-Streifen pro q-Einheit gilt ℓ = γλ/2. Für dieselbe Wellenlänge ergibt sich S₀/h = γ²·Kontrast(N_eff)/(2κμ·Kontrast(D in Streifen)). N_eff schliesst das Zeitgewicht und das Vorzeichen ein. Ohne unabhängiges γ ist S₀ nicht identifizierbar, da eine gemeinsame Skalierung von γ um a und S₀ um a² dieselbe Streifenantwort pro Photon liefert. Reflektivität, Winkel und weitere mechanische Bewegungen müssen am realen Gerät erfasst werden. Eine anderweitig geeichte Spiegelmessung belegt diese N19-Zuordnung nicht. [Strahlungsdruckkalibrierung bei LIGO](https://dcc.ligo.org/LIGO-P1500249/public) · [Michelson-Wegmessung, University of Wisconsin–Madison](https://lakeslab.ep.wisc.edu/EMA611Michelson.html)

## 3. Eine identische Kovarianz kann falsche Pulse liefern

Setze x = b/B, y = v₀/V und E = x² + y². Der frühere deterministische Nachweis gilt bei E ≤ 4 auf jeder der drei Spuren. Am nativen Raster 2 × 10⁻¹² geben jedoch auf der freien ersten Spur sowohl der Mittelpunkt als auch ein Anfangszustand mit E = 29/4 dieselben drei digitalen Nullwerte aus.

Für eine härtere Gegenprobe ziehen wir jede der sechs Koordinaten unabhängig aus {−64, 0, 64}. Jeder der beiden Randwerte hat Wahrscheinlichkeit 1/(18·64²). Mittelwerte, Varianzen, Kreuzkovarianzen und damit die gesamte kanonische Kovarianz in (q,P) stimmen mit PR 391 überein. Betrachte die zwei Zustände, bei denen nur das erste x von null abweicht. Sämtliche Anfangsimpulse sind dann null. Die vollständige stationäre Rechnung auf dem Referenzhintergrund und der ursprüngliche lokale Leser ergeben am **Empfänger 18 und am Speicher 7** übereinstimmend −10⁻⁶ bzw. +10⁻⁶, obwohl J = 0 gesetzt wurde. Der Effekt tritt bei beiden Trägheiten und beiden Transportwegen auf. Allein diese beiden Zustände haben zusammen Wahrscheinlichkeit r(1−r)⁵ ≈ 0,0027123 %, mit r = 1/(9·64²). Damit überschreitet der Modellfehler bei dieser Präparation bereits die von der Gaußschranke zugelassene Fehlerquote.

Drei Scherungen A = 150, 250, 350 liefern die Projektionen x + ty mit t = −1, 0, 1. Ihre zweiten Momente bestimmen ⟨x²⟩ = M₀, ⟨xy⟩ = (M₊−M₋)/4 und ⟨y²⟩ = (M₊+M₋)/2−M₀. Für eine unbekannte Mittellage braucht die Kovarianz zusätzlich die ersten Momente. Die Erfolgsschranke aus den gegebenen zweiten Momenten allein beträgt mit der Markow-Ungleichung mindestens 5/6 für alle drei Spuren zusammen. Für das radiale vierte Moment ergibt sich mit zwei zusätzlichen Scherungen A = 50, 450 eine positive Darstellung aus den rohen vierten Projektionsmomenten mit Gewichten 5/6 für t = 0, je 1/18 für t = ±1 und je 1/36 für t = ±2. Wäre für jede Spur das radiale vierte Populationsmoment höchstens 8/81, folgte eine gemeinsame Erfolgsschranke von 53/54. Endliche Stichproben liefern ohne weitere Annahmen keine solche obere Populationsschranke.

## 4. Ein Verteilungstest mit vorab festem Stichprobenumfang

Bereite pro Versuch ein neues, identisch verteiltes Dreierensemble vor. Erst danach wählt ein fairer, unabhängiger Zufallsentscheid für alle drei Spuren gemeinsam eine von zwei Scherungen, A = 150 oder 350. Eine separate, für diesen Versuch verbrauchte Präparation liefert drei Positionen. Der Leser misst ideal ΓB(x + αy), mit Γ um 32 und |α − s| ≤ 0,01 für die gewählte Einstellung s = ±1. Kalibriere pro Kanal Positionsgewinn, Nullpunkt und Scherung und erfasse Sättigung. Für eine getrennte äussere Impulsantwort β des verstärkten Kanals gilt A = β/(ΓμG), wenn die schwache Krageneichung G dieselbe Impulsskala und ℓ verwendet. Die tatsächliche Zuordnung der Kanäle, Linearität über den beanspruchten Bereich und normierten Fehler sind apparative Voraussetzungen.

Der obere Betrag der aus Rundung und Nullpunktfehler eingeschlossenen Projektion muss in allen drei Kanälen höchstens 2(1−0,01) sein. Könnten beide Einstellungen für denselben klassischen Zustand bestehen, so begrenzt ihre Differenz |y| ≤ 2. Die bekannten Scherfehler liefern dann |x±y| ≤ 2 und somit E ≤ 4. Liegt eine der drei Spuren ausserhalb des Kerns, meldet mindestens eine der zwei Einstellungen eine Auffälligkeit. Ein gemeinsamer Zufallsentscheid genügt dafür auch bei Korrelationen zwischen den Spuren. Dieser Schluss setzt eine gemeinsame klassische Zustandsverteilung und die spezifizierte Abbildung auch für Ausreisser voraus. Eine Übertragung auf einen allgemeinen quantenmechanischen Messprozess bleibt offen.

Bei einer tatsächlichen Aussenseiterquote von mindestens 5 % ist die Auffälligkeitswahrscheinlichkeit damit mindestens 1/40. Für unabhängige, gleich präparierte Dreierensembles genügen **119 vorab festgelegte Versuche ohne Auffälligkeit**, um eine Kernwahrscheinlichkeit von mindestens 95 % mit einseitig 95 % Konfidenz zu belegen. Es gilt (39/40)¹¹⁹ ≤ 0,05 < (39/40)¹¹⁸. Fehlende, gesättigte und unlesbare Anzeigen zählen als Auffälligkeit. Wer vorab eine Auffälligkeit tolerieren will, braucht mindestens 188 Versuche. Die Übertragung auf korrekte Klassifikation an beiden Orten gilt pro zertifizierter Modellfamilie und setzt die dortigen Dynamik- und Lesebedingungen voraus. Ein direkter End-zu-End-Test der viel höheren Gaußschranke aus PR 391 würde bei 95 % Konfidenz mindestens 65 566 563 fehlerfreie unabhängige Versuche derselben Population erfordern. [Exakte einseitige Binomialgrenzen, NIST](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm)

## Reproduktion und Messdaten

Python ab 3.10 und die Standardbibliothek genügen. Im entpackten Verzeichnis:

    python3 -B pruefen.py
    python3 -B eichen.py Synthetische_Rohdaten.json
    python3 -B zeugen.py Synthetische_Rohdaten.json Synthetische_Zeugenlaeufe.json
    python3 -B eichen.py Messstand.json

Der erste Befehl prüft die SHA-256-Listen, wiederholt den archivierten Vorgänger und vergleicht die fünf neuen JSON-Dateien bytegenau. Die beiden Beispiel-Eingaben zeigen das vollständige Format. Messgrössen können als Dezimal- oder Bruchstrings und als geschlossene Paare [Untergrenze, Obergrenze] eingegeben werden. Die Kraftsegmente verwenden Zeit in Einheiten von Δτ relativ zum mittleren Ablesezeitpunkt und einen vorzeichenbehafteten Gesamtimpuls in N·s. Die Ausgabecodes des Verteilungstests sind ganze Zahlen. Physische Rohdaten tragen die Kennung `measurement_records` mit Geräte-, Referenz-, Chargen- und Randomisierungsnachweisen. Software kann die Richtigkeit dieser Angaben nicht beglaubigen. Die beiden Prüfpläne wurden vor den jeweiligen Rechnungen lokal gehasht.

Der nächste Messschritt benötigt auf derselben Zeigerspur eine unabhängige Längenreferenz, die Zeitreihe des äusseren Impulses und die drei zugehörigen Positionsablesungen je Lauf. Der zweite Impulspegel und der Nullblock bleiben für die Kontrolle reserviert. Die 119 unabhängigen Dreierpräparationen gehören zum separaten Verteilungstest. Im geprüften N19-Ausgangspaket fehlen diese Messreihen. **Alle 60 physischen P3-Prüfpunkte stehen auf NOT_RUN.**
