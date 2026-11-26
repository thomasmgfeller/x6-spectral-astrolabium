"""Prediction from the single allowed record. No endpoint measurements enter this module."""
from fractions import Fraction as F

PROBES=(4,11,12,13)
PULSES=(-F(1,10**6),F(1,10**6))


def positive_roots(j,clock,edges,order):
    """Solve a free positive density equation using only predecessor clocks."""
    from quelle import box
    incoming=[(clock[i],c) for (i,k),c in edges.items() if k==j and c]
    n=sum(c for v,c in incoming)
    first=sum((c*v for v,c in incoming),box(0))
    second=19+sum((c*v*v for v,c in incoming),box(0))
    if n:
        root=(first*first-n*second).sqrt()
        candidates=[(first+root)/n,(first-root)/n]
    else:
        candidates=[second/(2*first)]
    levels=[clock[i] for i,k in order if k==j]
    return candidates,levels


def old_clocks(collar,edges,order):
    clocks=dict(collar)
    assert set(clocks)=={0,1,2,3}
    for j in (4,5,6,11,12,13,14):
        roots,pre=positive_roots(j,clocks,edges,order)
        chosen=[v for v in roots if all(v.lo>p.hi for p in pre)]
        assert len(chosen)==1 and all(v in chosen or any(v.hi<p.lo for p in pre) for v in roots)
        clocks[j]=chosen[0]
    return clocks


def far_moments(old,weights,edges):
    assert set(weights)==set(PROBES)
    def m(i):
        return sum(c*(old[i]-old[k]) for (k,j),c in edges.items() if j==i and c)
    v4=old[4]
    w14=(weights[11]*(old[11]-v4)-9*weights[12]*(old[12]-v4)
         +weights[13]*(old[13]-v4)-weights[4]*m(4))/(8*(old[14]-v4))
    bilinear=(weights[12]*m(12)-weights[13]*m(13))/(old[13]-old[12])
    moment=weights[12]*m(12)+old[12]*bilinear
    return bilinear-w14,moment-old[14]*w14


def read(old,weights,u,h,edges,order,windows):
    from quelle import box,SCALE
    W,M=far_moments(old,weights,edges)
    P=h*W-M
    assert P.lo>0
    s=(u*u-6)/(2*(u+3))
    clocks={**old,15:u,16:s,17:h}
    roots,pre=positive_roots(18,clocks,edges,order)
    def chart(t):
        return (t+F(11,6))/F(23,6)
    def inside(j,c):
        x=chart(c);l,r=windows[j]
        return l*SCALE<=x.lo<=x.hi<=r*SCALE
    chosen=[v for v in roots if inside(1,v)]
    assert len(chosen)==1 and inside(0,s)
    t=chosen[0]
    assert all(t.lo>v.hi for v in pre)
    for root in roots:
        if root is not t:
            interval=chart(root)
            assert interval.hi<windows[1][0]*SCALE or interval.lo>windows[1][1]*SCALE
    mz=-(u+3)
    mr=sum(c*(t-clocks[k]) for (k,i),c in edges.items() if i==18 and c)
    wr=P/(t-h)
    wz=(h-s)*(W+wr)/mz
    assert wz.lo>0 and wr.lo>0
    K0=wz*(s-u)
    arms=[]
    for source in PULSES:
        d=box(source)/(2*mz)
        B=mr-d
        C=d*(d-2*(t-s))
        q=C/(-B+(B*B-C).sqrt())
        assert B.hi<0 and inside(1,t+q) and inside(0,s+d)
        new_wr=P/(t+q-h)
        new_wz=(h-s-d)*(W+new_wr)/mz
        absolute=new_wz*(s+d-u)
        az=d*(1+(s+d-u)/(s-h))
        ar=q*(s+d-u)*(s+d-h)/(mz*(t+q-h))
        delta=az*wz+ar*wr
        assert (absolute-K0-delta).contains_zero()
        assert delta.lo>0 if source<0 else delta.hi<0
        arms.append({'delta':delta,'absolute':absolute,'s':s+d,'t':t+q,'wz':new_wz,'wr':new_wr})
    return {'W':W,'M':M,'P':P,'s':s,'t':t,'wz':wz,'wr':wr,'K0':K0,'arms':arms}
