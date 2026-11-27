"""Independent edge-by-edge finite differences at rational field values."""
from fractions import Fraction as F
from itertools import combinations
from feldroehre import POS
from sekantenimpuls import matrix
from versuch import LATE, midpoint, variables


def residual(y,w,source,edges,free,triple):
    def flow(node):
        incoming=sum(k*w[j]*(y[j]-y[i]) for i,j,k in edges if j==node)
        outgoing=sum(k*w[j]*(y[j]-y[i]) for i,j,k in edges if i==node)
        return outgoing-incoming
    density=[19-int(t==16)*source+sum(k*(y[j]-y[i])**2 for i,j,k in edges if j==t) for t in POS]
    g=[flow(j) for j in range(22)]
    assert sum(g)==0
    return density+[g[t] for t in (*free,*triple)]+[y[15]]+g[:4]


def audit(rows,edges,free):
    axes=variables(free)
    checks=0
    for a,b in zip(rows[::3],rows[2::3]):
        ya,wa=midpoint(a)
        yb,wb=midpoint(b)
        ma=[(l+r)/2 for l,r in zip(ya,yb)]
        mb=[(l+r)/2 for l,r in zip(wa,wb)]
        ja,jb=map(F,(a["source"],b["source"]))
        delta=[(yb[j]-ya[j] if k=="y" else wb[j]-wa[j]) for k,j in axes]+[jb-ja]
        assert all(ya[j]==yb[j] for j in set(range(22))-{j for k,j in axes if k=="y"})
        assert all(wa[j]==wb[j] for j in set(range(22))-{j for k,j in axes if k=="w"})
        for triple in combinations(LATE,3):
            jac=matrix(ma,mb,edges,free,triple)
            ra=residual(ya,wa,ja,edges,free,triple)
            rb=residual(yb,wb,jb,edges,free,triple)
            for l,r,row in zip(ra,rb,jac,strict=True):
                assert r-l==sum(c*x for c,x in zip(row[:33],delta,strict=True))
                checks+=1
    # Independent column derivatives at a single rational state for each triple.
    y,w=midpoint(rows[len(rows)//2])
    h=F(1,1000)
    n=0
    for triple in combinations(LATE,3):
        jac=matrix(y,w,edges,free,triple)
        for j,(field,node) in enumerate(axes+[("J",16)]):
            yp,ym,wp,wm=y.copy(),y.copy(),w.copy(),w.copy()
            if field=="y":
                yp[node]+=h
                ym[node]-=h
            if field=="w":
                wp[node]+=h
                wm[node]-=h
            jump=h if field=="J" else F(0)
            pos=residual(yp,wp,jump,edges,free,triple)
            neg=residual(ym,wm,-jump,edges,free,triple)
            for u,v,row in zip(pos,neg,jac,strict=True):
                assert (u-v)/(2*h)==row[j]
                n+=1
    return dict(secant_components=checks,derivative_entries=n)
