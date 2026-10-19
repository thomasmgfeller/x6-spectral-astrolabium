# Joint-moment feasibility — frozen 19 October 2026

The common-axis trial failed both prespecified improvement gates. This next
bounded diagnostic asks whether existing finite supports can satisfy the first
and second moments simultaneously, with the intended weight signs and bounded
total weight. It uses embedding coordinates and the known target metric.
It is not an intrinsic estimator, independent metric recovery or validation
of fields used as constraints. Always retain HOLD_PHASE3 and BD-C2 NO_GO.
All earlier scientific directories remain immutable.

## Supports and six fixed arms

Generate the unchanged balanced64 neighborhood, root, m, n, temporal endpoints
and nominal times. The accepted volume_shell weights are the baseline.
The rejected common-axis rule is not promoted or modified.

Two support families, retaining the same temporal endpoints:

* caps: the previous selected balanced64 shell caps, including their original
  minimum population rule. An unavailable cap stencil remains unavailable.
* full_shells: all events on the two original chain-level-m shells, before the
  spatial cap cut; require the same minimum population on both sides. This is
  a broader-support diagnostic, potentially boundary dominated and nonlocal
  in the diamond frame. It is not proposed as an accepted operator.

For each family construct its corresponding volume-shell baseline, including
strict positive interval-count requirements, then run all three weight policies:

* fixed_time: keep both negative temporal weights fixed at their baseline
  values; shell weights are free but nonnegative. caps/fixed_time is primary.
* free_time: temporal weights may vary but remain nonpositive; shell weights
  remain nonnegative. Zero weights are permitted, without a minimum occupation.
* unrestricted: every support weight may have either sign. Diagnostic only.

No adaptive support growth, refitted reference direction, new seeds or policy
selection. Record every arm, including failures and unavailable inputs.

## Dimensionless linear program and independent witnesses

Let z_b=(X_b-X_root)/tm and a_b=tm^2*w_b. For the 3 linear and 6 independent
quadratic monomials require

    sum a_b z_b = 0,
    sum a_b z_b z_b^T = 2*diag(-1,1,1).

Off-diagonal rows receive sqrt(2) scaling. Constants vanish through the existing
Bf=sum w_b*(f_b-f_root) form. Minimize sum |a_b| under each policy. For fixed_time,
move the fixed temporal contribution to the right-hand side. For free_time,
absorb the prescribed signs into the columns. For unrestricted weights split
each variable into nonnegative positive/negative parts. These give A*x=b,
x>=0, objective 1^T*x plus any fixed temporal absolute mass.

Use scipy.optimize.linprog(method='highs-ds'), presolve enabled, primal and dual
feasibility tolerance 1e-9, maximum 100000 iterations and 10 seconds per solve.
An apparent feasible optimum is accepted only after independently checking
primal residuals, signs, the dual inequality A^T*y<=1 and the primal/dual gap.
Reconstruct the complete original moments and the absolute weight sum as well.

An apparent infeasibility must have a separate numerical separating witness:
minimize b^T*y subject to A^T*y>=0 and -1<=y_i<=1. Require b^T*y < -1e-8 and
independently verify the inequalities. This is a tolerance-checked floating-point
certificate, not a formal interval-arithmetic proof. A solver status without a
valid witness is UNRESOLVED, never mathematical infeasibility. Budget exhaustion
or solver trouble is retained, without replacement or post-test repair.

Certificate tolerance is 1e-8*(1+||b||inf) for primal and reconstructed moments,
1e-8 for variable/dual inequality violations, and 1e-7*(1+|objective|) for the
duality gap. Infeasibility margin is strictly greater than 1e-8, with dual-vector
infinity norm <=1+1e-8. All residuals, witness vectors, weights, solver status,
input matrix, singular values, rank (relative cutoff 1e-10), and marked support
order are archived. The minimum objective is the quantity of interest; witnesses
need not be unique and are not interpreted as a preferred calibrated operator.

## Fixed observations and primary descriptive gate

Report feasible, infeasible-with-witness, unresolved and unavailable counts per
density and arm, with all 16 target clouds in the denominator. Record baseline
first/second-moment errors, minimum absolute weight mass, its ratio to the
corresponding baseline mass, positive/negative masses, support size and scaled
maximum coordinate distance. A mass ratio bounds an elementary independent
bounded field-noise amplification comparison; it is not an accuracy guarantee.
Report paired policy/support transitions and cloud-level means/standard errors.
Do not present tiny fitted polynomial errors as held-out scientific success.

At rho=32768, caps/fixed_time must be feasible on >=80% of all clouds AND have
minimum absolute weight mass <=2 times the baseline mass on >=80% of all clouds.
All available problems in every arm must receive verified feasible or
infeasible witnesses. Combined with complete execution, resource bounds and
software controls, these gates yield CAP_MOMENT_FEASIBILITY_SUPPORTED;
otherwise CAP_MOMENT_FEASIBILITY_HOLD. Both decisions remain coordinate-assisted
diagnostics and cannot release Phase 3. The absolute metric threshold 0.5 and
intrinsic/operator qualification are not replaced by fitted constraints.

## Fresh data, controls and replay

Publish this protocol before six development clouds; publish all implementation
and analysis sources before 48 fresh targets, 16 at each density 2048,8192,32768.
Seeds and budgets are in contract.json. Development can correct software errors
but cannot change this mathematical rule, policies, thresholds or parameters.
No post-test source changes, replacement clouds or optional stopping.

Independent controls: a symmetric hand-solvable timelike support with known
positive shell weights and negative temporal weights; a one-spatial-direction
support with a verified infeasibility witness; a sign-constrained impossible
example made feasible by unrestricted weights; mutation rejection for primal
and dual witnesses; uniform coordinate/tm scaling; mark-preserving permutation.
On one development and target cloud per density, repeat all LPs after event
permutation and transported time reversal, checking feasibility and minimum
mass rather than nonunique individual witness vectors. Verify constant/product
identities on every reconstructed feasible witness.

Replay every target. Public source and record hashes must match. Regenerated
relations, marks, support order and logical classifications must match exactly;
baseline geometry and evaluation use atol=1e-10, rtol=1e-9. Coordinate byte hashes
are reported separately. Every archived and regenerated LP witness is checked
independently; minimum objectives and their summaries use atol=1e-8, rtol=1e-7.
Nonunique primal/dual vectors and iteration counts need not be identical. These
LP tolerances are fixed before data and do not alter any earlier replay gate.

Software reference: SciPy's official linprog HiGHS documentation describes the
linear constraints, dual marginals, statuses and solver tolerances:
https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html
The executable environment retains the repository's NumPy/SciPy version pins.
