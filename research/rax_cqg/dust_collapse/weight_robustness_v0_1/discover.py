"""Optional candidate discovery. It is never used by the verifier.

Usage: python discover.py --output /absolute/path/to/empty/candidate-directory
The verified rational candidates in inputs/ are not overwritten.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize,root
from flint import ctx
import compute as c


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    dest=args.output.resolve()
    if dest==c.ROOT/'inputs':raise ValueError('do not overwrite certificate inputs')
    dest.mkdir(parents=True,exist_ok=True);ctx.prec=192
    os,ref,r,rn=c.orbit_data(c.read('inputs/quadrature.json'))
    for key in ('full6','positive'):
        blocks=[c.choose(o,key,rn) for o in os]
        a=np.array([[[complex(b[i,j]) for j in range(2)] for i in range(b.nrows())] for b in blocks])
        def fg(w,all_data=False):
            block=np.einsum('k,kij->ij',w,a);u,s,vh=np.linalg.svd(block,full_matrices=False)
            y=np.outer(u[:,0],vh[0]);g=np.real(np.einsum('ij,kij->k',y.conj(),a))
            return (s[0],g,u[:,0],vh[0].conj()) if all_data else (s[0],g)
        run=minimize(lambda w:fg(w)[0]*1000,np.ones(10)/10,jac=lambda w:fg(w)[1]*1000,
            bounds=[(0,1)]*10,constraints=[{'type':'eq','fun':lambda w:sum(w)-1,'jac':lambda w:np.ones(10)}],
            method='SLSQP',options={'ftol':1e-14,'maxiter':3000})
        support=np.flatnonzero(run.x>1e-7)
        def residual(x,all_data=False):
            w=np.zeros(10);w[support[:-1]]=x;w[support[-1]]=1-sum(x)
            f,g,u,v=fg(w,True)
            return (w,f,g,u,v) if all_data else (g[support[:-1]]-g[support[-1]])*1000
        polish=root(residual,run.x[support[:-1]],tol=1e-11)
        w,f,g,u,v=residual(polish.x,True)
        den=10**16;ns=[0]*10
        for k in support[:-1]:ns[k]=int(round(w[k]*den))
        ns[support[-1]]=den-sum(ns)
        if any(n<0 for n in ns):raise ArithmeticError('candidate is not feasible')
        pack=lambda vec:[{'real':format(z.real,'.17g'),'imag':format(z.imag,'.17g')} for z in vec]
        output={'support':support.tolist(),'weight_denominator':den,'weight_numerators':ns,
                'left_vector':pack(u),'right_vector':pack(v),
                'discovery':{'solver':'SciPy SLSQP plus active-face root; diagnostic only',
                             'objective':f,'candidate_gap':f-min(g),'success':[bool(run.success),bool(polish.success)]}}
        (dest/(key+'_candidate.json')).write_text(json.dumps(output,indent=2)+'\n')
        print(key,output['discovery'])

if __name__=='__main__':main()
