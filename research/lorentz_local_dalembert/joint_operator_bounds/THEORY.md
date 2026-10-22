# A finite operator bound retaining joint difference constraints

SPDX-License-Identifier: Apache-2.0

Scope and coverage are inherited unchanged from PR90: fixed A-selected packets,
independent homogeneous Poisson B, known density, flat 2+1. All constructions
below are deterministic outer bounds on the covered set. No new confidence
budget is spent, and no numerical optimization objective is accepted as proof.
The calculation still uses a necessary outer relaxation, not an exact
characterization of all realizable Lorentzian geometries.

## 1. Transforming a mean-difference constraint

Write q=f(mu)=a mu^(2/3), a=(12/(rho pi scale^3))^(2/3)>0.
For x in [lx,ux], y in [ly,uy], y-x<=d, maximize f(y)-f(x).
For fixed x, the maximizing y is min(uy,x+d). The feasible x interval is
[max(lx,ly-d),ux], provided it is nonempty and the original intervals are valid.
Let ell=max(lx,ly-d).

If d>=0, choose x*=ell. Before the cap y=uy, the derivative of
f(x+d)-f(x) is nonpositive by concavity. After the cap, f(uy)-f(x) decreases.
This also handles the case y<x forced by separated intervals.

If d<0, before the cap f'(x+d)-f'(x)>=0, while after the cap the expression
decreases. Thus x*=max(ell,min(ux,uy-d)), the cap location clamped to the
feasible interval. In both cases y*=min(uy,x*+d). Boundary points at zero
follow by continuity, without using an infinite derivative numerically.

Directed rational cube-root and pi enclosures bound f(y*)-f(x*) from above.
Take the smaller of this bound and the independent q-box upper difference.
Outward rounding onto a 10^-12 q lattice and integer shortest paths retain
validity. These are joint constraints q_j-q_i<=D_ij, with q_0=0 an auxiliary
zero variable (not the reference geometry). Negative cycles trigger failure.

## 2. Exact feasible transport proves support bounds

To bound c^T(q-q_ref), augment c with c_0=-sum(c), so the augmented vector
sums to zero. Send nonnegative flows from nodes with c_i<0 to nodes with c_j>0,
with total inflow minus outflow equal to c at every node. Then exactly

$$c^Tq=\sum_{i,j}t_{ij}(q_j-q_i)\le\sum_{i,j}t_{ij}D_{ij}.$$

Subtract c^T q_ref to get an upper bound on the perturbation linear form.
Repeat with -c and take the maximum to bound its absolute value. Also retain
the prior independent symmetric-box bound, and take the smaller valid bound.

The implementation chooses a deterministic greedy flow ordered by edge saving
D_ij-D_i0-D_0j. Every flow and coefficient balance is rational and checked
exactly. Complete connectivity guarantees completion. This is weak duality
proved by summing inequalities; it does not require optimal flow, strong
duality, a solver tolerance, or an assumption that the reference is feasible.
A greedy flow can be suboptimal. Box-only and joint runs may choose different
flows, so their component bounds are combined by minima to avoid regressions.

## 3. Apply the support function before absolute values

Use the same reference q_ref, exact pivot row transform S, and quadratic
intrinsic design D as in PR89. The root-centered coordinate-inner-product
forms v_j=Z_j q are linear, and the target b is linear. Let U(c) be the certified
bound on |c^T(q-q_ref)| from Section 2.

For each support point j set e_jr=U(Z_jr). For the exact design Jacobian J_j
at the reference, the linear term in transformed row r is bounded by
U((S J_j)_r). The explicit quadratic remainder before S has component bounds

(0,0,0,e_j0^2,e_j1^2,e_j2^2,e_j0 e_j1,e_j0 e_j2,e_j1 e_j2).

Multiplication by |S| bounds its transformed remainder. Frobenius norms give
E=L+Q for the full finite design perturbation, and the norm of U applied to
the transformed target rows gives e_b=B. This preserves joint constraints in
all linear forms and in the factors controlling the quadratic remainder.
It does not assume that a first-order derivative alone bounds finite error.
The final products and Frobenius norm remain conservative.

The previous resolvent theorem now applies unchanged:

$$e_M=2d_0E+E^2,\quad\gamma=\beta e_M.$$

When gamma<1, use the previously proved finite lambda and weight-error bounds.
When gamma>=1, return NO_CONTRACTION_CERTIFICATE, not instability or singularity.
Only the full set is evaluated. No artificial radius reduction is assigned
coverage. A successful full-set certificate would inherit PR90's simultaneous
coverage lower bound; an unsuccessful sufficient test proves no accuracy claim.

## 4. Attribution and limitations

Three evaluations use the same reference and pivots: the original symmetric
box; transport support bounds from marginal boxes only; and support bounds
from the joint graph. Comparing the latter two separates the contribution of
joint constraints from merely retaining box asymmetry. All twenty original
packets remain listed, including the prior count HOLD. There is no new fit.

Even a successful relative weight certificate would not alone prove the C3
field target. That target still requires the geometric radius/weighted cubic
remainder and field-noise terms in PR90's FIELD_CONTRACT.md. No constants are
silently supplied. The present theorem neither proves nor assumes statistical
indistinguishability of the earlier witness geometries.
