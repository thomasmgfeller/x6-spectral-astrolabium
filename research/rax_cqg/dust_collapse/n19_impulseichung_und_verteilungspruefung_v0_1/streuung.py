"""Blind early readout, population-moment identities, and genuine N19 misclassification controls."""
from fractions import Fraction as F
from itertools import product
from eichen import KS
from intervall import I,interval

B=F(1,10**12)
V=F(1,10**14)
K0=F(1,10**11)
FOCUS=F(250)
STEP=2*B


def round_code(q,step=STEP):
    f=F(q)/step+F(1,2)
    return f.numerator//f.denominator


def calibrator_moments():
    # These are population moments of explicit finite laws, with exact
    # weights; no inference from a finite laboratory sample is made here.
    out=[]
    for corr in (F(0),F(1,4),F(-1,4)):
        xy=[(F(x,3),F(y,3)+corr*F(x,3),F(1,4)) for x,y in product((-1,1),repeat=2)]
        moment=lambda t,n:sum(prob*(x+t*y)**n for x,y,prob in xy)
        a=moment(0,2)
        c=(moment(1,2)-moment(-1,2))/4
        d=(moment(1,2)+moment(-1,2))/2-a
        assert (a,c,d)==tuple(sum(p*f(x,y) for x,y,p in xy) for f in
                             (lambda x,y:x*x,lambda x,y:x*y,lambda x,y:y*y))
        weights={0:F(5,6),1:F(1,18),-1:F(1,18),2:F(1,36),-2:F(1,36)}
        radial=sum(p*(x*x+y*y)**2 for x,y,p in xy)
        assert sum(w*moment(t,4) for t,w in weights.items())==radial
        # Treat position codes as intervals, obtain conservative raw second moments.
        errors=[]
        for g in (1,32):
            def display(t):
                accum=interval(0)
                for x,y,p in xy:
                    code=round_code(g*B*(x+t*y))
                    lo,hi=(F(2*code+sign,2)*STEP/(g*B) for sign in (-1,1))
                    accum+=p*I(lo,hi).square()
                return accum
            ma,mm,mp=(display(t) for t in (0,-1,1))
            rec=[ma,(mp-mm)/4,(mp+mm)/2-ma]
            assert all(v.overlaps(true) for v,true in zip(rec,(a,c,d)))
            errors.append({'gain':g,'normalized_raw_second_moment_intervals':[v.data() for v in rec]})
        out.append({'slope':str(corr),'normalized_second_moments':list(map(str,(a,c,d))),
                    'radial_fourth':str(radial),'rounding_test':errors})
    return out


def run(prev,early):
    from quelle import box
    from proben import samples
    from ensemble import local_read
    from staubgeraet import solve,verify
    from wege import ROUTES
    arch= samples(prev,early)[0]
    name,y,w=arch[0]
    assert name=='reference'
    a=F(64)
    spike=1/(9*a*a)
    assert spike*a*a==F(1,9)
    # Each of six normalized coordinates independently has the same law.
    # Keep only the two atoms where b_u is nonzero and all other entries vanish.
    one_sign=spike*(1-spike)**5/2
    failures=[]
    for route in ROUTES:
        for k in KS:
            # Nominal matched apparatus or the specified weak, uncompensated apparatus.
            delta=box(0 if k==1 else -k)
            vel=(box(0),)*3
            st=solve(y,w,0,vel,k,delta,route)
            trial=[]
            for side in (-1,1):
                pos=(box(side*a*B),box(0),box(0))
                history,_=verify(st,0,vel,k,delta,route,pos)
                labels=[local_read(st['y'],history,i) for i in (18,7)]
                assert labels[0]!=0 and labels[1]!=0
                trial.append(list(map(str,labels)))
            failures.append({'route':route,'kappa':str(k),'true_J':'0','two_sites_by_sign':trial})
    # Three unamplified early points are identical on a valid core point and a point outside E<=4.
    blindness=[]
    for k in KS:
        for p in (F(0),K0*V):
            q=F(0);v=p/k
            codes=[round_code(q+j*8*v) for j in range(3)]
            E=((q+FOCUS*p/K0)/B)**2+(p/(K0*V))**2
            assert codes==[0,0,0]
            blindness.append({'kappa':str(k),'p':str(p),'E':str(E),'early_codes':codes})
    return {'target_variance_each_normalized':'1/9','spike_amplitude':'64','nonzero_probability_each':str(spike),
            'wrong_at_both_sites_probability_lower':str(2*one_sign),'actual_n19_failure_witnesses':failures,
            'early_codes_are_ambiguous':blindness,'moments':calibrator_moments(),
            'distribution_free_second_moment_success_lower':'5/6',
            'distribution_free_fourth_moment_success_lower_if_each_radial_fourth_at_most_8_over_81':'53/54'}
