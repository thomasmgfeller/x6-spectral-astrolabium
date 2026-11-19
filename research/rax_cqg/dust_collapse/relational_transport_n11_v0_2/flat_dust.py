"""Finite 1+3 Minkowski patch. Dust/BDG factors only; four fixed quadrature marks per clock."""
from functools import lru_cache
from itertools import product
from math import sin
import cmath
import json
import numpy as np
from ideals import minkowski_order

WEIGHTS = (6,1,1,4)
TIMES = (-.75,.125,.375,1.)
BETA = 4/np.sqrt(6.)
POINTS, PRED = minkowski_order()
N = len(PRED)
ANCESTORS = [tuple(i for i in range(N) if row & 1<<i) for row in PRED]
# Height two: every one of the 12 strict intervals is empty, coefficient b0=1.
GRAVITY = N-sum(len(row) for row in ANCESTORS)


@lru_cache(None)
def local_phase(k,parents):
    c = 1+BETA*sum((TIMES[k]-TIMES[v])**2 for v in parents)/2
    return (1+cmath.exp(-.25j*c)*sin(c/4)/(c/4))/2


def direct():
    assignments = np.array(list(product(range(4),repeat=N)))
    times = np.array(TIMES)[assignments]
    density = np.prod(np.array(WEIGHTS)[assignments]/12,axis=1)
    value = np.ones(len(density),complex)*np.exp(1j*GRAVITY)
    for j in range(N):
        c = np.ones(len(density))
        for i in ANCESTORS[j]:
            c += BETA*(times[:,j]-times[:,i])**2/2
        value *= (1+np.exp(-.25j*c)*np.sinc(c/(4*np.pi)))/2
    return np.dot(density,value)


def one_step(values,old,new):
    """Branch on currently enabled events in topological order; look up no future marks."""
    start = tuple(values)
    def visit(i,amplitude,prob):
        if i==N:
            yield tuple(values),amplitude,prob
            return
        parents = ANCESTORS[i]
        if values[i]>=0 or any(values[j]<0 for j in parents):
            yield from visit(i+1,amplitude,prob)
            return
        # Previously enabled vertices were seen to wait, newly enabled ones were untested.
        lo = old if all(start[j]>=0 for j in parents) else 0
        denom = sum(WEIGHTS[lo:])
        for k in range(lo,new):
            values[i] = k
            local = local_phase(k,tuple(values[j] for j in parents))
            yield from visit(i+1,amplitude*local,prob*WEIGHTS[k]/denom)
        values[i] = -1
        if new<len(WEIGHTS):
            yield from visit(i+1,amplitude,prob*sum(WEIGHTS[new:])/denom)
    yield from visit(0,1+0j,1.)


def causal_route(thresholds):
    seen = set()
    def advance(state,step):
        if step==len(thresholds):
            assert all(k>=0 for k in state) and state not in seen
            seen.add(state)
            return 1+0j,1.,1
        val = 0j
        total = 0.
        leaves = 0
        old = thresholds[step-1] if step else 0
        for next_state,weight,prob in one_step(list(state),old,thresholds[step]):
            w,p,n = advance(next_state,step+1)
            val += prob*weight*w
            total += prob*p
            leaves += n
        return val,total,leaves
    val,mass,n = advance((-1,)*N,0)
    assert n==len(seen)==4**N and abs(mass-1)<1e-12
    return cmath.exp(1j*GRAVITY)*val,mass,n


def compute():
    plain = direct()
    rows = {}
    for tag,ends in (("two_intermediate",(1,2,4)),("three_intermediate",(1,2,3,4))):
        composed,mass,n = causal_route(ends)
        assert abs(plain-composed)<1e-12
        rows[tag] = {"complex":[composed.real,composed.imag],"mass":mass,"completed_histories":n,
                     "abs_gap":abs(plain-composed)}
    return {"clock_nodes":TIMES,"weights_out_of_12":WEIGHTS,"orders_tested":1,
            "strict_timelike_pairs":-GRAVITY+N,"gravity_phase_action":GRAVITY,
            "direct_complex":[plain.real,plain.imag],"routes":rows,
            "scope":"Fixed flat 1+3 fixture, four-node clock quadrature and continuous density marks; no scalar readout or dynamical P3 ensemble."}


if __name__=="__main__":
    print(json.dumps(compute(),indent=2))
