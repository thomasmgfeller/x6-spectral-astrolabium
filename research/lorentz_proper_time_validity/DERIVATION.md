# Eigenzeit v0.2: model, observation and finite information

This is a deterministic sensitivity analysis of the existing fixed-budget
reference. There are no new sampled causal sets and no measured spacetime.
All endpoints, models and grids are fixed before evaluation. The outer proper
time T is supplied independently. The target theta=tau/T is the maximum
geodesic proper time between the central marked endpoints, not time on an
arbitrary accelerated worldline. Background counts exclude the endpoints.

## 1. What counts actually identify

Let D be the outer diamond and I the contained marked interval. Given m iid
observed points with probability measure nu, K is exactly Binomial(m,p), where
p=nu(I)/nu(D). The count identifies this probability. Converting it to proper
time requires additional geometry and sampling assumptions.

For uniform flat d-dimensional sampling, p=theta^d and the published raw
estimate is (K/m)^(1/d). A monotone transformation of a two-sided 95%
Clopper-Pearson probability interval gives a pointwise 95% proper-time
interval. This is fixed-budget coverage; neither simultaneous coverage over
the displayed cells nor optional-stopping coverage is asserted.

## 2. Exact curved-family probabilities

For d=4 take g=(1-h*t)^(-2) diag(-1,1,1,1), with 0<=h<2, on
|t|+norm(x)<1/2. This is the previously studied de Sitter coordinate patch.
Its physical volume measure is (1-h*t)^(-4) dt d^3x. For a central
coordinate diamond of span a,

    V_h(a) = (4*pi/3) integral[-a/2,a/2]
                (a/2-|t|)^3 (1-h*t)^(-4) dt.
    tau_h(a) = 2*atanh(h*a/2)/h.
    theta = atanh(h*a/2)/atanh(h/2).

Thus a=2*tanh(theta*atanh(h/2))/h and p=V_h(a)/V_h(1).
At h=0 the continuous limits are tau=a and p=a^4. The outer T=tau_h(1)
is assumed independently known; the flat estimate must not supply it.
The calculation uses exact family integrals, not a small-curvature RSS
truncation. Even the stronger h values are only stress points in this family.
No continuous or general-curvature validity window follows from this grid.

Fixed Gauss-Legendre integration on the two half intervals is compared with
adaptive integration. Agreement is not a rigorous quadrature error enclosure.
The old family and density-twin construction are documented in
[the curvature study](../lorentz_curvature/README.md); the conditional RSS
derivation remains [separate](../lorentz_rss_fixed_n/DERIVATION.md).

## 3. Density and missing observations in flat geometry

In a flat four-dimensional diamond, E[(2t)^2]=1/15. With sampling intensity
w(t)=1+beta*(2t)^2 (beta>-1), exact central-interval probability is

    p = a^4 (1+beta*a^2/15)/(1+beta/15),    theta=a.

For independent retention probabilities s_in and s_out, conditional on the
retained count m, p=s_in*q/(s_in*q+s_out*(1-q)), q=theta^4. Uniform thinning
leaves p unchanged. m is the observed count: a 50% uniform retention rate
requires twice as many initial points on average. Selective thinning can
change p even with arbitrarily large m. Correlated missingness is outside scope.

The flat density twin uses intensity (1-h*t)^(-4) and the *same* coordinate
endpoints as its curved partner. It has the same full iid coordinate law and
causal relations, hence the same count and every order statistic. Its true
proper-time ratio is a, rather than theta_h(a). The two rows deliberately
have different truths. This indistinguishability is inherited from the
known conformal construction, not newly established by count calculations.

## 4. An externally bounded nuisance ratio

In flat geometry let r be the average observed intensity inside I divided
by its average outside I. Then

    p = r*q/(1-q+r*q),       q = p/(r+(1-r)*p).

If externally justified bounds r_low<=r<=r_high are known, and [l,u] is a
Clopper-Pearson interval for p, a conservative proper-time interval is

    L = [l/(r_high+(1-r_high)*l)]^(1/d),
    U = [u/(r_low +(1-r_low )*u)]^(1/d).

The inverse is increasing in p and decreasing in r. Therefore the event
p in [l,u] implies theta in [L,U] for every r in the assumed bounds: the
fixed-budget coverage is at least 95% throughout that flat model class.
The bounds are assumptions, not estimated or certified by K. They do not
correct curved geometry, unknown dimension, scale error or dependent sampling.
Pointwise intensity bounds are sufficient but stronger than bounds on this
particular inside/outside average. Postselection of the endpoints is excluded.

For L>0 the harmonic center H=2LU/(L+U) has maximum relative error
(U-L)/(U+L) over all true values in [L,U]. For L=0 this radius is 1 and
the requested precision is not certified. Consequently

    P(radius<=0.1 AND |H/theta-1|>0.1) <= 0.05

under the stated fixed-budget model. This is an unconditional event bound,
not a bound conditional on successful precision declarations. The original
raw count estimate remains reported separately; it is not H.

As m increases, [l,u] approaches p while the nuisance interval generally
remains nonzero. Its limiting radius is reported in every row. More counts
cannot remove this assumed density uncertainty. This is a useful design
limit even if a particular finite-sample interval occasionally becomes narrow.

## 5. Numeric evaluation and declared decision

The grid enumerates binomial support between the lower and upper tail
quantiles at 1e-13 per side, retaining the omitted probability. No
renormalization is performed. Each reported event probability differs from
the full mathematical sum by at most the omitted mass, apart from library
roundoff. Raw relative bias and MSE have explicit omitted-tail bounds using
max(1,1/theta-1). These do not certify floating-point rounding errors.

An independent checker obtains coverage through integer acceptance bounds
from binomial CDF/survival functions, without inverse beta functions or the
producer's interval masks. It independently integrates geometry and checks
off-grid rational finite laws, interval inversion and intentional mutations.
Full replay checks every field and planning decision; it is internal checking,
not external scientific replication. Acceptance endpoints are archived.

A cell meets the declared criteria only if its assumptions hold, coverage
is at least 95% (numerical tolerance 5e-10), and it declares <=10% relative
precision with probability at least 90%. We publish the first passing
budget on the fixed grid, not an optimal or universally sufficient budget.
Cells outside the assumed class remain so even if their numeric coverage
happens to be high. No-warning results do not establish model validity.

## Attribution and next boundary

- [Original conditional flat reference](../lorentz_proper_time_domain/README.md).
- [Published sequential reference](../lorentz_proper_time_sequential/README.md)
  addresses optional stopping separately; this grid does not replace it.
- [NIST exact binomial confidence limits](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbici.htm).
- [Roy, Sinha and Surya](https://arxiv.org/abs/1212.0631), for the existing
  small-diamond curvature research context; no correction of their paper is claimed.

The next separate curvature task needs covariance-aware information planning,
an explicitly restricted one-parameter model, and independent scale. This
milestone does not attempt a new RSS inverse, a chain-clock calibration,
general geometric reconstruction or physical Planck-time measurement.
