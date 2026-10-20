# V1 — Mathematical Validation of the Minkowski-Diamond Sampler

**Project:** X6 Spectral Astrolabium — Proper-Time Laboratory

**Validation ID:** `V1_SAMPLING_GEOMETRY`

**Status:** **PASS**

**Residual gate:** `V1b_FINITE_IMPLEMENTATION_REGRESSION = OPEN`

**Applies to:** `research/lorentz_proper_time_lab`

**Validated object:** the idealized sampling transformation corresponding to `cloud()`, with exact independent Gaussian directions

**Model scope:** normalized flat Minkowski spacetime, dimensions $d\in\{2,3,4\}$, fixed sample size $m$, externally supplied scale $T$


---

## 1. Decision

The idealized transformation corresponding to `cloud()` is mathematically measure-correct when its uniforms are independent and its angular inputs are exact independent standard Gaussians. This is a theorem about that ideal model, not exact distributional equivalence of the finite implementation. It generates a constant-density sample with respect to the ordinary $d$-dimensional volume measure on the normalized Alexandrov interval

$$
D=\left\{(t,\mathbf{x})\in\mathbb{R}\times\mathbb{R}^{d-1}: |t|+\|\mathbf{x}\|<\frac12\right\}.
$$

For the concentric inner interval

$$
D_\theta=\left\{(t,\mathbf{x}): |t|+\|\mathbf{x}\|<\frac{\theta}{2}\right\},
\qquad 0<\theta<1,
$$

the induced inclusion probability is

$$
\Pr\{(t,\mathbf{x})\in D_\theta\}=\theta^d.
$$

Consequently, for $m$ independent sampled points,

$$
K\sim\operatorname{Binomial}(m,\theta^d).
$$

This validates the geometric sampling law on which the demonstrator's count-based proper-time estimator is built. It does **not** by itself validate the finite pseudo-random generator, floating-point implementation, confidence-interval implementation, estimator coverage, physical interpretation, or applicability outside the declared flat model.

---

## 2. Code under review

The geometric construction, after replacing `normal(random)` by an exact Gaussian draw and excluding zero-probability ideal boundary events, is:

```javascript
const A = 0.5 * random() ** (1 / d);
const t = (random() < 0.5 ? -1 : 1) * (0.5 - A);

const v = Array.from({ length: d - 1 }, () => normal(random));
const norm = Math.hypot(...v);

const r = A * random() ** (1 / (d - 1));
const point = [t, ...v.map(x => x * r / norm)];
```

Membership in the inner interval is tested by:

```javascript
Math.abs(t) + Math.hypot(...point.slice(1)) < theta / 2
```

The mathematical proof below treats the uniform draws as independent $U(0,1)$ variables and **replaces** `normal(random)` by independent exact standard normals, independent of those uniforms. This replacement is substantive: the actual normal transform is

```javascript
function normal(random) {
  const u = Math.max(0.5 / 4294967296, random());
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * random());
}
```

Its positive lower clamp changes the Gaussian law even if `random()` were continuous uniform. For the actual finite generator, zero is a possible output; the same zero can also give `A = 0` in `cloud()`, placing a point on an outer tip. The exact finite frequencies, dependence, angular discrepancies and floating-point effects belong to V1b. V1 does not silently identify this guarded transform with exact Gaussian sampling.

### Reviewed source pin

The code review uses repository commit `206e5e81691ccd46ce2614cdbb66fd27a8468228`:

| File | SHA-256 |
|---|---|
| `research/lorentz_proper_time_lab/core.js` | `5694637b2387bee6831008c53e86e1427bab341f4170648af8656181aee62795` |
| `app/proper-time.html` | `25ac6f50beb7bd602606a1a0be486d7339d01bbeabf4917728bebd594e69020e` |

`core.js` is the maintained numerical source. `build.py --check` confirms that the standalone HTML contains the expected assembled sources at this pin; this build check does not close V1b. No sampler or PRNG code was changed for this proof.

The supplied draft `V1_sampling_geometry.md` had SHA-256
`8448eb5ead28e6e658a785f67304774eedf6d4d61fe24584adf62b4e054b5d5d`.
This repository edition corrects the one-spatial-dimension radius statement, makes the ideal/guarded-normal distinction explicit, and records source provenance.

