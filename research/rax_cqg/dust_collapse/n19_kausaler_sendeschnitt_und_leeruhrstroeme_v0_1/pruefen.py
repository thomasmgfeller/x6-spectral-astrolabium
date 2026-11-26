"""Offline reproduction of the archived baseline and the three new calculations."""
from hashlib import sha256
import json
import subprocess
import sys

from vorstudie import ROOT, inputs
import schnitt, fortsetzung, anschluss, audit_schnitt


def check(name,data):
    assert (ROOT/name).read_bytes()==(json.dumps(data,indent=2,sort_keys=True)+'\n').encode(),name


def main():
    if not __debug__:
        raise SystemExit('Run without -O.')
    for name in ('SHA256SUMS','Pruefplan.sha256','Anschlussplan.sha256'):
        for row in (ROOT/name).read_text().splitlines():
            digest,path = row.split('  ',1)
            assert sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    with inputs() as (device,early):
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=device,check=True)
        structure = schnitt.run()
        states = fortsetzung.run(early)
        required = anschluss.run()
        check('Schnitt.json',structure)
        check('Fortsetzungen.json',states)
        check('Anschluss.json',required)
        check('Gegenrechnung.json',audit_schnitt.run(structure,states,required))
    print('PASS: 121 N19 cuts, native cut action and vacuum clock closure.')
    print('PASS: two signed density sources, fixed collars and frozen-prefix completions.')
    print('PASS: necessary first-cut currents, causal-order and rational-variation checks.')
    print('Physical P3 checkpoints: 60 NOT_RUN.')


if __name__ == '__main__':
    main()
