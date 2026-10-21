Eigenzeit: unabhängige SageMath-Prüfung

Start (innerhalb der aktivierten Sage-Conda-Umgebung):
  python audit_sage.py --exact-only
  python audit_sage.py

Die exakten Kontrollen prüfen den zuvor in Wolfram konstruierten Fehlermechanismus.
Der zweite Aufruf prüft die 64 archivierten X6-Wolken, davon 58 vollständig.
Die Daten sind retrospektiv; dieser Lauf ersetzt keine neue unabhängige Wolkenkampagne.

Der Prüfer importiert keine X6-Funktionen. Er baut die Polynombedingungen selbst auf
und löst das volle KKT-System mit Sage. Die gemeinsame Root-Messung ist im
Minimum-Varianz-Kriterium H=I+11^T enthalten. Die gemischten Monome werden ohne
sqrt(2)-Normierung verwendet; ihre homogenen Bedingungen bleiben äquivalent.

inputs.json enthält nur die für die Prüfung notwendigen archivierten Werte sowie
Hashes der ursprünglichen Wolkendateien. Alle Zahlen werden als die exakten
binären Rationalwerte der archivierten float64-Eingaben interpretiert. Höhere
Rechenpräzision macht diese Eingaben nicht zu exakt bekannten physikalischen
Koordinaten. Es gibt keine Behauptung rigoroser Intervallzertifikate für die
transzendenten Feldantworten; hierfür wird Präzisionskonvergenz geprüft.

CONTRACT.json enthält die vor Ausführung festgelegten numerischen Kriterien.
Ausgabe: exact_summary.json / audit_summary.json, Prüfprotokolle, records.json.
Historische HOLD-Gates werden durch diese Rechenprüfung nicht aufgehoben.

Basis: thomasmgfeller/x6-spectral-astrolabium, Commit
ee6460971c2b3ec48ea2ebb18002072ca3d22f97.

Sage-Dokumentation:
https://doc.sagemath.org/html/en/tutorial/tour_linalg.html
https://doc.sagemath.org/html/en/installation/conda.html

SPDX-License-Identifier: Apache-2.0
