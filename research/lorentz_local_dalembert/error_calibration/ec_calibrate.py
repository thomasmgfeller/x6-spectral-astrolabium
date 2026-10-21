"""SPDX-License-Identifier: Apache-2.0
Freeze the sole predeclared geometry quantile before inspecting test clouds.
"""
import json
import math
import numpy as np
from ec_common import HERE,cfg,write,sha,load_phase,source_check


def calibrate():
    source_check();c=cfg();executions,rows=load_phase('calibration')
    assert len(rows)==c['geometry_calibration_clouds']
    assert all(e['status']=='COMPLETE' and e['seconds']<=c['wall_seconds_per_worker'] and
               e['peak_mib']<=c['memory_mib_per_worker'] for e in executions)
    scales=np.asarray(json.loads((HERE/'development_fit.json').read_text())['fixed_scales'])
    scores=[]
    for row in rows:
        if row['evaluation']['status']=='COMPLETE':
            errors=np.asarray([f['error'] for f in row['evaluation']['fields']])
            scores.append(dict(index=row['index'],seed=row['seed'],score=float(np.max(np.abs(errors)/scales))))
    n=len(scores);k=math.ceil((n+1)*(1-c['geometry_miscoverage']))
    finite=n>=c['minimum_geometry_calibration_complete'] and k<=n
    q=sorted(v['score'] for v in scores)[k-1] if finite else None
    files={str(p.relative_to(HERE)):sha(p.read_bytes()) for p in sorted((HERE/'results/calibration').rglob('*')) if p.is_file()}
    return dict(status='FROZEN' if finite else 'ABSTAIN',clouds=len(rows),complete=n,
                rank=k,quantile=q,geometry_nominal_marginal_coverage=k/(n+1),
                total_nominal_marginal_coverage_lower=k/(n+1)-c['measurement_miscoverage'],
                fixed_scales=scales.tolist(),geometry_radii=(q*scales).tolist() if finite else None,
                scores=scores,calibration_files=files,
                interpretation='Simultaneous across the 16 predeclared outputs, marginal over accepted cloud and fresh calibration draws; not conditional on every cloud or the realized calibration set.')


if __name__=='__main__':
    target=HERE/'frozen_calibration.json';assert not target.exists()
    value=calibrate();write(target,value)
    print(json.dumps({k:value[k] for k in ['status','complete','rank','quantile','total_nominal_marginal_coverage_lower']}))
