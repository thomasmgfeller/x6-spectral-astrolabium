# Continuous exclusion of the node-15/node-5 coupled line

SPDX-License-Identifier: Apache-2.0

**Result: every step h in [-0.1,0.1] on this one coupled line is excluded as a
strong close-law counterexample.** This closes both signed PR111 rays 0 and 1,
including all values between the seven previously sampled steps. The other
58 paired rays and general finite-error operator stability remain open.

Node 15 moves in boosted x by `(250000000000/264451347681)*h`, node 5 by `-h`.
The landmarks, root, sampling density, scale and outer diamond stay fixed.
The excluded conjunction is unchanged selected-node order, symmetric relative
operator-weight gap **>20%**, and full conditional count/overlap-law **TV<=0.25**.
This is one one-dimensional family, not a two-dimensional box of independently
variable support displacements.

## Three completed steps

1. **The neighborhood of h=0.05 is certified directly.** The unchanged event
   `N(I(5,1))-2*N(I(2,5))<=891` proves full-law
   **TV >= 0.27022107157440214490** uniformly on **[0.045,0.055]**.
   All 210 selected-node pair relations preserve their signs and separation
   margins throughout this neighborhood. [focus.json](focus.json) retains the
   mean and probability enclosures.
2. **Both supports are handled in one operator calculation.** An exact rank-four
   moment update includes their interaction. Directed polynomial residuals
   certify matrix invertibility and the weight-gap bound on entire cells.
   [THEOREM.md](THEOREM.md) gives the algebra and complete-cover argument.
3. **Overlap correlations close the negative-direction gap.** The original
   screen left 202 cells between approximately -0.048877 and -0.031348.
   A separately frozen difference-count bound excludes every one with
   **TV >= 0.46181006724951309881**. The original HOLD output is preserved.

## Why the difference of overlapping counts helps

Set A=I(5,1), B=I(15,1) and D=N(A)-N(B). The shared points cancel in D, giving

    E[D] = mu_A-mu_B,
    Var(D) = mu_A+mu_B-2*mu_(A intersect B).

The overlapping counts are not treated as independent. A virtual future tip
constructs a subinterval contained in their intersection, hence a rigorous
lower bound on the common intensity and an upper bound on Var(D). A one-sided
Cantelli event then separates the two laws, with no numerical integration or
Monte Carlo overlap estimate. The virtual tip is only a proof device, not an
extra observed landmark. See [OVERLAP_PROOF.md](OVERLAP_PROOF.md).

For context, the reference variance upper bound for D is about **60.0271**.
At the weakest newly excluded cell, the moved mean lies in [34.3441,34.4239]
and its variance upper bound is about **70.5777**. The reference difference
mean is about **60.0270**. Keeping the shared-cloud covariance is decisive here.
This cancels shared count noise in an observed statistic; it does not demonstrate
a hidden geometry change whose full count law is unchanged.

## Complete coverage and decisions

The frozen screen starts with 64 closed cells and performs eight bounded
refinement rounds. It evaluates 472 cells in total and leaves a complete cover
of 268 terminal cells. The follow-up changes no interval endpoints and adds no
new geometries; it only certifies the previously unresolved terminal cells.

| Final terminal-cell certificate | Cells |
|---|---:|
| Operator gap at or below 20% | 27 |
| Single-count TV lower bound above 0.25 | 7 |
| Disjoint two-count event TV lower bound above 0.25 | 32 |
| Overlap-aware difference-count TV lower bound above 0.25 | 202 |
| Unresolved | 0 |

The lower bound 0.46181 applies to the 202 overlap follow-up cells, not to the
entire domain. In particular h=0 has TV=0 and is excluded by its zero operator
gap. All shared terminal endpoints are covered.

The initial result is [summary.json](summary.json); the final combined decision
is [combined_summary.json](combined_summary.json). The full archive is
[cells.json.gz](cells.json.gz), with [overlap certificates](overlap_certificates.json).
The original and follow-up contracts and source freezes are kept separately.
Both are internal reproducibility records, not external preregistration.

## Verification

```sh
python3 -B research/lorentz_local_dalembert/paired_continuous/pc_run.py --verify
python3 -B research/lorentz_local_dalembert/paired_continuous/pc_audit.py --verify
python3 -B research/lorentz_local_dalembert/paired_continuous/pc_overlap.py --verify
python3 -B research/lorentz_local_dalembert/paired_continuous/pc_overlap_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/paired_continuous/SHA256SUMS
python3 tests/python/verify_manifest.py
```

Independent audits compare 145 direct rational nine-moment solves against the
four-dimensional update, perform 4,468 direct quadratic checks, four direct
110-digit joint PMF sums, 203 whole-cell future-tip checks, 609 rational virtual-tip
checks, 203 variance identities and all 202 Cantelli events. They also verify the
complete cover and deterministic refinement sequence. Controls reject missing
coverage, a dropped two-endpoint cross term, and an unjustified matrix solve;
synthetic Poisson controls detect underestimated variance.

Inputs are pinned to PR111 commit `5b47e27614627a169986344d2d56e66e8e7ae753`,
tree `61a507c09d454848e80afd59742c0a50416136d2`. The local checkpoint commit can
differ because publication used the GitHub API; its source tree is identical.

## Next decision

Do not sample this line more densely: its declared continuous domain is closed.
The next useful expansion is to generalize the overlap-difference construction
to the remaining paired directions, preserving the exact observable mask and
the intersection lower bounds. A claim about all coordinated movements still
requires a genuinely multidimensional cover or a uniform modulus for the
operator. No full A/B-data likelihood or physical continuum accuracy is proved.
