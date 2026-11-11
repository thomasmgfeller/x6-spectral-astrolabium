"""Bounds for the declared finite AA Abel amplitude, not a physical kernel.

The scalar action is volume-weighted and independent of dust variables.
Clock and density supports remain exactly the compact supports of step 2.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import cmath
import math
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
BETA=4/s.sqrt(6)
GATES={k:'HOLD' for k in ('MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION')}

def aa_codes():
    optional=[(i,j) for i in (0,1) for j in (2,3,4)]+[(2,3),(2,4)]
    answer=[]
    for flags in product((0,1),repeat=8):
        rel={p for p,on in zip(optional,flags) if on}
        if any((i,k) not in rel for i,j in rel for j2,k in rel if j2==j):continue
        if not any((i,2) in rel for i in (0,1)):continue
        if not any((2,j) in rel for j in (3,4)):continue
        if not all(any((i,j) in rel for j in (3,4)) for i in (0,1)):continue
        if not all(any((i,j) in rel for i in (0,1)) for j in (3,4)):continue
        answer.append(sum(1<<(5*i+j) for i,j in rel))
    return sorted(answer)

def relations(code):return {(i,j) for i in range(5) for j in range(5) if code&(1<<(5*i+j))}

def reconstruct_h0(code):
    rel=relations(code); h=s.zeros(5)
    for i,j in rel:
        k=sum((i,z) in rel and (z,j) in rel for z in range(5))
        coefficient=(1,-9,16,-8)[k] if k<4 else 0
        d=s.zeros(5,1);d[i]=-1;d[j]=1
        h-=s.Rational(coefficient,2)*d*d.T
    return h

def history_certificate():
    records=[]
    for code in aa_codes():
        rel=relations(code);p=sum((i,2) in rel for i in (0,1));q=sum((2,j) in rel for j in (3,4))
        h=reconstruct_h0(code);j=(BETA*h).extract([2],[0,1,3,4])
        alpha=s.simplify(-BETA*h[2,2]);norm2=s.simplify((j*j.T)[0])
        records.append({'code':code,'p':p,'q':q,'alpha_massless':str(alpha),
                        'J_norm_squared':str(norm2),'J_norm_squared_over_alpha_squared':str(s.simplify(norm2/alpha**2))})
    return records

def scalar_inner(alpha,eta,epsilon):
    if not all(math.isfinite(x) for x in (alpha,eta,epsilon)) or alpha<=0 or epsilon<0:
        raise ValueError('alpha>0, epsilon>=0 and finite real inputs required')
    z=complex(epsilon,alpha)
    return math.sqrt(2*math.pi)/cmath.sqrt(z)*cmath.exp(-eta*eta/(2*z))

def positive_density_integral(k):
    if not math.isfinite(k):raise ValueError('finite real k required')
    if k==0:return 1+0j
    return cmath.exp(-.5j*k)*(math.sin(k/2)/(k/2))

def sector_factor(name,u,v):
    if name=='zero':return s.Rational(1,2)
    if name=='mixed':return (u+v)/(2*s.sqrt(2))
    if name=='double':return u*v/2
    if name=='plus':return (u+v+u*v)/(2*s.sqrt(3))
    raise ValueError('unknown sector')

def bound_matrix():
    # Equal widths sigma_s=sigma_a=1, massless universal bound, sum|c_C|=1.
    f=s.Matrix([s.sqrt(s.pi/2),s.sqrt(2),s.sqrt(3*s.pi/2),s.sqrt(6)])
    return s.sqrt(2*s.pi/BETA)*f*f.T

def evidence():
    cert=history_certificate();bound=bound_matrix();maximum=6*s.sqrt(2*s.pi/BETA)
    rate=s.simplify(maximum*(1/(2*BETA)+s.Rational(1,2)))
    return {'scope':'FINITE_AA_ABEL_EXISTENCE_WITH_COMPACT_DUST_SUPPORTS',
      'parent_model':'CST-DUST-KG-MIN-v0.1','history_count':len(cert),
      'p_q_histogram':{str(k):v for k,v in sorted(Counter((r['p'],r['q']) for r in cert).items())},
      'history_certificates':cert,'density_atom_and_continuous_sectors':'BOTH_INCLUDED',
      'alpha_lower_bound':'4/sqrt(6) + (mu*ell)^2',
      'scope_of_limit':'epsilon down to zero in exp(-epsilon*q2^2/2); clock and density boxes fixed',
      'history_weight_condition':'fixed complex c_C; Cnu=sum_C abs(c_C)<infinity; no divergent regulator prefactor',
      'matrix_order':['A|0|0m','A|0|1m','A|+|0m','A|+|1m'],
      'bound_matrix_per_Cnu':[[str(s.simplify(x)) for x in row] for row in bound.tolist()],
      'max_entry_bound_per_Cnu':str(maximum),'max_entry_bound_decimal':float(maximum),
      'max_abel_error_bound_per_epsilon_Cnu':str(rate),'max_abel_error_bound_decimal':float(rate),
      'density_fourier_factor':'E(k)=exp(-i*k/2)*sinc(k/2), E(0)=1, abs(E)<=1',
      'counterexamples':{
        'coupled_uniform':{'A':'0','J':'1','factor':'(1+epsilon)^(-1/2)','status':'FINITE'},
        'uncoupled_linear':{'A':'r','J':'0','positive_integral_limit':'2*exp(i*pi/4)','positive_status':'FINITE','atom_status':'DIVERGES_AS_epsilon^(-1/2)'},
        'vanishing_coupling':{'A':'0','J':'r','positive_integral':'asinh(1/sqrt(epsilon))','positive_status':'LOG_DIVERGENCE','mixture':'1/(2*sqrt(epsilon))+asinh(1/sqrt(epsilon))/2'},
        'unbounded_clock':{'all_density_atom':'dust action zero','unnormalized_clock_box_integral':'2*L','status':'DIVERGES_AS_L_to_infinity'}},
      'physical_kernel':'NOT_CONSTRUCTED','numerical_physical_entries':None,'physical_gates':GATES,
      'unregulated_full_integral_absolutely_convergent':False,
      'reduced_integral_after_Abel_interior_step_absolutely_convergent':True}

def rendered():return json.dumps(evidence(),indent=2,ensure_ascii=False,sort_keys=True)+'\n'

if __name__=='__main__':
    (ROOT/'results/existence_certificate.json').write_text(rendered(),encoding='utf-8')
