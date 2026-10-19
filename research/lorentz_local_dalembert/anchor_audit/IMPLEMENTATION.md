# Implementation freeze before target data

Protocol was published at `4b7e7aea9ba935295dd0d21963080c31f8ffc9a9`
before any new development cloud. The six fixed development clouds ran with
this implementation's source hashes; no density, scale, cap, threshold or seed
was changed. The complete development summary is in DEVELOPMENT.json. The
recorded source_commit there identifies the protocol ancestor; code was then
uncommitted. The target execution records the subsequent PUBLIC source freeze
and all inference, sampler, analyzer and verification hashes.

Development: legacy usable 1/6, balanced-first 5/6, oracle cap 6/6. At the
highest density, balanced-first metric RMS was 7.531, oracle cap 5.486. This
already warns that fixing missing anchors alone will not make the operator
accurate. No response to these errors was incorporated into parameters. Target
seeds have not yet been generated at the time of this note.

Controls passed: four variants of a genuine 85-element poset whose first valid
anchor ranks 66; comparison against exhaustive original search; time reversal
and relabelling; zero/one overlaps unresolved; original assembly parity;
2,272 exhaustive chain checks and five independent quadrature checks inherited.

Candidate inference imports no sampler or coordinate evaluator and accepts no
coordinates. Original sources remain byte-identical. Candidate search visits
all eligible common anchors and retains at most 64 that pass the original
balance/inversion rules. Per-pair valid ranks and rejection counts are stored.
Median aggregation may change successful old distances as more anchors enter;
this is part of the prespecified intervention. No independent-anchor standard
error is claimed, because anchors within a cloud are strongly dependent.

The oracle cap uses exact spatial pair distances on the existing discrete
shells. It preserves root, temporal points, scales and operator weights. Its
remaining errors cannot identify a unique cause among temporal calibration,
shell spread, frame wandering, angular sampling and finite-domain effects.
A boundary witness remains diagnostic only. A positive witness establishes
truncation, while zero sampled witnesses does not establish containment.

Commands (NumPy/SciPy versions are pinned in the inherited requirements file):

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/anchor_audit/controls.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/anchor_audit/run_audit.py --mode test --output /tmp/bk-anchor-fresh
python3 -B research/lorentz_local_dalembert/anchor_audit/audit_analysis.py /tmp/bk-anchor-fresh --output /tmp/bk-anchor-fresh/summary.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/anchor_audit/verify_audit.py --directory /tmp/bk-anchor-fresh
```

The target run is indivisible: all 48 seeds or a documented error/budget hold.
Replay verifies all records and recomputes the frozen decision. The old
phase12 verifier and BD reference are not modified by this follow-up.
