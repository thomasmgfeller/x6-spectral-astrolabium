# Single-count tails exclude all strong candidates in the frozen spatial grid

SPDX-License-Identifier: Apache-2.0

**FINITE_GRID_STRONG_PAIR_EXCLUDED.** All **15** previously unresolved strong-gap
candidates from PR107 are now excluded by certified Poisson count probabilities.
Together with the three already excluded, this settles **all 18** admissible
sampled candidates with symmetric operator gap >20%: each has full count/overlap
law **TV >= 0.40933011992491714757**, exceeding the required TV<=1/4.

The proof uses only one already selected interval count per candidate. No new
geometries, independent-count assumptions, Monte Carlo samples, background-volume
calculations or optimizations are needed. The 512-point spatial search is closed
for this strong-pair question. **The continuous geometry family remains open.**

| Quantity | PR107 Hellinger diagnostic | Certified count tails |
|---|---:|---:|
| Strong-gap sampled candidates | 18 | Same 18 |
| Excluded by full-law TV lower >1/4 | 3 | **18** |
| Unresolved strong candidates | 15 | **0** |
| Weakest full-law TV lower bound among the 18 | 0.1343968 | **0.4093301** |
| Largest-gap row 327: operator gap | 40.5458% | Unchanged |
| Row 327: full-law TV lower bound | 0.1817250 | **0.4735035** |

The earlier certified close-law pair (row 329, gap 0.0434832%, TV<=0.2118268)
remains valid and unchanged. This result removes apparent strong counterexample
candidates; it does not prove reconstruction accuracy or global stability.

## A threshold event gives a genuine full-law obstruction

For Poisson means 0<lambda<mu, the mass ratio is

    p_lambda(n) / p_mu(n) = exp(mu-lambda) * (lambda/mu)^n.

It decreases in n and crosses 1 at

    x = (mu-lambda) / log(mu/lambda).

Thus, for k=floor(x), the event E={N<=k} achieves the single-count total variation:

    TV(Poisson(lambda),Poisson(mu)) = F_lambda(k) - F_mu(k).

Equality at an integer crossing adds a zero difference and causes no problem.
For any event E, even without proving optimality, its probability difference
lower-bounds TV. Because this count is a measurable component of the joint data,

    TV(full count/overlap law) >= F_lambda(k) - F_mu(k).

This lower bound requires no independence between the 90 interval counts.
The single-count TV **upper** endpoint is NOT an upper bound on the full law.

## Enclose the mean and crossing rather than trusting rounded parameters

We reuse the exact rational mean enclosures of PR107 for the same inherited
largest-Hellinger interval. The geometric formula remains
rho*scale^3*pi*q^(3/2)/12. The audit recomputes these means from each exact geometry.
No rounded midpoint mean is used as the true distribution parameter.

For r>=1, t=(r-1)/(r+1) gives

    log(r) = 2 * sum_{j>=0} t^(2j+1)/(2j+1).

After L terms, the remainder lies between zero and
2*t^(2L+1)/((2L+1)*(1-t^2)). Rational mean endpoints and these log bounds enclose x.
All **18 crossing intervals have a unique integer floor**, so their threshold
events are optimal for every pair of means in the corresponding enclosures.
A fixed midpoint-threshold fallback is implemented and tested for ambiguous
crossings; that fallback certifies only an event difference, not optimality.

CDF monotonicity in the mean then gives, with lambda in [a,b] and mu in [c,d],

    F_b(k) - F_c(k) <= event difference <= F_a(k) - F_d(k).

Four endpoint CDF evaluations suffice. All 18 final probability intervals have
width below the frozen **1e-25** target, including uncertainty in the means.

## Certified Poisson CDF without numerical underflow

Set m=floor(mu), unnormalized weight w_m=1, and use

    w_(j-1) = w_j*j/mu,     w_(j+1) = w_j*mu/(j+1).

The normalizing constant cancels the unknown factor relating these weights to
the Poisson probabilities. Every multiply/divide is rounded outward on a fixed
10^-80 integer grid. The downward sum goes all the way to zero; the upward sum
ends at U=m+768. No finite prefix is renormalized as if it were the entire law.

If the upper bound for w_U is wU, the omitted infinite tail is at most

    T = wU * mu/(U+1) / (1-mu/(U+2)).

The bound follows because the first omitted weight is w_U*mu/(U+1), and all
subsequent ratios are at most mu/(U+2)<1. The tail is rounded upward and retained
in the denominator. For k<=U, if A bounds the numerator sum and Z the finite
normalizer sum, the certified CDF interval is

    [ A_lower/(Z_upper+T_upper), min(1,A_upper/Z_lower) ].

Thus the probability certificate uses integer/rational arithmetic and a proved
tail bound, rather than floating-point exp(-mu), which can underflow for the
large means in this dataset.

## Reproduction, controls and scope

[contract.json](contract.json) fixes the 18 inherited rows, their interval
selection, 32 logarithm terms, 80-digit grid, 768 upward terms, precision target
and stop rule before the new calculation. [certificates.json](certificates.json)
records all thresholds, crossing intervals, CDF bounds, normalizers and omitted
tails. [summary.json](summary.json) records the exclusion decision.

[audit.json](audit.json) reports:

- 16 independent exact small-mean CDF checks using an exponential series;
- an independent logarithm check through exponential bounds;
- 72 independent direct-PMF CDF sums using 100-digit Decimal arithmetic;
- reproduction of all 18 geometric mean enclosures;
- full coverage of the inherited 512-candidate grid and all >20% gap rows;
- controls for a dropped tail, ambiguous crossing, reversed means, zero mean,
  negative count threshold and six invalid inputs.

The Decimal comparisons audit implementation; they do not provide the rigorous
certificate. The exact recurrence, directed rounding and remainder proof do.

```sh
python -B research/lorentz_local_dalembert/poisson_tail_obstruction/pto_run.py --verify
python -B research/lorentz_local_dalembert/poisson_tail_obstruction/pto_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/poisson_tail_obstruction/SHA256SUMS
```

The exclusion is limited to the **512 frozen single-node spatial moves from one
fixed base**. All 18 strong-gap rows happen to use step 0.1. In particular, the
unsearched step interval between 0.03 and 0.1, simultaneous multi-node motions,
other reference geometries and different observations are not excluded.
The conditional selected-node law, known density and fixed outer-domain
assumptions remain unchanged; full B causal matrices and A-selection likelihoods
are outside the claim.

The next mathematical step is to use these count-test obstructions to bound
**continuous admissible step intervals**, then bound the operator variation on
the remaining intervals. This would address gaps between sampled steps. A new
search should be justified by an explicit remaining interval or another geometry
family, not by repeating this already settled finite grid.
