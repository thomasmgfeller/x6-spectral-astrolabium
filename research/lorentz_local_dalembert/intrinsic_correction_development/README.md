# Eigenzeit: Entwicklung der intrinsischen Korrektur (V1/V2)

**Historischer Entwicklungsstand vom 21.10.2026. V1 verworfen; V2 damals nur
bei exakten Intervalllängen geprüft. Keine wissenschaftliche Freigabe.**

[Vollständiges ursprüngliches Prüfpaket](Eigenzeit_Intrinsische_Korrektur_2026-10-21.zip) ·
[Ergebnisbericht und Herleitung](evidence/Ergebnisbericht.txt) ·
[V1-Korrekturcode](evidence/intrinsic_correction.py) ·
[V2-Vier-Landmarken-Operator](evidence/four_landmark_operator.py) ·
[Sage-Beweisprüfungen](evidence/exact_four_landmarks_sage.py)

## Einordnung in die veröffentlichte Entwicklung

Dieses Paket liegt zeitlich **vor** der bereits veröffentlichten
[Vier-Landmarken-Prüfung auf neuen Wolken](../four_landmark_count_covariance/README.md)
aus [PR #81](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/81).
Die Originaldateien bleiben unverändert. Ihr `NOT_RUN` für verrauschte
V2-Wolken bezeichnet den damaligen Stand, nicht den heutigen Gesamtstatus.
Die Nachfolgestudie führte später 32 neue Auswahlwolken und 162
Zählwiederholungen aus und endete ebenfalls auf **HOLD**.

Die Forschungsfolge ist damit nachvollziehbar: [retrospektiver Sage-Audit](../../lorentz_sage_reconstruction_audit/README.md)
→ dieses Entwicklungspaket → neue Wolken mit intrinsischer vierter Landmarke
und vollständiger Zählkovarianz. Die Veröffentlichung erfolgt nach der
Entwicklung und ist keine nachträgliche öffentliche Präregistrierung.

## V1: geometrisch konsistente Anpassung ohne nachgewiesenen Nutzen

V1 hält die bisherigen drei Landmarken fest und passt die Stützpunkte unter
Schur-/Abstandsbedingungen und den verfügbaren Ordnungsbedingungen an.
Der Korrekturcode verwendet intrinsische Eingaben; wahre Simulatorkoordinaten
und Feldwerte dienen erst nach Versiegelung der Gewichte zur Bewertung.
Die diagonale Verlustgewichtung berücksichtigt die Zählkorrelationen nicht
vollständig und ist keine gemeinsame Likelihood oder Unsicherheitskalibrierung.

Alle **64 archivierten Fälle** sind dokumentiert. Für die **58 zuvor
vollständigen Supports** entstehen rechnerisch akzeptierte Kandidaten; sechs
vorher unverfügbare Fälle bleiben erhalten. Beide alten Gruppen sind hier
bekannte Entwicklungsdaten, keine unberührte statistische Bestätigung.

| Rauschfreier Operator-RMSE | Original | V1 |
| --- | ---: | ---: |
| Alter Kalibrierblock, 30 vollständige Fälle | 2,322140 | 2,519857 |
| Alter Testblock, 28 vollständige Fälle | 1,446311 | 2,592466 |

Die interne geometrische Verlustfunktion verbessert sich, die
Operatorgenauigkeit verschlechtert sich. **V1 wurde für die Übernahme verworfen.**
Eine zulässige Geometrie allein ist kein Nachweis einer nützlichen Korrektur.
Die fehlende vollständige Landmarken-Zeitorientierung und die lokale,
nichtkonvexe Optimierung sind im Originalbericht ausdrücklich begrenzt.

## V2: vier externe Landmarken und exakte Distanzdifferenzen

V2 verwendet vier externe Landmarken, deren drei Differenzvektoren einen
nichtsingulären Frame bilden. Differenzen quadrierter Intervalllängen liefern
bei exakten Eingaben lineare Koordinatenfunktionen. Die zugehörige Metrik wird
aus denselben Landmarkenintervallen bestimmt. Bei vollem Momentenrang und
gleicher Minimum-Varianz-Zielfunktion stimmt der Operator mit der Lösung auf
wahren Koordinaten überein.

**Diese algebraische Aussage gilt für exakte Distanzen.** Sie bestätigt weder
den endlichen Zählfehler noch die Intrinsik einer noch nicht ausgeführten
Landmarkenauswahl. Das alte Archiv hatte nur drei externe Landmarken; deshalb
enthält dieses Paket keinen V2-Wolkentest. Auswahl und Zählkovarianz wurden
in der oben verlinkten Nachfolgestudie eigens implementiert und geprüft.

## Archivierte Kontrollen und Reproduktion

- SageMath 10.9: **11 exakte Geometriekontrollen**, **58 V1-Gewichtssysteme**
  separat bei 128/256 Bit und **10 exakte V2-Kontrollen** bestanden.
- Numerik: **acht V1- und vier V2-Kontrollen** bestanden.
- Der anfängliche Fehler beim Kopieren einer Sage-Negativkontrolle bleibt unter
  [attempts](evidence/attempts/) dokumentiert. Der unveränderte Freeze und das
  [Abschlussmanifest](evidence/completion_manifest.json) machen die Korrektur
  transparent; der Inferenzcode und die Kriterien wurden dadurch nicht verändert.

Die Kontrollen sind archivierte Rechennachweise, keine neuen unabhängigen
physikalischen Beobachtungen. Diese Veröffentlichung wiederholt die
Forschungskampagne nicht. Sie prüft die unveränderte Übernahme des Pakets.

In einer Arbeitskopie des Verzeichnisses `evidence`:

```sh
sha256sum -c SHA256SUMS.txt
OPENBLAS_NUM_THREADS=1 python3 numerical_controls.py
OPENBLAS_NUM_THREADS=1 python3 four_landmark_controls.py
```

In einer aktivierten SageMath-10.9-Python-Umgebung:

```sh
python exact_geometry_sage.py
python exact_four_landmarks_sage.py
python verify_candidate_sage.py
```

[Vollständige Reproduktionsanweisungen](evidence/README.txt),
[fixierte Sage-Umgebung](evidence/environment-explicit-sage.txt),
[Eingabedaten](evidence/intrinsic_inputs.json), getrennte
[Evaluationswahrheiten](evidence/evaluation_inputs.json) und sämtliche
Ergebnisse gehören zum Paket. Die Programme können Ergebnisdateien neu schreiben;
deshalb eine Kopie verwenden. Der V1-Runner überschreibt vorhandene Inferenzdaten
absichtlich nicht. [publication.json](publication.json) bindet die 32
bytegleichen Archivdateien und dieses ZIP:

```text
SHA256  11da8814725409270f9238751ba8f47a69cf245d3335dcce0fe701834b68ff77
```

## English scope

This is the complete historical intrinsic-correction development package,
published after the subsequent fresh-cloud pilot. V1 was evaluated on all
64 archived cases (58 previously complete, six unavailable). It improved its
internal geometry loss but worsened operator RMSE and was rejected for utility.
V2 introduced four external landmarks and passed exact-distance algebraic
controls; its noisy-cloud validation was not run **at the time of this archive**.
The later [fresh-cloud study](../four_landmark_count_covariance/README.md) is
published separately and also remains HOLD. Original files, including historical
`NOT_RUN` labels, failures, inputs and Sage logs, are preserved byte-for-byte.

**`HOLD_PHASE3`, `HOLD_EMBEDDING_COVARIANCE` and `METADATA_HOLD` remain unchanged.**
No curved-space, 3+1, Kalman or physical sensor qualification follows.

SPDX-License-Identifier: Apache-2.0
