# CST-DUST 8×8-Geometriekontrollkern v0.2

11. November 2026. Korrigierter Generator, drei NPZ/JSON-Kontrollpaare und Regressionstests.

**Formaler Kontrollkern mit unveränderten Zusatzlabels.** Die Identität auf
Stratum- und Materielabels ist eine ausdrückliche Testannahme. Die geerbten
gravitativen Polynome bestimmen diese Erweiterung nicht eindeutig. Die gemeinsame
physikalische 8×8-Materiematrix bleibt **NOT_CONSTRUCTED**, alle acht physikalischen
Gates bleiben **HOLD**. Die hier vorhandene numerische 8×8-Testmatrix ändert das nicht.

Der [Randkern-Benchmark](../boundary_kernel_benchmark_v0_1/README.md) bleibt die
Quellenreferenz. Dieses Paket korrigiert das anschließend eingereichte 8×8-Artefakt;
der ursprüngliche Upload ist in [provenance.json](provenance.json) durch Hashes
identifiziert. Vorherige wissenschaftliche Resultate werden nicht überschrieben.

## Daten

| Kontrollphase | Matrixdatei | Metadaten, exakte Werte und Diagnostik |
|---|---|---|
| z=1 | [NPZ](data/cst_dust_geometry_kernel_8x8_z1.npz) | [JSON](data/cst_dust_geometry_kernel_8x8_z1.json) |
| z=−1 | [NPZ](data/cst_dust_geometry_kernel_8x8_zm1.npz) | [JSON](data/cst_dust_geometry_kernel_8x8_zm1.json) |
| z=i | [NPZ](data/cst_dust_geometry_kernel_8x8_zi.npz) | [JSON](data/cst_dust_geometry_kernel_8x8_zi.json) |

Die Ausgabe ist jetzt **stratumweise** geordnet: alle vier Nullatom-Testlabels,
danach alle vier positiven Testlabels. Diese Namen sind zusätzliche Labels und
noch keine hergeleiteten Zustandsfunktionen. Der frühere obere rechte 4×4-Block
war ein Geometrieblock; er darf nicht als Stratumwechsel gelesen werden.

- [Generator](cst_dust_geometry_kernel_8x8.py), [Dateiformat](DATA_FORMAT.md), [Korrekturen](CORRECTIONS.md).
- [Exakte Diagnostik und Reichweite](DIAGNOSTICS.md), [Status](status.json).
- [19 Regressionstests](test_geometry_control.py), [archivierte Ergebnisse](results/tests.json).
- [Prüfpaket (ZIP)](CST_DUST_Geometriekontrollkern_8x8_v0_2_Pruefpaket.zip).

## Reproduktion

Getestet mit Python 3.12.14 und NumPy 2.3.5. Python ≥3.11 wird für diese
gepinnten Abhängigkeiten vorausgesetzt. Nach Installation aus requirements.txt:

```sh
python3 -m pip install -r requirements.txt
python3 -O -B cst_dust_geometry_kernel_8x8.py --phase 1 --output /tmp/geometry_z1.npz
python3 -O -B test_geometry_control.py --output /tmp/geometry_tests.json
python3 -O -B verify_package.py --replay
```

Der letzte Befehl erzeugt alle drei NPZ/JSON-Paare und das Testergebnis isoliert
neu und vergleicht die sieben Dateien bytegleich. NPZ wird ohne Pickle gelesen;
der Generator verwendet feste ZIP-Metadaten. Für exakte Quellenkontrollen dienen
die Phasen `1`, `-1`, `i`. Allgemeines `--kappa` oder `--z-real/--z-imag` wird
numerisch ausgewertet und ausdrücklich entsprechend gekennzeichnet.

Nichtendliche/verschwindende z, Überläufe, widersprüchliche Eingabemodi und
fehlgeschlagene Pflichtkontrollen führen zu Exitcode 2. Validierungsfehler
werden vor dem Schreiben von Ausgabedateien erkannt. Betriebssystem-/Dateifehler
werden ebenfalls nicht als Erfolg ausgegeben.

## Produkt und physikalischer Anschluss

`G_in_diagnostic=G_out_diagnostic=I8` ist die gewählte Normierung der formalen
Testbasis. Sie ist keine aus den vorhandenen Orbits hergeleitete physikalische
Gram-Matrix. Die echten Orbitfunktionen müssen erst auf diese Basis abgebildet
werden. Deshalb heißen die Felder ausdrücklich `*_diagnostic`; `G_in`, `G_out`
und eine erfundene Uhrschrittweite werden nicht als physikalische Eingaben geliefert.

Im Testprodukt ist der Kontrollkern nicht unitär. Für z=1 wird außerdem eine
bedingte spektrale Obstruktion gegen eine gemeinsame positive Metrik erläutert,
wenn dieselbe Zahlenmatrix als Koeffizientenabbildung interpretiert wird.
Kein Hamiltonoperator wird extrahiert. Keine kostenpflichtigen Läufe oder Zeitpläne.
