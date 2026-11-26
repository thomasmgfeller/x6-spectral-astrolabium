"""Stationary boundary-shape response on one verified N17 order."""
from fractions import Fraction as F
from itertools import combinations
import json
from felder import (ROOT, SOURCE, U, Z, INNER, PAST, FUTURE, COLLAR, E, X,
                    SCALE, Equations, filters, Box, box, serial)
from vakuum import independent_weights

CENTRE=F(1,6)
TARGET=F(1,12)  # nominal t at x=1/2 and e=1/6
DOMAIN=(F(-1,5),F(1,5))
EQ=Equations(COLLAR,COLLAR,'shift')
H=independent_weights(EQ.rel)


def distance(t):
    return (t.square()+6*t+6).sqrt_nonnegative_part()


def shape_factors(t):
    d=distance(t)
    return t*(d+t+9), d*(2-t)*(d+t+3)+27*(2-t+d)


def residual(t,eps):
    n,h=shape_factors(t)
    return (n-eps*h)/192


def derivative(t,eps):
    d=distance(t)
    dp=(t+3)/d
    hprime=dp*(2-t)*(d+t+3)-d*(d+t+3)+d*(2-t)*(dp+1)+27*(dp-1)
    return (d+2*t+9+t*dp-eps*hprime)/192


def sign_at(t,eps):
    r=residual(box(t),eps)
    return 1 if r.lo>0 else -1 if r.hi<0 else 0


def root_interval(eps):
    a,b=DOMAIN
    assert derivative(Box.hull(a,b),eps).lo>0
    assert sign_at(a,eps)==-1 and sign_at(b,eps)==1
    for k in range(45):
        m=(a+b)/2
        sign=sign_at(m,eps)
        if sign==1: b=m
        elif sign==-1: a=m
        else:
            left,right=(a+m)/2,(m+b)/2
            if sign_at(left,eps)==-1: a=left
            if sign_at(right,eps)==1: b=right
    assert sign_at(a,eps)==-1 and sign_at(b,eps)==1 and b-a<F(1,10**9)
    return Box.hull(a,b)


def clocks_old(method,e):
    y={j:box(j-5) for j in PAST+FUTURE}; y[3]=e-2
    ymid={j:box(j-5) for j in PAST+FUTURE};ymid[3]=box(CENTRE)-2
    for j in (i for i in EQ.order if i!=Z):
        assert all(i in y for i,_ in EQ.incoming[j])
        def solve(state):
            terms=[(b,state[i]) for i,b in EQ.incoming[j]]
            a=sum(b for b,_ in terms)
            origin=state[3] if method=='shift' else box(0)
            moment=sum((b*(v-origin) for b,v in terms),box(0))
            c=19+sum((b*(v-origin).square() for b,v in terms),box(0))
            if not a:
                assert moment.lo>0 or moment.hi<0
                return [origin+c/(2*moment)]
            disc=(moment.square()-a*c if method=='shift' else
                  -19*a-sum((b*k*(v-h).square() for (b,v),(k,h) in combinations(terms,2)),box(0)))
            assert disc.lo>0
            s=disc.sqrt_nonnegative_part()
            return [origin+(moment+sign*s)/a for sign in (-1,1)]
        centre_roots=solve(ymid)
        saved=Box.hull(*map(F,SOURCE['clock_midpoint'][str(j)]))
        choices=[k for k,v in enumerate(centre_roots) if v.intersection(saved) is not None]
        assert len(choices)==1
        idx=choices[0]
        ymid[j]=centre_roots[idx];y[j]=solve(y)[idx]
    return y


