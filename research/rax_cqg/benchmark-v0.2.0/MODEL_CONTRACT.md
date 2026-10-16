# Mathematical contract and evidence boundaries

Version 0.2.0. This document defines what the implementation computes. Statements about a chosen finite mathematical model must not be read as empirical statements about nature.

## 1. Finite strict orders

`R[i,j] = 1` means that element i strictly precedes j. The matrix is binary, irreflexive and transitively closed. Arbitrary labels are supported; an input matrix need not be upper triangular. `from_matrix` rejects a nontransitive matrix; `from_edges` closes an acyclic edge set.

To insert i < j into a closed order, the implementation first rejects a cycle, then adds every pair in

\[
(\operatorname{Anc}(i)\cup\{i\})\times(\operatorname{Desc}(j)\cup\{j\}).
\]

This is the transitive closure after that insertion. In particular, two fixed insertions give the same final closure in either order if their union with the original order is acyclic. An apparent order dependence caused by incomplete closure is a bug, not quantum noncommutativity. State-dependent rewrite rules could have a different algebra, but none is claimed here.

Python supports 0–512 elements; the browser core supports 0–96, with interactive generation starting at 4. These are practical resource limits. The number of elements and the thinning-step counter are not identified with physical time.

## 2. Reproducible sampling

Randomness uses PCG-XSH-RR 64/32, fixed stream 54, and an unsigned 32-bit seed. An open-interval variate is `(uint32 + 0.5) / 2**32`. Seed 42 starts with hexadecimal outputs `a15c02b7 7b47f409 ba1d3330 83d2f293 bfa4784b cbed606e`, matching the official reference convention. The RNG is local to each operation and is not cryptographic. Distinct seeds provide reproducible pseudorandom replicates, not a mathematical proof of independent samples.

| Model | Construction | Limitation |
|---|---|---|
| `chain` | All i < j for i < j as integer labels | Deterministic reference |
| `antichain` | Empty strict relation | Deterministic reference |
| `percolation` | Independent candidate edges i → j for i < j, probability p, then closure | Specified labelled ensemble, not uniform on unlabelled orders |
| `three_layer` | Layer sizes floor(N/4), floor(N/2), remainder; independent adjacent-layer edges, then closure | A fixed labelled three-layer ensemble, not uniform sampling of all KR orders |
| `minkowski_2d` | Fixed N independent uniform volume points in a 2D diamond | Continuum geometry is supplied as input |
| `minkowski_4d` | Fixed N independent uniform volume points in a 4D diamond | Continuum geometry is supplied as input |

For Minkowski models the endpoints are (-1/2, 0, …) and (1/2, 0, …), with c = 1. The coordinate domain is `|x| ≤ 1/2 − |t|`. In 2D, independent u,v uniform in (0,1) give t=(u+v)/2−1/2 and x=(v−u)/2, with constant Jacobian and diamond volume 1/2.

In 4D the spatial cross-section is a ball of radius a(t)=1/2−|t|, so the time density is proportional to a(t)^3. Inverse-CDF sampling gives

\[
t=\begin{cases}-\tfrac12+\tfrac12(2u)^{1/4},&u<1/2,\\
\tfrac12-\tfrac12[2(1-u)]^{1/4},&u\ge1/2.
\end{cases}
\]

The radius is a(t) v^(1/3), with independent uniform spherical direction. The 4D volume is π/24. This is uniform spacetime-volume sampling conditioned on N; the number of points is not Poisson sampled. Independent moment checks use E[t²]=1/60, E[t⁴]=1/1120, E[r²]=1/10 and E[r⁴]=3/224.

Causality uses the direct float64 comparison `dt > 0 and dt**2 >= sum(dx**2)`. There is no added epsilon and no silent closure repair. The resulting order is validated; a floating-point violation is rejected. Points extremely close to a light cone can produce platform-dependent edge decisions. No Lorentz-invariance test of machine arithmetic is claimed.

## 3. Order intervals and the 4D BDG bracket

For each related pair i < j, the number of interior elements is `(R @ R)[i,j]`. Let N_k be the number of related pairs with exactly k interior elements. Thus N_0 counts links. The implementation computes only the dimensionless interval combination

\[
B_4=N-N_0+9N_1-16N_2+8N_3.
\]

