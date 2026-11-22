"""Rational enclosures for the gates and causal addresses, Python stdlib only."""
from fractions import Fraction as Q
from itertools import permutations
from math import isqrt
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'quellen'))
from ordnung import INNER, ORDER

R = Q(1,64)
WIDE = Q(7,128)
H = Q(1,8)

def sqrt_bounds(x):
    n=10**36
    a=isqrt(x.numerator*n*n//x.denominator)
    return Q(a,n),Q(a+1,n)

def addresses(sequence,inner):
    # Each site sees its strict past, and whether a past site is in the marked interior.
    seen=0; selected=[]
    for vertex in sequence:
        if vertex in inner:
            if seen in (3,5): selected.append(vertex)
            seen+=1
    return tuple(selected)

def exact():
    lo,hi=sqrt_bounds(Q(3,722)); dl=sqrt_bounds(lo)[0];dh=sqrt_bounds(hi)[1]
    assert dl**4<=Q(3,722)<=dh**4
    result={}
    for name,(a,b) in {'left':(Q(-3,32),Q(-1,32)), 'right':(Q(1,32),Q(3,32))}.items():
        dmin,dmax=4*dl-b,4*dh-a
        # u' - u = Delta * h / D^(3/2). Include the dependence of D on Delta conservatively.
        low=dl*H/(dmax*sqrt_bounds(dmax)[1]);high=dh*H/(dmin*sqrt_bounds(dmin)[0]);
        assert R+high+Q(3,1000)<WIDE and 2*WIDE<Q(1,8) and 2*low>2*R
        assert (high<2*R if name=='left' else low>2*R)
        both=[max(Q(0),1-high/(2*R)),max(Q(0),1-low/(2*R))]
        result[name]={'shift_u_bounds':[str(low),str(high)], 'single_port_input_length_fraction_bounds':list(map(str,both)), 'guard_halfwidth_sufficient':str(R+high),'opposite_shifts_disjoint_at_fixed_inlet':True}
    assert addresses(ORDER,set(INNER))==(11,13)
    for labels in permutations(INNER):
        renamed=dict(zip(INNER,labels));seq=tuple(renamed.get(v,v) for v in ORDER)
        assert addresses(seq,set(labels))==(renamed[11],renamed[13])
    return {'lobes':result,'inner_relabellings_checked':5040,'chain_ports_by_past_counts':[3,5], 'halfwidth_in':str(R),'halfwidth_guard':str(WIDE),'spacing':str(Q(1,8)), 'uniform_additive_u_error_tolerated_by_guard':str(Q(3,1000))}