def components(t,epsilon,e,method):
    y=clocks_old(method,e)
    d=distance(t)
    y.update({Z:t,U:t-d})
    assert all(y[i].hi<y[j].lo for i,j in EQ.rel)
    w={**{i:box(F(1,8)) for i in PAST},**{j:box(F(1,64)) for j in FUTURE},U:box(0)}
    w[7]=(1+epsilon)/64
    for j in reversed(EQ.order):
        m=sum((b*(y[j]-y[i]) for i,b in EQ.incoming[j]),box(0))
        assert m.hi<0 or m.lo>0
        outgoing=sum((b*w[k]*(y[k]-y[j]) for k,b in EQ.outgoing[j]),box(0))
        w[j]=outgoing/m
    assert all(0<w[j].lo<=w[j].hi<SCALE for j in (*INNER,Z,*FUTURE,*PAST))
    return y,w


def action_checks(y,w):
    zero=box(0); step=F(1,1024)
    def lag(yy,ww):
        return 19*sum(ww.values(),zero)+sum((b*ww[k]*(yy[k]-yy[i]).square()
                                              for (i,k),b in H.items()),zero)
    for j in (*INNER,Z,U):
        assert all(y[k].lo-y[i].hi>step*SCALE for i,k in EQ.rel if j in (i,k))
        g=(lag({**y,j:y[j]-step},w)-lag({**y,j:y[j]+step},w))/(4*step)
        assert g.lo<=0<=g.hi
        if j!=U:
            delta=F(1,10**6)
            assert w[j].lo>delta*SCALE and w[j].hi<(1-delta)*SCALE
            variation=(lag(y,{**w,j:w[j]+delta})-lag(y,{**w,j:w[j]-delta}))/(2*delta)
            assert variation.lo<=0<=variation.hi


def charge(y,w,x,e):
    cut=e-2+(4-e)*box(x)
    past={i for i,v in y.items() if v.hi<cut.lo}
    assert all(i in past or v.lo>cut.hi for i,v in y.items())
    return -sum((b*w[j]*(y[j]-y[i]) for (i,j),b in H.items() if i in past and j not in past),box(0))


def x_interval(t):
    # x=(t+2-e)/(4-e), increasing in t and decreasing in e for t<2.
    lo=(F(t.lo,SCALE)+2-E[1])/(4-E[1])
    hi=(F(t.hi,SCALE)+2-E[0])/(4-E[0])
    return Box.hull(lo,hi)


def classify(t,epsilon,source):
    e=Box.hull(*E)
    y,w=components(t,epsilon,e,'shift')
    yy,ww=components(t,epsilon,e,'pairwise')
    assert all(y[j].intersection(yy[j]) is not None and w[j].intersection(ww[j]) is not None for j in y)
    action_checks(y,w)
    net=sum((b*w[j]*(y[j]-y[U]) for (i,j),b in H.items() if i==U),box(0))
    assert net.lo<=0<=net.hi
    windows=json.loads((ROOT/'basis/vorversuch.json').read_text())['CST']['x_fenster']
    windows=[tuple(map(F,iv)) for iv in windows]
    hit=[]
    for lo,hi in windows:
        ids=[]
        for j in (*INNER,Z):
            xx=x_interval(y[j])
            if F(xx.lo,SCALE)>hi or F(xx.hi,SCALE)<lo:continue
            assert lo<=F(xx.lo,SCALE)<=F(xx.hi,SCALE)<=hi
            ids.append(j)
        hit.append(ids)
    return {'mode':source,'epsilon':serial(epsilon),'Y_z':serial(t),'x_z_for_all_e':serial(x_interval(t)),
            'free_positive_min':str(F(min(w[j].lo for j in (*INNER,Z)),SCALE)),
            'free_positive_max':str(F(max(w[j].hi for j in (*INNER,Z)),SCALE)),
            'w_z':serial(w[Z]),'send_positive':hit[0],'receive_positive':hit[1]}


