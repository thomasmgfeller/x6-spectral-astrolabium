"""Replay every cloud, retaining strict inherited baseline checks."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
import numpy as np
from im_common import HERE,ROOT,config,sources,encode,compare
from im_controls import check
from im_analysis import load,summarize,validate_record
from run_intrinsic import run_cloud

SKIP={'seconds','peak_mib','coordinates_sha256','iterations','transform','features','design'}

def calibrated_compare(expected,actual,tolerance,path='root'):
    if isinstance(expected,dict):
        assert isinstance(actual,dict) and expected.keys()==actual.keys(),path
        for key in expected:
            if key not in SKIP:calibrated_compare(expected[key],actual[key],tolerance,path+'.'+key)
    elif isinstance(expected,list):
        assert len(expected)==len(actual),path
        for i,(a,b) in enumerate(zip(expected,actual)):calibrated_compare(a,b,tolerance,path+f'[{i}]')
    elif isinstance(expected,float):
        assert np.isfinite(expected) and np.isfinite(actual),path
        assert abs(expected-actual)<=tolerance['atol']+tolerance['rtol']*abs(expected),path
    else:assert expected==actual,path

def verify(directory):
    c,cfg=config();e,rows=load(directory)
    assert sources()==e['source_sha256'],'local frozen-source mismatch'
    for path,digest in sources().items():
        assert hashlib.sha256(subprocess.check_output(['git','show',e['source_commit']+':'+path],cwd=ROOT)).hexdigest()==digest,'public source mismatch '+path
    controls=check();expected=json.loads((directory/'summary.json').read_text())
    assert expected['complete'] and expected['budget_pass'] and expected['controls_pass'] and expected['certificates_pass']
    calibrated_compare(expected,summarize(directory),c['calibration_replay_tolerance']);exact=calibrations=0
    with tempfile.TemporaryDirectory(prefix='bk-intrinsic-') as tmp:
        p=Path(tmp);copy=dict(e,records=[])
        for row in rows:
            assert validate_record(row,c)
            actual=run_cloud(row['rho'],row['seed'],cfg,c,controls=row['cloud_controls'] is not None)
            actual=json.loads(encode(actual));assert validate_record(actual,c)
            compare(row['selection'],actual['selection']);compare(row['arms']['volume_shell'],actual['arms']['volume_shell'])
            calibrated_compare(row,actual,c['calibration_replay_tolerance']);exact+=row['coordinates_sha256']==actual['coordinates_sha256']
            calibrations+=sum(q is not None for q in [row['inference'].get('calibration'),row['coordinate_oracle']])
            data=encode(actual);name=f"rho-{row['rho']}-seed-{row['seed']}.json";(p/name).write_text(data)
            copy['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()))
        (p/'execution.json').write_text(json.dumps(copy));calibrated_compare(expected,summarize(p),c['calibration_replay_tolerance'])
    return dict(status='PASS_NUMERICAL_REPLAY',clouds=len(rows),coordinate_hashes_equal=exact,calibrations=calibrations,
        discrete_structure_landmarks_and_adoption_exact=True,controls=controls,
        baseline_tolerance=c['baseline_replay_tolerance'],calibration_tolerance=c['calibration_replay_tolerance'],
        decision=expected['decision'],phase3='HOLD_PHASE3',
        note='Every stored and recomputed calibration checked. Eigenvector sign choices and iterations are not observables; invariant features, objectives and unique weights are compared. Coordinate byte hashes are separate.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE/'results');a=p.parse_args()
    print(json.dumps(verify(a.directory),indent=2))
