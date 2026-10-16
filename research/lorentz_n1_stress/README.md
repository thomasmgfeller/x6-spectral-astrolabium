# Belastungstest: gleiche N1-Profile, zusätzlicher Nutzen und Grenze von Q1

**16. Oktober 2026 · vollständig berechnet und exakt gegengeprüft.**
Das unveränderte Q1 trennt **24 von 25 nichtisomorphen Paaren**, die unter
N1 **und** H7 gleich sind. **1 Paar bleibt auch unter H7+N1+Q1 gleich.**
Das liefert konkrete endliche Evidenz für zusätzlichen Informationsgehalt von Q1
und zugleich ein Gegenbeispiel gegen eine universelle Identifikationsgarantie dieses
Merkmalspakets. Vollständige Relationsmatrizen und exakte gerichtete Isomorphie
bleiben die Referenz.

## Status und ausdrücklich dokumentierte Abweichung

Rechenstatus: `PASS_EXACT_STRESS_TEST_WITH_PRE_RUN_DEVIATION`. Der öffentliche Upload des neuen Prüfvertrags wurde
durch die automatische Freigabeprüfung blockiert. Vertrag und Quellcode wurden
vor der ersten Zielerzeugung lokal versioniert und gehasht; **eine öffentliche
Vorregistrierung liegt nicht vor**. Diese vor dem Lauf dokumentierte Abweichung
steht in [PRE_RUN_DEVIATION.json](PRE_RUN_DEVIATION.json). Familie, Ziehungen,
Merkmale, Endpunkte und Ressourcenlimits wurden danach nicht geändert.

Die lokale Git-Zeitfolge ist nachvollziehbar, aber kein unabhängiger Zeitstempel.
Auch eine spätere Veröffentlichung macht daraus keine rückwirkende öffentliche
Vorregistrierung. Die Erstfassung war noch nicht veröffentlicht; die anschließend
erteilte Freigabe und der Publikationsweg sind in [PUBLICATION.md](PUBLICATION.md)
dokumentiert. Die ursprünglichen lokalen Commits bleiben im beigefügten
[Git-Bundle](local-history.bundle) bytegenau erhalten.

- Grundlage: `faeb2e003ff91cd3cc90b18db9617d725bebcb2f` (integrierter Vergleich, PR 35).
- Vertragscommit: `9da649b`.
- Quellfreeze: `4680e959a40d4e8fa9ff2193eaf8c10f2d85299d`.
- Ziellauf: 2026-10-16T12:29:24.871573+00:00 bis 2026-10-16T12:38:23.493650+00:00.
- Vor dem Freeze ausschließlich Spielzeugprüfungen mit höchstens sechs Elementen.

## Fragestellung und feste Familie

Die vorab lokal festgelegte Hauptfrage lautet: Unterscheidet Q1 mindestens ein
nichtisomorphes Paar, für das sowohl N1 als auch H7 übereinstimmen? Nur ein Unterschied
gegenüber N1 allein würde einen bereits von H7 erkannten Unterschied mitzählen.

Für jede Ordnung gilt

$$C=\begin{pmatrix}0&B\\0&0\end{pmatrix},\qquad B\in\{0,1\}^{m\times m},\qquad
\sum_jB_{ij}=\sum_iB_{ij}=3.$$

C ist die vollständige strikte Relation. Sie ist irreflexiv und transitiv, da es
keine Pfade mit zwei Relationen gibt. Untere Elemente haben das Gradpaar (0,3),
obere (3,0). Jedes untere Element hat drei Nachfolger mit Gradpaar (3,0), jedes
obere drei Vorgänger mit Gradpaar (0,3). **Das gesamte registrierte N1-Profil hängt
damit nur von m ab.** Gemeint ist genau die veröffentlichte N1-Definition, keine
unbeschränkte Gleichheit beliebig großer Nachbarschaften.

352 feste Erzeugungen bei m=6,7,8,9,10 beginnen jeweils mit derselben zirkulanten
Matrix und führen 20m² deterministisch gehashte Vorschläge für graderhaltende
Kantentausche aus. Alle Ziehungen, auch Wiederholungen und gegebenenfalls nicht
zusammenhängende Ordnungen, bleiben erhalten. Die erste Repräsentantin jeder
gerichteten Isomorphieklasse wird ausgewertet; keine Quotientierung durch Zeitumkehr.

Dies ist eine gezielte endliche Belastungsfamilie. Es wird weder uniforme Verteilung
noch ausreichende Mischung des Tauschverfahrens behauptet. Die Paare sind abhängig;
die Zahlen sind keine Erfolgswahrscheinlichkeiten und erhalten keine p-Werte.

## Vollständiges Hauptergebnis

