"""Reproduce the archived baseline and all N19 detector results offline."""
import sys
sys.dont_write_bytecode=True
from hashlib import sha256
import json
from vorstudie import ROOT, inputs
from sonden import analyse
from gegenrechnung import check
from feldkraft import run as force


def compare(name,data):
    expected=(json.dumps(data,indent=2,sort_keys=True)+'\n').encode()
    assert (ROOT/name).read_bytes()==expected,name


def main():
    for name in ('SHA256SUMS','Pruefplan.sha256','Kraftplan.sha256'):
        for line in (ROOT/name).read_text().splitlines():
            digest,item=line.split('  ',1)
            assert sha256((ROOT/item).read_bytes()).hexdigest()==digest,item
    ref=json.loads((ROOT/'Quellen.json').read_bytes())
    for path,item in ref['files'].items():
        assert sha256((ROOT/path).read_bytes()).hexdigest()==item['sha256'],path
    assert ref['files']['basis/Pulsvergleich.zip']['sha256']=='f59cd7bef25a707c797caefcc8a5336514de373a259ab047635cfb945fd9d1a2'
    with inputs(replay=True) as (bg,select,matrices,archived):
        compare('Ergebnisse.json',analyse(bg,select,matrices))
        compare('Gegenrechnung.json',check(bg,select,matrices,archived))
        compare('Feldkraft.json',force(bg,select,matrices))
    print('PASS: two unconstrained endpoint probes, 8 apparatus arms, stored readout, 225 transfer entries.')
    print('PASS: four kinetic steps, 32 force controls, symplectic maps, Gaussian bands and covariance ranks.')
    print('Physical P3 checkpoints: 60 NOT_RUN.')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O.')
    main()
