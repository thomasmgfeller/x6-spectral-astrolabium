"""Reproduce the reference mass-transfer study without network access."""
import argparse
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT/name).read_bytes())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def compare(a,b,path='',atol=1e-8,rtol=1e-9):
    if isinstance(a,dict):
        assert a.keys()==b.keys(),path
        for k,v in a.items():compare(v,b[k],path+'/'+k,atol,rtol)
    elif isinstance(a,list):
        assert len(a)==len(b)
        for i,v in enumerate(a):compare(v,b[i],path+'/'+str(i),atol,rtol)
    elif isinstance(a,bool):
        assert a is b,path
    elif isinstance(a,(int,float)):
        assert math.isclose(a,b,rel_tol=rtol,abs_tol=atol),(path,a,b)
    else:assert a==b,path

def audit_exact():
    from grenzen import certify
    from nullgrenze import solve
    for p,v in read('herkunft.json')['files'].items():assert digest(ROOT/p)==v['sha256'],p
    for name in ('pruefplan.sha256','eichung.sha256','aufloesungsplan.sha256','SHA256SUMS'):
        for line in (ROOT/name).read_text().splitlines():
            d,p=line.split(maxsplit=1);assert digest(ROOT/p)==d,p
    c=read('eichung.json')
    assert c['plan_sha256']==digest(ROOT/'pruefplan.txt')
    rec=read('quellen/p3.json')
    assert len(rec)==60 and all(v['checkpoint_id']=='P3' and v['execution']=='NOT_RUN' for v in rec)
    with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(ROOT/'quellen/pr355.zip') as z:
        assert z.testzip() is None
        z.extractall(tmp)
        subprocess.run([sys.executable,'-B','pruefen.py','--nur-exakt'],cwd=Path(tmp)/'Zwei_Zeiten',
                       check=True,stdout=subprocess.DEVNULL)
    rows=solve()
    assert rows==read('nullgrenze.json')
    assert certify(rows,c)==read('grenzen.json')['exact']
    print('PASS: source archive, finite stencil, two vacuum sectors, positive limits and finite exclusions.',flush=True)

def audit_numeric():
    from eichung import calibrate
    from gegenprobe import run as crosscheck
    from grenzen import noise
    from raster import run as small_masses
    from transfer import sweep
    c=read('eichung.json');repeated=calibrate()
    compare(repeated['levels'],c['levels'])
    assert all(abs(float(c[k])-float(repeated[k]))<1e-8 for k in ('offset','gain'))
    runs=sweep()
    compare(runs,read('transfer.json'))
    expected=read('raster.json');more=small_masses()
    for k,row in more.items():
        # Small absolute differences in the reconstructed mass are amplified by 1/M.
        for field in ('raw','calibrated','refinement'):
            assert abs(row[field]-expected[k][field])<1e-8
        for field in ('raw_within','calibrated_within'):assert row[field]==expected[k][field]
        m=2.**(-int(k.split('|')[1]))
        assert abs((row['relative_calibrated']-expected[k]['relative_calibrated'])*m)<1e-8
        assert abs((row['relative_raw']-expected[k]['relative_raw'])*m)<1e-8
    alt=crosscheck()
    compare(alt,read('gegenprobe.json'))
    assert max(abs(v-runs[k]['raw']) for k,v in alt.items())<1e-7
    compare(noise(runs,c),read('grenzen.json')['projected_noise'],atol=1e-14)
    for k,v in read('nullgrenze.json').items():
        y=runs[k+'|0']['raw'];lo,hi=map(Q,v['mass_interval'])
        assert float(lo)-1e-8<y<float(hi)+1e-8
    for centre in ('1/8','1/4'):
        print('M=1, centre',centre,'calibrated:',round(runs[centre+'|positive|1']['calibrated'],9))
    print('PASS: held-out masses and independent Clenshaw-Curtis comparison; 30 exploratory resolution cases.')

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Use Python without -O.')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--nur-exakt',action='store_true')
    args=ap.parse_args()
    audit_exact()
    if not args.nur_exakt:audit_numeric()
    print('Physical P3: 60 x NOT_RUN.')
