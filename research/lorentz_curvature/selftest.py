"""Independent small-order, exact Ricci and sampler checks; no target namespace."""
from fractions import Fraction as F
from itertools import combinations
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.stats import binomtest
from geometry import sample, relation, oracle, flat_density_twin_relation, require
from core import features, validate, pack, unpack


def brute(c):
    counts = []
    for k in range(2, 5):
        counts.append(sum(all(c[i,j] or c[j,i] for i,j in combinations(sub,2)) for sub in combinations(range(len(c)),k)))
    h = max(k for k in range(1, len(c)+1) if any(all(c[i,j] or c[j,i] for i,j in combinations(sub,2)) for sub in combinations(range(len(c)),k)))
    return counts+[h]


def reject(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError('invalid relation accepted')


def ricci_exact(h, eta):
    # Direct contraction of Christoffels and derivatives; independent of oracle().
    q, qp = h/(1-h*eta), h*h/(1-h*eta)**2
    gamma = np.full((4,4,4), F(0), dtype=object)
    derivative = gamma.copy()
    for tensor, val in [(gamma,q),(derivative,qp)]:
        tensor[0,0,0] = val
        for i in range(1,4):
            tensor[0,i,i] = tensor[i,0,i] = tensor[i,i,0] = val
    ricci = np.full((4,4), F(0), dtype=object)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                ricci[a,b] += (derivative[c,a,b] if c == 0 else 0) - (derivative[c,a,c] if b == 0 else 0)
                for d in range(4):
                    ricci[a,b] += gamma[c,c,d]*gamma[d,a,b] - gamma[c,b,d]*gamma[d,a,c]
    factor = 1/(1-h*eta)
    metric = np.diag([F(-1),F(1),F(1),F(1)])*factor**2
    require(bool(np.all(ricci == 3*h*h*metric)), 'exact Ricci contraction')
    require(sum(ricci[i,i]/metric[i,i] for i in range(4)) == 12*h*h, 'exact scalar curvature')


def run():
    count = 0
    for h in [F(0),F(1,4),F(3,4),F(5,4)]:
        for t in [F(-1,4),F(0),F(1,4)]:
            ricci_exact(h,t); count += 1
        o=oracle(float(h))
        tau=quad(lambda t:1/(1-float(h)*t),-.5,.5,epsabs=1e-13)[0]
        require(abs(tau-o['proper_time']) < 2e-13, 'independent proper time integral')
        nodes,weights=np.polynomial.legendre.leggauss(96)
        vol=0.
        for lo,hi in [(-.5,0),(0,.5)]:
            t=lo+(nodes+1)*(hi-lo)/2
            vol += float(np.dot(weights,(4*math.pi/3)*(.5-np.abs(t))**3/(1-float(h)*t)**4))*(hi-lo)/2
        require(abs(vol-o['volume'])<2e-13,'independent volume quadrature')
    rng=np.random.default_rng(830127)
    for i in range(24):
        x,_=sample(rng,8,dict(h=[0.,.25,.75,1.25][i%4]))
        c=relation(x); f=features(c)
        require([f['C2'],f['C3'],f['C4'],f['H']]==brute(c),'exhaustive subsets')
        perm=rng.permutation(len(c))
        require(features(c[np.ix_(perm,perm)])==f,'relabel invariance')
        require(np.array_equal(unpack(pack(c),len(c)),c),'relation archive roundtrip')
        require(np.array_equal(c,flat_density_twin_relation(x,1.25)),'independent causal predicate')
    chain=np.triu(np.ones((8,8),dtype=bool),1)
    require([features(chain)['C'+str(k)] for k in range(2,5)]==[math.comb(8,k) for k in range(2,5)],'complete chain counts')
    require(features(np.zeros((8,8),dtype=bool))['H']==1,'antichain height')
    bad=chain.copy();bad[0,2]=False;reject(lambda:validate(bad))
    bad=np.eye(4,dtype=bool);reject(lambda:validate(bad))
    bad=np.zeros((4,4),dtype=bool);bad[0,1]=bad[1,2]=bad[2,0]=True;reject(lambda:validate(bad))
    distribution=[]
    for h in [0.,.25,.75,1.25]:
        x=np.concatenate([sample(rng,128,dict(h=h))[0] for _ in range(20)])
        o=oracle(h)
        for cut in [-.2,0.,.2]:
            density=lambda t:(4*math.pi/3)*(.5-abs(t))**3/(1-h*t)**4
            p=quad(density,-.5,cut,points=[0] if cut>0 else None,epsabs=1e-12)[0]/o['volume']
            pv=float(binomtest(int(np.count_nonzero(x[:,0]<=cut)),len(x),p).pvalue)
            require(pv>1e-6,'development sampler CDF check')
            distribution.append(dict(h=h,cut=cut,p_value=pv))
        radial=np.linalg.norm(x[:,1:],axis=1)/(.5-np.abs(x[:,0]))
        require(abs(float(np.mean(radial**3))-.5)<.035,'conditional spatial volume distribution')
    return dict(status='PASS',exact_Ricci_cases=count,exhaustive_orders=24,relabel_cases=24,
                sampler_checks=distribution,meaning='Development checks only; no target namespace used')


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
