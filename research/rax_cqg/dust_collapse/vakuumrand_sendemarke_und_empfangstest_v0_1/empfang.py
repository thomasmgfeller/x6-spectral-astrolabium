"""Single positive receiving event above the N17 sender, arbitrary old ideal."""
from fractions import Fraction as F
from itertools import combinations
import json
from felder import ROOT, SOURCE, NODES, INNER, PAST, FUTURE, U, Z, E, SCALE, Box, box, serial
from randantwort import EQ, distance


def ideals():
    pred={j:set(i for i,k in EQ.rel if k==j) for j in NODES}
    items=[frozenset()]
    for j in sorted(NODES,key=lambda k:(len(pred[k]),k)):
        items += [p|{j} for p in items if pred[j]<=p]
    primary={p for p in items if Z in p}
    mandatory=pred[Z]|{Z}
    optional=sorted(set(NODES)-mandatory)
    independent=set()
    for n in range(len(optional)+1):
        for extra in combinations(optional,n):
            p=frozenset(mandatory|set(extra))
            if all(j not in p or i in p for i,j in EQ.rel):
                independent.add(p)
    assert independent==primary
    return sorted(primary,key=lambda p:(len(p),sorted(p)))


def time_at(interval):
    a,b=interval
    return Box.hull((1-a)*E[0]+4*a-2,(1-b)*E[1]+4*b-2)


def old_clocks(t):
    e=Box.hull(*E)
    y={j:box(j-5) for j in PAST+FUTURE}
    y.update({3:e-2,Z:t,U:t-distance(t)})
    states=[y]
    for j in EQ.order:
        if j==Z: continue
        following=[]
        for state in states:
            choices,unresolved=EQ.clock_roots(j,state)
            assert not unresolved
            for value in choices:
                after={**state,j:value}
                if EQ.clock_ok(j,after): following.append(after)
        states=following
    assert states
    return states


def run():
    send,recv=[tuple(map(F,v)) for v in json.loads((ROOT/'basis/vorversuch.json').read_text())['CST']['x_fenster']]
    ts,tr=time_at(send),time_at(recv)
    assert ts.hi<tr.lo
    old=old_clocks(ts)
    rows=[]
    r=17
    for p in ideals():
        # Computing with r maximal preserves all coefficients entering r for every
        # admissible future. An induced N17 order forbids r below any old free node.
        rel=EQ.rel|frozenset((i,r) for i in p)
        assert all(i!=j and ((i,k) in rel) for i,j in rel for h,k in rel if j==h)
        terms={}
        for i in p:
            n=sum((i,k) in rel and (k,r) in rel for k in range(18))
            terms[i]=(1,-9,16,-8)[n] if n<4 else 0
        row={'past':sorted(p),'branches':[]}
        for state in old:
            bad=[j for j in sorted(p) if state[j].lo>=tr.hi]
            if bad:
                row['branches'].append({'excluded_by_order':bad})
                continue
            direct=19+sum((b*(tr-state[i]).square() for i,b in terms.items()),box(0))
            # Recompute with the old restricted successor counts and expand
            # around the nominal sender clock; this evaluates a different expression.
            origin=box(F(1,12))
            a=0; m=box(0); c=box(19)
            for i in p:
                n=len({k for k in p if (i,k) in EQ.rel})
                b=(1,-9,16,-8)[n] if n<4 else 0
                v=state[i]-origin
                a+=b;m+=b*v;c+=b*v.square()
            shifted=a*(tr-origin).square()-2*m*(tr-origin)+c
            v=direct.intersection(shifted)
            assert v is not None
            # Keep both enclosures as an audit of the proposed necessary condition.
            row['branches'].append({'D_r':serial(v),'direct':serial(direct),'expanded':serial(shifted),
                                    'status':'OPEN' if v.lo<=0<=v.hi else 'excluded_by_density'})
        rows.append(row)
    return {'send_x':list(map(str,send)),'receive_x':list(map(str,recv)),
            'complete_old_clock_branches':len(old),'ideals':len(rows),'cases':rows}


if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
