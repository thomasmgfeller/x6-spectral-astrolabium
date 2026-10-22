# Eigenzeit: Ursache verletzter Kausalbeziehungen

**22.10.2026 — Diagnose abgeschlossen; wissenschaftliche Freigabe bleibt HOLD.**

[Ergebnisbericht (Deutsch)](package/Ergebnisbericht.txt) ·
[Vollständiges unverändertes Prüfpaket](Eigenzeit_Kausaldiagnose_2026-10-22.zip) ·
[Reproduktion](package/README.txt) ·
[Maschinenlesbare Auswertung](package/evidence/summary.json) ·
[Veröffentlichungsnachweis](publication.json)

## Befund

Die Diagnose untersucht den [Vier-Landmarken-Piloten vom 21.10.2026](../four_landmark_count_covariance/README.md).
Alle 32 ursprünglichen Auswahlversuche bleiben erhalten: 18 ausgewählte
Konfigurationen, elf ohne vierte Landmarke und drei frühere Audit-Ausfälle.
Der ursprüngliche Gesamtbefund bleibt **1/32 geometrisch qualifizierte Hauptfälle**.

Alle **39 verletzten Beziehungen** der 17 rechnerisch gültigen Hauptsysteme
betreffen gegenseitige Stützpunktabstände. Diese werden aus den unsicheren
Landmarkenabständen rekonstruiert; ihre bekannten Ordnungsbedingungen werden
erst danach geprüft. Es fehlen 23 tatsächliche Beziehungen, 16 zusätzliche
werden erzeugt. In allen 39 Fällen kippt das Intervallvorzeichen.

Mit denselben 18 Konfigurationen ergeben kontrollierte Ersetzungen durch
Werte aus der wahren Geometrie:

| Exakt ersetzte Eingaben | Vollständige Ordnung korrekt |
| --- | ---: |
| Keine | 1/18 |
| Nur Landmarken–Landmarken-Abstände | 2/18 |
| Nur Landmarken–Wurzel-Abstände | 1/18 |
| Nur Landmarken–Stützpunkt-Abstände | 5/18 |
| Landmarken–Landmarken und Landmarken–Stützpunkte | 18/18 |
| Alle drei Gruppen | 18/18 |

Das sind **Diagnoseinterventionen mit Zugang zur Wahrheit**, keine nutzbare
intrinsische Korrektur. Die Effekte sind nicht additiv. Alle 162 archivierten
Zählwiederholungen wurden nachgerechnet; die vollständigen 1.296 Interventionen
stehen in [interventions.json](package/evidence/interventions.json).
Die Originalmesspipeline enthält 154 gültige Gewichtssysteme, sieben
`COUNT_HOLD` und ein `UNRESOLVED`. Rohe Geometrieinterventionen dürfen nicht
als Freigabe der ursprünglichen Mindestzählkontrollen gelesen werden.

## Eingrenzung der Ursache

- **Rundung erklärt diese Fehler nicht:** Alle 5.275 Paarvorzeichen der 17
  gültigen Hauptsysteme stimmen mit einer exakten rationalen Gegenrechnung
  auf den Binär64-Eingaben überein. Die zusätzliche Rechnung einschließlich
  Zähltransformation und pi bei 80 und 120 Dezimalstellen bestätigt sie.
  Das ist eine getrennte Rechenformulierung, keine neue Sage-Ausführung.
- **Zählunsicherheit ist relevant:** 216 neue Zählwolken bei denselben 18
  Konfigurationen liefern 6/72, 11/72 und 31/72 vollständig bestandene
  Mess-/Solve-/Ordnungsprüfungen bei Dichtefaktoren 1, 4 und 16. Vier
  Wiederholungen erzeugen keine vier unabhängigen Landmarkenauswahlen.
- **Die nichtlineare Transformation hat einen Bias:** Die Rekonstruktion
  aus den erwarteten transformierten Poisson-Zählwerten besteht 15/18
  Ordnungsprüfungen. Das untersucht $G(E[q])$, nicht $E[G(q)]$; es zerlegt
  den gesamten Rekonstruktionsbias noch nicht vollständig.
- **Kein Abschneiden der gezählten Intervalle:** Alle Endpunkte liegen im
  äußeren Alexandrov-Diamanten; dessen kausale Konvexität schließt eine
  Beschneidung dieser Intervalle aus. Effekte der Gebietsgröße auf eine
  erneut ausgeführte Landmarkenauswahl sind damit nicht ausgeschlossen.

