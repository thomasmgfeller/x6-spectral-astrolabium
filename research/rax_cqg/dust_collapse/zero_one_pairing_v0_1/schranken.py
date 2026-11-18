"""Rationale Hüllen für die integrierten Uhramplituden und die Normquotienten."""
from fractions import Fraction as F
from functools import lru_cache
from math import comb, factorial, isqrt

B2 = F(8, 3)
DEGREE = 28
UNIT = 10**33


def root(x):
    x = F(x)
    k = isqrt(x.numerator*UNIT**2 // x.denominator)
    return F(k, UNIT), F(k+1, UNIT)


def times(x, y):
    values = [a*b for a in x for b in y]
    return min(values), max(values)


def plus(x, y):
    return x[0]+y[0], x[1]+y[1]


def scale(c, x):
    return times((c,c), x)


def square(x):
    return (0 if x[0]<=0<=x[1] else min(t*t for t in x), max(t*t for t in x))


def atan_inv(n):
    a = sum(F((-1)**j, (2*j+1)*n**(2*j+1)) for j in range(34))
    return a, a+F(1,69*n**69)


PI = plus(scale(16,atan_inv(5)),scale(-4,atan_inv(239)))


@lru_cache(maxsize=None)
def poly(j):
    # Integral_0^1 (y-u)^(2j) dy = poly(j)(u)/(2j+1).
    return tuple((-1)**k*comb(2*j+1,k) for k in range(2*j+1))


@lru_cache(maxsize=None)
def joint_moment(a,b,d):
    p,q=poly(a),poly(b)
    coeff = [0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):
            coeff[i+j] += x*y
    return sum(F(c,k+1)*d**k for k,c in enumerate(coeff))/((2*a+1)*(2*b+1))


@lru_cache(maxsize=None)
def dust_mean(p,d):
    # d=0 denotes the right-endpoint limit of the time average at the origin.
    moments = []
    for j in range(DEGREE+1):
        if p==1:
            moments.append(joint_moment(j,0,d))
        else:
            moments.append(sum(comb(j,a)*joint_moment(a,j-a,d) for a in range(j+1)))
    components = [[F(1,2),F(0)],[F(0),F(0)]]
    for m in range(DEGREE+1):
        sign = (1,-1,-1,1)[m%4]
        pref = F(sign, 2*factorial(m)*(m+1))
        for j in range(m+1):
            components[m%2][j%2] += pref*comb(m,j)*F(1,2)**(m-j)*B2**(j//2)*moments[j]
    err = F(4**(DEGREE+1), 2*factorial(DEGREE+1)*(DEGREE+2))
    return tuple(plus(plus((a,a),scale(b,root(B2))),(-err,err)) for a,b in components)


def norm_ratio_over_d2(d, t, full_graph_weight):
    avg = [plus(square(r),square(i)) for r,i in (dust_mean(1,d),dust_mean(2,d))]
    oblique = root(F(1370,1)/(841*t*t+529))
    axial1 = scale(4,root(F(9,12871)))
    group2 = plus(root(F(9,1423450)),scale(2,times(oblique,root(F(9,69185)))))
    common = scale(F(2)/(33*full_graph_weight)**2,times(PI,root(1+B2)))
    return times(common,plus(times(axial1,avg[0]),times(group2,avg[1])))


def decimal_bounds(iv, places=13):
    unit=10**places
    # Convert the integer floor and ceiling independently; formatting uses no floats.
    a=iv[0]*unit
    b=iv[1]*unit
    values=(a.numerator//a.denominator, -( (-b.numerator)//b.denominator))
    return [('-' if n<0 else '')+str(abs(n)//unit)+'.'+str(abs(n)%unit).zfill(places) for n in values]
