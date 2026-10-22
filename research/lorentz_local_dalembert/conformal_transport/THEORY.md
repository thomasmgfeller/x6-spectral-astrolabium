# Causal-diamond transport and a quadratic Poisson information bound

SPDX-License-Identifier: Apache-2.0

## Experiment and changed restriction

Condition on the same selected-node order and 90-interval measurement design.
Both geometries are embedded in flat 2+1 Minkowski space at the same known
homogeneous density. Their outer endpoints, physical normalization, outer
interval I(3,0), and surrounding physical B diamond remain fixed. Inner
landmarks, root and support points move together. Thus this family deliberately
relaxes PR95's fixed-inner-landmark restriction; it is not a new result within
that narrower family.

The channel is all 90 counts, overlaps of any order and optional total B count.
We exclude embedded coordinates, the full B causal matrix, extra geometric
measurements and the A-selection likelihood. All selected intervals lie inside
the fixed outer interval. Its duration is less than the surrounding physical
diamond's 3/2, so a common placement remains feasible throughout the family.
The density remains homogeneous in both physical models. A nonuniform density
appears only in the mathematical change of variables used for comparison.

## Exact rational conformal map

Use Minkowski product <x,y>=x_t y_t-x_x y_x-x_y y_y. Let p=z3, q=z0,
V=q-p, c=(p+q)/2 and R²=<V,V>/4. For X=z-c set Q=<X,X>, v=<V,X> and

    D = 1 + k*v/R² + k²*Q/R²,
    Omega = (1-k²)/D,
    T_k(z) = c + [(1-k²)X + V*(k*(R²+Q)+k²*v)/(2R²)]/D.

Everything is rational for rational inputs and k. No square root is needed to
move a point. In the rest frame of the diamond, null radial coordinates
u=t+r and v=t-r each transform as

    f_k(u)=(u+kR)/(1+ku/R).

For |k|<1, this maps [-R,R] monotonically onto itself. Hence T_k is a bijection
of the diamond, fixes its two tips, and has inverse T_-k. Composition obeys
T_j T_k = T_((j+k)/(1+jk)), so s=atanh(k) is the additive group parameter.

Direct substitution, or differentiating the rational map, gives

    <T_k(x)-T_k(y),T_k(x)-T_k(y)> = Omega(x) Omega(y) <x-y,x-y>,
    (dT_k)^T eta (dT_k) = Omega² eta,
    det(dT_k) = Omega³ > 0.

The denominators are positive on the diamond. By continuity from k=0, future
orientation is preserved. All causal intervals are mapped onto their deformed
counterparts, not merely their endpoint orders. The certificate checks all
210 selected-node interval identities exactly for each candidate. It uses the
actual affine-frame determinant: the old triangular-coordinate gauge is not
preserved and cannot be assumed here.

## Pull back the observation law

Extend T_k by the identity outside the outer interval, inside the fixed physical
B diamond. The boundary has zero volume; differentiability across it is not
needed for this measurable bijection. Given a homogeneous B Poisson cloud N,
counting points in T_k(I_i) is exactly counting T_-k(N) in I_i. The same holds
simultaneously for every overlap, and total count is preserved by the bijection.

The pulled-back cloud is Poisson with transformed intensity. The observations
are therefore a common deterministic function of either the homogeneous or
the transformed Poisson process. Data processing bounds their total variation
by that of these two auxiliary process laws. This does not compare physical
point coordinates as observables, and does not claim that B causal relations
across the boundary are preserved by the piecewise extension.

For intensity densities lambda0,lambda_s the Poisson affinity is exp(-J/2),
where J=integral (sqrt(lambda_s)-sqrt(lambda0))². Cauchy-Schwarz gives

    TV(observation laws) <= sqrt(1-exp(-J)) <= sqrt(J).

This retains all dependence and does not enumerate or approximate membership
atoms. The point-process law used for this bound is an auxiliary experiment.

## Quadratic bound by the flow speed

On the outer interval D, pushing square-root densities forward defines a
unitary group on L²(D,dx):

    U_s f(y)=sqrt(det dT_-s(y))*f(T_-s(y)).