[Paarweise Fehlerdaten](package/evidence/violated_pairs.json) ·
[Neue Zähldaten](package/evidence/density_records.json) ·
[Dichteauswertung](package/evidence/density_summary.json) ·
[Präzision und Bias](package/evidence/supplement.json)

## Sechs-Punkte-Gegenbeispiel

Vier Landmarken und zwei Stützpunkte mit 14 gezählten Intervallen reichen
für ein separat prüfbares Beispiel aus `cloud-02/B0`:

| Normiertes Intervallquadrat | Wert | Typ |
| --- | ---: | --- |
| Wahre Geometrie | +0,05120553304717898 | raumartig |
| Rekonstruktion | −0,00999147137836352 | zeitartig |

[Eingaben](package/evidence/minimal_counterexample.json) und
[Prüfer](package/verify_witness.py) sind vollständig enthalten. Der Prüfer
benötigt nur die Python-Standardbibliothek und verwendet rationale Arithmetik.
Das Beispiel wurde nachträglich als erstes B0-Fehlerpaar nach Wolkenindex
ausgewählt; es ist keine neue Unmöglichkeitsaussage.

## Reproduktion und Herkunft

Der Ordner `package/` entspricht allen **167 Mitgliedern** des unveränderten
ZIP-Archivs. Darin sind auch alle 141 ursprünglichen Archivdateien unverändert
enthalten. Die 166 Einträge der neuen [SHA-256-Liste](package/SHA256SUMS.txt)
prüfen alle Paketdateien außer der Prüfliste selbst.

In einer separaten Arbeitskopie von `package/`:

```sh
sha256sum -c SHA256SUMS.txt
python3 verify_witness.py
OPENBLAS_NUM_THREADS=1 python3 diagnose.py
OPENBLAS_NUM_THREADS=1 python3 density_diagnostic.py
OPENBLAS_NUM_THREADS=1 python3 supplement.py
```

Die Reproduktionsprogramme überschreiben ausschließlich die neuen
Ergebnisdateien dieser Arbeitskopie. Python 3.12.14, NumPy 2.3.5 und SciPy
1.17.0 wurden verwendet; Zeitmessungen müssen nicht bytegleich sein.

[PROTOCOL.txt](package/PROTOCOL.txt) und die beiden Hauptskripte wurden vor
ihrer Ausführung lokal gehasht. Das ist keine öffentliche Präregistrierung
und keine Verblindung gegenüber den bekannten alten Ergebnissen. Die
[ergänzenden Fragen](package/SUPPLEMENT_PLAN.txt) sind adaptive Folgeanalysen.

ZIP SHA-256:

```text
d42ebd87f279afd30cf1f1caf091cec54981ecd8a6ef694f779b52b927b5ef48
```

**`HOLD_PHASE3`, `HOLD_EMBEDDING_COVARIANCE` und `METADATA_HOLD` bleiben.**
Keine praktische Eigenzeitkorrektur, Operatorüberlegenheit, Krümmungs-,
3+1-, Kalman- oder physikalische Sensorqualifikation. Eine externe Replikation
des vollständigen Generators und Selektors wurde nicht ausgeführt.

## English scope

This fixed-configuration diagnosis localizes all 39 primary order mismatches
to indirectly reconstructed support-to-support intervals. All 162 archived
count records replay. Across 1,296 factorial interventions, replacing the
landmark metric and landmark-to-support distances by true geometry restores
all 18 selected primary configurations; this is an Oracle diagnostic, not
a usable intrinsic correction. The original overall qualification remains
1/32, including the 14 unselected attempts.

Exact rational calculations and separate 80/120-digit calculations preserve
all 5,275 checked pair signs. A new conditional campaign generates 216 count
clouds and passes 6/72, 11/72 and 31/72 complete checks at density factors
1/4/16, respectively. The configurations are the same 18 selected cases.
Concave count transformation also matters: reconstruction at expected
transformed inputs passes 15/18 orders, evaluating $G(E[q])$, not $E[G(q)]$.
All counted intervals are contained in the outer diamond; selection-domain
effects remain outside that conclusion.

The unchanged ZIP, all extracted files, full raw evidence, failed cases,
analysis plans and standalone six-node witness are published together.
All scientific holds remain unchanged. Publication does not claim a new
research rerun, public preregistration or independent third-party validation.

SPDX-License-Identifier: Apache-2.0
