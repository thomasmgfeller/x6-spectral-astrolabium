# Vergleich zusätzlicher Ordnungsmerkmale: N1 und Q1

**16. Oktober 2026 · PASS_FINITE_COMPARISON.** Der vorab festgelegte Vergleich
spricht im untersuchten Bereich für **H7+N1 als kostengünstigen Vorfilter**.
H7+N1 und H7+Q1 trennen alle sechs bekannten Kontrollpaare. N1 erfordert keine
zusätzlichen charakteristischen Polynome; Q1 erforderte hier 106.470.
Gleiche Fingerprints dürfen weiterhin **keine Identität begründen**: Vollständige
Relationen und eine exakte Isomorphieprüfung bleiben die Entscheidungsgrundlage.

**Grenze der neuen Stichprobe:** Unter den 120 unterschiedlichen Stichprobenordnungen
bei n=8/9 tritt schon für H7 keine Kollision auf. Dieser Teil belegt daher keine
zusätzliche Trennwirkung von N1 oder Q1. Die Trennleistungsentscheidung beruht auf
dem bekannten vollständigen kleinen Korpus und den vorab benannten Gegenbeispielen.
Eine allgemeine Überlegenheit oder Rekonstruktionsgarantie folgt daraus nicht.

## Vorabfestlegung und Wissensstand

- [Prüfvertrag vor dem Vergleich](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/6e3c44f91f106e59bd2407acffc9e55b428f5784).
- [Gehashtes Programm vor dem ersten Ziellauf](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f34c2266eae4d4edc6a0b016be877f3de5cebea7).
- Erster Ziellauf: 2026-10-16 12:05:09 bis 12:07:21 UTC. Keine Änderung des
  eingefrorenen Vertrags oder Rechenkerns nach dem Lauf; keine Protokollabweichung.
- Vor der Programmveröffentlichung wurden nur vier Spielzeugfälle mit n≤3 und
  Fehlerkontrollen ausgeführt, nicht der Zielkorpus oder die Stichprobe.

Dies ist eine nachvollziehbare Vorabfestlegung innerhalb des Repositorys, keine
externe Vorregistrierung und kein Blindtest. H7s Scheitern, die Trennung des
n≤7-Korpus durch H7+D und die sechs Kontrollpaare waren bekannt. Dass H7+N1 den
n≤7-Korpus trennt, folgt bereits aus seiner enthaltenen Gradinformation. Der
[Vertrag](contract.json) legt dieses Vorwissen ausdrücklich offen.

Einpunkt-Erweiterungen sind zudem ein bereits publizierter Ansatz der
Kausalset-Spektralgeometrie [1]. Unsere beidseitige, wurzelweise gepaarte S/A/K-
Auswertung ist ein hier festgelegter Vergleichsvertrag; sie ist keine identische
Replikation der dortigen Tabelle 4 und beansprucht keine Neuheit.

## Festgelegte Merkmale

C bezeichnet stets die volle strikte transitive Relation. Ausgewertet werden
H7 allein und die vier Ergänzungen **H7+D, H7+M11, H7+N1, H7+Q1**. Zusätzlich
werden D, M11, N1 und Q1 jeweils allein ausgewiesen. Die Richtung bleibt erhalten;
Zeitumkehr ist keine vereinbarte Äquivalenz.

| Merkmal | Festgelegter Inhalt |
|---|---|
| D | Sortierte Multimenge der vollständigen Vorgänger-/Nachfolgerzahlen je Element. |
| M11 | Zahl gemeinsamer Nachfolger von Paaren minimaler Elemente, die jeweils genau einen Nachfolger haben. |
| N1 | Pro Element: sein Gradpaar, die Multimenge der Gradpaare aller Vorgänger und diejenige aller Nachfolger. Diese Tripel werden als Multimenge sortiert. Genau eine Runde. |
| Q1 | Pro Element: ein neues Element unmittelbar in dessen Zukunft beziehungsweise Vergangenheit anfügen, transitiv abschließen, jeweils die drei charakteristischen Polynome von S, A und K bestimmen. Zukunft/Vergangenheit bleiben pro Wurzel gepaart; alle Wurzelpaare werden als Multimenge sortiert. |

