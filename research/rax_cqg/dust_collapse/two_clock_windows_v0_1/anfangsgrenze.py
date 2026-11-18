"""Rationale Untergrenze für das spätere Dichteatom. Direkte Ordnung und volle Gaußmatrix."""
import argparse
import json
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from math import factorial, isqrt
from pathlib import Path
from schnitt import ROOT, check_sources
from zero_one_pairing_v0_1 import schranken

S = 10**40


class Interval:
    """Endpunkte sind ganze Vielfache von 1/S, jede Operation rundet nach aussen."""
    def __init__(self, lo, hi):
        self.lo, self.hi = lo, hi

    @classmethod
    def from_fraction(cls, lo, hi=None):
        a, b = F(lo)*S, F(lo if hi is None else hi)*S
        return cls(a.numerator//a.denominator, -(-b.numerator//b.denominator))

    def __add__(self, y):
        return Interval(self.lo+y.lo, self.hi+y.hi)

    def __neg__(self):
        return Interval(-self.hi,-self.lo)

    def __sub__(self, y):
        return self + (-y)

    def __mul__(self, y):
        a = [v*w for v in (self.lo,self.hi) for w in (y.lo,y.hi)]
        return Interval(min(a)//S,-(-max(a)//S))

    def sq(self):
        a,b=self.lo**2,self.hi**2
        return Interval(0 if self.lo<=0<=self.hi else min(a,b)//S,-(-max(a,b)//S))

    def inv(self):
        if self.lo<=0<=self.hi: raise ArithmeticError('Intervall enthält null')
        return Interval(S*S//self.hi,-(-S*S//self.lo))

    def root(self):
        if self.lo<0: raise ArithmeticError('nicht reelle Wurzel')
        return Interval(isqrt(self.lo*S),isqrt(self.hi*S)+1)

    def output(self, digits=18):
        return schranken.decimal_bounds((F(self.lo,S),F(self.hi,S)),digits)


def num(x):
    return x if isinstance(x,Interval) else Interval.from_fraction(x)


class Box:
    def __init__(self,re,im=0):
        self.re,self.im=num(re),num(im)

    def __add__(self,y):
        return Box(self.re+y.re,self.im+y.im)

    def __sub__(self,y):
        return Box(self.re-y.re,self.im-y.im)

    def __mul__(self,y):
        return Box(self.re*y.re-self.im*y.im,self.re*y.im+self.im*y.re)

    def sqnorm(self):
        return self.re.sq()+self.im.sq()

    def inv(self):
        s=self.sqnorm().inv()
        return Box(self.re*s,(-self.im)*s)

    def root(self):
        real=((self.sqnorm().root()+self.re)*num(F(1,2))).root()
        return Box(real,self.im*(num(2)*real).inv())


@lru_cache(maxsize=None)
def phase(k):
    t=F(k,1024)
    if abs(t)>1: raise ArithmeticError('Taylorbereich')
    re=sum((-1)**j*t**(2*j)/factorial(2*j) for j in range(13))
    im=sum((-1)**j*t**(2*j+1)/factorial(2*j+1) for j in range(12))
    err=abs(t)**25/factorial(25)
    v=Box(Interval.from_fraction(re-err,re+err),Interval.from_fraction(im-err,im+err))
    for _ in range(10): v=v*v
    return v


def direct_order(code1,code2):
    rel=set()
    for code,offset in ((code1,0),(code2,3)):
        rel.update((i+offset,j+offset) for i in range(5) for j in range(i+1,5) if code & 1<<(5*i+j))
    for k in range(8):
        rel.update((i,j) for i in range(k) for j in range(k+1,8) if (i,k) in rel and (k,j) in rel)
    terms={(i,j):(1,-9,16,-8,0)[min(4,sum((i,k) in rel and (k,j) in rel for k in range(i+1,j)))]
           for i,j in rel}
    return terms


def enclose_scalar(terms, pi, factor):
    h=[[0]*8 for _ in range(8)]
    for (i,j),c in terms.items():
        h[i][i]-=c
        h[j][j]-=c
        h[i][j]+=c
        h[j][i]+=c
    # A different outer pivot order from the main calculation.
    order=(7,6,1,0,2,3,4,5)
    m=[[Box(int(i==j and i in (0,1,6,7)),num(-h[i][j])*factor) for j in order] for i in order]
    root=Box(1)
    for k in range(8):
        p=m[k][k]
        pivot_root=p.root()
        root=root*pivot_root
        inv=p.inv()
        for i in range(k+1,8):
            entry=m[i][k]*inv
            for j in range(k+1,8):
                m[i][j]=m[i][j]-entry*m[k][j]
    return Box(pi*pi*pi*num(F(1,8*1089)))*phase(8-sum(terms.values()))*root.inv()


def run():
    commit=check_sources()
    hist=json.loads((ROOT.parent/'amplitude_existence_v0_1/inputs/aa_hessians.json').read_text())['histories']
    pi=Interval.from_fraction(*schranken.PI)
    factor=num(F(2,3)).root()
    counts=Counter()
    sums={p:Box(0) for p in (1,2)}
    for a in hist:
        for b in hist:
            terms=direct_order(a['order_code'],b['order_code'])
            p=sum((j,2) in terms for j in (0,1))
            counts[terms.get((2,5),0)]+=1
            sums[p]=sums[p]+enclose_scalar(terms,pi,factor)
    record=Box(0)
    for p,z in sums.items():
        re,im=schranken.dust_mean(p,F(0))
        record=record+Box(4)*z*Box(Interval.from_fraction(*re),Interval.from_fraction(*im))
    atom=record.sqnorm()*num(F(1,2))
    if atom.lo<=0: raise ArithmeticError('positiver Anfangsbeitrag offen')
    return dict(commit=commit,counts=dict(sorted(counts.items())),
                parent_sums={str(p):[z.re.output(),z.im.output()] for p,z in sums.items()},
                right_density_atom_at_origin=atom.output(),pairs=sum(counts.values()))


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args()
    args.out.write_text(json.dumps(run(),sort_keys=True,indent=2)+'\n')
