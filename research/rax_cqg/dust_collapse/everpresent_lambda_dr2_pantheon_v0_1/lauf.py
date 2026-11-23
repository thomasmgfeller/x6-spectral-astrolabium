"""Everpresent Lambda Model 2. Run python lauf.py --cache /path/to/shared/data."""
import argparse
import csv
import json
import os
from pathlib import Path
import sys
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import numpy as np
import scipy
from numpy.polynomial.legendre import leggauss
from scipy.integrate import cumulative_simpson
from scipy.linalg import solve_triangular
from scipy.special import logsumexp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'pipeline'))
import datenpilot as ref

ALPHA, MU = .8824, .9804
STREAMS, SIZE, MODES = 16, 8192, 18
ANCHOR = np.log(3.33)/2
GRID = np.linspace(0, 2*ANCHOR, 513)
SCALE_MIN, SCALE_MAX = 10., 1000.
GN, GW = leggauss(64)
FIELDS = ['omega_m0','h_rd_Mpc','m_offset','chi2_bao','chi2_sn','log_scale_integral']
BATCH = 128


def basis(x):
    """Square-exponential covariance expansion, using x=log(a)."""
    t = np.sqrt(MU)*(np.asarray(x)+ANCHOR)
    columns = [ALPHA*np.exp(-t*t/2)]
    for k in range(1, MODES):
        columns.append(columns[-1]*t/np.sqrt(k))
    return np.stack(columns,axis=-1)


def log_matter_fraction(g):
    return np.log(2.)-np.logaddexp(0.,2*g)


def inv_e(q, coeff, design=None):
    """q=ln(1+z), coeff has one column per history."""
    g = (basis(-q) if design is None else design) @ coeff
    return np.exp(.5*(log_matter_fraction(g)-log_matter_fraction(basis(0.) @ coeff)-3*q[:,None]))


class Curve:
    def __init__(self, z):
        q = np.log1p(z)
        if np.min(q)<0 or np.max(q)>GRID[-1]+1e-12:
            raise ValueError('Redshift outside the frozen model interval')
        h = GRID[1]
        self.idx = np.minimum(np.floor(q/h).astype(int),len(GRID)-2)
        t = (q-GRID[self.idx])/h
        self.weights = [w[:,None] for w in (1-3*t*t+2*t**3,3*t*t-2*t**3,
                                              h*t*(1-t)**2,h*t*t*(t-1))]
        self.design = basis(-GRID)

    def comoving(self, coeff):
        slope = np.exp(GRID)[:,None]*inv_e(GRID,coeff,self.design)
        curve = cumulative_simpson(slope, dx=GRID[1], axis=0, initial=0)
        a,b,c,d = self.weights
        j = self.idx
        return a*curve[j]+b*curve[j+1]+c*slope[j]+d*slope[j+1]


def bao_shapes(bao, dm, dh):
    return ref.C_OVER_100*np.select([bao.tag[:,None]=='DM_over_rs',bao.tag[:,None]=='DH_over_rs'],
                                     [dm,dh], default=np.cbrt(bao.z[:,None]*dm**2*dh))


def log_scale_area(inv_scale, curvature):
    """Integral of exp[-C/2*(1/s-a_hat)^2] ds/(s_max-s_min)."""
    width=1/np.sqrt(curvature)
    lower=np.maximum(-14.,(1/SCALE_MAX-inv_scale)/width)
    upper=np.minimum(14.,(1/SCALE_MIN-inv_scale)/width)
    if np.any(lower>=upper):
        raise ArithmeticError('Scale peak far outside prior; use a boundary-tail integral')
    t=(lower+upper)[:,None]/2 + (upper-lower)[:,None]*GN/2
    a=inv_scale[:,None]+width[:,None]*t
    integral=np.sum(GW*np.exp(-t**2/2)/a**2,axis=1)*width*(upper-lower)/2/(SCALE_MAX-SCALE_MIN)
    return np.log(integral)


