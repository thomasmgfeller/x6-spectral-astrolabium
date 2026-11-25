# Welche N15-Ordnungen unterscheiden kausale Diamanten?

Ein Test mit den 1 048 zugelassenen Typen des veröffentlichten Sieben-Ereignis-Katalogs, ergänzt um dieselben zwei Viererkragen. Die Signatur eines Paars p ≺ q ist (m,l). Hier ist m die Zahl der Elemente im offenen Intervall, l die Zahl der Schritte auf der längsten Kette von p nach q einschliesslich der Endpunkte. Bei einem Link ist (m,l) = (0,1). Ein gerichtetes Intervall mit l Schritten enthält auf dieser Kette l+1 Elemente.

| Labels der gemessenen Paare | Verschiedene Ergebnisse | Eindeutig identifizierte Typen | Grösste Klasse |
|---|---:|---:|---:|
| Letztes Ereignis des Eingangskragens und erstes des Ausgangskragens | 6 | 1 | 442 |
| Multimenge von (m,l) über alle vergleichbaren Paare | 527 | 66 | 6 |
| Multimenge mit zusätzlichem Sektor beider Endpunkte (Vergangenheit, Inneres, Zukunft) | 1 021 | 996 | 4 |

Der feste Kragendiamant enthält alle sieben inneren Ereignisse. Seine Länge unterscheidet sechs Klassen. Bei der dritten Auslese liegen 52 Typen in 25 mehrfach besetzten Klassen. Die Typen 37724 und 37738 haben dieselbe Multimenge einschliesslich aller Endpunktsektoren. Typ 37724 hat ein isoliertes Element in der auf das Innere eingeschränkten Ordnung, Typ 37738 keines. Die beiden inneren Ordnungen sind damit weder isomorph noch durch Zeitumkehr ineinander überführbar. Dies wird zusätzlich durch Vergleich sämtlicher 7! Bijektionen geprüft.

Die Multimengen vergessen, welche Paare einen Endpunkt teilen. Die Aussage betrifft darum genau die drei definierten Auslesen. Sie liefert einen Testfall für weitere dynamische Prüfungen. Ob zusammengefasste Historien gleiche physikalische Aussagen erlauben, muss für das Zielobservable untersucht werden. Dynamischer Zeiger, Dekohärenz, Staubzeit, FLRW-Region und kosmische Rotverschiebung verlangen eigene Herleitungen. Aus einer Kollisionszahl folgt kein Wahrscheinlichkeitsmass über Typen.

**Reproduktion.** Mit Python 3 aus diesem Ordner und einer Kopie des unveränderten Projektkatalogs:

```sh
python -B diamanten.py /pfad/zu/gesamtkatalog.json --out neurechnung.json
cmp result.json neurechnung.json
```

Der SHA-256-Inhaltswert des Katalogs ist im Code hinterlegt. Der erste Algorithmus berechnet die längsten Ketten durch gerichtete dynamische Programmierung. Ein zweiter Algorithmus enumeriert sämtliche inneren Teilketten und ergänzt die linear vergleichbaren Kragenelemente des Intervalls. Beide prüfen alle 100 302 vergleichbaren Paare. Ein expliziter Etikettenwechsel mit transportierten Sektormarken kontrolliert die Implementierung. Die Invarianz für jede Isomorphie folgt aus der Bijektion der Paare, offenen Intervalle und Ketten.

[Originalkatalog am publizierten Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/bc909230d38975d3201175b56dfbe9ae8bfda087/research/rax_cqg/dust_collapse/n15_kosmologische_expansion_v0_1/quellen/gesamtkatalog.json) · [Kodierung und Kragen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/bc909230d38975d3201175b56dfbe9ae8bfda087/research/rax_cqg/dust_collapse/n15_kosmologische_expansion_v0_1/quellen/support.py) · [Brightwell und Gregory](https://doi.org/10.1103/PhysRevLett.66.260) · [Gibbons und Solodukhin](https://arxiv.org/abs/hep-th/0703098) · [Roy, Sinha und Surya](https://doi.org/10.1103/PhysRevD.87.044046)
