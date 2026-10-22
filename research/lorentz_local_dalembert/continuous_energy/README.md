# Continuous exclusion, an energy-bounded field class, and a controlled analytic bridge

SPDX-License-Identifier: Apache-2.0

The three requested steps are implemented, with separate claim boundaries:

| Step | Result | What remains open |
|---|---|---|
| Continuous spatial steps | **63 of 64 complete rays excluded** on h in [0,0.1] | One interval on one ray |
| Declared field class | Exact worst-case operator-response norms on a fixed order-derived energy ball | Physical justification of this additional regularity assumption |
| Kigami/Strichartz methods | Compatible auxiliary refinements and a sharp energy-dependent quadrature bound proved | Identification with physical causal-set refinement and the Lorentzian operator |

This advances beyond the finite-grid result of PR108. It does not prove global
stability, and it does not produce a strong statistically close counterexample.

## 1. Only one continuous interval remains unresolved

The fixed contract covers all **64** combinations of 16 support nodes, two
spatial axes in the rational boost frame, and both signs. Each ray compares the
same base geometry with every displacement magnitude **h in [0,0.1]**.

The calculation evaluates **8,242** interval cells, including two prescribed
refinement rounds, and leaves an exact, gap-free cover of **8,217** terminal
cells. Every discarded cell has a proof applying throughout the cell:

| Whole-cell decision | Terminal cells |
|---|---:|
| Symmetric operator gap is at most 20% | 5,717 |
| A single count proves full-law TV >1/4 | 682 |
| At least one known causal relation cannot be preserved | 1,788 |
| Unresolved | **30** |

All 30 unresolved leaves are contiguous on **one ray**:

    node 15, boosted x direction, sign -1
    h in [45/1024, 51/1024]
      = [0.0439453125, 0.0498046875].

The endpoints are included conservatively. Every other point of the declared
64-ray domain is excluded from the conjunction of unchanged causal order,
operator gap >20%, and full-law TV<=1/4. Further admissibility gates could only
shrink that conjunction. The remaining interval is **HOLD**, not a close-law
certificate, a demonstrated instability or an assertion that every point is
admissible.

The operator enclosure uses an exact rank-two covariance update for moving one
moment column. Polynomial cancellations are performed before interval arithmetic.
The original direct interval matrix expression was too pessimistic; the corrected
algebraic representation changes neither the search domain nor the fixed budget.
Exact rational coefficients and directed intervals replace floating-point inverse
proposals. Poisson tests preserve uncertain means and all count dependencies.

[cells.json.gz](cells.json.gz) contains the complete partition history;
[summary.json](summary.json) contains the surviving interval. The full proof is
in [THEOREMS.md](THEOREMS.md).

## 2. A specific field class and its exact response error

We use the **21-node, 32-edge Hasse graph** of the shared selected-node causal
order. Each immediate causal relation receives unit conductance, and direction
is ignored only in this auxiliary quadratic form:

    E(f) = sum over cover edges (f_i-f_j)^2,
    field class: E(f)<=1, modulo constants.

This choice is intrinsic to the known finite order, invariant under relabeling,
and avoids counting every transitive relation as another immediate variation.
Unit conductance and the unit energy budget are declared modeling choices, not
measured physical smoothness. No causal relation or Lorentzian operator is
replaced. The energy is fixed for every compared pair.

For weight difference v, extended by zero entries on the four landmarks,

    sup_{E(f)<=1} |v^T f| = sqrt(v^T L^dagger v).

The grounded linear system provides an exact rational certificate and an
extremizing potential. The symmetric relative response gap is invariant under
uniform conductance rescaling, although the absolute response bound is not.

The fixed comparison includes the certified close-law pair and all 18 previously
excluded strong-gap pairs:

| Pair | Original weight gap | Relative response gap on the declared energy class |
|---|---:|---:|
| Close-law row 329 | 0.0434832% | **0.0427318%** |
| Largest weight-gap row 327 | 40.5458% | **39.2773%** |

For row 329, the absolute worst-case difference over E(f)<=1 is enclosed by
**[0.35010025757195529113, 0.35010025757195529114]** in the inherited operator units.
The numbers do not show a dramatic suppression by this particular regularity
class. All original TV certificates remain unchanged. A different response
criterion does not retroactively change the original >20% weight-gap gate.

See [energy_graph.json](energy_graph.json), [energy_pairs.json](energy_pairs.json)
and [energy_summary.json](energy_summary.json).

## 3. Apply the analytic ideas where their hypotheses can be proved

The auxiliary finite graph satisfies the resistance-form conditions. Subdividing
each edge into n=2^m equal edges and assigning conductance n gives an exact
resistance-preserving trace back to every earlier level. The explicit Schur
complements for n=1,2,4,8 agree; the proof covers all dyadic levels. The control
without conductance rescaling fails, giving trace L/n.

This construction has a well-defined **auxiliary metric-graph limit**, with unit
length edges and energy sum_e integral |f'|^2. On its normalized length measure,
the trapezoidal rule with n cells per edge satisfies the sharp bound

    |integral f dmu - Q_n f| <= sqrt(E(f))/(n*sqrt(12*M)),   M=32.

Explicit piecewise-quadratic bubbles attain equality and provide exact controls.
This realizes the energy-dependent error approach discussed by Malmquist and
Strichartz in a model whose hypotheses we establish directly. It does not apply
their fractal theorem to an arbitrary causal set.

The physical transfer is explicitly
**HOLD_MISSING_GEOMETRIC_REFINEMENT_AND_LORENTZIAN_IDENTIFICATION**:
the new subdivision vertices are synthetic, the length measure is not spacetime
volume, and the positive graph Laplacian is not identified with the hyperbolic
d'Alembert operator. No four-dimensional or fractal spacetime limit is claimed.
See [compatibility.json](compatibility.json) and the primary-source references
in [THEOREMS.md](THEOREMS.md).

## Verification and the next justified task

[audit.json](audit.json) records 128 independent exact moment solves, 2,560 exact
moving-interval identities, 261 sampled interval-weight enclosure checks, all
64 complete covers, and the predetermined refinement priority. It also checks
energy duality, permutation and scale behavior, four exact subdivision/bubble
levels, and five rejection controls. Sampling audits implementation; interval
algebra and the written proofs establish whole-cell claims.

```sh
python -B research/lorentz_local_dalembert/continuous_energy/ce_run.py --verify
python -B research/lorentz_local_dalembert/continuous_energy/ce_energy.py --verify
python -B research/lorentz_local_dalembert/continuous_energy/ce_compat.py --verify
python -B research/lorentz_local_dalembert/continuous_energy/ce_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/continuous_energy/SHA256SUMS
```

The next targeted task is a joint-law obstruction or closeness certificate on
the **single remaining node-15 interval**, retaining its count correlations.
The present budget is closed. Further refinements or changes of field class
must be declared as a new experiment. Coordinated moves, other reference
geometries, arbitrary pair comparisons and physical continuum accuracy remain
outside this result.
