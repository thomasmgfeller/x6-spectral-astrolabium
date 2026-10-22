"""Certified Poisson likelihood-ratio event probabilities at finite counts.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'spatial_search'))
from ss_run import F,read,save,outward

def ceiling(x):return -((-x.numerator)//x.denominator)

def log_bounds(r,terms):
    """Positive atanh series, with a geometric upper bound on its remainder."""
    assert r>=1 and terms>0
    t=(r-1)/(r+1)
    partial=2*sum((t**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    remainder=2*t**(2*terms+1)/(F(2*terms+1)*(1-t*t))
    return partial,partial+remainder

def crossing(a,b,terms):
    assert 0<a[0]<=a[1]<b[0]<=b[1]
    loglo=log_bounds(b[0]/a[1],terms)[0]
    loghi=log_bounds(b[1]/a[0],terms)[1]
    assert loglo>0
    lo=(b[0]-a[1])/loghi;hi=(b[1]-a[0])/loglo
    lowfloor=lo.numerator//lo.denominator;highfloor=hi.numerator//hi.denominator
    unique=lowfloor==highfloor
    midpoint=sum(a+b)/4
    k=lowfloor if unique else midpoint.numerator//midpoint.denominator
    return k,unique,(lo,hi)

def cdf(mu,k,digits,upper_steps,maximum_mean):
    """Enclose P(Poisson(mu)<=k) without exp(-mu) or floating-point arithmetic.

    Weight at floor(mu) is 1. All recurrence weights are enclosed on a fixed
    10^-digits grid, then normalized with an explicitly retained infinite tail.
    """
    assert mu>=0 and mu<=maximum_mean
    assert isinstance(k,int) and digits>0 and upper_steps>0
    if k<0:return (F(0),F(0)),dict(degenerate=True)
    if mu==0:return (F(1),F(1)),dict(degenerate=True)
    mode=mu.numerator//mu.denominator;upper=mode+upper_steps
    assert k<=upper
    q=10**digits;lo=hi=q;slo=shi=q
    alo=ahi=q if mode<=k else 0
    n,d=mu.numerator,mu.denominator
    for j in range(mode,0,-1):
        lo=lo*j*d//n;hi=-((-hi*j*d)//n)
        slo+=lo;shi+=hi
        if j-1<=k:alo+=lo;ahi+=hi
    lo=hi=q
    for j in range(mode+1,upper+1):
        den=d*j
        lo=lo*n//den;hi=-((-hi*n)//den)
        slo+=lo;shi+=hi
        if j<=k:alo+=lo;ahi+=hi
    # First omitted weight, followed by ratios bounded by mu/(upper+2)<1.
    assert mu<upper+2
    tail=ceiling(F(hi)*mu/(upper+1)/(1-mu/(upper+2)))
    lower=F(alo,shi+tail);higher=min(F(1),F(ahi,slo))
    assert 0<=lower<=higher<=1
    return (lower,higher),dict(mode=mode,upper=upper,down_steps=mode,up_steps=upper_steps,
        omitted_weight_upper_grid_units=tail,normalizer_grid_bounds=[str(slo),str(shi+tail)])

def event_certificate(a,b,c):
    assert all(0<=lo<=hi for lo,hi in (a,b))
    if a[0]>b[0]:a,b=b,a
    k,optimal,x=crossing(a,b,c['log_series_terms'])
    bounds=[];records=[]
    for label,mu in [('small_lower',a[0]),('small_upper',a[1]),('large_lower',b[0]),('large_upper',b[1])]:
        bound,meta=cdf(mu,k,c['cdf_grid_digits'],c['cdf_upper_steps'],c['maximum_mean'])
        bounds.append(bound)
        records.append(dict(endpoint=label,mean=str(mu),cdf=outward(*bound,digits=60),**meta))
    # CDF decreases with the Poisson mean. Enclose the same event under both laws.
    lo=max(F(0),bounds[1][0]-bounds[2][1])
    hi=min(F(1),bounds[0][1]-bounds[3][0])
    assert lo<=hi
    return dict(threshold=k,optimal_single_count_event_certified=optimal,
        crossing_interval=outward(*x,digits=40),event_difference=outward(lo,hi,digits=60),
        full_law_tv_lower=outward(lo)[0],precision_target_met=hi-lo<=F(c['target_probability_interval_width']),
        endpoint_cdf_records=records)

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');old=read(HERE.parent/'spatial_search'/'marginal_diagnostic.json')
    scan=read(HERE.parent/'spatial_search'/'candidates.json.gz');threshold=F(c['strong_gap_gate'])
    assert [r['index'] for r in scan if 'relative' in r and F(r['relative'][0])>threshold]==[r['index'] for r in old['results']]
    assert all(F(r['relative'][0])>threshold or F(r['relative'][1])<=threshold for r in scan if 'relative' in r)
    rows=[]
    for previous in old['results']:
        assert previous['status']!='CONDITIONING_REJECTED'
        a,b=[tuple(map(F,v)) for v in previous['mean_intervals']]
        result=event_certificate(a,b,c)
        assert F(result['full_law_tv_lower'])>=F(previous['tv_lower'])
        row=dict(index=previous['index'],interval_index=previous['interval_index'],endpoints=previous['endpoints'],
            symmetric_gap=previous['symmetric_gap'],previous_tv_lower=previous['tv_lower'],
            previously_unresolved=previous['status']=='MARGINAL_INCONCLUSIVE',**result)
        row['status']='DISTINGUISHABLE_AT_TV_GATE' if F(row['full_law_tv_lower'])>F(c['tv_gate']) else 'HOLD'
        rows.append(row)
    unresolved=[r['index'] for r in rows if r['status']=='HOLD']
    summary=dict(status='FINITE_GRID_STRONG_PAIR_EXCLUDED' if not unresolved else 'HOLD_STRONG_CANDIDATE_LAW',
        checked=len(rows),previously_unresolved=sum(r['previously_unresolved'] for r in rows),
        newly_excluded=sum(r['previously_unresolved'] and r['status']=='DISTINGUISHABLE_AT_TV_GATE' for r in rows),
        total_excluded=sum(r['status']=='DISTINGUISHABLE_AT_TV_GATE' for r in rows),unresolved_indices=unresolved,
        optimal_thresholds_certified=sum(r['optimal_single_count_event_certified'] for r in rows),
        precision_targets_met=sum(r['precision_target_met'] for r in rows),
        minimum_full_law_tv_lower=min((r['full_law_tv_lower'] for r in rows),key=F),
        maximum_full_law_tv_lower=max((r['full_law_tv_lower'] for r in rows),key=F),
        scope='Only the 512 frozen PR107 candidates at its fixed base and steps. Individual-count TV lower bounds obstruct full count/overlap-law closeness without count-independence assumptions. No continuous-family, arbitrary-pair or global stability conclusion.')
    return rows,summary

if __name__=='__main__':
    for name,data in zip(('certificates.json','summary.json'),run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
    print(json.dumps(read(HERE/'summary.json')))
