# Eigenzeit: conformal transport sharpens the full Poisson-law bound

SPDX-License-Identifier: Apache-2.0

**A deterministic transport bound replaces a vacuous membership-change bound
for coordinated shape changes. No strong 10% counterexample is found.**

The outer endpoints, physical domain and known density remain fixed. All inner
points move together by a rational conformal flow preserving causal intervals.
Unlike PR95, inner landmarks and the root are allowed to move. Both physical
models retain homogeneous density; the nonuniform auxiliary density is only
a change-of-variables device for comparing their joint observation laws.

The proof gives TV <= sqrt(9U/10)*|atanh(k)| for the 90-count channel with all
overlap orders and optional total count. It does not assume independent counts
or a Gaussian distribution. The certificate uses exact rational arithmetic
and directed bounds, without a sampling-confidence qualifier.

| Quantity | Result |
|---|---:|
| Fixed coordinated deformations | 40 |
| Exact causal-order and margin passes | 40 |
| Candidates certified with TV <=1/4 | 36 |
| Selected flow parameter | -9/5000 |
| Symmetric relative weight separation | 0.15750177% |
| New TV upper bound | 0.248424353 |
| Previous slab TV upper bound on the same pair | 1 (vacuous) |
| Optimal equal-prior classification accuracy | <=62.421218% |
| Minimax expected weight error / fixed base norm | >=0.05922024% |
| Strong gate: disjoint 10% relative-error balls | Not met |

The meaningful improvement is the **same-pair information bound**. The larger
weight gap compared with PR95 also changes which landmark motions are allowed;
it must not be described as a controlled method-only performance gain.

See [full proof](THEORY.md), [fixed contract](contract.json),
[all candidates](candidates.json), [rational witness](witness.json),
[summary](summary.json) and [independent controls](audit.json).
All scientific HOLDs remain. The fixed search is complete; these results do
not prove stability or exclude strong pairs in other families. A subsequent
study should quantify operator sensitivity relative to the proved transport
cost before expanding the search budget.

## Reproduce

From the repository root:

```sh
python -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/conformal_transport/ct_run.py --verify
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/conformal_transport/ct_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/conformal_transport/SHA256SUMS
```

Controls verify exact inverse/composition laws, metric and volume Jacobians,
independent numerical integration of the transport inequality and conserved
volume, and independent SVD weight solutions. Quadrature is a check; the
certificate rests on the analytic proof and rational enclosures.

The channel excludes observed coordinates, a full B causal matrix, additional
geometric data and the A-selection likelihood. The target is discrete moment
weights, not continuum or smooth-field accuracy. No physical validation,
original-realization confidence-set membership, global stability, or 10%
impossibility is claimed.
