"""Compare exact outputs exactly, numerical arrays within a declared tolerance."""
import gzip
import json
import math
from pathlib import Path
import sys

EXACT = ['candidate_ledger.json.gz', 'selection.json.gz', 'support.json', 'summary.json', 'verification.json']
NUMERICAL = ['selected_records.json.gz', 'evaluation.json.gz']


def read(path):
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes())


def close(a, b, path=''):
    if isinstance(a, float) or isinstance(b, float):
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float)) and
                math.isfinite(a) and math.isfinite(b) and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)):
            raise ValueError('numerical mismatch '+path)
    elif isinstance(a, dict):
        if not isinstance(b, dict) or a.keys() != b.keys():
            raise ValueError('key mismatch '+path)
        for k in a:
            close(a[k], b[k], path+'/'+k)
    elif isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b):
            raise ValueError('length mismatch '+path)
        for i, (x, y) in enumerate(zip(a, b)):
            close(x, y, path+'/'+str(i))
    elif a != b:
        raise ValueError('exact mismatch '+path)


def compare(a, b):
    for name in EXACT:
        if read(a/name) != read(b/name):
            raise ValueError('exact mismatch '+name)
    for name in NUMERICAL:
        close(read(a/name), read(b/name), name)
    print('PASS: exact outputs agree; numerical arrays meet atol=rtol=1e-9')


if __name__ == '__main__':
    compare(Path(sys.argv[1]), Path(sys.argv[2]))
