"""Refine the nearest bracketing pair by two new incomparable stations."""
from itertools import product
from fractions import Fraction as F
from ordnungen import LAYERS,MATERIAL,ideals
from intervall import I
from auslese import target
from freie_felder import solve_quadratic,COLLAR

def branch(order,BY):
    y={j:BY[j] for j in COLLAR}
    traces={}
    for j in [4,5,6,11,12,13]:
        pred={i for i,k in order if k==j}
        c={}
        for i in pred:
            count=sum((i,k) in order for k in pred)
            if count<len(LAYERS):c[i]=LAYERS[count]
        roots=solve_quadratic(c,y)
        assert roots is not None
        permitted=[t for t in roots if t.h>max(y[i].l for i in pred) and t.l<BY[7].h]
        assert len(permitted)==1
        y[j]=permitted[0]
        traces[j]=[v.endpoints() for v in roots]
    return y,traces


def nearest_refinement(order,fields):
    block=target(fields)
    before={j for j in MATERIAL if fields[j].h<block.l}
    after={j for j in MATERIAL if fields[j].l>block.h}
    assert before|after|{16,18}==MATERIAL
    left=[j for j in before if all(i==j or fields[i].h<fields[j].l for i in before)]
    right=[j for j in after if all(i==j or fields[j].h<fields[i].l for i in after)]
    assert left==[12] and right==[14]
    assert (12,14) in order and not any((12,i) in order and (i,14) in order for i in range(19))
    nodes=set(range(19))
    down=ideals(order,nodes);up=ideals({(j,i) for i,j in order},nodes)
    parents=[p for p in down if 12 in p and all((i,14) in order for i in p)]
    futures=[f for f in up if 14 in f and all((12,i) in order for i in f)]
    assert len(parents)==2 and len(futures)==1
    y,tr=branch(order,fields)
    cases=[]
    for p_n,p_z in product(sorted(parents,key=len),repeat=2):
        f=futures[0]
        rel=order|{(i,19) for i in p_n}|{(i,20) for i in p_z}|{(19,i) for i in f}|{(20,i) for i in f}
        assert all((i,k) in rel for i,j in rel for a,k in rel if a==j)
        assert (19,20) not in rel and (20,19) not in rel
        def coeff(i,j):
            n=sum((i,m) in rel and (m,j) in rel for m in range(21))
            return LAYERS[n] if n<len(LAYERS) else 0
        assert {j:coeff(20,j) for j in f if coeff(20,j)}=={14:1,7:-9,8:16,9:-8}
        c={i:coeff(i,19) for i in p_n if coeff(i,19)}
        roots=solve_quadratic(c,y)
        assert roots is not None
        r=19+sum((v*(block-y[i]).sq() for i,v in c.items()),I.enclose(0))
        cases.append({'past_n':sorted(p_n),'past_z':sorted(p_z),'future':sorted(f),'coeff_n':c,
                      'D19':r.endpoints(),'all_roots':[x.endpoints() for x in roots],
                      'roots_overlapping_target':sum(x.h>=block.l and x.l<=block.h for x in roots)})
    return {'anchors':[12,14],'anchor_raw_times':[fields[12].endpoints(),fields[14].endpoints()],
            'native_density_roots':tr,'variants':cases}


def screen_native_pasts(order,by):
    nodes=set(range(19))
    allowed={0,1,2,3,4,5,6,11,12,13,14}
    candidates=[p for p in ideals(order,nodes) if p and p<=allowed and
                any(q in MATERIAL and all((i,q) in order for i in p) for q in nodes)]
    native,trace=branch(order,by)
    p14={i for i,j in order if j==14}
    def coefficients_for_past(past):
        sizes={i:sum((i,j) in order for j in past) for i in past}
        return {i:LAYERS[s] for i,s in sizes.items() if s<len(LAYERS)}
    roots14=solve_quadratic(coefficients_for_past(p14),native)
    possible=[t for t in roots14 if t.h>max(native[i].l for i in p14) and t.l<by[7].h]
    assert len(possible)==1
    native[14]=possible[0]
    w=target(by);rows=[]
    for p in sorted(candidates,key=lambda s:tuple(sorted(s))):
        c=coefficients_for_past(p)
        if any(native[i].l>=w.h for i in p):
            rows.append(dict(past=sorted(p),reason='past_outside_window'));continue
        roots=solve_quadratic(c,native)
        if roots is None:
            residual=19+sum((k*(w-native[i]).sq() for i,k in c.items()),I.enclose(0))
            rows.append(dict(past=sorted(p),reason='interval_contains_zero' if residual.haszero() else 'residual_sign',
                             residual=residual.endpoints()));continue
        eligible=[t for t in roots if t.h>=w.l and t.l<=w.h and t.h>max(native[i].l for i in p)]
        rows.append(dict(past=sorted(p),reason='candidate' if eligible else 'no_target_root',
                         roots=[t.endpoints() for t in roots]))
    return rows
