"""Exact phase bounds; Gauss-to-continuum estimate for the single N15_356087 clock."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import argparse,json
import numpy as np
import mpmath as mp
from mpmath import iv
from source import reference
from reference import layout,net
iv.dps=50
def I(x):
    x=F(x);return iv.mpf(x.numerator)/x.denominator
def mul(x,y):
    v=[a*b for a in x for b in y]
    return min(v),max(v)
def plus(x,y):return x[0]+y[0],x[1]+y[1]
def scaled(a,x):return mul((a,a),x)
def point(z):return(z,z)
def interval(x):return iv.mpf([I(x[0]).a,I(x[1]).b])
def bounds():
    inner,c,_=layout((7,356087))
    beta=(F('1.63299316185'),F('1.63299316186'))
    step=(F('.25389024'),F('.25389025'))
    assert beta[0]**2<F(8,3)<beta[1]**2
    assert step[0]**2*19*beta[1]<2<step[1]**2*19*beta[0]
    specs=[(96,31,93,2),(68,17,68,2),(48,10,44,F(5,2)),(48,1,56,3),(24,1,3,4),
           (56,1,65,3),(48,F(1,20),54,3),(10,F(1,50),2,10)]
    out={};total=iv.mpf(0)
    for j,(n,A,B,r) in zip((*inner,3),specs,strict=True):
        a=plus(scaled(-2,step),(-F(1,16),F(1,16))) if j==3 else point(F(0))
        length=F(1,32) if j==3 else F(3,2)
        terms={}
        for (i,k),v in c.items():
            if not v or j not in (i,k):continue
            o=k if j==i else i
            ran=(-F(3,2),F(3,2)) if o in inner else scaled(o-5,step)
            if o==3:ran=plus(ran,(-F(3,32),F(3,32)))
            tag=k if k in inner else ('P' if k in net.geometry.P else 'F')
            x,y=terms.get(tag,(0,point(0)))
            terms[tag]=x+v,plus(y,scaled(v,plus(a,scaled(-1,ran))))
        aa,bb=point(0),point(0)
        for tag,(x,y) in terms.items():
            mark=(0,1) if isinstance(tag,int) else (point(F(1,8)) if tag=='F' else (F(3,32),F(9,32)))
            aa=plus(aa,scaled(x,mark));bb=plus(bb,mul(mark,y))
        if max(map(abs,aa))*beta[1]*length**2/4>A or max(map(abs,bb))*beta[1]*length/2>B:
            raise ValueError(('quadratic phase coefficient',j,aa,bb))
        r=F(r)
        exponent=F(A)*(r**2-1/r**2)/4+F(B)*(r-1/r)/2
        err=4*iv.exp(I(exponent))*I(r**(1-2*n)/(r-1))
        total+=err
        out[str(j)]={'n':n,'A_cap':str(A),'B_cap':str(B),'ellipse':str(r),'error_approx':float(err.b)}
    if (total/iv.sqrt(768)).b>=I('2e-12'):raise ValueError('cubature error')
    # Local degree-5 interpolation at six consecutive nodes, central cell.
    # Cardinal maxima use distances bounded by (3,2,1,1,2,3).
    leb=sum(F(36,k*factorial(i)*factorial(5-i)) for i,k in enumerate((3,2,1,1,2,3)))
    assert leb==F(77,10)
    scale=beta[1]/2
    eu=F(36,720*14)*(scale*F(1,4)/2)**6
    ev=F(36,720*14)*(scale*F(3,2)*F(1,8))**6
    interp=I(eu+leb*ev)/iv.sqrt(768)
    assert interp.b<I('1.4e-8')
    return {'axes':out,'tensor_gauss_error_abs':'2e-12','lagrange_clock_error_abs':'1.4e-8',
            'auxiliary_factor_error':str(F(53**200,factorial(200)))}
def legendre(n,x):
    prev,cur=F(1),x
    for k in range(2,n+1):prev,cur=cur,((2*k-1)*x*cur-(k-1)*prev)/k
    return prev,cur
def nodes_audit(orders):
    result={}
    for n in sorted(set(orders)):
        xx,ww=net.quadrature(n); sw=F(0);max_x=F(0);last=-1
        for x,w in zip(xx,ww):
            with mp.workdps(60):
                m=mp.mpf(float(x))
                for _ in range(3):
                    pn=mp.legendre(n,m)
                    m-=pn*(1-m*m)/(n*(mp.legendre(n-1,m)-m*pn))
                centre=F(int(mp.nint(m*10**24)),10**24)
            width=F(2,10**24);lo,hi=centre-width,centre+width
            if not last<lo<hi<1 or legendre(n,lo)[1]*legendre(n,hi)[1]>=0:raise ValueError('root isolation')
            last=hi
            max_x=max(max_x,abs(F(float(x))-centre)+width)
            prev,cur=legendre(n,centre)
            deriv=n*(prev-centre*cur)/(1-centre**2)
            # Markov applied twice and |P_n|<=1 on [-1,1].
            dr=n**4*width;abs_hi=max(abs(lo),abs(hi));abs_lo=max(0,abs(centre)-width)
            if abs(deriv)<=dr:raise ValueError('derivative')
            wlo=1/((1-abs_lo**2)*(abs(deriv)+dr)**2)
            whi=1/((1-abs_hi**2)*(abs(deriv)-dr)**2)
            stored=F(float(w));sw+=max(abs(wlo-stored),abs(whi-stored))
        if sw>=F('1e-12') or max_x>=F('1e-14'):raise ValueError((n,float(sw),float(max_x)))
        result[n]={'weight_l1_upper':float(sw),'node_upper':float(max_x)}
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    data=bounds()
    data['gauss_nodes']=nodes_audit([v['n'] for v in data['axes'].values()]+[32,48,64,6,8,100])
    args.out.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
