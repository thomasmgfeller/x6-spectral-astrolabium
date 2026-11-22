"""Apply the previously fixed source and both window choices to the marked unit mass."""
import hashlib,json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from instrument import spectrum
ROOT=Path(__file__).resolve().parent

def evaluate(case):
    sector,m,rho,gate=case;old=json.loads((ROOT/'quellen/eichung.json').read_bytes());prior=json.loads((ROOT/'quellen/transfer.json').read_bytes());digest=(ROOT/'eichung_streng.sha256').read_text().split()[0];src=(ROOT/'eichung_streng.json').read_bytes();assert hashlib.sha256(src).hexdigest()==digest
    cal=json.loads(src);levels={}
    for n,k in ((3,4),(4,8),(5,10)):
        reading=spectrum(sector,m,rho,gate,n,k)
        levels[f'{n}x{k}']={key:reading[key] for key in ('raw','min_modulus','max_relative_angle')}
    assert reading['max_relative_angle']<1 and reading['min_modulus']>0
    key=('1/8' if rho==.125 else '1/4')+'|'+sector+'|'+str({.25:'1/4',1:1,0:0}[m]);ref=prior[key]
    if gate in ('open','wide'):
        assert abs(reading['raw']-ref['raw'])<1e-7
        assert max(abs(complex(*v)-complex(*ref['levels']['5x10']['complex_kernels'][label])) for label,v in reading['kernels'].items())<1e-12
    if sector=='vacuum':assert max(abs(v[1]) for v in reading['kernels'].values())<1e-15 and abs(reading['raw'])<1e-12
    if gate=='strict' and sector in ('positive','empty'):
        cc=spectrum(sector,m,rho,gate,5,9,'cc');alt={a:cc[a] for a in ('raw','min_modulus','max_relative_angle')}
    else:alt=None
    if gate=='strict':assert all(lobe[1]==0 for tag,lobe in reading['admitted_by_lobe'].items() if tag[0] in 'AB')
    value=reading['raw'];return key+'|'+gate,{'levels':levels,'cc_check':alt,'fine':reading,
       'with_original_calibration':float(old['gain'])*(value-float(old['offset'])),
       'strict_recalibrated':(float(cal['gain'])*(value-float(cal['offset']))) if gate=='strict' and cal['positive_local_calibration'] else None}

def run():
    cases=[(s,m,r,g) for s,m in [('positive',1),('positive',.25),('empty',0),('vacuum',0)] for r in (.125,.25) for g in ('open','wide','strict')]
    with ProcessPoolExecutor(max_workers=3) as pool:return dict(pool.map(evaluate,cases))
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
