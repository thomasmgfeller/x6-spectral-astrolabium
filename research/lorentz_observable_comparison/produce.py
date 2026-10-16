"""Fixed exact observable comparison; no external dependencies or network."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
METHODS = ['H7', 'H7+D', 'H7+M11', 'H7+N1', 'H7+Q1', 'D', 'M11', 'N1', 'Q1']


def require(ok, message):
    if not ok:
        raise ValueError(message)


def token(x):
    return json.dumps(x, separators=(',', ':'), sort_keys=True)


def mm(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def polynomial(a):
    n = len(a); b = [[int(i == j) for j in range(n)] for i in range(n)]; coeff = [1]
    for k in range(1, n+1):
        b = mm(a, b); tr = sum(b[i][i] for i in range(n))
        require(tr % k == 0, 'inexact recurrence'); coeff.append(-tr//k)
        for i in range(n):
            b[i][i] += coeff[-1]
    require(not any(map(any, b)), 'Cayley-Hamilton residual')
    return coeff


def spectra(c):
    n = len(c)
    s = [[c[i][j]+c[j][i] for j in range(n)] for i in range(n)]
    a = [[c[i][j]-c[j][i] for j in range(n)] for i in range(n)]
    sa, ass = mm(s, a), mm(a, s)
    k = [[sa[i][j]-ass[i][j] for j in range(n)] for i in range(n)]
    return [polynomial(m) for m in [s, a, k]]


def degrees(c):
    return [[sum(col), sum(row)] for col, row in zip(zip(*c), c)]


def isomorphic(a, b):
    da, db = degrees(a), degrees(b)
    if sorted(da) != sorted(db):
        return False
    options = {i: [j for j in range(len(b)) if da[i] == db[j]] for i in range(len(a))}
    order = sorted(options, key=lambda i: len(options[i])); assigned = {}; used = set()
    def visit(k):
        if k == len(a):
            return True
        i = order[k]
        for j in options[i]:
            if j in used or any(a[i][u] != b[j][v] or a[u][i] != b[v][j] for u, v in assigned.items()):
                continue
            assigned[i] = j; used.add(j)
            if visit(k+1):
                return True
            used.remove(j); del assigned[i]
        return False
    return visit(0)


def quill(c, v, future):
    n = len(c); result = [row+[0] for row in c]+[[0]*(n+1)]
    if future:
        for i in range(n):
            result[i][n] = int(i == v or c[i][v])
    else:
        for j in range(n):
            result[n][j] = int(j == v or c[v][j])
    return result


def features(c, timings):
    start = time.perf_counter(); n = len(c); d = degrees(c); e = sum(map(sum, c))
    h = [n, spectra(c), sum(x[0] == 0 for x in d), sum(x[1] == 0 for x in d),
         sum(x[1]*(x[1]-1)//2 for x in d), sum(x[0]*(x[0]-1)//2 for x in d)]
    timings['H7'] += time.perf_counter()-start
    start = time.perf_counter(); D = sorted(degrees(c)); timings['D'] += time.perf_counter()-start
    start = time.perf_counter(); unit = [i for i, x in enumerate(degrees(c)) if x == [0, 1]]
    motif = sum(sum(c[i][v]*c[j][v] for v in range(n)) for i in unit for j in unit if i < j)
    timings['M11'] += time.perf_counter()-start
    start = time.perf_counter(); dg = degrees(c)
    neighbor = sorted([[dg[v], sorted(dg[i] for i in range(n) if c[i][v]),
                       sorted(dg[j] for j in range(n) if c[v][j])] for v in range(n)])
    timings['N1'] += time.perf_counter()-start
    start = time.perf_counter()
    deck = sorted([[spectra(quill(c, v, True)), spectra(quill(c, v, False))] for v in range(n)])
    timings['Q1'] += time.perf_counter()-start
    return {'H7': h, 'D': D, 'M11': motif, 'N1': neighbor, 'Q1': deck}


def source(contract, path):
    raw = subprocess.check_output(['git', 'show', contract['base_commit']+':'+path], cwd=ROOT)
    require(hashlib.sha256(raw).hexdigest() == contract['source_sha256'][path], 'source hash')
    return json.loads(raw)


def panels(contract):
    atlas = source(contract, contract['population']['census']['source'])
    structural = source(contract, contract['population']['controls']['source'])
    census = [(r['id'], [[int(x) for x in row] for row in r['relation_rows']]) for r in atlas['records']]
    controls = [(name, [[int(x) for x in row] for row in r['relation_rows']]) for name, r in structural['records'].items()]
    sample = []; draws = []; cfg = contract['population']['challenge']; buckets = defaultdict(list)
    for n in cfg['sizes']:
        for threshold in cfg['thresholds_out_of_8']:
            for draw in range(cfg['draws_per_cell']):
                rows = [0]*n
                for i in range(n):
                    for j in range(i+1, n):
                        label = '|'.join(map(str, [cfg['seed'], n, threshold, draw, i, j]))
                        if hashlib.sha256(label.encode()).digest()[0] % 8 < threshold:
                            rows[i] |= 1 << j
                for i in reversed(range(n)):
                    for j in range(i+1, n):
                        if rows[i] >> j & 1:
                            rows[i] |= rows[j]
                c = [[(rows[i] >> j) & 1 for j in range(n)] for i in range(n)]
                key = token([n, sorted(degrees(c))]); name = None
                for other, a in buckets[key]:
                    if isomorphic(c, a):
                        name = other; break
                if name is None:
                    name = 'sample-n%d-p%d-r%02d' % (n, threshold, draw)
                    sample.append((name, c)); buckets[key].append((name, c))
                draws.append({'n': n, 'threshold': threshold, 'draw': draw, 'representative': name,
                              'relation_rows': [''.join(map(str, row)) for row in c]})
    return {'census': census, 'controls': controls, 'challenge': sample}, draws, [p['ids'] for p in structural['pairs']]


def value(f, method):
    return [f[x] for x in method.split('+')]


def integers(x):
    return 1 if type(x) is int else sum(integers(v) for v in x)


def summarize(records, control_pairs):
    summaries = {}; costs = {}
    for panel in ['census', 'controls', 'challenge']:
        rr = [r for r in records if r['panel'] == panel]; summaries[panel] = {}
        for n in sorted({len(r['relation_rows']) for r in rr}):
            subset = [r for r in rr if len(r['relation_rows']) == n]; table = {}
            for method in METHODS:
                groups = defaultdict(list)
                for r in subset:
                    groups[token(value(r['features'], method))].append(r['id'])
                residual = sorted(sorted(g) for g in groups.values() if len(g) > 1)
                table[method] = {'classes': len(groups), 'unresolved_pairs': sum(len(g)*(len(g)-1)//2 for g in residual),
                                 'max_class_size': max(map(len, groups.values())), 'residual_groups': residual}
            summaries[panel][str(n)] = {'orders': len(subset), 'methods': table}
        costs[panel] = {method: {'polynomial_calls': sum(3 if method == 'H7' else 6*len(r['relation_rows']) if method == 'Q1' else 0 for r in rr),
                                 'integer_payload': sum(integers(r['features'][method]) for r in rr)}
                        for method in ['H7', 'D', 'M11', 'N1', 'Q1']}
    lookup = {r['id']: r for r in records if r['panel'] == 'controls'}
    checks = [{'ids': ids, 'separated': {m: value(lookup[ids[0]]['features'], m) != value(lookup[ids[1]]['features'], m) for m in METHODS}}
              for ids in control_pairs]
    eligible = []
    for method in METHODS[1:5]:
        if all(v['methods'][method]['unresolved_pairs'] == 0 for name, panel in summaries.items() if name != 'controls' for v in panel.values()) and all(c['separated'][method] for c in checks):
            extra = method.split('+')[1]
            eligible.append({'method': method, 'polynomial_calls': sum(p[extra]['polynomial_calls'] for p in costs.values()),
                             'integer_payload': sum(p[extra]['integer_payload'] for p in costs.values())})
    eligible.sort(key=lambda x: (x['polynomial_calls'], x['integer_payload'], x['method']))
    return {'schema': 'x6.observable-comparison-summary/1', 'status': 'REQUIRES_EXACT_COUNTERCHECK',
            'panels': summaries, 'control_pairs': checks, 'incremental_costs': costs, 'finite_gate_ranking': eligible,
            'recommendation_scope': 'Bounded prefilter only; equal fingerprints always require full-relation isomorphism checks.'}


def run(directory):
    directory.mkdir(parents=True, exist_ok=False)
    contract = json.loads((HERE/'contract.json').read_text()); pp, draws, controls = panels(contract)
    records = []; timing = {}; started = time.perf_counter()
    with (directory/'records.jsonl').open('w') as out:
        for panel, entries in pp.items():
            timing[panel] = {k: 0.0 for k in ['H7', 'D', 'M11', 'N1', 'Q1']}
            for index, (name, c) in enumerate(entries):
                r = {'panel': panel, 'id': name, 'relation_rows': [''.join(map(str, row)) for row in c], 'features': features(c, timing[panel])}
                records.append(r); out.write(token(r)+'\n')
                if index % 200 == 0:
                    print(json.dumps({'phase': 'producer', 'panel': panel, 'completed': index+1, 'total': len(entries)}), flush=True)
    for name, data in [('draws.json', draws), ('summary.json', summarize(records, controls)), ('timing.json', {'kernel_seconds': timing, 'total_seconds': time.perf_counter()-started, 'scope': 'Single unoptimized serial run; not a general speed claim'})]:
        (directory/name).write_text(json.dumps(data, indent=2)+'\n')
