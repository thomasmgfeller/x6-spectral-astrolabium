# Conformal reference-point scan

SPDX-License-Identifier: Apache-2.0

## Question and result

PR97 excludes the strong fixed-base gap only near its original reference. Does
moving the reference along the same conformal family reveal stronger response?
The contract fixes nine bases a=-4/5,-3/5,...,4/5 and two relative steps
δ=±9/5000, giving 18 pairs. This is a finite search, not a continuous theorem.

Six pairs pass all inherited separation, intrinsic moment, conditioning and TV
gates. The selected base a=2/5 and endpoint b=1435/3574 have symmetric relative
weight gap in [0.00226508548492395679,0.00226508548492395680], i.e.
**0.22650855%**, with **TV <=0.248424353**. This is below the >20% gate for
disjoint relative 10% weight-error balls. No strong pair was found.

All 18 pairs preserve exact causal order; all pass the TV gate. Only bases
0,1/5,2/5 pass every admissibility gate. The other six bases fail the existing
minimum-separation margin; -4/5 and -3/5 also fail the intrinsic gate. Their
computed gaps and derivatives remain in the records but are not eligible.
No threshold was relaxed to include them. A failed sufficient conditioning
bound is not itself proof of actual ill-conditioning.

## Why the transport bound transfers

Write z(a)=T_a(z(0)). The exact diamond-preserving group law gives

    T_δ(z(a)) = z(b),   b=(a+δ)/(1+aδ),
    δ=(b-a)/(1-ab),    atanh(b)-atanh(a)=atanh(δ).

The two hypotheses are homogeneous Poisson models at the SAME known density
on the SAME physical domain, with selected interval endpoints z(a) and z(b).
Pull back the second model by T_δ inside the fixed outer diamond, leaving the
outside unchanged. The interval observation map then agrees with the first
one. PR96's Poisson transport proof applies with δ rather than b-a:

    TV <= sqrt((9/10) U) |atanh(δ)|,

where U is expected population of the unchanged outer diamond. Its coefficient
does not depend on the internal endpoint configuration. Thus changing a needs
no additional TV charge: each comparison concerns z(a) versus z(b), not either
one versus z(0). This argument retains the complete dependence of counts and
overlaps. It does not assume independent interval counts.

## Verification and reproducibility

`rs_run.py` uses rational coordinates, exact weights, analytic rational dual
 derivatives and outward rational square-root/log bounds inherited from PR96/97.
Every pair checks the full coordinate group law, conformal interval identities,
causal order, separation margin and intrinsic gates. At all nine bases the
weight solution in the rational boosted frame agrees exactly with the original
frame solution. Local derivatives describe relative δ at zero, not the global
coordinate a and not a uniform sensitivity bound.

`rs_audit.py` supplies 180 independent scalar null-coordinate composition and
inverse checks, verifies complete grid enumeration and selection, and exactly
reproduces the archived zero-base gap and derivative from PR96/97.

From repository root:

```sh
OPENBLAS_NUM_THREADS=1 python3 -B research/lorentz_local_dalembert/reference_scan/rs_run.py --verify
python3 -B research/lorentz_local_dalembert/reference_scan/rs_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/reference_scan/SHA256SUMS
python3 tests/python/verify_manifest.py
```

Contract and code were hashed before the first search. This local freeze is
reproducibility evidence, not external preregistration. Full replay is included
in the dedicated GitHub Actions job. No Monte Carlo or adaptive grid expansion.

## Decision and limits

Stop this 18-pair experiment. Neither its finite negative result nor PR97
excludes arbitrary nonzero pairs, unsampled references, other conformal
parameters or actual-TV-close pairs outside the sufficient upper certificate.
There is no global stability result or uniform 10% estimator guarantee.
All earlier scientific HOLDs remain. This is a conditional selected-node count
experiment; no A-selection likelihood, full B causal-matrix inference,
continuum accuracy or physical validation is claimed.

Next useful research target: nonconformal coordinated shape directions with
an explicit full-channel information bound, rather than adding points to this
same grid. Any new family needs a separately justified transport bound before
weight amplification can constitute a statistical counterexample.

Derivations and source attribution: [PR96 transport proof](../conformal_transport/THEORY.md)
and [PR97 sensitivity proof](../conformal_sensitivity/THEORY.md).
