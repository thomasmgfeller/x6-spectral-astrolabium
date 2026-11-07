# CST-DUST: Positive Historien und Schnittkonsistenz v0.1

Ein positives Hilfs-Dekohärenzfunktional, sein gemeinsames relatives Bra-/Ket-Maß
und ein präzises Schnittkriterium sind konstruiert. Die physikalische Auswahl
des Randprodukts, der Zustände und der Fortsetzung bleibt offen.

**Neuer Befund:** Ein beschränkter roher Kern bei endlichen Regulatoren ist auf
den deklarierten kontinuierlichen L²-Randräumen kompakt. Er kann nicht durch
eine einzige Normierung auf dem gesamten unendlichdimensionalen Raum isometrisch
werden. Das ist kein No-go für CST oder für kontrollierte singuläre Grenzwerte.

Der Zweistellenzeuge mit L=1 liefert zertifiziert verschiedene Normfaktoren
0.949281765835911… und 0.001646580694214… für zwei normierte orthogonale
Randfunktionen. Die geprüfte Historienpartition interferiert; ihre Diagonalen
sind keine klassischen Bounce-Wahrscheinlichkeiten. Acht physikalische Gates
bleiben HOLD. Frühere Kandidaten-FAILs bleiben bestehen.

## Reproduktion

```bash
python3 -O -B analyze.py
python3 -O -B replay.py
# Optional, braucht NumPy; keine Intervallzertifizierung:
python3 -B verify_quadrature.py
```

`DERIVATION.md` enthält Definitionen, Beweise, Bedingungen und Primärquellen.
`results/` enthält fünf exakt reproduzierte Ergebnisse, die unabhängige
Quadraturkontrolle und die Replay-Quittung. Die numerische Aussage gilt für
den deklarierten Zweistellenkern; es wurden keine neuen physikalischen
4D-Ensembles gerechnet. Der allgemeine Kompaktheitsbeweis ist im Text enthalten,
nicht durch einen formalen Beweisassistenten verifiziert.

`plan.json` wurde vor den Rechnungen gehasht. Die strukturellen Mechanismen
waren bekannt; keine blinde Vorhersage oder externe Präregistrierung.
`supplement_01.json` deklariert die nach dem ersten Kernlauf ergänzten
gemeinsamen Maßmomente und Quadraturen. `inputs/provenance.json` pinnt fünf
bytegleiche Vorgängertexte aus Main nach PR 247. Der Nachtrag ändert den Plan
und die Kernkriterien nicht.

Der PDF-Bericht fasst den Modellvertrag und die Ergebnisse zusammen; die
vollständigen rationalen Zertifikate und Beweise stehen im Prüfpaket.
