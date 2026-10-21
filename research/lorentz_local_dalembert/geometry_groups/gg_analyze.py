"""SPDX-License-Identifier: Apache-2.0"""
import json
import numpy as np
from gg_common import HERE,cfg,load_phase,model,write
from gu_analyze import coverage,stats

def shape(z):
    a=np.asarray(z);mu=float(a.mean());second=float(np.mean(a*a))
    return dict(n=len(a),mean_z=mu,second_moment=second,
        passed=bool(len(a)>=cfg()['minimum_complete'] and abs(mu)<=cfg()['shape_mean_limit']
            and cfg()['shape_second_moment_range'][0]<=second<=cfg()['shape_second_moment_range'][1]))

def model_summary(rows,which,q):
    arms={};screen=True
    for arm in cfg()['arms']:
        records=[r['evaluation']['models'][which]['arms'][arm] for r in rows]
        pred=[r['prediction']['models'][which][arm] for r in rows]
        block_names=sorted({k for r in records for k in r['standardized_blocks']})
        blocks={name:shape([r['standardized_blocks'][name] for r in records if name in r['standardized_blocks']]) for name in block_names}
        groups={}
        for name in cfg()['groups']:
            rs=[r['groups'][name] for r in records if name in r['groups']]
            if not rs:groups[name]=dict(n=0,passed=False);continue
            mu=float(np.mean([r['mean_z'] for r in rs]));second=float(np.mean([r['second_moment'] for r in rs]))
            okay=len(rs)>=cfg()['minimum_complete'] and abs(mu)<=cfg()['shape_mean_limit'] and cfg()['shape_second_moment_range'][0]<=second<=cfg()['shape_second_moment_range'][1]
            groups[name]=dict(n=len(rs),point_mean_z=mu,point_second_moment=second,passed=bool(okay),
                raw_rmse=float(np.sqrt(np.mean([r['raw_mse'] for r in rs]))),
                adjusted_rmse=float(np.sqrt(np.mean([r['adjusted_mse'] for r in rs]))),
                interval_family_coverage=coverage([r['max_abs_z'] for r in rs],q),
                interval_halfwidth_cloud_medians=stats([p['group_median_sd'][name]*q for p in pred if name in p['group_median_sd']]))
        arm_screen=all(v['passed'] for v in blocks.values()) and all(v['passed'] for v in groups.values());screen=screen and arm_screen
        arms[arm]=dict(blocks=blocks,groups=groups,shape_screen_passed=bool(arm_screen),
            family_coverage={name:coverage([r['family_scores'][name] for r in records],q) for name in ['interval','gram','block']},
            raw_rmse=float(np.sqrt(np.mean([r['raw_mse'] for r in records]))),
            adjusted_rmse=float(np.sqrt(np.mean([r['adjusted_mse'] for r in records]))),
            interval_halfwidth_cloud_medians=stats([float(np.median(p['interval_sd']))*q for p in pred]),
            gram_halfwidth_cloud_medians=stats([float(np.median(p['gram_sd']))*q for p in pred]),
            covariance_condition=stats([p['covariance_condition'] for p in pred]),
            shared_to_diagonal_variance_ratios={name:stats([p['blocks'][name]['shared_to_diagonal_variance_ratio'] for p in pred if name in p['blocks']]) for name in block_names})
    return dict(simultaneous=coverage([r['evaluation']['models'][which]['score'] for r in rows],q),
        shape_screen_passed=bool(screen),arms=arms,
        strata={feature:{level:coverage([r['evaluation']['models'][which]['score'] for r in rows if r['prediction'][feature]==level],q)
            for level in ['low','high']} for feature in ['support_stratum','condition_stratum']})

def phase_summary(rows,frozen):
    accepted=[r for r in rows if r['evaluation']['status']=='COMPLETE'];assert accepted
    return dict(attempts=len(rows),complete=len(accepted),abstentions=len(rows)-len(accepted),
        statuses={status:sum(r['evaluation']['status']==status for r in rows) for status in sorted({r['evaluation']['status'] for r in rows})},
        outside_development_range=sum(r['prediction']['outside_development_range'] for r in accepted),
        models={which:model_summary(accepted,which,frozen['models'][which]['quantile']) for which in cfg()['models']})

def paired_comparison(rows):
    accepted=[r for r in rows if r['evaluation']['status']=='COMPLETE']
    # Matched cloud bootstrap; both models, arms and focus groups use the same draws.
    rows=[r for r in accepted if all(g in r['evaluation']['models'][m]['arms'][a]['standardized_blocks']
        for m in cfg()['models'] for a in cfg()['arms'] for g in cfg()['focus_groups'])]
    a=np.array([[[r['evaluation']['models'][m]['arms'][arm]['standardized_blocks'][g]**2
        for arm in cfg()['arms'] for g in cfg()['focus_groups']] for m in cfg()['models']] for r in rows])
    assert len(rows)>0
    def distortion(v):return np.mean(np.abs(np.log(np.maximum(v,1e-15))),axis=-1)
    D=distortion(a.mean(axis=0));delta=float(D[1]-D[0])
    rng=np.random.default_rng(cfg()['bootstrap_seed']);boot=[]
    for _ in range(cfg()['bootstrap_repetitions']):
        dd=distortion(a[rng.integers(0,len(a),len(a))].mean(axis=0));boot.append(float(dd[1]-dd[0]))
    interval=np.quantile(boot,[.025,.975]).tolist()
    return dict(n=len(rows),metric='Mean absolute log second moment of focus-block standardized means, across both arms.',
        pooled_distortion=float(D[0]),grouped_distortion=float(D[1]),difference_grouped_minus_pooled=delta,
        paired_percentile_bootstrap_95=interval,improvement_screen_passed=bool(interval[1]<0),
        interpretation='Prespecified paired cloud bootstrap; approximate pilot evidence, not an exact finite-sample test.')

def analyze(calibration,test,frozen):
    assert frozen['status']=='FROZEN'
    phases={p:phase_summary(rows,frozen) for p,rows in [('calibration',calibration),('test',test)]}
    paired=paired_comparison(test);target=phases['test']['models']['grouped']
    gates=dict(minimum_complete=all(p['complete']>=cfg()['minimum_complete'] for p in phases.values()),
        observed_joint_coverage_at_least_95=target['simultaneous']['rate']>=1-cfg()['alpha'],
        all_grouped_shape_screens=target['shape_screen_passed'],paired_focus_improvement=paired['improvement_screen_passed'])
    return dict(execution='STUDY_COMPLETE',decision='GROUP_MODEL_PILOT_SUPPORTED' if all(gates.values()) else 'HOLD_GROUP_MODEL',
        gates=gates,holds=['HOLD_EMBEDDING_COVARIANCE','HOLD_PHASE3','METADATA_HOLD'],
        development=model(),calibration_rule=frozen,phases=phases,paired_test_comparison=paired,
        interpretation='Marginal invariant prediction sets and working second-moment shape; no conditional coordinate covariance, production correction or 4D transfer.')

def main():
    _,cal=load_phase('calibration');_,test=load_phase('test')
    out=analyze(cal,test,json.loads((HERE/'frozen_calibration.json').read_text()));write(HERE/'results/summary.json',out)
    print(json.dumps(dict(decision=out['decision'],gates=out['gates'],
        coverage={m:v['simultaneous'] for m,v in out['phases']['test']['models'].items()},paired=out['paired_test_comparison'])))

if __name__=='__main__':main()
