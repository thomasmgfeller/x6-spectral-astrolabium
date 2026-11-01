# Eigenzeit v0.2 · Trennleistung aus einer Einzelordnung

Eine unbeschriftete Kausalordnung mit **30.000 Ereignissen** genügt, um einen flachen 4D-Diamanten vom de-Sitter-Modell mit h = 1/2 und RT² ≈ 3,131 zu unterscheiden. Die Ereignisse müssen bei fester Anzahl unabhängig und gleichmäßig nach physischem Volumen im vollständigen Diamanten gezogen werden.

[Forschungsbericht (PDF)](Eigenzeit_Trennleistung_Einzelordnung_v0_2.pdf) · [Herleitung](package/BEWEIS.md) · [Vollständiges Prüfpaket (ZIP)](Eigenzeit_Trennleistung_Einzelordnung_v0_2_Pruefpaket.zip)

[Fortsetzung v0.3 mit drei Geometrien und einem kontinuierlichen Krümmungsintervall](../three_geometries_v0_3/README.md).

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

### Plattformvergleich der vier Beispiele

Der erste GitHub-Lauf reproduzierte das Zertifikat und die Gegenkontrollen bytegenau und scheiterte am Vergleich der Beispieldatei. Der Originalvergleich bleibt mit `--replay` ausführbar. Für die CI fixiert `--replay --cpu-baseline` bei den vier Simulationen den NumPy-Rechenpfad mit deaktiviertem AVX512F. Auch dieser Vergleich verlangt eine exakte Übereinstimmung aller Datenfelder mit dem jeweils festgelegten Referenzwert.

Die beiden lokalen Läufe unterscheiden sich nur in den Koordinatenprüfsummen. Die maximale Änderung einer Koordinatenkomponente beträgt 2⁻⁵². Beide vollständigen Ordnungsprüfsummen, alle Stichproben- und Paarzahlen, Entscheidungen und Paarungsprüfsummen stimmen überein. Für die Zufallspaarungen wurden zusätzlich alle einzelnen Vergleichbarkeiten abgeglichen. [Geprüfte Koordinatenvarianten](cpu_baseline.json) · [Vergleichsskript](portability_audit.py) · [Erster CI-Lauf](https://github.com/thomasmgfeller/x6-spectral-astrolabium/actions/runs/41292453426)

Auf einem Rechner mit dem ursprünglichen NumPy-Rechenpfad lässt sich der Vergleich im Verzeichnis dieser Studie wiederholen:

```sh
python -B portability_audit.py --capture /tmp/x6-v02-native
NPY_DISABLE_CPU_FEATURES=AVX512F python -B portability_audit.py --capture /tmp/x6-v02-baseline
python -B portability_audit.py --compare /tmp/x6-v02-native /tmp/x6-v02-baseline
```
