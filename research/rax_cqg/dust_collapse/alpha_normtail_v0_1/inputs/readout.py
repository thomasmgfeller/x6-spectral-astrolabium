"""Exact Gaussian-rational audits of explicitly chosen boundary instruments."""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
import intervals as v


def require(ok,message):
    if not ok:raise RuntimeError(message)


@dataclass(frozen=True)
class C:
    re:F=F(0)
    im:F=F(0)
    def __add__(self,other):
        b=as_c(other);return C(self.re+b.re,self.im+b.im)
    __radd__=__add__
    def __neg__(self):return C(-self.re,-self.im)
    def __sub__(self,other):return self+-as_c(other)
    def __rsub__(self,other):return as_c(other)+-self
    def __mul__(self,other):
        b=as_c(other);return C(self.re*b.re-self.im*b.im,self.re*b.im+self.im*b.re)
    __rmul__=__mul__
    def conj(self):return C(self.re,-self.im)
    def abs2(self):return self.re*self.re+self.im*self.im
    def __truediv__(self,other):
        b=as_c(other);require(b.abs2()>0,'Nonzero complex denominator')
        a=self*b.conj();return C(a.re/b.abs2(),a.im/b.abs2())


def as_c(x):return x if isinstance(x,C) else C(F(x))
ZERO=C();ONE=C(F(1))


def i_power(k):return (ONE,C(F(0),F(1)),-ONE,C(F(0),F(-1)))[k%4]


def phase(state,kg,kd):
    g,d=v.action(state);exponent=kg*(g-1)+kd*32*d
    require(exponent.denominator==1,'Declared diagnostic phase lies in Gaussian rationals')
    return i_power(exponent.numerator)


def psd_pivots(matrix):
    """Exact Hermitian Schur reduction, including zero-pivot PSD cases."""
    n=len(matrix);a=[[as_c(x) for x in row] for row in matrix];pivots=[]
    require(all(a[i][j]==a[j][i].conj() for i in range(n) for j in range(n)),
            'Hermitian matrix')
    for k in range(n):
        p=a[k][k];require(p.im==0 and p.re>=0,'Nonnegative Schur pivot')
        pivots.append(p.re)
        if not p.re:
            require(all(a[k][j]==ZERO for j in range(k+1,n)),'Zero pivot has zero row')
            continue
        for i in range(k+1,n):
            for j in range(k+1,n):a[i][j]=a[i][j]-a[i][k]*a[k][j]/p.re
    return pivots


def gram(amplitudes,channel_masses,kind):
    size=len(amplitudes)
    if kind=='all_numbers':
        a=[sum(row,ZERO) for row in amplitudes]
        return [[a[i].conj()*a[j] for j in range(size)] for i in range(size)]
    return [[sum((amplitudes[i][n].conj()*amplitudes[j][n]/channel_masses[n]
                  for n in range(len(channel_masses))),ZERO)
             for j in range(size)] for i in range(size)]


def subset_value(matrix,a,b):
    return sum((matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix))
                if a>>i&1 and b>>j&1),ZERO)


def functional_audit(matrix):
    n=len(matrix);full=(1<<n)-1;p=subset_value(matrix,full,full)
    require(p.im==0 and p.re>=0,'Nonnegative branch mass')
    pivots=psd_pivots(matrix);addition=grade2=0
    for a in range(full+1):
        for b in range(full+1):
            if a&b:continue
            for c in range(full+1):
                require(subset_value(matrix,a|b,c)==subset_value(matrix,a,c)+subset_value(matrix,b,c),
                        'Event additivity')
                addition+=1
                if a&c or b&c:continue
                mu=lambda x:subset_value(matrix,x,x)
                require(mu(a|b|c)==mu(a|b)+mu(a|c)+mu(b|c)-mu(a)-mu(b)-mu(c),
                        'Grade-two sum rule')
                grade2+=1
    if p.re:
        normalized=[[x/p.re for x in row] for row in matrix]
        require(subset_value(normalized,full,full)==ONE,'Normalized decoherence functional')
    else:normalized=None
    return {'total_mass':p.re,'psd_pivots':pivots,'additivity_checks':addition,
            'grade_two_checks':grade2,'normalized_atoms':normalized,
            'medium_decoherent':all(matrix[i][j]==ZERO for i in range(n) for j in range(n) if i!=j)}
