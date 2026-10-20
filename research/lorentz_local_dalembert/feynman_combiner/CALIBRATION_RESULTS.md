# Unabhängiger Operator-/Fusionspilot — 20. Oktober 2026

**Entscheid: CALIBRATION_HOLD; HOLD_PHASE3.**

Öffentlicher computational Freeze vor den neuen Wolken: `315d7c31507a852edc84b9e52dece561c81c72b3`.
32 Kalibrierwolken und 32 getrennte Testwolken bei rho=32768. Die Läufe wurden parallel berechnet; die Testauswertung erfolgte erst nach dem Einfrieren der aus Kalibrierdaten bestimmten Parameter. Keine Testdatenanpassung.

## Verfügbarkeit und Budget

| Split | Physische Wolken | Laufzeit (s) | Peak-RSS (MiB) | Status |
|---|---:|---:|---:|---|
| calibration | 32 | 1129.8 | 1381.4 | COMPLETE |
| test | 32 | 1199.9 | 1376.1 | COMPLETE |

Auswertbar: Kalibrierung 31/32, Test 30/32. Nicht verfügbare Wolken bleiben im Verfügbarkeitsnenner. Genauigkeitswerte gelten nur für vollständige, zuvor bewachte Fälle.

## Festgelegter Vergleich

Drei Operatorantworten derselben Wolke und desselben verrauschten Feldes: übertragene Basis, unbeschränkte L1-Gewichte, unbeschränkte Varianzgewichte. Die Vorzeichenbeschränkung wird separat geprüft. Das Testfeld lautet exp(t/2) cos(x/2) cos(y/2) relativ zum Root; sein wahrer Operatorwert ist -0.75. Keine räumliche Einbettung wird hier durch den Filter korrigiert.

Eine synthetische unabhängige Prädiktion mit Standardabweichung 0.5 wird pro Testwolke für alle Filterarme gemeinsam verwendet. Die Kalman-Anbindung ist daher ein Ein-Schritt-Vergleich mit explizit C=0, kein nachgewiesenes Bewegungsmodell.

| Filterarm | Mess-RMSE nach Bias-Korrektur | Posterior-RMSE | 95%-Abdeckung | Exaktes 95%-Intervall der Abdeckungsquote |
|---|---:|---:|---:|---|
| single | 1.310699 | 0.495234 | 93.33% | 77.9–99.2% |
| joint | 1.273731 | 0.492552 | 93.33% | 77.9–99.2% |
| naive_diagonal | 1.582393 | 0.568203 | 90.00% | 73.5–97.9% |

Gepaarter Posterior-RMSE-Quotient joint/single: **0.994584**; 95%-Bootstrapintervall 0.937345–1.052571. Vorab gefordert: <=0.95. Das Bootstrapintervall konditioniert auf die eingefrorene Kalibrierung.

### Eingefrorene Kalibrierung

Ausgewählter Einzelarm (Index 0/1/2): 2. Gemeinsame Fusionsgewichte: [0.08438483807632094, 0.0, 0.9156151619236799]. Kovarianzkondition: 83.5.

| Arm | Geschätzter Bias | Roh-RMSE Test | Fehler-RMSE ohne Feldrauschen |
|---|---:|---:|---:|
| Basis | -1.529922 | 4.342581 | 4.484861 |
| L1 | -0.208447 | 2.402290 | 0.893588 |
| Varianz-QP | -0.015267 | 1.307129 | 0.879317 |

Gemeinsame Fehlerkovarianz aus Kalibrierwolken (vor dem Faktor 1+1/n für Bias-Mittelschätzung):

| | Basis | L1 | Varianz-QP |
|---|---:|---:|---:|
| Basis | 12.7205 | 0.668746 | -0.0620916 |
| L1 | 0.668746 | 2.17817 | 1.38077 |
| Varianz-QP | -0.0620916 | 1.38077 | 1.11598 |

Korrelationen derselben Fehler:

| | Basis | L1 | Varianz-QP |
|---|---:|---:|---:|
| Basis | 1.0000 | 0.1270 | -0.0165 |
| L1 | 0.1270 | 1.0000 | 0.8856 |
| Varianz-QP | -0.0165 | 0.8856 | 1.0000 |

Vorzeichenbeschränktes QP mit geprüftem Zertifikat auf den vollständigen Testfällen: 23/30.

