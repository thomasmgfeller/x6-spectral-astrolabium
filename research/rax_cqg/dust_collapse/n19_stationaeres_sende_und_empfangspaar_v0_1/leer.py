"""Complete stationary-field screen for the specified empty-precursor family."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import json
from kegel import (ROOT,INNER,PAST,FUTURE,U,Z,H,R,OLD,NODES,ideals,mask,coefficients)
from positiv import E,WINDOWS,TS,TR,roots,density,ordered,serial,Box,SCALE,box

FREE=(*INNER,Z,R)
MID_E=F(1,6)
MID_S=F(1,2)
MID_R=sum(WINDOWS[1])/2
DOSE=F(6543,10**6)
UNIVERSE=NODES|{H,R}


def enumerate_orders():
    tails=[frozenset(FUTURE[k:]) for k in range(5)]
    for p in sorted(ideals(NODES,OLD),key=mask):
        if Z not in p:continue
        for a in sorted(ideals(p,OLD),key=mask):
            for i,f in enumerate(tails):
                if not all((k,l) in OLD for k in a for l in f):continue
                for j in range(i,5):
                    g=tails[j]
                    if all((k,l) in OLD for k in p for l in g):
                        yield p,a,i,j


def relation(case):
    p,a,i,j=case
    return (OLD|{(k,R) for k in p}|{(k,H) for k in a}|{(H,R)}|
            {(H,k) for k in FUTURE[i:]}|{(R,k) for k in FUTURE[j:]})


def key(case):
    p,a,i,j=case
    return (mask(p),mask(a),i,j)


@lru_cache(maxsize=8)
def prior(e0,e1,s0,s1,method):
    e=Box(e0,e1);ts=Box(s0,s1)
    y={i:box(i-5) for i in PAST+FUTURE}
    y.update({3:e-2,U:ts-(ts.square()+6*ts+6).sqrt_nonnegative_part(),Z:ts})
    pred,terms=coefficients(OLD,NODES,method)
    states=[y]
    for n in sorted(INNER,key=lambda k:(len(pred[k]),k)):
        following=[]
        for st in states:
            choices,unknown=roots(terms[n],st,method)
            assert not unknown
            for v in choices:
                more={**st,n:v}
                if ordered(OLD,more):following.append(more)
        states=following
    assert len(states)==1
    return states[0]


def coordinates(nominal):
    if nominal:
        e=box(MID_E)
        return e,box(MID_E-2+(4-MID_E)*MID_S),box(MID_E-2+(4-MID_E)*MID_R)
    return Box.hull(*E),TS,TR


def kernel(case,e,ts,tr,method):
    p,a,i,j=case
    state=prior(e.lo,e.hi,ts.lo,ts.hi,method)
    if any(state[k].lo>=tr.hi for k in p):
        return 'receiver_order',None
    rel=relation(case)
    pred,terms=coefficients(rel,UNIVERSE,method)
    assert dict(terms[R])[H]==1
    rad=-density([(k,b) for k,b in terms[R] if k!=H],state,tr,method)
    if rad.hi<=0:return 'no_strict_receiver_root',None
    yh=tr-rad.sqrt_nonnegative_part()
    y={**state,H:yh,R:tr}
    if not ordered(rel,y):return 'precursor_order',None
    order=sorted(FREE,key=lambda k:(len(pred[k]),k))
    incoming={k:sum((b*(y[k]-y[l]) for l,b in terms[k]),box(0)) for k in order}
    out={k:[] for k in UNIVERSE}
    for target,v in terms.items():
        for l,b in v:
            out[l].append((target,b*(y[target]-y[l])))
    return 'local_root',(rel,y,order,incoming,out,rad)


def currents(data,future,strict=False):
    _,y,order,incoming,out,_=data
    w={**dict(zip(FUTURE,future,strict=True)),U:box(0),H:box(0)}
    for n in reversed(order):
        result=sum((k*w[j] for j,k in out[n]),box(0))
        d=incoming[n]
        if d.lo<=0<=d.hi:
            return 'open_denominator',None
        w[n]=result/d
        if strict and (w[n].hi<=0 or w[n].lo>=SCALE):
            return 'density_domain',None
    gu,gh=(sum((k*w[j] for j,k in out[n]),box(0)) for n in (U,H))
    return 'complete',(w,gu,gh)


def fixed(row,e,ts,tr,method):
    reason,data=kernel(row,e,ts,tr,method)
    if data is None:return reason
    f=[box((1+DOSE)/64),box(F(1,64)),box(F(1,64)),box(F(1,64))]
    reason,result=currents(data,f,True)
    if result is None:return reason
    w,u,h=result
    if h.lo>0 or h.hi<0:return 'vacuum_h'
    if u.lo>0 or u.hi<0:return 'vacuum_u'
    return 'OPEN'


def scan_fixed():
    e,ts,tr=coordinates(False)
    rows=[]
    counts=Counter()
    for case in enumerate_orders():
        r=fixed(case,e,ts,tr,'shift')
        if r.startswith('open') or r=='OPEN':
            r=fixed(case,e,ts,tr,'pairwise')
        rows.append([*key(case),r]);counts[r]+=1
    return {'counts':dict(counts),'rows':rows}


if __name__=='__main__':print(json.dumps(scan_fixed(),sort_keys=True,separators=(',',':')))
