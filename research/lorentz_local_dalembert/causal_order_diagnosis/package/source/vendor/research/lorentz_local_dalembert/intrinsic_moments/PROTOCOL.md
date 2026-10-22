# Intrinsic landmark moment calibration — frozen 19 October 2026

The preceding coordinate-assisted feasibility audit found admissible moments
on all 16 high-density cap supports. It did not construct their weights from
the order. This bounded new trial tests one fixed order-derived construction,
a count-noise stability guard, and independent field responses. No earlier
scientific source, result, threshold or rejected candidate is modified.
The reference is the accepted volume_shell stencil on balanced64 caps.

This is a new experimental construction, not a reproduction of a published
embedding algorithm. The general use of interval volumes to estimate Minkowski
inner products is established context: Steven Johnston, *Embedding Causal Sets
into Minkowski Spacetime*, CQG 39 095006 (2022),
https://arxiv.org/abs/2111.09331. The formulas and all choices below define this
trial independently. Dimension 2+1, density and the flat model remain known.

## Fixed support and intrinsic landmark fields

Keep the original root, marked cap support, temporal endpoints and nominal tm.
Missing baseline stencils remain missing; never replace a cloud or enlarge its
support. The inference module receives only the marked causal order, density,
baseline stencil, two boundary labels and independent auxiliary Bernoulli
colour labels. It cannot access simulator coordinates or validation fields.

For causally related a,b estimate squared proper time as
q(a,b)=[N(a,b)/(rho*pi/12)]^(2/3), using strict interior interval counts.
Search both the common past and common future of root plus all support points.
Exclude the two artificial diamond endpoints. On each side retain, in increasing
mark order, at most 40 candidates whose intervals to every point have >=8
interior events. Enumerate triples whose members are pairwise comparable and
whose three mutual intervals also have >=8 events.

For a triple L_i rooted at o form the dimensionless symmetric Gram estimate

    H_ij = [-q(L_i,o)-q(L_j,o)+q(L_i,L_j)]/(2 tm^2),
    H_ii = -q(L_i,o)/tm^2.

Require one negative and two positive eigenvalues and spectral condition
max|lambda|/min|lambda| <=1000. Among all admissible past/future triples choose
the largest |det H|/product(-H_ii), breaking exact ties by the ascending tuple
of landmark marks. This uses the order only. No valid triple means fallback.

For each support b define

    V_ib = [-q(L_i,o)-q(o,b)+q(L_i,b)]/(2 tm^2).

If H=U diag(lambda) U^T (negative eigenvalue first), let
T=diag(1/sqrt|lambda|) U^T and Z=(T V)^T. Thus T H T^T=eta.
With exact continuum distances these are support displacements in an
orthonormal Lorentz frame, divided by tm. Finite-count estimates need not be
accurate. Neither target coordinates nor an alignment to them enters inference.
Landmarks may be remote: success would not establish locality.

## Unique regularized calibration with a hard mass bound

Use rows t,x,y,tt,xx,yy,sqrt(2)tx,sqrt(2)ty,sqrt(2)xy of Z as design D.
Target b_all=(0,0,0,-2,2,2,0,0,0). Set a0=tm^2*w_baseline.
Keep the two negative temporal coefficients fixed and move their contribution
to the right-hand side b. All other coefficients a must be nonnegative, with

    sum a <= 2 sum|a0| - sum|a0_temporal|.

Minimize the strictly convex objective

    F(a) = 1/2 ||D_shell a-b||^2 + lambda/2 ||a-a0_shell||^2,
    lambda = 0.01 * max(1e-12, ||D_shell||_F^2 / number_of_shell_points).

The fixed solver is accelerated projected gradient, initialized at a0_shell,
with Lipschitz constant the largest Hessian eigenvalue, strong convexity
lambda, momentum (sqrt(L)-sqrt(lambda))/(sqrt(L)+sqrt(lambda)), and Euclidean
projection onto the nonnegative capped simplex. Maximum 10000 iterations.
The convex first-order upper bound on suboptimality is

    gap = gradF(a).a - cap*min(0,min gradF(a)).

Independently check feasible signs/mass, fixed temporal coefficients, objective
and gap <=1e-9*(1+|F|), allowing feasibility tolerance 1e-10. An unverified
solution is UNRESOLVED and triggers baseline fallback, never claimed optimal.
Archive design, baseline, fitted coefficients, ridge, cap, objective, gap,
iterations, fitted residuals and amplification diagnostics. This is a soft
moment fit; tiny fitted residuals do not count as independent success.

## Two fixed intrinsic arms and count-noise guard

