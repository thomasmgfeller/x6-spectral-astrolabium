"""Rationale Intervallprüfung der Bessel-Schranke im Zweig ohne inneres Ereignis."""
from fractions import Fraction as F
from math import comb, factorial
from schranken import B2, PI, decimal_bounds, root, square

SCALE=10**32


def rounded(lo,hi):
    a,b=F(lo)*SCALE,F(hi)*SCALE
    return F(a.numerator//a.denominator,SCALE), F(-((-b.numerator)//b.denominator),SCALE)


class I:
    """Geschlossenes reelles Intervall, nach jeder Operation nach aussen gerundet."""
    def __init__(self,a,b=None):
        self.lo,self.hi=rounded(a,a if b is None else b)
    def __add__(self,other):
        return I(self.lo+other.lo,self.hi+other.hi)
    def __neg__(self):
        return I(-self.hi,-self.lo)
    def __sub__(self,other):
        return self+-other
    def __mul__(self,other):
        z=[a*b for a in (self.lo,self.hi) for b in (other.lo,other.hi)]
        return I(min(z),max(z))
    def reciprocal(self):
        if self.lo<=0<=self.hi:
            raise ValueError('Division durch ein Nullintervall')
        return I(1/self.hi,1/self.lo)
    def sqrt(self):
        return I(root(self.lo)[0],root(self.hi)[1])
    def sq(self):
        return I(*square((self.lo,self.hi)))
    def out(self):
        return decimal_bounds((self.lo,self.hi),places=12)


class C:
    def __init__(self,r,i=0):
        self.r=r if isinstance(r,I) else I(r)
        self.i=i if isinstance(i,I) else I(i)
    def __add__(self,o):
        return C(self.r+o.r,self.i+o.i)
    def __neg__(self):
        return C(-self.r,-self.i)
    def __sub__(self,o):
        return self+-o
    def __mul__(self,o):
        return C(self.r*o.r-self.i*o.i,self.i*o.r+self.r*o.i)
    def conj(self):
        return C(self.r,-self.i)
    def norm(self):
        return self.r.sq()+self.i.sq()
    def __truediv__(self,o):
        value=self*o.conj()
        inv=o.norm().reciprocal()
        return C(value.r*inv,value.i*inv)
    def sqrt(self):
        u=((self.norm().sqrt()+self.r)*I(F(1,2))).sqrt()
        return C(u,self.i*(I(2)*u).reciprocal())


def phase(n):
    a=sum(F((-1)**j*n**(2*j),factorial(2*j)) for j in range(25))
    b=sum(F((-1)**j*n**(2*j+1),factorial(2*j+1)) for j in range(24))
    err=F(n**49,factorial(49))
    return C(I(a-err,a+err),I(b-err,b+err))


def orbit_data():
    x=C(0,I(*root(B2)))
    one,two=C(1),C(2)
    r=one+x
    path_poly=x*x+C(4)*x+two
    detroots=[r,r.sqrt()*(path_poly/two).sqrt(),r*(one+two*x).sqrt()]
    za=[one/r,-((x+two)*(x*x-x-one))/(r*path_poly),(one-x)/r]
    zs=[one/r,(x+two)/path_poly,one/(one+two*x)]
    weights=(F(4,33),F(20,33),F(9,33))
    amp=[C(I(*PI)*I(w/2))*phase(f)/v for w,f,v in zip(weights,(2,1,0),detroots)]
    return amp,za,zs


def central_sum(k):
    return F((2*k+1)*comb(2*k,k),4**k)


def certified_bessel():
    amp,za,zs=orbit_data()
    one=C(1)
    coeff0=sum(amp,C(0))
    def excited(z):
        return sum((p*q for p,q in zip(amp,z)),C(0))/C(I(2).sqrt())
    w0=coeff0.norm()
    w3=w0+excited(za).norm()+excited(zs).norm()
    if not 0<w0.lo<=w3.hi<1: raise ValueError('Normbudget')
    # z_15=(1-i*b)/(1+i*b) has exact modulus one. For every other pair |z_i*z_j|<5/6.
    for z in za[:2]:
        if z.norm().hi>=F(25,36): raise ValueError('geometrischer Rest')
    if sum(a.norm().sqrt().hi for a in amp)>=1: raise ValueError('Vorfaktor des Restes')
    fixed=C(0)
    for i,v in enumerate(amp):
        for j,w in enumerate(amp):
            if i==j==2: continue
            fixed=fixed+v.conj()*w/(one-za[i].conj()*za[j]).sqrt()
    if not fixed.i.lo<=0<=fixed.i.hi: raise ValueError('Hermitizität')
    result={}
    for k in (2236,2237):
        # c_n<=1, sum |a_i*a_j|<1; the finite-tail error is <=6*(5/6)^(k+1).
        err=6*F(5,6)**(k+1)
        interval=amp[2].norm()*I(central_sum(k))+fixed.r+I(-err,err)
        result[str(k)]=interval.out()
        if k==2236 and interval.hi>=1 or k==2237 and interval.lo<=1:
            raise ValueError('Schwelle verfehlt')
    return dict(zero_packet_weight_00=w0.out(),zero_packet_weight_00_20_02=w3.out(),
                axial_partial_sums=result,first_excess_k=2237,first_excess_number_of_packets=2238,
                maximum_axial_Hermite_index=4474)
