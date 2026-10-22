# Eigenzeit: a proved full-law close pair and a homothety stopping rule

SPDX-License-Identifier: Apache-2.0

**A genuine but small conditional statistical lower bound is established.
Uniform scaling is ruled out as a close-law 10% counterexample in this family.
All scientific HOLDs remain.**

This follows PR93, which showed that the earlier shape-deformed pair was
statistically distinguishable. Here geometry 0 is compared with its exact
uniform dilation at fixed known density. The complete recorded count/overlap
channel, including optional total B count, reduces analytically to two Poisson
counts. No Monte Carlo or Gaussian approximation is used.

| Quantity | Deterministically certified result |
|---|---:|
| Frozen scales checked | 1,000 |
| Scales with TV upper bound <=1/4 | 592 |
| Selected scale | 62537/62500 = 1.000592 |
| Full count-channel TV upper bound | 0.249630486 |
| Best possible equal-prior classification accuracy | <=62.481525% |
| Weight gap / base weight norm | about 0.118295% |
| Minimax expected weight error / base norm | >=0.04438246% |
| Probability of weight error >=half the gap, for at least one geometry | >=37.518475% |
| Achievable classification accuracy for any feasible dilation with disjoint 10% error balls | >=99.798944% |

The close pair is far below the scale needed for a 10% impossibility result.
The final row proves that increasing the uniform dilation cannot fix this:
one recorded interval count already distinguishes every qualifying dilation.
The sensible next search changes **shape**, retaining all atom-law dependence,
with a certified information-distance constraint. Another unconstrained search
for confidence-set diameter would not answer this statistical question.

See [complete proof](THEORY.md), [fixed contract](contract.json),
[exact certificate and finite grid](certificate.json), [controls](audit.json).
The new witness is fully specified by the frozen source geometry and rational
scale; no approximate optimizer coordinates are required.

## Scope

Conditional on the selected-node causal order, free absolute landmark lengths,
and the stated finite count channel. Density is known and fixed. This is not a
claim about observing the complete B causal matrix, coordinates, extra geometric
measurements, or the A selection likelihood. It does not assert membership in
the previous realized confidence set. The target is the discrete quadratic
moment weight vector, not continuum or smooth-field error. The denominator in
the expected-loss bound is the same fixed base norm under both hypotheses.
No 10% reconstruction guarantee or global instability conclusion follows.

## Reproduce

From the repository root:

```sh
python -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
python -B research/lorentz_local_dalembert/full_law_scaling/fl_run.py --verify
python -B research/lorentz_local_dalembert/full_law_scaling/fl_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/full_law_scaling/SHA256SUMS
```

Exact rational/interval certificates are replayed. Independent small-mean
Poisson distribution enumeration checks the affinity/TV inequalities and an
atom-splitting control checks the dependence reduction formula. Those floating
controls are sanity checks; the mathematical certificate uses exact bounds.
