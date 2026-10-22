# From correlated Poisson counts to finite operator-error bounds

SPDX-License-Identifier: Apache-2.0

This proof concerns the existing flat 2+1, known-density, four-landmark model.
It does not certify curvature, unknown density, 3+1, physical data, or the
entire original causal set. The numerical evaluation is posthoc on archived
B0 records; the coverage statement is an analytic theorem for the fixed rule.

## 1. The actual counting boundary and its dependence

Condition on the complete selection cloud A, its chosen endpoints and the
fixed 20-packet B0 plan. The separate homogeneous Poisson process B has known
intensity rho in a containing diamond. If I_j is a selected Alexandrov
interval contained in this diamond, then

N_j=B(I_j) ~ Poisson(mu_j), mu_j=rho Vol(I_j).

The joint counts are generally dependent, with Cov(N_i,N_j)=rho Vol(I_i cap I_j).
An explicit representation uses the disjoint atoms of the interval membership
partition: independent Poisson atom counts sum to the N_j. Consequently the
joint log moment generating function is

log E exp(sum_j t_j N_j)
 = rho integral [exp(sum_j t_j 1_{I_j}(x))-1] dx.

We do not replace this expression by a product of marginal likelihoods. The
bound below only needs the correct marginals and a union bound, which remains
valid under this full dependence. The observed overlap counts are not treated
as deterministic covariance truth; their additional information is simply
not exploited to narrow the first conservative set.

The repository boundary draws a Poisson number of B points and then points
uniformly in the containing diamond, after selecting the packet from A.
This is precisely the idealized model above. Endpoint intervals lie in the
containing diamond by causal transitivity. The theorem assumes this geometry
and ideal randomness; finite PRNG/floating implementation is a separate
numerical issue. The source sampler and existing audits remain unchanged.

The count family depends on A, not on B fit success. Failed observed count
gates remain in the family. A resource-cap abort must return no finite result
(or the full parameter set), rather than silently condition on an accepted
Poisson count. We make no coverage claim conditional on B passing a fit, count
or cap gate. Fixed B0 sampling is not optional stopping.

## 2. A simultaneous finite-sample confidence box

For N~Poisson(mu), its moment generating function is
E exp(tN)=exp(mu(exp(t)-1)). Applying Markov's inequality and minimizing in t
gives the Chernoff tail bound exp[-d(n,mu)] on either appropriate tail, where

d(n,mu)=mu-n+n log(n/mu), with d(0,mu)=mu.

Thus P_mu(d(N,mu)>c)<=2 exp(-c). The discreteness of N can only make this
bound more conservative. For mu=0, N=0 almost surely and coverage is immediate.

To obtain simple rigorous endpoints, put r=n/mu and h(r)=r log r-r+1.
For r>=1, h(r)-(r-1)^2/(2r) has second derivative (r^2-1)/r^3>=0;
for 0<r<=1, h(r)-(r-1)^2/2 has second derivative 1/r-1>=0.
Both functions and their first derivatives vanish at r=1. Convexity on the
respective intervals, including the limit r=0, proves

d(n,mu) >= (n-mu)^2/[2 max(n,mu)].

Inverting the weaker quadratic sublevel condition yields

L(n)=max(0,n-sqrt(2nc)),
U(n)=n+c+sqrt(c^2+2nc).

If mu<=n, d<=c implies n-mu<=sqrt(2nc); if mu>=n it implies
(mu-n)^2<=2mu c, whose positive root is U(n). Therefore this interval contains
the Chernoff sublevel interval. At n=0 use U(0)=c: exclusion then has probability
exp(-mu)<exp(-c). No normal approximation, estimated variance or independence
between N_j is used.

For M=1736 counted intervals and c=12, the union bound gives

P(all mu_j in [L(N_j),U(N_j)] | A)
 >= 1-2 M exp(-12) > 0.97866729470924445571.

The numerical lower endpoint is certified by a positive finite Taylor sum
below exp(12). Integrating over A preserves the same guarantee for the fixed
family size; if another experiment has more intervals it needs a new budget.
This is a coverage frequency of the procedure over B draws, not a posterior
probability for the archived true geometry. It is also not a 97.86% guarantee
that the recovered operator has 10% error.

In 2+1 Minkowski, mu=(rho*pi/12)*scale^3*q^(3/2), q>0. Its increasing inverse
q=(12mu/(rho*pi*scale^3))^(2/3) maps the mean box to a simultaneous q box Q.
Directed rational pi, square-root and cube-root bounds enclose this map.
Intersecting with exact physical constraints known to hold for the truth
preserves coverage. Imposing unverified conditioning restrictions does not.

## 3. A finite-radius operator bound

Write original intrinsic landmark Gram H(q), root-centered inner products
v(q), monomial design D(q), and target b(q) as in the published inference.
H, v and b are linear in q, and D is at most quadratic. Let n_s be the support
count, H_w=I+11', and P=H_w^-1=I-11'/(n_s+1), so ||P||2<=1.

Choose any fixed invertible 9x9 row transform S. Here it is the exact inverse
of nine pivot columns of D(q0); QR merely proposes these columns, and rational
inversion verifies their independence. Replace D,b by S D,S b. The constraint
set and the unique minimum-energy weights remain exactly the same.

At q0 define

M0=D0 P D0', lambda0=M0^-1 b0,
a0=P D0' lambda0, w0=(-sum(a0),a0)/scale^2.

Exact rational moment equations and an independent solve in the original
Minkowski coordinate frame verify this reference. For any q in the symmetric
box |q-q0|<=t r that encloses Q at t=1, an exact polynomial expansion bounds

