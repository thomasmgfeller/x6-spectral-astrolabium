"""Invert the two unloaded positive-density equations using two independent precursor clocks."""
from fractions import Fraction as F
from itertools import product
from math import floor

STEPS=(F(2,10**12),F(1,10**12),F(5,10**13),F(25,10**14))
BIASES=(F(0), F(1,4*10**12),F(1,10**12))


def root(u,h):
    from uhrauslese import sender
    from speichermodell import square
    s=sender(u,0)
    b=16+9*u-s-h
    c=35-9*square(u)+square(s)+square(h)
    disc=square(b)-c
    if disc.lo<=0 or b.hi>=0:raise ValueError('uncertified receiver branch')
    other=-b+disc.sqrt()
    return c/other,other


def derivatives(u,h):
    from uhrauslese import sender
    from quelle import SCALE
    from nullreferenz import maxabs
    t,other=root(u,h)
    s=sender(u,0);f_t=2*(t+16+9*u-s-h)
    if f_t.hi>=0 or other.lo-t.hi<SCALE:
        raise ValueError('receiver roots not separated')
    fu=18*(t-u)-2*(t-s)*(u-s)/(u+3)
    fh=-2*(t-h)
    return -fu/f_t,-fh/f_t


def interval_analog(code_u,code_h,step,bias):
    from quelle import box,hull,SCALE
    from nullreferenz import maxabs
    if type(code_u) is not int or type(code_h) is not int or step<=0 or bias<0:
        raise ValueError('invalid precursor measurement')
    centers=[v*step for v in (code_u,code_h)]
    if any(abs(v)>=8 for v in centers):raise ValueError('saturated precursor')
    delta=step/2+bias
    u,h=[hull(c-delta,c+delta) for c in centers]
    du,dh=derivatives(u,h)
    center,other=root(*map(box,centers))
    guard=(maxabs(du)+maxabs(dh))*delta
    return center,center+hull(-guard,guard),guard


def qcode(x,step):
    from quelle import SCALE
    a,b=[floor(F(v,SCALE)/step+F(1,2)) for v in (x.lo,x.hi)]
    if a!=b:raise ValueError('ambiguous digit')
    return a


def extras(fixtures):
    from referenzwechsel import displaced
    _,y,w=fixtures[0]
    for alpha in (F(559727851,10**18),F(-3,10**7),F(2,10**7),F(7,10**7)):
        yield 'hold_'+str(alpha),*displaced(y,w,alpha)


def run(previous,early):
    from quelle import hull,box,SCALE
    from gemischt import ORDER,PAST,COEFF
    from zustand import gradients
    from proben import samples
    from referenzwechsel import displaced
    from nullreferenz import digit,maxabs
    from empfangsbit import CAL
    from uhrauslese import residual
    fixtures=samples(previous,early)[0];_,y,w=fixtures[0]
    prefix=sorted(i for i in y if (i,16) in ORDER)
    assert prefix==[0,1,2,15] and (17,16) not in ORDER and (16,17) not in ORDER
    assert all((j,18) in ORDER and (j,7) in ORDER for j in (15,17))
    lower,upper=[displaced(y,w,a) for a in (-F(1,10**6),F(1,10**6))]
    momenta=[]
    for yy,ww in (lower,upper):
        G,_=gradients(yy,ww)
        momenta.append([G[i] for i in PAST])
        assert all(yy[i].data()==y[i].data() and ww[i].data()==w[i].data() for i in prefix+[16])
        assert all(yy[i].data()==y[i].data() and ww[i].data()==w[i].data() for i in PAST)
        assert (ww[16]*(yy[16]-yy[15])-w[16]*(y[16]-y[15])).contains_zero()
    assert all((b-a).contains_zero() for a,b in zip(*momenta))
    # The constructed shift is the input alpha, so this difference is exact.
    assert (upper[0][18]-lower[0][18]-F(2,10**6)).contains_zero()
    cases=list(fixtures)+list(extras(fixtures));details=[]
    for n,yy,ww in cases:
        u,h,t=yy[15],yy[17],yy[18]
        predicted,alt=root(u,h)
        assert (t-predicted).contains_zero() and residual(u,h,predicted,0).contains_zero()
        assert alt.lo>t.hi+SCALE
        details.append({'name':n,'actual_digit':digit(t),'other_root':alt.data()})
    # A single rectangle containing all original and displaced u,h plus perturbations.
    def cover(i):
        return hull(min(F(yy[i].lo,SCALE) for _,yy,_ in cases)-F(3,10**6),
                    max(F(yy[i].hi,SCALE) for _,yy,_ in cases)+F(3,10**6))
    cu,ch=cover(15),cover(17)
    du,dh=derivatives(cu,ch)
    rows=[]
    for step,bias in product(STEPS,BIASES):
        err=(maxabs(du)+maxabs(dh))*(step/2+bias)
        largest=F(0)
        for _,yy,_ in cases:
            for su,sh in product((-1,1),repeat=2):
                au=qcode(yy[15]+su*bias,step);ah=qcode(yy[17]+sh*bias,step)
                ctr,band,_=interval_analog(au,ah,step,bias)
                assert band.lo<=yy[18].lo<=yy[18].hi<=band.hi
                largest=max(largest,maxabs(ctr-yy[18]))
        rows.append({'step':str(step),'bias':str(bias),'uniform_analog_error':str(err),
                     'meets_old_analog_CAL':err<=CAL,'max_observed_analog_error':str(largest)})
    return {'prefix':prefix,'same_four_momenta':[str(j) for j in PAST],
            'native_null_digits':[digit(lower[0][18]),digit(upper[0][18])],
            'worst_case_prefix_error_at_least':'1/1000000',
            'u_cover':cu.data(),'h_cover':ch.data(),'derivative_u':du.data(),'derivative_h':dh.data(),
            'backgrounds':details,'precision':rows}
