# Durchgeführte Prüfungen und offene Laborbelege

35 neue Python-Prüffälle bestehen. Zusätzlich bestanden die unveränderten
C1-Prüfungen mit 27 C++-Fällen und 18 Python-/PTY-Fällen, einschließlich des
unabhängig geprüften C1-Ende-zu-Ende-Laufs und seiner Manipulationskontrollen.
Die 35 Fälle enthalten mehrere Parametervarianten; diese werden nicht als
zusätzliche unabhängige Experimente gezählt.

**Frischer Checkout bestanden:** Commit `509c994`, zwölf von zwölf Schritten,
isolierte Python-3.12-Umgebung, zusätzlich alle zwölf bestehenden
Integrationsregressionen. Sämtliche getrackten Dateien blieben unverändert.
Maßgeblicher Lauf: `evidence/fresh-checkout/fresh-checkout.json` mit allen
zugehörigen Logs und Ergebnissen. Insgesamt 35 + 27 + 18 + 12 bestandene
Testfälle; dies sind Softwaretests, keine 92 physischen Versuche.

## V01–V10

| ID | Ausführung / reproduzierbarer Gegenfall | Status |
|---|---|---|
| V01 | NaN, ±Inf, boolesche Zahlen, falsche Einheiten und ungültige Werte; Ablehnung vor Stellbefehl | MODEL_PASS |
| V02 | 0↔2π, −10⁻⁸ rad nahe Null, Nullamplitude → undefiniert; Toleranz 10⁻¹² rad | MODEL_PASS |
| V03 | Nichtperiodischer symmetrischer Puls um 3 Samples verzögert; Rohfehler sichtbar, erlaubte Ausrichtung berichtet +3 | MODEL_PASS |
| V04 | Komplexe Töne +70 und −110 Hz, analytische Leistungen 4 und 0.25; zweiseitige DFT/Parseval | MODEL_PASS |
| V05 | Sample 300 verändert, danach sogar neu gehasht; abgeschnittene/verlängerte Datei, Modell als Hardware umetikettiert, ZIP-Pfadmanipulation | MODEL_PASS |
| V06 | Zeitüberlauf, falsche Reihenfolge, 4096 Samples vollständig, 4097 abgewiesen; C1-Puffer separat | MODEL_PASS |
| V07 | START-Duplikat, falsche Run-ID, Disconnect und Clock-valid-Verlust im D01-Modell; fehlender Tick verwirft Lauf | MODEL_PASS |
| V08 | Tatsächliche Zeitstempel verändern zeitabhängiges Signal; ±300 ppm, Jitter 0/200 µs, ungestörter Grenzfall | MODEL_PASS |
| V09 | Auswerter mit synthetischem Gut-/Fehlfall geprüft; 100-mV-Fehler wird nicht durch Fit entfernt | **Physische Messung NOT_PERFORMED** |
| V10 | Auswerter mit getrennten Läufen, unverändertem Kalibrierfit bei beschädigten Prüfdaten, Leak-/Extrapolationskontrollen geprüft | **Physische Messung NOT_PERFORMED** |

V01–V08 beziehen sich auf den spezifizierten Software-Referenzbereich, nicht auf
FPGA-/Pico-Echtzeitbetrieb. `tests/acvm/test_acvm.py` enthält die prüfbaren
Erwartungen. `qualification.json` führt die physischen Sperren separat auf;
ein synthetischer V09/V10-Gutfall ändert diese nicht.

## Optik und Geräteprotokolle

Analytische QHQ-Relativephase und verschwindende idealisierte Kreuzterme,
HWP-Faktor zwei, Achskalibrierung, ungeeignete Retardanz, HWP-Nullfit trotz
Quellenintensitätsdrift, unidentifizierbare Scans, monotone Kennlinien und
Extrapolationsverbot sind geprüft. ELL14-Befehl `0ma000057E4` wird gegen die
unabhängig festgelegte Testskala 1000 Impulse/Grad für 22.5° geprüft.

Eine echte POSIX-PTY-Verbindung transportiert fragmentierte ASCII-Antworten.
Falsche Seriennummer/Adresse/Modell, BUSY, Gerätefehler, verlorene Antwort und
falsche gemeldete Stellung führen zu den vorgesehenen Ergebnissen. PM100D-
Tests injizieren falsche Einheit, Sensor-ID, Wellenlänge, Fehlerqueue und
Überlaufwerte. Das prüft den Adapter, keinen realen ELL14/PM100D.

## Gleich budgetierter Regelvergleich

Kalibrierlauf `cal-17` enthält eigene synthetische Kalibrierpunkte. Der daraus
bestimmte Startstellwert ist für festen Stellwert und Regelung identisch.
PI-Gewinne sind vor den fünf Prüfläufen eingefroren. Jeder Prüflauf verwendet
für beide Verfahren dieselben Drift- und Rauschwerte und je **160 Messungen**.
Alle Werte einschließlich Anlauf bleiben in `feedback-benchmark.json` erhalten;
das vorab festgelegte Auswertefenster ist Index 40 bis 159.

| Prüflauf | RMSE fester Stellwert | RMSE Regelung |
|---|---:|---:|
| 101 | 0.0567112 | 0.0043663 |
| 102 | 0.0565313 | 0.0042450 |
| 103 | 0.0567207 | 0.0043705 |
| 104 | 0.0567727 | 0.0042561 |
| 105 | 0.0566229 | 0.0042720 |

Einheit: normierte Modellleistung. In allen fünf Läufen liegt der Regel-RMSE
unter der vorgegebenen Hälfte des Vergleichsfehlers. Das Modell nimmt eine
sofortige normierte Stellwirkung an; echte Motorlaufzeiten, Hysterese,
Sensordynamik und mechanische Drift sind damit nicht nachgewiesen. Es werden
weder ein Konfidenzintervall aus abhängigen Samples noch eine Übertragbarkeit
auf einen realen Sagnac-Aufbau behauptet.

## Reproduktion und Umfang

`python3 tests/acvm/qualify_checkout.py --output /absoluter/neuer/pfad`
fordert einen sauberen Checkout ohne `.venv`. Es erstellt eine isolierte
Umgebung mit `x6.py setup --profile core` und führt zwölf Schritte einschließlich Qualifikation, Export/Import,
Messauswertern, Vorlagenverweigerung, bestehenden Integrationsregressionen und
Quellinventar aus. Protokoll und Quellcommit stehen im beigefügten Nachweis.
Die ersten Checkout-Versuche deckten einen Interpreterfehler im neuen Prüfskript
auf: Die Umgebung existierte, direkte Integrationsregressionen liefen aber noch
unter dem Basis-Python. Der Ablauf verwendet jetzt den offiziellen Setup-Pfad
und danach ausdrücklich `.venv/bin/python`. Beide Fehlversuche bleiben erhalten.

Nicht ausgeführt: realer Motorlauf, PM100D-USB/VISA-Verbindung, automatisierter
Kalibrierscan, Pico-SDK-Zielbuild, unabhängige elektrische Aufnahme, optischer
Regelversuch, FPGA-Synthese/Timingabschluss und schneller photonischer Feed-forward.
Die konkrete verbleibende Laborarbeit steht in [CALIBRATION](CALIBRATION.md).
