"""Rational worst-case one-coordinate Gauss errors after freezing all remaining real variables."""
from fractions import Fraction as Q
from itertools import product
from math import ceil,log

INNER=(4,5,6,11,12,13)
PAST=(0,1,2,3)
FUTURE=(7,8,9,10)
BETA_HI=Q(5,3)
HALF=Q(1,2)
TOL=Q(1,32768)

def smallest_gauss(a,b):
    # z=(w+1/w)/2 on |w|=r. Chebyshev tail starts at polynomial degree 2n.
    options=[]
    for r in [Q(k,20) for k in range(22,55,2)]:
        M=a*(r*r-r**-2)/4+b*(r-1/r)/2
        peak=2**ceil(3*M/2)
        pref=4*peak/(1-1/r)
        n=max(1,ceil(log(float(pref/TOL))/(2*log(float(r)))))
        while pref*r**(-2*n)>TOL:n+=1
        options.append((n,pref*r**(-2*n),r))
    n,e,r=min(options)
    return {'n':n,'ellipse_r':str(r),'quadratic_bound':str(a),'linear_bound':str(b),'error_upper':str(e)}

def bounds(coeff):
    # All clock phases are polynomials before integration over the compact densities.
    steps=(Q(1,4),Q(13,50))
    assert 19**2*(Q(4)**2/6)*steps[0]**4<4<19**2*(Q(4)**2/6)*steps[1]**4
    assert BETA_HI**2 > Q(16,6)
    result={}
    for node in (*INNER,3):
        d=Q(1,32) if node==3 else Q(3,2)
        a=b=0
        terms=[(j if i==node else i,j,w) for (i,j),w in coeff.items() if node in (i,j) and w]
        # Group contributions before absolute values. For fixed densities the linear
        # coefficient is affine in all other clocks, the collar spacing and lobe shift.
        for bits in product((0,1),repeat=7):
            rho={**dict(zip(INNER,bits)),**dict.fromkeys(PAST,bits[-1]*Q(9,32)),**dict.fromkeys(FUTURE,Q(1,8))}
            weights={i:rho[j]*w for i,j,w in terms}
            net=sum(weights.values())
            a=max(a,BETA_HI/4*d*d*abs(net))
            old_radius=sum(abs(weights.get(k,0))*Q(3,2) for k in INNER if k!=node)
            # Fixed collar centres are (k-5)*step. The additional offset of the T3
            # centre is at most 1/16; if T3 is real and integrated it is at most 3/32.
            collar_net=sum(weights.get(k,0)*(k-5) for k in PAST+FUTURE)
            center_factor=(-2*net if node==3 else 0)-collar_net
            offset=abs(net)*Q(1,16) if node==3 else abs(weights.get(3,0))*Q(3,32)
            b=max(b,BETA_HI/2*d*(abs(center_factor)*steps[1]+old_radius+offset))
        result[str(node)]=smallest_gauss(a,b)
    broad=next((j for j in INNER if sum(bool(coeff.get((i,j))) for i in INNER)>=4),None)
    if broad is not None:
        # Before the continuous part of its density is integrated the phase is linear in z.
        pos=neg=Q(0)
        for (i,j),w in coeff.items():
            if j!=broad or not w:continue
            rad=Q(3,2) if i in INNER else abs(i-5)*steps[1]+(Q(3,32) if i==3 else 0)
            limit=(Q(3,2)+rad)**2
            if w>0:pos+=w*limit
            else:neg+=w*limit
        C=max(abs(1+BETA_HI/2*neg),1+BETA_HI/2*pos,1)
        result['density']=smallest_gauss(0,C/4)
    return result
