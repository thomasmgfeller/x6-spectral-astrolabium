# Eigenzeit: held-out Poisson discrimination of the witness pair

SPDX-License-Identifier: Apache-2.0

**Result: the existing witness pair is distinguishable under the stipulated
Poisson model. All scientific HOLDs remain.** Membership in the same conservative
confidence set does not establish statistical indistinguishability.

| Quantity | Result |
|---|---:|
| Training draws per geometry | 128 |
| Independent held-out draws per geometry | 512 |
| Held-out errors, geometry 0 / 1 | 125 / 111 |
| Empirical equal-prior accuracy | 76.953125% |
| Conservative continuous-model accuracy lower bound | 65.8369018% |
| Full observation law total variation lower bound | 0.3167380366 |
| Numerical validation confidence lower bound | 99.9987711% |

The classifier uses all 90 recorded interval counts, including the 16 omitted
by the earlier reconstruction mask. It was sealed before validation. Shared
Poisson clouds preserve the complete joint count distribution, including
higher-order overlap dependence. Whole-cell integer geometry has an explicit
continuous-law coupling error below 0.002912 per class. No Gaussian surrogate,
validation tuning or replacement witness search is used.

This is a conditional diagnostic for the already selected pair, under ideal
independent model sampling. PCG64 replay is numerical evidence, not proof of
ideal randomness. It gives achievable testing performance and a **TV lower
bound**, not a TV upper bound, physical validation, a statistical minimax risk
bound, or 10% operator accuracy. The earlier set-wise 7.41% bound is not revoked.

See [the fixed protocol](PROTOCOL.md), [proof and scope](THEORY.md),
[summary](summary.json), [independent controls](audit.json), and sealed model.
All 1,280 simulated count vectors and their seeds are archived. No physical
observations or provenance identifiers are used as classifier features.

## Reproduce

From the repository root, with Python 3.12 and g++:

```sh
python -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/poisson_testing/pt_replay.py
python -B research/lorentz_local_dalembert/poisson_testing/pt_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/poisson_testing/SHA256SUMS
```

Replay regenerates every shared cloud without overwriting evidence. Independent
controls compare the compiled kernel with the previous interval classifier and
with Python arbitrary-integer arithmetic at squared distances above int64 range.
Every archived classifier score is also checked with Python integers.

## Next decision

Do not promote this pair to an indistinguishability counterexample. Search for
operator-separated pairs constrained by joint-law closeness, with independent
validation and a proved TV/KL upper bound if claiming a testing lower bound.
In parallel mathematically, investigate which additional joint measurements
support a uniform stability theorem. More optimizer repeats on the same loose
confidence set alone do not resolve that question.
