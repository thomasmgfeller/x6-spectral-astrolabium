#!/usr/bin/env python3
"""Exact geometry and response identities, without inventing finite-weight numerics."""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import json
import sympy as s
from numeric_response import evaluate

ROOT=Path(__file__).resolve().parent
N=tuple(range(11));I=frozenset((4,5,6));B=frozenset(N)-I
C0=frozenset(combinations(N,2));C1=C0-{(4,5),(5,6)}

def geometric_count(rel):
    return sum(x in I and y in I for x,y in rel)

def filtration(rel):
    n={x:sum(y==x for _,y in rel) for x in N}
    return [sum(n[x]<=k for x in N) for k in N]

checks={}
checks['two_transitive_orders']=all(all((x,z) in rel for x,y in rel for yy,z in rel if y==yy) for rel in (C0,C1))
checks['observable_values_3_and_1']=[geometric_count(rel) for rel in (C0,C1)]==[3,1]
checks['common_outer_order']={(x,y) for x,y in C0 if x in B and y in B}=={(x,y) for x,y in C1 if x in B and y in B}
checks['common_cross_incidence']={(x,y) for x,y in C0 if (x in B)!=(y in B)}=={(x,y) for x,y in C1 if (x in B)!=(y in B)}
checks['boundary_preserving_relabel_invariance']=True
for perm in permutations(sorted(I)):
    m={**{x:x for x in B},**dict(zip(sorted(I),perm))}
    for rel in (C0,C1):
        transported={(m[x],m[y]) for x,y in rel}
        checks['boundary_preserving_relabel_invariance'] &= geometric_count(transported)==geometric_count(rel) and filtration(transported)==filtration(rel)

# lambda_intensity is not the old acceptance gain; it is the relative intensity.
lam=s.symbols('lambda_intensity',positive=True)
q=s.symbols('d_log_modulus_ratio',real=True)
E=(3+lam)/(1+lam)
checks['response_derivative_identity']=s.simplify(s.diff(E,lam)*2*lam*q+4*lam*q/(1+lam)**2)==0
l0,l1=s.symbols('lambda_low lambda_high',positive=True)
checks['finite_difference_identity']=s.simplify((3+l1)/(1+l1)-(3+l0)/(1+l0)-2*(l0-l1)/((1+l0)*(1+l1)))==0
checks['resolved_phase_blindness']=s.simplify((3*s.Abs(s.exp(s.I*s.symbols('theta',real=True)))**2+1)/(s.Abs(s.exp(s.I*s.symbols('theta',real=True)))**2+1)-2)==0
weak=s.simplify((3+s.I)/(1+s.I))
checks['coherent_weak_ratio_can_be_complex']=weak==2-s.I
checks['coherent_weak_ratio_can_exceed_geometric_spectrum']=s.simplify((3-s.Rational(1,2))/(1-s.Rational(1,2)))==5
checks['resolved_mean_in_geometric_range']=s.simplify(E-1)==2/(1+lam) and s.simplify(3-E)==2*lam/(1+lam)
checks['same_phase_blind_mean_different_interference']=sum([F(1),F(1)])==2 and abs(1+1)**2==4 and abs(1-1)**2==0
checks['source_values_in_common_positive_density_range']=F(0)<F(1,8)<F(1,4)<F(1,2)
checks['fixed_geometry_independent_of_source']=[geometric_count(C0),geometric_count(C1)]==[3,1]
checks['common_clock_box_contains_shifted_stationary_clocks']=s.simplify(25*s.sqrt(6)/38)<s.Rational(9,4)
assert all(bool(v) for v in checks.values()),checks
numeric_checks,numeric=evaluate(ROOT)
checks.update(numeric_checks)

result={
 'id':'CST-DUST-N11-GEOMETRY-RESPONSE-AUDIT-0.1',
 'status':'PASS_EXACT_GEOMETRY_AND_RESPONSE_IDENTITIES',
 'checks':{k:bool(v) for k,v in checks.items()},
 'geometries':{'C0':{'O':3,'past_cardinality_filtration':filtration(C0)},'C1':{'O':1,'past_cardinality_filtration':filtration(C1)}},
 'amplitude_contract':'a_c(rho)=A_c*W_c(rho), A_c=omega_c*g_c contains only fixed history weight and rho-independent scalar Gaussian factor. W_c already includes exp(i F_c), the full inner Dirichlet/clock-box integral and original atom+positive inner density measure. No second gravitational phase is inserted.',
 'relative_intensity':'lambda_intensity(rho)=|a_1(rho)/a_0(rho)|^2; defined only where a_0 is nonzero',
 'resolved_mean':'E[O|resolved record,success]=(3+lambda_intensity)/(1+lambda_intensity)',
 'derivative':'dE/drho=-4*lambda_intensity/(1+lambda_intensity)^2 * d/drho log|W_1/W_0|',
 'finite_difference':'E_high-E_low=2*(lambda_low-lambda_high)/((1+lambda_low)*(1+lambda_high))',
 'coherent_ratio':'O_weak=(3*a_0+a_1)/(a_0+a_1), only when denominator is nonzero; generally complex, not a Born mean',
 'synthetic_controls_only':{'complex_example':{'a0':'1','a1':'i','O_weak':'2-i'},'outside_spectrum_example':{'a0':'1','a1':'-1/2','O_weak':5},'phase_only_resolved_mean':2,'phase_only_coherent_squared_modulus_examples':[4,0]},
 'source_parameter':'rho changes fixed boundary density data and is not elapsed time or a calibrated mass',
 'source_values':['1/8','1/4'],
 'numerical_original_weight_response':'EVALUATED_FROM_COMPLETE_SIBLING_WEIGHTS_AT_N160_WITH_EQUAL_HISTORY_WEIGHTS',
 'numeric_diagnostic':numeric,
 'normalization':'All displayed means condition on successful resolved records. They do not supply a total success probability or a physical instrument completion.',
 'clock_domain':'Declared new common clock box [-3/2,3/2]; no causal-order theta restriction. Centered stationary witnesses fit, but the integral still includes nonmonotone clocks.',
 'physical_geometry_dynamics':'NOT_DERIVED_FROM_THESE_IDENTITIES_ALONE',
}
(ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
