"""A one-bit causal message generated from the receiver clock alone."""
from fractions import Fraction as F
from itertools import product
from math import ceil,floor

R=F(1,10**12)
STEP=2*R
K0=F(1,10**11)
V=F(1,10**14)
CAL=F(1,10**11)
THRESHOLD=125
RADII=(0,32,48,56,58,59,60,64,96,112,116,118,120,128)


def valid(code):
    return type(code) is int and -8<=code*STEP<8


def receiver_bit(clock,baseline):
    if not valid(clock) or not valid(baseline):return None
    return int(abs(clock-baseline)>THRESHOLD)


def late_code(clock,end_t,start_t,baseline):
    if not all(map(valid,(clock,end_t,start_t,baseline))):return None
    return clock-end_t+start_t-baseline


def classify(bit,late):
    if type(bit) is not int or bit not in (0,1) or type(late) is not int:return None
    if bit==0:return F(0)
    if late==0:return None
    return F(1 if late>0 else -1,10**6)


def bounds(v,uncertainty):
    from quelle import SCALE
    return [ceil((F(v.lo,SCALE)-uncertainty)/STEP),floor((F(v.hi,SCALE)+uncertainty)/STEP)]


def proof_rows(previous,early):
    from quelle import box,hull
    from proben import samples
    from staubgeraet import solve,verify
    from uhrauslese import LABELS
    from wege import ROUTES
    from nullreferenz import maxabs
    fixtures,_=samples(previous,early)
    results=[]
    for m in RADII:
        families=[]
        for (name,y,w),route,k,J in product(fixtures,ROUTES,(F(1),K0),LABELS):
            limit=m*K0*V/k
            vel=(hull(-limit,limit),)*3
            mismatch=hull(-K0,K0) if k==1 else box(-k)
            st=solve(y,w,J,vel,k,mismatch,route)
            hist,A=verify(st,J,vel,k,mismatch,route,(hull(-1,1),)*3)
            assert all(maxabs(z)<8-4*STEP for z in [y[18],st['y'][18],st['y'][7],hist[2][7]])
            dt=st['y'][18]-y[18]
            lo,hi=bounds(dt,CAL+2*R)
            # In analog coordinates, the late clock minus the third displacement equals t-A*v.
            l,h=bounds(dt-A[2][7]*vel[2],CAL+R+4*R)
            bitok=(-THRESHOLD<=lo<=hi<=THRESHOLD) if J==0 else (lo>THRESHOLD if J>0 else hi< -THRESHOLD)
            signok=(l>0 if J>0 else h<0) if J else True
            direct=(l>THRESHOLD if J>0 else h< -THRESHOLD) if J else -THRESHOLD<=l<=h<=THRESHOLD
            both=bitok and signok
            families.append(dict(background=name,route=route,k=str(k),J=str(J),receiver=[lo,hi],
                                 late=[l,h],bit_success=both,late_alone_fixed_rule=direct))
        # With known background and route, nonoverlapping scalar ranges suffice even without the bit.
        separations=[]
        for i in range(0,len(families),3):
            neg,zero,pos=families[i:i+3]
            assert F(neg['J'])<0==F(zero['J'])<F(pos['J'])
            separations.append(min(zero['late'][0]-neg['late'][1],pos['late'][0]-zero['late'][1]))
        results.append(dict(m=m,joint_one_bit=sum(v['bit_success'] for v in families),
                            joint_no_bit_fixed=sum(v['late_alone_fixed_rule'] for v in families),
                            three_sources_disjoint_at_7=sum(s>0 for s in separations),
                            minimum_late_separation_codes=min(separations),
                            minimum_nonzero_late_signed_code=min(r['late'][0] if F(r['J'])>0 else -r['late'][1] for r in families if F(r['J'])),
                            receiver_null_abs_max=max(max(map(abs,r['receiver'])) for r in families if F(r['J'])==0),
                            receiver_pulse_abs_min=min(r['receiver'][0] if F(r['J'])>0 else -r['receiver'][1] for r in families if F(r['J'])),
                            families=families if m in (64,128) else []))
    return results
