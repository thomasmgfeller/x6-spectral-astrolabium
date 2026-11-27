# Zweitprüfung der zwölf terminalen N24-Restfälle

Alle zwölf im Fallregister durch ein rationales Terminalzertifikat erledigten Kombinationen aus Präparation und Ordnung haben auch in dieser zweiten Rechnung einen exakten Widerspruch. Die zwölf Margen sind positiv und jeweils größer als 1/100000. Bei der Vorgängermenge {0,1,2,3,4,5,6,11,12,15,16,17,19,20,21,22} und A = 0 betragen sie mindestens 0,0002938 (schwer, Strahl 3) und 0,0002935 (leicht, Strahlen 3, 4 und 5). Die Größe einer Marge hängt von der Normierung der Multiplikatoren ab und hat keine physikalische Bedeutung.

## Elimination

Seien z = Y22, t = Y23 und c = k22,23. Für die terminale positive Hilfe ist H23 = 0. Nach Zentrierung am Sondenereignis gelten die Polynome

```text
A = Σ k_i23
U = Σ k_i23 (Yi − z)
V = 19 + Σ k_i23 (Yi − z)²
H23 = A(t − z) − U
D23 = V − 2(t − z) U + A(t − z)².
```

Für A ≠ 0 folgt A V − U² = 0 und für A = 0 folgen U = V = 0. In jeder alten Uhrgleichung wird w23(t − Yi) durch Z + w23(z − Yi) ersetzt, wobei Z = −G22_alt/c aus der freien Uhrgleichung G22 folgt. Somit gelten zusätzlich A Z = w23 U und Z + w23(z − Yi) ≥ 0 für jeden Vorgänger i. Für A = 0 und beliebig spätes t gilt dieselbe Projektion. Die Tabelle der Außenintervalle enthält keine Variable für t.

Der Prüfer rekonstruiert die alten Uhr- und Dichtegleichungen, die projizierten Bedingungen sowie rationale Sekanten- und Tangentenschranken für die Produkte in den Außenintervallen. Für jede Kombination bildet er die hinterlegte nichtnegative Summe notwendiger Ungleichungen der Form p ≤ 0. Die exakte untere Intervallschranke der Summe ist positiv. Je ein Satz rationaler Multiplikatoren genügt für die volle Ausgangsbox.

## Reproduktion und Reichweite

Die Verzeichnisse `positive_probe_next` und `geom_terminal_next` müssen nebeneinander liegen. Aus dem gemeinsamen Oberverzeichnis genügt `python3 -B geom_terminal_next/pruefen_zweit.py`. Der Nachweis nutzt die Python-Standardbibliothek. `Zweitnachweise.json` enthält die Multiplikatoren und `Ergebnisse.json` die erwarteten gekürzten Margen und zugehörigen Strahlen. Die letzte Zahl jeder Fallkennung ist die Bitmaske der Vorgängermenge von Ereignis 23.

Grunddaten, Schichtkoeffizienten und Außenintervallroutinen werden mit dem Hauptlauf geteilt. Die projizierten Polynome, Produktungleichungen, Multiplikatoren und Margenberechnung wurden separat erstellt. Die Rechnung betrifft die zwölf schwersten terminalen Fälle im vorgegebenen N24-Sektor bei normiertem Mittelpunkt. Die Diagnose macht keine Aussage über beliebige N25-Erweiterungen oder physikalische Eichungen.
