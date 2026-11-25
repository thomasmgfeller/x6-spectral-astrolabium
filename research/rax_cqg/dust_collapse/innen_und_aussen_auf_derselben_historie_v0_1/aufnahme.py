"""Forward acquisition at ordinary clock sources; the detector receives only four arms and an echo."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import dynamik as dyn
from auslese import read,TICK_SCALE

ARMS=tuple(product((1,-1),repeat=2))
PHYSICAL_SCALE=166*64
TIMES=(1200,1260,1320,1380,1440)


def arm_tables():
    # Two successive clocks on one station. Collect every affected incident edge exactly once.
    nodes=((-1,0),(0,0))
    edges=set()
    for t,j in nodes:
        for delta,k,b in dyn.STENCIL:
            edges.add((t,j,t+delta,j+k,b))
            edges.add((t-delta,j-k,t,j,b))
    tables=[]
    for a,b in ARMS:
        shift=dict(zip(nodes,(a,b)))
        terms=Counter()
        for t,i,u,j,c in edges:
            k=shift.get((u,j),0)-shift.get((t,i),0)
            terms[u,j]-=c*(16*(u-t)*k+k*k)
        tables.append(sorted((t,j,c) for (t,j),c in terms.items() if c))
    return tables


def quantize(lo,hi):
    center=((lo+hi)*TICK_SCALE+dyn.UNIT)//(2*dyn.UNIT)
    assert (center-1)*dyn.UNIT<=lo*TICK_SCALE<=hi*TICK_SCALE<=(center+1)*dyn.UNIT
    return center


def snapshot(at,L,t,tables):
    records=[]
    for j in range(4,L-3):
        arms=[]
        for table in tables:
            lo=hi=0
            for delta,k,c in table:
                a,b=at(t+delta,j+k)
                if c<0:a,b=b,a
                lo+=c*a;hi+=c*b
            arms.append(quantize(lo,hi))
        records.append([t-12*j,t+12*j,*arms])
    # Delivery order grants no sorting or membership information to the instrument.
    return records[1::2]+records[::2]


def bands(f):
    L=96*f
    i=L//16
    o=86 if f==1 else 9*L//10
    return list(range(i-2,i+3)),list(range(o-2,o+3))


def ray(j,t,T):
    before=lambda a: t>a and t-a>=12*j
    after=lambda a: a>t and a-t>=12*j
    e=t-12*j;r=t+12*j
    return 0<=e<r<=T and before(e) and not before(e+1) and after(r) and not after(r-1)


def run(r,q):
    tables=arm_tables()
    trail=[]
    for factor in (1,2,4,8,16,32,64):
        L=96*factor;inner,outer=bands(factor)
        ratio=r**(outer[0]-inner[0])
        trail.append({'length':L,'ratio_floor_1e9':ratio.numerator*10**9//ratio.denominator})
        if ratio<F(1,100):break
    assert ratio<F(1,100)
    summaries=[];raw={}
    def exposure(kind,f,t,snapshot_name):
        length=96*f;inner,outer=bands(f)
        assert all(ray(j,t,2688*f) for j in range(4,length-3))
        at=dyn.weight_fn(kind,length,r,q)
        records=snapshot(at,length,t,tables)
        key=f'{snapshot_name}_{length}_{t}'
        raw[key]={'length':length,'time':t,'inner':inner,'outer':outer,'echo_arms':records}
        result=read(records,length,t,inner,outer)
        for role,stations in [('inner_mean',inner),('outer_mean',outer)]:
            if role not in result:continue
            # Independent count-free reference for the evaluation only.
            expected=[sum(at(t,j)[k] for j in stations) for k in (0,1)]
            low,high=map(F,result[role])
            assert low<=F(expected[0],len(stations)*dyn.UNIT)<=F(expected[1],len(stations)*dyn.UNIT)<=high
        summaries.append({'acquisition':key,**result})
        return result,records
    for f in (1,factor):
        for relative in TIMES:
            result,_=exposure('profile',f,relative*f,'profile')
            expected=r**(bands(f)[1][0]-bands(f)[0][0])
            low,high=map(F,result['outer_over_inner'])
            assert low<=expected<=high
            assert result['state']==('DEPLETED' if f==factor else 'NOT_DEPLETED')
    for kind,status in [('uniform','NOT_DEPLETED'),('vacuum','NO_POSITIVE_REFERENCE'),
                        ('step','DEPLETED'),('reverse','NOT_DEPLETED')]:
        result,records=exposure(kind,1,1320,kind)
        assert result['state']==status
        if kind=='step':assert result['threshold_station_bracket']==[32,33]
    i,o=bands(1)
    assert read(records[:-1],96,1320,i,o)['state']=='MISSING_EXPOSURE'
    assert read([*records,records[0]],96,1320,i,o)['state']=='DUPLICATE'
    return {'geometric_extension':trail,'snapshots':summaries,'missing_exposure':'MISSING_EXPOSURE',
            'duplicate':'DUPLICATE','normalized_action_error_bound_per_arm':str(F(1,PHYSICAL_SCALE*TICK_SCALE))},raw
