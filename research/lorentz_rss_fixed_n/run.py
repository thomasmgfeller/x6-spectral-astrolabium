"""Run only after the immutable public source freeze; no adaptive stopping."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from datetime import datetime, timezone
import argparse
import hashlib
import json
from math import comb
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time
import numpy as np
import scipy
from core import chain_sums, flat_probability, taylor_sums
from quadrature import pair_probability, volume
from analysis import summarize

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'lorentz_curvature'))
from geometry import sample, relation, oracle, flat_points

FROZEN=['research/lorentz_rss_fixed_n/'+s for s in
        ['contract.json','core.py','quadrature.py','analysis.py','run.py','selftest.py','verify.py','DERIVATION.md','requirements.txt']]
FROZEN+=['research/lorentz_curvature/geometry.py']


def dump(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')


def seed_for(label,contract):
    return int.from_bytes(hashlib.sha256((contract['seed_namespace']+'/'+label).encode()).digest()[:16],'big')


def relation_hash(c):
    return hashlib.sha256(np.packbits(c.reshape(-1),bitorder='little').tobytes()).hexdigest()


def source_hashes(commit):
    hashes={}
    for name in FROZEN:
        actual=(ROOT/name).read_bytes()
        frozen=subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT)
        if actual!=frozen: raise ValueError('changed frozen source: '+name)
        hashes[name]=hashlib.sha256(actual).hexdigest()
    return hashes


def execute(output,source_commit):
    hashes=source_hashes(source_commit)
    contract=json.loads((HERE/'contract.json').read_text())
    output.mkdir(parents=True,exist_ok=False)
    dump(output/'provenance.json',dict(source_commit=source_commit,source_sha256=hashes,
         started_utc=datetime.now(timezone.utc).isoformat(),python=sys.version,numpy=np.__version__,scipy=scipy.__version__,
         scope='Public source commit precedes first target invocation; no independent preregistration or external replication'))
    start=time.perf_counter()
    resource.setrlimit(resource.RLIMIT_AS,(contract['resources']['address_space_bytes'],)*2)
    signal.alarm(contract['resources']['seconds'])
    n=contract['importance']['N']; hs=contract['importance']['h']; reps=contract['importance']['replicates']
    norm=np.array([comb(n,k) for k in [2,3,4]])
    p=np.array([flat_probability(4,k) for k in [2,3,4]])
    vols=np.array([volume(h) for h in hs])
    harray=np.array(hs)[:,None]
    theta=np.array([oracle(h)['R_tau_squared'] for h in hs])
    slopes=np.empty((reps,1+len(hs),3)); flats=np.empty((reps,3),dtype=np.int64)
    ihash=np.empty(reps,dtype='S64')
    for r in range(reps):
        rng=np.random.Generator(np.random.PCG64(seed_for(f'importance/{r:05}',contract)))
        x=flat_points(rng,n); x=x[np.argsort(x[:,0],kind='stable')]
        c=relation(x); ihash[r]=relation_hash(c)
        counts=chain_sums(c); flats[r]=counts
        times=x[:,0][None,:]
        weights=np.concatenate([(np.pi/24/vols[:,None])/(1-harray*times)**4,
                                (np.pi/24/vols[:,None])/(1+harray*times)**4])
        sums=chain_sums(c,weights)
        average=(sums[:len(hs)]+sums[len(hs):])/2
        slopes[r,0]=taylor_sums(c,x[:,0])/norm/(12*p)
        slopes[r,1:]=(average-counts)/norm/(theta[:,None]*p)
        if (r+1)%2048==0: print(f'importance: {r+1}/{reps}',flush=True)
    direct=[]; dhash=[]; geometry=[]
    for n in contract['direct']['sizes']:
        for h in contract['direct']['h']:
            rows=[]; rowhash=[]
            for r in range(contract['direct']['replicates_per_cell']):
                label=f'direct/N{n}/h{h:.2f}/{r:05}'
                rng=np.random.Generator(np.random.PCG64(seed_for(label,contract)))
                x,_=sample(rng,n,dict(h=h)); c=relation(x)
                rows.append(chain_sums(c)); rowhash.append(relation_hash(c))
            direct.append(rows); dhash.append(rowhash); geometry.append((n,h,oracle(h)))
            print(f'direct N={n}, h={h}: {len(rows)}',flush=True)
    quadrature=[]
    for h in sorted(set(contract['quadrature']['h']+contract['direct']['h'])):
        quadrature.append(dict(h=h,probabilities=[pair_probability(h,o) for o in contract['quadrature']['orders']],geometry=oracle(h)))
    data=dict(importance_slopes=slopes,importance_flat_counts=flats,importance_relation_sha256=ihash,
              direct_counts=np.array(direct,dtype=np.int64),direct_relation_sha256=np.array(dhash,dtype='S64'))
    np.savez_compressed(output/'raw.npz',**data)
    dump(output/'reference.json',dict(geometry=geometry,quadrature=quadrature))
    result=summarize(data,contract,geometry,quadrature)
    dump(output/'summary.json',result)
    dump(output/'resources.json',dict(elapsed_seconds=time.perf_counter()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                                      scope='Observed run, not a controlled performance benchmark'))
    dump(output/'hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir())})
    signal.alarm(0)
    print(result['primary_slope_status'],flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('output',type=Path);parser.add_argument('--source-commit',required=True)
    args=parser.parse_args();execute(args.output,args.source_commit)
