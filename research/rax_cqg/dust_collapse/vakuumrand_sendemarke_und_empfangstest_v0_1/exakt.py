"""Exact calculation at the nominal send time in Q(sqrt(937)).
Pairs store rational and radical coefficients. No interval solver is imported.
"""
from fractions import Fraction as F
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Number:
    a:F
    b:F=F(0)

    def __add__(self,other):
        q=num(other)
        return Number(self.a+q.a,self.b+q.b)
    __radd__=__add__

    def __neg__(self):
        return Number(-self.a,-self.b)

    def __sub__(self,other):
        return self+(-num(other))

    def __rsub__(self,other):
        return num(other)-self

    def __mul__(self,other):
        q=num(other)
        return Number(self.a*q.a+937*self.b*q.b,self.a*q.b+self.b*q.a)
    __rmul__=__mul__

    def __truediv__(self,other):
        q=num(other)
        norm=q.a*q.a-937*q.b*q.b
        return self*Number(q.a/norm,-q.b/norm)

    def as_pair(self): return [str(self.a),str(self.b)]


def num(value): return value if isinstance(value,Number) else Number(F(value))


def check():
    zero=num(0)
    t=num(F(1,12));u=Number(F(1,12),F(-1,12))
    y={0:num(-5),1:num(-4),2:num(-3),15:u,16:t,**{j:num(j-5) for j in range(7,11)}}
    # Enumerate the local density terms and solve the two current equations
    # directly as a linear system in w_z and the increment of w_7.
    parents={0:-8,1:16,2:-9,15:1}
    zf={7:1,8:-9,9:16,10:-8};uf={7:-9,8:16,9:-8}
    density=19+sum((b*(t-y[i])*(t-y[i]) for i,b in parents.items()),zero)
    assert density==zero
    moment=sum((b*(t-y[i]) for i,b in parents.items()),zero)
    a,b=moment,-(y[7]-t)
    c,d=t-u,uf[7]*(y[7]-u)
    rhs1=sum((weight*(y[k]-t)/64 for k,weight in zf.items()),zero)
    rhs2=-sum((weight*(y[k]-u)/64 for k,weight in uf.items()),zero)
    det=a*d-b*c
    wz=(rhs1*d-b*rhs2)/det
    increment=(a*rhs2-rhs1*c)/det
    w={i:num(0) for i in y}
    for i in (7,8,9,10):w[i]=num(F(1,64))
    w[7]+=increment;w[16]=wz
    edges={(i,16):v for i,v in parents.items()}
    edges.update({(16,i):v for i,v in zf.items()})
    edges.update({(15,i):v for i,v in uf.items()})
    def part(y,weights):
        # All terms of the matter action depending on Y_u, Y_z or w_z.
        return 19*weights[16]+sum((v*weights[j]*(y[j]-y[i])*(y[j]-y[i])
                                   for (i,j),v in edges.items()),zero)
    for i in (15,16):
        delta=F(1,2048)
        assert part({**y,i:y[i]+delta},w)-part({**y,i:y[i]-delta},w)==zero
    delta=F(1,10**7)
    assert part(y,{**w,16:w[16]+delta})-part(y,{**w,16:w[16]-delta})==zero
    return {'basis':['1','sqrt(937)'],'epsilon':(64*increment).as_pair(),'w_z':wz.as_pair(),
            'Y_u':u.as_pair(),'Y_z':t.as_pair(),'density_z':density.as_pair(),
            'stationary_clock_15_and_16':True}


if __name__=='__main__': print(json.dumps(check(),sort_keys=True,indent=2))
