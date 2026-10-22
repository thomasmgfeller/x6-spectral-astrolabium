# The remaining continuous interval is excluded by a joint count event

SPDX-License-Identifier: Apache-2.0

**All 64 declared fixed-base spatial rays are now excluded as strong close-law
counterexamples on the entire interval h in [0,0.1].** The one interval left
open by [PR109](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/109)
has the uniform bound

    TV(full reference law, full moved law) >= 0.26376136265637454647 > 1/4.

This excludes the required closeness gate. The result is deterministic and
applies throughout h in [45/1024,51/1024] for node 15 moving in the negative
boosted x direction. It closes all 30 remaining terminal cells without another
geometry search or additional spatial subdivision.

## Why the joint distribution changes the conclusion

Use two existing observations:

- X counts the interval I(2,15), before the moving node.
- Y counts the interval I(15,1), after the moving node.

These two regions are disjoint for every geometry under consideration. The
Poisson model therefore makes **these two counts** independent. Other counts
and overlaps retain all their original dependencies; they are not factored.

The fixed event is **Y - 2 X <= 787**. Moving the node decreases the mean of X
and increases that of Y, so the two changes reinforce one another in this
statistic. The same event has the following certified probability enclosures:

| Geometry | Event probability, rounded outward for display |
|---|---:|
| Fixed reference | [0.6326194312, 0.6326194313] |
| Any h in the remaining interval | [0.3355380862, 0.3688580686] |

The full-precision reference lower probability minus the moved upper probability
gives the TV lower bound above. A single observed event suffices to obstruct
full-law closeness. This is not a calculation of the exact full-law TV or an
optimal-test claim.

## Continuous coverage and exact arithmetic

The existing 8,217-leaf cover from PR109 is retained intact:

| Exclusion reason | Terminal cells |
|---|---:|
| Operator gap at most 20% | 5,717 |
| Known causal order violated | 1,788 |
| Single-count law separation | 682 |
| New joint-event law separation | **30** |
| Unresolved | **0** |

Exact quadratic extrema and outward volume bounds enclose both means on the
whole remaining interval. Poisson monotonicity reduces the event bound to four
mean-endpoint computations. Directed integer recurrences at 80 decimal digits
retain the infinite tails of both distributions. Each fixed-mean numerical
probability enclosure is narrower than 10^-65; the much wider moved-geometry
range reflects real parameter uncertainty, not numerical rounding.

The [contract](contract.json), [proof](THEOREM.md), [source freeze](freeze.json),
[probability certificate](certificate.json), [summary](summary.json) and
[audit](audit.json) are archived. The fixed event was proposed using already
known geometric means before its certificate evaluation; it is not an
independent-data validation. No Monte Carlo or Gaussian approximation enters
the proof.

## Validation and claim boundary

The independent audit checks six exact factorial/exponential-series examples,
four direct 110-digit PMF sums, six direct reconstructed-geometry checks and
all 64 continuous covers. Negative controls detect omitted-tail normalization
and false independence for identical counts. Six invalid inputs are rejected.
The earlier proof-bearing interval enclosures remain pinned and replayed in CI.

This result excludes the conjunction of **unchanged selected-node order,
symmetric weight gap above 20%, and full count/overlap-law TV at most 1/4**
within the declared family. It does not assert that the movements themselves
are impossible. It does not prove global stability, physical operator accuracy,
or a Lorentzian continuum limit. The auxiliary energy class of PR109 is not
needed for this exclusion.

Stop further refinement of these same 64 rays. The next genuinely different
question is whether **coordinated movements of several nodes** can cancel the
informative count changes while preserving a large operator response. A new
search must first specify that larger domain and retain joint-law constraints;
the present result supplies a negative control for it. Pairs of two non-reference
geometries and other base clouds also remain outside this certificate.

```sh
python -B research/lorentz_local_dalembert/joint_ray_obstruction/jr_run.py --verify
python -B research/lorentz_local_dalembert/joint_ray_obstruction/jr_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/joint_ray_obstruction/SHA256SUMS
```

Use the existing `finite_poisson_bounds/requirements.txt` environment.
