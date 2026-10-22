# Correlation-preserving surface tests: actual-pair cancellation certified

SPDX-License-Identifier: Apache-2.0

**SURFACE_CORRELATION_CERTIFIED. Positive cancellation is now certified for the
unchanged PR95 pair.** The TV upper bound decreases from
**0.01981978079819577960 to 0.01894939530593638801** (about 4.39% tighter).
The spatial grids, deformation, Poisson density and observation channel are
unchanged. This is a certified upper bound, not measured TV or an improvement
in reconstruction accuracy. The symmetric operator gap remains about 0.00365762%,
far below the 20% strong-pair threshold. No strong pair or global stability claim.

| Spatial grid | Fully labelled transfer cells | Directed transfer pairs | Actual cancellation lower bound | TV upper |
|---|---:|---:|---:|---:|
| 16 × 16, bisector split | 3 | 2 | 0 | 0.02814356767479259583 |
| 32 × 32, bisector split | 80 | 12 | 0.00018913258647640640 | 0.02255212956619461688 |
| 64 × 64, bisector split | 659 | 21 | 0.00070887297614050843 | 0.01894939530593638801 |

At level 64, of 8,320 surface rectangles, 6,398 are outside the outer diamond,
659 are completely labelled, and 1,263 remain unresolved. The unresolved
transfer mean upper bound is 0.01282469835364486998 and is fully retained.
The bound on total changed membership intensity is exactly the PR103 bound
0.02001882707982844326; the extra improvement therefore comes from signed
transfer accounting, not a smaller spatial change region.

## Preserve the correlation before applying interval bounds

In the inherited boosted frame the moving tip is v; its displacement is +h in x.
For a spatial point X=(x,y), set r=|X-v_space|. On either moving strip,

    t = v_t + s*(r+e),    s in {+1,-1},

where e lies between 0 and r1-r0, with its sign determined by the spatial
bisector. The inherited strip routine encloses e without subtracting two large
uncertain radii. For any OTHER fixed tip w, put d=v_t-w_t. The squared timelike
separation is EXACTLY

    Q_w = (t-w_t)^2 - |X-w_space|^2
        = d^2 + |v_space|^2 - |w_space|^2
          + 2 X·(w_space-v_space) + 2 s d r
          + 2 s d e + 2 r e + e^2.

The r^2 term cancels the spatial quadratic term before interval evaluation.
This avoids treating time and position as independent coordinates of a box.
All coefficients and interval operations are rational. The time difference
T_w=d+s*(r+e) is enclosed separately to distinguish future from past.
For either cone orientation k=+1 or -1:

- certainly inside when inf(k*T_w)>0 AND inf(Q_w)>0;
- impossible when sup(k*T_w)<=0 OR sup(Q_w)<=0;
- otherwise unresolved.

These implications apply throughout the complete spatial cell and strip.
The active moved-tip membership is imposed analytically as in PR103; the
opposite cone is false. All other tips are unchanged between the two geometries,
so the same correlated tests apply to both. Null boundaries have zero intensity.

## Reuse valid exclusions; do not trade one certificate for another

Some outer-diamond exclusions are sharper with the earlier integer box tests.
The implementation retains both: an outer or affected-interval impossibility
certificate from either method excludes the cell; any complete prior label is
reused; two complete labels must agree exactly. The grid and strip mass bounds
are identical to PR103. This is a combined certificate, not a claim that the
surface formula dominates every old interval bound separately.

A complete before/after pattern yields a directed transfer intensity interval.
Its lower and upper bounds are exact area times the inherited thickness bounds,
rounded outward to 30 decimals. Every unresolved cell contributes its entire
upper intensity to R. Interval counts, all overlaps, and optional total count
retain the same full-law coupling interpretation and conditional scope as PR95.
No interval-count independence approximation or unknown-label deletion is used.

## What is proven to cancel

For each atom b, incoming and outgoing transfer intensity intervals imply the
actual cancellation lower bound

    C_L = sum_b min(incoming_lower_b, outgoing_lower_b).

At level 64, C_L >=0.00070887297614050843 >0. This lower bound is reconstructed
independently from the archived directed-transfer table by the audit. Additional
unknown transfers cannot reduce it. Cancellation here means cancellation of
signed intensity differences in aggregate count laws; it need not be a literal
pairwise reversal between every two spatial cells.

Two valid upper bounds on the balanced residual mean D are combined:

    D <= M_upper - C_L,
    D <= (1/2) sum_b max(|inL-outU|, |inU-outL|) + R.

The resulting D upper bound is 0.01913123594185872978. The Poisson marking
coupling gives TV<=1-exp(-D). Its evaluation uses the inherited exact rational
alternating-series enclosure. The gap between M_upper and D_upper is NOT
reported as a lower bound on actual cancellation: it also reflects differences
between conservative upper enclosures. See ../boundary_transfers/README.md for
that distinction and ../paired_atoms/README.md for the coupling proof.

## Audit and remaining scope

- 48 exact rational Pythagorean-coordinate cases verify the expanded Q identity
  against direct Minkowski subtraction, including both time orientations and
  positive, zero and negative strip offsets.
- 32 archived complete-pattern cells supply 864 interior point checks using
  independent scalar causal membership under both geometries.
- 18,144 direct scalar quadratic values lie inside the corresponding enclosures.
- Cancellation is reconstructed from transfer lower bounds; unknown mass remains;
  uncertain bidirectional upper bounds alone do not create a cancellation claim.
- The spatial rectangles match PR103, and its localization upper bounds are
  retained at every grid level.

The point checks audit the implementation; rational interval algebra establishes
whole-cell coverage. These are not external peer review or empirical confidence
intervals. The fixed three-grid experiment stops here. At level 64, the largest
remaining surface-test ambiguity counts involve intervals (5,0), (3,1), (2,1),
(5,1), (3,0); these are internal node indices and overlapping cell counts, not
independent error contributions. A subsequent experiment should refine only
unresolved surface cells under a fixed area/intensity budget, with all known
certificates retained, before enlarging the geometry search.

## Reproduction

```sh
python3 -B research/lorentz_local_dalembert/surface_correlations/sf_run.py --verify
python3 -B research/lorentz_local_dalembert/surface_correlations/sf_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/surface_correlations/SHA256SUMS
```

Run from the repository root. Frozen sources, contract, complete transfer tables,
cell witnesses, summary and audit are included. The freeze is reproducibility
metadata, not a claim of external preregistration.
