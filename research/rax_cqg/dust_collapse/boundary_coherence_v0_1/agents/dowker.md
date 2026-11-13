# Dowker: two terminal matter records under the original action

## Choice frozen before the new Gaussian-moment calculation

Retain the original six histories, action, measures, preparation space, endpoint
density atoms, endpoint constant clock packets, and all old inner strata.
The original terminal packet is called `f0 = R_f`. Define

\[
x_+=(q_4+q_5)/\sqrt2,\qquad
f_2=\frac{2x_+^2-1}{\sqrt2}\,f_0.
\]

This is the first nonconstant *even* Hermite packet of the symmetric terminal
scalar mode, with the original unit Gaussian width. It is selected by lowest
degree, terminal permutation invariance, and global scalar parity, before
computing its amplitude; no center, width, coefficient, or detector phase is
fitted. The old packet is not replaced. The pair is a terminal **matter**
measurement, not a geometric measurement or a change to the action.

The check will compute its amplitude by a six-by-six Gaussian second moment,
reuse the old certified clock integrals, and report source hashes. It will not
perform a new clock quadrature or a search over packet choices.

Acceptance rules: exact orthonormality; invariance under both boundary label
permutations and global scalar sign; unchanged induced terminal order and clock
decoupling on terminal atoms; exact Gaussian-moment relation for every history;
finite-domain existence; and a contraction bound for the declared finite
instrument. Distinct matter outcomes must not be renamed radius or curvature.
Numerical physical claims remain ineligible unless a separate adapter is
derived. A new positive-density endpoint packet is outside this calculation.

## Executed result

**PASS_TWO_ORTHOGONAL_TERMINAL_MATTER_RECORDS.** The construction passes exact
normalization, symmetry, all-six-history Gaussian moment, rank, and finite
instrument contraction checks. It is not merely a proposal to look for an
observable later. `checks/r_records_results.json` contains reproducible exact
expressions and outward-rounded intervals. No new clock quadrature was run.

Under the original terminal scalar probability measure,
`q4,q5` are independent centered Gaussians with variance `1/2`. Thus

\[
\langle f_0,f_2\rangle=0,\qquad\|f_0\|=\|f_2\|=1.
\]

The endpoint density and quotient normalization factors are identical to the
old packet and cancel in this normalized scalar expectation. Both packets are
invariant under exchanging endpoint labels and under simultaneous scalar
reflection. On the kinematic terminal Hilbert space,
`P0=|f0><f0|`, `P2=|f2><f2|`, and `Pother=1-P0-P2` are a genuine PVM. This is a
mode-selective scalar matter measurement, not just a renamed class flag. A
physical detector interaction or a Hamiltonian whose energy eigenstates these
are has not been derived. The finite instrument below uses only the two
well-defined paired functionals on `E`; it does not assume a globally bounded
kernel or global `K†K`. Its completed Failure outcome is not identified with
the terminal projector `Pother`: it also incorporates the deliberately small
acceptance gain and whatever the finite accepted map does not resolve.

Set `D=diag(1,1,1,0,1,1)`, `Q_C=D-i beta H0_C`, and
`ell=(0,0,0,0,1,1)^T`. Gaussian source differentiation gives

\[
\frac{Z_C(J\ell)}{Z_C(0)}
 =\exp\!\left(\frac{J^2}{2}\ell^TQ_C^{-1}\ell\right),\qquad
a^{(2)}_{c,s}(g)=\eta_c a^{(0)}_{c,s}(g),\qquad
\eta_c=\frac{\ell^TQ_C^{-1}\ell-1}{\sqrt2}.
\]

The original Abel/Fresnel convention is retained. Polynomial times Gaussian
packets are Schwartz, and the already proved positive real damping after
boundary pairing remains intact. Consequently differentiation does not create
an additional convergence assumption. Because there is no direct scalar–dust
coupling, the formula holds for both inner strata and all `g` in `E` without
changing the old density or clock integrals. Every labelled history in a class
has the same multiplier:

\[
\begin{aligned}
\eta_1&=-\frac{64430531\sqrt2}{771663506}
        -i\frac{8175324\sqrt3}{385831753}
        \simeq-0.118080653112-0.036700132704i,\\
\eta_2&=-\frac{539495737\sqrt2}{10449188518}
        -i\frac{47339214\sqrt3}{5224594259}
        \simeq-0.073016405704-0.015693835688i.
\end{aligned}
\]

In particular `eta1 != eta2` exactly. The two classes therefore have linearly
independent terminal response vectors `(1,eta_c)`. For coherent class sums
`A_{r,s}=a^{(r)}_{1,s}+a^{(r)}_{2,s}`, the positive-stratum two-input/two-output
minor factors as

