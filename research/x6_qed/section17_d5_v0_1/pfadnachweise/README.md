# X6-QED §17 · Herkunft der 924 zusätzlichen Fälle

**4. November 2026 · DEVELOPMENT · CAL und C0-VALIDATION auf HOLD**

Die Fälle stammen aus der [veröffentlichten d=5-Auswertung in PR 222](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/bc4ae11e55f032cb977ab722c5fcbad33c16bcd7/research/x6_qed/section17_d5_v0_1). Für den Vergleich wurden dieselben 1.679 nichtleeren Syndrome einzelner vollständiger DEM-Fehlermechanismen, dieselben Cluster, Suchgrenzen und zulässigen Pfade verwendet. Das Erreichen beider Klassen in jedem Cluster öffnet den Margenvergleich. Eine PASS-Entscheidung erfordert zusätzliche Regeln und Evidenz.

## Was sich am Graphen ändert

Die primäre Zuordnung übernimmt die Observable-Maske jeder syntaktischen Komponente. Die Vergleichszuordnung legt das gesamte Observable-XOR eines Quellereignisses auf dessen erste Komponente und setzt seine übrigen Komponenten auf null. Die Gesamtwirkung jeder Quelle auf Detektoren und Observable bleibt erhalten. Verglichen wird der vom Decoder einzeln nutzbare Vorrat an Paaren aus Endpunkten und Masken. Beide Graphen haben 502 verschiedene Endpunktpaare, einschließlich terminaler Boundary-Kanten. 441 behalten ausschließlich ihre alte Maske. Bei 43 Paaren kommt Maske 1 zu Maske 0 hinzu, bei 18 Paaren kommt Maske 0 zu Maske 1 hinzu. Alle bisherigen Möglichkeiten bleiben verfügbar.

Ein *Ort* bezeichnet hier genau ein Endpunktpaar dieses Graphen. Eine *Pfadführung* bezeichnet alle geordneten Detektorfolgen und Boundary-Zuweisungen einer vollständigen Clustererklärung. Um zwei Paritäten bei identischer Pfadführung zu zeigen, wird genau ein Kantenauftreten mit einer anderen Komponentenmaske belegt. Verschiedene Komponenten dürfen im untersuchten C0-Entwicklungsmodell einzeln gewählt werden. Die angegebenen Quellen- und Komponenten-IDs machen die konkrete Auswahl überprüfbar.

## Vollständige Auszählung

| Gruppe | Syndrome | Ergebnis |
|---|---:|---|
| Neu, ein bislang blockierter Cluster | 459 | Eine zusätzliche Maske an einem einzigen Ort genügt, damit alle Cluster beide Klassen erreichen. |
| Neu, zwei bislang blockierte Cluster | 465 | Keine Freischaltung eines einzelnen Ortes genügt. Für jeden Fall ist ein hinreichendes Paar verschiedener Orte nachgewiesen. |
| Bereits mit der primären Zuordnung erreichbar | 55 | Bei allen 55 sind zwei verschiedene Paarungen erforderlich. Die Detektor-Detektor-Verbindung ergibt Klasse 0, zwei separate Boundary-Zuweisungen ergeben Klasse 1. |
| Unter beiden Zuordnungen blockiert | 700 | Mindestens ein Cluster bleibt einklassig. |

Für jedes der 924 neu hinzukommenden Syndrome existiert unter der Vergleichszuordnung **in jedem Cluster** ein Paar von Erklärungen mit identischer Pfadführung und genau einem geänderten Maskenbit. Bei keinem ist eine neue Pfadführung zwischen diesen beiden Erklärungen nötig. Eine beliebig vorab gewählte oder kürzeste Primärroute muss dafür nicht geeignet sein. Die Minimalzahlen 1 und 2 zählen Freischaltungen im Graphen, die für alle ursprünglich blockierten Cluster eines Syndroms gemeinsam ausreichen. Auch für die 55 Kontrollen erlaubt die alternative Zuordnung Beispiele mit identischer Führung.

Bei 750 der 924 Fälle war zunächst auch das XOR des gesamten Shots eindeutig. Bei 174 waren bereits beide Shot-Paritäten erreichbar, aber ein anderer Cluster löste §17.2 aus. Das erklärt, warum der Wechsel des Shot-Status und eine neu erreichbare Shot-Parität getrennt ausgewiesen werden.

## Zwei Beispiele

