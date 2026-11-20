"""Charge-resolved coherent dust amplitudes. Requires NumPy and SciPy."""
import argparse
from pathlib import Path
import numpy as np
from scipy.stats import qmc
from model import BASE,I,P,F,DELTA,BETA,setup,support,laws

MASSES=(.25,1.,4.)
RHOS=(.125,.25)
CUTS=(-np.inf,-1.,-.25,0.,.25,1.,np.inf)
SEEDS=(33501,33502,33503,33504)
def cloud(power,seed):
    return qmc.Sobol(15,scramble=True,seed=seed).random_base2(power)

def amplitudes(code, params, points, sizes):
    center,r,eps,f0,A,b=params
    u=center+(2*points[:,1:8]-1)*r
    frac=f0+u@A.T
    assert np.all(frac>0) and np.max(abs(frac.sum(axis=1)-1))<1e-12
    # First label with no internal past always exists; select a true minimal event.
    rel=support.geometry(code)[1]
    axis=next(j for j,v in enumerate(I) if not any((u0,v) in rel for u0 in I))
    out=np.zeros((len(sizes),3,2,6),complex)
    unsplit=np.zeros((len(sizes),3,2),complex)
    matched=np.zeros((len(sizes),2),complex)
    for offset in [-1/16,1/16]:
        delta=offset+(points[:,0]-.5)/16
        D=4*DELTA-delta
        e=delta/DELTA
        Y=np.zeros((len(points),15))
        Y[:,P]=P-5
        Y[:,3]+=e
        Y[:,F]=F-5
        Y[:,I]=-2+e[:,None]+(4-e[:,None])*u
        C=1+((Y**2)@b-2*Y*(Y@b)+Y**2*b.sum(axis=0))/19
        coeff=(Y[:,P]@b[P][:,I]-Y[:,I]*b[P][:,I].sum(axis=0))/(19*DELTA)
        base=15-b.sum()-C[:,F].sum(axis=1)/16
        L=C[:,P].sum(axis=1)/2
        outer=np.exp(1j*(base[:,None]-L[:,None]*np.array(RHOS)))*np.sinc(L[:,None]/(32*np.pi))
        for it,n in enumerate(sizes):
            # Matched empty inner: all seven zero atoms, keep original box clocks.
            # A common constant from the clock widths and atom weights is factored out.
            matched[it]+=np.mean(outer[:n]*D[:n,None]**7,axis=0)/2
        for m_idx,m in enumerate(MASSES):
            star=m*D[:,None]*frac
            lo=(1-eps)*star; hi=np.minimum(1.,(1+eps)*star)
            widths=np.maximum(0.,hi-lo)
            mid=lo+widths/2
            W=lo+widths*points[:,8:]
            W[:,axis]=mid[:,axis]
            p=(W*coeff).sum(axis=1)
            slope=coeff[:,axis]*widths[:,axis]/2
            k=-C[:,I[axis]]*widths[:,axis]/4
            jac=D**7*np.prod(widths*(7/(2*eps*m)),axis=1)
            val=np.exp(-.5j*np.sum(W*C[:,I],axis=1))[:,None]*outer*jac[:,None]
            assert np.all(slope[jac>0]!=0)
            slope_safe=np.where(slope==0,1.,slope)
            boundaries=[np.where(slope_safe>0,-1.,1.)]
            for cut in CUTS[1:-1]: boundaries.append(np.clip((cut-p)/slope_safe,-1,1))
            boundaries.append(-boundaries[0])
            for j,(a,c) in enumerate(zip(boundaries,boundaries[1:])):
                wid=np.abs(c-a)/2
                h=wid*np.exp(.5j*k*(c+a))*np.sinc(k*wid/np.pi)
                v=val*h[:,None]
                for it,n in enumerate(sizes): out[it,m_idx,:,j]+=v[:n].mean(axis=0)/2
            for it,n in enumerate(sizes):
                unsplit[it,m_idx]+=(val[:n]*np.sinc(k[:n,None]/np.pi)).mean(axis=0)/2
    assert np.max(abs(unsplit-out.sum(axis=-1)))<2e-12
    return out,matched

def run(power, dst, all_types, seeds, combined=False):
    import json
    if all_types:
        ranks=json.loads((BASE/'inputs/four/catalog.json').read_text())['ranks_pure_free_mixed']
        keys=sorted(int(k) for k,(a,_,b) in ranks.items() if a==b==0)
    elif combined:
        from model import combined_laws
        keys,_=combined_laws()
    else: keys,_=laws()
    sizes=[2**(power-2),2**power]
    samples=[cloud(power,seed) for seed in seeds]
    arr=np.empty((len(seeds),2,3,2,len(keys),6),complex)
    empty=np.empty((len(seeds),2,2,len(keys)),complex)
    for i,code in enumerate(keys):
        params=setup(code)
        for j,points in enumerate(samples):
            arr[j,:,:,:,i,:],empty[j,:,:,i]=amplitudes(code,params,points,sizes)
    np.savez_compressed(dst,keys=keys,seeds=seeds,sizes=sizes,amp=arr,empty=empty)
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--power',type=int,default=10)
    parser.add_argument('--output',required=True)
    parser.add_argument('--all',action='store_true')
    parser.add_argument('--combined',action='store_true')
    args=parser.parse_args()
    run(args.power,args.output,args.all,SEEDS,args.combined)