Formal ist mit $d(v)=(d^-(v),d^+(v))$

$$
N_1(C)=\operatorname{multiset}_{v}\left(d(v),
 \operatorname{multiset}_{u\prec v}d(u),
 \operatorname{multiset}_{v\prec w}d(w)\right).
$$

Für $b_v=e_v+C_{:v}$ und $a_v=e_v+C^T_{:v}$ sind die zwei Erweiterungen

$$
 C_v^+=\begin{pmatrix}C&b_v\\0&0\end{pmatrix},\qquad
 C_v^-=\begin{pmatrix}C&0\\a_v^T&0\end{pmatrix}.
$$

Die ursprüngliche Ordnung bleibt auf ihren n Elementen unverändert. Die neue
Relation ist jeweils der transitive Abschluss genau einer zusätzlichen Kante.
Die Gegenprüfung konstruiert diesen Abschluss unabhängig durch Kanteneinfügung
und Erreichbarkeit. Wurzeln mit gleichen Daten werden mit ihrer **Vielfachheit**
behalten; die beiden Richtungen dürfen nicht getrennt oder ungeordnet vermischt
werden. Diese Erweiterungen sind mathematische Sonden, keine physikalischen
Eingriffe oder zusätzliche Messungen an einem Gerät.

Beide Verfahren sind invariant unter Umbenennungen: Eine Permutation transportiert
Gradpaare und Vorgänger-/Nachfolgermengen bijektiv. Sie transportiert auch jede
wurzelbezogene Erweiterung auf die entsprechende Erweiterung der umbenannten
Ordnung, wobei das neue Element festgehalten wird. Ähnliche Matrizen haben gleiche
charakteristische Polynome; die äußere Multimenge entfernt die Wurzelnamen.
Der Checker prüft diesen Transport zusätzlich für jede Eingabematrix an einer
festen Umbenennung. Die allgemeine Invarianz folgt aus dem Argument, nicht allein
aus dieser einzelnen getesteten Permutation.

## Korpus und Stichprobe

| Teil | Umfang | Aussagebereich |
|---|---:|---|
| Vollständiger bestehender Korpus | 2.450 nichtisomorphe Ordnungen, n=1…7 | Vollständigkeit stammt aus der bereits exakt gegengeprüften Vorgängerstudie. |
| Bekannte Kontrollen | 12 Datensätze, sechs Paare | Beide n=7-Paare, das n=8-Gradpaar sowie drei verbundene Präfixpaare bei n=8,9,12. |
| Festgelegte neue Ziehungen | 128 | Je 16 pro Kombination aus n∈{8,9} und Kantenwahrscheinlichkeit 1/8, 2/8, 4/8, 6/8. |
| Unterschiedliche Stichprobenordnungen | 59 bei n=8; 61 bei n=9 | 120 Repräsentanten nach exakter gerichteter Isomorphieprüfung. |

Die Ziehungen verwenden die im Vertrag definierte SHA-256-Regel für obere
DAG-Kanten und danach den transitiven Abschluss. Der erste Repräsentant jeder
Isomorphieklasse bleibt erhalten. Die [vollständige Ziehungszuordnung](results/draws.json)
enthält auch die acht nicht zusätzlich aufgenommenen isomorphen Wiederholungen.
**Die Verteilung ist nicht gleichverteilt über Ordnungen.** Es gibt keine
Populationsschätzung, Signifikanzbehauptung oder vollständige n=8/9-Enumeration.

Vier Kontrollmatrizen erscheinen bereits im kleinen Korpus. Die drei Präfixpaare
sind verwandt. Die insgesamt 2.582 bearbeiteten Datensätze sind deshalb keine
2.582 global verschiedenen oder statistisch unabhängigen Beobachtungen.

## Trennleistung