**D0.** In der primären Zuordnung trägt die Kante D0–Boundary nur Bit 1. Die vollständige Quelle 2 besteht aus genau dieser Komponente. In der Alternative kann auf denselben Endpunkten Bit 0 gewählt werden. Dieser Beitrag stammt beispielsweise aus Komponente 1 der Quelle 162. Die ganze Quelle 162 kippt D0 **und D12** und hat logisches Gesamtbit 0. Der lokale Decoder kann den D0-Anteil der zerlegten Quelle allein wählen. Alle vollständigen einzelnen Quellereignisse für das Syndrom ausschließlich D0 haben Bit 1.

**D3 und D6.** Dieses Syndrom gehört zu den 55 Kontrollen. Der direkte Pfad D3–D6 hat in der primären Zuordnung Parität 0. Die terminalen Pfade D3–D0–Boundary und D6–D9–Boundary ergeben zusammen Parität 1. Die Abfrage aller zulässigen Pfade bestätigt für jeden der 55 Fälle, dass erst der Wechsel der Paarungsstruktur beide Klassen liefert.

Für jedes der 979 untersuchten Syndrome ergeben alle vollständigen einzelnen DEM-Fehlerereignisse mit passendem Detektorvektor jeweils nur eine logische Klasse. Das grenzt den Einzelfehlervergleich ein. Kombinationen mehrerer Quellereignisse können andere Paritäten liefern. Aus den lokalen Zeugen folgen weder Wahrscheinlichkeiten noch eine Fehlerrate oder ein physikalischer Fehlerkorrekturnachweis.

## Gegenprüfung

- Die Klassenmengen für beide Konventionen wurden für alle 1.679 Syndrome mit der veröffentlichten Tabelle verglichen.
- Ein separater Prüfer verifiziert 5.083 konkrete Erklärungen direkt anhand der Quellkomponenten, einschließlich Endpunkten, terminaler Boundary, Pfadlänge, Parität und Abdeckung aktiver Detektoren.
- Das zweite Suchverfahren aus PR 222 schaltete die 61 Orte einzeln frei und prüfte jeden gegen alle 1.679 Syndrome, insgesamt 102.419 Entscheidungen. Die zugehörigen 465 Doppel-Fälle wurden zusätzlich mit ihren ausgewiesenen Ortspaaren geprüft (99 verschiedene Paare). Ausgangsgraph und vollständige Vergleichszuordnung wurden ebenfalls gegengeprüft.

## Dateien und Wiederholung

- `results/cases.csv` enthält eine Zeile pro neuem oder gemeinsamem Fall. `min_distinct_sites` gibt die minimale Zahl aktivierter Orte an.
- `results/witnesses.jsonl` enthält für jedes dieser Syndrome sämtliche Cluster. Die Felder `primary` und `alternative` liefern je erreichbarer Klasse einen konkreten Zeugen. Eine Zeile wird mit Standard-JSON eingelesen. `paths` verwendet den Wert −1 für die Boundary.
- In `steps` bedeutet jedes Vierertupel der Reihe nach *Orts-ID, Maskenbit, Quellereignis-ID, Komponentenindex* (nullbasiert). Die Schritte folgen den Pfaden in derselben Reihenfolge. `sufficient_sites` ist eine konkret hinreichende minimale Ortsmenge. `single_whole_event_ids_by_bit` bezeichnet alle ganzen einzelnen Quellereignisse mit genau dem beobachteten Syndrom.
- `results/sites.json` enthält je Ort die Endpunkte und sämtliche zugelassenen Quellkomponenten je Maske. Liste 0 bezeichnet die syntaktische Zuordnung, Liste 1 die Vergleichszuordnung.
- `in/results/development_sources.json` enthält die ursprünglichen Detektoren, Masken und Quellwahrscheinlichkeiten. `in/protocol.json` beschreibt den ursprünglichen Suchraum, `rules.json` diese Folgeauswertung. Die Eingabedateien wurden gegen den Commit bc4ae11e55f032cb977ab722c5fcbad33c16bcd7 geprüft.
- `results/summary.json` und `results/verification.json` enthalten die maschinenlesbaren Zähler.

Vom entpackten Verzeichnis aus genügen Python 3.12 und die Standardbibliothek. Die Ausgabe enthält keine Zufallszahlen. Beide Programme ohne Optimierungsflag starten, damit die Prüfbedingungen ausgeführt werden.

```sh
sha256sum -c SHA256SUMS.txt
python3 trace.py replay
python3 check.py replay
diff -r results replay
```
