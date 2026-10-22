# Eigenzeit: finite-count accuracy and operator sensitivity

SPDX-License-Identifier: Apache-2.0

**22 October 2026 — certified bounded-error ambiguity; scientific HOLD remains.**

Two explicit geometries satisfy exactly the same order on 21 selected nodes
and have close expected interval counts, yet their discrete operator weights
differ by **14.82128499%** in symmetric relative l2 norm. Both also fit the
same actual archived count vector within the declared deterministic error set.
This gives an algorithm-independent **7.41064249% worst-case relative lower
bound for recovery of these weights in that set**. It is not a statistical
error probability or a bound for every continuum operator.

The frozen search's strong threshold was **25%**, and was **not met**. The
14.82% pair was selected afterwards as the strongest smaller diagnostic pair.
No threshold, source set, search budget or acceptance gate was relaxed. No
estimator is adopted and no previous scientific HOLD is lifted.

## Concrete pair and exact certificate

The witness is source cloud 09, fixed objective direction 0, sign +1, trial 1
(zero based), using the candidate B0 data from PR87. There are four landmarks,
one root and 16 supports, with 74 used interval counts. The same density 32768,
scale, node labels, empirical covariance metric and order are held fixed.

| Quantity | Certified result |
|---|---:|
| Order at both endpoints | All 210 unordered pairs match, with causal direction |
| Moment rank at both endpoints | Exactly 9 |
| Symmetric relative weight separation | 0.14821284985504466458–0.14821284985504466459 |
| Absolute l2 weight separation | 166.58639188155717442466–166.58639188155717442467 |
| Squared mean-pair discrepancy | 1.69350242016–1.69350242642, required <4 |
| Squared discrepancies from actual N | 11.686608810–11.686608821 and 13.617983904–13.617983917, required <74 |
| Largest marginal mean shift / sqrt(N_i) | <0.399615711 |
| Relative minimax lower bound for weights | >7.41064249% |
| Strong search threshold | 25%; not reached |

The norm uses **C_alpha=(19 C+diag(N))/20**, including empirical count overlaps.
The table's marginal shifts alone are not a joint uncertainty criterion; the
full fixed-matrix discrepancy is also checked. This metric is a declared
bounded-error model, **not a calibrated confidence region**. In particular,
sqrt(N_i) here is a plug-in marginal scale, not the unknown true standard
deviation. The original A/B poset and the geometry-dependent distribution of
the observed overlaps are outside this model.

[witness.json](witness.json) supplies exact decimal coordinates, integer N/C,
labels, scale, order and counted pairs. [certificate.json](certificate.json)
contains directed rational enclosures. [st_certificate.py](st_certificate.py)
recomputes exact order signs, unique moment weights, rank, original intrinsic
moment equations, and rigorous upper bounds below the inherited 1e5 condition
cutoffs. The exact landmark condition bounds are <347 and the intrinsic moment
condition bounds <18,624. A nonzero triangular landmark determinant proves
Lorentz signature. See [CERTIFICATE.md](CERTIFICATE.md) for the proof machinery.

There is also one fixed, postselected bounded nodal field f_i=sign(w1_i-w0_i)
with response separation **588.0585241522** in the existing operator units.
That field can oscillate and is **not a smooth-field counterexample**. The l2
weight separation equals the maximum response separation over unit-l2 nodal
fields. Neither statement establishes continuum truncation error.

## Complete search outcome and its limitations

The [frozen protocol](PROTOCOL.md) used all 20 selected archived PR87 B0 cases;
there were no fresh A/B clouds. Nineteen supplied qualified full-GLS feasibility
seeds; cloud 03 failed the existing count gate. This use does not adopt the
previously rejected full-GLS accuracy candidate.

Four fixed signed objectives per seed gave 76 trials. There were 49 verified
smaller pairs on 15 clouds and 27 trials without a qualified pair. **All 76
optimizers returned unsuccessful termination:** 42 positive directional
derivative exits, 28 iteration limits and six incompatible-inequality exits.
No per-objective timer fired. The 105.57-second campaign stayed within its
fixed budget; backtracked, rounded candidate points were independently checked
regardless of solver status. Their existence does not require convergence,
but the search supplies **no global optimum or upper bound**. In particular,
14.82% is the largest found separation, not the largest possible separation.

