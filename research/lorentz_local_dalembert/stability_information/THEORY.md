# What can and cannot be recovered from the selected interval counts

SPDX-License-Identifier: Apache-2.0

This note derives statements for the fixed 2+1 Minkowski, known-density,
selected-node experiment. It does not address the full causal-set Hauptvermutung,
curvature, 3+1, physical observations, or an exact joint Poisson likelihood.

## 1. Exact distances identify nondegenerate geometry

Write eta=diag(-1,1,1), and q(a,b)=-(b-a)'eta(b-a). Let four landmarks be
l0,...,l3, and let B have columns li-l0, i=1,2,3. If det(B) != 0, their Gram
matrix H=B'eta B is invertible, has signature (-,+,+), and is determined by

H_ij = [q(li,lj)-q(li,l0)-q(l0,lj)]/2.

For a point x, the inner products v_i(x)=(li-l0)'eta(x-l0) are similarly
determined by its four landmark distances. Its coefficients in the landmark
basis satisfy H u(x)=v(x), so u(x)=H^-1 v(x). The squared signed separation of
two supports is (v(y)-v(x))'H^-1(v(y)-v(x)). Every configuration with these exact
distances is related by a Lorentz isometry (and translation); the observed
time orientation removes the unwanted time reversal. A spatial reflection is
an isometry and does not change the scalar operator target.

All counted pairs in this input mask are timelike. With positive known density,
mu=rho*pi/12*q_phys^(3/2) is strictly increasing in positive q_phys and has
the smooth inverse q_phys=(12*mu/(rho*pi))^(2/3). Thus the exact mean counts
identify the nondegenerate geometry up to these irrelevant isometries. This
does NOT say that noisy finite counts identify it accurately.

Together with full moment rank (Section 3), these smooth inverses also imply
pointwise local Lipschitz continuity of the weights at a nondegenerate geometry
with positive counted intervals. Thus exact identifiability does imply local
continuity here. The unanswered question is the SIZE and uniformity of the
finite-error bound over the admissible set, not mere continuity at one point.

## 2. Error amplification is a different question

For u=H^-1 v and s=v'H^-1 v, differentiation gives exactly

ds = 2 u' dv - u' (dH) u.

Consequently |ds| <= 2||u|| ||dv|| + ||u||^2 ||dH|| to first order. Both uncertain
landmark geometry and uncertain landmark/support distances contribute; their
effects need not be additive after a nonlinear reconstruction. Near a null
support separation, even a small absolute ds can change its sign.

For ||H^-1 dH|| < 1, the resolvent identity gives the finite perturbation bound

||(H+dH)^-1-H^-1|| <= ||H^-1||^2 ||dH|| / (1-||H^-1 dH||).

The right-hand side depends on the scale and conditioning, not just matrix
rank. A condition-number cutoff alone is not an end-to-end error guarantee.

For q_phys>0, dmu/dq_phys=(rho*pi/8)*sqrt(q_phys). In the inverse direction,
dq_phys/dmu=(2/3)*q_phys/mu. The nonlinear transform and reconstruction therefore
must be studied together, with correlated count perturbations retained.

## 3. The operator target and its derivative

Let D contain the nine linear/quadratic monomials of root-centered support
coordinates in a fixed Minkowski frame, b=(0,0,0,-2,2,2,0,0,0), and
H_w=I+11'. The support weights a minimize a'H_w a/2 subject to D a=b.
If D has row rank nine, H_w is positive definite and the unique solution is

