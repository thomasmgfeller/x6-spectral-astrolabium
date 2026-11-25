"""Rational contraction certificates for three mixed stationary field histories."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

import n15

ROOT=Path(__file__).resolve().parent
INNER=n15.INNER
R=F(1,10**9)


def inverse(matrix):
    n=len(matrix)
    rows=[row[:] + [F(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for i in range(n):
        k=next(k for k in range(i,n) if rows[k][i])
        rows[i],rows[k]=rows[k],rows[i]
        rows[i]=[v/rows[i][i] for v in rows[i]]
        for k in range(n):
            if k!=i and rows[k][i]:
                t=rows[k][i]
                rows[k]=[a-t*b for a,b in zip(rows[k],rows[i])]
    return [r[n:] for r in rows]


def fields(x,active):
    y={**dict(zip(n15.support.PAST,map(F,(-5,-4,-3,F(-11,6))))),
       **{j:F(j-5) for j in n15.support.FUTURE},**dict(zip(INNER,x[:7]))}
    w=dict.fromkeys(n15.support.PAST,F(1,8))
    w.update(dict.fromkeys(n15.support.FUTURE,F(1,64)))
    w.update(dict.fromkeys(INNER,F(0))); w.update(dict(zip(active,x[7:])))
    return y,w


def system(x,active,edges):
    y,w=fields(x,active)
    moments=dict.fromkeys(active,F(19))
    grads=dict.fromkeys(INNER,F(0))
    for i,j,b in edges:
        dy=y[j]-y[i]
        if j in moments: moments[j]+=b*dy*dy
        if j in grads: grads[j]-=b*w[j]*dy
        if i in grads: grads[i]+=b*w[j]*dy
    return [moments[j] for j in active]+[grads[j] for j in INNER]


def shifted(x,k,step):
    v=x[:];v[k]+=step;return v


def jac(x,active,edges):
    # Symmetric differences at step one give exact derivatives of a quadratic polynomial.
    cols=[]
    for k in range(len(x)):
        plus=system(shifted(x,k,1),active,edges)
        minus=system(shifted(x,k,-1),active,edges)
        cols.append([(u-v)/2 for u,v in zip(plus,minus)])
    return [list(v) for v in zip(*cols)]


def certify(candidate,rel,edges):
    center=list(map(F,candidate['center']))
    active=candidate['active']
    empty=sorted(set(INNER)-set(active))
    n=len(center)
    j0=jac(center,active,edges)
    A=inverse(j0)
    assert all(sum(A[i][k]*j0[k][j] for k in range(n)) == int(i==j) for i,j in product(range(n),repeat=2))
    residual=system(center,active,edges)
    ycheck,wcheck=fields(center,active)
    ylist=[ycheck[j] for j in range(15)];wlist=[wcheck[j] for j in range(15)]
    code=n15.encode(rel,15)
    gamma=n15.variation.gamma_from_operator(code,15,ylist)
    _,gradient=n15.variation.current_and_gradient(code,15,ylist,wlist)
    assert residual==[19+2*gamma[j] for j in active]+[2*gradient[j] for j in INNER]
    eta=max(abs(sum(a*b for a,b in zip(row,residual))) for row in A)
    # J varies affinely. Bound ||I-A J(x)||_inf by ||A||_inf * ||J(x)-J(c)||_inf.
    curvature=[F(0)]*n
    for k in range(n):
        j1=jac(shifted(center,k,1),active,edges)
        for i in range(n):
            curvature[i]+=sum(abs(a-b) for a,b in zip(j1[i],j0[i]))
    norm_A=max(sum(map(abs,row)) for row in A)
    lip=norm_A*max(curvature)*R
    assert lip<1 and eta+lip*R<R
    y,w=fields(center,active)
    ye={j:R if j in INNER else F(0) for j in y}
    we={j:R if j in active else F(0) for j in w}
    assert min(y[j]-ye[j]-y[i]-ye[i] for i,j in rel)>0
    assert all(0<w[j]-R and w[j]+R<1 for j in active)
    assert all(w[j]==0 for j in empty)
    def edge_bounds(i,j,b):
        d=y[i]-y[j]; de=ye[i]+ye[j]
        vals=[b*den*t for den,t in product((w[j]-we[j],w[j]+we[j]),(d-de,d+de))]
        return min(vals),max(vals)
    flows={(i,j):edge_bounds(i,j,b) for i,j,b in edges}
    inlet=[v for (i,j),v in flows.items() if i in n15.support.PAST and j not in n15.support.PAST]
    qlo=sum(v[0] for v in inlet);qhi=sum(v[1] for v in inlet)
    assert qlo>0
    mins=[j for j in active if not any((i,j) in rel for i in INNER)]
    # All predecessors of these events belong to P. The elapsed time from event 0
    # bounds the moment per unit incoming positive flux.
    lower=sum(19*(w[j]-we[j])/(y[j]+ye[j]-y[0]) for j in mins)
    assert lower>qhi
    witness={}
    for k in empty:
        out=[pair for (i,j),pair in flows.items() if i==k]
        positive=sum(max(F(0),lo) for lo,hi in out)
        negative=sum(max(F(0),-hi) for lo,hi in out)
        assert positive>0 and negative>0
        witness[str(k)]={'positive_lower':str(positive),'negative_magnitude_lower':str(negative)}
    return {'active':active,'null':empty,'cube_radius':str(R),'eta_upper':float(eta),'lipschitz_upper':float(lip),
            'inlet_interval':list(map(str,(qlo,qhi))),'positive_inlet_lower':str(lower),
            'min_positive_to_available_ratio_lower':float(lower/qhi),'signed_outflow_certificate':witness,
            'first_min_gap':float(min(y[j]-ye[j]-y[i]-ye[i] for i,j in rel))}


def run():
    _,rel=n15.support.geometry(n15.TYPE)
    edges=[(i,j,b) for i,j,b in n15.variation.edges(n15.encode(rel,15),15) if b]
    raw=json.loads((ROOT/'Sattelpunkte.json').read_text())
    certificates=[certify(c,rel,edges) for c in raw]
    assert {tuple(row['null']) for row in certificates}=={(4,),(5,),(4,5)}
    # No stationary all-interior vacuum under the same nonempty future collar:
    # the maximal inner event 14 has only the four known future successors.
    outgoing=[(j,b) for i,j,b in edges if i==14]
    assert set(j for j,b in outgoing)==set(n15.support.FUTURE)
    assert sum(b for j,b in outgoing)==0 and sum(b*(j-5)*F(1,64) for j,b in outgoing)==-F(1,64)
    return {'certificates':certificates,'inequivalent_supports_shown':2,
            'terminal_clock_residual_when_w14_zero':'-1/64','complete_sector_classification':False}
