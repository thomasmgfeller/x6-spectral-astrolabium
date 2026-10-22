# Eigenzeit: fixed-anchor shape search with full count-law coupling

SPDX-License-Identifier: Apache-2.0

**No strong pair found in the fixed search. A small genuinely shape-dependent
statistical lower bound is certified. All scientific HOLDs remain.**

Following PR94, this search changes shape while keeping all four landmarks,
the root, outer interval, density and physical scale fixed. A common Poisson
cloud and a proved cone-boundary volume bound control the joint law of all 90
counts, overlaps of any order, and optional total count. No Gaussian approximation,
Monte Carlo confidence or covariance-only proxy is used.

| Result | Value |
|---|---:|
| Fixed candidates | 288 |
| Exact order/margin/rank passes | 252 |
| Actual causal-order changes | 32 |
| Margin-only rejections, order unchanged | 4 |
| Best symmetric relative weight gap | 0.00365762% |
| Selected pair TV upper bound | <0.25 |
| Best possible equal-prior classification accuracy | <62.5% |
| Minimax expected weight error / fixed base norm | >=0.00137161% |
| Strong gate: disjoint 10% relative-error balls | Not met |

The smaller lower bound is not an improvement on PR94's magnitude: it applies
to a more restricted family with landmarks and outer scale fixed. The search
shows that shape uncertainty can affect weights even with those anchors fixed,
but provides no evidence of a large unavoidable error.

**Do not infer stability from this negative result.** Only single-support-point
axis motions were searched, and the sufficient coupling bound is conservative.
The next justified improvement is a tighter joint-membership-law bound and
coordinated shape changes. This finite search is complete and will not be
expanded merely by repeating the same trials.

See [proof and limitations](THEORY.md), [fixed contract](contract.json),
[all candidates](candidates.json), [exact witness](witness.json),
[summary](summary.json), and [independent audit](audit.json).

## Reproduce

From the repository root:

```sh
python -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
python -B research/lorentz_local_dalembert/shape_coupling/sc_run.py --verify
python -B research/lorentz_local_dalembert/shape_coupling/sc_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/shape_coupling/SHA256SUMS
```

Independent controls check 8,748 exact cone comparisons, including 484 changed
memberships, and compare both rational weight vectors against a separate SVD
minimum-norm solve. The four margin-only rejections are independently checked
to retain their order and solvable moment systems. Full replay retains every
rejected candidate and verifies the deterministic selection.

The observation contract excludes full B causal matrices, embedded coordinates,
new measurements and A-selection likelihood. No claim is made about physical
validation, original-realization confidence membership, continuum accuracy,
global stability or 10% impossibility.
