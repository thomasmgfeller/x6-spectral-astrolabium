#!/usr/bin/env python3
"""One documented entry point for the frozen portable reference edition."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tools.reference_suite import decode,encode,read,safe_name,require,sha


def inventory():
    d=decode(read(ROOT/'RELEASE_BUNDLE.json'))
    require(d['schema']=='x6.reference-bundle/1','bundle schema')
    require(type(d['source_commit']) is str and len(d['source_commit'])==40,'source commit')
    files={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    require(files==set(d['files'])|{'RELEASE_BUNDLE.json'},'bundle file set')
    for n,h in d['files'].items():
        p=ROOT/safe_name(n)
        require(not any(x.is_symlink() for x in (p,*p.parents)) and sha(read(p))==h,'bundle file hash: '+n)
    return d


def reproduce(output):
    bundle=inventory();output.mkdir(parents=False,exist_ok=False)
    result={'schema':'x6.external-reproduction/1','release':bundle['release_tag'],'source_commit':bundle['source_commit'],
      'bundle_manifest_sha256':sha(read(ROOT/'RELEASE_BUNDLE.json')),
      'started_utc':datetime.now(timezone.utc).isoformat(),'runtime':{'python':platform.python_version(),'platform':platform.platform()},
      'person_level_independence':'NOT_ASSESSED','status':'RUNNING','steps':[],'deviations':[]}
    env={'PATH':os.environ.get('PATH',''),'LANG':'C.UTF-8','LC_ALL':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1'}
    def execute(name,args):
        proc=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,timeout=300)
        (output/(name+'.stdout.log')).write_bytes(proc.stdout);(output/(name+'.stderr.log')).write_bytes(proc.stderr)
        result['steps'].append({'name':name,'exit_code':proc.returncode})
        require(proc.returncode==0,'step failed: '+name)
    try:
        require(sys.version_info[:2]==(3,12),'Python 3.12 required for frozen reference')
        node=subprocess.run(['node','--version'],capture_output=True,text=True,env=env,timeout=5)
        result['runtime']['node']=node.stdout.strip();require(node.returncode==0 and node.stdout.startswith('v24.'),'Node 24 required')
        execute('finite-reference',[sys.executable,'-S','-B','x6.py','reference','qualify','--output',str(output/'reference')])
        expected=decode(read(ROOT/'docs/validation-v1/expected-reference.json'))
        for n,h in expected['reports_sha256'].items():
            actual=sha(read(output/'reference'/n))
            if actual!=h:result['deviations'].append({'file':n,'expected_sha256':h,'actual_sha256':actual})
        execute('guarded-runner',[sys.executable,'-S','-B','tests/rax-guarded/qualify.py','--output',str(output/'guarded')])
        execute('error-budget',[sys.executable,'-S','-B','tests/rax-guarded/check_budget.py','--qualification',str(output/'guarded/qualification.json')])
        execute('agent-preservation',[sys.executable,'-S','-B','tools/release/verify_archive.py'])
        require(not result['deviations'],'reference output differs; preserve both, do not replace expected values')
        result['status']='PASS_REFERENCE_REPRODUCTION'
    except (ValueError,OSError,KeyError,subprocess.SubprocessError) as exc:
        result['status']='FAIL';result['failure']=str(exc)
    result['finished_utc']=datetime.now(timezone.utc).isoformat()
    result['output_sha256']={str(p.relative_to(output)):sha(read(p)) for p in sorted(output.rglob('*')) if p.is_file()}
    (output/'REPRODUCTION.json').write_bytes(encode(result))
    print(json.dumps(result));return 0 if result['status']=='PASS_REFERENCE_REPRODUCTION' else 1


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    try:sys.exit(reproduce(a.output.resolve()))
    except (ValueError,OSError,KeyError) as exc:print(json.dumps({'status':'FAIL','failure':str(exc)}));sys.exit(1)
