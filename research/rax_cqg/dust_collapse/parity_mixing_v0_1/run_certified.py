"""Replay rigorous finite mixing witness; no network or stochastic sampling.

Shared finite sums contract the two output-clock axes of the 5D tensor rule.
Arb bounds all numerical arithmetic; a proved analytic tail is added separately.
"""
import argparse
import json
from time import monotonic
from flint import arb,acb,ctx
from core import *

class DustQuadrature:
    def __init__(self,n):
        self.n=n
        rule=[arb.legendre_p_root(n,k,weight=True) for k in range(n)]
        self.t=[r[0] for r in rule];self.w=[r[1]/2 for r in rule]
        assert all(w>0 for w in self.w) and sum(self.w).contains(1)
        # Multiply explicitly: arb's general real power can reject a ball
        # straddling zero, even for an integer-valued exponent.
        self.dd=[[(x-y)*(x-y)*beta()/4 for y in self.t] for x in self.t]
        assert all(v.is_finite() for row in self.dd for v in row)
        self.cache={};self.evaluations=0

    def output_factor(self,coefficients,indices):
        items=tuple(sorted((c,i) for c,i in zip(coefficients,indices) if c))
        mirrored=tuple(sorted((c,self.n-1-i) for c,i in items))
        key=min(items,mirrored)
        if key not in self.cache:
            result=acb(0)
            for l,w in enumerate(self.w):
                k=arb(1)/2+sum(c*self.dd[l][i] for c,i in key)
                result+=w*E(k)
            self.evaluations+=self.n
            if not result.is_finite():raise ArithmeticError('non-finite output-clock factor')
            self.cache[key]=result
        return self.cache[key]

    def evaluate(self,code):
        coeff=pair_coefficients(code)
        pred=[i for i,j,c in coeff if j==2]
        output=[[next((c for i,j,c in coeff if i==a and j==x),0) for a in (0,1,2)] for x in (3,4)]
        result=acb(0)
        for i,wi in enumerate(self.w):
            for j,wj in enumerate(self.w):
                for k,wk in enumerate(self.w):
                    inds=(i,j,k)
                    k2=arb(1)/2+sum(self.dd[k][inds[a]] for a in pred)
                    f=self.output_factor(output[0],inds)
                    g=self.output_factor(output[1],inds)
                    result+=wi*wj*wk*(1+E(k2))*(f+g+f*g)
        if not result.is_finite():raise ArithmeticError('non-finite dust quadrature')
        return result/(16*arb(3).sqrt())

def summarize(raw,error):
    if not raw.is_finite() or not error.is_finite():raise ArithmeticError('non-finite amplitude or error')
    enclosed=widen(raw,error)
    round_radius=(raw.real.rad()**2+raw.imag.rad()**2).sqrt()
    return {'quadrature_ball':pack(raw),'analytic_quadrature_error_bound':error.str(25,more=True),
            'arithmetic_complex_radius_bound':round_radius.str(25,more=True),
            'certified_ball':pack(enclosed),'absolute_value':abs(enclosed).str(25,more=True),
            'absolute_value_lower_bound':enclosed.abs_lower().str(25,more=True),
            'phase_radians':enclosed.arg().str(25,more=True),
            'classification':'NONZERO' if enclosed.abs_lower()>0 else 'UNRESOLVED'}

def compute(n=40,precision=128,progress=True):
    if not isinstance(n,int) or n<2 or not isinstance(precision,int) or precision<64:
        raise ValueError('integer n>=2 and precision>=64 required')
    ctx.prec=precision
    quadrature=DustQuadrature(n);ref,pivots_ref,alpha_ref=scalar_ground(reference_h0())
    totals={k:acb(0) for k in ('coupled','decoupled','difference','dust_only')}
    errors={k:arb(0) for k in totals};records=[];start=monotonic()
    for number,(code,members) in enumerate(orbits().items(),1):
        d=quadrature.evaluate(code);de,degrees=dust_error(code,n)
        scalar,pivots,alpha=scalar_ground(h0(code));phase=acb(0,f4(code)).exp()
        w=arb(len(members))/33
        factors={'coupled':scalar,'decoupled':ref,'difference':scalar-ref,'dust_only':acb(1)}
        for name,factor in factors.items():
            totals[name]+=w*phase*d*factor
            errors[name]+=w*de*abs(factor)
        records.append({'representative':code,'members':members,'multiplicity':len(members),'F4':f4(code),
                        'dust_quadrature_ball':pack(d),'dust_error_bound':de.str(25,more=True),
                        'weighted_degrees':degrees,'scalar_factor':pack(scalar),
                        'scalar_pivots':[pack(p) for p in pivots],'alpha':alpha.str(25,more=True),
                        'coupled_contribution':pack(w*phase*d*scalar),
                        'decoupled_contribution':pack(w*phase*d*ref)})
        if progress:print(f'orbit {number}/10: code={code}, cache={len(quadrature.cache)}, E evaluations={quadrature.evaluations}, elapsed={monotonic()-start:.1f}s',flush=True)
    summary={name:summarize(totals[name],errors[name]) for name in totals}
    c=unpack(summary['coupled']['certified_ball']);d=unpack(summary['decoupled']['certified_ball'])
    delta=unpack(summary['difference']['certified_ball'])
    result={'experiment_id':'CST-DUST-AA-EVEN-MIXING-v0.1','scope':'FINITE_DECLARED_CONTROL_ENSEMBLE_NOT_PHYSICAL_CST_KERNEL',
            'geometry':experiment_geometry(),'quadrature':{'n':n,'precision_bits':precision,'rho':2,
            'effective_tensor_rule':'40^5 nodes per orbit before exact finite-sum contraction' if n==40 else f'{n}^5 nodes per orbit before contraction',
            'cached_output_clock_integrals':len(quadrature.cache),'density_factor_evaluations':quadrature.evaluations},
            'reference_scalar_factor':pack(ref),'reference_scalar_pivots':[pack(p) for p in pivots_ref],
            'reference_alpha':alpha_ref.str(25,more=True),'orbit_results':records,'amplitudes':summary,
            'paired_difference_identity_overlap':(c-d).overlaps(delta),
            'relative_change_abs_delta_over_abs_decoupled':(abs(delta)/abs(d)).str(25,more=True),
            'amplitude_squared_ratio_not_probability':((abs(c)/abs(d))**2).str(25,more=True),
            'Abel_error':0,'history_truncation_inside_declared_family':0,'density_quadrature_error':0,
            'odd_parity_control':'M_(+,1),(0,0)=0 exactly at both lambda endpoints',
            'physical_gates':json.loads((ROOT/'experiment_contract.json').read_text())['physical_gates']}
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=40);p.add_argument('--precision',type=int,default=128)
    p.add_argument('--output',type=Path,default=ROOT/'results/certified_mixing.json');a=p.parse_args()
    result=compute(a.n,a.precision)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
    print(json.dumps(result['amplitudes'],indent=2))
