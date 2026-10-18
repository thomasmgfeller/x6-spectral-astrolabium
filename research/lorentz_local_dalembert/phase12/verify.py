"""Replay every held-out seed and recompute the decision; no success laundering."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import numpy as np
import analyze
import core
import experiment
import tests


def compare(expected, actual, path='root'):
    if isinstance(expected,dict):
        assert expected.keys()==actual.keys(),path
        for key in expected:
            if key in ['seconds','peak_mib','coordinates_sha256']: continue
            compare(expected[key],actual[key],path+'.'+key)
    elif isinstance(expected,list):
        assert len(expected)==len(actual),path
        for i,(a,b) in enumerate(zip(expected,actual)): compare(a,b,path+f'[{i}]')
    elif isinstance(expected,float):
        assert np.isfinite(expected) and np.isfinite(actual),path
        assert abs(expected-actual)<=1e-10+1e-9*abs(expected),path
    else:
        assert expected==actual,path


def main():
    directory=core.HERE/'results'
    execution,records=analyze.load(directory)
    root=core.HERE.parents[2]
    for name,digest in execution['source_sha256'].items():
        path=core.HERE/name
        assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,'local frozen source '+name
        data=subprocess.check_output(['git','show',execution['source_commit']+':'+str(path.relative_to(root))],cwd=root)
        assert hashlib.sha256(data).hexdigest()==digest,'public frozen source '+name
    controls=tests.check()
    try: compare({'probe':1.},{'probe':1.0001})
    except AssertionError: pass
    else: raise AssertionError('mutation guard failed')
    cfg=json.loads((core.HERE/'contract.json').read_text())
    exact_coordinates=0
    with tempfile.TemporaryDirectory(prefix='x6-bk-replay-') as temporary:
        replaydir=Path(temporary); replay_execution=dict(execution,records=[])
        for original in records:
            generated=experiment.run_cloud(original['rho'],original['seed'],cfg,relabel='relabel_pass' in original['evaluation'])
            # JSON round trip normalizes numpy scalar / arrays to ordinary types.
            from run import plain
            data=json.dumps(generated,default=plain,allow_nan=False,separators=(',',':'))+'\n'
            generated=json.loads(data)
            compare(original,generated)
            exact_coordinates+=original['coordinates_sha256']==generated['coordinates_sha256']
            name=f"rho-{generated['rho']}-seed-{generated['seed']}.json"
            (replaydir/name).write_text(data)
            replay_execution['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()))
        (replaydir/'execution.json').write_text(json.dumps(replay_execution))
        actual=analyze.summarize(replaydir)
        expected=json.loads((directory/'summary.json').read_text())
        compare(expected,actual)
    print(json.dumps(dict(status='PASS_NUMERICAL_REPLAY',clouds=len(records),coordinate_hashes_equal=exact_coordinates,
                          relation_and_discrete_outputs_exact=True,controls=controls,decision=actual['decision'],
                          tolerance='absolute 1e-10 + relative 1e-9; coordinate hashes reported separately'),indent=2))

if __name__=='__main__': main()
