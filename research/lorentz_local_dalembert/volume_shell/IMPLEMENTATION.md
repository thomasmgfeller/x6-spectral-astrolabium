# Implementation frozen before fresh target data

Public protocol: `ad952930c1251750127505cc6939fdaf0aef9158`.
Six fixed development clouds were completed with the recorded computational
hashes. Their source_commit points to the protocol ancestor, because code was
then uncommitted. The next public commit fixes all implementation, analysis and
verification sources before any target cloud. No parameters, seeds, gates,
weights or handling rules were changed in response to development results.

The candidate module imports only copy and math. It accepts the causal order,
existing stencil, known density and coefficient. It counts strict interiors,
uses qhat=(12 N/(pi rho))^(1/3), and changes inverse-square weights on fixed
shell memberships. The primary candidate leaves temporal weights untouched.
The secondary volume_both arm also changes temporal weights; it cannot replace
the primary arm after results. No embedding coordinates enter either candidate.

Five of six development clouds supply a usable baseline. The unavailable low
density cloud stays in all denominators. All controls pass: hand-counted weights,
time reversal, transported marks under permutation, density scaling, repeated
support accumulation, invalid-density rejection and explicit zero-interval HOLD.
Every available development stencil passes constant/product/affine tensor checks.
The coordinate oracle metrics reproduce the earlier S and TS moment controls.

Field evaluations use root-centered t,x,y. The exponential is exp(t+x+y), whose
flat d'Alembertian at the root is -1+1+1=1. This differs from any earlier test
field with different coefficients; fields are explicitly archived with targets.
Affine drift is recorded both dimensionally and as tm*||B(X)||/sqrt(3).
Neither the drift norm nor the metric error norm is frame invariant.

Counts on selected longest-chain shells are conditional. The volume formula is
not asserted unbiased for those selections; per-cloud errors against exact
proper time are diagnostic only. Unknown density, other dimensions, curved
space, reference alignment and intrinsic chart qualification remain outside
this milestone. Scientific Phase 3 always stays HOLD.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/volume_shell/run_volume.py --mode test --output /tmp/bk-volume-fresh
python3 -B research/lorentz_local_dalembert/volume_shell/volume_analysis.py /tmp/bk-volume-fresh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/volume_shell/verify_volume.py --directory /tmp/bk-volume-fresh
```

Replay reports coordinate byte hashes separately from exact discrete agreement
and tolerance-based agreement of all computed numerical outputs. No platform
bitwise-coordinate promise is made. Earlier sources and results remain intact.
