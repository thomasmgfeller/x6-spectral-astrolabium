"""Independent integral/CDF checks, adversarial controls and complete replay."""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import binom

HERE=Path(__file__).resolve().parent


def require(ok,message):
    if not ok:
        raise AssertionError(message)


def direct_integral(a,weight):
    # An adaptive integrator, independent of the producer's fixed-order nodes.
    def f(t): return (a/2-abs(t))**3*weight(t)
    return quad(f,-a/2,0,epsabs=1e-12,epsrel=1e-12)[0]+quad(f,0,a/2,epsabs=1e-12,epsrel=1e-12)[0]


def reference_probability(row):
    model,a=row['model'],row['a']
    if model=='uniform_flat': return a**row['d']
    if model in ['de_sitter','density_twin']:
        h=row['parameter']
        weight=lambda t:(1-h*t)**-4
        return direct_integral(a,weight)/direct_integral(1.,weight)
    if model=='density':
        b=row['parameter']
        weight=lambda t:1+b*(2*t)**2
        return direct_integral(a,weight)/direct_integral(1.,weight)
    if model=='thinning':
        q=a**4
        r=row['parameter']
        return r*q/(r*q+1-q)
    raise ValueError('unknown model')


def coverage_by_cdf(m,p,theta,d,bounds,alpha):
    q=theta**d
    rl,ru=bounds
    pmin=rl*q/(1-q+rl*q)
    pmax=ru*q/(1-q+ru*q)
    # Integer acceptance bounds, without inverse beta functions or producer masks.
    left,right=0,m
    while left<right:
        mid=(left+right)//2
        if binom.cdf(mid,m,pmin)>=alpha/2: right=mid
        else: left=mid+1
    low=left
    left,right=0,m
    while left<right:
        mid=(left+right+1)//2
        if binom.sf(mid-1,m,pmax)>=alpha/2: left=mid
        else: right=mid-1
    high=left
    if high<low: return 0.,[low,high]
    # Choose CDF or survival representation to avoid subtracting two near-ones.
    if low>m*p:
        value=binom.sf(low-1,m,p)-binom.sf(high,m,p)
    else:
        value=binom.cdf(high,m,p)-binom.cdf(low-1,m,p)
    return float(value),[low,high]


def check_row(row,contract):
    tol=contract['numerics']['probability_tolerance']
    p=reference_probability(row)
    require(abs(p-row['p'])<contract['numerics']['geometry_absolute_tolerance'],'independent geometry mismatch')
    if row['model']=='de_sitter':
        h=row['parameter']
        theta=math.log((1+h*row['a']/2)/(1-h*row['a']/2))/math.log((1+h/2)/(1-h/2))
        require(abs(theta-row['theta'])<1e-13,'proper-time ratio mismatch')
    elif row['geometry']=='flat':
        require(row['theta']==row['a'],'flat proper-time ratio mismatch')
    cov,acceptance=coverage_by_cdf(row['m'],p,row['theta'],row['d'],row['intensity_bounds'],contract['confidence_alpha'])
    require(abs(cov-row['coverage'])<tol,'independent CDF coverage mismatch')
    for key in ['coverage','precision_probability','false_precision_probability','raw_within_10percent_probability']:
        require(-tol<=row[key]<=1+tol,'invalid probability')
    require(row['false_precision_probability']<=row['precision_probability']+tol,'invalid joint probability')
    if row['in_assumed_class']:
        require(row['coverage']>=1-contract['confidence_alpha']-tol,'in-class coverage theorem violated')
        require(row['false_precision_probability']<=contract['confidence_alpha']+tol,'in-class fixed-budget precision bound violated')
    return abs(cov-row['coverage']),abs(p-row['p']),acceptance


