"""Frozen fixed-budget benchmark. Run only after public source publication."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
import numpy as np
import scipy
from geometry import sample, relation, flat_density_twin_relation, oracle, require
from core import features, fit, score, assess, pack, summarize, validate

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FROZEN=['contract.json','geometry.py','core.py','run.py','verify.py','reproduce.py','selftest.py','DESIGN.md','requirements.txt']


def dump(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')


def source_hashes(commit):
    result={}
    for name in FROZEN:
        data=(HERE/name).read_bytes()
        old=subprocess.check_output(['git','show',commit+':research/lorentz_curvature/'+name],cwd=ROOT)
        require(data==old,'source differs from public freeze: '+name)
        result[name]=hashlib.sha256(data).hexdigest()
    return result


def seed_for(label,contract):
    digest=hashlib.sha256((contract['seed_namespace']+'/'+label).encode()).digest()
    return int.from_bytes(digest[:16],'big')


def record(phase,n,family,index,contract):
    label=f'{phase}/N{n}/{family["id"]}/{index:04}'
    seed=seed_for(label,contract)
    x,proposed=sample(np.random.Generator(np.random.PCG64(seed)),n,family)
    c=relation(x)
    r=dict(id=label,phase=phase,N=n,family=family['id'],seed=str(seed),proposed=proposed,
           points_sha256=hashlib.sha256(x.astype('<f8').tobytes()).hexdigest(),
           relation=pack(c),features=features(c))
    if phase=='test' and family['h']:
        twin=flat_density_twin_relation(x,family['h'])
        require(np.array_equal(c,twin),'conformal twin relation mismatch')
        require(features(twin)==r['features'],'conformal twin feature mismatch')
        r['flat_density_twin']=dict(identical_full_relation=True,identical_features=True,features=features(twin),
                                   flat_proper_time=1.,flat_scalar_curvature=0.,
                                   density='proportional to (1-h*eta)^(-4)')
    if phase=='test' and family['id']=='flat_uniform':
        witness=None
        for j in range(n):
            pred,succ=np.flatnonzero(c[:,j]),np.flatnonzero(c[j])
            if len(pred) and len(succ):
                witness=[int(pred[0]),j,int(succ[0])];break
        if witness:
            bad=c.copy();bad[witness[0],witness[2]]=False
            try: validate(bad)
            except ValueError: rejected=True
            else: rejected=False
            require(rejected,'omitted transitive relation not rejected')
            r['relation_error_control']=dict(witness=witness,status='REJECTED_INVALID_RELATION')
        else:
            r['relation_error_control']=dict(witness=None,status='NO_TWO_STEP_WITNESS')
    return r


def execute(output,source_commit):
    contract=json.loads((HERE/'contract.json').read_text())
    hashes=source_hashes(source_commit)
    output.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter()
    dump(output/'provenance.json',dict(source_commit=source_commit,source_sha256=hashes,
         started_utc=datetime.now(timezone.utc).isoformat(),python=sys.version,numpy=np.__version__,scipy=scipy.__version__,
         public_freeze_requirement='Caller confirms public commit exists before this first target invocation'))
    resource.setrlimit(resource.RLIMIT_AS,(contract['resource_limit']['address_space_bytes'],)*2)
    signal.alarm(contract['resource_limit']['seconds'])
    records=[];models={}
    flat=contract['families'][0]
    for n in contract['sizes']:
        train=[record('train',n,flat,i,contract) for i in range(contract['training_per_size'])]
        model=fit(train)
        calibration=[record('calibration',n,flat,i,contract) for i in range(contract['calibration_per_size'])]
        bank=dict(scores=[score(r['features'],model) for r in calibration],heights=[r['features']['H'] for r in calibration])
        models[str(n)]=dict(training=model,calibration=bank)
        records.extend(train+calibration)
        for family in contract['families']:
            target=[]
            for i in range(contract['test_per_cell']):
                r=record('test',n,family,i,contract)
                r['assessment']=assess(r['features'],model,bank)
                if 'flat_density_twin' in r:
                    twin_assessment=assess(r['flat_density_twin']['features'],model,bank)
                    require(twin_assessment==r['assessment'],'twin assessment mismatch')
                    r['flat_density_twin']['assessment']=twin_assessment
                    r['flat_density_twin']['identical_scores_and_decisions']=True
                target.append(r)
            records.extend(target)
            print(f'N={n} {family["id"]}: {len(target)} orders completed',flush=True)
    result=summarize(records,contract)
    result['geometry']=[oracle(f['h']) for f in contract['families'] if f['id'].startswith('de_sitter')]+[oracle(0.)]
    result['unique_orders']=len(records)
    result['conformal_twin_checks']=sum('flat_density_twin' in r for r in records)
    result['relation_error_checks']=sum(r.get('relation_error_control',{}).get('status')=='REJECTED_INVALID_RELATION' for r in records)
    result['external_replication']=False
    data=json.dumps(records,separators=(',',':'),allow_nan=False).encode()
    (output/'records.json.gz').write_bytes(gzip.compress(data,mtime=0))
    dump(output/'models.json',models);dump(output/'summary.json',result)
    dump(output/'resources.json',dict(elapsed_seconds=time.perf_counter()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                                     platform=sys.platform,scope='Observed run, not a controlled performance benchmark'))
    dump(output/'hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir())})
    signal.alarm(0)
    print(json.dumps(result['primary'],indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--source-commit',required=True)
    args=ap.parse_args();execute(args.output,args.source_commit)
