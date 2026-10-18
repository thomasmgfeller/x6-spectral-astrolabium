# BK phase 1/2: bounded flat pilot

This protocol is fixed before generating new development or test clouds. The
implementation will be fixed in a second public commit before held-out runs.
Development seeds are for implementation debugging, not changing these gates.
The result may be HOLD; completing an implementation does not establish its
scientific adequacy. No phase-3 curvature work is part of this contract.

## Inputs and separation

Poisson sprinkle a causal diamond of duration 1 in 2+1 Minkowski space. Its
volume is pi/12. Add its two distinguished boundary endpoints. The estimator
receives only the strict transitive causal relation, known uniform density,
dimension and independent continuous random marks attached to events. Marks
resolve otherwise ambiguous choices; they are carried with events under
permutation. This is equivariance of a marked construction, not a canonical
frame of an unmarked symmetric poset. Coordinates are available only to the
sampler and the independent evaluator. Poisson count fluctuations are included;
unknown or spatially varying intensity is outside scope.

## Phase 1

Use edge counts for longest chains. Select one longest endpoint-to-endpoint
chain, breaking ties by marks, and its middle event as the reference. Use
n=round(0.55 rho^(25/84)), m=round(0.45 rho^(23/96)), with n>=m+1.
Insufficient chain length is a recorded failure, never a clipped scale.
Proper time is alpha2*rho^(-1/3)*chain_length. The fixed alpha2=1/sqrt(2)
is a numerical literature calibration in 2+1, not an exact theorem. Also record
the independent number-volume calibration (N_interval/(rho*pi/12))^(1/3).
No fit to embedding coordinates is allowed.

For each event at longest-chain level m, estimate its spacelike distance to
the chain reference at level m using intersection counts. Search common-past
anchors (common future on the past side); retain the 64 deepest by minimum
interval population, then apply the count-balance filter of the overlap paper,
with minimum interval population 8. Use the median distance from qualifying
anchors. This bounded anchor search is an explicitly tested implementation
choice, not a reproduction of the authors' unrestricted search. Missing
anchors, overlap endpoints and tied ranks are reported. Invert the continuum
2+1 overlap function numerically; estimate its time scale by longest chains.
The neighborhood includes every valid point with estimated distance at most
2*tau_m/3, including the reference event at distance zero. Fewer than four
points on either side is an operator failure. No unknown distances are set to
zero. All causal intervals in this causally convex domain are complete; a
finite diamond still limits the available shell. Report a geometric boundary
audit after inference, without using it to rescue selection.

## Phase 2

Assemble the symmetric BK stencil with C=243/29. Test constants, three affine
fields, three squares, three mixed products and exp(-(t^2-x^2-y^2)/2), using
coordinates relative to the selected event only as prescribed test fields.
Compute the product-identity metric from the resulting operator. Test the
identity against a separately accumulated weighted outer-product expression.
Compare the metric to diag(-1,1,1), not just its signature. Affine changes of
chart must satisfy the tensor transformation rule including translations.
A nonlinear chart control is diagnostic only, with its analytic target.

Additionally build three intrinsic chart fields from squared interval-volume
proper times to four common-past landmarks. Use the bottom endpoint as the
first landmark; choose three others by greedy independent-column pivoting of
their field differences on the stencil support, out of at most 128 marked
candidates. For landmark p_j, define
X^j(z)=[tau_volume(p_0,z)^2-tau_volume(p_j,z)^2]/(2*tau_n), centred at a_0.
In the ideal flat continuum these are affine fields. The evaluator obtains
their exact Jacobian from the selected landmarks' true coordinates, and checks
rank, condition, field error and metric error against J eta J^T. This oracle
is used only after selection. Same-cloud selection/count noise is included;
no fixed-smooth-field convergence claim transfers automatically to these fields.
This chart construction is our exploratory addition, not part of the BK paper.

## Analysis fixed before data

There are 48 independent held-out clouds, 16 per density. Cloud, not pair,
is the uncertainty unit. Report every seed, failures, populations, ties,
per-field responses, both metric matrices, scales, timing and peak memory.
Use cloud-mean relative time/space errors, spatial Spearman ranks, and RMS
operator errors scaled by max(1,abs(target)); metric error is Frobenius norm
relative to target norm. Report means with standard errors and Wilson intervals
for signature/availability fractions. No p-value or universal minimum budget
is inferred. Positive accuracy gates use the highest density; failure counts
retain failed clouds in their denominators. Improvement compares highest and
lowest density point estimates, and is only a finite-range diagnostic.

All implementations must pass meaningful independent small-poset chain checks,
quadrature checks, constant/product/affine-transform controls, coordinate-blind
API inspection, relabelling (including marks and endpoints), and negative
controls for insufficient neighborhoods and rank-deficient fields. Scientific
gates are recorded separately from software correctness. No tolerance is
adjusted after held-out outcomes. The 600-second/2-GiB budget applies to the
48-cloud target run; incomplete runs are a budget HOLD, not dropped samples.

## Sources

- Boguña & Krioukov, [Local d'Alembertian for causal sets](https://arxiv.org/html/2506.18745v1),
  Eqs. 30, 46–47, 76, 81, 86–91. Our n follows the temporal scaling condition;
  this is not a replication of the paper's n=m numerical example.
- Boguña & Krioukov, [Measuring spatial distances via causal overlaps](https://arxiv.org/html/2401.17376v2),
  Eqs. 16, 22, 34, 38, 47–50.
- The metric identity follows directly by applying the differential product
  rule twice. It is an algebraic extraction, not a curvature estimator.
