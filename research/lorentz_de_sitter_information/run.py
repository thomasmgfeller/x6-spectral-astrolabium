"""Run once only after public source freeze; deterministic fresh-seed holdout."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
from datetime import datetime, timezone
from pathlib import Path
import platform
import resource
import signal
import time
import numpy as np
import scipy
from core import (contract, sources, plan, dump, seed, geometry, chains,
                  count_check, relation_hash, summarize, digest)


def run(out, ref):
    started = datetime.now(timezone.utc).isoformat()
    tic = time.monotonic()
    source_hashes = sources(ref)
    out.mkdir(parents=True, exist_ok=False)
    p = plan()
    dump(out/'planning.json', p)
    if p['fresh_run_budget_gate']:
        counts = []
        for j, h in enumerate(contract()['h_grid']):
            cs, hashes = [], []
            for r in range(contract()['fresh_clouds_per_cell']):
                label = f'holdout/n128/h{j}/r{r}'
                rng = np.random.Generator(np.random.PCG64(seed(label)))
                x, _ = geometry.sample(rng, 128, {'h': h})
                c = geometry.relation(x)
                values = chains.chain_sums(c)
                if not np.array_equal(values, count_check(c)):
                    raise AssertionError('independent chain decomposition mismatch')
                cs.append(values)
                hashes.append(relation_hash(c))
            np.savez_compressed(out/f'cell-{j}.npz', counts=np.array(cs),
                                relation_sha256=np.array(hashes, dtype='S64'))
            counts.append(np.array(cs))
            print(f'completed h={h}: {len(cs)} clouds', flush=True)
        dump(out/'summary.json', summarize(counts, p))
    else:
        dump(out/'summary.json', {'status': 'BUDGET_GATE_FAILED_NO_FRESH_RUN',
                                 'curvature_interval_status': 'NOT_QUALIFIED'})
    dump(out/'execution.json', dict(started_utc=started, finished_utc=datetime.now(timezone.utc).isoformat(),
        source_ref=ref, source_sha256=source_hashes, python=platform.python_version(),
        numpy=np.__version__, scipy=scipy.__version__, seconds=time.monotonic()-tic,
        peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        seed_namespace=contract()['seed_namespace']))
    dump(out/'hashes.json', {p.name: digest(p) for p in sorted(out.iterdir())})


if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--source-ref', required=True)
    a.add_argument('--output', type=Path, required=True)
    args = a.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
    signal.alarm(600)
    run(args.output, args.source_ref)
