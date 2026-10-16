"""Fixed N1-equal stress family, exact full-relation deduplication."""
from collections import defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('prior_producer', HERE.parent/'lorentz_observable_comparison/produce.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
METHODS = ['N1', 'H7', 'Q1', 'H7+N1', 'N1+Q1', 'H7+N1+Q1']


def token(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'))


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2)+'\n')


def generate(cfg, m, draw):
    b = [[int((j-i) % m in (0, 1, 2)) for j in range(m)] for i in range(m)]
    accepted = 0
    for step in range(20*m*m):
        raw = hashlib.sha256(f'{cfg["seed"]}|{m}|{draw}|{step}'.encode()).digest()
        i, k, j, l = [int.from_bytes(raw[s:s+4], 'big') % m for s in (0, 4, 8, 12)]
        if i != k and j != l and b[i][j] and b[k][l] and not b[i][l] and not b[k][j]:
            b[i][j] = b[k][l] = 0
            b[i][l] = b[k][j] = 1
            accepted += 1
    c = [[0]*m+row for row in b]+[[0]*(2*m) for _ in range(m)]
    return c, accepted


def iso(a, b):
    """Backtrack exact directed relations, selecting fewest remaining options."""
    if len(a) != len(b):
        return False
    da, db = prior.degrees(a), prior.degrees(b)
    if sorted(da) != sorted(db):
        return False
    assigned = {}; used = set(); n = len(a)
    def visit():
        if len(assigned) == n:
            return True
        options = []
        for i in range(n):
            if i in assigned:
                continue
            choices = [j for j in range(n) if j not in used and da[i] == db[j] and
                       all(a[i][u] == b[j][v] and a[u][i] == b[v][j] for u, v in assigned.items())]
            if not choices:
                return False
            options.append((len(choices), i, choices))
        _, i, choices = min(options)
        for j in choices:
            assigned[i] = j; used.add(j)
            if visit():
                return True
            del assigned[i]; used.remove(j)
        return False
    return visit()


def prefilter(c):
    """Reject-only exact invariant; never used as an identity certificate."""
    m = len(c)//2; b = [row[m:] for row in c[:m]]
    def gram_profiles(x):
        return sorted(sorted(sum(u*v for u, v in zip(row, other)) for other in x) for row in x)
    return token([gram_profiles(b), gram_profiles(list(zip(*b)))])


def summarize(records):
    result = {}
    for m in sorted({r['m'] for r in records}):
        rr = [r for r in records if r['m'] == m]; table = {}
        for method in METHODS:
            groups = defaultdict(list)
            for r in rr:
                groups[token([r['features'][x] for x in method.split('+')])].append(r['id'])
            residual = sorted(sorted(g) for g in groups.values() if len(g) > 1)
            table[method] = {'classes': len(groups), 'unresolved_pairs': sum(len(g)*(len(g)-1)//2 for g in residual),
                             'max_class_size': max(map(len, groups.values())), 'residual_groups': residual}
        n1 = table['N1']['unresolved_pairs']; h7 = table['H7+N1']['unresolved_pairs']
        split = h7-table['H7+N1+Q1']['unresolved_pairs']
        witnesses = []
        for i, a in enumerate(rr):
            for b in rr[i+1:]:
                if a['features']['H7'] == b['features']['H7']:
                    witnesses.append({'ids': [a['id'], b['id']], 'q1_separated': a['features']['Q1'] != b['features']['Q1']})
        result[str(m)] = {'n': 2*m, 'representatives': len(rr), 'methods': table,
                         'n1_equal_pairs_split_by_q1': n1-table['N1+Q1']['unresolved_pairs'],
                         'h7_n1_equal_pairs_split_by_q1': split,
                         'incremental_gate': 'ADDITIONAL_SEPARATION_OBSERVED' if split else 'NO_OPPORTUNITY' if not h7 else 'NO_ADDITIONAL_SEPARATION',
                         'all_h7_equal_pairs': witnesses,
                         'costs': {method: {'polynomial_calls': sum(3 if method == 'H7' else 6*len(r['relation_rows']) if method == 'Q1' else 0 for r in rr),
                                           'integer_payload': sum(prior.integers(r['features'][method]) for r in rr)} for method in ['H7','N1','Q1']}}
    return {'schema': 'x6.n1-stress-summary/1', 'cells': result,
            'reference': 'Full relations and exact directed isomorphism; equality of fingerprints never proves identity.'}


def run(directory):
    directory.mkdir(parents=True, exist_ok=False)
    cfg = json.loads((HERE/'contract.json').read_text())['population']
    start = time.perf_counter(); records = []; draws = []; timings = {}; generation_seconds = 0.0
    for cell in cfg['cells']:
        m = cell['m']; buckets = defaultdict(list); selected = []
        begin = time.perf_counter()
        for draw in range(cell['draws']):
            c, accepted = generate(cfg, m, draw); key = prefilter(c)
            name = next((name for name, old in buckets[key] if iso(c, old)), None)
            if name is None:
                name = f'm{m}-r{draw:03d}'; buckets[key].append((name, c)); selected.append((name, c))
            draws.append({'m':m, 'draw':draw, 'accepted_switches':accepted, 'representative':name,
                          'relation_rows':[''.join(map(str,row)) for row in c]})
        generation_seconds += time.perf_counter()-begin
        timings[str(m)] = {k:0.0 for k in ['H7','D','M11','N1','Q1']}
        for index, (name, c) in enumerate(selected):
            f = prior.features(c, timings[str(m)])
            records.append({'id':name, 'm':m, 'relation_rows':[''.join(map(str,row)) for row in c],
                            'features':{k:f[k] for k in ['H7','N1','Q1']}})
            if index % 5 == 0:
                print(token({'phase':'produce','m':m,'completed':index+1,'total':len(selected)}), flush=True)
        (directory/'records.jsonl').write_text(''.join(token(r)+'\n' for r in records))
        save(directory/'draws.json', draws)
    save(directory/'summary.json', summarize(records))
    save(directory/'timing.json', {'generation_and_deduplication_seconds':generation_seconds,
                                  'kernel_seconds':timings, 'total_seconds':time.perf_counter()-start,
                                  'scope':'One serial execution, no general runtime comparison. Deduplication uses zero polynomials.'})
