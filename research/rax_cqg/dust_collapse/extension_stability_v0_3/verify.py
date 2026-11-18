"""Check the release and recompute outputs in a temporary directory, using one CPU thread."""
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent
CONTRACT_DIGESTS = {
    "study.json":"1210a638521facb7990883a55e9bbc339f5c8f4904184baa11e5ea38b8bdea62",
    "supplement.json":"9281da036a63a444868c59f06133b4a430d9f3ba74b2542897ea60e1d8c6a9cc",
}


def compare(expected, actual, path=()):
    if isinstance(expected, dict):
        assert expected.keys() == actual.keys(), path
        for k in expected:
            compare(expected[k], actual[k], (*path,k))
    elif isinstance(expected, list):
        assert len(expected) == len(actual), path
        for i, (a,b) in enumerate(zip(expected,actual)):
            compare(a,b,(*path,i))
    elif isinstance(expected, float):
        assert math.isclose(expected, actual, rel_tol=3e-8, abs_tol=5e-13), (path,expected,actual)
    else:
        assert expected == actual, (path,expected,actual)


def main():
    if not __debug__:
        raise RuntimeError("Run without Python optimization so all scientific checks execute")
    for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
        digest, relative = line.split('  ',1)
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == digest, relative
    for name, digest in CONTRACT_DIGESTS.items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE',None)
    with TemporaryDirectory() as tmp:
        clocks, results = (Path(tmp)/n for n in ('clocks_n13.json','results.json'))
        for name, args in [('compute.py',[clocks]),('analyze.py',[clocks,results])]:
            subprocess.run([sys.executable,'-B',str(ROOT/name),*args],check=True,env=env)
        for output in (clocks,results):
            compare(json.loads((ROOT/output.name).read_text()),json.loads(output.read_text()))
    print('PASS: 408 marked paths, domain audit, both exchange marginals, N13 clocks, '
          'v0.2 replay, four-outcome probabilities and weight diagnostics')


if __name__ == '__main__':
    main()
