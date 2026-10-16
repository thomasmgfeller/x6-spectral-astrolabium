# Diagnose des verbleibenden H7+N1+Q1-Gegenbeispiels

**16. Oktober 2026 · `PASS_EXACT_DIAGNOSIS` · nachträgliche Untersuchung bekannter Daten.**

Die festgelegte gerichtete Paarverfeinerung **R2 unterscheidet das bekannte Restpaar
bereits in Runde 2**. Sie trennt außerdem alle 6.849 größeninternen Paare der
207 vorhandenen Ordnungen. Die einfacheren Zweier- und Dreier-Schnittprofile I2
und I3 **trennen das Restpaar nicht**. Diese negativen Ergebnisse bleiben erhalten.

Damit liegt ein exaktes zusätzliches Trennzeugnis vor. Weder allgemeine
Rekonstruktion noch Überlegenheit auf unbekannten Daten ist damit nachgewiesen.
Die vollständige gerichtete Relation bleibt die Referenz.

## Festlegung und Geltungsbereich

Der [Vertrag](contract.json) wurde im Commit
[`ba166751`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/ba166751364aa1a267c4f3ae00cea51161f8709f)
veröffentlicht; die getesteten Ausführungsquellen wurden mit
[`00dc46ac`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/00dc46ac9077e94897453ff4320885524f4edfa2)
vor der neuen Merkmalsauswertung eingefroren und veröffentlicht. Details:
[freeze.json](freeze.json), [publication.json](publication.json).

Die Matrizen, ihre bisherigen Merkmale und das Zielpaar waren bereits bekannt.
Die Auswahl der drei Verfahren wurde dadurch motiviert. **Dies ist trotz der
vor dem neuen Lauf festgelegten Auswertung kein unabhängiger Testkorpus.**
Es wurden keine weiteren Ziehungen erzeugt und keine fehlgeschlagene Methode
durch eine nachträglich ausgewählte vierte Methode ersetzt.

Eingabe ist der unveränderte, in PR #36 geprüfte Korpus
[records.jsonl](../lorentz_n1_stress/results/records.jsonl), SHA-256
`97d583ecbf226671a5ffa411799eacb432a0e6106f8ea16c5fd236b7a3267540`.
Er enthält 207 gerichtete Isomorphie-Repräsentanten aus 352 festgelegten Erzeugungen.
Alle Korpuswerte und das bekannte Restpaar `m8-r012` / `m8-r070` bleiben erhalten.

## Warum weitere reine Knotenrunden nicht helfen

**Satz für diese Familie.** Sei die strikte Relation

$$C=\begin{pmatrix}0&B\\0&0\end{pmatrix},$$

wobei jede Zeile und Spalte von B genau d Einsen hat. Starte die gerichtete
Knoten-Farbverfeinerung mit den Vorgänger-/Nachfolgergraden und bilde jede neue
Farbe aus alter Farbe sowie den beiden Multimengen der Vorgänger- und
Nachfolgerfarben. Dann hängt ihr Ergebnis bei jeder Rundenzahl nur von m und d ab.

**Beweis.** Anfangs haben alle unteren Knoten Farbe (0,d), alle oberen (d,0).
Sind in einer Runde die Farben je Schicht konstant, besitzt jeder untere Knoten
keinen Vorgänger und d gleichfarbige Nachfolger; jeder obere besitzt d
gleichfarbige Vorgänger und keinen Nachfolger. Die nächste Farbe ist daher erneut
je Schicht konstant. Induktion beweist die Aussage für alle Runden. Bei gleicher
Schichtgröße sind auch die Farbhäufigkeiten gleich. Der Rechner kontrolliert drei
Runden auf allen Eingaben; die Allrundenaussage folgt aus dem Beweis.

Das betrifft genau diese Verfeinerung und Familie. Es ist keine Aussage über
beliebig große induzierte Nachbarschaften oder alle lokalen Verfahren.

## Die drei festgelegten Merkmale

- **I2:** Multimengen gemeinsamer Nachfolger jedes unteren Zweierpaars und
  gemeinsamer Vorgänger jedes oberen Zweierpaars; beide Richtungen bleiben getrennt.
