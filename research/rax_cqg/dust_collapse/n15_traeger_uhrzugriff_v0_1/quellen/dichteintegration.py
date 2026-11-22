"""Cross-check: sample all fields and the outer density; direct edge sum and binning."""
import json
import numpy as np
from fractions import Fraction as Q
from scipy.stats import qmc
from model import BASE,I,P,F,DELTA,BETA,combined_laws,setup,gram
from evaluate import readout
def run():
    keys,qs=combined_laws()
    chain=json.loads((BASE/'chain.json').read_text())
    change=np.array([float((Q(chain['alternative_same_N13']['law'].get(str(k),0))-Q(chain['law'].get(str(k),0)))/2) for k in keys])
    weights=[qs[0],qs[1],qs[0]+change]
    s=np.load(BASE/'scalars.npz')
    ix=np.searchsorted(s['keys'],keys)
    G=gram(list(zip(s['precision'][ix],s['factor'][ix])))
    out={}
    for seed in (932501,932502):
        pts=qmc.Sobol(16,scramble=True,seed=seed).random_base2(11)
        amps=np.zeros((2,len(keys),6),complex)
        for i,code in enumerate(keys):
            cen,r,eps,f0,A,b=setup(code)
            u=cen+r*(2*pts[:,1:8]-1)
            f=f0+u@A.T
            a,v=np.nonzero(b)
            bv=b[a,v]
            for lobe in (-1,1):
                delta=lobe/16+(pts[:,0]-.5)/16
                D=4*DELTA-delta
                T=np.zeros((len(pts),15))
                T[:,P]=(P-5)*DELTA
                T[:,F]=(F-5)*DELTA
                T[:,3]+=delta
                T[:,I]=T[:,3,None]+D[:,None]*u
                dt=T[:,v]-T[:,a]
                for im,m in enumerate((.25,4.)):
                    goal=m*D[:,None]*f
                    lo=(1-eps)*goal; width=np.maximum(np.minimum(1,(1+eps)*goal)-lo,0.)
                    jac=D**7*np.prod(width*(7/(2*eps*m)),axis=1)
                    W=np.zeros_like(T);W[:,I]=lo+pts[:,8:15]*width
                    W[:,F]=1/8
                    W[:,P]=(.125+(pts[:,15]-.5)/16)[:,None]
                    charge=np.zeros(len(pts));S=-W.sum(axis=1)/2
                    for j,(y,x) in enumerate(zip(a,v)):
                        S-=BETA/4*bv[j]*W[:,x]*dt[:,j]**2
                        if y in P and x not in P: charge-=BETA/2*bv[j]*W[:,x]*dt[:,j]
                    bins=np.searchsorted([-1.,-.25,0.,.25,1.],charge,side='right')
                    terms=jac*np.exp(1j*(15-b.sum()+S))
                    amps[im,i]+=(np.bincount(bins,terms.real,minlength=6)+1j*np.bincount(bins,terms.imag,minlength=6))/(2*len(pts))
        for im,m in enumerate((.25,4.)):
            for name,q in zip(('1:1','1:3','chain_reverse'),weights):
                result=readout(amps[im],G,q)
                out[f'{seed}/{m}/{name}']={'positive_sign_record':result['positive_sign_record'],
                                           'fine_bins':result['bin_probabilities']}
    return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
