# Joint-moment feasibility diagnostic

Public protocol: `4855dc84ff307e3b85bfc6887de5ae8e060ac90c`.

This is a coordinate-assisted linear-programming diagnostic. Known coordinates
and the target Minkowski metric enter the constraints. Exactly fitting those
moments does not validate metric reconstruction or the intrinsic operator.
The previous accepted volume-shell stencil is the primary support baseline;
the failed common-axis rule is not promoted.

Two support families and three fixed policies separate cap coverage, temporal
weight constraints and sign restrictions. Feasible optima require primal and
dual checks; infeasibility requires a separate numerical separating witness.
Floating-point witnesses are not formal exact-arithmetic proofs. Unresolved
solver cases remain unresolved. Minimum total absolute weight is the main LP
observable, not the particular nonunique primal or dual solution returned.

Six development clouds completed without changes to the rule or parameters.
All development software and certificate checks passed. The implementation and
analysis are publicly frozen before any target cloud is generated.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/moment_feasibility/feas_controls.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/moment_feasibility/verify_feasibility.py
```

Use the existing pinned `research/lorentz_bd_reference/requirements-replay.txt`.
`run_feasibility.py --mode test --output <new-directory>` refuses overwrite and
checks every computational source against HEAD. Each record stores the design
matrix once per support family; each policy's matrix is reconstructed from it.
Row order: t,x,y,tt,xx,yy,sqrt(2)tx,sqrt(2)ty,sqrt(2)xy.

Permutation/time-reversal controls transport the LP inputs and original root;
they do not change or requalify the inherited neighborhood selector. Archived
and replayed witnesses are independently checked, since LP optima can have
multiple primal/dual representations. Logical classifications and minimum
objectives must match; solver iteration counts and witness vectors need not.
Older source files and their stricter baseline replay gates remain unchanged.

For bounded errors in each field difference, absolute coefficient mass gives
a worst-case linear amplification bound. If root and support field values are
individually noisy, including the root coefficient gives a bound no larger
than twice that mass. The ratio compares these bounds, not measured variance
or accuracy. The selected LP witness need not be a preferred numerical stencil.
Always HOLD_PHASE3; this audit cannot qualify an intrinsic or curved operator.
