Eigenzeit: intrinsische Korrektur, Entwicklung vom 21.10.2026

Zuerst Ergebnisbericht.txt lesen.
V1: geometrisch zulässig, im archivierten Versuch praktisch VERWORFEN.
V2: Vier-Landmarken-Differenzoperator implementiert und exakt geprüft;
    verrauschte Wolken NICHT geprüft.

Reproduktion in einer KOPIE dieses Verzeichnisses:
  sha256sum -c SHA256SUMS.txt
  OPENBLAS_NUM_THREADS=1 python3 numerical_controls.py
  OPENBLAS_NUM_THREADS=1 python3 four_landmark_controls.py

Für einen neuen V1-Replay die vorhandenen inference.json und inference_seal.json
aus der Kopie in ein separates Archiv verschieben. Dann:
  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 run_candidate.py
  python3 evaluate_candidate.py
Der Runner überschreibt absichtlich keine vorhandene inference.json.

In einer aktivierten SageMath-10.9-Python-Umgebung:
  python exact_geometry_sage.py
  python exact_four_landmarks_sage.py
  python verify_candidate_sage.py

Der ursprüngliche Conda-Lock ist unter environment-explicit-sage.txt enthalten.
Beispiel: conda create -n x6-intrinsic-check --file environment-explicit-sage.txt
Danach conda activate x6-intrinsic-check. Die tatsächlich für die V1-Numerik
verwendeten Python-/NumPy-/SciPy-Versionen stehen in inference.json.

intrinsic_inputs.json enthält ausschließlich intrinsische Eingaben und
Provenienz. evaluation_inputs.json enthält die getrennten Simulationswahrheiten.
Der Korrekturcode importiert oder liest diese Wahrheiten nicht.
inference_seal.json bindet die vor der Bewertung fertigen Gewichte.
development_freeze.json fixiert den V1-Stand vor dem Ergebniszugriff lokal.
Dies ist KEINE öffentliche Präregistrierung und kein unabhängiger Testdatensatz.
Die erste fehlerhafte Sage-Kontrollkopie liegt unverändert unter attempts.
completion_manifest.json erklärt die Korrektur und enthält finale Dateihashes.

Alle 64 alten Fälle und alle V1-Ergebnisse bleiben enthalten.
Für V2 enthält das Archiv keine vierte externe Landmarke; ein Wolkentest kann
erst nach einer intrinsischen Neuauswahl und neuen Messungen ausgeführt werden.
