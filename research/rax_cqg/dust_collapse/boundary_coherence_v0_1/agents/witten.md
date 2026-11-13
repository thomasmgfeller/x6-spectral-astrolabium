# Common end event, coherence, and complete instrument

This agent role is a mathematical review label; the named scientist did not
participate. The outcome is a conditional finite-instrument construction and
an identifiability obstruction, not a physical detector derivation.

## 1. What is fixed, and what a common end event means

The frozen input is `causal_order_execution_v0_1/contracts/pilot.json`, SHA256
`442cc81227921135ccb046cdc238f8c2d9cae88f2082614490e59cfceba77ba3`.
The existing bounded amplitudes are in
`causal_order_execution_v0_1/checks/informatik/result_64.json`, SHA256
`5085b0f3d5bf2d9a70a184853c9d236fc2d41d7d2f7003b9c57ad980bdb34eae`.
No original file, history weight, action, packet, measure, or integration is
changed by this construction. The machine-readable specification is
`boundary_coherence_v0_1/contracts/coherence.json`.

The roles remain \(P=\{0\}\), \(A=\{1,2\}\), \(I=\{3\}\), and
\(R=\{4,5\}\). Both classes induce the same order on \(P\cup A\cup R\)
and are paired with the same input preparation and the same terminal packet
\(f_0=R_f\). Thus their already-defined amplitudes are linear functionals
on the same orthonormal two-dimensional preparation space
\(E=\operatorname{span}(g_0,g_+)\). Summing over future alternatives does
not discard the initial boundary \(P/A\), its preparation, or its integrals.
It also does not identify the class-dependent interior matter kernels.

**THEOREM — common mathematical pairing.** The frozen amplitudes can be
added as complex functionals on \(E\); no additional inner product on a
space of histories is needed for that addition.

**CONDITIONAL — physical common event.** The frozen contract supplies no
proof that an actual detector and its inaccessible environment carry no
class information. Identical external packets do not establish this.
Moreover, \(f_0\) is one terminal matter event. Its success/failure and
inner-density strata are not an already constructed pair of geometric
end-boundary measurements.

Here the inner-density flags \(s\in\{\mathrm{atom},\mathrm{positive}\}\)
remain separate. Forgetting these flags classically would sum their
probabilities; coherently adding them would require another instrument
change. This distinction avoids silently changing two aspects of the old
experiment at once.

## 2. Why classical forgetting does not identify a cross term

Write \(a_{cs}:E\to\mathbb C\) for a frozen amplitude row, with
\(a_{cs}=e^{i\kappa F_c}b_{cs}\), \((F_1,F_2)=(9,-7)\), and
\(\lambda=1/256\). The old accepted Kraus rows are

\[
M_{cs}=\lambda |c,s\rangle a_{cs},\qquad
Q_{\rm old}=\lambda^2\sum_{c,s}a_{cs}^{\dagger}a_{cs},\qquad
F_{\rm old}=(I_E-Q_{\rm old})^{1/2}.
\]

For a density operator \(\rho\) on \(E\), its old classical record map
contains only \(\lambda^2a_{cs}\rho a_{cs}^{\dagger}\).
Relabelling both classes as the same visible \(s\) yields

\[
p_s^{\rm forget}=\lambda^2\left(
a_{1s}\rho a_{1s}^{\dagger}+a_{2s}\rho a_{2s}^{\dagger}\right).
\]

**THEOREM — classical phase blindness.** Each row may be independently
rephased without changing this CP instrument. Consequently classical
coarse-graining does not revive the relative phase \(16\kappa\).

To expose the missing data, choose normalized environment vectors
\(|e_{1s}\rangle,|e_{2s}\rangle\), fixed independently of the input, and set

\[
\gamma_s=\langle e_{2s}|e_{1s}\rangle,\quad |\gamma_s|\le1,
\qquad
D_{12,s}(\rho)=\lambda^2\gamma_s a_{1s}\rho a_{2s}^{\dagger}.
\]

Every complex overlap in the unit disk has a realization, for example
\(e_{1s}=(1,0)\),
\(e_{2s}=(\overline{\gamma_s},\sqrt{1-|\gamma_s|^2})\).
The marked coherent dilation

\[
Vg=\lambda\sum_{c,s}a_{cs}(g)|c,s\rangle|e_{cs}\rangle
\;\oplus\;F_{\rm old}g
\]

is an isometry because the class flags are orthogonal. Measuring those
flags and discarding the environment gives exactly the old classical
instrument for every allowed \(\gamma_s\). Its off-diagonal elements
before class measurement differ between those realizations.

**NO-GO FROM OLD CLASSICAL DATA.** The old classical instrument alone
cannot identify \(\gamma_s\), the detector's relative phase reference,
or a physical \(D_{12,s}\). Existing complex amplitudes specify a useful
computational convention, but the missing apparatus information is not
reconstructed by their phases. Merely not reading a completed class
record does not reverse its decoherence.

