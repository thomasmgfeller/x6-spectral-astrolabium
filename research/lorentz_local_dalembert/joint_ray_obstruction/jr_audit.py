"""Independent series/PMF checks, continuous coverage and dependency controls.
SPDX-License-Identifier: Apache-2.0
"""
from jr_run import *
from decimal import Decimal,localcontext
from math import factorial
from collections import Counter
from ce_common import deform

def small_exact_reference(x,y,a,k):
    """Factorial series and an alternating exponential; no mode recurrence."""
    assert 0<x<=1 and 0<y and x+y<=1 and k>=0
    cutoff=100;s=x+y
    upper=sum(((-s)**j/F(factorial(j)) for j in range(121)),F(0))
    lower=upper-s**121/F(factorial(121))
    poly=F(0)
    for j in range(cutoff+1):
        poly+=x**j/F(factorial(j))*sum((y**n/F(factorial(n)) for n in range(k+a*j+1)),F(0))
    tail=x**(cutoff+1)/F(factorial(cutoff+1))/(1-x/F(cutoff+2))
    return lower*poly,upper*poly+tail

def decimal_reference(x,y,a,k):
    """Independent 110-digit direct PMF sum, used only as a numerical audit."""
    with localcontext() as ctx:
        ctx.prec=110
        x=Decimal(x.numerator)/Decimal(x.denominator)
        y=Decimal(y.numerator)/Decimal(y.denominator)
        cutoff=800;term=(-y).exp();prefix=[term]
        for j in range(1,k+a*cutoff+1):
            term=term*y/j;prefix.append(prefix[-1]+term)
        term=(-x).exp();answer=Decimal(0)
        for j in range(cutoff+1):
            if k+a*j>=0:answer+=term*prefix[k+a*j]
            term=term*x/(j+1)
        return +answer

def audit():
    frozen();c=read(HERE/'contract.json');cert=read(HERE/'certificate.json');summary=read(HERE/'summary.json')
    small=0
    for x,y in ((F(1,4),F(1,4)),(F(1,2),F(1,4)),(F(1,4),F(1,2))):
        for a,k in ((1,0),(2,1)):
            exact=small_exact_reference(x,y,a,k);bound,_=event(x,y,a,k,c)
            assert bound[0]<=exact[0]<=exact[1]<=bound[1];small+=1
    numerical=0
    for kind in ('base','moved'):
        for row in cert['event_records'][kind]:
            answer=decimal_reference(F(row['x_mean']),F(row['y_mean']),2,787)
            assert Decimal(row['probability'][0])<=answer<=Decimal(row['probability'][1]);numerical+=1
            assert F(row['numerical_width_upper'])<=F(c['numerical_event_width_target'])
            assert all(int(row['normalization'][name]['tail'])>0 for name in ('x','y'))
    # Exact counterexample to factoring overlapping/identical count variables:
    # if X=Y, P(Y-X<=0)=1. Independent Poisson(1) copies do not have this law.
    independent,_=event(F(1),F(1),1,0,c)
    assert independent[1]<1
    # Omitting the X tail and renormalizing its finite support changes the law.
    coarse=dict(c,x_upper_steps=1);rough,_=event(F(10),F(15),1,0,coarse)
    fine,_=event(F(10),F(15),1,0,c)
    x=weights(F(10),80,1,32768);y=weights(F(15),80,2048,32768)
    naive=sum((x['hi'][j]*sum(y['hi'][:j+1]) for j in range(x['upper']+1)),0)
    naive=F(naive,x['zlo']*y['zlo'])
    assert x['tail']>0 and naive<fine[0] and rough[0]<=fine[0]<=fine[1]<=rough[1]
    assert event(F(0),F(0),1,0,c)[0]==(F(1),F(1))
    assert event(F(0),F(0),1,-1,c)[0]==(F(0),F(0))
    invalid=0
    for call in [lambda:weights(F(-1),80,512,32768),lambda:weights(F(32769),80,512,32768),
                 lambda:weights(F(1),0,512,32768),lambda:weights(F(1),80,0,32768),
                 lambda:event(F(1),F(1),0,0,c),lambda:event(F(1),F(1),2,0,dict(c,y_upper_steps=1))]:
        try:call()
        except AssertionError:invalid+=1;continue
        raise AssertionError('invalid input accepted')
    assert invalid==6
    b=setup();domain=c['domain'];lo,hi=map(F,domain['h']);r=ray_data(b,15,1,-1);geometric_checks=0
    for row in cert['quadratic_ranges']:
        pair=row['interval'];qr=tuple(map(F,row['moved']))
        assert qr==q_bounds(b,r,*pair,lo,hi)
        # Exact polynomial extrema are the proof; direct reconstructed geometries
        # at endpoints and midpoint audit its implementation independently.
        for h in (lo,(lo+hi)/2,hi):
            z=deform(b['z'],15,1,-1,h);q=interval(z,*pair)
            assert qr[0]<=q<=qr[1];geometric_checks+=1
            assert b['boost'][2][0]<b['boost'][15][0]<b['boost'][1][0]
    for i,row in enumerate(cert['quadratic_ranges']):
        assert cert['base_mean_intervals'][i]==[str(v) for v in mean_bounds(b,(F(row['base']),)*2)]
        assert cert['moved_mean_intervals'][i]==[str(v) for v in mean_bounds(b,tuple(map(F,row['moved'])))]
    archive=read(HERE.parent/'continuous_energy'/'cells.json.gz')
    cells={(v['ray'],v['path']):v for v in archive['cells']};assert len(cells)==len(archive['cells'])
    parents={tuple(key) for round_ in archive['splits'] for key in round_}
    leaves=[v for key,v in cells.items() if key not in parents]
    assert len(leaves)==8217
    counts=Counter(v['status'] for v in leaves);assert dict(counts)==summary['inherited_states']
    for ray in range(64):
        intervals=sorted((F(v['lo']),F(v['hi'])) for v in leaves if v['ray']==ray)
        assert intervals[0][0]==0 and intervals[-1][1]==F(1,10)
        assert all(a<b for a,b in intervals)
        assert all(a[1]==b[0] for a,b in zip(intervals,intervals[1:]))
    holds=[v for v in leaves if v['status']=='HOLD'];assert len(holds)==30
    for v in holds:
        assert archive['rays'][v['ray']]==[15,1,-1] and lo<=F(v['lo'])<F(v['hi'])<=hi
    for v in leaves:
        if v['status']=='GAP_EXCLUDED':assert F(v['gap_upper'])<=F(1,5)
        if v['status']=='LAW_EXCLUDED':assert F(v['law']['tv_lower'])>F(1,4)
    p=tuple(map(F,cert['base_event_probability']));q=tuple(map(F,cert['moved_event_probability']))
    tv=F(cert['full_law_tv_lower']);assert F(1,4)<tv<=p[0]-q[1]
    assert summary['complete_rays_excluded']==64 and summary['unresolved_intervals']==[]
    return dict(status='PASS',independent_exact_factorial_series_cases=small,
        independent_direct_decimal_pmf_checks=numerical,decimal_precision=110,
        direct_geometry_checks=geometric_checks,complete_continuous_covers=64,
        inherited_terminal_cells=len(leaves),new_joint_event_cells=len(holds),
        dependence_counterexample=True,omitted_tail_negative_control=True,zero_mean_controls=2,
        invalid_inputs_rejected=invalid,
        scope='The proof uses exact disjointness, directed integer probability bounds and the inherited interval cover. Independent series and direct PMF checks audit implementation; no sampling approximation supplies the certificate.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
