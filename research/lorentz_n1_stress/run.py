"""Source-bound isolated finite experiment with fixed resource limits."""
import argparse
from datetime import datetime, timezone
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
SOURCES=['research/lorentz_n1_stress/'+f for f in ['contract.json','produce.py','check.py','run.py','PRE_RUN_DEVIATION.json']]+[
    'research/lorentz_observable_comparison/'+f for f in ['contract.json','produce.py','check.py']]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,obj):
    path.write_text(json.dumps(obj,indent=2)+'\n')


def freeze_check():
    f=json.loads((HERE/'freeze.json').read_text())
    require(f['sources']=={name:digest(ROOT/name) for name in SOURCES},'source freeze mismatch')
    publication=json.loads((HERE/'publication.json').read_text()); commit=publication['source_freeze_commit']
    for name in SOURCES+['research/lorentz_n1_stress/freeze.json']:
        raw=subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT)
        require(hashlib.sha256(raw).hexdigest()==digest(ROOT/name),'published source mismatch')
    base=json.loads((HERE/'contract.json').read_text())['base_commit']
    for name in SOURCES:
        if '/lorentz_observable_comparison/' in name:
            raw=subprocess.check_output(['git','show',base+':'+name],cwd=ROOT)
            require(hashlib.sha256(raw).hexdigest()==digest(ROOT/name),'historical definition changed')
    return commit


def child(name,directory):
    cfg=json.loads((HERE/'contract.json').read_text())['resources']
    resource.setrlimit(resource.RLIMIT_AS,(cfg['memory_bytes'],)*2)
    resource.setrlimit(resource.RLIMIT_CPU,(cfg['phase_seconds'],cfg['phase_seconds']+1))
    if name=='produce':
        import produce
        produce.run(directory)
    else:
        import check
        check.run(directory)


def phase(name,directory,log):
    cfg=json.loads((HERE/'contract.json').read_text())['resources']; started=time.perf_counter()
    with log.open('w') as output:
        subprocess.run([sys.executable,'-B','-O',str(HERE/'run.py'),'--child',name,str(directory)],
                       stdout=output,stderr=subprocess.STDOUT,timeout=cfg['phase_seconds'],check=True,
                       env={**os.environ,'PYTHONHASHSEED':'0'})
    return time.perf_counter()-started


def run(directory):
    commit=freeze_check(); require(not directory.exists(),'fresh output required')
    directory.parent.mkdir(parents=True,exist_ok=True); started=datetime.now(timezone.utc).isoformat()
    seconds={}
    try:
        for name in ['produce','check']:
            log=directory.parent/(directory.name+'-'+name+'.log')
            seconds[name]=phase(name,directory,log); log.rename(directory/(name+'.log'))
        files=['records.jsonl','draws.json','summary.json','timing.json','verification.json','produce.log','check.log']
        save(directory/'RESULTS.json',{'schema':'x6.n1-stress-run/1','status':'PASS_EXACT_STRESS_TEST_WITH_PRE_RUN_DEVIATION',
             'protocol_deviation':'Public pre-run publication blocked by automatic approval review; local commit and hash freeze precede target generation. See PRE_RUN_DEVIATION.json. No public preregistration claimed.',
             'source_freeze_commit':commit,'freeze_sha256':digest(HERE/'freeze.json'),
             'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),
             'python':platform.python_version(),'platform':platform.platform(),'seconds':seconds,
             'files':{f:digest(directory/f) for f in files}})
        print((directory/'RESULTS.json').read_text())
    except Exception as exc:
        directory.mkdir(parents=True,exist_ok=True)
        save(directory/'INCONCLUSIVE.json',{'status':'INCONCLUSIVE','started_utc':started,'error':str(exc)})
        raise


def selftest():
    import produce
    import check
    # Toy matrices only, at most six elements; no target generator or target seeds.
    toys=[[[0,1],[0,0]],[[0,1,1],[0,0,0],[0,0,0]],
          [[0,0,1,0],[0,0,0,1],[0,0,0,0],[0,0,0,0]]]
    for c in toys:
        timing={k:0.0 for k in ['H7','D','M11','N1','Q1']}
        require(produce.prior.features(c,timing)==check.prior.compute(c),'toy arithmetic')
        p=list(reversed(range(len(c)))); b=[[c[i][j] for j in p] for i in p]
        require(produce.iso(c,b),'toy directed isomorphism')
        check.prior.invariance(c)
    # Exhaust every 2x2 binary incidence matrix and compare independent exact solvers.
    mats=[]
    for bits in range(16):
        mats.append([[0,0]+[(bits>>(2*i+j))&1 for j in range(2)] for i in range(2)]+[[0]*4 for _ in range(2)])
    for a in mats:
        for b in mats:
            # Restrict to degree-positive layers, as required by stress family semantics.
            if all(sum(r[2:]) for r in a[:2]+b[:2]) and all(sum(c[i][j] for i in range(2)) for c in [a,b] for j in range(2,4)):
                require(produce.iso(a,b)==check.iso(a,b),'toy isomorphism disagreement')
    require(len(check.prior.negative_controls())==6,'predecessor rejection controls')
    print('PASS_TOY_ONLY_NO_TARGET_GENERATION')


if __name__=='__main__':
    p=argparse.ArgumentParser(); g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--freeze',action='store_true'); g.add_argument('--selftest',action='store_true')
    g.add_argument('--run',type=Path); g.add_argument('--child',nargs=2)
    a=p.parse_args()
    if a.freeze:
        save(HERE/'freeze.json',{'schema':'x6.n1-stress-freeze/1','created_utc':datetime.now(timezone.utc).isoformat(),
             'status':'FROZEN_BEFORE_TARGET_GENERATION','sources':{name:digest(ROOT/name) for name in SOURCES}})
    elif a.selftest:
        selftest()
    elif a.child:
        child(a.child[0],Path(a.child[1]))
    else:
        run(a.run)
