"""Run only after the public freeze; fresh simulation conditional on budget gate."""
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
from support import contract, dump, sources, seed, geometry, relation_hash, digest
from analysis import planning, analyze


def run(out, ref):
    start, tic = datetime.now(timezone.utc).isoformat(), time.monotonic()
    source_hashes = sources(ref)
    out.mkdir(parents=True, exist_ok=False)
    design = planning()
    dump(out/'planning.json', design)
    print(design['primary_status'], flush=True)
    rows = []
    if design['fresh_run_gate']:
        for j, cell in enumerate(contract()['fresh_cells']):
            all_counts = []
            for begin in range(0, cell['clouds'], contract()['storage_block']):
                counts, hashes = [], []
                end = min(cell['clouds'], begin+contract()['storage_block'])
                for r in range(begin, end):
                    rng = np.random.Generator(np.random.PCG64(seed(f'holdout/h{j}/r{r}')))
                    x, _ = geometry.sample(rng, 128, {'h': float(Q(cell['h']))})
                    c = geometry.relation(x)
                    counts.append(int(c.sum()))
                    hashes.append(relation_hash(c))
                np.savez_compressed(out/f'raw-{j}-{begin}.npz', c2=np.array(counts, dtype=np.int64),
                                    relation_sha256=np.array(hashes, dtype='S64'))
                all_counts.extend(counts)
                print(f'h={cell["h"]}: {end}/{cell["clouds"]} clouds', flush=True)
            result = analyze(np.array(all_counts, dtype=np.int64), cell)
            dump(out/f'groups-{j}.json.gz', result)
            rows.extend(result['rows'])
    dump(out/'summary.json', dict(primary_status=design['primary_status'], rows=rows,
        fresh_clouds=sum(c['clouds'] for c in contract()['fresh_cells']) if design['fresh_run_gate'] else 0,
        scope='Known uniform de Sitter model, fixed budgets; no unknown-density or stopping guarantee'))
    dump(out/'execution.json', dict(started_utc=start, finished_utc=datetime.now(timezone.utc).isoformat(),
        source_ref=ref, source_sha256=source_hashes, python=platform.python_version(), numpy=np.__version__,
        seconds=time.monotonic()-tic, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    dump(out/'hashes.json', {p.name:digest(p) for p in sorted(out.iterdir())})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-ref', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
    signal.alarm(600)
    run(args.output, args.source_ref)
