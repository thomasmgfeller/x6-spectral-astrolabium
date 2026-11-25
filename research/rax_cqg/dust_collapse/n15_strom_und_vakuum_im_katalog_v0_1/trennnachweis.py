"""Exact verifier for the final two supports, independent of the numerical certificate search."""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import lcm
from pathlib import Path
import json

from katalog import structure, INNER, FUTURE, n15

ROOT=Path(__file__).resolve().parent
IDS=(5,6,11,12,13,14)
ACTIVE=(13,14)
D=Q(23,6)


def midpoint(v,w):
    return tuple((a+b)/2 for a,b in zip(v,w))


def fixture_check(edges,rel):
    assert not any((4,j) in edges for j in set(ACTIVE)|FUTURE)
    # Check both gradient orientations and the normalized polynomial on an exact input.
    clocks=[Q(-5),Q(-4),Q(-3),Q(-11,6),Q(-3,2),Q(-1),Q(-1),2,3,4,5,0,0,1,Q(5,4)]
    ws=[Q(1,8)]*4+[0]*3+[Q(1,64)]*4+[0,0,Q(1,10),Q(1,5)]
    code=n15.encode(rel,15)
    gamma=n15.variation.gamma_from_operator(code,15,clocks)
    _,grad=n15.variation.current_and_gradient(code,15,clocks,ws)
    raw=[19+2*gamma[k] for k in ACTIVE]+[128*grad[k] for k in IDS]
    values=equations(edges,clocks,[64*w for w in ws],1)
    assert raw==values


def equations(edges,clocks,weights,denom):
    # clocks are K*Y when evaluating integers. Every returned equation equals K²*F.
    moments={j:19*denom**2 for j in ACTIVE}
    gradients={j:0 for j in IDS}
    for (i,j),b in edges.items():
        delta=clocks[j]-clocks[i]
        if j in moments:
            moments[j]+=b*delta**2
        current=b*weights[j]*delta*denom
        if i in gradients: gradients[i]+=current
        if j in gradients: gradients[j]-=current
    return [moments[j] for j in ACTIVE]+[gradients[j] for j in IDS]


def verify_leaf(z,dual,edges):
    # Simplex degree two in the clocks; affine in the two occupied weights.
    assert len(dual)==8 and all(type(x) is int for x in dual)
    pairs=list(combinations(range(7),2))
    points=list(z)+[midpoint(z[i],z[j]) for i,j in pairs]
    coordinates=[[Q(-11,6)+D*p for p in point] for point in points]
    den=lcm(6,*(v.denominator for p in coordinates for v in p))
    times=[]
    for p in coordinates:
        t=[-5*den,-4*den,-3*den,-11*den//6,-11*den//6,0,0,2*den,3*den,4*den,5*den,0,0,0,0]
        for k,v in zip(IDS,p):
            t[k]=v.numerator*(den//v.denominator)
        times.append(t)
    for u,v in product((0,64),repeat=2):
        weights=[8]*4+[0]*3+[1]*4+[0,0,u,v]
        vals=[sum(a*b for a,b in zip(dual,equations(edges,t,weights,den))) for t in times]
        assert min(vals[:7])>0
        # Twice the edge Bernstein coefficient at the midpoint.
        assert all(4*vals[k+7]-vals[i]-vals[j]>0 for k,(i,j) in enumerate(pairs))
    return 1


def visit(z,node,edges):
    if set(node)=={'p'}:
        return verify_leaf(z,node['p'],edges)
    assert set(node)=={'s','a','b'}
    i,j=node['s']
    assert 0<=i<j<7
    a,b=z.copy(),z.copy()
    a[i]=b[j]=midpoint(z[i],z[j])
    return visit(a,node['a'],edges)+visit(b,node['b'],edges)


def run(remaining):
    archive=json.loads((ROOT/'Trennzertifikate.json').read_text())
    covered={}
    for key,opts in remaining.items():
        rel,edges,_=structure(int(key))
        assert opts==[{'mask':96,'quiet':[4]}] and {j for i,j in enumerate(INNER) if 96&(1<<i)}==set(ACTIVE)
        fixture_check(edges,rel)
        for order in permutations(IDS):
            if any((v,u) in rel for n,u in enumerate(order) for v in order[n+1:]):continue
            name=key+':'+'-'.join(map(str,order))
            z=[tuple(Q(int(j in order[n:])) for j in IDS) for n in range(7)]
            covered[name]=visit(z,archive[name],edges)
    assert set(covered)==set(archive)
    return covered
