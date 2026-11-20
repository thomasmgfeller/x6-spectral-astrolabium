"""Reference-only and synthetic preflight. No call to the target evaluator."""
from fractions import Fraction as F
from math import factorial
from packet270 import cells, cuts
from study import DENSITIES, TYPES, HERE, REF_RADIUS, TARGET_RADIUS
import json


def qualification(ref,gram):
    assert gram['types']==list(TYPES)
    g,G=F(gram['gram_lower']),F(gram['gram_upper'])
    assert 0<g<=1<=G
    assert set(ref['packets'])==set(map(str,TYPES))
    points=cuts()
    polynomial_checks=[]
    for n in range(6):
        estimate=sum((-1)**k*(r**(n+1)-l**(n+1)) for k,(l,r) in enumerate(zip(points,points[1:])))/(2*(n+1))
        assert abs(estimate)<=6*F(1,2**51)
        polynomial_checks.append(str(estimate))
    assert F(37,1000)**2>F(4,3072)
    target_budget=F(37,1000)*(F(8,32768)+F(1,5000)+6*F(1,2**51)+F(1,10**8))
    assert target_budget < TARGET_RADIUS
    assert F(37,1000)*(F(8,32768)+F(1,5000))<REF_RADIUS
    maxima={rho:F(0) for rho in DENSITIES}
    minref={rho:F(1) for rho in DENSITIES}
    for j in TYPES:
        pack=ref['packets'][str(j)]
        cfg=pack['coordinate_bounds']
        ls=list(cells(cfg))
        assert sum(h for _,_,h in ls)==1
        qc=cfg['3']
        a,b=F(qc['quadratic_bound']),F(qc['linear_bound'])
        C=sum(a**k*(2*a+b)**(6-2*k)/(factorial(k)*factorial(6-2*k)) for k in range(4))/64
        for i,rho in enumerate(DENSITIES):
            lo,hi=map(F,pack['densities'][i]['modulus_interval'])
            assert pack['densities'][i]['density']==rho and 0<lo<=hi
            minref[rho]=min(minref[rho],lo)
            maxima[rho]=max(maxima[rho],G*C**2/(g*768*lo**2))
    return {'prefix':270,'positive_reference_denominators':22,'cell_inequalities':77,
            'min_reference_moduli_by_density':{r:str(v) for r,v in minref.items()},
            'gram_lower':str(g),'gram_upper':str(G),'target_radius':str(TARGET_RADIUS),
            'target_error_budget_upper':str(target_budget),
            'reference_only_analytic_ratio_upper':{r:str(v) for r,v in maxima.items()},
            'synthetic_signed_moment_residuals':polynomial_checks,'modulated_target_values_read_or_evaluated':0}


if __name__=='__main__':
    import argparse
    from pathlib import Path
    from study import write_fresh
    if not __debug__:raise SystemExit('Keep assertions enabled.')
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    write_fresh(args.output,qualification(json.loads((HERE/'reference.json').read_text()),
                                          json.loads((HERE/'gram/gram.json').read_text())))
