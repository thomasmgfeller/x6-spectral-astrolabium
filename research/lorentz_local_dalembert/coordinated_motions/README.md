# Coordinated support motions: first paired family checked

SPDX-License-Identifier: Apache-2.0

**Result: no strong close-law pair among 420 specified coupled motions.**
The final candidate has a **21.7147018%** symmetric operator-weight gap, but a
two-count event proves **full-law TV >= 0.29903841735657376508 > 1/4**.
The general finite-error stability problem remains open.

This study continues [PR110](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/110)
from source commit `45cfcc3d8432bcab0fcdfc6694aba0f257f5cf48`. That result excluded
64 continuous single-support rays. Here **two supports move at once**, with
velocities chosen to almost cancel the first derivative of a selected count
sum. This paired study covers seven points on each of 60 rays, not the full rays.

## Mathematical restriction

The 90 labeled count means split into 10 fixed entries and 16 blocks of five
entries, each involving exactly one movable support. Four fixed nondegenerate
landmarks give an exact inverse for each support displacement. Hence the
48-coordinate mean map has **exact rank 48**, and preserving all its means
forces every support to remain fixed. A scalar sum can be stationary while
its individually observed components change. Overlap correlations do not erase
a distinguishable marginal. This specializes the earlier identifiability proof;
it does not establish useful finite-noise operator stability.

[The proof](THEOREM.md) also lifts PR110's last-interval TV obstruction to arbitrary
simultaneous motions of the other supports: when node 15 stays on that same
excluded segment, other support motions cannot change its two named marginal
counts. The exact finite displacement inverse is in [structure.json](structure.json).

## Finite results

Node 15 is paired with each of the other 15 supports, using two spatial axes,
two signs and seven steps from 0.0001 to 0.1. The rational velocities make the
relative residual of the chosen aggregate derivative at most 1.21533e-11.
This is a tangent property; finite nonlinear changes are retained and checked.

| Initial screen outcome | Candidates |
|---|---:|
| Causal order or separation-margin rejected | 166 |
| Operator gap at or below 20% | 204 |
| Strong gap, certified full-law TV above 1/4 | 49 |
| Initially unresolved | 1 |
| Total | 420 |

All 50 strong, order-preserving candidates pass the inherited conditioning gates.
The largest operator gap in the admissible order/rank screen is about 41.7896%,
but that candidate is distinguishable at the declared TV gate.

The remaining candidate, row 12, moves node 15 by approximately +0.04726767
and node 5 by -0.05 in boosted x. The original screening lower bound
0.24934433 was **inconclusive**, not a closeness certificate. A separately
frozen follow-up evaluates the event

    X=N(I(2,5)), Y=N(I(5,1)), E={Y-2X<=891}.

The two regions lie in the past and future of the same tip and are disjoint.
The certified probability difference exceeds 0.29903841, excluding this last
point. The original HOLD result is preserved in [summary.json](summary.json);
the combined decision is [joint_summary.json](joint_summary.json). See the
[follow-up proof](JOINT_NOTE.md) and [full certificate](joint_certificate.json).

The finite aggregate itself is not conserved: the two selected anchor-0 mean
changes at row 12 are about -0.60760 and -0.19218. Their first derivatives nearly
cancel at zero; nonlinear curvature of the mean map matters at the sampled step.

## Reproduction and validation

From the repository root, with the inherited finite_poisson_bounds requirements:

```sh
python3 -B research/lorentz_local_dalembert/coordinated_motions/cm_run.py --verify
python3 -B research/lorentz_local_dalembert/coordinated_motions/cm_audit.py --verify
python3 -B research/lorentz_local_dalembert/coordinated_motions/cm_joint.py --verify
python3 -B research/lorentz_local_dalembert/coordinated_motions/cm_joint_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/coordinated_motions/SHA256SUMS
python3 tests/python/verify_manifest.py
```

The independent implementation audit checks 32 exact finite-displacement
identities, 16 rank-three blocks, 5,100 unaffected-interval identities, 60
high-precision derivative balances, all 420 direct order/margin decisions,
204 direct 110-digit marginal CDF sums and four direct 110-digit joint sums.
Negative controls reject a singular landmark frame and the false equivalence
between scalar-sum equality and equality of labeled count laws. Infinite tails
are retained. No floating-point optimizer or Monte Carlo supplies a certificate.

## Decision and next work

Stop extending this finite grid. The useful next task is continuous coverage
of the paired rays, beginning with the node-15/node-5 ray around h=0.05. A joint
event can bound a whole step interval only after enclosing both moving means;
the multi-support operator variation needs its own rank/update bound. Additional
support directions and other base geometries remain outside this finite result.
No general stability, full A/B likelihood, or physical continuum accuracy claim
is made. Source/contract freezes are internal reproducibility records, not
external preregistration or independent peer review.
