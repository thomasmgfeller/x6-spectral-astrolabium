# Full joint count-law bound through membership atoms

SPDX-License-Identifier: Apache-2.0

## Experiment and exact representation

Retain the unchanged pair selected in PR95: one support point moves, with all
landmarks, root, outer diamond, scale and known homogeneous Poisson density
fixed. The 90 selected intervals include the outer diamond. For each nonzero
90-bit pattern b, let A_b be the region belonging to exactly the intervals
whose bits are one. These regions are disjoint and partition the outer diamond
up to null boundaries. Their populations N_b are independent Poisson variables
with intensities lambda_b=rho*physical_volume(A_b).

Every interval count is sum_b b_i N_b. Every overlap count of order k is
sum_b (b_i1 ... b_ik) N_b. Consequently the complete dependent observation
vector is a deterministic function of the independent ATOM counts. This does
not make the interval counts independent. The optional total physical B count
is the outer total plus a common independent Poisson count outside the outer
diamond; adding that shared channel does not increase total variation.

The atom experiment is an upper-information comparison even if only ordinary
counts/pairwise overlaps are observed. We do not require enumerating all 2^90
patterns: unenumerated patterns must be retained through a rigorously bounded
residual intensity, never declared absent because a mesh did not find them.

## Poisson affinity and TV

For one Poisson coordinate, sum the geometric exponential series in the
square roots of its two probability masses:

    sum_n sqrt(Poi(lambda)(n)*Poi(mu)(n))
      = exp(-(lambda+mu)/2 + sqrt(lambda*mu)).

Multiplying over the finitely many atom labels gives affinity exp(-J/2), where

    J = sum_b (sqrt(lambda_b)-sqrt(mu_b))².

Writing p-q=(sqrt(p)-sqrt(q))(sqrt(p)+sqrt(q)) and applying Cauchy-Schwarz yields
TV<=sqrt(1-affinity²)=sqrt(1-exp(-J))<=min(1,sqrt(J)). Deterministic processing
cannot increase TV: pull back any output event to an input event. This proves
the same upper bound for all recorded counts and overlaps together. Zero
intensities are permitted; no logarithms or absolute-continuity assumptions
are required. Leskela's Theorem 5.3 gives the general Poisson-process result;
the finite calculation above fixes our normalization explicitly.

## Safe treatment of unresolved volume

Suppose certified cell interiors provide atom lower intensities a_b<=lambda_b
and c_b<=mu_b. The known upper total outer intensity U_upper gives residuals
R0=U_upper-sum_b a_b and R1=U_upper-sum_b c_b. Extend both finite dictionaries
by zero on every other possible label. Since

    (sqrt(a+r)-sqrt(a))² <= r,  a,r>=0,

we have ||sqrt(lambda)-sqrt(a)||_2<=sqrt(R0), and similarly for mu. Therefore

    sqrt(J) <= ||sqrt(a)-sqrt(c)||_2 + sqrt(R0)+sqrt(R1).

This is the implemented deterministic bound. Directed rational square roots
bound every term. It remains valid for atoms appearing only in one geometry,
rare patterns, and labels never certified in either mesh. If dictionaries are
empty with total upper intensity 1, the result is TV<=1, not a false zero-TV
certificate. Negative lower intensities and totals below their sum are rejected.

This residual treatment is deliberately conservative. Separate uncertainty
in two geometries can swamp their small intensity DIFFERENCE. A vacuous result
is a numerical enclosure failure, not evidence that actual TV is large.

## Certified rectangular-cell integration

Use the inherited outer-diamond bounding box in the rational Lorentz-boosted
frame. Round it outward and all endpoints outward on the 2^-16 coordinate
grid. Partition the box into 16³, 32³ and 64³ rectangular cells using integer
edges. The partitions are nested. Every cell is processed; no random sampling
is used. Volume is the exact integer product of side lengths times 2^-48.
The physical intensity multiplier rho*scale³ is exact rational input.

For each endpoint, interval arithmetic bounds the time difference and spatial
squared distance over the WHOLE cell and endpoint enclosure. Guaranteed cone
interior requires dmin>0 and dmin²>rmax; possible interior requires dmax>0 and
dmax²>=rmin. Combining future and past cone bounds encloses each interval's
membership. Only when all 90 memberships are certain is its entire volume
assigned to one atom. Other cells remain unresolved.

The nonzero labels cover points inside the outer interval, because that
interval is itself one of the 90 observations. Zero-label cells outside it are
ignored. Exact outer volume, rather than the much larger box volume, supplies
the residual intensity. The artificial bounding box is only an integration
device and does not change the physical sampling model.

Coordinate magnitudes are checked below 10^7, so squared differences and
sums fit int64. The total integer box volume is checked below 2^63; all cell
and atom integer volumes fit as well. Integer volume conservation is checked
at each stage. The audit additionally checks monotonic lower volumes under
refinement, a cone-crossing cell, and 1,719 independent rational point-membership
comparisons within 191 cells declared certain. These samples audit code;
whole-cell validity follows from the interval inequalities above.

## Controls: improvement and dependence

For atom intensities (100,100) versus (99,101), a common coupling shifts a
Poisson(1) component between two labels: (A+M,B) versus (A,B+M), where
A~Poi(99), B~Poi(100), M~Poi(1) are independent. It gives TV<=1-exp(-1), about
0.63212056. Exact atom intensities instead give sqrt(J)<=0.070711784. This
illustrates a sharper CERTIFICATE, not an actual TV calculation and not a
result for the repository geometry pair.

As a dependence control, on the eight three-bit labels use intensities
1 +/- (1/4)*(-1)^popcount(b). Both totals are 8 and all singleton and pairwise
intersection means agree. Triple intersection means are 3/4 and 5/4, so the
mixed third cumulant of the three ordinary counts differs. First and second
moments alone therefore do not identify their full law. This does not claim
that the JOINT DISTRIBUTION of pairwise-overlap observations is identical.

## Actual pair result and stopping decision

The fixed budget processes 299,008 cells per geometry across all three levels.
At the final level, 48 nonzero patterns have positive certified lower volume
in each geometry. Those are certified patterns, not a complete support list.
The unresolved mean upper bound remains 11,771.54685595 in each geometry out
of total outer mean about 21,164.10351. The new atom TV bound is 1 at all stages.
The older valid coupling bound, 0.24999999774322784776, is retained; there is
NO improved certified TV for the actual pair.

If the known square-root distance were exactly zero and residuals equal,
this particular sqrt(J) enclosure would need R<=1/64=0.015625 in each geometry
to certify TV<=1/4. The observed residual is roughly 753,379 times that ideal
allowance. This compares intensity budgets, NOT required mesh sizes or runtime,
and is not a lower bound on the accuracy needed by every possible method.

Status: HOLD_VOLUME_RESOLUTION. Stop uniform-grid refinement at the fixed
budget. The next promising task is to bound PAIRED atom-intensity differences
and common positive background masses directly, allowing shared boundary
uncertainty to cancel, rather than estimating two complete volume tables
separately. This requires a new validated construction before any stronger
statistical claim. No new geometry search, strong counterexample, global
stability, estimator accuracy guarantee or physical validation is claimed.
All earlier scientific HOLDs remain.

## Reference

L. Leskela, Information divergences and likelihood ratios of Poisson processes
and point patterns, arXiv:2404.00294v2, Theorem 5.3 and Section 6.2.
https://arxiv.org/html/2404.00294v2 ; DOI:10.1109/TIT.2024.3472448.
The finite affinity calculation, unresolved-mass enclosure, geometric
integration audit and repository-specific feasibility result are provided here.
