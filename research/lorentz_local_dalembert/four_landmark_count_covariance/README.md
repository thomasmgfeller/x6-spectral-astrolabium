# Eigenzeit: vier Landmarken und vollständige Zählkovarianz

**21.10.2026 — Neue Wolken vollständig geprüft. Wissenschaftlicher Status: HOLD.**

[Vollständiges unverändertes Prüfpaket herunterladen](Eigenzeit_Vier_Landmarken_Neue_Wolken_2026-10-21.zip) ·
[Ergebnisbericht (Deutsch)](evidence/Ergebnisbericht.txt) ·
[Maschinenlesbare Auswertung](evidence/analysis.json) ·
[Vorab festgelegtes Protokoll](evidence/PROTOCOL.txt) ·
[Alle Daten](evidence/results/)

Die vorausgehende [intrinsische Korrekturentwicklung V1/V2](../intrinsic_correction_development/README.md)
ist jetzt vollständig archiviert: verworfener V1-Kandidat, Herleitung des
Vier-Landmarken-Operators und damalige exakte Sage-Kontrollen. Die dortigen
`NOT_RUN`-Angaben beziehen sich auf den Stand vor dieser neuen Wolkenprüfung.

## Ergebnis

Die vierte Landmarke wird aus kausaler Ordnung, Intervallzählungen,
unabhängigen Markierungen, Signatur und Kondition auf einer Auswahlwolke A
bestimmt. Die ersten drei Landmarken und der Support stammen aus dem bisherigen
intrinsischen Selektor. Wahre Koordinaten und Auswertungsfelder sind bei der
Landmarkenauswahl nicht verfügbar. Nach versiegelter Auswahl liefern getrennte
Poisson-Wolken B die Zählungen und Intervallschnittmengen.

- **32 neue unabhängige Auswahlwolken**, davon 18 erfolgreiche Auswahlen.
  Drei alte Support-/Frame-Audits scheitern; elf weitere Fälle finden keine
  vierte Landmarke im festgelegten Budget. Keine Ersatzwolken.
- **162 tatsächlich ausgeführte Zählwiederholungen:** neun B-Wolken für jede
  erfolgreiche Auswahl. B0 ist der Hauptfall; B1–B8 prüfen die Streuung.
- **17 rechnerisch gültige Hauptsysteme, nur 1/32 geometrisch qualifiziert.**
  Die übrigen gültigen Hauptsysteme verletzen je ein bis vier beobachtete
  gerichtete Beziehungen. Rechnerische Gültigkeit ersetzt diese Prüfung nicht.
- **13 gemeinsam berechenbare Diagnosefälle:** Operator-RMSE Drei/Vier
  Landmarken **2,007005 / 2,533344**, jeweils auf derselben B0-Wolke und demselben
  A-Support. Die Verbesserungsschwelle wird verfehlt. Das deskriptive gepaarte
  95%-Bootstrapintervall des Verhältnisses ist breit: **0,645927–2,214611**.
  Weder eine allgemeine Verbesserung noch eine allgemeine Verschlechterung
  ist damit statistisch etabliert.

## Zählkorrelationen

Bei fester Auswahl A gilt für überlappende Poisson-Zählintervalle
`Cov(N_e,N_f | A) = rho_B Vol(I_e ∩ I_f)`. Die Schnittmengenzählungen schätzen
diese gemeinsame Kovarianz. Die Delta-Methode propagiert sie durch die
Abstandstransformation und die Ableitung des gesamten KKT-Systems, einschließlich
Momentmatrix und Zielmetrik, bis zur Kovarianz der Operatorgewichte.
Die Kovarianz wird zur Unsicherheitsvorhersage verwendet; eine neue
kovarianzoptimierte Gewichtspolitik wird hier nicht behauptet.

| Mittlere Antwortvarianz auf 13 vollständigen A-Gruppen | Wert |
| --- | ---: |
| Empirisch aus acht unabhängigen B-Wiederholungen | 4,920742 |
| Vorhersage aus B0 mit voller Zählkovarianz | 4,456599 |
| Negativkontrolle ohne Zählkorrelationen | 65,122184 |

Die Übereinstimmung mit voller Kovarianz ist ein **deskriptives Teilergebnis**.
Das vorab fixierte Kalibrierungs-Gate verlangt mindestens 16 vollständige
A-Gruppen; erreicht wurden 13. Die Auswahl vollständiger Fälle kann verzerren.
Die Fortpflanzung ist eine lineare Näherung für die bedingte Streuung, keine
Bias-Korrektur oder Konfidenzgarantie für die Kontinuumsableitung. Vier Felder
und acht Wiederholungen zählen nicht als zusätzliche unabhängige A-Wolken.

## Verifikation und Geltungsbereich

