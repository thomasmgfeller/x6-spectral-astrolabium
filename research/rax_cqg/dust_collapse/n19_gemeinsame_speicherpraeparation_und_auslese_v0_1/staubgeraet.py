"""Analytic completion of the dust saddle for the three prepared travelling pointers."""
from fractions import Fraction as F
from wege import ROUTES,forward


def solve(y,w,J,velocity,k,mismatch,route):
    from quelle import box,hull,SCALE
    from gemischt import FUT,COEFF
    from speichermodell import square
    from uhrauslese import sender
    vu,vh,vt=velocity
    pu,ph,pt=(k*v for v in velocity)
    summed=sum((square(v) for v in velocity),box(0))
    load_z=k*(summed if route=='positive_bridge' else square(vu))
    load_r=k*summed
    u,s0,h,t0=(y[i] for i in (15,16,17,18))
    W=sum(COEFF.get((17,i),0)*w[i] for i in FUT)
    W3=sum(COEFF.get((18,i),0)*w[i] for i in FUT)
    P=w[18]*(t0-h)
    C=1+mismatch
    denom=P+ph
    assert denom.lo>0 and C.lo>0
    rr=load_r*square(C)/square(denom)
    mz=-(u+3)
    mr=sum(c*(t0-y[i]) for (i,j),c in COEFF.items() if j==18 and c)
    ds=box(J)/(2*mz)
    def clocks(extra):
        d=ds+extra
        a=1+2*mismatch+rr
        b=mr-d+mismatch*(t0-s0-d)+(mismatch+rr)*(t0-h)
        c=d*(d-2*(t0-s0))+mismatch*square(t0-s0-d)+(mismatch+rr)*square(t0-h)
        discr=square(b)-a*c
        assert b.hi<0 and discr.lo>0 and a.lo>0
        divisor=-b+discr.sqrt()
        shift=c/divisor
        assert (divisor/a).lo>F(1,1000)*SCALE
        s=s0+d;t=t0+shift
        wr=denom/(C*(t-h))
        wz=((h-s)*(W+C*wr)+ph)/(mz+mismatch*(s-u))
        assert wz.lo>0 and wr.lo>0
        return s,t,wz,wr,shift,d
    def update(extra):
        s,_,wz,_,_,_=clocks(extra)
        return (load_z/square(wz)+mismatch*square(s-u))/(2*(u+3))
    wide=hull(-F(1,10**7),F(1,10**7))
    enclosed=update(wide)
    assert wide.lo<enclosed.lo<=enclosed.hi<wide.hi
    extra=update(enclosed)
    s,t,wz,wr,shift,d=clocks(extra)
    assert (extra-update(extra)).contains_zero()
    assert (s-sender(u,J)-extra).contains_zero()
    delta_z=C*wz*(s-u)-w[16]*(s0-u)
    delta_r=wr*(t-u)-w[18]*(t0-u)
    l1=(pu-delta_z+9*delta_r)/(y[11]-u)
    mr_new=mr+shift-d+mismatch*(2*t-s-h)
    l3=(pt-pu-ph-mismatch*w[7]*(y[7]-t)+shift*W3+wr*mr_new-w[18]*mr)/(y[14]-t)
    def tail(x,z):
        w8=-x/8;w9=2*w8
        return (box(0),w8,w9,(-9*w8+16*w9-z)/8)
    yy={**y,16:s,18:t}
    ww={**w,16:wz,18:wr}
    for i,dw,dm in zip(FUT,tail(l1,l3),tail(y[11]*l1,y[14]*l3)):
        if i!=7:
            ww[i]=w[i]+dw
            yy[i]=(w[i]*y[i]+dm)/ww[i]
    return dict(y=yy,w=ww,extra=extra,receiver_defect=load_r/square(wr))


def verify(state,J,velocity,k,mismatch,route,q):
    from gemischt import CLOCK,WEIGHT,ORDER,WINDOWS
    from quelle import SCALE,box
    from zustand import gradients
    yy,ww=state['y'],state['w']
    pointers,factors=forward(state,route,q,velocity)
    G,D=gradients(yy,ww)
    for channels,hist,v in zip(ROUTES[route],pointers,velocity):
        last=0;initial=k*v
        for j,inertia,probe in channels:
            delta_y=(yy[j]-yy[probe[0]]) if probe else box(0)
            relative=hist[j]-hist[last]-delta_y
            measured=k*ww[inertia]*relative
            assert (measured-initial).contains_zero()
            D[inertia]+=k*relative*relative
            if probe:
                i,_=probe
                G[i]+=mismatch*ww[j]*delta_y-measured
                G[j]-=mismatch*ww[j]*delta_y-measured
                D[j]+=mismatch*delta_y*delta_y
            last=j
    assert all(G[i].contains_zero() for i in CLOCK)
    assert all((D[i]-(J if i==16 else 0)).contains_zero() for i in WEIGHT)
    assert all(yy[i].hi<yy[j].lo for i,j in ORDER)
    assert all(ww[i].lo==ww[i].hi==0 if i in (15,17) else 0<ww[i].lo<=ww[i].hi<SCALE for i in yy)
    for end in (box(2),yy[7]):
        z={i:(v+F(11,6))/(end+F(11,6)) for i,v in yy.items()}
        for (lo,hi),target in zip(WINDOWS,(16,18)):
            assert lo*SCALE<z[target].lo<=z[target].hi<hi*SCALE
            assert all(i==target or ww[i].hi==0 or v.hi<lo*SCALE or v.lo>hi*SCALE for i,v in z.items())
    return pointers,factors
