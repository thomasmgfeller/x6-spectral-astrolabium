# Eigenzeit: unabhängige SageMath-Prüfung / independent SageMath audit

**21.10.2026 — Exact controls: PASS. Archived numerical audit: PASS. New-cloud confirmation: NOT_RUN.**

[Vollständiges unverändertes Prüfpaket herunterladen](Eigenzeit_Sage_Pruefung_2026-10-21.zip) ·
[Ergebnisbericht (Deutsch)](evidence/Ergebnisbericht.txt) ·
[Sage-Prüfcode](evidence/audit_sage.py) ·
[Maschinenlesbares Ergebnis](evidence/audit_summary.json) ·
[Vertrag und Toleranzen](evidence/CONTRACT.json)

## Ergebnis und Reichweite

Eine separat implementierte Rechnung mit **SageMath 10.9** bestätigt die
Gewichts- und Operatorauswertung des archivierten 2+1-Minkowski-Versuchs.
Der Prüfer importiert keine X6-Solver-, Designmatrix- oder Feldauswertungsfunktionen.
Er löst das vollständige KKT-System bei 128 und 256 Bit Präzision und erhält
die gemeinsame Rootkovarianz im Minimum-Varianz-Kriterium `H = I + 11ᵀ`.

- **16/16 exakte rationale Kontrollen** bestanden. Sage reproduziert den zuvor
  in Wolfram berechneten linearen Feldfehler **−20/231** exakt.
- **2.104/2.104 Prüfaussagen insgesamt** bestanden; darin sind die 16 exakten
  Kontrollen enthalten. Dies sind keine 2.104 unabhängigen statistischen Versuche.
- **64 archivierte Wolken** berücksichtigt: 30 vollständige von 32 im alten
  Kalibrierblock, 28 vollständige von 32 im alten Testblock. Sechs unverfügbare
  Supports bleiben erhalten; keine Wolke wurde ersetzt.

| Alter Testblock, 28 vollständige Wolken | Rauschfreier Operator-RMSE |
| --- | ---: |
| Originale rekonstruierte Geometrie | 1.446311382926 |
| Relationsprojektion | 1.455090213315 |
| Tatsächliche Simulatorgeometrie (Oracle) | 0.063031955409 |

Die vollständige quadratische Zerlegung ergibt
`2.091816616380 = 0.003973027403 + 2.074648518241 + 0.013195070736`:
Diskretisierungsrest, Rekonstruktionsdifferenz und signierter Kreuzterm.
Der Kreuzterm ist erforderlich; zwei unabhängige positive Fehlerbudgets folgen
daraus nicht. Die geprüften numerischen Unterschiede zwischen X6 und Sage
erklären den großen Original-Oracle-Unterschied in diesem Datensatz nicht.

**Diese Veröffentlichung bestätigt keine neue Population, keine nutzbare
Geometriekorrektur, keine zusätzliche Eigenzeitqualifikation und keinen
3+1-Transfer.** Die tatsächlichen und rekonstruierten Koordinaten werden aus
dem Archiv übernommen. Generator und intrinsischer Rekonstruktionsalgorithmus
sind damit nicht vollständig unabhängig implementiert oder bestätigt.
Die vier Sinus-/Kosinusfelder sind ebenfalls die früheren Felder.
Die sechs Ausfälle werden nicht als bestandene Geometrien gezählt.

**`HOLD_PHASE3`, `HOLD_EMBEDDING_COVARIANCE` und `METADATA_HOLD` bleiben bestehen.**

## Geprüfter Quellstand und Herkunft

Der Audit bezieht sich auf den unveränderlichen Forschungsstand
[`ee6460971c2b3ec48ea2ebb18002072ca3d22f97`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/ee6460971c2b3ec48ea2ebb18002072ca3d22f97),
nicht auf eine Behauptung über den aktuellen Gesamtzustand von `main`.
Siehe das ursprüngliche
[Ablationsprotokoll an diesem Commit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/ee6460971c2b3ec48ea2ebb18002072ca3d22f97/research/lorentz_local_dalembert/reconstruction_ablation/PROTOCOL.md).
Das selbständige [Eingabepaket](evidence/inputs.json) enthält die benötigten
Archivwerte und SHA-256-Hashes der ursprünglichen Wolkendateien.

