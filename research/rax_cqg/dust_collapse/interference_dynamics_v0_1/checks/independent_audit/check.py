#!/usr/bin/env python3
"""Independent exact audit of the full N11 dust-clock weight contract."""
from pathlib import Path
import itertools
import json
import sympy as s

OUT=Path(__file__).resolve().parent
beta=4/s.sqrt(6)
Delta=s.sqrt(2/(19*beta));k=beta*Delta
L=s.Rational(3,2)
rho=s.symbols('rho',real=True)
interior=[4,5,6];boundary=[0,1,2,3,7,8,9,10]
x=s.symbols('x4 x5 x6',real=True)
ri=s.symbols('r4 r5 r6',real=True)
b=[1,-9,16,-8]
def zero(v):assert s.simplify(s.expand(v))==0,v

# Density characteristic function under the original atom-plus-positive measure.
C=s.symbols('C',real=True,nonzero=True)
r=s.symbols('r',real=True)
D=s.Rational(1,2)+s.integrate(s.exp(-s.I*r*C/2),(r,0,1))/2
zero(D-(s.Rational(1,2)+(1-s.exp(-s.I*C/2))/(s.I*C)))
assert s.limit(D,C,0)==1
density_moments=[]
for n in range(7):
    moment=(s.Rational(1,2) if n==0 else 0)+s.integrate(r**n/2,(r,0,1))
    expected=1 if n==0 else s.Rational(1,2*(n+1))
    assert moment==expected
    density_moments.append(str(moment))

# Every one of the eight original inner strata occurs with weight 1/8.
E=s.symbols('E4 E5 E6')
stratum_sum=0;strata=[]
for mask in itertools.product([0,1],repeat=3):
    term=s.Rational(1,8)*s.prod(E[j] for j,m in enumerate(mask) if m)
    stratum_sum+=term
    strata.append({'positive_nodes':[interior[j] for j,m in enumerate(mask) if m],
                   'weight':'1/8','integrand_factor':str(term)})
zero(stratum_sum-s.prod((1+v)/2 for v in E))
assert len(strata)==8

# Independent reconstruction of order intervals, all boundary and interior terms.
pairs={(i,j) for i in range(11) for j in range(i+1,11)}
rows=[]
for name,relations in [('chain',pairs),('two_cover_deletion',pairs-{(4,5),(5,6)})]:
    assert all((i,l) in relations for i,j in relations for jj,l in relations if j==jj)
    coefficients={}
    for i,j in relations:
        size=sum((i,l) in relations and (l,j) in relations for l in range(11))
        coefficients[i,j]=b[size] if size<4 else 0
    T=[(j-5)*Delta for j in range(11)]
    densities=[rho]*11
    for j,v,w in zip(interior,x,ri):T[j]=v;densities[j]=w
    constraints=[s.expand(1+beta*s.Add(*(v*(T[j]-T[i])**2
                    for (i,jj),v in coefficients.items() if jj==j))/2)
                    for j in range(11)]
    F=11-sum(coefficients.values())
    S=F-s.Add(*(densities[j]*constraints[j] for j in range(11)))/2
    P=s.expand(sum(constraints[j] for j in boundary))
    zero(S-(F-rho*P/2-s.Add(*(v*constraints[j] for j,v in zip(interior,ri)))/2))
    if name=='chain':
        expected=125/s.Integer(19)+4*beta*x[0]**2-beta*x[1]**2/2-8*k*x[0]+2*k*x[1]+k*x[2]
        minimum=117/s.Integer(19)-9*beta/8-9*k/2
        minimizer={x[0]:Delta,x[1]:-L,x[2]:-L}
        lower=s.Rational(183,76)
        derivative_bound=125/s.Integer(38)+21*beta/16
    else:
        expected=112/s.Integer(19)-beta*x[0]**2/2+2*k*x[0]+k*x[1]+k*x[2]
        minimum=112/s.Integer(19)-9*beta/8-6*k
        minimizer={v:-L for v in x}
        lower=s.Rational(231,152)
        derivative_bound=56/s.Integer(19)-3*beta/16
    zero(P-expected)
    zero(P.subs(minimizer)-minimum)
    assert 0<Delta<L
    # beta<5/3 and k<5/12 follow by positive squaring against rational numbers.
    assert beta**2<s.Rational(25,9)
    assert beta**2<s.Rational(475,288)**2
    assert minimum>lower>0
    mean=P
    for variable in x:mean=s.integrate(mean,(variable,-L,L))/(2*L)
    zero(mean/2-derivative_bound)
    rows.append({'history':name,'F4':F,
        'outer_constraint_sum':str(P),
        'outer_constraint_sum_minimum':str(minimum),
        'strict_rational_minimum_lower_bound':str(lower),
        'outer_constraint_sum_mean':str(mean),
        'source_derivative_absolute_bound':str(derivative_bound),
        'source_derivative_bound_decimal':str(s.N(derivative_bound,18)),
        'all_outer_action_terms_included':True,
        'full_action_exactly_split_into_F_outer_and_inner':True})

# Scalar action has no r or T dependence: factorization can be exact, but its
# independent boundary packet must be identical for the two source comparisons.
q=s.symbols('q0:11',real=True)
Sphi=-beta*s.Add(*(v*(q[j]-q[i])**2 for (i,j),v in coefficients.items()))/4
assert all(s.diff(Sphi,v)==0 for v in (*x,*ri,rho))
ratio=s.Function('R')(rho)
incorrect=s.exp(s.I*(8+s.Rational(23,19)*rho))*ratio
zero(s.diff(incorrect,rho)/incorrect-s.diff(ratio,rho)/ratio-s.I*s.Rational(23,19))

result={
 'id':'INTERFERENCE-FULLWEIGHT-INDEPENDENT-AUDIT-0.1','all_checks_pass':True,
 'new_amplitude_quadratures':0,'density_factor':str(s.simplify(D)),
 'density_factor_at_zero':'1','density_moments_n0_to_6':density_moments,
 'density_derivative_bound_n_ge_1':'1/(2^(n+1)*(n+1))',
 'strata':strata,'histories':rows,
 'clock_contract':{'inner_domain':'[-3/2,3/2]^3','normalization':'1/27',
    'outer_values':'T_j=(j-5)*sqrt(2/(19*beta)), j in B',
    'clock_order_indicator':False,'new_vs_original_clock_box':True},
 'norm_bound':'|W_c(rho)|<=1 for real rho before scalar factor',
 'source_derivative':'W_c prime = -i/2 e^(iF4) E_T[P_B exp(-i*rho*P_B/2) product D(C_i)]',
 'no_double_counting':'W already contains e^(iF4) and complete off-shell dust phase; never multiply by exp(i*S_on_shell)',
 'double_counting_negative_control':'an extra exp(i*DeltaS_on) spuriously adds i*23/19 to d log(relative weight)/d rho',
 'boundary_scope':'fixed outer Dirichlet coordinates, all outer action terms, no outer state-packet or atom integration',
 'physical_scope':'conditional auxiliary full weight; no physical state or history measure derived',
 'probability_claim':False}
(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS independent full-weight audit: eight strata, exact boundary phase, both source derivative bounds, scalar independence')
