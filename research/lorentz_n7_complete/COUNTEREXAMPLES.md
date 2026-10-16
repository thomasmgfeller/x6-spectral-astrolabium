# Vollständige Restpaarliste für H7-bidirectional-moments

Beide Paare sind nichtisomorph, haben sieben Elemente, Höhe drei, acht strikte Relationen und je drei minimale/maximale Elemente. Innerhalb eines Paars stimmen sämtliche drei charakteristischen Polynome und beide Gabelzählungen überein.

Die Matrizen kodieren die volle Relation; Zeilen und Spalten sind in derselben Reihenfolge. Jede Zeile enthält sieben Bits, Spaltenindex von links nach rechts. Die IDs gelten für diesen kanonisierten Atlas.

## Paar 1: n7-0475 / n7-0734

`W_future=7`, `W_past=6`. `same_D=false`, `dual_isomorphic=false`.

Gemeinsame monische Polynome als Koeffizientenlisten, absteigend:

| Matrix | Koeffizienten |
|---|---|
| S | `[1, 0, -8, -4, 11, 4, -4, 0]` |
| A | `[1, 0, 8, 0, 11, 0, 4, 0]` |
| K | `[1, 0, -144, -16, 944, 64, -1536, 0]` |

### n7-0475

```text
0000000
0000011
0001111
0000001
0000010
0000000
0000000
```

Gradpaar-Multisatz: `[[0, 0], [0, 2], [0, 4], [1, 1], [1, 1], [3, 0], [3, 0]]`.

Automorphismen: 2; lineare Erweiterungen: 154; natürliche Beschriftungen: 77.

### n7-0734

```text
0000001
0000010
0001111
0000000
0000011
0000000
0000000
```

Gradpaar-Multisatz: `[[0, 1], [0, 1], [0, 4], [1, 0], [1, 2], [3, 0], [3, 0]]`.

Automorphismen: 2; lineare Erweiterungen: 162; natürliche Beschriftungen: 81.

Der linke Repräsentant enthält ein isoliertes Element (Gradpaar `(0,0)`), der rechte keines. Da Isomorphismen isolierte Elemente erhalten, sind die Ordnungen bereits aus diesen Matrizen nachweislich nichtisomorph.

## Paar 2: n7-0588 / n7-1112

`W_future=6`, `W_past=7`. `same_D=false`, `dual_isomorphic=false`.

Gemeinsame monische Polynome als Koeffizientenlisten, absteigend:

| Matrix | Koeffizienten |
|---|---|
| S | `[1, 0, -8, -4, 11, 4, -4, 0]` |
| A | `[1, 0, 8, 0, 11, 0, 4, 0]` |
| K | `[1, 0, -144, 16, 944, -64, -1536, 0]` |

### n7-0588

```text
0000000
0000111
0001011
0000001
0000001
0000000
0000000
```

Gradpaar-Multisatz: `[[0, 0], [0, 3], [0, 3], [1, 1], [1, 1], [2, 0], [4, 0]]`.

Automorphismen: 2; lineare Erweiterungen: 154; natürliche Beschriftungen: 77.

### n7-1112

```text
0000001
0000111
0001011
0000000
0000000
0000001
0000000
```

Gradpaar-Multisatz: `[[0, 1], [0, 3], [0, 3], [1, 0], [1, 0], [2, 1], [4, 0]]`.

Automorphismen: 2; lineare Erweiterungen: 162; natürliche Beschriftungen: 81.

Der linke Repräsentant enthält ein isoliertes Element (Gradpaar `(0,0)`), der rechte keines. Da Isomorphismen isolierte Elemente erhalten, sind die Ordnungen bereits aus diesen Matrizen nachweislich nichtisomorph.

## Folgerungen und Grenzen

Paar 2 ist die Zeitumkehr von Paar 1: links zu links, rechts zu rechts. Der Test quotiert diese Paare nicht zusammen. Die unterschiedlichen ungeraden Koeffizienten von `chi_K` und vertauschten Werte von `W_future/W_past` bleiben erhalten.

Die Gegenbeispiele sind bezüglich der Elementzahl minimal: Der vollständige, separat geprüfte Teilkorpus für n≤6 enthält keine primäre Kollision.

**Mathematische Folgerung:** Für jedes n≥7 gibt es solche Kollisionen. Füge beiden Ordnungen von Paar 1 dieselbe Zahl k=n−7 isolierter Elemente hinzu. S, A und K erhalten jeweils einen k-dimensionalen Nullblock; jedes charakteristische Polynom wird mit t^k multipliziert. Beide Endpunktzahlen steigen um k, beide Gabelzählungen bleiben unverändert. Die Anzahlen isolierter Elemente bleiben verschieden (k+1 gegen k), also bleiben die Ordnungen nichtisomorph. Diese Konstruktion behauptet keine vollständige Enumeration für n≥8.

Das Hinzufügen der Isoliertenzahl zur Signatur trennt diese beiden Paare im n=7-Korpus, wurde aber erst nach dem Resultat betrachtet. Es ändert den Status der getesteten Hypothese nicht; das bekannte verbundene n=8-Paar der Vorgängerstudie bleibt auch für diesen zusätzlichen Skalar ein Gegenbeispiel.

[Maschinenlesbare vollständige Zeugen](results/counterexamples.json) · [Prüfbericht](results/independent-results.json) · [Vertrag und Reproduktion](README.md)
