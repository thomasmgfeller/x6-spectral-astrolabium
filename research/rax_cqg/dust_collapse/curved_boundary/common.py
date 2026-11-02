"""Geometry in local similarity units U=Ts-s. New code needs numpy and scipy."""
import math
from functools import cache
import numpy as np
from scipy.special import roots_legendre

b=math.pi/24
factorial=math.factorial
@cache
def nodes(n):
    x,w=roots_legendre(n)
    return (x+1)/2,w/2

def coeff(j,k):
    moment=(192*factorial(2*j)*factorial(2*k+3)/
            (factorial(2*j+2*k+4)*2**(2*j+2*k+4)*(2*k+1)*(2*k+3)))
    return moment*factorial(8)/(factorial(8-2*j-2*k)*factorial(2*j)*factorial(2*k))

def geometry(h,w):
    ay=(1+h*w)**(1/3)
    ax=(1-(1-h)*w)**(1/3)
    divided=3/(ay*ay+ay*ax+ax*ax)
    amid=(ay+ax)/2
    e=(w*divided/(3*amid))**2
    pref=divided**4*amid**8
    S=(1+h*w)**2*divided**3
    # H(q) in powers of q=1-(r/d)^2.
    hpol=[sum(coeff(j,k)*math.comb(k,n)*(-1)**n*e**(j+k)
              for k in range(n,5) for j in range(5-k))*pref for n in range(5)]
    return S,hpol

def write_rows(path,rows):
    import csv
    with open(path,'w',newline='') as f:
        out=csv.DictWriter(f,fieldnames=list(rows[0]))
        out.writeheader()
        out.writerows(rows)