All 19 count Jacobians had full numerical gauge rank. Their unconstrained
local relative operator gains ranged from 0.10233 to 0.26952 per unit whitened
mean perturbation (median 0.18101). These are tangent sensitivities. Causal
constraints restrict feasible directions, and nonlinear finite changes can
differ. These numbers are not confidence intervals or finite-radius bounds.

The six synthetic controls pass. [audit.json](audit.json) records every case,
all 49 numerical pair rechecks, count/weight derivatives and the exact witness
verification. [execution.json](execution.json), [search.log](search.log) and
the 20 [result records](results/) include failures. [freeze.json](freeze.json)
pins source inputs and pre-search code; it is a local diagnostic freeze on
known data, not public preregistration. Certification/report code was added
after the search and is plainly separated from the frozen search code.

## What follows mathematically

[THEORY.md](THEORY.md) proves noiseless reconstruction with nondegenerate four
landmarks, derives the error-amplification identities, and proves the
two-point lower bound. Positive counted intervals and full moment rank also
give pointwise local continuity. The unresolved issue is a useful uniform
finite-error bound over the admitted configurations.

For any estimate based on this same bounded-error summary,

\[
\max_{i=0,1}\frac{\|\widehat w-w_i\|_2}{\|w_i\|_2}
\ge \frac{\|w_1-w_0\|_2}{\|w_0\|_2+\|w_1\|_2}
>0.0741064249.
\]

This rules out a uniform guarantee below that level in this model. It does
**not** rule out a 10% target, establish a failure probability in the actual
experiment, or prove that improving an existing solver is useless. Absence of
a >=25% pair also does not establish stability.

The next mathematical decisions should be:

1. Define the desired accuracy for the intended smooth-field/continuum target,
   including discretization bias; weight error and scalar response error are
   different targets.
2. Derive or certify finite-radius upper/lower bounds on the actual admissible
   geometry set, with explicit landmark and moment conditioning and causal
   margins. A better search alone is not an upper-bound proof.
3. Connect that set to the joint count/overlap observation law and selection,
   using justified coverage or testing bounds. If the resulting lower bound
   exceeds the target, change the information model or geometry selection;
   additional optimizer starts cannot remove that information limit.

These are analytic/model-design tasks before another broad accuracy campaign.

## Reproduction and independent algebra

Python 3.12, with pinned NumPy/SciPy in [requirements.txt](requirements.txt):

```sh
python -m pip install -r research/lorentz_local_dalembert/stability_information/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/lorentz_local_dalembert/stability_information/st_audit.py
OPENBLAS_NUM_THREADS=1 python -B research/lorentz_local_dalembert/stability_information/st_certificate.py
```

The audit takes about one second locally; it validates archived search outputs
and reruns the rational certificate, without launching optimization. For a new
execution of the frozen search, use a disposable checkout, remove only this
package's `results/`, `execution.json` and `search.log`, and run `st_search.py`
with both thread variables set to one. Keep the archived outputs elsewhere.
Wall-time limits and nonconvex solves are not bitwise portable. A rerun is a
separate execution, not a replacement for the published record.

[crosscheck_reduced.wl](crosscheck_reduced.wl) and its [raw result](crosscheck_reduced_result.json)
record an independent Wolfram calculation: exact selected-node orders and Gram
identity, analytic count derivative, 40-digit agreement on both weight norms
and bounded-field gap, and the two-point inequality. Wolfram emitted undefined
local-symbol H warnings but returned the agreeing values; those warnings are
retained. The earlier full-matrix request returned an internal service error
and is retained as [failed evidence](crosscheck_full_attempt.json), with its
[input](crosscheck.wl). It did not verify the covariance calculation. The
rigorous covariance bounds are checked by the rational Python certificate.

All files are inventoried by [SHA256SUMS](SHA256SUMS). External background
sources and their limited role are listed in [THEORY.md](THEORY.md).
