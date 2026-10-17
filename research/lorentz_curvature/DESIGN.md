# Bounded curvature sensitivity and exact density confounding — frozen design

Date: 2026-10-17. This is a prospective computation contract. The source
commit containing this document must be publicly available before the first
target invocation. Development checks use a separate namespace. No target
outcome is assumed. The complete result will be in `RESULTS.md`.

## 1. Question and limit

Can longest-chain height and a fixed joint statistic of 2-, 3-, and 4-chain
abundances distinguish the declared uniform flat reference from a specified
uniform curved reference at finite N? What warnings are also produced by
flat density and observation-mask disturbances?

The universal curvature claim is already ruled out for unrestricted sampling
density by the exact conformal-twin construction below. This benchmark
quantifies *model deviation sensitivity*, conditional on the declared
sampling assumptions. It does not estimate curvature, validate a physical
clock, identify dimension, or apply the small-curvature inversion formulas
of Roy, Sinha and Surya. A failed sensitivity gate is a result, not a reason
to add seeds or change the geometry.

## 2. Geometry, volume and an independent clock

Use c=1, signature (-,+,+,+), coordinates x=(eta,x1,x2,x3) and the fixed
coordinate diamond D: -1/2 < eta < 1/2, |x| < 1/2-|eta|. Endpoints are
(-1/2,0) and (+1/2,0). They are not counted among the N internal points.
The declared metric family is

    g_h = a_h(eta)^2 diag(-1,1,1,1),  a_h(eta) = 1/(1-h eta),  0 <= h < 2.

For h>0 this is the spatially flat patch of 4D de Sitter, after a conformal
time shift. Cosmic proper time is t = -log(1-h eta)/h, so a=exp(ht).
The conventional Ricci sign used here gives R=12 h^2 and R_(00)=-3 h^2 in
an orthonormal timelike frame. `selftest.py` contracts all Christoffels with
exact rational arithmetic independently of this formula.

Positive conformal multiplication preserves chronological relations:
x precedes y exactly when delta eta > |delta x|. Every future-directed
causal curve between the endpoints has length at most integral a d eta;
the central comoving curve attains this bound. Thus

    tau_h = log((1+h/2)/(1-h/2))/h,   tau_0=1,
    V_h = (4 pi/3) integral[-1/2,1/2] (1/2-|eta|)^3 a_h(eta)^4 d eta.

The oracle integrates this one-dimensional volume, with separate smooth
halves, and checks against Gauss-Legendre quadrature. Neither tau, h,
coordinates nor volume enters either order-only detector.

h = 1/4, 3/4, 5/4 are fixed in advance. The largest is a strong exact
geometrical stress case, not a small-curvature expansion. No perturbative
formula is assumed there; H tau and R tau^2 are reported to expose scale.
This family probes positive constant curvature only. It says nothing about
Weyl curvature, other metrics, or a generic spacetime sensor.

## 3. Uniform physical-volume sampling and controls

Each sample has exactly N=64 or 128 points. This is the conditional law of
a Poisson sprinkling given N; it is not a fluctuating Poisson-count experiment.
Fixing N removes total count as a detector input and changes the question
relative to an equal-known-intensity experiment.

The flat proposal is uniform in D: the slice half-width w has density
proportional to w^3, the time sign is equiprobable, and points are uniform
in the corresponding 3-ball. Rejection with probability

    [(1-h/2)/(1-h eta)]^4

produces density a_h^4 / V_h, precisely uniform in dV_g. The envelope is
finite on this diamond. The sampler rejects only proposals according to
this fixed law, never an inconvenient completed order. Separate seeds are
SHA-256-derived from phase/N/family/index; no seed replacement is allowed.

Controls (same fixed N):
- flat uniform null;
- flat spatial compression x -> x/2 at unchanged eta and flat metric;
- flat observation mask eta >= -0.2, with conditional uniform sampling in
  the visible region while the detector still assumes the whole diamond;
- paired deletion of one transitive relation with a retained two-step
  witness, if such a witness exists. Structural validation must refuse it.

**Exact density twin:** interpret each de Sitter point cloud instead as flat
spacetime with sampling density proportional to a_h^4. Its coordinate law
and every causal relation are identical, but its endpoint proper time is 1
and curvature is zero. An independent norm-based predicate checks equality
against the squared-cone predicate. Consequently every function of the
full order, including these scores and p-values, has the same distribution.
The paired examples are coupled identity checks, not extra independent
observations. Even without conditioning on N, choosing the flat intensity
measure rho_flat(x) d^4x = rho a_h^4 d^4x reproduces the Poisson order law.
Independent knowledge of the sampling law is therefore necessary for this
comparison to support a geometrical interpretation. More order features
cannot remove this exact ambiguity.