---

## 3. Definitions and assumptions

Let:

- $d\ge 2$ be the total spacetime dimension;
- $n=d-1$ be the number of spatial dimensions;
- $t\in\mathbb R$ be the time coordinate;
- $\mathbf{x}\in\mathbb R^n$ be the spatial vector;
- $\|\mathbf{x}\|$ be its Euclidean norm;
- $\omega_n$ be the volume of the unit $n$-ball;
- $U_1,U_2\sim U(0,1)$ be independent;
- $S\in\{-1,+1\}$ be independent with equal probabilities;
- $\mathbf N=(N_1,\ldots,N_n)$, with independent $N_i\sim N(0,1)$.

All of $U_1,U_2,S,N_1,\ldots,N_n$ are mutually independent, and a fresh independent set is used for every point. The ideal sampler can be written as

$$
A=\frac12 U_1^{1/d},
\qquad
T_c=S\left(\frac12-A\right),
$$

$$
R=A U_2^{1/n},
\qquad
\Omega=\frac{\mathbf N}{\|\mathbf N\|},
\qquad
\mathbf X=R\Omega.
$$

Here $T_c$ denotes the sampled time coordinate and must not be confused with the external scale $T$ used by the estimator.

---

## 4. Geometry of the target interval

At a fixed time $t$, the spatial section of $D$ is the $n$-ball

$$
B_n(A(t))=\{\mathbf{x}:\|\mathbf{x}\|<A(t)\},
\qquad
A(t)=\frac12-|t|.
$$

Its volume is

$$
\operatorname{Vol}_n(B_n(A(t)))=\omega_n A(t)^n
=\omega_{d-1}\left(\frac12-|t|\right)^{d-1}.
$$

A point uniform in the full interval cannot have a uniform time coordinate. Values near $t=0$ must occur more often because the spatial cross-section is larger there. The required marginal time density is proportional to $A(t)^{d-1}$.

---

## 5. Distribution of the cross-section radius $A$

For $0\le a\le 1/2$,

$$
\begin{aligned}
F_A(a)
&=\Pr\left(\frac12 U_1^{1/d}\le a\right)\\
&=\Pr\left(U_1\le (2a)^d\right)\\
&=(2a)^d.
\end{aligned}
$$

Therefore,

$$
f_A(a)=\frac{d}{da}F_A(a)=d\,2^d a^{d-1}.
$$

Thus the probability assigned to a cross-section is proportional to its spatial volume factor $a^{d-1}$.

**Sub-result:** PASS.

---

## 6. Marginal distribution of the time coordinate

Because

$$
T_c=S\left(\frac12-A\right),
$$

we have

$$
A=\frac12-|T_c|.
$$

Each sign is selected with probability $1/2$, hence, for $|t|<1/2$,

$$
\begin{aligned}
f_{T_c}(t)
&=\frac12 f_A\left(\frac12-|t|\right)\\
&=d\,2^{d-1}\left(\frac12-|t|\right)^{d-1}.
\end{aligned}
$$

This is exactly proportional to the volume of the spatial cross-section at time $t$.

Normalization follows directly:

$$
2\int_0^{1/2}d\,2^{d-1}\left(\frac12-t\right)^{d-1}\,dt=1.
$$

**Sub-result:** PASS.

---

## 7. Conditional radial distribution

Conditioned on $A=a$, the code sets

$$
R=aU_2^{1/n}, \qquad n=d-1.
$$

For $0\le r\le a$,

$$
\begin{aligned}
\Pr(R\le r\mid A=a)
&=\Pr\left(U_2^{1/n}\le\frac ra\right)\\
&=\Pr\left(U_2\le\left(\frac ra\right)^n\right)\\
&=\left(\frac ra\right)^n.
\end{aligned}
$$

Differentiation gives

$$
f_{R\mid A}(r\mid a)=\frac{n r^{n-1}}{a^n}
=\frac{(d-1)r^{d-2}}{a^{d-1}}.
$$

This is the radial density produced by uniform volume sampling in an $n$-ball. For $n>1$ ($d>2$), drawing the radius uniformly would be incorrect. For $n=1$ ($d=2$), the required exponent is 1 and the radius is indeed uniform on $[0,a]$.

