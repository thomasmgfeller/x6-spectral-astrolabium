"""Separate exact checker: determinants, closure, degree-class permutations.

No producer imports. Same authoring process; not external independent review.
"""
from collections import Counter, defaultdict
import copy
from fractions import Fraction
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
METHODS = ['H7', 'H7+D', 'H7+M11', 'H7+N1', 'H7+Q1', 'D', 'M11', 'N1', 'Q1']


def require(ok, why):
    if not ok:
        raise ValueError(why)


def match(a, b, why):
    require(a == b, why)


def rows(c):
    return [''.join(map(str, row)) for row in c]


def matrix(lines):
    n = len(lines)
    require(all(len(row) == n and set(row) <= {'0', '1'} for row in lines), 'matrix encoding')
    c = [[int(x) for x in row] for row in lines]
    require(all(not c[i][i] for i in range(n)), 'irreflexivity')
    for i in range(n):
        for j in range(n):
            for k in range(n):
                require(not(c[i][j] and c[j][k]) or c[i][k], 'transitivity')
    return c


def closure(c):
    result = copy.deepcopy(c); n = len(c)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                result[i][j] = int(result[i][j] or (result[i][k] and result[k][j]))
    return result


def extend(c, v, future):
    n = len(c); a = [row+[0] for row in c]+[[0]*(n+1)]
    if future:
        a[v][n] = 1
    else:
        a[n][v] = 1
    return closure(a)


