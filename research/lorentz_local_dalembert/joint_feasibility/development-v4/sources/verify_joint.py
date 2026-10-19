"""Full prospective replay, separate byte evidence and algebra validation."""
import argparse
import copy
import hashlib
import json
import resource
import signal
import subprocess
import time
from pathlib import Path
import numpy as np
from jf_common import HERE, ROOT, config, sources, encode
from jf_controls import check
from jf_analysis import load, summarize, validate
from run_joint import run_cloud


def compare(a, b, tolerance, path='root'):
    if isinstance(a, dict):
        assert isinstance(b, dict) and a.keys() == b.keys(), path
        for key in a:
            # Eigenvectors may change sign; Gram/vectors and derived scalar
            # guards are compared and each certificate is algebraically checked.
            if key not in {'seconds', 'peak_mib', 'coordinates_sha256', 'selection_seal', 'transform', 'features'}:
                compare(a[key], b[key], tolerance, path+'.'+key)
    elif isinstance(a, list):
        assert len(a) == len(b), path
        for i, (x, y) in enumerate(zip(a, b)):
            compare(x, y, tolerance, path+f'[{i}]')
    elif isinstance(a, float):
        assert np.isfinite(a) and np.isfinite(b), path
        assert abs(a-b) <= tolerance['atol']+tolerance['rtol']*abs(a), path
    else:
        assert a == b, path


def verify(directory):
    c, oc, guards, cfg = config()
    execution, rows = load(directory)
    assert sources() == execution['source_sha256'], 'current source mismatch'
    for path, expected in sources().items():
        public = subprocess.check_output(['git', 'show', execution['source_commit']+':'+path], cwd=ROOT)
        assert hashlib.sha256(public).hexdigest() == expected, 'public source mismatch '+path
    controls = check()
    expected_summary = json.loads((directory/'summary.json').read_text())
    compare(expected_summary, summarize(directory), c['replay_tolerance'])
    assert expected_summary['complete'] and expected_summary['budget_pass'] and expected_summary['controls_pass'] and expected_summary['certificates_pass']
    start = time.monotonic(); exact = 0
    def timeout(signum, stack):
        raise TimeoutError('fixed replay wall budget exhausted')
    signal.signal(signal.SIGALRM, timeout); signal.alarm(c['wall_budget_seconds'])
    try:
        for row in rows:
            validate(row, c, guards)
            actual = run_cloud(row['rho'], row['seed'], c, oc, guards, cfg, do_transport=row['transport_control'] is not None)
            actual = json.loads(encode(actual))
            validate(actual, c, guards)
            compare(row, actual, c['replay_tolerance'])
            exact += row['coordinates_sha256'] == actual['coordinates_sha256']
            print(json.dumps(dict(replayed=row['seed'], rho=row['rho'], joint_pass=row['joint_pass'])), flush=True)
    finally:
        signal.alarm(0)
    elapsed = time.monotonic()-start; peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
    assert elapsed <= c['wall_budget_seconds'] and peak <= c['memory_budget_mib']
    return dict(status='PASS_FULL_JOINT_REPLAY', clouds=len(rows), exact_discrete_decisions=True,
                coordinate_hashes_equal=exact, controls=controls, seconds=elapsed, peak_mib=peak,
                decision=expected_summary['decision'], phase3='HOLD_PHASE3')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--directory', type=Path, default=HERE/'results'); p.add_argument('--output', type=Path)
    a = p.parse_args(); result = verify(a.directory); text = json.dumps(result, indent=2)+'\n'
    if a.output:
        if a.output.exists():
            raise SystemExit('Refusing to overwrite verification evidence')
        a.output.write_text(text)
    print(text)
