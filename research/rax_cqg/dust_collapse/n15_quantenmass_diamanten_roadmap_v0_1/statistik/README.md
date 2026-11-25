# Ereignisbedarf für den synthetischen Dreifenstertest

Die beiden einfachen Hypothesen sind genau die äusseren, komovierenden FLRW-Staubräume aus dem publizierten Anschlussbeispiel. In drei benachbarten Zellen mit fester dimensionsloser Zeitbreite h werden Ereignisse eines Sprinklings mit konstanter Intensität gezählt. Bedingt auf die Gesamtzahl n sind die drei Anzahlen multinomialverteilt mit den hinterlegten Fensterwahrscheinlichkeiten. Die Modellchancen betragen je 1/2. Als prüfbare Konvention für „3σ“ wird der **mittlere** Fehler des optimalen Klassifikators auf höchstens Φ(−3) = 0,00134989803163009 festgelegt. Das ist eine neu gewählte Planungskonvention. Zufallszahlentests oder ein Fit an Beobachtungen spielen in dieser Rechnung keine Rolle.

| Breite h | Kleinstes äusseres n bzw. bewiesenes Intervall dafür |
|---|---:|
| 1/8 | **4 915 831** |
| 1/16 | 79 030 352 bis 79 047 392 |
| 1/32 | 1 267 125 541 bis 1 267 193 063 |
| 1/64 | 20 285 605 892 bis 20 285 875 451 |

Schmalere Fenster reduzieren den Glättungsfehler, machen aber die relativen Zählwahrscheinlichkeiten der beiden Modelle ähnlicher. Die Mindestzahl hängt von der Fensterwahl, den zwei fest vorgegebenen Modellen, den beobachteten Daten, dem Zufallsmodell, den Modellchancen und dem Fehlerkriterium ab. Sie ist eine Zahl äusserer Ereignisse. Sie liefert weder eine Mindestgrösse des lokalen N15-Trägers noch einen kosmologischen Prior. Bei n=4 915 831 beträgt der bedingte Fehlanteil unter der flachen Hypothese rund 0,001350028. Separate 3σ-Garantien für beide Hypothesen hätten einen anderen Prüfvertrag.

## Direkter Nachweis der ersten Ganzzahl

Für die beiden Vektoren p und q und die drei Anzahlen k_i ist die optimale Entscheidung durch das Vorzeichen von Σ k_i ln(p_i/q_i) gegeben. Bedingt man auf k₀, ist k₁ binomialverteilt mit m=n−k₀ und Erfolgschance t=p₁/(1−p₀) bzw. q₁/(1−q₀). Für h=1/8 ist die Log-Likelihood-Differenz streng steigend in k₁. Damit genügt pro k₀ eine binomiale Verteilungsfunktion. Die Rechnung schliesst die Logarithmen ein und prüft für jedes ausgewertete k₀ die Vorzeichen beidseits der Entscheidungsschwelle.

Der direkte Prüfer berechnet die Binomialgewichte ab dem Modus mit rationalen Quotienten und gerichteter Festkommarundung. Beide ausgelassenen Randbereiche werden durch geometrische Reihen eingeschlossen. Die bedingten CDFs werden vom Nachbarwert aus der Zerlegung Bin(m,t)=Bin(m−1,t)+Bernoulli(t) fortgesetzt. Die Gaussian-Schwelle selbst ist durch die integrierte alternierende Gaussreihe und eine rationale Einschliessung von π aus der Machin-Formel überprüft.

| n | Untere Schranke für den mittleren Fehler | Obere Schranke |
|---:|---:|---:|
| 4 915 830 | 0,0013498986641144 | 0,0013498986641170 |
| 4 915 831 | 0,0013498973117951 | 0,0013498973117977 |

Eine zusätzliche Beobachtung kann bei optimaler Entscheidung ignoriert werden. Der optimale Fehler ist daher monoton nicht zunehmend. Der Vergleich der zwei Nachbarzahlen mit Φ(−3) entscheidet die Mindestzahl. Die Schranken erlauben zusätzlich eine Störung jedes archivierten Dezimalwertes um 10⁻²⁴ vor Normierung. Dies deckt die Dezimalauflösung des Eingabeartefakts ab. Eine physikalische Modellunsicherheit ist darin nicht enthalten.

## Unabhängige endliche Schranken für alle Breiten

Sei ρ = Σᵢ √(pᵢqᵢ), rᵢ = √(pᵢqᵢ)/ρ und ℓᵢ = ln(pᵢ/qᵢ). Für n unabhängige Kategorienziehungen Xᵢ unter r setze S = Σ ℓ(Xᵢ). Durch min(P,Q)=√(PQ) exp(−|ln(P/Q)|/2) folgt für den Bayes-Fehler exakt

    eₙ = (ρⁿ/2) Eᵣ[exp(−|S|/2)].

Eine grobe Kontrolle ist (1−√(1−ρ²ⁿ))/2 ≤ eₙ ≤ ρⁿ/2. Die untere Schranke folgt aus Cauchy-Schwarz für den Totalvariationsabstand. Für engere Kriterien seien μ=n Eᵣℓ, σ²=n Varᵣℓ und β₃=Eᵣ|ℓ−Eᵣℓ|³/(Varᵣℓ)^(3/2). Der Berry–Esseen-Satz für identisch verteilte Summanden beschränkt den Kolmogorov-Abstand zwischen S und Z∼N(μ,σ²) durch 0,48 β₃/√n. Da exp(−|s|/2) auf der reellen Achse Gesamtvariation 2 hat, beträgt der Fehler der Ersetzung innerhalb des Erwartungswerts höchstens 0,96 β₃/√n. [Konstantenschranke nach Shevtsova](https://arxiv.org/abs/1111.6554)

Das Gaussintegral ist die Summe über ε=−1 und +1 von exp(σ²/8−εμ/2) Φ(εμ/σ−σ/2). Die Endpunktprüfungen verwenden Intervallarithmetik und eine Taylorentwicklung der Fehlerfunktion mit eingeschlossenem Rest. Die untere Schranke wird bei n_unten−1 gegen das Ziel geprüft, die obere bei n_oben. Der Beweis verwendet Monotonie des tatsächlichen optimalen Fehlers. Eine Monotonie der numerischen Näherung wird nicht vorausgesetzt. Für n=15 wird die Trefferquote für alle vier Breiten zusätzlich unmittelbar über die 136 möglichen Anzahldreier nachgerechnet.

## Reproduktion

Die Datei fenster.json ist die unveränderte Eingabe aus dem veröffentlichten N15-Anschlusstest. Beide Programme prüfen ihren SHA-256-Wert. Der direkte Prüfer benötigt Python 3.11 oder neuer. Der Prüfer für alle Fenster verwendet zusätzlich mpmath 1.3.0.

```sh
python -B exakte_schwelle.py
python -B ereigniszahl.py
```

[Quelle der Fensterwahrscheinlichkeiten am publizierten Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/bc909230d38975d3201175b56dfbe9ae8bfda087/research/rax_cqg/dust_collapse/n15_kosmologische_expansion_v0_1/resultate/volumenfenster.json)
