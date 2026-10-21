"""SPDX-License-Identifier: Apache-2.0"""
import math
from gg_common import HERE,cfg,load_phase,source_check,write

def rank(n):return math.ceil((n+1)*(1-cfg()['alpha']))
def calibrate(rows):
    accepted=[r for r in rows if r['evaluation']['status']=='COMPLETE'];n=len(accepted);k=rank(n)
    if n<cfg()['minimum_complete'] or k>n:return dict(status='HOLD',attempts=len(rows),complete=n,rank=k)
    models={}
    for which in cfg()['models']:
        scores=sorted(r['evaluation']['models'][which]['score'] for r in accepted)
        models[which]=dict(quantile=scores[k-1],scores=scores)
    return dict(status='FROZEN',attempts=len(rows),complete=n,rank=k,models=models,
        marginal_joint_coverage_bound_per_model=k/(n+1),
        scope='Per model: both arms, all intervals, Gram entries and nonempty blocks of a new accepted cloud. No simultaneous claim across the two models.')
def main():
    source_check();assert not (HERE/'frozen_calibration.json').exists()
    executions,rows=load_phase('calibration')
    assert len(rows)==cfg()['clouds_per_phase'] and all(e['status']=='COMPLETE' for e in executions)
    out=calibrate(rows);write(HERE/'frozen_calibration.json',out)
    print({k:v for k,v in out.items() if k!='models'});print({k:v['quantile'] for k,v in out.get('models',{}).items()})

if __name__=='__main__':main()
