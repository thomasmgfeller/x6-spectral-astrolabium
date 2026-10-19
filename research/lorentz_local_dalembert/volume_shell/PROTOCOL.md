# Intrinsic shell weighting: frozen protocol, 19 October 2026

The moment audit found much larger diagnostic improvements from shell proper
times and reference directions than from endpoint times. This next bounded
experiment tests only an intrinsic shell-weight candidate. It does not combine
an untested direction rule, change memberships, or qualify Phase 3. All earlier
phase12, anchor_audit, moment_audit and BD-C2 files remain immutable.

## Candidate and fixed comparators

For every selected point b, count strict interior events N(root,b) in the causal
interval, orienting endpoints according to the relation. In the known flat
2+1 reference, define qhat_b = [N/(rho * (pi/12))]^(1/3).
The count-to-time formula is a plug-in estimator; longest-chain shell selection
makes the counts conditional. No unbiasedness or independence is asserted.
Zero interior counts make the corresponding weighted stencil unavailable.
No pseudocount, clipping, fitted correction or test-dependent threshold.

Reuse the unchanged balanced64 stencil, root, temporal endpoints, two selected
shell populations, tn/tm and C=243/29. Five fixed arms on each cloud:

* raw: unchanged chain-time weights.
* volume_shell (sole primary candidate): each shell point gets
  C/(N_side * qhat_b²); temporal weights remain -(C+3)/tn².
* volume_both: same shell weights, temporal weight -(C+3)/qhat_b² for each
  of the two endpoints. Secondary ablation, never selected as a fallback winner.
* oracle_shell / oracle_both: corresponding weights using exact embedding
  proper times. These are coordinate-assisted diagnostic comparators, not
  intrinsic methods or lower bounds.

Weights for repeated support events are summed. All arms apply
Bf=sum_b weight_b*(f_b-f_root). The candidate module receives no coordinates,
sampler, test fields or evaluation outcomes. Reference axes and memberships stay
fixed. Correcting weights does not move points or align directions. Algebraic
metric responses of oracle arms must equal the previous S/TS moment controls.
Their responses on linear or general fields need not equal those artificial
coordinate-vector interventions; they are genuine reweighted operators here.

## Fresh data and execution

Publicly freeze this protocol before six development clouds; publicly freeze
implementation AND analysis before 48 fresh targets, 16 per density 2048, 8192,
32768. Seeds and bounded resources are in contract.json. No replacement seeds,
post-development parameter tuning, post-test source fixes or early statistical
stopping. Archive every cloud's status, count/time estimates, weights, hashes,
field responses and resources. Failure/budget exhaustion is a documented HOLD.

## Observables and prespecified descriptive gate

For smooth fields X=(t,x,y), measure M=1/2 sum w dX dX^T and its relative
Frobenius error ||M-eta||/sqrt(3). Also measure affine drift A=B(X), whose target
is zero, and dimensionless magnitude a=tm*||A||/sqrt(3). Archive both dimensional
A and a. The normalization allows same-scale comparisons; a small a by itself
does not establish convergence of the dimensional operator.

Record constants, all three linear fields, all six quadratic monomials and
exp(t+x+y), including known flat d'Alembertian targets. Test exact product
identity and affine transformation law. Report Lorentz signature for all arms,
actual/estimated proper-time ratios, interval populations, paired squared-error
reductions with cloud-level standard errors and denominators. No point-level
pseudoreplication. Errors are evaluated in the original diamond frame; the
Frobenius and Euclidean drift norms are not Lorentz-invariant.

Primary gate at rho=32768 for volume_shell: availability >=80%, paired metric
RMS <=75% of raw RMS, and paired affine drift RMS <=110% of raw drift RMS. Use
exactly the intersection of available clouds for both paired ratios. Missing
cases remain in the all-cloud availability denominator. Report all five arms
regardless of outcome. These are descriptive finite-budget thresholds, not a
confidence-certified noninferiority or convergence claim. All three gates plus
complete execution, resource and software controls must pass to label
INTRINSIC_SHELL_WEIGHTING_IMPROVED; otherwise SHELL_WEIGHTING_HOLD.

Always retain HOLD_PHASE3. The inherited absolute metric threshold 0.5, broader
field tests, intrinsic chart qualification and full flat acceptance are not
replaced by this improvement gate. If the primary arm fails, stop this candidate
at the declared budget without selecting the secondary arm or refitting. If it
passes, retain it only as a development candidate and separately investigate
reference-direction and angular/boundary effects with a new frozen protocol.

## Controls and replay

Independent hand-counted causal intervals and explicit weight formulas;
zero-count rejection; density-scaling law; time reversal and relabelling;
coordinate-blind module interface/import checks. On one development and target
cloud per density, repeat intrinsic weights under a fresh event permutation.
On every usable cloud check constants, product identity, affine tensor law and
oracle equivalence to the independently archived moment implementation.

Replay every target, verify public source and record hashes and recompute the
full summary. Discrete outputs/relation hashes exact, numerical outputs within
atol=1e-10 and rtol=1e-9. Coordinate byte hashes are reported separately; the
previous GitHub run passed numerical replay with 0/48 byte-identical coordinate
hashes, while the local run had 48/48. Do not assert platform bitwise identity
or change tolerances in response to this known distinction.
