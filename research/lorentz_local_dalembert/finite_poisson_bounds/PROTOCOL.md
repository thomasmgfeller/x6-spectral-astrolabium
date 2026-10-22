# Finite Poisson-to-operator bound: fixed analytical audit

SPDX-License-Identifier: Apache-2.0

Use the same 20 A-selected candidate B0 packets as PR88, without new clouds,
optimizer runs, simulator truth, field values, or changes to existing gates.
This is a posthoc analytical audit on known data, not independent validation.
The 1,736 interval indices depend on A only; retain the count-HOLD packet too.

## Probability model fixed before evaluation

Conditional on selected A, B is a separate homogeneous Poisson process of
known density 32768 in the containing 2+1 diamond. Each interval count is
Poisson with its volume mean; overlaps can make counts arbitrarily dependent.
Use c=12 and the proven conservative confidence interval

L(n)=max(0,n-sqrt(2nc)), U(n)=n+c+sqrt(c^2+2nc),

with the sharper U(0)=c. The derivation is Chernoff inversion plus a scalar
quadratic lower bound, not a Gaussian approximation. The union error over all
1,736 counts is <=2*1736*exp(-12)<0.05. Prove the numerical inequality using
a rational lower bound for exp(12), not floating-point probability estimates.
The family includes cloud 03, irrespective of its failed observed count gate.
There is no independence assumption between counted intervals or between
clouds in the union step. Finite PRNG arithmetic is not an ideal-probability
proof; the guarantee is conditional on the stated physical sampling model.

Coverage is before B-dependent fitting, count filters and resource-cap
selection. An aborted B draw must yield no finite certificate, with the full
parameter set as its confidence set. No claim of coverage conditional on
passing a filter or a cap. The fixed B0 plan has no optional stopping or
adaptive observation design. Additional future observations need a new error
budget. Physical departures from the model remain outside the theorem.

Convert every mean interval to squared proper-time intervals with outward
rational bounds for pi, square roots and cube roots. This gives one simultaneous
box covering the true interval vector under the model. The empirical overlap
covariance is not used to narrow this box; its dependence is allowed, not
discarded by an independence approximation. Known exact order and geometry
could shrink the confidence set without losing coverage if they are true
model constraints; this first bound deliberately takes the enclosing box.

## Finite matrix bound

For each of the 19 qualified PR88 feasibility seeds, round coordinates to the
same 12 decimal places, form exact q0, and take a symmetric radius covering the
whole confidence box. Record exact center order. Compute original intrinsic
moment design D(q), linear target b(q), and P=(I+11')^-1 exactly.

Choose nine pivot columns by numerical QR at q0 only; invert that submatrix
exactly to define a constant row transform S. Numerical pivots are proposals:
invertibility and all identities are checked rationally. Preserve these pivot
indices for deterministic replay across BLAS implementations. This transform
does not alter the moment constraints or minimum-energy weights.

Bound the transformed design perturbation by E(t)=t L+t^2 Q using exact
first derivatives in q (including cancellations after S) and quadratic
remainders. Bound transformed target changes by t B. With

M0=D0 P D0', beta>=||M0^-1||2, d0>=sqrt(||M0||2),
eM=2 d0 E+E^2, gamma=beta eM,

gamma<1 is sufficient for a finite resolvent/weight-error certificate. Norms
and every arithmetic upper bound are rational or rounded outward. Test the
fixed grid t=2^-k, k=0,...,40, once per seed. At k=0 the entire simultaneous
confidence box is covered; k>0 is only a local diagnostic with NO coverage
claim. A working 10% relative WEIGHT error threshold labels the bound; it is
not a newly validated physical or smooth-field performance target.

If the sufficient condition fails, record NO_CONTRACTION_CERTIFICATE. Do not
declare singularity, instability, impossibility, or a counterexample from that
failure. Do not change the interval construction, threshold, grid, source set,
conditioning cutoff or bound method after looking at the outcome.

Also compute a separate finite norm envelope using the inherited condition
cutoff 1e5 only on the domain where this cutoff is assumed to hold. That is a
restricted-domain bound, not evidence that the true geometry satisfies the
cutoff and not a full-confidence accuracy certificate.

## Additional interpretation

Check whether both exact PR88 witness geometries remain in the new confidence
box. This can give a lower bound on its target diameter; it is still not a
testing-distance or statistical-minimax lower bound. Derive a C3 Taylor
remainder bound for continuum fields separately, with explicit smoothness and
geometric-radius constants. Do not invent these constants from the data or
label a worst-direction nodal field smooth.

Seven synthetic controls precede freezing. Hash protocol, contract, controls,
scripts, inherited arithmetic and all source/reference records before the
numerical source audit. Post-run documentation and replay checks are separately
identified. All global scientific HOLDs remain regardless of mathematical
coverage or local-certification success.
