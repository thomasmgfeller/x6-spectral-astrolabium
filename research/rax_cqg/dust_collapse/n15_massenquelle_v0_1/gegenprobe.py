"""Independent operational checks on type 2324. Python standard library."""
import cmath
from fractions import Fraction as Q
from itertools import combinations, product
import json
import math

import massenquelle as study

P, I, F = study.P, study.I, study.F
Delta = float((study.support.DELTA[0] + study.support.DELTA[1]) / 2)
paths = ((4, 11), (4, 13), (5, 12), (6, 11), (14,))


def direct_relations():
    links = set()
    for path in paths:
        chain = P + path + F
        links.update(zip(chain, chain[1:]))
    future = [{b for a,b in links if a == i} for i in range(15)]
    for k in range(15):
        for i in range(15):
            if k in future[i]:
                future[i] |= future[k]
    weights = {}
    for i in range(15):
        for j in future[i]:
            mid = sum(v in future[i] and j in future[v] for v in range(15))
            weights[i,j] = (1, -9, 16, -8)[mid] if mid < 4 else 0
    return weights


def independent_source(y, w, edges):
    """Hessian contraction of the action, evaluated on every active edge."""
    u = [int(i in P) for i in range(15)]
    v = [76, 47, 24, 8] + [0]*11
    numerator = -sum(b*w[j]*(u[i]-u[j])*(v[i]-v[j]) for (i,j),b in edges.items())
    return numerator / (64*(y[7]-y[3]))


def source_and_phase(m, e, jitter, density_jitter, rho, edges):
    y = [Q(i-5) for i in range(15)]
    y[3] += e
    base = [Q(1,3)]*3 + [Q(2,3)]*3 + [Q(1,2)]
    u = {v:k+(-1)**v*jitter for v,k in zip(I,base)}
    f = dict.fromkeys(I,Q(0))
    for route in paths:
        mids = [Q(0)]+[(u[i]+u[j])/2 for i,j in zip(route,route[1:])]+[Q(1)]
        for v,a,b in zip(route,mids,mids[1:]):
            f[v] += (b-a)/len(paths)
    assert sum(f.values())==1
    w = [Q(0)]*15
    for j in I:
        y[j] = y[3]+(4-e)*u[j]
        w[j] = m*(4-e)*f[j]*(1+density_jitter*(-1)**j)
    # The physical collar weights cancel identically from the source Hessian.
    x = independent_source(y,w,edges)
    assert x == study.read_boundary(y,lambda shifted:study.action(shifted,w,edges),study.STEPS[1])
    physical=[float(rho) if i in P else 0.125 if i in F else Delta*float(w[i]) for i in range(15)]
    dust=-sum(physical)/2-sum(b*physical[j]*float(y[j]-y[i])**2 for (i,j),b in edges.items())/38
    return float(x),dust


def run():
    edges=direct_relations()
    assert edges==study.layer_coefficients(2324)
    out=[]
    for mass,rho in product((Q(0),Q(1,4),Q(1),Q(4)),(Q(1,8),Q(1,4))):
        a_minus=a_plus=0j
        count=0
        # Explicit positive atomic measure within the finite tube, including density endpoints.
        for e,j,d,r in product((Q(-1,3),Q(-1,6),Q(1,6),Q(1,3)),
                               (Q(-1,64),Q(1,64)),(-study.ETA,study.ETA),(-1,1)):
            x,s = source_and_phase(mass,e,j,d,rho+r*Q(1,32),edges)
            half=float(study.G)*x/2
            a_minus+=cmath.exp(1j*(s-half)); a_plus+=cmath.exp(1j*(s+half))
            count+=1
        a_minus/=count; a_plus/=count
        coherence=2*a_minus.conjugate()*a_plus/(abs(a_plus)**2+abs(a_minus)**2)
        reconstructed=cmath.phase(coherence)/float(study.G)
        assert abs(reconstructed-float(mass)) <= float(mass)*0.02+1e-14
        if mass==0:
            assert reconstructed==0
        out.append({"mass":str(mass),"input_density":str(rho),"histories":count,
                    "mass_from_xy":round(reconstructed,12),"pointer_visibility":round(abs(coherence),12)})
    return out


if __name__=='__main__':
    if not __debug__: raise RuntimeError("Run without -O")
    print(json.dumps(run(),indent=2))
