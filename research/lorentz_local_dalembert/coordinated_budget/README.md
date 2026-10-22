# Uniform certificate for coordinated nonconformal support motions

SPDX-License-Identifier: Apache-2.0

**Result:** all simultaneous movements of the 16 support points (48 coordinate
directions) satisfying the current exponential Poisson slab certificate have
symmetric weight gap from the fixed reference **at most 2.08376636%**. This is
a conservative uniform upper bound, below the >20% strong-counterexample gate.
Four landmarks, the root, density, scale and outer diamond remain fixed.

The proof covers the block displacement ball
sum_i(|dt_i|+sqrt(dx_i²+dy_i²)) <= (36/125)/C, C about 29726.7102.
Its radius is about 9.68826e-6 in the specified normalized boosted coordinates.
It contains every motion passing 1-exp(-C B)<=1/4 because log(4/3)<36/125.
The radius is a mathematical parameter, not a physical accuracy claim.

A single budget-aware interval calculation proves invertibility throughout
this set (residual norm <0.012356), then bounds the weight change using a
centered residual solve. Exact rational arithmetic and outward intervals are
used; there is no optimizer or Monte Carlo in the certificate.

- [Full proof and development record](THEORY.md)
- [Fixed contract](contract.json), [certificate](certificate.json), [summary](summary.json)
- [Independent arithmetic audit](audit.json): 48 dual derivative identities,
  136 exact nonlinear points and negative controls.

Reproduce from repository root:

```sh
python3 -B research/lorentz_local_dalembert/coordinated_budget/cb_run.py --verify
python3 -B research/lorentz_local_dalembert/coordinated_budget/cb_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/coordinated_budget/SHA256SUMS
python3 tests/python/verify_manifest.py
```

**Stop:** further coordinated search from this reference under the same
sufficient certificate. Next improve the bound for the full joint count law
before broadening shape optimization. No global stability, uniform 10%
estimation guarantee, physical validation, or exclusion of actual-TV-close
pairs outside this certified budget is claimed. All scientific HOLDs remain.
