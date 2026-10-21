# Frozen second-moment diagnosis — 19 October 2026

This protocol precedes development and all fresh target clouds. The preceding
anchor audit improved coverage but failed metric gates even with exact cap
selection. All previous phase12, anchor_audit and BD-C2 files remain immutable.
This experiment diagnoses that failure; it cannot authorize Phase 3.

## Estimand and fixed population

Reuse the unchanged marked Poisson diamond, longest-chain scales, balanced64
selection and exact-distance oracle cap from the prior audit. Use 16 independent
fresh clouds at each density 2048, 8192, 32768; seeds, development seeds and
budgets are in contract.json. No replacement, tuning, early statistical stopping
or target-informed code change. Freeze implementation and analysis publicly
before target execution. Record unavailable stencils explicitly. Every factorial
comparison within an arm uses exactly the same clouds and memberships.

For root displacements v-/v+ at chain distance n and shell displacements w,

    M = -(C+3)/(2 tn²) sum(v vᵀ)
        + C/(2 tm²) sum_over_sides(mean(w wᵀ)), C=243/29.

This is exactly the product-identity metric on smooth coordinate fields.
The target is eta=diag(-1,1,1), evaluated in the fixed diamond coordinates.
Frobenius error is frame dependent; covariance is tested separately.

## Three coordinate-assisted interventions, all 2³ combinations

Let q(v)=sqrt(-vᵀ eta v). Future-oriented temporal endpoint unit vectors
are u+=v+/q(v+) and u-=-v-/q(v-). Define u=(u++u-)/q(u++u-).

* T: rescale each temporal displacement by tn/q(v), retaining its direction.
  This removes endpoint proper-time scale mismatch, not general chain bias.
* S: rescale every selected shell displacement by tm/q(w), retaining its
  direction. This removes shell proper-time mean bias AND radial scatter;
  these effects are reported separately but not independently intervened on.
* D: replace each endpoint displacement by sign(v.time) q(v) u. For each
  shell, let a be its future-oriented reference unit vector. Apply the unique
  rotation-free boost in the (a,u) plane mapping a to u to all shell vectors:
  B=I+(u+a)(u+a)ᵀ eta/(1-uᵀ eta a)-2u aᵀ eta.
  This aligns reference axes and endpoint directions while retaining shell
  internal angular structure. It does not remove all angular sampling noise.

T/S commute with D. Memberships and original tn/tm stay fixed in every variant.
Coordinates never enter balanced64 construction. The oracle cap retains the
previous audit's coordinate selection on the original discrete shells; it is
not an ideal continuum cap or a lower bound. Direction controls are explicitly
oracle interventions, not implementable corrections for an unembedded poset.

## Exact decomposition, summaries, decision

Also split raw M=Tmoment+Smoment and compare with
Tideal=-(C+3)uuᵀ and Sideal=eta+(C+3)uuᵀ. Archive both matrices and their
errors. Report the signed cross term in ||dT+dS||²: cancellation or reinforcement
must not be inferred from separate norms alone.

Archive each cloud's eight matrices, relative errors and signatures, temporal
proper-time ratios, within-shell mean/SD proper-time ratios, endpoint/reference
rapidities relative to u, and population sizes. Summarize RMS per density and
arm; availability denominator is all 16 clouds. Paired raw-minus-controlled
squared errors have cloud-level means and standard errors. Compute all three
Shapley contributions over the full factorial of squared-error reductions,
including negative effects and interactions; their sum must equal raw minus
TSD squared error. These are diagnostic allocations, not unique physical causes.
No point-pair pseudoreplication, winner selection or p-value gate.

The descriptive decision is fixed in contract.json. Regardless of outcome,
retain HOLD_PHASE3 and BD-C2 NO_GO. If informative, the next work is an intrinsic
finite-density calibration proposal with its own freeze and fresh validation;
otherwise isolate the remaining shell/angular/boundary mechanisms. A residual
above the inherited metric threshold 0.5 blocks flat qualification even for
these coordinate-assisted controls. A successful oracle control never qualifies
an intrinsic operator.

## Software and replay requirements

Independent analytic hyperbolic-cap quadrature recovers eta; isolated synthetic
scale, shell and directional defects are corrected by their intended factor.
Check the exact raw product identity, Lorentz covariance for all variants,
Shapley conservation and degenerate input rejection. Inherited construction is
unchanged. Recompute every target cloud and summary from public frozen sources;
check source/record hashes, discrete fields exactly and numerical outputs at
atol=1e-10, rtol=1e-9. Report byte-coordinate hash agreement separately from
numerical replay. Archive failures, resources and complete denominators.