| Elemente n | Erzeugungen | Verschiedene Ordnungen | N1-gleiche Paare | Auch H7 gleich | Davon Q1 getrennt | Weiterhin gleich |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 32 | 6 | 15 | 1 | 1 | 0 |
| 14 | 32 | 11 | 55 | 1 | 1 | 0 |
| 16 | 96 | 32 | 496 | 5 | 4 | 1 |
| 18 | 96 | 68 | 2278 | 15 | 15 | 0 |
| 20 | 96 | 90 | 4005 | 3 | 3 | 0 |
| **Gesamt** | **352** | **207** | **6849** | **25** | **24** | **1** |

Die Paarzahlen vergleichen nur Ordnungen derselben Größe. Q1 allein trennt
6848 der 6849 N1-gleichen Paare in diesem Korpus. Der wissenschaftlich
stärkere Hauptbefund sind die 24 zusätzlichen Trennungen unter den 25
auch H7-gleichen Paaren. Alle Partitionen und Restklassen stehen vollständig in
[summary.json](results/summary.json), sämtliche Werte und Relationen in
[records.jsonl](results/records.jsonl), sämtliche Erzeugungen mit Zuordnung in
[draws.json](results/draws.json).

## Nachträgliche Diagnose: Zeitumkehr

Diese Diagnose wurde ausdrücklich **nach Einsicht in erste Teilergebnisse**
angelegt. Sie ändert keine Auswahl, kein Merkmal und keinen primären Endpunkt.
Jedes H7-Kollisionspaar wurde auf Isomorphie zur Zeitumkehr geprüft, mit zwei
verschiedenen exakten Algorithmen. Vollständige Ergebnisse:
[interpretation.json](interpretation.json), Reproduktion: `interpret.py`.

| Art des Paars | Q1 trennt | Q1 trennt nicht |
|---|---:|---:|
| Zur Zeitumkehr isomorph | 17 | 0 |
| Auch nach Zeitumkehr nicht isomorph | 7 | 1 |

Zeitumkehr ist im Vertrag keine Äquivalenz. Ihre Unterscheidung zählt deshalb als
zulässiger Informationsgewinn. Die zusätzliche Tabelle verhindert, dass bloße
Orientierungsunterschiede mit einer stärkeren Aussage über ungerichtete Strukturen
verwechselt werden.

## Konkretes positives Prüfzeugnis

Das erste positive Paar im festgelegten Korpus ist `m6-r001` /
`m6-r004` mit n=12. N1 und H7 stimmen exakt überein, Q1
unterscheidet; die vollen Relationen sind nicht gerichtet isomorph. Die folgenden
Zeilen sind die B-Blöcke. C wird mit der oben angegebenen Blockform eindeutig
rekonstruiert; es handelt sich um binäre Relationsdaten, nicht um Näherungswerte.

**m6-r001**

```text
011010
100101
011100
100011
000111
111000
```

**m6-r004**

```text
111000
010011
001110
101100
100101
010011
```

Ein exakter Unterschied liegt im sortierten Q1-Deck an Position
0 (Nullzählung), Richtung `future`,
Operator `S`. Die vollständigen Koeffizienten beider
charakteristischer Polynome stehen in `interpretation.json`. Sortierte
Deckpositionen behaupten keine Zuordnung der ursprünglichen Wurzeln.

## Konkretes negatives Prüfzeugnis

`m8-r012` / `m8-r070` mit n=16 ist ein
**nichtisomorphes Paar mit exakt gleichem H7, N1 und Q1**. Dieses Paar darf weder
weggefiltert noch als identischer Zustand zusammengefasst werden.

**m8-r012**

```text
01100010
11010000
00001110
10100001
00011100
11000010
00101001
00010101
```

**m8-r070**

```text
11100000
01011000
01001001
00000111
10000011
00010110
00110100
10101000
```

Die vollständigen Q1-Multimengen einschließlich Vielfachheiten und gepaarter
Vergangenheits-/Zukunftswerte sind gleich, nicht nur gerundete Eigenwerte.
Das Paar widerlegt universelle Eindeutigkeit des exakt hier definierten Pakets.
Es widerlegt weder alle möglichen Erweiterungsmerkmale noch das Forschungsprogramm.
Eine globale Minimalität der Größe dieses Gegenbeispiels wurde nicht untersucht.

## Exakte Gegenprüfung und Kosten

- 352 Erzeugungen unabhängig nachgerechnet; alle Grad-, Relations- und N1-Bedingungen geprüft.
- 207 Repräsentanten mit vollständigen Merkmalswerten geprüft.
- 23193 charakteristische Polynome durch einen zweiten exakten Rechenweg bestätigt.
- Alle 25 H7-gleichen Repräsentantenpaare exakt als nichtisomorph bestätigt.
- Jede Erzeugung ihrer Repräsentantin durch exakte Isomorphie zugeordnet; erste Repräsentanten und vollständige Abdeckung geprüft.
- Umbenennungstransport für alle Eingaben und alle gewurzelten Erweiterungen geprüft.
- 10 Fehlerkontrollen abgewiesen; vollständige Liste in [verification.json](results/verification.json).

