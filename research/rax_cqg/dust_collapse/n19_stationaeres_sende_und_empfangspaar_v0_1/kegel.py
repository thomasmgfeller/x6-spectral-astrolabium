"""Enumerate the complete set of labelled past cones; no field assumptions."""
from itertools import combinations
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'basis/zweig.json').read_bytes())
INNER,PAST,FUTURE=(tuple(DATA[k]) for k in ('inner','past','future'))
U,Z,H,R=15,16,17,18
NODES=frozenset(range(17))
OLD=(frozenset(map(tuple,DATA['order'])) | {(j,k) for j in (0,1,2) for k in (U,Z)}
     | {(U,Z)} | {(j,k) for j in (U,Z) for k in FUTURE})
CODE=(1,-9,16,-8)


def ideals(nodes,rel):
    pred={j:{i for i,k in rel if k==j and i in nodes} for j in nodes}
    result=[frozenset()]
    for j in sorted(nodes,key=lambda k:(len(pred[k]),k)):
        result.extend([p|{j} for p in result if pred[j]<=p])
    return result


def positions(nodes,ideals_list):
    for p in ideals_list:
        for no_future in ideals_list:
            if p<=no_future:
                f=nodes-no_future
                if all((i,j) in OLD for i in p for j in f):
                    yield p,f


def mask(s):
    return sum(1<<i for i in s)


def cones():
    result=[]
    for p in ideals(NODES,OLD):
        if Z not in p:continue
        for a,b in positions(p,ideals(p,OLD)):
            result.append((p,a,b))
    return sorted(result,key=lambda row:tuple(mask(s) for s in row))


def projected():
    # Independent three-state old-node labelling relative to h. The second
    # step chooses each possible old part of the receiver's down-set.
    order=sorted(NODES,key=lambda j:(sum(v==j for _,v in OLD),j))
    extensions=[]
    def assign(index,roles):
        if index==len(order):
            extensions.append(tuple(frozenset(j for j,k in roles.items() if k==v) for v in (-1,1)))
            return
        j=order[index]
        for k in (-1,0,1):
            if any(((i,j) in OLD and v>k) or
                   (v==1 and k==-1 and (j,i) not in OLD) or
                   (v==-1 and k==1 and (i,j) not in OLD)
                   for i,v in roles.items()):continue
            assign(index+1,{**roles,j:k})
    assign(0,{})
    required={i for i,j in OLD if j==Z}|{Z}
    available=sorted(NODES-required)
    old_ideals=[]
    for n in range(len(available)+1):
        for extra in combinations(available,n):
            p=frozenset(required|set(extra))
            if all(j not in p or i in p for i,j in OLD):
                old_ideals.append(p)
    return {(p,a,b&p) for p in old_ideals for a,b in extensions if a<=p}


def build(p,a,b):
    past=set(p)|{H}
    rel={(i,j) for i,j in OLD if j in p}
    rel.update((i,H) for i in a)
    rel.update((H,j) for j in b)
    rel.update((i,R) for i in past)
    return rel,past|{R}


def coefficients(rel,nodes,method):
    parents={j:{i for i,k in rel if k==j} for j in nodes}
    terms={}
    for j in nodes:
        terms[j]=[]
        for i in sorted(parents[j]):
            if method=='shift':
                n=sum(i in parents[k] for k in parents[j])
            else:
                n=sum((i,k) in rel and (k,j) in rel for k in nodes)
            if n<len(CODE):terms[j].append((i,CODE[n]))
    return parents,terms


if __name__=='__main__':
    cases=cones()
    assert len(cases)==len(set(cases)) and set(cases)==projected()
    from collections import Counter
    print(len(cases),Counter('h<z' if Z in b else 'z<h' if Z in a else 'parallel' for _,a,b in cases))
