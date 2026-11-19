"""Check the archive in place; --rebuild repeats the new computations in a fresh directory."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
SEED_DIGEST = 'bc8c8c14e8fbc044c5554d233d4544d2b9607a92580b23b6fb5191a45d8f6c08'
PLAN_DIGEST = '1cf97b377c864f11ad3dac35acda4047b91a4e02a7fade2d5d640115681e097e'

def read(path):
    return json.loads(path.read_bytes())

def check(condition, message):
    if not condition:
        raise ValueError(message)

def compare(a,b,atol):
    if isinstance(b,dict):
        return a.keys() == b.keys() and all(compare(a[k],v,atol) for k,v in b.items())
    if isinstance(b,list):
        return len(a)==len(b) and all(compare(x,y,atol) for x,y in zip(a,b))
    if isinstance(b,(float,int)):
        return math.isclose(a,b,rel_tol=0,abs_tol=atol)
    return a==b

def check_data():
    check(__debug__, 'Run without -O')
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name = line.split('  ',1)
        check(Path(name).name==name and hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name)
    plan_file = ROOT/'plan.json'
    check(hashlib.sha256(plan_file.read_bytes()).hexdigest()==PLAN_DIGEST,'design')
    sample = (ROOT/'uniforms_u32le.bin').read_bytes()
    check(len(sample)==65536*8*4 and hashlib.sha256(sample).hexdigest()==SEED_DIGEST,'draws')
    design=read(plan_file)['statistical_validation']
    endpoints=119*3*2*2
    exponent=F(design['draws'])*F(design['absolute_radius_each_real_component'])**2*384
    # exp(x) exceeds each partial sum of its positive Taylor series.
    exp_lower=sum((exponent**k/math.factorial(k) for k in range(101)),F(0))
    check(2*endpoints/exp_lower<F(design['alpha_family']),'simultaneous confidence level')
    # Absolute bias from the finite-grid CDF and the midpoint clock quantization.
    delta=F(3,2*2**32)
    check(F(400,2**32*27)+F('1e-12')<F('1e-8'),'finite-grid quantization')
    check(105*16*(12*delta+4*delta**2)/27 < F('3e-7'),'continuous-clock quantization')
    from source import CACHE
    from transfer_proof import run
    result=run()
    check(compare(result,read(ROOT/'certificate.json'),2e-13),'saved rational certificate')
    check(result['deterministic_safe_states']==1100 and len(result['remaining_unconditionally_uncovered'])==117,'coverage')
    check(result['deterministic_certified_transfer_percent_down']=='4.7074','deterministic limit')
    check(result['statistical_safe_states']==1217 and result['statistical_full_transfer_fraction']=='1/20','full support')
    gates=read(CACHE/'bounds.json')['metrics']
    for tag in ('coarse','fine'):
        _,_,contrast,sign=map(F,gates[tag]['1/20'])
        check(contrast<F(1,4) and sign<1,'inherited contrast and sign at five percent')
        for d in (0,1):
            v=result['statistical_cases'][f'{tag}_{d}']
            check(F(v['floor_ratio'])>=F('0.90000454179'),'success floor')
            check(F(v['minimum_sample_projection_slack'])>0,'projection slack')
    for f in ('target.json','near_witness.json'):
        clock=read(ROOT/f)
        for k in ('4,3','5,4'):
            check(clock[k]['cartesian_error']<1e-10,'Cartesian check')
        ref=clock['48,8']['amplitudes']
        for k in ('32,6','64,10'):
            check(max(abs(complex(*a)-complex(*b)) for a,b in zip(clock[k]['amplitudes'],ref))<1e-7,'direct-clock grids')
    cont=next(iter(read(ROOT/'continuum.json').values()))['amplitudes']
    fine=read(ROOT/'target.json')['48,8']['amplitudes']
    check(max(abs(complex(*a)-complex(*b)) for a,b in zip(cont,fine))<1e-10,'continuum control')
    audit=read(ROOT/'audit.json')
    check(all(v['complex_means']==238 and v['maximum_difference']<1e-12 for v in audit.values()),'component audit')
    print('PASS — rational planes, archived clocks, 1,217 states, inherited gates and joint error budget.',flush=True)

def rebuild():
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp)
        for file in ROOT.iterdir():
            if file.suffix in ('.py','.c','.bin') or file.name in ('input_v09.zip','plan.json'):
                shutil.copyfile(file,d/file.name)
        commands=(('target.py','target.json',[]),('near_witness.py','near_witness.json',[]),
                  ('target.py','continuum.json',['--continuous']),('continuum_bound.py','continuum_bound.json',[]),
                  ('sample_clocks.py','sample.json',[]),('audit_samples.py','audit.json',[]),
                  ('witness_search.py','witness.json',[]),('transfer_proof.py','certificate.json',[]))
        for script,output,extra in commands:
            print('Rebuild',output,flush=True)
            subprocess.run([sys.executable,'-B',script,*extra,'--out',output],cwd=d,check=True)
            actual=read(d/output);saved=read(ROOT/output)
            if output=='certificate.json':
                for name in ('deterministic_safe_states','remaining_unconditionally_uncovered',
                             'statistical_full_transfer_fraction','deterministic_certified_transfer_percent_down'):
                    check(actual[name]==saved[name],name)
                for group in ('statistical_cases','deterministic_cases'):
                    for key,row in saved[group].items():
                        check(abs(F(row['floor_ratio'])-F(actual[group][key]['floor_ratio']))<F('1e-10'),key)
            elif output=='witness.json':
                for key,row in actual.items():
                    check(compare(row['radius_envelope'],saved[key]['radius_envelope'],1e-9),key)
            else:
                check(compare(actual,saved,2e-12),output)
        print('PASS — fresh replay of both direct clocks, continuum bound, all saved draws, independent audit and feasible mixtures.',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rebuild',action='store_true')
    args=ap.parse_args()
    check_data()
    if args.rebuild:
        rebuild()
