# Eigenzeit und Volumen zweier kosmologischer Kausaldiamanten

Diese synthetische Kontrolle untersucht ein anderes Gebiet als die drei mitbewegten Messfenster aus PR 366. Die Ereignisse p und q liegen auf derselben komovierenden Geodäte, mitten im homogenen Aussenraum. Ihre Eigenzeiten liegen symmetrisch um die Vergleichsepoche t₀. Der Diamant muss vollständig im homogenen Gebiet liegen. Der Beobachter kann dazu in den beiden räumlich ausgedehnten FLRW-Aussenräumen hinreichend weit von der Vakuumgrenze platziert werden.

## Vergleichsgrösse

Mit c=1, Signatur −+++ und R=8πGρ für drucklosen Einstein-Staub mit Λ=0 ist V_M(τ)=πτ⁴/24 das Vierervolumen des Minkowski-Diamanten. Für kleine Diamanten um eine komovierende Geodäte u ist die führende relative Krümmungskorrektur τ²[R_uu/30−R/180]. Hier bezeichnet R_uu die Kontraktion des Ricci-Tensors mit u. In den zwei Staubhintergründen gilt R/H₀²=3Ωm0 und R_uu/H₀²=3Ωm0/2. Der theoretisch erwartete Grenzwert von c(τ)=(V/V_M−1)/(H₀τ)² beträgt folglich Ωm0/30. Die beiden Arme haben Ωm0 gleich 1 und 64/125. [Gibbons und Solodukhin, Gleichung 73](https://arxiv.org/pdf/hep-th/0703098) · [PR 366](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/366)

## Direkte Lichtkegelintegration

In Einheiten von H₀⁻¹ wird a(0)=1 gesetzt. Die radiale Lichtausbreitung erfüllt dχ=±dη und die Eigenzeit ds=a dη. Die beiden konformen Endzeiten η₋ und η₊ folgen für jede vorgegebene Eigenzeitdauer δ=H₀τ aus s(η₋)=−δ/2 und s(η₊)=δ/2. Ihr arithmetisches Mittel ist die Kreuzung der beiden radialen Lichtkegel. Die Schnittkugel hat Radius χ=min(η−η₋,η₊−η). Das Programm integriert a⁴(η) B(χ) über beide Teilintervalle. Im flachen Raum ist B=4πχ³/3 und im offenen Raum mit β=√Ωk0 gilt B=4π[sinh(2βχ)/(4β³)−χ/(2β²)]. Die verwendeten exakten Staubskalenfaktoren erfüllen (da/dη)²=Ωm0 a+Ωk0 a² und da/dη(0)=1. Als eigenständige Kontrolle werden beide Lichtkegel mit a≡1 und flacher Raumgeometrie ausgewertet. Für diesen statischen Minkowski-Fall bezeichnet δ lediglich die Eigenzeitdauer in denselben Einheiten.

| H₀τ | c(τ), flacher Staub | c(τ), offener Staub |
|---:|---:|---:|
| 1/4 | 0,0339493560 | 0,0173517981 |
| 1/8 | 0,0334847335 | 0,0171369574 |
| 1/16 | 0,0333710244 | 0,0170841785 |
| 1/32 | 0,0333427462 | 0,0170710408 |
| Grenzwert aus der Ricci-Korrektur | 0,0333333333 | 0,0170666667 |

Bei jeder Halbierung fällt die Abweichung vom jeweiligen Sollwert um etwa einen Faktor vier. Die Minkowski-Kontrolle stimmt bei 60 Dezimalstellen auf rund 1,6 × 10⁻⁶¹ relativ mit πτ⁴/24 überein. Das ist ein Test der Integrationsimplementierung. Alle Dauern wurden mit der vorgegebenen Kontinuumsuhr gesetzt. Die Unsicherheit eines diskreten Kettendauerschätzers oder die Auswahl geeigneter Endpunkte geht in diese Kontrolle nicht ein. Der Vergleich testet die Reaktion auf bekannte Hintergrundgeometrien. Für eine Theorievorhersage wären ausserdem äussere Quantendynamik, Zustandsgewichte und optische Distanzen erforderlich.

Python 3 mit mpmath 1.3.0. Der Aufruf erzeugt die vier Ergebniszeilen in diamant.json.

```sh
python -B diamant.py
```
