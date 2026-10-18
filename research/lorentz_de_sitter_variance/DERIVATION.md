# Model-certified cloud variance and Bennett confidence for C2

## Scope and development history

The estimand remains q=R T² in the known uniform physical-volume 4D de Sitter
family, h∈[0,1/2]. Each cloud has N iid points; M clouds are independent and
identically distributed, with M fixed before observing the target sample.
C2 counts unordered comparable pairs and U=C2/choose(N,2)∈[0,1].
The geometric mean function p(h), its strict monotonicity, rational inverse
and q transform are the unchanged C2 reference. This is a model-specific
variance certificate and an application of a classical concentration method,
not a new general concentration theorem or a general spacetime clock.

Historical published KL raw counts were inspected during development only:
empirical cloud variances were about 0.000309–0.000336 for N=128. This suggested
an opportunity but is not used as a population-variance guarantee. The
certificate below is analytic. The mathematical construction and off-grid
controls precede the public source freeze; target budget comparisons and
fresh simulation follow it. No previous scientific sources are edited.

## 1. Dependence is retained through a shared anchor

Let g(X,Y) be the symmetric binary comparability kernel, p=E g(X,Y),
r(x)=E[g(x,Y)|x] and w=E r(X)²=E[g(X,Y)g(X,Z)].
Disjoint pairs are independent. Distinct pairs sharing one endpoint have
covariance w−p². Counting the choose(N,2) variances and
3 choose(N,3) unordered overlapping pair pairs gives exactly

    Var(U) = [2p(1−p)+4(N−2)(w−p²)]/[N(N−1)]
           = [2p+4(N−2)w−(4N−6)p²]/[N(N−1)].

No individual pairs in a cloud are treated as independent observations.
The new information is a controlled calculation of w, not an increased
fictional sample count. For the flat uniform diamond p=1/10 and w=1/50.

## 2. Conditional interval volumes from Lorentz moments

Use conformal coordinates in the unit-duration Minkowski diamond D, with
endpoints (−1/2,0) and (1/2,0). Its flat volume is V0=π/24. The physical
volume weight is f_h(t)=(1−ht)^−4, with normalizer Z(h)=E0 f_h(T).
Causal comparability is unchanged by this conformal factor.

For x=(t,r), r_h(x) is the sum of its physical past and future interval
volumes divided by V0 Z(h). Compute their weighted volumes using

    f_h(u) = Σ[k≥0] a_k h^k u^k,  a_k=choose(k+3,3).

For the future interval from x to the top, put Δ=1/2−t,
c=(t+1/2)/2 and s=r². Its flat volume divided by V0 is (Δ²−s)².
A Lorentz transform of a unit rest diamond gives its time coordinate as
c+ΔT+rX1. The transformation preserves four-volume; the proper-duration
factor supplies (Δ²−s)². Rest-diamond moments are

    E0[T^(2a) X1^(2b)]
      = 192 (2a)! (2b+3)! /
        [(2b+1)(2b+3) 2^(2a+2b+4) (2a+2b+4)!].

An odd exponent in either variable integrates to zero. Expanding
(c+ΔT+rX1)^k therefore gives a finite rational polynomial Pk⁺(t,s):

    Pk⁺ = (Δ²−s)² Σ[2a+2b+c_index=k]
          k!/(c_index! (2a)! (2b)!)
          c^c_index Δ^(2a) s^b E0[T^(2a)X1^(2b)].

The past polynomial is Pk⁻(t,s)=(−1)^k Pk⁺(−t,s).
Set Fk=Pk⁺+Pk⁻. Their normalization is by V0, not by the interval's own
physical volume. The conditional comparability numerator is
A_h(x)=Σ a_k h^k Fk(x), and r_h(x)=A_h(x)/Z(h).

## 3. Rational wedge series and a uniform remainder

The normalized flat-diamond radial moments, with s=r², are zero for odd a;
for even a they are

    E0[t^a s^b] = 192 a! (2b+3)! /
                  [(2b+3) 2^(a+2b+4) (a+2b+4)!].

Thus the coefficients of

    W(h)=E0[f_h(T) A_h(X)²],       w(h)=W(h)/Z(h)³

are exact finite polynomial integrals. The implementation retains h-degree
16. Simultaneous time reflection removes every odd coefficient. Equivalently,
W=E0[g(X,Y)g(X,Z) f_h(Tx)f_h(Ty)f_h(Tz)]. This representation supplies a
simple absolute coefficient bound: since |Ti|≤1/2 and g≥0,

    |[h^k]W| ≤ (1/50) choose(k+11,11)/2^k.

