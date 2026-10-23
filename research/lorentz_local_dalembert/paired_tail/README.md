# Eigenzeit: exact tail tests close 22 more paired directions

**58 of the 60 frozen signed paired rays are now excluded continuously for
step magnitudes [0,0.1]. Two signed directions retain unresolved intervals.**
This adds 22 complete-ray exclusions to PR113's 36. An exclusion rules out
the conjunction of unchanged selected-node order, symmetric operator-weight
gap >20%, and full conditional count/overlap-law TV <=0.25. The remaining
HOLD intervals do not establish a counterexample. General stability is open.

## Result of the fixed-budget pass

The contract covers all 574 subcells retained by PR113. No new directions,
adaptive subdivision, extra coefficient sweep or second optimization pass
was added after evaluation.

| Result on the 574 input cells | Cells |
|---|---:|
| Exact single-count CDF exclusion | 509 |
| Fixed narrow-strip joint-event exclusion | 12 |
| Other disjoint two-count event exclusion | 15 |
| Unresolved | 38 |

The run evaluated 615 marginal events and 91 proposed joint events, plus the
one shared strip certificate. Tests stop for a cell once its exclusion is
proved. The weakest new excluded-cell TV lower bound is
**0.25033638866810490097 > 0.25**. This minimum concerns the newly excluded
cells, not h=0 or the entire deformation domain.

For node 15's negative boosted-x displacement with magnitude
s in [7/160,45/1024], the unchanged event

N(I(15,1)) - 2 N(I(2,15)) <= 787

has uniform full-law **TV >= 0.26263180954790746474**. The two count intervals
are disjoint past/future regions of the same tip. Their law remains unchanged
when another support moves. Exact pullbacks of the paired displacement ranges
apply this certificate to 12 complete input subcells.

The other joint tests also use only I(2,n) and I(n,1) for one moving tip.
Independence is justified by this disjointness, not assumed for the remaining
overlapping counts. Each integer threshold is fixed by the declared geometric
proposal rule before its probability is evaluated. The ranking score is a
proposal heuristic, not an optimality claim or probability bound.

## The two remaining directions

Indices and velocities use the original signed-ray convention from PR111;
s is the nonnegative step magnitude in that signed direction.

| Signed ray | Supports | Boosted axis | Signed velocities (node 15, partner) | Remaining s |
|---:|---|---|---|---|
| 3 | 15, 5 | y | (1, -110478339257/125000000000) | [327/5120, 93/1280] |
| 44 | 15, 17 | x | (-1, 292553733423/500000000000) | [5/128, 107/2560] |

The first interval contains 31 retained subcells and the second contains seven.
In the positive-line parameter used by `summary.json`, the second interval is
[-107/2560,-5/128] on line 45. Numerically, the remaining magnitudes are about
[0.0638672,0.0726563] and [0.0390625,0.0417969], respectively. Endpoints are
conservative: a boundary may already be covered by an adjacent exclusion.

A useful next bounded question is whether joint statistics involving both
moving supports, with their actual overlap dependence retained, close these
two residual intervals. This package neither proves that nor labels a HOLD
cell as a close-law witness.

## Proof and independent checks

See [THEOREM.md](THEOREM.md). The certificates use exact rational geometry,
quadratic extrema over entire cells, directed integer Poisson PMF recurrences,
and explicit infinite-tail bounds. They do not infer continuous coverage from
point sampling or silently normalize a truncated Poisson distribution.

Validation includes:

- Complete deterministic replay of all 574 new cells.
- 2,460 independent 100-digit direct marginal PMF evaluations.
- 199 distinct independent 110-digit direct joint PMF evaluations, auditing
  92 joint event certificates including the shared strip event.
- 2,397 direct reconstructed-geometry checks and 24 exact strip-displacement
  polynomial identities.
- All 30 line covers, representing all 60 signed rays, rebuilt from the
  unchanged predecessor evidence plus these records: 3,375 terminal cells in
  total, including the 38 HOLD cells. Coverage is not exclusion of every cell.
- Three independent exact small-mean factorial-series controls; rejection of
  an overlapping interval pair; a dependence counterexample; an omitted-tail
  negative control; missing-cell controls on all 29 newly processed lines.

The decimal calculations are independent implementation checks. The rigorous
probability certificates come from directed arithmetic and tail inequalities.
The full A-selection/B-graph likelihood, arbitrary coordinated motions, other
reference geometries, physical continuum accuracy and general finite-error
operator stability remain outside this claim.

## Source, freeze and reproduction

Source parent PR113: `db15b4d056713f4644386df620720d0dc2c7cddc`, source tree
`e796b814ee72ec35b109609270cbecd1caca3140`. All five parent workflow runs passed.
The contract, scientific code, proof and source evidence were internally hashed
before the first new event evaluation. Historical results were known; this is
not external preregistration. No predecessor evidence files were edited.

From the repository root, with Python 3.12 and the existing
`finite_poisson_bounds/requirements.txt` dependencies:

```sh
python3 -B research/lorentz_local_dalembert/paired_tail/pft_run.py --verify
python3 -B research/lorentz_local_dalembert/paired_tail/pft_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/paired_tail/SHA256SUMS
python3 tests/python/verify_manifest.py
```

`strip_certificate.json` holds the shared event. `certificates.json.gz` contains
all 574 input-cell decisions, including failed tests and unresolved cases.
`summary.json` is the final family status. A dedicated CI job reproduces the
new package.
