# Continuous exclusion on a frozen paired family

This package concerns the conditional, labelled 90-interval Poisson-count
experiment and the fixed reference configuration from PR111/PR112. Density,
landmarks 0–3 and root 4 are fixed. Each candidate line moves pivot 15 and one
other support along one boosted spatial axis, with the exact rational velocities
in `../coordinated_motions/directions.json`. Positive indices 3,5,...,59 and
h in [-1/10,1/10] cover the remaining 58 signed rays. Indices 0 and 1 were
excluded by PR112. These lines do not cover a multidimensional neighborhood.

A strong counterexample must preserve the selected-node order, pass the
inherited rank/conditioning/separation gates, have symmetric weight gap >1/5,
and have full conditional count-law TV <=1/4. A certified upper gap <=1/5,
a lower TV >1/4, or an order contradiction excludes that conjunction. HOLD
means that this calculation does not decide it. No full A-selection likelihood,
full B-graph likelihood, continuum error or arbitrary-motion stability is claimed.

## Both moving columns, both spatial axes

Let D be the 9 by 16 root-centered monomial matrix and H=I-11ᵀ/17.
With selectors E for the two moving columns, D(h)=D+U(h)Eᵀ, and each column
of U has degree two. For boosted x motion the physical-coordinate direction is
(-15v/8,17v/8,0); for y it is (0,0,v). Set Q=(DHDᵀ)⁻¹, V=DHE,
K=EᵀHE, W=[V,U] and C⁻¹=[[-K,I],[I,0]]. The four by four polynomial
matrix A=C⁻¹+WᵀQW and rhs WᵀQb give eta=A⁻¹WᵀQb. Woodbury then gives
lambda(h)=Qb-QW eta. In root-including centered maps R_D and R_E,

delta weights = ((R_E-R_D QV) eta_V - R_D QU eta_U)/scale².

Both moving columns and their interactions remain present. The unchanged
PR112 `solve_cell` centers the polynomial system at the rational cell midpoint,
forms exact residuals before directed interval rounding, and bounds a Neumann
series only when its infinity norm is strictly below one. A failed midpoint
inverse or contraction remains unresolved, never an assumed nonsingular solve.

In boosted coordinates all times are fixed. With scalar velocities v_i along
axis a, every pair has

q_ij(h)=q_ij(0)-2(s_j,a-s_i,a)(v_j-v_i)h-(v_j-v_i)²h².

Endpoints and an interior quadratic vertex give an exact whole-cell range.
This includes the cross term between the two moving tips. If a pair's entire
range has the opposite sign, the reference causal order is impossible.

## Overlap variance from a common future or past subinterval

For common future anchor k, put A=I(i,k), B=I(j,k); for common past anchor k,
put A=I(k,i), B=I(k,j). Both must be labelled observations in the experiment.
For D_count=N(A)-N(B), independent Poisson increments on the three disjoint
atoms A\B, B\A, A∩B give exactly

E D_count = mu_A-mu_B,
Var D_count = mu_A+mu_B-2 mu_intersection.

Overlapping interval counts themselves are never treated as independent.
Let e be the earlier and l the later moving tip in the boosted frame,
dt=t_l-t_e >=0, and r=|s_l-s_e|. Throughout a cell choose

delay >= max(0, sqrt(dt²-min(q_el))-dt).

For a common future anchor, v=(t_l+delay,s_l) is in both causal futures;
therefore I(v,k) is a subset of A∩B. For a common past anchor,
v=(t_e-delay,s_e) is in both causal pasts; I(k,v) is a subset. This also
works for equal tip times. Write T for the constant time from the chosen tip
to its common anchor. If delay<T and

q_sub_lower = min(q_tip,k)-2T*delay+delay² >0,

the enclosed interval has intensity at least
rho*scale³*pi*q_sub_lower^(3/2)/12. Otherwise use zero. Exact rational square
root and pi bounds give an outward intensity enclosure. Subtracting twice this
lower bound from the two upper means yields a rigorous upper variance. A
uniform delay itself defines a valid virtual tip; no monotonicity guess about
an unknown overlap volume is needed. For inadmissible geometries the physical
observation model is irrelevant: every law exclusion is asserted only on the
unchanged-order subset, where all observation intervals remain inside I(3,0).

## A labelled integer event, no independence approximation

For two disjoint mean enclosures [m_L-,m_L+] and [m_H-,m_H+], choose k as the
floor of the midpoint of their centers. If a=k+1-m_L+>0 and b=m_H--k>0,
Cantelli gives for the measurable event {D_count<=k}

TV >= max(0, 1-V_L/(V_L+a²)-V_H/(V_H+b²)).

V_L and V_H are upper variances. The +1 uses integer-valued counts. Overlapping
mean enclosures or an unusable threshold give zero. Every common anchor is a
separate measurable sub-observation; selecting a proved lower bound requires
no union correction. The alternative marginal certificate is the inherited
Poisson Hellinger lower bound. No overlapping-coordinate product law is used.

## Continuous coverage and bounded scope

Before any new campaign classification, the contract, source, this derivation,
and imported dependencies are hashed. Previous finite-grid and PR112 results
are known; this is an internal freeze, not external preregistration. The
contract fixes uniform cells and a finite widest-HOLD bisection budget per
line. All terminal cells, including HOLD, must cover the entire closed domain.
Numerical point tests audit implementations; the inequalities above establish
whole-cell claims. The result is the certified union of exclusion cells, not
an inference from a finite sampling grid or evidence of general stability.