This is the 4D Benincasa–Dowker interval bracket, with the interior-count indexing stated explicitly. The paper's interval indexing is shifted by one relative to N_k here. Dimensional normalization, gravitational constants and discreteness length are omitted; `bdg4_bracket` must not be called a measured gravitational action or curvature. Evaluating this polynomial on any finite order does not establish manifoldlikeness, convergence, suppression or the applicability of a 4D continuum interpretation. In particular, applying B_4 to the 2D reference is a combinatorial comparison, not a dimensionally appropriate gravitational action.

Exact examples: four-element antichain B_4=4; three-element chain plus an isolate B_4=11; one minimum below three incomparable elements B_4=1; four-element diamond B_4=−16.

## 4. Graph diagnostics

H=R+Rᵀ is the simple undirected comparability-graph adjacency matrix, **not the link-graph adjacency**. It discards causal orientation. M=ΣR is its number of undirected edges. L=diag(H1)−H is the combinatorial graph Laplacian.

| Export key | Definition |
|---|---|
| `ordering_fraction` | 2M/[N(N−1)]; convention 0 when N<2 |
| `height` | Maximum number of elements in a chain; 0 for the empty order |
| `spectral_radius` | max absolute eigenvalue of H; 0 for N=0 |
| `adjacency_spectral_width` | largest minus smallest eigenvalue of H |
| `algebraic_connectivity` | Second-smallest eigenvalue of L; null for N<2; small negative roundoff clamped to 0 |
| `adjacency_spectral_std` | sqrt(2M/N), because tr(H)=0 and tr(H²)=2M; 0 for N=0 |
| `h2_spectral_entropy` | −Σ w_i ln(w_i), w_i=λ_i(H)²/(2M); null for M=0 |
| `triangles` | tr(H³)/6 |
| `triangles_per_vertex` | tr(H³)/(6N); 0 for N=0 |

The spectral entropy is an entropy of graph-derived weights, not evidence of quantum entanglement. The spectral standard deviation contains no information beyond N and M. A graph and its causal dual have identical H. Spectra do not uniquely reconstruct a graph or a spacetime; none of these observables proves the causal-set Hauptvermutung.

Full signed spectra are computed and exported. The JavaScript Jacobi method stops at off-diagonal Frobenius norm ≤ 10^−12 max(1, initial Frobenius norm), with at most 60 sweeps; failure to converge is an error. Numerical parity checks are finite and use 10^−9 absolute and relative tolerances.

## 5. Thinning

At each step, every surviving element is retained independently with probability q, then the induced order is taken. Original element indices are retained in the path. Two independent rounds with retention q₁,q₂ have the same subset distribution as one round with retention q₁q₂. This distributional statement does not mean that arbitrary seeded trajectories coincide.

The implementation does not define a renormalization transformation on couplings, a fixed point, an invariant action, or a continuum limit. Calling the procedure thinning avoids attributing those additional properties to it.

## 6. Stable classical graph field

The field reference uses d independent real components per vertex and

\[
Q=m^2I+gL,\qquad S(\phi)=\frac12\sum_{a=1}^d\phi_a^TQ\phi_a,
\qquad m>0,\ g\ge0.
\]

Since xᵀLx=Σ_{\{i,j\}∈E}(x_i−x_j)²≥0, Q is positive definite and its eigenvalues are at least m². With density proportional to exp(−S), covariance per component is Q^−1 and

\[
\log Z=\frac d2[N\log(2\pi)-\log\det Q].
\]

Sampling uses Cholesky and Box–Muller normals. The analytic positivity statement assumes exact real arithmetic; extreme scales can exceed floating-point range or conditioning, and are not a supported physical limit. This is a classical Euclidean Gaussian model. It has no Lorentzian propagator, canonical quantum field, entanglement calculation, or backreaction. Its graph coupling discards orientation.

## 7. Relational clock reference

The equations embedded in the supplied Gmail image links were not available as readable equations. The following is an explicit reference model, not a reconstruction of those images and not an inferred property of the causal-set code.

Assume two qubits, ℏ=1, ω>0,

\[
H_T=H_S=\operatorname{diag}(-\omega/2,+\omega/2),\quad
|\Psi\rangle=(|01\rangle+|10\rangle)/\sqrt2,
\quad C=H_T\otimes I+I\otimes H_S.
\]

Then C|Ψ⟩=0. Choose |τ⟩=exp(−iH_Tτ)|+⟩. The partial inner product ⟨τ|Ψ⟩ has squared norm 1/2; its normalized system state is exp(−iH_Sτ)|+⟩ and satisfies i∂τ|ψ(τ)⟩=H_S|ψ(τ)⟩. The zero-point convention is part of this chosen constraint.

