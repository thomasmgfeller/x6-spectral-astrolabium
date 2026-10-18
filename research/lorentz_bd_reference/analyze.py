"""Frozen group-level analysis. Intervals across clouds, never independent pairs."""
import numpy as np
from scipy.stats import t
from core import contract, invert, c2_interval, forward_grid, truth, seed

def group_result(n, c2, bd, h):
    g = contract()['group_size']
    p = c2/(n*(n-1)/2)
    target = truth(h)
    pp, yy, nn = p.reshape(-1,g), bd.reshape(-1,g), n.reshape(-1,g)
    critical = t.ppf(.975, g-1)
    pe = critical*pp.std(axis=1, ddof=1)/np.sqrt(g)
    be = critical*yy.std(axis=1, ddof=1)/np.sqrt(g)
    means = pp.mean(axis=1)
    predictions = {'C2': invert(means), 'BD': yy.mean(axis=1)}
    intervals = {'C2': [c2_interval(a-b, a+b) for a,b in zip(means,pe)],
                 'BD': [[float(a-b),float(a+b)] for a,b in zip(predictions['BD'],be)]}
    # Conditional on each observed N>=2, Hoeffding's U-statistic MGF gives
    # Var-proxy sum_i(1/floor(N_i/2))/(4 M^2) for the unweighted mean.
    he = np.sqrt(np.log(40)/2*np.sum(1/(nn//2),axis=1)/g**2)
    conservative = [c2_interval(a-b,a+b) for a,b in zip(means,he)]
    rows = {}
    for method, values in predictions.items():
        ii = intervals[method]
        error = values-target
        halfwidth = [(b-a)/2 for a,b in ii if a is not None] if all(v is not None for v in ii) else [(v[1]-v[0])/2 for v in ii if v is not None]
        se = values.std(ddof=1)/np.sqrt(len(values))
        d = float(t.ppf(.975,len(values)-1)*se)
        rows[method] = dict(bias=float(error.mean()), bias_mc_interval=[float(error.mean()-d),float(error.mean()+d)],
            sd_group_estimates=float(values.std(ddof=1)), rmse=float(np.sqrt(np.mean(error**2))),
            covered=sum(v is not None and v[0]<=target<=v[1] for v in ii), groups=len(ii),
            incompatible=sum(v is None for v in ii), median_halfwidth=float(np.median(halfwidth)) if halfwidth else None,
            estimates=values.tolist(), intervals=ii)
    pg,_ = forward_grid()
    rows['C2']['clipped_group_estimates'] = int(np.sum((means<pg[0])|(means>pg[-1])))
    rows['C2']['hoeffding_intervals'] = conservative
    rows['C2']['hoeffding_covered'] = sum(v is not None and v[0]<=target<=v[1] for v in conservative)
    rng = np.random.default_rng(seed('analysis-bootstrap'))
    indices = rng.integers(0,len(means),size=(5000,len(means)))
    ebd=(predictions['BD']-target)**2
    ec2=(predictions['C2']-target)**2
    ratios = np.sqrt(ebd[indices].mean(axis=1)/ec2[indices].mean(axis=1))
    rows['rmse_ratio_bootstrap_95'] = np.quantile(ratios,[.025,.975]).tolist()
    return rows

def gate(rows, controls_pass):
    c = contract()['gate']
    primary = next(r for r in rows if r['flat_expected_count']==2048 and r['h']==.5)
    flat = next(r for r in rows if r['flat_expected_count']==2048 and r['h']==0)
    bd,c2 = primary['metrics']['BD'],primary['metrics']['C2']
    target = primary['truth']
    checks = dict(rmse=bd['rmse']<=c['bd_rmse_at_most_c2_factor']*c2['rmse'],
        bias=abs(bd['bias'])<=c['bd_absolute_relative_bias_max']*target,
        width=bd['median_halfwidth']<=c['bd_median_relative_halfwidth_max']*target,
        coverage=bd['covered']>=c['bd_covered_groups_min'],
        flat_bias=abs(flat['metrics']['BD']['bias'])<=c['flat_absolute_bias_max'],
        cost=primary['method_cost_ratio']<=c['total_method_cost_ratio_max'])
    status = c['invalid_controls_or_incomplete_run'] if not controls_pass else c['pass'] if all(checks.values()) else c['fail']
    return dict(status=status, checks=checks, controls_pass=controls_pass)
