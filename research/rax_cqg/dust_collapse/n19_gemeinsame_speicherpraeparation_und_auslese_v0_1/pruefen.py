"""Reproduce the pinned archive followed by all four exact local reports."""
from hashlib import sha256
import json
import subprocess
import sys

from archiv import ROOT,inputs
import ensemble
import ein_zustand
import kontrollen
import praeparation


def check_report(name,result):
    data=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    assert (ROOT/name).read_bytes()==data,name
    print('PASS',name)


def main():
    if not __debug__:
        raise SystemExit('Python ohne -O starten.')
    for path in [ROOT/'SHA256SUMS',*sorted(ROOT.glob('*.sha256'))]:
        for line in path.read_text().splitlines():
            hash_value,name=line.split('  ',1)
            assert sha256((ROOT/name).read_bytes()).hexdigest()==hash_value,name
    with inputs() as (baseline,prev,early):
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=baseline,check=True)
        check_report('Praeparation.json',praeparation.run())
        check_report('Klassifikation.json',ensemble.run(prev,early))
        check_report('GleichePraeparation.json',ein_zustand.run(prev,early))
        check_report('Gegenproben.json',kontrollen.controls(prev,early))
    print('60 physische P3-Pruefpunkte: NOT_RUN.')


if __name__=='__main__':
    main()
