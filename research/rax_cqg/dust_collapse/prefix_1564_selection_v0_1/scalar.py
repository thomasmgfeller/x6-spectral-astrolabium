"""Reconstruct the exact Gaussian precision from the coupled action in the shared chart."""
from itertools import combinations, product
from unittest.mock import patch
import mpmath as mp
import sympy as sp
import sys
from prefix import INPUT
sys.path.insert(0,str(INPUT))
import geometry

INNER=(4,5,6,11,12,13)


def layout(key):
    n,mask=key
    inner=INNER[:n]
    past,future=geometry.P,geometry.F
    rel=set(combinations(past,2))|set(combinations(future,2))|set(product(past,inner+future))|set(product(inner,future))
    rel.update(p for k,p in enumerate(combinations(inner,2)) if mask&(1<<k))
    nodes=past+inner+future
    assert len(nodes)==n+8 and all((a,d) in rel for a,b in rel for c,d in rel if c==b)
    weights={}
    for i,j in rel:
        size=sum((i,k) in rel and (k,j) in rel for k in nodes)
        weights[i,j]=(1,-9,16,-8)[size] if size<4 else 0
    return inner,weights,len(nodes)-sum(weights.values())


def rate(key):
    inner,coeff,_=layout(key)
    n=8+len(inner)
    frame=sp.zeros(n)
    frame[1:4,:3]=sp.eye(3)
    frame[7:10,3:6]=sp.eye(3)
    frame[:4,-2]=geometry.BM
    frame[7:11,-1]=geometry.BP
    for col,node in enumerate(inner):
        frame[node,6+col]=1
    matrix=sp.zeros(n)
    for (i,j),b in coeff.items():
        diff=frame[i,:]-frame[j,:]
        matrix-=sp.Rational(b,2)*diff.T*diff
    matrix[-2,:3]-=geometry.AM[1:4,:].T
    matrix[:3,-2]-=geometry.AM[1:4,:]
    matrix[-1,3:6]+=geometry.AP[:3,:].T
    matrix[3:6,-1]+=geometry.AP[:3,:]
    matrix[-2,-2]-=geometry.AM.dot(geometry.BM)
    matrix[-1,-1]+=geometry.AP.dot(geometry.BP)
    # Damping of the inherited centred Gaussian input, before scalar integration.
    hidden=[0,1,2,*range(6,n)]
    out=[3,4,5]
    block=(matrix[hidden,hidden]+sp.I*sp.diag(1,1,1,*([0]*(n-6)))).to_DM().convert_to(sp.QQ_I)
    cross=matrix[hidden,out].to_DM().convert_to(sp.QQ_I)
    piv=list(block.rref()[1])
    selected=cross.extract(piv,[0,1,2])
    sol,den=block.extract(piv,piv).solve_den(selected)
    assert block.extract(list(range(block.shape[0])),piv)*sol==cross.scalarmul(den)
    eff=matrix[out,out].to_DM().convert_to(sp.QQ_I)-(selected.transpose()*sol).scalarmul(1/den)
    omega=eff.scalarmul(sp.QQ_I(0,-1)).to_Matrix()
    assert omega==omega.T and omega.applyfunc(sp.re).is_positive_definite
    return omega


def states(keys):
    out={}
    with patch.object(geometry,'order',layout):
        for key in keys:
            details,state=geometry.kernel(key)
            assert details['status']=='ADMISSIBLE'
            out[key]=state
    return out


def overlap(left,right):
    P,N=left
    Q,M=right
    return mp.conj(N)*M*(2*mp.pi)**mp.mpf('1.5')/geometry.continued_sqrt(P.apply(mp.conj)+Q)
