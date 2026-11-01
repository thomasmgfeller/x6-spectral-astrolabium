# Eigenzeit v0.10 · Wie viel Drift verträgt die Kalibrierung?

Die Studie untersucht, wann markierte Referenzzählungen in 16 Zellen ausreichen, um die anschließende Krümmungsschätzung im vollständigen vierdimensionalen Kausaldiamanten freizugeben. Für den neuen Messplan darf ein gemeinsamer Verstärkungsfaktor zwischen 0,99 und 1,01 variieren. Die bedingte Trefferwahrscheinlichkeit jeder Zelle darf pro Versuch um höchstens 20 ppm (0,002 Prozentpunkte) vom skalierten Zielwert abweichen. Beide Grenzen müssen unabhängig belegt sein. [Bericht (PDF)](Eigenzeit_Driftreserve_v0_10.pdf) · [Herleitung](BEWEIS.md) · [Prüfpaket mit Code und Rohzählungen (ZIP)](Eigenzeit_Driftreserve_v0_10_Pruefpaket.zip)

| Größe im 20-ppm-Modell | Zertifizierte Grenze |
|---|---:|
| Kumulierte Versuche je noch aktiver Zelle | 29, 41 und 61 Millionen |
| Erste Stufe / Höchstaufwand über alle 16 Zellen | 464 / 976 Millionen |
| Erwarteter Aufwand für jedes günstige Zielprofil | höchstens 546.942.262 |
| Wahrscheinlichkeit einer Freigabe bei zu großem physischem Kontrast | höchstens 0,93601 % |
| Überdeckung des Krümmungsintervalls über alle abgeschlossenen Durchläufe einschließlich HOLD | mindestens 95,15 % |

Die günstige Klasse umfasst Ziele mit mindestens 49 % Nachweiswahrscheinlichkeit in jeder Zelle und einem Verhältnis zwischen größtem und kleinstem Zellmittel von höchstens 1,0002. Bei günstigen Zielen auf dem untersuchten Krümmungsraster liefert das Verfahren mit mindestens 80,15 % Wahrscheinlichkeit ausschließlich den richtigen Rasterwert. [Zertifikat](certificate.json)

**Grenze der Unterscheidbarkeit.** Bei ungefähr 169,56 ppm liegt im Zählmodell die Schwelle für eine gleichmäßige endliche Trennung günstiger und physisch unsicherer Ziele. Bei 180 ppm geben zwei explizit konstruierte Ziele für jede mögliche Folge von Referenzzählungen dieselbe Wahrscheinlichkeit. Weitere Zählungen können sie deshalb auch bei adaptiver Zellwahl nicht unterscheiden. [Beweis, Abschnitt 5](BEWEIS.md) · [Feldbeispiel mit 180 ppm](unsupported_180ppm.json)

**Synthetischer Stresstest.** Im vorab festgelegten Szenario verdeckt ein gegenläufiger Zellfehler von 20 ppm einen zu großen Zielkontrast. Auf denselben 60.000 unabhängig vom Pilot erzeugten Wiederholungen gab v0.9 in 992 Fällen und v0.10 in 356 Fällen fälschlich frei. Der getrennte Pilot umfasst acht Profile mit je 8.000 Auswertungen. Zwei der Profile verwenden absichtlich dieselben Zählungen. [Stresstest](focus.json) · [Pilot](pilot.json) · [Vorstudie v0.9](../three_look_followup_v0_9/README.md)

**Für reale Messungen gilt HOLD.** Es fehlen markierte Referenzzählungen und unabhängige Nachweise für die Modellannahmen, insbesondere für die Restabweichung von höchstens 20 ppm je Zelle und Versuch. Die synthetischen GO- und HOLD-Beispiele zeigen, welche Krümmungswerte bei identischem Wissenschaftszähler nach der letzten Nachmessung zulässig sind. [Feldvorlage](field_worksheet.json) · [Beispiel GO](final_go.json) · [Beispiel HOLD](final_hold.json)

## Reproduktion

Im Wurzelverzeichnis des Repositorys mit Python 3.12 ausführen.

```sh
python -m pip install -r tools/workflow/requirements-research.txt
python -B research/eigenzeit/drift_reserve_v0_10/publication_check.py --replay
```

Der Prüflauf vergleicht Bericht, Archiv, beide Prüfsummenlisten und alle 56 aus v0.9 übernommenen Dateien. Er berechnet das Zertifikat und die unabhängigen Kontrollen neu, reproduziert die sieben Zählmatrizen des Piloten und erzeugt die zwölf Batches des Stresstests aus ihren Seeds. Alle vier Ergebnisprotokolle werden byteweise mit der veröffentlichten Fassung verglichen. [Unabhängige Kontrollen](verification.json) · [Veröffentlichungsnachweis](PUBLICATION.json)

Die Folgestudie prüft die 20-ppm-Bedingung anhand gepaarter Referenzmessungen und zeigt, wann ein gemeinsamer Fehler beider Kanäle unentdeckt bleibt. [Referenzaudit v0.11 mit Feldprotokoll](../reference_audit_v0_11/README.md)
