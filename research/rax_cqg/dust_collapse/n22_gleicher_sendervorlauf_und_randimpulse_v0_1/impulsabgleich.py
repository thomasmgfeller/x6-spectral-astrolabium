"""Enclose all 30 mixed-boundary equations with the same early momenta."""
from fractions import Fraction as F
from decimal import Decimal as D
from quelle import box,hull,SCALE
from algebra import mid,inv
from feldroehre import POS,absmax
from randversuch import dot,build,PAST
from impulsfelder import fields
from leseregel import digits,decode,ERROR,REFERENCE

EXTRA=(('y',8),('y',9),('w',7),('w',8),('w',9))

def coords(y,w,axes):
    return [(y if k=='y' else w)[j] for k,j in axes]

def setcoords(y,w,axes,x):
    yy,ww=y.copy(),w.copy()
    for (k,j),s in zip(axes,x,strict=True):
        (yy if k=='y' else ww)[j]=s
    return yy,ww

def certify_currents(seed,collar,source,coeff,free,rel,goals):
    axes=[('y',j) for j in free]+[('w',j) for j in POS]+list(EXTRA)
    by,bw=build(seed,collar)
    y,w=list(map(mid,by)),list(map(mid,bw))
    c=[(i,j,mid(k)) for (i,j),k in sorted(coeff.items())]
    x=coords(y,w,axes)
    for _ in range(5):
        v,A,_=fields(*setcoords(y,w,axes,x),mid(source),c,free,axes,list(map(mid,goals)),D)
        pre=inv(A)
        x=[a-sum(k*b for k,b in zip(row,v)) for a,row in zip(x,pre)]
    x=[F(v).limit_denominator(10**21) for v in x]
    cy,cw=setcoords(by,bw,axes,list(map(box,x)))
    c=[(i,j,box(k)) for (i,j),k in sorted(coeff.items())]
    v,A,_=fields(cy,cw,box(source),c,free,axes,list(map(box,goals)),box)
    C=[[(j,box(k)) for j,k in enumerate(row) if k] for row in inv(A)]
    radii=[F(1,10**10 if k=='y' else 10**11) for k,j in axes]
    yy,ww=setcoords(by,bw,axes,[box(u)+hull(-r,r) for u,r in zip(x,radii)])
    _,Aj,_=fields(yy,ww,box(source),c,free,axes,list(map(box,goals)),box)
    beta=[];q=[]
    for i,row in enumerate(C):
        beta.append(absmax(dot(row,v))/radii[i])
        q.append(sum(absmax(int(i==j)-dot(row,col))*s for j,(s,col) in enumerate(zip(radii,zip(*Aj))))/radii[i])
    eta=max(a+b for a,b in zip(beta,q))
    assert max(q)<1 and eta<1,(float(max(q)),float(eta))
    ly,lw=setcoords(by,bw,axes,[box(u)+hull(-r*(a+b),r*(a+b)) for u,r,a,b in zip(x,radii,beta,q)])
    assert all(ly[i].hi<ly[j].lo for i,j in rel)
    assert all(0<lw[i].lo<=lw[i].hi<SCALE for i in set(range(22))-{15,17,20})
    assert all(lw[i].lo==lw[i].hi==0 for i in (15,17,20))
    assert all(absmax(ly[j]-ly[i])<8 for i,j in ((15,16),(15,18),(17,18),(18,7)))
    fv,_,_=fields(ly,lw,box(source),c,free,axes,list(map(box,goals)),box)
    assert all(v.contains_zero() for v in fv)
    l,h=map(F,ly[21].data())
    ds=list(digits(l-ERROR,h+ERROR))
    decisions=sorted({decode(n,r) for n in ds for r in range(REFERENCE-1,REFERENCE+2)})
    width=lambda v:str(F(-(-v*10**12//1),10**12))
    # Independent rational checks of all columns, using receiving-edge energy derivatives.
    y,w=([sum(map(F,v.data()))/2 for v in s] for s in (cy,cw))
    ce=[(i,j,F(k)) for (i,j),k in coeff.items()]
    _,ja,_=fields(y,w,source,ce,free,axes,goals,F)
    def independent(z,u):
        vals=[19-source*(t==16)+sum(k*(z[b]-z[a])**2 for a,b,k in ce if b==t) for t in POS]
        def flow(t):return sum(k*u[b]*(z[b]-z[a])*(int(a==t)-int(b==t)) for a,b,k in ce if t in (a,b))
        return vals+[flow(t) for t in free]+[z[15]-goals[0]]+[flow(t)-goals[t+1] for t in range(4)]
    for col,(k,j) in enumerate(axes):
        a,b=y.copy(),y.copy();v,s=w.copy(),w.copy()
        lo,hi=(a,b) if k=='y' else (v,s)
        dh=F(1,1000);lo[j]-=dh;hi[j]+=dh
        upper,lower=independent(b,s),independent(a,v)
        assert all((u-l)/(2*dh)==row[col] for u,l,row in zip(upper,lower,ja))
    return dict(J=str(source),receiver=ly[21].data(),receiver_codes=[min(ds),max(ds)],decisions=decisions,
                control_values={k+str(j):(ly if k=='y' else lw)[j].data() for k,j in EXTRA},
                control_displacements={k+str(j):((ly if k=='y' else lw)[j]-(by if k=='y' else bw)[j]).data() for k,j in EXTRA},
                fixed_past={str(j):[(str(goals[0]) if j==15 else ly[j].data()[0]),lw[j].data()[0]] for j in PAST},
                goals=list(map(str,goals)),equations=len(axes),upper_contraction=width(max(q)),upper_image=width(eta),
                jacobian_entries=len(axes)**2,strict_relations=len(rel))
