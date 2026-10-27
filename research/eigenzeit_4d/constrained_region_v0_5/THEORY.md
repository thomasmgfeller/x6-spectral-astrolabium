# Using exact geometric constraints without a global nonlinear search

The model, observable 20-cell Poisson law, confidence region and ellipsoid
from [v0.3](../joint_region_v0_3/THEORY.md) remain unchanged. The improved
square-root and PSD norm bounds from [v0.4](../refined_bound_v0_4/THEORY.md)
are retained. All assumptions are still conditional: flat 3+1 space, known
intensity, fixed labelled timelike-chain landmarks and independent anchors.

## Exact constraints and a corrected point estimate

Write P=[b_p,b_q], d=b_p-b_q, and

```text
q(s) = -d^T G^-1 d,
r_a(s) = b_a^T G^-1 b_a - s_0a,  a=p,q.
```

Every model-compatible mean vector satisfies r_p=r_q=0, as established in
the [necessary norm conditions](../refined_bound_v0_4/REALIZABILITY.md).
For any real coefficients k_p,k_q, held fixed after observing y, define

```text
F_k(s) = q(s) + k_p r_p(s) + k_q r_q(s).
```

On the geometric subset, F_k=q exactly. We bound F_k throughout the entire
original confidence region. This also bounds q on its intersection with
the exact geometric constraints. No approximate feasibility solver or
unproved projection of the confidence region is needed.

The point estimate changes from q(s_hat) to F_k(s_hat). This correction
uses the observed norm residuals; it is not a claim that noisy counts
already satisfy the constraints. The reported proper-time estimate is
the positive square root of F_k(s_hat), with the same known physical scale.

## Choosing coefficients

Let g be the cell-count gradient of q and R the two rows of residual
gradients at the observed center. A floating proposal solves the weighted
least-squares problem for g+k^T R using the fixed ellipsoid weights U.
Coefficients are rounded to integer multiples of 2^-20 and limited to
absolute value 16. An ill-conditioned proposal gives k=(0,0).

This optimization proposes coefficients only. Every allowed dyadic pair is
valid for the proof, and every issued certificate is recomputed with those
exact coefficients using outward interval arithmetic. The proof does not
need a certified optimizer or assume that the gradient approximation is
accurate beyond first order. When varying a possible mean vector in the
region, k is held fixed at its observed value.

## Complete nonlinear remainder

Set X=G_hat^-1 P_hat and H=DeltaP-DeltaG X. Direct expansion gives the exact
matrix identity

```text
P_new^T G_new^-1 P_new - P_hat^T G_hat^-1 P_hat
 = X^T DeltaP + DeltaP^T X - X^T DeltaG X + H^T G_new^-1 H.
```

Let

```text
K = [[k_p-1, 1], [1, k_q-1]].
```

Then F_k=trace(K P^T G^-1 P)-k_p s_0p-k_q s_0q. Its first derivative
retains the cancellation between q and the two residuals before taking
absolute values. Its remaining matrix-inverse term is exactly
`trace(K H^T G_new^-1 H)`.

Use the same exact-center LDL whitening W as v0.4. The existing bound
epsilon<1 implies that the inverse of W^T G_new W has operator norm at
most 1/(1-epsilon). For any symmetric K and symmetric A,

```text
|trace(K H^T A H)| <= ||A||_op trace(H |K| H^T).
```

This follows by diagonalizing K and applying the operator-norm bound to
each resulting vector quadratic form. Here |K| is the spectral absolute
value, not entrywise absolute values. For a symmetric 2 by 2 K with its
off-diagonal entries equal to one,

```text
|K| = (K^2 + |det K| I) / sqrt(trace(K^2)+2|det K|).
```

The formula follows from the two eigenvalues and has a strictly positive
denominator in this case. The implementation uses the exact dyadic
determinant and encloses the formula by directed arithmetic. It adds
2^-40 I to form a strictly positive majorant M, then encloses its Cholesky
factor R_M, where M=R_M R_M^T. This also covers singular K.

The linear cell-count coefficients of `(W^T H) R_M` are eight-vectors v_b.
Weighted Cauchy-Schwarz bounds their sum over the ellipsoid by

```text
sqrt(96 lambda_max(sum_b U_b v_b v_b^T)).
```

The 8 by 8 matrix is positive semidefinite. Trace, Frobenius and maximum
absolute-row-sum bounds enclose its largest eigenvalue; the smallest
validated upper endpoint is used. The exact square-root remainder bounds
from v0.4 add the remaining nonlinear terms. Denote the resulting norm
bound by H_bound and the complete first-derivative/Taylor bound by A_bound.
Then on the whole confidence region,

```text
|F_k(s)-F_k(s_hat)| <= A_bound + H_bound^2/(1-epsilon).
```

Thus the same interval encloses the true q whenever its mean is in the
region and satisfies the exact model constraints. No inverse remainder
or square-root remainder is discarded.

## Certification and fallback

All positive candidates are evaluated at 60 significant decimal digits
with outward rounding. If the corrected estimate's enclosure is positive,
the existing inequalities `121 qlo >=100 qhat_hi` and
`81 qhi <=100 qhat_lo` certify at most 10% relative proper-time error.
Here qhat encloses the corrected estimate F_k(s_hat).

The fixed selection rule uses a validated geometric certificate when
available, otherwise a validated v0.4 certificate, otherwise HOLD. Both
bounds hold on the same original confidence event, including their
data-dependent coefficient and method selection. Consequently no union
penalty is needed for this fallback. For every fixed admissible model
parameter, the unconditional probability of issuing a wrong certificate
remains at most `2^30 exp(-24)`, approximately 0.04054 per observation.
This is not conditional coverage after selecting certified observations,
simultaneous coverage of the experiment, or a guarantee under curvature
or other violations of the flat-space model.

## Validation boundary

The development observations are the published v0.4 data. Fresh validation
uses a new frozen seed, the unchanged twenty geometries, the original
budget and the same 16x budget at which v0.4 remained HOLD. The larger
budget is the predeclared primary gate. Geometric generalization and
intrinsic landmark selection are not tested.

The audit verifies the corrected center separately and tests F_k, with
the certificate's coefficients held fixed, at ambient ellipsoid boundary
points. Such points need not be geometrically realizable, so their raw q
is not the quantity the corrected full-region bound promises to enclose.
At actual model means, the residuals vanish and F_k=q.

These are internal derivations and reproducibility checks. No novelty,
independent expert review or proof-assistant verification is asserted.
