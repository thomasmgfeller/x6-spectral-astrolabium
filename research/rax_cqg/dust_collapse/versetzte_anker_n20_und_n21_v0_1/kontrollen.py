"""Exact variations of the original action and rational checks of interval operations."""
from fractions import Fraction as F
from itertools import product
from intervall import I,Q
from freie_felder import structure,DUST
from ordnungen import LAYERS


def arithmetic():
    numbers=[F(-17,13),F(-1,3),F(-1,10**17),F(0),F(1,10**17),F(2,7),F(8,3)]
    ranges=[(a,b,I.enclose(a,b)) for a in numbers for b in numbers if a<=b]
    def contains(candidate,points):
        assert all(F(candidate.l,Q)<=p<=F(candidate.h,Q) for p in points)
    for a,b,x in ranges:
        contains(x,[a,b])
        contains(x.sq(),[s*s for s in (a,(a+b)/2,b)]+([0] if a<=0<=b else []))
        if a>=0:
            root=x.sqrt()
            assert F(root.l,Q)**2<=a<=b<=F(root.h,Q)**2
        for c,d,y in ranges:
            pairs=list(product((a,b),(c,d)))
            contains(x+y,[i+j for i,j in pairs])
            contains(x-y,[i-j for i,j in pairs])
            contains(x*y,[i*j for i,j in pairs])
            if not y.haszero():contains(x/y,[i/j for i,j in pairs])
    return len(ranges)**2


def action_checks(order,records,routes):
    k=F(1,79);mu=-k;J=F(1,43);step=F(1,4096)
    velocities=(F(-2,11),F(3,13),F(5,17));mom=[k*v for v in velocities]
    y=[F(i-8,9) for i in range(20)]
    for i,v in {0:-5,1:-4,2:-3,3:F(-11,6),7:2,8:3,9:4,10:5,15:-2,16:F(1,12),17:-4,18:F(1,8),19:F(1,11)}.items():y[i]=F(v)
    w=[F(i+1,31) if i not in (15,17,19) else F(0) for i in range(20)]
    traces=[]
    for v,track in zip(velocities,routes,strict=True):
        hist={0:F(0)};last=0
        for j,inertia,probe in track:
            delta=y[probe[1]]-y[probe[0]] if probe else 0
            hist[j]=hist[last]+delta+v/w[inertia];last=j
        traces.append(hist)
    total=0;receiver_checks=0;dust_checks=0
    for p,f,_ in records:
        pred,succ,inc,out=structure(order,p,f)
        # Independent layer definition by explicitly intersecting each old/new open interval.
        edges=[(i,j) for i in range(20) for j in range(20) if j in succ[i]]
        counts={(i,j):sum((i,a) in edges and (a,j) in edges for a in range(20)) for i,j in edges}
        coeff={(i,j):LAYERS[t] for (i,j),t in counts.items() if t<4}
        assert coeff=={(i,j):c for j,m in inc.items() for i,c in m.items()}
        def action(Y,W):
            val=19*sum(W)+sum(c*W[j]*(Y[j]-Y[i])**2 for (i,j),c in coeff.items())-J*W[16]
            for track,hist in zip(routes,traces,strict=True):
                last=0
                for j,inertia,probe in track:
                    gap=Y[probe[1]]-Y[probe[0]] if probe else 0
                    val+=k*W[inertia]*(hist[j]-hist[last]-gap)**2
                    if probe:val+=mu*W[j]*gap**2
                    last=j
            return val
        def diff(j,kind):
            left,right=y.copy(),y.copy()
            if kind=='Y':
                left[j]-=step;right[j]+=step
                return -(action(right,w)-action(left,w))/(4*step)
            left,right=w.copy(),w.copy()
            left[j]-=step;right[j]+=step
            return (action(y,right)-action(y,left))/(2*step)
        g=sum(v*w[j]*(y[j]-y[19]) for j,v in out[19].items())
        assert diff(19,'Y')==g
        total+=1
        if f=={14,7,8,9,10}:
            for j in DUST:
                density=19+sum(v*(y[j]-y[i])**2 for i,v in inc[j].items())
                flow=sum(v*w[n]*(y[n]-y[j]) for n,v in out[j].items())-w[j]*sum(v*(y[j]-y[i]) for i,v in inc[j].items())
                assert diff(j,'W')==density and diff(j,'Y')==flow
                dust_checks+=2
        if f-set((7,8,9,10)) not in ({18},{17,18}):continue
        s,r,u,h,z=(y[j] for j in (16,18,15,17,19))
        a=s-u;b=r-h;t=r-s;delta=r-z;ws=w[16];wr=w[18]
        ca=inc[18][15];ch=inc[18][17];cz=inc[18][19]
        C=lambda i,x:sum(v*w[j]*(y[j]-x) for j,v in out[i].items() if j in (7,8,9,10))
        slope=sum(v*w[j] for j,v in out[17].items() if j in (7,8,9,10))
        load=k*sum(v*v for v in velocities)
        m,square=0,19
        for i,v in inc[18].items():
            if i in (0,1,2,3):
                m+=v*(r-y[i]);square+=v*(r-y[i])**2
        expected={(17,'Y'):C(17,r)+(slope+(ch-k)*wr)*b-mom[1],
                  (16,'W'):(1-k)*a*a-s*s-6*s-6-J+load/ws**2,
                  (16,'Y'):C(16,s)+(1-k)*wr*t+ws*(s+3-(1-k)*a),
                  (15,'Y'):(1-k)*ws*a+ca*wr*(t+a)+C(15,u)-mom[0],
                  (18,'W'):square+ca*(t+a)**2+(1-k)*t*t+(ch-k)*b*b+cz*delta**2+load/wr**2,
                  (18,'Y'):C(18,r)-k*w[7]*(y[7]-r)+mom[0]+mom[1]-mom[2]-wr*(m+ca*(t+a)+(1-k)*t+(ch-k)*b+cz*delta)}
        for (j,kind),val in expected.items():
            assert diff(j,kind)==val;receiver_checks+=1
    return {'vacuum':total,'dust_side':dust_checks,'receiver':receiver_checks}