| Vorab festgelegtes Kriterium | Ergebnis |
|---|---|
| execution_complete | PASS |
| availability | PASS |
| rmse_improvement | FAIL |
| coverage | PASS |

## Ergänzende Unsicherheitsdiagnose

Die bedingte Feldrauschvarianz des Varianz-QP ist stark wolkenabhängig. Der eingefrorene Pilot verwendete eine gemeinsame empirische Kovarianz; die folgende Diagnose ändert diese Auswertung nicht.

| Split | Minimum | Median | Maximum |
|---|---:|---:|---:|
| calibration | 0.200970 | 0.668375 | 7.840072 |
| test | 0.152566 | 0.561800 | 50.046060 |

Der Extremfall bleibt vollständig enthalten. Für einen Folgeversuch ist die bekannte wolkenabhängige Feldrauschkovarianz separat von der noch zu kalibrierenden Geometrieunsicherheit zu behandeln. Aus einer globalen mittleren Kovarianz folgt keine gleich gute Unsicherheitsbeschreibung jeder einzelnen Wolke.

## Nachprüfung und Kausalität

64 archivierte Wolken, 122 LP-Zertifikate, 103 QP-Zertifikate und 5684 verwendete Intervalle nachgeprüft. Alle regenerierten Koordinaten-Hashes und Feld-/Rauschantworten stimmen überein. Die vollständige teure Rahmensuche wurde in dieser Nachprüfung nicht erneut ausgeführt.

Ergänzende, nicht als primäres Abnahmekriterium registrierte Relationsdiagnose: 55/64 ausgewählte rekonstruierte Punktmengen haben mindestens eine fehlende oder zusätzliche gerichtete Relation. Insgesamt fehlen 62 Relationen; 74 werden zusätzlich vorhergesagt. Geprüft werden Root und Stützpunkte, nach Orientierung der rekonstruierten Zeitachse am markierten Zukunftspunkt. Es erfolgt keine lautlose Reparatur.

Die Relationsdiagnose umfasst 30494 gerichtete Nichtdiagonalpaare, davon 8632 wahre Relationen. Eine Wolke mit mindestens einem Fehlpaar ist nicht gleichbedeutend mit einer überwiegend falschen Rekonstruktion.

Alle zum Zählen verwendeten Intervalle sind im Simulator kausal. Das garantiert nicht, dass die rekonstruierten Koordinaten alle Paarrelationen erhalten. Die Stützen verwenden auch Zukunftsdaten; dieser Pilot ist offline. Eine Online-Ausgabe braucht eine deklarierte Verzögerung oder eine neu validierte vergangenheitsbasierte Konstruktion.

## Geltungsgrenzen

- Minimierte bedingte Feldrauschvarianz enthält keine Garantie über Geometriefehler. Gemeinsamer Bias kann trotz kleiner Streuung bestehen.
- Bias und Kovarianz sind an genau diese Dichte, Auswahlregel und Testfeldverteilung gebunden. Unabhängige neue Felder und andere Skalen sind noch zu prüfen.
- Die empirische Kovarianz und nominellen Gaussian-Intervalle sind keine garantierten Fehlergrenzen. Die kleine Testzahl erlaubt nur breite Abdeckungsintervalle.
- Die ursprüngliche naive Unabhängigkeits-Negativkontrolle und die hier diagonalisierte kalibrierte Kovarianz sind unterschiedliche Versuche.
- Keine validierte Einbettungskovarianz, keine sequenzielle Filtervalidierung, kein Neuheits-/Krümmungsnachweis. HOLD_PHASE3 bleibt bestehen.

## Reproduktion

Die vollständigen Einzelwolken liegen in `independent_clouds.zip` samt SHA256-Manifest. Im Modulordner entpacken, danach vom Repository-Root:

```sh
python -m zipfile -e research/lorentz_local_dalembert/feynman_combiner/independent_clouds.zip research/lorentz_local_dalembert/feynman_combiner
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/feynman_combiner/verify_calibration.py
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/feynman_combiner/analyze_calibration.py test
```

Für eine vollständige Neuberechnung in einem separaten Checkout ohne entpackte Ergebnisordner `run_calibration.py --split calibration`, dann `analyze_calibration.py fit`, dann `run_calibration.py --split test` und `analyze_calibration.py test` verwenden. Bestehende Ergebnisordner werden nicht überschrieben.
