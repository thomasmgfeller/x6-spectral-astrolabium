"""Fail-closed artifact verifier; optional replay never rewrites production files."""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
import subprocess
import sys
from flint import arb
import reference as r
import audit
import run

HERE=r.HERE


def integrity():
    run.frozen();r.balls.configure(192)
    listed={}
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        audit.check(not Path(name).is_absolute() and '..' not in Path(name).parts,'safe manifest path')
        audit.check(name not in listed,'unique manifest path')
        listed[name]=digest
        audit.check(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,'file hash '+name)
    actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS'}
    audit.check(actual==set(listed),'complete package inventory')
    low=json.loads((HERE/'results/SOURCE.json').read_text());high=json.loads((HERE/'results/SOURCE_192bit.json').read_text())
    audit.compare(low,high)
    previous=json.loads((r.BASE/'results/SOURCE.json').read_text())
    union={(x['probe_index'],x['mass']) for x in previous['rows']+low['rows']}
    audit.check(union=={(i,m) for i in range(28) for m in range(3)},'all 84 probe/mass pairs')
    audit.check(len(previous['rows'])+len(low['rows'])==84,'no duplicate rows')
    dlow=json.loads((HERE/'results/DETECTOR.json').read_text());dhigh=json.loads((HERE/'results/DETECTOR_192bit.json').read_text())
    run.compare_detector(dlow,dhigh)
    for d in (dlow,dhigh):
        within=all(max(r.balls.decode(x['value']).real.rad(),r.balls.decode(x['value']).imag.rad())<arb(d['radius_goal']) for x in d['rows'])
        expected='WITHIN_RADIUS_GOAL' if within else 'ENCLOSED_BUT_SPATIAL_RADIUS_GOAL_NOT_MET'
        audit.check(d['status']==expected,'actual spatial error controls status')
        audit.check(d['E4_Dirac_detector']=='HOLD_NOT_A_SPINOR_REFERENCE','scalar detector scope')
        for row in d['rows']:
            for key in ('value','interval_cubature_core','source_edge_product_error','detector_cap_product_error'):
                audit.check(r.balls.decode(row[key]).is_finite(),'finite detector certificate')
    contract=json.loads((HERE.parent/'e4_v0_1/contract.json').read_text())
    audit.check(contract['freeze_status']=='NOT_FROZEN','E4 still unfrozen')
    for s in (low,high):
        audit.check((s['G1'],s['G2'],s['G3'])==('HOLD','NOT_RUN','NOT_RUN'),'science gates unchanged')
    result=json.loads((HERE/'results/AUDIT.json').read_text())
    audit.check(result['status']=='PASS' and result['detector']['sharp_point_containment_cases']==8,'audit complete')
    return low,dlow


def main():
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');a=p.parse_args()
    low,dlow=integrity()
    if a.replay:
        with tempfile.TemporaryDirectory(prefix='cspp-massive-replay-') as tmp:
            subprocess.run([sys.executable,'-B',str(HERE/'run.py'),'all','--out',tmp],check=True)
            audit.compare(low,json.loads((Path(tmp)/'SOURCE.json').read_text()))
            run.compare_detector(dlow,json.loads((Path(tmp)/'DETECTOR.json').read_text()))
        integrity()
    print(json.dumps({'status':'PASS','new_massive_amplitudes':50,'total_fixed_amplitudes':84,
      'scalar_spatial_detector':dlow['status'],'isolated_replay':a.replay,'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'}))

if __name__=='__main__':main()
