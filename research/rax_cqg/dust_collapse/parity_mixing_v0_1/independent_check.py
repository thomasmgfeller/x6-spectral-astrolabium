"""Independent float64 control: full 5D rule and eigenphase scalar integral.

This is an implementation cross-check, never the certified error source.
It uses all 33 histories, no orbit reduction and no clock contraction.
"""
import json
import math
from fractions import Fraction
import numpy as np
from numpy.polynomial.legendre import leggauss
from core import ROOT

def scalar_from_eigenphases(H0):
    m=np.array([[float(Fraction(str(v))) for v in row] for row in H0])*4/math.sqrt(6)
    inds=[0,1,3,4];alpha=-m[2,2];j=m[2,inds]
    k=m[np.ix_(inds,inds)]+np.outer(j,j)/alpha
    eigenvalues=np.linalg.eigvalsh(k)
    factor=4*math.pi*math.sqrt(2*math.pi/alpha)*np.exp(-1j*math.pi/4)
    factor*=np.prod((1+eigenvalues**2)**(-.25))*np.exp(.5j*np.sum(np.arctan(eigenvalues)))
    return complex(factor)

def evaluate(n=8):
    data=json.loads((ROOT/'inputs/aa_hessians.json').read_text())['histories']
    nodes,weights=leggauss(n);weights=weights/2
    grid=np.array(np.meshgrid(*([nodes]*5),indexing='ij')).reshape(5,-1)
    weight_grid=np.prod(np.array(np.meshgrid(*([weights]*5),indexing='ij')),axis=0).reshape(-1)
    ref=np.mean([np.array([[float(Fraction(v)) for v in row] for row in r['H0_over_va']]) for r in data],axis=0)
    ar=scalar_from_eigenphases(ref);coupled=0j;decoupled=0j;records=[]
    for r in data:
        code=r['order_code'];rel={(i,j) for i in range(5) for j in range(5) if code&(1<<(5*i+j))}
        k=np.full((3,grid.shape[1]),.5)
        for i,j in sorted(rel):
            layers=sum((i,z) in rel and (z,j) in rel for z in range(5))
            k[j-2]+=(1,-9,16,-8)[layers]/math.sqrt(6)*(grid[j]-grid[i])**2
        e=np.exp(-.5j*k)*np.sinc(k/(2*math.pi))
        integrand=(1+e[0])*(e[1]+e[2]+e[1]*e[2])/(16*math.sqrt(3))
        dust=complex(np.dot(weight_grid,integrand));a=scalar_from_eigenphases(r['H0_over_va'])
        phase=np.exp(1j*r['F4'])/33;coupled+=phase*dust*a;decoupled+=phase*dust*ar
        records.append({'code':code,'dust':[dust.real,dust.imag],'scalar':[a.real,a.imag]})
    return {'n':n,'histories':33,'implementation':'float64 independent full five-dimensional tensor rule; no certified accuracy claim',
            'coupled':[coupled.real,coupled.imag],'decoupled':[decoupled.real,decoupled.imag],'records':records}

if __name__=='__main__':
    result=evaluate()
    (ROOT/'results/independent_5d_n8.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print({k:v for k,v in result.items() if k!='records'})
