# U(1)-Eichfeld-Labor · Gauge field lab v0.1

**Ergebnis.** Im Vier-Ereignis-Diamanten stimmt die U(1)-Flussphase bei 256 lokalen Eichwahlen und jeweils allen 24 Umnummerierungen bis auf Rundungsfehler mit der analytischen Referenz überein. Beim verblindeten 4D-Test verfehlt der vorab festgelegte Schätzer die quantitative Anforderung für beide Feldtypen. Gemessen wird die doppelte klassische Maxwell-Lagrangedichte $J=|\mathbf E|^2-|\mathbf B|^2$ in natürlichen Einheiten auf festen Minkowski-Ordnungen. [Labor im Browser öffnen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/eichfeld/index.html) · [Forschungsbericht (PDF)](X6_Eichfeld_U1_Blindtest.pdf) · [Vollständiges Prüfpaket (ZIP)](X6_Eichfeld_U1_Pruefpaket.zip)

| Vorgegebenes Feld | Richtiges Vorzeichen | Relativer Fehler in J höchstens 25 % |
| --- | ---: | ---: |
| Elektrisch | 65/128 · FAIL | 1/128 · FAIL |
| Magnetisch | 126/128 · PASS | 86/128 · FAIL |

Je Ordnung wurden 64 Innenereignisse zufällig gezogen und zwei feste Randspitzen ergänzt. Jede der 256 Vorhersagen verwendet eine eigene Geometrie. Der Schätzer sah nur die direkte Kausalordnung, die Transportphasen und die zuvor kalibrierte Matrix. Je zwei Enthaltungen pro Feldtyp zählen in beiden Kriterien als Fehlschläge. Die Ziele waren mindestens 90 % für das Vorzeichen und mindestens 80 % für die Genauigkeit von J, jeweils für beide Klassen. Die exakten Binomialgrenzen sind gemeinsam zu mindestens 99 % abgesichert, bedingt auf die Kalibrierung. [Versuchsplan](design.json) · [Schätzer](estimator.py) · [Kontrollen](controls.json) · [256 Einzelwerte (CSV)](data/scores.csv) · [Konfidenzgrenzen (JSON)](data/summary.json)

**English summary.** On a fixed four-event diamond the measured phase is invariant under local rephasing and relabelling, with a maximum complex error below 1.76 × 10⁻¹⁵. On blinded four-dimensional orders the estimator recovered the sign for 65/128 electric and 126/128 magnetic fields. It met the ±25% accuracy criterion for 1/128 and 86/128 respectively. The magnetic sign test passed. Both magnitude tests failed. The two large opposing contributions to the electric estimate fluctuate between orders. The experiment concerns synthetic constant fields on prescribed flat geometries. The browser interface and the paper are in German.

## Reproduktion

Das ZIP enthält den ursprünglichen Astrolabium-Kern samt Lizenzhinweisen, sämtliche Eingaben, Lösungsschlüssel, Vorhersagen, Prüfsummen, die PDF-Druckquelle und die eigenständige HTML-Datei. Die veröffentlichten Dateien für Labor und Bericht sind bytegleich mit den entsprechenden Dateien im ZIP. Die Verblindung wurde innerhalb des Projekts mit getrenntem Vorhersageprozess und Prüfsummen vor der Aufdeckung durchgeführt. Der aktuelle Browserzugang spielt die abgeschlossene Prüfung nach.

Nach dem Entpacken in ein eigenes Arbeitsverzeichnis wechseln. Die Anleitung im Archiv enthält zusätzlich die Befehle zur vollständigen Neuerzeugung aus dem archivierten Startwert.

```sh
sha256sum -c SHA256SUMS
export OPENBLAS_NUM_THREADS=1
python3 evaluate.py data
node verify_js.cjs data
```

[Model contract of the RAX-CQG benchmark](../benchmark-v0.2.0/MODEL_CONTRACT.md) · [Sverdlov, Gauge Fields in Causal Set Theory](https://arxiv.org/abs/0807.2066) · [Sverdlov and Bombelli, Dynamics for causal sets with matter fields](https://arxiv.org/abs/0905.1506)
