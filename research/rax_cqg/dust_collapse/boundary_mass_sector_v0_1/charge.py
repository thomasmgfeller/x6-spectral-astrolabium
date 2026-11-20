"""Initial cut momentum for the published dust action, with exact order counts."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"inputs/variation_v0_1"))
from variation import current_and_gradient, matter_action, kernel
from gluing import encode

P=(0,1,2,3)
I=(4,5,6,11,12,13,14)
FUT=(7,8,9,10)
UNIT=10**22

def sqrt_down(x):
    return F(isqrt(x.numerator*UNIT**2//x.denominator),UNIT)

def sqrt_up(x):
    low=sqrt_down(x)
    return low if low**2==x else low+F(1,UNIT)

def add(a,b): return a[0]+b[0],a[1]+b[1]
def scale(k,a): return tuple(sorted((k*a[0],k*a[1])))
def mul(a,b):
    vals=[u*v for u,v in product(a,b)]
    return min(vals),max(vals)

def bounds(x): return list(map(str,x))

beta=(4/sqrt_up(F(6)),4/sqrt_down(F(6)))
delta=(sqrt_down(2/(19*beta[1])),sqrt_up(2/(19*beta[0])))
assert 0<delta[0]<=delta[1]<F(1,3)
offsets=tuple(F(i,32) for i in (-3,-1,1,3))

def row(d):
    return tuple(kernel(d+3-i) for i in range(4))

def charge_coefficient(d,off,s):
    b=row(d)
    # p=-Q: p_v/w_v = beta/2 * [sum b_i*T_i - s*sum b_i].
    a=sum(v*(i-5) for i,v in enumerate(b))
    linear=add(scale(a,delta),scale(-sum(b),(s,s)))
    return mul(scale(F(1,2),beta),add(linear,(b[3]*off,b[3]*off)))

def envelope(signature):
    # Linear in each hidden clock and density. Taking the positive part over w in [0,1]
    # leaves a convex upper envelope in the external clock offset; minima are concave.
    allmax,allmin=[],[]
    for off in offsets:
        pos=(F(0),F(0))
        neg=(F(0),F(0))
        for d,n in enumerate(signature):
            vals=[charge_coefficient(d,off,s) for s in (F(-3,2),F(3,2))]
            maxima=tuple(max(F(0),*(v[i] for v in vals)) for i in range(2))
            minima=tuple(min(F(0),*(v[i] for v in vals)) for i in range(2))
            pos=add(pos,scale(n,maxima))
            neg=add(neg,scale(n,minima))
        allmax.append(pos);allmin.append(neg)
    return (tuple(min(v[i] for v in allmin) for i in range(2)),
            tuple(max(v[i] for v in allmax) for i in range(2)))

def order(mask):
    rel=set(combinations(P,2))|set(combinations(FUT,2))|set(product(P,I+FUT))|set(product(I,FUT))
    rel.update(pair for b,pair in enumerate(combinations(I,2)) if mask&(1<<b))
    deg=[sum((v,u) in rel for v in I) for u in I]
    return rel,deg

def source_checks(rel,deg):
    # Exact rational coefficient identities independent of the physical beta.
    n=15
    for v,d in zip(I,deg):
        actual=[kernel(sum((u,z) in rel and (z,v) in rel for z in range(n))) for u in P]
        assert tuple(actual)==row(d)
    code=encode(rel,n)
    T=[F(i%7-3,5) for i in range(n)]
    w=[F((i%5)+1,7) for i in range(n)]
    j,grad=current_and_gradient(code,n,T,w)
    p=-sum(x for u,v,x in j if u in P and v not in P)
    assert p==-sum(grad[u] for u in P)
    direct=sum(w[v]*sum(b*(T[u]-T[v])/2 for u,b in zip(P,row(d))) for v,d in zip(I,deg))
    assert direct==p
    tau=F(2,5)
    plus=[v+(tau/2 if i in P else 0) for i,v in enumerate(T)]
    minus=[v-(tau/2 if i in P else 0) for i,v in enumerate(T)]
    a,b=(matter_action(code,n,t,w) for t in (plus,minus))
    assert b-a==tau*p
    curvature=-sum(w[v]*sum(row(d))/2 for v,d in zip(I,deg))
    assert a+b-2*matter_action(code,n,T,w)==curvature*tau**2/4
    return curvature

def catalogue():
    d=json.loads((ROOT/"inputs/prefix_1564_two_event_v0_1/inputs/catalog.json").read_text())
    return sorted(int(k) for k,(a,_,b) in d["ranks_pure_free_mixed"].items() if a==b==0)

def run():
    records,cache={},{}
    counts=Counter()
    visible_hist=Counter()
    support_hist=Counter()
    maxvals=[]
    for mask in catalogue():
        rel,deg=order(mask)
        signature=tuple(deg.count(d) for d in range(4))
        visible=sum(signature)
        visible_hist[visible]+=1
        if signature not in cache: cache[signature]=envelope(signature)
        lo,hi=cache[signature]
        assert hi[0]>0 and lo[1]<=0
        source_checks(rel,deg)
        # Half-open or closed endpoints give the same nonzero reference mass away from p=0.
        passes={}
        for m in [F(1,4),F(4)]:
            left=m*F(99,100)
            assert hi[0]>left or hi[1]<left
            passes[str(m)]=hi[0]>left
            support_hist[str(m)]+=int(passes[str(m)])
        maxvals.append((mask,hi))
        records[str(mask)]={"n_d_0_to_3":signature,"zero_atom":str(F(1,2**visible)),
                            "momentum_inf_bounds":bounds(lo),"momentum_sup_bounds":bounds(hi),
                            "trial_windows_nonempty_positive_measure":passes}
        counts["mixed_source_curvature_structurally_possible"]+=int(any(1<=d<=3 for d in deg))
    assert len(records)==1048 and sum(visible_hist.values())==1048
    minimum=tuple(min(v[i] for _,v in maxvals) for i in range(2))
    maximum=tuple(max(v[i] for _,v in maxvals) for i in range(2))
    limiting=[k for k,v in maxvals if v[0]<=minimum[1]]
    limiting_signatures={tuple(records[str(k)]["n_d_0_to_3"]) for k in limiting}
    # If several signatures tie within enclosures, report all as candidates.
    gain=scale(F(4)*F(99,100),(1/minimum[1],1/minimum[0]))
    return {"types":len(records),"visible_density_histogram":dict(sorted(visible_hist.items())),
            "distinct_visible_signatures":len(cache),"raw_zero_atom_range":[str(F(1,2**max(visible_hist))),str(F(1,2**min(visible_hist)))],
            "boundary_source_identities_verified":len(records),"curvature_possible":counts["mixed_source_curvature_structurally_possible"],
            "trial_gain_one_window_support_counts":support_hist,"minimum_of_type_suprema":bounds(minimum),
            "maximum_of_type_suprema":bounds(maximum),"types_attaining_or_within_enclosure_of_minimum":limiting,
            "limiting_signatures":sorted(limiting_signatures),"strict_all_types_gain_threshold":bounds(gain)},records
