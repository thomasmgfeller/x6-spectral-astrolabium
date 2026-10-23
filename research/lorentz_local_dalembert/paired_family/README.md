# Eigenzeit: continuous paired-family screen

**Result: 36 of the 60 frozen signed rays are excluded continuously on step
magnitudes [0, 0.1]; 24 rays retain explicitly archived unresolved intervals.**
This includes the two rays already closed in PR112: **34 rays are newly closed**.
An exclusion rules out the conjunction of unchanged selected-node order,
symmetric operator-weight gap >20%, and full conditional count/overlap-law
TV <=0.25. HOLD does not establish a counterexample. General stability remains
open.

The new calculation covers all remaining 29 lines (58 signed rays), always
moving node 15 and one of the other 15 supports along a boosted x or y axis.
Velocities remain exactly those frozen in PR111. A line parameter h in
[-0.1,0.1] covers both signed rays. It is not independent two-support motion.

## Results and preserved stages

| Stage | Closed signed rays, including PR112 | Remaining signed rays |
|---|---:|---:|
| Previous continuous certificate | 2 | 58 |
| New bounded interval campaign | 25 | 35 |
| Fixed-anchor probability-test transfer | 36 | 24 |

The first campaign evaluates **4,722 cells**, ending with 2,825 terminal cells:
444 operator-gap exclusions, 325 order exclusions, 5 overlap-difference
exclusions and 2,051 HOLD cells. The original evidence is retained unchanged
in `cells.json.gz`, `summary.json` and `direction_summary.json`.

A separately frozen pass transports previously certified one-count tests and
one disjoint two-count test through exact displacement maps. It partitions
only original HOLD cells. The final cover of the 29 new lines has 3,107 cells:
444 gap, 325 order, 5 overlap-difference, 1,759 transferred-law exclusions,
and **574 HOLD subcells**. Subdivision changes cell counts; it does not create
additional independent experiments. The transferred exclusions use 171 distinct
historical marginal certificates plus the inherited joint certificate.

Eight new whole lines are closed, alongside the inherited line. Further signed
half-lines are closed even when the opposite direction retains a HOLD segment.
`combined_summary.json` is the final status. The initial `summary.json` counts
signed rays arising from fully closed lines only; `direction_summary.json`
explicitly accounts for each half-line, including one-sided closures.

The five overlap-difference exclusions use a common-future/past subset bound
for the covariance of N(A)-N(B). Their minimum TV lower bound is
**0.25549665638125688162**, applying only to those five cells, not to h=0 or
the full domain. Shared Poisson points are never treated as independent
interval counts. See [the continuous proof](THEOREM.md) and
[the probability-transfer proof](TRANSFER_PROOF.md).

## Validation

- Complete deterministic campaign replay, including 101 exact equality checks
  for the faster rational exponential sum.
- 319 direct exact nine-moment comparisons against the rank-four update.
- 43,100 direct quadratic checks; moving-endpoint cross terms retained on both axes.
- 410 whole-cell virtual-tip checks (232 future, 178 past), plus 1,230 rational
  virtual-tip evaluations and all five Cantelli events.
- 1,874 full-polynomial displacement identities and whole-cell mean inclusions
  for 1,759 transported subcells; all 2,051 initial HOLD-cell partitions checked.
- Complete covers, deterministic refinements, missing-cell negative controls,
  equal-mean/symmetry controls, and an independent synthetic product-Poisson
  check that detects underestimated variance.

The probability arithmetic of transported historical certificates is inherited
from the pinned source evidence and its audits; it is not presented as a newly
independent replay of every historical tail probability. Their source workflows
passed before publication of this package.

## Freeze and execution correction

`freeze_initial.json` preserves the original scientific freeze. Profiling after
two line summaries showed that repeated Fraction summation dominated runtime.
`pf_fast.py` evaluates exactly the same 80/81-term rational Taylor polynomials
using one integer common denominator. A JSON-key normalization fixes replay of
integer-keyed anchor lookups. `execution_amendment.json` records both changes
and the two already observed summaries; the audit verifies they are unchanged.
No scientific thresholds, directions, stopping rules or probability formulas
were retuned. `freeze.json` pins the final executable forms. The transfer rule
has its own contract and freeze. These are internal freezes, not external
preregistration.

## Reproduce

Run from the repository root, using Python 3.12 and the repository's existing
`finite_poisson_bounds/requirements.txt` dependencies:

```sh
python3 -B research/lorentz_local_dalembert/paired_family/pf_fast.py --verify
python3 -B research/lorentz_local_dalembert/paired_family/pf_audit.py --verify
python3 -B research/lorentz_local_dalembert/paired_family/pf_directions.py --verify
python3 -B research/lorentz_local_dalembert/paired_family/pf_transfer.py --verify
python3 -B research/lorentz_local_dalembert/paired_family/pf_transfer_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/paired_family/SHA256SUMS
python3 tests/python/verify_manifest.py
```

The dedicated CI job uses these commands. Source parent:
`3dc35356fbecae2a0dac485dd64bc0c86a508206`, tree
`2fb3d24023f833b1a446601518f0c2a0dea0a958`.

## Remaining exact intervals

The table uses the **positive-ray line convention** h, so negative intervals
belong to the opposite signed ray. Endpoints are conservative closed intervals;
some endpoints may already be covered by an adjacent exclusion.

| Positive ray index | Moving supports | Boosted axis | Remaining h intervals |
|---:|---|---|---|
| 3 | 15, 5 | y | [327/5120, 233/2560] |
| 5 | 15, 6 | x | [-45/1024, -7/160] |
| 7 | 15, 6 | y | [113/1280, 63/640] |
| 11 | 15, 7 | y | [401/5120, 63/640] |
| 17 | 15, 9 | x | [-45/1024, -7/160] |
| 19 | 15, 9 | y | [79/1024, 1/10] |
| 21 | 15, 10 | x | [-45/1024, -7/160] |
| 23 | 15, 10 | y | [103/1280, 63/640] |
| 25 | 15, 11 | x | [-45/1024, -7/160] |
| 27 | 15, 11 | y | [981/10240, 63/640] |
| 29 | 15, 12 | x | [-45/1024, -7/160] |
| 33 | 15, 13 | x | [-45/1024, -27/640]; [63/1280, 17/320] |
| 37 | 15, 14 | x | [-45/1024, -7/160] |
| 41 | 15, 16 | x | [-45/1024, -7/160] |
| 43 | 15, 16 | y | [233/2560, 63/640] |
| 45 | 15, 17 | x | [-45/1024, -5/128]; [113/2560, 17/320] |
| 49 | 15, 18 | x | [-45/1024, -7/160] |
| 53 | 15, 19 | x | [-45/1024, -7/160] |
| 55 | 15, 19 | y | [383/5120, 63/640] |
| 57 | 15, 20 | x | [-45/1024, -7/160]; [67/1280, 17/320] |
| 59 | 15, 20 | y | [969/10240, 63/640] |

The next bounded question is whether sharper exact marginal or joint count
events close these 24 signed directions, especially the repeated narrow
negative-x strip [-45/1024,-7/160]. The current moment bounds do not answer it.
Arbitrary coordinated motions, other reference geometries, the full A/B data
likelihood, physical continuum accuracy and general finite-error operator
stability remain outside this certificate.
