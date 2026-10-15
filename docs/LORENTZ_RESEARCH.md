# Lorentzian priority: reference, comparison and research gates

Research baseline: 11 October 2026; navigation/window reconciled 15 October 2026.
The user's priority is Lorentzian spectral
geometry. Both Lorentzian tracks run first; the three existing signal/graph
controls follow with 24 cases each. The authorised exclusive cutoff is
19 October 2026 at 00:00:00 Europe/Zurich (`2026-10-18T22:00:00Z`), including
Sunday 18 October. See `MATH_AGENT.md` for control and the
[central module register](MODULE_REGISTRY.md) for source pins and evidence.

This page describes the scheduled main-branch n=3..5/propagator baseline.
The full n=6 atlas generator remains on `research/lorentz-v1-workpackages`.
The byte-identical independent verifier and fixed atlas are also available in
main through the [offline reference suite](OFFLINE_REFERENCE.md), with exact
source provenance. Fingerprints, Fabric and Neutral Discovery
have later branch sources. Their exact entry points, finite results and next
acceptance gates are in the register. They are not automatically part of this
scheduled agent or evidence of a general reconstruction theorem.

## Research reference and exact replication

Yazdi, Letizia and Kempf, *Lorentzian Spectral Geometry with Causal Sets*,
CQG 38 (2021), [preprint v1](https://arxiv.org/abs/2008.02291v1), studied
orders up to nine elements. Tables 1–2 give our small-order targets. Additional
invariants and quill perturbations improve discrimination; finite enumerations
do not settle reconstruction for arbitrary orders.

Our first track independently enumerates binary upper-triangle relations on
3–5 elements, retains transitively closed relations, and identifies isomorphic
orders by all permutations. Every finite order has a natural labeling, so this
covers these sizes. Reverse orders remain distinct unless isomorphic. This
is not a replication of the full nine-element study.

For `C_ij = 1` iff i precedes j, we use `S=C+C.T`, `A=C-C.T`, `K=SA-AS`.
These are fixed nonzero multiples of the self-adjoint part, anti-self-adjoint
part, and their commutator. Scaling preserves equality classes of spectra.
We classify tuples of characteristic polynomials using arbitrary-precision
integer Faddeev–LeVerrier with exact division. No tolerance or eigenvalue
rounding decides a collision. A has imaginary eigenvalues; multiplying it
by i would yield equivalent classification.

| Elements | Nonisomorphic orders | Classes from three spectra | Classes adding ordered minimal/maximal counts |
|---|---:|---:|---:|
| 3 | 5 | 4 | 5 |
| 4 | 16 | 14 | 16 |
| 5 | 63 | 53 | 63 |

These literature expectations are not newly discovered numbers. A mismatch
fails the run. Every representative, polynomial, relabeling check and unresolved
group is retained in `lorentz_orders.json`. Opposite three-element forks
illustrate lost time orientation. Minimal/maximal counts form an ordered pair.

## Two sequences against a known Lorentzian operator

Jones and Yazdi, *Spectral Density of the Causal Propagator*,
[arXiv:2606.00311v3](https://arxiv.org/html/2606.00311v3), revised 29 September
2026, propose an asymptotic spectral-density conjecture with supporting
examples. It remains a conjecture. We use the established massless 1+1
Minkowski diamond example in equations 11–14 for calibration.

Uniform null coordinates u,v in [-1,1] give a diamond of volume V=4.
Sampling is conditional on fixed N, not an unconditioned Poisson count.
Causality requires both coordinates to increase. In the paper's convention:

```
Delta_c = (C.T - C)/2
H = i Delta_c V/N
```

V/N supplies the integration measure. The continuum positive eigenvalues
combine `1/(n*pi)` for positive integers n and `1/z` for positive nonzero
roots of `tan(z)=2z`. Bisection stays between tangent poles and excludes zero.
Both mode families are included in the sorted analytic reference.

The comparison protocol is fixed before the comparison sequence:

- Sizes 64 and 128, three independent samples per size and sequence.
- Reference seed base 20260805, reused identically each slot.
- Comparison seed base changes with the recorded slot. Samples are independent
  of the reference and not nested across sizes.
- Metric: relative L2 error of the largest eight positive eigenvalues against
  the analytic values. Also report distance between sequence mean spectra and
  each individual error, with no selective seed/rank removal.
- Hermiticity, plus/minus pairing and relabeling checks use absolute tolerance
  1e-10. They test implementation, not physical Lorentz invariance.
- Archive coordinates, seeds, normalization and every positive eigenvalue in
  `lorentz_propagator.json`, separately from the exact polynomial track.

The frozen sample is a reproducibility reference; the analytic spectrum is
the comparison target. Neither sequence is an empirical spacetime dataset.
Three replicates cannot justify a reliable uncertainty model, p-value or
general convergence rate. Errors need not fall on every increase of N. We do
not fit an exponent or test the general 2026 conjecture at these sizes. Small
eigenvalues near the discreteness scale require a justified cutoff later.

## Priorities and evidence gates

| Priority | Work | Completion criterion |
|---|---|---|
| 1, implemented | Exact n=3..5 replication and two finite-diamond sequences | Literature counts match; complete artifacts and numerical checks |
| 2, next | Larger collision corpus and quill-response invariants | Independently checked isomorphism; explicit unresolved pairs; comparison to 2021 method |
| 3 | Finite-size study of the 1+1 propagator | Preregistered sizes/ranks, more seeds, justified cutoff, uncertainty estimates and compute budget |
| 4 | Restricted stability or identifiability theorem | Explicit assumptions, proof, counterexamples and novelty review |
| 5 | Other geometries or dimensions | Correct dimension-dependent Green function, volume measure and independent controls |
| Supporting | Held-out denoising benchmark and source agents | Untouched test sequences, clean targets or defensible proxies, fair comparator tuning |

For the main scheduled baseline, items 2–5 and the full denoising comparison
remain outside its executed scope. Item 2 now has a finite n=6 branch result
as recorded above; larger/general reconstruction questions remain open. Good finite
tests do not automatically extend the runtime window or establish a physical
interpretation. A useful near-term output is an independently checkable
benchmark and negative-result corpus. New mathematics requires a proved
statement and separate literature/expert review.

## Forecast revision

Earlier probability ranges in `MATH_FORECAST_2026_10.md` concern a finite-signal
and undirected-graph program. They are retained as historical judgments and
must not be relabeled as probabilities for Lorentzian discovery. There is no
calibrated success estimate here. Known-case replication is directly testable;
a general reconstruction theorem or Lorentzian Weyl analogue is a much larger
research goal.

The scheduled review reads evidence and primary literature, explains changes
and proposes the next falsifiable question. It cannot promote a conjecture to
a theorem, self-modify code or extend the pilot.
