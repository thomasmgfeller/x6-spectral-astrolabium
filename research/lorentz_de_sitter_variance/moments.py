"""Exact shared-anchor moments and a uniform cloud-variance certificate."""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb, factorial
from common import reference

DEGREE=16
CELLS=64
add, mul, scale, power=reference.add,reference.mul,reference.scale,reference.power

@lru_cache(None)
def rest_moment(a,b):
    # E[t^(2a) x_1^(2b)] in the uniform unit-duration Minkowski diamond.
    return Q(192*factorial(2*a)*factorial(2*b+3),
             (2*b+1)*(2*b+3)*2**(2*a+2*b+4)*factorial(2*a+2*b+4))

@lru_cache(None)
def radial_moment(a,b):
    # Polynomial variables are t and s=r^2, including the normalized r^2 measure.
    if a%2:return Q(0)
    return Q(192*factorial(a)*factorial(2*b+3),
             (2*b+3)*2**(a+2*b+4)*factorial(a+2*b+4))

@lru_cache(None)
def profile_moment(k):
    # Future interval x -> top; divide its unnormalized kth time moment by V0.
    delta={(0,0):Q(1,2),(1,0):Q(-1)}
    center={(0,0):Q(1,4),(1,0):Q(1,2)}
    duration4=power(add(power(delta,2),{(0,1):Q(-1)}),2)
    terms=[]
    for a in range(k//2+1):
        for b in range((k-2*a)//2+1):
            c=k-2*a-2*b
            coefficient=Q(factorial(k),factorial(c)*factorial(2*a)*factorial(2*b))*rest_moment(a,b)
            poly=mul(power(center,c),power(delta,2*a))
            poly={(i,j+b):value*coefficient for (i,j),value in poly.items()}
            terms.append(poly)
    future=mul(duration4,add(*terms))
    past={(i,j):value*(-1)**(k+i) for (i,j),value in future.items()}
    return add(future,past)

@lru_cache(None)
def coefficients():
    profiles=[scale(profile_moment(k),Q(comb(k+3,3))) for k in range(DEGREE+1)]
    squares=[]
    for k in range(DEGREE+1):
        terms=[]
        for i in range(k//2+1):
            terms.append(scale(mul(profiles[i],profiles[k-i]),Q(1 if i==k-i else 2)))
        squares.append(add(*terms))
    out=[]
    for k in range(DEGREE+1):
        out.append(sum((Q(comb(ell+3,3))*value*radial_moment(a+ell,b)
                        for ell in range(k+1) for (a,b),value in squares[k-ell].items()),Q(0)))
    assert all(out[k]==0 for k in range(1,DEGREE+1,2))
    return tuple(out)

def numerator_tail(h):
    # Reflection removes odd orders. Coefficient absolute values <= w0*C(k+11,11)/2^k.
    x=h/2; k=DEGREE+2
    first=coefficients()[0]*comb(k+11,11)*x**k
    ratio=x*x*Q((k+13)*(k+12),(k+2)*(k+1))
    assert 0<=ratio<1
    return first/(1-ratio)

def volume_bounds(h):
    z=h*h/4; poly=reference.coefficients()[1]
    lo=reference.evaluate(poly,z)
    return lo,lo+reference.tails(z)[1]

def wedge_bounds(h):
    if not isinstance(h,Q) or not 0<=h<=Q(1,2):raise ValueError('h in [0,1/2] required')
    center=reference.evaluate(coefficients(),h); error=numerator_tail(h)
    zl,zu=volume_bounds(h)
    return max(Q(0),(center-error)/zu**3),min(Q(1),(center+error)/zl**3)

@lru_cache(None)
def certificate(n=128):
    if type(n) is not int or n<2:raise ValueError('integer n>=2 required')
    reference.certificate(); coeffs=coefficients(); rows=[]
    for i in range(CELLS):
        left,right=Q(i,2*CELLS),Q(i+1,2*CELLS)
        # Outward interval bound for the numerator polynomial over the whole cell.
        upper=sum((c*(right if c>=0 else left)**k for k,c in enumerate(coeffs)),Q(0))+numerator_tail(right)
        wupper=upper/volume_bounds(left)[0]**3
        pl=reference.probability(left)[0];pu=reference.probability(right)[1]
        variance=(2*pu+4*(n-2)*wupper-(4*n-6)*pl*pl)/(n*(n-1))
        rows.append(dict(h=[str(left),str(right)],wedge_upper=str(wupper),variance_upper=str(variance)))
    upper=max(Q(row['variance_upper']) for row in rows)
    # Enlarge to an exact decimal for compact, stable published decisions.
    denominator=10**12; upper=Q(-((-upper.numerator*denominator)//upper.denominator),denominator)
    assert 0<upper<Q(1,4)
    return dict(n=n,cells=CELLS,degree=DEGREE,coefficients=[str(x) for x in coeffs],
                flat_wedge=str(coeffs[0]),uniform_variance_upper=str(upper),rows=rows,
                statement='Uniform across h in [0,1/2], known uniform physical-volume model')
