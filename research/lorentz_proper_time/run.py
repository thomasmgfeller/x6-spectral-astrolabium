"""Source-bound runner; original design remains an immutable historical record."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DESIGN='9684959af9700f0def30a16811498b49950ca406'
SOURCES=['research/lorentz_proper_time/'+name for name in
         ['contract.json','design_examples.json','check_design.py','proper_core.py','proper_common.py',
          'proper_analysis.py','produce.py','check.py','selftest.py','compare.py','run.py','requirements.txt','IMPLEMENTATION.md']]
SOURCES+=['research/lorentz_matching_geometry/core.py','.github/workflows/lorentz-proper-time-run.yml']


def require(ok,why):
    if not ok:
        raise ValueError(why)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n')


def source_check(ref):
    frozen=json.loads((HERE/'freeze.json').read_text())
    require(frozen['sources']=={p:sha(ROOT/p) for p in SOURCES},'frozen source changes')
    for path in SOURCES+['research/lorentz_proper_time/freeze.json']:
        data=subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)
        require(hashlib.sha256(data).hexdigest()==sha(ROOT/path),'source commit mismatch '+path)
    for name in ['contract.json','design_examples.json','check_design.py']:
        path='research/lorentz_proper_time/'+name
        data=subprocess.check_output(['git','show',DESIGN+':'+path],cwd=ROOT)
        require(hashlib.sha256(data).hexdigest()==sha(ROOT/path),'changed prospective design '+name)
    cfg=json.loads((HERE/'contract.json').read_text())
    old=cfg['sampling']['rng_source']
    require(sha(ROOT/old['path'])==old['sha256'],'changed prior stream')
    return cfg


def freeze():
    import selftest
    toys=selftest.run()
    require(not (HERE/'freeze.json').exists(),'never replace source freeze')
    save(HERE/'freeze.json',dict(schema='x6.proper-time-source-freeze/1',created_utc=datetime.now(timezone.utc).isoformat(),
        design_commit=DESIGN,status='BEFORE_TARGET_GENERATION',sources={p:sha(ROOT/p) for p in SOURCES},toys=toys))


def run(directory,ref):
    cfg=source_check(ref)
    require(not directory.exists(),'fresh output directory')
    directory.mkdir(parents=True)
    started=datetime.now(timezone.utc).isoformat(); times={}
    def bound():
        limit=cfg['resources']
        resource.setrlimit(resource.RLIMIT_AS,(limit['memory_bytes'],)*2)
        resource.setrlimit(resource.RLIMIT_CPU,(limit['phase_seconds'],limit['phase_seconds']+1))
    env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','PYTHONHASHSEED':'0'}
    try:
        for phase in ['produce','check']:
            begin=time.perf_counter()
            with (directory/(phase+'.log')).open('w') as log:
                subprocess.run([sys.executable,'-B','-O',str(HERE/(phase+'.py')),str(directory)],stdout=log,stderr=subprocess.STDOUT,
                               check=True,timeout=cfg['resources']['phase_seconds'],preexec_fn=bound,env=env)
            times[phase]=time.perf_counter()-begin
            print(phase+' completed',flush=True)
        import numpy
        save(directory/'RESULTS.json',dict(schema='x6.proper-time-run/1',status='PASS_COMPLETE_STUDY',source_commit=ref,
          design_commit=DESIGN,started_utc=started,completed_utc=datetime.now(timezone.utc).isoformat(),phase_seconds=times,
          python=platform.python_version(),numpy=numpy.__version__,platform=platform.platform(),
          network='No numerical network calls; OS network isolation enforced separately by CI.',
          sources=json.loads((HERE/'freeze.json').read_text())['sources'],files={p.name:sha(p) for p in sorted(directory.iterdir()) if p.is_file()}))
    except Exception as exc:
        save(directory/'INCONCLUSIVE.json',dict(status='INCONCLUSIVE',started_utc=started,error=str(exc),source_commit=ref))
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--selftest',action='store_true'); g.add_argument('--freeze',action='store_true'); g.add_argument('--run',type=Path)
    parser.add_argument('--source-ref')
    args=parser.parse_args()
    if args.selftest:
        import selftest
        print(json.dumps(selftest.run(),indent=2))
    elif args.freeze:
        freeze()
    else:
        require(args.source_ref is not None,'source-ref required')
        run(args.run,args.source_ref)
