"""Replay the archived groundwork, exact constructions and uniform bounds."""
from hashlib import sha256
import json
import subprocess
import sys
from grundlage import ROOT,inputs
import amplitude,fenster,gegenprobe_bilanz


def compare(name,value):
    expected=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
    assert (ROOT/name).read_bytes()==expected,name


def main():
    if not __debug__:
        raise SystemExit('Run without -O.')
    for name in ('SHA256SUMS','Pruefplan.sha256','Eichband.sha256'):
        for row in (ROOT/name).read_text().splitlines():
            digest,path=row.split('  ',1)
            assert sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    with inputs() as (previous,early):
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=previous,check=True)
        amplitudes=amplitude.run(early)
        bounds=fenster.run(early,amplitudes)
        compare('Amplituden.json',amplitudes)
        compare('Fenster.json',bounds)
        compare('Gegenprobe.json',gegenprobe_bilanz.run(bounds,amplitudes))
    print('PASS: native amplitude symmetry, 12 pulse continuations and fixed G0/G1 witnesses.')
    print('PASS: absolute calibration, calibration-free reversal bounds and crossed controls.')
    print('PASS: 18 exact action checks and 72 independent two-pulse reconstructions.')
    print('Physical P3 checkpoints: 60 NOT_RUN.')


if __name__=='__main__':
    main()
