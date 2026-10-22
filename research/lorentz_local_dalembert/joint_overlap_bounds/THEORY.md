# Joint overlap confidence constraints

SPDX-License-Identifier: Apache-2.0

Scope: the fixed conditional-A, independent homogeneous Poisson-B experiment
in flat 2+1 with known density. No conditional-on-PASS or sequential guarantee.
The Poisson restriction principle is described in Last and Penrose,
*Lectures on the Poisson Process*, Chapter 5:
https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf . The following finite
confidence construction and projection proof are supplied here explicitly.

## A covered joint set

For each A-selected pair of intervals I_i,I_j, the recorded overlap C_ij
and counts N_i,N_j yield three observations

C_ij=B(I_i intersect I_j), A_ij=N_i-C_ij, A_ji=N_j-C_ij.

They count disjoint sets for this pair, so have independent Poisson laws with
means v_ij, a_ij, a_ji. Across different pairs independence is neither assumed
nor needed. The means satisfy mu_i=v_ij+a_ij and mu_j=v_ij+a_ji.
Apply the prior proved scalar interval [L_c(n),U_c(n)] to each of these three
observations with c=20, and to original marginals with c=12. For M=1736 and
K=230796 (three observations for each unordered pair within each packet),

$$\Pr(\text{all constraints cover their true means}\mid A)
\ge 1-2M e^{-12}-2K e^{-20}>0.97771588268635579693.$$

K counts repeated/dependent observations conservatively. None is selected
using B. The small decrease from the previous marginal-only coverage pays
for the additional simultaneous constraints; the old percentage cannot simply
be carried over unchanged. This is repeated-sampling coverage, not a posterior
probability or an accuracy guarantee. An empty feasible set must not produce
an accuracy certificate. Resource aborts require abstention/full sets.

Eliminating v gives the valid necessary inequalities

$$L_{20}(A_{ij})-U_{20}(A_{ji})\le\mu_i-\mu_j
\le U_{20}(A_{ij})-L_{20}(A_{ji}).$$

Also L(C)+L(A_ij)<=mu_i<=U(C)+U(A_ij), and similarly for j.
These inequalities are consequences of the joint set, not a characterization
of its full projection. Discarding constraints makes an outer relaxation and
therefore preserves coverage. No Gaussian covariance approximation is used.

## Exact order information

Orient I_i=I(a_i,b_i) using the recorded strict endpoint order. If
 a_j<=a_i and b_i<=b_j, then I_i is contained in I_j by transitivity.
Thus mu_i<=mu_j and mu_j-mu_i is the mean of the observed exclusive count
N_j-C_ij, with its own c=20 bounds. The observed identity C_ij=N_i is checked
exactly. This is set inclusion, not inference from coincident observed counts.

If the two lower endpoints are comparable and the two upper endpoints are
comparable, their intersection is I(max(a_i,a_j),min(b_i,b_j)). If these
endpoints are not strictly causally ordered the intersection is empty;
otherwise, if this interval is in the selected list, its mean is exactly
mu_k. Apply the bounds on C_ij to mu_k and bounds on the exclusive counts
to mu_i-mu_k and mu_j-mu_k. Recorded count identities are checked exactly.
Spacelike-incomparable lower or upper endpoints are not arbitrarily ordered.

Every valid geometry satisfying the complete selected endpoint order obeys
these constraints. The converse is false: a mean vector passing them need not
admit any Lorentzian embedding. The algorithm does not certify all geometric
rank/signature constraints or all nontrivial overlap volumes.

## Certified propagation

Introduce mu_0=0 and a directed graph: edge i->j of weight d_ij encodes
mu_j-mu_i<=d_ij. Round every upper bound outward onto a 10^-6 count lattice.
For each path, summing its inequalities gives a valid difference upper bound.
Floyd-Warshall takes the minimum of these valid bounds. Integer arithmetic is
exact here; a checked magnitude bound protects the int64 additions. A negative
cycle proves the relaxation empty and triggers abstention. No edge is dropped.

The resulting marginal enclosure is [-d_i0,d_0i], intersected with the original
exact rational box. Every original feasible mean vector remains enclosed.
For reporting, the pair-difference width is d_ij+d_ji. Compare it to the width
of the old independent-coordinate projection, (U_i-L_i)+(U_j-L_j).
These are projection widths, not volume ratios or population accuracy.

Only marginal enclosures are passed to the prior polynomial/resolvent bound.
This discards joint information. Failure to improve that bound therefore does
not imply that the new joint information has no value. A future bound must
retain the difference constraints throughout its polynomial and matrix analysis.

## Witness interpretation

Directed rational enclosures evaluate the mean vectors of the two exact PR88
geometries against every propagated edge. Both pass. This proves membership
in the computed necessary relaxation only. In particular it does not verify
their general intersection volumes against every overlap observation. Do not
transfer the old recovery lower bound to the full overlap-constrained geometry
set without that missing check. No statistical indistinguishability is proved.
