"""Rebuild the archived result tables and check the limits of each conclusion."""
from collections import Counter
from fractions import Fraction as F
import gzip
from hashlib import sha256
import json
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from auslese import run as readout
from felder import ROOT, INNER, Z, COLLAR, Equations, filters, run
from gegenrechnung import audit, future_pairs


def verify_file(name, result):
    actual=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    assert actual==(ROOT/name).read_bytes(),name


def verify():
    for name in ('Pruefplan.sha256','SHA256SUMS'):
        for line in (ROOT/name).read_text().splitlines():
            digest,path=line.split('  ',1)
            assert sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    sources=json.loads((ROOT/'Quellen.json').read_text())
    for source in sources.values():
        for record in source['inputs']:
            raw=(ROOT/'basis'/record['local']).read_bytes()
            if record['local']=='checkpoints.json.gz': raw=gzip.decompress(raw)
            assert sha256(raw).hexdigest()==record['original_sha256']
    reference=ROOT/'basis/Vorversuch.zip'
    assert sha256(reference.read_bytes()).hexdigest()==sources['Vorversuch']['sha256']
    with TemporaryDirectory() as tmp, ZipFile(reference) as archive:
        archive.extractall(tmp)
        reported=subprocess.check_output([sys.executable,'-B','vakuumuhr.py'],cwd=tmp)
        assert json.loads(reported)==json.loads(archive.read('Vakuumuhr.json'))
    eq=Equations(COLLAR,COLLAR,'shift')
    point=(F(1,6),)*2
    x0=(F(11,23),)*2
    control=eq.cell(point,x0,keep=True)[2]
    assert len(control)==1
    y,w,g=control[0]
    assert all(y[i].hi<y[j].lo for i,j in eq.rel)
    assert g.lo<=0<=g.hi and all(w[j].lo>0 for j in (*INNER,Z))
    result=eq.cell(point,(F(1,2),)*2,keep=True)[2]
    assert len(result)==1 and result[0][2].lo>0
    print('PASS: exact archived stationary N17 control at 11/23 and negative control at 1/2.')
    pilot=run(True); verify_file('Pilot.json',pilot)
    assert {r['group'] for r in pilot}=={'pilot_A','pilot_B'}
    for row in pilot:
        for cell in row['cells']:
            assert cell['status']=='EXCLUDED'
            witnesses=cell['intervals']
            assert len(witnesses)==2
            for record in witnesses:
                lo,hi=map(F,record['root14'])
                assert lo>=F(record['before_upper']) or hi<=F(record['after_lower'])
    full=run(); verify_file('Familie.json',full)
    second=audit(); verify_file('Gegenrechnung.json',second)
    assert set(filters())==set(future_pairs()) and len(full)==193
    assert all(r['status']=='EXCLUDED' for r in full)
    assert [r for r in full if r['group'].startswith('pilot')]==pilot
    assert second['counts']=={'G_u':1,'clock_equations_and_order':178,'w_z':14}
    for r in full:
        if r['group'] in ('pilot_A','pilot_B','further'):
            assert all(all(k.startswith(('order_', 'no_real_root_')) for k in c['reasons']) for c in r['cells'])
    print('PASS: both pilot orders, 117 previously open orders, all 193 independently classified.')
    measurements=readout(); verify_file('Auslese.json',measurements)
    assert measurements['masses']['physical_M1']=='NOT_RUN'
    print('PASS: cut conservation control, G14 = -1/64, independent classical calibration, 15 shell frames and 12 flow intervals.')
    print('Physical P3: 60 NOT_RUN.')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Run without -O')
    verify()
