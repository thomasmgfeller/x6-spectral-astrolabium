"""Recover the realized mass from eleven fine phases at one cut and the old inlet."""
from fractions import Fraction as F
from modell import ORDER,INNER,PAST,CUT,EDGES,H

def run():
    slots=(4,5,6); targets=tuple(ORDER[CUT:CUT+3]);tri=[[ -EDGES.get((i,j),0) for j in targets] for i in slots]
    weights=(F(47,8),F(3),F(1));assert [sum(row[k]*w for row,w in zip(tri,weights)) for k in range(3)]==[8,8,8]
    y={i:F(k*k+1,37) for k,i in enumerate(ORDER)}
    V=dict(zip(PAST,[F(k,64) for k in (76,47,24,8)]))
    def phase(unit,slot=None,t=0,u=0,v=0):
        yy={j:y[j]+(u+v*V[j] if j in PAST else 0) for j in ORDER}
        act=F(-1,2)
        for (i,j),b in EDGES.items():
            if j==unit:
                delta=yy[j]-yy[i]-(t if slot==i and j in ORDER[CUT:] else 0)
                act-=F(b,38)*delta**2
        return act
    rows=[]
    for unit in ORDER:
        base=phase(unit)
        K=[(phase(unit,i,H)+phase(unit,i,-H)-2*base)/H**2 for i in slots]
        left=19*sum(a*b*phase(unit,u=a*H,v=b*H) for a in (-1,1) for b in (-1,1))/(4*H**2)
        right=F(19,8)*sum(w*k for w,k in zip(weights,K));assert left==int(unit in INNER[:4]) and right==int(unit in INNER[4:]);rows.append([int(left),int(right)])
    # H-scaled shifts on Y with D restored all yield a common 1/D in second differences.
    return {'slots':slots,'targets':targets,'minus_layer_matrix':tri,'basis_recovered':rows,'combination_before_19_over_8':list(weights),'total_settings':11}
