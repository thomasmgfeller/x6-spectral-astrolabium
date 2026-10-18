# Sharper fixed-budget C2 intervals using binary relative entropy

## Scope and unchanged assumptions

The target remains q=R T² for the known uniform physical-volume 4D de Sitter
family, with 0≤h≤1/2, independent identical clouds, fixed point count N and
prespecified cloud count M. The rational geometry and its monotonicity proof
from `../lorentz_de_sitter_c2/DERIVATION.md` remain unchanged. This study
improves a concentration bound, not the observation model or identifiability.
There is no physical time calibration, unknown-density guarantee or optional
stopping permission. No new general concentration theorem is claimed.

## 1. Preserve the Bernoulli moment-generating function

Let g(X_i,X_j)∈{0,1} indicate comparability, with expectation p. Within each
cloud, U=C2/choose(N,2) is the average over all pairs. For m=floor(N/2),
average the m disjoint pairs in a uniformly permuted cloud. Its conditional
permutation average is U. For every fixed permutation, the m pair indicators
are iid Bernoulli(p). Jensen's inequality therefore gives

    E exp(λmU) ≤ (1−p+p exp(λ))^m.

For M independent clouds and S=Mm,

    E exp(λS Ubar) ≤ (1−p+p exp(λ))^S.

This uses S=M floor(N/2), **not** M choose(N,2). No pair independence within
a whole cloud is asserted. Optimizing the exponential Markov bound gives

    P(Ubar≥u) ≤ exp[−S D(u||p)] for u≥p,
    P(Ubar≤u) ≤ exp[−S D(u||p)] for u≤p,
    D(u||p)=u ln(u/p)+(1−u) ln((1−u)/(1−p)).

By the two one-sided bounds,

    P(S D(Ubar||p)>c) ≤ 2 exp(−c),  c=3.69>ln(40).

Endpoint values u=0 or 1 use the continuous limit 0 ln(0)=0. The existing
rational Taylor certificate proves exp(3.69)>40, hence failure probability
is below 5%. This is the classical Chernoff/Hoeffding reduction for a binary
kernel; see Hoeffding (1963), Sections 2 and 5,
https://doi.org/10.1080/01621459.1963.10500830.
The complete reduction is given above rather than treating the data as binomial.

The previous method instead bounded the centered mgf quadratically. The KL
construction retains the binary-kernel probability dependence, potentially
improving precision when p is far from 1/2, as it is in this model.

## 2. Numerical decisions retain mathematical enclosures

For a positive rational x, write x=2^k y, 1≤y≤2. Set z=(y−1)/(y+1),
so 0≤z≤1/3. Use

    ln(y)=2 Σ[j=0..23] z^(2j+1)/(2j+1) + remainder,
    0≤remainder≤2 z^49/[49(1−z²)].

The same enclosure at y=2 supplies ln(2); negative k reverses its interval
endpoints before multiplication. Exact rational arithmetic gives outward
logarithm and KL bounds. The KL lower bound may be clipped at zero, since
relative entropy is nonnegative. No floating logarithm decides an exclusion.

Geometric probability endpoints are rounded outward to multiples of 2^−64
before KL evaluation. This contains the already certified geometric interval.
Floating values in output files are for presentation and numerical cross-checks.

For observed u, retain every h for which S D(u||p(h))≤c. Because D(u||p)
decreases for p<u and increases for p>u, and p(h) is strictly increasing,
this set is an interval, possibly empty. At a rational bisection point discard
lower h values only when p_upper<u and the **lower** KL bound at (u,p_upper)
exceeds c/S. Discard upper h values analogously using p_lower>u. After
36 steps return an outer enclosure; ambiguous numerical decisions retain
parameters. Empty sets mean model-domain incompatibility, not precision.

## 3. Nesting inside the existing reference without spending more alpha

Binary Pinsker follows directly: for fixed p,

    f(u)=D(u||p)−2(u−p)²,
    f''(u)=1/[u(1−u)]−4≥0,  f(p)=f'(p)=0.

Thus D(u||p)≥2(u−p)², including endpoints by continuity. Every exact KL
confidence set is contained in the exact quadratic/Hoeffding band at the
same c and S. The old outward implementation contains that quadratic band.
Intersecting the new outer KL interval with the old reported interval still
contains the entire exact KL set and **preserves its 95% coverage**. This is
not an arbitrary intersection of two unrelated 95% procedures, which would
require a different error allocation. Reported intervals cannot become wider.

The unchanged outward q transform and harmonic midpoint rule apply: for
q∈[L,U], L>0, the midpoint 2LU/(L+U) has relative error at most (U−L)/(U+L).
A precision report requires that exact radius to be ≤1/5. Under the stated
model and fixed budget, wrong precision has unconditional probability ≤5%.
This does not assert 95% coverage conditional on selection for precision.

## 4. Sufficient design budgets and a fair comparison

At a prespecified true h, obtain a geometric probability enclosure [pL,pU].
On the KL coverage event, Ubar belongs to

    A = union[p∈[pL,pU]] {u∈[0,1]: S D(u||p)≤c}.

Compute an outer [uL,uU] by first-argument bisection. For u<pL, exclusion is
safe only when a lower bound for D(u||pL) exceeds c/S; for u>pU use pU.
This works because ∂D(u||p)/∂p=(p−u)/[p(1−p)]. Round [uL,uU] outward.

To enclose the union of confidence intervals for observations in [uL,uU],
discard a lower h segment only if p_upper<uL and D_lower(uL||p_upper)>c/S;
use the symmetric rule above uU. Intersect with the reference union obtained
by inverting [uL−ε,uU+ε]. This outer interval contains every actual report on
the KL event. If its q-radius is ≤1/5, coverage and precision are jointly
achieved with probability ≥95% at that fixed budget and true h.

For the Hoeffding comparator retain the original 2ε design rule. Locate a
sufficient integer M for each method by the specified binary search, then
check both its passing certificate and the adjacent M−1 failure. These are
refined sufficient design boundaries for the specified procedures, not
necessary or statistically optimal sample sizes. The comparison does not
reuse the old coarse powers-of-four grid as though those counts were minima.
The primary gate requires at least a twofold reduction in these sufficient
counts at **each** nonzero prespecified h in {0.1,0.25,0.5}.

## 5. Fresh checks and interpretation

Only if the budget gate passes, execute the bounded fresh-seed campaign:
4096 clouds each at h=0,0.1,0.25 and 65536 at h=0.5, all N=128. Report paired
Hoeffding/KL intervals at the declared group sizes, preserving every outcome.
The larger h=0.5 campaign tests useful precision in the already declared
domain; its upper boundary can help precision and must not be generalized.
Grouping reuses clouds across budgets, so no pooled independent success rate
is reported. In particular, four groups at M=16384 or one group at M=65536
do not estimate a population qualification rate precisely.

The coverage proof is analytical; the simulations check implementation and
illustrate precision. Large planning counts are not simulated. Failure of
the gate or any check is retained without refitting, reseeding or enlargement.
All scientific sources from the previous stages remain unchanged.