def evaluate(bao, sn, dm, dh, distance_sn, omega):
    y = bao_shapes(bao,dm,dh)
    w = solve_triangular(bao.chol,y,lower=True)
    curvature=np.sum(w*w,axis=0)
    inv_scale=(bao.obs @ w)/curvature
    if np.any((1/inv_scale<SCALE_MIN)|(1/inv_scale>SCALE_MAX)):
        raise ArithmeticError('Unconstrained profile scale outside the frozen prior')
    chi_b=np.sum((bao.obs[:,None]-w*inv_scale)**2,axis=0)
    mag=5*np.log10((1+sn.zhel[:,None])*distance_sn)
    v=solve_triangular(sn.chol,sn.obs[:,None]-mag,lower=True)
    offset=sn.ones @ v/sn.ones_norm2
    chi_s=np.sum((v-sn.ones[:,None]*offset)**2,axis=0)
    return np.stack([omega,1/inv_scale,offset,chi_b,chi_s,log_scale_area(inv_scale,curvature)],axis=1)


def log_like(rows):
    bao=rows[:,5]-rows[:,3]/2
    return np.stack([bao,bao-rows[:,4]/2],axis=1)


def reference(bao,sn,n):
    om,wo=ref.quadrature(ref.OMEGA_BINS,n)
    terms=[]
    for start in range(0,len(om),16):
        sample=om[start:start+16]
        terms.append(evaluate(bao,sn,bao.distance.comoving(sample,0),ref.inv_expansion(bao.z[:,None],sample,0),
                              sn.distance.comoving(sample,0),sample))
    return logsumexp(log_like(np.vstack(terms)),b=(wo/.98)[:,None],axis=0)


