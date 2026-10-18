# Eigenzeit: geglättete Benincasa–Dowker-Referenz

**Implementiert, auf getrennten Poisson-Testdaten verglichen und vollständig
wiederholt. Ergebnis: NO_GO für variable Krümmung im festgelegten Pilotbudget.**

[Ergebnisse](RESULTS.md) · [Methoden](METHODS.md) · [Vertrag](contract.json) ·
[Prüfprotokoll](VERIFICATION.json) · [Rohdaten](results/) ·
[lokaler d’Alembertian: vorbereiteter Reproduktionszweig](../lorentz_local_dalembert/README.md)

Bekannte uniforme physische Dichte, 4D Minkowski/de Sitter und externe Eigenzeit
T=1. Der Operator ist für skalare Felder implementiert; der Hauptvergleich nutzt
R=-2B(1) am oberen Diamantpunkt gegen die bestehende C2-Modellinversion.
Keine unbekannte Eigenzeit, kein allgemeiner Krümmungsschätzer nachgewiesen.

384 Entwicklungs- und 6.144 Testwolken; Poisson-verteilte Punktzahlen.
Alle 6.528 Wolken wurden aus ihren Seeds reproduziert. Zusätzlich wurden
102 Wolken mit einem unabhängigen Relationsprädikat geprüft. Die Quellen sind
vor dem Lauf lokal festgeschrieben; die öffentliche Vorregistrierung wurde
durch automatische Publikationsprüfung blockiert.

```sh
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_bd_reference/verify.py --archive research/lorentz_bd_reference/results --replay
```

Ein C++17-Compiler (`g++`) ist erforderlich. Die Veröffentlichung muss den
Quellencommit `2d2539123162ddc032b85ba51af56255ca36a906` in der Historie erhalten;
ein Squash allein reicht für die Provenienzprüfung nicht. Für einen neuen Lauf
ist ein neuer Ausgabeordner erforderlich. `report.py` erzeugt Bericht und Grafik
aus dem unveränderten Archiv und benötigt zusätzlich Matplotlib.

English: Implemented 4D smoothed BD curvature reference with genuine Poisson
sprinkling, held-out comparison and full internal replay. The declared pilot
gate fails. Restricted-model C2, nominal intervals, modest scale separation;
no universal superiority or continuum-limit claim. Apache-2.0.

## Nachbau auf anderen Rechnern

Der unveränderte Originalprüfer verlangt bitgleiche Gleitkommawerte. Der erste
GitHub-Nachbau scheiterte an 2,84e-14 Rundungsabweichung. Für unterschiedliche
Rechner gibt es deshalb eine [separate numerische Plattformprüfung](PORTABILITY.md):

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_bd_reference/replay_portable.py
```

Sie verlangt weiterhin exakte Archiv-/Quellenprüfsummen, alle ganzzahligen
Intervallzählungen, Auswahl- und Entscheidungswerte. Nur Gleitkommafelder
nutzen die offengelegte numerische Toleranz. Koordinaten-Bytehashes werden
gesondert berichtet. Status: `PASS_PORTABLE_NUMERICAL_REPLAY`; kein behaupteter
bitgleicher Replay. Der ursprüngliche Prüfvertrag und die Daten bleiben gleich.
