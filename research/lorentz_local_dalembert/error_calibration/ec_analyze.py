"""SPDX-License-Identifier: Apache-2.0
Keep mean bias, between-cloud spread and conditional measurement covariance separate.
"""
import json
import numpy as np
from scipy.stats import beta,norm
from ec_common import HERE,cfg,ARMS,write,load_phase,source_check
from ec_measure import noise_tests


def cp(k,n,alpha):
    return [0. if k==0 else float(beta.ppf(alpha/2,k,n-k+1)),
            1. if k==n else float(beta.ppf(1-alpha/2,k+1,n-k))]


def rejects(tests,alpha):
    return [x for x in tests if (not x['passed'] if x['degenerate'] else
                                min(x['mean_p'],x['variance_p'])<alpha)]


def analyze():
    source_check();c=cfg(); executions,rows=load_phase('test')
    calibration=json.loads((HERE/'frozen_calibration.json').read_text())
    assert calibration['status']=='FROZEN'
    schedule=json.loads((HERE/'seed_schedule.json').read_text())['test']
    assert [(r['index'],r['seed'],r['noise_key']) for r in rows]==[(s['index'],s['geometry_seed'],s['noise_key']) for s in schedule]
    good=[r for r in rows if r['evaluation']['status']=='COMPLETE'];n=len(good)
    assert n>1
    e=np.array([[f['error'] for f in r['evaluation']['fields']] for r in good])
    mu=e.mean(axis=0);centered=e-mu
    geometry_cov=np.einsum('cfa,cfb->fab',centered,centered)/n
    second=np.einsum('cfa,cfb->fab',e,e)/n
    np.testing.assert_allclose(second,geometry_cov+np.einsum('fa,fb->fab',mu,mu),atol=1e-10)
    noises=np.array([r['evaluation']['conditional_noise_covariance'] for r in good])
    mean_noise=noises.mean(axis=0)
    alpha=c['noise_test_family_alpha']/c['noise_test_maximum_count']
    z=float(norm.ppf(1-c['measurement_miscoverage']/(2*len(ARMS)*len(c['fields']))))
    radii=np.asarray(calibration['geometry_radii'])
    tests=[];failures=[];wrong_root=[];wrong_diagonal=[];coverage=[]
    for r in good:
        v=r['evaluation']; covariance=np.array(v['conditional_noise_covariance'])
        full=np.array(v['full_coefficients'])
        wrong=c['field_noise_sigma']**2*(full[:,1:]@full[:,1:].T)
        measurement_radius=z*np.sqrt(np.maximum(0,np.diag(covariance)))
        clean=np.array([f['error'] for f in v['fields']])
        observed=np.array([np.array(f['observed'])-f['truth'] for f in v['fields']])
        holdout=np.array([f['noise']['holdout'] for f in v['fields']])
        coverage.append(dict(index=r['index'],seed=r['seed'],
            geometry=bool(np.all(np.abs(clean)<=radii)),
            measurement=bool(np.all(np.abs(holdout)<=measurement_radius)),
            total=bool(np.all(np.abs(observed)<=radii+measurement_radius)),
            measurement_radii=measurement_radius.tolist(),total_radii=(radii+measurement_radius).tolist()))
        for f in v['fields']:
            values=noise_tests(f['noise'],covariance)
            tests.append(dict(index=r['index'],field=f['name'],tests=values))
            failures.extend([dict(index=r['index'],field=f['name'],**x) for x in rejects(values,alpha)])
            if rejects(noise_tests(f['noise'],wrong),alpha):wrong_root.append([r['index'],f['name']])
            if rejects(noise_tests(f['noise'],np.diag(np.diag(covariance))),alpha):wrong_diagonal.append([r['index'],f['name']])
    proportions={}
    for kind in ['geometry','measurement','total']:
        k=sum(v[kind] for v in coverage)
        interval=cp(k,n,.05/3)
        proportions[kind]=dict(successes=k,total=n,rate=k/n,simultaneous_95_binomial_interval=interval,
            population_95_percent_empirically_certified=interval[0]>=.95)
    rng=np.random.default_rng(c['bootstrap_seed'])
    indices=rng.integers(0,n,size=(c['bootstrap_replicates'],n))
    cloud_losses=np.mean(e*e,axis=1)
    boot_loss=cloud_losses[indices].mean(axis=1)
    comparisons={}
    for name,a,b in [('metadata_vs_original',1,0),('projected_metadata_vs_projected',3,2),('projected_vs_original',2,0)]:
        ratios=np.sqrt(boot_loss[:,a]/boot_loss[:,b])
        interval=np.quantile(ratios,[.025,.975]).tolist()
        ratio=float(np.sqrt(cloud_losses[:,a].mean()/cloud_losses[:,b].mean()))
        comparisons[name]=dict(clean_rmse_ratio=ratio,paired_cloud_bootstrap_95=interval,
            descriptive_five_percent_improvement=ratio<=.95 and interval[1]<1)
    components=[]
    for a,name in enumerate(ARMS):
        bias2=float(np.mean(mu[:,a]**2))
        spread=float(np.mean(geometry_cov[:,a,a]))
        measurement=float(mean_noise[a,a]);geom=bias2+spread
        components.append(dict(arm=name,bias_squared=bias2,geometry_spread=spread,
            clean_rmse=float(np.sqrt(geom)),measurement_variance=measurement,
            total_expected_mse=geom+measurement,geometry_fraction=geom/(geom+measurement),
            expected_rmse_by_measurement_averages={str(k):float(np.sqrt(geom+measurement/k)) for k in [1,16,512]},
            clean_rmse_cloud_bootstrap_95=np.sqrt(np.quantile(boot_loss[:,a],[.025,.975])).tolist()))
    geom_summary={}
    for name in ['original','projected']:
        vals=[r['evaluation']['geometry'][name] for r in good]
        errors=np.concatenate([v['proper_time_errors'] for v in vals])
        geom_summary[name]=dict(clouds=n,clouds_with_relation_errors=sum(v['missing_relations']+v['extra_relations']>0 for v in vals),
            missing=sum(v['missing_relations'] for v in vals),extra=sum(v['extra_relations'] for v in vals),
            ordered_pairs=sum(v['ordered_pairs'] for v in vals),causal_pairs=sum(v['causal_pairs'] for v in vals),
            gram_relative_rms=float(np.sqrt(np.mean([v['gram_relative_error']**2 for v in vals]))),
            proper_time_rmse_all_causal_pairs=float(np.sqrt(np.mean(errors**2))),
            proper_time_rmse_cloud_weighted=float(np.sqrt(np.mean([v['proper_time_rmse']**2 for v in vals]))))
    execution_ok=len(rows)==c['test_clouds'] and all(x['status']=='COMPLETE' and x['seconds']<=c['wall_seconds_per_worker'] and x['peak_mib']<=c['memory_mib_per_worker'] for x in executions)
    controls=dict(root_omission_detected=bool(wrong_root),ignored_cross_covariance_detected=bool(wrong_diagonal))
    supported=execution_ok and n>=c['minimum_test_complete'] and not failures and all(controls.values()) and proportions['total']['rate']>=c['minimum_empirical_joint_coverage']
    summary=dict(schema='x6.geometry-noise-calibration-results/1',
        decision='CALIBRATION_COMPONENTS_SUPPORTED' if supported else 'CALIBRATION_HOLD',
        phase3='HOLD_PHASE3',embedding_covariance='HOLD_EMBEDDING_COVARIANCE',
        scheduled=len(rows),complete=n,unavailable=[dict(index=r['index'],seed=r['seed'],reason=r['evaluation']['status']) for r in rows if r['evaluation']['status']!='COMPLETE'],
        execution_within_budget=execution_ok,execution=executions,calibration_complete=calibration['complete'],
        conformal_geometry_quantile=calibration['quantile'],
        nominal_marginal_total_coverage_lower=calibration['total_nominal_marginal_coverage_lower'],
        noise_checks=dict(family_alpha=c['noise_test_family_alpha'],maximum_tests=c['noise_test_maximum_count'],
            alpha_per_test=alpha,tested_directions=sum(len(x['tests']) for x in tests),rejected=failures,
            positive_controls=controls,root_omission_detected_cloud_fields=len(wrong_root),diagonal_detected_cloud_fields=len(wrong_diagonal)),
        coverage=proportions,coverage_records=coverage,components=components,
        clean_mean_bias_per_field=mu.tolist(),clean_geometry_covariance_per_field=geometry_cov.tolist(),
        clean_uncentered_second_moment_per_field=second.tolist(),mean_conditional_measurement_covariance=mean_noise.tolist(),
        expected_total_second_moment_per_field=(second+mean_noise[None,:,:]).tolist(),
        geometry_diagnostics=geom_summary,descriptive_comparisons=comparisons,
        limits=['Synthetic known-noise calibration in fixed-density flat 2+1 only.',
                'Operator/model error includes reconstruction, discretization and selection; it is not isolated coordinate error.',
                'Conformal statement is simultaneous across 16 fixed outputs but marginal over independent accepted clouds and calibration draws.',
                'No per-cloud or fixed-calibration conditional coverage claim; Gaussian input noise and seed assumptions are explicit.',
                'No changes to operator weights, Kalman gain, embedding precision, prior historical HOLDs, 4D sampler or main branch.'])
    return summary,tests


if __name__=='__main__':
    summary,tests=analyze();write(HERE/'results/summary.json',summary);write(HERE/'results/noise_checks.json',tests)
    print(json.dumps(dict(decision=summary['decision'],complete=summary['complete'],
        noise_rejections=len(summary['noise_checks']['rejected']),coverage=summary['coverage'],components=summary['components'])))
