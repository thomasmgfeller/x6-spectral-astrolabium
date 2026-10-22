# Local sensitivity and a continuous fixed-base exclusion certificate

SPDX-License-Identifier: Apache-2.0

## What is proved, and for which pairs

Let z(k) be exactly the one-parameter causal-diamond flow of PR96, with z(0)
the same fixed reference geometry, and w(k) its minimum-norm physical quadratic
moment weight vector. Outer endpoints, physical scale and known density remain
fixed; inner landmarks and root move. This certificate compares **w(0) with
w(k)**. It does not exclude arbitrary pairs w(k1),w(k2) at nonzero parameters.

The aim is to exclude the strong separation gate

    2 ||w(k)-w(0)|| / (||w(k)||+||w(0)||) > 1/5

throughout the parameter region covered by the current transport certificate
beta(k)<=1/4. The threshold is necessary for disjoint closed relative 10% error
balls. Excluding that gate is not a uniform 10% reconstruction guarantee.

Crucially, beta is an UPPER bound for actual total variation. The statement
beta(k)<=1/4 implies |k|<0.002 does NOT imply that actual TV<=1/4 forces that
parameter restriction. True close-law pairs outside the certificate-covered
region remain possible. No actual-TV lower bound is derived here.

## Local sensitivity, computed exactly

In the existing determinant-one rational Lorentz frame, form the nine moment
rows D(k) from offsets of the 16 support points relative to the root:
linear coordinates, their squares, and their three cross-products. Let
s=D 1 and S=D D^T-s s^T/17. With b=(0,0,0,-2,2,2,0,0,0),

    lambda = S^-1 b,
    a = D^T lambda - (1^T D^T lambda)/17,
    w = (-sum(a),a) / physical_scale².

The rational boost improves numerical conditioning but does not change these
weights: the constant/linear/quadratic exactness constraints and flat
Minkowski d'Alembertian are Lorentz invariant. The exact base solve is also
checked against the original unboosted coordinates.

Differentiate the rational coordinate map and moment equations using exact
rational first-order dual arithmetic:

    lambda' = -S^-1 S' lambda.

Differentiating the weight formula then gives the exact vector w'(0). Directed
square-root bounds yield

    ||w'(0)||/||w(0)|| in
      [0.87251601925448267837, 0.87251601925448267838].

The infinitesimal speed of the PR96 transport upper certificate is
c=sqrt(9U/10), about 138.01338036. Hence the ratio of weight speed to certificate
speed lies in [0.00632196687717567287,0.00632196687717567288]. This is a derivative
with respect to a proved upper certificate, NOT a derivative with respect to
actual TV, Fisher information of the recorded counts, or an inverse information
bound. The local ratio alone cannot be extrapolated into a global statement.

## The entire certificate-covered region fits in the verified interval

PR96 proved beta(k)<=min(1,c*|atanh(k)|), and its implemented beta is the directed
upper enclosure of that expression. The present code verifies with LOWER
bounds that c*atanh(0.002)>1/4. Monotonicity of atanh therefore implies that
any parameter passing that implemented beta<=1/4 gate belongs to
[-0.002,0.002]. We cover this closed interval, which is slightly larger than
the region passing the gate.

## Validated interval linear solves

All interval endpoints are integers divided by 10^30. Addition is exact on
that grid; multiplication and reciprocals use floor/ceiling integer division.
Division rejects intervals containing zero. First-order dual interval arithmetic
encloses both a rational expression and its derivative on each entire cell.
There is no hardware floating-point rounding-mode assumption.

For a cell I with midpoint m, let Q be an archived rational approximation to
S(m)^-1. Floating point is used only to propose Q. Every bound below is checked
with outward integer intervals. The mean-value theorem supplies

    Q S(k) in Q S(m) + [Q S'(I)] * (I-m) = A(I).

Preconditioning before interval enclosure avoids much of the dependency
inflation of the natural product Q[S(I)]. Let E=Id-A(I). If eta=|| |E| ||_infty<1,
then every A(k), and therefore S(k), is invertible. This follows from the
convergent Neumann series. Q need not be trusted as an inverse in advance;
invertibility of the square product Q S(k) establishes invertibility of both.

For A(k)x=b(k), choose any fixed midpoint proposal x0. Enclose the residual
r=b-A x0 and write x-x0=r+E(x-x0). With a_i=sup|r_i| and M_ij=sup|E_ij|,

    |x-x0| <= max(a)/(1-eta) * 1.

This is a proved initial enclosure. From any valid componentwise radius R,
a+M R is another valid enclosure. The code intersects the old and new radii
for 12 iterations, always rounding upwards. The conclusion is inclusion, not
an unchecked residual tolerance or iterative convergence claim.

Apply this solve first to A lambda=Q b, then to

    A lambda' = -(Q S') lambda.

Centered mean-value enclosures for D and the solved multipliers enclose every
component of w(k) and w'(k) on the cell. Squared endpoint maxima and directed
square roots bound their Euclidean norms. Because S is invertible throughout,
there is no unobserved rank singularity between sampled endpoints.

## Cover, bounds and stopping rule

The prescribed partition sequence is 64,128,256,512,1024 cells. Stop at the
first gap-free cover with a strong-gate exclusion, otherwise report unresolved.
The first natural-interval implementation failed the contraction test at the
first cell of every level. This is recorded in initial_attempt.json. Rewriting
the SAME interval problem using the centered preconditioned mean-value form
resolves numerical enclosure inflation, without expanding the domain or budget.
The revised attempts are all archived:

| Cells | All inverses certified | Symmetric gap upper |
|---|---|---:|
| 64 | yes | 0.976968 |
| 128 | yes | 0.372784 |
| 256 | yes | 0.166800 |

The union of the 256 closed cells is exactly [-0.002,0.002], with shared endpoints
and no gaps. Each cell bounds d(k)=||w(k)-w(0)||/||w(0)||. Their maximum obeys

    d(k) <= 0.15395951106632971072.

The reverse triangle inequality gives ||w(k)|| >= (1-d)||w(0)||. Consequently,

    2||w(k)-w(0)||/(||w(k)||+||w(0)||)
      <= 2d/(2-d)
      <= 0.16679971212902427196 < 1/5.

This bound is conservative; it is an upper certificate, not a newly observed
16.68% change. The sampled PR96 changes were around 0.16%. The conservative
uniform derivative bound (458.3923 relative units per k) is also archived;
it is much looser than the exact local derivative and is not used to claim
small derivative throughout. The direct weight enclosure is the useful bound.

The strong fixed-base gate is now excluded on the whole covered interval, not
merely the earlier 40-point grid. No further refinement is needed for this
stopping decision. This does not prove stability over arbitrary geometries,
exclude other reference points, exclude other conformal directions, or exclude
true close-law pairs outside the current upper-certificate gate.

## Verification and reproducibility

Replay reads the sealed rational Q proposals; it never relies on reproducing
BLAS inverses bit for bit. It rechecks every attempted cover and every interval
operation used in the certificate. Independent controls include rational endpoint
arithmetic, exact Cramer-rule systems, rejection of a zero divisor and a useless
preconditioner, exact point solves inside selected cells, and centered differences
of independently solved rational weights. The finite-difference check is a
control only; the local derivative is exact and the continuum proof uses the
interval argument above. The initial implementation failure is retained.

## Reference

S. M. Rump, *Verified bounds for least squares problems and underdetermined
linear systems*, SIAM Journal on Matrix Analysis and Applications,
https://doi.org/10.1137/110840248, provides background on validated linear solves.
The elementary Neumann/residual proof needed by this implementation is given
above in full. No external numerical claim is used for the certificate.
