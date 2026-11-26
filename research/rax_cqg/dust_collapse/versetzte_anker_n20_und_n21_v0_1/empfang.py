"""Interval test of the coupled receiver branch with unknown interior fields."""
from fractions import Fraction as F
from collections import Counter
from intervall import I,Q,span
from auslese import target,affine
from freie_felder import structure,intersection

E=I.enclose(0)
ONE=I.enclose(1)
# Outward device errors. |k|=1e-11, |v_j|<=1.12e-12; exact k below.
K=I.enclose(F(1,10**11))
J=I.enclose(F(-1,10**6),F(1,10**6))
MOM=I.enclose(F(-112,10**25),F(112,10**25))
LOAD=I.enclose(0,3*F(1,10**11)*F(112,10**14)**2)


def check_box(data,Y,W,z,s,r,alpha,small):
    pred,succ,inc,out=data
    # Each of the nine unsettled cases requires z and 16 incomparable,
    # and r=18 in their future, so the observed positive comparator is 16.
    delta=intersection(r-z,I(0,2*Q));t=intersection(r-s,I(0,2*Q))
    if delta is None or t is None or not delta.h or not t.h:return 'time'
    collar=lambda i,clock:affine({j:v for j,v in out[i].items() if j in (7,8,9,10)},Y,W,clock)
    cz=inc[18][19];ca=inc[18][15];ch=inc[18][17]
    assert inc[18][16]==1 and out[15][16]==1
    charge=-collar(19,z)/cz
    if charge.h<=0 or charge.l>delta.h:return 'Gz'
    assert charge.l>0
    delta=intersection(delta,I(charge.l,2*Q))
    wr=intersection(charge/delta,I(0,Q))
    if wr is None:return 'Gz'
    # Avoid loss of precision when squaring very small weights: the lower weight
    # bound obtained from the vacuum equation is macroscopic in both families.
    assert wr.l>Q//1000
    # Solve the affine null-clock equation at 17 for beta=r-Y17.
    slope=sum((k*W[j] for j,k in out[17].items() if j in (7,8,9,10)),E)
    denom=slope+(ch-K)*wr
    num=MOM-collar(17,r)
    beta=I(0,r.h+5*Q)
    if 17 in succ[19]:beta=intersection(beta,I(0,delta.h))
    if 17 in pred[19]:beta=intersection(beta,I(delta.l,7*Q))
    if beta is None:return 'G17_time'
    if denom.haszero():
        if not (num-denom*beta).haszero():return 'G17'
    else:
        beta=intersection(beta,num/denom)
        if beta is None:return 'G17'
    # D16 requires alpha=s-Y15>0. Split possible sender weights at 10^-6.
    maxterm=I.enclose(0,F(3,10**22)) if not small else None
    # For w>=1e-6 the actual load/w² is <=3.764e-23; allow 3e-22.
    basic=s.sq()+6*s+6+J
    d2=I(0,basic.h) if small else basic-maxterm
    d2=d2/(ONE-K)
    alpha=intersection(alpha,d2.sqrt())
    if alpha is None:return 'D16'
    u=s-alpha
    if 15 in pred[19] and u.l>=z.h:return 'time'
    ws=I(0,Q//10**6) if small else I(Q//10**6,Q)
    rhs=-collar(16,s)-(ONE-K)*wr*t
    fac=s+3-(ONE-K)*alpha
    if not (rhs-fac*ws).haszero():return 'G16'
    if not fac.haszero():
        ws=intersection(ws,rhs/fac)
        if ws is None:return 'G16'
    if not ((ONE-K)*ws*alpha+ca*wr*(t+alpha)+collar(15,u)-MOM).haszero():return 'G15'
    dcoll=I.enclose(19)
    scoll=E
    for i,c in inc[18].items():
        if i in (0,1,2,3):
            dcoll+=c*(r-Y[i]).sq();scoll+=c*(r-Y[i])
    d=dcoll+ca*(t+alpha).sq()+(ONE-K)*t.sq()+(ch-K)*beta.sq()+cz*delta.sq()+LOAD/wr.sq()
    if not d.haszero():return 'D18'
    g=collar(18,r)-K*W[7]*(Y[7]-r)+3*MOM-wr*(scoll+ca*(t+alpha)+(ONE-K)*t+(ch-K)*beta+cz*delta)
    if not g.haszero():return 'G18'
    return 'open'


def classify_receiver(order,p,f,Y,W,windows,narrow=False,max_depth=13):
    data=structure(order,p,f);z=target(Y)
    if narrow:
        raw=lambda pair:Y[3]+(Y[7]-Y[3])*I.enclose(*pair)
        s,r=map(raw,windows)
    else:
        s=z;r=I(z.l,Y[7].h)
    stats=Counter();examples=[]
    def visit(boxes,small,d):
        state=check_box(data,Y,W,*boxes,small)
        if state!='open' or d>=max_depth:
            stats[state]+=1
            if state=='open' and len(examples)<1:examples.append([x.endpoints() for x in boxes]+[small])
            return
        # In the large weight branch D16 already pins alpha closely.
        scale=[4,4,1,1 if small else 0]
        axis=max(range(4),key=lambda j:scale[j]*(boxes[j].h-boxes[j].l))
        for part in boxes[axis].split():
            sub=boxes.copy();sub[axis]=part
            visit(sub,small,d+1)
    for small in (False,True):
        visit([z,s,r,I(0,4*Q)],small,0)
    return dict(terminal=dict(stats),example=examples)
