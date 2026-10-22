# Eigenzeit: sensitivity and a continuous stopping certificate

SPDX-License-Identifier: Apache-2.0

**The strong fixed-base separation gate is excluded throughout the current
certificate-covered PR96 flow. All scientific HOLDs remain.**

This replaces a finite grid result with a verified continuous interval result.
It compares the original reference geometry with its one-parameter conformal
flow; it does not compare arbitrary pairs of nonzero parameters. Inner landmarks
and root move, while outer endpoints and known density remain fixed.

| Quantity | Certified value |
|---|---:|
| Exact local relative weight speed | 0.8725160193 |
| Local transport upper-certificate speed | 138.0133804 |
| Ratio of those speeds | 0.006321967 |
| Verified parameter interval | [-0.002,0.002] |
| Cells in the completed continuous cover | 256 |
| Uniform fixed-base relative gap upper | 15.39595111% |
| Uniform symmetric relative gap upper | 16.67997122% |
| Gate needed for disjoint relative 10% error balls | >20% |

**The 16.68% number is a conservative upper bound, not an observed increase.**
The previous sampled gaps were around 0.16%. The exact local speed ratio alone
would not justify extrapolation; the separate interval certificate supports
the stopping decision. The archived uniform derivative enclosure is loose
and is not presented as a sharp sensitivity estimate.

The current transport upper-certificate gate implies membership in this interval.
Actual TV<=1/4 need not: the certificate is sufficient, not necessary. Therefore
we stop expanding this fixed-reference search under the same certificate, while
leaving other geometry directions, reference points and sharper law bounds open.
No general stability result or 10% reconstruction guarantee follows.

See [proof and scope](THEORY.md), [contract](contract.json),
[summary](summary.json), [local derivative](local.json),
[covering cells](cells.json), [independent audit](audit.json), and the
[recorded initial enclosure failure](initial_attempt.json).

## Reproduce

From the repository root:

```sh
python -m pip install -r research/lorentz_local_dalembert/finite_poisson_bounds/requirements.txt
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/conformal_sensitivity/cs_run.py
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/conformal_sensitivity/cs_audit.py --verify
sha256sum -c research/lorentz_local_dalembert/conformal_sensitivity/SHA256SUMS
```

All linear preconditioners are archived as rational proposals in compressed JSON.
Replay validates their residual contractions using outward integer intervals.
It does not regenerate floating-point inverse proposals. The 64- and 128-cell
attempts are retained; the first successful cover has 256 cells. A previous
natural interval form failed and was replaced by a centered mean-value form,
without changing the parameter range or maximum partition budget.

The observation contract and target remain those of PR96: conditional finite
count/overlap/optional-total data and discrete quadratic moment weights. No
physical validation, full B causal-matrix inference, A-selection likelihood,
smooth-field accuracy or global impossibility claim is made.

## CI portability repair

A separately triggered legacy replay failed a raw coordinate hash across CPU
dispatch paths. Complete verification coordinate fixtures now match the original
published raw hashes exactly; fresh coordinates are checked point by point at
2^-50 absolute tolerance while relations, interval bits, integer measurements and
scientific gates remain exact. Native and AVX512-disabled full replays pass. See
[diagnosis and evidence](../eligibility_before_cap/coordinate_fixtures/README.md).
The new interval certificate and original scientific evidence are unchanged.
