# Proofs and claim boundaries

SPDX-License-Identifier: Apache-2.0

## 1. Continuous single-node operator enclosure

Let M have the nine linear/quadratic moment rows and sixteen support columns.
Write s for its column sum, S=M M^T-s s^T/17, b=(0,0,0,-2,2,2,0,0,0)^T,
Q=S^(-1), and lambda=Q b. The minimum-norm weights include the root and annihilate
constants. Moving a single support point by h changes its moment column by a
quadratic vector d(h)=p1*h+p2*h^2. Put v=M_j-s/17. Direct expansion gives

    S(h)=S + d v^T + v d^T + (16/17) d d^T.

With U=[v,d] and C=[[0,1],[1,16/17]], the Woodbury formula yields

    lambda(h)=lambda - Q U B^(-1) U^T lambda,
    B=C^(-1)+U^T Q U,
    C^(-1)=[[-16/17,1],[1,0]].

The 2-by-2 determinant being nonzero certifies the full moment rank for every h
in the cell. If (alpha,beta)=B^(-1)(v^T lambda,d^T lambda), then
delta_lambda=-Qv*alpha-Qd*beta. Center all 17 moment columns, including the root
column -s/17. For centered column c_i, the exact weight change is

    delta_w_i = [-c_i^T Qv*alpha - c_i^T Qd*beta
                 +(1_{i=j}-1/17)*d^T lambda(h)] / scale^2.

All coefficients are multiplied and cancelled as exact rationals **before**
enclosing h. Raw interval matrix products can lose those cancellations and fail
to certify even small steps. Horner evaluation and directed fixed-point interval
arithmetic enclose the resulting polynomial/rational expressions. No random or
floating-point inverse proposal is used.

If D bounds the Euclidean norm of delta_w, N0 is a lower bound for ||w(0)||,
and N1 bounds ||w(h)|| from below throughout the cell, then

    2 ||w(h)-w(0)|| / (||w(h)||+||w(0)||) <= 2 D/(N0+N1).

Thus a bound <=1/5 excludes a >20% gap on the entire cell. This remains valid
even when further admissibility conditions would reject part of the cell.

In the rational boost frame the motion is spatial. For any other selected point,

    q(h)=q(0)+2*sign*(x_other-x_moved)*h-h^2.

Its exact extrema on a cell occur at its endpoints or at the quadratic vertex.
A cell whose entire q-range contradicts the original causal/spacelike relation
is excluded. Null points are inadmissible under the inherited strict margins.
Uncertified geometry boundaries are retained unless another proof excludes them.

For a measured interval with positive q-range, monotonicity of q^(3/2) gives a
uniform Poisson mean enclosure. The inherited Hellinger or threshold-event lower
bound then applies to **every** h in that cell. Any such lower bound >1/4 excludes
the full count/overlap-law closeness gate by marginalization. Counts are never
assumed independent. A threshold event remains valid even when it cannot be
proved optimal throughout the parameter cell.

The three exclusions (order, operator gap, count law) are exhaustive reasons for
rejecting a cell, not an assumption that all cells must be rejected. Remaining
HOLD leaves are included in the exact interval cover and explicitly reported.
This certifies only comparison to the one fixed reference geometry.

## 2. Fixed auxiliary energy and response norm

Let G be the undirected version of the Hasse graph of the shared 21-node order,
with unit conductance on every cover relation. It is connected. Its Laplacian L
defines

    E(f)=f^T L f = sum_{cover edges {i,j}} (f_i-f_j)^2.

This uses the shared order, without embedding coordinates or count-dependent
tuning. Choosing unit conductances and E(f)<=1 is an explicit **auxiliary
regularity assumption**. E is not identified with physical Lorentzian energy.
The original directed order and the d'Alembert weights remain unchanged.

Extend each 17-component weight vector by four zero landmark entries. For any
weight difference v, sum(v)=0. Ground one vertex and solve Lx=v. Connectedness
makes the grounded system invertible; the omitted equation follows from sum(v)=0.
For every f,

    |v^T f|=|x^T L f| <= sqrt(x^T L x) sqrt(f^T L f).

Since x^T L x=v^T x=v^T L^dagger v, equality is attained by a suitable multiple
of x (unless v=0). Therefore

    sup_{E(f)<=1} |v^T f| = sqrt(v^T L^dagger v).

