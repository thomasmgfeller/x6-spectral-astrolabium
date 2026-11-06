# CST-DUST Staubstrom-Kalibrierung v0.1

Ein konservativer markierter Strom und sein Messadapter, bedingt kalibriert an
REF-DUST-FB-01. Keine neuen Zufallsensembles, keine dynamische CST-Qualifikation.
Alle physikalischen CST-Gates einschließlich Regularität bleiben HOLD.

## Reproduzieren

Python 3 mit NumPy und SciPy:

```sh
python3 calibrate.py
python3 audit_checkpoint.py
```

`calibrate.py` prüft den eingefrorenen Plan und die bytegenaue Vertragskopie,
reproduziert 86 Graphkontrollen, 420 Massenfälle, 144 Flussfälle, 315 Expositionen,
1575 Integrationsvergleiche, 1260 Poissonfälle und 12 Kovarianzmatrizen.
`audit_checkpoint.py` erzeugt den P2-Datensatz und prüft ihn mit dem unveränderten
Eltern-Gate; die Zusatzprüfung propagiert deterministische Kalibriergrenzen.
Ausführungsumgebung: `results/run_manifest.json`.

Der Bericht und die Abbildungen lassen sich zusätzlich mit Matplotlib und
ReportLab erzeugen: `python3 build_report.py`. Benötigte Schriften: DejaVu Sans
und DejaVu Sans Mono unter `/usr/share/fonts/truetype/dejavu/`.
Der PDF-Zielpfad liegt standardmäßig in `../output/pdf/`.

## Dateien und Interpretationsgrenzen

- `DERIVATION.md`: Definitionen, Beweise, Kalibrierung, Quellen und offene Punkte.
- `plan.json`, `plan.sha256`: unveränderter Plan vor den neuen lokalen Rechnungen.
- `current.py`: rational-exakter markierter Kantenstrom; keine Bewegungsdynamik.
- `observables.py`: klassische Referenz, Exposition und Intervalladapter.
- `results/verification.json`: Zusammenfassung der reproduzierten Ergebnisse.
- `results/reference_decisions.json`: ausschließlich bedingte Referenzaussagen.
- `results/checkpoint_P2_record.json`, `checkpoint_P2_audit.json`: eigenständige
  Entscheidung aller acht physikalischen Vertrags-Gates; alle HOLD.
- `results/checkpoint_P2_CST.json`: lesbare Zusammenfassung dieser Abgrenzung.
- `results/*.csv`: vollständige numerische Ergebnisse, keine real gemessenen Daten.
- `inputs/`: unveränderte Vertrags- und Herkunftsdaten.
- `SHA256SUMS`: Prüfsummen des Paketinhalts ohne die Prüfsummendatei selbst.

PASS beim Zählplan bedeutet ausreichende Referenz-Präzisionswahrscheinlichkeit
unter den angegebenen Annahmen. Es bedeutet weder tatsächlich beobachtete
Trefferquoten noch endliche inverse Zählmomente, zurückgewonnene Staubdynamik,
Singularitätsauflösung oder einen Horizontnachweis.
