"""Exact affine Jacobians on a joint rectangular field domain."""
from decimal import Decimal
from fractions import Fraction as F
from math import lcm
from algebra import inv
from feldroehre import POS
from paarstudie import upper
from sekanten import ALL, UNIT, majorant, norm_proof
from versuch import system, variables


def matrix(y,w,edges,free,triple):
    axes=variables(free)
    _, jac, _ = system(y,w,F(0),edges,free,axes,[F(0)]*5,triple,
                         dict.fromkeys(triple,F(0)),F)
    start=len(POS)+len(free)
    for i,row in enumerate(jac):
        # The three extra columns carry changes of the prescribed impulse values.
        row.append(F(-int(i==POS.index(16))))
        row.extend(F(int(i==start+j)) for j in range(3))
    assert len(jac)==33 and all(len(row)==36 for row in jac)
    return jac


def guard_bound(M,rhs,weights,q):
    # Enclose all unknowns for impulse changes of absolute value at most one.
    vals=[[int(i==j)-v for j,v in enumerate(row)] for i,row in enumerate(M)]
    decimal_b=[Decimal(v.numerator)/Decimal(v.denominator) for v in rhs]
    approx=[F(sum(a*b for a,b in zip(row,decimal_b))).limit_denominator(10**18) for row in inv(vals)]
    gap=max([F(0)]+[(b+sum(a*x for a,x in zip(row,approx))-u)/weight
                     for b,row,u,weight in zip(rhs,M,approx,weights)])
    shift=gap/(1-q)+F(1,10**30)
    guard=[v+shift*s for v,s in zip(approx,weights)]
    assert all(v>=0 for v in guard)
    assert all(b+sum(a*x for a,x in zip(row,guard))<=v for b,row,v in zip(rhs,M,guard))
    return guard


def prove(bounds,edges,free,triple):
    mid={a:F(lo+hi,2*UNIT) for a,(lo,hi) in bounds.items()}
    radii={a:hi-lo for a,(lo,hi) in bounds.items()}
    y,w=([mid[k,j] for j in range(22)] for k in ("y","w"))
    A=matrix(y,w,edges,free,triple)
    changes={}
    for axis in ALL:
        if not radii[axis]:
            continue
        k,j=axis
        yy,ww=y.copy(),w.copy()
        (yy if k=="y" else ww)[j]+=1
        B=matrix(yy,ww,edges,free,triple)
        cols={}
        for col in range(len(A[0])):
            diff=[(i,B[i][col]-A[i][col]) for i in range(len(A)) if B[i][col]!=A[i][col]]
            if diff:
                den=lcm(*(v.denominator for _,v in diff))
                cols[col]=den,[(i,int(v*den)) for i,v in diff]
        changes[axis]=cols
    full=majorant(A,changes,radii)
    M=[row[:33] for row in full]
    q,weights=norm_proof(M)
    if q is None:
        return dict(triple=list(triple),status="OPEN")
    rhs=[sum(row[33:]) for row in full]
    guard=guard_bound(M,rhs,weights,q)
    response=F(upper(guard[-1]))
    return dict(triple=list(triple),status="EXCLUDED",norm_upper=upper(q),weights=weights,
                supersolution=list(map(str,guard)),source_per_max_impulse=str(response),
                minimum_adjacent_gap=str(F(1,10**6)/response))
