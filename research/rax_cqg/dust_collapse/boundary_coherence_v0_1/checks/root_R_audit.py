#!/usr/bin/env python3
"""Exact rational-interval propagation for the two terminal scalar records.

Conditional on inherited amplitudes and the independently derived Gaussian
moment enclosures. This does not promote scalar mode outcomes to geometry.
"""
from pathlib import Path
import json
from fractions import Fraction as F
from math import factorial
from root_exact_audit import I, cadd, cmul, cabs2

ROOT=Path(__file__).resolve().parents[1]
raw=json.loads((ROOT/'sources/result_64.json').read_text())
moments=json.loads((ROOT/'checks/r_records_results.json').read_text())
def zbox(z): return (I(*z['real']),I(*z['imag']))
A=[[zbox(z) for z in row] for row in raw['analysis']['amplitudes']]
eta=[zbox(moments['eta_by_class'][str(c)]) for c in (1,2)]
gain2=F(1,1024**2)
results=[]
checks={}
probabilities=[]
phase_zero_probabilities=[]
# Independent exact rational Taylor enclosures on the real argument 16.
# For each finite real Taylor polynomial, the next-derivative bound is <=1.
# This implements removal of F4 phases only, with no numerical quadrature.
cos16=sum((F((-1)**j*16**(2*j),factorial(2*j)) for j in range(81)),F(0))
sin16=sum((F((-1)**j*16**(2*j+1),factorial(2*j+1)) for j in range(81)),F(0))
cos_error=F(16**161,factorial(161))
sin_error=F(16**162,factorial(162))
rotation=(I(cos16-cos_error,cos16+cos_error),I(-sin16-sin_error,-sin16+sin_error))
for k,row in enumerate(A):
    variants={}
    p_values={}
    for coherent in (False,True):
        q=[]
        records=[]
        for j in range(2):
            total=I(0)
            for s in range(2):
                x,y=row[s],row[s+2]
                if j:
                    x,y=cmul(eta[0],x),cmul(eta[1],y)
                val=cabs2(cadd(x,y)) if coherent else cabs2(x)+cabs2(y)
                records.append({'R_record':['f0','f2'][j],'stratum':['atom','positive'][s],'raw_weight':val.out(),'unconditional':(gain2*val).out()})
                total+=val
            q.append(total)
        Z=q[0]+q[1]
        p2=q[1]/Z
        key='coherent' if coherent else 'dephased'
        p_values[key]=p2
        variants[key]={'R2_given_success':p2.out(),'R0_given_success':(q[0]/Z).out(),'success':(gain2*Z).out(),'failure':(1-gain2*Z).out(),'records':records}
        checks[f'input{k}_{key}_positive_normalizer']=Z.a>0
        checks[f'input{k}_{key}_R_probability_range']=p2.a>0 and p2.b<1
        checks[f'input{k}_{key}_success_below_one']=(gain2*Z).b<1
    d=p_values['coherent']-p_values['dephased']
    checks[f'input{k}_coherent_dephased_contrast_nonzero']=d.nonzero()
    phase_zero_weights=[]
    for j in range(2):
        total=I(0)
        for s in range(2):
            x,y=cmul(rotation,row[s]),row[s+2]
            if j:
                x,y=cmul(eta[0],x),cmul(eta[1],y)
            total+=cabs2(cadd(x,y))
        phase_zero_weights.append(total)
    p_phase0=phase_zero_weights[1]/sum(phase_zero_weights,I(0))
    phase_delta=p_values['coherent']-p_phase0
    checks[f'input{k}_F4_phase_ablation_contrast_nonzero']=phase_delta.nonzero()
    phase_zero_probabilities.append(p_phase0)
    results.append({'input':['g0','gplus'][k],**variants,'coherent_minus_dephased_R2':d.out(),'counterfactual_kappa0_R2_given_success':p_phase0.out(),'kappa1_minus_counterfactual_kappa0_R2':phase_delta.out()})
    probabilities.append(p_values['coherent'])
delta=probabilities[1]-probabilities[0]
checks['coherent_R2_preparation_contrast_nonzero']=delta.nonzero()
checks['uniform_full_E_bound_below_one']=F(moments['direct_coherent_class_sum_effect_norm_upper_exact'])<1
delta0=phase_zero_probabilities[1]-phase_zero_probabilities[0]
interaction=delta-delta0
checks['source_contrast_change_under_F4_ablation_nonzero']=interaction.nonzero()
out={'id':'TWO-R-RECORD-EXACT-RATIONAL-AUDIT-0.1','arithmetic':'Exact Fraction interval operations with outward decimal conversion. Inherited amplitude and Gaussian moment boxes are premises, not regenerated numerical integrals.','phase_ablation':'Multiply class1 by exp(-16i), class2 unchanged: equals removing exp(9i), exp(-7i) up to a global phase. sin/cos via exact rational Taylor polynomials through degree160/161 with real Lagrange remainder. Counterfactual action change, not a physical gravity knob.','physical_scope':'Conditional auxiliary coherent instrument, terminal scalar modes only.','gain':'1/1024','results':results,'delta_R2_gplus_minus_g0':delta.out(),'delta_R2_percentage_points':(100*delta).out(),'counterfactual_kappa0_source_contrast':delta0.out(),'source_contrast_kappa1_minus_kappa0':interaction.out(),'checks':checks,'all_checks_pass':all(checks.values())}
assert out['all_checks_pass'],checks
(ROOT/'checks/root_R_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_pass':True,'checks':len(checks),'R2_given_success':[p.out() for p in probabilities],'delta_R2':delta.out()},indent=2))
