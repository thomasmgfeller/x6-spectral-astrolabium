# Lorentz: vollständige exakte Prüfung bis n=7

**Ergebnis vom 16. Oktober 2026: H7-bidirectional-moments ist widerlegt.**
Für alle 2.045 nichtisomorphen strikten Ordnungen mit sieben Elementen liefern
`(F0, W_future, W_past)` nur **2.043 Signaturklassen**. Genau zwei Klassen enthalten
je zwei nichtisomorphe Ordnungen. Alle vier Ordnungen haben Höhe drei.
Die vollständigen Gegenbeispiele bleiben [lesbar](COUNTEREXAMPLES.md) und
[maschinenlesbar](results/counterexamples.json) erhalten.

Das ist ein exaktes endliches Rechenergebnis mit algorithmisch getrennter
Gegenprüfung. Es ist keine externe menschliche Begutachtung und keine physikalische
Bestätigung von Raumzeit, relationaler Zeit oder Quantengravitation.

## Fragestellung und Konventionen

Geprüft wurde ausschließlich die vorab festgelegte Implikation

\[
1\leq |P|=|Q|\leq7,\quad
(F_0,W_+,W_-)(P)=(F_0,W_+,W_-)(Q)\ \Longrightarrow\ P\cong Q.
\]

`C[i][j]=1` bedeutet `i<j` in der **vollständigen strikten transitiven Relation**,
nicht nur im Hasse-Diagramm. Die Zahl der Elemente ist kein physikalischer Zeitparameter.

\[
S=C+C^T,\qquad A=C-C^T,\qquad
K=SA-AS=2(C^TC-CC^T).
\]

`F0=(n, chi_S, chi_A, chi_K, n_min, n_max)`, mit `chi_M(t)=det(tI-M)`.
Die gespeicherten Koeffizienten stehen in absteigender Potenzreihenfolge.
`W_future=sum_v binomial(outdegree(v),2)` und
`W_past=sum_v binomial(indegree(v),2)` zählen gerichtete Gabeln; zwischen deren
beiden Endpunkten wird keine Unvergleichbarkeit verlangt.
Isomorphien erhalten die Richtung. Zeitumkehr wird nicht als zusätzliche
Äquivalenz eingeführt. Isolierte Elemente gehören zur Population.

Der stärkere Gradpaar-Multisatz `D` wird nur als diagnostische Kontrolle berichtet.
Er ersetzt die beiden Skalare **nicht** im Hypothesentest.

## Vollständiges Resultat

| n | Ordnungen | F0 | F0 + W_future | F0 + W_future + W_past | F0 + D |
|---|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 | 2 | 2 |
| 3 | 5 | 5 | 5 | 5 | 5 |
| 4 | 16 | 16 | 16 | 16 | 16 |
| 5 | 63 | 63 | 63 | 63 | 63 |
| 6 | 318 | 314 | 318 | 318 | 318 |
| 7 | 2.045 | 2.037 | 2.042 | **2.043** | 2.045 |

Die Zahlen in den letzten vier Spalten zählen Signaturklassen, nicht die Anzahl
einzeln identifizierter Ordnungen. Für die primäre Signatur bei n=7 gibt es
2.041 Einzelklassen und zwei Zweierklassen. n=7 ist im untersuchten Sinn die
kleinste Gegenbeispielgröße. Die frühere positive Prüfung aller 164 Ordnungen mit
Höhe höchstens zwei wird reproduziert; die beiden neuen Paare liegen außerhalb
dieser Teilpopulation.

Insgesamt wurden 2.450 Repräsentanten und 7.350 charakteristische Polynome exakt
gegengerechnet. Der zweite Enumerator untersucht bei n=7 alle `2^21=2.097.152`
oberen binären Matrizen. Genau 96.428 sind transitive, natürlich beschriftete
Ordnungen. Jede wird genau einem Repräsentanten zugeordnet. Die entsprechenden
Anzahlen für n=1 bis 6 sind 1, 2, 7, 40, 357 und 4.824.

## Warum die Population vollständig ist

Der Produzent fügt jeder kleineren Ordnung einen maximalen Punkt hinzu, dessen
Vergangenheit jedes mögliche Ordnungsideal durchläuft. Jede endliche Ordnung
entsteht so: Entferne einen maximalen Punkt und betrachte dessen strikte
Vergangenheit im Rest. Sie ist ein Ordnungsideal. Durch Induktion wird deshalb
jede Isomorphieklasse erreicht. Innerhalb der nach Ein-/Ausgangsgrad sortierten
Klassen werden alle Permutationen durchlaufen; das minimale Matrixwort liefert
einen eindeutigen Repräsentanten. Isomorphismen müssen diese Gradklassen erhalten.

Der Gegenprüfer benutzt diesen Generator und diese Kanonisierung nicht. Jede
endliche Ordnung besitzt eine lineare Erweiterung und damit eine obere
Relationsmatrix. Alle oberen Binärmatrizen werden durchlaufen; das Bitkriterium
`i<j => successors(j) subset successors(i)` testet genau Transitivität.
Eine gerichtete Bijektionssuche prüft sowohl die paarweise Verschiedenheit der
Repräsentanten als auch die eindeutige Zuordnung jeder gültigen Matrix.
Die bloße Übereinstimmung mit bekannten Anzahlen ist somit nicht das einzige
Vollständigkeitsargument.

