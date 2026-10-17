"""Worker for the frozen target cohort. Invoke through run.py for resource limits."""
import argparse
import hashlib
import json
import platform
import resource
import time
from pathlib import Path
import numpy as np
import scipy
from threadpoolctl import threadpool_limits, threadpool_info
from core import diamond_order, regional_diagnostics
from analyze import summarize

HERE = Path(__file__).resolve().parent


def write(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False)+'\n')


def draw(n, replicate, cfg):
    seed = cfg['sampling']['seed_base'] + 100*n + replicate
    points = np.random.default_rng(seed).uniform(-1, 1, (n, 2))
    order = diamond_order(points)
    region = np.flatnonzero(np.all(np.abs(points) < cfg['sampling']['inner_halfwidth'], axis=1))
    metadata = {'n':n, 'replicate':replicate, 'seed':seed, 'n_a':len(region),
                'points_sha256':hashlib.sha256(points.astype('<f8').tobytes()).hexdigest(),
                'order_sha256':hashlib.sha256(order.astype('u1').tobytes()).hexdigest(),
                'region_sha256':hashlib.sha256(region.astype('<i8').tobytes()).hexdigest()}
    return order, region, metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-ref', required=True)
    args = parser.parse_args()
    cfg = json.loads((HERE/'contract.json').read_text())
    records = []
    started = time.monotonic()
    with threadpool_limits(cfg['budget']['blas_threads']):
        with (args.output/'records.jsonl').open('x') as stream:
            for n in cfg['sampling']['sizes']:
                for replicate in range(cfg['sampling']['replicates_per_size']):
                    start = time.monotonic()
                    order, region, record = draw(n, replicate, cfg)
                    record['diagnostics'] = regional_diagnostics(order, region, cfg['regularization']['sensitivity_coefficients'])
                    record['elapsed_seconds'] = time.monotonic()-start
                    stream.write(json.dumps(record, sort_keys=True, allow_nan=False)+'\n')
                    stream.flush()
                    records.append(record)
                    print(json.dumps({'n':n, 'replicate':replicate, 'status':record['diagnostics']['cutoffs']['1.0']['double']['status'], 'elapsed_seconds':record['elapsed_seconds']}), flush=True)
        result = summarize(records, cfg)
        write(args.output/'summary.json', result)
        write(args.output/'environment.json', {
            'source_ref':args.source_ref, 'python':platform.python_version(), 'numpy':np.__version__, 'scipy':scipy.__version__,
            'platform':platform.platform(), 'threadpools':threadpool_info(), 'elapsed_seconds':time.monotonic()-started,
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            'scope':'local numerical reference; no experimental measurement or feature-utility comparison'})
    print(json.dumps({'status':result['status'], 'primary_fit':result['fits']['1.0']}), flush=True)


if __name__ == '__main__':
    main()
