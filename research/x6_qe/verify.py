#!/usr/bin/env python3
"""Qualified X6-QE finite references. No external services or result-side code."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import stat
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core
import independent

IDS = ('star-k1-6', 'cycle-4', 'rook-4x4', 'shrikhande')
SOURCES = ('core.py', 'independent.py', 'verify.py', 'inputs.json', 'contract.json')
LIMIT = 1024 * 1024
require = core.require


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False,
                       allow_nan=False) + '\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    def pairs(items):
        d = {}
        for k, v in items:
            require(k not in d, 'duplicate JSON key')
            d[k] = v
        return d
    def constant(x):
        raise ValueError('nonfinite JSON')
    return json.loads(data, object_pairs_hook=pairs, parse_constant=constant)


def read(path):
    path = Path(path)
    s = path.lstat()
    require(stat.S_ISREG(s.st_mode) and s.st_size <= LIMIT, 'bounded regular file required')
    data = path.read_bytes()
    require(len(data) <= LIMIT, 'file grew beyond bound')
    return data


def source_hashes():
    return {n: digest(read(HERE/n)) for n in SOURCES}


def inputs(doc):
    require(type(doc) is dict and set(doc) == {'schema', 'graphs'} and
            doc['schema'] == 'x6.qe.inputs/1', 'input schema')
    require(type(doc['graphs']) is list and len(doc['graphs']) == 4, 'graph coverage')
    require([g['id'] for g in doc['graphs']] == list(IDS), 'ordered graph IDs')
    return {g['id']: core.adjacency(g) for g in doc['graphs']}


def invariant_checks(a):
    n = len(a)
    orders = [list(reversed(range(n))), list(range(1, n))+[0],
              sorted(range(n), key=lambda x: digest(str(x).encode()))]
    chi, k4 = core.characteristic(a), len(core.k4_cliques(a))
    arcs, t = core.nonbacktracking(a)
    index = {arc: k for k, arc in enumerate(arcs)}
    for order in orders:
        b = core.relabel(a, order)
        require(core.characteristic(b) == chi and len(core.k4_cliques(b)) == k4,
                'relabeling invariant')
        new_arcs, new_t = core.nonbacktracking(b)
        perm = [index[(order[i], order[j])] for i, j in new_arcs]
        require(new_t == [[t[i][j] for j in perm] for i in perm], 'arc conjugacy')
    return len(orders)


def envelope(doc):
    require(type(doc) is dict and set(doc) == {'schema', 'status', 'source_files',
            'result', 'result_sha256', 'negative_controls'}, 'report fields')
    require(doc['schema'] == 'x6.qe.report/1' and doc['status'] == 'PASS_WITH_SCOPE_LIMITS',
            'report schema/status')
    require(doc['source_files'] == source_hashes(), 'source binding')
    require(doc['result_sha256'] == digest(encode(doc['result'])), 'result digest')


def check_report(raw, expected):
    doc = decode(raw)
    require(encode(doc) == raw, 'noncanonical JSON')
    envelope(doc)
    require(raw == encode(expected), 'full replay differs')


INPUT_ATTACKS = ('negative-index', 'boolean-index', 'float-index', 'out-of-range',
                 'self-loop', 'duplicate-edge', 'reversed-edge', 'unknown-graph-field',
                 'missing-graph', 'duplicate-graph-id')
REPORT_ATTACKS = ('wrong-spectrum', 'wrong-zeta', 'wrong-motif-count', 'missing-row',
                  'boolean-motif-count', 'invented-quantum-claim', 'missing-control',
                  'wrong-source', 'duplicate-key', 'nonfinite', 'truncated')


def rejected(action, label):
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError):
        return
    raise ValueError('negative control accepted: '+label)


def controls(original, expected):
    for name in INPUT_ATTACKS:
        bad = copy.deepcopy(original)
        graph = bad['graphs'][0]
        if name == 'negative-index': graph['edges'][0][0] = -1
        elif name == 'boolean-index': graph['edges'][0][0] = False
        elif name == 'float-index': graph['edges'][0][0] = 0.0
        elif name == 'out-of-range': graph['edges'][0][1] = graph['n']
        elif name == 'self-loop': graph['edges'][0][1] = 0
        elif name == 'duplicate-edge': graph['edges'].insert(1, graph['edges'][0][:])
        elif name == 'reversed-edge': graph['edges'][0].reverse()
        elif name == 'unknown-graph-field': graph['prime'] = True
        elif name == 'missing-graph': bad['graphs'].pop()
        elif name == 'duplicate-graph-id': bad['graphs'][1]['id'] = IDS[0]
        rejected(lambda: inputs(bad), name)
    for name in REPORT_ATTACKS:
        bad = copy.deepcopy(expected)
        rows = bad['result']['graphs']
        if name == 'wrong-spectrum': rows[2]['adjacency_characteristic'][-1] += 1
        elif name == 'wrong-zeta': rows[2]['ihara_reciprocal_ascending'][-1] += 1
        elif name == 'wrong-motif-count': rows[2]['k4_count'] = 0
        elif name == 'missing-row': rows.pop()
        elif name == 'boolean-motif-count': rows[0]['k4_count'] = False
        elif name == 'invented-quantum-claim': bad['result']['scope']['quantum_memory'] = 'CONFIRMED'
        elif name == 'missing-control': bad['negative_controls'].pop()
        elif name == 'wrong-source': bad['source_files']['core.py'] = '0'*64
        bad['result_sha256'] = digest(encode(bad['result']))
        if name in REPORT_ATTACKS[:7]:
            # Integrity passes; complete semantic replay must still reject.
            envelope(bad)
        raw = encode(bad)
        if name == 'duplicate-key': raw = b'{"status":"PASS_WITH_SCOPE_LIMITS",'+raw[1:]
        elif name == 'nonfinite': raw = b'{"bad":NaN}'
        elif name == 'truncated': raw = raw[:-5]
        rejected(lambda: check_report(raw, expected), name)


def evaluate():
    require(sys.version_info[:2] == (3, 12), 'Python 3.12 required')
    before = source_hashes()
    contract = decode(read(HERE/'contract.json'))
    require(contract['schema'] == 'x6.qe.contract/1' and contract['graph_ids'] == list(IDS),
            'contract identity')
    require(contract['inputs_sha256'] == digest(read(HERE/'inputs.json')), 'input binding')
    require(encode(contract['acceptance']) == encode({'graphs': 4, 'reference_cases': 3,
            'relabelings': 12, 'negative_controls': 21, 'numerical_tolerance': 0}),
            'acceptance contract')
    original = decode(read(HERE/'inputs.json')); graphs = inputs(original)
    rows = []
    for name, a in graphs.items():
        row = dict(id=name, **core.summarize(a))
        for key, value in contract['expected'][name].items():
            require(encode(row[key]) == encode(value), 'fixed expectation: '+name+'/'+key)
        row['independent'] = independent.certify(name, a, row)
        row['relabelings'] = invariant_checks(a)
        if name in IDS[:2]:
            counts = {str(k): independent.primitive_orbits(a, k) for k in range(1, 9)}
            wanted = {str(k): int(name == 'cycle-4' and k == 4)*2 for k in range(1, 9)}
            require(counts == wanted, 'primitive cycle convention')
            row['primitive_oriented_cycles_lengths_1_to_8'] = counts
        rows.append(row)
    require(rows[2]['adjacency_characteristic'] == rows[3]['adjacency_characteristic'],
            'cospectral pair')
    require(rows[2]['ihara_reciprocal_ascending'] == rows[3]['ihara_reciprocal_ascending'],
            'equal global Ihara zeta')
    result = {'reference_cases': 3, 'graphs': rows,
              'case_conclusions': {
                  'star': 'NO_NONTRIVIAL_IHARA_CYCLE_SIGNAL',
                  'cycle': 'PRIMITIVE_DOES_NOT_MEAN_PRIME_LENGTH',
                  'cospectral_pair': 'LOCAL_K4_SEPARATES_EQUAL_SPECTRUM_AND_GLOBAL_IHARA'},
              'scope': contract['scope'], 'independent_person_review': 'NOT_PERFORMED'}
    report = {'schema': 'x6.qe.report/1', 'status': 'PASS_WITH_SCOPE_LIMITS',
              'source_files': before, 'result': result, 'result_sha256': digest(encode(result)),
              'negative_controls': [{'id': x, 'rejected': True} for x in INPUT_ATTACKS+REPORT_ATTACKS]}
    controls(original, report)
    require(source_hashes() == before, 'sources changed during execution')
    envelope(report)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output', type=Path)
    g.add_argument('--verify-report', type=Path)
    args = p.parse_args()
    try:
        if args.output:
            require(not args.output.exists() and not args.output.is_symlink(), 'output must be new')
        report = evaluate()
        if args.verify_report:
            check_report(read(args.verify_report), report)
        else:
            with args.output.open('xb') as stream:
                stream.write(encode(report))
        print(json.dumps({'status': report['status'], 'reference_cases': 3, 'graphs': 4,
                          'relabelings': 12, 'negative_controls_rejected': len(report['negative_controls']),
                          'external_review': False, 'physical_validation': False}))
        return 0
    except (ValueError, OSError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
