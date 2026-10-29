"""Independent Fourier-space sanity check; deliberately NOT an error certificate."""
import json
import time
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre


def evaluate(pmax,np_,nmu,ns):
    pn,pw=roots_legendre(np_);p=(pn+1)*pmax/2;pw=pw*pmax/2
    mu,mw=roots_legendre(nmu);sn,sw=roots_legendre(ns);s=(sn+1)/4;sw=sw/4
    source=4*np.pi*s*s*np.exp(1-1/(1-4*s*s))*sw
    answers=np.zeros(2,complex)
    for start in range(0,len(p),16):
        pp=p[start:start+16];ww=pw[start:start+16]
        q=np.sqrt(pp[:,None]**2+16-8*pp[:,None]*mu)
        fhat=np.sum(np.sinc(q[:,:,None]*s/np.pi)*source,axis=2)
        angular=np.sum(mw*fhat*np.exp(1.5j*pp[:,None]*mu),axis=1)
        x=pp/2;detector=3*(np.sin(x)-x*np.cos(x))/x**3
        omega=np.sqrt(1+pp*pp)
        for j,(lo,hi) in enumerate([(1.75,2),(2,2.25)]):
            timefactor=(np.sin(omega*hi)-np.sin(omega*lo))/(omega*(hi-lo))
            answers[j]+=np.sum(ww*pp**2*detector*timefactor*angular)/(4*np.pi**2)
    return answers


if __name__=='__main__':
    rows=[];started=time.monotonic()
    for params in [(128,512,192,96),(256,1024,384,160)]:
        z=evaluate(*params)
        rows.append({'parameters':params,'values':[[v.real,v.imag] for v in z]})
        print(params,z,flush=True)
    out={'status':'DIAGNOSTIC_ONLY_NO_CERTIFIED_FOURIER_CUTOFF','rows':rows,'elapsed_seconds':time.monotonic()-started}
    (Path(__file__).parent/'results/FOURIER_DIAGNOSTIC.json').write_text(json.dumps(out,indent=2)+'\n')
