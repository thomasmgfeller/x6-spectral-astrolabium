"""Rational necessary constraints after eliminating the terminal helper's time."""
from fractions import Fraction as F
from itertools import combinations
from intervall import S
from ordnungen import EMPTY, POS

def add(row,key,v):
    row[key]=row.get(key,0)+v
    if not row[key]:
        del row[key]

def square(row,i,j,c):
    add(row,(i,i),c)
    add(row,(j,j),c)
    add(row,tuple(sorted((i,j))),-2*c)

def terms(m,y,w):
    boxes={(i,):(F(v.l,S),F(v.h,S)) for i,v in y.items() if i!=23}
    boxes.update({(100+i,):(F(v.l,S),F(v.h,S)) for i,v in w.items() if i not in EMPTY})
    rows=[]
    def le(row,b=0):
        rows.append((row,b))
    def eq(row,b=0):
        le(row,b)
        le({i:-k for i,k in row.items()},-b)
    def times(row,i):
        return {tuple(sorted((j[0],i))):k for j,k in row.items()}
    # The terminal free helper has positive weight. H23=0 exactly.
    parents={i:k for i,k,c in m.inc[23]}
    a=sum(parents.values())
    assert not m.tail and m.row22[23] and 22 in parents
    mean={(i,):k for i,k in parents.items()}
    if a:
        for i,j in m.rel:
            if j==23:
                row={key:-val/a for key,val in mean.items()}
                add(row,(i,),1)
                le(row)
        row={}
        for i,j in combinations(sorted(parents),2):
            square(row,i,j,parents[i]*parents[j])
        eq(row,-19*a)
    else:
        eq(mean)
        eq({(i,i):k for i,k in parents.items()},-19)
        for i in range(23):
            eq(times(mean,i))
    for i,j in m.rel:
        if j!=23:
            le({(i,):1,(j,):-1})
    eq({(22,):2,(7,):-1,(3,):-1})
    for j in POS:
        row={}
        for i,k,v in m.inc[j]:
            square(row,i,j,k)
        eq(row,-19)
    if not m.out[21]:
        h={}
        for i,k,v in m.inc[21]:
            add(h,(21,),k)
            add(h,(i,),-k)
        eq(h)
        for i in range(23):
            eq(times(h,i))
    for i in (4,5,6,*range(11,22)):
        row={}
        for j,k,v in m.out[i]:
            if j==23:
                # w23*(Y23-Yi)= -F22(Y22)/k22,23 + w23*(Y22-Yi).
                for l,r,u in m.out[22]:
                    if l!=23:
                        add(row,(l,100+l),-k*r/m.row22[23])
                        add(row,(22,100+l),k*r/m.row22[23])
                add(row,(22,123),k)
                add(row,(i,123),-k)
            else:
                add(row,(j,100+j),k)
                add(row,(i,100+j),-k)
        if i not in EMPTY:
            for j,k,v in m.inc[i]:
                add(row,(i,100+i),-k)
                add(row,(j,100+i),k)
        eq(row)
    monoms=sorted({key for row,b in rows for key in row if len(key)==2})
    for i,j in monoms:
        l,h=boxes[(i,)]; s,t=boxes[(j,)]
        corners=[l*s,l*t,h*s,h*t]
        boxes[i,j]=(0 if i==j and l<=0<=h else min(corners),max(corners))
        for u,v,sign in ((l,s,1),(h,t,1),(l,t,-1),(h,s,-1)):
            row={(i,j):-sign}
            add(row,(i,),sign*v)
            add(row,(j,),sign*u)
            le(row,sign*u*v)
        if i==j:
            for v in ((l+h)/2,0):
                le({(i,):2*v,(i,i):-1},v*v)
    for i,j in m.rel:
        if j==23 or any(key not in boxes for key in ((i,i),(j,j),tuple(sorted((i,j))))):
            continue
        l=max(0,boxes[j,][0]-boxes[i,][1]); h=boxes[j,][1]-boxes[i,][0]
        row={(i,):l+h,(j,):-l-h}
        square(row,i,j,1)
        le(row,-l*h)
        for v in (l,(l+h)/2,h):
            row={(i,):-2*v,(j,):2*v}
            square(row,i,j,-1)
            le(row,v*v)
    return boxes,rows

def margin(boxes,rows,certificate):
    lhs={}
    rhs=0
    for i,weight in certificate:
        v=F(weight)
        assert v>0 and 0<=i<len(rows)
        row,b=rows[i]
        rhs+=v*b
        for key,k in row.items():
            add(lhs,key,v*k)
    return sum(min(k*l,k*h) for key,k in lhs.items() for l,h in [boxes[key]])-rhs

def discover(boxes,rows):
    import numpy as np
    from scipy.sparse import lil_matrix
    from scipy.optimize import linprog
    keys=sorted(boxes)
    col={key:i for i,key in enumerate(keys)}
    a=lil_matrix((len(rows),len(keys)+1))
    b=[]
    for i,(row,rhs) in enumerate(rows):
        for key,k in row.items():
            a[i,col[key]]=float(k)
        a[i,-1]=-1
        b.append(float(rhs))
    c=np.zeros(len(keys)+1)
    c[-1]=1
    result=linprog(c,A_ub=a.tocsr(),b_ub=b,bounds=[boxes[key] for key in keys]+[(0,None)],method="highs")
    if result.success and result.fun>1e-10:
        cert=[[i,str(F(float(-v)).limit_denominator(10**12))] for i,v in enumerate(result.ineqlin.marginals) if v < -1e-12]
        if cert and margin(boxes,rows,cert)>0:
            return cert
    return None
