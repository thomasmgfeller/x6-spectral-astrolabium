"""Replay sealed early forecasts, then independently propagate all ten states."""
from pathlib import Path
import csv
import hashlib
import json
import platform
import time
import numpy as np
import scipy
from scipy.fft import dst,idst
from scipy.integrate import quad
from scipy.special import ndtr
from forecast import seal
from states import early_moments,image_state,full
from propagate import evolution

ROOT=Path(__file__).resolve().parent


def require(condition,message):
    if not condition:raise ValueError(message)


def spectral_check(case,forecast,L,n=8192):
    dx=L/(n+1);q=dx*np.arange(1,n+1);k=np.pi*np.arange(1,n+1)/L
    psi=image_state(q,case)/np.sqrt(forecast['norm_raw'])
    coeff=dst(psi,type=1,norm='ortho');rows=[]
    for t in (0.,forecast['T_b']/2,forecast['T_b'],1.5*forecast['T_b'],6.):
        evolved=idst(coeff*np.exp(1j*case['hbar']*k*k*t),type=1,norm='ortho')
        numeric=float(dx*np.dot(q*q,abs(evolved)**2))
        prediction=forecast['A']-2*forecast['J']*t+4*forecast['E']*t*t
        rows.append({'T':t,'V_numeric':numeric,'V_prediction':prediction,'abs_error':abs(numeric-prediction)})
    return rows


def controls(cases,forecasts):
    boundaries=[];slopes=[]
    for case in cases[:8]:
        f=forecasts[case['id']];t=f['T_b']
        slope=image_state(0.,case,t,derivative=True)/np.sqrt(f['norm_raw'])
        require(abs(slope)>0.,'Gaussian boundary coefficient vanished numerically')
        slopes.append({'case':case['id'],'T':t,'slope_squared':float(abs(slope)**2),
                       'inverse_V_squared':'DIVERGENT_BY_NONZERO_LINEAR_BOUNDARY_TERM'})
    for case in (cases[0],cases[7]):
        d=forecasts[case['id']];n=early_moments(case,'N')
        t=d['T_b'];neumann_wall=abs(image_state(0.,case,t,bc='N'))**2/n['norm_raw']
        neumann_checks=[]
        for tt in (.5*t,t,1.5*t):
            observed=quad(lambda q:float(q*q*abs(image_state(q,case,tt,bc='N'))**2/n['norm_raw']),
                          0,32,epsabs=1e-10,epsrel=1e-10,limit=600)[0]
            predicted=n['A']-2*n['J']*tt+4*n['E']*tt*tt
            neumann_checks.append({'T':tt,'V_quadrature':observed,'V_prediction':predicted,'abs_error':abs(observed-predicted)})
        boundaries.append({'case':case['id'],'D_T_b':d['T_b'],'N_T_b':n['T_b'],
                           'D_V_b':d['V_b'],'N_V_b':n['V_b'],
                           'neumann_wall_density':float(neumann_wall),
                           'neumann_late_checks':neumann_checks,
                           'neumann_inverse_V':'DIVERGENT_BY_NONZERO_WALL_VALUE'})
    case=cases[0];f=forecasts[case['id']];c=case['components'][0]
    q0,p,h,s=c['q'],c['p'],case['hbar'],case['sigma']
    t=q0/p # twice the classical arrival time; follows only from initial data.
    mean=q0-2*p*t;variance=s*s+(h*t/s)**2
    transparent={'case':case['id'],'T':t,'signed_q_mean':mean,'V_mean':mean*mean+variance,
                 'probability_q_positive':float(ndtr(mean/np.sqrt(variance))),
                 'T_b':q0*p/(2*(p*p+h*h/(4*s*s))),
                 'V_b':q0*q0+s*s-(q0*p)**2/(p*p+h*h/(4*s*s)),
                 'physical_status':'DIAGNOSTIC_ONLY_NEGATIVE_Q_OUTSIDE_PHYSICAL_HALF_LINE'}
    # Cutoff inverse moment at the forecast bounce, not at a fitted late time.
    t=f['T_b'];slope2=slopes[0]['slope_squared'];cutoffs=[]
    def density(q):return float(abs(image_state(q,case,t))**2/f['norm_raw'])
    for power in range(6,13):
        eps=2.**(-power)
        value=quad(lambda q:density(q)/q**4,eps,.5,epsabs=1e-9,epsrel=1e-10,limit=500)[0]
        value+=quad(lambda q:density(q)/q**4,.5,32,epsabs=1e-9,epsrel=1e-10,limit=500)[0]
        cutoffs.append({'epsilon':eps,'inverse_second_cutoff':value,'scaled':eps*value,'slope_squared':slope2})
    return {'boundary_comparison':boundaries,'gaussian_wall_slopes':slopes,
            'transparent_line':transparent,'cutoffs':cutoffs}


