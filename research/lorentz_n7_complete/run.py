"""Bounded exact experiment and artifact verification (standard library).

python run.py --freeze        # before the complete n=7 run
python run.py --run results   # fresh directory only
python run.py --verify results
"""
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
SOURCES=['contract.json','producer.py','independent.py','controls.py','run.py']


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
def load(path):
    import independent
    return independent.decode(path.read_text())
def freeze_check():
    frozen=load(HERE/'freeze.json')
    if frozen['sources']!={name:digest(HERE/name) for name in SOURCES}:raise ValueError('source freeze mismatch')
    return frozen


def child(phase,path):
    contract=load(HERE/'contract.json');limits=contract['resources']
    resource.setrlimit(resource.RLIMIT_AS,(limits['memory_bytes_per_phase'],)*2)
    budget=limits['producer_seconds' if phase=='produce' else 'independent_seconds']
    resource.setrlimit(resource.RLIMIT_CPU,(budget,budget+1))
    if phase=='produce':
        import producer
        save(path,producer.produce())
    else:
        import independent
        from controls import controls
        atlas=load(path/'atlas.json');report=independent.verify(atlas)
        save(path/'independent-results.json',report)
        save(path/'controls.json',controls(atlas,report))


def bounded(phase,path,log_path):
    contract=load(HERE/'contract.json')
    budget=contract['resources']['producer_seconds' if phase=='produce' else 'independent_seconds']
    started=time.monotonic()
    with log_path.open('w') as log:
        subprocess.run([sys.executable,'-u','-O',str(HERE/'run.py'),'--child',phase,str(path)],
                       check=True,timeout=budget,stdout=log,stderr=subprocess.STDOUT,
                       env={**os.environ,'PYTHONHASHSEED':'0'})
    return round(time.monotonic()-started,6)


def run(directory):
    freeze_check();directory.mkdir(parents=True,exist_ok=False)
    started=datetime.now(timezone.utc).isoformat()
    try:
        producer_seconds=bounded('produce',directory/'atlas.json',directory/'producer.log')
        independent_seconds=bounded('check',directory,directory/'independent.log')
        atlas=load(directory/'atlas.json');report=load(directory/'independent-results.json')
        save(directory/'counterexamples.json',atlas['primary_counterexamples'])
        files=['atlas.json','independent-results.json','counterexamples.json','controls.json','producer.log','independent.log']
        save(directory/'RESULTS.json',{
            'schema':'x6.lorentz-n7-results/1','status':'PASS_EXACT_COUNTERCHECK',
            'hypothesis_status':report['hypothesis_status'],
            'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),
            'runtime':{'python':platform.python_version(),'platform':platform.platform()},
            'seconds':{'producer':producer_seconds,'independent':independent_seconds},
            'freeze_sha256':digest(HERE/'freeze.json'),'files':{f:digest(directory/f) for f in files},
            'by_n':{n:{'orders':v['orders'],'classes':{k:x['classes'] for k,x in v['groups'].items()}} for n,v in atlas['by_n'].items()},
            'primary_counterexample_pairs':len(atlas['primary_counterexamples']),
            'checked_representatives':report['representatives_checked'],
            'checked_exact_polynomials':report['exact_polynomials_checked']})
        print((directory/'RESULTS.json').read_text())
    except Exception as exc:
        save(directory/'INCONCLUSIVE.json',{'status':'INCONCLUSIVE','error':str(exc),'started_utc':started})
        raise


def verify(directory):
    freeze_check();result=load(directory/'RESULTS.json')
    import independent
    from controls import controls
    independent.require(result['freeze_sha256']==digest(HERE/'freeze.json'),'freeze binding')
    for name,expected in result['files'].items():
        independent.require(digest(directory/name)==expected,'artifact hash '+name)
    atlas=load(directory/'atlas.json');report=independent.verify(atlas)
    independent.same(report,load(directory/'independent-results.json'),'saved countercheck report')
    independent.same(controls(atlas,report),load(directory/'controls.json'),'saved controls')
    independent.same(atlas['primary_counterexamples'],load(directory/'counterexamples.json'),'saved witnesses')
    expected={n:{'orders':v['orders'],'classes':{k:x['classes'] for k,x in v['groups'].items()}} for n,v in atlas['by_n'].items()}
    independent.same(result['by_n'],expected,'result summary')
    for key,value in [('status',report['status']),('hypothesis_status',report['hypothesis_status']),
                      ('primary_counterexample_pairs',report['primary_pairs_checked']),
                      ('checked_representatives',report['representatives_checked']),
                      ('checked_exact_polynomials',report['exact_polynomials_checked'])]:
        independent.same(result[key],value,'result '+key)
    print(json.dumps({'status':'PASS_REPRODUCED_EXACT_COUNTERCHECK','hypothesis_status':report['hypothesis_status']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--freeze',action='store_true');g.add_argument('--run',type=Path)
    g.add_argument('--verify',type=Path);g.add_argument('--child',nargs=2)
    args=parser.parse_args()
    if args.freeze:
        if (HERE/'freeze.json').exists():raise ValueError('freeze already exists; preserve it')
        save(HERE/'freeze.json',{'schema':'x6.lorentz-n7-freeze/1','created_utc':datetime.now(timezone.utc).isoformat(),
             'scope':'Workflow-local prospective freeze; no full n=7 computation yet; no external preregistration claim',
             'sources':{name:digest(HERE/name) for name in SOURCES}})
    elif args.child:child(args.child[0],Path(args.child[1]))
    elif args.run:run(args.run.resolve())
    else:verify(args.verify.resolve())
