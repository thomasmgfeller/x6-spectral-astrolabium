"""Exact continuous matter moments and certified real-phase Taylor bounds."""
from fractions import Fraction as F
from math import comb, factorial, lcm
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
import readout as r


def require(ok,message):r.require(ok,message)


def density_moment(k):return F(1) if k==0 else F(1,2*(k+1))


def multiply(a,b):
    c={}
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            key=i+k,j+l;c[key]=c.get(key,0)+x*y
    return {k:v for k,v in c.items() if v}


def coefficients(h,kind):
    a={(0,0):F(1,2),(2,0):4*h*h}
    if kind=='antichain':b={(0,0):F(1,2),(0,2):4*h*h}
    else:b={(0,0):F(1,2),(2,0):4*h*h,(1,1):-8*h*h,(0,2):-32*h*h}
    D=lcm(*(x.denominator for x in list(a.values())+list(b.values())))
    return {k:int(v*D) for k,v in a.items()},{k:int(v*D) for k,v in b.items()},D


def continuous_moments(h,kind,K):
    """Normalized ordered-clock moments. All integrals are exact rationals."""
    a,b,D=coefficients(h,kind)
    ap=[{(0,0):1}];bp=[{(0,0):1}]
    for _ in range(K):ap.append(multiply(ap[-1],a));bp.append(multiply(bp[-1],b))
    L=lcm(*range(1,2*K+3))**2;W=2*lcm(*range(1,K+2))
    wm=[W]+[W//(2*(k+1)) for k in range(1,K+1)]
    integrals={(i,j):2*L//((i+1)*(i+j+2)) for i in range(2*K+1)
               for j in range(2*K+1-i)}
    require(all(2*L%((i+1)*(i+j+2))==0 for i,j in integrals),'Exact integral denominator')
    moments=[]
    for k in range(K+1):
        total=0
        for q in range(k+1):
            s=k-q;factor=comb(k,q)*wm[q]*wm[s]
            integral=sum(x*y*integrals[i+j0,j1]
                         for (i,_),x in ap[q].items() for (j0,j1),y in bp[s].items())
            total+=factor*integral
        moments.append(F((-1)**k*total,D**k*L*W**2))
    return moments


def one_moments(h,K):
    return [(-1)**k*density_moment(k)*sum(
            (F(comb(k,j))*F(1,2)**(k-j)*(4*h*h)**j/F(2*j+1)
             for j in range(k+1)),F(0)) for k in range(K+1)]


def phase_bound(h,kind):
    one=F(1,2)+4*h*h
    if kind=='one':return one
    if kind=='antichain':return 2*one
    return one+max(F(1,2),36*h*h-F(1,2))


def amplitude(moments,mu,M):
    K=len(moments)-1
    t=sum((r.i_power(k)*(mu**k*moments[k]/factorial(k)) for k in range(K+1)),r.ZERO)
    error=(abs(mu)*M)**(K+1)/factorial(K+1)
    return t,error


def visibility(t,error):
    slack=2*error+error**2
    return [max(F(0),t.abs2()-slack),min(F(1),t.abs2()+slack)]


def polynomial_value(poly,x,y,D):
    return sum((F(c,D)*x**i*y**j for (i,j),c in poly.items()),F(0))


def low_order_independent(h,kind,K=3):
    """Direct four-variable power, explicit atom/uniform mixture, distinct route."""
    a,b,D=coefficients(h,kind)
    action={(i,j,1,0):-F(c,D) for (i,j),c in a.items()}
    action.update({(i,j,0,1):-F(c,D) for (i,j),c in b.items()})
    poly={(0,0,0,0):F(1)};out=[]
    for k in range(K+1):
        val=F(0)
        for (i,j,u,v),c in poly.items():
            density=F(0)
            for atom1 in [False,True]:
                for atom2 in [False,True]:
                    dw1=F(int(u==0)) if atom1 else F(1,u+1)
                    dw2=F(int(v==0)) if atom2 else F(1,v+1)
                    density+=dw1*dw2/4
            val+=c*F(2,(i+1)*(i+j+2))*density
        out.append(val)
        nxt={}
        for key,c in poly.items():
            for key2,d in action.items():
                z=tuple(x+y for x,y in zip(key,key2));nxt[z]=nxt.get(z,F(0))+c*d
        poly={z:c for z,c in nxt.items() if c}
    return out
