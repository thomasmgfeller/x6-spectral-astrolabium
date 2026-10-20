"""Frozen scalar analysis: calibration fitting and held-out evaluation are separate."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.stats import beta
HERE=Path(__file__).resolve().parent


def read_split(name):
    folder=HERE/('independent_'+name);execution=json.loads((folder/'execution.json').read_text())
    rows=[]
    for entry in execution['records']:
        raw=(folder/entry['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==entry['sha256']
        rows.append(json.loads(raw))
    good=[r for r in rows if r['operator']['status']=='COMPLETE']
    return execution,rows,good


def simplex(cov):
    r=minimize(lambda w:w@cov@w,np.ones(3)/3,jac=lambda w:2*cov@w,method='SLSQP',
               bounds=[(0,1)]*3,constraints=[dict(type='eq',fun=lambda w:w.sum()-1,jac=lambda w:np.ones(3))],
               options=dict(ftol=1e-12,maxiter=2000))
    w=r.x;gradient=2*cov@w
    gap=float(gradient@w-gradient.min())
    if not r.success or w.min()<-1e-10 or abs(w.sum()-1)>1e-10 or gap>1e-7*(1+abs(r.fun)):
        raise ValueError('simplex certificate failed')
    return w.tolist()


def fit(c):
    e,rows,good=read_split('calibration')
    out=dict(status='HOLD',complete=len(good),total=len(rows),execution_complete=e['status']=='COMPLETE')
    if e['status']=='COMPLETE' and len(good)>=c['minimum_calibration_complete']:
        errors=np.array([r['operator']['observed'] for r in good])+.75
        bias=errors.mean(axis=0);cov=np.cov(errors,rowvar=False);condition=float(np.linalg.cond(cov))
        if np.linalg.eigvalsh(cov).min()>0 and condition<=c['maximum_covariance_condition']:
            out.update(status='FROZEN',bias=bias.tolist(),joint_covariance=cov.tolist(),
                       covariance_condition=condition,joint_weights=simplex(cov),
                       naive_weights=simplex(np.diag(np.diag(cov))),
                       best_single=int(np.argmin(np.diag(cov))))
    (HERE/'frozen_calibration.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


def analyze(c):
    raw=(HERE/'frozen_calibration.json').read_bytes();cal=json.loads(raw)
    execution,rows,good=read_split('test')
    out=dict(decision='CALIBRATION_HOLD',scope='Offline scalar diagnostic only; HOLD_PHASE3',
             calibration_sha256=hashlib.sha256(raw).hexdigest(),total=len(rows),complete=len(good),arms={})
    if cal['status']!='FROZEN' or not good:
        (HERE/'independent_summary.json').write_text(json.dumps(out,indent=2)+'\n');return
    error=np.array([r['operator']['observed'] for r in good])+.75
    clean=np.array([r['operator']['clean'] for r in good])+.75
    corrected=error-np.array(cal['bias']);cov=np.array(cal['joint_covariance'])*(1+1/cal['complete'])
    prior=np.array([np.random.default_rng(np.random.SeedSequence([r['seed'],912343])).normal(scale=c['prior_sigma']) for r in good])
    single=np.eye(3)[cal['best_single']];post_errors={}
    for name,w,assumed in [('single',single,cov),('joint',cal['joint_weights'],cov),
                           ('naive_diagonal',cal['naive_weights'],np.diag(np.diag(cov)))]:
        w=np.array(w);v=float(w@assumed@w);measurement=corrected@w
        p=c['prior_sigma']**2;k=p/(p+v);pv=p*v/(p+v);post=prior+k*(measurement-prior)
        hits=int(np.sum(np.abs(post)<=1.95996398454*np.sqrt(pv)));n=len(post)
        ci=[float(beta.ppf(.025,hits,n-hits+1)) if hits else 0.,float(beta.ppf(.975,hits+1,n-hits)) if hits<n else 1.]
        out['arms'][name]=dict(measurement_rmse=float(np.sqrt(np.mean(measurement**2))),
            measurement_bias=float(measurement.mean()),reported_measurement_variance=v,
            posterior_rmse=float(np.sqrt(np.mean(post**2))),coverage=hits/n,coverage_exact_95=ci,
            gain=k,mean_nees=float(np.mean(post**2)/pv),mean_nis=float(np.mean((measurement-prior)**2)/(p+v)),
            weights=w.tolist())
        post_errors[name]=post
    out['raw_rmse_by_arm']=np.sqrt(np.mean(error**2,axis=0)).tolist()
    out['clean_rmse_by_arm']=np.sqrt(np.mean(clean**2,axis=0)).tolist()
    out['test_raw_bias']=error.mean(axis=0).tolist()
    out['test_error_covariance']=np.cov(error,rowvar=False).tolist()
    out['mean_conditional_field_covariance']=np.mean([r['operator']['conditional_field_covariance'] for r in good],axis=0).tolist()
    out['calibration_correlation']=(np.array(cal['joint_covariance'])/np.sqrt(np.outer(np.diag(cal['joint_covariance']),np.diag(cal['joint_covariance'])))).tolist()
    rng=np.random.default_rng(70030000);index=rng.integers(0,len(good),size=(5000,len(good)))
    ratio=np.sqrt(np.mean(post_errors['joint'][index]**2,axis=1)/np.mean(post_errors['single'][index]**2,axis=1))
    observed=out['arms']['joint']['posterior_rmse']/out['arms']['single']['posterior_rmse']
    out['paired_rmse_ratio']=observed;out['paired_bootstrap_95']=np.quantile(ratio,[.025,.975]).tolist()
    out['signed_qp_verified']=sum(r['operator'].get('signed_qp',{}).get('status')=='VERIFIED' for r in good if r['operator'].get('signed_qp'))
    gates=dict(execution_complete=execution['status']=='COMPLETE',availability=len(good)>=c['minimum_test_complete'],
               rmse_improvement=observed<=c['required_rmse_ratio'],coverage=out['arms']['joint']['coverage']>=c['minimum_test_coverage'])
    out['gates']=gates
    if all(gates.values()):out['decision']='PILOT_SUPPORTED'
    (HERE/'independent_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['fit','test']);args=p.parse_args()
    c=json.loads((HERE/'calibration_contract.json').read_text())
    fit(c) if args.mode=='fit' else analyze(c)