Its infinitesimal generator is A f=-v·grad f-(div v)f/2, where v is the vector
field generating T_s. In rest coordinates,

    v_t = R-(t²+r²)/R,
    v_x = -2t*x/R,  v_y = -2t*y/R,
    div v = -6t/R.

For the constant square-root intensity f=sqrt(rho), Af=3t sqrt(rho)/R.
The physical interval has volume 2*pi*R³/3. Its spatial section at time t has
area pi*(R-|t|)². Therefore

    E_uniform_D[t²/R²]
      = [2 integral_0^1 u²(1-u)² du] / [2 integral_0^1 (1-u)² du]
      = 1/10,
    ||Af||² = (9/10)*U,

where U=rho*Vol(D) is the outer mean count (including the physical scale³).
The smooth formulas on the bounded diamond show f is in the generator domain:
for s in a compact finite range, denominators stay uniformly positive and the
square-root Jacobian and its derivative are bounded, permitting L²
differentiation. The flow stays inside D; there is no outward boundary term.

Since U_s is unitary, ||d(U_s f)/ds||=||U_s Af||=||Af||. Integrating in L² gives

    sqrt(J)=||U_s f-f|| <= |s|*sqrt(9U/10),
    J <= (9/10)*U*atanh(k)²,
    TV <= min(1, sqrt(9U/10)*|atanh(k)|).

Outside D the intensity does not change, so it contributes zero. The same
bound holds for either sign and either pullback convention. Unlike the earlier
membership-change union bound, this argument accounts for probability mass
redistribution under a smooth transport. It is a deterministic bound under the
stipulated model, without Monte Carlo confidence qualifications.

## Rational certification and finite search

U is enclosed by the existing exact pi/square-root routines. For x=|k|,
atanh(x) is bounded below by its first 12 nonnegative series terms and above
by adding x^25/[25(1-x²)]. Directed square roots give a rational TV upper bound.
All 40 candidates k=±j/10000, j=1,...,20 are fixed in the contract. The chosen
pair maximizes the lower symmetric relative weight gap among candidates with
TV upper <=1/4 and passing exact order/margin checks. Both selected weight
vectors are solved rationally and pass intrinsic conditioning gates.
No Monte Carlo selection penalty applies to exact valid bounds. The contract
and hash freeze are reproducibility evidence, not external preregistration.

For D_w=||w1-w0|| and beta a proved TV upper bound, integrating the triangle
inequality against min(p0,p1) yields, for every estimator,

    max_g E_g ||w_hat-w_g|| / ||w0||
       >= (D_w/||w0||)*(1-beta)/2.

The denominator is the same fixed base norm in both hypotheses. The optimum
equal-prior classification accuracy is at most (1+beta)/2. Disjoint relative
10% weight-error balls require 2D_w/(||w0||+||w1||)>1/5.

## Result and limits

All 40 candidates preserve exact order and the inherited separation margins;
36 pass the TV gate. At k=-9/5000 the symmetric relative gap is about 0.157502%,
TV <=0.248424353, and the expected weight-error lower bound is 0.05922024% of
the fixed base norm. The generalized old slab bound on this SAME pair is
5779.2054 before clipping, hence only TV<=1. The new comparison is informative.

No candidate meets the strong weight-separation gate. This is not a theorem
excluding all conformal flows, other shape families, or statistical instability.
The operator target remains the discrete quadratic moment weight vector; no
smooth-field, continuum or physical accuracy conclusion follows. Inner
landmarks move, so comparisons of gap magnitudes with PR95 are not controlled
method-only comparisons. The same-pair TV-bound comparison is controlled.

## References and attribution

- L. Leskela, *Information divergences and likelihood ratios of Poisson
  processes and point patterns*, arXiv:2404.00294,
  https://arxiv.org/abs/2404.00294 — Poisson information-distance formulas.
- M. Arzano, *Conformal quantum mechanics of causal diamonds*, JHEP 05 (2020)
  072, https://doi.org/10.1007/JHEP05(2020)072 — background on diamond-preserving
  conformal flows. No quantum or thermal interpretation is used here.

The explicit flow, L² speed calculation, 9/10 coefficient, finite geometric
checks and application to this observation channel are derived above. Numeric
quadrature in the audit is an independent sanity check, not the proof.