**Sub-result:** PASS.

---

## 8. Angular distribution

The vector $\mathbf N$ has a rotationally invariant multivariate standard-normal distribution. Therefore its normalized direction

$$
\Omega=\frac{\mathbf N}{\|\mathbf N\|}
$$

is uniform on the unit sphere $S^{n-1}=S^{d-2}$. The Gaussian direction is independent of its Gaussian norm by rotational invariance. Its independence from the separately generated spatial radius $R$ follows from the mutual independence assumed in Section 3. For $n=1$, $S^0=\{-1,+1\}$ consists of two equally likely signs; no continuous angular coordinate is needed.

Under the ideal continuous model,

$$
\Pr(\|\mathbf N\|=0)=0.
$$

The implementation's `if (!norm)` branch guards a case of probability zero in the ideal Gaussian model. Its behavior under the actual PRNG and arithmetic remains an implementation question; the ideal theorem alone does not prove that the branch is unreachable.

**Sub-result:** PASS under the ideal Gaussian-input assumption.

---

## 9. Constant joint density

Conditioned on $T_c=t$, $\mathbf X$ is uniform in the spatial ball of radius

$$
a=\frac12-|t|.
$$

Thus

$$
f_{\mathbf X\mid T_c}(\mathbf{x}\mid t)
=
\frac{1}{\omega_{d-1}a^{d-1}}
$$

for $\|\mathbf{x}\|<a$, and zero otherwise. Multiplying by the time density gives

$$
\begin{aligned}
f_{T_c,\mathbf X}(t,\mathbf{x})
&=f_{T_c}(t)f_{\mathbf X\mid T_c}(\mathbf{x}\mid t)\\
&=d2^{d-1}a^{d-1}
  \frac{1}{\omega_{d-1}a^{d-1}}\\
&=\frac{d2^{d-1}}{\omega_{d-1}}.
\end{aligned}
$$

The result is constant over $D$. Therefore the transformation generates uniform volume density on the target interval.

---

## 10. Independent normalization check

The volume of $D$ is

$$
\begin{aligned}
\operatorname{Vol}_d(D)
&=2\int_0^{1/2}
\omega_{d-1}\left(\frac12-t\right)^{d-1}\,dt\\
&=2\omega_{d-1}\int_0^{1/2}a^{d-1}\,da\\
&=\frac{\omega_{d-1}}{d2^{d-1}}.
\end{aligned}
$$

Consequently,

$$
\frac{1}{\operatorname{Vol}_d(D)}
=\frac{d2^{d-1}}{\omega_{d-1}},
$$

which agrees exactly with the joint density derived above.

**Sub-result:** PASS.

---

## 11. Inner-volume law

The inner interval $D_\theta$ is obtained by scaling all $d$ coordinates of $D$ by $\theta$. Its volume therefore satisfies

$$
\operatorname{Vol}_d(D_\theta)
=\theta^d\operatorname{Vol}_d(D).
$$

Since the outer sample is uniform,

$$
\Pr\{(T_c,\mathbf X)\in D_\theta\}
=
\frac{\operatorname{Vol}_d(D_\theta)}
     {\operatorname{Vol}_d(D)}
=\theta^d.
$$

The code's membership predicate

```javascript
Math.abs(t) + Math.hypot(...p.slice(1)) < theta / 2
```

matches this definition. The distinction between `<` and `<=` concerns only the boundary, which has zero volume in the ideal continuous model.

For independent points, the indicators

$$
I_i=\mathbf 1\{(T_{c,i},\mathbf X_i)\in D_\theta\}
$$

are Bernoulli variables with probability $\theta^d$. Hence

$$
K=\sum_{i=1}^m I_i
\sim\operatorname{Binomial}(m,\theta^d).
$$

**Sub-result:** PASS under ideal independent inputs.

A fixed number of independent uniform-volume points is the conditional law of a homogeneous Poisson process given its total count $m$. It is not the unconditioned Poisson experiment: V1 proves the binomial count law at fixed budget, not a physical Poisson intensity or a random total count.

---

## 12. Deterministic reference values

The following values are consequences of the proved model and may be used in V1b and later regression tests.

For $\theta=0.5$:

