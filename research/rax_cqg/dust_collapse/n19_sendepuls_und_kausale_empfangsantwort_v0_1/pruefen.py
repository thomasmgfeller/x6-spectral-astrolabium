"""Offline verification. Run with Python 3.10 or newer."""
import sys
sys.dont_write_bytecode = True
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from gegenrechnung import audit
from ordnung import ROOT, load_background, select
from puls import run


def reproduce():
    for manifest in ('Pruefplan.sha256', 'SHA256SUMS'):
        for line in (ROOT / manifest).read_text().splitlines():
            expected, name = line.split('  ', 1)
            assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    provenance = json.loads((ROOT / 'Quellen.json').read_bytes())
    for name, item in provenance['inputs'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == item['sha256'], name
    assert sha256((ROOT / 'basis/N19.zip').read_bytes()).hexdigest() == '0b0f66e0b4b1fde995a0135c9b19dcff31853b686e2d8b73e9f28dcbf6ef347c'
    with TemporaryDirectory() as tmp, ZipFile(ROOT / 'basis/N19.zip') as archive:
        archive.extractall(tmp)
        subprocess.run([sys.executable, '-B', 'pruefen.py'], cwd=tmp, check=True)
        upstream = subprocess.check_output(
            [sys.executable, '-B', '-c',
             'from paar import CASE, relation; import json; print(json.dumps(sorted(relation(CASE))))'],
            cwd=tmp)
        assert {tuple(edge) for edge in json.loads(upstream)} == load_background().relation
    for function, filename in ((run, 'Ergebnisse.json'), (audit, 'Gegenrechnung.json')):
        out = json.dumps(function(), indent=2, sort_keys=True) + chr(10)
        assert out.encode() == (ROOT / filename).read_bytes(), filename
    bg = load_background()
    _, receiver = select(bg)
    bg.weights[receiver] = (0, 0)
    try:
        select(bg)
    except ValueError:
        pass
    else:
        raise AssertionError('reader accepted missing material receiver')
    print('PASS: source, receiver, all pulse arms, causality and two boundary-rank certificates.')
    print('PASS: 361 Hessian entries, both full 11-by-11 responses, 171 relabellings, 20 dust differences.')
    print('Physical P3 checkpoints: 60 NOT_RUN.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Please run without -O.')
    reproduce()
