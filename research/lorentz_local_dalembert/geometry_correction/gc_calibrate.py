"""SPDX-License-Identifier: Apache-2.0"""
import json
import math
from gc_common import HERE,cfg,load_phase,source_check,write

def calibrate(rows):
    accepted=[r for r in rows if r['evaluation']['status']=='COMPLETE'];n=len(accepted)
    k=math.ceil((n+1)*(1-cfg()['alpha']))
    if n<cfg()['minimum_complete'] or k>n:return dict(status='HOLD',complete=n,rank=k)
    variants={}
    for name in cfg()['variants']:
        scores=sorted(r['evaluation']['variants'][name]['score'] for r in accepted)
        variants[name]=dict(quantile=scores[k-1],scores=scores)
    return dict(status='FROZEN',attempts=len(rows),complete=n,rank=k,variants=variants,
        marginal_joint_coverage_bound_per_variant=k/(n+1),
        scope='Per fixed variant: all invariant intervals, Gram entries and block means of a new accepted cloud; no coordinate covariance or joint claim across variants.')
def main():
    source_check();assert not (HERE/'frozen_calibration.json').exists()
    executions,rows=load_phase('calibration')
    assert len(rows)==cfg()['clouds_per_phase'] and all(e['status']=='COMPLETE' for e in executions)
    out=calibrate(rows);write(HERE/'frozen_calibration.json',out)
    print(json.dumps({k:v for k,v in out.items() if k!='variants'}))
    print(json.dumps({k:v['quantile'] for k,v in out.get('variants',{}).items()}))
if __name__=='__main__':main()
