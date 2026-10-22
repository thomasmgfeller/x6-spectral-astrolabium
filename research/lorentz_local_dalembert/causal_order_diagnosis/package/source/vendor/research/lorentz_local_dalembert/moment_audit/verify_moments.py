"""Replay every fresh cloud and the frozen analysis from public source hashes."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from moment_common import HERE,ROOT,config,sources,encode
from moment_controls import check,compare
from run_moments import run_cloud
from moment_analysis import load,summarize


def verify(directory):
    contract,cfg=config();execution,rows=load(directory)
    assert sources()==execution['source_sha256'],'local source hash mismatch'
    for path,digest in sources().items():
        data=subprocess.check_output(['git','show',execution['source_commit']+':'+path],cwd=ROOT)
        assert hashlib.sha256(data).hexdigest()==digest,'public source hash mismatch '+path
    controls=check();expected=json.loads((directory/'summary.json').read_text())
    assert expected['complete'] and expected['budget_pass'] and expected['algebra_pass']
    compare(expected,summarize(directory));exact=0
    with tempfile.TemporaryDirectory(prefix='bk-moments-') as tmp:
        p=Path(tmp);re=dict(execution,records=[])
        for row in rows:
            actual=run_cloud(row['rho'],row['seed'],cfg);data=encode(actual)
            compare(row,json.loads(data));exact+=row['coordinates_sha256']==actual['coordinates_sha256']
            name=f"rho-{row['rho']}-seed-{row['seed']}.json";(p/name).write_text(data)
            re['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()))
        (p/'execution.json').write_text(json.dumps(re));compare(expected,summarize(p))
    return dict(status='PASS_NUMERICAL_REPLAY',clouds=len(rows),coordinate_hashes_equal=exact,
                relation_and_discrete_outputs_exact=True,controls=controls,tolerance=contract['replay_tolerance'],
                decision=expected['decision'],phase3='HOLD_PHASE3',note='Numerical replay is not external replication.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE/'results');a=p.parse_args()
    print(json.dumps(verify(a.directory),indent=2))
