"""Construct new held-out null histories and check what an absolute receiver digit forgets."""
from fractions import Fraction as F
from itertools import product
from empfangsbit import STEP,K0,V,CAL,R,THRESHOLD,bounds,receiver_bit


def displaced(y,w,alpha):
    from quelle import box
    from gemischt import COEFF,CLOCK,WEIGHT,FUT,PAST
    from zustand import gradients,check
    from algebra import solve_box
    u=y.copy()
    tt,hh=y[18],y[17]
    other=sum((c*(tt-y[i]) for (i,j),c in COEFF.items() if j==18 and i!=17),box(0))
    u[18]=tt+alpha
    u[17]=u[18]-((tt-hh)*(tt-hh)-2*alpha*other).sqrt()
    coords=[('w',j) for j in WEIGHT+FUT]+[('M',j) for j in FUT]
    old,_=gradients(y,w);new,_=gradients(u,w)
    def row(i):
        incoming=sum((c*(u[i]-u[k]) for (k,j),c in COEFF.items() if j==i),box(0))
        out=[]
        for typ,j in coords:
            c=COEFF.get((i,j),0)
            if typ=='M':a=box(c)
            elif j in FUT:a=-c*u[i]
            else:a=c*(u[j]-u[i])-(incoming if j==i else box(0))
            out.append(a)
        return out
    def unit(key):return [box(int(z==key)) for z in coords]
    ids=CLOCK+PAST
    matrix=[row(i) for i in ids]+[unit(('w',16)),
             [a-y[7]*b for a,b in zip(unit(('M',7)),unit(('w',7)))]]
    rhs=[old[i]-new[i] for i in ids]+[box(0),box(0)]
    dw=dict(zip(coords,solve_box(matrix,rhs)))
    ww=w.copy()
    for j in WEIGHT+FUT:ww[j]=w[j]+dw['w',j]
    for j in FUT:u[j]=(w[j]*y[j]+dw['M',j])/ww[j]
    assert (u[7]-y[7]).contains_zero() and (ww[16]-w[16]).contains_zero()
    u[7]=y[7];ww[16]=w[16]
    check(u,ww)
    G,_=gradients(u,ww)
    assert all((G[i]-old[i]).contains_zero() for i in PAST)
    return u,ww


def run(previous,early):
    from quelle import box,hull
    from proben import samples
    from staubgeraet import solve,verify
    from uhrauslese import LABELS
    from wege import ROUTES
    from nullreferenz import digit,maxabs
    from kollision import midpoint
    base=samples(previous,early)[0][0];name,y,w=base
    assert name=='reference'
    v0=(box(0),)*3;route='positive_bridge'
    def zr(yy,ww,J):
        st=solve(yy,ww,J,v0,K0,box(-K0),route)
        h,_=verify(st,J,v0,K0,box(-K0),route,v0)
        return st,h
    driven,_=zr(y,w,LABELS[2])
    target=digit(driven['y'][18])
    # Solve for a different undriven baseline giving the very same receiver clock digit.
    shift=F(0)
    for _ in range(4):
        null=displaced(y,w,shift)
        quiet,_=zr(*null,F(0))
        if digit(quiet['y'][18])==target:break
        shift+=F(round((target*STEP-midpoint(quiet['y'][18]))*10**18),10**18)
    assert digit(quiet['y'][18])==target
    baseline_a,baseline_b=digit(y[18]),digit(null[0][18])
    assert receiver_bit(target,baseline_a)==1 and receiver_bit(target,baseline_b)==0
    rows=[]
    for alpha in (shift,F(-3,10**7),F(2,10**7),F(7,10**7)):
        yy,ww=displaced(y,w,alpha)
        safe=0
        for route,k,J in product(ROUTES,(F(1),K0),LABELS):
            vel=(hull(-96*K0*V/k,96*K0*V/k),)*3
            delta=hull(-K0,K0) if k==1 else box(-k)
            st=solve(yy,ww,J,vel,k,delta,route)
            hist,A=verify(st,J,vel,k,delta,route,(hull(-1,1),)*3)
            assert all(maxabs(a)<8-2*STEP for a in (yy[18],st['y'][18],st['y'][7],hist[2][7]))
            d=st['y'][18]-yy[18]
            lo,hi=bounds(d,CAL+2*R)
            l,h=bounds(d-A[2][7]*vel[2],CAL+5*R)
            safe+=int((-THRESHOLD<=lo<=hi<=THRESHOLD) if J==0 else
                      (lo>THRESHOLD and l>0 if J>0 else hi< -THRESHOLD and h<0))
        rows.append({'alpha':str(alpha),'families':12,'one_bit_correct_at_m96':safe})
    return {'same_absolute_clock_code':target,'positive_source':str(LABELS[2]),'other_source':'0',
            'second_null_shift':str(shift),'separate_calibration_codes':[baseline_a,baseline_b],
            'paired_bits':[1,0],'wrong_baseline_bit_for_zero':receiver_bit(target,baseline_a),'holdout':rows}
