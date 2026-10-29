"""Independent identities, negative controls and higher-precision enclosure replay."""
import argparse
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import numpy as np
from flint import arb, acb, ctx
from balls import HERE, plan, configure, integrate, real_value, decode, encode, write
import budget
import source

def check(ok,message):
    if not ok:
        raise RuntimeError('FAIL: '+message)

def controls():
    out={}; coefficients=[1,-9,16,-8]
    def w(n,e):
        return sum(Q(coefficients[j])*math.comb(n,j)*e**j*(1-e)**(n-j)
                   for j in range(min(3,n)+1))
    count=0
    for e in [Q(1),Q(1,2),Q(1,16),Q(1,256)]:
        for n in range(65):
            value=w(n,e); delta=w(n+1,e)-value
            check(abs(value)<=16,'convex weight envelope')
            check(abs(delta)<=25*e,'coupled add-one envelope')
            # Independent binomial coupling, using the extended coefficient list.
            c=coefficients+[0]*66
            independent=e*sum(Q(c[j+1]-c[j])*math.comb(n,j)*e**j*(1-e)**(n-j)
                              for j in range(n+1))
            check(delta==independent,'exact binomial add-one identity')
            count+=1
    check(w(2,Q(1))-w(1,Q(1))==25,'sharp increment 25 at epsilon=1')
    out['exact_rational_weight_and_coupling_cases']=count
    # The s integral of s^(2j)*(v-s)^2 and subsequent v integral.
    for j,expected in [(0,Q(1)),(1,Q(1,20)),(2,Q(1,105))]:
        coefficient=Q(24)*sum(Q(c,2*j+i+1) for i,c in enumerate([1,-2,1]))/Q(2*(4*j+4))
        check(coefficient==expected,'diamond moment '+str(j))
    out['exact_diamond_moments']=3
    # Independent integration in v verifies the Bessel K reduction, with a
    # separately bounded v>H tail; this is an enclosure comparison, not a fit.
    for ell in [.5,1.5]:
        q=arb(ell)**-4; c=(arb.pi()*q/24).sqrt(); L=arb(2); H=arb(24)
        for y in [.125,1,4]:
            b=arb(y)/c; z=b/(2*L*L)
            exact=b*(z.bessel_k(1)-z.bessel_k(0))
            f=lambda v,analytic: (v-b/v)**2/v*(-(v*v+b*b/(v*v))/(4*L*L)).exp()
            direct=real_value(integrate(f,b.sqrt(),H))
            tail=2*L*L*(-H*H/(4*L*L)).exp()
            bounded=direct+arb(0,tail.upper())
            check(bounded.overlaps(exact),'independent Bessel reduction')
    out['bessel_reduction_cases']=6
    # Independent exact KG plane modes test the light-cone boundary term/sign.
    count=0; negative=0
    for tau in [.25,.5,1.5]:
        tau=arb(tau)
        for k in [0,1,4]:
            for m in [0,1,2]:
                exact=(tau*(arb(k*k+m*m)).sqrt()).cos()
                K=(k*tau).cos(); surface=m*m*tau*tau/2*(k*tau).sinc()
                f=lambda r,analytic: r*r*(k*r).sinc()*(-m*m*(tau*tau-r*r)/4).hypgeom_0f1(3)
                integral=real_value(integrate(f,0,tau))
                value=K-surface+arb(m)**4*tau/8*integral
                check(value.overlaps(exact),'KG plane-mode identity')
                if m and k==0:
                    check(not (value+2*surface).overlaps(exact),'wrong surface sign rejected')
                    negative+=1
                count+=1
    out['exact_KG_plane_modes']=count; out['wrong_sign_negative_controls']=negative
    A,_,_=source.normalization(ctx.prec)
    positive,_,_=source.kirchhoff([-.5,0,0,.5],A)
    negative,_,_=source.kirchhoff([-.5,0,0,-.5],A)
    check(positive.overlaps(negative.conjugate()),'source reflection conjugation')
    for point in [[0,0,0,0],[.5,0,0,.5],[-.5,0,0,0]]:
        z,_,_=source.kirchhoff(point,A);check(z.is_zero(),'exact Huygens boundary/support')
    check(source.kirchhoff([-1,0,0,0],A)[0].overlaps(acb(A/arb(1).exp())),'Cauchy initial value')
    for point in [[-.5,0,0,.5],[.5,0,0,.5]]:
        reflected=[-2-point[0],*point[1:]]
        check(source.kirchhoff(point,A)[0].overlaps(source.kirchhoff(reflected,A)[0]),'time reversal')
    rejected=0
    for operation in [lambda:budget.variance_upper(.125,24,1),
                      lambda:source.massive_center([0,0,0,.5],1,A)]:
        try: operation()
        except ValueError: rejected+=1
    check(rejected==2,'inadmissible smoothing and unsupported massive probes rejected')
    out['boundary_symmetry_initial_controls']=7;out['scope_negative_controls']=rejected
    return out

