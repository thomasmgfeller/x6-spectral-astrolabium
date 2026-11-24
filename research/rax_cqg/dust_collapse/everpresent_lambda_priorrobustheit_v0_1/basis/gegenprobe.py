"""Direct redshift quadrature, generalized least squares and AP predictions."""
import argparse
import json
from math import factorial
import os
from pathlib import Path
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from numpy.polynomial.legendre import leggauss
from numpy.polynomial.polynomial import polyval
from scipy.integrate import quad
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize_scalar
import lauf

ROOT=Path(__file__).resolve().parent
A,M=.8824,.9804
NODES,WEIGHTS=leggauss(48)
FACTOR=np.sqrt([float(factorial(j)) for j in range(18)])


def matter(z,coeff):
    t=np.sqrt(M)*(np.log(3.33)/2-np.log1p(z))
    g=A*np.exp(-t*t/2)*polyval(t,coeff/FACTOR)
    return 1-np.tanh(g)


def distances(z,c):
    def dh(zz):
        return np.sqrt(matter(zz,c)/matter(0.,c)/(1+zz)**3)
    integrand=dh(z[:,None]*(NODES+1)/2)
    return z*(integrand@WEIGHTS)/2,dh(z)


def ap_distributions(index_z, c):
    # Independent redshift quadrature at all six anisotropic BAO redshifts.
    def build(z):
        t=np.sqrt(M)*(np.log(3.33)/2-np.log1p(z))
        return A*np.exp(-t[:,None]**2/2)*t[:,None]**np.arange(18)/FACTOR
    nodes=(index_z[:,None]*(NODES+1)/2).ravel()
    all_z=np.r_[0.,index_z,nodes]
    b=build(all_z)
    pieces=[]
    for start in range(0,len(c),256):
        phi=b @ c[start:start+256].T
        m=1-np.tanh(phi)
        inv=np.sqrt(m/m[:1])/(1+all_z[:,None])**1.5
        radial=inv[1:1+len(index_z)]
        integral=(index_z/2)[:,None]*np.einsum('zqn,q->zn',inv[1+len(index_z):].reshape(len(index_z),48,-1),WEIGHTS)
        pieces.append(integral/radial)
    return np.hstack(pieces)


