# C2 in a restricted 4D de Sitter diamond: exact enclosures and confidence

This is a model-conditional construction for dimensionless q = R T²,
with **known uniform physical-volume sampling**, independent clouds of N iid
points and a fixed cloud count M. The domain 0 ≤ h ≤ 1/2 is fixed in advance.
No statement identifies curvature under an unknown sampling density.
No physical measurement, absolute time calibration or external replication
is supplied. The proof below and its code remain open to external audit.

## 1. Geometry without a local-curvature truncation

The coordinate diamond is −1/2 ≤ t ≤ 1/2, |x| ≤ 1/2−|t|, with conformal
scale factor (1−h t)^−1. Physical density relative to flat coordinate volume
is W_h(t)=(1−h t)^−4. V0=π/24 and

    z = h²/4 ∈ [0,1/16],
    V(h)/V0 = V(z) = Σ[j≥0] 2 z^j/(j+2).

This follows by integrating t^(2j) over the flat diamond; odd moments vanish.
For two independent points, p(h) is the probability they are causally related.
Write p=N(z)/V(z)², where N is the unnormalized comparable-pair integral
divided by V0². Time reversal and interchange of the two ordered points
remove every odd power of h. The degree-16 numerator is obtained by exact
rational integration, not a fit to simulations or the RSS expansion.

For t<u, set a=1/2+t, b=1/2−u, d=u−t. Let K(t,u) be the spatial pair volume
divided by π². Its four polynomial pieces are:

1. −1/2≤t≤u≤0: K=(16/9)(1/2+t)³(u−t)³.
2. 0≤t≤u≤1/2: K=(16/9)(1/2−u)³(u−t)³.
3. t≤0≤u, u−t≤1/2: K=F(a,b,d).
4. t≤0≤u, u−t≥1/2: K=(16/9)(1/2+t)³(1/2−u)³.

Here

    18 F = a⁶+b⁶+d⁶ −9(a⁴b²+a⁴d²+a²b⁴+a²d⁴+b⁴d²+b²d⁴)
           +16(a³b³+a³d³+b³d³)+18a²b²d².

To derive F, integrate 4πs² times the overlap volume of two balls over
0≤s≤d. For |a−b|≤s≤a+b the overlap is
π(a+b−s)²[s²+2s(a+b)−3(a−b)²]/(12s); below |a−b| it is the smaller ball.
In region 3, |a−b|≤d≤a+b. The resulting polynomial is symmetric in a,b,
so either radius ordering gives the same F. In the same-sign time regions
d=|a−b|; in region 4 d≥a+b. This exhausts the ordered time domain.

Each monomial t^i u^j is integrated between affine rational boundaries.
The factor 2π²/V0²=1152 converts the ordered integral into N. Explicitly,

    n_j = 4^j Σ[i=0..2j] choose(i+3,3) choose(2j−i+3,3)
          ×1152 ∫[t<u] K(t,u) t^i u^(2j−i) dt du.

The first coefficients are n0=1/10, n1=14/75, n2=79/315, n3=218/735.
All seventeen coefficients are regenerated with exact fractions.

## 2. Uniform truncation and monotonicity certificate

Because |t|,|u|≤1/2 and the flat comparable probability is 1/10,

    |n_j| ≤ choose(2j+7,7)/10.

The Vandermonde sum of the two weight coefficients gives this bound.
Uniform convergence on |h|≤1/2 justifies integration and differentiation
term by term. For the omitted numerator terms, beginning at J=17, use

    e_N(z) = [choose(2J+7,7) z^J/10] / (1−r),
    r = z (2J+9)(2J+8)/[(2J+2)(2J+1)].

The ratio decreases thereafter. For the z-derivative tail multiply the
first term by J/z and replace r with r(J+1)/J. At z=0 both tails are zero.
For volume the nonnegative tail is at most

    e_V(z) = [2 z^J/(J+2)]/(1−z).

Its derivative tail uses first term 2J z^(J−1)/(J+2) and ratio upper bound
z(J+1)/J. All these bounds are rational on rational input.

Let N16,V16 be the polynomials. A probability enclosure is

    (N16−e_N)/(V16+e_V)² ≤ p ≤ (N16+e_N)/V16²,

