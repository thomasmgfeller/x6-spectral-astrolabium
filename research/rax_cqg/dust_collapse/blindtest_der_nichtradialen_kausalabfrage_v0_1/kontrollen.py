"""Synthetic record generation for closed, flat and open spatial slices. SI-free c=1 units."""
from fractions import Fraction as F
from hashlib import sha256
from random import Random

DT = F(1,1000)
THETA = F(1,9200)
CLOCK = F(2,10**6)
ANGLE = THETA/200
FACTORS = (0,1,4,8)
STRATA = ((7800,8900),(9050,9190),(9210,9350),(9500,10800))

def cases(seed):
    tab=[]
    for sign in (-1,0,1):
        for stratum,(low,high) in enumerate(STRATA):
            for index in range(10):
                key=f'{seed}|{sign}|{stratum}|{index}'.encode()
                rng=Random(sha256(b'physics:'+key).digest())
                tab.append({'id':sha256(b'marker:'+key).hexdigest()[:18],
                            'curvature_sign':sign, 'length':rng.randint(15,40),
                            'radius_milli':rng.randint(low,high), 'h_milli':rng.randint(-800,800),
                            'q_milli':rng.randint(-2000,2000), 'stratum':stratum})
    assert len({r['id'] for r in tab})==120
    return sorted(tab,key=lambda r:r['id'])

def corner(factor,hard):
    s=1 if hard else -1
    return s*factor*CLOCK,DT-s*factor*CLOCK,THETA+s*factor*ANGLE

def sn_interval(k,x):
    """Space form function sn_k(x); series through degree 5 plus absolute tail."""
    assert 0<=x<1 and abs(k)*x*x<1
    centre=x-k*x**3/6+k*k*x**5/120
    rem=2*abs(k)**3*x**7/5040
    return centre-rem,centre+rem

def parameters(row):
    return (F(row['curvature_sign'],row['length']**2),F(row['radius_milli'],1000),
            F(row['h_milli'],1000),F(row['q_milli'],1000))

def relation(row,t0,t1,angle):
    k,r,h,q=parameters(row)
    # 1/a is positive on the entire queried interval, including clock offsets.
    guard=max(abs(t0),abs(t1))
    assert 1-abs(h)*guard-abs(q)*guard**2>0 and t0<t1
    light=t1-t0+h*(t1*t1-t0*t0)/2+q*(t1**3-t0**3)/3
    left=sn_interval(k,light/2)
    right=sn_interval(F(1),angle/2)
    if left[0]>=r*right[1]:return 'JA'
    if left[1]<r*right[0]:return 'NEIN'
    return 'UNBESTIMMT'

def crosscheck(row,t0,t1,angle):
    """Invert the chord via integral bounds; independently integrate time by Simpson."""
    k,r,h,q=parameters(row)
    def speed(t):return 1+h*t+q*t*t
    budget=(t1-t0)*(speed(t0)+4*speed((t0+t1)/2)+speed(t1))/6
    w=angle/2
    amin=r*(w-w**3/6)
    amax=r*w
    eps=abs(k)*amax**2
    assert 0<=eps<F(1,4)
    # Distance/2 = integral from 0 to r*sin(w) of (1-k*s²)^(-1/2) ds.
    dlo,dhi=2*amin*(1-2*eps),2*amax*(1+2*eps)
    if budget>=dhi:return 'JA'
    if budget<dlo:return 'NEIN'
    return 'UNBESTIMMT'

def frames(truth):
    out=[]
    for row in truth:
        values={}
        for f in FACTORS:
            pair=[]
            for hard in (True,False):
                args=corner(f,hard)
                v=relation(row,*args)
                assert v==crosscheck(row,*args) and v!='UNBESTIMMT'
                pair.append(v)
            values[str(f)]=pair
        out.append({'id':row['id'],'antworten':values})
    return out
