"""Validate an extracted copy without network or third-party dependencies."""
from hashlib import sha256
from pathlib import Path
import json
from auswertung import results
from gegenrechnung import test

ROOT=Path(__file__).resolve().parent

def validate():
    sums={}
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        value,name=line.split('  ',1)
        assert name not in sums and sha256((ROOT/name).read_bytes()).hexdigest()==value,name
        sums[name]=value
    for path,record in json.loads((ROOT/'Herkunft.json').read_text())['files'].items():
        assert sums[path]==record['sha256'],path
    r=results()
    assert r==json.loads((ROOT/'ergebnisse.json').read_text())
    fresh=test(r)
    old=json.loads((ROOT/'quadratur.json').read_text())
    def compare(a,b):
        if isinstance(a,dict):
            assert a.keys()==b.keys()
            for k in a:compare(a[k],b[k])
        else: assert abs(a-b)<4e-10
    compare(fresh,old)
    checkpoints=json.loads((ROOT/'basis/quellen/basis/quellen/p3.json').read_text())
    assert len(checkpoints)==60 and all(x['execution']=='NOT_RUN' and x['checkpoint_id']=='P3' for x in checkpoints)
    print('PASS · Summen- und Dichteschätzer auf beiden Paketen, Portwahrscheinlichkeit, Schnitttransport, Fensterkontrolle und SHA-256. P3 · 60 NOT_RUN.')

if __name__=='__main__':
    if not __debug__: raise SystemExit('Ohne -O starten, damit die Prüfungen ausgeführt werden.')
    validate()
