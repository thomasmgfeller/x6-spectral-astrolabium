"""Target execution; exact matching and numerical geometry outputs are separate."""
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations
import gzip
import hashlib
import json
from pathlib import Path
import resource
import time
import tracemalloc
from core import (Stream, decode, encode, from_joint, joint_matrix, layers, lift_witness,
                  match, require, sorted_columns, token, verify_relation)
import geometry
from selftest import counterexample

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def savez(path, value):
    path.write_bytes(gzip.compress((token(value)+'\n').encode(), mtime=0))


def readz(path):
    return json.loads(gzip.decompress(path.read_bytes()))


def matrix(record):
    return [[int(x) for x in row] for row in record['relation_rows']]


def matching(directory, cfg):
    started = time.perf_counter()
    tracemalloc.start()
    source = ROOT/'research/lorentz_relational_boundary/results'
    inputs = json.loads((source/'inputs.json').read_text())
    indexed = {r['id']: r['future'] for r in readz(source/'indexed.json.gz')}
    refs = readz(source/'reference.json.gz')
    require(len(inputs) == cfg['matching']['orders'], 'all old inputs')
    decoded = {}
    for r in inputs:
        b = layers(matrix(r))[2]
        rebuilt = decode(indexed[r['id']])
        require(Counter(zip(*b)) == Counter(zip(*rebuilt)), 'archived indexed reconstruction')
        decoded[r['id']] = rebuilt
    decoding_seconds = time.perf_counter()-started
    pairs, timings, copies = [], [], []
    budget = cfg['matching']['node_budget_per_comparison']
    for ref in refs:
        a, b = ref['ids']
        t = time.perf_counter()
        result = match(decoded[a], decoded[b], budget)
        elapsed = time.perf_counter()-t
        require(result['status'] != 'INCONCLUSIVE', 'matching budget exhaustion: '+a+' '+b)
        require((result['status'] == 'ISOMORPHIC') == ref['isomorphic'], 'archived pair disagreement')
        pairs.append(dict(ids=[a, b], **result))
        timings.append(dict(ids=[a, b], seconds=elapsed))
    require(len(pairs) == cfg['matching']['same_size_pairs'], 'all same-size pairs')
    for r in inputs:
        c = matrix(r)
        for repeat in range(cfg['matching']['relabelings_per_order']):
            permutation = Stream('relabel', cfg['matching']['seed'], r['id'], repeat).shuffle(range(len(c)))
            d = [[c[i][j] for j in permutation] for i in permutation]
            low, high, incidence = layers(d)
            enc = encode(incidence)
            result = match(decoded[r['id']], decode(enc), budget)
            require(result['status'] == 'ISOMORPHIC', 'renamed copy must match')
            p = lift_witness(c, d, result['witness'])
            copies.append(dict(id=r['id'], repeat=repeat, output_to_original=permutation,
                               source_to_target=p, nodes=result['nodes']))
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    cost = dict(elapsed_seconds=time.perf_counter()-started, decode_seconds=decoding_seconds,
                python_traced_peak_bytes=peak, process_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                pair_times=timings, warning='One traced run, including decoding/copy checks; no comparative speed benchmark. Linux ru_maxrss includes interpreter and imports.')
    controls = counterexample()
    save(directory/'three_layer.json', controls)
    savez(directory/'matching.json.gz', dict(pairs=pairs, renamed_copies=copies))
    save(directory/'matching_summary.json', dict(orders=len(inputs), pairs=len(pairs),
         nonisomorphic=sum(r['status'] == 'NONISOMORPHIC' for r in pairs),
         renamed_copies=len(copies), verified_full_relation_witnesses=len(copies),
         inconclusive=0, search_nodes=sum(r['nodes'] for r in pairs),
         max_pair_search_nodes=max(r['nodes'] for r in pairs),
         reference='All 7088 pair judgements from hash-bound PR39 exact reference reused; witnesses and search newly computed.',
         decoded_incidence_binary_entries=sum(len(b)*len(b[0]) for b in decoded.values()),
         indexed_json_bytes=sum(len((token(e)+'\n').encode()) for e in indexed.values())))
    save(directory/'matching_costs.json', cost)


def geometric(directory, cfg):
    started = time.perf_counter()
    records = []
    for n in cfg['geometry']['sizes']:
        for family in cfg['geometry']['families']:
            for split in ['train', 'test']:
                for draw in range(cfg['geometry'][split+'_per_cell']):
                    r = geometry.sample(family, n, split, draw)
                    r['features'] = geometry.features(matrix(r))
                    records.append(r)
            print(token(dict(produced=family, n=n)), flush=True)
    evaluation = geometry.evaluate(records, cfg['geometry'])
    savez(directory/'geometry_records.json.gz', records)
    savez(directory/'geometry_evaluation.json.gz', evaluation)
    save(directory/'geometry_summary.json', dict(orders=len(records),
         cells={n: {method: {k: v for k, v in cell.items() if k in ['confusion', 'balanced_accuracy']}
                    for method, cell in methods.items()} for n, methods in evaluation['cells'].items()},
         primary=evaluation['primary']))
    save(directory/'geometry_costs.json', dict(elapsed_seconds=time.perf_counter()-started,
         process_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         maximum_eigen_residual=max(r['features']['eigen_residual'] for r in records),
         warning='Single process wall time and Linux peak RSS; includes interpreter and NumPy/BLAS.'))


if __name__ == '__main__':
    import sys
    cfg = json.loads((HERE/'contract.json').read_text())
    directory = Path(sys.argv[2])
    (matching if sys.argv[1] == 'matching' else geometric)(directory, cfg)
