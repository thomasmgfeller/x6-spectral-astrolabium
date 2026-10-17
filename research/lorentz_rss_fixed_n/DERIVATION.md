# Roy–Sinha–Surya conditional on a fixed point count

## Assumptions and attribution

Let D be a deterministic causal diamond in a smooth d-dimensional Lorentzian
manifold, d >= 2, with physical volume V. Its endpoints and geometry are fixed
before sampling. Conditional on N=n, the points are independent with probability
measure dV/V. Chains count totally ordered k-element subsets once, including
relations that are not links. Endpoints are not included among the n random points.

Source: M. Roy, D. Sinha, S. Surya, *The Discrete Geometry of a Small Causal
Diamond*, [arXiv:1212.0631v1](https://arxiv.org/html/1212.0631v1), equations
8–9, 13–14, 31–32; published in Physical Review D 87, 044046 (2013).
We use d for their dimension n and n for the fixed sample size. The paper's
Poisson formulas are valid in their stated model. Conditioning, factorial
moments and the overlap identity below are standard probability arguments;
we make no priority or novelty claim.

## Exact conditional mean

Define the ordered integral

\[
I_k=\int_{D^k}{\bf1}\{x_1\prec\cdots\prec x_k\}\prod_i dV(x_i).
\]

A given labeled ordered tuple has probability I_k/V^k. There are (n)_k
distinct labeled tuples, and each chain contributes exactly one chronologically
ordered tuple. Consequently, for n >= k,

\[
E[C_k\mid N=n]=(n)_k I_k/V^k,\qquad
E[F_k\mid N=n]=k!I_k/V^k,\quad F_k=C_k/\binom nk.
\]

For Poisson N of mean rho V, E[(N)_k]=(rho V)^k. Averaging recovers
E_rho[C_k]=rho^k I_k exactly. Substituting n^k for (n)_k introduces a finite-n
factor; substituting a flat volume for V introduces a separate geometric error.
Our older benchmark already uses the exact binomial denominator.

## Small-diamond expansion

At the midpoint and in the orthonormal frame of the endpoint geodesic,
RSS gives (omitting higher orders)

\[
I_k=\chi_k V_0^k[1+\alpha_k RT^2+\beta_k R_{00}T^2+\cdots],\quad
V=V_0[1+\alpha_1 RT^2+\beta_1R_{00}T^2+\cdots],
\]

\[
\alpha_k=-\frac{dk}{12(kd+2)((k+1)d+2)},\qquad
\beta_k=\frac{dk}{12((k+1)d+2)},
\]

\[
\chi_k=\frac1k\left(\frac{\Gamma(d+1)}2\right)^{k-1}
\frac{\Gamma(d/2)\Gamma(d)}{\Gamma(kd/2)\Gamma((k+1)d/2)}.
\]

Expanding the actual denominator V^k yields

\[
E[F_k\mid n]=p_k[1+A_kRT^2+B_kR_{00}T^2+\cdots],\qquad
p_k=k!\chi_k,\quad A_k=\alpha_k-k\alpha_1,\quad B_k=\beta_k-k\beta_1.
\]

RSS's expansion is local: T must be small relative to curvature and derivative
scales, inside a suitable convex normal neighborhood. Small scalar curvature
alone is not a general criterion. In this de Sitter family all curvature scales
are controlled by H*T and curvature derivatives vanish.

In d=4 the exact rational values are:

| k | p_k | A_k | B_k | A_k-B_k/4 |
|---|---|---|---|---|
| 2 | 1/10 | 2/315 | -2/105 | 1/90 |
| 3 | 1/350 | 4/315 | -2/45 | 1/42 |
| 4 | 1/29400 | 28/1485 | -4/55 | 1/27 |

For de Sitter, R00=-R/4, so the leading relative response is
b_k RT^2 with b_k=k(k-1)/(36(2k+1)). The unconditioned coefficient
alpha_k-beta_k/4=-k/(24(2k+1)) has the opposite sign. Conditioning on a
fixed count changes what is being compared; this is not a contradiction.

## Exact covariance identity, not an independence approximation

Let H_A indicate that the subset A forms a chain and let
mu_(k,l,s)=E[H_A H_B] for |A|=k, |B|=l and |A intersect B|=s.
Exchangeability makes this independent of the labels. For disjoint subsets,
independence gives mu_(k,l,0)=p_k(D)p_l(D), where here p_k(D)=E[F_k]
is the exact geometry-dependent probability, not its flat approximation.
Counting subset pairs by overlap gives exactly

\[
\operatorname{Cov}(F_k,F_l\mid n)=
\sum_{s=1}^{\min(k,l)}
\frac{\binom{k}{s}\binom{n-k}{l-s}}{\binom nl}
\left[\mu_{k,l,s}-p_k(D)p_l(D)\right].
\]

An impossible binomial coefficient is zero. For fixed k,l the leading
overlap weight is kl/n; the variance is ordinarily O(1/n), not O(n^-k),
unless the first-order projection is degenerate. We verify the full finite-n
identity by exhaustive rational enumeration of an independent finite atomic
model. We do not derive closed curved-space values of every mu here.
For the geometric experiment we estimate the complete covariance matrix
from independent causal sets, preserving its off-diagonal entries.

## Independent forward checks

Geometry is g_h=(1-h*eta)^-2 diag(-1,1,1,1) on
|eta|+norm(x)<1/2, 0<=h<2. R=12h² and T=2 atanh(h/2)/h (T=1 at h=0).
The existing validated rejection sampler supplies actual iid fixed-n
curved draws. This module does not modify it or its archived evidence.

For k=2, we independently integrate I2=integral_D dV(x) Vol(I(x,q)).
At time u, that inner volume uses the intersection of spatial 3-balls of
radii u-eta and 1/2-u with center separation r=norm(x). Split at
u=(eta+1/2-r)/2 and u=(eta+1/2+r)/2. The outer parts are contained balls.
In the middle, with L=1/2-eta, the lens volume is

\[
\frac{\pi(L-r)^2}{12r}
\left[r^2+2rL-3(2u-\eta-1/2)^2\right].
\]

Multiply by (1-h*u)^-4, integrate u, then integrate x with
4*pi*r²(1-h*eta)^-4 dr d eta. Divide 2I2 by V². Gauss–Legendre
orders 12,20,32 are fixed in advance. Their agreement is a numerical
convergence diagnostic, not interval-arithmetic certification. The C2
5% remainder criterion is relative to the true curvature signal p2(h)-p2(0),
not to the much larger flat baseline. The grid is a set of tested points,
not a proof of a continuous validity interval.

For k=2,3,4 we additionally use flat iid clouds and the exact known density
ratio w_h(eta)=(V0/Vh)(1-h*eta)^-4. Products of k weights on each chain
give an unbiased importance estimate of p_k(h). Time reversal maps a flat
cloud to another flat cloud and reverses every chain. Averaging w_h(eta)
and w_h(-eta) **at the level of whole chain products** cancels odd powers.
It would be wrong to average the individual point weights first.
Subtracting the same cloud's unweighted count gives a paired response.

The primary derivative avoids finite differences. Since E_flat[eta²]=1/60,
w_h(eta)=1+4h eta+h²(10eta²-1/6)+O(h³). For a k-chain its product's h²
coefficient is 2 sum eta_i² + 8(sum eta_i)²-k/6. Polynomial dynamic
programming sums this over all chains. Divide by binom(n,k)*12*p_k
to estimate the limiting response per RT². Actual curved draws and
importance estimates are archived separately: the latter's reduced variance
is not the noise level of a single measured causal set.

The stated Student-t intervals rely on independent replicate clouds and a
large-sample approximation. Bonferroni does not make that approximation an
exact finite-sample guarantee. No adaptive stopping or seed search is used.

## Identifiability and exploratory inversion

For d=4, the 2-by-2 matrix with rows (A2,B2),(A3,B3) has determinant
-4/99225, so the leading mean equations have a unique dimensionless linear
inverse. Invert y_k=F_k/p_k-1 to (RT²,R00T²), without clipping negative
values. Nonzero determinant does not guarantee useful precision at finite n.
We report bias and single-order RMSE on fresh direct draws without fitting
parameters to these draws. This is an exploratory assessment, not a qualified
curvature estimator or a confidence region. De Sitter tests only R00=-R/4;
it cannot validate the two Ricci directions independently.

C1=n carries no remaining count fluctuation. Normalized order statistics
provide no absolute scale: an independently calibrated T or other scale is
needed for absolute curvature. The flat model in the Eigenzeit Lab cannot
silently supply that scale in a curved geometry. Freely varying sampling
density still permits the previously proved conformal density twins. All
their order statistics, of every chain length, remain indistinguishable.