- **I3:** Für jedes untere beziehungsweise obere Dreiertripel werden die drei
  sortierten Zweierschnittgrößen und die Dreierschnittgröße gemeinsam gespeichert.
  Alle Nullen und Vielfachheiten bleiben erhalten.
- **R2:** Gerichtete Farbverfeinerung auf **geordneten Knotenpaaren**. Initial
  werden beide Gradpaare, Gleichheit und beide Relationsrichtungen gespeichert.
  Die Aktualisierung lautet

$$c_{t+1}(u,v)=\operatorname{encode}\!\left(c_t(u,v),
\left\{\!\left\{(c_t(u,w),c_t(w,v)):w\in V\right\}\!\right\}\right).$$

Die inneren Farbpaare sind geordnet und bleiben gekoppelt. Zwei getrennte
Randverteilungen wären eine andere, schwächere Aktualisierung. Die Kodierung
vergleicht exakte Tupel einschließlich ihrer Vielfachheiten; keine gerundeten
Eigenwerte und keine Hashgleichheit entscheiden über Merkmalsgleichheit.

Die Farbnummern werden für alle Ordnungen derselben Größe gemeinsam vergeben.
Sie sind **nur innerhalb dieser gemeinsamen Auswertung vergleichbar**, keine
portablen Fingerprints einzelner Graphen. Beim Vergleich neuer Eingaben müssen
die Farben gemeinsam neu bestimmt oder ihre vollständigen Definitionen erhalten
werden. Abgebrochen wird erst, wenn die Zahl der Farbklassen nicht mehr wächst.
Da die alte Farbe Teil jeder neuen Farbe ist, können Klassen nur geteilt werden;
dieses Kriterium beweist Stabilität der Partition.

**Invarianz.** Eine gerichtete Isomorphie erhält die Anfangstupel. Die Bijektion
der Zwischenknoten w erhält in jeder Runde die vollständige Multimenge der
geordneten Farbpaare. Induktion liefert den Transport aller Paarfarben.
Unterschiedliche Farbhäufigkeiten beweisen deshalb Nichtisomorphie. Gleiche
Häufigkeiten beweisen keine Isomorphie.

R2 ist eine konkret festgelegte gerichtete Anwendung der bekannten
Weisfeiler-Leman-Paarverfeinerung, kein Neuheitsanspruch.

## Vollständiges Ergebnis

Die Zahlen zählen ungetrennte, bereits als nichtisomorph bekannte Paare derselben Größe.

| Elemente | Ordnungen | Verglichene Paare | I2 allein | I3 allein | R2 allein | H7+N1+Q1 |
|---:|---:|---:|---:|---:|---:|---:|
| 12 | 6 | 15 | 0 | 0 | 0 | 0 |
| 14 | 11 | 55 | 1 | 0 | 0 | 0 |
| 16 | 32 | 496 | 29 | 4 | 0 | 1 |
| 18 | 68 | 2278 | 317 | 9 | 0 | 0 |
| 20 | 90 | 4005 | 535 | 9 | 0 | 0 |
| **Gesamt** | **207** | **6849** | **882** | **22** | **0** | **1** |

Mit H7+N1 verbleiben bei I2 insgesamt 15, bei I3 sechs und bei R2 null Paare.
Zum bereits bestehenden H7+N1+Q1 hinzugefügt lassen I2 und I3 jeweils das eine
bekannte Restpaar offen; R2 trennt es. Sämtliche Klassen, Kombinationen und
Restgruppen stehen in [summary.json](results/summary.json). Die Paarzahlen sind
abhängig und keine Populations-Erfolgswahrscheinlichkeiten; es werden keine
p-Werte angegeben.

## Konkretes mathematisches Trennzeugnis

Das Zielpaar bleibt unter I2 und I3 exakt gleich. In R2 stimmen die Farbhäufigkeiten
bei Initialisierung und nach Runde 1 überein. In Runde 2 unterscheidet eine
Farbklasse: **null geordnete Paare in `m8-r012`, zwei in `m8-r070`.**

