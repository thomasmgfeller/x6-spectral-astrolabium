"""Additional exact quadratic identities and nonnegative squares on the late clocks."""
from itertools import combinations, combinations_with_replacement
from fractions import Fraction as Q
from lineare_huelle import inequalities,add

LATE=tuple(range(15,23))
def product(i,j):
    return tuple(sorted((i,j)))

def expanded(model,y,w):
    boxes,rows=inequalities(model,y,w)
    def ensure(i,j):
        key=product(i,j)
        if key in boxes:return key
        l,h=boxes[i,];r,s=boxes[j,]
        bounds=(l*r,l*s,h*r,h*s)
        boxes[key]=(0 if i==j and l<=0<=h else min(bounds),max(bounds))
        for u,v,e in ((l,r,1),(h,s,1),(l,s,-1),(h,r,-1)):
            row={key:-e};add(row,(j,),e*u);add(row,(i,),e*v)
            rows.append((row,e*u*v))
        return key
    for i,j in combinations_with_replacement(LATE,2):ensure(i,j)
    for v in [k[0] for k in boxes if len(k)==1]:
        row={}
        add(row,ensure(21,v),model.terminal_sum)
        for i,k,_ in model.inc[21]:add(row,ensure(i,v),-k)
        rows.append((row,0));rows.append(({k:-c for k,c in row.items()},0))
    rel=set(model.rel)
    gaps=[(a,b) for a,b in combinations(LATE,2)]
    def limits(a,b):
        lo=boxes[b,][0]-boxes[a,][1]
        hi=boxes[b,][1]-boxes[a,][0]
        if (a,b) in rel:lo=max(0,lo)
        if (b,a) in rel:hi=min(0,hi)
        return lo,hi
    for (a,b),(c,d) in combinations(gaps,2):
        l,h=limits(a,b);r,s=limits(c,d)
        for u,v,sign in [(l,r,1),(h,s,1),(l,s,-1),(h,r,-1)]:
            row={}
            for i,j,coef in [(b,d,-1),(b,c,1),(a,d,1),(a,c,-1)]:
                add(row,product(i,j),sign*coef)
            for i,coef in [(b,v),(a,-v),(d,u),(c,-u)]:add(row,(i,),sign*coef)
            rows.append((row,sign*u*v))
    return boxes,rows

def square_cut(vector):
    assert len(vector)==len(LATE)+1 and all(type(i) is int for i in vector)
    constant,*v=vector
    row={}
    for i,a in zip(LATE,v):
        add(row,(i,),-2*a*constant)
        for j,b in zip(LATE,v):
            add(row,product(i,j),-a*b)
    return row,constant**2

def with_cuts(model,y,w,cuts):
    boxes,rows=expanded(model,y,w)
    rows.extend(square_cut(v) for v in cuts)
    return boxes,rows
