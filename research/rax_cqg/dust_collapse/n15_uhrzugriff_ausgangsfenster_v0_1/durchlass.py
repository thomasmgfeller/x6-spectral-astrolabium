"""Certified accepted fractions of the unshifted positive or atomic measure."""
from collections import defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from math import comb
from geometrie import H,exact
from intervalle import I
from auslese import settings

@lru_cache(None)
def marginal(positive):
    # x ranges over [-1,1]. Integrate every other clock out of product(8*f_j).
    poly={(0,)*7:Q(1)}
    if positive:
        for j in range(7):
            new=defaultdict(Q);terms=([(0,1),(1,1)] if j==0 else [(5,-1),(6,-1)] if j==6 else [(j-1,-1),(j+1,1)])
            for powers,c in poly.items():
                new[powers]+=c*(Q(3,2) if j in (0,6) else 1)
                for axis,sign in terms:
                    idx=list(powers);idx[axis]+=1;new[tuple(idx)]+=c*Q(sign,16)
            poly=new
    out=defaultdict(Q)
    for powers,c in poly.items():
        for i,p in enumerate(powers):
            if i not in (3,5):c*=0 if p%2 else Q(1,p+1)
        out[powers[3],powers[5]]+=c
    return {k:v for k,v in out.items() if v}

def moment(power,sign):
    if sign==0:return [Q(0) if power%2 else Q(1,power+1)]
    n=power+1;orientation=1 if sign>0 else (-1)**power
    vals=[Q(orientation*comb(n,j)*(-2)**j,2*n) for j in range(n+1)]
    vals[0]-=Q(orientation*(-1)**n,2*n)
    return vals

def polynomial(positive,a,b):
    out=defaultdict(Q)
    for (i,j),c in marginal(positive).items():
        for m,p in enumerate(moment(i,a)):
            for n,q in enumerate(moment(j,b)):out[m+n]+=c*p*q
    return {k:v for k,v in out.items() if v}

@lru_cache(None)
def lobe(positive,a,b,right):
    if right and (a or b):return I.of(0)
    delta=I.of(Q(3,722)).sqrt().sqrt();lo,hi=(Q(1,32),Q(3,32)) if right else (Q(-3,32),Q(-1,32))
    dlow,dhigh=4*delta-hi,4*delta-lo;p=14 if positive else 7
    total=I.of(0)
    for k,c in polynomial(positive,a,b).items():
        # Integrate D^(p-3k/2), with uniform outer offset and equal lobe lengths.
        m=2*(p+1)-3*k;assert m>0
        primitive=(dhigh.sqrt()**m-dlow.sqrt()**m)*Q(2,m)
        total+=c*(32*H*delta)**k*primitive
    return total

def run():
    exact();profiles={}
    for positive in (False,True):
        table={};den=lobe(positive,0,0,False)+lobe(positive,0,0,True)
        for tag,(s,_) in settings().items():
            a,b=(int(x/H) for x in s[:2]);pair=[lobe(positive,a,b,t) for t in (False,True)]
            r=(pair[0]+pair[1])/den
            table[tag]={'total':r.rounded(13),'by_lobe':[(v/lobe(positive,0,0,right)).rounded(13) for right,v in enumerate(pair)]}
            if a or b:assert 0<r.lo<=r.hi<I.of(1).lo and pair[1].hi==0
        profiles['positive' if positive else 'atom']=table
    return {'geometry':exact(),'strict_acceptance':profiles}
if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2,sort_keys=True))
