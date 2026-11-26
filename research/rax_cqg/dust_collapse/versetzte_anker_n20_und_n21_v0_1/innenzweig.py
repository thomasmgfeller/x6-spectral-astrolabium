"""Unforced native past of event 14 and two necessary equations on its revised cone."""
from intervall import I,span,Q
from auslese import affine,target
from ordnungen import coefficients
from collections import Counter


def incoming(order,p,j):
    ext=order|{(i,19) for i in p}|{(19,f) for f in {j}|{b for a,b in order if a==j}}
    return {i:c for i,c in coefficients({(v,u) for u,v in ext},{i for i,k in ext if k==j}).items()}


def roots(c,times):
    A=sum(c.values())
    B=sum((-2*k*times[i] for i,k in c.items()),I.enclose(0))
    C=19+sum((k*times[i].sq() for i,k in c.items()),I.enclose(0))
    if A==0:return [-C/B]
    d=B.sq()-4*A*C
    if d.h<0:return []
    assert d.l>0
    return [(-B+sign*d.sqrt())/(2*A) for sign in (-1,1)]


def past14(order,by):
    times=dict(by)
    for j in (4,5,6,11,12,13):
        p={i for i,k in order if k==j}
        c=coefficients({(v,u) for u,v in order},p)
        possible=[t for t in roots(c,times) if t.h>max(times[i].l for i in p) and t.l<by[7].h]
        assert len(possible)==1
        times[j]=possible[0]
    return times


def classify14(order,records,BY,BW,depth=20):
    Y=past14(order,BY); w=target(BY)
    f14=frozenset({14,7,8,9,10})
    cases=[p for p,f,_ in records if f==f14]
    # Different labelled pasts can give the same polynomial when symmetric old clocks coincide.
    rows=[]
    for p in cases:
        c=incoming(order,p,14)
        assert c.pop(19)==1
        ay=sum(c.values())
        b=sum((k*Y[i] for i,k in c.items()),I.enclose(0))
        d=19+sum((k*Y[i].sq() for i,k in c.items()),I.enclose(0))
        ranges=Counter();open_boxes=[]
        def walk(z,y,h):
            if y.h<=z.l:
                ranges['causality']+=1;return
            gap=I(max(0,y.l-z.h),y.h-z.l)
            deriv=ay*y-b+gap
            D=ay*y.sq()-2*b*y+d+gap.sq()
            if not D.haszero():
                ranges['density']+=1;return
            B=affine({7:-9,8:16,9:-8},BY,BW,z)
            C=affine({7:1,8:-9,9:16,10:-8},BY,BW,y)
            if B.h>=0:raise ValueError('missing collar deficit')
            # Equivalent consequence of G19 and G14, without division by y-z.
            coupled=C*gap+B*deriv
            if not coupled.haszero():
                ranges['clock_pair']+=1;return
            if h==depth:
                open_boxes.append((z.endpoints(),y.endpoints()));return
            if y.h-y.l>z.h-z.l:
                for piece in y.split():walk(z,piece,h+1)
            else:
                for piece in z.split():walk(piece,y,h+1)
        lower=max([w.l]+[Y[i].l for i,k in order if k==14])
        walk(w,I(lower,BY[7].h),0)
        rows.append(dict(past=sorted(p),terminal=dict(ranges),unresolved=len(open_boxes),example=open_boxes[:1]))
    return rows
