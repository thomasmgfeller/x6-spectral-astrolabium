"""Sparse exact polynomial transfer in four jointly distributed real weights."""
from flint import acb,arb
from kernel import require,ball
ZERO=(0,0,0,0)

class Poly:
    def __init__(self,terms=None):self.terms={k:acb(v) for k,v in (terms or {}).items() if not acb(v).is_zero()}
    @staticmethod
    def const(x):return Poly({ZERO:acb(x)})
    @staticmethod
    def variable(i):
        n=list(ZERO);n[i]=1;return Poly({tuple(n):1})
    def __add__(self,other):
        other=other if isinstance(other,Poly) else Poly.const(other);out=dict(self.terms)
        for k,v in other.terms.items():out[k]=out.get(k,acb(0))+v
        return Poly(out)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.terms.items()})
    def __sub__(self,other):return self+-other if isinstance(other,Poly) else self+(-acb(other))
    def __rsub__(self,other):return -self+other
    def __mul__(self,other):
        other=other if isinstance(other,Poly) else Poly.const(other);out={}
        for k,v in self.terms.items():
            for l,w in other.terms.items():
                n=tuple(a+b for a,b in zip(k,l));out[n]=out.get(n,acb(0))+v*w
        return Poly(out)
    __rmul__=__mul__
    def conj(self):return Poly({k:v.conjugate() for k,v in self.terms.items()})
    def mean(self,law):return sum((v*law.moment(k) for k,v in self.terms.items()),acb(0))
    def evaluate(self,x):
        return sum((v*product_power(x,k) for k,v in self.terms.items()),acb(0))

def product_power(x,k):
    r=acb(1)
    for a,n in zip(x,k):r*=acb(ball(a))**n
    return r

def covariance(polys,law):
    mu=[p.mean(law) for p in polys];centered=[p-m for p,m in zip(polys,mu)]
    C=[[(p*q.conj()).mean(law) for q in centered] for p in centered]
    P=[[(p*q).mean(law) for q in centered] for p in centered]
    return mu,C,P

def causal_orders(K,b,law):
    """v0,v1,...,vn. K is strictly lower triangular, b random and correlated."""
    n=len(b)
    require(all(not K[i][j].terms for i in range(n) for j in range(i,n)),'retarded lower triangle')
    K0=[[x.mean(law) for x in row] for row in K];b0=[x.mean(law) for x in b]
    def solve0(rhs):
        out=[]
        for i in range(n):out.append(rhs[i]+sum((K0[i][j]*out[j] for j in range(i)),Poly()))
        return out
    base=solve0([Poly.const(x) for x in b0]);delta=[[K[i][j]-K0[i][j] for j in range(n)] for i in range(n)]
    forcing=[b[i]-b0[i]+sum((delta[i][j]*base[j] for j in range(i)),Poly()) for i in range(n)]
    orders=[base,solve0(forcing)]
    for _ in range(n-1):orders.append(solve0([sum((delta[i][j]*orders[-1][j] for j in range(i)),Poly()) for i in range(n)]))
    require(all(not p.terms for p in orders[-1]),'nilpotent expansion terminates')
    return orders[:-1]

def solve_polynomial(K,b):
    out=[]
    for i in range(len(b)):out.append(b[i]+sum((K[i][j]*out[j] for j in range(i)),Poly()))
    return out


def observation_orders(Q,orders,law):
    """Include random detector coefficients and their cross correlations."""
    Q0=[[p.mean(law) for p in row] for row in Q]
    dQ=[[p-m for p,m in zip(row,means)] for row,means in zip(Q,Q0)]
    out=[]
    for k in range(len(orders)+1):
        row=[]
        for i in range(len(Q)):
            a=sum((Q0[i][j]*orders[k][j] for j in range(len(Q[i]))),Poly()) if k<len(orders) else Poly()
            if k:a+=sum((dQ[i][j]*orders[k-1][j] for j in range(len(Q[i]))),Poly())
            row.append(a)
        out.append(row)
    return out