||D-D0||2 <= ||D-D0||F <= E(t)=t L+t^2 Q2,
||b-b0||2 <= t B = e_b.

The code preserves first-order cancellations after S by computing the exact
gradient in q before taking absolute values. Quadratic remainders use
|delta v_i|^2 and |delta v_i delta v_j|. Taking Frobenius/Euclidean norms of
the resulting entrywise bounds proves E and e_b; these are not derivatives
used as unproved finite approximations.

Choose rigorous beta>=||M0^-1||2 and d0>=sqrt(||M0||2). Because M0 and its
inverse are symmetric, their induced infinity norms give valid spectral norm
upper bounds. Then for M=D P D',

||M-M0||2 <= e_M=2 d0 E+E^2,
gamma=beta e_M.

If gamma<1, the resolvent/Neumann bound proves M invertible throughout the
entire box, with ||M^-1||2<=beta/(1-gamma). Subtracting M lambda=b and
M0 lambda0=b0 yields the finite bound

||lambda-lambda0||2 <= d_lambda
 = beta [e_b+e_M ||lambda0||2]/(1-gamma).

Finally ||w-w0||2=||H_w^(1/2)(a-a0)||2/scale^2. Since

H_w^(1/2)(a-a0)
 = P^(1/2) D0' (lambda-lambda0)
   + P^(1/2)(D-D0)' lambda,

and ||P^(1/2) D0'||2=sqrt(||M0||2), we obtain

||w-w0||2 <= B_w
 = [d0 d_lambda+E(||lambda0||2+d_lambda)]/scale^2.

If r_w=B_w/||w0||2<1, reverse triangle inequality gives

||w-w0||2/||w||2 <= r_w/(1-r_w).

Thus r_w<=1/11 is sufficient for at most 10% relative weight error. All norms
and products used for the upper bound are evaluated exactly or rounded
outward. This theorem is for every valid geometry in the box, including
directions missed by an optimizer. Data-dependent reference/pivot choices are
permitted because the bound, if successful, encloses the whole original Q.

A certificate at t=1 combined with Section 2 would bound the probability of
a false accuracy certificate by 2M exp(-12), under the model. This does NOT
give the same coverage conditional on the event that certification succeeds.
At t<1 the set has been shrunk artificially and no coverage follows. Gamma>=1
means this sufficient proof failed; it does not prove a singular matrix,
instability, a large actual error, or necessary sample size.

## 4. A restricted-domain finite envelope

Suppose, as an additional domain restriction, the ORIGINAL intrinsic D has
cond_2(D)<=kappa=1e5. If at least one entry obeys |D_ij|>=d_min>0 throughout
the original box, then sigma_min(D)>=d_min/kappa. If ||b||2<=b_max there,

||w||2 <= sqrt(n_s+1) kappa b_max/(scale^2 d_min).

Proof: set u=H_w^(1/2)a; it is the minimum-norm solution of
D H_w^-1/2 u=b, whose smallest singular value is at least
sigma_min(D)/sqrt(n_s+1). Then ||w||2=||u||2/scale^2.
The error relative to w0 is at most this envelope plus ||w0||2 by triangle
inequality. Bounds on D entries and b come from the same polynomial boxes.

This bound is finite but can be enormous. The true geometry's conditioning
has NOT been certified merely because a fitted geometry passes a condition
cutoff. Hence this restricted-domain envelope must not be presented as an
unconditional confidence guarantee for true operator error.

## 5. The remaining smooth-field term

Fix a specified Minkowski frame and physical support displacement y_j. Let
f be C3 on each segment from the root to its support, with Euclidean operator
norm ||D^3 f||<=M3 in that frame. Quadratic moment exactness and Taylor's
integral remainder imply

|sum_j w_j f(x_j) - Box f(x0)|
 <= M3/6 sum_support |w_j| ||y_j||2^3.

If estimated weights w_hat and true weights w both annihilate constants,
the geometry/weight term for fixed common nodal values obeys

|(w_hat-w)' f| <= ||w_hat-w||2 ||f-f(x0)1||2.

Additional nodal measurement error e contributes <=||w_hat||2 ||e||2
(or ||w_hat||1 ||e||infinity). These three terms bound total absolute error:
geometry/weight error, discretization remainder, and field measurement error.
For relative scalar error one additionally needs a nonzero lower bound on
|Box f(x0)|. A relative weight bound alone is insufficient, especially near
zero continuum response. No numeric M3, geometric radius or response lower
bound has been supplied for the intended physical field class. We do not
invent them or claim smooth-field accuracy from the adversarial sign field.

## Sources and independent checks

The proof above is included in full. Background references are:

- G. Last and M. Penrose, *Lectures on the Poisson Process*, Cambridge University
  Press, DOI 10.1017/9781316104477. Author institutional record:
  https://publikationen.bibliothek.kit.edu/1000185543 . This supplies the general
  Poisson-process framework, not a validation of this reconstruction.
- Berkeley Data 140, *Chernoff Bound*, original course text:
  https://data140.org/textbook/content/chapter-19/chernoff-bound/ . The two-sided
  scalar specialization, explicit endpoints and union step are derived here.
- Wolfram's official point-process definition:
  https://reference.wolfram.com/language/ref/PoissonPointProcess.html . Counts
  in a fixed region have the volume-times-intensity Poisson mean; independence
  applies to disjoint regions, and is not assumed for the overlapping intervals.

Wolfram independently verifies the Poisson MGF, both scalar convexity checks,
endpoint identity, numerical family bound, and weight-energy identity. It does
not certify the entire numerical audit. The reproducible rational computation
and explicit proof above carry the finite-bound claims.
