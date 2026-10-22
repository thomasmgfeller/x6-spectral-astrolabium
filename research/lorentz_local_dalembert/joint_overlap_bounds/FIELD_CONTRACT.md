# Normalized smooth-field benchmark and error target

SPDX-License-Identifier: Apache-2.0

This declares a mathematical benchmark for future certification, not measured
physical constants. Fix a Minkowski frame, length L>0 and field amplitude F>0
before evaluating fields. All root-to-support segments must lie in the
Euclidean ball of radius L in that frame. These frame-dependent regularity
bounds are not Lorentz-invariant assumptions.

Use fields f(x)=f(x0)+F phi((x-x0)/L), with phi(0)=0, phi C3 on the ball,
||grad phi||_2<=1 and ||D^3 phi||_op<=1 throughout it. This is a concrete
normalized C3 class. It includes bounded-gradient affine fields and
phi(u)=g.u+u^T H u/2 whenever ||g||+||H||_2<=1. For this quadratic subclass,
D3 phi=0 and L^2 Box(f)/F=tr(eta H), eta=diag(-1,1,1).

The primary target is absolute normalized response error

$$E=\frac{L^2}{F}|\widehat w^T(f+e)-\Box f(x_0)|.$$

A future working accuracy gate is E<=0.1 uniformly over the declared class
and admissible geometries. This is not an existing PASS gate or a physical
accuracy promise. Use absolute error because affine, constant, and wave-like
fields can have zero Box response. Relative error requires a separate,
predeclared nonzero response floor and is not the primary metric.

Let w be the true quadratic-moment-exact weights, let both w and w_hat
annihilate constants, and let |e_j|<=epsilon F. With r_j=||x_j-x0||/L<=1,
the already proved Taylor and weight-error identities give

$$E\le L^2\|\widehat w-w\|_2\sqrt{n_s}
 +\frac{L^2}{6}\sum_{j\ne0}|w_j|r_j^3
 +\epsilon L^2\|\widehat w\|_1.$$

Proof: the gradient bound implies |f_j-f0|<=F r_j<=F; apply Cauchy-Schwarz
to the geometry/weight term. The third derivative bound in physical coordinates
is F/L^3, so Taylor's cubic remainder gives the second term. The nodal noise
bound and the l1 norm give the third. Every term is dimensionless. Root field
noise is included in the last term. For the quadratic subclass the middle
term is exactly zero. Sharper radii may replace sqrt(n_s) by sqrt(sum r_j^2).

The same nodal observations are used in the weight-error decomposition for
each candidate truth; independently evaluating a different synthetic field
on every candidate geometry cannot be substituted for common observed data.
A sign vector attaining the full weight norm need not belong to this smooth
class and cannot establish its worst-case field error.

To obtain an actual uniform certificate still requires a certified common
frame/radius bound for every admissible geometry, a bound on w_hat-w and the
weighted cubic moment throughout that set, and a declared measurement-noise
budget epsilon. There is no new field performance claim in this audit.
Normalizing L=F=1 is a change of units for this benchmark, not a determination
of the physical scales. No true-coordinate radius is silently imported.