| $d$ | $p=\theta^d$ | $E[K]$ for $m=16\,384$ | $\operatorname{Var}(K)=mp(1-p)$ |
|---:|---:|---:|---:|
| 2 | 0.25 | 4096 | 3072 |
| 3 | 0.125 | 2048 | 1792 |
| 4 | 0.0625 | 1024 | 960 |

General identities:

$$
E[K]=m\theta^d,
\qquad
\operatorname{Var}(K)=m\theta^d(1-\theta^d),
$$

$$
\Pr(K=0)=(1-\theta^d)^m.
$$

These are reference expectations, not acceptance of any particular finite simulation result.

---

## 13. Gate result

```yaml
validation_id: V1_SAMPLING_GEOMETRY
status: PASS
evidence_type: analytical_proof
validated_object: idealized_transform_with_exact_independent_Gaussians
reviewed_source_commit: 206e5e81691ccd46ce2614cdbb66fd27a8468228
source_sha256:
  research/lorentz_proper_time_lab/core.js: 5694637b2387bee6831008c53e86e1427bab341f4170648af8656181aee62795
  app/proper-time.html: 25ac6f50beb7bd602606a1a0be486d7339d01bbeabf4917728bebd594e69020e
validated:
  - time-marginal transformation
  - conditional spatial radius
  - isotropic spatial direction under ideal Gaussian draws
  - constant joint volume density
  - inner-volume probability theta^d
  - induced fixed-budget binomial count law
scope:
  spacetime: flat Minkowski
  interval: normalized central Alexandrov interval
  dimensions: [2, 3, 4]
  sample_budget: fixed
  external_scale_T: assumed known
not_validated:
  - finite PRNG quality
  - bit-level reproducibility across runtimes
  - floating-point edge behavior
  - numerical normal-generator quality and lower-clamp discrepancy
  - implementation-level exact iid or Poisson behavior
  - Clopper-Pearson implementation
  - estimator bias and RMSE implementation
  - empirical or exact interval coverage established by this document
  - curved-spacetime applicability
  - physical discreteness of spacetime
  - Planck-scale interpretation
residual_gate:
  id: V1b_FINITE_IMPLEMENTATION_REGRESSION
  status: OPEN
```

---

## 14. Reproducibility record

A reproducible use of this validation should record at least:

1. repository URL;
2. exact Git commit SHA;
3. path and hash of the tested HTML/JavaScript file;
4. application schema/version, currently reported by the supplied code as `x6.proper-time-lab/1.0`;
5. browser name and exact version;
6. operating system and architecture;
7. JavaScript engine and version, where available;
8. dimension $d$, budget $m$, $\theta$, external scale $T$, confidence level and seed;
9. the exact PRNG and normal-transform source code;
10. raw generated results, not only plots or rounded labels;
11. the test script and its dependencies with fixed versions;
12. execution date in ISO 8601 format.

Suggested machine-readable record:

```json
{
  "validation_id": "V1_SAMPLING_GEOMETRY",
  "validation_status": "PASS",
  "evidence_type": "ANALYTICAL_PROOF",
  "record_kind": "V1B_EXECUTION_TEMPLATE_NOT_AN_EXECUTION_RESULT",
  "residual_gate": "V1b_FINITE_IMPLEMENTATION_REGRESSION",
  "residual_gate_status": "OPEN",
  "execution_status": "NOT_RUN",
  "repository": "https://github.com/thomasmgfeller/x6-spectral-astrolabium",
  "git_commit": "FILL_WITH_EXACT_SHA",
  "source_path": "app/proper-time.html",
  "source_sha256": "FILL_WITH_SHA256",
  "schema": "x6.proper-time-lab/1.0",
  "runtime": {
    "browser": "FILL_WITH_NAME_AND_VERSION",
    "javascript_engine": "FILL_IF_AVAILABLE",
    "operating_system": "FILL_WITH_OS_AND_ARCH"
  },
  "parameters": {
    "d": 4,
    "m": 16384,
    "theta": 0.5,
    "T": 1,
    "alpha": 0.05,
    "seed": 20261017
  },
  "expected": {
    "inside_probability": 0.0625,
    "mean_K": 1024,
    "variance_K": 960
  },
  "test_protocol_commit": "FILL_WITH_PRE_RESULT_PROTOCOL_SHA",
  "test_script_path": "FILL_WITH_TEST_SCRIPT_PATH",
  "test_script_sha256": "FILL_WITH_SHA256",
  "dependencies": "FILL_WITH_PINNED_LOCKFILE_AND_SHA256",
  "prng_and_normal_source_path": "research/lorentz_proper_time_lab/core.js",
  "prng_and_normal_source_sha256": "FILL_WITH_SHA256",
  "raw_data_path": "FILL_WITH_RAW_DATA_PATH",
  "raw_data_sha256": "FILL_WITH_SHA256",
  "execution_date": "FILL_WITH_ISO_8601_DATE"
}
```

