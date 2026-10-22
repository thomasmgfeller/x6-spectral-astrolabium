# Count-to-operator stability audit

SPDX-License-Identifier: Apache-2.0

This is a diagnostic on the 20 already observed selected A configurations in
PR87, using only candidate B0 counts, overlaps, selected-node causal order,
density and scale. It is not a new independent validation campaign. No simulator
truth, field values, source-A graph or B point coordinates enter the search.
All 20 cases, including count/base failures, remain in the inventory.

## Boundary and target

The target w(z) is the existing unique minimum-energy, quadratic-moment-exact
operator weight vector on the fixed root/support nodes. It is a discrete target,
not the unknown continuum d'Alembertian. The available count mean is
mu_ab(z)=rho*pi/12*scale^3*q_ab(z)^(3/2), q_ab=-(z_b-z_a)'eta(z_b-z_a), on the
unchanged four-landmark input mask. Six continuous Poincare gauge freedoms are
fixed as in the prior fitter. All observed selected-node causal relations are
required at both endpoints; the full original A/B poset is outside this boundary.

Use C_alpha=.95*C+.05*diag(N), fixed exactly as in PR86. This empirical matrix
defines a deterministic norm, NOT a calibrated confidence set or joint Poisson
likelihood. Close mean vectors need not imply close full joint count/overlap
distributions. We do not model C's geometry-dependent sampling distribution.
No Cramer-Rao, Le Cam, coverage or unconditional statistical-impossibility claim
can be inferred solely from this diagnostic.

## Fixed search

The archived full-GLS algorithm supplies one order-consistent starting geometry
per case. This is a feasibility seed, not adoption of the rejected estimator.
Reject bases with failed original gates, rank-deficient local Jacobian, or
(mu-N)'C_alpha^-1(mu-N)>m, where m is the number of used intervals. The last
bound is a declared deterministic radius squared, not a 68% or 95% region.

Compute A=C_alpha^-1/2 Dmu and W=Dw. Record the SVD of A and of W A^+.
These give unconstrained tangent sensitivity; active causal constraints can
restrict reachable perturbations. Numerical small singular values are not an
exact rank-deficiency proof. The first two left singular vectors of W A^+
give four fixed signed linear objectives in the weights. Maximize each with
one SLSQP start, 120 iterations, 12-second budget, complete order constraints,
pair discrepancy <=2 and observed discrepancy squared <=m. No extra starts.
The whole search budget is 1200 seconds. Inspect only the final and best visited
objective points, using fractions .999*2^(-k), k=0..19. Round coordinates to
12 decimal places, recheck original moment/Gram/order gates, and keep pairs
with numerical slack 1e-7 in both count-norm bounds.

A strong numerical pair needs ||w1-w0|| / ((||w1||+||w0||)/2) >=.25.
The first source index with such a pair is the certificate target; choose the
largest separation among its four fixed objectives. Search failures and small
pairs remain; absence of a witness is not a uniform stability theorem. All
source code, controls, input hashes and this protocol are frozen before search.
This local diagnostic freeze is not public preregistration; source outcomes
are already known from PR87.

## Certification and interpretation

After search, independently recompute rational coordinates, exact pair-order
signs, exact moment rank/weights and rigorous enclosing bounds for expected
counts and the prescribed discrepancy. Verify that both geometries lie in the
same deterministic observation set around the actual integer N. This creates
a two-point lower bound for recovery of this discrete target in that set.
The worst input field direction may be chosen after finding the pair; it is
an operator-norm witness, not an independent smooth-field accuracy result.
Any optional fixed smooth-field nodal values must be held identical between
geometries and explicitly distinguished from evaluating the same continuum
function at two different geometries.

For a fixed common observation y, the triangle inequality gives
max(||w_hat(y)-w0||,||w_hat(y)-w1||) >= ||w1-w0||/2.
This is algorithm-independent in the stated bounded-error information model.
It does not show that a specific solver cannot improve, does not give a
probability under the original correlated Poisson experiment, and does not
rule out additional observables or other operator targets.

An independent Wolfram check will verify selected symbolic identities and,
if a witness is found, its numeric algebra. Exact proof scope will be carried
by the independently reproducible rational/interval certificate, not by a
numerical optimizer success flag. All global scientific HOLDs remain.
