"""Verify the frozen package and reproduce its scientific JSON in isolation."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
RESULTS = ('BOUNDS_128.json', 'BOUNDS_192.json', 'CHECKS.json')


def verify_hashes():
    count = 0
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        path = HERE / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise AssertionError(f'Package hash mismatch: {name}')
        count += 1
    return count


def main():
    count = verify_hashes()
    with tempfile.TemporaryDirectory(prefix='cspp-v018-') as temp:
        root = Path(temp)
        for name in ('bounds.py', 'verify.py', 'PROTOCOL.json', 'PROVENANCE.json'):
            shutil.copy2(HERE / name, root / name)
        shutil.copytree(HERE / 'evidence', root / 'evidence')
        (root / 'results').mkdir()
        for args in (['bounds.py', '--bits', '128'], ['bounds.py', '--bits', '192'], ['verify.py']):
            run = subprocess.run([sys.executable, *args], cwd=root, text=True, capture_output=True)
            if run.returncode:
                raise RuntimeError(f'{args}:\n{run.stdout}\n{run.stderr}')
        for name in RESULTS:
            expected = json.loads((HERE / 'results' / name).read_text())
            actual = json.loads((root / 'results' / name).read_text())
            if actual != expected:
                raise AssertionError(f'Scientific JSON differs: {name}')
        print(json.dumps({'status': 'PASS', 'package_hashes': count,
                          'exact_scientific_reproductions': list(RESULTS),
                          'precision_overlaps': actual['precision_overlaps'],
                          'negative_controls': actual['negative_controls'],
                          'METHOD': 'HOLD', 'G1': 'HOLD'}, indent=2))


if __name__ == '__main__':
    main()
