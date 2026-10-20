"""New cloud search; weight seal precedes field evaluation. No overwrite/retries."""
import argparse
import hashlib
import json
import resource
import signal
import subprocess
import time
import numpy as np
import scipy
from mb_common import HERE, ROOT, contract, config, sources, encode, digest, write_json
from mb_model import prepare
from mb_fields import evaluate
from cg_cloud import run_cloud
from run_calibration import coordinates_only


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--shard',type=int,choices=[0,1],required=True)
    args = p.parse_args()
    cfg = contract()
    dest = HERE/f'test-{args.shard}'
    if dest.exists():
        raise SystemExit('Refusing to overwrite evidence')
    bound = sources()
    sha = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    for path, expected in bound.items():
        assert hashlib.sha256(subprocess.check_output(['git','show',sha+':'+path],cwd=ROOT)).hexdigest()==expected,path
    raw = (HERE/'frozen_model.json').read_bytes()
    frozen = json.loads(raw)
    assert frozen['status']=='FROZEN' and frozen['source_sha256']==bound
    assert subprocess.check_output(['git','show',sha+':'+str((HERE/'frozen_model.json').relative_to(ROOT))],cwd=ROOT)==raw
    seeds = list(range(cfg['test_seeds'][0],cfg['test_seeds'][1]+1))[args.shard::2]
    assert not (set(seeds)&set(frozen['training_seeds']+frozen['calibration_seeds']))
    jf, oc, guards, estimator_cfg = config()
    dest.mkdir()
    execution = dict(status='RUNNING',source_commit=sha,source_sha256=bound,
                     calibration_sha256=hashlib.sha256(raw).hexdigest(),shard=args.shard,
                     numpy=np.__version__,scipy=scipy.__version__,records=[])
    start = time.monotonic()
    def save():
        write_json(dest/'execution.json',execution)
    def timeout(*unused):
        raise TimeoutError('declared wall budget')
    save()
    signal.signal(signal.SIGALRM,timeout)
    signal.alarm(cfg['wall_budget_seconds_per_shard'])
    try:
        for seed in seeds:
            row = run_cloud(cfg['rho'],seed,jf,oc,guards,estimator_cfg)
            prepared = prepare(row['intrinsic'],frozen['models'])
            seal = hashlib.sha256(encode(prepared).encode()).hexdigest()
            z = coordinates_only(cfg['rho'],seed,oc)
            assert digest(z)==row['coordinates_sha256']
            row['metadata_inference'] = prepared
            row['inference_seal'] = seal
            row['evaluation'] = evaluate(prepared,row['selection']['selected'],z,seed,transfer=True)
            assert hashlib.sha256(encode(prepared).encode()).hexdigest()==seal
            name = f'seed-{seed}.json'
            data = encode(row).encode()
            (dest/name).write_bytes(data)
            execution['records'].append(dict(file=name,sha256=hashlib.sha256(data).hexdigest()))
            save()
            print(json.dumps(dict(seed=seed,status=row['evaluation']['status'],seconds=row['seconds'])),flush=True)
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024 > cfg['memory_budget_mib_per_shard']:
                raise MemoryError('declared memory budget')
        execution['status']='COMPLETE'
    except Exception as e:
        execution.update(status='HOLD',reason=repr(e))
        raise
    finally:
        signal.alarm(0)
        execution.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        save()


if __name__=='__main__':
    main()
