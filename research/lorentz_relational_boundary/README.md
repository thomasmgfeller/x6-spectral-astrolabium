# Schnittprofile: begrenzte Rekonstruktion und nachgewiesener Informationsverlust

Das bekannte 32-Elemente-Gegenbeispiel wird bereits durch **dreifache gemeinsame
Nachbarschaften** getrennt. Dennoch liefern selbst die Histogramme sämtlicher
Schnittordnungen allgemein keinen eindeutigen Identifikator. Eine explizite
Gegenbeispielfamilie beweist dies für jede gerade Elementzahl n≥12.

Ein präziser positiver Befund steht daneben: Behält man die **Zuordnung zu den
jeweiligen Teilmengen** und eine bekannte Gradschranke, lassen sich die Spalten
einer Zweischichten-Inzidenzmatrix exakt rekonstruieren. Hier gelangen alle
**434 Rekonstruktionen** – 217 Ordnungen in beiden Richtungen. Dies ist eine
beschriftete Darstellung mit einem eingeschränkten Rekonstruktionssatz, kein
kompakter universeller Fingerabdruck und keine Lösung des allgemeinen
Isomorphieproblems.

## Untersuchungsstatus und öffentlicher Ablauf

Die Studie ist eine **Diagnose bekannter Daten mit theoriegeleiteten Kontrollen**.
Die 207 ursprünglichen Stressordnungen sowie `closed-rook` und
`closed-shrikhande` waren bekannt. Auch die Trennung des letzten Paars durch
Viererschnitte war bereits bekannt. Die zusätzlichen acht Zyklusordnungen wurden
gezielt als erwartete Gegenbeispiele ausgewählt. Es gibt keine blinde Validierung
oder Aussage über eine zufällig gezogene Population.

Der [Vertrag](contract.json) wurde im Commit
[`6b0db84`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/6b0db8489794ac1c006bd568ac3e4c625fe1ea4a)
am **16.10.2026 um 14:36:29 UTC** öffentlich festgelegt. Nach den Kleintests
folgte die [Quellenfixierung](freeze.json) im Commit
[`99ecd62`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/99ecd6271b9664beadbb38117c641d5c3fcb779f)
um **14:43:41 UTC**. Erst danach begann die neue Zielauswertung um
14:43:49 UTC; sie endete um 14:45:11 UTC. Die Ausführungsquellen blieben erhalten.
Die Chronologie steht in [publication.json](publication.json), die ursprüngliche
Laufquittung mit allen Dateihashes in [RESULTS.json](results/RESULTS.json).

## Vollständiger fester Vergleich

Der Korpus enthält alle 207 ursprünglichen Stressrepräsentanten, die beiden
32-Elemente-Kontrollen und jeweils zwei Zyklusordnungen mit 12,14,16,18 Elementen.
Alle **217** Eingaben sind verschieden bis auf gerichtete Isomorphie.
Sämtliche **7.088 größeninternen Paare** wurden neu gegengeprüft.
Die Referenz verwendet vollständige Relationen beziehungsweise beim 32er-Paar
das getrennt berechnete vollständige Vierer-Schnittzertifikat.

`P1`, `P12`, `P123` und `P1234` behalten die Histogramme bis zur ersten, zweiten,
dritten beziehungsweise vierten Schnittordnung. `Pall` behält alle Ordnungen,
jeweils einschließlich der Nullwerte, Multiplizitäten und getrennten Zukunft-/
Vergangenheitsrichtung. Bei einer Gradschranke d sind alle Schnitte mit mehr
als d Wurzeln leer; ihre binomialen Nullmultiplizitäten werden dennoch gespeichert.

**P123 ist nicht das frühere I3:** I3 bewahrt zusätzlich innerhalb jeder
Dreiergruppe ihre drei paarweisen Schnittgrößen. Die hier verglichenen reinen
Histogramme verlieren diese Zuordnung und sind schwächer.

R2 verwendet unverändert die bisherigen beiden Kerne. Seine Farben wurden für
den gesamten neuen Korpus jeder Größe gemeinsam neu berechnet. Alte Farbnummern
wurden nicht zwischen verschiedenen Korpora verglichen.

| n | Ordnungen | Nichtisomorphe Paare | P12 offen | P123 offen | Pall offen | R2 offen | R2+Pall offen |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 12 | 8 | 28 | 1 | 1 | 1 | 0 | 0 |
| 14 | 13 | 78 | 2 | 2 | 2 | 0 | 0 |
| 16 | 34 | 561 | 30 | 30 | 30 | 0 | 0 |
| 18 | 70 | 2.415 | 318 | 318 | 318 | 0 | 0 |
| 20 | 90 | 4.005 | 535 | 535 | 535 | 0 | 0 |
| 32 | 2 | 1 | 1 | 0 | 0 | 1 | 0 |
| Insgesamt | 217 | 7.088 | 887 | 886 | 886 | 1 | 0 |

