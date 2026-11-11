# CST-DUST: paritätserlaubter Mischblock v0.1

Der erste Atom-zu-Positiv-Übergang mit Materiepaket 0→0 wird im deklarierten 33-Historien-Kontrollensemble berechnet. Sowohl die ursprüngliche Wirkung als auch die auf Wirkungsebene entkoppelte Skalarreferenz liefern einen zertifizierten Nichtnullwert. Die Kopplung ist für diesen Mischungszeugen nicht notwendig, verändert aber die komplexe Amplitude nachweislich.

Physikalische CST-Matrix weiterhin NOT_CONSTRUCTED; alle acht physikalischen Gates HOLD. Die gleichmäßigen Historiengewichte, κ=1, kompakten Staubmaße und Randpakete sind explizite Kontrollentscheidungen. Die Zahlen sind keine physikalischen Wahrscheinlichkeiten.

## Inhalt

- `CST_DUST_Mischblock_v0_1.pdf`: Ergebnisbericht und Fehlerbudget.
- `DERIVATION.md`: vollständige Herleitung, Normierung, Phasenzweige, Entkopplung und analytischer Quadraturfehlerbeweis.
- `experiment_contract.json`: vor der numerischen Auswertung festgelegter primärer Versuch.
- `results/certified_mixing.json`: primäre Einschließungen, sämtliche Orbitbeiträge und Fehlergrenzen.
- `results/causation_diagnostics.json`: Zerlegung der Amplitudenänderung.
- `results/crosscheck_48.json`: Kontrolle mit 48 Knoten und 192 Bit.
- `results/independent_5d_n8.json`: unabhängige direkte 5D-Float64-Kontrolle; kein Fehlerzertifikat.
- `inputs/`, `provenance.json`: eingefrorene GitHub-Basis aus PR #279–281.

## Reproduktion ohne Netzwerk

Python 3.10+, Python-FLINT 0.9.0 und NumPy 2.3.5; Details in `requirements.txt` und `environment.json`.

```sh
python verify.py
python verify.py --extended
```

Der Standardlauf prüft alle Datei-Hashes, fünf Herkunfts-Blobs, 27 Tests und wiederholt die primäre 40er-Ballrechnung samt Ursachendiagnostik. `--extended` wiederholt zusätzlich die 48er-Rechnung. Der Verifier verändert keine Referenzdaten. Das ZIP außerhalb des entpackten Paketordners belassen, da die Inventur absichtlich vollständig ist.

Bewusster Neuaufbau:

```sh
python run_certified.py
python run_certified.py --n 48 --precision 192 --output results/crosscheck_48.json
python independent_check.py
python causation.py
python make_report.py
python package.py
```

`package.py` erneuert das Manifest und ist deshalb kein Integritätsprüfer fremder Pakete. PDF-Bau benötigt zusätzlich ReportLab, Matplotlib und Pillow. Lizenz: Apache-2.0; siehe `LICENSE` und `NOTICE`.
