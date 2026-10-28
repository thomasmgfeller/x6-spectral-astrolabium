# CSPP v0.8: unabhängige G1-Prüfung vor Dirac

**Ergebnis: Alle zwölf untersuchten Parameterzellen scheitern an einer
notwendigen G1-Bedingung. Dirac wird nicht begonnen.** G1 bleibt HOLD,
G2/G3 bleiben NOT_RUN. Das Ergebnis betrifft diese bisherige Operatorfamilie
und diese zwölf Zellen, keinen allgemeinen Unmöglichkeitssatz.

Die Testfamilie, Fehlerbudgets, Ensemblegröße und Abbruchregeln wurden am
28. Oktober 2026 um 11:49:31 Schweizer Zeit vor dem ersten neuen Zufallsaufruf
[öffentlich eingefroren](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/b8d4d1f68be151ece433d74900a23fc64726744f).
Der neue Lauf begann um 11:50:05. Alle ursprünglich eingefrorenen Quellen
sind weiterhin bytegleich; siehe [FREEZE.json](FREEZE.json) und
[REGISTRATION.json](REGISTRATION.json).

## Unabhängige Daten und statistische Entscheidung

- **256 frische Wolken**, je 64 bei nu=512,1024,2048,4096; insgesamt 490.744 Punkte.
- Alle drei bisherigen Glättungen epsilon=1,1/4,1/16, innerhalb jeder Wolke gepaart.
- Alle zehn unveränderten glatten Skalarfelder an 21 festen inneren Proben.
- 768 Zellrealisierungen und 7.680 Feld-/Zellrealisierungen, ohne Ausfall,
  verworfene Wolke, Ersatzziehung oder vorzeitige statistische Beendigung.
- Eigene Methodenvalidierungsströme. Der spätere E4-Bestätigungsseed bleibt unbenutzt.

Die notwendige Bedingung lautet Populations-RMS <=10% für **jedes** Feld.
Die vorab festgelegte Binomialregel kontrolliert das gemeinsame Risiko einer
falschen Ablehnung über 120 Feld-/Zellentests auf höchstens 2,5%, unter dem
unabhängigen Wolkenmodell. Sie setzt keine beschränkte RMS-Verteilung voraus.
Die statistische Einheit ist die Wolke, nicht eine einzelne Probe.

**119 von 120 Tests verwerfen die 10-%-Bedingung.** In jeder Parameterzelle
haben mehrere Felder in allen 64 Wolken einen sicher eingeschlossenen Fehler
über 20%. Daraus folgt jeweils eine simultane untere Populations-RMS-Grenze
von **18,7184%**. Die Grenze ist konservativ und keine Schätzung des gesamten
Fehlers: Die binäre Regel verwendet nur die Überschreitung der 20-%-Schwelle.

Die einzige Nichtverwerfung betrifft das konstante innere Feld bei nu=512,
epsilon=1/16:15 sichere Überschreitungen reichen nicht für die vorab verlangten 30.
Das ist keine Freigabe; die übrigen neun Felder derselben Zelle scheitern.
Bei nu=1024,epsilon=1/16 hat dieses Feld 45 Überschreitungen; in den übrigen
118 Feld-/Zellentests sind es jeweils 64. Alle Einzelergebnisse stehen in
[DECISION_128.json](results/DECISION_128.json).

Zur Größenordnung: größter beobachteter gepoolter normalisierter RMS unter
allen zehn Feldern, jeweils über 64 Wolken und 21 Proben. Diese Werte sind
**deskriptiv**; die abgesicherte Entscheidung beruht auf der oben genannten
vorregistrierten Regel. Die Zielzahl in dieser Tabelle ist 0,100.

| Erwartete Punkte nu | epsilon=1 | epsilon=1/4 | epsilon=1/16 |
|---:|---:|---:|---:|
| 512 | 334,413 | 8,984 | 1,466 |
| 1024 | 700,844 | 19,732 | 2,036 |
| 2048 | 1.563,632 | 40,294 | 3,600 |
| 4096 | 2.838,505 | 77,632 | 7,997 |

## Fehlerkontrolle und Reproduktion

Der exakte diskrete Operatorfehler wird getrennt von gerundeter
Feldauswertung sowie Koeffizienten-/Summationsrundung eingeschlossen.
Die größten normalisierten numerischen Beiträge betragen 6,952e-13
beziehungsweise 1,791e-12 und bleiben weit unter den getrennten Budgets 1e-8.
Der größte Ball-Komponentenradius liegt unter 6,006e-34.
Eine präzise Rechnung des diskreten Operators behebt dessen großen
Kontinuumsfehler somit nicht.

