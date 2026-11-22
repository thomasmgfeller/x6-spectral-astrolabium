"""Separate numerical integration from direct clock/density formulas; not used to decide bounds."""
import cmath
import math
from itertools import combinations
from fractions import Fraction as Q
from modell import a,s
from traeger import edges


def halton(i,b):
    x,scale=0.,1.
    while i:
        i,digit=divmod(i,b);scale/=b;x+=digit*scale
    return x


def independent_rules(code):
    internal=edges(code,7)
    chains=[seq for k in range(1,8) for seq in combinations(range(7),k)
            if all(edge in internal for edge in combinations(seq,2))]
    paths=[seq for seq in chains if not any(set(seq)<set(long) for long in chains)]
    height=max(map(len,paths))
    centres=[0.5 if all(len(p)==1 for p in paths if j in p) else
             max(p.index(j)+1 for p in paths if j in p)/(height+1) for j in range(7)]
    visible=[sum((i,j) in internal for i in range(7))<4 for j in range(7)]
    return paths,centres,visible


def estimate(code,*,reconstructed=False):
    paths,centres,visible=independent_rules(code)
    if reconstructed:
        visible=[True]*7
    edges3=a.coefficients(a.support.geometry(code)[1])
    delta=(3/722)**.25
    sums={rho:[[0j,0j],[0j,0j]] for rho in a.RHO}
    for n in range(1,4097):
        q=[halton(n,b) for b in (2,3,5,7,11,13,17,19,23)]
        u=[centres[i]+(q[i]-.5)/32 for i in range(7)]
        f=[0.]*7
        for path in paths:
            cuts=[0.]+[(u[i]+u[j])/2 for i,j in zip(path,path[1:])]+[1.]
            for j,l,h in zip(path,cuts,cuts[1:]):
                f[j]+=(h-l)/len(paths)
        fv=[f[j] if vis else 0. for j,vis in enumerate(visible)]
        for lobe,(left,right) in enumerate(a.support.WINDOWS):
            off=float(left)+float(right-left)*q[7];D=4*delta-off
            y={v:v-5 for v in s.P+s.F};y[3]+=off/delta
            y.update({v:y[3]+D*u[i]/delta for i,v in enumerate(s.I)})
            coef=[1.]*15
            for i,j,k in edges3:coef[j]+=k*(y[i]-y[j])**2/19
            w=[4*D*v for v in f]
            deriv=[-coef[v]*wj*.005 for v,wj in zip(s.I,w)]
            jac=D**14*math.prod(f)
            for arm,sign in enumerate((1,-1)):
                args=[d+sign*.01*fval for d,fval in zip(deriv,fv)]
                sf=math.prod(math.sin(z)/z if z else 1. for z in args)
                inner=-.5*sum(coef[v]*wj for v,wj in zip(s.I,w))
                future=-sum(coef[v] for v in s.F)/16
                past=-sum(coef[v] for v in s.P)/2
                for rho in sums:
                    phase=inner+future+past*(float(rho)+(q[8]-.5)/16)+sign*sum(fv)
                    sums[rho][lobe][arm]+=jac*sf*cmath.exp(1j*phase)
    def decode(z):return cmath.phase(z)/2-1
    result={}
    for rho,(left,right) in sums.items():
        val={}
        for key,t in [('gleichphasig',1),('gegenphasig',-1),('vierteldrehung',1j)]:
            p,n=(l+t*r for l,r in zip(left,right))
            val[key]=decode(p*n.conjugate())
        val['dephasiert']=decode(sum(p*n.conjugate() for p,n in (left,right)))
        result[rho]=val
    return result
