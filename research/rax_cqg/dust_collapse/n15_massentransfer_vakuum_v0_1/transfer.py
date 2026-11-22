"""Apply the frozen calibration to prespecified reference preparations."""
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from antwort import spectrum

ROOT=Path(__file__).resolve().parent

def frozen():
    digest,name=(ROOT/'eichung.sha256').read_text().split()
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
    return json.loads((ROOT/name).read_text())

def evaluate(args):
    m,rho,sector=args
    cal=frozen()
    rows={}
    for n,k in ((3,4),(4,8),(5,10)):
        runs=spectrum(float(m),float(rho),sector,n,k)
        rows[f'{n}x{k}']=runs if n==5 else {key:runs[key] for key in ('raw','min_modulus')}
    coarse=rows['4x8'];fine=rows['5x10'];raw=fine['raw']
    assert abs(raw-coarse['raw'])<1e-8 and fine['min_modulus']>0
    estimate=float(cal['gain'])*(raw-float(cal['offset']))
    result={'levels':rows,'raw':raw,'calibrated':estimate}
    if m:
        err1=(raw/float(m)-1);err2=(estimate/float(m)-1)
        result.update(raw_relative_error=err1,calibrated_relative_error=err2,
                      raw_within_2pct_numerical=abs(err1)<=.02,calibrated_within_2pct_numerical=abs(err2)<=.02)
    if m==4:
        basis=json.loads((ROOT/'quellen/referenz.json').read_text())
        assert abs(raw-basis[str(rho)]['fine_grid_at_h_1_over_8']['all_clock_mass'])<1e-8
    return f'{rho}|{sector}|{m}',result

def sweep():
    cases=[(m,r,s) for r in (Q(1,8),Q(1,4)) for s,ms in [
        ('vacuum',[0]),('empty',[0]),('limit',[0]),('positive',[Q(1,64),Q(1,8),Q(1,4),Q(1,2),Q(1),Q(4)])] for m in ms]
    with ProcessPoolExecutor(max_workers=3) as pool:
        return dict(pool.map(evaluate,cases))

if __name__=='__main__':
    print(json.dumps(sweep(),indent=2,sort_keys=True))
