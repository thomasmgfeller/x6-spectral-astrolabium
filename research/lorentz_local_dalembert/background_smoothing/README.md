# Common positive background: certified, but no additional smoothing gain

SPDX-License-Identifier: Apache-2.0

**HOLD_BACKGROUND_SMOOTHING.** All **158** labels involved in the PR105 transfer
table now have a certified positive common diagonal intensity. Previously only
10 could be certified from the inherited atom-volume bounds. The fixed local
search checks 1,036 boxes and certifies 880; taking the largest valid box for each
of the 148 previously unsupported labels proves complete background coverage.

This does **not** improve the best TV upper bound:
**0.01706315569576179848 remains unchanged**. Common positivity is qualitatively
useful, but the available lower-volume certificates are too small to make this
Hellinger bound competitive. This is not evidence that the true common volumes
are small or that every possible smoothing method must fail.

| Certificate for the known-transfer component | TV upper bound |
|---|---:|
| Hellinger, inherited diagonal lower bounds | 0.12677627261281013671 |
| Hellinger, added certified common boxes | 0.11299896624912544976 |
| Existing balanced Poisson coupling | 0.01070565078593052008 |

The unresolved transfer-mean upper bound remains 0.00644704023662276662 and is
retained in the full-law calculation. Combining it with the best known-component
bound reproduces PR105 exactly. The geometry and tiny symmetric operator gap
(about 0.00365762%) are unchanged; no reconstruction-accuracy improvement, strong
pair, global stability statement or physical claim is made.

## Convert marginal information to actual common background

Let m_b be the Poisson intensity of the region with label b under BOTH geometries.
Let out_b/in_b be the known off-diagonal transfer intensities, and let unknown
outgoing/incoming intensity have total at most R. Then

    lambda_b = m_b + out_b + unknown_out_b,
    mu_b     = m_b + in_b  + unknown_in_b.

The separate PR100 atom-volume lower bounds a_b<=lambda_b and c_b<=mu_b do NOT
directly certify common spatial volume. However,

    m_b >= max(0, a_b-outU_b-R, c_b-inU_b-R).

This deduction is valid even if the separate atom regions do not overlap.
The audit includes a control that would fail if marginal lower volumes were
silently treated as common diagonal intensity.

## Fixed local box certificate

For each unsupported label, choose its incident certified transfer leaf with
largest lower intensity; ties use the lexicographic cell ID. Take its spatial
center and move time to the required common side of both moving cone boundaries.
Offsets are exactly h times [2,8,32,128,512,2048,8192]. The proposed cube has
half-width offset/8. Cube and tip coordinates are enclosed outward on the
inherited 2^-18 grid.

The unchanged PR100 whole-box cone classifier must assign the SAME complete
90-bit target label under BOTH geometries. Such a cube lies in the actual common
diagonal region; its intensity rho*scale^3*integer_volume/unit^3 is exact. Since
the outer interval is one of the bits, nonzero certified target cubes also lie
inside the fixed observation diamond. A candidate crossing any relevant boundary
is rejected. No label is accepted by sampling alone.

For each label use the maximum of the inherited diagonal lower bound and all
certified cube intensities. **Do not sum possibly overlapping cubes.** The code
records every accepted box, its source transfer cell and multiplier. It does not
extend the fixed offset list after inspecting results.

## Smoothing while preserving unresolved transfers

Choose a set S of known directed transfers. All omitted transfers and all
unresolved transfers form an independent Poisson residual with mean at most

    B = R + sum of omitted transfer upper intensities.

The retained component has atom means m_b+outS_b and m_b+inS_b. Let

    dU_b = max(|inL_b-outU_b|, |inU_b-outL_b|),
    L0_b = mL_b+outL_b,  L1_b = mL_b+inL_b.

The squared root-intensity difference is bounded termwise by

    J_b <= min(dU_b, dU_b^2/(sqrt(L0_b)+sqrt(L1_b))^2).

When the denominator vanishes, retain the linear bound dU_b. Root denominator
bounds are rounded downward and J contributions upward. With J_U=sum J_b,
Poisson affinity gives TV_known<=sqrt(1-exp(-J_U)). The same component also has
the balanced coupling bound TV_known<=1-exp(-sum dU_b/2). Take the smaller
certified bound kappa.

Couple the residual via a common Poisson event total and the appropriate marks
for each geometry. If no residual event occurs, the retained-component coupling
suffices. The full observation law therefore obeys

    TV_full <= 1-exp(-B)*(1-kappa).

The increasing expression is evaluated at B's upper bound with rational
exponential enclosures. This retains all dependencies between interval and
overlap counts, including unseen labels in the residual. The optional outside
count remains common as in PR95. No assumption of independent interval counts
is introduced.

The three fixed variants are: all known transfers with inherited background;
all known transfers with certified local boxes; and only edges with positive
background at both endpoints, with the others sent to the residual. After the
local certificates all 88 edges qualify, so the latter two variants coincide.
All variants also retain their balanced coupling fallback and the PR105 bound.

## Quantified limitation and stopping decision

The local-box Hellinger calculation has J_U=0.01285098773078545516. A sufficient
sqrt(J) target to match the known-component coupling bound is approximately
0.00011461095875029476 for J, about 112 times smaller. This is only a sufficient
certificate target: it is not a necessary condition, a required multiplier of
physical density, or a lower bound on actual TV.

Available diagonal lower certificates range from about 1.25e-9 to 546.42.
These are lower bounds, not measurements of the actual regional intensities.
The largest J contributions and their labels are listed in diagnostics.json,
so subsequent work can target demonstrably weak certificates rather than assuming
that mere positivity is enough.

Stop this fixed box search. It establishes complete positive-background coverage
but does not pass the additional-gain gate. Further numerical enlargement should
first justify a feasible route to substantially stronger background lower bounds.
The central stability question still requires a much larger operator separation
at statistically close laws, not just a progressively smaller TV certificate
for this same tiny deformation.

## Validation and reproduction

The independent audit checks corners and centers of the largest certified common
box for each of the 148 new labels under both geometries: **2,664 exact scalar
membership checks**. It verifies exact integer volumes and maximum-only
aggregation. Controls cover the marginal-to-diagonal deduction, a positive
smoothing example, retained unknown mass, residual composition and invalid input.
Point checks audit implementation; whole-cell interval inequalities provide the
coverage proof. No external peer review is implied.

```sh
python3 -B research/lorentz_local_dalembert/background_smoothing/bs_run.py --verify
python3 -B research/lorentz_local_dalembert/background_smoothing/bs_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/background_smoothing/SHA256SUMS
```

Run from the repository root. The contract, source/input freeze, box certificates,
method bounds, diagnostics, summary and audit are archived for reproduction.
