# Fester Familientransfer und gemeinsames Gegenbeispiel für H7, N1, Q1 und R2

Die beiden Strukturkontrollen liefern **zwei nichtisomorphe Ordnungen mit je
32 Elementen, die auch H7+N1+Q1+R2 gemeinsam nicht unterscheiden**. Ein exaktes
Vierer-Schnittzertifikat beweist ihre Nichtisomorphie. Das ist eine konkrete Grenze
der bisherigen Merkmalskombination, keine Aussage über ein kleinstes Gegenbeispiel.

In den separat ausgewiesenen 72 neuen Ziehungen trennen Q1 und R2 jeweils alle
539 nichtisomorphen größeninternen Ziehungspaare. Schon H7+N1+Q1 lässt dort kein
Paar offen: Diese Stichprobe belegt deshalb **keinen Zusatznutzen von R2 gegenüber
H7+N1+Q1**. Der Erfolg am früheren Restpaar bleibt gültig.

## Vorabfestlegung und Prüfstatus

Der [Vertrag](contract.json) wurde im Commit
[`eb54890`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/eb54890b02f6205b9ceff1a37d7f8d6a487ddf32)
um **2026-10-16 13:48:06 UTC** öffentlich festgelegt. Die
[Ausführungsquellen mit Hashes](freeze.json) folgten im Commit
[`b4f2eac`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/b4f2eaca554574c25a16ee84f8aeb1795a821ec3)
um **13:52:59 UTC**, vor der ersten Erzeugung der Zielmatrizen.
Zuvor liefen ausschließlich Tests an Ordnungen mit höchstens vier Elementen.

H7, N1, Q1 sowie beide R2-Kerne wurden unverändert aus den vorherigen Studien
importiert. Es gab keine nachträgliche Änderung der eingefrorenen Quellen,
kein Nachziehen von Eingaben und keine Entfernung von Duplikaten oder Fehlschlägen.
Die [Laufquittung](results/RESULTS.json) enthält die tatsächlichen Zeitpunkte,
Quellenbindung, Plattform und SHA-256-Hashes; [publication.json](publication.json)
ordnet die öffentliche Chronologie ein.

**Die Evidenzarten bleiben getrennt:** Die Zufallsfamilien sind neue Ziehungen
aus vorab festgelegten deterministischen Generatoren. Sie sind keine gleichverteilte
Stichprobe aller Ordnungen; neu gezogene Ordnungen können zu früheren Ordnungen
isomorph sein. Die bekannten Rook-/Shrikhande-Ausgangsgraphen wurden gezielt aus
der Theorie gewählt. Ihre Strukturkontrollen sind keine blinde Entdeckung und
werden nicht als unabhängige Zufallsstichprobe ausgegeben.

## Vollständiger fester Korpus

| Familie | Größen n | Eingaben | Isomorphieklassen innerhalb des neuen Korpus | Tatsächliche Höhen |
|---|---|---:|---:|---|
| Kubisch reguläre Zweischichtenordnungen | 16, 22 | 24 | 23 | 24 × Höhe 2 |
| Bernoulli-Kanten zwischen zwei Schichten | 8, 12 | 24 | 24 | 24 × Höhe 2 |
| Kanten zwischen drei Schichten, transitiv abgeschlossen | 9, 12 | 24 | 24 | 23 × Höhe 3; 1 × Höhe 1 |
| Geschlossene Nachbarschaften der beiden Strukturkontrollen | 32 | 2 | 2 | 2 × Höhe 2 |

Alle 74 beschrifteten Eingaben bleiben erhalten. `reg-m8-d00` und `reg-m8-d04`
sind isomorph; damit ergeben sich 73 Isomorphieklassen insgesamt. Die degenerierte
Dreischichten-Ziehung und sämtliche isolierten Elemente wurden ebenfalls behalten.
Die beiden nichtregulär angelegten Generatorfamilien enthalten 23 beziehungsweise
35 isolierte Elemente, verteilt auf zehn beziehungsweise 13 Eingaben.

## Paarvergleich ohne Vermischung von Duplikaten und Fehlern

