# Knoten-Zuordnung, drei Schichten und ein erster Geometriepilot

Die exakte Zuordnungsreferenz besteht den bisherigen Korpus. Der Dreischicht-Satz
lässt sich unter ausdrücklich angegebenen Voraussetzungen beweisen. Der neue
Geometriepilot liefert dagegen **keinen nachgewiesenen Zusatznutzen der hier
getesteten Schnittprofile** gegenüber den festgelegten Standardmerkmalen.

Dies ist eine ausführbare Forschungsnotiz zum Anschluss an
[PR #39](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/39),
keine etablierte Theorie und keine externe Begutachtung.

## 1. Exakte Vergleichsreferenz mit expliziten Knotenbijektionen

Die indizierten Schnittdaten werden in Spaltenmultimengen zurückverwandelt.
Eine vollständige Suche nach Zeilenbijektionen prüft Teilspaltenmuster;
anschließend werden die Spalten paarweise zugeordnet. Eine positive Entscheidung
liefert eine konkrete Abbildung von Quell- zu Zielknoten. Sie wird erneut gegen
**jeden Eintrag der vollständigen gerichteten Relationsmatrix** geprüft.

| Prüfung | Ergebnis |
| --- | ---: |
| Vorhandene Ordnungen aus PR #39 | 217 |
| Sämtliche größeninternen Paarvergleiche | 7.088/7.088 stimmen mit der Referenz überein |
| Frisch umbenannte Kopien, drei je Ordnung | 651/651 erkannt |
| Vollständig geprüfte Knotenbijektionen | 651 |
| Suchbudgetüberschreitungen | 0 |

Damit werden insbesondere das 16er-Restpaar, das 32er-Rook/Shrikhande-Paar und
die vier Zykluspaare korrekt unterschieden. Die ursprünglichen 7.088
Nichtisomorphie-Referenzurteile werden **hashgebunden aus PR #39 übernommen**;
neu berechnet werden die Suchentscheidungen und sämtliche positiven Zeugen.
Es wird nicht behauptet, dass noch einmal ein personell unabhängiger Prüfer
alle historischen Referenzurteile berechnet hätte.

Eine Entscheidung ist unabhängig von der Knotennummerierung. Die ausgegebene
Bijektion muss wegen möglicher Automorphismen nicht eindeutig sein. Das Verfahren
liefert keine kanonische Nummerierung. Allgemein kann die Laufzeit exponentiell
sein; ein Abbruch liefert `INCONCLUSIVE`, niemals ein falsches Negativurteil.
Automatische Seitenerkennung gilt hier für positive Zweischichtenordnungen;
bei isolierten Elementen wird eine vorgegebene Seitenzuordnung benötigt.

API-Beispiel, nach Einfügen des Modulverzeichnisses in den Python-Suchpfad:

```python
from core import encode, match_indexed, lift_witness
result = match_indexed(encode(A), encode(B))
# result['witness']['rows'] und ['columns']: Quelle -> Ziel,
# für die durch decode sortierten Spalten.
# Bei vollständigen positiven Zweischichtenrelationen C, D:
# node_map = lift_witness(C, D, result['witness'])
```

## 2. Drei Schichten: eine widerlegte und eine bewiesene Aussage

Die [Forschungsbeweise](PROOFS.md) trennen zwei Aussagen:

- **Widerlegt:** Es genügt, die untere–mittlere und mittlere–obere Beziehung
  jeweils unabhängig bis auf Umnummerierung zu rekonstruieren. Ein explizites
  Gegenbeispiel mit sechs Knoten hat auf beiden Seiten einzeln isomorphe
  Beziehungen, aber insgesamt 10 beziehungsweise 9 Relationen. Zusätzlich
  wurden sämtliche 720 Knotenpermutationen geprüft.
- **Bewiesen, eingeschränkt:** Speichert man die gemeinsamen Schnittzahlen der
  **gepaarten** Vorgänger-/Nachfolgernachbarschaften jedes mittleren Knotens,
  rekonstruiert Möbius-Inversion beide Seiten mit derselben mittleren Zuordnung.
  Für eine angegebene Schichtung, feste äußere Labels und eine Ordnung, die nur
  durch angrenzende Beziehungen erzeugt wird, folgt daraus die ganze Ordnung.
  Direkte untere–obere Verbindungen ohne mittleren Weg müssen ausgeschlossen
  oder zusätzlich angegeben werden.

Alle 256 Paare binärer 2×2-Nachbarmatrizen wurden bis zur vollständigen Relation
rekonstruiert. Der allgemeine Satz beruht auf dem Beweis; die endlichen Tests
prüfen die Implementierung. Es wird keine allgemeine kompakte Darstellung,
keine freie Zuordnung aller Schichten und keine graphentheoretische Neuheit behauptet.

## 3. Vorab festgelegter Geometriepilot

**720 neue Ordnungen**, N∈{16,36,64}, vier Erzeugerfamilien, je Größe und Familie
20 Trainings- und 40 Testziehungen. Die insgesamt 480 Testordnungen wurden
nicht für Skalierung, Schwerpunktbildung oder Parameterauswahl verwendet.
Die pseudorandomisierten Ziehungen haben feste öffentlich dokumentierte Schlüssel.

| Familie | Konstruktion |
| --- | --- |
| Minkowski | Gleichverteilte unabhängige Nullkoordinaten (u,v) im Einheitsquadrat; t=(u+v)/2, x=(u−v)/2. Gleiches N entspricht einem auf N konditionierten Sprinkling im 1+1-dimensionalen Alexandrov-Diamanten. Endliche 52-Bit-Pseudorandomisierung ist eine numerische Approximation. |
| Geschichtet | Drei vorgegebene Schichten, Größen N/4,N/2,N/4; unabhängige angrenzende Kanten mit p=1/2 und transitiver Abschluss. |
| Gitter | N ohne Zurücklegen gezogene Gitterpunkte aus einem Quadrat mit 2√N Punkten pro Seite; kausale Ordnung einschließlich lichtartiger Paare. |
| Gestörtes Gitter | Gleiche Stichprobenkonstruktion, zusätzliche unabhängige Koordinatenstörungen in (−0,2;0,2) Gittereinheiten. |

**Basis B:** getrennte Eingangs-/Ausgangs-Linkgradhistogramme, vollständiges
Histogramm der strikten Intervallinneren und sortierte Eigenwerte des
kombinatorischen Laplace-Operators des symmetrisierten Hasse-Diagramms.
Alle Normierungen stehen in [contract.json](contract.json).

**Zusatz P123:** Histogramme gemeinsamer strikter Nachfolger und Vorgänger aller
Ein-, Zwei- und Dreiermengen, jeweils mit Nullwerten und Multiplizitäten.
Hier werden alle Knoten als Wurzeln verwendet. Das ist eine ausdrücklich
definierte Erweiterung der reinen Schnittprofile auf allgemeine endliche
Ordnungen. **Pall, H7, N1, Q1 und R2 werden in diesem Pilot nicht ausgewertet.**
Insbesondere wird der Befund nicht der früheren Kombination R2+Pall zugeschrieben.

Für B, P123 und B+P123 wird derselbe vorab festgelegte Klassifikator verwendet:
nächster Klassenschwerpunkt nach ausschließlich am Training berechneter
Standardisierung. Standardabweichungen ≤10⁻¹² werden als numerisch konstant
behandelt; es gibt keine nachträgliche Abstimmung von Gewichten oder Parametern.

### Testergebnis

Gleichgewichtete Trefferquote über die vier Klassen (*balanced accuracy*),
jeweils 160 Testordnungen pro Zeile:

| N | Basis B | P123 allein | B + P123 | Differenz zur Basis |
| ---: | ---: | ---: | ---: | ---: |
| 16 | 65,625 % | 56,250 % | 66,875 % | +1,250 Prozentpunkte |
| 36 | 74,375 % | 58,750 % | 64,375 % | −10,000 Prozentpunkte |
| **64, primär** | **69,375 %** | **57,500 %** | **62,500 %** | **−6,875 Prozentpunkte** |

Die vorab festgelegte Erfolgsschwelle bei N=64 war mindestens +5 Prozentpunkte
und eine positive untere 95%-Bootstrap-Grenze. Sie wird **nicht erreicht**.
Das gepaarte, nach Klassen geschichtete Test-Bootstrap mit 2.000 Ziehungen ergibt
für die Differenz gerundet **[−13,75; 0,00] Prozentpunkte**. Dieses Intervall
ist bedingt auf den einen Trainingsdatensatz und umfasst keine Unsicherheit
durch erneutes Training oder andere Erzeugerfamilien. Auch eine statistisch
gesicherte Verschlechterung wird wegen der Nullgrenze nicht behauptet.

Die vollständige primäre Verwechslungsmatrix von B+P123 steht hier, Zeilen sind
wahre Klassen, Spalten vorhergesagte Klassen:

| Wahr / vorhergesagt | Minkowski | Geschichtet | Gitter | Gestörtes Gitter |
| --- | ---: | ---: | ---: | ---: |
| Minkowski | 14 | 0 | 6 | 20 |
| Geschichtet | 0 | 40 | 0 | 0 |
| Gitter | 8 | 0 | 27 | 5 |
| Gestörtes Gitter | 15 | 0 | 6 | 19 |

Die leichte Trennung geschichteter Ordnungen ist damit kein Beleg für einen
allgemeinen Geometriedetektor. Die schwierigere Trennung von Minkowski-Ziehungen
und gestörten Gittern gelingt hier nur begrenzt. Lichtartige Gitterpaare,
Relationsdichte, Höhe, Rand und der fest gewählte Klassifikator können die
Ergebnisse beeinflussen. Eine verschlechterte Klassifikation nach Hinzufügen
von Merkmalen beweist keinen Informationsverlust der vollständigen Merkmalsmenge:
Der festgelegte Klassifikator kann zusätzliche, korrelierte Koordinaten ungünstig
gewichten. Dieser Pilot belegt schlicht keinen Zusatznutzen dieses Verfahrens.

## 4. Literaturanschluss und Reichweite

Astrid Eichhorn, Harald Mack, Kim Tuyen Le und Fabian Wagner,
[*Charting causal set configuration space with graph observables*](https://arxiv.org/abs/2605.27514v1),
arXiv:2605.27514v1, eingereicht am 26. Mai 2026, untersuchen neun Klassen
anhand von Graphobservablen. Linkgrade, Intervallhäufigkeiten und das Spektrum
des symmetrisierten Hasse-Laplace-Operators motivieren unsere Basis.
Die dortige Intervallgröße zählt die beiden Endpunkte mit; unser Index k zählt
das strikte Innere, also entspricht er dort k+2. Unser kleiner Vierfamilienpilot
ist keine Replikation der gesamten Arbeit.

Die gezogenen Punktmengen und Graphen sind synthetische Erzeugerdaten. Aus ihrer
Unterscheidbarkeit folgt weder eine Krümmungsrekonstruktion noch ein
Mannigfaltigkeitszertifikat, ein Kontinuumslimes oder eine physikalische
Validierung. Die exakte endliche Rekonstruktionsfrage und diese geometrische
Forschungsfrage bleiben unterschiedliche Abnahmen.

## 5. Chronologie, Gegenprüfung und Kosten

- Öffentlicher Vertrag: [`3e96130`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/3e96130f2907586ba331e6fa2a4d776542accd99), 16.10.2026, 17:49:31 UTC.
- Öffentliche Quellenfixierung: [`fc14a04`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/fc14a049885a9efc1604ce4e4b542945b82c4fcb), 17:53:47 UTC. Die numerische Standardisierungsschwelle wurde davor präzisiert.
- Zielausführung: 17:54:05 bis 17:55:23 UTC. **Keine Rechenquelle wurde nach Betrachtung der Zielergebnisse verändert.** [Chronologie](publication.json) und [Laufquittung](results/RESULTS.json) sind archiviert.

Vorherige Kleintests: alle 256 Paare binärer 2×2-Matrizen gegen vollständige
Permutationssuche, alle 512 binären 3×3-Rekonstruktionen und umbenannten Kopien,
alle 256 Dreischicht-Konstruktionen. Fehlerkontrollen verwerfen fehlende
Teilmengen, falsche Leerzählung, falsche/duplizierte Bijektionen; Budgetabbruch
bleibt `INCONCLUSIVE`. Der Zielprüfer verwirft zusätzlich fehlende Beobachtungen.

Im Zielversuch werden Intervallgrößen getrennt über Matrixprodukte und Bitmengen,
Schnittprofile über explizites Aufzählen von Wurzelmengen je Nachbar und über
Bitmengen berechnet. Hasse-Abschluss und ursprüngliche Relation stimmen überein.
Alle 720 Geometrieordnungen werden umnummeriert und erneut geprüft. Ein separater
skalarer Schwerpunkt-Klassifikator bestätigt alle Vorhersagen. Der größte
Eigenwertunterschied zwischen den beiden NumPy-Rechenwegen beträgt
4,98×10⁻¹⁴; der größte Eigenvektorresidual 2,23×10⁻¹⁴. Diese beiden numerischen
Wege sind keine unabhängigen mathematischen Spektralbeweise.

| Phase, ein lokaler Lauf | Zeit | Linux-Prozess-Spitzenspeicher |
| --- | ---: | ---: |
| Zuordnung einschließlich Dekodieren und Kopien, mit Speicherverfolgung | 37,75 s | 96,20 MiB |
| Geometrieerzeugung, Merkmale und Auswertung | 9,42 s | 69,14 MiB |
| Getrennte Gegenprüfung | 29,45 s | nicht separat berichtet |

Die Python-Speicherverfolgung erfasst für die erste Phase zusätzlich einen
Peak von 24,07 MiB. Prozess-RSS schließt Interpreter und importierte Bibliotheken
ein. Es sind beschreibende Einzellaufkosten, kein kontrollierter
Geschwindigkeitsvergleich. Die 217 dekodierten Inzidenzmatrizen haben zusammen
18.283 binäre Einträge; ihre indizierten JSON-Darstellungen benötigen 737.158
Bytes. Das sind verschiedene Einheiten, keine behauptete Kompressionsrate.

## 6. Reproduktion und externe Prüfung

Voraussetzungen: vollständiger Git-Checkout, Linux/POSIX, Python 3.12,
NumPy 2.3.5. Nach einmaliger Installation läuft die Rechnung ohne Netzwerk.
Ausgabeverzeichnisse müssen neu sein; pro Phase gelten 1.800 Sekunden und
2 GiB Adressraum. Fehler und Ressourcenabbrüche bleiben als `INCONCLUSIVE.json`
mit Protokollen erhalten.

```sh
python3 -m pip install -r research/lorentz_matching_geometry/requirements.txt
OPENBLAS_NUM_THREADS=1 python3 -B -O research/lorentz_matching_geometry/run.py --selftest
OPENBLAS_NUM_THREADS=1 python3 -B -O research/lorentz_matching_geometry/run.py \
  --run /tmp/x6-matching-geometry \
  --source-ref fc14a049885a9efc1604ce4e4b542945b82c4fcb
python3 research/lorentz_matching_geometry/compare.py \
  research/lorentz_matching_geometry/results /tmp/x6-matching-geometry
```

Der [CI-Prüfweg](../../.github/workflows/lorentz-matching-geometry.yml) wiederholt
den vollständigen Lauf in einem Netzwerk-Namespace ohne Netzwerkzugang.
Exakte Ergebnisse und Entscheidungen werden exakt verglichen; numerische
Arrays mit atol=rtol=10⁻⁹. Laufzeiten, Speicherwerte und numerische Residuen
werden nicht auf Bytegleichheit geprüft.

Alle [Rohdaten und Auswertungen](results/) bleiben zugänglich:

- `matching.json.gz`: jede Paarentscheidung und alle Knotenbijektionen.
- `three_layer.json`: vollständige Matrizen des Gegenbeispiels.
- `geometry_records.json.gz`: Koordinaten, Relationsmatrizen und sämtliche Merkmale.
- `geometry_evaluation.json.gz`: Skalierungswerte, Klassenschwerpunkte, Einzelvorhersagen, Distanzen und Bootstrap-Ergebnis.
- `matching_summary.json`, `geometry_summary.json`, `verification.json`: lesbare Zusammenfassungen.
- `matching_costs.json`, `geometry_costs.json`, `numerical_check.json`, `RESULTS.json`: Kosten und Provenienz.

Die getrennten Implementierungen stammen aus demselben Bearbeitungsprozess.
Eine externe Replikation steht aus. Dafür sind insbesondere der Beweis mit
seinen Schichtvoraussetzungen, der Erhalt jeder mittleren Zuordnung und die
fehlende Verwendung der Testdaten beim Fit zu prüfen.

Der nächste sinnvolle Versuch wäre neu festzulegen: dichtere Größenfolgen,
an Dichte und Höhe angepasste Kontrollen und ein eigenständig begründetes
geometrisches Ziel. Der bestehende Testsatz bleibt unverändert ein veröffentlichter
negativer Befund; ein neues Verfahren braucht neue Testziehungen.
