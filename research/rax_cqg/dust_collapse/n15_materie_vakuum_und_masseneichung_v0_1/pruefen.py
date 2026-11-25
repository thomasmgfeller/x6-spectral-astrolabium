"""Verify the package using Python 3.10+ and the standard library."""
import hashlib
import json
from math import isclose
from pathlib import Path
import sys

import n15
import klassik
import symmetrie
import sattel

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result():
    if not __debug__:
        raise SystemExit("Bitte Python ohne -O starten.")
    for name, source in json.loads((ROOT/'Herkunft.json').read_text())['inputs'].items():
        path=ROOT/name
        assert digest(path)==source['sha256'],name
    assert digest(ROOT/'Pruefplan.md')==(ROOT/'Pruefplan.sha256').read_text().split()[0]
    assert digest(ROOT/'Zusatzplan.md')==(ROOT/'Zusatzplan.sha256').read_text().split()[0]
    return {'stationary_null_sectors':sattel.run(),'finite_action':n15.run(),'order_symmetry_follow_up':symmetrie.run(),
            'classical_surface':klassik.radius_test(),'classical_mass':klassik.mass_test(),
            'physical_CST':n15.physical_status()}


def compare(a,b):
    if isinstance(a,dict):
        return isinstance(b,dict) and a.keys()==b.keys() and all(compare(a[k],b[k]) for k in a)
    if isinstance(a,list):
        return isinstance(b,list) and len(a)==len(b) and all(compare(x,y) for x,y in zip(a,b))
    if isinstance(a,float):
        return isinstance(b,(float,int)) and isclose(a,b,rel_tol=2.e-12,abs_tol=1.e-12)
    return a==b


if __name__=="__main__":
    data=json.dumps(result(),indent=2,ensure_ascii=False,allow_nan=False)
    if sys.argv[1:]==['--json']:
        print(data)
    elif len(sys.argv)==1:
        assert compare(json.loads(data),json.loads((ROOT/'Ergebnisse.json').read_text()))
        print('PASS: endliche Wirkung, stationäre Nullatomsektoren, Ordnungs-Symmetrie, dynamischer Rand, Referenz-Eichung.')
        print('Physischer CST-P3-Lauf: HOLD_NOT_ELIGIBLE; 60 x NOT_RUN.')
    else:
        raise SystemExit('Aufruf: python -B pruefen.py [--json]')
