"""Replay all checks in the distributed archive."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def run(stem):
    return json.loads(subprocess.check_output([sys.executable,'-B',str(ROOT/(stem+'.py'))],cwd=ROOT))


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run with active assertions.')
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Prüfsummenfehler: '+name)
    print('PASS SHA-256',flush=True)
    for name,expected in [('massenquelle','ergebnis'),('einzelpaket','einzelpaket'),('katalog','katalog')]:
        assert run(name)==json.loads((ROOT/(expected+'.json')).read_text())
        print('PASS',name,flush=True)
    result=run('gegenprobe')
    saved=json.loads((ROOT/'gegenprobe.json').read_text())
    assert len(result)==len(saved)==8
    for a,b in zip(result,saved):
        assert a.keys()==b.keys()
        for k in a:
            if k in ('mass_from_xy','pointer_visibility'):
                assert abs(a[k]-b[k])<1e-10
            else:
                assert a[k]==b[k]
    print('PASS acht unabhängige Zeigerprüfungen',flush=True)
