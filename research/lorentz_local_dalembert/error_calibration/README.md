# Getrennte Kalibrierung von Geometriefehler und Messunsicherheit

Vorab veröffentlichter Versuch auf dem Forschungszweig von PR #69.
Neue Zielwolken noch nicht ausgeführt. [Protokoll](PROTOCOL.md) und
[maschinenlesbarer Vertrag](contract.json) trennen systematischen
Operatorfehler, Wolkenstreuung und bedingte Feldrauschkovarianz.

Die vier bestehenden Varianten bleiben unverändert. Geplant sind 32 neue
Kalibrierwolken, ein öffentlicher Kalibrierfreeze und 32 neue Testwolken;
jeweils vier neue analytische Felder und 512 Rauschwiederholungen.
HOLD_PHASE3 und HOLD_EMBEDDING_COVARIANCE bleiben bestehen.

Originalcode: Apache-2.0. Dies ist synthetische Kalibrierung im flachen
2+1-Modell, kein Instrumenten- oder Krümmungsnachweis.
