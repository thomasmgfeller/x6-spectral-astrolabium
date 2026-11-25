"""All labelled one-event extensions of the archived N15 saddle; outward intervals."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
from basis.intervall import Box, SCALE, box

ROOT = Path(__file__).resolve().parent
SOURCE = json.loads((ROOT/'basis/zweig.json').read_text())
R = set(map(tuple,SOURCE['order']))
INNER, PAST, FUTURE = map(tuple,(SOURCE['inner'],SOURCE['past'],SOURCE['future']))
OLD, Z = set(range(15)), 15
B = (1,-9,16,-8)


def extensions():
    down, up = [],[]
    for mask in range(1<<15):
        s = frozenset(i for i in OLD if mask & (1<<i))
        if all(v not in s or u in s for u,v in R):
            down.append(s)
        if all(u not in s or v in s for u,v in R):
            up.append(s)
    for p in down:
        for f in up:
            if p.isdisjoint(f) and all((u,v) in R for u in p for v in f):
                yield p,f, R | {(u,Z) for u in p} | {(Z,v) for v in f}


def coeff(relation):
    nodes=sorted(set().union(*(set(pair) for pair in relation))) if relation else []
    def order(v,i):
        return sum((v,z) in relation and (z,i) in relation for z in nodes)
    return {k:B[n] for k in relation if (n:=order(*k))<4}


def strictly_ordered(y,r):
    undecided=False
    for u,v in r:
        if u not in y or v not in y:continue
        if y[v].hi<=y[u].lo:return 'no'
        if y[u].hi>=y[v].lo:undecided=True
    return 'unknown' if undecided else 'yes'


def serial(x):
    return [str(F(x.lo,SCALE)),str(F(x.hi,SCALE))]


def solve(r,e,x,audit=True,extra=False):
    nodes=OLD|{Z,16} if extra else OLD|{Z}
    pool=list(INNER)+([16] if extra else [])
    variables=[]
    while pool:
        i=next(j for j in pool if all((k,j) not in r for k in pool))
        variables.append(i);pool.remove(i)
    h=coeff(r)
    y={j:box(j-5) for j in PAST+FUTURE}
    y[3]=e-2
    y[Z]=y[3]+x*(y[7]-y[3])
    rows=[];unknown=[]

    def complete(clock,flags):
        flags=list(flags)
        w={**{j:box(F(1,8)) for j in PAST},**{j:box(F(1,64)) for j in FUTURE},Z:box(0)}
        for j in reversed(variables):
            out=sum((b*w[i]*(clock[i]-clock[j]) for (k,i),b in h.items() if k==j),box(0))
            moment=sum((b*(clock[j]-clock[k]) for (k,i),b in h.items() if i==j),box(0))
            if moment.lo<=0<=moment.hi:
                residual=out-moment*Box.hull(0,1)
                if residual.lo<=0<=residual.hi:unknown.append('density_singular')
                return
            w[j]=out/moment
            if w[j].hi<=0 or w[j].lo>=SCALE:return
            if w[j].lo<=0 or w[j].hi>=SCALE:
                flags.append('density_domain')
                w[j]=w[j].intersection(Box.hull(0,1))
        if strictly_ordered(clock,r)=='unknown':flags.append('clock_order')
        flux_terms=[b*w[j]*(clock[j]-clock[Z]) for (u,j),b in h.items() if u==Z]
        flux=sum(flux_terms,box(0))
        gross=Box(sum(max(v.lo,-v.hi,0) for v in flux_terms),
                  sum(max(abs(v.lo),abs(v.hi)) for v in flux_terms))
        gravity=len(nodes)-sum(h.values())
        # Second implementation: insert ±eta into the COMPLETE action, rebuild
        # interval cardinalities independently, including every old regraded pair.
        if audit:
            gap=min(clock[j].lo-clock[i].hi for i,j in r if i==Z or j==Z)
            assert gap>0
            eta=min(F(1,256), F(gap,4*SCALE))
            def value(sign):
                yc=clock.copy();yc[Z]=yc[Z]+sign*eta
                pred={v:{u for u in nodes if (u,v) in r} for v in nodes}
                succ={v:{u for u in nodes if (v,u) in r} for v in nodes}
                coeffs={ (i,j):B[len(succ[i]&pred[j])] for i,j in r if len(succ[i]&pred[j])<4}
                geom=len(nodes)-sum(coeffs.values())
                lag=19*sum(w.values(),box(0))+sum((b*w[j]*(yc[j]-yc[i]).square() for (i,j),b in coeffs.items()),box(0))
                assert geom==gravity
                return 38*geom-lag
            delta=(value(1)-value(-1))/(4*eta)
            assert flux.intersection(delta) is not None
            if flux.lo>0:assert delta.lo>0
            if flux.hi<0:assert delta.hi<0
            for j in variables:
                eq=19+sum((b*(clock[j]-clock[i]).square() for (i,v),b in h.items() if v==j),box(0))
                g=sum((b*w[v]*(clock[v]-clock[i])*(int(i==j)-int(v==j))
                       for (i,v),b in h.items() if i==j or v==j),box(0))
                assert eq.lo<=0<=eq.hi and g.lo<=0<=g.hi
        rows.append({'flux':serial(flux),'absolute_sum':serial(gross),'F4':gravity,'bounds_only':sorted(set(flags))})

    def visit(idx,clock,flags):
        if strictly_ordered(clock,r)=='no':return
        if idx==len(variables):
            complete(clock,flags);return
        j=variables[idx]
        inputs=[(i,b) for (i,v),b in sorted(h.items()) if v==j]
        assert all(i in clock for i,_ in inputs)
        # Solve for Y_j relative to a nearby known predecessor.
        origin=clock[3]
        degree=sum(b for _,b in inputs)
        first=sum((b*(clock[i]-origin) for i,b in inputs),box(0))
        c=19+sum((b*(clock[i]-origin).square() for i,b in inputs),box(0))
        if degree:
            disc=first.square()-degree*c
            if disc.hi<0:return
            if disc.lo<=0<=disc.hi:flags=flags+('discriminant_boundary',)
            roots=[origin+(first+sgn*disc.sqrt_nonnegative_part())/degree for sgn in (-1,1)]
        elif first.lo>0 or first.hi<0:
            roots=[origin+c/(2*first)]
        else:
            if first.lo==first.hi==0 and (c.lo>0 or c.hi<0):return
            unknown.append('clock_singular');return
        for root in roots:
            visit(idx+1,{**clock,j:root},flags)
    visit(0,y,())
    return rows, sorted(set(unknown))


def study(e,x,audit):
    stats=Counter();results=[]
    for p,f,r in extensions():
        stats['all']+=1
        if not(p and f):continue
        stats['two_sided']+=1
        rows,unknown=solve(r,e,x,audit)
        if unknown:stats['orders_with_undecided_branch']+=1
        if rows:stats['orders_with_candidate']+=1
        for row in rows:
            lo,hi=map(F,row['flux'])
            if lo>0:stats['positive']+=1
            elif hi<0:stats['negative']+=1
            else:stats['possibly_zero']+=1
        if rows or unknown:
            results.append({'past':sorted(p),'future':sorted(f),'branches':rows,'unresolved':unknown})
    return {'counts':dict(stats),'cases':results}
