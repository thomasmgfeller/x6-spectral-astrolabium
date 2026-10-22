# Coordinated support motions: a uniform stopping certificate

SPDX-License-Identifier: Apache-2.0

## 1. Observation model and full-law coupling

Keep PR95's reference geometry, four landmarks, root, normalization scale s,
known homogeneous Poisson density rho and physical outer diamond fixed. Move
any of the 16 support nodes by d_i in the same rational Lorentz-boosted frame.
Define

    B(d) = sum_i (|d_it| + sqrt(d_ix²+d_iy²)).

For the statistical interpretation require the same selected-node causal order
and all inherited admissibility gates. The observed data are the 90 interval
counts, overlaps of any order and optionally the total B-cloud count. No
coordinates, full B causal matrix or A-selection likelihood is included.

Under a common Poisson cloud, moving tip i can change future/past membership
only in two slabs of time thickness at most 2 eta_i each, where
eta_i=|d_it|+sqrt(d_ix²+d_iy²). Their intersection with the fixed outer diamond
has combined volume at most 4 A eta_i. A is the same directed spatial projection
area bound as in PR95. The union bound on volume remains valid when slabs
intersect and when many intervals share a tip. Thus its expected Poisson
population is at most M=C B(d), C=4 rho s³ A. Outside this union every interval
membership agrees point by point, so all counts and overlaps agree jointly.

Consequently

    TV(P0,Pd) <= 1-exp(-C B(d)).

This is a sufficient upper certificate, not an equality or a lower bound for
actual TV. Passing its 1/4 gate implies C B(d)<=log(4/3). Use the rational
superset h=(36/125)/C. Since log(4/3)=2 atanh(1/7), a positive-series enclosure
with explicit tail proves log(4/3)<36/125=0.288. Every passing displacement
therefore satisfies B(d)<h. This includes the older linear gate C B<=1/4.
No probability or independence approximation is used.

## 2. Exact operator equations

Let D contain the nine linear/quadratic monomials of support-minus-root
coordinates in its 16 columns. Write H=I-11^T/17, S=D H D^T and
b=(0,0,0,-2,2,2,0,0,0)^T. With lambda=S^-1 b, support weights are
H D^T lambda/s² and the root weight is minus their sum. These are the
minimum-norm quadratic moment weights used throughout the preceding work.

At the rational reference compute S0, lambda0 and Q=S0^-1 exactly. Verify
Q S0=I and S0 lambda0=b. The boosted and original-frame weights agree exactly.
For each support column j, put v_j=D_j-sum_k D_k/17. If p is the derivative of
D_j with respect to one coordinate, direct differentiation gives

    S' = p v_j^T + v_j p^T,
    Q S' = (Q p) v_j^T + (Q v_j) p^T,
    Q S' lambda0 = (Q p)(v_j^T lambda0)+(Q v_j)(p^T lambda0).

The second expression is evaluated before bounding entries; the third is
evaluated before bounding the centered residual. This retains cancellations
that would be lost by multiplying independent absolute entry bounds afterward.

## 3. Mean-value bound using the total budget

All points z+theta*d for theta in [0,1], B(d)<=h, are contained in the rational
coordinate box with radius h around each moving coordinate. Fixed coordinates
remain fixed. Outward fixed-point intervals on this box enclose every derivative
above. Let m_ijt,m_ijx,m_ijy be upper absolute derivative bounds for an entry of
Q S' at support i. For any displacement at that support,

    |m_t contribution + m_x contribution + m_y contribution|
      <= max(m_t,sqrt(m_x²+m_y²)) (|d_t|+sqrt(d_x²+d_y²)).

This follows from the triangle inequality and Cauchy-Schwarz in the spatial
plane. Sum over supports, bound by the largest support coefficient, and apply
the integral mean-value identity. For each matrix entry obtain

    |(Q S(z+d)-I)_ab| <= h K_ab,
    K_ab = max_i max(m_it,sqrt(m_ix²+m_iy²)).