def replay():
    from run import frozen
    frozen(); configure(plan()['replay_precision_bits'])
    oldbudget=json.loads((HERE/'results/BUDGET.json').read_text())
    newbudget=budget.compute()
    check(len(newbudget['rows'])==len(oldbudget['rows'])==7,'fixed budget matrix')
    for old,new in zip(oldbudget['rows'],newbudget['rows']):
        for key in ['mean_infinite','relative_bias','relative_boundary_bound',
                    'expected_N_admissibility_min']:
            check(decode(old[key]).overlaps(decode(new[key])),'higher-precision overlap '+key)
        for key in ['ell_k','H','witness_status','rho_sufficient_for_stochastic_RMS',
                    'single_witness_total_RMS_within_goal','witness_RMS_target_impossible_at_chosen_H']:
            check(old[key]==new[key],'stable budget decision '+key)
        # Upper bounds chosen from enclosure endpoints are not enclosures of
        # one common exact number. Precision may legitimately improve them.
        for record in [old,new]:
            if record['single_witness_total_RMS_within_goal']:
                check(decode(record['relative_RMS_upper_at_sufficient_density']).real
                      <= arb(plan()['gaussian']['relative_total_RMS_goal']),
                      'replayed sufficient RMS inequality')
    oldsource=json.loads((HERE/'results/SOURCE.json').read_text());newsource=source.compute()
    check(decode(oldsource['normalization_A']).overlaps(decode(newsource['normalization_A'])),'normalization replay')
    check(len(oldsource['rows'])==len(newsource['rows'])==34,'fixed source matrix')
    for old,new in zip(oldsource['rows'],newsource['rows']):
        check((old['probe_index'],old['mass'])==(new['probe_index'],new['mass']),'source identity')
        check(decode(old['value']).overlaps(decode(new['value'])),'higher-precision source overlap')
        check(new['enclosure_status']==old['enclosure_status']=='WITHIN_RADIUS_GOAL','source radius goal')
    # Compare the new witness to the independently computed v0.2 double integral.
    mrows=json.loads((HERE.parent/'scale_calibration_v0_2/results/MEAN.json').read_text())['rows']
    vals=np.load(HERE.parent/'scale_calibration_v0_2/results/mean.npz')['values']
    comparisons=0
    for new in newbudget['rows']:
        indices=[i for i,r in enumerate(mrows) if r['L']==2 and r['H']==64 and r['ell_k']==new['ell_k']]
        if indices:
            diff=(decode(new['mean_infinite'])-acb(complex(vals[indices[0],-1,0]))).abs_upper()
            check(diff<arb('1e-7'),'legacy double-quadrature regression')
            comparisons+=1
    return {'budget_rows':7,'reference_amplitudes':34,'precision_bits':ctx.prec,
            'legacy_mean_regressions':comparisons,'claim':'each enclosure is independently computed; overlap is a regression check, not the enclosure proof'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--replay',action='store_true')
    ap.add_argument('--output',type=Path);a=ap.parse_args();configure()
    result={'controls':controls(),'software_status':'PASS','G1':'HOLD','full_reference':'HOLD'}
    if a.replay:result['replay']=replay()
    if a.output:write(a.output,result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