def all_uniform():
    # For unit amplitude with collar-only successors, keep w_z > 1.
    # Such solutions could become admissible after dilution.
    t=Box.hull((1-X[0])*E[0]+4*X[0]-2,(1-X[1])*E[1]+4*X[1]-2)
    outcomes=[]
    for fu,fz in filters():
        if not fu<=COLLAR: continue
        eq=Equations(fu,fz,'shift')
        def test(iv):
            d=distance(iv)
            out=sum((b*(box(k-5)-iv)/64 for k,b in eq.outgoing[Z]),box(0))
            wz=out/(d-iv-3)
            if wz.hi<=0:return 'nonpositive',serial(wz)
            assert wz.lo>0
            u=iv-d
            gu=wz*d + sum((b*(box(k-5)-u)/64 for k,b in eq.outgoing[U] if k in FUTURE),box(0))
            if fu==fz==COLLAR:
                gu=gu.intersection(residual(iv,box(0)))
                assert gu is not None
            assert gu.hi<0 or gu.lo>0
            return 'nonzero_Gu',serial(gu)
        status,iv=test(t)
        outcomes.append({'u_future':sorted(fu),'z_future':sorted(fz),'reason':status,'value_at_unit_scale':iv})
    assert len(outcomes)==15
    return outcomes


def run():
    t0=box(TARGET)
    n,h=shape_factors(t0); eps=n/h
    rows=[]
    for ep in (F(-1,100),F(0),F(1,100)):
        rows.append(classify(root_interval(box(ep)),box(ep),'fixed_before_run'))
    rows.append(classify(t0,eps,'inverse_from_nominal_send_time'))
    rounded=F(6543,10**6)
    assert box(rounded-F(1,2*10**6)).hi<eps.lo<=eps.hi<box(rounded+F(1,2*10**6)).lo
    rows.append(classify(root_interval(box(rounded)),box(rounded),'rounded_after_inversion'))
    anchors=json.loads((ROOT/'basis/vorversuch.json').read_text())['CST']['x_fenster'][0]
    lo,hi=map(F,anchors)
    # For all e at once: the latest lower t-bound and earliest upper t-bound.
    t_low=(1-lo)*E[1]+4*lo-2
    t_high=(1-hi)*E[0]+4*hi-2
    accepted=[]
    for boundary in (t_low,t_high):
        n_bound,h_bound=shape_factors(box(boundary))
        assert h_bound.lo>0
        accepted.append(n_bound/h_bound)
    envelope=Box(accepted[0].hi,accepted[1].lo)
    assert envelope.lo<box(rounded).lo<=box(rounded).hi<envelope.hi
    # Reconstruct all fields over the simultaneous clock-and-dose envelope.
    components(Box.hull(t_low,t_high),envelope,Box.hull(*E),'pairwise')
    base_y,base_w=components(box(0),box(0),box(CENTRE),'pairwise')
    cuts=(F(47,100),F(49,100))
    current=charge(base_y,base_w,cuts[0],box(CENTRE)).intersection(charge(base_y,base_w,cuts[1],box(CENTRE)))
    assert current is not None and current.lo>0
    charges={}
    for s in (F(0),F(1,4),F(1)):
        weights={k:s*v for k,v in base_w.items()}
        q=charge(base_y,weights,cuts[0],box(CENTRE)).intersection(charge(base_y,weights,cuts[1],box(CENTRE)))
        bounded=q.intersection(s*current)
        assert bounded is not None
        charges[str(s)]=serial(bounded)
    return {'reference_type':SOURCE['type'],'e':list(map(str,E)),'controls':rows,
            'sufficient_epsilon_interval_for_send':serial(envelope),'fixed_shape_current':charges, 'uniform_collar_cases':all_uniform(),
            'monotonic_derivative_Gu_on_local_chart':serial(derivative(Box.hull(*DOMAIN),Box.hull(F(-1,100),F(1,100)))),
            'physical_vacuum_measurement':None,'independent_positive_rest_mass':None,
            'physical_radius':None,'physical_P3':'HOLD_NOT_ELIGIBLE','physical_checkpoints_not_run':60}


if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
