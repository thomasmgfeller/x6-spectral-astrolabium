"""Source-bound, resource-limited runner; no target generation in toy checks."""
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
SOURCES=['research/lorentz_relational_transfer/'+x for x in ['contract.json','produce.py','check.py','run.py']]+[
    f'research/{folder}/{name}.py' for folder in ['lorentz_observable_comparison','lorentz_residual_diagnosis','lorentz_n1_stress'] for name in ['produce','check']]
def require(ok,why):
    if not ok: raise ValueError(why)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,obj): path.write_text(json.dumps(obj,indent=2)+'\n')

def selftest():
    import produce,check
    graphs=[]; edges=[(i,j) for i in range(4) for j in range(i+1,4)]
    for bits in range(64):
        c=[[0]*4 for _ in range(4)]
        for bit,(i,j) in enumerate(edges): c[i][j]=(bits>>bit)&1
        c=check.old.closure(c); graphs.append((f'toy-{bits:02d}',c))
        timings={k:0.0 for k in ['H7','N1','Q1','D','M11']}
        check.match(produce.spectral.features(c,timings),check.old.compute(c),'toy spectral features')
        check.match(produce.structural(c),check.structural(c),'toy structural statistics')
        rev=[list(reversed(r)) for r in reversed(c)]
        require(produce.exact.iso(c,rev) and check.old.iso(c,rev),'toy relabelled isomorphism')
    check.match(produce.pair.pair_refine(graphs),check.pair.refine(graphs),'toy all-round agreement')
    arrays=[[[0,1,2],[1,0,0],[2,0,0]],[[0,1,2],[2,0,0],[1,0,0]]]
    actual,_=produce.pair.refine_step(arrays); wrong,_=produce.pair.refine_step(arrays,marginal=True)
    checked,_=check.pair.refine_step(arrays); check.match(actual,checked,'toy paired update')
    require(actual[0][0][0]!=actual[1][0][0] and wrong[0][0][0]==wrong[1][0][0],'joint versus marginal fault')
    for degree in [1,2]:
        for d in range(3): check.match(produce.regular('toy',2,d,degree),check.regular('toy',2,d,degree),'toy switches')
    for family,n in [('height2',4),('height3',3)]:
        for p in [2,4,6]:
            for d in range(3): check.match(produce.sampled('toy',family,n,p,d),check.sampled('toy',family,n,p,d),'toy hash/reachability replay')
    for name in ['closed-rook','closed-shrikhande']:
        check.match(produce.structured(name,1),check.structured(name,1),'toy structured generator')
    # Four-subset logic has empty domains at n<=4; the target reference is
    # checked by explicit incidences after freezing, never pre-evaluated here.
    star=[[0,0,0,1],[0,0,0,1],[0,0,0,1],[0,0,0,0]]
    check.match(produce.certificate(star),check.certificate(star),'toy certificate domain')
    records=[]
    for i,(_,c) in enumerate(graphs[:8]):
        f=produce.spectral.features(c,{k:0.0 for k in ['H7','D','M11','N1','Q1']}); f['R2']=[i]
        records.append({'id':str(i),'n':4,'family':'height2','relation_rows':produce.rows(c),'features':f})
    # Replace arbitrary toy R2 IDs with true joint histograms before accounting.
    t=produce.pair.pair_refine([(r['id'],produce.matrix(r['relation_rows'])) for r in records])
    for r,a in zip(records,t['rounds'][-1]['matrices']): r['features']['R2']=produce.pair.hist(a)
    ref=produce.reference(records,{}); check.match(ref,check.reference(records,{}),'toy full pair reference')
    methods=json.loads((HERE/'contract.json').read_text())['methods']
    check.match(produce.summary(records,ref,methods),check.summary(records,ref,methods),'toy pair accounting')
    return {'status':'PASS_TOY_ONLY','maximum_order_size':4,'upper_DAG_closures':64,'joint_marginal_fault_detected':True,'target_generation':False}

def freeze():
    result=selftest()
    save(HERE/'freeze.json',{'schema':'x6.relational-transfer-freeze/1','created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'BEFORE_TARGET_INPUT_GENERATION','sources':{p:sha(ROOT/p) for p in SOURCES},'toy_checks':result})

def source_check(commit):
    frozen=json.loads((HERE/'freeze.json').read_text())
    require(frozen['sources']=={p:sha(ROOT/p) for p in SOURCES},'source hash mismatch')
    for p in SOURCES+['research/lorentz_relational_transfer/freeze.json']:
        raw=subprocess.check_output(['git','show',commit+':'+p],cwd=ROOT)
        require(hashlib.sha256(raw).hexdigest()==sha(ROOT/p),'source commit mismatch: '+p)
    return json.loads((HERE/'contract.json').read_text())

def run(directory,commit):
    cfg=source_check(commit); require(not directory.exists(),'fresh output required')
    directory.parent.mkdir(parents=True,exist_ok=True); start=datetime.now(timezone.utc).isoformat(); seconds={}
    limits=cfg['resources']
    def bound():
        resource.setrlimit(resource.RLIMIT_AS,(limits['memory_bytes'],)*2)
        resource.setrlimit(resource.RLIMIT_CPU,(limits['phase_seconds'],limits['phase_seconds']+1))
    try:
        for phase in ['produce','check']:
            log=directory.parent/(directory.name+'-'+phase+'.log'); begin=time.perf_counter()
            with log.open('w') as out:
                subprocess.run([sys.executable,'-B','-O',str(HERE/(phase+'.py')),str(directory)],stdout=out,stderr=subprocess.STDOUT,
                    check=True,timeout=limits['phase_seconds'],preexec_fn=bound,env={**os.environ,'PYTHONHASHSEED':'0'})
            seconds[phase]=time.perf_counter()-begin; log.rename(directory/(phase+'.log'))
        files=sorted(p.name for p in directory.iterdir() if p.is_file())
        save(directory/'RESULTS.json',{'schema':'x6.relational-transfer-run/1','status':'PASS_EXACT_FIXED_TRANSFER','source_commit':commit,
            'freeze_sha256':sha(HERE/'freeze.json'),'started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),
            'seconds':seconds,'python':platform.python_version(),'platform':platform.platform(),
            'network_scope':'No computational network calls; OS network isolation is separately enforced by CI, not asserted locally.',
            'files':{name:sha(directory/name) for name in files}})
        print((directory/'RESULTS.json').read_text())
    except Exception as exc:
        directory.mkdir(parents=True,exist_ok=True)
        save(directory/'INCONCLUSIVE.json',{'status':'INCONCLUSIVE','started_utc':start,'error':str(exc)})
        raise

if __name__=='__main__':
    parser=argparse.ArgumentParser(); group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--selftest',action='store_true'); group.add_argument('--freeze',action='store_true'); group.add_argument('--run',type=Path)
    parser.add_argument('--source-ref'); args=parser.parse_args()
    if args.selftest: print(json.dumps(selftest(),indent=2))
    elif args.freeze: freeze()
    else:
        require(bool(args.source_ref),'--source-ref required'); run(args.run,args.source_ref)
