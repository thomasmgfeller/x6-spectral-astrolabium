"""Certified tensor integration of the normalized continuous field measure."""
from fractions import Fraction as F
from itertools import product
from math import factorial
import geometry as g
import gauss
import intervals_fp as fp


def integrate(orders,h,mu,tolerance=F(1,10**10)):
    n=len(orders[0]);bounds=[g.derivative_bounds(o,h) for o in orders]
    if mu==0:
        return [(fp.ONE,fp.ZERO) for _ in orders],[F(0) for _ in orders],{
            'orders':[], 'evaluations':0,'normalization_interval':[F(1),F(1)],
            'derivative_bounds':bounds,'quadrature_errors':[F(0) for _ in orders]}
    qs,errors=gauss.select_orders(bounds,mu,tolerance,n)
    rules=[gauss.rule(q) for q in qs]
    unique=[];geometry_indices=[]
    for order in orders:
        polynomials,_=g.action_polynomials(order,h);indices=[]
        for poly in polynomials:
            key=tuple(sorted(poly.items()))
            if key not in unique:unique.append(key)
            indices.append(unique.index(key))
        geometry_indices.append(indices)
    compiled=[[(key,fp.I.rational(mu*c)) for key,c in poly] for poly in unique]
    keys=sorted({key for poly in compiled for key,_ in poly})
    accum=[(fp.ZERO,fp.ZERO) for _ in orders];norm=fp.ZERO
    for ix in product(*(range(q) for q in qs)):
        u=[rules[j][0][i] for j,i in enumerate(ix)]
        powers=[[fp.ONE,x,x*x] for x in u]
        monomials={}
        for key in keys:
            v=fp.ONE
            for j,k in enumerate(key):v=v*powers[j][k]
            monomials[key]=v
        chars=[]
        for poly in compiled:
            t=sum((monomials[key]*c for key,c in poly),fp.ZERO)
            chars.append(fp.density_characteristic(t))
        weight=fp.I.rational(factorial(n))
        for j,i in enumerate(ix):weight=weight*rules[j][1][i]*(u[j]**j)
        norm=norm+weight
        for j,indices in enumerate(geometry_indices):
            value=(fp.ONE,fp.ZERO)
            for k in indices:value=fp.cmul(value,chars[k])
            accum[j]=fp.cadd(accum[j],fp.cscale(value,weight))
    fp.require(norm.contains(1),'Normalized tensor Jacobian integral')
    for value,error in zip(accum,errors):
        arithmetic=value[0].radius()+value[1].radius()
        fp.require(arithmetic<=F(1,10**20),'Arithmetic error budget')
        fp.require(arithmetic+error<=tolerance,'Total amplitude error budget')
    return accum,errors,{'orders':qs,'evaluations':__import__('math').prod(qs),
        'normalization_interval':norm.endpoints(),'unique_density_polynomials':len(unique),
        'derivative_bounds':bounds,'quadrature_errors':errors}
