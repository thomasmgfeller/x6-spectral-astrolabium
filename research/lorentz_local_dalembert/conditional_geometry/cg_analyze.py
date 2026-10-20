"""Frozen estimators and paired finite-pilot evaluation; no test refitting."""
import hashlib
import json
import numpy as np
from scipy.stats import beta
from cg_common import HERE, contract


def simplex2(r):
    r = np.asarray(r, float)
    if r.shape != (2, 2) or not np.isfinite(r).all() or not np.allclose(r, r.T):
        raise ValueError('finite symmetric two-arm covariance required')
    if np.linalg.eigvalsh(r).min() < -1e-10*max(1, np.linalg.norm(r)):
        raise ValueError('indefinite covariance')
    d = r[0, 0]+r[1, 1]-2*r[0, 1]
    if d <= 1e-14*max(1, np.linalg.norm(r)):
        return np.array([1., 0.])
    w = np.clip((r[1, 1]-r[0, 1])/d, 0., 1.)
    return np.array([w, 1-w])


def metrics(post, variances, innovations=None, innovation_variances=None):
    post, v = np.asarray(post), np.asarray(variances)
    n = len(post)
    hits = int(np.sum(np.abs(post) <= 1.959963984540054*np.sqrt(v)))
    ci = [float(beta.ppf(.025, hits, n-hits+1)) if hits else 0.,
          float(beta.ppf(.975, hits+1, n-hits)) if hits < n else 1.]
    out = dict(n=n, rmse=float(np.sqrt(np.mean(post*post))), bias=float(np.mean(post)),
               coverage=hits/n, coverage_hits=hits, coverage_exact_95=ci,
               mean_nees=float(np.mean(post*post/v)))
    if innovations is not None:
        out['mean_nis'] = float(np.mean(np.asarray(innovations)**2/innovation_variances))
    return out


def load_rows():
    rows, executions = [], []
    for shard in [0, 1]:
        folder = HERE/f'test-{shard}'
        e = json.loads((folder/'execution.json').read_text())
        executions.append(e)
        for record in e['records']:
            raw = (folder/record['file']).read_bytes()
            assert hashlib.sha256(raw).hexdigest() == record['sha256']
            rows.append(json.loads(raw))
    return executions, sorted(rows, key=lambda r:r['seed'])


