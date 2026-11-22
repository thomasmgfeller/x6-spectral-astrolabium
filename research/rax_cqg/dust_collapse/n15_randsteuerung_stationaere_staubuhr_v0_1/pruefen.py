"""Offline verification on Python 3.10+, using only the standard library."""
import hashlib
import json
from pathlib import Path
from fractions import Fraction
import gegenpaar
import randgleichung
import stationaer
import dichteschale
import monoton
import zeitdifferenz
import kontrolle

ROOT = Path(__file__).resolve().parent

def load(name):
    return json.loads((ROOT / name).read_bytes())

def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if not __debug__:
        raise RuntimeError('Run Python without -O.')
    for p in ['SHA256SUMS','pruefplan.sha256','dichteplan.sha256','monotonieplan.sha256','kontrollplan.sha256']:
        for line in (ROOT / p).read_text().splitlines():
            digest, name = line.split(maxsplit=1)
            assert checksum(ROOT / name) == digest, name
    src=load('herkunft.json')
    assert src['commit']=='2737fc792ada1de4e2a07f139f227339497fb66c'
    for name,meta in src['files'].items():
        assert checksum(ROOT/'quellen'/name)==meta['sha256'],name
    for module in (gegenpaar,randgleichung,stationaer,dichteschale,monoton,zeitdifferenz,kontrolle):
        filename = module.__name__+'.json'
        # Use the stored rational / integer convention, including numeric dictionary keys.
        data = (json.dumps(module.run(), sort_keys=True, indent=2, default=str)+'\n').encode()
        assert data == (ROOT / filename).read_bytes(), filename
        print('PASS',filename)
    from stationaer import DELTA,S
    for duration,lo,hi in [(Fraction(15,16),Fraction(1,32),Fraction(3,32)),(Fraction(17,16),-Fraction(3,32),-Fraction(1,32))]:
        off=4*DELTA-duration
        assert lo*S<off.lo<=off.hi<hi*S
    shell = load('dichteschale.json'); assert all('0' not in data['counts'] for data in shell.values())
    assert all(not x['open_offset_intervals'] for x in load('monoton.json').values())
    # The independent enclosed gap is strictly negative throughout each outer lobe.
    for d in load('zeitdifferenz.json').values():assert Fraction(d['Y5_minus_Y4'][1])<0
    for case in load('randgleichung.json')['references'].values():
        assert {key:value['accessible_target_dimension'] for key,value in case['modes'].items()}=={
            'inlet':0,'outlet':0,'fixed_3_7':1,'fixed_7':2,'both':2}
    rows=load('quellen/p3.json')
    assert len(rows)==60 and all(r['checkpoint_id']=='P3' and r['execution']=='NOT_RUN' for r in rows)
    print('PASS: verified source bytes, calibration durations and 60 physical P3 entries marked NOT_RUN.')

if __name__=='__main__':
    main()
