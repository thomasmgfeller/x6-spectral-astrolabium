# Intrinsic landmark calibration: fixed pilot closes with HOLD

19 October 2026. **INTRINSIC_MOMENT_HOLD; HOLD_PHASE3; BD-C2 NO_GO unchanged.**

The 48 preregistered target clouds completed. Neither intrinsic arm adopted new
weights in any cloud. All 42 available baseline stencils had no eligible landmark
triple; six low-density stencils were unavailable. The fallback preserved the
volume-shell baseline exactly. This rejects this fixed landmark selection rule
on the specified supports and density range. It does not rule out intrinsic
moment calibration in general.

## Public chronology and execution

- Protocol and contract before development: `e20dcf39979a3d19848f95122f5ba7cf94dbc180`.
- Implementation, analysis and six development clouds before targets:
  `f1795f2ad98f3b9132f6303e32fe4e6debeb217a`.
- Target records: [execution manifest](results/execution.json), including all
  source and record SHA-256 hashes; [complete frozen summary](results/summary.json).
- All 48 targets completed in **123.778 seconds**, peak RSS **353.699 MiB**;
  bounds were 1200 seconds and 2048 MiB. NumPy 2.3.5, SciPy 1.17.0.

The previously started batch finished across the conversation interruption. Its
original complete records were recovered, hash-checked and retained, with no
replacement seeds, discarded records or overwritten run. All computational
sources, constants and decision gates remain at the public freeze. The six
development clouds remain separate from the 48 targets.

## Availability and primary decision

| Density | Target clouds | Baseline available | Eligible triples across available clouds | Raw adoption | Guarded adoption |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2048 | 16 | 10/16 | 0 | 0/16 | 0/16 |
| 8192 | 16 | 16/16 | 0 | 0/16 | 0/16 |
| 32768 | 16 | 16/16 | 0 | 0/16 | 0/16 |

The primary density is 32768. Availability is 100% (required at least 80%), but
guarded adoption is 0% (required at least 80%). Every paired primary RMS ratio
is **1.0**, whereas independent-field, metric and affine-drift ratios each had
to be at most 0.75. Baseline availability includes fallback; it is not evidence
that the proposed calibration was available.

At density 2048 there are no retained candidates on either side in any available
cloud. At density 8192 only one cloud retains candidates (two on its future
side). At density 32768, some clouds retain as many as the fixed cap of 40
candidates on one side, but none supplies a triple with all three mutual causal
intervals meeting the minimum count. These are descriptive counts from the
archived records, not a new gate or proof of a general obstruction.

The failure occurs **before Gram-signature/conditioning checks, intrinsic
optimization and the thinning guard**. Consequently this target campaign does
not measure the guard's effectiveness or the accuracy of a constructed
intrinsic frame. Analytic software controls for those components pass, but
cannot replace target evidence.

## Independent fields and coordinate diagnostic

The 20 sine/cosine fields are evaluated after inference, and never used for
landmark selection, fitting or guarding. The table uses the same available
stencils for each paired comparison and includes all fallbacks. Scores are
root-mean-square over clouds of the corresponding per-cloud errors; field
normalization is specified in [the protocol](PROTOCOL.md).

| Density | Paired clouds | Field RMS: baseline / both intrinsic arms | Field RMS: coordinate oracle | Metric RMS: baseline / oracle | Affine drift RMS: baseline / oracle |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2048 | 10 | 11.585937 | 6.722834 | 3.000207 / 0.615437 | 1.956754 / 1.106148 |
| 8192 | 16 | 14.860707 | 3.841421 | 2.861638 / 0.173263 | 2.127737 / 0.524131 |
| 32768 | 16 | 27.652199 | 0.964096 | 3.980046 / 0.080702 | 2.892267 / 0.107117 |

The coordinate oracle solves the same regularized optimization using true
simulation displacements. It obtains verified solutions on 42/42 available
stencils. At the primary density, its field/metric/drift RMS ratios are
0.034865 / 0.020277 / 0.037036. Its Lorentz-signature count is 16/16,
versus 10/16 for the baseline and both fallback arms. This is diagnostic
evidence on independent fields **for the coordinate-assisted weights**;
it cannot pass the intrinsic gate or establish convergence, locality or a
physical metric reconstruction. The independent-field error is nonzero.

The summary retains all 20 field-level errors and paired squared-error
reductions with cloud-level standard errors. Intrinsic paired reductions and
their standard errors are exactly zero because the weights are unchanged.
These fixed pilot gates are descriptive; no statistical significance claim or
confidence guarantee is made.

## Amplification and numerical verification

At density 32768, mean dimensionless absolute coefficient mass is 16.387621
for the baseline/fallback and 15.579953 for the oracle. The mean dimensionless
sum of squared coefficients, including the root, is 84.200045 versus 76.202655.
At density 2048 the oracle's corresponding squared-coefficient mean increases
from 85.536839 to 262.665320. Thus improved field error is not a general noise
improvement. The dimensional factors are retained in each record.

Absolute coefficient mass bounds errors in bounded field differences. The
squared-coefficient sum is a variance multiplier only for independent,
equal-variance additive field noise. Neither is a measured robustness result.
No empirical thinning-guard evidence exists in this campaign because no frame
reaches that stage.

Software checks include exact polarization/scaling, signature rejection,
analytic quadratic optima, invalid-certificate rejection, inconsistent-half
guard rejection and the coordinate-blind inference interface. Mark-preserving
relabeling and transported time reversal are tested on the first target at each
density, conditional on the inherited root/support. Constants and product
identities pass on all available arms. All 42 stored coordinate-oracle
certificates independently satisfy the frozen feasibility and relative
optimality-gap bounds; no intrinsic target certificate exists.

[VERIFICATION.json](VERIFICATION.json) records a full local numerical replay of
all 48 clouds and all 42 calibrations. Both archived and recomputed certificates
are checked. Discrete structure, candidate counts and fallback decisions must
match exactly; inherited baseline checks retain atol=1e-10, rtol=1e-9. New
calibration comparisons retain atol=1e-7, rtol=1e-6. Coordinate byte hashes are
reported separately. This is internal reproducibility, not external replication.

```sh
python3 -m pip install -r research/lorentz_bd_reference/requirements-replay.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/intrinsic_moments/verify_intrinsic.py
```

## Consequence for the next milestone

Close this candidate as HOLD without lowering count thresholds or promoting the
oracle. Before proposing another full test campaign, examine the geometric and
combinatorial availability of landmarks relative to the frozen support. A new
construction needs its own public protocol, development data and fresh targets.
The present result does not distinguish a fundamental obstruction from the
effects of finite support, boundaries, the candidate cap and count thresholds.
Known density and flat 2+1 geometry remain assumptions. Phase 3, curved-space
claims, 3+1 validation and external replication remain open.
