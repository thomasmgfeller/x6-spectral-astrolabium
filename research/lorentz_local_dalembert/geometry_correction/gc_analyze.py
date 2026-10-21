"""SPDX-License-Identifier: Apache-2.0"""
import json
import numpy as np
from gc_common import HERE,cfg,load_phase,write
from gu_analyze import coverage,stats

def accepted(rows):return [r for r in rows if r['evaluation']['status']=='COMPLETE']
def paired(rows):
    rows=accepted(rows);names=cfg()['variants']
    a=np.array([[r['evaluation']['variants'][v]['group_balanced_mse'] for v in names] for r in rows])
    rng=np.random.default_rng(cfg()['bootstrap_seed'])
    draws=rng.integers(0,len(a),size=(cfg()['bootstrap_repetitions'],len(a)))
    means=a.mean(axis=0);boot=a[draws].mean(axis=1);out={}
    for comparator in names[:-1]:
        j=names.index(comparator);ratio=float(np.sqrt(means[-1]/means[j]))
        interval=np.quantile(np.sqrt(boot[:,-1]/boot[:,j]),[.025,.975]).tolist()
        out[comparator]=dict(n=len(rows),rmse_ratio_full_over_comparator=ratio,
            paired_percentile_bootstrap_95=interval,upper_below_one=bool(interval[1]<1))
    return out
def phase_summary(rows,frozen):
    good=accepted(rows);variants={}
    for name in cfg()['variants']:
        es=[r['evaluation']['variants'][name] for r in good];ps=[r['prediction']['variants'][name] for r in good]
        q=frozen['variants'][name]['quantile']
        variants[name]=dict(group_balanced_rmse=float(np.sqrt(np.mean([e['group_balanced_mse'] for e in es]))),
            interval_rmse=float(np.sqrt(np.mean([e['interval_mse'] for e in es]))),
            groups={g:dict(n=sum(g in e['groups'] for e in es),rmse=float(np.sqrt(np.mean([e['groups'][g]['mse'] for e in es if g in e['groups']]))))
                for g in ['root','support_spacelike','support_causal']},
            simultaneous=coverage([e['score'] for e in es],q),
            family_coverage={f:coverage([e['family_scores'][f] for e in es],q) for f in ['interval','gram','block']},
            fallbacks=sum(p['status']=='FALLBACK' for p in ps),order_violations=sum(not p['order']['passed'] for p in ps),
            iterations=stats([p.get('iterations',0) for p in ps]),
            halfwidth_cloud_medians=stats([q*float(np.median(r['prediction']['interval_sd'])) for r in good]))
    return dict(attempts=len(rows),complete=len(good),abstentions=len(rows)-len(good),
        statuses={s:sum(r['evaluation']['status']==s for r in rows) for s in sorted({r['evaluation']['status'] for r in rows})},
        variants=variants,covariance_condition=stats([r['prediction']['covariance_condition'] for r in good]),
        unconstrained_bias_group_balanced_rmse=float(np.sqrt(np.mean([r['evaluation']['unconstrained_bias_group_balanced_mse'] for r in good]))))
def decide(phases,comparison):
    c=cfg();full=phases['test']['variants']['full'];base=phases['test']['variants']['baseline']
    group_ratios={g:full['groups'][g]['rmse']/base['groups'][g]['rmse'] for g in base['groups']}
    gates=dict(minimum_complete=all(p['complete']>=c['minimum_complete'] for p in phases.values()),
        all_orders_exact=all(v['order_violations']==0 for p in phases.values() for v in p['variants'].values()),
        full_fallback_rate=all(p['variants']['full']['fallbacks']/p['complete']<=c['maximum_fallback_rate'] for p in phases.values()),
        full_joint_coverage=full['simultaneous']['rate']>=1-c['alpha'],
        practical_improvement_over_baseline=comparison['baseline']['rmse_ratio_full_over_comparator']<=c['required_rmse_ratio'],
        paired_improvement_over_baseline=comparison['baseline']['upper_below_one'],
        paired_improvement_over_diagonal=comparison['diagonal']['upper_below_one'],
        every_group_noninferior=all(r<=c['maximum_group_rmse_ratio'] for r in group_ratios.values()))
    return gates,group_ratios
def analyze(calibration,test,frozen):
    assert frozen['status']=='FROZEN'
    phases={p:phase_summary(rows,frozen) for p,rows in [('calibration',calibration),('test',test)]}
    comparison=paired(test);gates,group_ratios=decide(phases,comparison)
    return dict(execution='STUDY_COMPLETE',decision='BATCH_CORRECTION_PILOT_SUPPORTED' if all(gates.values()) else 'HOLD_BATCH_CORRECTION',
        gates=gates,group_rmse_ratios_full_over_baseline=group_ratios,phases=phases,paired_test_comparison=comparison,
        calibration_rule=frozen,holds=['HOLD_EMBEDDING_COVARIANCE','HOLD_KALMAN','HOLD_PHASE3','METADATA_HOLD'],
        interpretation='Fixed offline batch correction pilot; approximate paired cloud bootstrap; no conditional coordinate covariance, operator benefit or 4D qualification.')
def main():
    _,cal=load_phase('calibration');_,test=load_phase('test')
    out=analyze(cal,test,json.loads((HERE/'frozen_calibration.json').read_text()));write(HERE/'results/summary.json',out)
    print(json.dumps(dict(decision=out['decision'],gates=out['gates'],paired=out['paired_test_comparison'])))
if __name__=='__main__':main()
