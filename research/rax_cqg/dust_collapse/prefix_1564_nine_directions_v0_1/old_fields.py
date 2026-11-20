"""Nonzero fibre check independent of the exterior quadrature, on a positive-mass density atom."""
from fractions import Fraction as Q
from mpmath import iv

def check_one(coeff):
    iv.dps=35
    beta=4/iv.sqrt(6)
    step=iv.sqrt(2/(19*beta))
    t={k:(k-5)*step for k in range(4)}
    t[3]+=iv.mpf(1)/16
    t.update(dict.fromkeys([4,5,6,11,12],0))
    inc=[(i,v) for (i,j),v in coeff.items() if j==13 and v]
    S=sum(coeff.get((13,k),0) for k in range(7,11))
    L=sum((k-5)*coeff.get((13,k),0) for k in range(7,11))
    deriv=Q(5,3)*(Q(3,2)*abs(S)+Q(13,50)*abs(L))/16+Q(5,3)*3*sum(abs(v) for _,v in inc)/8
    for n in (128,512,2048):
        total=iv.mpc(0)
        for i in range(n):
            s=iv.mpf(3)*(2*i+1-n)/(2*n)
            angle=-beta/32*(S*s**2-2*L*step*s)
            C=1+beta/2*sum(v*(s-t[k])**2 for k,v in inc)
            if 0 in C:
                rad=abs(C)/8
                dust=1+iv.mpc(iv.mpf([-1,1])*rad,iv.mpf([-1,1])*rad)
            else:
                dust=(1+iv.exp(-iv.j*C/4)*iv.sin(C/4)/(C/4))/2
            total+=iv.exp(iv.j*angle)*dust
        err=3*deriv/(4*n)
        threshold=err+Q(1,20)
        if abs(total/n)>iv.mpf(threshold.numerator)/threshold.denominator:
            return {'inner_clock_points':n,'modulus_strictly_greater_than':'1/20',
                    'normalized_midpoint_error_at_most':str(err)}
    raise ArithmeticError('Failed to prove nonvanishing with the declared grids')
