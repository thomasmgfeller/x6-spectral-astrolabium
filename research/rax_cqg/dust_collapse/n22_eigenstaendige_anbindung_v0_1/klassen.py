from fractions import Fraction as F
from math import isqrt
from anbindungen import coefficients, enumerate_extensions, enumerate_by_insertion, naive_one, relation

S = 10**9
DUST = (4,5,6,11,12,13,14)
OLD_FREE = (*DUST,15,16,17,18)


def clock_ranges(collar, window, edges, coeff, enclose):
    result = {j:tuple(v[:2]) for j,v in collar.items()}
    for j in OLD_FREE:
        assert (0,j) in edges and (j,7) in edges
        result[j] = (collar[0][0],collar[7][1])
    result[19]=result[20]=window
    known = set(collar)
    stages=[]
    for j in DUST:
        pred=tuple(sorted(i for i,k in edges if k==j))
        if not set(pred)<=known:
            continue
        succ=tuple(sorted(k for i,k in edges if i==j and k in known))
        inc=tuple(sorted((i,c) for (i,k),c in coeff.items() if k==j))
        stages.append((j,pred,succ,inc))
        known.add(j)
    old=tuple(sorted((j,tuple(v[:2])) for j,v in collar.items()))
    for j,proof in enclose(old,tuple(stages)).items():
        result[j]=proof['enclosure']
    return result


def clock21(family, positive, po, fo, edges, coeff, bounds):
    pred = [bounds[i][0] for i,j in edges if j==21]
    succ = [bounds[j][1] for i,j in edges if i==21]
    if po and fo:
        return 'order',(max(pred),min(succ))
    if family == 'A':
        assert not pred and coeff[21,19]==1
        square=0
        for (i,j),c in coeff.items():
            if j==19 and c<0:
                gap=max(0,bounds[19][1]-bounds[i][0])
                square+=(-c)*gap*gap
        radius=isqrt(square)+1
        return 'D19',(bounds[19][0]-radius,min(succ))
    assert not succ and (20,21) in edges
    assert all(hi<6*S for lo,hi in bounds.values())
    if not positive:
        return 'terminal_zero',(6*S,6*S)
    incoming=[(i,c) for (i,j),c in coeff.items() if j==21]
    mass=sum(c for _,c in incoming)
    lo=hi=0
    sqlo=sqhi=19*S*S
    for i,c in incoming:
        a,b=bounds[i]
        lo+=min(c*a,c*b)
        hi+=max(c*a,c*b)
        d=0 if a<=0<=b else min(a*a,b*b)
        u=max(a*a,b*b)
        sqlo+=min(c*d,c*u)
        sqhi+=max(c*d,c*u)
    if mass:
        a,b=sorted((F(lo,mass),F(hi,mass)))
        return 'G21',(max(max(pred),a//1),-(-b//1))
    if not(lo<=0<=hi and sqlo<=0<=sqhi):
        return 'terminal_moments',None
    return 'projected_moments',(6*S,6*S)


def catalog(order, witnesses, collar, window, structure, enclose):
    rows=[]
    for cid,seed in witnesses.items():
        family=seed['case'][0]
        serial,original=structure(order,seed['row'],family)
        base={(a,b) for a,b in serial if max(a,b)<21}
        ext=enumerate_extensions(base,seed['row'],family)
        assert set(ext)==enumerate_by_insertion(base,family)
        assert {pair for pair,d in ext.items() if d==1}==naive_one(base,seed['row'],family)
        for (po,fo),dist in sorted(ext.items(),key=lambda x:(x[1],x[0])):
            edges=relation(base,po,fo,family)
            coeff=coefficients(edges)
            assert len(edges^serial)==dist
            if not dist:assert coeff==original
            bounds=clock_ranges(collar,window,edges,coeff,enclose)
            for weight in ('0','+'):
                method,span=clock21(family,weight=='+',po,fo,edges,coeff,bounds)
                rows.append(dict(id=f'{cid}/{po}/{fo}/{weight}',cid=cid,family=family,weight=weight,
                                 po=po,fo=fo,distance=dist,edges=edges,coeff=coeff,
                                 bounds=bounds,method=method,span=span))
    return rows