Der Produzent nutzt ganzzahlige Faddeev-LeVerrier-Rekursion mit
Cayley-Hamilton-Restprüfung und direkte Erweiterungsmatrizen. Der Checker nutzt
Bareiss-Determinanten mit exakter Interpolation sowie Kanteneinfügung mit
transitivem Abschluss. Identitätsprüfung: adaptive vollständige Relationsbijektionen
gegen getrennte Zeilenbijektionen mit exaktem Vergleich der Spaltenmuster.
Schnittzahlen sind dort nur notwendige Vorfilter, keine Identitätszertifikate.

| Merkmal | Logische Polynomaufrufe im Korpus | Ganzzahlwerte im gespeicherten Merkmal |
|---|---:|---:|
| H7 | 621 | 12942 |
| N1 | 0 | 30096 |
| Q1 | 22572 | 460608 |

Zusätzlich zur H7-Basis benötigt Q1 genau 6n Polynome je Repräsentantin, N1 keine.
Produzentenphase: 233.69 s; Gegenprüfung: 304.93 s.
Diese einmaligen Laufzeiten stammen aus einer nicht optimierten seriellen Umgebung
und begründen keine allgemeine Effizienzbehauptung. Python 3.12.14;
Laufzeit- und Umgebungsdaten in [RESULTS.json](results/RESULTS.json).

Beide Algorithmen stammen aus demselben Arbeitsprozess. Dies ist eine getrennte
algorithmische Gegenprüfung, keine externe fachliche Begutachtung. Kein Zugriff
auf Netzquellen erfolgt im Rechenkern. Eine erzwungene Netzisolation per `unshare`
war lokal nicht verfügbar; die vorbereitete CI fordert sie separat an. Ein
GitHub-CI-Lauf wird hier nicht als ausgeführt behauptet.

## Reproduktion

Voraussetzung: Python-Standardbibliothek und vollständiger Git-Checkout mit dem
angegebenen Basiscommit. Die historischen lokalen Commits werden zunächst aus dem
archivierten Git-Bundle geladen; diese Wiederherstellung verändert keinen Branch
und keine Arbeitsdatei. Das Zielverzeichnis für den Rechenlauf muss neu sein.

```sh
git bundle verify research/lorentz_n1_stress/local-history.bundle
git fetch research/lorentz_n1_stress/local-history.bundle refs/heads/research/n1-stress:refs/archive/n1-stress-local
python3 -B -O research/lorentz_n1_stress/run.py --selftest
python3 -B -O research/lorentz_n1_stress/run.py --run /tmp/n1-stress-fresh
cmp research/lorentz_n1_stress/results/records.jsonl /tmp/n1-stress-fresh/records.jsonl
cmp research/lorentz_n1_stress/results/summary.json /tmp/n1-stress-fresh/summary.json
cmp research/lorentz_n1_stress/results/verification.json /tmp/n1-stress-fresh/verification.json
python3 -B -O research/lorentz_n1_stress/interpret.py
```

Je Phase gelten 1800 Sekunden und 2 GiB. Unvollständigkeit, Zeitüberschreitung oder
Prüffehler führen zu `INCONCLUSIVE`. Der erste Lauf ist komplett mit Prüfsummen
archiviert; ein zusätzlicher vollständiger Wiederholungslauf ist lokal nicht
beansprucht. Die CI führt bei der Veröffentlichung einen frischen vollständigen
Lauf aus; ihr aktueller Status ist separat auf GitHub zu prüfen.

## Konsequenz

N1 bleibt ein kostengünstiger Vorfilter. Q1 besitzt in dieser festgelegten Familie
zusätzlichen Informationsgehalt und kann als weitere Filterstufe geprüft werden.
Der Test begründet keine allgemeine Kosten-Nutzen-Empfehlung für reale Anwendungen.
Bei gleichen Fingerprints bleibt die vollständige gerichtete Isomorphieprüfung
verbindlich. Der nächste Forschungsauftrag kann gezielt das archivierte Restpaar
untersuchen; weitere Merkmale brauchen einen neuen, getrennt festgelegten Vertrag.

Keine vierdimensionale Rekonstruktion, Kontinuumsgrenze, physikalische Kausalität,
Quantendynamik oder neue Physik wird aus diesem endlichen Kombinatoriktest abgeleitet.

## Literaturkontext

Y. K. Yazdi, M. Letizia und A. Kempf, *Lorentzian Spectral Geometry with Causal Sets*,
Classical and Quantum Gravity 38 (2021) 015011,
[arXiv:2008.02291](https://arxiv.org/abs/2008.02291),
[DOI:10.1088/1361-6382/abc3f8](https://doi.org/10.1088/1361-6382/abc3f8).
Einpunkt-Erweiterungen sind ein publizierter Ansatz. Unsere festen S/A/K-Decks,
gerichtete Paarung und Belastungsfamilie sind keine identische Replikation dieser
Arbeit und beanspruchen keine Neuheit. Die hier berichteten Zahlen stammen aus
den eigenen vollständig beigefügten Rechenartefakten.
