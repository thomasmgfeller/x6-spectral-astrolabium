# Conditional noise and relation-compatible geometry: frozen pilot

All 64 PR69 clouds are now openly reused as development/calibration data,
including the former test split. None is a fresh validation observation here.
Exactly 32 new seeds in contract.json are reserved for evaluation; no replacement.
Two deterministic shards split the list by parity. Code, protocol, contract and
calibration parameters must be committed and publicly reachable before those
clouds are generated. Outcome-dependent changes require a new protocol/test set.

## Measurement model and limits

For cloud C and two operators (original QP and projected-geometry QP), write
z = theta 1 + b(C) + B(C) epsilon. The event noise is independent zero-mean
Gaussian with KNOWN sigma=0.001; selection and weights do not access epsilon.
The full B includes the root coefficient -sum(a)/scale² and all support
coefficients a/scale². Therefore N(C)=sigma² B B^T is the exact conditional
field-noise covariance, including cross-arm and root correlations.

For fixed C, b(C) is a deterministic clean-response error, NOT additional
random sensor noise. Across independently sampled clouds, the total covariance
identity is Cov(z-theta)=Cov(b(C))+E[N(C)]: the cross term is zero by conditional
zero-mean noise. We estimate mu and G=Cov(b) ONLY from clean simulation responses
on development clouds. Thus G includes discretization, reconstruction, support
selection and field/model effects; it is not a separately identified curvature
error or an embedding covariance. No noisy residual covariance is added again.

Working matrices R(C)=G*(1+1/n_cal)+N(C) keep these terms separate. G/n_cal is
only bias-mean estimation variance for this calibration distribution. G is
NOT a proved conditional covariance at C; b(C) can be systematically related
to N(C), and adaptive fusion weights can induce residual bias. We explicitly
report clean bias and noise-stratified clean errors, coverage, NEES and NIS.
Parameter uncertainty/non-Gaussian errors are not solved by this decomposition.
Calibration with clean truth is simulation-assisted and not available from a
single real noisy cloud without independent calibration information.

## Relation correction

Retain the frozen selection and hidden-colour audit. Extract the full observed
strict order on root+support BEFORE accessing hidden coordinates/field truth.
Orient the initial reconstruction with the designated future anchor; normalize
by the inherited scale; fix root=0. Minimize half the squared displacement in
this chosen reconstruction frame. For every observed i<j in the order impose
t_j-t_i >= ||s_j-s_i|| + margin. For every incomparable pair choose the unit
direction u from its initial spatial displacement and impose
u·(s_j-s_i) >= +(t_j-t_i)+margin AND >= -(t_j-t_i)+margin.
By Cauchy-Schwarz these two affine constraints ensure strict spacelike separation.
The feasible region is a convex inner approximation (Lorentz cones plus affine
halfspaces), not a proof that every valid order can be repaired. The objective
is frame/gauge dependent; no Lorentz-boost equivariance is claimed.

Use SLSQP with analytic Jacobians and fixed tolerances. Acceptance requires
solver success, all constraint slacks >= -1e-8, relative shift <=25%, and an
independent strict squared-interval order check. A failure is UNRESOLVED, never
a proof of nonembeddability. No relation labels are changed. Recompute both
unrestricted minimum-variance QPs, require moment/KKT certificates and bounded
design condition, then seal weights before hidden field evaluation. A repaired
order is a construction requirement, NOT independent evidence of correct metric
lengths. Report all failed cases and the clean operator error after projection.

The observed relation is assumed complete and exact. Missing edges cannot be
treated as incomparable when the measurement order is partial or uncertain.
Projection uses root/support only, not all landmarks or the whole cloud. Original
colour guards apply to original geometry; projected geometry is not thereby
newly qualified by those guards. No nonlinear covariance projection is claimed.

## Frozen analysis and gates

Two scalar responses use the same diagnostic field exp(t/2)cos(x/2)cos(y/2),
truth -0.75, one shared field-noise sample, one independent synthetic prior of
sigma=0.5 per fresh cloud. This remains an offline one-step pilot with future
supports and prior/measurement cross covariance zero BY CONSTRUCTION only.

Compare on the common complete cases:
1. Original QP, global G00*(1+1/n)+mean(N00).
2. Original QP, conditional G00*(1+1/n)+N00(C).
3. Projected QP, conditional G11*(1+1/n)+N11(C).
4. Joint original/projected fusion with simplex weights minimizing w^T R(C) w.
5. Noise-only joint fusion dropping G: labelled negative control.
6. Independent prior alone, for context and absent-measurement accounting.

Bias corrections from clean calibration are the same in all eligible arms.
Availability is measured over all 32; absent cases keep their prior and are
never labelled measurements. Report common-case and all-cloud fallback RMSE.
Report raw/clean errors, mean bias, conditional N ranges, per-cloud weights and
separate noise/geometry/bias-mean contributions, nominal 95% coverage with exact
binomial interval, NIS/NEES, paired cloud bootstrap with 5000 frozen draws.
Bootstrap conditions on calibration; correlated noise replicates never increase
the number of independent physical clouds.

Gates, budget and seeds are fixed in contract.json. Projection's zero wrong-pair
gate is checked separately from accuracy. Require no >5% clean-RMSE degradation;
at least 5% posterior improvement for conditional vs global and joint vs
conditional-original. A point estimate passing is only pilot support, not a
guarantee. HOLD_PHASE3 always persists. Historical results remain byte-unchanged.

## Verification and references

Independent field replay, QP certificates, exact root-noise algebra, shared-arm
noise negative control, pure-geometry/no-noise control, nontransitive input
rejection, missing/extra relation counterexamples, relabelling and spatial
rotation checks; numerical constraint Jacobians checked by finite differences.
The numerical order predicate is independent of the optimizer constraints.

The covariance identity above follows directly by conditioning. The convex
cone formulation uses standard optimization, not a novelty claim; see Lobo,
Vandenberghe, Boyd & Lebret (1998), Applications of Second-Order Cone Programming:
https://stanford.edu/~boyd/papers/socp.html . No global optimality or infeasibility
certificate is claimed for SLSQP; accepted feasibility is checked independently.
