"""Exact action polynomials, Bernstein bounds and ordered-clock integrals."""
from fractions import Fraction as F
from itertools import product
from math import comb,factorial
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
import intervals as v


def add(a,b):
    out=dict(a)
    for k,x in b.items():out[k]=out.get(k,F(0))+x
    return {k:x for k,x in out.items() if x}
def scale(a,c):return {k:x*c for k,x in a.items() if x*c}
def mul(a,b):
    out={}
    for k,x in a.items():
        for l,y in b.items():
            z=tuple(i+j for i,j in zip(k,l));out[z]=out.get(z,F(0))+x*y
    return {k:x for k,x in out.items() if x}


def action_polynomials(order,h,cube=True):
    n=len(order);zero=(0,)*n
    x=[{}]+[{tuple(int(k>=j if cube else k==j) for k in range(n)):F(1)} for j in range(n)]
    a=[{zero:F(1,2)} for _ in order]
    for y,z,k in v.m.intervals(v.m.with_anchor(order)):
        if k>=4:continue
        diff=add(x[z],scale(x[y],-1))
        a[z-1]=add(a[z-1],scale(mul(diff,diff),4*h*h*v.m.B[k]))
    phase={}
    for j,poly in enumerate(a):
        for key,c in poly.items():phase[key+tuple(int(i==j) for i in range(n))]=-c
    return a,phase


def derivative(poly,j):
    out={}
    for key,c in poly.items():
        if key[j]:
            z=list(key);z[j]-=1;out[tuple(z)]=c*key[j]
    return out


def bernstein_bounds(poly,dimension):
    if not poly:return F(0),F(0)
    degrees=[max(k[j] for k in poly) for j in range(dimension)];values=[]
    for index in product(*(range(d+1) for d in degrees)):
        value=F(0)
        for key,c in poly.items():
            if any(a>b for a,b in zip(key,index)):continue
            f=c
            for a,b,d in zip(key,index,degrees):f*=F(comb(b,a),comb(d,a))
            value+=f
        values.append(value)
    return min(values),max(values)


def derivative_bounds(order,h):
    n=len(order);_,phase=action_polynomials(order,h);out=[]
    for j in range(n):
        first=bernstein_bounds(derivative(phase,j),2*n)
        second=bernstein_bounds(scale(derivative(derivative(phase,j),j),F(1,2)),2*n)
        out.append({'first_range':first,'quadratic_range':second,
                    'D':max(map(abs,first)),'A':max(map(abs,second))})
    return out


def evaluate(poly,values):
    return sum((c*product_values(values,key) for key,c in poly.items()),F(0))
def product_values(values,key):
    out=F(1)
    for x,k in zip(values,key):out*=x**k
    return out


def density_moment(k):return F(1) if k==0 else F(1,2*(k+1))


def integrate_monomial(key,n,cube):
    out=F(factorial(n));acc=0
    for j in range(n):
        if cube:out/=key[j]+j+1
        else:acc+=key[j];out/=acc+j+1
    for j in range(n,2*n):out*=density_moment(key[j])
    return out


def low_moments(order,h,K=3,cube=True):
    n=len(order);_,phase=action_polynomials(order,h,cube=cube)
    poly={(0,)*(2*n):F(1)};out=[]
    for _ in range(K+1):
        out.append(sum((c*integrate_monomial(key,n,cube) for key,c in poly.items()),F(0)))
        poly=mul(poly,phase)
    return out