Die nach dem Ergebnis angelegte Interpretation [certificate.json](results/certificate.json)
übersetzt diese bereits gefundene Klasse in direkte Relationszählungen.
Sie ist keine vierte Methode des festgelegten Vergleichs. Setze
G = B Bᵀ; Gᵤᵥ zählt die gemeinsamen Nachfolger unterer Knoten u und v.
Gesucht werden geordnete verschiedene untere Paare mit Gᵤᵥ=2 und folgender
Multimenge von (Gᵤ𝓌,G𝓌ᵥ) über **alle acht unteren w**, einschließlich u und v:

| Gemeinsame-Nachfolger-Zählpaar | Vielfachheit |
|---|---:|
| (0,0) | 2 |
| (0,1) | 1 |
| (1,0) | 1 |
| (1,2) | 1 |
| (2,1) | 1 |
| (2,3) | 1 |
| (3,2) | 1 |

In `m8-r070` erfüllen die Paare **(3,5) und (5,3)** diese Bedingung (Nullzählung),
in `m8-r012` kein Paar. Die vollständigen B-Blöcke stehen im Zertifikat.
Skalarprodukte und explizite Mengenschnitte liefern dieselben Zahlen; die
Zugehörigkeit wurde für alle geordneten unteren Paare beider Ordnungen mit
der ursprünglichen R2-Klasse abgeglichen.

**Warum dies ein Zertifikat ist:** Eine gerichtete Isomorphie muss die beiden
Schichten erhalten. Sie transformiert B durch Zeilen- und Spaltenpermutationen,
also G durch dieselbe Permutation seiner Zeilen und Spalten. Sie erhält daher
die Häufigkeit des angegebenen vollständigen Zählmusters. Null und zwei können
nicht durch Umbenennung ineinander übergehen. Dies beweist die Nichtisomorphie
dieses Paars unmittelbar. Der ebenfalls erneut geprüfte Ausschluss einer
Isomorphie zur Zeitumkehr ist ein separater Befund.

Die verlorene Information liegt hier in der Zuordnung gemeinsamer Nachbarschaften
zu einem bestimmten Wurzelpaar. Die global gesammelten I3-Tripelmuster bewahren
diese Zuordnung nicht ausreichend. Daraus folgt keine allgemeine Rangordnung
aller Schnitt-, Spektral- und Erweiterungsmerkmale.

## Prüfung und Kosten

- Bitmengen-Schnitte gegen explizite Inzidenzsummen für I2 und I3.
- Zwischenknoten-Aufzählung gegen Mengenschnitte von Farbklassen für R2;
  **jede Farbmatrix jeder Runde** wurde verglichen.
- Umbenennung aller 207 Eingaben und Transport sämtlicher Paarfarben überprüft.
- Beide bisherigen exakten Spektralrechenwege bestätigen die vollständige
  H7/N1/Q1-Gleichheit des Zielpaars erneut: jeweils 198 Polynome.
- Zwei exakte Isomorphiealgorithmen bestätigen Nichtisomorphie und Nichtdualität.
- Sechs gezielte Fehlerfälle verworfen: Selbstschleife, falscher Dreierschnitt,
  verlorene Vielfachheit, fehlende Ordnung, falsche Paarfarbe und falsche Restklasse.
- Vor dem Quellfreeze: Spielzeugfälle bis vier Knoten; ein synthetischer
  Drei-Knoten-Farbtest erkennt den Verlust der Kopplung beider Farbkomponenten.

| Merkmal | Neue Polynomaufrufe | Ganzzahlen im Merkmal |
|---|---:|---:|
| I2 | 0 | 15430 |
| I3 | 0 | 150472 |
| R2 | 0 | 109818 |

R2 benötigt hier 6.400.448 logische Zwischenknotenbeiträge. Einschließlich der
abschließenden Stabilitätsprüfung laufen je Größe 4, 4, 5, 5 und 5 Runden.
Die vollständigen Rundenspuren enthalten zusätzlich 412.444 Ganzzahlen. Die
R2-Histogrammgröße allein ist **kein** eigenständiger Speicherbedarf ohne
gemeinsamen Farbkontext. [costs.json](results/costs.json) enthält die Zähldefinitionen.

