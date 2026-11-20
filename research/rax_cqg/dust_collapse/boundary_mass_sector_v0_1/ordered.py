"""Sharp support ceiling under the extra restriction of strictly increasing hidden clocks."""
from fractions import Fraction as F
from itertools import product
from charge import P,I,order,catalogue,delta,beta,row,offsets,bounds,scale,add,mul

def term(d,shift,early):
    b=row(d)
    a=sum(v*(i-5) for i,v in enumerate(b))
    clock=(-2,shift) if early else (2,F(0))  # s=-2*Delta+shift or s=2*Delta
    linear=a-sum(b)*clock[0]
    constant=b[3]*shift-sum(b)*clock[1]
    lo,hi=add(scale(linear,delta),(constant,constant))
    # A term is algebraically zero only when both coefficients vanish.
    assert lo>0 or hi<0 or lo==hi==0
    return (linear,constant) if lo>0 else (0,F(0))

def run():
    # Store constants in units of 1/32 for inexpensive exact vertex evaluation.
    terms={(off,d,early):(a,int(32*b)) for off,d,early in product(offsets,range(7),(False,True))
           for a,b in [term(d,off,early)]}
    value_cache={}
    def value(score):
        if score not in value_cache:
            a,b=score
            value_cache[score]=mul(scale(F(1,2),beta),add(scale(a,delta),(F(b,32),F(b,32))))
        return value_cache[score]
    result={}
    counts={"1/4":0,"4":0}
    ideal_count=0
    min_sup=None
    for mask in catalogue():
        rel,deg=order(mask)
        pred=[sum(1<<j for j,u in enumerate(I) if (u,v) in rel) for v in I]
        ideals=[bits for bits in range(128) if all(not(bits>>i&1) or not(p & ~bits) for i,p in enumerate(pred))]
        ideal_count+=len(ideals)
        scores=set()
        for off in offsets:
            for bits in ideals:
                pairs=[terms[off,d,bool(bits>>j&1)] for j,d in enumerate(deg)]
                scores.add((sum(a for a,b in pairs),sum(b for a,b in pairs)))
        supremum=tuple(max(value(s)[i] for s in scores) for i in range(2))
        min_sup=supremum if min_sup is None else tuple(min(a,b) for a,b in zip(supremum,min_sup))
        flags={}
        for m in (F(1,4),F(4)):
            cut=m*F(99,100)
            assert supremum[1]<cut or supremum[0]>cut
            flags[str(m)]=supremum[0]>cut
            counts[str(m)]+=int(flags[str(m)])
        result[mask]={"ordered_sup_bounds":bounds(supremum),"trial_windows":flags}
    return {"ideal_vertices_all_orders":ideal_count,"gain_one_trials":counts,
            "minimum_type_sup_bounds":bounds(min_sup),
            "strict_gain_threshold_for_both_on_all":bounds(scale(F(99,25),(1/min_sup[1],1/min_sup[0])))},result