## 4. Algorithms fixed before targets

C_k counts k distinct comparable elements, including non-neighbouring
relations; these are not link counts or inclusive-interval abundances.
C1=N; the detector uses C2/choose(N,2), C3/choose(N,3), C4/choose(N,4).
The joint statistic Q is the maximum absolute standardized feature, using
means and sample standard deviations from 256 flat training orders per N.
Longest-chain height H counts internal vertices. All methods see only the
full strict relation. Independent verification uses C3=sum indegree*outdegree
and C4=sum_(i precedes j) indegree(i)*outdegree(j), plus a separate height DP.
Brute-force subset enumeration checks small orders and relabelings.

For each N an independent bank of B=1023 flat calibration orders is drawn.
Q has upper-rank p=(1+#Q_cal >= Q_obs)/(B+1); H uses the conservative
two-sided tied-rank p=min(1,2*(1+min(#H_cal<=H_obs,#H_cal>=H_obs))/(B+1)).
Each detector warns at p<=0.025. No feature is selected by target outcomes.

Conditional on training, exchangeability gives the rank guarantee marginal
over the random calibration bank and a fresh null target. **The bank is
shared.** Target rejection probabilities conditional on the realized bank
need not equal 0.025. The 512 target orders per family/N are independent
conditional on training and bank; their Clopper-Pearson intervals describe
that conditional warning probability. They must not be presented as an
independent binomial proof of the marginal nominal rank level. The two
methods and paired twins are not independent, and warning by either method
is not automatically a 2.5% combined test.

There are 8,702 independent orders: per N, 256 training + 1023 calibration
+ 6*512 targets. There are additionally 3,072 coupled density-twin checks
and at most 1,024 paired relation-error checks.

## 5. Decisions, uncertainty and stopping

The prespecified primary cell is N=128, de_sitter_125, compared with
flat_uniform at N=128. For each of the two methods require both:

1. upper one-sided conditional null-warning bound <= 0.05;
2. lower one-sided conditional alternative-warning bound >= 0.80.

The four selected one-sided endpoints share family alpha=0.05, i.e.
0.0125 per endpoint. This Bonferroni rule does not require method independence.
Only these four endpoints are asserted jointly; the other endpoints emitted
for convenience are not part of that joint assertion. Passing means
PRIMARY_MODEL_DEVIATION_SENSITIVITY_ESTABLISHED in this primary cell.
Otherwise record PRIMARY_SENSITIVITY_NOT_ESTABLISHED. The label
NOT_IDENTIFIABLE_WITH_UNRESTRICTED_SAMPLING_DENSITY applies in either case.

All secondary rate intervals are pointwise two-sided 95%, descriptive only.
Joint-only and height-only counts are paired descriptions, not a superiority
claim. Density/mask warnings are detection of a sampling-model violation,
not successful identification of curvature and not null false alarms.

Hard execution budget: 600 seconds and 2 GiB address space. Abort on invalid
generated orders, nonfinite scores, zero training scales, hash violations,
or resource exhaustion. No further seeds, tuned thresholds, new primary
cells, or post-hoc rescue runs. Display, repeated interactive looks and
Planck-unit conversion are outside this finite benchmark.

## 6. Evidence and sources

Archive every training, calibration and target full relation, feature,
namespace/seed, proposal count and coordinate hash. Record the original
source commit, source hashes, execution metadata and all test p-values.
Preserve the complete first run. Replay reconstructs every point cloud and
relation using the same seeds in a new directory and compares all scientific
outputs. Self-checks and CI replay are internal reproducibility, not external
replication. Sources and environment use float64; this is not formally
verified interval arithmetic.

- Roy, Sinha and Surya, *The Discrete Geometry of a Small Causal Diamond*,
  Phys. Rev. D 87, 044046 (2013), https://arxiv.org/abs/1212.0631,
  especially definitions of k-chains and their curvature-dependent abundance.
  Their asymptotic curvature inversion is not claimed as implemented here.
- Surya, *The causal set approach to quantum gravity*, Living Rev. Relativity
  22, 5 (2019), https://arxiv.org/abs/1903.11544, for causal order, volume and
  sprinkling foundations. The exact density-twin proof above is given here
  explicitly; it does not depend on empirical classification accuracy.
- Existing bounded time and chain reference:
  ../lorentz_proper_time_sequential/README.md. That original frozen evidence
  remains unchanged. No new scientific priority is claimed for these known
  geometry or statistical constructions.
