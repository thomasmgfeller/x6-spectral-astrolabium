# Eigenzeit v0.5 · Unabhängige Kalibrierung der Beprobungsdichte

Die Krümmungsregel aus v0.4 setzt voraus, dass das Verhältnis der höchsten zur niedrigsten wissenschaftlichen Beprobungsdichte pro physischem Vierervolumen höchstens **1,002** beträgt. Zwei vorab wählbare Referenzmessungen prüfen diese Voraussetzung für den vollständigen vierdimensionalen Kausaldiamanten. Ist der Kontrast tatsächlich größer, beträgt die Fehlfreigabe unter den dokumentierten externen Annahmen bei jeder Route höchstens **1 %**. [Forschungsbericht (PDF)](Eigenzeit_Kalibrierung_v0_5.pdf) · [Herleitung](BEWEIS.md) · [Code, Rohzählungen und Beispiele (ZIP)](Eigenzeit_Kalibrierung_v0_5_Pruefpaket.zip)

| Kalibrierung in 16 Zellen | Versuche pro Zelle | Hinreichendes Gesamtbudget | Bedingungen für mindestens 99,7 % Freigabe |
|---|---:|---:|---|
| Hohe Nachweisrate | 23.162 | 370.592 | Alle Zellen haben mindestens 99,95 % Nachweiswahrscheinlichkeit. |
| Relative Nachweisrate | 65.000.000 | 1.040.000.000 | Das Minimum beträgt mindestens 49 %, das Verhältnis der Zellmittel höchstens 1,0002. |

Für beide Regeln werden unabhängige Referenzversuche, die Erfassung aller Ausfälle und externe Kontrastgrenzen für Erzeugungsdichte, Drift und Effizienzschwankungen innerhalb jeder Zelle vorausgesetzt. Für jeden dieser drei Faktoren wurde höchstens 1,0001 angesetzt. Ein homogenes Referenzsignal mit 50 % Nachweiswahrscheinlichkeit liefert dieselben Zellzählungen wie eine Anlage mit 25 % und 75 % in gleichwahrscheinlichen Unterzellen. Bei mittlerer Effizienz sind für die untersuchten Fehlerziele und feste Zellbudgets mindestens 60.032.864 Referenzversuche notwendig. [Zertifikat](certificate.json)

**Feldstatus HOLD.** Es liegen keine realen Referenzdaten und keine unabhängigen Belege für die drei Grenzen vor. Bei HOLD gibt die Auswertung alle drei Rastermodelle und das volle Krümmungsintervall zurück. Bei GO greift die Regel aus v0.4 für 3.200.000 wissenschaftliche Ereignisse. Über alle Wiederholungen einschließlich HOLD beträgt die modellweite Überdeckung mindestens 95,1569 %. In der jeweils günstigen Klasse liegt die Wahrscheinlichkeit der richtigen Einzelausgabe für jeden Rasterpunkt über 80 %. [Leeres Feldprotokoll](field_no_evidence.json) · [Synthetischer Pilot](pilot.json) · [Prüfergebnis](verification.json) · [Vorstudie v0.4](../density_contrast_v0_4/README.md)

Die Folgestudie v0.6 senkt das hinreichende Budget der relativen Route bei identischen Fehlerzielen von 1,04 Milliarden auf 752 Millionen Referenzversuche. [Budgetgrenzen, Beweis und gepaarter Kontrolllauf](../relative_calibration_v0_6/README.md)

## Reproduktion

Im Wurzelverzeichnis des Repositorys mit Python 3.12 und den festgelegten NumPy- und SciPy-Versionen ausführen.

```sh
python -m pip install -r tools/workflow/requirements-research.txt
python -B research/eigenzeit/calibration_v0_5/publication_check.py --replay
```

Der Befehl prüft PDF, ZIP, die beiden internen Prüfsummenlisten und die separat verlinkten Dateien. Anschließend berechnet er das Zertifikat und die unabhängigen Kontrollen neu und reproduziert die Rohzählungen aus den festgelegten Seeds. Das ZIP enthält sieben eigenständig simulierte Szenarien und eine gekoppelte Gegenkontrolle mit jeweils 20.000 Wiederholungen. Die Anleitung zur Anwendung auf eigene Daten befindet sich in der README des ZIP. [Veröffentlichungsnachweis](PUBLICATION.json)
