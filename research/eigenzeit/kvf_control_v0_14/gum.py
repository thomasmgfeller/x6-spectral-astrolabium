"""Multivariate GUM evaluation of a SYNTHETIC correlation readout.

Type A: covariance of paired second-moment means. Type B: three shared
rectangular noise-calibration quantities. GUM 102 first-order propagation
is compared with propagation of an explicitly assigned joint input PDF.
"""
import numpy as np
from scipy.stats import chi2, beta

HALFWIDTHS=np.array([.002,.002,.001])
NOISE_MEANS=np.array([.05,.05,0.])
PDF_RADIUS=8.
MC_TRAIN=1_000_000
MC_REGION=1_000_000
MC_VALIDATE=100_000


def correct_and_normalize(x):
    x=np.asarray(x,dtype=float)
    a=x[...,0:9:3]-x[...,9,None]
    b=x[...,1:9:3]-x[...,10,None]
    c=x[...,2:9:3]-x[...,11,None]
    if np.any(a<=0) or np.any(b<=0) or np.any(c*c>=a*b):
        raise ValueError('HOLD_INPUT_DOMAIN')
    return c/np.sqrt(a*b)


def jacobian(x):
    r=correct_and_normalize(x)
    J=np.zeros((3,12))
    for i in range(3):
        a,b,c=x[3*i:3*i+3]-x[9:12]
        J[i,3*i:3*i+3]=[-r[i]/(2*a),-r[i]/(2*b),1/np.sqrt(a*b)]
        J[i,9:12]=-J[i,3*i:3*i+3]
    return J


def make_inputs(arrays):
    means=[]; ua=np.zeros((9,9)); counts=[]
    for i,xy in enumerate(arrays):
        if xy.ndim!=2 or xy.shape[1]!=2 or len(xy)<20 or not np.all(np.isfinite(xy)):
            raise ValueError('HOLD_RAW_INPUT')
        z=np.column_stack([xy[:,0]**2,xy[:,1]**2,xy[:,0]*xy[:,1]])
        means.extend(z.mean(axis=0));counts.append(len(xy))
        ua[3*i:3*i+3,3*i:3*i+3]=np.cov(z,rowvar=False,ddof=1)/len(z)
    x=np.r_[means,NOISE_MEANS]
    ux=np.zeros((12,12));ux[:9,:9]=ua;ux[9:,9:]=np.diag(HALFWIDTHS**2/3)
    return x,ux,counts


def pdf_spec(x,ux):
    d=9
    # A radially truncated N(0,Sigma) has covariance kappa*Sigma.
    # Choosing Sigma=UA/kappa retains exactly the assigned Type-A covariance.
    kappa=chi2.cdf(PDF_RADIUS**2,d+2)/chi2.cdf(PDF_RADIUS**2,d)
    sigma=ux[:9,:9]/kappa
    dev=PDF_RADIUS*np.sqrt(np.diag(sigma))
    lo=x[:9]-dev;hi=x[:9]+dev
    for i in range(3):
        amin=lo[3*i]-(x[9]+HALFWIDTHS[0])
        bmin=lo[3*i+1]-(x[10]+HALFWIDTHS[1])
        cmax=max(abs(lo[3*i+2]-(x[11]+HALFWIDTHS[2])),abs(hi[3*i+2]-(x[11]-HALFWIDTHS[2])))
        if min(amin,bmin)<=0 or cmax*cmax>=amin*bmin:
            raise ValueError('HOLD_PDF_SUPPORT')
    return sigma,float(kappa)


def draws(x,ux,n,seed):
    sigma,_=pdf_spec(x,ux)
    chol=np.linalg.cholesky(sigma)
    rng=np.random.default_rng(seed)
    out=[];remaining=n;rejected=0
    while remaining:
        size=min(100_000,remaining)
        z=rng.standard_normal((size,9))
        keep=np.sum(z*z,axis=1)<=PDF_RADIUS**2
        rejected+=int(np.count_nonzero(~keep));z=z[keep]
        xx=np.empty((len(z),12));xx[:,:9]=x[:9]+z@chol.T
        xx[:,9:]=x[9:]+rng.uniform(-1,1,(len(z),3))*HALFWIDTHS
        out.append(correct_and_normalize(xx));remaining-=len(z)
    return np.concatenate(out),rejected


def interval(successes,total,alpha=.01):
    return [0. if successes==0 else float(beta.ppf(alpha/2,successes,total-successes+1)),
            1. if successes==total else float(beta.ppf(1-alpha/2,successes+1,total-successes))]