Das ZIP ist bytegleich mit dem vom Nutzer freigegebenen Prüfpaket:

```text
SHA256  cedd50f512cc0096903ace72245e1284aea85fdd280877ff934170637d6e9959
```

[SHA256SUMS](evidence/SHA256SUMS.txt) bindet die ausgepackten Belege.
[publication.json](publication.json) dokumentiert Publikationsbasis,
geprüften Quellstand, Status und unveränderte HOLD-Entscheide.
Die [ursprünglichen Laufprotokolle](evidence/audit_run.log) und der
[exakte Kontrolllauf](evidence/exact_run.log) bleiben erhalten.
Ein erster Lauf endete vor jeder mathematischen Prüfung wegen eines
Sage-API-Aufrufs zur Matrixkopie; ursprünglicher Code, Vertrag und Fehlerprotokoll
liegen unverändert unter [attempts](evidence/attempts/). Die dokumentierte
API-Korrektur änderte keine Daten, Toleranzen oder mathematischen Kriterien.

## Reproduktion

In einer aktivierten SageMath-10.9-Umgebung:

```sh
cd research/lorentz_sage_reconstruction_audit/evidence
sha256sum -c SHA256SUMS.txt
python audit_sage.py --exact-only
python audit_sage.py
```

Der Lauf schreibt Ergebnisdateien in dieses Verzeichnis. Für einen Vergleich
mit den unveränderten Archivdateien vorher eine Kopie anlegen. Die zweite
Ausführung umfasst die exakten Kontrollen ebenfalls. Erwartet werden 16/16
exakte Kontrollen, insgesamt 2.104/2.104 Kontrollen und 58 geprüfte vollständige
Wolken; die Laufzeit ist kein bytegleiches Reproduktionsziel.

[environment-explicit.txt](evidence/environment-explicit.txt) fixiert die
Linux-64-Conda-Pakete des ausgeführten Laufs. Installation beispielsweise mit
`conda create -n x6-sage-audit --file environment-explicit.txt`, anschließend
`conda activate x6-sage-audit`. Sage-10.9-Conda verwendet hier Python 3.13.16;
das Python wird innerhalb dieser Sage-Umgebung ausgeführt.

Archivierte float64-Eingaben werden als ihre exakten binären Rationalwerte
interpretiert. Höhere Rechenpräzision macht daraus keine exakt bekannten
Kontinuumskoordinaten. Für transzendente Feldwerte wird Präzisionskonvergenz
geprüft; es wird kein rigoroses Intervallzertifikat behauptet.

## English scope

This is an independent **computational audit of archived data**, using SageMath
10.9 and a separately implemented full KKT solve. All 16 exact controls and
2,104 total assertions pass. The 64 scheduled archived clouds remain visible;
58 have complete supports and six remain unavailable. The original 28-cloud
test block reproduces operator RMSE 1.446311 with reconstructed geometry and
0.063032 with simulator geometry. The signed MSE cross term is retained.

The implementation imports no X6 solver or field evaluator. It still receives
the archived true and reconstructed coordinates; it does not independently
reimplement the sprinkling generator or the intrinsic reconstruction pipeline.
There are **no new clouds, no new fields, no prospective statistical
confirmation, no qualified correction, and no additional proper-time or 4D
qualification**. High numerical precision does not remove input errors.
Existing scientific HOLD decisions remain in force.

The next statistical step is a separately frozen planning/confirmation design
with new clouds and fields. This publication does not retroactively classify
the archived data as an untouched confirmation set.

SPDX-License-Identifier: Apache-2.0
