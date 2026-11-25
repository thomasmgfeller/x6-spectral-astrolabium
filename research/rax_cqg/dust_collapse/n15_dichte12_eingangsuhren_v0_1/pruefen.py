"""Run from an unpacked offline copy with Python 3.10 or later."""
import hashlib
import json
from pathlib import Path
from versuch import run
from gegenrechnung import check

ROOT=Path(__file__).resolve().parent

def sha256(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def verify():
    manifest={}
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert name not in manifest and sha256(name)==digest, name
        manifest[name]=digest
    for name,record in json.loads((ROOT/'Herkunft.json').read_text())['files'].items():
        assert manifest[name]==record['sha256'], name
    expectation=json.loads((ROOT/'ergebnisse.json').read_bytes())
    assert run()==expectation
    floating=check(expectation)
    saved=json.loads((ROOT/'quadratur.json').read_text())
    assert saved.keys()==floating.keys()
    for rho,rows in floating.items():
        for grid,values in rows.items():
            for key,x in values.items():
                assert abs(x-saved[rho][grid][key])<5e-14
    p3=json.loads((ROOT/'quellen/basis/quellen/p3.json').read_text())
    assert len(p3)==60 and all(r['checkpoint_id']=='P3' and r['execution']=='NOT_RUN' for r in p3)
    print('PASS · beide Paketpaare, sechs Gewichte, alle 16 N16-Ideale, 576 Wirkungsvergleiche, beide Dichtezentren, zwei Kontrollgitter, SHA-256.')
    print('P3 · 60 archivierte Einträge NOT_RUN.')

if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Ohne die Python-Option -O starten, damit alle Prüfungen laufen.')
    verify()
