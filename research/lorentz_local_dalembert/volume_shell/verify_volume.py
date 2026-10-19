"""Full numerical replay; coordinate byte equality is a separate reported fact."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from volume_common import HERE,ROOT,config,sources,encode,compare
from volume_controls import check
from volume_analysis import load,summarize
from run_volume import run_cloud


def verify(directory):
    contract,cfg=config();e,rows=load(directory)
    assert sources()==e['source_sha256'],'local frozen-source mismatch'
    for path,digest in sources().items():
        data=subprocess.check_output(['git','show',e['source_commit']+':'+path],cwd=ROOT)
        assert hashlib.sha256(data).hexdigest()==digest,'public source mismatch '+path
    controls=check();expected=json.loads((directory/'summary.json').read_text())
    assert expected['complete'] and expected['budget_pass'] and expected['algebra_pass']
    compare(expected,summarize(directory));exact=0
    with tempfile.TemporaryDirectory(prefix='bk-volume-') as tmp:
        p=Path(tmp);copy=dict(e,records=[])
        for row in rows:
            actual=run_cloud(row['rho'],row['seed'],cfg,relabel=row['relabel_pass'] is not None)
            data=encode(actual);compare(row,json.loads(data));exact+=row['coordinates_sha256']==actual['coordinates_sha256']
            name=f"rho-{row['rho']}-seed-{row['seed']}.json";(p/name).write_text(data)
            copy['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()))
        (p/'execution.json').write_text(json.dumps(copy));compare(expected,summarize(p))
    return dict(status='PASS_NUMERICAL_REPLAY',clouds=len(rows),coordinate_hashes_equal=exact,
                relation_and_discrete_outputs_exact=True,controls=controls,tolerance=contract['replay_tolerance'],
                decision=expected['decision'],phase3='HOLD_PHASE3',
                note='Coordinate byte equality is separate from numerical replay; no external replication claim.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE/'results');a=p.parse_args()
    print(json.dumps(verify(a.directory),indent=2))