Zusätzlich wird die Zahl natürlicher Beschriftungen pro Klasse überprüft:
Sie ist `L(P)/|Aut(P)|`. Der Produzent zählt lineare Erweiterungen per
Teilmengenrekursion und Automorphismen per Gradklassenpermutation; der Gegenprüfer
zählt natürliche Matrizen und Automorphismen per gerichteter Bijektionssuche.
Die freie Wirkung von `Aut(P)` auf den linearen Erweiterungen begründet die Formel.
`ideal_extensions` im Atlas ist nur Produzententelemetrie, kein separat geprüftes
Ergebnis des zweiten Enumerators.

## Exakte Algebra und Fehlerkontrollen

Der Produzent verwendet Faddeev–LeVerrier mit exakten Divisionen und
Cayley–Hamilton-Restprüfung. Der Gegenprüfer berechnet Determinanten mit pivotiertem
Bareiss-Verfahren an n+1 ganzzahligen Stellen und interpoliert rational exakt.
Er konstruiert K direkt über `2(C^TC-CC^T)` und zählt Gabeln ausdrücklich als
Tripel. Er importiert keinen Produzentencode. Die Implementierungen wurden im
selben Arbeitsprozess erstellt; gemeinsame konzeptionelle Fehler sind dadurch
nicht ausgeschlossen.

Vor dem Hauptlauf bestanden n≤4 und handrechenbare Ankerfälle. Im Hauptlauf
bestanden außerdem 17 Kontrollgruppen: eine Gruppe exakter Anker und 16
Zurückweisungskontrollen, darunter doppelte Isomorphieklassen, falsche Polynome,
falsche Zählgrößen, koordinierte Manipulation von Automorphismen/Erweiterungen und
fehlende tatsächliche Gegenbeispiele. Die Prüfungen bleiben unter `python -O`
aktiv. Alle Vergleiche verwenden ganze oder rationale Zahlen ohne Toleranz.

## Eingefrorener Vertrag und Reproduktion

[Vertrag](contract.json), Implementierungen und [Quellhashes](freeze.json) wurden
vor dem vollständigen n=7-Lauf im Commit
[`ab3e4f5dd534f94940e0d72602d11e89403a6b9f`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/ab3e4f5dd534f94940e0d72602d11e89403a6b9f)
veröffentlicht. Dies ist ein prospektiv fixierter Arbeitsablauf, keine externe
Präregistrierung. Die bekannten n≤6- und Höhe-zwei-Ergebnisse waren vorher bekannt.

Python 3.12 unter Linux/POSIX, ausschließlich Standardbibliothek:

```sh
python3 -O research/lorentz_n7_complete/run.py --verify research/lorentz_n7_complete/results
python3 research/lorentz_n7_complete/run.py --run /tmp/lorentz-n7-new-run
```

Der erste Befehl prüft Quell-/Artefakthashes und berechnet die vollständige
Gegenprüfung neu. Der zweite erzeugt beide Rechnungen in einem **neuen** Ordner.
Je Phase gelten 600 Sekunden und 1 GiB Adressraum; Überschreitungen oder
Widersprüche ergeben `INCONCLUSIVE`. Die Rechnung benötigt kein Netzwerk;
die GitHub-CI wiederholt sie in einem Netzwerk-Namespace ohne externe Verbindung.
Erfolgreiche Softwareprüfung (`PASS_EXACT_COUNTERCHECK`) und widerlegte Hypothese
(`REFUTED_BY_COUNTEREXAMPLE`) sind bewusst verschiedene Statusfelder.

[RESULTS.json](results/RESULTS.json) bindet die Resultate an die eingefrorenen
Quellen. [Atlas](results/atlas.json), [Gegenprüfbericht](results/independent-results.json),
[Kontrollen](results/controls.json) und beide Phasenprotokolle sind vollständig erhalten.
Der ursprüngliche Lauf benötigte etwa 2,8 bzw. 9,2 Sekunden; das ist eine
Umgebungsbeobachtung, kein Leistungsversprechen. Dieses Modul hat eine eigene CI;
es erweitert nicht nachträglich die eingefrorene gemeinsame Zehn-Berichte-Suite.

## Einordnung und nächste Arbeit

Die Spektral-/Gradidee ist bereits in Yazdi, Letizia und Kempf,
[*Lorentzian Spectral Geometry with Causal Sets*](https://arxiv.org/abs/2008.02291),
Abschnitt 3.2/Tabelle 2, untersucht. Dort werden 2.037 Klassen mit Spektren und
Endpunktzahlen sowie 2.045 mit Gradpaaren für n=7 berichtet. Das Gradbeispiel in
Abbildung 1 zählt Hasse-Kanten; hier sind ausdrücklich Vollrelationsgrade definiert.
Zahlengleichheit allein belegt keine Identität der Gradkonventionen. Neuheit der
hier dokumentierten skalaren Gegenbeispiele wird ohne breitere Literaturprüfung
nicht beansprucht.

Die zwei Paare sind zueinander zeitumgekehrte Paare. Innerhalb eines Paars sind
die Ordnungen nicht dual zueinander. Bereits die Zahl isolierter Elemente (1
gegen 0) beweist ihre Nichtisomorphie. Dass dieser zusätzliche Skalar die beiden
Restpaare trennt, ist eine **nachträgliche Beobachtung**, keine Rettung der
ursprünglichen Hypothese. Die allgemeinere Variante scheitert ebenfalls schon am
bekannten verbundenen n=8-Gegenbeispiel aus der [Vorgängerstudie](../lorentz_n6_residuals/README.md).

Als nächstes sinnvoll: die Struktur der minimalen Gegenbeispiele mathematisch
erklären und daraus eine begrenzte neue Aussage mit klaren Voraussetzungen
ableiten. Eine unabhängige externe Replikation bleibt offen. Größere Durchläufe
sollten einer neuen präzisen Frage folgen, da die unveränderte H7-Signatur
bereits widerlegt ist.
