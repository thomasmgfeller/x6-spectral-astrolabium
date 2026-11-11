# CST-DUST Randkern-Benchmark v0.1

11. November 2026. Quellenbasierte endliche Reproduktion; keine physikalische Hamiltonextraktion.

Der Benchmark reproduziert getrennte Bausteine der [Staubball-Reihe](../README.md)
und konkretisiert den Anschluss an [N0B-2C-MF v0.2](../n0b_2c_mf_v0_2/README.md).
Er liefert geometrische Verklebungskerne, einen endlichen Ausschnitt des positiven
Labelquotienten, die ursprüngliche Uhrkern-Negativkontrolle und eine stationäre
Schurantwort. Diese Daten haben unterschiedliche Zustandsräume und werden
**nicht zu einer vermeintlich physikalischen 8×8-Materiematrix zusammengesetzt**.

**41 eng begrenzte Kontrollen bestanden. Alle acht physikalischen Gates bleiben
HOLD. Die 8×8-Materiematrix ist NOT_CONSTRUCTED.** Das ältere scoped FAIL des
Kandidaten CST-DUST-V1-RAW-K wird reproduziert und bleibt separat erhalten.

## Daten und Reichweite

| Datei | Tatsächlich bereitgestellt | Grenze |
|---|---|---|
| [gluing.json](results/gluing.json) | Vier exakte Laurent-Polynome, 219 gelabelte Ordnungen, Phasenwerte | Geometrische Teilordnungen, keine zeitlichen Randzustände |
| [label_quotient.json](results/label_quotient.json) | Projektoren und Gram-Matrizen für m=0,1,2 | Hilfshistorienraum, nur Labelconstraints |
| [raw_clock_kernel.json](results/raw_clock_kernel.json) | Zertifizierte Intervalle des unveränderten Zweistellen-Uhrkerns | FAIL für jede gemeinsame positive Metrik unter der festgelegten Identifikation |
| [schur.json](results/schur.json) | Exakte stationäre Schurantwort und neun Substitutionen | Keine kompakte Quantenintegration, keine Oszillatorzustände |
| [verification.json](results/verification.json) | 41 Kontrollentscheidungen samt Geltungsbereich | Keine externe Replikation oder physikalische Validierung |

Die Labelkontrolle umfasst 15 diskrete markierte Zustände in zehn Orbits,
verteilt auf drei verschiedene m-Sektoren. Das ist keine gemeinsame
zehndimensionale physikalische Randbasis. Die vollständige ältere m≤4-Kampagne
wird hier nicht nochmals ausgeführt.

## Lesen und nachrechnen

- [DERIVATION.md](DERIVATION.md): Definitionen, Nachweise, Grenzen und Korrekturen.
- [OFFENE_RANDBASIS.json](OFFENE_RANDBASIS.json): fehlende Angaben zur vorgeschlagenen 8×8-Matrix.
- [status.json](status.json) und [plan.json](plan.json): getrennte Entscheidungen und festgelegter Reproduktionsumfang.
- [provenance.json](provenance.json): Basiscommit, Originalpfade und Blob-Identitäten.
- [Lesefassung als PDF](CST_DUST_Randkern_Benchmark_v0_1.pdf), erzeugt aus [REPORT.md](REPORT.md).
- [Prüfpaket als ZIP](CST_DUST_Randkern_Benchmark_v0_1_Pruefpaket.zip).

Im Paketordner, Python 3.10 oder neuer; die Rechnung benötigt nur die Standardbibliothek:

```sh
python3 -O -B benchmark.py --output /tmp/cst-randkern-results
python3 -O -B verify_package.py --replay
```

Der Replay läuft isoliert und vergleicht alle fünf Ergebnisdateien bytegleich.
Originalprogramme und zwei Referenzergebnisse liegen unverändert in `inputs/`.
Git-Blob-Identitäten und Paket-SHA-256-Prüfsummen werden geprüft. Ein entpacktes
ZIP ist eigenständig nachrechenbar. Liegt das äußere ZIP daneben im Paketordner,
wird zusätzlich sein deterministischer Neuaufbau bytegleich geprüft.

PDF-Neubau: `python3 -B build_report.py` nach Installation von
`requirements-report.txt`, mit DejaVu Sans unter dem im Builder angegebenen Pfad
oder über `CST_RB_FONT_DIR`. ZIP-Neubau: `python3 -B package.py`.

## Nächster physikalischer Anschluss

Benötigt werden konkrete Randtestfunktionen, ein gemeinsamer Variations-/Uhrvertrag,
die daraus hergeleiteten Produkte und Kernmatrixelemente sowie eine begründete
Materiemodenreduktion. Ein Nullatom der Dichte ist weder eine Eich-Nullrichtung
noch automatisch der Oszillatorgrundzustand. Ein einzelner verschwindender
Mischblock beweist keine Superselektion; ein nichtverschwindender Block noch
keinen physikalischen Zeitübergang oder den speziellen Term g₁(Q)φ.

Bekannte Resultate werden reproduziert; dies ist keine blinde Vorhersage und
keine externe Präregistrierung. Keine Produktionssimulation, keine neuen
Zeitpläne und keine kostenpflichtigen Rechenläufe.