a=H_w^-1 D' (D H_w^-1 D')^-1 b,
w=(-1'a,a)/scale^2.

These are the same weights as the frozen four-landmark construction after its
invertible coordinate change; they are exact on quadratic fields in the given
geometry. They are NOT automatically accurate for arbitrary continuum fields.

For K=[H_w D'; D 0], K u=(0,b), the derivative is
du=K^-1[-(dK)u], since b and H_w are fixed. This gives W=D_theta w. It includes
the movement of the root relative to every support and the constant-field
constraint. The search uses this analytic derivative, checked against central
differences on a separate synthetic fixture.

## 4. Local information geometry

Fix the empirical positive-definite C_alpha=.95 C+.05 diag(N), factor it as
L L', remove six continuous Lorentz/translation gauge freedoms, and define
A=L^-1 D_theta mu. For a locally full-column-rank A, a small feasible change
h in geometry gives whitened mean perturbation A h and target perturbation W h.

The sharp UNCONSTRAINED tangent gain is K_local=||W A^+||_2:
sup_{||A h||<=1} ||W h||=K_local. The equality follows by setting h=A^+u;
components of u orthogonal to range(A) contribute nothing. If A has a kernel
and W does not vanish on it, no finite linear gain exists. Numerically small
singular values alone are not a proof of an exact kernel. In this nondegenerate
four-landmark setting the smooth inverse above explains local identifiability.

Known causal inequalities can restrict directions, especially at active fitted
constraints. Therefore this tangent SVD is a search guide, not a certified
finite-radius upper bound or a statistical covariance. Every proposed finite
pair must be checked again against the exact nonlinear means and full order.

## 5. A deterministic, algorithm-independent lower bound

For the actual fixed summary (N,C_alpha), define

E_R = {z: same selected-node order and declared geometry gates,
             ||L^-1(mu(z)-N)|| <= R}.

Here R=sqrt(m), m=number of used count intervals, is a declared error budget.
No probabilistic coverage is assigned to E_R. If z0,z1 both belong to E_R,
then any estimate w_hat based only on this bounded-error summary satisfies

max(||w_hat-w(z0)||, ||w_hat-w(z1)||) >= ||w(z1)-w(z0)||/2.

Proof: ||w1-w0|| <= ||w1-w_hat||+||w_hat-w0|| by the triangle inequality.
The same proof works for a fixed scalar field vector f and target w(z)'f.
This is an existence/worst-case bound: at least one admissible geometry incurs
that error. It is not a statement that every real experiment or every estimator
has that error on the true geometry. The targets can differ even though the
two mean vectors are additionally close in the C_alpha metric.

For nonzero w0,w1 a corresponding relative bound is

max(||w_hat-w0||/||w0||, ||w_hat-w1||/||w1||)
    >= ||w1-w0||/(||w0||+||w1||).

Indeed, if both relative errors were smaller, their absolute errors would sum
to less than ||w1-w0||. This is half the symmetric relative separation used by
the search. It is a worst-case relative error of the WEIGHT VECTOR (equivalently
the operator norm on l2-bounded nodal fields), not relative scalar response
error on each field, and not an RMSE under a sampling distribution.

The l2 weight norm describes the operator on l2-bounded nodal fields. An exact
l-infinity field witness can instead take f_i=sign(w1_i-w0_i), giving separation
||w1-w0||_1. Such a field is chosen adversarially and can oscillate rapidly.
It is not evidence of the same failure size on a prespecified smooth-field
class. A continuum minimax bound would additionally require a stated field
regularity class and control of discretization error.

## 6. What this does not prove

C_alpha is estimated, random and correlated with N. Its fixed quadratic norm
is not the full Poisson observation law. Neither the covariance's dependence
on geometry nor the entire original A/B causal graph is modelled here. A
statistical indistinguishability claim would require a bound on the actual
joint distributions (for example a valid divergence/testing bound), including
selection and overlaps, or a justified calibrated approximation. Closeness of
means alone is insufficient. A Gaussian calculation with fixed C could only
be a surrogate calculation, not a Poisson proof.

Thus a certified pair rules out a uniformly tighter guarantee for this
particular discrete target and bounded-error information set. It cannot rule
out richer observables, a different operator, a smoother field class, or a
better average-case estimator. Conversely, failure to find a pair does not
prove stability: the nonconvex search is finite and has no global certificate.

## References and independent checks

The elementary triangle-inequality bound is proved here. Its interpretation
through a modulus of continuity is consistent with the classical optimal
recovery viewpoint: D. L. Donoho, *Statistical Estimation and Optimal Recovery*,
Annals of Statistics 22(1), 238–270 (1994), DOI 10.1214/aos/1176325367,
https://projecteuclid.org/journals/annals-of-statistics/volume-22/issue-1/Statistical-Estimation-and-Optimal-Recovery/10.1214/aos/1176325367.full .
The probabilistic theorems in that work are not transferred to this correlated
Poisson setting without checking their assumptions.

The broader intrinsic-operator context is Boguñá and Krioukov, *Local
d'Alembertian for causal sets*, https://arxiv.org/abs/2506.18745 . Its convergence
analysis is not a validation of this finite four-landmark estimator.

Wolfram Language independently simplifies the Gram identity to zero, derives
dmu/dq, and confirms that two nonnegative errors with sum >=Delta cannot both
be <Delta/2. Those symbolic checks do not certify the whole numerical campaign.
