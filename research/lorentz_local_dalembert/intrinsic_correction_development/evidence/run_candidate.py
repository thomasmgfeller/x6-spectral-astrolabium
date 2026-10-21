"""Compute and seal inference BEFORE an independent evaluator sees field truth."""
import hashlib
import json
import os
import platform
import time
from pathlib import Path
import numpy as np
import scipy
from intrinsic_correction import correct

HERE = Path(__file__).resolve().parent


def main():
    contract = json.loads((HERE/'contract.json').read_text())
    data = json.loads((HERE/'intrinsic_inputs.json').read_text())
    out = HERE/'inference.json'
    if out.exists():
        raise SystemExit('Refuse to overwrite inference evidence')
    rows = []
    start = time.monotonic()
    for row in data['records']:
        entry = {k:row[k] for k in ['phase', 'index', 'seed', 'status']}
        if row['status'] == 'COMPLETE':
            try:
                entry['correction'] = correct(row, contract['solver'])
            except Exception as exc:
                entry['correction'] = dict(status='ERROR', reason=repr(exc))
        rows.append(entry)
        (HERE/'inference.partial.json').write_text(json.dumps(rows, indent=2)+'\n')
        print(row['phase'], row['index'], entry.get('correction', {}).get('status', row['status']), flush=True)
    result = dict(records=rows, seconds=time.monotonic()-start,
                  versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__),
                  source_hashes={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in
                                 ['intrinsic_correction.py', 'run_candidate.py', 'contract.json', 'intrinsic_inputs.json']})
    out.write_text(json.dumps(result, indent=2)+'\n')
    (HERE/'inference_seal.json').write_text(json.dumps(dict(sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
           statement='All candidate weights computed before archived truth evaluation in this run.'), indent=2)+'\n')


if __name__ == '__main__':
    main()
