"""Read the unsigned activity of a whole event star, without cancellation between edges."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import aufnahme as aq
import dynamik as dy
from auslese import TICK_SCALE

@lru_cache(maxsize=None)
def arm_tables(dt,k,left,right):
    # Origin is the emitting station. left/right give the accessible guard extent.
    nodes=((0,0),(dt,k))
    edges=set()
    for t,x in nodes:
        for d,s,b in dy.STENCIL:
            if -left<=x+s<=right:edges.add((t,x,t+d,x+s,b))
            if -left<=x-s<=right:edges.add((t-d,x-s,t,x,b))
    tables=[]
    for a,b in aq.ARMS:
        pulse=dict(zip(nodes,(a,b)))
        weights={}
        for t,x,u,y,c in edges:
            change=pulse.get((u,y),0)-pulse.get((t,x),0)
            if change:
                key=(u,y)
                weights[key]=weights.get(key,0)-c*(16*(u-t)*change+change**2)
        tables.append([(u,y,c) for (u,y),c in weights.items() if c])
    return tables


def edge_record(w,L,t,x,d,k):
    result=[]
    for table in arm_tables(d,k,min(x,8),min(L-x,8)):
        lo=hi=0
        for u,y,c in table:
            a,b=w(t+u,x+y)
            if c<0:a,b=b,a
            lo+=c*a;hi+=c*b
        result.append(aq.quantize(lo,hi))
    return [t,x,t+d,x+k,*result]


def decode(records,t,j):
    needed={(t,j,t+d,j+k) for d,k,b in dy.STENCIL}|{(t-d,j-k,t,j) for d,k,b in dy.STENCIL}
    keys=[tuple(rec[:4]) for rec in records]
    if len(keys)!=len(needed) or set(keys)!=needed:return 'MISSING_EXPOSURE'
    low=high=0
    for t1,_,t2,_,a,b,c,d in records:
        signal=a-b-c+d
        low+=(t2-t1)*max(0,abs(signal)-4)
        high+=(t2-t1)*(abs(signal)+4)
    return F(low,8*TICK_SCALE),F(high,8*TICK_SCALE)


def acquire_star(w,L,t,j):
    records=[]
    for dt,k,b in dy.STENCIL:
        records.extend((edge_record(w,L,t,j,dt,k),edge_record(w,L,t-dt,j-k,dt,k)))
    estimate=decode(records,t,j)
    # Independent positive-sum reference from edge currents and density enclosures.
    total=[0,0]
    for dt,k,b in dy.STENCIL:
        for idx in (0,1):
            total[idx]+=abs(b)*dt*(w(t,j)[idx]+w(t+dt,j+k)[idx])
    assert estimate[0]<=F(total[0],dy.UNIT)<=F(total[1],dy.UNIT)<=estimate[1]
    return records,estimate


def run(r,q,factor):
    raw={};results=[]
    for f in (1,factor):
        length=96*f;inner,outer=aq.bands(f)
        w=dy.weight_fn('profile',length,r,q)
        for time in aq.TIMES:
            t=time*f; stars={};estimates={}
            for j in inner+outer:
                records,e=acquire_star(w,length,t,j)
                stars[str(j)]=records;estimates[j]=e
            def avg(which,side):
                return sum(estimates[j][side] for j in which)/len(which)
            lower=avg(outer,0)/avg(inner,1);upper=avg(outer,1)/avg(inner,0)
            assert lower<=r**(outer[0]-inner[0])<=upper
            assert (upper<F(1,100))==(f==factor)
            results.append({'length':length,'ticks':t,'lower':str(lower),'upper':str(upper),
                     'inner_activity_over_h':[str(avg(inner,0)),str(avg(inner,1))],
                     'outer_activity_over_h':[str(avg(outer,0)),str(avg(outer,1))]})
            raw[f'{length}_{t}']=stars
    step=dy.weight_fn('step',96,r,q)
    profile={}
    for j in range(32,38):
        rec,interval=acquire_star(step,96,1320,j)
        raw.setdefault('sharp_96_1320',{})[str(j)]=rec
        profile[str(j)]=list(map(str,interval))
        assert (interval[0]>0)==(j<37)
    assert decode(rec[:-1],1320,37)=='MISSING_EXPOSURE'
    return {'smooth':results,'sharp_activity_over_h':profile,'records_per_event':len(rec)},raw