The placeholders are deliberate: this is a future execution-record template, not evidence that V1b has run or passed. The concrete source pin reviewed for V1 is recorded separately in Section 2.

### Hashing example

From the repository root:

```bash
git rev-parse HEAD
sha256sum app/proper-time.html research/lorentz_proper_time_lab/core.js
```

The resulting digest should be copied into the record. A validation result without an exact commit and source hash is informative but not a frozen reproducibility artifact.

---

## 15. Required V1b follow-up

V1 proves the transformation in the ideal probability model. V1b should test the concrete implementation against that model. A finite discrepancy need not invalidate the theorem, but a mismatch in its assumptions or its claimed mapping to the code requires revising the applicability statement.

Existing `verify.py`, `browser_test.cjs` and `verification.json` already provide bounded implementation checks (including sampled support, time moments and inner counts). Those checks retain their own status; they are not retroactively relabelled as the more specific V1b below. Their sampled seeds and outputs are development evidence. The following list is a test-plan outline, **not yet a frozen numerical acceptance contract**. Before new V1b results are inspected, publish the exact grid, seed policy, thresholds, multiplicity rule and stopping rule.

Recommended minimum checks:

1. **Seed replay:** identical seeds and parameters produce byte-identical exported JSON in the same declared runtime.
2. **Reference vector:** freeze the first generated PRNG outputs for selected seeds, including `0`, `1`, `20261017`, and `4294967295`.
3. **Support:** all sampled points satisfy
   $$
   |t|+\|\mathbf{x}\|<1/2
   $$
   including targeted cases that force zero PRNG output, `A=0`, an extremely small normal input and a zero computed direction. A returned boundary point or nonfinite value must be counted and assessed under a predeclared policy; it must not disappear through silent replacement.
4. **Time marginal:** transform each sample to
   $$
   Z=(2A)^d=\left(1-2|t|\right)^d;
   $$
   under the ideal model, $Z\sim U(0,1)$.
5. **Conditional radial law:** for nonzero $A$, transform
   $$
   W=(R/A)^{d-1};
   $$
   under the ideal model, $W\sim U(0,1)$.
6. **Angular symmetry and independence:** verify sign balance, zero-centered coordinate moments, permutation symmetry and dependence between direction, time and radial transforms, using predeclared tolerances. Symmetry and a few moments alone do not establish a uniform angular law; include a suitable dimension-specific directional discrepancy check.
7. **Inner count:** regenerate full clouds (the UI repetition mode samples binomial counts directly and therefore cannot validate `cloud()` geometry). Compare observed $K$ across a predeclared seed set with the binomial law $\operatorname{Binomial}(m,\theta^d)$.
8. **No seed selection:** seeds, parameter grid, test statistics, tolerances and stopping rule must be fixed before viewing results.
9. **Failure diagnostics:** retain raw data and distinguish PRNG, transformation, normal-generation and floating-point failure modes.

With a fixed seed the program is deterministic; a finite family of seeds is not by itself proof of independent randomness or of PRNG suitability beyond the tested regimes. No single Monte Carlo run should be used as proof of uniformity. The analytical result in this document is the proof; V1b is an implementation regression and discrepancy-detection layer.

---

## 16. Interpretation limits

### Supported statement

> Under the declared flat-Minkowski, known-dimension, externally scaled and fixed-budget assumptions, the idealized `cloud()` transformation with independent exact Gaussian directions is mathematically consistent with uniform-volume sampling in the normalized Alexandrov interval. The concentric inner interval has probability mass $\theta^d$, yielding the stated binomial count model under ideal independent draws.

