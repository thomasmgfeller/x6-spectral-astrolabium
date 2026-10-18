"""Frozen C2 confidence experiment; public source ref required before first run."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
from datetime import datetime, timezone
from fractions import Fraction as Q
from pathlib import Path
import platform
import resource
import signal
import time
import numpy as np
import scipy
from support import contract, dump, sources, seed, geometry, relation_hash, digest
from analysis import mathematics, planning, analyze_cell


def run(out, ref):
    start, tic = datetime.now(timezone.utc).isoformat(), time.monotonic()
    source_hashes = sources(ref)
    out.mkdir(parents=True, exist_ok=False)
    dump(out/'mathematics.json', mathematics())
    dump(out/'planning.json', planning())
    for j, value in enumerate(contract()['fresh_h']):
        counts, hashes = [], []
        for r in range(contract()['fresh_clouds_per_h']):
            rng = np.random.Generator(np.random.PCG64(seed(f'holdout/h{j}/r{r}')))
            x, _ = geometry.sample(rng, 128, {'h': float(Q(value))})
            c = geometry.relation(x)
            counts.append(int(c.sum()))
            hashes.append(relation_hash(c))
        counts = np.array(counts, dtype=np.int64)
        np.savez_compressed(out/f'raw-{j}.npz', c2=counts, relation_sha256=np.array(hashes, dtype='S64'))
        dump(out/f'groups-{j}.json.gz', analyze_cell(counts, Q(value)))
        print(f'completed h={value}: {len(counts)} fresh clouds', flush=True)
    dump(out/'execution.json', dict(started_utc=start, finished_utc=datetime.now(timezone.utc).isoformat(),
        source_ref=ref, source_sha256=source_hashes, python=platform.python_version(),
        numpy=np.__version__, scipy=scipy.__version__, seconds=time.monotonic()-tic,
        peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    dump(out/'hashes.json', {p.name: digest(p) for p in sorted(out.iterdir())})


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-ref', required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
    signal.alarm(600)
    run(args.output, args.source_ref)