Erster Lauf: Produzentenphase 3,18 s, Gegenprüfung einschließlich Umbenennungen
und Zielpaar-Referenzen 39,14 s, Python 3.12.14. Diese Einzelmessung ist **kein
kontrollierter Geschwindigkeitsvergleich** mit den historischen Q1-Laufzeiten.
Es wurde keine industrielle Effizienz nachgewiesen. Zwei Implementierungen aus
demselben Arbeitsprozess ersetzen keine externe Begutachtung.

## Reproduktion

Voraussetzung: vollständiger Git-Checkout, Python-Standardbibliothek. Der Runner
prüft den Originalkorpus und alle eingefrorenen Quellen gegen den öffentlichen
Quellcommit. Das Ausgabeziel muss neu sein.

```sh
python3 -B -O research/lorentz_residual_diagnosis/run.py --selftest
python3 -B -O research/lorentz_residual_diagnosis/run.py \
  --source-ref 00dc46ac9077e94897453ff4320885524f4edfa2 \
  --run /tmp/residual-diagnosis-fresh
for name in features.jsonl rounds.json summary.json costs.json target.json verification.json; do
  cmp "research/lorentz_residual_diagnosis/results/$name" "/tmp/residual-diagnosis-fresh/$name"
done
python3 -B -O research/lorentz_residual_diagnosis/explain.py
```

Die [CI](../../.github/workflows/lorentz-residual-diagnosis.yml) ist vom Repository-
Wurzelverzeichnis unter `.github/workflows/lorentz-residual-diagnosis.yml` erreichbar.
Sie wiederholt die vollständige Auswertung ohne Netzwerkzugriff und vergleicht
alle sechs deterministischen Ergebnisdateien bytegenau. Die getrennt markierte
Zertifikatsinterpretation wird ebenfalls wiederholt. Tatsächliche Laufdaten und
Prüfsummen: [RESULTS.json](results/RESULTS.json). Ein abgebrochener oder fehlerhafter
Lauf erhält `INCONCLUSIVE`; ein fehlendes Trennresultat wäre kein Rechenfehler.

## Konsequenz und nächstes offenes Abnahmekriterium

R2 ist nach diesem Befund ein begründeter Kandidat für eine zusätzliche
Isomorphie-Vorfilterstufe. Die alten Spektralmerkmale sind dadurch weder allgemein
ersetzt noch nutzlos. Bei Merkmalsgleichheit bleibt die vollständige gerichtete
Isomorphieprüfung erforderlich.

Der nächste getrennte Prüfauftrag ist ein **vor den neuen Eingaben festgelegter
Vergleich auf anderen Größen und Ordnungsfamilien**, einschließlich nichtregulärer
und höherer Schichten sowie gezielter R2-Gegenbeispiele. Erst danach sind Aussagen
über Übertragbarkeit und eine praktisch geeignete Auswahlregel möglich. Diese
neuen Eingaben wurden in diesem Auftrag nicht erzeugt.

Keine neue Physik, Raumzeitrekonstruktion, Quantendynamik, Kontinuumsgrenze,
allgemeine Vollständigkeit oder Neuheit wird aus diesem Befund abgeleitet.

## Literaturanschluss

- L. Babel, I. V. Chuvaeva, M. Klin, D. V. Pasechnik: *Algebraic Combinatorics in
  Mathematical Chemistry. Methods and Algorithms. II. Program Implementation of
  the Weisfeiler-Leman Algorithm*, [arXiv:1002.1921](https://arxiv.org/abs/1002.1921).
  Literaturgrundlage für die Verfeinerung von Knoten und geordneten Paaren.
- F. Fuhlbrück, J. Köbler, I. Ponomarenko, O. Verbitsky: *The Weisfeiler-Leman
  Algorithm and Recognition of Graph Properties*,
  [arXiv:2005.08887](https://arxiv.org/abs/2005.08887).
  Kontext für Möglichkeiten und Grenzen von WL-Verfahren.

Die eigenen Zahlen und das konkrete Trennzeugnis stammen ausschließlich aus den
beigefügten Rechenartefakten; sie werden nicht den Literaturquellen zugeschrieben.
