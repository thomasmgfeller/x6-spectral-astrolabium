# Eigenzeit: finite error bounds with Poisson coverage

SPDX-License-Identifier: Apache-2.0

**22 October 2026 — coverage proved; full-radius accuracy not certified.**

This executes the two next mathematical tasks after PR88: derive a finite
upper error bound, and connect the admissible count region to the actual
correlated Poisson model. It uses the same 20 archived candidate B0 packets,
with no new clouds, optimization runs, truth coordinates or field inputs.

| Question | Result |
|---|---|
| Can count uncertainty have a proved sampling interpretation? | Yes. A simultaneous box for all 1,736 means has coverage at least 97.8667%, conditional on the independent A selection and the stated Poisson model. |
| Can a finite operator-error upper bound be proved? | Yes, with an explicit sufficient matrix-perturbation criterion, checked by rational arithmetic. |
| Does it certify <=10% weight error on the full confidence box? | **0 of 19** computable reference cases. The twentieth retains its prior count HOLD. |
| Is local finite stability certified? | Yes, all 19 cases on much smaller boxes; these have **no coverage claim**. |
| Does the PR88 ambiguity survive the new count region? | Yes. Both exact geometries are strictly inside; their weight gap remains 14.82%. |
| Is physical/smooth-field accuracy now established? | No. Field regularity, discretization and response-scale terms remain separate. |

The confidence percentage describes coverage of the **mean-count vector**, not
success probability of the research approach, accuracy of the reconstructed
operator, or probability that this archived truth lies in a particular set.
The full-radius failure is a failure of this sufficient upper-bound method;
it is **not** proof that 10% accuracy is impossible or that the actual matrices
are singular. All scientific HOLDs remain and no estimator is adopted.

## Probability bridge

Conditional on A, each selected interval count in the separate B process is
Poisson with its volume mean. Counts can overlap and be strongly dependent.
For c=12, use the conservative Chernoff intervals

$$
L(n)=\max(0,n-\sqrt{2nc}),\qquad
U(n)=n+c+\sqrt{c^2+2nc},
$$

with U(0)=c. A union bound gives

$$
\Pr(\forall j:\mu_j\in[L(N_j),U(N_j)]\mid A)
\ge 1-2\cdot1736\,e^{-12}>0.97866729470924445571.
$$

No interval-independence assumption, Gaussian approximation, or fixed empirical
covariance is needed. The extra overlap observations are not used to narrow
this initial set, so the result is deliberately conservative. The construction
has coverage before B-dependent count/fit/resource filtering; it does not claim
coverage conditional on passing those filters or under optional stopping.
The mean intervals are converted to proper-time-squared intervals using directed
rational pi/square-root/cube-root bounds.

Both exact PR88 witness geometries lie inside the new mean box, with minimum
slack exceeding 15 counts for each geometry. The 7.41% uniform recovery lower
bound therefore also applies to the target set containing these witnesses.
**This is a confidence-set diameter/recovery statement, not a statistical
minimax risk or indistinguishability theorem.** The two full observation laws
have not been proved close. See the bridge in [audit.json](audit.json).

## Upper-bound result

The original intrinsic design D(q) is quadratic in interval values q, and its
target b(q) is linear. We derive exact finite polynomial bounds, then apply a
resolvent bound to M=D P D', P=(I+11')^-1. A fixed exact row transformation
reduces avoidable numerical conditioning without changing the target weights.

The sufficient condition gamma=beta(2 d0 E+E^2)<1 must hold throughout the
whole uncertainty box. At full radius it fails in all 19 computable cases.
The frozen diagnostic grid shrinks that radius by 2^-k. A <=10% relative
weight-error certificate first appears at k=16,...,19 depending on the case.
Those artificial boxes are 65,536–524,288 times narrower than the conservative
full box. **These factors are not necessary measurement improvements or sample
size predictions.** They quantify how conservative this proof is on these
inputs; smaller uncertainty sets must be statistically justified separately.

For the earlier witness's source cloud 09, k=18 gives a proved relative
weight-error upper bound of 8.493% around its reference. Its full box does not
satisfy the sufficient criterion. There is no contradiction with the 14.82%
pair: the small box and the full confidence box are different sets.

A separate global norm envelope on the restricted domain already assumed to
satisfy the inherited cond(D)<=1e5 gate is finite in all 19 cases, but ranges
from about 5.96e7 to 1.58e8 in weight norm. The corresponding absolute error is
at most that envelope plus the reference weight norm. These bounds are far too
large for useful accuracy, and the true geometry's conditioning gate is not
established by the confidence theorem. They cannot be promoted to unconditional
operator-error guarantees.

## What is now resolved and what comes next

[THEORY.md](THEORY.md) supplies complete proofs of the confidence box, finite
weight perturbation bound, restricted envelope, and a separate C3 Taylor
remainder for continuum fields. For a specified smoothness bound M3,

$$
|w^T f-\Box f(x_0)|
\le \frac{M_3}{6}\sum_{j\ne0}|w_j|\,\|x_j-x_0\|^3.
$$

Weight uncertainty and field-measurement error add their own norm bounds.
Relative scalar accuracy also needs a nonzero lower bound on the continuum
response. We have not supplied arbitrary physical smoothness/radius constants.

The next work should tighten the **joint** admissible geometry set using the
Poisson overlap structure and exact geometry/order constraints, and fix the
intended field class and error scale. Another batch of optimizer starts would
not turn the current sufficient bound into a global certificate. Conversely,
the present negative certification outcome does not justify abandoning the
physical reconstruction approach. It identifies the remaining proof gap.

## Evidence and reproduction

- [PROTOCOL.md](PROTOCOL.md), [contract.json](contract.json), and [freeze.json](freeze.json)
  pin the rule, source family, target, dyadic grid and 54 source/code hashes
  before evaluation. This is a local freeze on known data, not preregistration
  of a new independent experiment.
- [summary.json](summary.json), [execution.log](execution.log), and all 20
  [result records](results/) include failed full-box certificates and the count
  HOLD. The console capture contains 19 lines; cloud 31 is fully present in
  its result file and the 20-record summary, and independently replays exactly.
  The full audit ran in about 10.74 seconds locally.
- [fp_verify.py](fp_verify.py) recomputes all 20 records exactly using archived
  pivot proposals, checks the prior witness against the new box, and runs seven
  synthetic controls. No Monte Carlo coverage claim is used.
- [crosscheck.wl](crosscheck.wl) and [Wolfram output](crosscheck_result.txt)
  independently verify the scalar probability algebra and weight-energy
  identity. The full rational audit is separate from these symbolic checks.
- [SHA256SUMS](SHA256SUMS) inventories the package. Existing scientific evidence
  and thresholds remain unchanged.

From the repository root, Python 3.12:

```sh
python -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/finite_poisson_bounds/fp_verify.py
```

To repeat the original evaluation separately, use a disposable checkout and
remove only this package's `results/` and `summary.json` before running
`fp_run.py`. Keep the published outputs. New numerical QR pivot proposals may
differ by platform; the verifier uses the archived proposals and checks their
invertibility and identities exactly.
