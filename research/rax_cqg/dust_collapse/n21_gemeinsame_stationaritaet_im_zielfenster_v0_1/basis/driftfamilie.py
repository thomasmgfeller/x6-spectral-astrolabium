"""Relative receive-clock shifts and interval certificates over the drift family."""
from fractions import Fraction as F

LIMIT = F(1,10**6)
LABELS = (-LIMIT,F(0),LIMIT)


def shift(y,w,j,velocity,state):
    """Evaluate the small root directly, retaining the common unloaded coordinate."""
    from quelle import box
    from empfangsbit import K0
    from speichermodell import square
    from gemischt import COEFF
    k=K0
    mu=box(-k)
    u,s,h,t=(y[i] for i in (15,16,17,18))
    load=k*sum((square(v) for v in velocity),box(0))
    denom=w[18]*(t-h)+k*velocity[1]
    rr=load*square(1+mu)/square(denom)
    # The sender clock shift and coefficients of a*x²+2*b*x+c=0.
    d=box(j)/(-2*(u+3))+state['extra']
    a=1+2*mu+rr
    b=sum((c*(t-y[i]) for (i,n),c in COEFF.items() if n==18 and c),box(0))-d+mu*(t-s-d)+(mu+rr)*(t-h)
    c=d*(d-2*(t-s))+mu*square(t-s-d)+(mu+rr)*square(t-h)
    disc=square(b)-a*c
    assert denom.lo>0 and a.lo>0 and b.hi<0 and disc.lo>0
    x=c/(-b+disc.sqrt())
    assert (a*square(x)+2*b*x+c).contains_zero()
    assert (t+x-state['y'][18]).contains_zero()
    return x


def cell(y,w,lo,hi):
    from empfangsbit import K0,STEP,V,R,bounds
    from quelle import hull,box
    from referenzwechsel import displaced
    from staubgeraet import solve,verify
    from kalibriervergleich import margins
    from nullreferenz import maxabs
    yy,ww=displaced(y,w,hull(6*STEP+lo,6*STEP+hi))
    v=(hull(-112*V,112*V),)*3
    q=(hull(-1,1),)*3
    shifts,transfer={},{}
    for j in LABELS:
        state=solve(yy,ww,j,v,K0,box(-K0),'positive_bridge')
        history,A=verify(state,j,v,K0,box(-K0),'positive_bridge',q)
        assert all(maxabs(a)<8-4*R for a in (state['y'][18],state['y'][7],history[2][7]))
        shifts[j]=shift(yy,ww,j,v,state)
        transfer[j]=A[2][7]
    rows={}
    for j in LABELS:
        # Null and target may have different momenta at the same native background.
        dt=shifts[j]-shifts[0]
        early=bounds(dt,2*R)
        late=bounds(dt-transfer[j]*v[2],5*R)
        digit,budget=margins(early,late,j)
        rows[str(j)]={'receiver':early,'signed':late,'digit_budget':digit,'plateau_budget':budget}
    return {'delta':[str(lo),str(hi)],'load_analog':shifts[0].data(),
            'load_digit':bounds(shifts[0],STEP),'sources':rows}


def certify(y,w):
    leaves=[]
    def collect(lo,hi,depth):
        try:
            item=cell(y,w,lo,hi)
            assert min(s['plateau_budget'] for s in item['sources'].values())>=11
            assert -31<=item['load_digit'][0]<=item['load_digit'][1]<=-30
        except (AssertionError,ValueError,ZeroDivisionError):
            if depth>=12:
                raise
            mid=(lo+hi)/2
            collect(lo,mid,depth+1)
            collect(mid,hi,depth+1)
        else:
            leaves.append(item)
    collect(-LIMIT,LIMIT,0)
    edges=[tuple(map(F,c['delta'])) for c in leaves]
    assert edges[0][0]==-LIMIT and edges[-1][1]==LIMIT
    assert all(a<b for a,b in edges) and all(a[1]==b[0] for a,b in zip(edges,edges[1:]))
    load=[min(F(c['load_analog'][0]) for c in leaves),max(F(c['load_analog'][1]) for c in leaves)]
    return {'leaves':leaves,'load_analog':list(map(str,load)),
            'minimum_budget':min(s['plateau_budget'] for c in leaves for s in c['sources'].values())}