def run():
    start=time.monotonic();plan=seal()
    provenance=json.loads((ROOT/'provenance.json').read_text())
    for name,row in provenance['inputs'].items():
        require(hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==row['sha256'],'Input '+name)
    fp=ROOT/'forecast.json';require(hashlib.sha256(fp.read_bytes()).hexdigest()==(ROOT/'FORECAST_SHA256').read_text().split()[0],'Forecast changed')
    frozen=json.loads(fp.read_text());forecasts=frozen['cases']
    require(not frozen['uses_late_evolution'],'Forecast leakage')
    rows=[];traces=[];spectral=[]
    for case in plan['cases']:
        cid=case['id'];fresh=early_moments(case);target=forecasts[cid]
        for key in ('A','J','E','T_b','V_b','norm_raw'):
            require(np.isclose(fresh[key],target[key],rtol=1e-11,atol=1e-11),'Early forecast replay '+cid)
        check=spectral_check(case,target,plan['reference']['domain_L'])
        require(max(x['abs_error'] for x in check)<plan['acceptance']['spectral_crosscheck_absolute_V'],'Spectral control '+cid)
        spectral.append({'case':cid,'rows':check})
        for level in plan['reference']['levels']:
            actual=evolution(case,plan['reference'],level)
            require(actual['interior_minimum'] and actual['strict_turn'],'Interior strict turn '+cid)
            require(actual['max_norm_error']<plan['acceptance']['norm_error'],'Norm '+cid)
            for point in actual.pop('trace'):traces.append({'case':cid,'N':level['N'],'dt':level['dt'],**point})
            et=abs(actual['T_b_observed']/target['T_b']-1)
            ev=abs(actual['V_b_observed']/target['V_b']-1)
            rows.append({'case':cid,**level,'T_b_forecast':target['T_b'],'V_b_forecast':target['V_b'],
                         **actual,'relative_T_error':et,'relative_V_error':ev})
            print(json.dumps({'case':cid,'N':level['N'],'relative_T_error':et,'relative_V_error':ev}),flush=True)
    decisions=[]
    for case in plan['cases']:
        selected=[r for r in rows if r['case']==case['id']]
        monotone=all(a[key]>b[key] for key in ('relative_T_error','relative_V_error') for a,b in zip(selected,selected[1:]))
        last=selected[-1]
        passed=monotone and last['relative_T_error']<=plan['acceptance']['finest_relative_T_b_error'] and last['relative_V_error']<=plan['acceptance']['finest_relative_V_b_error']
        decisions.append({'case':case['id'],'errors_decrease':monotone,'status':'PASS' if passed else 'FAIL'})
    result={'plan_sha256':frozen['plan_sha256'],'forecast_sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),
            'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'cases':rows,'decisions':decisions,'spectral_crosschecks':spectral,
            'controls':controls(plan['cases'],forecasts),
            'status':{'early_moment_reference_forecast':'PASS' if all(d['status']=='PASS' for d in decisions) else 'FAIL',
                      'full_CST_bounce':'HOLD_NOT_ELIGIBLE','singularity_resolution':'NOT_ESTABLISHED',
                      'old_dominant_candidate':'CLOSED_REJECTED_FOR_DOMINANT_BOUNCE',
                      'independent_experimental_or_external_replication':False},
            'runtime_seconds':time.monotonic()-start}
    out=ROOT/'results';out.mkdir(exist_ok=True)
    for name,data in [('late_traces.csv',traces),('prediction_errors.csv',rows)]:
        with (out/name).open('w',newline='') as f:
            wr=csv.DictWriter(f,fieldnames=list(data[0]));wr.writeheader();wr.writerows(data)
    (out/'verification.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'runtime_seconds':result['runtime_seconds']},indent=2))
    require(all(d['status']=='PASS' for d in decisions),'Declared reference forecast gate failed')


if __name__=='__main__':run()
