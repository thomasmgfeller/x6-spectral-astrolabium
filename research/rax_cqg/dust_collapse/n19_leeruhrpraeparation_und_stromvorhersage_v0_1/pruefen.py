"""Offline replay of all published inputs, new certificates and independent controls."""
from hashlib import sha256
import json
import subprocess
import sys
from referenz import ROOT,inputs
import uhrwahl,fortsetzungen,kompression,gegenrechnung


def compare(name,data):
    assert (ROOT/name).read_bytes()==(json.dumps(data,indent=2,sort_keys=True)+'\n').encode(),name


def main():
    if not __debug__:
        raise SystemExit('Run without -O.')
    for name in ('SHA256SUMS','Pruefplan.sha256','Erweiterung.sha256','Fensterplan.sha256'):
        for line in (ROOT/name).read_text().splitlines():
            expected,path=line.split('  ',1)
            assert sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    with inputs() as (cut,early):
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=cut,check=True)
        clock=uhrwahl.run(early)
        witness=fortsetzungen.run(early)
        band=kompression.run(early,witness)
        compare('Uhrwahl.json',clock)
        compare('Stromzeugen.json',witness)
        compare('Fensterschranke.json',band)
        compare('Gegenrechnung.json',gegenrechnung.audit(early,clock,witness,band))
    print('PASS: vacuum clock alternatives and externally scheduled preparation.')
    print('PASS: two calibrated pairs, including matched four momenta, eight full pulse continuations.')
    print('PASS: one-parameter reconstruction, full receiver-window bound and independent elimination.')
    print('Physical P3 checkpoints: 60 NOT_RUN.')


if __name__=='__main__':
    main()