Alle **161.280 komplexen Operatorwerte** überlappen in den 128-/192-Bit-Einschließungen.
Beide CPU-Konfigurationen bestätigen alle benötigten Kausalrelationen,
Intervallzahlen und Gebietsmitgliedschaften. Pro Konfiguration werden
721.365.292 Wolke/Wolke- und Wolke/Probe-Vergleiche geprüft.
Die maximale Koordinatenabweichung bei deaktiviertem AVX-512 beträgt 8,882e-16;
auf kanonischen Koordinaten unterscheiden sich die numerischen Wirkungen
höchstens um 3,553e-15, innerhalb der unveränderten Toleranzen.
Die exakten Near-null-Fallbacks werden durch separate Grenzfalltests geprüft.

Die 128-Bit-Produktion dauerte 121,14s, die 192-Bit-Wiederholung 130,45s;
maximale gemessene RSS 324,33MiB. Die beiden CPU-Audits dauerten zusammen
rund 166s. Einschließungen gelten für die gespeicherten dyadischen Koordinaten;
eine Identität mit idealer kontinuierlicher Poisson-Geometrie wird nicht behauptet.

[Amendment01](amendment_01/README.md) dokumentiert eine ausschließlich technische
Korrektur am Veröffentlichungsprüfer: irrational gerundete RMS-Berichtswerte
müssen nicht bei 128 und 192Bit bytegleich sein. Der neue Prüfer verlangt
weiterhin exakt gleiche Zählungen, rationale Endpunkte und Entscheidungen
und kontrolliert jede veröffentlichte Untergrenze zusätzlich bei 256Bit.
Der ursprüngliche Prüfer, alle eingefrorenen Analysequellen und sämtliche
Prüfdaten bleiben erhalten und unverändert.

[Amendment02](amendment_02/README.md) korrigiert zusätzlich einen eindeutigen
Importpfad im Replay-Aufrufer: GitHub hatte wegen eines gleichnamigen
Vorgängermoduls vor der Neuberechnung abgebrochen. Der richtige eingefrorene
v0.8-Audit wird jetzt ausdrücklich geladen; keine Prüfung wird übersprungen.

```bash
python -m pip install -r research/cspp/independent_g1_v0_8/requirements.txt
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python -O -B research/cspp/independent_g1_v0_8/publication_checks.py
python -B research/cspp/independent_g1_v0_8/publication_checks.py --replay
```

Der Replay verwendet dieselben archivierten Wolken in temporären Dateien;
er ist kein weiteres unabhängiges Experiment. Die CI prüft außerdem jede
ursprünglich eingefrorene Quelldatei gegen den öffentlichen Vorregistrierungscommit.
[CHECKS.json](results/CHECKS.json), [AUDIT.json](results/AUDIT.json),
[CPU_DEFAULT.json](results/CPU_DEFAULT.json) und
[CPU_BASELINE.json](results/CPU_BASELINE.json) enthalten die Kontrollen.

## Entscheidung und Reihenfolge der nächsten Arbeiten

**Kein Dirac-Ausbau auf Basis dieser Kandidaten.** Die notwendige lokale
Operatorprüfung scheitert bereits. Deshalb werden gemäß Abbruchregel keine
neuen Propagationsensembles oder fermionischen Läufe an diese Kampagne angehängt.
Die Anfangsdaten-/Propagationsnachweise aus v0.7 bleiben Entwicklungsnachweise;
die räumliche Detektorintegration und eine vollständige positive G1-Qualifikation
bleiben offen. Nichtverwerfen allein hätte ebenfalls kein G1-PASS geliefert.

Vor einer neuen positiven G1-Prüfung braucht es einen verbesserten und innerhalb
des Budgets begründeten skalaren Kandidaten, eine obere Genauigkeitskontrolle
und die vollständige Anfangsdaten-/Propagationskette. Dafür sind ein neuer
Freeze und wieder unabhängige Daten erforderlich. Die Daten dieser Kampagne
sind danach bekannt und dürfen nicht erneut als unberührt bezeichnet werden.

Erst nach bestandenem G1 folgt G2 mit **direkter Dirac-Wirkung und Quadratvergleich**
Q_C² gegen B_C tensor I4, zusätzlich Spin-/Lorentztransformation,
Umnummerierung, Dispersion/Zusatzmoden, Norm/Strom und Kausalität.
Eine Matrixwurzel allein genügt nicht. Flavor und Kohärenz folgen erst nach
den nötigen Operator-, Spinstruktur- und gemeinsamen Geometrieprüfungen bis G3.

[Festes Protokoll](PROTOCOL.json), [Herleitung und Grenzen](METHODS.md).
Dieser PR baut auf dem noch offenen PR#139 auf; frühere Pakete und deren
wissenschaftliche HOLDs bleiben unverändert.