### Unsupported statements

V1 does not establish that:

- physical spacetime is fundamentally discrete;
- causal-set sprinkling is the unique physical model;
- the estimator is a physical clock;
- the longest chain is calibrated as proper time in this implementation;
- the result extends unchanged to curved spacetime;
- the external scale $T$ can be inferred from order alone;
- a Planck-scale interpretation has been measured;
- pseudo-random output is equivalent to physical randomness.

These exclusions are part of the validation result, not optional caveats.

---

## 17. Sources and provenance

### Project sources

- [X6 Research Hub](https://thomasmgfeller.github.io/x6-spectral-astrolabium/)
- [Proper-Time Laboratory README](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/206e5e81691ccd46ce2614cdbb66fd27a8468228/research/lorentz_proper_time_lab/README.md)
- [Proper-Time Demonstrator](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/proper-time.html)
- [Reproducible Jupyter notebook](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/206e5e81691ccd46ce2614cdbb66fd27a8468228/research/lorentz_proper_time_lab/eigenzeit.ipynb)
- [Proper-Time Domain Validity Contract](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/206e5e81691ccd46ce2614cdbb66fd27a8468228/research/lorentz_proper_time_domain/README.md)
- [Causal Orders — Time Domain](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/causal-orders.html#time-domain)

### External context

1. C. J. Fewster, E. Hawkins, C. Minz and K. Rejzner, “Local structure of sprinkled causal sets,” *Physical Review D* **103**, 086020 (2021). The paper explicitly studies finite causal sets sprinkled into Alexandrov subsets of Minkowski spacetime in dimensions $1+1$, $1+2$, and $1+3$, and reviews the sprinkling process. [DOI](https://doi.org/10.1103/PhysRevD.103.086020) · [arXiv](https://arxiv.org/abs/2011.02965)
2. Z.-Q. J. Lu, *Estimating Instrument Performance: with Confidence Intervals and Confidence Bounds*, NIST Technical Note 2119 (2020). This is relevant to later interval-validation gates; it includes treatment of the binomial model and a section on the Clopper–Pearson interval. [NIST Technical Note 2119](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.2119.pdf)
3. [NIST/SEMATECH e-Handbook: Confidence intervals for proportions](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm). This page describes Wilson intervals for proportions, not the Clopper–Pearson construction. It provides comparative statistical context only; it is not the source of the geometric V1 proof or a validation of the implemented interval routine.
4. [Mulberry32 reference implementation](https://github.com/cprosche/mulberry32). Its Version 3 JavaScript form documents the same integer-mixing structure and 32-bit state update as the demonstrator (apart from local naming and signed/unsigned storage). This is implementation provenance, not a benchmark endorsement. This reference does not establish suitability for every scientific simulation; that remains part of V1b.

### Source-use boundary

The PASS decision is derived directly from the displayed transformation by change-of-variables, conditional-volume and scaling arguments. External sources provide domain context and provenance; they are not substitutes for the proof. The Clopper–Pearson references are included for traceability to later validation gates and are not used to infer V1.

---

## 18. Review and change control

This file should be revised if any of the following changes:

- the definition of the outer or inner interval;
- the exponent in the draw of $A$;
- the exponent in the draw of $R$;
- the distribution or normalization of the angular vector;
- supported dimensions;
- the membership predicate;
- the interpretation of $\theta$, $T$, or $d$;
- the claim that the sample is uniform by spacetime volume.

Suggested commit message:

```text
validation: add V1 proof for Minkowski-diamond sampler
```

Suggested repository path:

```text
research/lorentz_proper_time_lab/validation/V1_sampling_geometry.md
```

---

## 19. Final sign-off

```text
V1_SAMPLING_GEOMETRY: PASS

Evidence type:
Analytical proof of the idealized geometric transformation corresponding to the pinned source.
The guarded normal generator and finite PRNG are not asserted to realize that ideal law exactly.

Confidence boundary:
PASS applies to the ideal measure transformation only.
Finite PRNG, clamped normal generation, floating-point and runtime behavior remain OPEN under V1b.
This PASS does not resolve embedding covariance or alter METADATA_HOLD / HOLD_PHASE3.
```
