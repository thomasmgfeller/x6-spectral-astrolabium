"""Certify nonzero coherent dust norm for the single-path marker comparisons."""
from fractions import Fraction as Q
from itertools import product
import json

import massenquelle as study

iv=study.zweifenster
point=iv.interval
P,I,F=study.P,study.I,study.F


def square(value):
    lo,hi=value.lo,value.hi
    return iv.Interval(0 if lo<=0<=hi else min(lo**2,hi**2),max(lo**2,hi**2))


def phase_bounds(e,k,m,delta,rho,edges):
    y={i:point(i-5) for i in P+F}
    y[3]+=e
    others=[j for j in I if j not in (4,13)]
    u={j:point(Q(1,2)+Q(index,2*(len(others)+1))) for index,j in enumerate(others,1)}
    u[4],u[13]=point(Q(1,2))-k,k
    for j in I:
        y[j]=y[3]+(4-e)*u[j]
    w={j:point(Q(0)) for j in I}
    w[4],w[13]=m*delta*(4-e)/4,3*m*delta*(4-e)/4
    for j in F:w[j]=point(Q(1,8))
    slopes={j:point(Q(-1,2)) for j in range(15)}
    for (i,j),b in edges.items():
        slopes[j]-=Q(b,38)*square(y[j]-y[i])
    entrance=iv.Interval(rho-Q(1,32),rho+Q(1,32))
    return entrance*sum(slopes[i] for i in P)+sum(w[j]*slopes[j] for j in I+F)


def run():
    delta=iv.Interval(*study.support.DELTA)
    mu,nu=iv.moments(delta)
    edges=study.layer_coefficients(2324)
    output={}
    for mode,rho in product(('baseline','same_means','same_curve'),(Q(1,8),Q(1,4))):
        mass=Q(1) if mode=='baseline' else Q(19,20)
        bounds=[]
        for lo,hi in study.support.WINDOWS:
            sign=1 if hi<0 else -1
            a=4+23*nu+sign*93*mu;b=48+3*nu+sign*24*mu
            for n in range(16):
                width=(hi-lo)/16
                e=iv.Interval(lo+n*width,lo+(n+1)*width)/delta
                if mode=='baseline':
                    k=point(Q(3,8))
                elif mode=='same_means':
                    k=((a+b*Q(3,8))/mass-a)/b
                else:
                    k=iv.Interval(study.rival_profile(e.hi),study.rival_profile(e.lo))
                assert Q(1,4)<k.lo<=k.hi<Q(1,2)
                bounds.append(phase_bounds(e,k,mass,delta,rho,edges))
        span=max(v.hi for v in bounds)-min(v.lo for v in bounds)
        floor=1-span**2/8
        assert floor>0
        output[mode+';'+str(rho)]={
            'phase_span_upper':str(span),'modulus_lower':str(floor),'exact_probe_phase':str(study.G*mass)}
    return output


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Active assertions required.')
    print(json.dumps(run(),indent=2,sort_keys=True))
