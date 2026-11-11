# CST-DUST: Zustandsreduktion und Verklebung v0.1

Schritt 5 prüft den Vierzustandsraum aus PR #280 und den endlichen Mischblock aus PR #282. Die Erweiterung auf 15 orthonormale Testzustände zeigt für den normierten Atom-/Grundpaketeingang einen ausgelassenen Anteil von **0.102348630703 ± 10⁻¹²**. Das entspricht **36.7087702939 % der Amplitudennorm innerhalb der getesteten 15er-Ausgangsspalte**, nicht einer physikalischen Wahrscheinlichkeit oder einer globalen Restschranke. Die bisherigen Matrixelemente bleiben bei unverändertem Kern und unveränderten Zuständen exakt gleich.

Ein separates Achtpunktbeispiel weist fünf fehlende schnittübergreifende Wirkungsterme nach. Die korrigierte lokale Teilwirkungssumme und die gemeinsame Wirkung liefern unterschiedliche normierte Nullatombeiträge. Die exakte gestufte Integration derselben gemeinsamen Wirkung stimmt dagegen mit der direkten Rechnung überein. Die entkoppelte Referenz aus Schritt 4 besitzt außerdem eine ungedämpfte Feldrichtung und bildet den untersuchten Eingang nicht in das ungegewichtete Rand-L² ab.

**32 Prüfungen bestanden.** Physikalischer CST-Kern weiterhin NOT_CONSTRUCTED; alle acht physikalischen Gates HOLD. Keine vollständige 15×15-Matrix, kein vollständiger 1089-Historienpaarlauf, keine obere Fehlergrenze für den unendlichen Zustandsraum.

## Inhalt

- `CST_DUST_Reduktion_Verklebung_v0_1.pdf`: Ergebnisbericht, Zustandsanteile und Fehlerbudget.
- `DERIVATION.md`: vollständige mathematische Herleitung und Definitionsbereichsanalyse.
- `experiment_contract.json`: vor der primären numerischen Auswertung eingefrorener Versuch.
- `results/states.json`: vollständige Gram-Matrix I₁₅ und Paketdefinitionen.
- `results/reduction.json`: zertifizierte Testspalte, Orbitbeiträge und Breitenkontrollen.
- `results/crosscheck_56.json`: Kontrolle mit 56 Knoten und 224 Bit.
- `results/gluing.json`: exakte Wirkungsdefekte und normierte Kernbeiträge.
- `results/independent_5d_n8.json`: unabhängige direkte Float64-Kontrolle; kein Fehlerzertifikat.
- `inputs/`, `provenance.json`: sieben eingefrorene Herkunftsdateien aus Main `d4cac775a044177e9d66d517c11c941cb812f0a6`.

## Reproduktion

Python 3.12 mit den Versionen in `requirements.txt`. Nach Installation dieser Abhängigkeiten benötigt die Prüfung kein Netzwerk.

```sh
python verify.py
python verify.py --extended
```

Der Standardlauf prüft Dateiinventar, SHA-256- und Git-Blob-Werte, 32 Tests und den bytegleichen Replay der primären Rechnung, der exakten Zustände und der Verklebungsrechnung. `--extended` wiederholt zusätzlich die 56er-Rechnung bytegleich und die unabhängige direkte 5D-Float64-Kontrolle mit absoluter Vergleichstoleranz 3·10⁻¹⁴. Diese Float64-Toleranz ist kein Fehlerzertifikat für die primäre Rechnung. Der Verifier ändert keine Referenzdateien.

Bewusster Neuaufbau:

```sh
python write_exact_states.py
python run_reduction.py
python run_reduction.py --n 56 --precision 224 --output results/crosscheck_56.json
python independent_check.py
python gluing.py
python make_report.py
python package.py
```

Der PDF-Bau benötigt zusätzlich ReportLab, Matplotlib und Pillow. `package.py` ist ein Release-Bauer, kein Prüfer fremder Pakete. Das ZIP außerhalb des entpackten Paketordners belassen, damit die vollständige Dateiinventur erhalten bleibt. Lizenz: Apache-2.0; siehe `LICENSE` und `NOTICE`.