def determinant(m):
    a = copy.deepcopy(m); previous = sign = 1; n = len(a)
    for k in range(n-1):
        if not a[k][k]:
            pivot = next((i for i in range(k+1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]; sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                x = a[i][j]*pivot-a[i][k]*a[k][j]
                require(x % previous == 0, 'nonexact determinant step'); a[i][j] = x//previous
        for i in range(k+1, n):
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


def polynomial(a):
    n = len(a); values = [determinant([[x*int(i == j)-a[i][j] for j in range(n)] for i in range(n)]) for x in range(n+1)]
    result = [Fraction(0)]*(n+1); basis = [Fraction(1)]
    for k in range(n+1):
        for j, b in enumerate(basis):
            result[j] += values[0]*b
        values = [v-u for u, v in zip(values, values[1:])]; nxt = [Fraction(0)]*(len(basis)+1)
        for j, b in enumerate(basis):
            nxt[j] -= k*b/(k+1); nxt[j+1] += b/(k+1)
        basis = nxt
    require(all(v.denominator == 1 for v in result), 'fractional coefficient')
    return list(map(int, reversed(result)))


def spectral(c):
    n = len(c)
    matrices = [[[c[i][j]+c[j][i] for j in range(n)] for i in range(n)],
                [[c[i][j]-c[j][i] for j in range(n)] for i in range(n)],
                [[2*sum(c[v][i]*c[v][j]-c[i][v]*c[j][v] for v in range(n)) for j in range(n)] for i in range(n)]]
    return [polynomial(a) for a in matrices]


def degree(c):
    return [(sum(c[j][i] for j in range(len(c))), sum(c[i])) for i in range(len(c))]


def small(c):
    n = len(c); dg = degree(c)
    D = sorted([a, b] for a, b in dg)
    m = sum(c[i][v]*c[j][v] for i, j in combinations(range(n), 2) for v in range(n) if dg[i] == dg[j] == (0, 1))
    neighbors = []
    for i in range(n):
        past = []; future = []
        for j in range(n):
            if c[j][i]:
                past.append(list(dg[j]))
            if c[i][j]:
                future.append(list(dg[j]))
        neighbors.append([list(dg[i]), sorted(past), sorted(future)])
    return {'D': D, 'M11': m, 'N1': sorted(neighbors)}


def compute(c):
    n = len(c); d = degree(c); f = small(c)
    f['H7'] = [n, spectral(c), sum(v[0] == 0 for v in d), sum(v[1] == 0 for v in d),
               sum(c[v][i]*c[v][j] for v in range(n) for i, j in combinations(range(n), 2)),
               sum(c[i][v]*c[j][v] for v in range(n) for i, j in combinations(range(n), 2))]
    f['Q1'] = sorted([[spectral(extend(c, v, True)), spectral(extend(c, v, False))] for v in range(n)])
    return f


def iso(a, b):
    if a == b:
        return True
    da, db = degree(a), degree(b)
    if sorted(da) != sorted(db):
        return False
    groups = [[i for i, v in enumerate(da) if v == d] for d in sorted(set(da))]
    target = [[i for i, v in enumerate(db) if v == da[g[0]]] for g in groups]
    assignment = {}
    def visit(k):
        if k == len(groups):
            return True
        for p in permutations(target[k]):
            assignment.update(zip(groups[k], p))
            if all(a[i][j] == b[u][v] for i, u in assignment.items() for j, v in assignment.items()) and visit(k+1):
                return True
            for i in groups[k]:
                del assignment[i]
        return False
    return visit(0)


def load_source(contract, path):
    raw = subprocess.check_output(['git', 'show', contract['base_commit']+':'+path], cwd=ROOT)
    require(hashlib.sha256(raw).hexdigest() == contract['source_sha256'][path], 'source binding')
    return json.loads(raw)


def check_inputs(contract, records, draws):
    census = load_source(contract, contract['population']['census']['source'])
    controls = load_source(contract, contract['population']['controls']['source'])
    lookup = {(r['panel'], r['id']): r for r in records}
    require(len(lookup) == len(records), 'duplicate id')
    expected = {( 'census', r['id']): r['relation_rows'] for r in census['records']}
    expected.update({('controls', k): v['relation_rows'] for k, v in controls['records'].items()})
    require({k for k in lookup if k[0] != 'challenge'} == set(expected), 'source population coverage')
    for key, row in expected.items():
        match(lookup[key]['relation_rows'], row, 'source matrix')
    cfg = contract['population']['challenge']; specs = [(n, p, r) for n in cfg['sizes'] for p in cfg['thresholds_out_of_8'] for r in range(cfg['draws_per_cell'])]
    require(len(draws) == len(specs) == cfg['draws_total'], 'draw count')
    encountered = set()
    for entry, (n, p, r) in zip(draws, specs):
        match([entry['n'], entry['threshold'], entry['draw']], [n, p, r], 'draw specification')
        c = [[0]*n for _ in range(n)]
        for i, j in combinations(range(n), 2):
            label = f'{cfg["seed"]}|{n}|{p}|{r}|{i}|{j}'
            c[i][j] = int(hashlib.sha256(label.encode('utf-8')).digest()[0] % 8 < p)
        c = closure(c); match(rows(c), entry['relation_rows'], 'draw replay')
        name = entry['representative']; require(('challenge', name) in lookup, 'missing representative')
        require(iso(c, matrix(lookup['challenge', name]['relation_rows'])), 'forged deduplication')
        if name not in encountered:
            match(name, 'sample-n%d-p%d-r%02d' % (n, p, r), 'first representative naming')
            match(lookup['challenge', name]['relation_rows'], rows(c), 'first representative bytes')
        encountered.add(name)
    require(encountered == {key[1] for key in lookup if key[0] == 'challenge'}, 'unused representative')
    # Census uniqueness was exhaustively proved in the pinned predecessor study.
    # Re-establish exact uniqueness for each new/control panel within degree buckets.
    for panel in ['challenge', 'controls']:
        buckets = defaultdict(list)
        for r in records:
            if r['panel'] == panel:
                c = matrix(r['relation_rows']); buckets[tuple(sorted(degree(c)))].append(c)
        require(all(not iso(a, b) for bucket in buckets.values() for a, b in combinations(bucket, 2)), 'duplicate isomorphism representative')
    return [p['ids'] for p in controls['pairs']]


def choose(f, method):
    return [f[k] for k in method.split('+')]


def key(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'))


def payload(x):
    pending = [x]; count = 0
    while pending:
        obj = pending.pop()
        if isinstance(obj, list):
            pending.extend(obj)
        else:
            require(type(obj) is int, 'noninteger feature'); count += 1
    return count


def summary(records, pairs):
    panels = {}; costs = {}
    for panel in ['census', 'controls', 'challenge']:
        selected = [r for r in records if r['panel'] == panel]; panels[panel] = {}
        for n in sorted(set(len(r['relation_rows']) for r in selected)):
            rr = [r for r in selected if len(r['relation_rows']) == n]; methods = {}
            for method in METHODS:
                values = [key(choose(r['features'], method)) for r in rr]; counts = Counter(values)
                residual = sorted(sorted(r['id'] for r, v in zip(rr, values) if v == g) for g, count in counts.items() if count > 1)
                methods[method] = {'classes': len(counts), 'unresolved_pairs': sum(v*(v-1)//2 for v in counts.values()), 'max_class_size': max(counts.values()), 'residual_groups': residual}
            panels[panel][str(n)] = {'orders': len(rr), 'methods': methods}
        costs[panel] = {method: {'polynomial_calls': (3*len(selected) if method == 'H7' else sum(6*len(r['relation_rows']) for r in selected) if method == 'Q1' else 0),
                                  'integer_payload': sum(payload(r['features'][method]) for r in selected)} for method in ['H7', 'D', 'M11', 'N1', 'Q1']}
    lookup = {r['id']: r['features'] for r in records if r['panel'] == 'controls'}
    controls = [{'ids': p, 'separated': {m: choose(lookup[p[0]], m) != choose(lookup[p[1]], m) for m in METHODS}} for p in pairs]
    rank = []
    for method in METHODS[1:5]:
        passed = all(entry['methods'][method]['unresolved_pairs'] == 0 for p in ['census', 'challenge'] for entry in panels[p].values())
        if passed and all(c['separated'][method] for c in controls):
            extra = method.split('+')[1]
            rank.append({'method': method, 'polynomial_calls': sum(c[extra]['polynomial_calls'] for c in costs.values()), 'integer_payload': sum(c[extra]['integer_payload'] for c in costs.values())})
    return {'schema': 'x6.observable-comparison-summary/1', 'status': 'REQUIRES_EXACT_COUNTERCHECK', 'panels': panels,
            'control_pairs': controls, 'incremental_costs': costs,
            'finite_gate_ranking': sorted(rank, key=lambda r: (r['polynomial_calls'], r['integer_payload'], r['method'])),
            'recommendation_scope': 'Bounded prefilter only; equal fingerprints always require full-relation isomorphism checks.'}


def invariance(c):
    n = len(c); p = list(reversed(range(n))); relabelled = [[c[i][j] for j in p] for i in p]
    match(small(c), small(relabelled), 'small feature relabelling')
    extended_p = p+[n]
    for new_v, old_v in enumerate(p):
        for future in [True, False]:
            old = extend(c, old_v, future)
            match(extend(relabelled, new_v, future), [[old[i][j] for j in extended_p] for i in extended_p], 'quill permutation transport')


def negative_controls():
    rejected = []
    def reject(name, fn):
        try:
            fn()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('bad data accepted: '+name)
    reject('missing_transitive_closure', lambda: matrix(['010', '001', '000']))
    c = matrix(['011', '000', '000']); expected = compute(c)
    bad = copy.deepcopy(expected); bad['Q1'].pop()
    reject('lost_deck_multiplicity', lambda: match(bad, expected, 'features differ'))
    bad = copy.deepcopy(expected); index = next(i for i, v in enumerate(bad['Q1']) if v[0] != v[1]); bad['Q1'][index].reverse(); bad['Q1'].sort()
    reject('reversed_direction_pair', lambda: match(bad, expected, 'features differ'))
    bad = copy.deepcopy(expected); bad['Q1'][0][0][0][-1] += 1
    reject('altered_polynomial', lambda: match(bad, expected, 'features differ'))
    reject('forged_deduplication', lambda: require(iso(matrix(['01', '00']), matrix(['00', '00'])), 'forged deduplication'))
    rr = [{'panel': p, 'id': x, 'relation_rows': ['011', '000', '000'], 'features': expected} for p in ['census', 'controls', 'challenge'] for x in ['a', 'b']]
    good = summary(rr, [['a', 'b']]); bad = copy.deepcopy(good); bad['panels']['census']['3']['methods']['H7']['residual_groups'] = []
    reject('omitted_collision_group', lambda: match(bad, good, 'summary differs'))
    return rejected


def run(directory):
    contract = json.loads((HERE/'contract.json').read_text())
    records = [json.loads(line) for line in (directory/'records.jsonl').read_text().splitlines()]
    draws = json.loads((directory/'draws.json').read_text()); pairs = check_inputs(contract, records, draws)
    polynomials = 0
    for index, r in enumerate(records):
        c = matrix(r['relation_rows']); match(r['features'], compute(c), 'feature mismatch '+r['id']); invariance(c)
        polynomials += 3+6*len(c)
        if index % 200 == 0:
            print(json.dumps({'phase': 'checker', 'completed': index+1, 'total': len(records)}), flush=True)
    expected = summary(records, pairs); match(json.loads((directory/'summary.json').read_text()), expected, 'partition/cost/ranking mismatch')
    result = {'schema': 'x6.observable-comparison-verification/1', 'status': 'PASS_EXACT_COUNTERCHECK',
              'records': len(records), 'exact_polynomials_checked': polynomials, 'relabelled_inputs_checked': len(records),
              'challenge_draws_checked': len(draws), 'negative_controls_rejected': negative_controls(),
              'scope': 'Independent algorithms in the same authoring process; finite corpus, biased challenge sample; no external human review.'}
    (directory/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)
