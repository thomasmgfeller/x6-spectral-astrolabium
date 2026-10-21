"""SPDX-License-Identifier: Apache-2.0"""
import math
from gu_common import HERE,cfg,load_phase,source_check,write

def rank(n):return math.ceil((n+1)*(1-cfg()['alpha']))
def calibrate(rows):
    accepted=[r for r in rows if r['evaluation']['status']=='COMPLETE'];n=len(accepted);k=rank(n)
    if n<cfg()['minimum_complete'] or k>n:return dict(status='HOLD',attempts=len(rows),complete=n,rank=k)
    scores=sorted(r['evaluation']['score'] for r in accepted)
    return dict(status='FROZEN',attempts=len(rows),complete=n,rank=k,quantile=scores[k-1],
        marginal_joint_coverage_bound=k/(n+1),scores=scores,
        scope='Both arms, all intervals, root Gram entries and nonempty blocks of a new COMPLETE cloud; marginal over calibration/test draws.')
def main():
    source_check();assert not (HERE/'frozen_calibration.json').exists()
    executions,rows=load_phase('calibration')
    assert len(rows)==cfg()['clouds_per_phase'] and all(e['status']=='COMPLETE' for e in executions)
    out=calibrate(rows);write(HERE/'frozen_calibration.json',out);print(out)

if __name__=='__main__':main()
