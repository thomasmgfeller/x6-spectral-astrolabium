"""Exact finite action, clock forces and linear systems on a seven-event interior."""
from fractions import Fraction as Q
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'quellen'))
from ordnung import PAST,INNER,FUTURE,ORDER,A,B,pairs_from_intervals
E=PAST+FUTURE
EDGES=pairs_from_intervals()

def unit(node):return {v:Q(v==node) for v in ORDER}

def dwells(u):
    between=[Q(0)]+[(l+r)/2 for l,r in zip(u,u[1:])]+[Q(1)]
    return [q-p for p,q in zip(between,between[1:])]

def scalar_coefficients(y):
    coeff=dict.fromkeys(ORDER,Q(-1,2))
    for (i,j),b in EDGES.items():coeff[j]-=Q(b,38)*(y[j]-y[i])**2
    return coeff

def action(y,w):return sum(w[v]*c for v,c in scalar_coefficients(y).items())

def force(y,w):
    # K Y = -19 times the gradient of S.
    out=dict.fromkeys(ORDER,Q(0))
    for (i,j),b in EDGES.items():
        term=b*w[j]*(y[j]-y[i]);out[j]+=term;out[i]-=term
    return out

def matrix(w):
    # Independent assembly by exact polarization of the action.
    indices=ORDER;zero=dict.fromkeys(indices,Q(0));a0=action(zero,w)
    basis={i:unit(i) for i in indices};single={i:action(basis[i],w) for i in indices};out={}
    for col in indices:
        check=force(basis[col],w)
        for row in INNER:
            y={v:basis[col][v]+basis[row][v] for v in indices}
            val=-19*(action(y,w)-single[col]-single[row]+a0)
            assert val==check[row];out[row,col]=val
    return out

def eliminate(rows):
    r=[list(map(Q,row)) for row in rows];piv=[]
    for c in range(len(r[0])):
        j=len(piv);found=next((i for i in range(j,len(r)) if r[i][c]),None)
        if found is None: continue
        r[j],r[found]=r[found],r[j];div=r[j][c];r[j]=[x/div for x in r[j]]
        for i in range(len(r)):
            f=r[i][c]
            if i!=j and f:r[i]=[v-f*u for v,u in zip(r[i],r[j])]
        piv.append(c)
    return r,piv

def nullspace(rows):
    r,piv=eliminate(rows);n=len(r[0]);basis=[]
    for col in range(n):
        if col in piv:continue
        v=[Q(i==col) for i in range(n)]
        for i,k in enumerate(piv):v[k]=-r[i][col]
        assert all(sum(x*y for x,y in zip(row,v))==0 for row in rows);basis.append(v)
    return basis

def solve(rows,rhs):
    n=len(rows[0]);r,piv=eliminate([list(a)+[b] for a,b in zip(rows,rhs)])
    if n in piv:return None
    x=[Q(0)]*n
    for i,k in enumerate(piv):x[k]=r[i][-1]
    assert all(sum(v*w for v,w in zip(row,x))==y for row,y in zip(rows,rhs));return x

def rank(rows):return len(eliminate(rows)[1])
