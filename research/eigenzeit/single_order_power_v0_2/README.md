# Eigenzeit v0.2 · Trennleistung aus einer Einzelordnung

Eine unbeschriftete Kausalordnung mit **30.000 Ereignissen** genügt, um einen flachen 4D-Diamanten vom de-Sitter-Modell mit h = 1/2 und RT² ≈ 3,131 zu unterscheiden. Die Ereignisse müssen bei fester Anzahl unabhängig und gleichmäßig nach physischem Volumen im vollständigen Diamanten gezogen werden.

[Forschungsbericht (PDF)](Eigenzeit_Trennleistung_Einzelordnung_v0_2.pdf) · [Herleitung](package/BEWEIS.md) · [Vollständiges Prüfpaket (ZIP)](Eigenzeit_Trennleistung_Einzelordnung_v0_2_Pruefpaket.zip)

| Wahre Geometrie | Risiko, sie zu verwerfen | Wahrscheinlichkeit, die andere zu verwerfen |
|---|---:|---:|
| Minkowski | höchstens 4,73 % | mindestens 80,30 % |
| de Sitter mit h = 1/2 | höchstens 4,89 % | mindestens 80,71 % |

Die Regel zählt die vergleichbaren Paare der transitiven Ordnung. Im Zwischenbereich bleiben beide Modelle zulässig. Für das Ziel von 80 % Trennleistung bei höchstens 5 % Fehlalarm sind mindestens 9.857 Ereignisse notwendig. Wo zwischen 9.857 und 30.000 das Minimum liegt, ist offen. Eine zweite Regel verarbeitet 48.000 disjunkte, unabhängig von den Daten gepaarte Abfragen aus einer Ordnung mit 96.000 Ereignissen.

Die Garantien folgen aus der endlichen Wahrscheinlichkeitsrechnung. Die vier vorab festgelegten Einzelbeispiele kontrollieren die Implementierung. Eine unabhängige empirische Bestimmung der Leistung und Aussagen für andere Krümmungen bleiben offen. [Zertifikat](package/certificate.json) · [Entscheidungsregel](package/decision.py) · [Vier Einzelbeispiele](package/examples.json) · [Vorstudie mit 128 Ereignissen](../single_order_128_v0_1/README.md)

## Reproduktion

Vom Wurzelverzeichnis des Repositorys aus:

```sh
python3 research/eigenzeit/single_order_power_v0_2/publication_check.py
python3 research/eigenzeit/single_order_power_v0_2/publication_check.py --replay
```

Der erste Befehl prüft die vollständigen Originaldateien, die beiden Prüfsummenverzeichnisse und die einzeln zugänglichen Paketdateien. Der zweite berechnet das Zertifikat, die Gegenkontrollen und alle vier Beispiele erneut. Er erfordert Python 3.12, NumPy, SciPy und einen C++17-Compiler. [Umgebung](package/environment.json) · [Abhängigkeiten](../../../tools/workflow/requirements-research.txt) · [Nutzung mit eigenen Ordnungen](package/README.md) · [Veröffentlichungsnachweis](PUBLICATION.json)