- Vollständiger numerischer Replay: **32 Datensätze, 162 Zählwiederholungen PASS**.
- Separater SageMath-10.9-Prüfer: **alle 17 gültigen Hauptsysteme PASS**;
  Gewichte bei 128/256 Bit, vollständige Kovarianz bei 256 Bit, maximale relative
  Kovarianzabweichung rund **1,11e−11**.
- **Zehn numerische und 15 exakte Sage-Vorprüfungen PASS**.
- **59 vorab eingefrorene Dateien und 55 übernommene Quelldateien unverändert**.
  Der Freeze war lokal vor Datenerzeugung, keine öffentliche Präregistrierung.

Die getrennte Sage-Rechnung prüft die algebraische Gewichts- und
Kovarianzauswertung aus archivierten Zählungen. Sie ist keine unabhängige
Neuentwicklung des Generators oder des Selektors und keine externe Replikation.
Der Pilot betrifft flaches **2+1-Minkowski-Modell**, bekannte Dichte 32768,
äußere Diamantdauer 1,5 und vier unveränderte analytische Felder.

**Gesamtstatus HOLD. `HOLD_PHASE3`, `HOLD_EMBEDDING_COVARIANCE` und
`METADATA_HOLD` bleiben bestehen.** Keine Krümmungs-, 3+1-, Kalman- oder
physikalische Sensorqualifikation. Der Fehlschlag betrifft diese konkrete
Pipeline; die exakten Vier-Landmarken-Identitäten sind damit nicht widerlegt.

## Herkunft und Reproduktion

Die unveränderten benötigten Quellen liegen in [evidence/vendor](evidence/vendor/).
[Quellbindungen](evidence/vendor_sources.json) beziehen sich auf
[`ee6460971c2b3ec48ea2ebb18002072ca3d22f97`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/ee6460971c2b3ec48ea2ebb18002072ca3d22f97).
[freeze.json](evidence/freeze.json) bindet den prospektiven Versuchsstand;
[completion_manifest.json](evidence/completion_manifest.json) unterscheidet
später ergänzte Prüf-/Berichtsdateien. [publication.json](publication.json)
bindet die Veröffentlichung an das unveränderte ZIP und dessen 141 Dateien.
Der vorausgehende [retrospektive Sage-Audit](../../lorentz_sage_reconstruction_audit/README.md)
bleibt als eigene Untersuchung erhalten.

In einer separaten Arbeitskopie von `evidence`, mit Python, NumPy und SciPy:

```sh
cd research/lorentz_local_dalembert/four_landmark_count_covariance/evidence
sha256sum -c SHA256SUMS.txt
OPENBLAS_NUM_THREADS=1 python3 verify_records.py
OPENBLAS_NUM_THREADS=1 python3 analyze.py
OPENBLAS_NUM_THREADS=1 python3 controls.py
```

Die Programme schreiben ihre Ergebnisdateien neu. Produktionsversionen:
Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0. Für die unabhängige Gegenrechnung
in einer aktivierten SageMath-10.9-Python-Umgebung:

```sh
python exact_geometry_sage.py
python exact_covariance_sage.py
python verify_sage.py
```

Die [fixierte Linux-64-Conda-Umgebung](evidence/environment-explicit-sage.txt)
und [vollständigen Ausführungsanweisungen](evidence/README.txt) sind enthalten.
Eine vollständige Neugenerierung benötigt eine separate Kopie ohne `results/`;
vorhandene Versuchsdaten werden nicht überschrieben. SHA-256 des ZIP:

```text
2aa0bf345f1522444b8268adca0276693827cb6de8d1ded2c8c61d30bd9941e0
```

## English scope

This prospective, locally frozen 2+1 flat-space pilot adds an intrinsic fourth
landmark and propagates full overlapping-count covariance through the complete
KKT weight solve. All 32 new selection clouds are recorded; 18 admit a fourth
landmark and receive nine independent count clouds each (162 completed count
replicates). Only **1/32 primary cases** meets the full observed-order check.
On 13 common computable diagnostic cases, four-landmark operator RMSE is 2.533344
versus 2.007005 for the three-landmark baseline on the same B0 count cloud.

In 13 complete replicate groups, observed response variance is 4.920742;
full-covariance prediction is 4.456599 and the diagonal-count negative control
is 65.122184. This is descriptive: at least 16 complete groups were required.
Repeated counts and four fields do not increase the number of independent
selection clouds. First-order propagation does not remove systematic bias.

All 162 count records replay; a separately formulated Sage implementation
confirms weights and covariance for all 17 valid primary systems. Computational
checks pass, while the scientific decision remains **HOLD**. There is no
qualified geometry correction, curved-space/3+1 transfer, Kalman validation or
physical sensor claim. Sources, controls, failures and original logs are retained.

SPDX-License-Identifier: Apache-2.0
