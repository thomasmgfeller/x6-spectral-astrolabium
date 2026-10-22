# Eigenzeit: joint overlap bounds and a smooth-field target

SPDX-License-Identifier: Apache-2.0

**22 October 2026 — joint constraints improve; full operator accuracy remains open.**

This follows PR89 using all twenty existing candidate B0 packets. It adds
confidence constraints from intersections and exclusive interval parts, exact
causal inclusions, and known-interval intersections. No new sampling, fitting,
truth-coordinate input or observed field data is used.

| Result | Finding |
|---|---|
| Joint confidence coverage under the fixed Poisson model | Greater than 97.7715%, for 1,736 original means plus 230,796 derived observations; overlap dependence is allowed. |
| Pair-difference ranges narrower than the old marginal box | **21,868** unordered pairs across all twenty packets. |
| Strongest pair-difference width reduction | Remaining width about **10.30%** of the old width; this is not a volume reduction or accuracy factor. |
| Original marginal intervals narrowed | **0 / 1,736**. |
| Full-box <=10% relative weight certificates | **0 / 19** computable cases; one prior count HOLD retained. |
| Two prior exact witness geometries | Both satisfy the new necessary relaxation. Their full geometric overlap compatibility is not established. |

The propagation uses 20,600 order-derived nested pairs and 26,888 pairs whose
intersection is a known selected interval. These categories overlap. All
count identities, integer shortest paths and output records are replayed.

The negative operator result is informative: projecting joint constraints
back to a rectangle loses their gains. It is not evidence that overlap data
are useless or that the physical reconstruction is impossible. The next
bound should work directly on the constrained set. Conversely, passing the
necessary relaxation does not prove that either witness remains in the full
geometric confidence set, so the earlier recovery lower bound is **not**
promoted to a lower bound for that stronger set.

[THEORY.md](THEORY.md) derives the simultaneous confidence budget and exact
constraint propagation. The added union-bound budget slightly reduces the
coverage lower bound from PR89's 97.8667%; it is not unchanged. The coverage
percentage is not reconstruction success probability. All prior HOLDs remain.

[FIELD_CONTRACT.md](FIELD_CONTRACT.md) fixes a normalized C3 field class and
an absolute dimensionless response error. It separates geometry/weight error,
cubic discretization remainder, and field noise. Zero-response fields are
included; a relative-error denominator is not invented. A working E<=0.1 target
is declared for future certification, with no new scientific PASS claim.

[PROTOCOL.md](PROTOCOL.md), [contract.json](contract.json), and [freeze.json](freeze.json)
were fixed before this numerical audit of known archived data. They are not
preregistration of an independent experiment. Results, summary and audit are
complete. [SHA256SUMS](SHA256SUMS) inventories this package.

From the repository root, Python 3.12 with the prior pinned requirements:

```sh
python -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/joint_overlap_bounds/jo_run.py --verify
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/joint_overlap_bounds/jo_audit.py --verify
```

The four synthetic controls cover transitive constraint propagation, a
zero-count tail, empty-set rejection, and a nested-pair gain. The audit also
checks an exact quadratic-field response. These controls and replay verify
the implementation; the analytic theorem supplies coverage.