intrinsic_raw applies the verified calibration whenever a frame and verified
solution exist, otherwise the unchanged baseline. intrinsic_guarded is the
sole primary arm: it additionally requires all the conditions below.

Generate an auxiliary independent Bernoulli(1/2) label per event, with RNG seed
seed XOR 789073. Freeze the selected root, support and landmarks. Recompute
all used interval counts separately in each colour, multiplying counts by two
before the 2/3 power. These are conditional thinning stress tests. They do not
reselect a cloud/neighborhood, are not independent samples of the selected
geometry, and do not yield confidence bounds for Poisson selection error.

The guard requires: full Gram condition <=100; every used full interval >=16;
every used half interval >=4; both half-Gram matrices have Lorentz signature;
and, for each half h,

    ||T H_h T^T-eta||_F/sqrt(3) <=0.25,
    ||T(V_h-V)||_F / max(||T V||_F,1e-12) <=0.25.

Failure of any condition uses baseline weights. Report each failure reason,
adoption and fallback explicitly. A fourth arm, coordinate_oracle, applies the
same regularized optimization to true displacements/tm after inference, for
diagnosis only. It is not a competing intrinsic method and cannot pass the
primary decision. The unchanged volume_shell is the paired baseline.

## Independent fields, noise and preregistered decisions

Evaluate weights only after inference on the true displacement x=X-X_root.
For k in {(1,0,0),(0,1,0),(0,0,1),(1,.6,.8),(.5,1,-.5)} and
frequencies s in {.5,1}, use both cos(s*k.x) and sin(s*k.x): 20 fields.
At the root their exact d'Alembertian targets are s^2*(kt^2-kx^2-ky^2)
and zero respectively. Normalize each response error by s^2*||k||_2^2.
These fields are never used in frame selection, weight fitting or guarding.
The per-cloud independent-field score is RMS over these 20 normalized errors.
Also retain the previous true-coordinate metric error and normalized affine
drift as diagnostics and gates, with the previous definitions unchanged.

For each arm report all-cloud availability/adoption, fallback reasons,
cloud-level error RMS, paired squared-error reductions with standard errors,
signature counts, absolute mass and sum of squared coefficients including
the root coefficient. The latter is the variance multiplier for equal,
independent, zero-mean additive field noise; it is an analytic comparison,
not evidence of measured noise robustness. Coefficient mass is a worst-case
bounded-difference amplification measure, not a variance or accuracy guarantee.

At rho=32768 the primary method must have availability >=80% AND actual
guarded adoption >=80% of all 16 clouds. Its paired RMS ratios relative to
volume_shell, using the same available clouds, must each be <=0.75 for
independent fields, metric error and affine drift. Missing observations and
fallback remain visible; no selected-subset improvement can pass the gates.
Complete execution, resource bounds, software controls and independently
verified calibration certificates are also required. All gates yield
INTRINSIC_MOMENT_IMPROVEMENT; otherwise INTRINSIC_MOMENT_HOLD.
These are fixed descriptive pilot gates, not confidence or convergence claims.
Always HOLD_PHASE3 and BD-C2 NO_GO. The earlier absolute metric threshold 0.5
and curved/3+1/external validation requirements are not replaced.

## Freezes, controls, execution and replay

Publish this protocol and contract before six development clouds. Development
may fix software defects but may not change the rule or constants. Publish
all computational and analysis sources before 48 new target clouds, 16 per
density, with seeds specified in contract.json. No retuning, replacement or
optional stopping. Wall budget 1200 seconds and RSS budget 2048 MiB per batch.

Controls before development: exact continuum polarization and Gram identities;
analytic one-variable and active-mass-bound quadratic optima; mutation rejection
of signs, mass and optimality witnesses; rank/signature failures; count-guard
failure on deliberately inconsistent halves; uniform distance/tm rescaling;
constant/product identities; and source-interface isolation from coordinates.
On one development and target cloud per density test the new inference under
mark-preserving relabeling and transported time reversal, conditional on the
existing root/support. Auxiliary colour labels are transported. These controls
do not requalify or alter the inherited neighborhood selector.

Replay all 48 targets. Verify public computational-source and record hashes,
all stored and recomputed optimization witnesses, and exact discrete structure,
selected landmarks, classes, adoption and fallback reasons. Baseline replay
retains atol=1e-10, rtol=1e-9; new calibration arrays/evaluations/summaries use
atol=1e-7, rtol=1e-6. Iteration counts and eigenvector sign choices are not
observables; compare invariant feature products, objectives and final weights.
The strict convex ridge gives a unique calibration. Coordinate byte hashes
are separately reported, with no byte-identity or external-replication claim.
