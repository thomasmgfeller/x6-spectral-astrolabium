"""Reproduce the complete offline evidence from its pinned inputs."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent


def main():
    if not __debug__:
        raise SystemExit('Run without -O.')
    for name in ('SHA256SUMS','Pruefplan.sha256'):
        for row in (ROOT/name).read_text().splitlines():
            digest, filename = row.split('  ',1)
            assert sha256((ROOT/filename).read_bytes()).hexdigest() == digest, filename
    refs = json.loads((ROOT/'Quellen.json').read_bytes())
    for name, item in refs['files'].items():
        assert sha256((ROOT/name).read_bytes()).hexdigest() == item['sha256'], name
    archive = ROOT/'basis/Staubantwort.zip'
    assert sha256(archive.read_bytes()).hexdigest() == '0a76d1506cedfedfad6cd17f8f18c2a067b181fa2994b5bf25fdf4579bb622a2'
    with TemporaryDirectory() as tmp, ZipFile(archive) as z:
        z.extractall(tmp)
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=tmp,check=True)
    from frueh import run
    from gemischt import evaluate_mixed
    from gegenprobe import audit
    early, preparation = run(), evaluate_mixed()
    for name, data in [('Frueher_Zugriff.json',early),('Randpraeparation.json',preparation),
                       ('Gegenprobe.json',audit(early,preparation))]:
        expected = (json.dumps(data,indent=2,sort_keys=True)+'\n').encode()
        assert expected == (ROOT/name).read_bytes(), name
    print('PASS: same-source counterexample and causal collection sites.')
    print('PASS: relaxed two-parameter Hessian and all three mixed targets.')
    print('PASS: independent action differences, nodal equations and interval elimination.')
    print('Physical P3 checkpoints: 60 NOT_RUN.')


if __name__ == '__main__':
    main()