Applying the SAME argument directly to Q S' lambda0 gives a sharper vector
bound r on |Q(S(z+d)-S0)lambda0|. Interval arithmetic rounds every operation
outward at 10^-30; square-root bounds use directed rational integer arithmetic.
The derivative box is a superset. The resulting bound on Q S applies to the
budget ball, not to every point of the larger box.

## 4. Invertibility and centered solve

Let A=Q S(z+d), enclosed entrywise by I+[-hK,hK]. Its verified residual satisfies
||I-A||_infinity <=0.012355855<1. Thus every budgeted S is invertible by the
Neumann-series argument. For e=lambda-lambda0,

    A e = -Q(S-S0)lambda0.

Solve this centered equation with the symmetric vector enclosure [-r,r].
The initial error radius is max(r)/(1-eta). Componentwise refinements
r_new=min(r_old, residual_bound+|I-A|r_old) remain valid: if the old component
bounds contain the error, substitution in the equation gives the new bounds.
The implementation uses outward integer rounding and 12 refinements.

The enclosed D and lambda yield all 17 weight intervals. Sum the squared
component distance bounds and divide by a lower bound for ||w0||. This gives

    ||w(d)-w0||/||w0|| <= r0 = 0.02062279809948729522.

Since ||w(d)|| >= (1-r0)||w0||, the symmetric relative gap obeys

    2||w(d)-w0||/(||w(d)||+||w0||)
       <= 2 r0/(2-r0) <= 0.02083766356375750216 < 1/5.

These displayed decimal values are outward upper bounds. The 2.084% bound is
conservative, not an observed displacement or reconstruction error.

## 5. Conclusion and limits

The >20% strong separation gate is excluded for ALL simultaneous support
motions from this fixed reference that pass the current exponential slab
coupling certificate. No raster or sampled-direction assumption enters this
conclusion. It remains valid for the admissible subset because the arithmetic
bound covers a larger set; order/margin/conditioning rejection cannot enlarge
that set.

This excludes a way to construct a strong statistical counterexample under
one sufficient certificate. It does not prove general stability, existence of
a uniformly accurate estimator, impossibility of close-law geometries outside
this budget, or a bound for arbitrary pairs/reference geometries. It does not
cover moving landmarks/root, other measurement channels or continuum/physical
accuracy. Failing the sufficient coupling gate does not imply actual TV>1/4.

The next meaningful work is to reduce information-bound conservatism, e.g.
with rigorously enclosed joint membership-atom intensities, before expanding
this fixed-landmark shape search. Repeating coordinated optimization under the
same budget cannot reach the strong gate.

## 6. Audit and development record

Before freezing this final implementation, exploratory enclosures at the
older linear budget 1/4 were compared. A natural 48-dimensional box enclosure
failed contraction (eta about 1.212). A budget-aware matrix enclosure contracted
(eta about 0.01073), but a noncentered solve gave a loose symmetric gap about
54.56%. Centering the residual reduced that to about 1.806%. The final
certificate covers the larger 0.288 Poisson budget and gives 2.084%.
These were algebraic formulation diagnostics, not held-out statistical trials.
The local hash freeze is reproducibility evidence, not external preregistration.

`cb_audit.py` checks 48 analytic matrix/residual derivative identities against
exact rational dual differentiation. At 136 exact nonlinear points it checks
matrix, centered residual, multiplier and weight enclosures, including all
coordinate-axis endpoints, spatial 3-4-5 directions and eight coordinated
motions. It rejects a singular system and a false enclosure. These samples
check implementation; the uniform proof is Sections 3-4, not empirical coverage.

The Poisson coupling geometry extends [PR95](../shape_coupling/THEORY.md).
The exact moment system and verified-solve machinery are inherited from
[PR97](../conformal_sensitivity/THEORY.md); the budget dual-norm and centered
residual construction above are the new certificate.
