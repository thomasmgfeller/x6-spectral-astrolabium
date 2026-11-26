"""Verify source bytes, reproduce the baseline and replay the three new tests."""
from collections import Counter
from fractions import Fraction as F
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from empfang import run as receiver
from exakt import check as exact
from felder import ROOT,Box,box,SCALE
from randantwort import run as response
from vakuum import run as vacuum


def reproduce(name, result):
    assert (json.dumps(result,sort_keys=True,indent=2)+'\n').encode()==(ROOT/name).read_bytes(),name


def verify():
    for name in ('Pruefplan.sha256','Empfangsplan.sha256','SHA256SUMS'):
        for line in (ROOT/name).read_text().splitlines():
            digest,path=line.split('  ',1)
            assert sha256((ROOT/path).read_bytes()).hexdigest()==digest
    ref=ROOT/'basis/PR384.zip'
    assert sha256(ref.read_bytes()).hexdigest()=='b82b947157ad2c2ebd728e7d7abc3fc56ad066a5164b72d6398b43b822ec0b1c'
    with ZipFile(ref) as z,TemporaryDirectory() as tmp:
        for path in ('felder.py','basis/zweig.json','basis/intervall.py','basis/vorversuch.json','LICENSE','NOTICE'):
            assert z.read(path)==(ROOT/path).read_bytes()
        z.extractall(tmp)
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=tmp,check=True,stdout=subprocess.DEVNULL)
        classes=json.loads(z.read('Familie.json'))
        future={7,8,9,10}
        clock_only=[v for v in classes if not set(v['u'])<=future]
        assert len(clock_only)==178
        assert all(all(all(reason.startswith(('order_', 'no_real_root_')) for reason in cell['reasons'])
                       for cell in v['cells']) for v in clock_only)
        ledger=json.loads(gzip.decompress(z.read('basis/checkpoints.json.gz')))
        assert len(ledger)==60 and all(v['execution']=='NOT_RUN' for v in ledger)
        p=json.loads(z.read('basis/massentest.json'))['physical']
        assert p['independent_physical_calibration_pair'] is None and p['physical_vacuum_reading'] is None
    v=vacuum();reproduce('Vakuum.json',v)
    assert list(sorted(v['families'].values()))==[1,19,173]
    ex=exact();reproduce('Exakt.json',ex)
    r=response();reproduce('Randantwort.json',r)
    assert Counter(row['reason'] for row in r['uniform_collar_cases'])=={'nonpositive':11,'nonzero_Gu':4}
    # Independent field calculation compared to the exact result in Q(sqrt(937)).
    rad=box(937).sqrt_nonnegative_part()
    for k in ('epsilon','w_z'):
        a,b=map(F,ex[k])
        inner=box(a)+b*rad
        target=Box.hull(*map(F,r['controls'][3][k]))
        assert inner.intersection(target) is not None
    assert r['controls'][3]['send_positive']==r['controls'][4]['send_positive']==[16]
    assert all(not row['send_positive'] for row in r['controls'][:3])
    assert all(not row['receive_positive'] for row in r['controls'])
    assert F(r['monotonic_derivative_Gu_on_local_chart'][0])>0
    q=receiver();reproduce('Empfang.json',q)
    assert q['complete_old_clock_branches']==1 and q['ideals']==20
    cases=[x for c in q['cases'] for x in c['branches']]
    assert sum('excluded_by_order' in c for c in cases)==5
    remaining=[c for c in cases if 'D_r' in c]
    assert len(remaining)==15
    for c in remaining:
        assert c['status']=='excluded_by_density'
        for method in ('D_r','direct','expanded'):
            lo,hi=map(F,c[method])
            assert max(lo,-hi)>F(543,100)
    print('PASS — PR 384 replay, vacuum boundary conditions on 193 orders, admissible scaled matter control.')
    print('PASS — exact Q(sqrt(937)) send-time control, full matter equations, fixed-dose forward checks.')
    print('PASS — all 20 induced one-receiver pasts checked; no stationary positive receiver in its window.')
    print('Physical mass gain and shell radius unavailable; 60 physical P3 checkpoints NOT_RUN.')


if __name__=='__main__':
    if not __debug__: raise SystemExit('Run without -O')
    verify()
