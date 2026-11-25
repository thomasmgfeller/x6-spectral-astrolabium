"""Positive clock roots for every causal past with zero or one new ancestor."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import sys
import json
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from erweiterung import R,OLD,INNER,PAST,FUTURE,Box,box,SCALE,B,extensions

U,Z=15,16
E=Box.hull(F(1,6)-F(1,2**22),F(1,6)+F(1,2**22))
windows=[[F(t) for t in w] for w in json.loads((ROOT/'basis/vorversuch.json').read_bytes())['CST']['x_fenster']]
SLAB=(windows[0][0],windows[1][1])

def ideals(nodes):
    nodes=sorted(nodes);out=set()
    for mask in range(1<<len(nodes)):
        s=frozenset(v for n,v in enumerate(nodes) if mask>>n&1)
        if all(v not in s or u in s for u,v in R if u in nodes and v in nodes):out.add(s)
    return out

def cones():
    ext=list(extensions())
    old_ideals={p for p,f,r in ext}
    assert old_ideals==ideals(OLD)
    for pz in sorted(old_ideals,key=lambda a:(len(a),tuple(sorted(a)))):
        base={(i,j) for i,j in R if j in pz}|{(i,Z) for i in pz}
        yield (pz,None,None),base
        inside=ideals(pz)
        direct={(p,pz-d) for p in inside for d in inside if p<=d and all((i,j) in R for i in p for j in pz-d)}
        projected={(p,f & pz) for p,f,r in ext if p<=pz}
        assert projected==direct
        for p,f in sorted(direct,key=lambda q:(tuple(sorted(q[0])),tuple(sorted(q[1])))):
            r=base|{(i,U) for i in p}|{(U,j) for j in f}|{(U,Z)}
            yield (pz,p,f),r

def roots(key,r,e,shift):
    nodes=set(key[0])|{Z}
    if key[1] is not None:nodes.add(U)
    order=sorted(nodes,key=lambda j:(sum(v==j for _,v in r),j))
    pred={j:[(i,B[count]) for i,v in sorted(r) if v==j and (count:=sum((i,k) in r and (k,j) in r for k in nodes))<4] for j in order}
    oldfixed=set(PAST+FUTURE)
    states=[{}]
    unresolved=0
    for j in order:
        states2=[]
        for y in states:
            if j in oldfixed:
                candidates=[e-2 if j==3 else box(j-5)]
            else:
                ref=(e-2) if shift else box(0)
                a=sum(b for i,b in pred[j])
                t=sum((b*(y[i]-ref) for i,b in pred[j]),box(0))
                c=19+sum((b*(y[i]-ref).square() for i,b in pred[j]),box(0))
                if a:
                    disc=t.square()-a*c
                    if disc.hi<0:continue
                    rad=disc.sqrt_nonnegative_part()
                    candidates=[ref+(t+sgn*rad)/a for sgn in (-1,1)]
                elif t.lo>0 or t.hi<0:candidates=[ref+c/(2*t)]
                else:
                    if t.lo!=0 or t.hi!=0 or c.lo<=0<=c.hi:unresolved+=1
                    continue
            for val in candidates:
                if all(val.hi>v.lo for i,v in y.items() if (i,j) in r):
                    states2.append({**y,j:val})
        states=states2
        if not states:break
    return [((y[Z]-(e-2))/(4-e)) for y in states],unresolved

def endpoints(b):return [str(F(b.lo,SCALE)),str(F(b.hi,SCALE))]
def gap(b):return max(F(b.lo,SCALE)-SLAB[1],SLAB[0]-F(b.hi,SCALE),F(0))
def trial():
    stats=Counter(); rows=[]; maybe=[]; nearest={}
    for key,r in cones():
        n=int(key[1] is not None)
        stats[f'cones_{n}']+=1
        # Each coordinate choice provides an outer enclosure of all allowed roots.
        a,u=roots(key,r,E,False);b,v=roots(key,r,E,True)
        if u or v:maybe.append([str(key),u,v])
        parts=[i for p in a for q in b if (i:=p.intersection(q)) is not None]
        intervals=sorted(set(tuple(endpoints(t)) for t in parts))
        if intervals:stats[f'with_roots_{n}']+=1
        if parts:
            low=min(gap(t) for t in parts)
            if n not in nearest or low<nearest[n]:nearest[n]=low
            if low==0:stats[f'overlap_{n}']+=1
            rows.append({'ancestor':n,'old_past':sorted(key[0]),'past_u':None if not n else sorted(key[1]),
                         'future_u_in_past':None if not n else sorted(key[2]),'x_outer_enclosures':intervals})
    return {'counts':dict(stats),'min_gap':{str(k):str(v) for k,v in nearest.items()},
            'singular':maybe,'cases':rows}
if __name__=='__main__':
    d=trial()
    print(d['counts'], len(d['singular']),[float(F(v)) for v in d['min_gap'].values()])