For the first omitted even k=18, x=h/2 and
ρ=x² (k+13)(k+12)/[(k+2)(k+1)], successive even majorants have ratio at
most ρ<1 throughout the domain. Consequently

    |W−W16| ≤ (1/50) choose(29,11) x^18 /(1−ρ).

The normalizer Z is exactly the volume series already certified in the C2
reference: Z=Σ[j≥0] 2(h²/4)^j/(j+2). Its positive terms and certified tail
provide lower/upper bounds. Dividing W16±remainder by the appropriate
positive Z³ bounds encloses w. All decisions use rational arithmetic.

For a variance bound uniform in h, split [0,1/2] into 64 closed cells.
On each cell bound W16 by endpoint powers according to coefficient signs,
add the right-end remainder, and divide by the left-end positive truncated
Z³. The established monotonicity of p supplies pL at the left and pU at the
right. Then

    v_cell = [2pU+4(N−2)wU−(4N−6)pL²]/[N(N−1)]

bounds the variance everywhere in that cell. Take the maximum over all
cells and round upward to a multiple of 10^−12. This is a whole-domain
certificate, not evidence inferred from checking 64 isolated parameter points.
For N=128 the implementation derives v=0.000338822592.

## 4. Bennett bound for whole clouds

For Y=U−E U, E Y=0, |Y|≤1 and E Y²≤v. For λ≥0, Taylor expansion and
E Y^k≤E|Y|^k≤v for every k≥2 imply

    E exp(λY) ≤ 1+v(exp λ−1−λ) ≤ exp[v(exp λ−1−λ)].

Apply the same argument to −Y. For M independent clouds, multiplication of
mgfs and exponential Markov, optimized at λ=ln(1+e/v), give

    P(|Ubar−p|≥e) ≤ 2 exp[−M B_v(e)],
    B_v(e)=(v+e) ln(1+e/v)−e.

This is the classical Bennett construction. A primary reference for its
variance-sensitive role is Maurer and Pontil, *Empirical Bernstein Bounds
and Sample Variance Penalization* (2009), Theorem 3:
https://www.cs.mcgill.ca/~colt2009/papers/012.pdf.
Our argument is given explicitly above; it uses an analytically certified
model variance, not a sample-variance plug-in or their empirical bound.

Choose c=3.69>ln40, as certified by the existing rational Taylor proof.
B_v is increasing for e≥0. Its rational lower bound uses the unchanged KL
logarithm routine. Bisection returns an outward e with M B_lower(e)>c.
If even e=1 is not excluded, return 1, which contains every possible mean
error. Inverting [Ubar−e,Ubar+e] with the existing outward geometric inverse
therefore gives model-conditional coverage at least 95% for fixed M.

A q-interval [L,U] with L>0 qualifies for relative 20% precision only if
(U−L)/(U+L)≤1/5. The associated estimator is the harmonic midpoint
2LU/(L+U). Empty intervals mean model-domain incompatibility, never precision.
The probability of a false precision release is unconditionally at most
5% under the assumptions; no conditional-on-selection claim is made.

**The new interval is not intersected with a separate 95% KL interval.**
There is no established nesting theorem between these two constructions.
Both are reported side by side, including any case where Bennett is wider.
There is no data-dependent method selection without error allocation.

## 5. Design gate, fresh checks and limits

For a prespecified true h, invert [pL(h)−2e,pU(h)+2e]. On the coverage event
this encloses all reported intervals; if its q-radius is ≤1/5, coverage and
precision occur jointly with probability at least 95% at that fixed budget.
Binary-search an integer sufficient budget and verify its certificate and
the immediate predecessor's failure. These are sufficient procedure
boundaries, not necessary or globally optimal sample sizes.

Compare against the unchanged refined KL procedure at h=0.1,0.25,0.5.
The primary gate requires at least a factor-two reduction at every point.
Only a passing gate authorizes the fixed 45,056-cloud fresh campaign in the
contract. No enlargement, reseeding, refitting or post hoc domain extension.
The strongest-curvature point lies at the fixed upper model boundary, which
helps precision. Small-curvature budgets may remain impractically large.

Independent sphere-lens quadrature checks the shared-anchor geometry without
using Lorentz moment polynomials. Symbolic integration checks moment constants.
Exact finite controls expose false pair independence, naive zero observed
variance and falsely independent duplicated clouds. These are internal
verification routes, not external peer review or external replication.
Unknown density remains nonidentifiable from the same causal relations;
absolute R needs independent T. Optional stopping is not protected.
