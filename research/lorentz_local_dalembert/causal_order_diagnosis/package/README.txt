Eigenzeit causal-order diagnosis — 2026-10-22

Start with Ergebnisbericht.txt (German).
No original scientific gates or source files were modified.

Contents
  source/              all 141 original archive members, unchanged
  evidence/            new raw diagnostic records, outcomes, logs and hashes
  PROTOCOL.txt         initial locally frozen analysis plan
  SUPPLEMENT_PLAN.txt  adaptive follow-up precision and bias questions
  diagnose.py          original replay and 2x2x2 exact-distance interventions
  density_diagnostic.py  216 new conditional Poisson count clouds
  supplement.py        Decimal 80/120 and Poisson mean-input diagnostics
  make_witness.py      export of first B0 mismatch in cloud-index order
  verify_witness.py    six-node counterexample, standard-library only

Runtime used: Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0.
The original source environment lock remains under source/.

Fast standalone check, no external packages:
  python3 verify_witness.py

Reproduction in a separate extracted working copy (commands overwrite the NEW
evidence outputs only, never source/):
  OPENBLAS_NUM_THREADS=1 python3 diagnose.py
  OPENBLAS_NUM_THREADS=1 python3 density_diagnostic.py
  OPENBLAS_NUM_THREADS=1 python3 supplement.py
  OPENBLAS_NUM_THREADS=1 python3 make_witness.py
  python3 verify_witness.py

Raw count draws and results are deterministic with the pinned runtime.
Elapsed-time fields and execution logs need not be byte-identical on rerun.
The conditional density campaign has a 600-second budget; on a slower machine
it records BUDGET_HOLD without replacement draws. The original run completed
all 216 scheduled clouds. A highest-density draw was independently regenerated
and matched both accepted-point hash and counts exactly.

Interpretation limits:
- The archived 32 selections are not 162 or 216 independent selections.
- Truth substitutions diagnose causes; they are not deployable estimators.
- Geometric intervention tallies do not bypass original minimum-count gates
  for scientific qualification. Density tallies do apply those gates.
- Mean transformed inputs test G(E[q]), not E[G(q)].
- Standalone rational arithmetic is exact for recorded binary64 numbers;
  the Decimal supplement separately checks the nonlinear input transformation.
- No new Sage run, independent third-party replication, correction or physics
  qualification is claimed.

SPDX-License-Identifier: Apache-2.0