R2 und Pall ergänzen sich auf diesem festen Korpus: Das 32er-Paar wird durch
Pall, die anderen 886 Pall-Restpaare durch R2 getrennt. **Dass die Kombination
hier alle Paare trennt, ist keine allgemeine Eindeutigkeitsgarantie.** H7+N1+Q1
allein lässt zwei Paare offen, das ursprüngliche 16er- und das 32er-Paar.
Alle neun festgelegten Verfahren, vollständigen Restpaarlisten und getrennten
Familienergebnisse sind archiviert; keine Fehlfälle wurden entfernt.

## Die beiden bekannten Restpaare

Für `m8-r012` / `m8-r070` bleiben **alle** gepoolten Schnittordnungen gleich.
Beide Ordnungen sind zusammenhängend; die Beschränkung auf Zusammenhang löst
das Problem also ebenfalls nicht. R2 trennt dieses Paar weiterhin.

Für `closed-rook` / `closed-shrikhande` stimmen erste und zweite Ordnung überein;
die dritte unterscheidet sie. Unter den 560 unteren Dreiermengen ergeben sich:

| Gemeinsame Nachfolger | closed-rook | closed-shrikhande |
|---:|---:|---:|
| 0 | 96 | 160 |
| 1 | 432 | 272 |
| 2 | 0 | 96 |
| 3 | 0 | 32 |
| 4 | 32 | 0 |

Die obere Richtung liefert dieselben Werte. Dies ist die **erste trennende
Ordnung innerhalb der hier definierten reinen Schnittprofile**; es wird keine
globale Minimalität unter anderen Merkmalen behauptet.

## Zwei Aussagen mit Beweis statt einer immer längeren Merkmalsliste

Die [vollständigen Beweise](PROOFS.md) halten Voraussetzungen und Schlussfolgerungen getrennt:

1. **Rekonstruktion mit Zuordnung.** Für eine m×u-Inzidenzmatrix mit maximalem
   Spaltengrad d genügen die Werte g(S) für jede beschriftete Zeilenteilmenge
   S mit |S|≤d einschließlich g(∅)=u. Möbius-Inversion rekonstruiert die
   Spaltennachbarschaften samt Multiplizitäten. Zeilenlabels bleiben erhalten;
   Spalten können permutiert werden. Bei positiven Zweischichtenordnungen sind
   die Seiten intrinsisch erkennbar. Bei isolierten Elementen setzt der Satz
   eine angegebene Seitenzuordnung voraus.
2. **Grenze ohne Zuordnung.** Eine einzelne zyklische Zweischichtenordnung und
   die Vereinigung zweier solcher Zyklen haben für jedes m≥6 dieselben
   Schnitt-Histogramme sämtlicher Ordnungen. Eine besitzt eine, die andere zwei
   Zusammenhangskomponenten. Die Nichtisomorphie ist damit bewiesen. Die vier
   endlichen Kontrollpaare bestätigen die Zählformel; der allgemeine Beweis
   folgt aus der Konstruktion und nicht aus einer Extrapolation der Tests.

In den vier Zykluskontrollen trennen R2 und H7+N1+Q1 die jeweiligen Paare.
Diese Familie ist deshalb ausdrücklich nur ein Gegenbeispiel für Pall als
universellen Identifikator.

## Gegenprüfung und Kosten

Vor der Quellenfixierung wurden alle **512 binären 3×3-Matrizen** durch beide
Encoder und Decoder geprüft, einschließlich leerer Spalten und nicht scharfer
Gradschranken. Hinzu kamen die 64 vier-elementigen DAG-Abschlüsse und der
Kontrollfehler, der gemeinsame R2-Farbinformation durch getrennte Randhäufigkeiten ersetzt.

Auf dem vollständigen Zielkorpus stimmen Bitmengen-Schnittzahlen mit expliziten
Inzidenzsummen überein. Absteigende Subtraktion und alternierende Inklusion–Exklusion
liefern identische Spaltenmultiplizitäten. Explizite Spaltenbijektionen bestätigen
jeweils die vollständige rekonstruierte Matrix. Alle Teilmengenwerte transportieren
korrekt unter der Umkehrung der Zeilen- und Spaltenlabels; alle R2-Rundenspuren
stimmen zwischen den Kernen und unter vollständiger Knoten-Umbeschriftung überein.

