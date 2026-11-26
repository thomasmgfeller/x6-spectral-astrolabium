"""Reproduce every supplied report and the authenticated offline baseline."""
from hashlib import sha256
import json
import subprocess
import sys

from grunddaten import ROOT,inputs
import auslesetest
import gegenversuch
import schwachtest
import traeger


def check_file(name,report):
    exact=(json.dumps(report,indent=2,sort_keys=True)+'\n').encode()
    assert exact==(ROOT/name).read_bytes(),name
    print('PASS',name)


def main():
    if not __debug__:
        raise SystemExit('Python ohne -O starten.')
    for manifest in [ROOT/'SHA256SUMS',*sorted(ROOT.glob('*.sha256'))]:
        for line in manifest.read_text().splitlines():
            digest,name=line.split('  ',1)
            assert sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    with inputs() as (base,previous,early):
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=base,check=True)
        check_file('Staubtraeger.json',traeger.run(early))
        check_file('Empfang.json',auslesetest.run(previous,early))
        check_file('Kontrollen.json',gegenversuch.run(early))
        check_file('Schwachkopplung.json',schwachtest.run(previous,early))
    print('60 physische P3-Pruefpunkte: NOT_RUN.')


if __name__=='__main__':
    main()