\[
\det\begin{pmatrix}A_{0,+}(g_0)&A_{0,+}(g_+)\\
                    A_{2,+}(g_0)&A_{2,+}(g_+)\end{pmatrix}
 =(\eta_2-\eta_1)
 [a^{(0)}_{1,+}(g_0)a^{(0)}_{2,+}(g_+)
  -a^{(0)}_{1,+}(g_+)a^{(0)}_{2,+}(g_0)].
\]

The bracket is the old certified nonzero minor. The new minor is enclosed by
`Re∈[-7.812823328,-7.812451007]×10^-9` and
`Im∈[-2.357821750,-2.357784517]×10^-8`; thus this finite input-to-terminal-matter
map has rank two. The inner-atom restriction remains rank one because the two
input preparations still multiply every class response by one common factor.
Rank two establishes independent amplitudes; numerical probability contrasts
are separately evaluated by the interference check rather than inferred from
rank alone.

## Instrument normalization fixed before these response values

`contracts/r_records.json` freezes `lambda_R=1/1024`, separately from the old
one-packet diagnostic gain `1/256`. The weighted output norms are exactly

\[
\|f_0\|_{V_R}^2=65,\quad\|f_2\|_{V_R}^2=799,\quad
\langle f_0,f_2\rangle_{V_R}=98\sqrt2.
\]

Using the inherited `C_star<3/5` and input weighted norm `2257/16`, the
four `r×s` direct-coherent-class-sum records obey the a priori bound

\[
\Big\|\sum_{r,s}M_{r,s}^{\dagger}M_{r,s}\Big\|
 \le \frac{2\cdot4(3/5)^2(2257/16)(65+799)}{1024^2}
 =0.3347479248046875<1.
\]

Here `M_{r,s}(g)=lambda_R A_{r,s}(g)|r,s>` and `r=0,2` labels terminal packets,
not geometry classes. Failure is recomputed as the positive square root of
the remaining effect on `E`. The old failure operator is not retained. The
same sufficient bound at the old gain exceeds one; this means that the old
bound no longer certifies contraction, not that the actual operator has been
proved noncontractive. There is no gain fitting to the small numerical
responses. The retained inner-stratum flag remains an auxiliary apparatus
assumption inherited from the pilot; the scalar terminal pair alone does not
justify its physical measurability.

## What is and is not available at the terminal boundary

The induced order on `R` is the same two-element antichain for all six
histories. Even the larger induced order on `P∪A∪R` agrees. Every observable
depending only on the induced terminal order is therefore constant on this
family. A past-inclusive invariant might distinguish classes, but would cease
to be an intrinsic `R`-order measurement; an interpretation as radius or
curvature would still require a separate derivation.

Kinematically, permissible label-invariant terminal observables include
symmetric functions of the unordered endpoint field data and mode projectors
commuting with endpoint permutation. Scalar examples are `q4+q5`,
`(q4-q5)^2`, and the explicit pair above. Symmetric density-sector counts and
unordered clock-pair observables are also definable on the full terminal
space, but their accessibility differs in this fixed experiment:

| Terminal data | Result under the frozen support and action |
|---|---|
| Induced terminal order | Always the same antichain; no geometric discrimination. |
| Scalar modes | The explicit `f0/f2` pair yields independent finite responses. Odd total scalar-parity packet amplitudes vanish. |
| Terminal densities | The original packet probes only `r4=r5=0`. Other density sectors require new terminal packets and new dust integrals. |
| Terminal clocks on the atomic density support | The action is independent of `t4,t5`; constant-orthogonal clock modes have zero amplitude. Clock bins alone give class- and preparation-independent factors. |
| Past/incidence data reconstructed from R | Not contained in the intrinsic R order or derived from these two matter records. |

The old one-`f` amplitude matrix alone cannot reconstruct an orthogonal
terminal row: adding `|f2><ell_input|` to an otherwise unspecified kernel leaves
all its old `f0` pairings unchanged. The new result is possible because the
original quadratic scalar action supplies the extra Gaussian-moment relation,
not because the old matrix by itself contained a hidden second measurement.

**Acceptance decision:** terminal matter-record construction and finite
instrument existence pass. Geometric/physical eligibility remains **HOLD**:
there is still no calibrated physical clock, mass, radius, curvature, or
physical CST history measure. The new packet is independent of all clocks and
preserves `T→-T`; Einstein's oriented-current zeros and `C_A>=1` source
obstruction are untouched. This is a concrete extension beyond the artificial
class-record basis, but not yet a gravitational response experiment.
