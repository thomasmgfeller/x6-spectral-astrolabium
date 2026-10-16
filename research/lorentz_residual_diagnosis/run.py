"""Bounded, source-bound runner. --selftest uses n<=4 toy inputs only."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import resource
import os
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCES=['research/lorentz_residual_diagnosis/'+x for x in ['contract.json','produce.py','check.py','run.py']]+[
    'research/lorentz_n1_stress/'+x for x in ['produce.py','check.py']]+[
    'research/lorentz_observable_comparison/'+x for x in ['produce.py','check.py']]


def require(ok,why):
    if not ok:
        raise ValueError(why)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,obj):
    path.write_text(json.dumps(obj,indent=2)+'\n')


def selftest():
    import produce,check
    graphs=[]
    edges=[(i,j) for i in range(4) for j in range(i+1,4)]
    for bits in range(64):
        c=[[0]*4 for _ in range(4)]
        for bit,(i,j) in enumerate(edges):
            c[i][j]=(bits>>bit)&1
        for w in range(4):
            for u in range(4):
                for v in range(4):
                    c[u][v]=int(c[u][v] or (c[u][w] and c[w][v]))
        graphs.append(('toy-%02d'%bits,c))
    joint=produce.pair_refine(graphs); reference=check.refine(graphs)
    check.match(joint,reference,'toy joint refinement disagreement')
    # Synthetic three-vertex color arrays test the actual update kernels;
    # these are colored-array controls, not additional causal-set target data.
    arrays=[[[0,1,2],[1,0,0],[2,0,0]],[[0,1,2],[2,0,0],[1,0,0]]]
    actual,_=produce.refine_step(arrays); wrong,_=produce.refine_step(arrays,marginal=True)
    checked,_=check.refine_step(arrays)
    check.match(actual,checked,'toy colored-array kernel disagreement')
    require(actual[0][0][0]!=actual[1][0][0] and wrong[0][0][0]==wrong[1][0][0],'joint/marginal information control')
    for bits in range(1,16):
        c=[[0,0]+[(bits>>(2*i+j))&1 for j in range(2)] for i in range(2)]+[[0]*4 for _ in range(2)]
        if all(sum(c[i]) for i in range(2)) and all(sum(c[i][j] for i in range(2)) for j in range(2,4)):
            expected=check.intersections(c)
            for key,k in [('I2',2),('I3',3)]:
                check.match(produce.intersections(c,k),expected[key],'toy intersections')
    # Explicit three-root example, still only four vertices.
    c=[[0,0,0,1],[0,0,0,1],[0,0,0,1],[0,0,0,0]]
    check.match(produce.intersections(c,3),[[[1,1,1,1]],[]],'known triple star')
    check.match(check.intersections(c)['I3'],[[[1,1,1,1]],[]],'known triple star reference')
    return {'status':'PASS_TOY_ONLY','n_max':4,'upper_dag_draws':64,'joint_colors_after_one_round':joint['rounds'][1]['colors'],
            'synthetic_color_control_vertices':3,'separated_marginal_fault_detected':True}


def freeze():
    save(HERE/'freeze.json',{'schema':'x6.residual-source-freeze/1','created_utc':datetime.now(timezone.utc).isoformat(),
        'status':'BEFORE_NEW_FEATURE_EVALUATION_ON_KNOWN_CORPUS','sources':{p:sha(ROOT/p) for p in SOURCES},'toy_checks':selftest()})


def source_check(commit):
    frozen=json.loads((HERE/'freeze.json').read_text()); cfg=json.loads((HERE/'contract.json').read_text())
    require(frozen['sources']=={p:sha(ROOT/p) for p in SOURCES},'source hash mismatch')
    for p in SOURCES+['research/lorentz_residual_diagnosis/freeze.json']:
        raw=subprocess.check_output(['git','show',commit+':'+p],cwd=ROOT)
        require(hashlib.sha256(raw).hexdigest()==sha(ROOT/p),'source commit mismatch: '+p)
    require(sha(ROOT/cfg['input']['records'])==cfg['input']['sha256'],'input corpus hash mismatch')
    return cfg


def run(directory,commit):
    cfg=source_check(commit); require(not directory.exists(),'fresh output required')
    directory.parent.mkdir(parents=True,exist_ok=True); start=datetime.now(timezone.utc).isoformat(); seconds={}
    limits=cfg['resources']
    def bound():
        resource.setrlimit(resource.RLIMIT_AS,(limits['memory_bytes'],)*2)
        resource.setrlimit(resource.RLIMIT_CPU,(limits['phase_seconds'],limits['phase_seconds']+1))
    try:
        for name in ['produce','check']:
            log=directory.parent/(directory.name+'-'+name+'.log'); begin=time.perf_counter()
            with log.open('w') as out:
                subprocess.run([sys.executable,'-B','-O',str(HERE/(name+'.py')),str(directory)],
                    stdout=out,stderr=subprocess.STDOUT,check=True,timeout=limits['phase_seconds'],preexec_fn=bound,
                    env={**os.environ,'PYTHONHASHSEED':'0'})
            seconds[name]=time.perf_counter()-begin; log.rename(directory/(name+'.log'))
        files=sorted(p.name for p in directory.iterdir() if p.is_file())
        save(directory/'RESULTS.json',{'schema':'x6.residual-run/1','status':'PASS_EXACT_DIAGNOSIS','source_commit':commit,
            'input_sha256':cfg['input']['sha256'],'freeze_sha256':sha(HERE/'freeze.json'),
            'started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),'seconds':seconds,
            'python':platform.python_version(),'platform':platform.platform(),
            'network_scope':'No network calls in computation. OS network isolation is separately enforced by the CI shell, not asserted by this runner.',
            'files':{name:sha(directory/name) for name in files}})
        print((directory/'RESULTS.json').read_text())
    except Exception as exc:
        directory.mkdir(parents=True,exist_ok=True)
        save(directory/'INCONCLUSIVE.json',{'status':'INCONCLUSIVE','started_utc':start,'error':str(exc)})
        raise


if __name__=='__main__':
    p=argparse.ArgumentParser(); g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--selftest',action='store_true');g.add_argument('--freeze',action='store_true');g.add_argument('--run',type=Path)
    p.add_argument('--source-ref');a=p.parse_args()
    if a.selftest: print(json.dumps(selftest(),indent=2))
    elif a.freeze: freeze()
    else:
        require(bool(a.source_ref),'--source-ref required');run(a.run,a.source_ref)