| Methode | Klassen bei n=7 / 2.045 | Ungelöste Paare bei n=7 | Bekannte Kontrollpaare getrennt / 6 | Ungelöste Stichprobenpaare |
|---|---:|---:|---:|---:|
| H7 | 2.043 | 2 | 0 | 0 |
| H7+D | 2.045 | 0 | 5 | 0 |
| H7+M11 | 2.043 | 2 | 1 | 0 |
| H7+N1 | 2.045 | 0 | 6 | 0 |
| H7+Q1 | 2.045 | 0 | 6 | 0 |

Für n≤6 sind bereits alle H7-Klassen Einzelklassen. H7+D scheitert weiterhin am
bekannten n=8-Gradpaar. M11 trennt dieses Paar, lässt aber die anderen fünf
Kontrollpaare ungelöst. N1 und Q1 trennen sämtliche hier geprüften Kontrollpaare.

Als sekundärer Befund sind **N1 allein und Q1 allein im vollständigen n≤7-Korpus
injektiv auf Isomorphieklassen**. D allein besitzt dagegen sieben ungelöste Paare
bei n=6 und 189 bei n=7. Das ist keine Fortsetzung der ursprünglichen H7-Hypothese
und keine allgemeine Aussage über größere Ordnungen.

[summary.json](results/summary.json) enthält für jede Methode, Größe und jeden
Teilbestand Klassenanzahl, größte Klasse, alle Restgruppen und die Anzahl
ungelöster nichtisomorpher Paare. Alle Merkmalswerte und vollständigen Matrizen
stehen in [records.jsonl](results/records.jsonl). Gruppen werden durch die vollen
exakten Werte verglichen; Hashes dienen der Dateibindung, nicht der Isomorphie.

## Aufwand und vorab festgelegte Entscheidung

Die Ergänzungen werden in dieser Referenzimplementierung für jeden Datensatz
berechnet, ohne Zwischenabbruch oder globalen Spektrencache. Angaben sind
**zusätzlich zu H7**, über alle drei Teilbestände; Kontrollwiederholungen werden
entsprechend erneut gerechnet.

| Ergänzung | Zusätzliche charakteristische Polynome | Gespeicherte Ganzzahlen im Zusatzmerkmal | Endliches Entscheidungskriterium erfüllt |
|---|---:|---:|---|
| D | 0 | 35.490 | Nein: Kontrollpaar bleibt ungelöst |
| M11 | 0 | 2.582 | Nein: bekannte Kollisionen bleiben |
| N1 | 0 | 148.242 | Ja |
| Q1 | 106.470 | 951.882 | Ja |

Q1 berechnet 6n Polynome an Matrizen der Größe n+1. Der N1-Datensatz enthält
2n+4E Ganzzahlen, wenn E die Zahl voller strikter Relationen ist. Die Tabelle
zählt Ganzzahlen, nicht Bytes oder Prozessoroperationen; große Koeffizienten
benötigen unterschiedlich viele Bits. Auch Verfahren mit null Polynomen haben
Rechenkosten. Die lexikographische Auswahl nach Polynomaufrufen und dann
Ganzzahlanzahl ist eine **vorab definierte Auswahlregel**, kein Beweis allgemeiner
Laufzeitoptimalität.

Unter genau dieser Regel liegt **H7+N1 vor H7+Q1**. Im vorhandenen Korpus wurde
kein zusätzlicher Trenngewinn von Q1 gegenüber N1 beobachtet. Die Stichprobe
enthält aber auch keine H7-Kollision und kann die Gleichwertigkeit bei schweren
unbekannten Fällen nicht prüfen.

Die einmal gemessenen Zusatz-Kernelzeiten lagen bei rund 0,034 s für N1 und
41,48 s für Q1; alle Details stehen in [timing.json](results/timing.json).
Das sind unoptimierte Python-Beobachtungen einer einzelnen Umgebung, keine
wiederholte Leistungsstudie und kein übertragbares Geschwindigkeitsversprechen.
Der gesamte Produzentenprozess dauerte etwa 44,55 s, die Gegenprüfung 87,88 s.

## Prüfung und Reproduktion

