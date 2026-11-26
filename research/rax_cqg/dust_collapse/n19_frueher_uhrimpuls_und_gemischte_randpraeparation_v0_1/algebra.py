"""Numerical proposals and interval enclosures; proposals alone never pass a test."""
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from quelle import box,hull,Box,SCALE
getcontext().prec=64


def mid(v):
    if isinstance(v,Box):return D(v.lo+v.hi)/D(2*SCALE)
    if isinstance(v,F):return D(v.numerator)/D(v.denominator)
    return D(v)


def magnitude(v):
    return F(max(abs(v.lo),abs(v.hi)),SCALE)


def inv(a):
    n=len(a)
    rows=[[mid(v) for v in row]+[D(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot=max(range(j,n),key=lambda i:abs(rows[i][j]))
        rows[j],rows[pivot]=rows[pivot],rows[j]
        d=rows[j][j]
        assert d
        rows[j]=[v/d for v in rows[j]]
        for i in range(n):
            if i!=j and rows[i][j]:
                c=rows[i][j]
                rows[i]=[u-c*v for u,v in zip(rows[i],rows[j])]
    return [r[n:] for r in rows]


def prod(a,b):
    return sum(x*y for x,y in zip(a,b,strict=True))


def matvec(A,x):
    return [prod(row,x) for row in A]


def correction(A):
    C=[[box(v) for v in row] for row in inv(A)]
    cols=list(zip(*A))
    radii=[sum(magnitude(box(i==j)-prod(row,col)) for j,col in enumerate(cols))
           for i,row in enumerate(C)]
    q=max(radii)
    assert q<1, float(q)
    return C,q


def solve_box(A,b):
    C,q=correction(A)
    candidate=[box(v) for v in matvec(inv(A),[mid(v) for v in b])]
    residual=[v-w for v,w in zip(b,matvec(A,candidate))]
    err=max(magnitude(v) for v in matvec(C,residual))/(1-q)
    return [v+hull(-err,err) for v in candidate]


def gauss_box(A,b):
    """Outward interval Gaussian elimination with pivot choices from absolute centres."""
    n=len(A)
    rows=[list(row)+[v] for row,v in zip(A,b)]
    for j in range(n):
        p=max(range(j,n),key=lambda k:abs(mid(rows[k][j])))
        rows[p],rows[j]=rows[j],rows[p]
        assert not rows[j][j].contains_zero()
        for i in range(j+1,n):
            c=rows[i][j]/rows[j][j]
            rows[i][j]=box(0)
            for k in range(j+1,n+1):rows[i][k]=rows[i][k]-c*rows[j][k]
    x=[box(0)]*n
    for j in reversed(range(n)):
        x[j]=(rows[j][-1]-prod(rows[j][j+1:n],x[j+1:]))/rows[j][j]
    return x
