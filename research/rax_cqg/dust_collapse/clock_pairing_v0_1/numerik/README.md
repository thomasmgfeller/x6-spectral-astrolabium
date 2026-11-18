# Positiver Referenztransport für höchstens zwei Ereignisse

Der Solver berechnet rationale Übergangsgewichte für die Ordnungen leer, Einzelelement, Zweierkette und Zweierantikette. Er hält das Anfangsprodukt c während jeder Rechnung fest. Der spätere Enduhrwert tritt bei der Definition des Transports nicht auf.

## Nachrechnung

Aus diesem Verzeichnis ausführen. Python 3 und seine Standardbibliothek genügen.

```sh
python3 -O -B solver.py --out replay.json
cmp replay.json ergebnisse.json
```

Ohne Argument liefert das Programm dieselben Daten auf der Standardausgabe. Prüfverletzungen brechen auch im optimierten Python-Modus ab.

## Konstruktion und Geltungsbereich

Für einen Schritt der Länge d hat der unnormierte Kern B(d) Diagonale eins. Vom leeren Zustand zum Einzelelement steht d, zu jeder Zweierordnung w d²/2, vom Einzelelement zu jeder Zweierordnung w d, wobei w = 2⁻ᵅ. Alle übrigen Einträge verschwinden. Wegen B(d) B(e) = B(d+e) und B(0) = I ist B(−s) der algebraische inverse Kern. Ein inverser stochastischer Zeittransport wird dafür nicht vorausgesetzt.

Die Normgewichte h(s) = B(−s)c erfüllen h(a) = B(b−a) h(b). Bei positiven h ergibt Pᵢⱼ(a,b) = Bᵢⱼ(b−a) hⱼ(b)/hᵢ(a) eine zeilenstochastische, schnittkonsistente Übergangsfamilie. In der vollständigen Referenz mit ausgezeichnetem Vergangenheitsrecord entspricht die Zeilensumme der scharfen Zweignorm. Aus dieser Identität folgt keine Isometrie der vier mal vier Matrix P im euklidischen Skalarprodukt. Für gegebenes c ist die Metrik in dieser Klasse eindeutig bestimmt, weil B invertierbar ist.

Setze k = w(c₂+c₃). Dann sind h₁(s)=c₁−ks, h₀(s)=c₀−c₁s+ks²/2 und h₀′(s)=−h₁(s). Für die verwendeten positiven c liegen die Minima aller Komponenten auf [0,1] bei s=1, die oberen beiden Typen haben konstantes Gewicht. Dies gibt einen Positivitätsnachweis über das gesamte Intervall.

## Ergebnisse

Die beiden Primärfälle haben α=1 und c=(1,β,1,1). Angegeben ist die Wahrscheinlichkeit, dass der leere Anfang bei der Ablesung noch leer ist.

| β | Komponentenminima auf [0,1] | u=1/4 | u=1/2 |
| --- | --- | --- | --- |
| 5/4 | (1/4, 1/4, 1, 1) | 23/32 | 1/2 |
| 4/3 | (1/6, 1/3, 1, 1) | 67/96 | 11/24 |

Für jede Festlegung stimmen alle Einträge der direkten und zusammengesetzten Transportmatrizen überein. Mit Schrittweite 1/8 sind es 26 Unterteilungen über alle Endpunktpaare bis 1/2 und 502 bis 1. Die 26 sind im grösseren Satz enthalten. Durch explizites Summieren über die vier letzten Records bei beiden Enduhrwerten bleiben alle geprüften früheren Marginalen gleich. Zur Gegenprobe haben wir die Endnorm für jeden neuen Endwert auf eins zurückgesetzt. Dann erhält man für dasselbe frühe Ereignis bei u=1/4 die Werte 32/41, 41/52 und 13/16, je nachdem ob der Lauf bei 1/4, 1/2 oder 1 endet.

Das JSON enthält zusätzlich vier Referenzen mit c=(3,2,1,1) bzw. (4,2,1,1) und α=1 bzw. 2.

## Abgegrenzter kohärenter Hilfstest

Zusätzlich definiert der Solver einen Registerraum mit erhaltenem Anfangstyp i und abgelesenem Endtyp y. Jede Basisrichtung wird auf die Zweige |i,y⟩ mit positiven Amplituden √Pᵢᵧ abgebildet. Wegen Orthogonalität der Anfangslabels und Zeilennorm eins ist dies eine Isometrie in diesem Hilfsraum. Der Zwischenrecord j kann über die normierte bedingte Brücke mit Koeffizienten √[PᵢⱼPⱼᵧ/Pᵢᵧ] eingefügt werden. Ereignisse mit Pᵢᵧ=0 haben keine befüllte Brücke.

Die abstrakten Präparationen (|leer⟩ ± |ein⟩)/√2 werden bei s=1/8 angesetzt, der Rechenzwischenschnitt liegt bei 3/16, die Auslese bei 1/4. Ein fester Plus-Effekt auf |leer,ein⟩ und |ein,ein⟩ liefert für die beiden Präparationen die Wahrscheinlichkeiten (p+q)/4 ± √(pq)/2, mit p=P(leer,ein), q=P(ein,ein). Der quadrierte Kontrast ist 128/981 bzw. 1352/9367 für die beiden Primärfälle. Am Auslesezeitpunkt gehen beide Beiträge vom gleichen Endtyp ein in die Zukunft. Summieren über jede spätere Fortsetzung mit Gesamtgewicht eins lässt den frühen Record unverändert. Die Hilfspräparation, die positiven Wurzeln und der Effekt sind zusätzliche explizite Modellentscheidungen. Eine physikalisch begründete Präparation und Auslese für kohärente Zeitpakete muss an der ursprünglichen Amplitude gesondert geprüft werden.

Die Zahlen gelten im Vier-Typen-Referenzraum. Die physikalische Auswahl des Anfangsprodukts, ein gekoppeltes Dekohärenzfunktional, die Grenze wachsender Ereigniszahl und die 524 P3-Vergleiche sind eigenständige Aufgaben. Physikalische P3-Vergleiche aus diesem Lauf: 0.
