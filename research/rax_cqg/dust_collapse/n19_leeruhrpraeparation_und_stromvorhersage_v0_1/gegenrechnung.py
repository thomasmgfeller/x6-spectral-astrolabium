"""Rational complement checks and a separate enclosed linear elimination."""
from fractions import Fraction as F
from itertools import product


def audit(early,clocks,witness,precision):
    from quelle import box,hull
    from gemischt import CLOCK,WEIGHT,FUT,ORDER
    from algebra import gauss_box
    from zustand import nominal
    y,w=nominal(early)[1]
    edges={}
    for i,j in ORDER:
        length=sum((i,k) in ORDER and (k,j) in ORDER for k in y)
        if length<4:
            edges[i,j]=(1,-9,16,-8)[length]
    coordinates=witness['coordinates']

    def matrix(yy):
        # Create columns by applying the nodal flux rule to unit weights or
        # unit far moments. No analytic row matrix from the primary solver.
        result=[]
        for key in coordinates:
            field=key[0];site=int(key[1:])
            G=[box(0) for _ in range(19)]
            for (i,j),c in edges.items():
                if j!=site:
                    continue
                if j in FUT:
                    flow=c if field=='M' else -c*yy[i]
                else:
                    flow=c*(yy[j]-yy[i])
                G[i]+=flow
                G[j]-=flow
            result.append([G[i] for i in CLOCK]+[box(key=='w16')]+G[:4]+
                          [box(key=='M7')-y[7]*int(key=='w7')])
        return list(map(list,zip(*result)))

    # Check the strongest family by reconstructing the *absolute* background
    # variables directly; the primary solver used differences from a reference.
    from zustand import gradients
    reference_G=gradients(y,w)[0]
    for member in witness['results']['all_momenta']['backgrounds']:
        yy=y.copy()
        for i in (17,18):
            yy[i]+=hull(*member['dY'+str(i)])
        coeff=matrix(yy)
        known={i:(box(0) if i in WEIGHT+FUT else ww) for i,ww in w.items()}
        current=gradients(yy,known)[0]
        rhs=[-current[i] for i in CLOCK]+[w[16]]+[reference_G[i]-current[i] for i in range(4)]+[box(0)]
        absolute=gauss_box(coeff,rhs)
        for k,v in zip(coordinates,absolute):
            i=int(k[1:])
            start=w[i] if k[0]=='w' else w[i]*y[i]
            first=start+hull(*member['delta_weights_and_far_moments'][k])
            assert (first-v).contains_zero()
    # Independent rational test of the eliminated pulse formula. Use an arbitrary
    # receiver shift and adjust its density source (irrelevant to the identity).
    checked=0
    for d,q in product((F(-1,1000),F(1,1000)),(F(-1,2000),F(1,2000))):
        u,s,h,t,mz,wz,wr=map(F,('-5/2','1/4','-9/2','3/10','-1/2','1/15','1/36'))
        f0=wz*mz/(h-s)-wr
        wr_new=wr*(t-h)/(t+q-h)
        wz_new=wz+(-d*f0+wr_new*(t+q-s-d)-wr*(t-s))/mz
        direct=wz_new*(s+d-u)-wz*(s-u)
        compressed=wz*d*(1+(s+d-u)/(s-h))+wr*q*(s+d-u)*(s+d-h)/(mz*(t+q-h))
        assert direct==compressed
        checked+=1
    assert [r['both_windows'] for r in clocks['tests']]==[False,False,True,True,True]
    for row in precision['bounds']:
        assert F(row['max_relative_error']) < F(12,10**6)
    return {'second_interval_elimination':'absolute weights and moments',
            'strong_backgrounds_checked':2,'independent_unknowns_each':17,
            'rational_flux_identities':checked,
            'relative_error_below_12_per_million_for_both_pulses':True}
