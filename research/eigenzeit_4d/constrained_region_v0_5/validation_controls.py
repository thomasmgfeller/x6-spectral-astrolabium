"""Exact identity tests and independent checks for the geometric correction."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import json,random
import numpy as np
import constrained as c
from intervals import I,precision
from witnesses import point_interval
from realizability import residuals

ROOT=Path(__file__).resolve().parent


def corrected_point(cells,coefficients):
    q=point_interval(cells);r=residuals(cells)
    return q+sum((I(int(coefficients[a]))/c.SCALE*r[a] for a in range(2)),I(0))


def inv(A):
    n=len(A);a=[list(row)+[F(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
    for i in range(n):
        pivot=next(k for k in range(i,n) if a[k][i])
        a[i],a[pivot]=a[pivot],a[i];z=a[i][i];a[i]=[v/z for v in a[i]]
        for j in range(n):
            if j!=i:
                z=a[j][i];a[j]=[x-z*y for x,y in zip(a[j],a[i])]
    return [row[n:] for row in a]


def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F(0)) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A):return [list(x) for x in zip(*A)]
def add(A,B):return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def minus(A):return [[-v for v in row] for row in A]


def float_point(y,coefficients):
    s=-np.sqrt(c.C@np.asarray(y,float))
    G=np.einsum('k,kij->ij',s,c.GS2/2)
    P=np.einsum('k,kia->ia',s,c.BP2/2)
    X=np.linalg.solve(G,P);d=P[:,0]-P[:,1]
    q=-d@(X[:,0]-X[:,1]);r=np.einsum('ia,ia->a',P,X)-s@c.SP
    return float(q+np.dot(np.array(coefficients)/c.SCALE,r))


def main():
    precision(60);rng=random.Random(2026102713);checks=0
    # Matrix inverse remainder identity, exactly over rational inputs.
    for _ in range(60):
        G=[[F([-4,3,5,7][i] if i==j else 0) for j in range(4)] for i in range(4)]
        E=[[F(rng.randint(-4,4),50) for j in range(4)] for i in range(4)];E=[[E[i][j]+E[j][i] for j in range(4)] for i in range(4)]
        P=[[F(rng.randint(-8,8),3) for a in range(2)] for i in range(4)]
        D=[[F(rng.randint(-4,4),40) for a in range(2)] for i in range(4)]
        W=mm(inv(G),P);H=add(D,minus(mm(E,W)))
        lhs=add(mm(mm(tr(add(P,D)),inv(add(G,E))),add(P,D)),minus(mm(mm(tr(P),inv(G)),P)))
        rhs=add(add(mm(tr(W),D),mm(tr(D),W)),minus(mm(mm(tr(W),E),W)))
        rhs=add(rhs,mm(mm(tr(H),inv(add(G,E))),H))
        assert lhs==rhs;checks+=1
    # Check the majorant of both K and -K, including singular K.
    pairs=[(0,0),(c.SCALE,c.SCALE),(2*c.SCALE,2*c.SCALE)]
    pairs += [(rng.randint(-16*c.SCALE,16*c.SCALE),rng.randint(-16*c.SCALE,16*c.SCALE)) for _ in range(100)]
    for kp,kq in pairs:
        a=F(kp,c.SCALE)-1;d=F(kq,c.SCALE)-1;det=abs(a*d-1)
        scalar=lambda f:I(f.numerator)/f.denominator
        den=(scalar(a*a+d*d+2+2*det)).sqrt()
        m00=scalar(a*a+1+det)/den+I(1)/(2**40)
        m11=scalar(d*d+1+det)/den+I(1)/(2**40)
        m01=scalar(a+d)/den
        for sign in [-1,1]:
            aa=m00+sign*scalar(a);dd=m11+sign*scalar(d);bb=m01+sign
            assert aa.lo>0 and dd.lo>0 and (aa*dd-bb.square()).lo>0;checks+=1
    # Exact mean vectors: both consistency identities vanish and F equals q.
    gs=json.loads((ROOT.parent/'poisson_v0_2/geometries.json').read_text())
    for g in gs:
        atoms=[F(x) for x in g['atom_ratios']];M=2**32
        cells=[M*atoms[k] for k in c.baseline.previous.KEEP]+[M*sum(atoms[k] for k in c.baseline.previous.MERGED)]
        k=[rng.randint(-3*c.SCALE,3*c.SCALE) for _ in range(2)]
        q=corrected_point(cells,k)
        target=F(g['tau_squared'])*65536/abs(F(g['signed_intervals'][c.baseline.previous.baseline.INDEX[(0,6)]]))
        assert F(q.lo)<=target<=F(q.hi);checks+=1
    y=np.load(ROOT.parent/'refined_bound_v0_4/fresh_counts.npz')['cells'][55,0]
    r=c.evaluate(y,diagnostics=True);proof=c.evaluate(y,True,r['coefficients'])
    independent=corrected_point(y,r['coefficients'])
    assert proof['certified'] and independent.lo<=Decimal(proof['qhat_upper']) and independent.hi>=Decimal(proof['qhat_lower']);checks+=1
    analytic=np.array(r['gradient']);numeric=[]
    for b in range(20):
        h=max(1.,float(y[b])*1e-5);v=y.astype(float);u=v.copy();v[b]+=h;u[b]-=h
        numeric.append((float_point(v,r['coefficients'])-float_point(u,r['coefficients']))/(2*h))
    difference=np.linalg.norm(analytic-numeric)/np.linalg.norm(analytic)
    assert difference<1e-4;checks+=1
    assert c.evaluate([0]*20)['reason']=='COUNT_GUARD';checks+=1
    assert c.evaluate([-1]+[100]*19)['reason']=='INVALID_CELL_COUNTS';checks+=1
    return {'status':'PASS_CONTROLS','checks':checks,'exact_matrix_identities':60,
            'majorant_positivity_checks':206,'exact_geometry_correction_checks':20,
            'fixed_coefficient_derivative_relative_difference':float(difference)}


if __name__=='__main__':print(json.dumps(main(),indent=2))
