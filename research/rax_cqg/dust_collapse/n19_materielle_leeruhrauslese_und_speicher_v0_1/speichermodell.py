"""Stationary coupled dust-register solution, including finite terminal loads."""
from fractions import Fraction as F


def square(v):
    from quelle import SCALE,hull
    lower=0 if v.contains_zero() else min(v.lo*v.lo,v.hi*v.hi)
    return hull(F(lower,SCALE*SCALE),F(max(v.lo*v.lo,v.hi*v.hi),SCALE*SCALE))


def coupled(y,w,initial_source,source,pu,ph,chain=True,gain=1,mismatch=0,pt=0,stiffness=1):
    """Continue an unloaded background onto either explicitly defined apparatus."""
    from quelle import box,hull,SCALE
    from gemischt import FUT,COEFF
    from uhrauslese import sender
    h,u,s0,t0=[y[j] for j in (17,15,16,18)]
    W=sum(COEFF.get((17,j),0)*w[j] for j in FUT)
    W3=sum(COEFF.get((18,j),0)*w[j] for j in FUT)
    P=w[18]*(t0-h)
    denominator=P+gain*ph
    assert denominator.lo>0
    assert stiffness>0
    if not chain:
        assert mismatch==0
    coupling=1+mismatch
    q2=(square(pu)+square(ph))*coupling*coupling/(stiffness*square(denominator))
    mz=-(u+3)
    mr0=sum(c*(t0-y[i]) for (i,j),c in COEFF.items() if j==18 and c)
    a=1+2*mismatch+q2
    ds=(box(source-initial_source))/(2*mz)
    def geometry(extra):
        d=ds+extra
        b=mr0-d+mismatch*(t0-s0-d)+(mismatch+q2)*(t0-h)
        c=d*(d-2*(t0-s0))+mismatch*square(t0-s0-d)+(mismatch+q2)*square(t0-h)
        discr=square(b)-a*c
        assert b.hi<0 and discr.lo>0
        divisor=-b+discr.sqrt()
        shift=c/divisor
        other=divisor/a
        assert other.lo>F(1,1000)*SCALE
        t=t0+shift
        s=s0+d
        wr=denominator/(coupling*(t-h))
        wz=((h-s)*(W+coupling*wr)+gain*ph)/(mz+mismatch*(s-u))
        assert wz.lo>0 and wr.lo>0
        return s,t,wz,wr,shift,d
    def fixed_point(extra):
        s,_,wz,_,_,_=geometry(extra)
        return (square(pu)/(stiffness*square(wz))+mismatch*square(s-u))/(2*(u+3)) if chain else box(0)
    # A strict self-map of this compact interval gives existence by the
    # intermediate value theorem (for each exact admissible input).
    radius=F(1,10**7)
    wide=hull(-radius,radius)
    err=fixed_point(wide)
    assert wide.lo<err.lo<=err.hi<wide.hi
    extra=fixed_point(err)
    s,t,wz,wr,shift,d=geometry(extra)
    assert (s-sender(u,source)-extra).contains_zero()
    assert (extra-fixed_point(extra)).contains_zero()
    # Recover the two free far-layer changes while keeping the shared
    # row 12/13 moments and the full field at 7 fixed.
    change_z=coupling*wz*(s-u)-w[16]*(s0-u)
    change_r=wr*(t-u)-w[18]*(t0-u)
    l1=(gain*pu-change_z+9*change_r)/(y[11]-u)
    mr=mr0+shift-d+mismatch*(t-s)+mismatch*(t-h)
    l3=(pt-gain*(pu+ph)-mismatch*w[7]*(y[7]-t)+shift*W3+wr*mr-w[18]*mr0)/(y[14]-t)
    def future(x,z):
        f8=-x/8
        f9=2*f8
        return (box(0),f8,f9,(-9*f8+16*f9-z)/8)
    yy={**y,16:s,18:t}
    ww={**w,16:wz,18:wr}
    for i,dw,dm in zip(FUT,future(l1,l3),future(y[11]*l1,y[14]*l3)):
        if i!=7:
            ww[i]=w[i]+dw
            yy[i]=(w[i]*y[i]+dm)/ww[i]
    if chain:
        relay=gain*(s-u)+pu/(stiffness*wz)
        xu=relay+gain*(t-s)+pu/(stiffness*wr)
    else:
        relay=None
        xu=gain*(t-u)+pu/(stiffness*wr)
    xh=gain*(t-h)+ph/(stiffness*wr)
    stored=(xu+pu/(stiffness*ww[7]),xh+ph/(stiffness*ww[7]))
    state=dict(y=yy,w=ww,relay=relay,read=(xu,xh),stored=stored,extra=extra,
               stamp=yy[7]-t+pt/(stiffness*ww[7]),receiver_source_defect=(square(pu)+square(ph))/(stiffness*square(wr)),q=shift)
    verify(state,source,pu,ph,chain,gain,mismatch,pt,stiffness)
    return state


def verify(state,source,pu,ph,chain,gain,mismatch,pt,stiffness):
    from gemischt import CLOCK,WEIGHT,ORDER,WINDOWS
    from quelle import box,SCALE
    from zustand import gradients
    y,w=state['y'],state['w']
    xu,xh=state['read']
    zu,zh=state['stored']
    r,z,k=18,16,7
    relay=state['relay']
    # Derivatives of the unreduced link action, keeping every position independent.
    if chain:
        v1=relay-gain*(y[z]-y[15])
        v2=xu-relay-gain*(y[r]-y[z])
        p1=stiffness*w[z]*v1
    else:
        v2=xu-gain*(y[r]-y[15])
    vh=xh-gain*(y[r]-y[17])
    p2,pmh=stiffness*w[r]*v2,stiffness*w[r]*vh
    p7u,p7h=stiffness*w[k]*(zu-xu),stiffness*w[k]*(zh-xh)
    assert (p2-p7u).contains_zero() and (pmh-p7h).contains_zero()
    assert (p7u-pu).contains_zero() and (p7h-ph).contains_zero()
    G,D=gradients(y,w)
    if chain:
        for i,j in [(15,z),(z,r),(17,r),(r,k)]:
            gap=y[j]-y[i]
            flow=mismatch*w[j]*gap
            G[i]+=flow
            G[j]-=flow
            D[j]+=mismatch*gap*gap
    if chain:
        assert (p1-p2).contains_zero()
        G[15]-=gain*p1
        G[z]+=gain*(p1-p2)
        D[z]+=stiffness*v1*v1
    else:
        G[15]-=gain*p2
    stamp_momentum=stiffness*w[k]*(state['stamp']-(y[k]-y[r]))
    assert (stamp_momentum-pt).contains_zero()
    G[r]+=gain*(p2+pmh)-stamp_momentum
    G[17]-=gain*pmh
    D[r]+=stiffness*(v2*v2+vh*vh)
    assert all(G[j].contains_zero() for j in CLOCK)
    assert all((D[j]-(source if j==z else 0)).contains_zero() for j in WEIGHT)
    assert all(y[i].hi<y[j].lo for i,j in ORDER)
    assert all((0<w[j].lo<=w[j].hi<SCALE) if j not in (15,17) else w[j].lo==w[j].hi==0 for j in y)
    for end in (box(2),y[7]):
        chart={i:(v+F(11,6))/(end+F(11,6)) for i,v in y.items()}
        for (lo,hi),j in zip(WINDOWS,(z,r)):
            assert lo*SCALE<chart[j].lo<=chart[j].hi<hi*SCALE
            assert all(i==j or w[i].hi==0 or t.hi<lo*SCALE or t.lo>hi*SCALE for i,t in chart.items())
