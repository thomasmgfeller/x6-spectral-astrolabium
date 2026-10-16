# Zwei verschiedene Ordnungen mit gleichem H7+N1+Q1+R2

**Endliches Gegenbeispiel:** `closed-rook` und `closed-shrikhande`, jeweils
32 Elemente, erfüllen sämtliche Gleichheiten des bisherigen Merkmalsbündels.
Eine gerichtete Isomorphie ist durch das unten angegebene Zählzertifikat
ausgeschlossen. Es wird weder Minimalität noch Neuheit der Graphkonstruktion behauptet.

Die Konstruktion, beide Eingaben und das Vierer-Zertifikat wurden im Vertrag vor
der Zielerzeugung festgelegt. Die algebraische Erklärung in Abschnitt 4 und
`explain.py` entstanden **nach** der Auswertung. Sie sind keine weiteren
Kandidaten des eingefrorenen Vergleichs.

## 1. Vollständige Relationen

Die unteren Elemente sind 0,…,15, die oberen 16,…,31. Für jedes der beiden
folgenden B gilt C[i,16+j]=B[i,j]; alle anderen C-Einträge sind null. Damit
ist C bereits strikt und transitiv. Die Ausgangsgraphen haben Koordinaten
(a,b) in Z₄² und die Nummer 4a+b; B enthält deren geschlossene Nachbarschaften.

### closed-rook

```text
1111100010001000
1111010001000100
1111001000100010
1111000100010001
1000111110001000
0100111101000100
0010111100100010
0001111100010001
1000100011111000
0100010011110100
0010001011110010
0001000111110001
1000100010001111
0100010001001111
0010001000101111
0001000100011111
```

### closed-shrikhande

```text
1101110000001001
1110011000001100
0111001100000110
1011100100000011
1001110111000000
1100111001100000
0110011100110000
0011101110010000
0000100111011100
0000110011100110
0000011001110011
0000001110111001
1100000010011101
0110000011001110
0011000001100111
1001000000111011
```

Jede Zeile und jede Spalte hat Summe sieben. Beide B sind symmetrisch.
Eine Vertauschung der unteren und oberen Schicht bildet die umgekehrte Relation
wieder auf C ab: Beide Ordnungen sind selbstdual.

## 2. Exaktes Nichtisomorphiezeugnis

Für jede der binomial(16,4)=1.820 Vierermengen U der unteren Schicht wird
die Anzahl gemeinsamer Nachfolger gezählt. Das vollständige Histogramm lautet:

| Gemeinsame Nachfolger | closed-rook: Vierermengen | closed-shrikhande: Vierermengen |
|---:|---:|---:|
| 0 | 1.284 | 1.308 |
| 1 | 528 | 464 |
| 2 | 0 | 48 |
| 3 | 0 | 0 |
| 4 | 8 | 0 |
| 5–16 | 0 | 0 |
| Insgesamt | 1.820 | 1.820 |

Beispielsweise hat bei `closed-rook` die Vierermenge {0,1,2,3} genau die
Nachfolger {16,17,18,19} gemeinsam. Bei `closed-shrikhande` existiert keine
Vierermenge mit vier gemeinsamen Nachfolgern. Die oberen Vierermengen liefern
dieselben Häufigkeiten für gemeinsame Vorgänger.

Eine gerichtete Isomorphie muss die durch ihre Grade erkennbaren Schichten
aufeinander abbilden. Sie induziert eine Bijektion der Vierermengen und ihrer
gemeinsamen Nachfolger. Daher müsste sie das Histogramm erhalten. Die Häufigkeiten
8 und 0 widersprechen dem; die Ordnungen sind nichtisomorph. Wegen ihrer
Selbstdualität gilt das auch nach Umkehrung einer der beiden Relationen.
Das vollständige Histogramm wird im eingefrorenen Produzenten durch Bitmengen
und im getrennten Prüfer durch explizite Inzidenzzählung berechnet.

## 3. Welche Informationen gemeinsam gleich bleiben

H7 hat n=32, jeweils 16 minimale/maximale Elemente und beide Gabelzählungen
gleich 336. Seine drei charakteristischen Polynome sind:

$$
\chi_S(x)=(x^2-49)(x^2-9)^6(x^2-1)^9,
$$
$$
\chi_A(x)=(x^2+49)(x^2+9)^6(x^2+1)^9,
$$
$$
\chi_K(x)=(x^2-9604)(x^2-324)^6(x^2-4)^9.
$$

