"""Full target replay and source/record integrity; no external replication claim."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from common import HERE, ROOT, config, sources, encode
from audit_analysis import load, summarize
from run_audit import run_cloud
from controls import check, compare


def verify(directory):
    audit,cfg=config(); execution,records=load(directory)
    assert sources()==execution['source_sha256'],'local frozen source mismatch'
    for path,digest in execution['source_sha256'].items():
        data=subprocess.check_output(['git','show',execution['source_commit']+':'+path],cwd=ROOT)
        assert hashlib.sha256(data).hexdigest()==digest,'public frozen source mismatch '+path
    controls=check(); exact=0
    expected=json.loads((directory/'summary.json').read_text())
    assert expected['complete'] and expected['budget_pass'] and expected['algebra_pass']
    with tempfile.TemporaryDirectory(prefix='bk-anchor-replay-') as temporary:
        replay=Path(temporary); execution_copy=dict(execution,records=[])
        for row in records:
            actual=run_cloud(row['rho'],row['seed'],cfg,do_relabel=row['relabel_pass'] is not None)
            data=encode(actual); actual=json.loads(data)
            compare(row,actual)
            exact+=row['coordinates_sha256']==actual['coordinates_sha256']
            name=f"rho-{row['rho']}-seed-{row['seed']}.json"
            (replay/name).write_text(data)
            execution_copy['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()))
        (replay/'execution.json').write_text(json.dumps(execution_copy))
        generated=summarize(replay)
        # Timing is not a replay invariant. The original target's budget record
        # is retained; actual per-arm clocks appear only as descriptive outputs.
        for cell in generated['cells']:
            for method in cell['methods'].values(): method.pop('method_seconds')
        comparable=json.loads(json.dumps(expected))
        for cell in comparable['cells']:
            for method in cell['methods'].values(): method.pop('method_seconds')
        compare(comparable,generated)
    return dict(status='PASS_NUMERICAL_REPLAY',clouds=len(records),coordinate_hashes_equal=exact,
                relation_and_discrete_outputs_exact=True,controls=controls,decision=expected['decision'],
                phase3='HOLD_PHASE3',tolerance=audit['replay_tolerance'],
                note='Coordinate byte hashes reported separately; numerical replay is not external replication.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE/'results')
    a=p.parse_args();print(json.dumps(verify(a.directory),indent=2))