clipped to [0,1]. V16≥1. The code also bounds the enclosure width uniformly
by 2e_N+(||N16||+e_N)(2e_V+e_V²), using coefficient absolute norms at zmax.

For monotonicity, p'(z)=[N'V−2NV']/V³. The polynomial D=N16'V16−2N16V16'
is bounded below on [0,zmax] by its constant term plus all negative
coefficients evaluated at zmax. Bound the omitted difference in absolute
value by

    ||N16'|| e_V + e_N' (||V16||+e_V)
    +2[||N16|| e_V' + e_N (||V16'||+e_V')].

The remaining rational lower bound is strictly positive. Thus p is strictly
increasing in z, and hence in h on this domain, including the endpoint 0.
This is a finite rational inequality over the entire interval, not a
monotonicity test on a grid. `certificate()` fails closed if it is not positive.

## 3. Dependent pairs and a finite-sample probability band

For a cloud, U=C2/choose(N,2) is a degree-2 U-statistic with a [0,1] kernel.
Let m=floor(N/2). Average the m disjoint-pair kernel values over a uniform
random permutation of the points. Conditional on the point cloud, the
permutation average is U, since each unordered pair has equal probability
of appearing. For each fixed permutation its m terms are independent.
Jensen's inequality and Hoeffding's bounded-variable lemma therefore give

    E exp[λ(U−p)] ≤ exp[λ²/(8m)].

For M independent equal-N, equal-model clouds, their average Ubar satisfies

    P(|Ubar−p|≥ε) ≤ 2 exp[−2Mm ε²].

Individual pairs within a cloud have never been assumed independent.
Use ε≥sqrt(3.69/(2Mm)), rounded upward to a rational multiple of 2^−40.
A finite positive Taylor sum proves exp(3.69)>40, so the failure probability
is strictly below 0.05. The band is pointwise for a **fixed M**. Looking at
several budgets and stopping at a favourable result has no such guarantee.
This is the classical Hoeffding reduction, not a new concentration theorem:
W. Hoeffding (1963), *Probability Inequalities for Sums of Bounded Random
Variables*, DOI https://doi.org/10.1080/01621459.1963.10500830, Sections 4–5.
The construction and proof are stated here to make the dependency explicit.

## 4. Conservative inversion and reporting

Invert [Ubar−ε,Ubar+ε] intersected with the image of [0,1/2]. At each rational
bisection point, discard a lower segment only if the **upper** bound for
p is below the band's lower edge; discard an upper segment only if the
**lower** bound for p exceeds its upper edge. Return an outer enclosure
after 36 iterations, or an empty set only when the entire model domain is
excluded by certified bounds. An empty result is reported as incompatibility,
never as precision. With probability at least 95% the true h is retained.

Map to q=48 atanh(h/2)² using twenty positive terms of the atanh series and
the tail x^41/[41(1−x²)], x=h/2. Rational outward bounds retain q as well.
For q∈[L,U], L>0, H=2LU/(L+U) obeys |H/q−1|≤(U−L)/(U+L).
Only a nonempty interval with this radius ≤1/5 qualifies for relative 20%
precision. For L=0 the procedure abstains. Wrong precision has unconditional
probability at most 5% under the declared model and fixed budget. This is
not 95% conditional coverage among selected reports.

## 5. A sufficient budget, not an estimated optimum

At a specified true h, enclose p(h), enlarge it by **2ε**, and invert. On
the same coverage event, the actual data band lies inside this enlarged
band. If its q-radius is ≤1/5, the procedure therefore both covers and
qualifies with probability at least 95%. The reported first passing power
of four is a sufficient fixed-budget design value, not a global minimum.
These deterministic large-budget calculations do not simulate that many
clouds. Unknown density, dependent clouds, changing geometry, measurement
errors and optional stopping are outside this theorem.

The fresh simulations are implementation stress checks, not the proof of
coverage. Nested grouping reuses the same clouds across budgets; no aggregate
independent coverage estimate is made. The old geometric quadrature is an
independent numerical cross-check, not the source of the certified bounds.
