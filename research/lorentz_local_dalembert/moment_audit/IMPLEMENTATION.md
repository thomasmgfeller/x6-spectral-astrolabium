# Implementation freeze before fresh targets

Protocol commit: `54012b288b4cccbc5215f91d87d8193b38874a15`.
Six fixed development clouds ran before this source freeze. Their execution
records the protocol ancestor and hashes of then-uncommitted implementation.
No parameter, seed, definition, acceptance threshold or intervention was changed
in response to development. Target clouds have not yet been generated.

The analytic controls recover eta from exact hyperbolic-area quadrature; four
separately injected defects exercise temporal scale, shell scale, reference
axis wandering and endpoint wandering. A combined defect is corrected, and all
eight tensors obey Lorentz covariance under a non-collinear boost. Three
non-timelike/empty inputs are rejected. The raw moment tensor agrees with the
unchanged product identity on every available development stencil.

The implementation preserves signed temporal/shell cancellation and allocates
factorial squared-error reductions with the three-factor Shapley formula.
This is a diagnostic decomposition; contributions depend on the chosen
interventions, observer and error norm. The observer is the normalized sum of
the future-oriented temporal endpoint unit vectors. Error is reported in the
original diamond frame; tensor covariance does not make that norm invariant.

S jointly removes shell proper-time bias and within-shell scatter. D removes
endpoint and reference-axis disagreement, retaining internal angular sampling.
Selection is never recomputed after a control. Correcting the vectors can
therefore leave a non-ideal angular cap. No intrinsic field/curvature claim is
made. Original source files and all prior data remain unchanged.

Run the frozen target and its complete replay:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/moment_audit/run_moments.py --mode test --output /tmp/bk-moment-fresh
python3 -B research/lorentz_local_dalembert/moment_audit/moment_analysis.py /tmp/bk-moment-fresh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/moment_audit/verify_moments.py --directory /tmp/bk-moment-fresh
```
