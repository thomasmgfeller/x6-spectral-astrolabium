"""Inputs and exact arithmetic shared by the finite Poisson audit.
SPDX-License-Identifier: Apache-2.0
"""
import sys
import hashlib
from pathlib import Path
from fractions import Fraction as F
import numpy as np
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'stability_information'
DATA=HERE.parent/'eligibility_before_cap'
sys.path.insert(0,str(OLD))
from st_common import read,save,input_mask,frozen as prior_frozen
from st_certificate import sqrt_bounds,pi_bounds,outward,solve,interval,exact_weights

def frozen():
    prior_frozen()
    for name,h in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name

def up(x,digits=24):return F(outward(x,digits=digits)[1])
def rootup(x):return up(sqrt_bounds(x)[1])
def normup(v):return rootup(sum(x*x for x in np.asarray(v,dtype=object).flat))
def infnorm(A):return max(sum(abs(x) for x in row) for row in A)
def inverse(A):
    n=len(A)
    return np.array([solve(A,[int(i==j) for i in range(n)]) for j in range(n)],dtype=object).T

def cube_bounds(x,digits=32):
    assert x>=0
    scale=10**digits;integer=x.numerator*scale**3//x.denominator
    lo=0;hi=1<<((integer.bit_length()+2)//3)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**3<=integer:lo=mid
        else:hi=mid
    return F(lo,scale),F(lo+1,scale)

def count_box(n,c=12):
    n,c=F(n),F(c)
    assert n>=0 and n.denominator==1 and c>0
    if n==0:return F(0),c  # Exact zero-count tail, sharper than quadratic inversion.
    low=max(F(0),n-sqrt_bounds(2*n*c)[1])
    high=n+c+sqrt_bounds(c*c+2*n*c)[1]
    return F(outward(low,digits=30)[0]),F(outward(high,digits=30)[1])

def q_box(counts,rho,scale,c=12):
    pi0,pi1=pi_bounds();factor=F(rho,12)*scale**3
    result=[]
    for n in counts:
        lo,hi=count_box(n,c)
        result.append((cube_bounds((lo/(factor*pi1))**2)[0],
                       cube_bounds((hi/(factor*pi0))**2)[1]))
    return result

def confidence_bound(total,c=12):
    # e^c exceeds every finite sum of its positive Taylor series.
    lower=sum(F(c)**k/F(__import__('math').factorial(k)) for k in range(120))
    upper=F(2*total)/lower
    assert upper<F(1,20)
    return upper

def input_record(index):
    source=read(DATA/f'results/cloud-{index:02d}.json.gz')
    p=source['selection']['arms']['candidate']['packet']
    obs=source['replicates'][0]['arms']['candidate']['observed']
    anchors=set(p['landmarks'])
    mask=[i for i,(a,b) in enumerate(p['pairs']) if a in anchors or b in anchors]
    assert mask==list(np.flatnonzero(input_mask(p)))
    return p,obs,mask
