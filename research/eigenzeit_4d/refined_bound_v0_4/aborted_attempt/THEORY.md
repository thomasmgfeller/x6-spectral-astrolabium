# Sharper propagation on the same confidence region

All assumptions and the finite-sample confidence proof in
[v0.3](../joint_region_v0_3/THEORY.md) remain in force. In particular, the
20 observable independent Poisson cells are an invertible transform of the
available interval counts, without the withheld target-interval count.
The region `sum D(y_i || lambda_i) <= 48` and its noncoverage bound
`2^30 exp(-24) < 0.05` are unchanged. Its enclosing ellipsoid is
`sum delta_b^2/U_b <= 96`. No asymptotic cutoff is introduced.

## 1. Exact square-root remainder

For n>0, m>0, direct rationalization gives

```text
-sqrt(m) + sqrt(n) + (m-n)/(2 sqrt(n))
    = (m-n)^2 / [2 sqrt(n) (sqrt(m)+sqrt(n))^2] >= 0.
```

The existing ellipsoid gives `m_j >= L_j > 0` and
`(m_j-n_j)^2 <= 96 v_j`. Hence the absolute remainder is bounded by

```text
r_j = 96 v_j / [2 sqrt(n_j) (sqrt(L_j)+sqrt(n_j))^2].
```

Since `n_j >= L_j`, this bound is no greater than the previous
`96 v_j/(8 L_j^(3/2))`. It improves an analytic bound without truncating
the function or dropping a remainder. The code keeps the same positive
lower-envelope guard. No certificate is issued when that guard fails.

## 2. Four-dimensional PSD bounds

Let `B_b` be the symmetric, whitened matrix coefficient of `delta_b` in
the linear Gram-matrix fluctuation, and `h_b` the corresponding four-vector
coefficient in the inverse-remainder source. These are `B'_b,h'_b` in v0.3.
For any unit vector x, weighted Cauchy-Schwarz gives

```text
||sum_b delta_b B_b x||^2
 <= (sum_b delta_b^2/U_b) (sum_b U_b ||B_b x||^2)
 <= 96 x^T S_B x,
S_B = sum_b U_b B_b^T B_b.
```

Therefore the operator norm of the linear matrix fluctuation is at most
`sqrt(96 lambda_max(S_B))`. Similarly, writing the vector fluctuation as
a matrix times the ellipsoid coordinates yields the bound
`sqrt(96 lambda_max(S_H))`, where `S_H=sum_b U_b h_b h_b^T`.
Both S matrices are positive semidefinite and 4 by 4.

For any symmetric positive semidefinite S, each of the following is a
rigorous upper bound on its largest eigenvalue:

```text
trace(S),  sqrt(sum_ij S_ij^2),  max_i sum_j |S_ij|.
```

The first follows from nonnegative eigenvalues, the second from the
Frobenius norm, and the third from the matrix infinity norm. The code
evaluates all three with outward intervals and selects the smallest upper
endpoint. It does not rely on a floating eigensolver for certification.
The trace choice reproduces the old linear bounds; taking the minimum
therefore cannot weaken the exact analytic bound.

The nonlinear remainder sums use the improved r_j above. All later steps
are unchanged: `epsilon<1`, the exact inverse identity, and

```text
|q-qhat| <= A + H^2/(1-epsilon).
```

Every issued certificate is checked with outward 60-digit arithmetic.
The same exact inequalities `121 qlo >=100 qhat_hi` and
`81 qhi <=100 qhat_lo` certify at most 10% relative proper-time error
throughout the region. For each fixed admissible model parameter, the
unconditional probability of issuing a wrong certificate is at most
`2^30 exp(-24)`. This is neither conditional coverage after selecting
certificates nor simultaneous coverage of all observations.

## 3. Why a sharper remainder cannot solve every case

For each of the five family-3 geometries, one archived high-density
development observation has two explicit integer mean vectors inside the
same unrestricted Poisson region. They are stored in
[REGION_WITNESSES.json](REGION_WITNESSES.json).

Membership is checked without a floating logarithm. For lambda>0,
`log u<=u-1` implies

```text
D(y || lambda) <= (y-lambda)^2/lambda.
```

The sum on the right is evaluated as an exact rational and is <=48.
The case y=lambda=0 contributes zero. Each mean vector produces a positive
reconstructed q and the Lorentzian LDL sign pattern; its q is enclosed by
a separate interval solve. The enclosures satisfy

```text
81 q_large_lower > 121 q_small_upper.
```

Consequently the two allowed 10% estimate intervals are disjoint:
`0.9 sqrt(q_large) > 1.1 sqrt(q_small)`. No single estimate can have
at most 10% relative error on this entire unrestricted region. This is
a finite, checkable obstruction to this region-wide certification rule
on these five observations.

The alternative mean vectors are NOT shown to arise from flat-space
landmark geometries. The witness is therefore not a physical pair of
indistinguishable geometries, not a statistical impossibility theorem,
and not a failure of proper-time reconstruction in general. Restricting
the region to physically realizable means could remove these witnesses;
such a restriction is not implemented here.

## 4. Information-budget experiment

The new method is evaluated with fresh counts at the previous expected
outer count, four times that count and sixteen times that count. The
largest budget is the predeclared primary availability gate; the other
two are descriptive comparisons. Passing at a larger budget does not
close the original-budget gate. All 20 geometries remain the previous
fixed set, so geometric generalization and intrinsic selection remain open.

The 20-cell law samples the joint counts directly. Billions of individual
spacetime points are not generated or claimed as a point-cloud benchmark.
This experiment measures the required statistical information in the
specified model, not the runtime of building those full causal sets.

These derivations and checks are internal research evidence. They do not
assert novelty, independent expert review or proof-assistant verification.
