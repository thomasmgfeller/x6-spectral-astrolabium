# Five-element field integral: mathematical preparation and volunteer contract

7 November 2026. Source main: `3177458a7f8545f845054e235cd3dcd7e829eff3`
([PR 258](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/258)).
Status: **prepared, short controls passed, production NOT RUN**.
This is a numerical reference-model task. All eight physical gates remain HOLD.

## 1. Fixed question and measure

Compute the continuous matter amplitude for each of the **357 naturally
clock-labelled orders** on five new elements. The initial anchor is not one
of those five. Ideal recursion and independent transitivity filtering give
the same complete set. An unlabelled isomorphism quotient with uniform weights
is not an interchangeable input.

The anchor has T=-2, w=0. New clocks are T_j=-2+4h x_j with
0<x_1<...<x_5<1. Keep the inherited density law

\[
 \nu(dw)=\tfrac12\delta_0(dw)+\tfrac12\mathbf1_{(0,1)}(w)dw,
 \quad S_d=-\sum_{j=1}^5w_j a_j,\quad
 a_j=\tfrac12+4h^2\sum_{y\prec j}B_{k(y,j)}(x_j-x_y)^2.
\]

The sum includes the anchor x=0. B=(1,-9,16,-8), B_k=0 for k>=4;
k counts elements strictly between y and j. These are reference assumptions,
not a physical derivation of the dust measure or gravitational amplitude.

Integrate the five density variables analytically, exactly as in PR 257:

\[
 \chi(t)=\tfrac12+\tfrac12\frac{1-e^{-it}}{it},\quad \chi(0)=1,
 \qquad A_p(h,\mu)=120\int_{x_1<\cdots<x_5}\prod_{j=1}^5\chi(\mu a_j)\,d^5x.
\]

For real t, |chi(t)|<=1, since chi is the characteristic function of a
probability measure; hence |A_p|<=1. No Monte Carlo sampling is needed.
Set x_j=product_(k=j..5)u_k. The Jacobian is
J=120*u_2*u_3^2*u_4^3*u_5^4 on [0,1]^5 and integrates to one.
At mu=0 every A_p=1 exactly, requiring no production quadrature.

## 2. Derivative bounds without an expensive density-corner enumeration

For theta=-mu*sum_j w_j a_j, each clock coordinate has degree at most two.
Write any first or half-second derivative as sum_j w_j b_j(u). Elevate all
b_j to their common multivariate clock Bernstein degree. At a fixed clock
Bernstein index I let the coefficients be beta_(j,I). The full density
Bernstein corners select each coefficient or zero, so their minimum and
maximum are exactly

\[
 L_I=\sum_j\min(0,\beta_{j,I}),\qquad
 U_I=\sum_j\max(0,\beta_{j,I}).
\]

The convex-hull property bounds the polynomial between min_I L_I and
max_I U_I. This removes explicit enumeration of 2^5 density corners while
retaining the full tensor Bernstein enclosure. `prepare.py` implements this
with exact rational arithmetic and cached coefficient vectors. It is checked
against the original complete Bernstein routine, including three n=5 cases.
The theorem uses the linear dependence on w; it would not extend unchanged
to a nonlinear density action.

All derivative terms scale as h^2. The constant 1/2 has zero derivative.
Thus bounds at h=1/4 are one quarter of those at h=1/2. Multiplication by
|mu| gives bounds D>=|theta'|, 2A>=|theta''|.

## 3. Fixed quadrature and total error budget