def evaluate(arrays,seeds,mode='SYNTHETIC'):
    if mode!='SYNTHETIC':
        return {'status':'HOLD_FIELD_TRANSFER','physical_release':False}
    x,ux,counts=make_inputs(arrays)
    v=correct_and_normalize(x);J=jacobian(x)
    uv=J@ux@J.T
    # Linear corrected second moments, in declared synthetic readout units.
    L=np.zeros((9,12));L[:,:9]=np.eye(9)
    for i in range(3):L[3*i:3*i+3,9:12]=-np.eye(3)
    h=L@x;uh=L@ux@L.T
    sigma,kappa=pdf_spec(x,ux)
    sample,reject1=draws(x,ux,MC_TRAIN,seeds[0])
    mean=sample.mean(axis=0);cov=np.cov(sample,rowvar=False)
    inverse=np.linalg.inv(cov)
    blocks=sample.reshape(10,-1,3).mean(axis=1)
    sem=blocks.std(axis=0,ddof=1)/np.sqrt(10)
    region,reject2=draws(x,ux,MC_REGION,seeds[1])
    z=region-mean
    q=np.einsum('ij,jk,ik->i',z,inverse,z)
    radius=float(np.quantile(q,.95,method='higher'))
    # Report sampling variability of the radius as an order-statistic bracket.
    from scipy.stats import binom
    qsorted=np.sort(q)
    index_lo=int(binom.ppf(.005,MC_REGION,.95))
    index_hi=int(binom.ppf(.995,MC_REGION,.95))+1
    radius_ci=[float(qsorted[max(0,index_lo-1)]),float(qsorted[min(MC_REGION-1,index_hi-1)])]
    check,reject3=draws(x,ux,MC_VALIDATE,seeds[2])
    z=check-mean
    qcheck=np.einsum('ij,jk,ik->i',z,inverse,z)
    inside=int(np.count_nonzero(qcheck<=radius))
    ci=interval(inside,MC_VALIDATE)
    return {'status':'SYNTHETIC_GUM_EVALUATION','physical_release':False,
            'pairs_per_setting':counts,'input_estimate':x.tolist(),'input_covariance':ux.tolist(),
            'corrected_second_moments':h.tolist(),'corrected_second_moment_covariance':uh.tolist(),
            'coherence_estimate_first_order':v.tolist(),'jacobian':J.tolist(),
            'coherence_covariance_first_order':uv.tolist(),
            'coherence_standard_uncertainty_first_order':np.sqrt(np.diag(uv)).tolist(),
            'assigned_type_A_pdf':'ellipsoid-truncated multivariate Gaussian, centered at observed second moments; a modelling approximation, not the exact sampling law',
            'type_A_pdf_radius':PDF_RADIUS,'type_A_pdf_kappa':kappa,
            'type_A_base_Gaussian_tail_removed':float(chi2.sf(PDF_RADIUS**2,9)),
            'assigned_type_B_pdf':'independent rectangular quantities, each shared across all three settings',
            'mc_seeds':seeds,'mc_trials':[MC_TRAIN,MC_REGION,MC_VALIDATE],
            'rejection_counts':[reject1,reject2,reject3],
            'mc_mean':mean.tolist(),'mc_covariance':cov.tolist(),
            'mc_standard_uncertainty':np.sqrt(np.diag(cov)).tolist(),
            'mc_mean_numerical_sem':sem.tolist(),
            'mc_minus_first_order_mean':(mean-v).tolist(),
            'relative_mc_standard_uncertainty_change':(np.sqrt(np.diag(cov)/np.diag(uv))-1).tolist(),
            'joint_region':{'dimension':3,'shape':'(rho-mean)^T inverse(covariance) (rho-mean) <= radius_squared',
                            'target_assigned_pdf_probability':.95,'radius_squared':radius,
                            'radius_squared_order_statistic_99pct_interval':radius_ci,
                            'validation_inside':inside,'validation_draws':MC_VALIDATE,
                            'validation_probability_99pct_interval':ci,
                            'validation_interval_contains_target':ci[0]<=.95<=ci[1],
                            'scope':'assigned input PDF; no claim of repeated-sampling coverage for physical data'},
            'mc_policy':'fixed budgets under JCGM 102 7.1.7 and 7.2.1; numerical precision diagnostics reported; not an implementation of adaptive clause 7.8',
            'Delta_AB_measured':False}