Hier bezeichnet A im H7-Ausdruck die antisymmetrische Relationsmatrix C−Cᵀ,
nicht die unten als G bezeichnete Graphadjazenz. K=2(CᵀC−CCᵀ).
Die Faktoren wurden nachträglich ausmultipliziert und mit den zuvor zweifach
berechneten Koeffizienten verglichen.

N1 ist bei jeder unteren Wurzel das Profil eines Elements mit Gradpaar (0,7)
und sieben Nachfolgern mit Gradpaar (7,0); oben gilt das umgekehrte Profil.
Q1 stimmt als vollständiges Multiset der geordneten Zukunft-/Vergangenheitspaare
pro Wurzel überein. Die Gleichheit ist für alle Koeffizienten geprüft, nicht
aus gerundeten Eigenwerten abgeleitet. Die vollständigen Decks stehen in
[records.jsonl.gz](results/records.jsonl.gz).

R2 hat in den vier archivierten Runden 8,10,12,12 gemeinsame Farben.
Beide Histogramme stimmen in jeder Runde überein. Die letzte Runde ohne
Aufspaltung ist ein Stabilitätsnachweis, da jede Signatur ihre alte Farbe behält.

## 4. Warum weitere R2-Runden nicht helfen

Dies ist eine nachträgliche Erklärung des endlichen Ergebnisses. Sei G die
Adjazenz eines der beiden stark regulären Graphen und N=J−I−G die Relation
verschiedener nicht benachbarter Knoten. Beide Graphen haben dieselben Parameter
(16,6,2,2). Die drei disjunkten Relationsmatrizen erfüllen:

$$
G^2=6I+2G+2N,\qquad GN=NG=3G+4N,\qquad N^2=9I+6G+4N.
$$

Diese Gleichungen werden für beide archivierten Matrizen durch exakte
ganzzahlige Multiplikation geprüft. I ist das Einselement. Somit sind alle
Zwischenknotenzahlen für zwei Relationstypen konstant auf dem Endpunkttyp
I, G oder N und stimmen zwischen beiden Graphen überein.

Betrachte nun eine Hilfspartition der geordneten Paare der 32-Elemente-Ordnung:
zwei Schichtangaben und einer der drei Typen I,G,N. Sie hat zwölf Klassen.
Die anfänglichen R2-Farben sind auf jeder dieser Klassen konstant, denn
B=I+G und die Grade sind innerhalb jeder Schicht gleich. Ist das für Runde t
wahr, so hängen auch sämtliche geordneten Zwischenfarben-Häufigkeiten der
Runde t+1 nur vom Hilfsklassentyp ab: Sie sind Summen der obigen gemeinsamen
Multiplikationskonstanten. Induktiv kann R2 keine Hilfsklasse weiter aufspalten,
und dieselben Klassen haben in beiden Ordnungen dieselben Farben.

Jeder Schichtblock enthält 16 Paare vom Typ I, 96 vom Typ G und 144 vom Typ N.
Die Klassenhäufigkeiten sind damit ebenfalls identisch. Folglich bleiben die
R2-Histogramme **in jeder Runde** gleich. Dies erklärt die Grenze auf diesem
Paar; es behauptet keine allgemeine Gleichwertigkeit mit H7 oder Q1.

## 5. Nachprüfen

Der eingefrorene vollständige Lauf steht in [README.md](README.md).
Die getrennt gekennzeichnete nachträgliche Prüfung läuft mit:

```sh
python3 -B -O research/lorentz_relational_transfer/explain.py
```

Sie prüft die Algebra, alle H7-Faktoren, gemeinsame Farben der zwölf Hilfsklassen
in jeder archivierten Runde und die Gleichheit des gesamten Merkmalsbündels.
Zusätzlich verwirft sie einen entfernten R2-Histogrammeintrag auf
Multiplizitätsebene und ein ausgelassenes Restpaar. Der ursprüngliche eingefrorene
Negativtest erhöhte die Multiplizität um eins; die ergänzende Verringerung um eins
ist ausdrücklich nachträglich dokumentiert. Keine eingefrorenen Quellen oder
Ergebnisse wurden dafür geändert. Die Quittung ist [explanation.json](results/explanation.json).

Die graphentheoretische Einordnung folgt
[Brouwers Beschreibung](https://aeb.win.tue.nl/graphs/Shrikhande.html) und der
[WL-Literatur](https://arxiv.org/abs/2005.08887). Insbesondere darf B=I+G nicht
mit dem gewöhnlichen bipartiten Doppelgraphen B=G verwechselt werden; letzterer
ist für diese beiden Ausgangsgraphen isomorph und liefert dieses Zeugnis nicht.