Für die acht neuen Zyklusordnungen wurden **744 charakteristische Polynome je
Rechenweg** neu berechnet und verglichen. Die H7/N1/Q1-Werte der übrigen **209**
Eingaben wurden aus den durch Hashes gebundenen, bereits geprüften Artefakten
übernommen. Diese alten Polynome wurden in dieser Studie nicht erneut berechnet.

Acht Negativkontrollen verwerfen eine fehlende Teilmenge, falsche Gradschranke,
geänderte Schnittzahl, verlorene Spaltenmultiplizität, falsche Spaltenbijektion,
beschädigte R2-Spur, ausgelassene Eingabe und ausgelassenes Restpaar.
Die getrennten Implementierungen stammen aus demselben Bearbeitungsprozess;
sie ersetzen keine externe menschliche Prüfung.

Die beiden 32-Elemente-Ordnungen benötigen je Richtung **26.333 zugeordnete
Einträge** bei d=7, während ihre Inzidenzmatrix nur 256 binäre Einträge hat.
Das Dateiformat speichert je Teilmenge eine Maske und eine Schnittzahl. Insgesamt
sind es 326.184 Ganzzahlen für diese zugeordneten Daten beider Richtungen;
Pall benötigt 11.134 Ganzzahlen. Diese unterschiedlichen Einheiten und
Informationsgehalte dürfen nicht als gleichwertige Speicherkosten ausgegeben werden.
R2 hat zusätzlich 430.996 Ganzzahlen in der Rundenspur und benötigt den gemeinsamen
Farbkontext. Seine 6.732.112 Zwischenknotenbeiträge und die beschreibenden
Einzellaufzeiten stehen in den Kosten- und Zeitdateien; ein kontrollierter
Geschwindigkeitsbenchmark wird nicht behauptet.

## Reproduktion und Artefakte

```sh
python3 -B -O research/lorentz_relational_boundary/run.py --selftest
python3 -B -O research/lorentz_relational_boundary/run.py \
  --run /tmp/x6-boundary-fresh \
  --source-ref 99ecd6271b9664beadbb38117c641d5c3fcb779f
```

Das Ausgabeverzeichnis muss neu sein und der Quellcommit im Git-Verlauf vorliegen.
Pro Phase gelten 1.800 Sekunden und 2 GiB Adressraum. Fehler oder unvollständige
Läufe werden als `INCONCLUSIVE` erhalten. Der
[GitHub-Prüfweg](../../.github/workflows/lorentz-relational-boundary.yml)
wiederholt den vollständigen Lauf bei abgeschaltetem Netzwerk und vergleicht
alle deterministischen Dateien. Lokal wird keine OS-Netzisolierung behauptet.

- [inputs.json](results/inputs.json): sämtliche vollständigen Relationsmatrizen.
- [records.json.gz](results/records.json.gz), [indexed.json.gz](results/indexed.json.gz) und [reconstruction.json.gz](results/reconstruction.json.gz): alle Merkmale, zugeordneten Werte und vollständigen Rekonstruktionszeugen.
- [rounds.json.gz](results/rounds.json.gz), [reference.json.gz](results/reference.json.gz) und [summary.json.gz](results/summary.json.gz): alle Rundenspuren, Paarreferenzen und Restpaarlisten.
- [summary_counts.json](results/summary_counts.json), [controls.json](results/controls.json), [costs.json](results/costs.json), [verification.json](results/verification.json) und [timing.json](results/timing.json): direkt lesbare Zusammenfassungen und Prüfquittung.

Alle `.json.gz`-Dateien enthalten vollständiges gzip-komprimiertes UTF-8-JSON.
Die nächste offene Arbeit ist die explizite Behandlung der Knoten-Zuordnung und
eine begründete Erweiterung auf höhere Schichten. Der vorliegende Satz darf
nicht als Rekonstruktion beliebiger Kausalmengen ausgegeben werden. Keine
Neuheits-, Minimalitäts-, Physik- oder Kontinuumsbehauptung.


## Folgestudie nach diesem Stand

Die [Knoten-Zuordnungs- und Geometriestudie](../lorentz_matching_geometry/README.md) ergänzt explizite Isomorphiezeugen, ein Dreischicht-Gegenbeispiel und einen eingeschränkten gemeinsamen Rekonstruktionssatz. Der erste prospektive Geometriepilot weist für die dort getesteten P123-Merkmale keinen Zusatznutzen nach. Die oben archivierten Quellen und ursprünglichen Befunde bleiben unverändert.