Die Tabelle zählt **nichtisomorphe Ziehungspaare**, keine unabhängigen
Zufallsexperimente. Bei n=12 sind auch die 144 familienübergreifenden Paare enthalten.
Das isomorphe Duplikatpaar bei n=16 zählt nicht als Merkmalsfehler.

| n | Eingaben | Alle Paare | Nichtisomorphe Paare | H7 offen | N1 offen | Q1 offen | R2 offen | H7+N1+Q1+R2 offen |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 12 | 66 | 66 | 0 | 0 | 0 | 0 | 0 |
| 9 | 12 | 66 | 66 | 0 | 0 | 0 | 0 | 0 |
| 12 | 24 | 276 | 276 | 0 | 0 | 0 | 0 | 0 |
| 16 | 12 | 66 | 65 | 1 | 65 | 0 | 0 | 0 |
| 22 | 12 | 66 | 66 | 0 | 66 | 0 | 0 | 0 |
| 32, Strukturkontrollen | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Das neue H7+N1-Kollisionspaar `reg-m8-d02` / `reg-m8-d05` wird sowohl durch
Q1 als auch durch R2 getrennt. Bei den 72 Stichprobeneingaben ist das
vorab definierte Zusatznutzen-Kriterium für R2 gegenüber H7+N1+Q1
`NO_OPPORTUNITY`. Bei den Strukturkontrollen lautet es
`NO_ADDITIONAL_SEPARATION`. Es gibt hier keine zusätzliche R2-Trennung dieser
stärkeren Ausgangskombination. Alle acht verglichenen Kombinationen und sämtliche
Restpaare stehen in [summary.json](results/summary.json).

## Warum die Strukturkontrollen ein Gegenbeispiel sind

Für jeden der beiden 16-Knoten-Graphen sei A seine Adjazenzmatrix und B=I+A.
Die strikte Ordnung hat die Relation C=[[0,B],[0,0]]. Sie hat 16 untere und
16 obere Elemente, jeweils sieben Nachfolger beziehungsweise Vorgänger.
Die gewöhnlichen bipartiten Doppelgraphen mit B=A wären als Gegenbeispiel
ungeeignet: Sie sind isomorph. Das wurde bereits bei der Auswahl berücksichtigt.

Unter allen 1.820 Vierermengen der unteren Schicht haben bei `closed-rook`
genau **acht** Mengen vier gemeinsame Nachfolger. Bei `closed-shrikhande`
hat **keine** Vierermenge mehr als zwei gemeinsame Nachfolger. Eine gerichtete
Isomorphie müsste diese Häufigkeiten erhalten; sie existiert daher nicht.
Die obere Schicht liefert dasselbe Zertifikat. Beide Ordnungen sind jeweils
selbstdual, sodass auch Zeitumkehr die Nichtisomorphie nicht beseitigt.

R2 besitzt bei beiden Kontrollen die gemeinsamen globalen Farbanzahlen
**8 → 10 → 12 → 12**; die Histogramme stimmen in jeder Runde überein.
Die letzte Runde bestätigt die stabile Partition. Der
[vollständige Gegenbeispielnachweis](COUNTEREXAMPLE.md) enthält die beiden
Inzidenzmatrizen, das endliche Zertifikat und eine nachträgliche algebraische
Erklärung der allrundigen R2-Gleichheit. Das Vierer-Zertifikat war als
Referenzprüfung vorab festgelegt; es ist kein nachträglich hinzugefügter Kandidat
in der Vergleichstabelle.

## Gegenprüfung und Aufwand

Die getrennte Prüfung rekonstruiert alle Eingaben durch Kantenmengen und
Erreichbarkeitssuche, statt durch die Matrixoperationen des Produzenten.
Sie bestätigt alle **541** Isomorphieentscheidungen und **6.294**
charakteristischen Polynome je Rechenweg. Faddeev–LeVerrier mit
Cayley–Hamilton-Restprüfung wird durch Bareiss-Determinanten und exakte
Interpolation gegengeprüft. Die zwei R2-Kerne stimmen in jeder Farbmatrix
jeder Runde überein; die Umkehrung sämtlicher Knotenlabels transportiert
alle Rundenspuren korrekt.