For the k-th derivative of exp(i theta), differentiation of
f'=i theta' f with theta'''=0 gives the majorant recurrence

\[
 H_0=1,\quad H_1=D,\quad H_k=D H_{k-1}+2A(k-1)H_{k-2}.
\]

Positive density integration preserves this bound. For zero-based clock
coordinate j=0,...,4, Leibniz's rule and u in [0,1] give

\[
 B_{m,j}=120\sum_{l=0}^j {m\choose l}\frac{j!}{(j-l)!}H_{m-l}.
\]

For Gauss-Legendre quadrature on [0,1],
C_q=(q!)^4/[(2q+1)((2q)!)^3]. The positive Peano kernel also bounds the
complex absolute error. Positive normalized quadratures and telescoping
the five coordinate operators give

\[
 |A_p-Q_p|\le\sum_{j=0}^4 C_{q_j}B_{2q_j,j}.
\]

The standard Gaussian remainder is documented in
[NIST DLMF 3.5(v)](https://dlmf.nist.gov/3.5#v). Our model-specific
derivative bound and tensor application are specified above. All coordinate
maxima are over all 357 geometries, independent of observed integral values.
Choose the first even q in 8,...,128 making each coordinate bound <=1e-9.
The resulting global quadrature radius is <=5e-9. Require an accumulated
arithmetic radius <=4e-9 and total complex amplitude radius <=1e-8.

| h | mu | Fixed Gaussian orders | Points | Blocks of at most 65,536 |
|---|---|---|---:|---:|
| 1/4 | 1/4 | 10,12,12,12,14 | 241,920 | 4 |
| 1/4 | 1 | 18,20,20,24,28 | 4,838,400 | 74 |
| 1/2 | 1/4 | 18,20,20,24,28 | 4,838,400 | 74 |
| 1/2 | 1 | 44,46,50,56,76 | 430,707,200 | 6,573 |

There are 440,625,920 points and 6,725 blocks in total. The largest
configuration accounts for 97.75% of points. The two equal grids have
different integrands: the constant mu/2 differs. Do not reuse their values.
At every point 89 distinct density polynomials are shared across geometries,
followed by shared prefix products. The q=76 rule exceeds the old kernel's
q<=64 cap; the new cap is explicitly 128. No old production result is changed.

These are exact operation counts, not measured runtime or a cost quotation.
The plan was frozen before the new nonzero point controls. This is local
planning, not external preregistration or a blind physical prediction.

## 4. Finite sums can be distributed without a new approximation

Index the tensor grid lexicographically, last coordinate fastest. For N
points and B=65,536, block s is [sB,min((s+1)B,N)). These ranges are disjoint
and cover exactly 0,...,N-1. A block returns the unnormalised weighted sum
for every geometry and its Jacobian weight sum. Summing all blocks recovers
the original finite quadrature exactly. Do not average blocks or divide
them by their local Jacobian mass.

Each endpoint is an integer divided by 2^60. Whole-block endpoint sums use
Python integers and are exact; there is no floating-point reduction-order
error. The analytic quadrature radius is added **once after complete
collection**, not once per block. Incomplete or duplicate block sets cannot
produce a final amplitude. The full normalization interval must contain 1.

The inherited arithmetic uses outward interval rounding, range-reduced
Taylor enclosures and checked signed 128-bit integer operations. See
[GCC overflow builtins](https://gcc.gnu.org/onlinedocs/gcc/Integer-Overflow-Builtins.html).
An overflow, timeout or failed error budget means rejection, never PASS.
The global 60-bit arithmetic budget is an acceptance criterion; its success
for the unrun large integral is not presumed. If it fails, a separately
reviewed higher-precision revision is needed, preserving the rejected output.

## 5. Reuse across couplings and expected mathematical benefit

Once A_p is enclosed, gravitational phases and alpha do not require new
five-dimensional integrations:

\[
 a_5(g,\mu)=\frac1{357}\sum_p e^{igG_p}A_p(\mu),\quad
 G_p=S_g(p)-1,\quad c_5=\frac{357h^5}{120}2^{-10\alpha}.
\]

The collector provides a_5 and visibility bounds for g/pi=0,1/18,1/9.
If |a_5-t|<=epsilon and |a_5|<=1, the conservative visibility radius is
2epsilon+epsilon^2 around |t|^2, intersected with [0,1]. The same matter
integrals serve alpha=1,2. Lower-number amplitudes remain those of PR 258.

Keep its exact c_6, Z_6 and alpha-dependent Delta_6. The unknown higher-field
rest after a successful n=5 computation is R_6=c_6+Delta_6; before it was
c_5+c_6+Delta_6. With Zmax=Z_6+Delta_6, the remaining upper weight fractions
would be:

| h | alpha | Before n=5 | After n=5 (excluding known-sector numerical errors) |
|---|---:|---:|---:|
| 1/4 | 1 | 2.25060e-6 | 4.03224e-8 |
| 1/4 | 2 | 2.18989e-9 | 1.20408e-12 |
| 1/2 | 1 | 5.72832e-5 | 2.09017e-6 |
| 1/2 | 2 | 5.67224e-8 | 6.23763e-11 |

Exact fractions are in plan.json. These are prospective uncertainty
budgets, not measured results. The maximal removed fraction of the old
unknown-field weight is 96.35–99.95%; existing errors must still be added.

For the number-preserving filter set S_+/-=sum_(n<=5)c_n v_n^+/-. Then
P_count lies in [S_-/Zmax,min(1,(S_++R_6)/Zmax)]. For the coherent all-number
channel, use t=sum_(n<=5)c_n t_n/Z_5 and radius
sum_(n<=5)c_n epsilon_n/Z_5+2R_6/Zmax before the visibility map. Retain the
intersection with valid predecessor bounds. This final integration into the
PR 258 evidence is a subsequent review after external results; the present
collector only produces the n=5 channels and does not rewrite prior files.

## 6. Acceptance and scientific limits

1. Validate source hashes and reproduce the short controls on a second machine.
2. Obtain timing samples across the fixed grid; reserve block IDs publicly.
3. Execute only the agreed blocks on donated resources. Return failures too.
4. A separate contributor replays every accepted production block. Hashes
   identify bytes; they do not prove numerical correctness or independence.
5. Collect a complete unique set per configuration. Check normalization,
   quadrature and arithmetic budgets. A complete collection alone remains
   provisional until its external replay ledger is reviewed.
6. Review the channel and tail propagation before updating scientific evidence.

The controls include full-action identities, simplex/cube moments, original
versus optimized Bernstein bounds, interval arithmetic, exact block
additivity, analytic mu=0 cases, nonzero n=5 point enclosures and rejected
invalid collections. They are finite software checks, not a formal proof
assistant or external replication. The production integral is NOT RUN here.

MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING and
EXTENSION all remain HOLD. This task does not choose a physical measure,
derive four-dimensional CST dynamics, establish backreaction, close a
junction or predict a bounce. An absent volunteer or an unsuccessful run
does not erase the mathematical preparation or justify a physical claim.
