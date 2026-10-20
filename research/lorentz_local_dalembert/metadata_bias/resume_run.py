"""Explicit continuation only; immutable old evidence and frozen numerical sources."""
import argparse
import hashlib
import json
import os
import resource
import signal
import subprocess
import time
import zipfile
import numpy as np
import scipy
from mb_common import HERE, ROOT, contract, config, sources, encode, digest
from mb_model import prepare
from mb_fields import evaluate
from cg_cloud import run_cloud
from run_calibration import coordinates_only


def original_checkpoint():
    cp=json.loads((HERE/'checkpoint.json').read_text())
    archive=HERE/'interrupted_clouds.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==cp['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        for name,sha in cp['record_sha256'].items():
            assert hashlib.sha256(z.read(name)).hexdigest()==sha,name
    assert cp['missing_seeds']==list(range(70210027,70210032))
    return cp


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--shard',type=int,choices=[0,1],required=True)
    args=parser.parse_args(); cfg=contract(); cp=original_checkpoint()
    dest=HERE/f'continuation-{args.shard}'
    if dest.exists(): raise SystemExit('Refusing to overwrite continuation evidence')
    frozen_bytes=(HERE/'frozen_model.json').read_bytes(); frozen=json.loads(frozen_bytes)
    assert hashlib.sha256(frozen_bytes).hexdigest()==cp['calibration_sha256']
    bound=sources(); assert bound==frozen['source_sha256']==cp['source_sha256']
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    extra={str((HERE/n).relative_to(ROOT)):hashlib.sha256((HERE/n).read_bytes()).hexdigest()
           for n in ['resume_run.py','RESUMPTION.md']}
    for path,h in {**bound,**extra}.items():
        assert hashlib.sha256(subprocess.check_output(['git','show',sha+':'+path],cwd=ROOT)).hexdigest()==h,path
    seeds=[s for s in cp['missing_seeds'] if s%2==args.shard]
    jf,oc,guards,estimator_cfg=config(); dest.mkdir()
    start=time.monotonic()
    e=dict(status='RUNNING',shard=args.shard,source_commit=sha,original_freeze=cp['source_commit'],
           source_sha256=bound,continuation_source_sha256=extra,
           checkpoint_sha256=hashlib.sha256((HERE/'checkpoint.json').read_bytes()).hexdigest(),
           calibration_sha256=cp['calibration_sha256'],planned_seeds=seeds,
           numpy=np.__version__,scipy=scipy.__version__,records=[],current_seed=None)
    def save():
        e.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        tmp=dest/'execution.tmp'; tmp.write_text(json.dumps(e,indent=2)+'\n')
        os.replace(tmp,dest/'execution.json')
    def timeout(*unused): raise TimeoutError('declared continuation wall budget')
    signal.signal(signal.SIGALRM,timeout); signal.alarm(cfg['wall_budget_seconds_per_shard']); save()
    try:
        for seed in seeds:
            e['current_seed']=seed; save()
            row=run_cloud(cfg['rho'],seed,jf,oc,guards,estimator_cfg)
            prepared=prepare(row['intrinsic'],frozen['models'])
            seal=hashlib.sha256(encode(prepared).encode()).hexdigest()
            z=coordinates_only(cfg['rho'],seed,oc); assert digest(z)==row['coordinates_sha256']
            row['metadata_inference']=prepared; row['inference_seal']=seal
            row['evaluation']=evaluate(prepared,row['selection']['selected'],z,seed,transfer=True)
            assert hashlib.sha256(encode(prepared).encode()).hexdigest()==seal
            raw=encode(row).encode(); name=f'seed-{seed}.json'
            with (dest/name).open('xb') as f: f.write(raw)
            e['records'].append(dict(file=name,sha256=hashlib.sha256(raw).hexdigest()))
            e['current_seed']=None; save()
            print(json.dumps(dict(seed=seed,status=row['evaluation']['status'],seconds=row['seconds'])),flush=True)
            if e['peak_mib']>cfg['memory_budget_mib_per_shard']: raise MemoryError('declared memory budget')
        e['status']='COMPLETE'
    except Exception as err:
        e.update(status='HOLD',reason=repr(err)); raise
    finally:
        signal.alarm(0); save()


if __name__=='__main__': main()
