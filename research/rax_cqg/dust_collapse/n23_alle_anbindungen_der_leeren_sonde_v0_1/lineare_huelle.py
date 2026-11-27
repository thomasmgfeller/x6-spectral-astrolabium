"""Rational outer polytope for clock coordinates, weights and their products."""
from fractions import Fraction as Q
from intervall import S
from filter import FREE
from ordnungen import EMPTY, POS

def add(row,key,value):
    row[key] = row.get(key,0)+value
    if not row[key]:
        del row[key]

def gap2(row,i,j,k):
    add(row,(i,i),k)
    add(row,(j,j),k)
    add(row,tuple(sorted((i,j))),-2*k)

def inequalities(model,y,w):
    boxes = {(i,):(Q(v.l,S),Q(v.h,S)) for i,v in y.items()}
    for i,v in w.items():
        if i not in EMPTY:
            boxes[100+i,]=(Q(v.l,S),Q(v.h,S))
    rows = []
    def le(row,rhs=0):
        rows.append((row,rhs))
    def eq(row,rhs=0):
        le(row,rhs)
        le({k:-v for k,v in row.items()},-rhs)
    for i,j in model.rel:
        le({(i,):1,(j,):-1})
    squares=set()
    for j in POS:
        d={}
        for i,k,_ in model.inc[j]:
            gap2(d,i,j,k)
            squares.add((i,j))
        eq(d,-19)
    # The stationarity of the terminal positive clock removes Y21 from its incoming derivative.
    terminal={}
    for i,k,_ in model.inc[21]:
        add(terminal,(i,i),k)
    add(terminal,(21,21),-model.terminal_sum)
    eq(terminal,-19)

    for i in FREE:
        row={}
        for j,k,_ in model.out[i]:
            add(row,(j,100+j),k)
            add(row,(i,100+j),-k)
        if i not in EMPTY:
            for a,k,_ in model.inc[i]:
                add(row,(i,100+i),-k)
                add(row,(a,100+i),k)
        eq(row)
    monomials=sorted({key for row,_ in rows for key in row if len(key)==2})
    for i,j in monomials:
        l,h=boxes[i,];r,s=boxes[j,]
        corners=(l*r,l*s,h*r,h*s)
        boxes[i,j]=(0 if i==j and l<=0<=h else min(corners),max(corners))
        for u,v,sign in [(l,r,1),(h,s,1),(l,s,-1),(h,r,-1)]:
            row={(i,j):-sign}
            add(row,(j,),sign*u)
            add(row,(i,),sign*v)
            le(row,sign*u*v)
        if i==j:
            for v in ((l+h)/2,Q(0)):
                le({(i,):2*v,(i,i):-1},v*v)
    for i,j in sorted(squares):
        l=max(0,boxes[j,][0]-boxes[i,][1])
        h=boxes[j,][1]-boxes[i,][0]
        row={(i,):l+h,(j,):-l-h}
        gap2(row,i,j,1)
        le(row,-l*h)
        for v in (l,(l+h)/2,h):
            row={(i,):-2*v,(j,):2*v}
            gap2(row,i,j,-1)
            le(row,v*v)
    # Sign and affine upper/lower weight bounds for a clock difference multiplied by the same weight.
    for j in sorted({b for a,b in monomials if b>=100}):
        for a,b in model.rel:
            if (a,j) not in boxes or (b,j) not in boxes:
                continue
            lo,hi=boxes[j,]
            le({(a,j):1,(b,j):-1,(a,):-lo,(b,):lo})
            le({(a,j):-1,(b,j):1,(a,):hi,(b,):-hi})
    return boxes,rows

def margin(boxes,rows,certificate):
    lhs={}
    rhs=0
    for idx,mult in certificate:
        c=Q(mult)
        assert 0<=idx<len(rows) and c>0
        row,b=rows[idx]
        rhs+=c*b
        for key,v in row.items():
            add(lhs,key,c*v)
    return sum(min(c*l,c*h) for key,c in lhs.items() for l,h in [boxes[key]])-rhs
