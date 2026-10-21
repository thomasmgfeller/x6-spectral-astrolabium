"""Full numerical replay, exact discrete decisions and separate byte evidence."""
import argparse
import copy
import hashlib
import json
import resource
import signal
import subprocess
import time
from pathlib import Path
from od_common import HERE, ROOT, config, sources, encode
from od_controls import check
from od_analysis import summarize, validate
from volume_analysis import load
from verify_intrinsic import calibrated_compare
from run_outer import run_cloud


def compare(expected, actual, tolerance):
    a, b = copy.deepcopy(expected), copy.deepcopy(actual)
    # NumPy/libm coordinate bytes can differ while order and numeric replay agree.
    for row in (a, b):
        row['frozen_inner'].pop('coordinates')
    calibrated_compare(a, b, tolerance)


def verify(directory):
    c, ic, cfg = config()
    execution, rows = load(directory)
    assert sources() == execution['source_sha256'], 'local frozen-source mismatch'
    for path, digest in sources().items():
        data = subprocess.check_output(['git', 'show', execution['source_commit']+':'+path], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == digest, 'public source mismatch '+path
    controls = check()
    summary = json.loads((directory/'summary.json').read_text())
    calibrated_compare(summary, summarize(directory), c['replay_tolerance'])
    assert summary['complete'] and summary['budget_pass'] and summary['controls_pass']
    start = time.monotonic()
    def timeout(signum, frame):
        raise TimeoutError('fixed replay wall budget exhausted')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(c['wall_budget_seconds'])
    exact = 0
    try:
        for row in rows:
            validate(row, ic)
            actual = run_cloud(row['rho'], row['seed'], c, ic, cfg,
                               controls=any(s['controls'] is not None for s in row['stages']))
            actual = json.loads(encode(actual))
            validate(actual, ic)
            compare(row, actual, c['replay_tolerance'])
            exact += sum(a['coordinates_sha256'] == b['coordinates_sha256'] for a, b in zip(row['stages'], actual['stages']))
            print(json.dumps(dict(replayed=row['seed'], rho=row['rho'])), flush=True)
    finally:
        signal.alarm(0)
    elapsed = time.monotonic()-start
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
    assert elapsed <= c['wall_budget_seconds'] and peak <= c['memory_budget_mib']
    return dict(status='PASS_NUMERICAL_REPLAY', clouds=len(rows), variants=3*len(rows),
                coordinate_hashes_equal=exact, discrete_decisions_exact=True,
                controls=controls, seconds=elapsed, peak_mib=peak,
                decision=summary['decision'], phase3='HOLD_PHASE3')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--directory', type=Path, default=HERE/'results')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    result = verify(a.directory)
    data = json.dumps(result, indent=2)+'\n'
    if a.output:
        if a.output.exists():
            raise SystemExit('Refusing to overwrite verification evidence')
        a.output.write_text(data)
    print(data)
