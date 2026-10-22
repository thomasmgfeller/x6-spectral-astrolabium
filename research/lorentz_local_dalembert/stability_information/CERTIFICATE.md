# Scope and construction of the exact certificate

SPDX-License-Identifier: Apache-2.0

The coordinates are the frozen search's 12-decimal rounded pair, interpreted
as exact rationals. The scale is the archived JSON decimal, also an exact
rational; its last-bit interpretation differs from binary floating point and
the certificate recomputes every relevant quantity under this stated choice.
The pair is a post-search smaller-pair diagnostic, not a strong search success.

## Geometry and weights

All 210 unordered interval signs and causal time directions at each endpoint
are evaluated by integer/Fraction arithmetic, with no tolerance in the sign
comparison. The minimum absolute interval is positive at both endpoints. The
first endpoint is very close to the frozen order margin (~1.000258e-8); this
is retained and is one reason not to infer a wide stable neighborhood.

The landmark basis is triangular with nonzero diagonal, so its Gram matrix
has exactly one negative and two positive eigenvalues by congruence. Exact
inversion of the 9x9 moment Schur matrix establishes full row rank and the
unique minimum-energy weights. Both the moment constraints and KKT stationarity
are checked as exact rational equalities. The original intrinsic moment
constraints are checked independently after the landmark coordinate change.

For symmetric H, cond_2(H)<=||H||_inf||H^-1||_inf. For the original intrinsic
design D, cond_2(D)^2=cond_2(DD')<=||DD'||_inf||(DD')^-1||_inf. Exact rational
inverses and outward square roots therefore prove the original condition
cutoffs, as well as rank; the gates are not inferred only from floating SVD.

## Means, covariance and discrepancy

Let K=19 C+diag(N), so C_alpha=K/20. Bareiss fraction-free elimination produces
74 positive leading principal minors. Sylvester's criterion proves positive
definiteness exactly; the minor sequence's digest is recorded.

NumPy proposes an inverse, symmetrized and rounded to a rational matrix P with
denominator 10^18. It is only a proposal. The exact integer matrix residual
R=I-C_alpha P has ||R||_inf=eta<1. The Neumann-series bound gives

||C_alpha^-1-P||_inf <= ||P||_inf eta/(1-eta) = E.

The frozen pair's residual is about 6.01e-13 and E<1.48e-13. A different BLAS
may propose a slightly different P; each proposal must pass the exact bound.
Since the inverse and P are symmetric, for any v the quadratic error is at
most ||v||_1 ||v||_inf E. No exact dense rational inversion is required.

Pi is enclosed using Machin's identity and alternating rational arctangent
series. Square roots use integer isqrt on a 65-decimal grid, with directed
endpoints. Multiplying positive bounds encloses each
mu=(rho*pi/12)*scale^3*q^(3/2), then rounds outward to 30 decimal places.

For a residual vector enclosed by midpoint v and coordinate half-width delta,
the midpoint quadratic form v'Pv is exact. Its mean-rounding error is bounded by

||P||_inf [2 ||v||_1 delta + m delta^2].

The additional inverse error is bounded by

(||v||_1+m delta)(||v||_inf+delta) E.

Adding both bounds gives the reported rigorous intervals for the mean-pair
discrepancy and both discrepancies from actual N. Their upper endpoints remain
strictly below the frozen limits. The common deterministic observation set
therefore contains both geometries.

## Target gap and lower bound

The weights and their differences are exact rationals. Integer square-root
bounds enclose the l2 gap and both norms, hence the symmetric relative gap.
The triangle-inequality proof in THEORY.md then applies to any estimate in
this fixed information model. The sign-field witness has exact integer nodal
values and a rational response gap. It is postselected and may be highly
oscillatory; no smooth-field or continuum claim is made.

This is a finite certificate for one pair, not a verified global optimization,
a probability statement, a joint Poisson divergence bound or a validation of
the entire original A/B causal graph. The certificate does not turn numerical
nonconvergence elsewhere into evidence of absence.