Der Produzent nutzt Faddeev–LeVerrier mit Cayley–Hamilton-Restprüfung. Der
getrennte Checker importiert keinen Produzentencode und nutzt Bareiss-
Determinanten sowie rationale Interpolation. Er berechnet die erweiterten
Matrizen, Motive, Profile, Partitionen und Auswahlentscheidung erneut. Jede
Stichprobenziehung und jede Entfernung eines isomorphen Duplikats wird überprüft.
Die bereits bewiesene Vollständigkeit des n≤7-Korpus wird quellengebunden
übernommen, nicht in dieser Studie nochmals enumeriert.

[verification.json](results/verification.json) dokumentiert:

- 2.582 vollständig überprüfte Datensätze;
- 114.216 exakt gegengeprüfte charakteristische Polynome, einschließlich 7.746
  H7-Basispolynomen;
- 2.582 Umbenennungs-/Erweiterungstransportprüfungen und 128 reproduzierte Ziehungen;
- sechs verworfene Fehlerfälle: fehlender Abschluss, verlorene Vielfachheit,
  vertauschte Richtungszuordnung, geändertes Polynom, falsche Deduplikation und
  unterschlagene Kollisionsgruppe.

```sh
# Python 3.12 und Git; keine Drittbibliothek.
# Ein frisches Zielverzeichnis wählen.
python3 -B -O research/lorentz_observable_comparison/run.py --run /tmp/x6-observable-fresh
cmp research/lorentz_observable_comparison/results/records.jsonl /tmp/x6-observable-fresh/records.jsonl
cmp research/lorentz_observable_comparison/results/summary.json /tmp/x6-observable-fresh/summary.json
python3 -B -O research/lorentz_observable_comparison/run.py --verify research/lorentz_observable_comparison/results
```

Ein vollständiger Git-Checkout mit dem angegebenen Quell- und Freeze-Commit ist
nötig. Beide Rechenphasen sind auf je 900 Sekunden und 2 GiB begrenzt. Die CI
führt einen frischen Lauf samt Gegenprüfung ohne Netzverbindung aus und vergleicht
sämtliche deterministischen Ergebnisdateien bytegenau. Laufzeiten, Umgebungsdaten
und Zeitstempel werden dabei nicht als identische Ergebnisse verlangt.

[RESULTS.json](results/RESULTS.json) bindet die Dateien durch SHA-256. Ein Fehler
oder Zeitlimit führt zu `INCONCLUSIVE`, nicht zu einem bestandenen Vergleich.
Algorithmisch unterschiedliche Prüfwege sind keine externe unabhängige
Begutachtung. Es wird keine physikalische Validierung beansprucht.

## Konsequenz und nächster sinnvoller Test

N1 eignet sich nach diesem begrenzten Vergleich als erster Kandidat für einen
preiswerten zusätzlichen Vorfilter. Diese Veröffentlichung ändert keinen
historischen Vertrag und ersetzt keine bestehende Zustandsidentität oder
Historiengewichtung durch einen Fingerprint. Ob Q1 bei schwierigeren Klassen
seinen höheren Aufwand rechtfertigt, bleibt offen.

Der nächste Test sollte **gezielt Ordnungen mit identischen lokalen Profilen**
erzeugen und N1 und Q1 daran gegeneinander prüfen. Eine weitere kleine allgemeine
Stichprobe würde die hier sichtbare Schwierigkeit voraussichtlich schlecht
adressieren. Auch dabei müssen Fragestellung und Familie vor dem Lauf feststehen;
eine gefundene Kollision bleibt erhalten.

## Literatur

[1] Y. K. Yazdi, M. Letizia und A. Kempf, *Lorentzian Spectral Geometry with
Causal Sets*, Class. Quantum Grav. 38 (2021) 015011,
[arXiv:2008.02291](https://arxiv.org/abs/2008.02291), Abschnitt 4.2.
Die Arbeit untersucht Spektren zusätzlicher Elemente mit angefügter Relation
und berichtet endliche Trennungsergebnisse bis n=9. Unser Operatorpaket,
Wurzelpaarformat, Korpus und Kostenvergleich sind davon ausdrücklich zu unterscheiden.