def selftest():
    from core import inverse_odds,interval_arrays,volume,summarize
    c=json.loads((HERE/'contract.json').read_text())
    # Off-grid, exact rational finite law; not a target-grid efficacy result.
    m,p=19,Fraction(2,7)
    exact=[Fraction(math.comb(m,k))*p**k*(1-p)**(m-k) for k in range(m+1)]
    require(sum(exact)==1,'exact rational binomial identity')
    require(max(abs(float(v)-binom.pmf(k,m,float(p))) for k,v in enumerate(exact))<1e-14,'rational probabilities')
    for r in [0.37,1.,2.8]:
        q=.173
        prob=r*q/(1-q+r*q)
        require(abs(inverse_odds(prob,r)-q)<1e-15,'odds identity')
    for a,h in [(.31,0.),(.83,.37),(.29,1.43)]:
        expected=direct_integral(a,lambda t:(1-h*t)**-4)
        require(abs(volume(a,h)-expected)<1e-13,'off-grid quadrature')
    # Clopper-Pearson limits independently invert binomial tails with brentq.
    for k in [0,1,8,18,19]:
        lo,hi=interval_arrays(np.array([k]),m,3,[1.,1.],.05)
        lower=0. if k==0 else brentq(lambda x:binom.sf(k-1,m,x)-.025,0,1,xtol=1e-14)
        upper=1. if k==m else brentq(lambda x:binom.cdf(k,m,x)-.025,0,1,xtol=1e-14)
        require(abs(lo[0]**3-lower)<1e-12 and abs(hi[0]**3-upper)<1e-12,'independent interval inversion')
    cell=dict(model='uniform_flat',d=3,theta=.37,planning_theta=.37,a=.37,parameter=0.,p=.37**3,geometry='flat',relative_intensity=1.)
    row=summarize(cell,73,'nominal',[1.,1.],c)
    check_row(row,c)
    q=.37**4
    selective=dict(model='thinning',d=4,theta=.37,planning_theta=.37,a=.37,
                   parameter=.63,p=.63*q/(1-q+.63*q),geometry='flat',relative_intensity=.63)
    robust=summarize(selective,73,'off_grid_bounds',[.3,2.8],c)
    check_row(robust,c)
    require(robust['in_assumed_class'] and robust['coverage']>=.95,'bounded nuisance coverage')
    rejected=0
    for key,delta in [('coverage',-.1),('p',.01),('theta',.01)]:
        bad=copy.deepcopy(row); bad[key]+=delta
        try: check_row(bad,c)
        except AssertionError: rejected+=1
    require(rejected==3,'mutations must be rejected')
    for args in [(np.array([-1]),19,4,[1,1],.05),(np.array([3.5]),19,4,[1,1],.05),(np.array([2]),19,4,[2,1],.05)]:
        try: interval_arrays(*args)
        except ValueError: continue
        raise AssertionError('invalid inputs not rejected')
    print('PASS_OFF_GRID_SELFTESTS_WITH_3_RESULT_MUTATIONS')


def compare(a,b,path='root'):
    if isinstance(a,dict):
        require(a.keys()==b.keys(),'replay keys '+path)
        for k in a: compare(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        require(len(a)==len(b),'replay length '+path)
        for i,(x,y) in enumerate(zip(a,b)): compare(x,y,path+'/'+str(i))
    elif isinstance(a,float):
        require(math.isclose(a,b,rel_tol=1e-9,abs_tol=5e-10),'replay float '+path)
    else: require(a==b,'replay exact value '+path)


def verify(results,replay=False):
    from run import FROZEN,ROOT
    c=json.loads((HERE/'contract.json').read_text())
    hashes=json.loads((results/'hashes.json').read_text())
    for f,digest in hashes.items():
        require(Path(f).name==f,'unsafe archive path')
        require(hashlib.sha256((results/f).read_bytes()).hexdigest()==digest,'archive hash '+f)
    execution=json.loads((results/'execution.json').read_text())
    for f in FROZEN:
        raw=(HERE/f).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==execution['frozen_sha256'][f],'source digest '+f)
        pinned=subprocess.check_output(['git','show',execution['source_commit']+':research/lorentz_proper_time_validity/'+f],cwd=ROOT)
        require(raw==pinned,'public source pin '+f)
    rows=json.loads((results/'grid.json').read_text())
    errors=[check_row(row,c) for row in rows]
    # Retain integer acceptance bounds as independent auxiliary evidence.
    report=dict(status='PASS_VALIDITY_MAP_CHECKS',rows=len(rows),
                max_independent_coverage_error=max(x[0] for x in errors),
                max_independent_geometry_error=max(x[1] for x in errors),
                acceptance_bounds=[x[2] for x in errors],
                external_replication=False,full_replay=replay)
    if replay:
        from run import run
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'replay'
            run(out,execution['source_commit'])
            for f in ['grid.json','planning.json']:
                compare(json.loads((results/f).read_text()),json.loads((out/f).read_text()))
        report['status']='PASS_FULL_PROPER_TIME_VALIDITY_REPLAY'
    print(json.dumps({k:v for k,v in report.items() if k!='acceptance_bounds'}))
    return report


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--selftest',action='store_true')
    a.add_argument('--results',type=Path,default=HERE/'results')
    a.add_argument('--replay',action='store_true')
    a.add_argument('--report',type=Path)
    ns=a.parse_args()
    selftest()
    if not ns.selftest:
        report=verify(ns.results,ns.replay)
        if ns.report: ns.report.write_text(json.dumps(report,indent=2)+'\n')