def analyze():
    c = contract()
    frozen = (HERE/'frozen_calibration.json').read_bytes()
    cal = json.loads(frozen)
    assert cal['status'] == 'FROZEN'
    executions, rows = load_rows()
    assert all(e['calibration_sha256'] == hashlib.sha256(frozen).hexdigest() for e in executions)
    good = [r for r in rows if r['evaluation']['status'] == 'COMPLETE']
    out = dict(decision='CONDITIONAL_HOLD', scope=c['scope'], total=len(rows), complete=len(good),
               calibration_sha256=hashlib.sha256(frozen).hexdigest(), arms={}, records=[])
    if not good:
        (HERE/'summary.json').write_text(json.dumps(out, indent=2)+'\n')
        return out
    g = np.array(cal['geometry_covariance'])
    bvar = np.array(cal['bias_mean_covariance'])
    global_r = g+bvar+np.array(cal['mean_noise_covariance'])
    bias = np.array(cal['bias'])
    p = c['prior_sigma']**2
    clean = np.array([r['evaluation']['clean'] for r in good])+.75
    noises = np.array([r['intrinsic']['conditional_field_covariance'] for r in good])
    post_errors = {}
    for row in good:
        noise = np.array(row['intrinsic']['conditional_field_covariance'])
        r = g+bvar+noise
        corrected = np.array(row['evaluation']['observed'])+.75-bias
        prior = float(np.random.default_rng(np.random.SeedSequence([row['seed'],912343])).normal(scale=c['prior_sigma']))
        record = dict(seed=row['seed'], prior_error=prior, before=row['intrinsic']['before'],
                      after=row['intrinsic']['projection']['after'],
                      projection_shift=row['intrinsic']['projection']['relative_shift'], arms={})
        specs = [('global_original', np.array([1.,0.]), global_r),
                 ('conditional_original', np.array([1.,0.]), r),
                 ('conditional_projected', np.array([0.,1.]), r),
                 ('conditional_joint', simplex2(r), r),
                 ('noise_only_negative', simplex2(noise), noise)]
        for name, w, assumed in specs:
            v = float(w@assumed@w)
            assert v > 0
            measurement = float(w@corrected)
            k = p/(p+v)
            post = prior+k*(measurement-prior)
            record['arms'][name] = dict(weights=w.tolist(), measurement_error=measurement,
                posterior_error=post, posterior_variance=p*v/(p+v), gain=k,
                innovation=measurement-prior, innovation_variance=p+v,
                assumed_measurement_variance=v, noise_contribution=float(w@noise@w),
                geometry_contribution=float(w@g@w), bias_mean_contribution=float(w@bvar@w))
        out['records'].append(record)
    for name in out['records'][0]['arms']:
        a = [r['arms'][name] for r in out['records']]
        post = np.array([r['posterior_error'] for r in a])
        post_errors[name] = post
        m = metrics(post, [r['posterior_variance'] for r in a],
                    [r['innovation'] for r in a], np.array([r['innovation_variance'] for r in a]))
        measurement = np.array([r['measurement_error'] for r in a])
        m.update(measurement_rmse=float(np.sqrt(np.mean(measurement**2))), measurement_bias=float(measurement.mean()))
        completed = {r['seed']:r['arms'][name]['posterior_error'] for r in out['records']}
        all_errors = [completed.get(r['seed'],float(np.random.default_rng(np.random.SeedSequence([r['seed'],912343])).normal(scale=c['prior_sigma']))) for r in rows]
        m['all_clouds_with_prior_fallback_rmse'] = float(np.sqrt(np.mean(np.array(all_errors)**2)))
        out['arms'][name] = m
    prior = np.array([r['prior_error'] for r in out['records']])
    out['arms']['prior_only'] = metrics(prior, np.full(len(prior),p))
    out['clean_rmse'] = np.sqrt(np.mean(clean**2, axis=0)).tolist()
    out['clean_bias'] = clean.mean(axis=0).tolist()
    out['noise_diagonal_range'] = [dict(min=float(a.min()),median=float(np.median(a)),max=float(a.max())) for a in [noises[:,0,0],noises[:,1,1]]]
    order = np.argsort(noises[:,0,0])
    out['noise_strata_diagnostic'] = [dict(n=len(ids),seeds=[good[i]['seed'] for i in ids],
        clean_bias=clean[ids].mean(axis=0).tolist(), clean_rmse=np.sqrt(np.mean(clean[ids]**2,axis=0)).tolist()) for ids in np.array_split(order,3)]
    out['relation_counts'] = dict(before_failed=sum(not r['intrinsic']['before']['passed'] for r in good),
        after_failed=sum(not r['intrinsic']['projection']['after']['passed'] for r in good),
        before_missing=sum(r['intrinsic']['before']['missing'] for r in good),
        before_extra=sum(r['intrinsic']['before']['extra'] for r in good),
        pairs=sum(r['intrinsic']['before']['pairs'] for r in good))
    rng = np.random.default_rng(c['bootstrap_seed'])
    index = rng.integers(0,len(good),size=(c['bootstrap_draws'],len(good)))
    out['comparisons'] = {}
    for label, a, b in [('conditional_vs_global','conditional_original','global_original'),
                         ('joint_vs_original','conditional_joint','conditional_original'),
                         ('projected_vs_original','conditional_projected','conditional_original')]:
        ratio = np.sqrt(np.mean(post_errors[a][index]**2,axis=1)/np.mean(post_errors[b][index]**2,axis=1))
        out['comparisons'][label] = dict(rmse_ratio=out['arms'][a]['rmse']/out['arms'][b]['rmse'],
                                      paired_bootstrap_95=np.quantile(ratio,[.025,.975]).tolist())
    gates = dict(execution_complete=len(rows)==32 and all(e['status']=='COMPLETE' for e in executions),
        budgets=all(e['seconds']<=c['wall_budget_seconds_per_shard'] and e['peak_mib']<=c['memory_budget_mib_per_shard'] for e in executions),
        availability=len(good)>=c['minimum_test_complete'],
        accepted_relations_exact=out['relation_counts']['after_failed']==0,
        clean_accuracy_preserved=out['clean_rmse'][1]<=c['maximum_clean_rmse_ratio']*out['clean_rmse'][0],
        conditional_improvement=out['comparisons']['conditional_vs_global']['rmse_ratio']<=c['required_rmse_ratio'],
        joint_improvement=out['comparisons']['joint_vs_original']['rmse_ratio']<=c['required_rmse_ratio'],
        nominal_coverage=out['arms']['conditional_joint']['coverage']>=c['minimum_test_coverage'])
    out['gates'] = gates
    if all(gates.values()):
        out['decision'] = 'CONDITIONAL_PILOT_SUPPORTED'
    (HERE/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
    return out


if __name__ == '__main__':
    result = analyze()
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