def observation_table(path, header, rows):
    with path.open('w',newline='',encoding='utf8') as stream:
        writer=csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def run(cache,out):
    files=ref.inputs(cache)
    bao,sn=ref.BAO(files),ref.Pantheon(files)
    assert len(bao.z)==13 and sn.n==1590
    z=np.r_[bao.z,sn.distance.z]
    curve=Curve(z)
    q=np.log1p(bao.z)
    template=basis(-q)
    baseline=ref.best_fit(bao,sn,True,True)
    archive=json.loads((ROOT/'pipeline/ergebnis.json').read_text())['posteriors']['DESI_DR2_plus_PantheonPlus']['best_fit']
    assert abs(baseline['chi2_min']-archive['chi2_min'])<1e-7
    log_ref=reference(bao,sn,32)
    check_ref=reference(bao,sn,24)
    assert max(abs(log_ref-check_ref))<1e-7
    draws=[]
    for seed in np.random.SeedSequence(20261124).spawn(STREAMS):
        rng=np.random.Generator(np.random.PCG64(seed))
        draws.append(rng.standard_normal((SIZE,MODES)))
    draws=np.vstack(draws)
    blocks=[]
    for i in range(0,len(draws),BATCH):
        coeff=draws[i:i+BATCH].T
        dm=curve.comoving(coeff)
        omega=np.exp(log_matter_fraction(basis(0.) @ coeff))
        blocks.append(evaluate(bao,sn,dm[:13],inv_e(q,coeff,template),dm[13:],omega))
        if (i+BATCH)%SIZE==0:
            print('Stream', (i+BATCH)//SIZE, '/', STREAMS, flush=True)
    rows=np.vstack(blocks)
    out.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(out/'historien.npz', fields=np.array(FIELDS), rows=rows,coefficients=draws)
    delta=rows[:,3]+rows[:,4]-baseline['chi2_min']
    best=int(np.argmin(delta))
    ll=log_like(rows)
    log_e=logsumexp(ll,axis=0)-np.log(len(rows))
    block_e=logsumexp(ll.reshape(STREAMS,SIZE,2),axis=1)-np.log(SIZE)
    stats={}
    for j,name in enumerate(('BAO','BAO_SN')):
        weights=np.exp(ll[:,j]-ll[:,j].max())
        ratio=np.exp(log_e[j]-log_ref[j])
        relative_se=weights.std(ddof=1)/np.sqrt(len(rows))/weights.mean()
        ratios=np.exp(block_e[:,j]-log_ref[j])
        stats[name]=dict(log_Z_model=float(log_e[j]),log_Z_ref=float(log_ref[j]),ratio=float(ratio),
                         MC_se_iid=float(relative_se*ratio),MC_se_blocks=float(ratios.std(ddof=1)/np.sqrt(STREAMS)),
                         ESS=float(weights.sum()**2/(weights@weights)),ratios_by_stream=ratios.tolist())
    ids=[0,best]
    columns=['first','best_draw','flat_lcdm']
    selected=draws[ids].T
    d=curve.comoving(selected)
    om=np.array([baseline['omega_m']])
    dm=np.column_stack((d[:13],bao.distance.comoving(om,0)))
    dh=np.column_stack((inv_e(q,selected),ref.inv_expansion(bao.z[:,None],om,0)))
    ds=np.column_stack((d[13:],sn.distance.comoving(om,0)))
    scale=np.r_[rows[ids,1],baseline['h_rd_Mpc']]
    mb0=5*np.log10((1+sn.zhel[:,None])*ds)
    v=solve_triangular(sn.chol,sn.obs[:,None]-mb0,lower=True)
    offsets=sn.ones @ v/sn.ones_norm2
    assert np.allclose(offsets[:2],rows[ids,2],rtol=0,atol=1e-10)
    predictions=bao_shapes(bao,dm,dh)/scale
    raw_bao=np.loadtxt(files['desi_gaussian_bao_ALL_GCcomb_mean.txt'],usecols=(1,))
    assert np.allclose(raw_bao,bao.chol @ bao.obs)
    observation_table(out/'DESI_vorhersagen.csv',['z','observable','observed',*columns],zip(bao.z,bao.tag,raw_bao,*predictions.T))
    observation_table(out/'Pantheon_vorhersagen.csv',['selected_row_zero_based','zHD','zHEL','observed_m_b_corr',*columns],
                      zip(range(sn.n),sn.distance.z,sn.zhel,sn.obs,*(mb0+offsets).T))
    sz=np.array([0.,.1,.3,.5,1.,1.5,2.33])
    fixed_chi=Curve(sz).comoving(draws[0:1].T)[:,0]
    fixed_e=1/inv_e(np.log1p(sz),draws[0:1].T)[:,0]
    fixed_de=np.tanh(basis(-np.log1p(sz)) @ draws[0])
    observation_table(out/'erste_distanzkurve.csv',['z','Omega_de','H_over_H0','H0_DM_over_c','H0_DL_over_c'],
                      zip(sz,fixed_de,fixed_e,fixed_chi,(1+sz)*fixed_chi))
    outdata=dict(seed=20261124,hyperparameters=dict(alpha=ALPHA,mu=MU),count=len(rows),streams=STREAMS,
                 per_stream=SIZE,software=dict(numpy=np.__version__,scipy=scipy.__version__),observations=dict(DESI=len(bao.z),PantheonPlus=sn.n),
                 flat_lcdm=baseline,reference_logZ_quadrature_maxdiff=float(max(abs(log_ref-check_ref))),ensemble=stats,
                 conditional_SN_given_BAO_relative_predictive_density=float(np.exp((log_e-log_ref)[1]-(log_e-log_ref)[0])),
                 count_delta_chi2_le_0=int(np.sum(delta<=0)),count_delta_chi2_le_4=int(np.sum(delta<=4)),
                 delta_chi2_quantiles=dict(zip(['p05','median','p95'],np.quantile(delta,[.05,.5,.95]).tolist())),
                 selected={key:dict(id=idx,**dict(zip(FIELDS,rows[idx].tolist())),chi2=float(delta[idx]+baseline['chi2_min']),
                                     delta_chi2=float(delta[idx])) for key,idx in zip(columns,ids)})
    (out/'ergebnis.json').write_text(json.dumps(outdata,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in outdata.items() if k not in ('ensemble',)},ensure_ascii=False),flush=True)
    print('Joint evidence ratio',stats['BAO_SN']['ratio'],'ESS',stats['BAO_SN']['ESS'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache',type=Path,default=ROOT/'cache')
    p.add_argument('--out',type=Path,default=ROOT/'resultate')
    args=p.parse_args()
    run(args.cache,args.out)
