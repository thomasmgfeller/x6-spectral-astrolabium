# Eigenzeit: actual overlap volumes of the two witness geometries

SPDX-License-Identifier: Apache-2.0

**22 October 2026 — both witnesses remain compatible, with an explicitly
probabilistic numerical enclosure.**

PR90–91 retained only necessary joint mean constraints. This audit evaluates
the actual intersection and exclusive-region volumes of both exact PR88
geometries against the original pairwise-overlap confidence bands. No witness
is refitted and no statistical threshold is relaxed.

| Check, per geometry | Result |
|---|---|
| Original interval means | All **74** inside their c=12 bands |
| Unordered interval pairs | **2,701** |
| Analytically resolved intersection pairs | **2,221** |
| Numerically integrated pairs | **480** (240 distinct endpoint configurations) |
| Total mean constraints, including intersection and both exclusive parts | **8,177 / 8,177** inside |
| Numerical sample cells | **4,194,304**; the first 1,048,576 left one constraint unresolved |
| Final exclusions / unresolved constraints | **0 / 0**, for both witnesses |
| Simultaneous numerical failure budget | Less than **1.372e-6**, or **0.0001372%**, under iid uniform cell sampling |

The numerical method uses equal-volume cells, exact integer whole-cell
classification and simultaneous binomial confidence bounds. Boundary cells
remain explicitly uncertain. It is **not a deterministic integration proof**.
The mathematical numerical guarantee assumes ideal iid uniform draws; the
reproducible implementation uses pinned NumPy PCG64 and fixed seeds. Replay
cannot prove that ideal randomness assumption. The three predeclared sample
stages are all included in the error budget, including the unused final stage.

This numerical confidence is separate from the >97.7715% repeated-measurement
coverage of PR90's confidence set. Neither is a probability that the witness
is physically true, a reconstruction success probability or a guarantee of
operator accuracy.

## What this resolves

Subject to the stated numerical coverage event, the pair survives the actual
**pairwise-overlap volume** constraints, not just the earlier difference
relaxation. Its exact **14.82% symmetric relative weight separation** therefore
still yields a **7.41% set-wise uniform recovery lower bound** for this set.
A uniform 5% weight guarantee over this set is incompatible with that pair;
10% accuracy is **not** ruled out by this lower bound.

The check does not prove that the two full observation laws are statistically
indistinguishable. Higher-order overlap atoms, all original A/B relations and
smooth-field response accuracy are outside this result. The adversarial sign
field used earlier is not assumed to be C3. All scientific HOLDs remain.

[THEORY.md](THEORY.md) proves analytic reductions, the containing box, exact
cell enclosures, the binomial numerical budget and the set-wise lower-bound
interpretation. [PROTOCOL.md](PROTOCOL.md), [contract.json](contract.json) and
[freeze.json](freeze.json) were fixed before evaluation of the already known
witnesses. This is not an independent-data validation.

## Next discriminating question

The remaining statistical question is how much information the **joint law**
of the actually available measurements contains, beyond these conservative
pairwise confidence bands. A testing-distance or likelihood analysis must
specify that experiment and account for higher-order interval membership;
it cannot assume that matching means/covariances establishes equality of laws.
The 10% smooth-field objective remains a separate target. Further repetitions
of the same optimizer would not close either proof gap.

## Reproduction

All analytic bounds, per-stage inner/outer hit counts, numerical bounds,
constraint decisions and membership hashes are archived in the two compressed
geometry records. Both complete seeded integrations replay exactly. The audit
adds 4,725 exact cell-point checks, six exact binomial-tail controls and three
decision controls. Analytic means of all 74 individual diamonds are enclosed
by the randomized integrator at every executed stage.

```sh
python -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/witness_overlap_volumes/wv_run.py --verify
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/witness_overlap_volumes/wv_audit.py --verify
```

The replay comparator was corrected to normalize in-memory count tuples to
JSON lists before equality. No numerical output changed; freeze.json records
the original pre-evaluation source hash and this verification-only revision.

Python 3.12. [SHA256SUMS](SHA256SUMS) inventories the complete package.
[summary.json](summary.json) and [audit.json](audit.json) retain the numerical
and measurement coverage claims separately.
