# Causal Stability Lab — mathematical scope

This instrument analyzes finite real linear history problems with a fixed passive probe. It does not sample Poisson clouds, implement a spinor operator, evolve quantum states or prove stability for the CSPP family. IEEE-754 calculations are diagnostics, not ball certificates. The original 192-bit certificate is retained in `tests/` only as an independently produced regression reference.

## Exact finite identities

For prescribed history h, active forcing f, a strictly lower triangular active transfer K and a passive probe:

    u = H h + K u + f
    A = q_H h + q_A u
    R = (I-K)^(-1) = I + K + ... + K^(N-1).

Thus the history-to-probe row is g = q_H + q_A R H. Its exact induced norm from real history l-infinity to absolute probe amplitude is Gamma_H = sum_j |g_j|. A perturbation h_j = eta sign(g_j) attains eta Gamma_H (zero coefficients can take either sign). This is a deterministic worst-case norm, not a variance or a probability. The response to active forcing is bounded by ||R||_infinity ||f||_infinity.

The absolute path majorant is P_H = |q_H|1 + |q_A| (I-|K|)^(-1) |H|1. Since |K| is also nilpotent, this is finite and Gamma_H <= P_H. The display's reduction 1-Gamma_H/P_H measures cancellation relative to this absolute path bound. It does not establish noise suppression or immunity to operator perturbations. Exact cancellation can coexist with large active error amplification.

## A sufficient uniform criterion — conditional theorem

If a family K_N satisfies sup_N ||K_N||_infinity <= r < 1, then

    sup_N ||(I-K_N)^(-1)||_infinity <= 1/(1-r).

Proof: apply submultiplicativity to the finite Neumann series and majorize it by the scalar infinite geometric series. To obtain a uniform history-to-probe bound, one additionally needs uniform bounds on ||H_N||_infinity, ||q_A,N||_1 and ||q_H,N||_1. The result is their corresponding sum/product bound. Observing ||K||<1 for one finite matrix does not prove any of these hypotheses across density, domain or infinite past. Failure of this sufficient criterion does not prove instability.

## Exact counterexample and positive control

For K_N = gamma S_N, where S_N has ones on the first subdiagonal, all eigenvalues are exactly zero, yet

    ||(I-K_N)^(-1)||_infinity = sum_{k=0}^{N-1} |gamma|^k.

For gamma >= 0 this stays uniformly bounded for gamma < 1, grows linearly at gamma = 1 and grows exponentially for gamma > 1. With H=(gamma,0,...,0)^T and q_A=(0,...,0,gamma), the history-to-probe gain is gamma^(N+1). The statements refer to this algebraic family. They do not establish the behavior of random causal sets. No positive Lyapunov exponent or physical temporal growth rate is inferred from graph length.

## CSPP fixture

The base is the immutable v0.25 publication at commit 13d12544fba9ac8fd54549eacc4a1ec19a2d6b51 of thomasmgfeller/x6-spectral-astrolabium, PROOF.md sections 2 and 6. The continuum parameters are rho=3/pi, epsilon=1/16, q=3/(16*pi), m=1, a=1/sqrt(2*pi). The coefficient family and local diagonal are unchanged:

    c(theta) = (1,-9,16,-8,0) + theta (9/8,-141/8,111/2,-63,24)
    d(theta) = -1 - 3 theta/8
    D = 1 - a d, beta = a epsilon / D
    w(n) = sum_k c_k binom(n,k) epsilon^k (1-epsilon)^(n-k).

All points are totally ordered in the underlying causal order, hence each interval count is the index separation minus one. Three points are prescribed history. Five are active in the original fixture and one is a passive probe. The transfer graph omits history-to-history edges because history values are clamped. It is not a Hasse diagram or a metric embedding. Varying the active count extends this synthetic order, not a physical density sweep.

At theta=21 and N=5 the original certificate gives Gamma_H approximately 0.6186537891469113 and P_H approximately 0.866523792024921. The reference gamma=7.308927861000362 is a different, coarse coefficient envelope from the proof and must not be confused with the row norm ||K|| or the chain coupling gamma. The program computes its own finite matrices and checks against the independently produced certificate.

The degree-four fixed-q family was rejected by the published two-scale mean screen. Showing a finite history response here does not reverse that result. METHOD and G1 remain HOLD. Compact KG production, density-uniform stability, infinite-past stability and physical stochastic covariance are not evaluated by this instrument.

## Rendering and animation

Node positions are a schematic layout; distances and angles have no physical metric interpretation. Animation reveals a topological evaluation order, not a preferred physical time. Edge colors show the sign of the computed contribution for the selected perturbation. Edge visibility controls never alter the matrices. The curve sweeps finite active-node counts in the same toy family. Frame rate and playback rate do not affect results. No smoothing filter is applied to model values.