This is an exact response-error norm on the declared class. Constants remain
unrestricted but cause no divergence because the weights annihilate them.
Replacing L by a*L rescales the absolute norm by 1/sqrt(a); the symmetric
relative response gap is invariant. Relabeling the nodes also preserves it.
The field class and these response norms do not change any statistical TV bound.

This finite auxiliary form meets the resistance-form requirements: its domain is
all real functions on the finite vertex set; connectedness makes constants its
only zero-energy functions; the quotient by constants is a finite-dimensional
Hilbert space; arbitrary finite data can be interpolated; effective resistance
is finite and positive between distinct vertices. Clipping a function to [0,1]
cannot increase any edge difference and therefore satisfies the Markov property.
The dual formula applied to v=e_i-e_j gives

    |f_i-f_j|^2 <= R(i,j)*E(f),
    R(i,j)=(e_i-e_j)^T L^dagger (e_i-e_j).

Thus the claimed resistance control is available in this auxiliary model, with
no assumption that the causal-set d'Alembert operator is its Laplacian.

## 3. A compatible auxiliary refinement and its limit

Replace each edge by a path of n=2^m edges with conductance n. Given endpoint
values a,b, minimizing the path energy gives linear interpolation and

    min n * sum_{k=1}^n (f_k-f_{k-1})^2 = (b-a)^2.

Consequently the Schur complement (trace) onto the original vertices is exactly
L at every level. Trace onto an earlier dyadic level also agrees with that
level's form: each earlier subedge is replaced by resistors with the same total
series resistance. The associated effective resistance between existing
vertices is preserved. Leaving conductance at 1 instead gives trace L/n and
does not preserve the original form.

There is a concrete limit for this **constructed auxiliary model**: attach a
unit interval to every edge, glue endpoints at the graph vertices, and use
continuous edgewise H^1 functions with energy sum_e integral_e |f'|^2.
The trace on the original vertices is the graph energy above. For any H^1
function, the derivative of its dyadic piecewise-linear interpolant is the
cell average of f'. These averages converge to f' in L^2; hence interpolant
energies converge to the metric-graph energy. This is a metric-graph limit with
one-dimensional edges, not a derived four-dimensional spacetime limit.

## 4. Sharp energy-dependent quadrature error on the auxiliary limit

Let M be the number of unit edges, use normalized length measure (total mass 1),
and let Q_n be the composite trapezoidal rule with n equal cells per edge.
On a cell of length ell=1/n, integration by parts gives

    integral_0^ell f(s) ds - ell*(f(0)+f(ell))/2
      = integral_0^ell (ell/2-s) f'(s) ds.

The squared L^2 norm of the kernel is ell^3/12. Cauchy-Schwarz over all M*n
cells, followed by normalization by M, proves

    |integral f dmu - Q_n f| <= sqrt(E(f)) / (n*sqrt(12*M)).

The constant is sharp. On every cell set f(s)=s*(ell-s), so all quadrature
samples vanish and the pieces fit continuously. Its total energy is M/(3*n^2)
and normalized integral 1/(6*n^2), giving equality. The bound separates sampling
scale from function energy, in the spirit of the energy-dependent integration
bounds studied by Malmquist and Strichartz. Here it is proved directly for the
metric graph; a theorem for p.c.f. fractals is not transplanted to causal sets.

## Applicability and stopping decision

The finite positive energy, trace compatibility, resistance control and
quadrature estimate are now explicit and checked. Applying the construction to
the actual causal-set continuum still requires a justified refinement of the
physical data, a measure and scale tied to spacetime sampling, and a proved
relationship to the hyperbolic Lorentzian operator. These are **OPEN**, so the
physical Kigami/Strichartz transfer is **HOLD**. Artificial edge-subdivision
vertices are not additional observations and supply no statistical information.

Primary methodological references:

- Jun Kigami, [Analysis on Limits of Networks](https://doi.org/10.1017/CBO9780511470943.003),
  compatible finite Dirichlet forms and resistance-preserving limits.
- Jun Kigami, [Harmonic Analysis for Resistance Forms](https://www-an.acs.i.kyoto-u.ac.jp/~kigami/ulcg.pdf),
  resistance metrics, Green functions and regularity.
- Jens Malmquist and Robert S. Strichartz,
  [Numerical integration for fractal measures](https://arxiv.org/abs/1606.02773),
  energy-dependent error estimates under their stated fractal hypotheses.
