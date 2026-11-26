"""Replay the authenticated baseline and compare the four new reports byte for byte."""
from hashlib import sha256
import json
import subprocess
import sys

from vorgaenger import ROOT,inputs
import aufloesung
import gegenpruefung
import uhrauslese
import vergleich


def main():
    if not __debug__:
        raise SystemExit('Python ohne -O starten.')
    for name in ('SHA256SUMS','Pruefplan.sha256','Uhrkontrolle.sha256'):
        for row in (ROOT/name).read_text().splitlines():
            digest,path=row.split('  ',1)
            assert sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    with inputs() as (previous,early):
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=previous,check=True)
        reports=[('Paarvergleich.json',vergleich),('Aufloesung.json',aufloesung),
                 ('Uhrkontrolle.json',uhrauslese),('Gegenpruefung.json',gegenpruefung)]
        for name,module in reports:
            encoded=(json.dumps(module.run(previous,early),indent=2,sort_keys=True)+'\n').encode()
            assert (ROOT/name).read_bytes()==encoded,name
            print('PASS',name)
    print('60 physische P3-Pruefpunkte: NOT_RUN.')


if __name__=='__main__':
    main()
