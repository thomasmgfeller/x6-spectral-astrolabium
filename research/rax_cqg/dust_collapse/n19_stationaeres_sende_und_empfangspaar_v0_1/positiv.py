"""Outward-rounded necessary clock and density equations on N19 causal pasts."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import json
from kegel import (ROOT,INNER,PAST,FUTURE,U,Z,H,R,CODE,OLD,cones,build,coefficients,mask)
from basis.intervall import Box,SCALE,box

E=(F(1,6)-F(1,2**22), F(1,6)+F(1,2**22))
WINDOWS=[tuple(map(F,v)) for v in json.loads((ROOT/'basis/vorversuch.json').read_text())['CST']['x_fenster']]
def time_window(w):
    a,b=w
    return Box.hull((1-a)*E[0]+4*a-2,(1-b)*E[1]+4*b-2)
TS,TR=map(time_window,WINDOWS)


def serial(v):
    return [str(F(k,SCALE)) for k in (v.lo,v.hi)]


def roots(terms,y,method):
    origin=box(F(-11,6)) if method=='shift' else box(0)
    a=sum(b for i,b in terms)
    m=sum((b*(y[i]-origin) for i,b in terms),box(0))
    c=19+sum((b*(y[i]-origin).square() for i,b in terms),box(0))
    if a:
        disc=(m.square()-a*c if method=='shift' else
              -19*a - sum((b*k*(y[i]-y[j]).square() for (i,b),(j,k) in combinations(terms,2)),box(0)))
        if disc.hi<0:return [],False
        s=disc.sqrt_nonnegative_part()
        return [origin+(m+sign*s)/a for sign in (-1,1)],False
    if m.lo>0 or m.hi<0:return [origin+c/(2*m)],False
    impossible=m.lo==m.hi==0 and (c.lo>0 or c.hi<0)
    return [],not impossible


def density(terms,y,t,method):
    if method=='shift':
        return 19+sum((b*(t-y[i]).square() for i,b in terms),box(0))
    origin=box(F(1,12))
    c=19+sum((b*(y[i]-origin).square() for i,b in terms),box(0))
    m=sum((b*(y[i]-origin) for i,b in terms),box(0))
    return sum(b for _,b in terms)*(t-origin).square()-2*m*(t-origin)+c


def chains_u(t):
    # If u<h<z, D_h fixes u from the clock of h. D_z is then a scalar test.
    # Start with the entire ordered domain -3<Y_u<Y_h<t.
    active=[Box(-3*SCALE,t.hi)]
    kept=[]
    while active:
        interval=active.pop()
        rad=interval.square()+6*interval+6
        if rad.hi<0:continue
        u=interval-rad.sqrt_nonnegative_part()
        if u.hi<=-3*SCALE or interval.lo>=t.hi:continue
        g=19-8*(t+4).square()+16*(t+3).square()-9*(t-u).square()+(t-interval).square()
        if g.lo>0 or g.hi<0:continue
        if interval.hi-interval.lo<SCALE//100000:
            kept.append((interval,u))
        else:
            mid=(interval.lo+interval.hi)//2
            active.extend((Box(interval.lo,mid),Box(mid,interval.hi)))
    # Merge adjacent cells; convex overestimation cannot exclude a true solution.
    groups=[]
    for h,u in sorted(kept,key=lambda pair:pair[0].lo):
        if groups and h.lo<=groups[-1][0].hi:
            hh,uu=groups.pop()
            groups.append((Box(hh.lo,h.hi),Box(min(u.lo,uu.lo),max(u.hi,uu.hi))))
        else:groups.append((h,u))
    return groups


@lru_cache(maxsize=256)
def chain_cache(lo,hi):
    return chains_u(Box(lo,hi))


def sender_states(p,a,b,terms,base,t,method):
    if Z not in b:
        assert dict(terms[Z])=={0:-8,1:16,2:-9,U:1}
        d=(t.square()+6*t+6).sqrt_nonnegative_part()
        return [{**base,U:t-d,Z:t}],False
    if U in a:
        assert dict(terms[H])=={0:-8,1:16,2:-9,U:1}
        assert dict(terms[Z])=={1:-8,2:16,U:-9,H:1}
        return [{**base,H:h,U:u,Z:t} for h,u in chain_cache(t.lo,t.hi)],False
    assert a<={0,1,2} and dict(terms[Z])[U]==1
    options,singular=roots(terms[H],base,method)
    states=[]
    for h in options:
        y={**base,H:h,Z:t}
        rest=[(i,b) for i,b in terms[Z] if i!=U]
        rad=-density(rest,y,t,method)
        if rad.hi<0:continue
        states.append({**y,U:t-rad.sqrt_nonnegative_part()})
    return states,singular


def ordered(rel,y):
    return all(y[i].lo<y[j].hi for i,j in rel if i in y and j in y)


def evaluate(case,method,ts=TS,tr=TR):
    p,a,b=case
    if p & set(FUTURE):return {'fixed_order':1},[],False
    rel,nodes=build(p,a,b)
    pred,terms=coefficients(rel,nodes,method)
    base={j:box(j-5) for j in PAST if j in p}
    if 3 in p:base[3]=Box.hull(*E)-2
    states,singular=sender_states(p,a,b,terms,base,ts,method)
    counts=Counter()
    if not states and not singular:counts['sender_density']+=1
    def trim(candidates):
        out=[]
        for y in candidates:
            y[R]=tr
            if ordered(rel,y):out.append(y)
            else:counts['clock_order']+=1
        return out
    states=trim(states)
    order=sorted([j for j in nodes if j in INNER or j==H],key=lambda j:(len(pred[j]),j))
    for j in order:
        following=[]
        for y in states:
            if j in y:following.append(y);continue
            options,undecided=roots(terms[j],y,method)
            singular|=undecided
            if not options and not undecided:counts['ancestor_density']+=1
            following.extend({**y,j:v} for v in options)
        states=trim(following)
        if not states:break
    residuals=[density(terms[R],y,tr,method) for y in states]
    return dict(counts),residuals,singular


def group(case):
    _,a,b=case
    if Z in a:return 'z_before_h'
    if Z in b:return 'h_before_z'
    return 'incomparable'


def scan():
    rows=[]
    for case in cones():
        reps=[evaluate(case,m) for m in ('shift','pairwise')]
        envelopes=[res for counts,res,sing in reps if not sing]
        if len(envelopes)==2:
            parts=[v for a in envelopes[0] for b in envelopes[1] if (v:=a.intersection(b)) is not None]
        elif envelopes: parts=envelopes[0]
        else: parts=[]
        status=('OPEN' if not envelopes or any(v.lo<=0<=v.hi for v in parts) else
                'residual_excluded' if parts else 'no_receiver_branch')
        rows.append({'key':[mask(s) for s in case], 'class':group(case),'status':status,
                     'counts':[r[0] for r in reps],'singular':[r[2] for r in reps],
                     'residuals':[serial(v) for v in parts]})
    return rows


if __name__=='__main__':print(json.dumps(scan(),sort_keys=True,separators=(',',':')))
