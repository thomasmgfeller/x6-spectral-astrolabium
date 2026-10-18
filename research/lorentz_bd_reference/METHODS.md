# Frozen BD–C2 Poisson pilot

## Target and scope

This is a finite-budget curvature comparison in 3+1 dimensions, conditional on
known uniform physical density and externally specified diamond duration T=1.
It does not estimate an unknown T or establish a general spacetime clock.
The metric before rescaling is a(eta)^2(-d eta^2+d x^2), a=1/(1-h eta),
on |eta|+|x|<1/2. Divide all lengths by tau=2 atanh(h/2)/h (tau=1 at h=0).
Then T=1, R=q=48 atanh(h/2)^2 and V=V_coordinate/tau^4.
Use rho=lambda_flat/(pi/24), identical across h. N is drawn from Poisson(rho V).
Given N, positions are iid with density a^4 relative to coordinate volume.
No fixed-N substitution, N/rho plug-in density or zero-count resampling is used.

## Reference operator

Benincasa & Dowker, corrected arXiv:1001.2725v4, equations 8–9:

    B_e phi(x) = (4/sqrt(6))*sqrt(e*rho)*[-phi(x)+e sum_y f(n_y,e) phi(y)]
    f(n,e) = sum_{k=0}^3 c_k choose(n,k) e^k (1-e)^(n-k)
    c = (1,-9,16,-8); n_y = #{z : y<z<x}; R_hat = -2 B_e 1(x).

The diagonal and interval endpoints are excluded. The formula has a finite
e=1 limit. The physical smoothing length is l_k=(e rho)^(-1/4).
An evaluation event x at the diamond apex is inserted as a fixed probe; it is
not counted in N or C2. Every sampled point is below x, so n_y equals the
number of successors of y. The same counts give C2=sum_y n_y. This saves
memory without approximating the operator: O(N^2) work, O(N) storage.

The finite diamond supplies a declared infrared cutoff. No infinite-volume
convergence claim follows. The continuum mean integrates the Poisson kernel
over the identical finite region using sphere-intersection volumes. Comparing
this mean with the simulations separates implementation errors from finite
scale/cutoff bias. Orders 64 and 96 must agree within 1e-6; the simulated mean
must lie within 5 estimated standard errors plus quadrature difference.

## Comparator and uncertainty

C2 is the existing exact forward map p(h)=E[C2/choose(N,2)], inverted on
0<=h<=0.5. Its geometric coefficients are unchanged. A dense numerical inverse
is checked against rational off-grid enclosures; this pilot's reported
intervals are numerical, not a replacement for the certified fixed-N suite.
The point estimate uses the clipped inverse of the average per-cloud U statistic.
Domain clipping and incompatible intervals are reported, including the benefit
of the upper model boundary for h=0.5. BD has no corresponding model clipping.

Both methods use the same 32 independent clouds per estimate and nominal 95%
Student intervals across clouds. C2 transforms the probability endpoints.
These intervals address sampling uncertainty; BD bias is not automatically
covered, and empirical coverage is a measured outcome. The old N=128 Bennett
bound cannot be reused unchanged for random N. As a conservative secondary
check, conditional on all N_i>=2, Hoeffding's U-statistic MGF gives a probability
radius sqrt(log(40)*sum_i 1/floor(N_i/2)/(2 M^2)). Its C2 inversion is reported
separately. Neither procedure authorizes optional stopping.

## Design and decision

The machine-readable contract fixes densities, epsilons, h values, seeds,
sample counts, selection, gates and limits before target data. 128 fresh flat
development clouds per density select epsilon by group MSE. No bias subtraction
is performed. All 512 new test clouds per cell are retained. Every epsilon's
raw result is archived, but only the development-selected epsilon enters the gate.
No result from the earlier fixed-N studies is used as development or test data.

The primary practical gate uses lambda_flat=2048 and h=0.5, plus a flat-bias
control. All limits must pass: 20% RMSE improvement over C2, relative bias <=10%,
median interval halfwidth <=20% of R, coverage >=14/16, flat absolute bias <=0.2,
and extraction cost <=2 times C2. This is a screening decision, not a powered
superiority test. A paired 5000-resample bootstrap interval for the RMSE ratio
is descriptive. Failure stops variable-curvature expansion within this budget.

Costs include generation and common relation counting for both methods. BD is
conservatively charged evaluation of all four epsilon candidates; C2 is charged
the sum of counts. Group analysis, compilation and forward-map setup are reported
separately. This ratio concerns data-to-statistic extraction on one host, not a
hardware-independent speed claim. RAM, wall and CPU consumption are recorded.

## Controls and reproducibility

Algebraic tests cover thinning, the Poisson transform, epsilon=1, linearity,
density scaling and a deliberately wrong endpoint count. A separate norm-based
causal predicate checks samples; full replay regenerates every cloud and count.
All counts, coordinates' hashes, seeds, software versions and source hashes are
retained. The source commit is published before development and test execution.
No external replication or independent peer review is claimed.

## Primary sources

- Benincasa & Dowker, *The Scalar Curvature of a Causal Set*,
  [corrected v4](https://arxiv.org/abs/1001.2725v4),
  [PRL 104, 181301](https://doi.org/10.1103/PhysRevLett.104.181301).
- The pre-existing C2 geometry and certificates are documented in
  [the C2 derivation](../lorentz_de_sitter_c2/DERIVATION.md) and
  [the fixed-N Bennett study](../lorentz_de_sitter_variance/README.md).

Apache-2.0. Original implementation of published mathematical formulas.
