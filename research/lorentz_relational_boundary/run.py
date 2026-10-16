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
SOURCES=['research/lorentz_relational_boundary/'+x for x in ['contract.json','produce.py','check.py','run.py']]+[
    f'research/{folder}/{name}.py' for folder in ['lorentz_observable_comparison','lorentz_residual_diagnosis','lorentz_n1_stress'] for name in ['produce','check']]
def require(ok,why):
    if not ok: raise ValueError(why)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,obj): path.write_text(json.dumps(obj,indent=2)+'\n')

def selftest():
    import produce,check
    for bits in range(512):
        b=[[(bits>>(3*i+j))&1 for j in range(3)] for i in range(3)]
        x,y=produce.encode(b),check.encode(b); check.match(x,y,'toy encoder')
        check.match(produce.decode(x),check.decode(y),'toy inverse')
        check.match(produce.reconstruct(b,x),check.reconstruct(b,y),'toy entire relation')
        check.match(produce.pooled(x),check.pooled(y),'toy histogram')
        # A declared cap can exceed the true maximum; supply every extra zero.
        counts=dict(x['counts']); loose={**x,'degree_cap':3,'counts':[[i,counts.get(i,0)] for i in range(8)]}
        check.match(produce.decode(loose),produce.decode(x),'non-tight degree cap')
        check.match(check.decode(loose),check.decode(y),'non-tight cap reference')
    graphs=[]; edges=[(i,j) for i in range(4) for j in range(i+1,4)]
    for bits in range(64):
        c=[[0]*4 for _ in range(4)]
        for bit,(i,j) in enumerate(edges): c[i][j]=(bits>>bit)&1
        graphs.append((f'toy-{bits:02d}',check.old.closure(c)))
    check.match(produce.pair.pair_refine(graphs),check.pair.refine(graphs),'toy R2 all rounds')
    arrays=[[[0,1,2],[1,0,0],[2,0,0]],[[0,1,2],[2,0,0],[1,0,0]]]
    actual,_=produce.pair.refine_step(arrays); wrong,_=produce.pair.refine_step(arrays,marginal=True)
    checked,_=check.pair.refine_step(arrays); check.match(actual,checked,'toy paired kernel')
    require(actual[0][0][0]!=actual[1][0][0] and wrong[0][0][0]==wrong[1][0][0],'paired information control')
    c=produce.cycle([3]); check.match(c,check.cycle([3]),'toy cycle recipe')
    timing={k:0.0 for k in ['H7','D','M11','N1','Q1']}; f=produce.old.features(c,timing)
    check.match(f,check.old.compute(c),'toy exact spectra')
    e=produce.encode([row[3:] for row in c[:3]]); f['Pall']=[3,3,produce.pooled(e),produce.pooled(e)]
    t=produce.pair.pair_refine([('a',c),('b',c)]); records=[]
    for name,colors in zip(['a','b'],t['rounds'][-1]['matrices']):
        records.append({'id':name,'family':'cycles','m':3,'relation_rows':produce.rows(c),'features':{**f,'R2':produce.pair.hist(colors)}})
    refs=produce.reference(records); check.match(refs,check.reference(records),'toy exact isomorphism')
    methods=json.loads((HERE/'contract.json').read_text())['pooled_features']['methods']
    check.match(produce.summary(records,refs,methods),check.summary(records,refs,methods),'toy reference accounting')
    return {'status':'PASS_TOY_ONLY','binary_3_by_3_matrices':512,'maximum_order_size':6,'upper_DAG_closures':64,'joint_marginal_fault_detected':True,'target_generation':False}

def freeze():
    result=selftest()
    save(HERE/'freeze.json',{'schema':'x6.relational-boundary-freeze/1','created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'BEFORE_NEW_TARGET_PROFILES_AND_CYCLE_GENERATION','sources':{p:sha(ROOT/p) for p in SOURCES},'toy_checks':result})

def source_check(commit):
    frozen=json.loads((HERE/'freeze.json').read_text())
    require(frozen['sources']=={p:sha(ROOT/p) for p in SOURCES},'source hash mismatch')
    for p in SOURCES+['research/lorentz_relational_boundary/freeze.json']:
        raw=subprocess.check_output(['git','show',commit+':'+p],cwd=ROOT)
        require(hashlib.sha256(raw).hexdigest()==sha(ROOT/p),'source commit mismatch: '+p)
    cfg=json.loads((HERE/'contract.json').read_text())
    require(all(sha(ROOT/p)==h for p,h in cfg['sources'].items()),'input source hash mismatch')
    return cfg

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
        save(directory/'RESULTS.json',{'schema':'x6.relational-boundary-run/1','status':'PASS_EXACT_BOUNDARY_STUDY','source_commit':commit,
            'input_sha256':cfg['sources'],
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