The possibilities are physically distinct: \(\gamma=0\) means orthogonal
remaining markers; \(\gamma=1\) means identical environment states with
a specified phase reference; general complex \(\gamma\) gives partial
visibility and an extra phase. Full erasure is sufficient, not necessary,
for a cross term. A nonzero overlap does not guarantee a nonzero real
cross term at every detector phase. A fitted input-dependent \(\gamma(g)\)
need not define a linear quantum channel and is excluded here.

Without choosing an overlap, there is still an honest bound. With
\(x_s=a_{1s}\rho a_{2s}^{\dagger}\) and
\(q_{cs}=a_{cs}\rho a_{cs}^{\dagger}\), positivity of \(\rho\) gives
\(|D_{12,s}|\le\lambda^2|x_s|\le\lambda^2\sqrt{q_{1s}q_{2s}}\).
The possible direct-event probabilities lie in
\(\lambda^2[q_{1s}+q_{2s}-2|x_s|,q_{1s}+q_{2s}+2|x_s|]\).
This is an overlap-sensitivity envelope, not an inferred physical fringe.

## 3. A direct class-blind instrument, with its own failure map

For each inner stratum define the common visible event and its environment
by the linear map

\[
N_sg=\lambda\bigl[a_{1s}(g)e_{1s}+a_{2s}(g)e_{2s}\bigr],\qquad
\mathcal J_s(\rho)=\operatorname{tr}_{\rm env}(N_s\rho N_s^\dagger)
|s\rangle\langle s|.
\]

The notation identifies the scalar trace with the output probability.
Equivalently, expand each \(N_s\) in an orthonormal environment basis to
obtain its ordinary Kraus rows. The probability is

\[
p_s^\gamma(\rho)=\lambda^2\left[
a_{1s}\rho a_{1s}^{\dagger}+a_{2s}\rho a_{2s}^{\dagger}
+2\operatorname{Re}\left(\gamma_s a_{1s}\rho a_{2s}^{\dagger}\right)
\right].
\]

For \(\gamma_s=1\), a single accepted Kraus row suffices:
\(C_s=\lambda|s\rangle(a_{1s}+a_{2s})\).
For general overlap, the environment Gram matrix is

\[
G_s=\begin{pmatrix}1&\overline{\gamma_s}\\\gamma_s&1\end{pmatrix},
\qquad 0\le G_s\le(1+|\gamma_s|)I_2.
\]

The inherited analytic bound was

\[
Q_{\rm old}\le B I_E,\qquad
B=\frac{264069}{1310720}<0.202.
\]

It follows, as an **operator inequality on all of \(E\)**, that

\[
0\le Q_\gamma=\sum_sN_s^\dagger N_s
\le (1+\max_s|\gamma_s|)Q_{\rm old}
\le 2B I_E=\frac{264069}{655360}I_E<I_E.
\]

**CONDITIONAL EXISTENCE THEOREM ON \(E\).** All the chosen \(\gamma_s\)
therefore give CP accepted maps at the old gain. The new failure row
\(F_\gamma=(I_E-Q_\gamma)^{1/2}\), with its own flag, completes them to
a trace-preserving instrument. Its failure effect is bounded below by
\((391291/655360)I_E\). These claims use no undefined global
\(K^\dagger K\) and require no new quadrature.

This is a new instrument, not deterministic erasure of the old class
register. In particular, at \(\theta=0\), \(C_s\) is \(\sqrt2\) times
the diagnostic plus-port row below. Keeping both that larger row and
the old failure map would generally violate completeness. The accepted
probability and failure must be reported together; normalizing on success
alone would conceal the difference.

For a pure input, the interference contribution contains

\[
D_{12,s}(g)=\lambda^2\gamma_s e^{16i\kappa}
b_{1s}(g)\overline{b_{2s}(g)}.
\]

This is sensitivity to the finite action phase under an explicit detector
assumption, not evidence that a calibrated gravitational observable has
been measured.

## 4. A norm-preserving plus/minus diagnostic

If the coherent class register in \(V\) is accessible before irreversible
measurement, rotate it by the unitary with rows
\((1,\pm e^{i\theta})/\sqrt2\). For full overlap its Kraus rows are

\[
M_{\pm,s}=\frac{\lambda}{\sqrt2}|\pm,s\rangle
\bigl(a_{1s}\pm e^{i\theta}a_{2s}\bigr).
\]

With general environment overlap the probabilities are