The clock is periodic in its observable probabilities, with period P=2π/ω. The states at different τ are not orthogonal. A normalized continuous phase POVM on [0,P) has density E(τ)=(2/P)|τ⟩⟨τ| and integrates to I. Its clock probability density is 1/P. The ket can change by a global sign after P; the physical ray and probabilities repeat.

A finite-dimensional clock has no exact canonical commutator [T,H]=iI: the traces of the two sides would disagree. No ideal, globally unbounded clock is represented. The construction assumes Hilbert spaces, the Born rule, Hamiltonians and a constraint; it demonstrates conditional evolution within that framework. It does not derive quantum mechanics, identify the growth index with τ, or prove that physical time is nonfundamental. Clock-system interactions and general constraints can change the conditional equation and require separate analysis.

## 8. Move algebra and QSG

The supplied classical reset example uses column-stochastic matrices

\[
P_0=\begin{pmatrix}1&1\\0&0\end{pmatrix},\qquad
P_1=\begin{pmatrix}0&0\\1&1\end{pmatrix},\qquad
[P_0,P_1]=\begin{pmatrix}1&1\\-1&-1\end{pmatrix}.
\]

This is ordinary classical order dependence. It establishes neither quantum interference nor a quantum causal growth model. A proposed QSG extension must define its state spaces, transition maps, amplitudes or measures, positivity/normalization, physical equivalence of growth histories, covariance and causality conditions before claiming their compatibility. No such extension is implemented.

Srivastava and Surya's 2026 QSG preprint studies operator-valued transitions and several quantum Bell-causality implementations, with important assumptions including nonsingular transitions. Two studied orderings force a commutative algebra; another gives restrictions without a general noncommutative solution. These are results for the specified constructions, not a no-go theorem for all noncommutative causal models and not a validation of RAX-CQG.

## 9. Records and evidence

Experiment schema: `RAX-CQG-EXPERIMENT-0.2`. The relation rows are bit strings. The SHA-256 input is the decimal N, newline, then every row followed by newline. A hash checks accidental alteration of that matrix representation; it authenticates neither authorship nor physical validity. A valid hash does not verify a claimed seed or provenance. Import recomputes metrics from the matrix; release verification separately replays the included pilot seeds.

The pilot retains full matrices, generator parameters, seed conventions, coordinates where applicable, spectra and source hashes. Statistical summaries use sample standard deviation (ddof=1), SEM=sd/√n and t intervals with n−1 degrees of freedom. Means exclude undefined metrics and explicitly report their counts, so those means are conditional on defined values. Sparse and very small samples can violate the usefulness of a t approximation. The pilot supports reproducibility checks, not a continuum or model-selection result.

## Primary sources

1. D. M. T. Benincasa and F. Dowker, *The Scalar Curvature of a Causal Set*, Phys. Rev. Lett. 104, 181301 (2010). [arXiv:1001.2725](https://arxiv.org/abs/1001.2725). Source for the four-dimensional interval bracket; indexing conventions must be matched.
2. D. P. Rideout and R. D. Sorkin, *A Classical Sequential Growth Dynamics for Causal Sets*, Phys. Rev. D 61, 024002 (2000). [arXiv:gr-qc/9904062](https://arxiv.org/abs/gr-qc/9904062). Background for classical sequential growth and its conditions.
3. D. N. Page and W. K. Wootters, *Evolution without evolution: Dynamics described by stationary observables*, Phys. Rev. D 27, 2885 (1983). [DOI](https://doi.org/10.1103/PhysRevD.27.2885).
4. P. A. Höhn, A. R. H. Smith and M. P. E. Lock, *The Trinity of Relational Quantum Dynamics*. [arXiv:1912.00033](https://arxiv.org/abs/1912.00033). Background on relational dynamics, conditioning and their assumptions.
5. R. Srivastava and S. Surya, QSG preprint (2026). [arXiv:2603.25503](https://arxiv.org/abs/2603.25503). Specific operator-valued quantum sequential growth analysis; not implemented here.
6. M. E. O'Neill, PCG official minimal C implementation and reference output. [pcg-random.org/download.html](https://www.pcg-random.org/download.html). Algorithm attribution and license are in `THIRD_PARTY_NOTICES.txt`.