def main(cache,out):
    files=lauf.ref.inputs(cache)
    ref=json.loads((out/'ergebnis.json').read_text())
    with np.load(out/'historien.npz') as data:
        rows=data['rows']
        draws=data['coefficients']
    ids=[0,1,ref['selected']['best_draw']['id']]
    bao=np.loadtxt(files['desi_gaussian_bao_ALL_GCcomb_mean.txt'],dtype=str,skiprows=1)
    zb=bao[:,0].astype(float)
    obs=bao[:,1].astype(float)
    covb=np.loadtxt(files['desi_gaussian_bao_ALL_GCcomb_cov.txt'])
    cb=cho_factor(covb,lower=False)
    table=np.genfromtxt(files['Pantheon+SH0ES.dat'],names=True,dtype=None,encoding='utf8')
    mask=table['zHD']>.01
    z=table['zHD'][mask]
    zhel=table['zHEL'][mask]
    mobs=table['m_b_corr'][mask]
    full=np.loadtxt(files['Pantheon+SH0ES_STAT+SYS.cov'],skiprows=1).reshape(len(table),-1)
    cs=cho_factor(full[np.ix_(mask,mask)],lower=False)
    duration=len(z)
    ci_one=cho_solve(cs,np.ones(duration))
    outrows=[]
    for idx in ids:
        c=draws[idx]
        dm,dh=distances(zb,c)
        geometric=np.where(bao[:,2]=='DM_over_rs',dm,np.where(bao[:,2]=='DH_over_rs',dh,(zb*dm**2*dh)**(1/3)))
        y=2997.92458*geometric
        def quadratic(s):
            r=obs-y/s
            return r @ cho_solve(cb,r)
        opt=minimize_scalar(quadratic,bounds=(10,1000),method='bounded',options={'xatol':1e-10})
        assert opt.success
        chi_b=opt.fun
        s=opt.x
        spread=s*s/np.sqrt(y@cho_solve(cb,y))
        points=np.unique(np.clip(s+spread*np.array([-16,-8,-4,0,4,8,16]),10,1000))
        area=quad(lambda h: np.exp((chi_b-quadratic(h))/2),10.,1000.,points=points,epsabs=2e-12)[0]/990.
        ds,_=distances(z,c)
        r=mobs-5*np.log10((1+zhel)*ds)
        offset=(ci_one@r)/sum(ci_one)
        rr=r-offset
        chi_s=rr @ cho_solve(cs,rr)
        a=rows[idx]
        dchi=abs(chi_b-a[3])+abs(chi_s-a[4])
        assert dchi<2e-5 and abs(s-a[1])<5e-6 and abs(np.log(area)-a[5])<3e-7
        outrows.append(dict(id=idx,profile_chi2_abs_difference=float(dchi),h_rd_abs_difference=float(abs(s-a[1])),
                            scale_log_integral_abs_difference=float(abs(np.log(area)-a[5]))))
    # Directly integrate the reference-scale likelihood on the original pipeline's tensor grid.
    bmodel=lauf.ref.BAO(files)
    smodel=lauf.ref.Pantheon(files)
    om,wo=lauf.ref.quadrature(lauf.ref.OMEGA_BINS,32)
    scale,ws=lauf.ref.quadrature(lauf.ref.SCALE_BINS,40)
    bc,inv,curv=bmodel.profile(om,0.)
    sc=np.concatenate([smodel.profile(om[i:i+16],0.) for i in range(0,len(om),16)])
    from scipy.special import logsumexp
    base=bc[:,None]+curv[:,None]*(1/scale[None,:]-inv[:,None])**2
    log_measure=np.log(wo[:,None]*ws[None,:]/(.98*990.))
    zref=logsumexp(-.5*(base+sc[:,None])+log_measure)
    err=abs(zref-ref['ensemble']['BAO_SN']['log_Z_ref'])
    assert err<1e-8
    u=np.sqrt(M)*np.log(3.33)/2
    var_bound=A*A*u**36/factorial(18)/(1-u*u/19)
    dd={k:ref['ensemble'][k]['ratio'] for k in ('BAO','BAO_SN')}
    res=dict(checked_histories=outrows,reference_logZ_abs_diff_direct_tensor=float(err),
             max_truncated_gp_pointwise_RMS_upper=float(np.sqrt(var_bound)),
             conditional_predictive_ratio=dd['BAO_SN']/dd['BAO'])
    (out/'kontrollen.json').write_text(json.dumps(res,indent=2)+'\n')
    rz=np.unique(zb[bao[:,2]=='DM_over_rs'])
    ap=ap_distributions(rz,draws)
    q16,med,q84=np.quantile(ap,[.16,.5,.84],axis=1)
    dx=[]
    for j,v in enumerate(rz):
        i=int(np.flatnonzero((zb==v)&(bao[:,2]=='DM_over_rs'))[0])
        k=int(np.flatnonzero((zb==v)&(bao[:,2]=='DH_over_rs'))[0])
        measured=obs[i]/obs[k]
        grad=np.array([1/obs[k],-obs[i]/obs[k]**2])
        sigma=float(np.sqrt(grad @ covb[np.ix_([i,k],[i,k])] @ grad))
        matter0=ref['flat_lcdm']['omega_m']
        inv=lambda zz:(matter0*(1+zz)**3+1-matter0)**-.5
        lcdm=quad(inv,0.,v)[0]/inv(v)
        dx.append([v,measured,sigma,ap[j,0],q16[j],med[j],q84[j],ap[j,ids[-1]],lcdm])
    lauf.observation_table(out/'DESI_skalenfrei.csv',['z','AP_observed','sigma_linearized','first','prior_p16','prior_p50','prior_p84','best_draw','flat_lcdm'],dx)
    print(json.dumps(res,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache',type=Path,default=ROOT/'cache')
    p.add_argument('--out',type=Path,default=ROOT/'resultate')
    a=p.parse_args()
    main(a.cache,a.out)
