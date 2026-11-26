"""Reproduce both the inherited study and the new measurement study offline."""
from hashlib import sha256
import json
import subprocess
import sys

from geraeteaudit import run as audit
from studie import run as study
from vorlage import ROOT, reference


def check_results(name, data):
    encoded = (json.dumps(data,indent=2,sort_keys=True)+'\n').encode()
    assert (ROOT/name).read_bytes() == encoded, name


def main():
    if not __debug__:
        raise SystemExit('Run without -O.')
    for name in ('SHA256SUMS','Pruefplan.sha256','Kopplung.sha256'):
        for row in (ROOT/name).read_text().splitlines():
            expected,path = row.split('  ',1)
            assert sha256((ROOT/path).read_bytes()).hexdigest() == expected,path
    with reference() as source:
        subprocess.run([sys.executable,'-B','pruefen.py'],check=True,cwd=source)
        results = study(source)
        check_results('Register.json',results)
        check_results('Gegenrechnung.json',audit(source,results))
    print('PASS: five coupled stationary states, shared early readouts and sender controls.')
    print('PASS: eighteen exact instrument checks and weak-coupling scaling.')
    print('Physical P3 checkpoints: 60 NOT_RUN.')


if __name__ == '__main__':
    main()
