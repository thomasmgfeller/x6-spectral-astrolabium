"""Verify a fresh offline copy with Python's standard library."""
from pathlib import Path
import hashlib
import json
from registertest import run
from register_quadratur import check
from schnittoperator import verify

ROOT=Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT/name).read_text())

def compare(a,b):
    if isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:compare(a[k],b[k])
    elif isinstance(a,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):compare(x,y)
    else:
        assert abs(a-b)<4e-10

def main():
    manifest={}
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        value,name=line.split('  ',1)
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==value and name not in manifest,name
        manifest[name]=value
    for path,record in read('Herkunft.json')['files'].items():
        assert manifest[path]==record['sha256']
    result=run()
    assert result==read('ergebnisse.json')
    assert verify()==read('operator.json')
    compare(check(result),read('quadratur.json'))
    p3=read('vorstudie/basis/quellen/basis/quellen/p3.json')
    assert len(p3)==60 and all(x['checkpoint_id']=='P3' and x['execution']=='NOT_RUN' for x in p3)
    print('PASS · drei Protokolle, zwei Uhrfenster, 90 rationale Kontrollen, Schnittoperator, zwei Kontrollgitter und SHA-256. P3 · 60 NOT_RUN.')

if __name__=='__main__':
    if not __debug__:raise SystemExit('Ohne -O starten, damit die Prüfungen laufen.')
    main()
