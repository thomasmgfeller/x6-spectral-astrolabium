"""SPDX-License-Identifier: Apache-2.0"""
import json
import numpy as np
from scipy.stats import beta
from gu_common import HERE,cfg,load_phase,model,write

def coverage(values,q):
    n=len(values);k=sum(v<=q for v in values)
    if not n:return dict(n=0,covered=0,rate=None,clopper_pearson_95=None)
    lo=0. if k==0 else float(beta.ppf(.025,k,n-k+1))
    hi=1. if k==n else float(beta.ppf(.975,k+1,n-k))
    return dict(n=n,covered=k,rate=k/n,clopper_pearson_95=[lo,hi])
def stats(values):
    a=np.array(values)
    return dict(n=len(a),mean=float(a.mean()),median=float(np.median(a)),min=float(a.min()),max=float(a.max()))
def phase_summary(rows,q):
    complete=[r for r in rows if r['evaluation']['status']=='COMPLETE'];arms={}
    assert complete
    for arm in cfg()['arms']:
        records=[r['evaluation']['arms'][arm] for r in complete]
        pred=[r['prediction']['arms'][arm] for r in complete]
        blocks={};screen=True
        for name in cfg()['blocks']:
            vals=[r['standardized_blocks'][name] for r in records if name in r['standardized_blocks']]
            if not vals:blocks[name]=dict(n=0);screen=False;continue
            z=np.array(vals);mu=float(z.mean());second=float(np.mean(z*z))
            okay=abs(mu)<=cfg()['shape_mean_limit'] and cfg()['shape_second_moment_range'][0]<=second<=cfg()['shape_second_moment_range'][1]
            screen=screen and okay
            blocks[name]=dict(n=len(z),mean_z=mu,second_moment=second,screen_passed=okay,
                shared_to_diagonal_variance_ratio=stats([p['blocks'][name]['shared_to_diagonal_variance_ratio'] for p in pred if name in p['blocks']]))
        point_second=float(np.mean([r['standardized_pointwise_second_moment'] for r in records]))
        screen=screen and cfg()['shape_second_moment_range'][0]<=point_second<=cfg()['shape_second_moment_range'][1]
        arms[arm]=dict(
            simultaneous=coverage([r['score'] for r in records],q),
            family_coverage={name:coverage([r['family_scores'][name] for r in records],q) for name in ['interval','gram','block']},
            raw_rmse=float(np.sqrt(np.mean([r['raw_mse'] for r in records]))),
            bias_adjusted_rmse=float(np.sqrt(np.mean([r['adjusted_mse'] for r in records]))),
            raw_cloud_balanced_mean=float(np.mean([r['raw_mean_error'] for r in records])),
            adjusted_cloud_balanced_mean=float(np.mean([r['adjusted_mean_error'] for r in records])),
            interval_halfwidth_cloud_medians=stats([float(np.median(p['interval_sd']))*q for p in pred]),
            interval_halfwidth_physical_cloud_medians=stats([float(np.median(r['prediction']['arms'][arm]['interval_sd']))*q*r['prediction']['scale']**2 for r in complete]),
            gram_halfwidth_cloud_medians=stats([float(np.median(p['gram_sd']))*q for p in pred]),
            covariance_condition=stats([p['covariance_condition'] for p in pred]),
            pointwise_second_moment=point_second,standardized_blocks=blocks,
            covariance_screen='WORKING_COVARIANCE_SCREEN_PASSED' if screen else 'WORKING_COVARIANCE_SCREEN_FAILED')
    strata={}
    for feature in ['support_stratum','condition_stratum']:
        strata[feature]={level:coverage([r['evaluation']['score'] for r in complete if r['prediction'][feature]==level],q) for level in ['low','high']}
    return dict(attempts=len(rows),complete=len(complete),abstentions=len(rows)-len(complete),
        statuses={status:sum(r['evaluation']['status']==status for r in rows) for status in sorted(set(r['evaluation']['status'] for r in rows))},
        simultaneous=coverage([r['evaluation']['score'] for r in complete],q),
        scores=stats([r['evaluation']['score'] for r in complete]),arms=arms,strata=strata,
        outside_development_range=sum(r['prediction']['outside_development_range'] for r in complete))
def analyze(calibration,test,frozen):
    assert frozen['status']=='FROZEN';q=frozen['quantile']
    summaries={phase:phase_summary(rows,q) for phase,rows in [('calibration',calibration),('test',test)]}
    enough=all(x['complete']>=cfg()['minimum_complete'] for x in summaries.values())
    return dict(decision='INVARIANT_CALIBRATION_COMPLETED' if enough else 'HOLD',
        holds=['HOLD_EMBEDDING_COVARIANCE','HOLD_PHASE3','METADATA_HOLD'],
        development=model(),calibration_rule=frozen,phases=summaries,
        interpretation='Calibrated marginal invariant prediction sets; covariance shape screened separately. No validated conditional coordinate covariance, geometry correction or 4D transfer.')
def main():
    _,cal=load_phase('calibration');_,test=load_phase('test')
    out=analyze(cal,test,json.loads((HERE/'frozen_calibration.json').read_text()))
    write(HERE/'results/summary.json',out)
    print(json.dumps(dict(decision=out['decision'],test=out['phases']['test']['simultaneous'],
        screens={a:v['covariance_screen'] for a,v in out['phases']['test']['arms'].items()})))

if __name__=='__main__':main()
