Vier Landmarken: neue Wolken mit vollständiger Zählkovarianz

Ergebnis: HOLD. Vollständig ausgeführt: 32 Auswahlwolken, 18 erfolgreiche
Vier-Landmarken-Auswahlen, 162 unabhängige Zählwiederholungen. Nur 1/32
Hauptfälle geometrisch qualifiziert. Details in Ergebnisbericht.txt.

Wichtige Dateien:
  contract.json / PROTOCOL.txt / freeze.json: Regeln vor Datenerzeugung
  selection.py: Koordinatenfreie vierte Landmarkenauswahl
  inference.py: Gewichte und komplette Zählkovarianz-Fortpflanzung
  simulation.py: isolierte Koordinaten-/Simulationsgrenze
  run_pilot.py: begrenzte Ausführung, Seeds und Inferenzsiegel
  results/cloud-XX.json.gz: alle Auswahlen, Zählungen, Schnittmengen, Gewichte
  results/truth/: erst nach dem Inferenzsiegel exportierte Evaluationsdaten
  analysis.json: Ergebnis, alle Gate-Entscheide und Einzelfälle
  record_verification.json: vollständiger Replay aller 162 Zählwiederholungen
  sage_verification.json: unabhängige Prüfung der 17 gültigen Hauptsysteme
  vendor/: erforderliche unveränderte X6-Quellen und Konfigurationen

Schneller Replay mit Python, NumPy, SciPy:
  sha256sum -c SHA256SUMS.txt
  OPENBLAS_NUM_THREADS=1 python3 verify_records.py
  OPENBLAS_NUM_THREADS=1 python3 analyze.py
  OPENBLAS_NUM_THREADS=1 python3 controls.py

Unabhängiger Sage-Replay in einer aktivierten SageMath-10.9-Python-Umgebung:
  python exact_geometry_sage.py
  python exact_covariance_sage.py
  python verify_sage.py
Der beigelegte environment-explicit-sage.txt fixiert die hierfür verwendeten
Linux-64-Conda-Pakete. Die Versionen des Produktionslaufs stehen in
results/worker-0.json und results/worker-1.json.

Vollständige Neugenerierung nur in einer separaten Kopie OHNE results/:
  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 run_pilot.py 0
  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 run_pilot.py 1
Die beiden Befehle dürfen gleichzeitig in getrennten Terminals laufen.
Je Prozess sind bis zu 3000 MiB und 1200 Sekunden vorgesehen. Vorhandene
Versuchsdaten werden absichtlich nicht überschrieben. Danach analyze.py und
die Prüfskripte ausführen. Laufzeiten sind keine bytegleichen Reproduktionsziele.

Vorab-Freeze und alle ursprünglichen Eingaben bleiben unverändert. Nach dem
Freeze ergänzte Replay-/Berichtsdateien ändern keinen Versuchsparameter;
completion_manifest.json unterscheidet diese. Nicht alle formal gültigen
Gewichte sind geometrisch qualifiziert: qualified und order immer mitlesen.

Vier Felder und acht Streuungswiederholungen sind keine zusätzlichen unabhängigen
Auswahlwolken. Die Zählkovarianz ist eine bedingte lineare Näherung für die
Operatorstreuung, keine Gesamtfehler- oder Krümmungsfreigabe.
