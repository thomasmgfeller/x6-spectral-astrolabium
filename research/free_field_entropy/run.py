"""Verify a committed freeze and execute a resource-bounded offline worker."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def verify_freeze(source_ref):
    freeze = json.loads((HERE/'freeze.json').read_text())
    if freeze['status'] != 'BEFORE_TARGET_GENERATION':
        raise ValueError('pre-target freeze required')
    committed = subprocess.check_output(['git','show',source_ref+':research/free_field_entropy/freeze.json'],cwd=ROOT)
    if committed != (HERE/'freeze.json').read_bytes():
        raise ValueError('freeze differs from source commit')
    for rel, digest in freeze['sources'].items():
        raw = (ROOT/rel).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('changed frozen source: '+rel)
        other = subprocess.check_output(['git','show',source_ref+':'+rel],cwd=ROOT)
        if other != raw:
            raise ValueError('source commit mismatch: '+rel)
    return freeze


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--source-ref',required=True)
    args = p.parse_args()
    freeze = verify_freeze(args.source_ref)
    cfg = json.loads((HERE/'contract.json').read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output/'freeze.json').write_text(json.dumps(freeze,indent=2,sort_keys=True)+'\n')
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONHASHSEED='0')
    def limit():
        amount = cfg['budget']['memory_bytes']
        resource.setrlimit(resource.RLIMIT_AS, (amount, amount))
    start = time.monotonic()
    status, code = 'UNSET', None
    try:
        result = subprocess.run([sys.executable,'-B',str(HERE/'produce.py'),'--output',str(args.output.resolve()),
                                 '--source-ref',args.source_ref],env=env,preexec_fn=limit,timeout=cfg['budget']['wall_seconds'],check=False)
        code = result.returncode
        status = 'COMPLETED' if code == 0 else 'WORKER_FAILED'
    except subprocess.TimeoutExpired:
        status = 'BUDGET_EXCEEDED'
    finally:
        (args.output/'execution.json').write_text(json.dumps({'status':status,'returncode':code,'elapsed_seconds':time.monotonic()-start,
            'budget':cfg['budget'],'source_ref':args.source_ref},indent=2,sort_keys=True)+'\n')
    if status != 'COMPLETED':
        raise SystemExit('Incomplete cohort retained; no replacement or automatic rerun: '+status)


if __name__ == '__main__':
    main()