\[
p_{\pm,s}^\gamma(\rho)=\frac{\lambda^2}{2}\left[
a_{1s}\rho a_{1s}^{\dagger}+a_{2s}\rho a_{2s}^{\dagger}
\pm2\operatorname{Re}\left(e^{-i\theta}\gamma_s
a_{1s}\rho a_{2s}^{\dagger}\right)\right].
\]

**THEOREM — completeness preservation.** Summing both ports cancels the
cross terms as an operator identity, for all inputs and all allowed
overlaps. Thus \(Q_{\pm}=Q_{\rm old}\) and the old failure map is retained
exactly. The observable fringe is port resolved; success summed over
both ports remains independent of the relative gravity phase.

The diagnostic phase is \(\theta=0\). It and its provisional numerical
values were discussed before this execution: this is an inherited
diagnostic, not a new blind preregistration. The finite cases
\(\gamma=0,1/2,1\) disclose assumption sensitivity. Removing the gravity
phase with \(\kappa=0\) while holding all \(b_{cs}\) fixed is a
counterfactual action ablation, not a calibrated change of Newton's
constant. Only already bounded amplitude rectangles are needed.

These plus/minus ports require a coherent register and do not by
themselves construct the user's physical terminal detector. Their value
is a cheap normalization and interference control on the more direct
common-event proposal.

## 5. Phase covariance, eligibility, and decision rule

**THEOREM — phase covariance.** Under a computational row rephasing
\(a_{cs}\mapsto e^{i\chi_{cs}}a_{cs}\), the same full experiment has
\(\gamma_s\mapsto e^{-i(\chi_{1s}-\chi_{2s})}\gamma_s\), or the
corresponding transported detector coefficients. In matrix notation,
\(a\mapsto Da\) requires \(U\mapsto UD^\dagger\). If overlap is held
fixed and the compensation is instead made through the relative
plus/minus phase, then
\(\theta_s\mapsto\theta_s+\chi_{1s}-\chi_{2s}\). One compensates a
given change once. The invariant is
\(e^{-i\theta}\gamma_s a_{1s}\rho a_{2s}^{\dagger}\).

The prior preparation remains intact. No source adapter follows from
this instrument change: the source obstruction
\(C_i=1+\frac\beta2(t_i-t_0)^2\ge1\) remains, and all class mixers
with clock-independent coefficients preserve global clock reflection.
Consequently the original oriented one-current event amplitudes still
vanish. There is no new mass, physical clock, radius, curvature, or
exterior interpretation.

The complementary terminal-packet construction in `agents/dowker.md`
keeps \(f_0\) and proposes a second symmetric even scalar matter packet.
It is a separate candidate for two actual terminal matter outcomes.
The old \(B\) and this report's \(2B\) cover only \(f_0\); an enlarged
instrument must supply its own contraction bound. It must not be
silently called a geometric detector.

The next evidential decision is therefore precise: either independently
justify a common physical detector, its residual environmental overlap,
and its phase reference, or retain only the conditional instrument
theorems and overlap-sensitivity bounds. If that information remains
absent, stop short of assigning a physical \(D_{12}\); enlarging phase
scans cannot supply it. A subsequent physical claim needs a separately
derived directed source and geometric readout.

## Verification scope

The proof above establishes positivity, completeness, phase covariance,
and the nonidentifiability statement algebraically from the frozen pilot.
The JSON contract is parsed and its source hashes and exact rational
bound identities are checked locally. The Hilbert agent independently
checked the environment Gram orientation, its explicit realization,
phase transport, and the all-input operator bound without a correction.

The independent information-agent code and regenerated
`checks/interference_results.json` were reviewed against this contract.
An initially missing factor \(|\gamma|\) in the reported phase visibility
was identified and corrected; the regenerated output now has exactly
zero visibility at \(\gamma=0\) and half visibility at \(\gamma=1/2\).
At \(\kappa=\gamma=1\), \(\theta=0\), the plus-port preparation contrast
is enclosed by
\([-0.000062160805,-0.000062132202]\), while total success is unchanged.
The direct common-event construction has its separately recomputed
failure map. These are propagated inherited enclosures, not a new
validation of their original quadrature or floating-point assumptions.

The additional `checks/extended_R.py` and `checks/extended_R_results.json`
were also reviewed for instrument structure. Their real-overlap models
are CP mixtures of the class-dephased and directly coherent terminal
instruments; they use the separate gain \(1/1024\), full effects on
\(E\), and their own failure roots. For the coherent inherited-action
case their \(f_2\) probability contrast is enclosed by
\([2.5190715,2.5242797]\times10^{-6}\). That contrast is conditional on
success: the two unconditional success probabilities are only about
\(3.58872\times10^{-10}\) and \(9.34809\times10^{-10}\), respectively.
This review checks consistency with the conditional instrument theory;
it does not establish a physical coherence mechanism, certify the old
quadrature anew, or turn these terminal scalar modes into geometry.
