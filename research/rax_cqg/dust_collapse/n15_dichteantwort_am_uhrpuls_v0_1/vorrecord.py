"""Integrate positive support leakage for a past record of w11/D alone."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from randquelle import DELTA,H,ETA,RADIUS,INNER,I,S
from modell import dwell
from phase359 import box

SPAN=2*RADIUS
SLOPE=SPAN/2
A=F(1,8)
FMIN=A-SLOPE
FMAX=A+SLOPE

def residual(x,y):
    # Integrate the five unused clocks exactly by Simpson cubature. Each degree <= 2.
    pts=(0,F(1,2),1);weights=(F(1,6),F(2,3),F(1,6))
    total=F(0)
    for indices in product(range(3),repeat=5):
        independent=iter(indices);u=[];w=F(1)
        for k,j in enumerate(INNER):
            if j==6:t=x
            elif j==12:t=y
            else:
                i=next(independent);t=pts[i];w*=weights[i]
            u.append(F(k+1,8)+SPAN*(t-F(1,2)))
        f=dwell(u)
        for j in INNER:
            if j!=11:w*=f[j]
        total+=w
    return total

def add(a,b):
    size=max(len(a),len(b))
    return [x+y for x,y in zip(a+[F(0)]*(size-len(a)),b+[F(0)]*(size-len(b)))]
def mul(a,b):
    z=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return z
def power(a,n):
    z=[1]
    for _ in range(n):z=mul(z,a)
    return z
def integral(poly,a,b):
    return sum(c*(b**(k+1)-a**(k+1))/(k+1) for k,c in enumerate(poly))

@lru_cache(None)
def weights_on_difference():
    values={(x,y):residual(F(x),F(y)) for x,y in product((0,1),repeat=2)}
    c=values[0,0];a=values[1,0]-c;b=values[0,1]-c;k=values[1,1]-a-b-c
    assert c+(a+b)/2+k/4==residual(F(1,2),F(1,2))
    # d=y-x. At fixed d, Q(x,x+d)=c+bd+(a+b+kd)x+kx².
    pieces=[]
    for lo,hi in (([0,-1],[1]),([0],[1,-1])):
        p=[F(0)]
        for n,coeff in enumerate(([c,b],[a+b,k],[k]),start=1):
            dx=add(power(hi,n),[-v for v in power(lo,n)])
            p=add(p,mul([v/n for v in coeff],dx))
        pieces.append(tuple(p))
    return pieces

def moments(intercept,slope,positive_part):
    total=F(0)
    for (l,u),p in zip(((-1,0),(0,1)),weights_on_difference()):
        a,b=F(l),F(u)
        if positive_part:
            root=-intercept/slope
            if slope>0:a=max(a,root)
            else:b=min(b,root)
        if a<b:total+=integral(mul(p,[intercept,slope]),a,b)
    return total

def at_q(q,sign):
    centre=A-sign*q/2
    if sign==1:
        # [B-(1-eta)f]_+ - [B-(1+eta)f]_+
        B=(1-ETA)*FMIN
        terms=[moments(B-k*centre,-k*SLOPE,True) for k in (1-ETA,1+ETA)]
    else:
        # [(1+eta)f-B]_+ - [(1-eta)f-B]_+
        B=(1+ETA)*FMAX
        terms=[moments(k*centre-B,k*SLOPE,True) for k in (1+ETA,1-ETA)]
    return terms[0],terms[1],moments(centre,SLOPE,False)

def run(n=2048):
    # Each positive-part term increases with q; the denominator is affine in q.
    result={}
    pieces=weights_on_difference()
    assert all(isinstance(v,F) for p in pieces for v in p)
    for sign,arm in ((1,'plus'),(-1,'minus')):
        num=I.of(0);den=I.of(0)
        for mid in (F(-1,16),F(1,16)):
            for k in range(n):
                a=mid-F(1,32)+F(k,16*n)
                D=4*DELTA-box(a,a+F(1,16*n))
                q=DELTA*H/(D*D.sqrt())
                l1,l2,ld=at_q(F(q.lo,S),sign);u1,u2,ud=at_q(F(q.hi,S),sign)
                assert l1<=u1 and l2<=u2
                weight=D**14
                num+=weight*box((l1-u2)/(2*ETA),(u1-l2)/(2*ETA))
                den+=weight*box(min(ld,ud),max(ld,ud))
        result[arm]=(num/den).rounded(10)
    result['ohne_mitbewegung']=[0,0]
    result['zellen_pro_offsetfenster']=n
    result['differenzgewichte']=[[str(v) for v in p] for p in pieces]
    return result

if __name__=='__main__':
    import json
    print(json.dumps(run(),sort_keys=True,indent=2))
