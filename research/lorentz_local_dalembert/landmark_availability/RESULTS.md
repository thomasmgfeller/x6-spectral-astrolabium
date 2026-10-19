# Landmark diagnosis: enlarging the search cannot rescue the frozen support

19 October 2026. **Retrospective conditional diagnosis complete.**
**INTRINSIC_MOMENT_HOLD, HOLD_PHASE3 and BD-C2 NO_GO remain unchanged.**

The 48 archived target clouds from PR #65 were reconstructed, including all
six unavailable stencils. On the 42 available supports, exhaustive searches
over **all** eligible candidates still yield zero threshold-eight landmark
triples. The 40-candidate cap is therefore not the cause of this failure on
these supports. At the highest density there are up to 75 eligible candidates
on one side, but the best achievable minimum mutual interval count is only
**2**, below the required **8**. The support-count threshold remains eight
throughout that comparison.

This is a diagnosis using previously seen data, not a new validation result.
It addresses the next milestone recorded in the preceding
[intrinsic-calibration report](../intrinsic_moments/RESULTS.md). No weights,
prior sources, archived results or scientific thresholds were changed.

## Exhaustive original-support results

Each numerator counts clouds with a qualifying triple on at least one side.
Denominators include every available stencil; unavailable stencils are shown
separately. Candidate screening always requires eight interior events to every
point of the relevant support. The sweep changes only the mutual-pair
threshold, and is diagnostic.

| Density | Available / all | Triple at k=8: cap 40 | Triple at k=8: all candidates | Triple at k=0: all | Triple at k=2: all | Triple at k=4: all |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2048 | 10/16 | 0/10 | 0/10 | 0/10 | 0/10 | 0/10 |
| 8192 | 16/16 | 0/16 | 0/16 | 0/16 | 0/16 | 0/16 |
| 32768 | 16/16 | 0/16 | 0/16 | 10/16 | 2/16 | 0/16 |

Even k=0 requires a strictly ordered three-element chain. Lowering k does not
validate a frame, its Gram signature or condition number, a calibration, or
the noise guard. These stages were not evaluated by this audit.

## A finite-poset obstruction, with an exact certificate

Suppose s<a<b<c<T, where s is any point that all three future landmarks must
cover and T is the outer diamond endpoint. Three disjoint open intervals
(s,a), (a,b), (b,c), together with a,b,c, lie inside (s,T). Therefore

    N(s,T) >= N(s,a) + N(a,b) + N(b,c) + 3 >= 3k + 3.

The time-reversed statement holds for past landmarks. At k=8, at least 27
interior events are necessary for every constrained point. The common cone
also needs at least 2k+3=19 nonboundary events. Neither condition is sufficient.

These elementary bounds certify impossibility on both sides in **31/42**
available clouds: 10/10 at density 2048, 16/16 at 8192, and 5/16 at 32768.
The remaining 11 clouds also have no valid triple, established by exhaustive
counting rather than by this coarse bound. All side counts, maximizing
witnesses where they exist, and exact bounds are archived in the
[individual records](results/).

## Which constraints consume the available region?

Here the candidate cap is removed and k stays eight. Each relaxation keeps
the root, then constrains landmarks to cover only the indicated archived
points. It does not modify the original operator.

| Density | Full support | Temporal endpoints only | Shell points only | Root only |
| ---: | ---: | ---: | ---: | ---: |
| 2048 | 0/10 | 0/10 | 0/10 | 0/10 |
| 8192 | 0/16 | 0/16 | 0/16 | 11/16 |
| 32768 | 0/16 | 0/16 | 0/16 | 16/16 |

Thus removing only the temporal endpoints does not fix the tested rule;
removing only shell constraints does not fix it either. At high density the
order contains root-covering triples, but none covers the original support
under the count requirements. Root-only triples cannot supply all distances
required by the original construction and cannot be adopted as a repair.

The 40-candidate cap *can* matter in a different diagnostic: for root-only
constraints at density 8192, uncapped availability is 11/16 versus 0/16 with
the cap. At 32768 it is 16/16 versus 14/16. This does not explain the
full-support result, where both searches give zero.

## Exact-volume comparison

Replacing the measured counts by rho*(pi/12)*tau^3 from exact simulation
coordinates, with the same support and causal relation, also gives **0/42**
full-support triples at threshold eight without a cap. For root-only coverage
the exact-volume proxy gives 0/10, 2/16 and 16/16 across the three densities,
versus 0/10, 11/16 and 16/16 from observed counts.

These are mean-volume proxies before conditioning, not the conditional
expectation of counts after data-dependent selection. Screening can choose
different candidates. The comparison shows that replacing noisy counts by
exact volumes alone does not rescue this rule on these finite clouds. It does
not separate boundary effects causally or establish an infinite-density
obstruction. Outside-diamond landmarks, mixed-side triples, overlapping frames
and other embedding constructions were not examined.

## Reproduction and provenance

- All 48 records completed in **68.019 seconds**, peak RSS **434.754 MiB**,
  within the 1200-second / 2048-MiB limits.
- Every inherited computational-source hash and original record hash checked.
  Reconstructed relations, marks, original retained candidate counts and
  original eligible-triple counts agree exactly.
- Independent brute-force enumeration passes on 100 small transitive orders;
  three exact-chain controls check the packing bound at 26, 27 and 28 events.
- Mark-preserving relabeling and transported time reversal pass on the first
  available archived cloud at each density, conditional on its fixed support.
- [VERIFICATION.json](VERIFICATION.json) records complete numerical replay.
  Discrete results agree exactly; continuum values use atol=rtol=1e-9.
  Coordinate byte identity is reported separately; no external replication
  or cross-platform bitwise guarantee is claimed.

The local source snapshot recorded in execution.json is
`4097ccf9940ce4d6e9c0e591ab47cbad04a8e300`. Its public equivalent is
[`7a7dd8baefc1b4c61480bde1a3a23c3eb48bb2ab`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/7a7dd8baefc1b4c61480bde1a3a23c3eb48bb2ab).
Their entire Git trees are identical:
`f882756a8dfaea9de343433f764339fc745b1b75`. Authenticated object transfer
changed commit metadata, not source bytes. Publication occurred during the
diagnostic run; **no public preregistration is claimed** for this retrospective
analysis. The execution manifest preserves the original local source ID.

```sh
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/landmark_availability/verify_audit.py
```

Full [protocol](PROTOCOL.md), [summary](results/summary.json) and
[execution manifest](results/execution.json) are provided.

## Decision for the next construction

Close the candidate-cap explanation for the original fixed supports. Do not
spend another target batch merely increasing 40 or lowering eight. Develop a
construction that explicitly addresses common-cone coverage and reserves
enough causal depth for its landmarks. First compare feasibility in a larger
outer diamond at fixed inner evaluation scale, or use an independently
specified multi-frame/embedding construction. Any choice changes the method
and needs development data, a public protocol and fresh targets before an
improvement claim. This diagnosis does not choose or qualify that replacement.

Known density, flat 2+1 geometry, and fixed selected neighborhoods remain
assumptions. Intrinsic metric accuracy, count-noise robustness, locality,
3+1 validation, curvature and external replication remain open.