Sechs absichtliche Fehler werden zurückgewiesen: Selbstschleife, ausgelassene
Eingabe, veränderter Q1-Koeffizient, falsche R2-Multiplizität, beschädigte
Rundenspur und ausgelassenes Referenzpaar. Diese getrennten Codepfade stammen
aus demselben Bearbeitungsprozess; sie ersetzen keine externe menschliche Prüfung.
Der eingefrorene Multiplizitätstest addiert eins. Eine gesondert gekennzeichnete
nachträgliche Prüfung entfernt zusätzlich ein Vorkommen und ein Restpaar;
[explanation.json](results/explanation.json) dokumentiert diese Ergänzung und
die algebraische Erklärung, ohne die eingefrorenen Quellen zu verändern.

| Methode | Charakteristische Polynome | Ganzzahlen im Merkmalswert |
|---|---:|---:|
| H7 | 222 | 3.628 |
| N1 | 0 | 8.912 |
| Q1 | 6.072 | 108.888 |
| R2 | 0 | 21.438 |

R2 benötigt zusätzlich die gemeinsame Farbbedeutung und hier **78.212**
Ganzzahlen in der vollständigen Rundenspur. Die Histogramme sind deshalb keine
eigenständig vergleichbaren, portablen Fingerabdrücke. Es wurden 1.192.440
Zwischenknotenbeiträge ausgewertet. Die Stabilisierung erfolgt für n=8,9,12,16,22,32
nach 3,2,3,4,5,3 Runden, jeweils einschließlich der letzten Runde ohne Aufspaltung.
[timing.json](results/timing.json) enthält deskriptive Einzelmessungen,
keinen kontrollierten Geschwindigkeitsbenchmark.

## Reproduktion und Dateien

```sh
python3 -B -O research/lorentz_relational_transfer/run.py --selftest
python3 -B -O research/lorentz_relational_transfer/run.py \
  --run /tmp/x6-transfer-fresh \
  --source-ref b4f2eaca554574c25a16ee84f8aeb1795a821ec3
```

Das Ausgabeverzeichnis muss neu sein; der Quellcommit muss im Git-Verlauf
vorliegen. Pro Phase gelten 1.800 Sekunden und 2 GiB Adressraum. Eine unvollständige
Berechnung wird als `INCONCLUSIVE` erhalten. Die
[GitHub-Prüfung](../../.github/workflows/lorentz-relational-transfer.yml)
wiederholt den vollständigen Lauf mit abgeschaltetem Netzwerk und vergleicht
alle deterministischen Ausgabedateien. Laufzeiten und Zeitstempel werden nicht
auf Bytegleichheit geprüft. Lokal wird keine Betriebssystem-Netzisolierung behauptet.

- [inputs.json](results/inputs.json): alle vollständigen Relationen und Erzeugungsmetadaten.
- [records.jsonl.gz](results/records.jsonl.gz): sämtliche exakten Merkmalswerte und Strukturstatistiken; gzip-komprimiertes UTF-8-JSONL.
- [rounds.json.gz](results/rounds.json.gz): jede R2-Farbmatrix jeder Runde; gzip-komprimiertes UTF-8-JSON.
- [reference.json](results/reference.json): vollständige Isomorphieentscheidungen.
- [certificate.json](results/certificate.json), [verification.json](results/verification.json) und [costs.json](results/costs.json): Zertifikat, Gegenprüfung und logische Kosten.

Die nächste offene Frage ist eine **begründet eingeschränkte** Rekonstruktion
oder ein neuer, getrennt festzulegender Vergleich stärkerer relationaler Merkmale.
Das vorhandene Vierer-Zertifikat darf nicht ohne neue Prüfung zur universellen
Lösung erklärt werden. Vollständige Relationen und exakte Isomorphie bleiben
verbindlich. Keine Neuheits-, Minimalitäts-, Physik- oder Kontinuumsbehauptung.

Quellen zur Einordnung: A. E. Brouwer,
[Shrikhande graph](https://aeb.win.tue.nl/graphs/Shrikhande.html), insbesondere
die gleiche bipartite Verdopplung; Fuhlbrück, Köbler, Ponomarenko und Verbitsky,
[The Weisfeiler–Leman Algorithm and Recognition of Graph Properties](https://arxiv.org/abs/2005.08887).
Die endlichen Ergebnisse oben stammen aus den archivierten Berechnungen.
