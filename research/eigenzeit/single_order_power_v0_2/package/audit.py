"""Independent floating reference checks, structural controls and exact expected decisions."""
from fractions import Fraction as Q
from math import sqrt, erfc, comb, log, ceil
from io import BytesIO
import json
import numpy as np
from scipy.stats import binom
from scipy.special import roots_legendre
from decision import DESIGN, thresholds, classify
from apply_order import observed_count
from certificate import normal_tail,binomial_enclosures

def main(result):
    for n in (5,16,33):
        for p in (Q(1,10),Q(1,2),Q(7,8)):
            left,right=binomial_enclosures(n,p,1,n-1)
            mass=[comb(n,k)*p**k*(1-p)**(n-k) for k in range(n+1)]
            assert left[0]<=sum(mass[:2])<=left[1] and right[0]<=sum(mass[-2:])<=right[1]
    for k in range(161):
        z=Q(k,40)
        assert float(normal_tail(z))+1e-14>=.5*erfc(float(z)/sqrt(2))
    for method in ('full_order','matching'):
        n=DESIGN[method]['n'];_,lo,hi=thresholds(method)
        for count,k in [(lo,1),(lo+1,2),(hi-1,2),(hi,1)]:assert len(classify(method,n,count))==k
        for count in (-1,thresholds(method)[0]+1,1.5):
            try:classify(method,n,count)
            except ValueError:continue
            raise AssertionError('bad count accepted')
    for sample in (b'',b'\x01\x00',b'\x00\x00\x00',b'\x80\x00'):
        try:observed_count(BytesIO(sample),2)
        except ValueError:continue
        raise AssertionError('invalid encoding accepted')
    assert observed_count(BytesIO(b'\x02\x00'),2)[0]==1
    x,w=roots_legendre(120);u=x[:,None];v=x[None,:]
    weight=3/8*(u-v)**2*w[:,None]*w[None,:]
    flat_g=(((1+u)*(1+v))**2+((1-u)*(1-v))**2)/16
    assert abs(np.sum(weight*flat_g)-.1)<1e-12 and abs(np.sum(weight*flat_g**2)-.02)<1e-12
    check=[];n=DESIGN['full_order']['n']
    for i,row in enumerate(result['full']):
        pl,pu,vl,vu=map(lambda a:float(Q(a)),row['parameter_enclosures'])
        dl,du=map(lambda a:float(Q(a)),row['density_enclosure']);m3=float(Q(row['third_abs_upper']))
        quadrature=du*np.sum(weight*np.maximum(pu-dl*flat_g,du*flat_g-pl)**3)
        assert quadrature<m3
        op=DESIGN['full_order'];lo=float(Q(op['reject_curved_U_le']));hi=float(Q(op['reject_flat_U_ge']))
        for kind,gap in [('alpha',hi-pu if i==0 else pl-lo),('miss',lo-pu if i==0 else pl-hi)]:
            _,k,_,_,_=row[kind+'_terms'];r=int(k)*float(Q(op['residual_step']))
            vr=2*(pu*(1-pu)-2*vl)/(n*(n-1))
            ref=.5*erfc((gap-r)*sqrt(n)/(2*sqrt(2*vu)))+.3328*(m3/vl**1.5+.429)/sqrt(n)+vr/(vr+r*r)
            upper=float(Q(row[kind+'_terms'][0]))
            assert ref<=upper+1e-14 and upper-ref<1e-5
        m,l,k=thresholds('matching')
        checkrow=result['matching'][i]
        alpha=binom.sf(k-1,m,pl) if i==0 else binom.cdf(l,m,pl)
        power=binom.cdf(l,m,pl) if i==0 else binom.sf(k-1,m,pl)
        assert abs(alpha-float(Q(checkrow['null_error_upper'])))<1.1e-9
        assert abs(power-float(Q(checkrow['power_lower'])))<1.1e-9
        check.append(dict(h=row['h'],numeric_third_moment_envelope=round(float(quadrature),12)))
    a=result['necessary']
    assert ceil(log((.2+sqrt(.19))**2)/log(float(Q(a['affinity_squared_lower']))))==a['minimum_not_excluded']
    return dict(status='PASS',normal_checks=161,exact_toy_binomial_cases=9,
                integer_sides_checked=8,third_moment_quadrature=check,
                checks='flat analytic first two moments, 4 full-order risk bounds, 4 matching tails, affinity cut, corrupt packed inputs')
if __name__=='__main__':
    import sys
    with open(sys.argv[1]) as f:print(json.dumps(main(json.load(f)),indent=2))
