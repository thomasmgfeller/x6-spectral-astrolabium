# Implementation decisions and development observations

Protocol commit: `032024b2369a42e52538ec97466831623b1b47f5`.
No held-out seed has been generated at the time of this implementation note.

The original protocol is unchanged. The implementation uses a dense relation
matrix plus integer bitsets for interval intersections, and a small C++ dynamic
program for longest chains. Longest paths on the transitive closure have the
same maximum edge count as on the reduction: a skipped comparable intermediate
event would lengthen the path. Independent exhaustive small-DAG checks test
both time orientations and permuted labels. Marks break path/anchor/pivot ties.
The overlap inversion uses fixed Gauss quadrature and a monotone interpolation
table, compared with independent adaptive quadrature. Exact zero/one overlap
values are reported as unresolved, except the identical reference event.

Six development clouds (the two fixed development seeds at each density) were
used. Three had enough neighbors for an operator; three did not. The first
low-density pair was also run separately for initial debugging. At the largest
density, one development cloud supplied intrinsic chart landmarks. The
operator errors were large even when the valid distance rankings were good.
No parameter, seed, threshold, radius, population rule or landmark limit was
changed in response. This evidence argues against assuming a positive result.

After those observations we added *diagnostic outputs*, without changing the
estimator: oracle recall/precision of the intended distance cap. They disclose
selection error that a rank score on successfully estimated distances would
hide. A boundary diagnostic samples an ideal continuum cap after inference;
a nonzero value is a truncation witness, whereas zero is not a proof of full
containment. Neither diagnostic replaces the prescribed acceptance gates.

The analyzer spells out the protocol's gates: the highest-density neighborhood
availability must be at least 80%; conditional time/space accuracy and ranking
must meet the fixed thresholds; lowest-to-highest time/space/metric error must
improve. Phase 2 requires the stated operator, oracle metric, intrinsic metric,
chart-field and availability/signature thresholds. Signatures use all 16 clouds
as denominator, including unavailable ones; chart errors are conditional on a
chart whose oracle Jacobian condition is at most 100. Missing charts therefore
cannot disappear from the availability/signature gates. Mean and SE use
independent clouds; acceptance uses RMS errors. The affine-chart test is an
algebraic covariance check, not independent evidence for metric accuracy.

Tests for the artificial stencil demonstrate the product rule and sensitivity
to components. They cannot establish accuracy of the randomly reconstructed
BK stencil. The latter is assessed only by the held-out clouds. All constants,
source files, exact seed schedule and analysis will be publicly fixed before
that run. The resulting commit is recorded in `results/execution.json`.

Run with Python 3.12, numpy 2.3.5, scipy 1.17.0 and g++ supporting C++17:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python3 -B research/lorentz_local_dalembert/phase12/tests.py
python3 -B research/lorentz_local_dalembert/phase12/run.py --mode test --output /tmp/bk-phase12-new
python3 -B research/lorentz_local_dalembert/phase12/analyze.py /tmp/bk-phase12-new
```

Use the frozen source commit for target regeneration. The 600-second wall
budget is enforced by a timer. Peak RSS is recorded and checked after each
cloud; the 2-GiB rule is an acceptance gate, not a kernel-enforced memory cap.
The C++ build cache in the system temporary directory is source-hash keyed.
No generated library, simulation coordinate array or private input is needed.
