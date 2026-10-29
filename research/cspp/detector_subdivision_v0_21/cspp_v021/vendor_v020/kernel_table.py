"""Rigorous upper table for n0=0..191 and Poisson means in 512 closed bins.

Each binary64 entry is rounded upward from an Arb enclosure, and is only
used as an upper bound. Inputs outside the table fall back to kappa.
"""
import math
from fractions import Fraction as F
import numpy as np
from flint import arb, ctx
from kernel import weight, positive_indices

def make_table():
    positive=set(positive_indices()[0]);kappa=arb('4976184375/4294967296')
    out=np.empty((192,512),dtype=np.float64)
    for n in range(192):
        coeff=[arb(str(weight(n+j)/math.factorial(j))) if n+j in positive else arb(0) for j in range(max(0,71-n))]
        bs=[arb(str(F(math.comb(n,j),16**j)*F(15,16)**(n-j))) for j in range(min(n,3)+1)]
        for i in range(512):
            mu=arb(2*i+1,1);z=mu/16
            ps=[1-9*z+8*z*z-arb(4)/3*z**3,-9+16*z-4*z*z,16-8*z,arb(-8)]
            signed=(-z).exp()*sum(b*p for b,p in zip(bs,ps))
            correction=arb(0)
            for c in reversed(coeff):correction=correction*mu+c
            E=-signed+2*(-mu).exp()*correction
            if not E.is_finite():raise ArithmeticError('finite kernel table entry')
            u=min(kappa,max(arb(0),E.upper()))
            f=float(u)
            while not arb(f)>=u:f=float(np.nextafter(f,np.inf))
            out[n,i]=f
    return out

def upper(table,nlo,nhi,mulo,muhi):
    cap=arb('4976184375/4294967296')
    lo=max(0,int((mulo.lower()/2).floor().unique_fmpz()))
    hi=max(0,int((muhi.upper()/2).floor().unique_fmpz()))
    if nhi>=table.shape[0] or hi>=table.shape[1]:return cap
    if nlo>nhi or lo>hi:raise ArithmeticError('unordered table query')
    return min(cap,arb(float(np.max(table[int(nlo):int(nhi)+1,lo:hi+1]))))
